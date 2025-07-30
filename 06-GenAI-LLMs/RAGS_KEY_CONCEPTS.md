# RAG (Retrieval-Augmented Generation) Key Concepts

## 1. Hybrid AI Architecture
**What it is**: Framework that combines retrieval systems with generative models to provide accurate, contextual responses using external knowledge.

**Core Components**:
- **Knowledge Base**: External documents, databases, APIs
- **Retrieval System**: Search and rank relevant information
- **Generator**: LLM that creates responses using retrieved context
- **Orchestrator**: Coordinates retrieval and generation

## 2. RAG Architecture
**Basic RAG Pipeline**:
```python
def rag_pipeline(query):
    # 1. Retrieve relevant documents
    relevant_docs = retriever.search(query, top_k=5)
    
    # 2. Create context from retrieved documents
    context = "\n".join([doc.content for doc in relevant_docs])
    
    # 3. Generate response using context
    prompt = f"""
    Context: {context}
    
    Question: {query}
    
    Answer based on the provided context:
    """
    
    response = llm.generate(prompt)
    return response, relevant_docs
```

**Advanced RAG Architecture**:
```yaml
# Multi-Stage RAG
1. Query Processing: Understand and refine user query
2. Retrieval: Multiple retrieval strategies
3. Reranking: Score and reorder retrieved documents
4. Context Fusion: Combine information from multiple sources
5. Generation: Create response with citations
6. Post-processing: Fact-check and format output
```

## 3. Document Processing and Indexing
**Document Chunking**:
```python
def chunk_document(text, chunk_size=500, overlap=50):
    """Split document into overlapping chunks"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Find sentence boundary to avoid cutting mid-sentence
        if end < len(text):
            last_period = chunk.rfind('.')
            if last_period > chunk_size * 0.8:
                end = start + last_period + 1
                chunk = text[start:end]
        
        chunks.append({
            'content': chunk,
            'start_pos': start,
            'end_pos': end
        })
        
        start = end - overlap
    
    return chunks
```

**Embedding Generation**:
```python
from sentence_transformers import SentenceTransformer

# Initialize embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks):
    """Generate embeddings for document chunks"""
    embeddings = []
    
    for chunk in chunks:
        # Create embedding for chunk content
        embedding = embedder.encode(chunk['content'])
        
        embeddings.append({
            'content': chunk['content'],
            'embedding': embedding,
            'metadata': {
                'start_pos': chunk['start_pos'],
                'end_pos': chunk['end_pos']
            }
        })
    
    return embeddings
```

## 4. Vector Databases
**Popular Vector Databases**:
```yaml
# Pinecone (Managed)
- Cloud-native vector database
- High performance and scalability
- Built-in filtering and metadata

# Weaviate (Open Source)
- GraphQL API
- Hybrid search capabilities
- Multi-modal support

# Chroma (Open Source)  
- Simple Python API
- Local and distributed deployment
- Built-in embedding functions

# FAISS (Facebook AI)
- High-performance similarity search
- Multiple index types
- CPU and GPU support
```

**Vector Database Operations**:
```python
import chromadb

# Initialize Chroma client
client = chromadb.Client()
collection = client.create_collection("knowledge_base")

# Add documents with embeddings
def add_documents(documents):
    for i, doc in enumerate(documents):
        collection.add(
            embeddings=[doc['embedding'].tolist()],
            documents=[doc['content']],
            metadatas=[doc['metadata']],
            ids=[f"doc_{i}"]
        )

# Query similar documents
def retrieve_documents(query, top_k=5):
    query_embedding = embedder.encode(query)
    
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=['documents', 'distances', 'metadatas']
    )
    
    return results
```

## 5. Retrieval Strategies
**Dense Retrieval**:
```python
# Semantic similarity using embeddings
def dense_retrieval(query, embeddings, top_k=5):
    query_embedding = embedder.encode(query)
    
    # Calculate cosine similarity
    similarities = []
    for doc in embeddings:
        similarity = cosine_similarity(
            query_embedding.reshape(1, -1),
            doc['embedding'].reshape(1, -1)
        )[0][0]
        similarities.append((similarity, doc))
    
    # Sort by similarity and return top-k
    similarities.sort(reverse=True)
    return [doc for _, doc in similarities[:top_k]]
```

**Sparse Retrieval (BM25)**:
```python
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize

def sparse_retrieval(query, documents, top_k=5):
    # Tokenize documents
    tokenized_docs = [word_tokenize(doc.lower()) for doc in documents]
    
    # Create BM25 index
    bm25 = BM25Okapi(tokenized_docs)
    
    # Query and get scores
    query_tokens = word_tokenize(query.lower())
    scores = bm25.get_scores(query_tokens)
    
    # Get top-k documents
    top_indices = scores.argsort()[-top_k:][::-1]
    return [documents[i] for i in top_indices]
```

**Hybrid Retrieval**:
```python
def hybrid_retrieval(query, documents, embeddings, alpha=0.7):
    """Combine dense and sparse retrieval"""
    
    # Dense retrieval scores
    dense_results = dense_retrieval(query, embeddings)
    dense_scores = {doc['content']: score for score, doc in dense_results}
    
    # Sparse retrieval scores  
    sparse_results = sparse_retrieval(query, [doc['content'] for doc in embeddings])
    sparse_scores = {doc: score for score, doc in enumerate(sparse_results)}
    
    # Combine scores
    combined_scores = {}
    for doc in embeddings:
        content = doc['content']
        dense_score = dense_scores.get(content, 0)
        sparse_score = sparse_scores.get(content, 0)
        
        combined_scores[content] = alpha * dense_score + (1 - alpha) * sparse_score
    
    # Return top results
    sorted_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs[:5]
```

## 6. Query Processing
**Query Expansion**:
```python
def expand_query(original_query, llm):
    """Generate related queries to improve retrieval"""
    
    prompt = f"""
    Original query: {original_query}
    
    Generate 3 related queries that might help find relevant information:
    1.
    2. 
    3.
    """
    
    expanded_queries = llm.generate(prompt)
    return [original_query] + expanded_queries.split('\n')

def multi_query_retrieval(queries, retriever):
    """Retrieve documents for multiple related queries"""
    all_results = []
    
    for query in queries:
        results = retriever.search(query, top_k=3)
        all_results.extend(results)
    
    # Deduplicate and rerank
    unique_results = list({doc['content']: doc for doc in all_results}.values())
    return unique_results[:5]
```

**Query Classification**:
```python
def classify_query(query, llm):
    """Determine query type to choose appropriate retrieval strategy"""
    
    prompt = f"""
    Classify this query into one of these categories:
    - factual: Asking for specific facts or information
    - analytical: Requiring analysis or comparison
    - procedural: Asking how to do something
    - conceptual: Asking for explanations or definitions
    
    Query: {query}
    Category:
    """
    
    category = llm.generate(prompt).strip().lower()
    return category

def adaptive_retrieval(query, category, retriever):
    """Adapt retrieval strategy based on query type"""
    
    if category == 'factual':
        # Use precise matching
        return retriever.search(query, top_k=3, similarity_threshold=0.8)
    elif category == 'analytical':
        # Retrieve diverse perspectives
        return retriever.search(query, top_k=7, diversity_penalty=0.5)
    elif category == 'procedural':
        # Focus on step-by-step content
        return retriever.search(query, top_k=5, filter_type='procedure')
    else:
        # Default retrieval
        return retriever.search(query, top_k=5)
```

## 7. Context Management
**Context Ranking**:
```python
def rerank_contexts(query, retrieved_docs, reranker_model):
    """Rerank retrieved documents for relevance"""
    
    query_doc_pairs = [(query, doc['content']) for doc in retrieved_docs]
    
    # Use cross-encoder for reranking
    scores = reranker_model.predict(query_doc_pairs)
    
    # Sort by relevance score
    ranked_docs = sorted(
        zip(retrieved_docs, scores), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    return [doc for doc, score in ranked_docs]
```

**Context Compression**:
```python
def compress_context(contexts, query, max_tokens=2000):
    """Compress contexts to fit within token limit"""
    
    # Calculate token counts
    total_tokens = sum(count_tokens(ctx) for ctx in contexts)
    
    if total_tokens <= max_tokens:
        return contexts
    
    # Compress by extracting most relevant sentences
    compressed_contexts = []
    remaining_tokens = max_tokens
    
    for context in contexts:
        sentences = context.split('.')
        relevant_sentences = []
        
        for sentence in sentences:
            sentence_tokens = count_tokens(sentence)
            if sentence_tokens <= remaining_tokens:
                # Check relevance to query
                relevance_score = calculate_relevance(query, sentence)
                if relevance_score > 0.5:
                    relevant_sentences.append(sentence)
                    remaining_tokens -= sentence_tokens
        
        if relevant_sentences:
            compressed_contexts.append('. '.join(relevant_sentences))
    
    return compressed_contexts
```

## 8. Generation with Citations
**Response Generation**:
```python
def generate_with_citations(query, contexts, llm):
    """Generate response with source citations"""
    
    # Number contexts for citation
    numbered_contexts = []
    for i, context in enumerate(contexts, 1):
        numbered_contexts.append(f"[{i}] {context}")
    
    context_text = "\n\n".join(numbered_contexts)
    
    prompt = f"""
    Based on the following sources, answer the question. 
    Include citations using [1], [2], etc. format.
    
    Sources:
    {context_text}
    
    Question: {query}
    
    Answer with citations:
    """
    
    response = llm.generate(prompt)
    
    return {
        'answer': response,
        'sources': contexts,
        'citations': extract_citations(response)
    }

def extract_citations(text):
    """Extract citation numbers from generated text"""
    import re
    citations = re.findall(r'\[(\d+)\]', text)
    return [int(c) for c in citations]
```

## 9. Evaluation Metrics
**Retrieval Metrics**:
```python
def evaluate_retrieval(queries, ground_truth, retriever):
    """Evaluate retrieval performance"""
    
    total_precision = 0
    total_recall = 0
    total_f1 = 0
    
    for query, relevant_docs in zip(queries, ground_truth):
        retrieved_docs = retriever.search(query, top_k=10)
        retrieved_ids = {doc['id'] for doc in retrieved_docs}
        relevant_ids = set(relevant_docs)
        
        # Calculate metrics
        tp = len(retrieved_ids & relevant_ids)
        precision = tp / len(retrieved_ids) if retrieved_ids else 0
        recall = tp / len(relevant_ids) if relevant_ids else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        total_precision += precision
        total_recall += recall
        total_f1 += f1
    
    n_queries = len(queries)
    return {
        'precision': total_precision / n_queries,
        'recall': total_recall / n_queries,
        'f1': total_f1 / n_queries
    }
```

**End-to-End Evaluation**:
```python
def evaluate_rag_system(test_cases, rag_system):
    """Evaluate complete RAG system"""
    
    results = []
    
    for case in test_cases:
        query = case['query']
        expected_answer = case['answer']
        
        # Generate response
        response = rag_system.generate(query)
        
        # Evaluate different aspects
        relevance = calculate_relevance(response['answer'], expected_answer)
        faithfulness = check_faithfulness(response['answer'], response['sources'])
        completeness = assess_completeness(response['answer'], expected_answer)
        
        results.append({
            'query': query,
            'relevance': relevance,
            'faithfulness': faithfulness,
            'completeness': completeness
        })
    
    return results
```

## 10. Advanced RAG Patterns
**Multi-Hop RAG**:
```python
def multi_hop_rag(initial_query, max_hops=3):
    """Perform multiple retrieval steps for complex queries"""
    
    current_query = initial_query
    all_contexts = []
    
    for hop in range(max_hops):
        # Retrieve documents for current query
        contexts = retriever.search(current_query, top_k=5)
        all_contexts.extend(contexts)
        
        # Generate follow-up query if needed
        if hop < max_hops - 1:
            follow_up_prompt = f"""
            Based on the information found, what additional information 
            is needed to fully answer: {initial_query}
            
            Current information: {contexts[0]['content'][:200]}...
            
            Next query:
            """
            current_query = llm.generate(follow_up_prompt)
    
    # Generate final answer using all contexts
    return generate_with_citations(initial_query, all_contexts, llm)
```

**Adaptive RAG**:
```python
def adaptive_rag(query, confidence_threshold=0.8):
    """Adapt retrieval strategy based on query complexity"""
    
    # Assess query complexity
    complexity = assess_query_complexity(query)
    
    if complexity == 'simple':
        # Direct retrieval
        contexts = retriever.search(query, top_k=3)
        return generate_response(query, contexts)
    
    elif complexity == 'medium':
        # Enhanced retrieval with reranking
        contexts = retriever.search(query, top_k=7)
        reranked_contexts = rerank_contexts(query, contexts)
        return generate_response(query, reranked_contexts[:5])
    
    else:  # complex
        # Multi-step retrieval with query decomposition
        sub_queries = decompose_query(query)
        all_contexts = []
        
        for sub_query in sub_queries:
            contexts = retriever.search(sub_query, top_k=3)
            all_contexts.extend(contexts)
        
        return generate_response(query, all_contexts)
```