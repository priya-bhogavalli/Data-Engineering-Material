# 🎯 Generative AI - Best Practices Guide

> **Production-ready GenAI implementation strategies for data engineering teams**

## 🏗️ **Architecture Best Practices**

### 🔒 **Security First**
```yaml
Input Validation:
  - Sanitize all user inputs
  - Implement prompt injection detection
  - Set maximum input length limits
  - Validate data types and formats

API Security:
  - Use environment variables for API keys
  - Implement API key rotation
  - Set up rate limiting per user/service
  - Monitor API usage patterns

Data Protection:
  - Never send PII to external APIs
  - Implement data masking techniques
  - Use on-premises models for sensitive data
  - Maintain audit logs for compliance
```

### ⚡ **Performance Optimization**
```python
# Smart model routing based on complexity
def route_request(query_complexity: str, budget: str) -> str:
    routing_matrix = {
        ("simple", "low"): "gpt-3.5-turbo",
        ("simple", "high"): "claude-3-haiku", 
        ("medium", "low"): "gpt-3.5-turbo",
        ("medium", "high"): "gpt-4-turbo",
        ("complex", "any"): "gpt-4-turbo"
    }
    return routing_matrix.get((query_complexity, budget), "gpt-3.5-turbo")

# Implement caching for common queries
import hashlib
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_ai_response(prompt_hash: str) -> str:
    # Cache responses based on prompt similarity
    pass
```

## 🎯 **Prompt Engineering Excellence**

### 📝 **Template Standards**
```python
STANDARD_PROMPT_TEMPLATE = """
Role: {role_description}
Task: {specific_task}
Context: {relevant_context}
Requirements:
{numbered_requirements}
Format: {output_format}
Constraints: {limitations}

Input: {user_input}
Output:
"""

# Example implementation
def create_sql_prompt(requirement: str, schema: dict) -> str:
    return STANDARD_PROMPT_TEMPLATE.format(
        role_description="Senior Database Engineer with 10+ years PostgreSQL experience",
        specific_task="Convert business requirement to optimized SQL query",
        relevant_context=f"Database schema: {schema}",
        numbered_requirements="""
1. Generate syntactically correct PostgreSQL
2. Optimize for performance using indexes
3. Include proper error handling
4. Add explanatory comments
5. Follow snake_case naming conventions""",
        output_format="SQL query with comments",
        limitations="No DDL statements, SELECT queries only",
        user_input=requirement
    )
```

### 🧠 **Advanced Techniques**
```python
# Chain of Thought for complex problems
COT_TEMPLATE = """
Problem: {problem}

Let me solve this step by step:

Step 1: Understanding
{understanding_prompt}

Step 2: Analysis  
{analysis_prompt}

Step 3: Solution
{solution_prompt}

Step 4: Validation
{validation_prompt}

Final Answer:
"""

# Few-shot learning with examples
FEW_SHOT_TEMPLATE = """
Here are examples of {task_type}:

Example 1:
Input: {example1_input}
Output: {example1_output}

Example 2:
Input: {example2_input}  
Output: {example2_output}

Now solve:
Input: {new_input}
Output:
"""
```

## 🔍 **Quality Assurance Framework**

### ✅ **Testing Strategy**
```python
class AIQualityTester:
    def __init__(self):
        self.test_cases = []
        
    def add_test_case(self, input_data: str, expected_output: str, 
                     validation_func: callable = None):
        self.test_cases.append({
            'input': input_data,
            'expected': expected_output,
            'validator': validation_func
        })
    
    def run_tests(self, ai_function: callable) -> dict:
        results = {'passed': 0, 'failed': 0, 'details': []}
        
        for test in self.test_cases:
            try:
                actual = ai_function(test['input'])
                
                if test['validator']:
                    passed = test['validator'](actual, test['expected'])
                else:
                    passed = actual.strip() == test['expected'].strip()
                
                if passed:
                    results['passed'] += 1
                else:
                    results['failed'] += 1
                    results['details'].append({
                        'input': test['input'],
                        'expected': test['expected'],
                        'actual': actual
                    })
                    
            except Exception as e:
                results['failed'] += 1
                results['details'].append({
                    'input': test['input'],
                    'error': str(e)
                })
        
        return results

# SQL validation example
def validate_sql(generated_sql: str, expected_pattern: str) -> bool:
    import sqlparse
    try:
        parsed = sqlparse.parse(generated_sql)
        return len(parsed) > 0 and expected_pattern.lower() in generated_sql.lower()
    except:
        return False
```

### 📊 **Monitoring & Metrics**
```python
import time
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AIMetrics:
    response_time: float
    token_count: int
    cost: float
    quality_score: float
    user_satisfaction: float

class AIMonitor:
    def __init__(self):
        self.metrics: List[AIMetrics] = []
        
    def track_request(self, start_time: float, tokens: int, 
                     cost: float, quality: float = None):
        response_time = time.time() - start_time
        
        metric = AIMetrics(
            response_time=response_time,
            token_count=tokens,
            cost=cost,
            quality_score=quality or 0.0,
            user_satisfaction=0.0  # To be updated with feedback
        )
        
        self.metrics.append(metric)
        
    def get_performance_summary(self) -> Dict:
        if not self.metrics:
            return {}
            
        return {
            'avg_response_time': sum(m.response_time for m in self.metrics) / len(self.metrics),
            'total_cost': sum(m.cost for m in self.metrics),
            'avg_quality': sum(m.quality_score for m in self.metrics) / len(self.metrics),
            'total_requests': len(self.metrics)
        }
```

## 🛡️ **Error Handling & Resilience**

### 🔄 **Retry Logic**
```python
import time
import random
from functools import wraps

def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    # Exponential backoff with jitter
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                    
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def call_ai_api(prompt: str) -> str:
    # AI API call implementation
    pass
```

### 🚨 **Fallback Strategies**
```python
class AIService:
    def __init__(self):
        self.primary_model = "gpt-4-turbo"
        self.fallback_model = "gpt-3.5-turbo"
        self.cache = {}
        
    def generate_response(self, prompt: str) -> str:
        # Try cache first
        cache_key = hash(prompt)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Try primary model
            response = self._call_model(prompt, self.primary_model)
        except Exception as e:
            try:
                # Fallback to secondary model
                response = self._call_model(prompt, self.fallback_model)
            except Exception as e2:
                # Final fallback to template response
                response = self._generate_template_response(prompt)
        
        # Cache successful response
        self.cache[cache_key] = response
        return response
    
    def _generate_template_response(self, prompt: str) -> str:
        return "I apologize, but I'm unable to process your request at the moment. Please try again later."
```

## 💰 **Cost Management**

### 📊 **Budget Controls**
```python
class CostController:
    def __init__(self, daily_budget: float = 100.0):
        self.daily_budget = daily_budget
        self.daily_spend = 0.0
        self.request_count = 0
        
    def check_budget(self, estimated_cost: float) -> bool:
        return (self.daily_spend + estimated_cost) <= self.daily_budget
    
    def estimate_cost(self, prompt: str, model: str) -> float:
        token_count = len(prompt.split()) * 1.3  # Rough estimation
        
        pricing = {
            "gpt-4-turbo": 0.01,
            "gpt-3.5-turbo": 0.0005,
            "claude-3-opus": 0.015
        }
        
        return (token_count / 1000) * pricing.get(model, 0.01)
    
    def track_spend(self, actual_cost: float):
        self.daily_spend += actual_cost
        self.request_count += 1
        
        if self.daily_spend > self.daily_budget * 0.8:
            self._send_budget_alert()
    
    def _send_budget_alert(self):
        # Implementation for budget alerts
        pass
```

### 🎯 **Optimization Strategies**
```python
# Smart prompt compression
def compress_prompt(prompt: str, max_length: int = 2000) -> str:
    if len(prompt) <= max_length:
        return prompt
    
    # Keep essential parts: role, task, requirements
    lines = prompt.split('\n')
    essential_lines = []
    
    for line in lines:
        if any(keyword in line.lower() for keyword in 
               ['role:', 'task:', 'requirements:', 'format:']):
            essential_lines.append(line)
    
    compressed = '\n'.join(essential_lines)
    
    # If still too long, truncate examples
    if len(compressed) > max_length:
        compressed = compressed[:max_length] + "..."
    
    return compressed

# Batch processing for efficiency
def batch_process_requests(requests: List[str], batch_size: int = 10) -> List[str]:
    results = []
    
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]
        
        # Combine requests into single prompt
        combined_prompt = "Process these requests:\n\n"
        for j, req in enumerate(batch):
            combined_prompt += f"{j+1}. {req}\n"
        
        # Single API call for batch
        batch_response = call_ai_api(combined_prompt)
        
        # Parse individual responses
        individual_responses = parse_batch_response(batch_response, len(batch))
        results.extend(individual_responses)
    
    return results
```

## 🔐 **Compliance & Governance**

### 📋 **Audit Trail**
```python
import json
import datetime
from dataclasses import dataclass, asdict

@dataclass
class AIAuditLog:
    timestamp: str
    user_id: str
    prompt: str
    response: str
    model_used: str
    cost: float
    quality_score: float
    
class AIAuditor:
    def __init__(self, log_file: str = "ai_audit.jsonl"):
        self.log_file = log_file
        
    def log_interaction(self, user_id: str, prompt: str, response: str,
                       model: str, cost: float, quality: float = None):
        
        log_entry = AIAuditLog(
            timestamp=datetime.datetime.now().isoformat(),
            user_id=user_id,
            prompt=self._sanitize_for_logging(prompt),
            response=self._sanitize_for_logging(response),
            model_used=model,
            cost=cost,
            quality_score=quality or 0.0
        )
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(asdict(log_entry)) + '\n')
    
    def _sanitize_for_logging(self, text: str) -> str:
        # Remove PII and sensitive information
        import re
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Remove phone numbers
        text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', text)
        
        # Remove SSNs
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
        
        return text
```

### 🛡️ **Content Moderation**
```python
class ContentModerator:
    def __init__(self):
        self.blocked_patterns = [
            r'DROP\s+TABLE',
            r'DELETE\s+FROM',
            r'TRUNCATE',
            # Add more patterns
        ]
        
    def validate_input(self, prompt: str) -> tuple[bool, str]:
        # Check for malicious patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return False, f"Blocked pattern detected: {pattern}"
        
        # Check prompt length
        if len(prompt) > 10000:
            return False, "Prompt too long"
        
        return True, "Valid"
    
    def validate_output(self, response: str) -> tuple[bool, str]:
        # Check for harmful content
        harmful_indicators = ['password', 'secret', 'private key']
        
        for indicator in harmful_indicators:
            if indicator.lower() in response.lower():
                return False, f"Potentially harmful content: {indicator}"
        
        return True, "Valid"
```

## 🚀 **Production Deployment**

### 🐳 **Containerization**
```dockerfile
# Dockerfile for AI service
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### ⚖️ **Load Balancing**
```python
# FastAPI service with load balancing
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from typing import List

app = FastAPI()

class AIRequest(BaseModel):
    prompt: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500

class LoadBalancer:
    def __init__(self):
        self.models = {
            "gpt-3.5-turbo": {"capacity": 100, "current_load": 0},
            "gpt-4-turbo": {"capacity": 50, "current_load": 0}
        }
    
    def get_available_model(self, requested_model: str) -> str:
        model_info = self.models.get(requested_model)
        
        if not model_info:
            return "gpt-3.5-turbo"  # Default fallback
        
        if model_info["current_load"] < model_info["capacity"]:
            return requested_model
        
        # Find alternative with capacity
        for model, info in self.models.items():
            if info["current_load"] < info["capacity"]:
                return model
        
        raise HTTPException(status_code=503, detail="All models at capacity")

load_balancer = LoadBalancer()

@app.post("/generate")
async def generate_response(request: AIRequest):
    try:
        model = load_balancer.get_available_model(request.model)
        
        # Increment load
        load_balancer.models[model]["current_load"] += 1
        
        try:
            # Process request
            response = await process_ai_request(request.prompt, model)
            return {"response": response, "model_used": model}
        finally:
            # Decrement load
            load_balancer.models[model]["current_load"] -= 1
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_ai_request(prompt: str, model: str) -> str:
    # Simulate AI processing
    await asyncio.sleep(1)
    return f"Response from {model}: {prompt[:50]}..."
```

## 📈 **Continuous Improvement**

### 🔄 **A/B Testing**
```python
import random
from enum import Enum

class PromptVersion(Enum):
    VERSION_A = "a"
    VERSION_B = "b"

class ABTester:
    def __init__(self, split_ratio: float = 0.5):
        self.split_ratio = split_ratio
        self.results = {"a": [], "b": []}
    
    def get_prompt_version(self, user_id: str) -> PromptVersion:
        # Consistent assignment based on user_id
        hash_value = hash(user_id) % 100
        
        if hash_value < (self.split_ratio * 100):
            return PromptVersion.VERSION_A
        else:
            return PromptVersion.VERSION_B
    
    def record_result(self, version: PromptVersion, quality_score: float):
        self.results[version.value].append(quality_score)
    
    def get_performance_comparison(self) -> dict:
        if not self.results["a"] or not self.results["b"]:
            return {"error": "Insufficient data"}
        
        avg_a = sum(self.results["a"]) / len(self.results["a"])
        avg_b = sum(self.results["b"]) / len(self.results["b"])
        
        return {
            "version_a_avg": avg_a,
            "version_b_avg": avg_b,
            "improvement": ((avg_b - avg_a) / avg_a) * 100,
            "sample_sizes": {
                "a": len(self.results["a"]),
                "b": len(self.results["b"])
            }
        }
```

### 📊 **Feedback Loop**
```python
class FeedbackCollector:
    def __init__(self):
        self.feedback_data = []
    
    def collect_feedback(self, interaction_id: str, rating: int, 
                        comments: str = None):
        feedback = {
            "interaction_id": interaction_id,
            "rating": rating,  # 1-5 scale
            "comments": comments,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.feedback_data.append(feedback)
        
        # Trigger improvement if rating is low
        if rating <= 2:
            self._trigger_improvement_analysis(interaction_id)
    
    def _trigger_improvement_analysis(self, interaction_id: str):
        # Analyze what went wrong and suggest improvements
        pass
    
    def get_feedback_summary(self) -> dict:
        if not self.feedback_data:
            return {}
        
        ratings = [f["rating"] for f in self.feedback_data]
        
        return {
            "average_rating": sum(ratings) / len(ratings),
            "total_feedback": len(self.feedback_data),
            "rating_distribution": {
                str(i): ratings.count(i) for i in range(1, 6)
            }
        }
```

---

**🎯 Remember: These best practices should be adapted to your specific use case and organizational requirements. Start with the basics and gradually implement more advanced patterns as your AI systems mature.**