# 🚀 Production Deployment - Key Concepts

## 🎯 **Real-World Analogy: The Restaurant Kitchen**

> **Think of production deployment like running a high-end restaurant kitchen. You need fast service (low latency), handle rush hours (scaling), maintain quality (monitoring), and ensure food safety (security) - all while keeping costs reasonable.**

## 🔥 **Core Concepts**

### 1. **FastAPI Production Setup** ⚡

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

app = FastAPI(title="GenAI API", version="1.0.0")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-15T10:30:00Z"}

# Main endpoint
@app.post("/generate")
async def generate_response(request: dict):
    try:
        # Process request
        response = await process_llm_request(request)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_llm_request(request):
    # Simulate LLM processing
    await asyncio.sleep(0.1)
    return {"response": "Generated content"}
```

### 2. **Container Deployment** 🐳

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - redis
      - postgres
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: genai_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

### 3. **Kubernetes Deployment** ☸️

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: genai-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: genai-api
  template:
    metadata:
      labels:
        app: genai-api
    spec:
      containers:
      - name: api
        image: genai-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openai-key
---
apiVersion: v1
kind: Service
metadata:
  name: genai-service
spec:
  selector:
    app: genai-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 4. **Auto-Scaling Configuration** 📈

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: genai-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: genai-api
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 📊 **Monitoring & Observability**

### **Prometheus Metrics**
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Metrics
REQUEST_COUNT = Counter('genai_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('genai_request_duration_seconds', 'Request duration')
ACTIVE_CONNECTIONS = Gauge('genai_active_connections', 'Active connections')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    
    # Track request
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    ACTIVE_CONNECTIONS.inc()
    
    try:
        response = await call_next(request)
        return response
    finally:
        # Track duration
        duration = time.time() - start_time
        REQUEST_DURATION.observe(duration)
        ACTIVE_CONNECTIONS.dec()

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### **Structured Logging**
```python
import structlog
import json

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

@app.post("/generate")
async def generate_response(request: dict):
    request_id = generate_request_id()
    
    logger.info(
        "Request received",
        request_id=request_id,
        user_id=request.get("user_id"),
        model=request.get("model", "default")
    )
    
    try:
        response = await process_llm_request(request)
        
        logger.info(
            "Request completed",
            request_id=request_id,
            response_length=len(str(response)),
            processing_time=0.5
        )
        
        return response
    except Exception as e:
        logger.error(
            "Request failed",
            request_id=request_id,
            error=str(e),
            exc_info=True
        )
        raise
```

## 🔒 **Security & Performance**

### **Rate Limiting**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/generate")
@limiter.limit("10/minute")
async def generate_response(request: Request, data: dict):
    return await process_request(data)
```

### **Caching Strategy**
```python
import redis
import json
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_cache_key(prompt, model_config):
    content = f"{prompt}_{json.dumps(model_config, sort_keys=True)}"
    return hashlib.md5(content.encode()).hexdigest()

async def cached_llm_call(prompt, model_config):
    cache_key = get_cache_key(prompt, model_config)
    
    # Try cache first
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    
    # Generate new response
    response = await llm_generate(prompt, model_config)
    
    # Cache for 1 hour
    redis_client.setex(cache_key, 3600, json.dumps(response))
    
    return response
```

### **Load Balancing**
```python
import random
from typing import List

class LoadBalancer:
    def __init__(self, endpoints: List[str]):
        self.endpoints = endpoints
        self.health_status = {endpoint: True for endpoint in endpoints}
    
    def get_healthy_endpoint(self):
        healthy_endpoints = [
            endpoint for endpoint, is_healthy in self.health_status.items()
            if is_healthy
        ]
        
        if not healthy_endpoints:
            raise Exception("No healthy endpoints available")
        
        return random.choice(healthy_endpoints)
    
    async def health_check(self):
        for endpoint in self.endpoints:
            try:
                # Perform health check
                response = await check_endpoint_health(endpoint)
                self.health_status[endpoint] = response.status_code == 200
            except:
                self.health_status[endpoint] = False

# Usage
lb = LoadBalancer([
    "http://api-1:8000",
    "http://api-2:8000", 
    "http://api-3:8000"
])

@app.post("/generate")
async def generate_response(request: dict):
    endpoint = lb.get_healthy_endpoint()
    return await forward_request(endpoint, request)
```