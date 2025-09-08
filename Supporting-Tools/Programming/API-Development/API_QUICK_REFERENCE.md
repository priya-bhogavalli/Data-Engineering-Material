# API Development Quick Reference

## 🚀 HTTP Methods & Status Codes

### HTTP Methods
```
GET     - Retrieve data (idempotent, safe)
POST    - Create new resource
PUT     - Update/replace entire resource (idempotent)
PATCH   - Partial update
DELETE  - Remove resource (idempotent)
HEAD    - Get headers only
OPTIONS - Get allowed methods
```

### HTTP Status Codes
```
2xx Success
200 OK              - Request successful
201 Created         - Resource created
202 Accepted        - Request accepted for processing
204 No Content      - Success, no response body

3xx Redirection
301 Moved Permanently
302 Found (temporary redirect)
304 Not Modified

4xx Client Error
400 Bad Request     - Invalid request syntax
401 Unauthorized    - Authentication required
403 Forbidden       - Access denied
404 Not Found       - Resource doesn't exist
405 Method Not Allowed
409 Conflict        - Resource conflict
422 Unprocessable Entity - Validation error
429 Too Many Requests

5xx Server Error
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

## 🔐 Authentication Methods

### API Key
```python
headers = {'X-API-Key': 'your-api-key'}
```

### Bearer Token (JWT)
```python
headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIs...'}
```

### Basic Auth
```python
import base64
credentials = base64.b64encode(b'username:password').decode()
headers = {'Authorization': f'Basic {credentials}'}
```

### OAuth 2.0 Flow
```
1. Authorization Request → Authorization Server
2. Authorization Grant ← Authorization Server  
3. Access Token Request → Authorization Server
4. Access Token ← Authorization Server
5. Protected Resource Request → Resource Server
```

## 📊 Request/Response Patterns

### Pagination
```python
# Offset-based
GET /api/users?page=2&per_page=50

# Cursor-based  
GET /api/users?cursor=abc123&limit=50

# Response format
{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 50,
    "total": 1000,
    "has_next": true
  }
}
```

### Filtering & Sorting
```python
# Filtering
GET /api/users?status=active&role=admin&created_after=2023-01-01

# Sorting
GET /api/users?sort=name,-created_at  # name ASC, created_at DESC

# Field selection
GET /api/users?fields=id,name,email
```

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["Invalid email format"],
      "age": ["Must be between 0 and 150"]
    },
    "timestamp": "2023-12-07T10:30:00Z",
    "request_id": "req_123456"
  }
}
```

## 🔄 REST API Design

### Resource Naming
```
# Collections (plural nouns)
GET    /api/users           # Get all users
POST   /api/users           # Create user

# Individual resources
GET    /api/users/123       # Get user 123
PUT    /api/users/123       # Update user 123
DELETE /api/users/123       # Delete user 123

# Nested resources
GET    /api/users/123/orders     # Get orders for user 123
POST   /api/users/123/orders     # Create order for user 123
```

### Query Parameters
```
?page=1&per_page=50          # Pagination
?sort=name,-created_at       # Sorting
?filter=status:active        # Filtering
?include=profile,orders      # Include related data
?fields=id,name,email        # Field selection
?expand=true                 # Expand nested objects
```

## 🛡️ Security Headers

```python
# Security headers
response.headers['X-Content-Type-Options'] = 'nosniff'
response.headers['X-Frame-Options'] = 'DENY'
response.headers['X-XSS-Protection'] = '1; mode=block'
response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
response.headers['Content-Security-Policy'] = "default-src 'self'"

# CORS headers
response.headers['Access-Control-Allow-Origin'] = 'https://myapp.com'
response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
response.headers['Access-Control-Max-Age'] = '86400'
```

## 📈 Performance Optimization

### Caching Headers
```python
# Cache for 1 hour
response.headers['Cache-Control'] = 'public, max-age=3600'

# No caching
response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'

# ETag for conditional requests
response.headers['ETag'] = '"unique-etag-value"'

# Last-Modified
response.headers['Last-Modified'] = 'Wed, 21 Oct 2015 07:28:00 GMT'
```

### Rate Limiting Headers
```python
response.headers['X-RateLimit-Limit'] = '1000'      # Requests per hour
response.headers['X-RateLimit-Remaining'] = '999'   # Remaining requests
response.headers['X-RateLimit-Reset'] = '1609459200' # Reset timestamp
response.headers['Retry-After'] = '3600'            # Retry after seconds
```

## 🧪 Testing Checklist

### Functional Testing
- [ ] All CRUD operations work correctly
- [ ] Input validation works
- [ ] Error handling returns proper status codes
- [ ] Authentication/authorization works
- [ ] Pagination works correctly

### Security Testing
- [ ] SQL injection prevention
- [ ] XSS prevention  
- [ ] CSRF protection
- [ ] Input sanitization
- [ ] Proper authentication

### Performance Testing
- [ ] Response time under normal load
- [ ] Behavior under high load
- [ ] Memory usage
- [ ] Database query optimization
- [ ] Caching effectiveness

### Integration Testing
- [ ] Database integration
- [ ] External API integration
- [ ] Service-to-service communication
- [ ] Error propagation
- [ ] Transaction handling

## 📚 Documentation Elements

### OpenAPI/Swagger Spec
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
```

### API Documentation Sections
- [ ] Overview and purpose
- [ ] Authentication methods
- [ ] Base URL and versioning
- [ ] Request/response formats
- [ ] Error codes and messages
- [ ] Rate limiting information
- [ ] Code examples in multiple languages
- [ ] SDKs and client libraries

## 🔧 Common Patterns

### Bulk Operations
```python
# Bulk create
POST /api/users/bulk
{
  "users": [
    {"name": "John", "email": "john@example.com"},
    {"name": "Jane", "email": "jane@example.com"}
  ]
}

# Bulk update
PATCH /api/users/bulk
{
  "updates": [
    {"id": 1, "name": "John Updated"},
    {"id": 2, "email": "jane.new@example.com"}
  ]
}
```

### Async Operations
```python
# Start async operation
POST /api/data/process
Response: 202 Accepted
{
  "job_id": "job_123",
  "status": "processing",
  "status_url": "/api/jobs/job_123"
}

# Check status
GET /api/jobs/job_123
{
  "id": "job_123",
  "status": "completed",
  "result_url": "/api/data/processed/job_123"
}
```

### Webhooks
```python
# Register webhook
POST /api/webhooks
{
  "url": "https://myapp.com/webhook",
  "events": ["user.created", "user.updated"],
  "secret": "webhook_secret"
}

# Webhook payload
POST https://myapp.com/webhook
{
  "event": "user.created",
  "data": {
    "id": 123,
    "name": "John Doe"
  },
  "timestamp": "2023-12-07T10:30:00Z"
}
```