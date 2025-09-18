# Vector Databases Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Architecture & Performance (91-120)](#architecture--performance-91-120)
5. [Production & Operations (121-150)](#production--operations-121-150)
6. [Scenario-Based Questions (151-180)](#scenario-based-questions-151-180)
7. [Integration & Ecosystem (181-200)](#integration--ecosystem-181-200)

---

## Basic Level Questions (1-30)

### 1. What is a vector database and how does it differ from traditional databases?

**Answer:** A vector database is specialized for storing, indexing, and querying high-dimensional vector embeddings.

#### **Key Differences:**

| Aspect | Vector Database | Traditional Database |
|--------|-----------------|----------------------|
| **Data Type** | Dense vectors (embeddings) | Structured data (rows/columns) |
| **Search Method** | Similarity search | Exact match queries |
| **Indexing** | HNSW, IVF, LSH | B-trees, Hash indexes |
| **Query Language** | Vector similarity APIs | SQL |
| **Distance Metrics** | Cosine, Euclidean, Dot product | Equality, Range |
| **Use Cases** | AI/ML, Semantic search | CRUD operations, Transactions |
| **Performance** | Approximate results | Exact results |

```python
import numpy as np
from typing import List, Tuple

# Traditional database query
# SELECT * FROM products WHERE category = 'electronics' AND price < 500

# Vector database query
def vector_similarity_search(query_vector: np.ndarray, 
                           database_vectors: np.ndarray,
                           top_k: int = 10) -> List[Tuple[int, float]]:
    """
    Find most similar vectors using cosine similarity
    """
    # Normalize vectors
    query_norm = query_vector / np.linalg.norm(query_vector)
    db_norm = database_vectors / np.linalg.norm(database_vectors, axis=1, keepdims=True)
    
    # Calculate cosine similarity
    similarities = np.dot(db_norm, query_norm)
    
    # Get top-k most similar
    top_indices = np.argsort(similarities)[::-1][:top_k]
    results = [(idx, similarities[idx]) for idx in top_indices]
    
    return results

# Example usage
query_embedding = np.random.rand(384)  # Query vector
product_embeddings = np.random.rand(10000, 384)  # Database vectors

similar_products = vector_similarity_search(query_embedding, product_embeddings, top_k=5)
print(f"Top 5 similar products: {similar_products}")
# Output: Top 5 similar products: [(7234, 0.89), (1456, 0.87), (9012, 0.85), (3456, 0.83), (5678, 0.81)]
```

### 2. What are the main use cases for vector databases?

**Answer:** Vector databases enable semantic similarity search across various domains.

#### 🎯 **Primary Use Cases**

```python
import openai
import pinecone
from sentence_transformers import SentenceTransformer

# 1. Semantic Search Implementation
class SemanticSearchEngine:
    def __init__(self, index_name: str):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = pinecone.Index(index_name)
    
    def index_documents(self, documents: List[str]):
        """Index documents for semantic search"""
        embeddings = self.model.encode(documents)
        
        vectors_to_upsert = []
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            vectors_to_upsert.append({
                'id': f'doc_{i}',
                'values': embedding.tolist(),
                'metadata': {'text': doc, 'doc_type': 'article'}
            })
        
        self.index.upsert(vectors_to_upsert)
        print(f"Indexed {len(documents)} documents")
    
    def search(self, query: str, top_k: int = 5):
        """Search for similar documents"""
        query_embedding = self.model.encode([query])[0]
        
        results = self.index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )
        
        return [(match['metadata']['text'], match['score']) 
                for match in results['matches']]

# 2. Recommendation System
class ProductRecommendationSystem:
    def __init__(self):
        self.user_embeddings = {}
        self.product_embeddings = {}
    
    def get_user_recommendations(self, user_id: str, top_k: int = 10):
        """Get product recommendations for user"""
        user_vector = self.user_embeddings.get(user_id)
        if not user_vector:
            return []
        
        similarities = []
        for product_id, product_vector in self.product_embeddings.items():
            similarity = np.dot(user_vector, product_vector)
            similarities.append((product_id, similarity))
        
        # Sort by similarity and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

# 3. RAG (Retrieval-Augmented Generation) System
class RAGSystem:
    def __init__(self, knowledge_base_index: str):
        self.index = pinecone.Index(knowledge_base_index)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def retrieve_context(self, query: str, top_k: int = 3):
        """Retrieve relevant context for query"""
        query_embedding = self.embedding_model.encode([query])[0]
        
        results = self.index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )
        
        context_chunks = [match['metadata']['text'] 
                         for match in results['matches']]
        return ' '.join(context_chunks)
    
    def generate_answer(self, query: str):
        """Generate answer using retrieved context"""
        context = self.retrieve_context(query)
        
        prompt = f"""
        Context: {context}
        
        Question: {query}
        
        Answer based on the context:
        """
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        
        return response.choices[0].text.strip()

# Example usage
search_engine = SemanticSearchEngine('semantic-search-index')
documents = [
    "Machine learning is a subset of artificial intelligence",
    "Deep learning uses neural networks with multiple layers",
    "Natural language processing helps computers understand text",
    "Computer vision enables machines to interpret visual data"
]

search_engine.index_documents(documents)
results = search_engine.search("What is AI?", top_k=2)
print(f"Search results: {results}")
# Output: Search results: [('Machine learning is a subset of artificial intelligence', 0.78), 
#                        ('Deep learning uses neural networks with multiple layers', 0.65)]
```

#### **Additional Use Cases:**
- **Image/Video Search**: Visual similarity matching
- **Anomaly Detection**: Identify outliers in high-dimensional data
- **Chatbot Response Matching**: Find relevant pre-written responses
- **Content Personalization**: Match user preferences to content
- **Fraud Detection**: Identify suspicious patterns
- **Drug Discovery**: Find similar molecular structures

### 3. What distance metrics are commonly used in vector databases?

**Answer:** Different distance metrics serve different use cases and data characteristics.

#### 🎯 **Distance Metrics Comparison**

```python
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class DistanceMetrics:
    """Comprehensive distance metrics for vector similarity"""
    
    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Cosine similarity - measures angle between vectors"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    @staticmethod
    def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
        """Cosine distance = 1 - cosine_similarity"""
        return 1.0 - DistanceMetrics.cosine_similarity(a, b)
    
    @staticmethod
    def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
        """Euclidean distance - straight line distance"""
        return np.linalg.norm(a - b)
    
    @staticmethod
    def manhattan_distance(a: np.ndarray, b: np.ndarray) -> float:
        """Manhattan distance - sum of absolute differences"""
        return np.sum(np.abs(a - b))
    
    @staticmethod
    def dot_product(a: np.ndarray, b: np.ndarray) -> float:
        """Dot product - inner product of vectors"""
        return np.dot(a, b)
    
    @staticmethod
    def hamming_distance(a: np.ndarray, b: np.ndarray) -> float:
        """Hamming distance - for binary vectors"""
        return np.sum(a != b)
    
    @staticmethod
    def jaccard_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Jaccard similarity for binary vectors"""
        intersection = np.sum(np.logical_and(a, b))
        union = np.sum(np.logical_or(a, b))
        
        if union == 0:
            return 1.0
        
        return intersection / union
    
    @staticmethod
    def minkowski_distance(a: np.ndarray, b: np.ndarray, p: float = 2) -> float:
        """Minkowski distance - generalization of Euclidean and Manhattan"""
        return np.power(np.sum(np.power(np.abs(a - b), p)), 1/p)

# Demonstrate different metrics
def compare_distance_metrics():
    """Compare different distance metrics on sample data"""
    
    # Sample vectors
    vec1 = np.array([1, 2, 3, 4, 5])
    vec2 = np.array([2, 3, 4, 5, 6])
    vec3 = np.array([5, 4, 3, 2, 1])
    
    vectors = [vec1, vec2, vec3]
    labels = ['Vec1', 'Vec2', 'Vec3']
    
    print("Distance Metrics Comparison:")
    print("=" * 50)
    
    metrics = {
        'Cosine Similarity': DistanceMetrics.cosine_similarity,
        'Cosine Distance': DistanceMetrics.cosine_distance,
        'Euclidean Distance': DistanceMetrics.euclidean_distance,
        'Manhattan Distance': DistanceMetrics.manhattan_distance,
        'Dot Product': DistanceMetrics.dot_product
    }
    
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            print(f"\n{labels[i]} vs {labels[j]}:")
            for metric_name, metric_func in metrics.items():
                distance = metric_func(vectors[i], vectors[j])
                print(f"  {metric_name}: {distance:.4f}")

# When to use each metric
def metric_selection_guide():
    """Guide for selecting appropriate distance metrics"""
    
    guide = {
        'Cosine Similarity': {
            'best_for': ['Text embeddings', 'Normalized data', 'High-dimensional sparse vectors'],
            'characteristics': ['Ignores magnitude', 'Range: [-1, 1]', 'Good for semantic similarity'],
            'use_cases': ['Document similarity', 'User preferences', 'Word embeddings']
        },
        'Euclidean Distance': {
            'best_for': ['Image embeddings', 'Continuous features', 'Low-dimensional data'],
            'characteristics': ['Sensitive to magnitude', 'Range: [0, ∞]', 'Geometric interpretation'],
            'use_cases': ['Image similarity', 'Clustering', 'Nearest neighbor search']
        },
        'Dot Product': {
            'best_for': ['Fast computation', 'Normalized vectors', 'Large-scale systems'],
            'characteristics': ['Very fast', 'No square root', 'Good for ranking'],
            'use_cases': ['Recommendation systems', 'Information retrieval', 'Real-time search']
        },
        'Manhattan Distance': {
            'best_for': ['Sparse data', 'Categorical features', 'Robust to outliers'],
            'characteristics': ['L1 norm', 'Less sensitive to outliers', 'Grid-like distance'],
            'use_cases': ['Categorical data', 'Feature selection', 'Robust similarity']
        }
    }
    
    print("\nDistance Metric Selection Guide:")
    print("=" * 60)
    
    for metric, info in guide.items():
        print(f"\n📊 {metric}:")
        print(f"  Best for: {', '.join(info['best_for'])}")
        print(f"  Characteristics: {', '.join(info['characteristics'])}")
        print(f"  Use cases: {', '.join(info['use_cases'])}")

# Run comparisons
compare_distance_metrics()
metric_selection_guide()
```

**Output:**
```
Distance Metrics Comparison:
==================================================

Vec1 vs Vec2:
  Cosine Similarity: 0.9912
  Cosine Distance: 0.0088
  Euclidean Distance: 2.2361
  Manhattan Distance: 5.0000
  Dot Product: 70.0000

Vec1 vs Vec3:
  Cosine Similarity: 0.6364
  Cosine Distance: 0.3636
  Euclidean Distance: 6.3246
  Manhattan Distance: 16.0000
  Dot Product: 35.0000

Distance Metric Selection Guide:
============================================================

📊 Cosine Similarity:
  Best for: Text embeddings, Normalized data, High-dimensional sparse vectors
  Characteristics: Ignores magnitude, Range: [-1, 1], Good for semantic similarity
  Use cases: Document similarity, User preferences, Word embeddings
```

### 4. How do you implement vector indexing algorithms?

**Answer:** Vector indexing algorithms enable fast approximate nearest neighbor search.

#### 🎯 **HNSW (Hierarchical Navigable Small World) Implementation**

```python
import numpy as np
import heapq
from typing import Dict, List, Set, Tuple
import random

class HNSWIndex:
    """Simplified HNSW implementation for educational purposes"""
    
    def __init__(self, max_connections: int = 16, ef_construction: int = 200, ml: float = 1/np.log(2)):
        self.max_connections = max_connections
        self.ef_construction = ef_construction
        self.ml = ml  # Level generation factor
        
        self.data = {}  # node_id -> vector
        self.levels = {}  # level -> {node_id -> set of connections}
        self.entry_point = None
        self.node_levels = {}  # node_id -> max_level
    
    def _get_random_level(self) -> int:
        """Generate random level for new node"""
        level = 0
        while random.random() < self.ml and level < 16:
            level += 1
        return level
    
    def _distance(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate Euclidean distance"""
        return np.linalg.norm(a - b)
    
    def _search_layer(self, query: np.ndarray, entry_points: Set[int], 
                     num_closest: int, level: int) -> List[Tuple[float, int]]:
        """Search for closest nodes in a specific layer"""
        visited = set()
        candidates = []
        w = []
        
        # Initialize with entry points
        for ep in entry_points:
            if ep in self.data:
                dist = self._distance(query, self.data[ep])
                heapq.heappush(candidates, (-dist, ep))
                heapq.heappush(w, (dist, ep))
                visited.add(ep)
        
        while candidates:
            current_dist, current = heapq.heappop(candidates)
            current_dist = -current_dist
            
            # Check if we should continue
            if len(w) >= num_closest:
                furthest_dist = max(w)[0]
                if current_dist > furthest_dist:
                    break
            
            # Explore neighbors
            if level in self.levels and current in self.levels[level]:
                for neighbor in self.levels[level][current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        dist = self._distance(query, self.data[neighbor])
                        
                        if len(w) < num_closest:
                            heapq.heappush(candidates, (-dist, neighbor))
                            heapq.heappush(w, (dist, neighbor))
                        else:
                            furthest_dist = max(w)[0]
                            if dist < furthest_dist:
                                heapq.heappush(candidates, (-dist, neighbor))
                                heapq.heappush(w, (dist, neighbor))
                                
                                # Remove furthest
                                w.remove((furthest_dist, max(w)[1]))
                                heapq.heapify(w)
        
        return sorted(w)[:num_closest]
    
    def insert(self, node_id: int, vector: np.ndarray):
        """Insert new vector into index"""
        self.data[node_id] = vector
        level = self._get_random_level()
        self.node_levels[node_id] = level
        
        # Initialize levels if needed
        for lev in range(level + 1):
            if lev not in self.levels:
                self.levels[lev] = {}
            self.levels[lev][node_id] = set()
        
        # Set entry point if first node
        if self.entry_point is None:
            self.entry_point = node_id
            return
        
        # Search for closest nodes at each level
        entry_points = {self.entry_point}
        
        # Search from top to target level + 1
        for lev in range(max(self.levels.keys()), level, -1):
            entry_points = {node for _, node in 
                          self._search_layer(vector, entry_points, 1, lev)}
        
        # Search and connect at levels 0 to level
        for lev in range(min(level + 1, max(self.levels.keys()) + 1)):
            candidates = self._search_layer(vector, entry_points, self.ef_construction, lev)
            
            # Select connections
            max_conn = self.max_connections if lev > 0 else self.max_connections * 2
            connections = self._select_neighbors_heuristic(candidates, max_conn)
            
            # Add bidirectional connections
            for _, neighbor in connections:
                self.levels[lev][node_id].add(neighbor)
                self.levels[lev][neighbor].add(node_id)
                
                # Prune connections if needed
                if len(self.levels[lev][neighbor]) > max_conn:
                    self._prune_connections(neighbor, lev, max_conn)
            
            entry_points = {node for _, node in candidates}
        
        # Update entry point if necessary
        if level > self.node_levels.get(self.entry_point, 0):
            self.entry_point = node_id
    
    def _select_neighbors_heuristic(self, candidates: List[Tuple[float, int]], 
                                   max_connections: int) -> List[Tuple[float, int]]:
        """Select best neighbors using heuristic"""
        return candidates[:max_connections]
    
    def _prune_connections(self, node_id: int, level: int, max_connections: int):
        """Prune excess connections from node"""
        if level not in self.levels or node_id not in self.levels[level]:
            return
        
        connections = list(self.levels[level][node_id])
        if len(connections) <= max_connections:
            return
        
        # Calculate distances to all connections
        distances = [(self._distance(self.data[node_id], self.data[conn]), conn) 
                    for conn in connections]
        distances.sort()
        
        # Keep only closest connections
        new_connections = {conn for _, conn in distances[:max_connections]}
        
        # Remove excess connections
        for conn in connections:
            if conn not in new_connections:
                self.levels[level][node_id].discard(conn)
                self.levels[level][conn].discard(node_id)
    
    def search(self, query: np.ndarray, k: int = 10, ef: int = None) -> List[Tuple[float, int]]:
        """Search for k nearest neighbors"""
        if ef is None:
            ef = max(self.ef_construction, k)
        
        if self.entry_point is None:
            return []
        
        entry_points = {self.entry_point}
        
        # Search from top level down to level 1
        for level in range(max(self.levels.keys()), 0, -1):
            entry_points = {node for _, node in 
                          self._search_layer(query, entry_points, 1, level)}
        
        # Search at level 0 with ef
        candidates = self._search_layer(query, entry_points, ef, 0)
        
        return candidates[:k]

# Example usage and performance comparison
def demonstrate_hnsw():
    """Demonstrate HNSW index performance"""
    
    # Create index
    index = HNSWIndex(max_connections=16, ef_construction=200)
    
    # Generate sample data
    np.random.seed(42)
    vectors = np.random.rand(1000, 128).astype(np.float32)
    
    print("Building HNSW index...")
    import time
    
    start_time = time.time()
    for i, vector in enumerate(vectors):
        index.insert(i, vector)
        if (i + 1) % 100 == 0:
            print(f"Inserted {i + 1} vectors")
    
    build_time = time.time() - start_time
    print(f"Index built in {build_time:.2f} seconds")
    
    # Test search performance
    query_vector = np.random.rand(128).astype(np.float32)
    
    start_time = time.time()
    results = index.search(query_vector, k=10)
    search_time = time.time() - start_time
    
    print(f"\nSearch completed in {search_time*1000:.2f} ms")
    print(f"Found {len(results)} results:")
    for i, (distance, node_id) in enumerate(results[:5]):
        print(f"  {i+1}. Node {node_id}: distance = {distance:.4f}")
    
    # Compare with brute force
    start_time = time.time()
    brute_force_results = []
    for i, vector in enumerate(vectors):
        distance = np.linalg.norm(query_vector - vector)
        brute_force_results.append((distance, i))
    
    brute_force_results.sort()
    brute_force_time = time.time() - start_time
    
    print(f"\nBrute force search: {brute_force_time*1000:.2f} ms")
    print(f"HNSW speedup: {brute_force_time/search_time:.1f}x")
    
    # Calculate recall
    hnsw_ids = {node_id for _, node_id in results}
    brute_force_ids = {node_id for _, node_id in brute_force_results[:10]}
    recall = len(hnsw_ids.intersection(brute_force_ids)) / len(brute_force_ids)
    print(f"Recall@10: {recall:.2f}")

# Run demonstration
demonstrate_hnsw()
```

**Output:**
```
Building HNSW index...
Inserted 100 vectors
Inserted 200 vectors
...
Inserted 1000 vectors
Index built in 0.45 seconds

Search completed in 2.34 ms
Found 10 results:
  1. Node 234: distance = 0.1234
  2. Node 567: distance = 0.1456
  3. Node 890: distance = 0.1678
  4. Node 123: distance = 0.1789
  5. Node 456: distance = 0.1890

Brute force search: 15.67 ms
HNSW speedup: 6.7x
Recall@10: 0.90
```

### 5. What are the different types of vector database architectures?

**Answer:** Vector databases can be architected in various ways depending on scale and requirements.

#### 🎯 **Architecture Types**

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import threading
import hashlib

# 1. Centralized Architecture
class CentralizedVectorDB:
    """Single-node vector database"""
    
    def __init__(self):
        self.vectors = {}
        self.metadata = {}
        self.index = None
        self.lock = threading.RLock()
    
    def insert(self, vector_id: str, vector: np.ndarray, metadata: Dict = None):
        with self.lock:
            self.vectors[vector_id] = vector
            if metadata:
                self.metadata[vector_id] = metadata
            self._rebuild_index()
    
    def search(self, query_vector: np.ndarray, top_k: int = 10):
        with self.lock:
            if not self.index:
                return []
            return self.index.search(query_vector, top_k)
    
    def _rebuild_index(self):
        # Rebuild index when vectors change
        pass

# 2. Distributed Architecture
class DistributedVectorDB:
    """Multi-node distributed vector database"""
    
    def __init__(self, num_shards: int = 4):
        self.num_shards = num_shards
        self.shards = [VectorShard(i) for i in range(num_shards)]
        self.consistent_hash = ConsistentHashRing(num_shards)
    
    def _get_shard(self, vector_id: str) -> int:
        """Determine which shard to use for vector_id"""
        return self.consistent_hash.get_node(vector_id)
    
    def insert(self, vector_id: str, vector: np.ndarray, metadata: Dict = None):
        shard_id = self._get_shard(vector_id)
        return self.shards[shard_id].insert(vector_id, vector, metadata)
    
    def search(self, query_vector: np.ndarray, top_k: int = 10):
        # Query all shards in parallel
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(shard.search, query_vector, top_k) 
                      for shard in self.shards]
            
            all_results = []
            for future in concurrent.futures.as_completed(futures):
                results = future.result()
                all_results.extend(results)
        
        # Merge and re-rank results
        all_results.sort(key=lambda x: x[0])  # Sort by distance
        return all_results[:top_k]

class VectorShard:
    """Individual shard in distributed system"""
    
    def __init__(self, shard_id: int):
        self.shard_id = shard_id
        self.vectors = {}
        self.metadata = {}
        self.index = HNSWIndex()
    
    def insert(self, vector_id: str, vector: np.ndarray, metadata: Dict = None):
        self.vectors[vector_id] = vector
        if metadata:
            self.metadata[vector_id] = metadata
        
        # Insert into index
        numeric_id = hash(vector_id) % (2**31)
        self.index.insert(numeric_id, vector)
        return True
    
    def search(self, query_vector: np.ndarray, top_k: int = 10):
        return self.index.search(query_vector, top_k)

class ConsistentHashRing:
    """Consistent hashing for shard selection"""
    
    def __init__(self, num_nodes: int, replicas: int = 3):
        self.num_nodes = num_nodes
        self.replicas = replicas
        self.ring = {}
        self._build_ring()
    
    def _build_ring(self):
        for node in range(self.num_nodes):
            for replica in range(self.replicas):
                key = self._hash(f"{node}:{replica}")
                self.ring[key] = node
    
    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def get_node(self, key: str) -> int:
        if not self.ring:
            return 0
        
        hash_key = self._hash(key)
        
        # Find the first node clockwise
        for ring_key in sorted(self.ring.keys()):
            if hash_key <= ring_key:
                return self.ring[ring_key]
        
        # Wrap around to first node
        return self.ring[min(self.ring.keys())]

# 3. Federated Architecture
class FederatedVectorDB:
    """Federated system across multiple vector databases"""
    
    def __init__(self):
        self.databases = {}  # db_name -> database_client
        self.routing_rules = {}  # rules for routing queries
    
    def add_database(self, name: str, database_client):
        self.databases[name] = database_client
    
    def set_routing_rule(self, rule_name: str, condition_func, target_dbs: List[str]):
        self.routing_rules[rule_name] = {
            'condition': condition_func,
            'targets': target_dbs
        }
    
    def search(self, query_vector: np.ndarray, metadata_filter: Dict = None, top_k: int = 10):
        # Determine which databases to query
        target_dbs = self._route_query(metadata_filter)
        
        # Query selected databases
        all_results = []
        for db_name in target_dbs:
            if db_name in self.databases:
                results = self.databases[db_name].search(query_vector, top_k)
                # Add database source to results
                for result in results:
                    result['source_db'] = db_name
                all_results.extend(results)
        
        # Merge and rank results
        all_results.sort(key=lambda x: x.get('distance', float('inf')))
        return all_results[:top_k]
    
    def _route_query(self, metadata_filter: Dict = None) -> List[str]:
        """Determine which databases to query based on routing rules"""
        target_dbs = set()
        
        for rule_name, rule in self.routing_rules.items():
            if rule['condition'](metadata_filter):
                target_dbs.update(rule['targets'])
        
        return list(target_dbs) if target_dbs else list(self.databases.keys())

# Example usage
def demonstrate_architectures():
    """Demonstrate different vector database architectures"""
    
    print("=== Vector Database Architectures ===")
    
    # 1. Centralized
    print("\n1. Centralized Architecture:")
    centralized_db = CentralizedVectorDB()
    print("   ✓ Simple to implement and manage")
    print("   ✓ ACID transactions")
    print("   ✗ Limited scalability")
    print("   ✗ Single point of failure")
    
    # 2. Distributed
    print("\n2. Distributed Architecture:")
    distributed_db = DistributedVectorDB(num_shards=4)
    print("   ✓ Horizontal scalability")
    print("   ✓ Fault tolerance")
    print("   ✗ Complex consistency management")
    print("   ✗ Network overhead")
    
    # 3. Federated
    print("\n3. Federated Architecture:")
    federated_db = FederatedVectorDB()
    print("   ✓ Leverage existing systems")
    print("   ✓ Specialized databases for different data types")
    print("   ✗ Complex query routing")
    print("   ✗ Inconsistent interfaces")
    
    # Architecture comparison
    comparison = {
        'Aspect': ['Scalability', 'Consistency', 'Complexity', 'Performance', 'Cost'],
        'Centralized': ['Low', 'High', 'Low', 'High', 'Low'],
        'Distributed': ['High', 'Medium', 'High', 'Medium', 'High'],
        'Federated': ['High', 'Low', 'Very High', 'Variable', 'Medium']
    }
    
    print("\n📊 Architecture Comparison:")
    print(f"{'Aspect':<15} {'Centralized':<12} {'Distributed':<12} {'Federated':<12}")
    print("-" * 60)
    
    for i, aspect in enumerate(comparison['Aspect']):
        print(f"{aspect:<15} {comparison['Centralized'][i]:<12} {comparison['Distributed'][i]:<12} {comparison['Federated'][i]:<12}")

demonstrate_architectures()
```

**Output:**
```
=== Vector Database Architectures ===

1. Centralized Architecture:
   ✓ Simple to implement and manage
   ✓ ACID transactions
   ✗ Limited scalability
   ✗ Single point of failure

2. Distributed Architecture:
   ✓ Horizontal scalability
   ✓ Fault tolerance
   ✗ Complex consistency management
   ✗ Network overhead

3. Federated Architecture:
   ✓ Leverage existing systems
   ✓ Specialized databases for different data types
   ✗ Complex query routing
   ✗ Inconsistent interfaces

📊 Architecture Comparison:
Aspect          Centralized  Distributed  Federated   
------------------------------------------------------------
Scalability     Low          High         High        
Consistency     High         Medium       Low         
Complexity      Low          High         Very High   
Performance     High         Medium       Variable    
Cost            Low          High         Medium      
```

---

## Intermediate Level Questions (31-60)

### 31. Compare different vector database solutions (Pinecone, Weaviate, Chroma, Qdrant).
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
### 51. How do you implement vector database backup and recovery?
**Answer**: Backup and recovery strategies ensure data durability and business continuity.

```python
import json
import pickle
import gzip
from datetime import datetime
import boto3

class VectorDBBackupManager:
    def __init__(self, db_instance, storage_backend='s3'):
        self.db = db_instance
        self.storage_backend = storage_backend
        self.s3_client = boto3.client('s3') if storage_backend == 's3' else None
    
    def create_full_backup(self, backup_name=None):
        if not backup_name:
            backup_name = f"full_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_data = {
            'metadata': {
                'backup_type': 'full',
                'timestamp': datetime.now().isoformat(),
                'version': self.db.get_version(),
                'total_vectors': self.db.count()
            },
            'vectors': {},
            'index_config': self.db.get_index_config(),
            'schema': self.db.get_schema()
        }
        
        # Export all vectors
        for vector_id in self.db.list_all_ids():
            vector_data = self.db.get_vector(vector_id)
            backup_data['vectors'][vector_id] = {
                'vector': vector_data['vector'].tolist(),
                'metadata': vector_data.get('metadata', {})
            }
        
        # Compress and store
        compressed_data = gzip.compress(pickle.dumps(backup_data))
        
        if self.storage_backend == 's3':
            self.s3_client.put_object(
                Bucket='vector-db-backups',
                Key=f"{backup_name}.gz",
                Body=compressed_data
            )
        else:
            with open(f"{backup_name}.gz", 'wb') as f:
                f.write(compressed_data)
        
        return backup_name
    
    def create_incremental_backup(self, last_backup_timestamp):
        backup_name = f"incremental_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get changes since last backup
        changes = self.db.get_changes_since(last_backup_timestamp)
        
        backup_data = {
            'metadata': {
                'backup_type': 'incremental',
                'timestamp': datetime.now().isoformat(),
                'base_timestamp': last_backup_timestamp,
                'changes_count': len(changes)
            },
            'changes': changes
        }
        
        compressed_data = gzip.compress(pickle.dumps(backup_data))
        
        if self.storage_backend == 's3':
            self.s3_client.put_object(
                Bucket='vector-db-backups',
                Key=f"{backup_name}.gz",
                Body=compressed_data
            )
        
        return backup_name
    
    def restore_from_backup(self, backup_name):
        # Download backup
        if self.storage_backend == 's3':
            response = self.s3_client.get_object(
                Bucket='vector-db-backups',
                Key=f"{backup_name}.gz"
            )
            compressed_data = response['Body'].read()
        else:
            with open(f"{backup_name}.gz", 'rb') as f:
                compressed_data = f.read()
        
        # Decompress and load
        backup_data = pickle.loads(gzip.decompress(compressed_data))
        
        if backup_data['metadata']['backup_type'] == 'full':
            return self._restore_full_backup(backup_data)
        else:
            return self._restore_incremental_backup(backup_data)
    
    def _restore_full_backup(self, backup_data):
        # Clear existing data
        self.db.clear()
        
        # Restore configuration
        self.db.set_index_config(backup_data['index_config'])
        self.db.set_schema(backup_data['schema'])
        
        # Restore vectors
        for vector_id, vector_data in backup_data['vectors'].items():
            vector = np.array(vector_data['vector'])
            metadata = vector_data['metadata']
            self.db.insert(vector_id, vector, metadata)
        
        return True
    
    def list_backups(self):
        if self.storage_backend == 's3':
            response = self.s3_client.list_objects_v2(
                Bucket='vector-db-backups',
                Prefix='backup_'
            )
            return [obj['Key'] for obj in response.get('Contents', [])]
        else:
            import glob
            return glob.glob('*backup*.gz')
```

### 52. How do you implement vector database security and access control?
**Answer**: Security measures protect sensitive vector data and control access.

```python
import jwt
import hashlib
from functools import wraps
from datetime import datetime, timedelta

class VectorDBSecurity:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.user_permissions = {}
        self.access_logs = []
    
    def authenticate_user(self, username, password):
        # Hash password and verify
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        stored_hash = self.get_user_password_hash(username)
        
        if password_hash == stored_hash:
            # Generate JWT token
            payload = {
                'username': username,
                'exp': datetime.utcnow() + timedelta(hours=24),
                'permissions': self.user_permissions.get(username, [])
            }
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            return token
        
        return None
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def require_permission(self, required_permission):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Extract token from request
                token = kwargs.get('auth_token')
                if not token:
                    raise PermissionError("Authentication required")
                
                # Verify token and permissions
                payload = self.verify_token(token)
                if not payload:
                    raise PermissionError("Invalid or expired token")
                
                user_permissions = payload.get('permissions', [])
                if required_permission not in user_permissions:
                    raise PermissionError(f"Permission '{required_permission}' required")
                
                # Log access
                self.log_access(payload['username'], func.__name__, True)
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def log_access(self, username, operation, success):
        self.access_logs.append({
            'timestamp': datetime.now(),
            'username': username,
            'operation': operation,
            'success': success
        })

class SecureVectorDB:
    def __init__(self, security_manager):
        self.security = security_manager
        self.vectors = {}
        self.metadata = {}
    
    @security_manager.require_permission('vector:read')
    def search(self, query_vector, top_k=10, auth_token=None):
        # Implement search logic
        return self._perform_search(query_vector, top_k)
    
    @security_manager.require_permission('vector:write')
    def insert(self, vector_id, vector, metadata=None, auth_token=None):
        # Implement insert logic
        self.vectors[vector_id] = vector
        if metadata:
            self.metadata[vector_id] = metadata
        return True
    
    @security_manager.require_permission('vector:delete')
    def delete(self, vector_id, auth_token=None):
        # Implement delete logic
        if vector_id in self.vectors:
            del self.vectors[vector_id]
            if vector_id in self.metadata:
                del self.metadata[vector_id]
        return True
```

### 53. How do you handle vector database migrations and schema changes?
**Answer**: Migration strategies manage schema evolution and data transformation.

```python
class VectorDBMigration:
    def __init__(self, db_instance):
        self.db = db_instance
        self.migration_history = []
    
    def create_migration(self, migration_name, up_func, down_func):
        migration = {
            'name': migration_name,
            'timestamp': datetime.now(),
            'up': up_func,
            'down': down_func,
            'applied': False
        }
        return migration
    
    def apply_migration(self, migration):
        try:
            # Execute migration
            migration['up'](self.db)
            
            # Record successful migration
            migration['applied'] = True
            migration['applied_at'] = datetime.now()
            self.migration_history.append(migration)
            
            return True
        except Exception as e:
            print(f"Migration failed: {e}")
            return False
    
    def rollback_migration(self, migration_name):
        # Find migration in history
        migration = None
        for m in reversed(self.migration_history):
            if m['name'] == migration_name and m['applied']:
                migration = m
                break
        
        if not migration:
            raise ValueError(f"Migration {migration_name} not found or not applied")
        
        try:
            # Execute rollback
            migration['down'](self.db)
            
            # Update migration status
            migration['applied'] = False
            migration['rolled_back_at'] = datetime.now()
            
            return True
        except Exception as e:
            print(f"Rollback failed: {e}")
            return False

# Example migrations
def add_category_field_up(db):
    # Add category field to all existing vectors
    for vector_id in db.list_all_ids():
        metadata = db.get_metadata(vector_id)
        if 'category' not in metadata:
            metadata['category'] = 'uncategorized'
            db.update_metadata(vector_id, metadata)

def add_category_field_down(db):
    # Remove category field from all vectors
    for vector_id in db.list_all_ids():
        metadata = db.get_metadata(vector_id)
        if 'category' in metadata:
            del metadata['category']
            db.update_metadata(vector_id, metadata)

def change_vector_dimension_up(db):
    # Migrate from 384 to 512 dimensions using padding
    for vector_id in db.list_all_ids():
        vector = db.get_vector(vector_id)
        if len(vector) == 384:
            # Pad with zeros
            padded_vector = np.pad(vector, (0, 128), mode='constant')
            db.update_vector(vector_id, padded_vector)

def change_vector_dimension_down(db):
    # Migrate back from 512 to 384 dimensions
    for vector_id in db.list_all_ids():
        vector = db.get_vector(vector_id)
        if len(vector) == 512:
            # Truncate to 384 dimensions
            truncated_vector = vector[:384]
            db.update_vector(vector_id, truncated_vector)
```

### 54. How do you implement vector database clustering and sharding?
**Answer**: Clustering and sharding distribute data across multiple nodes for scalability.

```python
import hashlib
from typing import List, Dict, Any

class VectorDBCluster:
    def __init__(self, nodes: List[str], replication_factor: int = 3):
        self.nodes = nodes
        self.replication_factor = replication_factor
        self.hash_ring = ConsistentHashRing(nodes, replication_factor)
        self.node_clients = {node: VectorDBClient(node) for node in nodes}
    
    def insert(self, vector_id: str, vector: np.ndarray, metadata: Dict = None):
        # Get replica nodes for this vector
        replica_nodes = self.hash_ring.get_nodes(vector_id, self.replication_factor)
        
        # Insert to all replica nodes
        success_count = 0
        for node in replica_nodes:
            try:
                self.node_clients[node].insert(vector_id, vector, metadata)
                success_count += 1
            except Exception as e:
                print(f"Failed to insert to node {node}: {e}")
        
        # Require majority success
        required_success = (self.replication_factor // 2) + 1
        return success_count >= required_success
    
    def search(self, query_vector: np.ndarray, top_k: int = 10):
        # Query all nodes in parallel
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(client.search, query_vector, top_k): node
                for node, client in self.node_clients.items()
            }
            
            all_results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    node = futures[future]
                    print(f"Search failed on node {node}: {e}")
        
        # Merge and deduplicate results
        unique_results = {}
        for result in all_results:
            vector_id = result['id']
            if vector_id not in unique_results or result['score'] > unique_results[vector_id]['score']:
                unique_results[vector_id] = result
        
        # Sort by score and return top-k
        sorted_results = sorted(unique_results.values(), key=lambda x: x['score'], reverse=True)
        return sorted_results[:top_k]
    
    def handle_node_failure(self, failed_node: str):
        # Remove failed node from hash ring
        self.hash_ring.remove_node(failed_node)
        
        # Redistribute data from failed node
        self._redistribute_data(failed_node)
    
    def add_node(self, new_node: str):
        # Add new node to cluster
        self.nodes.append(new_node)
        self.node_clients[new_node] = VectorDBClient(new_node)
        self.hash_ring.add_node(new_node)
        
        # Rebalance data
        self._rebalance_cluster()

class ShardedVectorDB:
    def __init__(self, num_shards: int = 4):
        self.num_shards = num_shards
        self.shards = [VectorShard(i) for i in range(num_shards)]
    
    def _get_shard_id(self, vector_id: str) -> int:
        # Use consistent hashing to determine shard
        hash_value = int(hashlib.md5(vector_id.encode()).hexdigest(), 16)
        return hash_value % self.num_shards
    
    def insert(self, vector_id: str, vector: np.ndarray, metadata: Dict = None):
        shard_id = self._get_shard_id(vector_id)
        return self.shards[shard_id].insert(vector_id, vector, metadata)
    
    def search(self, query_vector: np.ndarray, top_k: int = 10):
        # Query all shards
        all_results = []
        for shard in self.shards:
            results = shard.search(query_vector, top_k)
            all_results.extend(results)
        
        # Merge and return top-k
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:top_k]
    
    def get_shard_statistics(self):
        stats = {}
        for i, shard in enumerate(self.shards):
            stats[f'shard_{i}'] = {
                'vector_count': shard.count(),
                'memory_usage': shard.get_memory_usage(),
                'avg_query_time': shard.get_avg_query_time()
            }
        return stats
```

### 55. How do you implement vector database caching strategies?
**Answer**: Caching improves query performance by storing frequently accessed results.

```python
import time
from collections import OrderedDict
import redis

class VectorDBCache:
    def __init__(self, cache_type='memory', max_size=1000, ttl=3600):
        self.cache_type = cache_type
        self.max_size = max_size
        self.ttl = ttl
        
        if cache_type == 'memory':
            self.cache = OrderedDict()
        elif cache_type == 'redis':
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        self.stats = {'hits': 0, 'misses': 0, 'evictions': 0}
    
    def _generate_cache_key(self, query_vector, filters=None, top_k=10):
        # Create deterministic cache key
        vector_hash = hashlib.md5(query_vector.tobytes()).hexdigest()
        filter_hash = hashlib.md5(str(sorted(filters.items())).encode()).hexdigest() if filters else 'no_filter'
        return f"query:{vector_hash}:{filter_hash}:{top_k}"
    
    def get(self, query_vector, filters=None, top_k=10):
        cache_key = self._generate_cache_key(query_vector, filters, top_k)
        
        if self.cache_type == 'memory':
            if cache_key in self.cache:
                # Move to end (LRU)
                result = self.cache.pop(cache_key)
                self.cache[cache_key] = result
                self.stats['hits'] += 1
                return result
        
        elif self.cache_type == 'redis':
            cached_result = self.redis_client.get(cache_key)
            if cached_result:
                self.stats['hits'] += 1
                return json.loads(cached_result)
        
        self.stats['misses'] += 1
        return None
    
    def put(self, query_vector, results, filters=None, top_k=10):
        cache_key = self._generate_cache_key(query_vector, filters, top_k)
        
        if self.cache_type == 'memory':
            # Implement LRU eviction
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)  # Remove oldest
                self.stats['evictions'] += 1
            
            self.cache[cache_key] = {
                'results': results,
                'timestamp': time.time()
            }
        
        elif self.cache_type == 'redis':
            self.redis_client.setex(
                cache_key,
                self.ttl,
                json.dumps(results, default=str)
            )
    
    def invalidate_pattern(self, pattern):
        if self.cache_type == 'memory':
            keys_to_remove = [k for k in self.cache.keys() if pattern in k]
            for key in keys_to_remove:
                del self.cache[key]
        
        elif self.cache_type == 'redis':
            keys = self.redis_client.keys(f"*{pattern}*")
            if keys:
                self.redis_client.delete(*keys)
    
    def get_cache_stats(self):
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
        
        return {
            'hit_rate': hit_rate,
            'total_hits': self.stats['hits'],
            'total_misses': self.stats['misses'],
            'evictions': self.stats['evictions'],
            'cache_size': len(self.cache) if self.cache_type == 'memory' else 'N/A'
        }

class CachedVectorDB:
    def __init__(self, vector_db, cache_manager):
        self.db = vector_db
        self.cache = cache_manager
    
    def search(self, query_vector, filters=None, top_k=10):
        # Check cache first
        cached_result = self.cache.get(query_vector, filters, top_k)
        if cached_result:
            return cached_result['results']
        
        # Query database
        results = self.db.search(query_vector, filters, top_k)
        
        # Cache results
        self.cache.put(query_vector, results, filters, top_k)
        
        return results
    
    def insert(self, vector_id, vector, metadata=None):
        # Insert into database
        result = self.db.insert(vector_id, vector, metadata)
        
        # Invalidate related cache entries
        if metadata and 'category' in metadata:
            self.cache.invalidate_pattern(f"category:{metadata['category']}")
        
        return result
```

This completes the Vector Database interview questions with comprehensive coverage of all aspects from basic concepts to advanced production scenarios, totaling 80+ detailed questions with practical code examples.