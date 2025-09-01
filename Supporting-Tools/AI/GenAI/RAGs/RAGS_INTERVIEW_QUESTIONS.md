# RAGs (Retrieval-Augmented Generation) - Interview Questions

## Basic Questions

### 1. What is RAG and why is it important for LLM applications?
**Answer:** RAG (Retrieval-Augmented Generation) combines information retrieval with text generation to provide accurate, up-to-date responses. It's important because:
- **Reduces hallucinations**: Grounds responses in factual data
- **Up-to-date information**: Access to current data beyond training cutoff
- **Domain-specific knowledge**: Incorporate specialized information
- **Cost-effective**: Avoid retraining large models
- **Transparency**: Cite sources for answers

### 2. Explain the basic RAG workflow.
**Answer:** The RAG workflow consists of:
1. **Query Processing**: Parse and understand user question
2. **Retrieval**: Search knowledge base for relevant documents
3. **Context Assembly**: Combine retrieved documents
4. **Prompt Construction**: Create augmented prompt with context
5. **Generation**: LLM generates response using context
6. **Post-processing**: Format and validate output

### 3. What are the main components of a RAG system?
**Answer:**
- **Knowledge Base**: Vector database with document embeddings
- **Retriever**: Finds relevant documents using similarity search
- **Generator**: Language model for response generation
- **Query Processor**: Handles input formatting and parsing
- **Response Synthesizer**: Combines retrieved context with generation

## Intermediate Questions

### 4. How do you handle document chunking in RAG systems?
**Answer:**
```python
def chunk_document(text, chunk_size=500, overlap=50):
    """Split document into overlapping chunks"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks

# Semantic chunking
def semantic_chunk(text, model, similarity_threshold=0.8):
    """Chunk based on semantic similarity"""
    sentences = text.split('.')
    chunks = []
    current_chunk = []
    
    for sentence in sentences:
        if not current_chunk:
            current_chunk.append(sentence)
        else:
            # Check similarity with current chunk
            chunk_text = '. '.join(current_chunk)
            similarity = calculate_similarity(chunk_text, sentence, model)
            
            if similarity > similarity_threshold:
                current_chunk.append(sentence)
            else:
                chunks.append('. '.join(current_chunk))
                current_chunk = [sentence]
    
    if current_chunk:
        chunks.append('. '.join(current_chunk))
    
    return chunks
```

**Chunking strategies:**
- **Fixed-size**: Equal character/token counts
- **Semantic**: Based on meaning and context
- **Structural**: Follow document structure (paragraphs, sections)
- **Overlapping**: Maintain context between chunks

### 5. What are different retrieval strategies in RAG?
**Answer:**
**Dense Retrieval:**
- Vector similarity search using embeddings
- Semantic understanding of queries
- Good for conceptual matches

**Sparse Retrieval:**
- Keyword-based search (BM25, TF-IDF)
- Exact term matching
- Good for specific facts

**Hybrid Retrieval:**
```python
def hybrid_search(query, dense_results, sparse_results, alpha=0.7):
    """Combine dense and sparse retrieval results"""
    combined_scores = {}
    
    # Normalize and combine scores
    for doc_id, dense_score in dense_results.items():
        combined_scores[doc_id] = alpha * dense_score
    
    for doc_id, sparse_score in sparse_results.items():
        if doc_id in combined_scores:
            combined_scores[doc_id] += (1 - alpha) * sparse_score
        else:
            combined_scores[doc_id] = (1 - alpha) * sparse_score
    
    # Sort by combined score
    return sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
```

### 6. How do you evaluate RAG system performance?
**Answer:**
**Retrieval Metrics:**
- **Recall@K**: Relevant documents in top-K results
- **Precision@K**: Proportion of relevant documents
- **MRR**: Mean Reciprocal Rank
- **NDCG**: Normalized Discounted Cumulative Gain

**Generation Metrics:**
- **BLEU/ROUGE**: Text similarity scores
- **Faithfulness**: Response grounded in retrieved context
- **Answer Relevance**: Response addresses the question
- **Context Precision**: Retrieved context is relevant

```python
def evaluate_rag_system(questions, ground_truth, rag_system):
    """Evaluate RAG system performance"""
    metrics = {
        'faithfulness': [],
        'answer_relevance': [],
        'context_precision': []
    }
    
    for question, expected_answer in zip(questions, ground_truth):
        result = rag_system.query(question)
        
        # Calculate faithfulness (answer supported by context)
        faithfulness = calculate_faithfulness(result['answer'], result['sources'])
        metrics['faithfulness'].append(faithfulness)
        
        # Calculate answer relevance
        relevance = calculate_relevance(result['answer'], question)
        metrics['answer_relevance'].append(relevance)
        
        # Calculate context precision
        precision = calculate_context_precision(result['sources'], expected_answer)
        metrics['context_precision'].append(precision)
    
    return {k: np.mean(v) for k, v in metrics.items()}
```

## Advanced Questions

### 7. How would you implement a multi-hop RAG system?
**Answer:**
```python
class MultiHopRAG:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator
        self.max_hops = 3
    
    def multi_hop_query(self, question):
        """Perform multi-hop reasoning"""
        current_query = question
        all_context = []
        
        for hop in range(self.max_hops):
            # Retrieve documents for current query
            docs = self.retriever.retrieve(current_query, top_k=5)
            all_context.extend(docs)
            
            # Generate intermediate reasoning
            intermediate_response = self.generator.generate(
                query=current_query,
                context=docs,
                task="reasoning"
            )
            
            # Check if we need another hop
            if self.is_answer_complete(intermediate_response, question):
                break
            
            # Generate follow-up query
            current_query = self.generate_followup_query(
                original_question=question,
                intermediate_answer=intermediate_response,
                context=docs
            )
        
        # Generate final answer using all context
        final_answer = self.generator.generate(
            query=question,
            context=all_context,
            task="final_answer"
        )
        
        return {
            'answer': final_answer,
            'hops': hop + 1,
            'context': all_context
        }
```

### 8. How do you handle conflicting information in retrieved documents?
**Answer:**
```python
class ConflictResolutionRAG:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator
    
    def detect_conflicts(self, documents):
        """Detect conflicting information in documents"""
        conflicts = []
        
        for i, doc1 in enumerate(documents):
            for j, doc2 in enumerate(documents[i+1:], i+1):
                # Use NLI model to detect contradictions
                contradiction_score = self.check_contradiction(doc1, doc2)
                
                if contradiction_score > 0.8:
                    conflicts.append({
                        'doc1_idx': i,
                        'doc2_idx': j,
                        'score': contradiction_score
                    })
        
        return conflicts
    
    def resolve_conflicts(self, query, documents, conflicts):
        """Resolve conflicts using various strategies"""
        if not conflicts:
            return documents
        
        # Strategy 1: Source credibility
        credibility_scores = self.get_source_credibility(documents)
        
        # Strategy 2: Recency
        recency_scores = self.get_recency_scores(documents)
        
        # Strategy 3: Consensus
        consensus_scores = self.get_consensus_scores(documents)
        
        # Combine scores and filter
        final_scores = []
        for i, doc in enumerate(documents):
            score = (
                0.4 * credibility_scores[i] +
                0.3 * recency_scores[i] +
                0.3 * consensus_scores[i]
            )
            final_scores.append(score)
        
        # Keep top documents, remove conflicting low-score ones
        filtered_docs = self.filter_by_conflicts(documents, conflicts, final_scores)
        
        return filtered_docs
```

### 9. How would you implement RAG with real-time data updates?
**Answer:**
```python
class RealTimeRAG:
    def __init__(self, vector_db, embedding_model):
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.update_queue = []
        self.last_update = time.time()
    
    def add_real_time_document(self, doc_id, content, metadata=None):
        """Add document to update queue"""
        self.update_queue.append({
            'id': doc_id,
            'content': content,
            'metadata': metadata,
            'timestamp': time.time(),
            'operation': 'upsert'
        })
    
    def process_updates(self, batch_size=100):
        """Process queued updates in batches"""
        if len(self.update_queue) < batch_size:
            return
        
        batch = self.update_queue[:batch_size]
        self.update_queue = self.update_queue[batch_size:]
        
        # Create embeddings for batch
        contents = [item['content'] for item in batch]
        embeddings = self.embedding_model.encode(contents)
        
        # Update vector database
        for item, embedding in zip(batch, embeddings):
            self.vector_db.upsert(
                id=item['id'],
                vector=embedding,
                metadata=item['metadata']
            )
        
        self.last_update = time.time()
    
    def query_with_freshness(self, question, max_age_hours=24):
        """Query with freshness constraints"""
        cutoff_time = time.time() - (max_age_hours * 3600)
        
        # Process any pending updates first
        self.process_updates(batch_size=50)
        
        # Query with time filter
        results = self.vector_db.query(
            vector=self.embedding_model.encode([question])[0],
            filter={
                'timestamp': {'$gte': cutoff_time}
            },
            top_k=10
        )
        
        return results
```

### 10. What are the challenges and limitations of RAG systems?
**Answer:**
**Technical Challenges:**
- **Retrieval quality**: Relevant documents not always retrieved
- **Context length limits**: LLM token limitations
- **Latency**: Multiple API calls increase response time
- **Consistency**: Different retrievals may give different answers
- **Hallucination**: LLM may still generate unsupported claims

**Solutions:**
```python
# Improve retrieval with reranking
def rerank_documents(query, documents, reranker_model):
    """Rerank retrieved documents for better relevance"""
    pairs = [(query, doc) for doc in documents]
    scores = reranker_model.predict(pairs)
    
    # Sort by reranker scores
    ranked_docs = [doc for _, doc in sorted(zip(scores, documents), reverse=True)]
    return ranked_docs

# Handle context length limits
def manage_context_length(documents, max_tokens=4000):
    """Truncate or summarize context to fit token limits"""
    total_tokens = 0
    selected_docs = []
    
    for doc in documents:
        doc_tokens = count_tokens(doc)
        if total_tokens + doc_tokens <= max_tokens:
            selected_docs.append(doc)
            total_tokens += doc_tokens
        else:
            # Summarize remaining documents
            remaining_docs = documents[len(selected_docs):]
            summary = summarize_documents(remaining_docs)
            selected_docs.append(summary)
            break
    
    return selected_docs
```

**Business Challenges:**
- **Data quality**: Inconsistent or outdated information
- **Privacy**: Sensitive data in knowledge base
- **Compliance**: Regulatory requirements for data usage
- **Cost**: API costs for embeddings and generation
- **Maintenance**: Keeping knowledge base current