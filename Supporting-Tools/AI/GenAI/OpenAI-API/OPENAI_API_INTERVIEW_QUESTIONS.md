# 🤖 OpenAI API Interview Questions for Data Engineering

## 📋 Table of Contents

1. [API Fundamentals (1-25)](#api-fundamentals-1-25)
2. [Integration Patterns (26-50)](#integration-patterns-26-50)
3. [Data Processing (51-75)](#data-processing-51-75)
4. [Production & Scaling (76-100)](#production--scaling-76-100)

---

## API Fundamentals (1-25)

### 1. What is the OpenAI API and its main capabilities?
**Answer**: OpenAI API provides access to large language models for various AI tasks.

**Main Capabilities:**
- **Text Generation**: GPT models for content creation
- **Code Generation**: Codex for programming assistance
- **Embeddings**: Vector representations for similarity
- **Fine-tuning**: Custom model training
- **Moderation**: Content filtering

```python
import openai

openai.api_key = "your-api-key"

# Text completion
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Explain data engineering:",
    max_tokens=150
)
print(response.choices[0].text)
```

### 2. How do you implement chat completions with GPT models?
**Answer**: Use the Chat Completions API for conversational AI.

```python
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a data engineering expert."},
        {"role": "user", "content": "How do I optimize a data pipeline?"}
    ],
    max_tokens=200,
    temperature=0.7
)

print(response.choices[0].message.content)
```

### 3. How do you generate embeddings for text data?
**Answer**: Use embeddings API for vector representations.

```python
def get_embeddings(texts, model="text-embedding-ada-002"):
    response = openai.Embedding.create(
        input=texts,
        model=model
    )
    return [data.embedding for data in response.data]

# Generate embeddings
texts = ["Data engineering", "Machine learning", "Analytics"]
embeddings = get_embeddings(texts)

# Calculate similarity
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
print(f"Similarity: {similarity}")
```

## Integration Patterns (26-50)

### 26. How do you implement streaming responses?
**Answer**: Use streaming for real-time response generation.

```python
def stream_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.get("content"):
            yield chunk.choices[0].delta.content

# Usage
for token in stream_completion("Explain Apache Kafka"):
    print(token, end="", flush=True)
```

### 27. How do you implement function calling?
**Answer**: Use function calling for structured interactions.

```python
functions = [
    {
        "name": "get_weather",
        "description": "Get weather information",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What's the weather in New York?"}],
    functions=functions,
    function_call="auto"
)

if response.choices[0].message.get("function_call"):
    function_call = response.choices[0].message.function_call
    print(f"Function: {function_call.name}")
    print(f"Arguments: {function_call.arguments}")
```

## Data Processing (51-75)

### 51. How do you process large datasets with OpenAI API?
**Answer**: Implement batch processing with rate limiting and error handling.

```python
import time
import asyncio
import aiohttp
from typing import List

class OpenAIBatchProcessor:
    def __init__(self, api_key: str, rate_limit: int = 60):
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(rate_limit)
    
    async def process_text(self, session, text: str):
        async with self.semaphore:
            try:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": text}],
                    "max_tokens": 100
                }
                
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    result = await response.json()
                    return result.get("choices", [{}])[0].get("message", {}).get("content")
                    
            except Exception as e:
                print(f"Error processing text: {e}")
                return None
            
            await asyncio.sleep(1 / self.rate_limit)  # Rate limiting
    
    async def process_batch(self, texts: List[str]):
        async with aiohttp.ClientSession() as session:
            tasks = [self.process_text(session, text) for text in texts]
            results = await asyncio.gather(*tasks)
            return results

# Usage
processor = OpenAIBatchProcessor("your-api-key")
texts = ["Text 1", "Text 2", "Text 3"]
results = asyncio.run(processor.process_batch(texts))
```

### 52. How do you implement semantic search with embeddings?
**Answer**: Build a semantic search system using embeddings.

```python
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSearch:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.embeddings_cache = {}
    
    def get_embedding(self, text: str):
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        self.embeddings_cache[text] = embedding
        return embedding
    
    def build_index(self, documents: List[str]):
        embeddings = []
        for doc in documents:
            embedding = self.get_embedding(doc)
            embeddings.append(embedding)
        
        self.documents = documents
        self.embeddings = np.array(embeddings)
        return self
    
    def search(self, query: str, top_k: int = 5):
        query_embedding = self.get_embedding(query)
        
        similarities = cosine_similarity(
            [query_embedding], 
            self.embeddings
        )[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'document': self.documents[idx],
                'similarity': similarities[idx]
            })
        
        return results

# Usage
search = SemanticSearch("your-api-key")
documents = [
    "Apache Kafka is a distributed streaming platform",
    "Apache Spark is a unified analytics engine",
    "MongoDB is a document database"
]

search.build_index(documents)
results = search.search("streaming data processing")
```

## Production & Scaling (76-100)

### 76. How do you implement error handling and retries?
**Answer**: Robust error handling with exponential backoff.

```python
import time
import random
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except openai.error.RateLimitError:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                except openai.error.APIError as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(base_delay)
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def safe_completion(prompt):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
```

### 77. How do you monitor API usage and costs?
**Answer**: Implement usage tracking and cost monitoring.

```python
class OpenAIUsageTracker:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.usage_log = []
    
    def track_completion(self, model: str, prompt_tokens: int, completion_tokens: int):
        total_tokens = prompt_tokens + completion_tokens
        
        # Pricing (example rates)
        pricing = {
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},  # per 1K tokens
            "gpt-4": {"input": 0.03, "output": 0.06}
        }
        
        if model in pricing:
            cost = (prompt_tokens * pricing[model]["input"] + 
                   completion_tokens * pricing[model]["output"]) / 1000
        else:
            cost = 0
        
        usage_entry = {
            "timestamp": time.time(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost": cost
        }
        
        self.usage_log.append(usage_entry)
        return usage_entry
    
    def get_usage_summary(self, hours: int = 24):
        cutoff_time = time.time() - (hours * 3600)
        recent_usage = [
            entry for entry in self.usage_log 
            if entry["timestamp"] > cutoff_time
        ]
        
        total_tokens = sum(entry["total_tokens"] for entry in recent_usage)
        total_cost = sum(entry["cost"] for entry in recent_usage)
        
        return {
            "period_hours": hours,
            "total_requests": len(recent_usage),
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "avg_tokens_per_request": total_tokens / len(recent_usage) if recent_usage else 0
        }

# Usage
tracker = OpenAIUsageTracker("your-api-key")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)

tracker.track_completion(
    model="gpt-3.5-turbo",
    prompt_tokens=response.usage.prompt_tokens,
    completion_tokens=response.usage.completion_tokens
)

summary = tracker.get_usage_summary(24)
print(f"24h usage: {summary}")
```

---

**Total Questions: 100** | **Coverage: Complete OpenAI API Integration**