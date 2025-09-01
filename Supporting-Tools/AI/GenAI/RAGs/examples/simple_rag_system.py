"""
Simple RAG (Retrieval-Augmented Generation) System Example
Demonstrates basic RAG implementation using OpenAI and vector search
"""

import openai
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
from typing import List, Dict, Any

class SimpleRAGSystem:
    def __init__(self, openai_api_key: str, embedding_model: str = 'all-MiniLM-L6-v2'):
        """Initialize RAG system with OpenAI and embedding model"""
        openai.api_key = openai_api_key
        self.embedding_model = SentenceTransformer(embedding_model)
        self.knowledge_base = []
        self.embeddings = []
    
    def add_documents(self, documents: List[str]):
        """Add documents to knowledge base and create embeddings"""
        print(f"Adding {len(documents)} documents to knowledge base...")
        
        # Store documents
        self.knowledge_base.extend(documents)
        
        # Create embeddings
        new_embeddings = self.embedding_model.encode(documents)
        
        if len(self.embeddings) == 0:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
        
        print(f"Knowledge base now contains {len(self.knowledge_base)} documents")
    
    def retrieve_relevant_docs(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve most relevant documents for a query"""
        if not self.knowledge_base:
            return []
        
        # Create query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top-k most similar documents
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        relevant_docs = []
        for idx in top_indices:
            relevant_docs.append({
                'document': self.knowledge_base[idx],
                'similarity': float(similarities[idx]),
                'index': int(idx)
            })
        
        return relevant_docs
    
    def generate_response(self, query: str, context_docs: List[str]) -> str:
        """Generate response using OpenAI with retrieved context"""
        # Prepare context
        context = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(context_docs)])
        
        # Create prompt
        prompt = f"""Based on the following context documents, answer the user's question. 
If the answer cannot be found in the context, say so clearly.

Context:
{context}

Question: {query}

Answer:"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def query(self, question: str, top_k: int = 3, return_sources: bool = True) -> Dict[str, Any]:
        """Main RAG query method"""
        print(f"\nProcessing query: {question}")
        
        # Step 1: Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_docs(question, top_k)
        
        if not relevant_docs:
            return {
                'answer': "No relevant documents found in knowledge base.",
                'sources': [],
                'query': question
            }
        
        print(f"Retrieved {len(relevant_docs)} relevant documents")
        
        # Step 2: Extract document texts for generation
        context_docs = [doc['document'] for doc in relevant_docs]
        
        # Step 3: Generate response
        answer = self.generate_response(question, context_docs)
        
        result = {
            'answer': answer,
            'query': question
        }
        
        if return_sources:
            result['sources'] = relevant_docs
        
        return result

def main():
    """Example usage of RAG system"""
    
    # Sample knowledge base - data engineering concepts
    documents = [
        "Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in Java, Scala, Python and R, and an optimized engine that supports general execution graphs.",
        
        "ETL stands for Extract, Transform, Load. It's a data integration process that combines data from multiple sources into a single, consistent data store that is loaded into a data warehouse.",
        
        "A data lake is a centralized repository that allows you to store all your structured and unstructured data at any scale. You can store your data as-is, without having to first structure the data.",
        
        "Apache Kafka is a distributed streaming platform that is used to build real-time data pipelines and streaming applications. It is horizontally scalable, fault-tolerant, and fast.",
        
        "Data warehousing is the process of collecting and managing data from varied sources to provide meaningful business insights. A data warehouse is typically used to connect and analyze business data from heterogeneous sources.",
        
        "Apache Airflow is an open-source platform to develop, schedule, and monitor workflows. It allows you to programmatically author, schedule and monitor workflows as directed acyclic graphs (DAGs).",
        
        "Snowflake is a cloud-based data warehousing platform that provides data storage, processing, and analytic solutions. It separates compute and storage, allowing for independent scaling.",
        
        "DBT (Data Build Tool) is a command-line tool that enables data analysts and engineers to transform data in their warehouse more effectively by writing simple SQL SELECT statements."
    ]
    
    # Initialize RAG system (you need to provide your OpenAI API key)
    api_key = "your-openai-api-key-here"  # Replace with actual key
    rag_system = SimpleRAGSystem(api_key)
    
    # Add documents to knowledge base
    rag_system.add_documents(documents)
    
    # Example queries
    queries = [
        "What is Apache Spark?",
        "How does ETL work?",
        "What's the difference between a data lake and data warehouse?",
        "Tell me about workflow orchestration tools",
        "What is machine learning?"  # This should indicate no relevant docs
    ]
    
    # Process queries
    for query in queries:
        result = rag_system.query(query)
        
        print(f"\nQuery: {result['query']}")
        print(f"Answer: {result['answer']}")
        
        if 'sources' in result and result['sources']:
            print("\nSources:")
            for i, source in enumerate(result['sources'], 1):
                print(f"{i}. (Similarity: {source['similarity']:.3f}) {source['document'][:100]}...")
        
        print("-" * 80)

if __name__ == "__main__":
    main()