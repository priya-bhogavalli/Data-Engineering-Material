# OpenAI API Key Concepts

## 1. AI-Powered API Platform
**What it is**: RESTful API service providing access to OpenAI's large language models and AI capabilities.

**Core Models**:
- **GPT-4**: Most capable model for complex tasks
- **GPT-3.5-turbo**: Fast and efficient for most use cases
- **DALL-E**: Image generation from text descriptions
- **Whisper**: Speech-to-text transcription
- **Embeddings**: Text similarity and search

## 2. Authentication and Setup
**API Key Management**:
```python
import openai
import os

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Alternative: Direct assignment (not recommended for production)
openai.api_key = "sk-your-api-key-here"

# Using OpenAI Python client (v1.0+)
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

**Environment Setup**:
```bash
# Install OpenAI library
pip install openai

# Set environment variable
export OPENAI_API_KEY="sk-your-api-key-here"

# Or in .env file
OPENAI_API_KEY=sk-your-api-key-here
```

## 3. Chat Completions API
**Basic Chat Completion**:
```python
# Using new client (v1.0+)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful data analyst."},
        {"role": "user", "content": "Explain what is ETL in data engineering."}
    ],
    max_tokens=150,
    temperature=0.7
)

print(response.choices[0].message.content)
```

**Message Roles**:
```python
messages = [
    {
        "role": "system", 
        "content": "You are an expert data engineer specializing in Python and SQL."
    },
    {
        "role": "user", 
        "content": "How do I optimize a slow SQL query?"
    },
    {
        "role": "assistant", 
        "content": "Here are key strategies to optimize SQL queries..."
    },
    {
        "role": "user", 
        "content": "Can you show me an example with indexes?"
    }
]
```

## 4. Model Parameters
**Key Parameters**:
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=0.7,        # Creativity (0-2, default: 1)
    max_tokens=500,         # Response length limit
    top_p=0.9,             # Nucleus sampling (0-1)
    frequency_penalty=0.0,  # Reduce repetition (-2 to 2)
    presence_penalty=0.0,   # Encourage new topics (-2 to 2)
    stop=["END", "\n\n"]   # Stop sequences
)
```

**Parameter Effects**:
```yaml
# Temperature
0.0: Deterministic, focused responses
0.7: Balanced creativity and coherence  
1.5: More creative and varied responses

# Max Tokens
- Controls response length
- Includes both prompt and completion
- GPT-4: up to 8,192 tokens
- GPT-3.5-turbo: up to 4,096 tokens
```

## 5. Function Calling
**Function Definition**:
```python
functions = [
    {
        "name": "get_database_schema",
        "description": "Get the schema of a database table",
        "parameters": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "Name of the database table"
                },
                "database": {
                    "type": "string", 
                    "description": "Database name"
                }
            },
            "required": ["table_name"]
        }
    }
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "What's the schema of the users table?"}
    ],
    functions=functions,
    function_call="auto"
)
```

**Function Execution**:
```python
import json

def get_database_schema(table_name, database="default"):
    # Your database schema retrieval logic
    return {
        "table": table_name,
        "columns": ["id", "name", "email", "created_at"],
        "types": ["int", "varchar", "varchar", "timestamp"]
    }

# Check if function was called
if response.choices[0].message.function_call:
    function_name = response.choices[0].message.function_call.name
    arguments = json.loads(response.choices[0].message.function_call.arguments)
    
    if function_name == "get_database_schema":
        result = get_database_schema(**arguments)
        
        # Send result back to model
        messages.append({
            "role": "function",
            "name": function_name,
            "content": json.dumps(result)
        })
```

## 6. Embeddings API
**Text Embeddings**:
```python
# Generate embeddings
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="Data engineering involves building systems for data collection and processing"
)

embedding = response.data[0].embedding
print(f"Embedding dimension: {len(embedding)}")  # 1536 dimensions
```

**Similarity Search**:
```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity(text1, text2):
    # Get embeddings for both texts
    response1 = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text1
    )
    response2 = client.embeddings.create(
        model="text-embedding-ada-002", 
        input=text2
    )
    
    emb1 = np.array(response1.data[0].embedding).reshape(1, -1)
    emb2 = np.array(response2.data[0].embedding).reshape(1, -1)
    
    return cosine_similarity(emb1, emb2)[0][0]

similarity = get_similarity(
    "Data engineering and ETL processes",
    "Building data pipelines and transformations"
)
```

## 7. Image Generation (DALL-E)
**Image Creation**:
```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A modern data center with servers and network cables, digital art style",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
print(f"Generated image: {image_url}")
```

**Image Variations**:
```python
# Create variations of existing image
response = client.images.create_variation(
    image=open("original_image.png", "rb"),
    n=2,
    size="1024x1024"
)

for i, image in enumerate(response.data):
    print(f"Variation {i+1}: {image.url}")
```

## 8. Audio Processing (Whisper)
**Speech-to-Text**:
```python
# Transcribe audio file
with open("meeting_recording.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )

print(transcript)
```

**Audio Translation**:
```python
# Translate non-English audio to English
with open("spanish_audio.mp3", "rb") as audio_file:
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )

print(translation.text)
```

## 9. Error Handling and Rate Limits
**Error Handling**:
```python
from openai import OpenAIError, RateLimitError, APIError

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    print("Rate limit exceeded. Please wait.")
except APIError as e:
    print(f"API error: {e}")
except OpenAIError as e:
    print(f"OpenAI error: {e}")
```

**Rate Limiting**:
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def make_api_call(messages):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

# Usage with automatic retry
response = make_api_call([
    {"role": "user", "content": "Explain database indexing"}
])
```

## 10. Streaming Responses
**Stream Chat Completion**:
```python
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Write a Python function to connect to PostgreSQL"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
```

**Async Streaming**:
```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def stream_response():
    stream = await async_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Explain data warehousing"}],
        stream=True
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

asyncio.run(stream_response())
```

## 11. Cost Management
**Token Counting**:
```python
import tiktoken

def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Estimate cost before API call
prompt = "Explain machine learning algorithms"
token_count = count_tokens(prompt)
print(f"Estimated tokens: {token_count}")

# Pricing (as of 2024)
# GPT-3.5-turbo: $0.0015/1K input tokens, $0.002/1K output tokens
# GPT-4: $0.03/1K input tokens, $0.06/1K output tokens
```

**Usage Monitoring**:
```python
def track_usage(response):
    usage = response.usage
    print(f"Prompt tokens: {usage.prompt_tokens}")
    print(f"Completion tokens: {usage.completion_tokens}")
    print(f"Total tokens: {usage.total_tokens}")
    
    # Calculate approximate cost (GPT-3.5-turbo)
    input_cost = usage.prompt_tokens * 0.0015 / 1000
    output_cost = usage.completion_tokens * 0.002 / 1000
    total_cost = input_cost + output_cost
    print(f"Estimated cost: ${total_cost:.6f}")
```

## 12. Best Practices
**Prompt Engineering**:
```python
# Good prompt structure
system_prompt = """You are an expert data engineer. 
Provide clear, practical answers with code examples when relevant.
Focus on best practices and real-world applications."""

user_prompt = """I need to design a data pipeline that:
1. Extracts data from multiple APIs
2. Transforms the data for analytics
3. Loads it into a data warehouse

Please provide a high-level architecture and Python code examples."""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]
```

**Security Considerations**:
```python
# Never log API keys
import logging
logging.getLogger("openai").setLevel(logging.WARNING)

# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sanitize user inputs
def sanitize_input(user_input):
    # Remove potential injection attempts
    forbidden_patterns = ["ignore previous", "system:", "assistant:"]
    for pattern in forbidden_patterns:
        if pattern.lower() in user_input.lower():
            return "Invalid input detected"
    return user_input
```