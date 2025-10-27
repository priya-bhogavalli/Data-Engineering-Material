# 🔗 LangChain & LangGraph - Key Concepts

## 🎯 **Real-World Analogy: The AI Application Assembly Line**

> **Think of LangChain as a factory assembly line for AI applications, where LangGraph is the advanced workflow manager that can handle complex, branching processes with decision points and loops.**

## 🔥 **Core Concepts**

### 1. **LangChain Fundamentals** ⛓️

```python
# Basic LangChain components
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Simple chain
llm = OpenAI(temperature=0.7)
prompt = PromptTemplate(
    input_variables=["product"],
    template="Write a product description for {product}"
)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("wireless headphones")
```

### 2. **LangGraph Workflows** 📊

```python
# Advanced workflow with decision points
from langgraph.graph import StateGraph, END

class AgentState:
    messages: list
    next_action: str

def analyze_query(state):
    if "technical" in state.messages[-1]:
        return {"next_action": "technical_search"}
    return {"next_action": "general_search"}

def route_query(state):
    if state.next_action == "technical_search":
        return "technical_agent"
    return "general_agent"

# Build workflow
workflow = StateGraph(AgentState)
workflow.add_node("analyzer", analyze_query)
workflow.add_node("technical_agent", technical_search)
workflow.add_node("general_agent", general_search)

workflow.add_conditional_edges(
    "analyzer", 
    route_query,
    {"technical_agent": "technical_agent", "general_agent": "general_agent"}
)
```

### 3. **Production Patterns** 🚀

```python
# Enterprise-ready LangChain application
class ProductionLangChainApp:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.memory = ConversationBufferWindowMemory(k=10)
        self.tools = [SearchTool(), DatabaseTool(), CalculatorTool()]
        
    def create_agent(self):
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    async def process_request(self, user_input):
        try:
            agent = self.create_agent()
            response = await agent.arun(user_input)
            return {"status": "success", "response": response}
        except Exception as e:
            return {"status": "error", "message": str(e)}
```

## 🛠️ **Key Components**

### **Chains vs Agents vs Workflows**
- **Chains**: Linear sequence (A → B → C)
- **Agents**: Dynamic tool selection based on input
- **Workflows**: Complex branching with state management

### **Memory Management**
```python
# Different memory types
memory_types = {
    "ConversationBufferMemory": "Store all messages",
    "ConversationBufferWindowMemory": "Store last K messages", 
    "ConversationSummaryMemory": "Summarize old messages",
    "VectorStoreRetrieverMemory": "Semantic search in history"
}
```

### **Tool Integration**
```python
# Custom tool creation
@tool
def database_query(query: str) -> str:
    """Execute SQL query on database"""
    return execute_sql(query)

@tool  
def api_call(endpoint: str, params: dict) -> str:
    """Make API call to external service"""
    return requests.get(endpoint, params=params).json()
```