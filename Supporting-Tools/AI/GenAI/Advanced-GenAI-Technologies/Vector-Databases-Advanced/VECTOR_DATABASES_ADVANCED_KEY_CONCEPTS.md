# 🗄️ Vector Databases Advanced - Key Concepts

## 🎯 **Real-World Analogy: The Smart Library with AI Librarian**

> **Think of vector databases as a futuristic library where instead of organizing books by title or author, everything is organized by meaning and similarity. The AI librarian can instantly find related content even if you describe it vaguely.**

## 🔥 **Core Concepts**

### 1. **Vector Embeddings** 📊

```python
# Creating embeddings for similarity search
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert text to vectors
texts = [
    "Python data processing",
    "Machine learning algorithms", 
    "Database optimization",
    "Data pipeline automation"
]

embeddings = model.encode(texts)
print(f"Each text becomes a {embeddings.shape[1]}-dimensional vector")

# Similarity calculation
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similarity = cosine_similarity(embeddings[0], embeddings[1])
print(f"Similarity between texts: {similarity:.3f}")
```

### 2. **Production Vector Databases** 🚀

#### **Pinecone (Managed)**
```python
import pinecone

# Initialize Pinecone
pinecone.init(api_key="your-key", environment="us-west1-gcp")

# Create index
index = pinecone.Index("document-search")

# Upsert vectors with metadata
index.upsert([
    ("doc1", embedding1.tolist(), {"title": "Python Guide", "category": "programming"}),
    ("doc2", embedding2.tolist(), {"title": "ML Basics", "category": "ai"})
])

# Query similar documents
results = index.query(
    vector=query_embedding.tolist(),
    top_k=5,
    include_metadata=True,
    filter={"category": "programming"}
)
```

#### **Weaviate (Open Source)**
```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# Define schema
schema = {
    "classes": [{
        "class": "Document",
        "properties": [
            {"name": "title", "dataType": ["string"]},
            {"name": "content", "dataType": ["text"]},
            {"name": "category", "dataType": ["string"]}
        ]
    }]
}

client.schema.create(schema)

# Add documents (auto-vectorization)
client.data_object.create({
    "title": "Python Data Engineering",
    "content": "Complete guide to Python for data engineering...",
    "category": "programming"
}, "Document")

# Semantic search
result = client.query.get("Document", ["title", "content"]) \
    .with_near_text({"concepts": ["data processing"]}) \
    .with_limit(5) \
    .do()
```

#### **Azure AI Search**
```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Initialize client
search_client = SearchClient(
    endpoint="https://your-service.search.windows.net",
    index_name="documents",
    credential=AzureKeyCredential("your-key")
)

# Vector search
results = search_client.search(
    search_text=None,
    vector_queries=[{
        "vector": query_embedding,
        "k_nearest_neighbors": 5,
        "fields": "content_vector"
    }],
    select=["title", "content", "category"]
)
```

### 3. **RAG Implementation** 🔍

```python
# Complete RAG system
class RAGSystem:
    def __init__(self, vector_db, llm):
        self.vector_db = vector_db
        self.llm = llm
    
    def retrieve_context(self, query, k=5):
        # Get relevant documents
        query_embedding = self.embed_text(query)
        results = self.vector_db.query(query_embedding, top_k=k)
        return [doc['content'] for doc in results]
    
    def generate_answer(self, query, context):
        prompt = f"""
        Context: {' '.join(context)}
        
        Question: {query}
        
        Answer based on the context:
        """
        return self.llm.generate(prompt)
    
    def answer_question(self, query):
        context = self.retrieve_context(query)
        return self.generate_answer(query, context)
```

## 🛠️ **Advanced Patterns**

### **Hybrid Search**
```python
# Combine vector and keyword search
def hybrid_search(query, vector_weight=0.7, keyword_weight=0.3):
    # Vector similarity
    vector_results = vector_search(query)
    
    # Keyword search
    keyword_results = keyword_search(query)
    
    # Combine scores
    combined_results = []
    for doc in all_documents:
        vector_score = get_vector_score(doc, vector_results)
        keyword_score = get_keyword_score(doc, keyword_results)
        
        final_score = (vector_score * vector_weight + 
                      keyword_score * keyword_weight)
        combined_results.append((doc, final_score))
    
    return sorted(combined_results, key=lambda x: x[1], reverse=True)
```

### **Multi-Modal Vectors**
```python
# Text + Image embeddings
from transformers import CLIPModel, CLIPProcessor

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def create_multimodal_embedding(text, image=None):
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    
    # Combine text and image embeddings
    text_embedding = outputs.text_embeds
    if image:
        image_embedding = outputs.image_embeds
        combined = torch.cat([text_embedding, image_embedding], dim=1)
        return combined
    return text_embedding
```