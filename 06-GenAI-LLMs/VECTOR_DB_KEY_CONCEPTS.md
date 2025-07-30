# Vector Database Key Concepts

## 1. Specialized Database for Embeddings
**What it is**: Database optimized for storing, indexing, and querying high-dimensional vector embeddings at scale.

**Core Features**:
- **Vector Storage**: Efficient storage of dense vectors
- **Similarity Search**: Find nearest neighbors quickly
- **Metadata Filtering**: Combine vector search with traditional filters
- **Scalability**: Handle billions of vectors
- **Real-time Updates**: Insert/update vectors dynamically

## 2. Vector Similarity Search
**Distance Metrics**:
```python
import numpy as np

# Cosine Similarity (most common)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Euclidean Distance
def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

# Dot Product
def dot_product(a, b):
    return np.dot(a, b)

# Manhattan Distance
def manhattan_distance(a, b):
    return np.sum(np.abs(a - b))
```

**Approximate Nearest Neighbor (ANN)**:
```yaml
# Why ANN?
- Exact search: O(n) time complexity
- ANN search: O(log n) with slight accuracy trade-off
- Essential for large-scale applications

# Common ANN Algorithms
HNSW: Hierarchical Navigable Small World
IVF: Inverted File Index
LSH: Locality Sensitive Hashing
```

## 3. Popular Vector Databases
**Pinecone (Managed)**:
```python
import pinecone

# Initialize
pinecone.init(api_key="your-api-key", environment="us-west1-gcp")

# Create index
pinecone.create_index("example-index", dimension=1536, metric="cosine")
index = pinecone.Index("example-index")

# Upsert vectors
index.upsert([
    ("id1", [0.1, 0.2, 0.3, ...], {"text": "sample document"}),
    ("id2", [0.4, 0.5, 0.6, ...], {"text": "another document"})
])

# Query
results = index.query(
    vector=[0.1, 0.2, 0.3, ...],
    top_k=5,
    include_metadata=True
)
```

**Chroma (Open Source)**:
```python
import chromadb

# Initialize client
client = chromadb.Client()
collection = client.create_collection("documents")

# Add documents
collection.add(
    embeddings=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
    documents=["Document 1", "Document 2"],
    metadatas=[{"source": "web"}, {"source": "pdf"}],
    ids=["id1", "id2"]
)

# Query
results = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3]],
    n_results=5,
    include=['documents', 'distances', 'metadatas']
)
```

**Weaviate (GraphQL)**:
```python
import weaviate

# Initialize client
client = weaviate.Client("http://localhost:8080")

# Create schema
schema = {
    "classes": [{
        "class": "Document",
        "vectorizer": "text2vec-openai",
        "properties": [
            {"name": "content", "dataType": ["text"]},
            {"name": "source", "dataType": ["string"]}
        ]
    }]
}
client.schema.create(schema)

# Add data
client.data_object.create({
    "content": "Sample document content",
    "source": "web"
}, "Document")

# Vector search
result = client.query.get("Document", ["content", "source"]) \
    .with_near_text({"concepts": ["search query"]}) \
    .with_limit(5) \
    .do()
```

## 4. Indexing Strategies
**HNSW (Hierarchical Navigable Small World)**:
```yaml
# Parameters
M: Maximum connections per node (16-64)
efConstruction: Size of candidate set during construction (200-800)
efSearch: Size of candidate set during search (100-500)

# Characteristics
- High recall and speed
- Memory intensive
- Good for high-dimensional data
```

**IVF (Inverted File)**:
```yaml
# Parameters
nlist: Number of clusters (sqrt(n) to 4*sqrt(n))
nprobe: Number of clusters to search (1-nlist)

# Characteristics
- Memory efficient
- Configurable speed/accuracy trade-off
- Good for large datasets
```

**Product Quantization (PQ)**:
```python
# Compress vectors to reduce memory
import faiss

# Create PQ index
dimension = 768
m = 8  # Number of subquantizers
bits = 8  # Bits per subquantizer

index = faiss.IndexPQ(dimension, m, bits)
index.train(training_vectors)
index.add(vectors)

# Search
distances, indices = index.search(query_vector, k=10)
```

## 5. Hybrid Search
**Vector + Keyword Search**:
```python
# Combine dense and sparse retrieval
def hybrid_search(query, vector_db, text_index, alpha=0.7):
    # Vector search
    vector_results = vector_db.search(
        query_embedding=embed(query),
        top_k=20
    )
    
    # Keyword search (BM25)
    keyword_results = text_index.search(
        query=query,
        top_k=20
    )
    
    # Combine scores
    combined_scores = {}
    for result in vector_results:
        combined_scores[result.id] = alpha * result.score
    
    for result in keyword_results:
        if result.id in combined_scores:
            combined_scores[result.id] += (1 - alpha) * result.score
        else:
            combined_scores[result.id] = (1 - alpha) * result.score
    
    # Return top results
    return sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:10]
```

**Metadata Filtering**:
```python
# Filter by metadata before vector search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={"source": {"$eq": "documentation"}},
    where_document={"$contains": "python"}
)

# Complex filters
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={
        "$and": [
            {"category": {"$eq": "technical"}},
            {"date": {"$gte": "2024-01-01"}},
            {"$or": [
                {"priority": {"$eq": "high"}},
                {"urgent": {"$eq": True}}
            ]}
        ]
    }
)
```

## 6. Performance Optimization
**Batch Operations**:
```python
# Batch insert for better performance
def batch_upsert(vectors, batch_size=100):
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(batch)
        
# Batch query
def batch_query(queries, batch_size=10):
    results = []
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        batch_results = index.query(batch, top_k=5)
        results.extend(batch_results)
    return results
```

**Index Tuning**:
```python
# FAISS index optimization
import faiss

# GPU acceleration
res = faiss.StandardGpuResources()
gpu_index = faiss.index_cpu_to_gpu(res, 0, cpu_index)

# Index with preprocessing
index = faiss.IndexFlatIP(dimension)
index = faiss.IndexPreTransform(
    faiss.PCAMatrix(dimension, 256),  # Dimensionality reduction
    index
)

# Composite index for large datasets
quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFPQ(quantizer, dimension, nlist=1000, m=8, bits=8)
```

## 7. Data Management
**Vector Lifecycle**:
```python
class VectorManager:
    def __init__(self, collection):
        self.collection = collection
    
    def add_document(self, doc_id, content, metadata):
        embedding = self.embed(content)
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )
    
    def update_document(self, doc_id, new_content, new_metadata):
        # Delete old version
        self.collection.delete(ids=[doc_id])
        
        # Add new version
        self.add_document(doc_id, new_content, new_metadata)
    
    def delete_document(self, doc_id):
        self.collection.delete(ids=[doc_id])
    
    def bulk_update(self, updates):
        # Batch delete
        ids_to_delete = [update['id'] for update in updates]
        self.collection.delete(ids=ids_to_delete)
        
        # Batch insert
        new_embeddings = [self.embed(update['content']) for update in updates]
        self.collection.add(
            ids=[update['id'] for update in updates],
            embeddings=new_embeddings,
            documents=[update['content'] for update in updates],
            metadatas=[update['metadata'] for update in updates]
        )
```

## 8. Monitoring and Observability
**Performance Metrics**:
```python
import time
import logging

class VectorDBMonitor:
    def __init__(self):
        self.metrics = {
            'query_latency': [],
            'query_count': 0,
            'index_size': 0,
            'memory_usage': 0
        }
    
    def track_query(self, query_func, *args, **kwargs):
        start_time = time.time()
        
        try:
            result = query_func(*args, **kwargs)
            latency = time.time() - start_time
            
            self.metrics['query_latency'].append(latency)
            self.metrics['query_count'] += 1
            
            # Log slow queries
            if latency > 1.0:
                logging.warning(f"Slow query detected: {latency:.2f}s")
            
            return result
            
        except Exception as e:
            logging.error(f"Query failed: {e}")
            raise
    
    def get_stats(self):
        if self.metrics['query_latency']:
            avg_latency = sum(self.metrics['query_latency']) / len(self.metrics['query_latency'])
            p95_latency = sorted(self.metrics['query_latency'])[int(0.95 * len(self.metrics['query_latency']))]
        else:
            avg_latency = p95_latency = 0
        
        return {
            'avg_query_latency': avg_latency,
            'p95_query_latency': p95_latency,
            'total_queries': self.metrics['query_count']
        }
```

## 9. Use Cases and Applications
**Semantic Search**:
```python
def semantic_search(query, documents_collection):
    # Embed query
    query_embedding = embed_text(query)
    
    # Search similar documents
    results = documents_collection.query(
        query_embeddings=[query_embedding],
        n_results=10,
        include=['documents', 'distances', 'metadatas']
    )
    
    return [
        {
            'document': doc,
            'similarity': 1 - distance,  # Convert distance to similarity
            'metadata': meta
        }
        for doc, distance, meta in zip(
            results['documents'][0],
            results['distances'][0], 
            results['metadatas'][0]
        )
    ]
```

**Recommendation System**:
```python
def recommend_items(user_id, user_embeddings, item_embeddings, top_k=10):
    # Get user embedding
    user_vector = user_embeddings.get(user_id)
    
    # Find similar items
    results = item_embeddings.query(
        query_embeddings=[user_vector],
        n_results=top_k,
        include=['metadatas', 'distances']
    )
    
    recommendations = []
    for metadata, distance in zip(results['metadatas'][0], results['distances'][0]):
        recommendations.append({
            'item_id': metadata['item_id'],
            'score': 1 - distance,
            'category': metadata['category']
        })
    
    return recommendations
```

**Anomaly Detection**:
```python
def detect_anomalies(new_vectors, normal_vectors_db, threshold=0.8):
    anomalies = []
    
    for i, vector in enumerate(new_vectors):
        # Find nearest neighbors in normal data
        results = normal_vectors_db.query(
            query_embeddings=[vector],
            n_results=5
        )
        
        # Check if closest match is below threshold
        closest_similarity = 1 - results['distances'][0][0]
        
        if closest_similarity < threshold:
            anomalies.append({
                'index': i,
                'vector': vector,
                'similarity_to_normal': closest_similarity
            })
    
    return anomalies
```

## 10. Best Practices
**Data Preparation**:
```python
# Normalize vectors for cosine similarity
def normalize_vectors(vectors):
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

# Handle missing embeddings
def safe_embed(text, embedding_model):
    try:
        if not text or len(text.strip()) == 0:
            return np.zeros(embedding_model.dimension)
        return embedding_model.encode(text)
    except Exception as e:
        logging.warning(f"Embedding failed for text: {text[:50]}... Error: {e}")
        return np.zeros(embedding_model.dimension)
```

**Index Management**:
```python
# Regular index maintenance
def maintain_index(collection):
    # Check index health
    stats = collection.get_stats()
    
    # Rebuild if fragmented
    if stats['fragmentation_ratio'] > 0.3:
        collection.rebuild_index()
    
    # Clean up deleted vectors
    if stats['deleted_count'] > 1000:
        collection.compact()
    
    # Update index parameters based on size
    if stats['vector_count'] > 1000000:
        collection.update_index_params({
            'nlist': int(np.sqrt(stats['vector_count'])),
            'nprobe': 128
        })
```

**Error Handling**:
```python
def robust_vector_search(query_embedding, collection, retries=3):
    for attempt in range(retries):
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=10
            )
            return results
            
        except Exception as e:
            if attempt == retries - 1:
                logging.error(f"Vector search failed after {retries} attempts: {e}")
                return {'documents': [[]], 'distances': [[]], 'metadatas': [[]]}
            
            time.sleep(2 ** attempt)  # Exponential backoff
            logging.warning(f"Vector search attempt {attempt + 1} failed: {e}")
```