# Vector Databases - Interview Questions

## Basic Questions

### 1. What is a vector database and how does it differ from traditional databases?
**Answer:** A vector database is specialized for storing, indexing, and querying high-dimensional vector embeddings. Key differences:
- **Data type**: Stores dense vectors vs structured data
- **Similarity search**: Finds similar vectors vs exact matches
- **Indexing**: Uses specialized algorithms (HNSW, IVF) vs B-trees
- **Queries**: Semantic similarity vs SQL queries
- **Use cases**: AI/ML applications vs traditional CRUD operations

### 2. What are the main use cases for vector databases?
**Answer:**
- **Semantic search**: Find similar documents/content
- **Recommendation systems**: Similar products/content
- **RAG systems**: Retrieve relevant context for LLMs
- **Image/video search**: Visual similarity matching
- **Anomaly detection**: Identify outliers in data
- **Chatbots**: Find relevant responses
- **Personalization**: User preference matching

### 3. What distance metrics are commonly used in vector databases?
**Answer:**
- **Cosine similarity**: Measures angle between vectors, good for normalized data
- **Euclidean distance**: Straight-line distance, sensitive to magnitude
- **Dot product**: Inner product, fast computation
- **Manhattan distance**: Sum of absolute differences
- **Hamming distance**: For binary vectors

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)
```

## Intermediate Questions

### 4. Compare different vector database solutions (Pinecone, Weaviate, Chroma, Qdrant).
**Answer:**
**Pinecone:**
- Fully managed cloud service
- Easy to use, good performance
- Expensive for large datasets
- Limited customization

**Weaviate:**
- Open-source with cloud options
- GraphQL API, rich filtering
- Built-in vectorization modules
- Good for complex queries

**Chroma:**
- Lightweight, embeddable
- Python-native, easy integration
- Good for prototyping
- Limited scalability

**Qdrant:**
- High performance, Rust-based
- Rich filtering capabilities
- Self-hosted or cloud
- Good for production workloads

### 5. How do you handle metadata filtering in vector databases?
**Answer:**
```python
# Example with Pinecone
import pinecone

# Initialize connection
pinecone.init(api_key="your-key", environment="your-env")
index = pinecone.Index("your-index")

# Query with metadata filtering
results = index.query(
    vector=[0.1, 0.2, 0.3, ...],  # Query vector
    top_k=10,
    filter={
        "category": {"$eq": "technology"},
        "date": {"$gte": "2023-01-01"},
        "price": {"$lt": 100}
    }
)

# Hybrid search: vector similarity + metadata filtering
results = index.query(
    vector=query_vector,
    top_k=50,  # Get more candidates
    filter=metadata_filter,
    include_metadata=True
)
```

**Best practices:**
- **Pre-filtering**: Apply metadata filters before vector search
- **Post-filtering**: Filter after vector search (less efficient)
- **Hybrid approach**: Combine both for optimal results
- **Index metadata**: Ensure metadata fields are indexed

### 6. What are the challenges with vector database performance and how do you optimize it?
**Answer:**
**Performance challenges:**
- **High dimensionality**: Curse of dimensionality
- **Index building time**: Large datasets take time to index
- **Memory usage**: Vectors consume significant memory
- **Query latency**: Real-time requirements
- **Accuracy vs speed**: Trade-off between precision and performance

**Optimization strategies:**
```python
# Dimensionality reduction
from sklearn.decomposition import PCA

def reduce_dimensions(vectors, target_dim=256):
    pca = PCA(n_components=target_dim)
    reduced_vectors = pca.fit_transform(vectors)
    return reduced_vectors, pca

# Quantization
def quantize_vectors(vectors, bits=8):
    min_val, max_val = vectors.min(), vectors.max()
    scale = (2**bits - 1) / (max_val - min_val)
    quantized = ((vectors - min_val) * scale).astype(np.uint8)
    return quantized, min_val, scale

# Batch operations
def batch_upsert(index, vectors, batch_size=100):
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        index.upsert(batch)
```

## Advanced Questions

### 7. How would you design a scalable vector database architecture?
**Answer:**
```python
# Distributed vector database design
class DistributedVectorDB:
    def __init__(self, num_shards=4):
        self.num_shards = num_shards
        self.shards = [VectorShard(i) for i in range(num_shards)]
        self.router = ConsistentHashRouter(num_shards)
    
    def insert(self, vector_id, vector, metadata=None):
        shard_id = self.router.get_shard(vector_id)
        return self.shards[shard_id].insert(vector_id, vector, metadata)
    
    def search(self, query_vector, top_k=10, filters=None):
        # Query all shards in parallel
        futures = []
        for shard in self.shards:
            future = shard.search_async(query_vector, top_k, filters)
            futures.append(future)
        
        # Merge results from all shards
        all_results = []
        for future in futures:
            results = future.get()
            all_results.extend(results)
        
        # Re-rank and return top-k
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results[:top_k]
```

**Architecture components:**
- **Sharding**: Distribute vectors across nodes
- **Replication**: Multiple copies for fault tolerance
- **Load balancing**: Distribute queries evenly
- **Caching**: Cache frequent queries
- **Monitoring**: Track performance metrics

### 8. How do you handle vector database updates and versioning?
**Answer:**
```python
class VersionedVectorDB:
    def __init__(self):
        self.current_version = 0
        self.versions = {}  # version -> index mapping
        self.pending_updates = []
    
    def update_vector(self, vector_id, new_vector, metadata=None):
        # Add to pending updates
        self.pending_updates.append({
            'id': vector_id,
            'vector': new_vector,
            'metadata': metadata,
            'operation': 'update'
        })
    
    def commit_updates(self):
        # Create new version
        new_version = self.current_version + 1
        
        # Apply updates to create new index
        new_index = self.create_new_version(self.pending_updates)
        self.versions[new_version] = new_index
        
        # Update current version
        self.current_version = new_version
        self.pending_updates = []
    
    def search_version(self, query_vector, version=None):
        if version is None:
            version = self.current_version
        
        index = self.versions[version]
        return index.search(query_vector)
```

**Update strategies:**
- **Immutable versions**: Create new versions for updates
- **In-place updates**: Modify existing index (faster but complex)
- **Batch updates**: Group updates for efficiency
- **Blue-green deployment**: Switch between versions
- **Rollback capability**: Revert to previous versions

### 9. How do you implement approximate nearest neighbor search?
**Answer:**
```python
# HNSW (Hierarchical Navigable Small World) implementation concept
class HNSW:
    def __init__(self, max_connections=16, ef_construction=200):
        self.max_connections = max_connections
        self.ef_construction = ef_construction
        self.levels = {}  # level -> {node_id: connections}
        self.vectors = {}  # node_id -> vector
    
    def insert(self, node_id, vector):
        # Determine level for new node
        level = self._get_random_level()
        
        # Insert at each level
        for lev in range(level + 1):
            if lev not in self.levels:
                self.levels[lev] = {}
            
            # Find closest nodes at this level
            candidates = self._search_layer(vector, lev, self.ef_construction)
            
            # Connect to closest nodes
            connections = self._select_neighbors(candidates, self.max_connections)
            self.levels[lev][node_id] = connections
            
            # Update reverse connections
            for neighbor in connections:
                if neighbor in self.levels[lev]:
                    self.levels[lev][neighbor].add(node_id)
        
        self.vectors[node_id] = vector
    
    def search(self, query_vector, k=10, ef=50):
        # Start from top level
        entry_points = self._get_entry_points()
        
        # Search through levels
        for level in reversed(range(len(self.levels))):
            entry_points = self._search_layer(
                query_vector, level, ef, entry_points
            )
        
        return entry_points[:k]
```

**ANN algorithms:**
- **HNSW**: Hierarchical navigable small world graphs
- **IVF**: Inverted file with clustering
- **LSH**: Locality-sensitive hashing
- **Product quantization**: Compress vectors for faster search

### 10. How do you monitor and troubleshoot vector database performance?
**Answer:**
```python
# Monitoring metrics
class VectorDBMonitor:
    def __init__(self):
        self.metrics = {
            'query_latency': [],
            'index_size': 0,
            'memory_usage': 0,
            'cache_hit_rate': 0,
            'error_rate': 0
        }
    
    def log_query(self, query_time, results_count, cache_hit=False):
        self.metrics['query_latency'].append(query_time)
        if cache_hit:
            self.metrics['cache_hits'] += 1
        self.metrics['total_queries'] += 1
    
    def get_performance_report(self):
        return {
            'avg_latency': np.mean(self.metrics['query_latency']),
            'p95_latency': np.percentile(self.metrics['query_latency'], 95),
            'cache_hit_rate': self.metrics['cache_hits'] / self.metrics['total_queries'],
            'memory_usage_gb': self.metrics['memory_usage'] / (1024**3)
        }
```

**Key metrics:**
- **Query latency**: Response time distribution
- **Throughput**: Queries per second
- **Recall**: Search accuracy
- **Memory usage**: RAM consumption
- **Index build time**: Time to create/update index
- **Cache hit rate**: Efficiency of caching

**Troubleshooting:**
- **Slow queries**: Check index parameters, dimensionality
- **High memory usage**: Consider quantization, compression
- **Low recall**: Adjust search parameters, index quality
- **Index corruption**: Backup and recovery procedures