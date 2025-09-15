# LangGraph - Key Concepts

## 🔗 What is LangGraph?

LangGraph is a library for building stateful, multi-actor applications with LLMs, built on top of LangChain. It extends the LangChain Expression Language with:
- **Stateful execution**: Persistent state across interactions
- **Graph-based workflows**: Node and edge-based execution flow
- **Human-in-the-loop**: Built-in approval and feedback mechanisms
- **Multi-agent coordination**: Complex agent interactions and handoffs

## 🏗️ Core Architecture

```
Graph = Nodes + Edges + State + Conditional Logic
```

### Key Components
1. **Nodes**: Individual processing units (agents, tools, functions)
2. **Edges**: Connections between nodes (conditional or direct)
3. **State**: Shared data structure across the graph
4. **Conditional Edges**: Dynamic routing based on state/output
5. **Checkpoints**: State persistence and recovery points

## 📊 Graph Structure

### Basic Graph Example
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class GraphState(TypedDict):
    messages: list
    current_step: str
    data: dict

def agent_node(state: GraphState):
    # Process with LLM agent
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def tool_node(state: GraphState):
    # Execute tool
    result = tool.invoke(state["data"])
    return {"data": result}

# Build graph
workflow = StateGraph(GraphState)
workflow.add_node("agent", agent_node)
workflow.add_node("tool", tool_node)
workflow.add_edge("agent", "tool")
workflow.add_edge("tool", END)

app = workflow.compile()
```

## 🔄 State Management

### State Definition
```python
from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class DataPipelineState(TypedDict):
    messages: Annotated[list, add_messages]
    source_config: dict
    transformation_rules: list
    pipeline_code: str
    validation_results: dict
    deployment_status: str
```

### State Updates
```python
def update_state(current_state, new_data):
    # Merge new data with current state
    return {**current_state, **new_data}

def reducer_function(left, right):
    # Custom state reduction logic
    return {
        "messages": left["messages"] + right["messages"],
        "data": {**left["data"], **right["data"]}
    }
```

## 🎯 Node Types

### 1. **Agent Nodes**
```python
def data_analyst_agent(state):
    prompt = f"""
    Analyze the data source configuration:
    {state['source_config']}
    
    Provide insights and recommendations.
    """
    
    response = llm.invoke(prompt)
    return {
        "messages": [response],
        "analysis_complete": True
    }
```

### 2. **Tool Nodes**
```python
def database_query_node(state):
    query = state["sql_query"]
    results = database.execute(query)
    
    return {
        "query_results": results,
        "data_sample": results[:100]  # First 100 rows
    }
```

### 3. **Human Input Nodes**
```python
def human_approval_node(state):
    # This will pause execution and wait for human input
    return {"approval_pending": True}
```

### 4. **Conditional Nodes**
```python
def route_based_on_quality(state):
    quality_score = state["data_quality_score"]
    
    if quality_score > 0.9:
        return "deploy"
    elif quality_score > 0.7:
        return "review"
    else:
        return "fix_issues"
```

## 🔀 Edge Types

### 1. **Direct Edges**
```python
# Simple sequential flow
workflow.add_edge("extract", "transform")
workflow.add_edge("transform", "load")
```

### 2. **Conditional Edges**
```python
def quality_check_router(state):
    if state["quality_score"] > 0.8:
        return "deploy"
    else:
        return "fix_data"

workflow.add_conditional_edges(
    "quality_check",
    quality_check_router,
    {
        "deploy": "deployment_node",
        "fix_data": "data_cleaning_node"
    }
)
```

### 3. **Dynamic Edges**
```python
def dynamic_routing(state):
    # Route based on runtime conditions
    if state["error_count"] > 5:
        return "error_handler"
    elif state["processing_time"] > 300:
        return "optimization_node"
    else:
        return "continue_processing"
```

## 🔄 Execution Patterns

### 1. **Sequential Processing**
```python
workflow = StateGraph(State)
workflow.add_node("step1", process_step1)
workflow.add_node("step2", process_step2)
workflow.add_node("step3", process_step3)

workflow.add_edge("step1", "step2")
workflow.add_edge("step2", "step3")
workflow.add_edge("step3", END)
```

### 2. **Parallel Processing**
```python
# Fan-out pattern
workflow.add_edge("input", "process_a")
workflow.add_edge("input", "process_b")
workflow.add_edge("input", "process_c")

# Fan-in pattern
workflow.add_edge("process_a", "combine")
workflow.add_edge("process_b", "combine")
workflow.add_edge("process_c", "combine")
```

### 3. **Loop Processing**
```python
def should_continue(state):
    return "continue" if state["iterations"] < 5 else "end"

workflow.add_conditional_edges(
    "processing_node",
    should_continue,
    {
        "continue": "processing_node",  # Loop back
        "end": END
    }
)
```

## 🧠 Memory and Persistence

### Checkpointing
```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Enable state persistence
memory = SqliteSaver.from_conn_string(":memory:")
app = workflow.compile(checkpointer=memory)

# Execute with thread ID for persistence
config = {"configurable": {"thread_id": "pipeline_123"}}
result = app.invoke(initial_state, config)

# Resume from checkpoint
resumed_result = app.invoke(None, config)
```

### State History
```python
# Get execution history
history = app.get_state_history(config)
for checkpoint in history:
    print(f"Step: {checkpoint.metadata['step']}")
    print(f"State: {checkpoint.values}")
```

## 🎯 Data Engineering Use Cases

### 1. **ETL Pipeline Orchestration**
```python
class ETLPipelineState(TypedDict):
    source_data: dict
    transformed_data: dict
    validation_results: dict
    load_status: str

def extract_node(state):
    data = extract_from_source(state["source_config"])
    return {"source_data": data}

def transform_node(state):
    transformed = apply_transformations(
        state["source_data"], 
        state["transformation_rules"]
    )
    return {"transformed_data": transformed}

def validate_node(state):
    results = validate_data_quality(state["transformed_data"])
    return {"validation_results": results}

def load_node(state):
    if state["validation_results"]["passed"]:
        load_to_warehouse(state["transformed_data"])
        return {"load_status": "success"}
    else:
        return {"load_status": "failed"}

# Build ETL workflow
etl_workflow = StateGraph(ETLPipelineState)
etl_workflow.add_node("extract", extract_node)
etl_workflow.add_node("transform", transform_node)
etl_workflow.add_node("validate", validate_node)
etl_workflow.add_node("load", load_node)

etl_workflow.add_edge("extract", "transform")
etl_workflow.add_edge("transform", "validate")
etl_workflow.add_conditional_edges(
    "validate",
    lambda state: "load" if state["validation_results"]["passed"] else END,
    {"load": "load"}
)
```

### 2. **Multi-Agent Data Analysis**
```python
def data_profiler_agent(state):
    profile = analyze_data_profile(state["dataset"])
    return {"data_profile": profile}

def anomaly_detector_agent(state):
    anomalies = detect_anomalies(state["dataset"])
    return {"anomalies": anomalies}

def insight_generator_agent(state):
    insights = generate_insights(
        state["data_profile"], 
        state["anomalies"]
    )
    return {"insights": insights}

def coordinator_agent(state):
    # Coordinate between agents
    if not state.get("data_profile"):
        return "profiler"
    elif not state.get("anomalies"):
        return "detector"
    elif not state.get("insights"):
        return "generator"
    else:
        return "report"

analysis_workflow = StateGraph(AnalysisState)
analysis_workflow.add_node("profiler", data_profiler_agent)
analysis_workflow.add_node("detector", anomaly_detector_agent)
analysis_workflow.add_node("generator", insight_generator_agent)
analysis_workflow.add_node("coordinator", coordinator_agent)

analysis_workflow.add_conditional_edges(
    "coordinator",
    coordinator_agent,
    {
        "profiler": "profiler",
        "detector": "detector", 
        "generator": "generator",
        "report": END
    }
)
```

### 3. **Real-time Stream Processing**
```python
class StreamState(TypedDict):
    batch_data: list
    processed_data: list
    alerts: list
    metrics: dict

def stream_ingestion_node(state):
    # Consume from Kafka
    batch = consume_kafka_batch()
    return {"batch_data": batch}

def processing_node(state):
    processed = process_stream_batch(state["batch_data"])
    return {"processed_data": processed}

def alerting_node(state):
    alerts = check_for_alerts(state["processed_data"])
    return {"alerts": alerts}

def metrics_node(state):
    metrics = calculate_metrics(state["processed_data"])
    return {"metrics": metrics}

stream_workflow = StateGraph(StreamState)
stream_workflow.add_node("ingest", stream_ingestion_node)
stream_workflow.add_node("process", processing_node)
stream_workflow.add_node("alert", alerting_node)
stream_workflow.add_node("metrics", metrics_node)

# Parallel processing after ingestion
stream_workflow.add_edge("ingest", "process")
stream_workflow.add_edge("process", "alert")
stream_workflow.add_edge("process", "metrics")
```

## 🔧 Advanced Features

### 1. **Human-in-the-Loop**
```python
from langgraph.prebuilt import create_react_agent

def human_approval_required(state):
    return state["risk_level"] == "HIGH"

workflow.add_conditional_edges(
    "risk_assessment",
    human_approval_required,
    {
        True: "human_approval",
        False: "auto_proceed"
    }
)

# Human approval node
def human_approval_node(state):
    # This pauses execution until human input
    approval = input(f"Approve action: {state['proposed_action']}? (y/n): ")
    return {"approved": approval.lower() == 'y'}
```

### 2. **Error Handling and Recovery**
```python
def error_handler_node(state):
    error = state.get("error")
    
    if error["type"] == "connection_error":
        # Retry with backoff
        return {"retry_count": state.get("retry_count", 0) + 1}
    elif error["type"] == "data_quality_error":
        # Route to data cleaning
        return {"route_to": "data_cleaning"}
    else:
        # Escalate to human
        return {"escalate": True}

def should_retry(state):
    return (state.get("retry_count", 0) < 3 and 
            state.get("error", {}).get("type") == "connection_error")

workflow.add_conditional_edges(
    "error_handler",
    should_retry,
    {
        True: "retry_operation",
        False: "escalate_error"
    }
)
```

### 3. **Dynamic Graph Modification**
```python
def adaptive_workflow(state):
    # Modify graph based on runtime conditions
    if state["data_size"] > 1000000:
        # Add parallel processing nodes
        workflow.add_node("parallel_process_1", process_chunk_1)
        workflow.add_node("parallel_process_2", process_chunk_2)
        workflow.add_edge("split_data", "parallel_process_1")
        workflow.add_edge("split_data", "parallel_process_2")
    
    return state
```

## 📊 Monitoring and Observability

### Execution Tracking
```python
def track_execution(state, node_name):
    metrics = {
        "node": node_name,
        "timestamp": datetime.now(),
        "state_size": len(str(state)),
        "execution_time": time.time()
    }
    
    # Log to monitoring system
    logger.info("Node execution", extra=metrics)
    
    return state

# Wrap nodes with tracking
def tracked_node(original_node):
    def wrapper(state):
        start_time = time.time()
        result = original_node(state)
        duration = time.time() - start_time
        
        track_execution(result, original_node.__name__)
        return result
    
    return wrapper
```

### Performance Monitoring
```python
class GraphMonitor:
    def __init__(self):
        self.execution_times = {}
        self.state_sizes = {}
        self.error_counts = {}
    
    def monitor_node(self, node_name, state, duration):
        self.execution_times[node_name] = duration
        self.state_sizes[node_name] = len(str(state))
    
    def get_performance_report(self):
        return {
            "avg_execution_time": np.mean(list(self.execution_times.values())),
            "max_state_size": max(self.state_sizes.values()),
            "total_errors": sum(self.error_counts.values())
        }
```

## 🚀 Best Practices

### 1. **State Design**
- Keep state minimal and focused
- Use typed dictionaries for clarity
- Implement proper state reducers
- Consider state serialization

### 2. **Node Design**
- Make nodes pure functions when possible
- Handle errors gracefully
- Keep nodes focused on single responsibilities
- Use proper typing

### 3. **Graph Structure**
- Design clear execution flows
- Use conditional edges for dynamic routing
- Implement proper error handling paths
- Consider parallel execution opportunities

### 4. **Performance Optimization**
- Use checkpointing for long-running workflows
- Implement proper caching strategies
- Monitor state size growth
- Optimize node execution times

## 🔗 Resources

### Official Documentation
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub Repository](https://github.com/langchain-ai/langgraph)

### Tutorials and Examples
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)
- [Multi-Agent Examples](https://github.com/langchain-ai/langgraph/tree/main/examples)
- [Human-in-the-Loop Patterns](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/)

### Community Resources
- [LangChain Community Discord](https://discord.gg/langchain)
- [LangGraph Examples Repository](https://github.com/langchain-ai/langgraph-example)
- [LangChain Blog](https://blog.langchain.dev/)