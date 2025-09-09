
### Q1: How do you design RESTful APIs for data services?
**Answer:**
```python
# RESTful API design principles
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Resource-based URLs
class DatasetResource(Resource):
    def get(self, dataset_id=None):
        """GET /api/v1/datasets/{id} - Retrieve dataset"""
        if dataset_id:
            return self.get_dataset(dataset_id)
        return self.list_datasets()
    
    def post(self):
        """POST /api/v1/datasets - Create new dataset"""
        data = request.get_json()
        return self.create_dataset(data), 201
    
    def put(self, dataset_id):
        """PUT /api/v1/datasets/{id} - Update dataset"""
        data = request.get_json()
        return self.update_dataset(dataset_id, data)
    
    def delete(self, dataset_id):
        """DELETE /api/v1/datasets/{id} - Delete dataset"""
        self.delete_dataset(dataset_id)
        return '', 204

# Query parameters for filtering
class DataQueryResource(Resource):
    def get(self):
        """GET /api/v1/data?filter=active&sort=created_at&limit=100"""
        filters = request.args.get('filter')
        sort_by = request.args.get('sort', 'id')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        return self.query_data(filters, sort_by, limit, offset)

# Register resources
api.add_resource(DatasetResource, '/api/v1/datasets', '/api/v1/datasets/<int:dataset_id>')
api.add_resource(DataQueryResource, '/api/v1/data')
```

### Q2: How do you implement API versioning and backward compatibility?
**Answer:**
```python
# URL versioning
@app.route('/api/v1/users/<int:user_id>')
def get_user_v1(user_id):
    user = get_user(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email
    })

@app.route('/api/v2/users/<int:user_id>')
def get_user_v2(user_id):
    user = get_user(user_id)
    return jsonify({
        'id': user.id,
        'full_name': user.name,  # Changed field name
        'email': user.email,
        'created_at': user.created_at.isoformat(),  # Added field
        'profile': {  # Nested structure
            'avatar_url': user.avatar_url,
            'bio': user.bio
        }
    })

# Header versioning
@app.route('/api/users/<int:user_id>')
def get_user_versioned(user_id):
    version = request.headers.get('API-Version', 'v1')
    
    if version == 'v2':
        return get_user_v2(user_id)
    else:
        return get_user_v1(user_id)

# Content negotiation
@app.route('/api/users/<int:user_id>')
def get_user_content_negotiation(user_id):
    accept_header = request.headers.get('Accept', 'application/json')
    
    if 'application/vnd.api.v2+json' in accept_header:
        return get_user_v2(user_id)
    else:
        return get_user_v1(user_id)
```

## Data API Design

### Q3: How do you design APIs for large dataset access?
**Answer:**
```python
# Pagination implementation
class PaginatedDataAPI(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 50)), 1000)  # Max 1000
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Query data with pagination
        total_count = self.get_total_count()
        data = self.get_data(offset=offset, limit=per_page)
        
        # Calculate pagination metadata
        total_pages = (total_count + per_page - 1) // per_page
        has_next = page < total_pages
        has_prev = page > 1
        
        return {
            'data': data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': has_next,
                'has_prev': has_prev,
                'next_page': page + 1 if has_next else None,
                'prev_page': page - 1 if has_prev else None
            },
            'links': {
                'self': f'/api/v1/data?page={page}&per_page={per_page}',
                'next': f'/api/v1/data?page={page+1}&per_page={per_page}' if has_next else None,
                'prev': f'/api/v1/data?page={page-1}&per_page={per_page}' if has_prev else None
            }
        }

# Cursor-based pagination for large datasets
class CursorPaginatedAPI(Resource):
    def get(self):
        cursor = request.args.get('cursor')
        limit = min(int(request.args.get('limit', 50)), 1000)
        
        # Query data using cursor
        data, next_cursor = self.get_data_with_cursor(cursor, limit)
        
        response = {
            'data': data,
            'pagination': {
                'limit': limit,
                'has_more': next_cursor is not None,
                'next_cursor': next_cursor
            }
        }
        
        if next_cursor:
            response['links'] = {
                'next': f'/api/v1/data?cursor={next_cursor}&limit={limit}'
            }
        
        return response

# Streaming API for real-time data
from flask import Response
import json

@app.route('/api/v1/stream')
def stream_data():
    def generate():
        for data_chunk in get_streaming_data():
            yield f"data: {json.dumps(data_chunk)}\n\n"
    
    return Response(generate(), mimetype='text/plain')
```

### Q4: How do you implement data filtering and search APIs?
**Answer:**
```python
# Advanced filtering API
class DataFilterAPI(Resource):
    def get(self):
        # Parse filter parameters
        filters = self.parse_filters(request.args)
        search_query = request.args.get('q')
        sort_fields = request.args.getlist('sort')
        
        # Build query
        query = self.build_query(filters, search_query, sort_fields)
        
        # Execute query with pagination
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 50)), 1000)
        
        results = self.execute_query(query, page, per_page)
        
        return {
            'data': results['data'],
            'filters_applied': filters,
            'search_query': search_query,
            'sort_fields': sort_fields,
            'pagination': results['pagination']
        }
    
    def parse_filters(self, args):
        """Parse complex filter parameters"""
        filters = {}
        
        # Range filters: ?price_min=100&price_max=500
        for key, value in args.items():
            if key.endswith('_min'):
                field = key[:-4]
                filters.setdefault(field, {})['gte'] = float(value)
            elif key.endswith('_max'):
                field = key[:-4]
                filters.setdefault(field, {})['lte'] = float(value)
            elif key.endswith('_in'):
                # List filters: ?category_in=electronics,books
                field = key[:-3]
                filters[field] = {'in': value.split(',')}
            elif key not in ['page', 'per_page', 'sort', 'q']:
                # Exact match filters
                filters[key] = {'eq': value}
        
        return filters

# GraphQL-style field selection
class SelectiveDataAPI(Resource):
    def get(self):
        # Parse field selection: ?fields=id,name,email,profile.avatar_url
        fields = request.args.get('fields', '').split(',')
        include_relations = request.args.getlist('include')
        
        data = self.get_data()
        
        if fields and fields != ['']:
            data = self.select_fields(data, fields)
        
        if include_relations:
            data = self.include_relations(data, include_relations)
        
        return {'data': data}
    
    def select_fields(self, data, fields):
        """Select only specified fields"""
        if isinstance(data, list):
            return [self.select_fields(item, fields) for item in data]
        
        result = {}
        for field in fields:
            if '.' in field:
                # Nested field selection
                parts = field.split('.')
                if parts[0] in data:
                    result.setdefault(parts[0], {})
                    if isinstance(data[parts[0]], dict):
                        result[parts[0]][parts[1]] = data[parts[0]].get(parts[1])
            else:
                if field in data:
                    result[field] = data[field]
        
        return result
```

## API Security & Authentication

### Q5: How do you implement API authentication and authorization?
**Answer:**
```python
# JWT Authentication
import jwt
from functools import wraps
from datetime import datetime, timedelta

class JWTManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def generate_token(self, user_id, permissions):
        payload = {
            'user_id': user_id,
            'permissions': permissions,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

# Authentication decorator
def require_auth(permissions=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return {'error': 'No token provided'}, 401
            
            try:
                # Remove 'Bearer ' prefix
                token = token.replace('Bearer ', '')
                payload = jwt_manager.verify_token(token)
                
                # Check permissions
                if permissions:
                    user_permissions = payload.get('permissions', [])
                    if not any(perm in user_permissions for perm in permissions):
                        return {'error': 'Insufficient permissions'}, 403
                
                # Add user info to request context
                request.current_user = payload
                return f(*args, **kwargs)
            
            except Exception as e:
                return {'error': str(e)}, 401
        
        return decorated_function
    return decorator

# Usage
@app.route('/api/v1/admin/users')
@require_auth(['admin', 'user_management'])
def get_all_users():
    return jsonify({'users': get_users()})

# API Key authentication
class APIKeyAuth:
    def __init__(self):
        self.api_keys = {}  # In production, use database
    
    def validate_api_key(self, api_key):
        key_info = self.api_keys.get(api_key)
        if not key_info:
            return None
        
        # Check if key is active and not expired
        if key_info['active'] and key_info['expires_at'] > datetime.utcnow():
            return key_info
        
        return None

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return {'error': 'API key required'}, 401
        
        key_info = api_key_auth.validate_api_key(api_key)
        if not key_info:
            return {'error': 'Invalid API key'}, 401
        
        request.api_key_info = key_info
        return f(*args, **kwargs)
    
    return decorated_function
```

### Q6: How do you implement rate limiting and throttling?
**Answer:**
```python
# Rate limiting implementation
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
from datetime import datetime, timedelta

# Simple rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

@app.route('/api/v1/data')
@limiter.limit("100 per minute")
def get_data():
    return jsonify({'data': 'some data'})

# Custom rate limiter with Redis
class CustomRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, key, limit, window_seconds):
        """Check if request is allowed based on rate limit"""
        current_time = datetime.utcnow()
        window_start = current_time - timedelta(seconds=window_seconds)
        
        # Use sliding window log
        pipe = self.redis.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start.timestamp())
        
        # Count current requests
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(current_time.timestamp()): current_time.timestamp()})
        
        # Set expiration
        pipe.expire(key, window_seconds)
        
        results = pipe.execute()
        current_requests = results[1]
        
        return current_requests < limit
    
    def get_rate_limit_info(self, key, limit, window_seconds):
        """Get rate limit information"""
        current_time = datetime.utcnow()
        window_start = current_time - timedelta(seconds=window_seconds)
        
        # Count requests in current window
        current_requests = self.redis.zcount(key, window_start.timestamp(), current_time.timestamp())
        
        # Calculate reset time
        oldest_request = self.redis.zrange(key, 0, 0, withscores=True)
        reset_time = None
        if oldest_request:
            reset_time = datetime.fromtimestamp(oldest_request[0][1]) + timedelta(seconds=window_seconds)
        
        return {
            'limit': limit,
            'remaining': max(0, limit - current_requests),
            'reset_time': reset_time.isoformat() if reset_time else None,
            'retry_after': max(0, (reset_time - current_time).total_seconds()) if reset_time else 0
        }

# Rate limiting decorator
def rate_limit(limit, window_seconds, key_func=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate rate limit key
            if key_func:
                key = key_func()
            else:
                key = f"rate_limit:{request.remote_addr}:{f.__name__}"
            
            # Check rate limit
            if not rate_limiter.is_allowed(key, limit, window_seconds):
                rate_info = rate_limiter.get_rate_limit_info(key, limit, window_seconds)
                
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'rate_limit': rate_info
                })
                response.status_code = 429
                response.headers['X-RateLimit-Limit'] = str(limit)
                response.headers['X-RateLimit-Remaining'] = str(rate_info['remaining'])
                response.headers['Retry-After'] = str(int(rate_info['retry_after']))
                
                return response
            
            # Add rate limit headers to successful responses
            rate_info = rate_limiter.get_rate_limit_info(key, limit, window_seconds)
            response = f(*args, **kwargs)
            
            if hasattr(response, 'headers'):
                response.headers['X-RateLimit-Limit'] = str(limit)
                response.headers['X-RateLimit-Remaining'] = str(rate_info['remaining'])
            
            return response
        
        return decorated_function
    return decorator

# Usage with custom key function
def api_key_rate_limit_key():
    api_key = request.headers.get('X-API-Key')
    return f"rate_limit:api_key:{api_key}"

@app.route('/api/v1/premium-data')
@rate_limit(1000, 3600, key_func=api_key_rate_limit_key)  # 1000 requests per hour per API key
def get_premium_data():
    return jsonify({'data': 'premium data'})
```

## API Documentation & Testing

### Q7: How do you document APIs effectively?
**Answer:**
```python
# OpenAPI/Swagger documentation
from flask_restx import Api, Resource, fields
from flask_restx import reqparse

api = Api(app, doc='/docs/', title='Data API', description='Data Engineering API')

# Define models for documentation
dataset_model = api.model('Dataset', {
    'id': fields.Integer(required=True, description='Dataset ID'),
    'name': fields.String(required=True, description='Dataset name'),
    'description': fields.String(description='Dataset description'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'size': fields.Integer(description='Dataset size in bytes'),
    'format': fields.String(enum=['csv', 'json', 'parquet'], description='Data format')
})

dataset_list_model = api.model('DatasetList', {
    'datasets': fields.List(fields.Nested(dataset_model)),
    'total_count': fields.Integer(description='Total number of datasets'),
    'pagination': fields.Raw(description='Pagination information')
})

# Request parsers for documentation
dataset_parser = reqparse.RequestParser()
dataset_parser.add_argument('name', type=str, required=True, help='Dataset name')
dataset_parser.add_argument('description', type=str, help='Dataset description')
dataset_parser.add_argument('format', type=str, choices=['csv', 'json', 'parquet'], help='Data format')

query_parser = reqparse.RequestParser()
query_parser.add_argument('page', type=int, default=1, help='Page number')
query_parser.add_argument('per_page', type=int, default=50, help='Items per page')
query_parser.add_argument('sort', type=str, help='Sort field')
query_parser.add_argument('filter', type=str, help='Filter criteria')

@api.route('/datasets')
class DatasetListAPI(Resource):
    @api.doc('list_datasets')
    @api.expect(query_parser)
    @api.marshal_with(dataset_list_model)
    def get(self):
        """Fetch all datasets with pagination and filtering"""
        args = query_parser.parse_args()
        return self.get_datasets(args)
    
    @api.doc('create_dataset')
    @api.expect(dataset_parser)
    @api.marshal_with(dataset_model, code=201)
    def post(self):
        """Create a new dataset"""
        args = dataset_parser.parse_args()
        return self.create_dataset(args), 201

@api.route('/datasets/<int:dataset_id>')
class DatasetAPI(Resource):
    @api.doc('get_dataset')
    @api.marshal_with(dataset_model)
    @api.response(404, 'Dataset not found')
    def get(self, dataset_id):
        """Fetch a dataset by ID"""
        return self.get_dataset(dataset_id)
    
    @api.doc('update_dataset')
    @api.expect(dataset_parser)
    @api.marshal_with(dataset_model)
    def put(self, dataset_id):
        """Update a dataset"""
        args = dataset_parser.parse_args()
        return self.update_dataset(dataset_id, args)
    
    @api.doc('delete_dataset')
    @api.response(204, 'Dataset deleted')
    @api.response(404, 'Dataset not found')
    def delete(self, dataset_id):
        """Delete a dataset"""
        self.delete_dataset(dataset_id)
        return '', 204
```

### Q8: How do you implement comprehensive API testing?
**Answer:**
```python
# Unit tests for API endpoints
import unittest
from unittest.mock import patch, MagicMock
import json

class TestDatasetAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_get_datasets_success(self):
        """Test successful dataset retrieval"""
        response = self.app.get('/api/v1/datasets')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('datasets', data)
        self.assertIn('pagination', data)
    
    def test_get_datasets_with_pagination(self):
        """Test dataset retrieval with pagination"""
        response = self.app.get('/api/v1/datasets?page=2&per_page=10')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['pagination']['page'], 2)
        self.assertEqual(data['pagination']['per_page'], 10)
    
    def test_create_dataset_success(self):
        """Test successful dataset creation"""
        dataset_data = {
            'name': 'Test Dataset',
            'description': 'A test dataset',
            'format': 'csv'
        }
        
        response = self.app.post(
            '/api/v1/datasets',
            data=json.dumps(dataset_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Dataset')
    
    def test_create_dataset_validation_error(self):
        """Test dataset creation with invalid data"""
        invalid_data = {
            'description': 'Missing required name field'
        }
        
        response = self.app.post(
            '/api/v1/datasets',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_dataset_not_found(self):
        """Test retrieving non-existent dataset"""
        response = self.app.get('/api/v1/datasets/99999')
        
        self.assertEqual(response.status_code, 404)
    
    @patch('app.database.get_dataset')
    def test_get_dataset_with_mock(self, mock_get_dataset):
        """Test dataset retrieval with mocked database"""
        mock_dataset = {
            'id': 1,
            'name': 'Mock Dataset',
            'description': 'A mocked dataset'
        }
        mock_get_dataset.return_value = mock_dataset
        
        response = self.app.get('/api/v1/datasets/1')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Mock Dataset')
        mock_get_dataset.assert_called_once_with(1)

# Integration tests
class TestDatasetAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Set up test database
        self.setup_test_database()
    
    def tearDown(self):
        # Clean up test database
        self.cleanup_test_database()
    
    def test_full_dataset_lifecycle(self):
        """Test complete dataset CRUD operations"""
        # Create dataset
        dataset_data = {
            'name': 'Integration Test Dataset',
            'description': 'Dataset for integration testing',
            'format': 'json'
        }
        
        create_response = self.app.post(
            '/api/v1/datasets',
            data=json.dumps(dataset_data),
            content_type='application/json'
        )
        
        self.assertEqual(create_response.status_code, 201)
        created_dataset = json.loads(create_response.data)
        dataset_id = created_dataset['id']
        
        # Read dataset
        get_response = self.app.get(f'/api/v1/datasets/{dataset_id}')
        self.assertEqual(get_response.status_code, 200)
        retrieved_dataset = json.loads(get_response.data)
        self.assertEqual(retrieved_dataset['name'], dataset_data['name'])
        
        # Update dataset
        update_data = {
            'name': 'Updated Integration Test Dataset',
            'description': 'Updated description'
        }
        
        update_response = self.app.put(
            f'/api/v1/datasets/{dataset_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(update_response.status_code, 200)
        updated_dataset = json.loads(update_response.data)
        self.assertEqual(updated_dataset['name'], update_data['name'])
        
        # Delete dataset
        delete_response = self.app.delete(f'/api/v1/datasets/{dataset_id}')
        self.assertEqual(delete_response.status_code, 204)
        
        # Verify deletion
        get_deleted_response = self.app.get(f'/api/v1/datasets/{dataset_id}')
        self.assertEqual(get_deleted_response.status_code, 404)

# Performance tests
import time
import concurrent.futures

class TestAPIPerformance(unittest.TestCase):
    def test_api_response_time(self):
        """Test API response time under normal load"""
        start_time = time.time()
        response = self.app.get('/api/v1/datasets')
        end_time = time.time()
        
        response_time = end_time - start_time
        self.assertLess(response_time, 1.0)  # Should respond within 1 second
    
    def test_concurrent_requests(self):
        """Test API under concurrent load"""
        def make_request():
            return self.app.get('/api/v1/datasets')
        
        # Make 50 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            responses = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for response in responses:
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

## Key Takeaways

**Essential API Development for Data Engineering:**
- **RESTful design** with proper HTTP methods and status codes
- **Pagination and filtering** for large datasets
- **Authentication and authorization** with JWT/API keys
- **Rate limiting** to prevent abuse
- **Comprehensive documentation** with OpenAPI/Swagger
- **Thorough testing** including unit, integration, and performance tests
- **Error handling** with meaningful error messages
- **API versioning** for backward compatibility