# Redis Complete Guide for Data Engineering

## 🎯 What is Redis?

Redis (Remote Dictionary Server) is an **in-memory data structure store** used as a database, cache, message broker, and streaming engine. It's essential for data engineering applications requiring high-performance caching, real-time analytics, and session management.

### Key Characteristics
- **In-Memory**: Extremely fast data access with sub-millisecond latency
- **Data Structures**: Rich set of data types (strings, hashes, lists, sets, sorted sets)
- **Persistence**: Optional disk persistence with RDB and AOF
- **Clustering**: Horizontal scaling with Redis Cluster
- **Pub/Sub**: Built-in message broker capabilities

## 💾 Core Concepts

### 1. Data Types and Operations
```bash
# Strings - Basic key-value operations
SET user:1001:name "John Doe"
GET user:1001:name
INCR page_views
INCRBY user:1001:score 10
EXPIRE user:1001:session 3600  # TTL in seconds

# Hashes - Object-like structures
HSET user:1001 name "John Doe" email "john@example.com" age 30
HGET user:1001 name
HGETALL user:1001
HINCRBY user:1001 login_count 1

# Lists - Ordered collections
LPUSH recent_orders order:1001 order:1002
RPOP recent_orders
LRANGE recent_orders 0 9  # Get first 10 items
LTRIM recent_orders 0 99  # Keep only first 100 items

# Sets - Unique collections
SADD user:1001:interests "data-science" "python" "redis"
SISMEMBER user:1001:interests "python"
SINTER user:1001:interests user:1002:interests  # Intersection
SUNION user:1001:interests user:1002:interests  # Union

# Sorted Sets - Ordered by score
ZADD leaderboard 1500 "player1" 1200 "player2" 1800 "player3"
ZRANGE leaderboard 0 -1 WITHSCORES
ZREVRANK leaderboard "player1"  # Get rank (highest first)
ZINCRBY leaderboard 100 "player1"
```

### 2. Python Integration
```python
import redis
import json
from datetime import datetime, timedelta

# Connection setup
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True
)

# Connection pool for production
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=20,
    decode_responses=True
)
r = redis.Redis(connection_pool=pool)

# Basic operations
def cache_user_data(user_id, user_data):
    """Cache user data with expiration"""
    key = f"user:{user_id}"
    
    # Store as hash
    r.hset(key, mapping=user_data)
    r.expire(key, 3600)  # 1 hour TTL
    
    return True

def get_user_data(user_id):
    """Retrieve cached user data"""
    key = f"user:{user_id}"
    
    if r.exists(key):
        return r.hgetall(key)
    return None

# Session management
def create_session(user_id, session_data):
    """Create user session with automatic expiration"""
    session_id = f"session:{user_id}:{datetime.now().timestamp()}"
    
    # Store session data
    r.hset(session_id, mapping={
        'user_id': user_id,
        'created_at': datetime.now().isoformat(),
        'data': json.dumps(session_data)
    })
    
    # Set expiration (30 minutes)
    r.expire(session_id, 1800)
    
    return session_id

# Rate limiting
def is_rate_limited(user_id, limit=100, window=3600):
    """Check if user has exceeded rate limit"""
    key = f"rate_limit:{user_id}"
    
    # Use sliding window with sorted sets
    now = datetime.now().timestamp()
    window_start = now - window
    
    # Remove old entries
    r.zremrangebyscore(key, 0, window_start)
    
    # Count current requests
    current_count = r.zcard(key)
    
    if current_count >= limit:
        return True
    
    # Add current request
    r.zadd(key, {str(now): now})
    r.expire(key, window)
    
    return False
```

## 🔧 Data Engineering Use Cases

### 1. Real-time Analytics Cache
```python
import redis
import json
from datetime import datetime, timedelta

class RealTimeAnalytics:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )
    
    def track_event(self, user_id, event_type, properties=None):
        """Track user events for real-time analytics"""
        timestamp = datetime.now()
        
        # Store individual event
        event_key = f"event:{user_id}:{timestamp.timestamp()}"
        event_data = {
            'user_id': user_id,
            'event_type': event_type,
            'timestamp': timestamp.isoformat(),
            'properties': json.dumps(properties or {})
        }
        
        self.redis_client.hset(event_key, mapping=event_data)
        self.redis_client.expire(event_key, 86400)  # 24 hours
        
        # Update counters
        date_key = timestamp.strftime('%Y-%m-%d')
        hour_key = timestamp.strftime('%Y-%m-%d:%H')
        
        # Daily counters
        self.redis_client.hincrby(f"daily_events:{date_key}", event_type, 1)
        self.redis_client.hincrby(f"daily_users:{date_key}", user_id, 1)
        
        # Hourly counters
        self.redis_client.hincrby(f"hourly_events:{hour_key}", event_type, 1)
        
        # Real-time leaderboard
        if event_type == 'purchase':
            amount = properties.get('amount', 0) if properties else 0
            self.redis_client.zincrby('revenue_leaderboard', amount, user_id)
    
    def get_real_time_stats(self, date=None):
        """Get real-time analytics statistics"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get daily stats
        daily_events = self.redis_client.hgetall(f"daily_events:{date}")
        daily_users = len(self.redis_client.hgetall(f"daily_users:{date}"))
        
        # Get hourly breakdown for today
        hourly_stats = {}
        for hour in range(24):
            hour_key = f"{date}:{hour:02d}"
            hourly_events = self.redis_client.hgetall(f"hourly_events:{hour_key}")
            if hourly_events:
                hourly_stats[hour] = hourly_events
        
        # Get top revenue generators
        top_users = self.redis_client.zrevrange('revenue_leaderboard', 0, 9, withscores=True)
        
        return {
            'date': date,
            'daily_events': daily_events,
            'daily_active_users': daily_users,
            'hourly_breakdown': hourly_stats,
            'top_revenue_users': top_users
        }
    
    def get_user_activity(self, user_id, hours=24):
        """Get recent user activity"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cutoff_timestamp = cutoff_time.timestamp()
        
        # Find user events in time range
        pattern = f"event:{user_id}:*"
        events = []
        
        for key in self.redis_client.scan_iter(match=pattern):
            event_timestamp = float(key.split(':')[-1])
            if event_timestamp >= cutoff_timestamp:
                event_data = self.redis_client.hgetall(key)
                events.append(event_data)
        
        # Sort by timestamp
        events.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return events

# Usage example
analytics = RealTimeAnalytics()

# Track events
analytics.track_event('user123', 'page_view', {'page': '/dashboard'})
analytics.track_event('user123', 'purchase', {'amount': 99.99, 'product': 'premium_plan'})

# Get stats
stats = analytics.get_real_time_stats()
print(f"Today's events: {stats['daily_events']}")
print(f"Active users: {stats['daily_active_users']}")
```

### 2. Distributed Caching Layer
```python
import redis
import pickle
import hashlib
from functools import wraps

class DistributedCache:
    def __init__(self, redis_hosts=None):
        """Initialize distributed cache with multiple Redis instances"""
        if not redis_hosts:
            redis_hosts = [{'host': 'localhost', 'port': 6379}]
        
        self.redis_clients = []
        for host_config in redis_hosts:
            client = redis.Redis(**host_config, decode_responses=False)
            self.redis_clients.append(client)
    
    def _get_client(self, key):
        """Get Redis client based on key hash (consistent hashing)"""
        key_hash = int(hashlib.md5(key.encode()).hexdigest(), 16)
        client_index = key_hash % len(self.redis_clients)
        return self.redis_clients[client_index]
    
    def set(self, key, value, ttl=3600):
        """Set value in cache with TTL"""
        client = self._get_client(key)
        serialized_value = pickle.dumps(value)
        return client.setex(key, ttl, serialized_value)
    
    def get(self, key):
        """Get value from cache"""
        client = self._get_client(key)
        serialized_value = client.get(key)
        
        if serialized_value:
            return pickle.loads(serialized_value)
        return None
    
    def delete(self, key):
        """Delete key from cache"""
        client = self._get_client(key)
        return client.delete(key)
    
    def cache_result(self, ttl=3600, key_prefix=''):
        """Decorator to cache function results"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                key_parts = [key_prefix, func.__name__]
                key_parts.extend([str(arg) for arg in args])
                key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
                cache_key = ':'.join(filter(None, key_parts))
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                
                return result
            return wrapper
        return decorator

# Usage example
cache = DistributedCache()

@cache.cache_result(ttl=1800, key_prefix='user_profile')
def get_user_profile(user_id):
    """Expensive database operation"""
    # Simulate database query
    import time
    time.sleep(0.5)  # Simulate delay
    
    return {
        'user_id': user_id,
        'name': f'User {user_id}',
        'email': f'user{user_id}@example.com',
        'preferences': {'theme': 'dark', 'notifications': True}
    }

# First call - hits database
profile = get_user_profile(123)  # Takes ~0.5 seconds

# Second call - hits cache
profile = get_user_profile(123)  # Returns instantly
```

### 3. Message Queue and Pub/Sub
```python
import redis
import json
import threading
import time
from datetime import datetime

class RedisMessageQueue:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
    
    def publish_message(self, channel, message):
        """Publish message to channel"""
        message_data = {
            'timestamp': datetime.now().isoformat(),
            'data': message
        }
        
        return self.redis_client.publish(channel, json.dumps(message_data))
    
    def subscribe_to_channel(self, channel, callback):
        """Subscribe to channel and process messages"""
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        
        print(f"Subscribed to channel: {channel}")
        
        try:
            for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        message_data = json.loads(message['data'])
                        callback(channel, message_data)
                    except json.JSONDecodeError:
                        print(f"Invalid JSON message: {message['data']}")
        except KeyboardInterrupt:
            print(f"Unsubscribing from {channel}")
            pubsub.unsubscribe(channel)
            pubsub.close()
    
    def add_to_queue(self, queue_name, item, priority=0):
        """Add item to priority queue"""
        item_data = {
            'id': f"{queue_name}:{datetime.now().timestamp()}",
            'timestamp': datetime.now().isoformat(),
            'data': item
        }
        
        # Use sorted set for priority queue
        return self.redis_client.zadd(
            f"queue:{queue_name}", 
            {json.dumps(item_data): priority}
        )
    
    def get_from_queue(self, queue_name, count=1):
        """Get items from priority queue (highest priority first)"""
        queue_key = f"queue:{queue_name}"
        
        # Get highest priority items
        items = self.redis_client.zrevrange(queue_key, 0, count-1)
        
        if items:
            # Remove items from queue
            self.redis_client.zrem(queue_key, *items)
            
            # Parse and return items
            return [json.loads(item) for item in items]
        
        return []
    
    def get_queue_size(self, queue_name):
        """Get current queue size"""
        return self.redis_client.zcard(f"queue:{queue_name}")

# Usage example
mq = RedisMessageQueue()

# Message handler
def handle_data_processing_message(channel, message):
    print(f"Processing message from {channel}: {message['data']}")
    # Process the data
    time.sleep(1)  # Simulate processing
    print(f"Completed processing: {message['data']['task_id']}")

# Start subscriber in separate thread
subscriber_thread = threading.Thread(
    target=mq.subscribe_to_channel,
    args=('data_processing', handle_data_processing_message)
)
subscriber_thread.daemon = True
subscriber_thread.start()

# Publish messages
for i in range(5):
    message = {
        'task_id': f'task_{i}',
        'data_source': 'database',
        'processing_type': 'etl'
    }
    mq.publish_message('data_processing', message)
    time.sleep(0.5)

# Priority queue example
mq.add_to_queue('etl_jobs', {'job': 'daily_report'}, priority=1)
mq.add_to_queue('etl_jobs', {'job': 'urgent_fix'}, priority=10)
mq.add_to_queue('etl_jobs', {'job': 'weekly_summary'}, priority=2)

# Process jobs by priority
jobs = mq.get_from_queue('etl_jobs', count=3)
for job in jobs:
    print(f"Processing job: {job['data']['job']}")
```

## ⚡ Performance Optimization

### 1. Connection Management
```python
import redis
from redis.sentinel import Sentinel

# Connection pooling
def create_redis_pool():
    """Create optimized Redis connection pool"""
    return redis.ConnectionPool(
        host='localhost',
        port=6379,
        db=0,
        max_connections=50,
        retry_on_timeout=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        socket_keepalive=True,
        socket_keepalive_options={},
        health_check_interval=30
    )

# Redis Sentinel for high availability
def create_sentinel_connection():
    """Create Redis connection with Sentinel for HA"""
    sentinel = Sentinel([
        ('sentinel1', 26379),
        ('sentinel2', 26379),
        ('sentinel3', 26379)
    ])
    
    # Get master connection
    master = sentinel.master_for(
        'mymaster',
        socket_timeout=0.1,
        password='password',
        db=0
    )
    
    # Get slave connection for read operations
    slave = sentinel.slave_for(
        'mymaster',
        socket_timeout=0.1,
        password='password',
        db=0
    )
    
    return master, slave

# Pipeline operations for bulk operations
def bulk_operations_example():
    """Demonstrate Redis pipeline for bulk operations"""
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Use pipeline for multiple operations
    pipe = r.pipeline()
    
    # Queue multiple operations
    for i in range(1000):
        pipe.set(f"key:{i}", f"value:{i}")
        pipe.expire(f"key:{i}", 3600)
    
    # Execute all operations at once
    results = pipe.execute()
    
    print(f"Executed {len(results)} operations in pipeline")
```

### 2. Memory Optimization
```python
# Memory-efficient data structures
def optimize_memory_usage():
    """Examples of memory-efficient Redis usage"""
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Use hashes for objects instead of multiple keys
    # Instead of:
    # SET user:1001:name "John"
    # SET user:1001:email "john@example.com"
    # SET user:1001:age "30"
    
    # Use:
    r.hset('user:1001', mapping={
        'name': 'John',
        'email': 'john@example.com',
        'age': '30'
    })
    
    # Use bit operations for boolean flags
    # Set user preferences as bits
    r.setbit('user:1001:preferences', 0, 1)  # email_notifications
    r.setbit('user:1001:preferences', 1, 0)  # sms_notifications
    r.setbit('user:1001:preferences', 2, 1)  # push_notifications
    
    # Check preferences
    email_pref = r.getbit('user:1001:preferences', 0)
    
    # Use sorted sets for time-series data
    timestamp = int(time.time())
    r.zadd('user:1001:activity', {f'login:{timestamp}': timestamp})
    
    # Get recent activity (last hour)
    recent_activity = r.zrangebyscore(
        'user:1001:activity',
        timestamp - 3600,
        timestamp
    )
```

## 🔒 Security and Monitoring

### 1. Security Configuration
```bash
# redis.conf security settings
bind 127.0.0.1 10.0.0.1  # Bind to specific interfaces
port 0                   # Disable default port
port 6380               # Use custom port

# Authentication
requirepass your_strong_password
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command DEBUG ""
rename-command CONFIG "CONFIG_b840fc02d524045429941cc15f59e41cb7be6c52"

# SSL/TLS
tls-port 6380
tls-cert-file /path/to/redis.crt
tls-key-file /path/to/redis.key
tls-ca-cert-file /path/to/ca.crt
```

### 2. Monitoring and Metrics
```python
import redis
import time

class RedisMonitor:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
    
    def get_server_info(self):
        """Get comprehensive Redis server information"""
        info = self.redis_client.info()
        
        return {
            'version': info['redis_version'],
            'uptime_seconds': info['uptime_in_seconds'],
            'connected_clients': info['connected_clients'],
            'used_memory': info['used_memory'],
            'used_memory_human': info['used_memory_human'],
            'used_memory_peak': info['used_memory_peak'],
            'total_commands_processed': info['total_commands_processed'],
            'instantaneous_ops_per_sec': info['instantaneous_ops_per_sec'],
            'keyspace_hits': info['keyspace_hits'],
            'keyspace_misses': info['keyspace_misses'],
            'expired_keys': info['expired_keys'],
            'evicted_keys': info['evicted_keys']
        }
    
    def calculate_hit_ratio(self):
        """Calculate cache hit ratio"""
        info = self.redis_client.info()
        hits = info['keyspace_hits']
        misses = info['keyspace_misses']
        
        if hits + misses == 0:
            return 0
        
        return (hits / (hits + misses)) * 100
    
    def monitor_slow_queries(self):
        """Monitor slow queries"""
        slow_log = self.redis_client.slowlog_get(10)
        
        slow_queries = []
        for entry in slow_log:
            slow_queries.append({
                'id': entry['id'],
                'timestamp': entry['start_time'],
                'duration_microseconds': entry['duration'],
                'command': ' '.join(entry['command'])
            })
        
        return slow_queries
    
    def get_memory_usage_by_key_pattern(self, pattern='*'):
        """Analyze memory usage by key patterns"""
        memory_usage = {}
        
        for key in self.redis_client.scan_iter(match=pattern):
            try:
                memory = self.redis_client.memory_usage(key)
                key_type = self.redis_client.type(key)
                
                if key_type not in memory_usage:
                    memory_usage[key_type] = {'count': 0, 'total_memory': 0}
                
                memory_usage[key_type]['count'] += 1
                memory_usage[key_type]['total_memory'] += memory
                
            except redis.ResponseError:
                # Handle keys that might have expired
                continue
        
        return memory_usage

# Usage
monitor = RedisMonitor()

# Get server stats
stats = monitor.get_server_info()
print(f"Redis version: {stats['version']}")
print(f"Memory usage: {stats['used_memory_human']}")
print(f"Hit ratio: {monitor.calculate_hit_ratio():.2f}%")

# Monitor slow queries
slow_queries = monitor.monitor_slow_queries()
for query in slow_queries:
    print(f"Slow query: {query['command']} ({query['duration_microseconds']}μs)")
```

## 🎯 Best Practices Summary

### 1. Data Modeling Best Practices
- **Use appropriate data types** for your use case
- **Implement proper key naming conventions** (e.g., `object:id:field`)
- **Set TTL on temporary data** to prevent memory bloat
- **Use hashes for objects** instead of multiple string keys

### 2. Performance Best Practices
- **Use connection pooling** for production applications
- **Implement pipelining** for bulk operations
- **Monitor memory usage** and implement eviction policies
- **Use Redis Cluster** for horizontal scaling

### 3. Security Best Practices
- **Enable authentication** with strong passwords
- **Bind to specific interfaces** instead of all interfaces
- **Rename dangerous commands** or disable them
- **Use SSL/TLS** for encrypted connections

### 4. Operational Best Practices
- **Monitor key metrics** (hit ratio, memory usage, slow queries)
- **Implement proper backup strategies** (RDB + AOF)
- **Set up Redis Sentinel** for high availability
- **Plan for capacity** and implement monitoring alerts

This guide provides essential Redis knowledge for data engineering. Focus on understanding data structures, caching patterns, and performance optimization for building high-performance data applications.