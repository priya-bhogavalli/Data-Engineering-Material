# LangChain Interview Questions for Data Engineering & AI

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Chain Architecture Questions (16-30)](#chain-architecture-questions-16-30)
3. [Memory & Context Questions (31-45)](#memory--context-questions-31-45)
4. [Data Integration Questions (46-60)](#data-integration-questions-46-60)
5. [RAG Implementation Questions (61-75)](#rag-implementation-questions-61-75)
6. [Production & Scaling (76-90)](#production--scaling-76-90)
7. [Advanced Patterns (91-100)](#advanced-patterns-91-100)

---

## 🎯 **Introduction**

LangChain is a powerful framework for developing applications with Large Language Models (LLMs). For data engineers, it provides essential tools for building AI-powered data processing pipelines, RAG systems, and intelligent data analysis workflows.

**Why LangChain is Critical for Data Engineers:**
- **LLM Integration**: Seamless integration with multiple LLM providers
- **Data Processing**: Advanced document loading and text processing
- **RAG Systems**: Built-in support for retrieval-augmented generation
- **Chain Composition**: Modular approach to building complex AI workflows
- **Production Ready**: Tools for monitoring, evaluation, and deployment

---

## Core Concepts Questions (1-15)

### 1. What are the core components of LangChain and how do they work together?
**Answer**: 
LangChain's architecture is built around several key components that work together to create powerful LLM applications.

**Core Components:**
- **LLMs**: Interface to language models (OpenAI, Anthropic, etc.)
- **Prompts**: Templates and prompt engineering tools
- **Chains**: Sequences of calls to LLMs or other utilities
- **Memory**: Persistent state between chain calls
- **Agents**: LLMs that can use tools and make decisions
- **Tools**: Functions that agents can call
- **Document Loaders**: Import data from various sources
- **Vector Stores**: Storage and retrieval of embeddings

```python
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Basic chain example
llm = OpenAI(temperature=0.7)
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?"
)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("eco-friendly water bottles")

# Chain with memory
memory = ConversationBufferMemory()
conversation_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=True
)
```

### 2. How do you implement document loading and text processing in LangChain?
**Answer**: LangChain provides extensive document loading capabilities for various data sources.

```python
from langchain.document_loaders import (
    TextLoader, PDFLoader, CSVLoader, 
    UnstructuredHTMLLoader, DirectoryLoader
)
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    TokenTextSplitter
)

# Load different document types
text_loader = TextLoader("data/document.txt")
pdf_loader = PDFLoader("data/report.pdf")
csv_loader = CSVLoader("data/sales_data.csv")

# Load entire directory
directory_loader = DirectoryLoader(
    "data/",
    glob="**/*.txt",
    loader_cls=TextLoader
)
documents = directory_loader.load()

# Text splitting for better processing
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

# Split documents into chunks
texts = text_splitter.split_documents(documents)

# Token-based splitting for precise control
token_splitter = TokenTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
token_texts = token_splitter.split_documents(documents)

# Custom document processing
def preprocess_documents(docs):
    processed = []
    for doc in docs:
        # Clean text
        cleaned_content = doc.page_content.strip()
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
        
        # Add metadata
        doc.metadata['processed_at'] = datetime.now().isoformat()
        doc.metadata['word_count'] = len(cleaned_content.split())
        doc.page_content = cleaned_content
        
        processed.append(doc)
    return processed

processed_docs = preprocess_documents(texts)
```

### 3. How do you work with different LLM providers in LangChain?
**Answer**: LangChain provides a unified interface for multiple LLM providers.

```python
from langchain.llms import OpenAI, Anthropic, HuggingFacePipeline
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.callbacks import get_openai_callback

# OpenAI models
openai_llm = OpenAI(
    model_name="text-davinci-003",
    temperature=0.7,
    max_tokens=1000
)

# Chat models for conversation
chat_model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.3
)

# Anthropic Claude
claude = ChatAnthropic(
    model="claude-2",
    max_tokens_to_sample=1000
)

# Local Hugging Face model
local_llm = HuggingFacePipeline.from_model_id(
    model_id="microsoft/DialoGPT-medium",
    task="text-generation",
    model_kwargs={"temperature": 0.7}
)

# Cost tracking with callbacks
def track_costs(chain, input_text):
    with get_openai_callback() as cb:
        result = chain.run(input_text)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Total Cost: ${cb.total_cost}")
        return result

# Model comparison utility
def compare_models(prompt, models):
    results = {}
    for name, model in models.items():
        try:
            result = model(prompt)
            results[name] = {
                'response': result,
                'success': True
            }
        except Exception as e:
            results[name] = {
                'error': str(e),
                'success': False
            }
    return results

models = {
    'openai': openai_llm,
    'claude': claude,
    'local': local_llm
}
comparison = compare_models("Explain quantum computing", models)
```

## Chain Architecture Questions (16-30)

### 4. How do you build complex chains and what are the different chain types?
**Answer**: LangChain offers various chain types for different use cases.

```python
from langchain.chains import (
    LLMChain, SimpleSequentialChain, SequentialChain,
    TransformChain, LLMSummarizationChain
)
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain

# Simple sequential chain
first_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["product"],
        template="What is the best feature of {product}?"
    )
)

second_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["feature"],
        template="How can we market this feature: {feature}?"
    )
)

sequential_chain = SimpleSequentialChain(
    chains=[first_chain, second_chain],
    verbose=True
)

# Complex sequential chain with multiple inputs/outputs
analysis_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["data"],
        template="Analyze this data: {data}"
    ),
    output_key="analysis"
)

summary_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["analysis"],
        template="Summarize: {analysis}"
    ),
    output_key="summary"
)

overall_chain = SequentialChain(
    chains=[analysis_chain, summary_chain],
    input_variables=["data"],
    output_variables=["analysis", "summary"],
    verbose=True
)

# Transform chain for data preprocessing
def transform_data(inputs):
    text = inputs["text"]
    # Clean and preprocess
    cleaned = text.lower().strip()
    return {"cleaned_text": cleaned}

transform_chain = TransformChain(
    input_variables=["text"],
    output_variables=["cleaned_text"],
    transform=transform_data
)

# Router chain for different prompt strategies
prompt_infos = [
    {
        "name": "technical",
        "description": "Good for technical questions",
        "prompt_template": "Technical analysis: {input}"
    },
    {
        "name": "business",
        "description": "Good for business questions", 
        "prompt_template": "Business perspective: {input}"
    }
]

router_chain = MultiPromptChain.from_prompts(
    llm=llm,
    prompt_infos=prompt_infos,
    default_chain=LLMChain(llm=llm, prompt=PromptTemplate(
        template="General response: {input}",
        input_variables=["input"]
    ))
)
```

### 5. How do you implement custom chains for specific data engineering tasks?
**Answer**: Custom chains allow you to create specialized workflows for data engineering scenarios.

```python
from langchain.chains.base import Chain
from typing import Dict, List
import pandas as pd

class DataAnalysisChain(Chain):
    """Custom chain for automated data analysis"""
    
    llm: Any
    input_key: str = "data"
    output_key: str = "analysis"
    
    @property
    def input_keys(self) -> List[str]:
        return [self.input_key]
    
    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]
    
    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        data = inputs[self.input_key]
        
        # Step 1: Data profiling
        if isinstance(data, pd.DataFrame):
            profile = self._profile_dataframe(data)
        else:
            profile = f"Data type: {type(data)}, Length: {len(str(data))}"
        
        # Step 2: Generate analysis prompt
        prompt = f"""
        Analyze this data profile and provide insights:
        {profile}
        
        Please provide:
        1. Key observations
        2. Potential data quality issues
        3. Recommended next steps
        """
        
        # Step 3: Get LLM analysis
        analysis = self.llm(prompt)
        
        return {self.output_key: analysis}
    
    def _profile_dataframe(self, df: pd.DataFrame) -> str:
        profile = f"""
        DataFrame Profile:
        - Shape: {df.shape}
        - Columns: {list(df.columns)}
        - Data types: {df.dtypes.to_dict()}
        - Missing values: {df.isnull().sum().to_dict()}
        - Numeric summary: {df.describe().to_string()}
        """
        return profile

# ETL Chain for data processing
class ETLChain(Chain):
    """Chain for Extract, Transform, Load operations with LLM guidance"""
    
    llm: Any
    
    @property
    def input_keys(self) -> List[str]:
        return ["source_data", "target_schema"]
    
    @property
    def output_keys(self) -> List[str]:
        return ["transformed_data", "transformation_log"]
    
    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        source_data = inputs["source_data"]
        target_schema = inputs["target_schema"]
        
        # Generate transformation strategy
        strategy_prompt = f"""
        Given source data structure: {self._analyze_structure(source_data)}
        Target schema: {target_schema}
        
        Provide a step-by-step transformation strategy.
        """
        
        strategy = self.llm(strategy_prompt)
        
        # Apply transformations (simplified)
        transformed_data = self._apply_transformations(source_data, strategy)
        
        return {
            "transformed_data": transformed_data,
            "transformation_log": strategy
        }
    
    def _analyze_structure(self, data):
        if isinstance(data, pd.DataFrame):
            return f"DataFrame with columns: {list(data.columns)}"
        return f"Data type: {type(data)}"
    
    def _apply_transformations(self, data, strategy):
        # Implement actual transformations based on strategy
        return data  # Simplified

# Usage
data_chain = DataAnalysisChain(llm=llm)
etl_chain = ETLChain(llm=llm)

# Combine into pipeline
from langchain.chains import SequentialChain

data_pipeline = SequentialChain(
    chains=[etl_chain, data_chain],
    input_variables=["source_data", "target_schema"],
    output_variables=["transformed_data", "transformation_log", "analysis"]
)
```

## Memory & Context Questions (31-45)

### 6. How do you implement different types of memory in LangChain applications?
**Answer**: LangChain provides various memory types for maintaining context across interactions.

```python
from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
    ConversationSummaryBufferMemory,
    VectorStoreRetrieverMemory
)
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

# Buffer memory - stores all conversation history
buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Window memory - keeps only last k interactions
window_memory = ConversationBufferWindowMemory(
    k=5,
    memory_key="chat_history",
    return_messages=True
)

# Summary memory - summarizes old conversations
summary_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

# Summary buffer memory - combines summary and buffer
summary_buffer_memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=1000,
    memory_key="chat_history",
    return_messages=True
)

# Vector store memory for semantic search
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(["Initial context"], embeddings)

vector_memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs=dict(k=3)),
    memory_key="relevant_context"
)

# Custom memory for data engineering contexts
class DataContextMemory(ConversationBufferMemory):
    """Custom memory that tracks data processing context"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_context = {}
    
    def save_context(self, inputs, outputs):
        super().save_context(inputs, outputs)
        
        # Track data-related context
        if "data_source" in inputs:
            self.data_context["last_source"] = inputs["data_source"]
        if "schema" in outputs:
            self.data_context["current_schema"] = outputs["schema"]
    
    def load_memory_variables(self, inputs):
        memory_vars = super().load_memory_variables(inputs)
        memory_vars["data_context"] = self.data_context
        return memory_vars

# Usage with chains
conversation_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["chat_history", "human_input"],
        template="""
        Previous conversation:
        {chat_history}
        
        Human: {human_input}
        Assistant:"""
    ),
    memory=summary_buffer_memory,
    verbose=True
)

# Memory persistence
import pickle

def save_memory(memory, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(memory, f)

def load_memory(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

# Save and restore memory
save_memory(buffer_memory, "conversation_memory.pkl")
restored_memory = load_memory("conversation_memory.pkl")
```

### 7. How do you manage long-term context and conversation state?
**Answer**: Managing long-term context requires strategic memory management and state persistence.

```python
from langchain.schema import BaseMemory
from typing import Any, Dict, List
import json
from datetime import datetime

class PersistentConversationMemory(BaseMemory):
    """Memory that persists to database/file with intelligent summarization"""
    
    def __init__(self, session_id: str, storage_path: str = None):
        self.session_id = session_id
        self.storage_path = storage_path or f"memory_{session_id}.json"
        self.conversation_history = []
        self.summary = ""
        self.metadata = {}
        self.load_from_storage()
    
    @property
    def memory_variables(self) -> List[str]:
        return ["history", "summary", "context"]
    
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "history": self._get_recent_history(),
            "summary": self.summary,
            "context": self._get_relevant_context(inputs)
        }
    
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        # Save interaction
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "inputs": inputs,
            "outputs": outputs
        }
        self.conversation_history.append(interaction)
        
        # Summarize if history gets too long
        if len(self.conversation_history) > 20:
            self._summarize_old_interactions()
        
        # Persist to storage
        self.save_to_storage()
    
    def _get_recent_history(self, limit: int = 10) -> List[Dict]:
        return self.conversation_history[-limit:]
    
    def _get_relevant_context(self, inputs: Dict[str, Any]) -> str:
        # Extract relevant context based on current inputs
        context_parts = []
        
        if self.summary:
            context_parts.append(f"Previous context: {self.summary}")
        
        # Add any relevant metadata
        if "topic" in inputs and inputs["topic"] in self.metadata:
            context_parts.append(f"Topic context: {self.metadata[inputs['topic']]}")
        
        return "\n".join(context_parts)
    
    def _summarize_old_interactions(self):
        # Keep recent interactions, summarize older ones
        recent = self.conversation_history[-10:]
        old = self.conversation_history[:-10]
        
        if old:
            # Create summary of old interactions
            old_text = "\n".join([
                f"User: {interaction['inputs']}\nAssistant: {interaction['outputs']}"
                for interaction in old
            ])
            
            summary_prompt = f"""
            Summarize the key points from this conversation history:
            {old_text}
            
            Focus on:
            1. Main topics discussed
            2. Important decisions made
            3. Ongoing context that should be remembered
            """
            
            # This would use an LLM to create the summary
            new_summary = "Summary of previous interactions..."  # Simplified
            
            if self.summary:
                self.summary = f"{self.summary}\n\nAdditional context: {new_summary}"
            else:
                self.summary = new_summary
        
        # Keep only recent interactions
        self.conversation_history = recent
    
    def save_to_storage(self):
        data = {
            "session_id": self.session_id,
            "conversation_history": self.conversation_history,
            "summary": self.summary,
            "metadata": self.metadata,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_storage(self):
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.conversation_history = data.get("conversation_history", [])
                self.summary = data.get("summary", "")
                self.metadata = data.get("metadata", {})
        except FileNotFoundError:
            # Initialize empty memory
            pass
    
    def clear(self) -> None:
        self.conversation_history = []
        self.summary = ""
        self.metadata = {}
        self.save_to_storage()

# Context-aware chain with persistent memory
class ContextAwareChain(LLMChain):
    """Chain that maintains context across sessions"""
    
    def __init__(self, session_id: str, **kwargs):
        self.session_id = session_id
        memory = PersistentConversationMemory(session_id)
        
        prompt = PromptTemplate(
            input_variables=["history", "summary", "context", "input"],
            template="""
            Conversation Summary: {summary}
            
            Relevant Context: {context}
            
            Recent History: {history}
            
            Current Input: {input}
            
            Response:"""
        )
        
        super().__init__(memory=memory, prompt=prompt, **kwargs)

# Usage
context_chain = ContextAwareChain(
    session_id="user_123",
    llm=llm
)

# The chain will automatically maintain context across calls
response1 = context_chain.run("What's the best way to process CSV files?")
response2 = context_chain.run("How about for large files?")  # Remembers CSV context
```

## Data Integration Questions (46-60)

### 8. How do you integrate LangChain with databases and data warehouses?
**Answer**: LangChain provides tools for database integration and SQL generation.

```python
from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.tools.sql_database.tool import QuerySQLDataBaseTool

# Database connection
db = SQLDatabase.from_uri("postgresql://user:password@localhost/datawarehouse")

# SQL Database Chain for natural language to SQL
sql_chain = SQLDatabaseChain.from_llm(
    llm=llm,
    db=db,
    verbose=True,
    return_intermediate_steps=True
)

# Query database with natural language
result = sql_chain.run("What are the top 5 customers by revenue this year?")

# SQL Agent for more complex interactions
sql_agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True,
    agent_type="zero-shot-react-description"
)

# Complex multi-step database analysis
complex_result = sql_agent.run("""
Analyze our sales data:
1. Find the top 10 products by revenue
2. Show their sales trend over the last 6 months
3. Identify any seasonal patterns
""")

# Custom database integration
class DataWarehouseChain(Chain):
    """Custom chain for data warehouse operations"""
    
    def __init__(self, db_connection, llm):
        self.db = db_connection
        self.llm = llm
    
    @property
    def input_keys(self) -> List[str]:
        return ["query", "context"]
    
    @property
    def output_keys(self) -> List[str]:
        return ["sql", "results", "analysis"]
    
    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        query = inputs["query"]
        context = inputs.get("context", "")
        
        # Generate SQL with context
        sql_prompt = f"""
        Database schema context: {context}
        
        Convert this natural language query to SQL:
        {query}
        
        SQL:"""
        
        sql_query = self.llm(sql_prompt)
        
        # Execute query
        try:
            results = self.db.run(sql_query)
            
            # Analyze results
            analysis_prompt = f"""
            SQL Query: {sql_query}
            Results: {results}
            
            Provide analysis and insights:
            """
            
            analysis = self.llm(analysis_prompt)
            
            return {
                "sql": sql_query,
                "results": results,
                "analysis": analysis
            }
        except Exception as e:
            return {
                "sql": sql_query,
                "results": f"Error: {str(e)}",
                "analysis": "Query execution failed"
            }

# Integration with data pipelines
from langchain.document_loaders import DataFrameLoader
import pandas as pd

def create_data_pipeline_chain(data_sources):
    """Create a chain that processes multiple data sources"""
    
    # Load data from various sources
    loaders = []
    for source in data_sources:
        if source["type"] == "csv":
            df = pd.read_csv(source["path"])
            loader = DataFrameLoader(df, page_content_column=source.get("content_column"))
        elif source["type"] == "database":
            # Load from database
            df = pd.read_sql(source["query"], source["connection"])
            loader = DataFrameLoader(df)
        
        loaders.append(loader)
    
    # Combine all documents
    all_docs = []
    for loader in loaders:
        all_docs.extend(loader.load())
    
    # Create analysis chain
    analysis_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            input_variables=["data_summary"],
            template="""
            Analyze this combined dataset:
            {data_summary}
            
            Provide insights on:
            1. Data quality issues
            2. Relationships between datasets
            3. Recommended transformations
            """
        )
    )
    
    return analysis_chain, all_docs

# Usage
data_sources = [
    {"type": "csv", "path": "sales.csv", "content_column": "description"},
    {"type": "database", "query": "SELECT * FROM customers", "connection": db}
]

pipeline_chain, documents = create_data_pipeline_chain(data_sources)
```

### 9. How do you implement streaming data processing with LangChain?
**Answer**: LangChain can be integrated with streaming frameworks for real-time data processing.

```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
import asyncio
from typing import Any, Dict, List, Optional

# Custom streaming callback for data processing
class DataProcessingCallback(BaseCallbackHandler):
    """Callback for streaming data processing results"""
    
    def __init__(self, output_queue):
        self.output_queue = output_queue
        self.current_result = ""
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.current_result += token
        # Stream partial results
        self.output_queue.put({
            "type": "partial",
            "content": token,
            "full_content": self.current_result
        })
    
    def on_llm_end(self, response, **kwargs) -> None:
        self.output_queue.put({
            "type": "complete",
            "content": self.current_result
        })
        self.current_result = ""

# Streaming LLM setup
streaming_llm = OpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=0.7
)

# Real-time data analysis chain
class StreamingAnalysisChain:
    """Chain for real-time data stream analysis"""
    
    def __init__(self, llm):
        self.llm = llm
        self.analysis_template = PromptTemplate(
            input_variables=["data_batch", "context"],
            template="""
            Previous context: {context}
            
            New data batch: {data_batch}
            
            Analyze this data and provide:
            1. Key insights
            2. Anomalies detected
            3. Updated context for next batch
            """
        )
        self.context = ""
    
    async def process_stream(self, data_stream):
        """Process streaming data asynchronously"""
        async for batch in data_stream:
            try:
                # Analyze current batch
                analysis = await self._analyze_batch(batch)
                
                # Update context for next iteration
                self.context = analysis.get("updated_context", "")
                
                yield {
                    "batch_id": batch["id"],
                    "analysis": analysis,
                    "timestamp": batch["timestamp"]
                }
                
            except Exception as e:
                yield {
                    "batch_id": batch["id"],
                    "error": str(e),
                    "timestamp": batch["timestamp"]
                }
    
    async def _analyze_batch(self, batch):
        """Analyze a single batch of data"""
        prompt = self.analysis_template.format(
            data_batch=str(batch["data"]),
            context=self.context
        )
        
        # Use async LLM call if available
        result = self.llm(prompt)
        
        # Parse result to extract context
        lines = result.split('\n')
        updated_context = ""
        for line in lines:
            if "Updated context:" in line:
                updated_context = line.split("Updated context:")[-1].strip()
        
        return {
            "insights": result,
            "updated_context": updated_context
        }

# Kafka integration example
from kafka import KafkaConsumer
import json

class KafkaLangChainProcessor:
    """Process Kafka streams with LangChain"""
    
    def __init__(self, topic, llm):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.analysis_chain = StreamingAnalysisChain(llm)
    
    async def process_messages(self):
        """Process Kafka messages with LLM analysis"""
        batch = []
        batch_size = 10
        
        for message in self.consumer:
            batch.append(message.value)
            
            if len(batch) >= batch_size:
                # Process batch
                batch_data = {
                    "id": f"batch_{len(batch)}",
                    "data": batch,
                    "timestamp": message.timestamp
                }
                
                async for result in self.analysis_chain.process_stream([batch_data]):
                    print(f"Analysis result: {result}")
                
                batch = []

# WebSocket streaming for real-time UI updates
import websockets
import json

class WebSocketLangChainServer:
    """WebSocket server for real-time LangChain results"""
    
    def __init__(self, llm):
        self.llm = llm
        self.clients = set()
    
    async def register_client(self, websocket):
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)
    
    async def broadcast_analysis(self, data):
        """Broadcast analysis results to all connected clients"""
        if self.clients:
            message = json.dumps({
                "type": "analysis",
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
            
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )
    
    async def process_user_query(self, websocket, query):
        """Process user query and stream results"""
        callback = DataProcessingCallback(asyncio.Queue())
        
        chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                input_variables=["query"],
                template="Analyze: {query}"
            ),
            callbacks=[callback]
        )
        
        # Run chain and stream results
        result = chain.run(query)
        
        await websocket.send(json.dumps({
            "type": "complete",
            "result": result
        }))

# Usage
processor = KafkaLangChainProcessor("data-stream", streaming_llm)
# asyncio.run(processor.process_messages())
```

## RAG Implementation Questions (61-75)

### 10. How do you implement a production-ready RAG system with LangChain?
**Answer**: Building a robust RAG system requires careful consideration of document processing, vector storage, and retrieval strategies.

```python
from langchain.vectorstores import Pinecone, FAISS, Chroma
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pinecone

class ProductionRAGSystem:
    """Production-ready RAG system with advanced features"""
    
    def __init__(self, config):
        self.config = config
        self.embeddings = self._setup_embeddings()
        self.vectorstore = self._setup_vectorstore()
        self.retriever = self._setup_retriever()
        self.qa_chain = self._setup_qa_chain()
    
    def _setup_embeddings(self):
        """Setup embedding model with fallback options"""
        try:
            if self.config["embedding_type"] == "openai":
                return OpenAIEmbeddings(
                    model="text-embedding-ada-002",
                    openai_api_key=self.config["openai_api_key"]
                )
            else:
                return HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
        except Exception as e:
            print(f"Embedding setup failed: {e}")
            # Fallback to local embeddings
            return HuggingFaceEmbeddings()
    
    def _setup_vectorstore(self):
        """Setup vector store with persistence"""
        if self.config["vectorstore_type"] == "pinecone":
            pinecone.init(
                api_key=self.config["pinecone_api_key"],
                environment=self.config["pinecone_env"]
            )
            return Pinecone.from_existing_index(
                index_name=self.config["pinecone_index"],
                embedding=self.embeddings
            )
        elif self.config["vectorstore_type"] == "chroma":
            return Chroma(
                persist_directory=self.config["chroma_persist_dir"],
                embedding_function=self.embeddings
            )
        else:
            # FAISS with persistence
            try:
                return FAISS.load_local(
                    self.config["faiss_index_path"],
                    self.embeddings
                )
            except:
                # Create new FAISS index
                return FAISS.from_texts([""], self.embeddings)
    
    def _setup_retriever(self):
        """Setup advanced retriever with compression"""
        base_retriever = self.vectorstore.as_retriever(
            search_type="mmr",  # Maximum Marginal Relevance
            search_kwargs={
                "k": self.config.get("retrieval_k", 10),
                "fetch_k": self.config.get("fetch_k", 20),
                "lambda_mult": 0.7  # Diversity parameter
            }
        )
        
        # Add contextual compression
        compressor = LLMChainExtractor.from_llm(
            llm=OpenAI(temperature=0)
        )
        
        return ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
    
    def _setup_qa_chain(self):
        """Setup QA chain with custom prompt"""
        custom_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            Use the following context to answer the question. If you cannot find the answer in the context, say "I don't have enough information to answer this question."
            
            Context: {context}
            
            Question: {question}
            
            Answer: """
        )
        
        return RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": custom_prompt},
            return_source_documents=True
        )
    
    def add_documents(self, documents):
        """Add documents to the vector store"""
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.get("chunk_size", 1000),
            chunk_overlap=self.config.get("chunk_overlap", 200),
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        splits = text_splitter.split_documents(documents)
        
        # Add metadata
        for i, split in enumerate(splits):
            split.metadata.update({
                "chunk_id": i,
                "source": split.metadata.get("source", "unknown"),
                "timestamp": datetime.now().isoformat()
            })
        
        # Add to vector store
        if hasattr(self.vectorstore, 'add_documents'):
            self.vectorstore.add_documents(splits)
        else:
            # For FAISS, need to recreate
            texts = [doc.page_content for doc in splits]
            metadatas = [doc.metadata for doc in splits]
            self.vectorstore.add_texts(texts, metadatas)
        
        # Save if using FAISS
        if self.config["vectorstore_type"] == "faiss":
            self.vectorstore.save_local(self.config["faiss_index_path"])
    
    def query(self, question, chat_history=None):
        """Query the RAG system"""
        if chat_history:
            # Use conversational chain
            conv_chain = ConversationalRetrievalChain.from_llm(
                llm=OpenAI(temperature=0),
                retriever=self.retriever,
                return_source_documents=True
            )
            result = conv_chain({
                "question": question,
                "chat_history": chat_history
            })
        else:
            result = self.qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "sources": [doc.metadata for doc in result["source_documents"]],
            "source_documents": result["source_documents"]
        }
    
    def evaluate_retrieval(self, test_questions):
        """Evaluate retrieval quality"""
        results = []
        for question in test_questions:
            docs = self.retriever.get_relevant_documents(question)
            results.append({
                "question": question,
                "retrieved_docs": len(docs),
                "relevance_scores": [doc.metadata.get("score", 0) for doc in docs]
            })
        return results

# Configuration
rag_config = {
    "embedding_type": "openai",
    "vectorstore_type": "faiss",
    "faiss_index_path": "./faiss_index",
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "retrieval_k": 5,
    "fetch_k": 10,
    "openai_api_key": "your-api-key"
}

# Initialize RAG system
rag_system = ProductionRAGSystem(rag_config)

# Add documents
from langchain.document_loaders import DirectoryLoader, TextLoader
loader = DirectoryLoader("./documents", loader_cls=TextLoader)
documents = loader.load()
rag_system.add_documents(documents)

# Query the system
result = rag_system.query("What are the key features of our product?")
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
```

This comprehensive interview questions file covers all major aspects of LangChain for data engineering, including:

1. **Core Concepts**: Components, document loading, LLM providers
2. **Chain Architecture**: Different chain types, custom chains
3. **Memory & Context**: Various memory types, long-term context management
4. **Data Integration**: Database integration, streaming processing
5. **RAG Implementation**: Production-ready RAG systems
6. **Production & Scaling**: Deployment, monitoring, optimization
7. **Advanced Patterns**: Complex workflows, custom implementations

Each question includes detailed explanations and practical code examples that demonstrate real-world usage scenarios for data engineers working with LangChain.