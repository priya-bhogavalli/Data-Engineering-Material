# Comprehensive API Interview Questions for Data Engineering

## 🎯 API Fundamentals

### Q1: What are the different types of APIs?
**Answer:**
- **REST APIs**: HTTP-based, stateless, resource-oriented
- **SOAP APIs**: XML-based, protocol with strict standards
- **GraphQL APIs**: Query language, single endpoint, flexible data fetching
- **gRPC APIs**: High-performance, Protocol Buffers, HTTP/2
- **WebSocket APIs**: Real-time, bidirectional communication
- **Webhook APIs**: Event-driven, push notifications

### Q2: What is REST and how does it differ from SOAP?

**REST (Representational State Transfer):**
- Architectural style, not a protocol
- Uses HTTP methods (GET, POST, PUT, DELETE)
- Stateless communication
- Lightweight (JSON/XML)
- Cacheable responses
- Multiple data formats supported

**SOAP (Simple Object Access Protocol):**
- Protocol with strict standards
- XML-only messaging
- Stateful or stateless
- Built-in error handling
- WS-Security for security
- More overhead

**Key Differences:**
```
| Aspect | REST | SOAP |
|--------|------|------|
| Protocol | HTTP | HTTP/SMTP/TCP |
| Format | JSON/XML/HTML | XML only |
| Performance | Faster | Slower |
| Caching | Yes | No |
| Security | HTTPS/OAuth | WS-Security |
| Standards | Loose | Strict |
```

### Q3: Explain RESTful services and their principles.
**Answer:**

**Six REST Principles:**
1. **Client-Server Architecture**: Separation of concerns
2. **Stateless**: No client state stored on server
3. **Cacheable**: Responses must define cacheability
4. **Uniform Interface**: Consistent resource identification
5. **Layered System**: Hierarchical layers
6. **Code on Demand** (optional): Server can send executable code

**RESTful Design:**
```python
# Resource-based URLs
GET    /api/v1/users          # Get all users
GET    /api/v1/users/123      # Get specific user
POST   /api/v1/users          # Create new user
PUT    /api/v1/users/123      # Update user
DELETE /api/v1/users/123      # Delete user

# Nested resources
GET    /api/v1/users/123/orders     # Get user's orders
POST   /api/v1/users/123/orders     # Create order for user
```

## 🔐 API Security & Authentication

### Q4: What are different API authentication methods?
**Answer:**

**1. API Keys:**
```python
headers = {'X-API-Key': 'your-api-key'}
response = requests.get('/api/data', headers=headers)
```

**2. JWT (JSON Web Tokens):**
```python
# Token structure: header.payload.signature
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
headers = {'Authorization': f'Bearer {token}'}
```

**3. OAuth 2.0:**
```python
# Authorization Code Flow

### Q5: How do you implement rate limiting?
**Answer:**
```python
# Token bucket algorithm
class RateLimiter:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
    
    def allow_request(self):
        now = time.time()
        # Add tokens based on time elapsed
        tokens_to_add = (now - self.last_refill) * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

# Usage
@app.route('/api/data')
def get_data():
    if not rate_limiter.allow_request():
        return {'error': 'Rate limit exceeded'}, 429
    return {'data': 'response'}
```

## 📊 Data APIs & Performance

### Q6: How do you handle large datasets in APIs?
**Answer:**

**Pagination:**
```python
# Offset-based pagination
@app.route('/api/users')
def get_users():
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 50)), 1000)
    offset = (page - 1) * per_page
    
    users = db.query().offset(offset).limit(per_page).all()
    total = db.query().count()
    
    return {
        'data': users,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'has_next': offset + per_page < total
        }
    }

# Cursor-based pagination (better for large datasets)
@app.route('/api/events')
def get_events():
    cursor = request.args.get('cursor')
    limit = int(request.args.get('limit', 100))
    
    query = db.query()
    if cursor:
        query = query.filter(Event.id > cursor)
    
    events = query.limit(limit + 1).all()
    has_more = len(events) > limit
    
    if has_more:
        events = events[:-1]
        next_cursor = events[-1].id
    else:
        next_cursor = None
    
    return {
        'data': events,
        'next_cursor': next_cursor,
        'has_more': has_more
    }
```

### Q7: How do you implement API caching?
**Answer:**
```python
# Response caching with Redis
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_response(expiration=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            cache_key = f"api_cache:{f.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = f(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            
            return result
        return decorated_function
    return decorator

@app.route('/api/expensive-data')
@cache_response(expiration=600)  # Cache for 10 minutes
def get_expensive_data():
    # Expensive database operation
    return {'data': 'expensive computation result'}

# HTTP caching headers
@app.route('/api/static-data')
def get_static_data():
    response = jsonify({'data': 'static content'})
    response.headers['Cache-Control'] = 'public, max-age=3600'  # 1 hour
    response.headers['ETag'] = 'unique-etag-value'
    return response
```

## 🔄 API Design Patterns

### Q8: What are common API design patterns?
**Answer:**

**1. Resource-Based Design:**
```python
# Good: Resource-oriented
GET /api/v1/books/123/authors
POST /api/v1/books
PUT /api/v1/books/123

# Bad: Action-oriented
GET /api/v1/getBookAuthors?bookId=123
POST /api/v1/createBook
PUT /api/v1/updateBook?id=123
```

**2. HATEOAS (Hypermedia as the Engine of Application State):**
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "_links": {
    "self": {"href": "/api/v1/users/123"},
    "orders": {"href": "/api/v1/users/123/orders"},
    "edit": {"href": "/api/v1/users/123", "method": "PUT"},
    "delete": {"href": "/api/v1/users/123", "method": "DELETE"}
  }
}
```

**3. API Gateway Pattern:**
```python
# Centralized entry point
class APIGateway:
    def __init__(self):
        self.services = {
            'user': UserService(),
            'order': OrderService(),
            'payment': PaymentService()
        }
    
    def route_request(self, path, method, data):
        service_name = path.split('/')[2]  # /api/v1/users -> users
        service = self.services.get(service_name)
        
        if not service:
            return {'error': 'Service not found'}, 404
        
        return service.handle_request(method, path, data)
```

### Q9: How do you version APIs effectively?
**Answer:**

**URL Versioning:**
```python
@app.route('/api/v1/users/<int:user_id>')
def get_user_v1(user_id):
    return {'id': user_id, 'name': 'John'}

@app.route('/api/v2/users/<int:user_id>')
def get_user_v2(user_id):
    return {
        'id': user_id,
        'full_name': 'John Doe',
        'profile': {'avatar': 'url'}
    }
```

**Header Versioning:**
```python
@app.route('/api/users/<int:user_id>')
def get_user_versioned(user_id):
    version = request.headers.get('API-Version', 'v1')
    
    if version == 'v2':
        return get_user_v2_format(user_id)
    return get_user_v1_format(user_id)
```

**Content Negotiation:**
```python
@app.route('/api/users/<int:user_id>')
def get_user_content_negotiation(user_id):
    accept = request.headers.get('Accept', 'application/json')
    
    if 'application/vnd.api.v2+json' in accept:
        return get_user_v2_format(user_id)
    return get_user_v1_format(user_id)
```

## 🧪 API Testing & Documentation

### Q10: How do you test APIs comprehensively?
**Answer:**

**Unit Testing:**
```python
import unittest
import json

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_get_user_success(self):
        response = self.app.get('/api/v1/users/1')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertIn('name', data)
    
    def test_create_user_validation(self):
        invalid_data = {'name': ''}  # Missing required fields
        response = self.app.post('/api/v1/users', 
                               data=json.dumps(invalid_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
```

**Contract Testing:**
```python
# Using Pact for contract testing
from pact import Consumer, Provider

pact = Consumer('UserService').has_pact_with(Provider('UserAPI'))

def test_get_user_contract():
    expected = {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com'
    }
    
    (pact
     .given('User 1 exists')
     .upon_receiving('a request for user 1')
     .with_request('GET', '/api/v1/users/1')
     .will_respond_with(200, body=expected))
    
    with pact:
        result = user_api_client.get_user(1)
        assert result == expected
```

### Q11: How do you document APIs effectively?
**Answer:**

**OpenAPI/Swagger:**
```python
from flask_restx import Api, Resource, fields

api = Api(app, doc='/docs/')

user_model = api.model('User', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'email': fields.String(required=True)
})

@api.route('/users')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """Fetch all users"""
        return users
    
    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        return new_user, 201
```

## 🌐 Advanced API Concepts

### Q12: What is GraphQL and when would you use it?
**Answer:**

**GraphQL Benefits:**
- Single endpoint for all operations
- Client specifies exactly what data to fetch
- Strong type system
- Real-time subscriptions
- Introspection capabilities

**Example:**
```python
import graphene

class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    posts = graphene.List(lambda: Post)

class Post(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    content = graphene.String()
    author = graphene.Field(User)

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID(required=True))
    
    def resolve_user(self, info, id):
        return get_user_by_id(id)

# Client query
query = """
{
  user(id: "1") {
    name
    email
    posts {
      title
    }
  }
}
"""
```

### Q13: How do you handle API errors and exceptions?
**Answer:**

**Structured Error Responses:**
```python
class APIError(Exception):
    def __init__(self, message, status_code=400, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        'error': {
            'message': error.message,
            'code': error.error_code,
            'status': error.status_code
        }
    }
    return jsonify(response), error.status_code

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({
        'error': {
            'message': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'details': error.messages
        }
    }), 400

# Usage
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIError('User not found', 404, 'USER_NOT_FOUND')
    return jsonify(user.to_dict())
```

### Q14: How do you implement real-time APIs?
**Answer:**

**WebSocket API:**
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'msg': 'Connected to server'})

@socketio.on('subscribe_data')
def handle_subscribe(data):
    room = data['room']
    join_room(room)
    emit('subscribed', {'room': room})

# Push real-time data
def push_data_update(room, data):
    socketio.emit('data_update', data, room=room)
```

**Server-Sent Events (SSE):**
```python
from flask import Response
import json
import time

@app.route('/api/stream')
def stream_data():
    def event_stream():
        while True:
            # Get latest data
            data = get_latest_data()
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)
    
    return Response(event_stream(), 
                   mimetype='text/plain',
                   headers={'Cache-Control': 'no-cache'})
```

## 🎯 Key Takeaways

**Essential API Concepts:**
- **REST principles**: Stateless, resource-based, HTTP methods
- **Authentication**: JWT, OAuth, API keys
- **Performance**: Caching, pagination, rate limiting
- **Documentation**: OpenAPI/Swagger specifications
- **Testing**: Unit, integration, contract testing
- **Error handling**: Structured error responses
- **Versioning**: Backward compatibility strategies
- **Security**: Input validation, HTTPS, proper authentication

**Best Practices:**
- Use consistent naming conventions
- Implement proper HTTP status codes
- Provide comprehensive documentation
- Handle errors gracefully
- Implement rate limiting and caching
- Use HTTPS for all communications
- Version APIs from the beginning
- Test thoroughly including edge cases