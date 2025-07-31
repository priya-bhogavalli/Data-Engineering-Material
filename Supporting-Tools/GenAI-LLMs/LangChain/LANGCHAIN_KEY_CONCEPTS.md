# LangChain Key Concepts

## 1. LangChain Fundamentals
**What is LangChain**: Framework for developing applications powered by language models.

**Core Components**:
- **LLMs**: Large Language Model interfaces
- **Prompts**: Template management for model inputs
- **Chains**: Combine LLMs with other components
- **Agents**: Use LLMs to decide actions
- **Memory**: Persist state between calls
- **Retrievers**: Interface with external data

## 2. LLMs and Chat Models
```python
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Basic LLM
llm = OpenAI(temperature=0.7, max_tokens=100)
response = llm("What is data engineering?")

# Chat model
chat = ChatOpenAI(temperature=0)
messages = [
    SystemMessage(content="You are a data engineering expert."),
    HumanMessage(content="Explain ETL processes.")
]
response = chat(messages)

# Streaming responses
for chunk in llm.stream("Explain machine learning"):
    print(chunk, end="", flush=True)
```

## 3. Prompt Templates
```python
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate

# Basic prompt template
template = """
You are a data analyst. Given the following data:
{data}

Question: {question}
Answer:
"""

prompt = PromptTemplate(
    input_variables=["data", "question"],
    template=template
)

# Chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful data engineering assistant."),
    ("human", "How do I optimize this SQL query: {query}?")
])

# Few-shot prompting
examples = [
    {
        "query": "SELECT * FROM users WHERE age > 25",
        "optimization": "Add index on age column: CREATE INDEX idx_users_age ON users(age)"
    },
    {
        "query": "SELECT COUNT(*) FROM orders GROUP BY customer_id",
        "optimization": "Consider using window functions for better performance"
    }
]

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate(
        input_variables=["query", "optimization"],
        template="Query: {query}\nOptimization: {optimization}"
    ),
    prefix="Here are examples of SQL query optimizations:",
    suffix="Query: {input}\nOptimization:",
    input_variables=["input"]
)
```

## 4. Chains
```python
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.chains.summarize import load_summarize_chain

# Basic LLM Chain
llm_chain = LLMChain(llm=llm, prompt=prompt)
result = llm_chain.run(data="sales_data.csv", question="What are the trends?")

# Sequential chains
# Chain 1: Generate SQL query
sql_prompt = PromptTemplate(
    input_variables=["question"],
    template="Generate SQL query for: {question}"
)
sql_chain = LLMChain(llm=llm, prompt=sql_prompt, output_key="sql_query")

# Chain 2: Explain the query
explain_prompt = PromptTemplate(
    input_variables=["sql_query"],
    template="Explain this SQL query: {sql_query}"
)
explain_chain = LLMChain(llm=llm, prompt=explain_prompt, output_key="explanation")

# Combine chains
overall_chain = SequentialChain(
    chains=[sql_chain, explain_chain],
    input_variables=["question"],
    output_variables=["sql_query", "explanation"]
)

# Document summarization
docs = [Document(page_content="Long document text...")]
summarize_chain = load_summarize_chain(llm, chain_type="map_reduce")
summary = summarize_chain.run(docs)
```

## 5. Memory
```python
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.memory import ConversationBufferWindowMemory

# Buffer memory - stores all conversation
memory = ConversationBufferMemory()
memory.save_context(
    {"input": "What is Apache Spark?"}, 
    {"output": "Apache Spark is a distributed computing framework..."}
)

# Window memory - keeps last k interactions
window_memory = ConversationBufferWindowMemory(k=5)

# Summary memory - summarizes old conversations
summary_memory = ConversationSummaryMemory(llm=llm)

# Using memory in chains
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

response1 = conversation.predict(input="What is data warehousing?")
response2 = conversation.predict(input="How does it relate to ETL?")

# Custom memory
from langchain.schema import BaseMemory

class DataEngineeringMemory(BaseMemory):
    def __init__(self):
        self.context = {}
    
    def save_context(self, inputs, outputs):
        # Save relevant data engineering context
        if "database" in inputs.get("input", "").lower():
            self.context["last_database_topic"] = inputs["input"]
    
    def load_memory_variables(self, inputs):
        return {"context": self.context}
```

## 6. Retrievers and Vector Stores
```python
from langchain.vectorstores import Chroma, FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# Load and split documents
loader = TextLoader("data_engineering_docs.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
texts = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# Similarity search
docs = vectorstore.similarity_search("What is ETL?", k=3)

# Retriever interface
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
relevant_docs = retriever.get_relevant_documents("data pipeline optimization")

# Custom retriever
from langchain.schema import BaseRetriever

class SQLDocumentRetriever(BaseRetriever):
    def __init__(self, sql_docs):
        self.sql_docs = sql_docs
    
    def get_relevant_documents(self, query):
        # Custom logic to find relevant SQL documentation
        relevant = []
        for doc in self.sql_docs:
            if any(keyword in doc.page_content.lower() 
                   for keyword in query.lower().split()):
                relevant.append(doc)
        return relevant[:3]
```

## 7. Agents
```python
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import DuckDuckGoSearchRun

# Define tools
search = DuckDuckGoSearchRun()

def sql_query_tool(query: str) -> str:
    """Execute SQL queries on the database"""
    # Connect to database and execute query
    return f"Query result for: {query}"

def data_analysis_tool(data: str) -> str:
    """Analyze data and provide insights"""
    # Perform data analysis
    return f"Analysis of: {data}"

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Search for current information about data engineering topics"
    ),
    Tool(
        name="SQL Query",
        func=sql_query_tool,
        description="Execute SQL queries on the database"
    ),
    Tool(
        name="Data Analysis",
        func=data_analysis_tool,
        description="Analyze data and provide insights"
    )
]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use agent
response = agent.run("Find the latest trends in data engineering and analyze our sales data")

# Custom agent
from langchain.agents import BaseSingleActionAgent

class DataEngineeringAgent(BaseSingleActionAgent):
    def plan(self, intermediate_steps, **kwargs):
        # Custom planning logic for data engineering tasks
        return AgentAction(tool="SQL Query", tool_input="SELECT * FROM metrics", log="")
```

## 8. RAG (Retrieval Augmented Generation)
```python
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

# Basic RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

result = qa_chain({"query": "How to optimize Spark performance?"})
print(result["result"])
print("Sources:", result["source_documents"])

# Custom RAG with prompt
template = """
Use the following pieces of context to answer the question about data engineering.
If you don't know the answer, just say that you don't know.

Context: {context}

Question: {question}
Answer:
"""

QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

# Multi-query retrieval
from langchain.retrievers.multi_query import MultiQueryRetriever

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

docs = multi_query_retriever.get_relevant_documents("data pipeline best practices")
```

## 9. Output Parsers
```python
from langchain.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser
from langchain.schema import OutputParserException
from pydantic import BaseModel, Field

# Pydantic parser
class DataPipelineAnalysis(BaseModel):
    pipeline_name: str = Field(description="Name of the data pipeline")
    bottlenecks: list = Field(description="List of performance bottlenecks")
    recommendations: list = Field(description="List of optimization recommendations")
    estimated_improvement: str = Field(description="Estimated performance improvement")

parser = PydanticOutputParser(pydantic_object=DataPipelineAnalysis)

prompt = PromptTemplate(
    template="Analyze the following data pipeline and provide recommendations.\n{format_instructions}\n{query}",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# List parser
list_parser = CommaSeparatedListOutputParser()
list_prompt = PromptTemplate(
    template="List the top 5 data engineering tools.\n{format_instructions}",
    input_variables=[],
    partial_variables={"format_instructions": list_parser.get_format_instructions()}
)

# Custom parser
class SQLQueryParser:
    def parse(self, text: str) -> dict:
        # Extract SQL query from LLM response
        import re
        sql_match = re.search(r'```sql\n(.*?)\n```', text, re.DOTALL)
        if sql_match:
            return {"query": sql_match.group(1).strip()}
        return {"query": None, "error": "No SQL query found"}
```

## 10. Advanced Patterns
```python
# Callback handlers for monitoring
from langchain.callbacks import StdOutCallbackHandler

class DataEngineeringCallbackHandler(StdOutCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"Starting LLM with prompts: {prompts}")
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"Starting chain: {serialized.get('name', 'Unknown')}")

# Error handling and retries
from langchain.llms.base import LLM
import time

class ReliableLLM(LLM):
    def __init__(self, base_llm, max_retries=3):
        self.base_llm = base_llm
        self.max_retries = max_retries
    
    def _call(self, prompt, stop=None):
        for attempt in range(self.max_retries):
            try:
                return self.base_llm(prompt, stop=stop)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff

# Async operations
import asyncio
from langchain.llms import OpenAI

async def process_multiple_queries():
    llm = OpenAI()
    queries = [
        "What is Apache Kafka?",
        "Explain data warehousing",
        "How does Spark work?"
    ]
    
    tasks = [llm.agenerate([query]) for query in queries]
    results = await asyncio.gather(*tasks)
    return results

# Custom chain for data engineering workflows
class DataPipelineChain:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def run(self, pipeline_config):
        # 1. Analyze pipeline configuration
        analysis = self.llm(f"Analyze this pipeline: {pipeline_config}")
        
        # 2. Generate optimizations
        optimizations = self.llm(f"Suggest optimizations for: {analysis}")
        
        # 3. Create implementation plan
        plan = self.llm(f"Create implementation plan: {optimizations}")
        
        return {
            "analysis": analysis,
            "optimizations": optimizations,
            "implementation_plan": plan
        }
```