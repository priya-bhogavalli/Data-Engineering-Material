# Advanced API Interview Questions for Data Engineering

## 🏗️ API Architecture & Design

### Q15: How do you design microservices APIs?
**Answer:**
```python
# Service boundaries and API contracts
class UserService:
    def __init__(self):
        self.base_url = "http://user-service:8080"
    
    def get_user(self, user_id):
        return requests.get(f"{self.base_url}/users/{user_id}")
    
    def create_user(self, user_data):
        return requests.post(f"{self.base_url}/users", json=user_data)

class OrderService:
    def __init__(self):
        self.base_url = "http://order-service:8081"
        self.user_service = UserService()
    
    def create_order(self, order_data):
        # Validate user exists
        user = self.user_service.get_user(order_data['user_id'])
        if user.status_code != 200:
            raise ValueError("Invalid user")
        
        return requests.post(f"{self.base_url}/orders", json=order_data)

# API Gateway for service orchestration
class APIGateway:
    def __init__(self):
        self.services = {
            'users': UserService(),
            'orders': OrderService()
        }
    
    def route_request(self, service, endpoint, method, data=None):
        service_instance = self.services.get(service)
        if not service_instance:
            return {'error': 'Service not found'}, 404
        
        return getattr(service_instance, method)(endpoint, data)
```

### Q16: What are API design anti-patterns to avoid?
**Answer:**

**1. Chatty APIs:**
```python
# Bad: Multiple API calls needed
user = api.get_user(user_id)
profile = api.get_user_profile(user_id)
preferences = api.get_user_preferences(user_id)

# Good: Single comprehensive call
user_data = api.get_user_complete(user_id, include=['profile', 'preferences'])
```

**2. Overfetching/Underfetching:**
```python
# Bad: Returns unnecessary data
{
  "id": 1,
  "name": "John",
  "email": "john@example.com",
  "password_hash": "...",  # Sensitive data
  "internal_notes": "...", # Internal data
  "full_address": {...}    # Unnecessary for list view
}

# Good: Field selection
GET /api/users?fields=id,name,email
```

**3. Inconsistent Naming:**
```python
# Bad: Inconsistent conventions
GET /api/getUsers
POST /api/user_create
PUT /api/updateUser

# Good: Consistent REST conventions
GET /api/users
POST /api/users
PUT /api/users/{id}
```

## 🔄 API Integration Patterns

### Q17: How do you handle API integration failures?
**Answer:**

**Circuit Breaker Pattern:**
```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
circuit_breaker = CircuitBreaker()

def call_external_api():
    return circuit_breaker.call(requests.get, 'https://api.example.com/data')
```

**Retry with Exponential Backoff:**
```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                raise e
            
            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)

# Usage
def api_call():
    response = requests.get('https://api.example.com/data', timeout=5)
    response.raise_for_status()
    return response.json()

result = retry_with_backoff(api_call, max_retries=3)
```

### Q18: How do you implement API monitoring and observability?
**Answer:**

**Metrics Collection:**
```python
import time
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
api_requests_total = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration')

def monitor_api(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        method = request.method
        endpoint = request.endpoint
        
        try:
            result = func(*args, **kwargs)
            status = getattr(result, 'status_code', 200)
            api_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
            return result
        except Exception as e:
            api_requests_total.labels(method=method, endpoint=endpoint, status=500).inc()
            raise e
        finally:
            duration = time.time() - start_time
            api_request_duration.observe(duration)
    
    return wrapper

@app.route('/metrics')
def metrics():
    return generate_latest()
```

**Distributed Tracing:**
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)
        
        # Database call
        with tracer.start_as_current_span("database_query") as db_span:
            user = db.query(User).filter(User.id == user_id).first()
            db_span.set_attribute("db.statement", "SELECT * FROM users WHERE id = ?")
        
        if not user:
            span.set_attribute("error", True)
            return {'error': 'User not found'}, 404
        
        return user.to_dict()
```

## 📊 Data API Optimization

### Q19: How do you optimize APIs for big data scenarios?
**Answer:**

**Streaming Responses:**
```python
import json
from flask import Response

@app.route('/api/large-dataset')
def stream_large_dataset():
    def generate():
        yield '{"data": ['
        
        first = True
        for chunk in get_data_chunks():
            if not first:
                yield ','
            yield json.dumps(chunk)
            first = False
        
        yield ']}'
    
    return Response(generate(), mimetype='application/json')

# Async processing for large operations
import asyncio
import aiohttp

async def process_large_dataset(dataset_id):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for chunk_id in get_chunk_ids(dataset_id):
            task = process_chunk(session, chunk_id)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return combine_results(results)

async def process_chunk(session, chunk_id):
    async with session.get(f'/api/chunks/{chunk_id}') as response:
        return await response.json()
```

**Data Compression:**
```python
import gzip
import json
from flask import request

@app.route('/api/compressed-data')
def get_compressed_data():
    data = get_large_data()
    
    # Check if client accepts gzip
    if 'gzip' in request.headers.get('Accept-Encoding', ''):
        json_data = json.dumps(data)
        compressed_data = gzip.compress(json_data.encode('utf-8'))
        
        response = Response(compressed_data)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Type'] = 'application/json'
        return response
    
    return jsonify(data)
```

### Q20: How do you implement API aggregation and composition?
**Answer:**

**Backend for Frontend (BFF) Pattern:**
```python
class MobileAPIComposer:
    def __init__(self):
        self.user_service = UserService()
        self.order_service = OrderService()
        self.product_service = ProductService()
    
    async def get_user_dashboard(self, user_id):
        # Parallel API calls
        user_task = asyncio.create_task(self.user_service.get_user(user_id))
        orders_task = asyncio.create_task(self.order_service.get_recent_orders(user_id))
        recommendations_task = asyncio.create_task(self.product_service.get_recommendations(user_id))
        
        user, orders, recommendations = await asyncio.gather(
            user_task, orders_task, recommendations_task
        )
        
        # Compose mobile-optimized response
        return {
            'user': {
                'name': user['name'],
                'avatar': user['profile']['avatar_url']
            },
            'recent_orders': [
                {
                    'id': order['id'],
                    'total': order['total'],
                    'status': order['status']
                } for order in orders[:5]  # Limit for mobile
            ],
            'recommendations': recommendations[:3]  # Top 3 only
        }

@app.route('/api/mobile/dashboard/<int:user_id>')
async def mobile_dashboard(user_id):
    composer = MobileAPIComposer()
    dashboard_data = await composer.get_user_dashboard(user_id)
    return jsonify(dashboard_data)
```

## 🔒 Advanced API Security

### Q21: How do you implement API security best practices?
**Answer:**

**Input Validation and Sanitization:**
```python
from marshmallow import Schema, fields, validate, ValidationError

class UserCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    age = fields.Int(validate=validate.Range(min=0, max=150))
    role = fields.Str(validate=validate.OneOf(['user', 'admin', 'moderator']))

@app.route('/api/users', methods=['POST'])
def create_user():
    schema = UserCreateSchema()
    
    try:
        validated_data = schema.load(request.json)
    except ValidationError as err:
        return {'errors': err.messages}, 400
    
    # Sanitize input
    validated_data['name'] = html.escape(validated_data['name'])
    
    user = create_user_in_db(validated_data)
    return user.to_dict(), 201
```

**SQL Injection Prevention:**
```python
# Bad: Vulnerable to SQL injection
def get_user_by_email(email):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return db.execute(query)

# Good: Parameterized queries
def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    return db.execute(query, (email,))

# Using ORM (SQLAlchemy)
def get_user_by_email(email):
    return User.query.filter(User.email == email).first()
```

**CORS Configuration:**
```python
from flask_cors import CORS

# Restrictive CORS configuration
CORS(app, 
     origins=['https://myapp.com', 'https://admin.myapp.com'],
     methods=['GET', 'POST', 'PUT', 'DELETE'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

# Custom CORS handling
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in ['https://myapp.com', 'https://admin.myapp.com']:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    
    return response
```

## 🧪 API Testing Strategies

### Q22: How do you implement comprehensive API testing?
**Answer:**

**Property-Based Testing:**
```python
from hypothesis import given, strategies as st
import requests

@given(st.integers(min_value=1, max_value=1000000))
def test_get_user_with_valid_ids(user_id):
    response = requests.get(f'/api/users/{user_id}')
    assert response.status_code in [200, 404]
    
    if response.status_code == 200:
        data = response.json()
        assert 'id' in data
        assert data['id'] == user_id

@given(st.text(min_size=1, max_size=100))
def test_create_user_with_various_names(name):
    user_data = {'name': name, 'email': 'test@example.com'}
    response = requests.post('/api/users', json=user_data)
    
    if response.status_code == 201:
        data = response.json()
        assert data['name'] == name
```

**Load Testing:**
```python
import asyncio
import aiohttp
import time

async def load_test_endpoint(session, url, concurrent_requests=100):
    async def make_request():
        async with session.get(url) as response:
            return response.status, await response.text()
    
    start_time = time.time()
    
    # Create concurrent requests
    tasks = [make_request() for _ in range(concurrent_requests)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    end_time = time.time()
    
    # Analyze results
    successful_requests = sum(1 for r in results if isinstance(r, tuple) and r[0] == 200)
    failed_requests = len(results) - successful_requests
    total_time = end_time - start_time
    
    print(f"Total requests: {len(results)}")
    print(f"Successful: {successful_requests}")
    print(f"Failed: {failed_requests}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Requests per second: {len(results) / total_time:.2f}")

# Run load test
async def run_load_test():
    async with aiohttp.ClientSession() as session:
        await load_test_endpoint(session, 'http://localhost:5000/api/users')

asyncio.run(run_load_test())
```

## 🎯 Key Advanced Concepts

**API Architecture Patterns:**
- Microservices API design
- API Gateway pattern
- Backend for Frontend (BFF)
- Event-driven APIs
- CQRS with APIs

**Performance Optimization:**
- Response streaming
- Data compression
- Async processing
- Connection pooling
- CDN integration

**Security Measures:**
- Input validation/sanitization
- SQL injection prevention
- XSS protection
- CORS configuration
- Rate limiting by user/API key

**Monitoring & Observability:**
- Metrics collection (Prometheus)
- Distributed tracing (Jaeger)
- Logging strategies
- Health checks
- SLA monitoring