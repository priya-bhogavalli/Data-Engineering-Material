# Redis Comprehensive Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Data Structures & Operations (16-30)](#data-structures--operations-16-30)
3. [Performance & Optimization (31-45)](#performance--optimization-31-45)
4. [Persistence & Durability (46-60)](#persistence--durability-46-60)
5. [Clustering & High Availability (61-75)](#clustering--high-availability-61-75)
6. [Security & Administration (76-90)](#security--administration-76-90)
7. [Integration & Architecture (91-100)](#integration--architecture-91-100)

---

## 🎯 **Introduction**

Redis is an open-source, in-memory data structure store used as a database, cache, and message broker. For data engineers, Redis provides high-performance caching, real-time analytics, session management, and pub/sub messaging capabilities.

**Why Redis is Critical for Data Engineers:**
- **High Performance**: Sub-millisecond latency for real-time applications
- **Rich Data Structures**: Strings, hashes, lists, sets, sorted sets, streams
- **Persistence Options**: RDB snapshots and AOF logging
- **Scalability**: Redis Cluster for horizontal scaling
- **Versatility**: Caching, session store, message broker, real-time analytics

---

## Core Concepts Questions (1-15)

### 1. What is Redis and how does it differ from traditional databases?
**Answer**: 
Redis (Remote Dictionary Server) is an in-memory data structure store that differs significantly from traditional disk-based databases.

**Key Differences:**
- **Storage**: In-memory vs. disk-based storage
- **Performance**: Sub-millisecond latency vs. millisecond latency
- **Data Model**: Key-value with rich data structures vs. relational tables
- **Persistence**: Optional persistence vs. always persistent
- **Use Cases**: Caching, sessions, real-time analytics vs. transactional systems

```python
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Basic operations
r.set('user:1000', 'John Doe')
user = r.get('user:1000')
print(user.decode('utf-8'))  # Output: John Doe

# Set with expiration
r.setex('session:abc123', 3600, 'user_data')  # Expires in 1 hour

# Check if key exists
if r.exists('user:1000'):
    print("User exists")
```

### 2. Explain Redis data structures and their use cases.
**Answer**: 
Redis supports multiple data structures, each optimized for specific use cases.

**String Operations:**
```python
# Basic string operations
r.set('counter', 0)
r.incr('counter')  # Atomic increment
r.incrby('counter', 5)  # Increment by 5
r.decr('counter')  # Atomic decrement

# Bit operations
r.setbit('user_activity', 100, 1)  # Set bit at position 100
r.getbit('user_activity', 100)    # Get bit at position 100
r.bitcount('user_activity')       # Count set bits
```

**Hash Operations:**
```python
# User profile as hash
r.hset('user:1000', mapping={
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30,
    'last_login': '2024-01-15'
})

# Get specific field
name = r.hget('user:1000', 'name')

# Get all fields
user_data = r.hgetall('user:1000')

# Increment numeric field
r.hincrby('user:1000', 'login_count', 1)
```

**List Operations:**
```python
# Message queue using lists
r.lpush('task_queue', 'process_order_123')
r.lpush('task_queue', 'send_email_456')

# Process tasks (blocking pop)
task = r.brpop('task_queue', timeout=10)

# Recent activity log
r.lpush('user:1000:activity', 'logged_in')
r.ltrim('user:1000:activity', 0, 99)  # Keep only last 100 activities
```

### 3. How does Redis handle memory management and what happens when memory is full?
**Answer**: 
Redis uses various memory management strategies and eviction policies.

**Memory Configuration:**
```bash
# redis.conf settings
maxmemory 2gb
maxmemory-policy allkeys-lru

# Available eviction policies:
# noeviction - return errors when memory limit reached
# allkeys-lru - evict least recently used keys
# volatile-lru - evict LRU keys with expire set
# allkeys-random - evict random keys
# volatile-random - evict random keys with expire set
# volatile-ttl - evict keys with shortest TTL
```

**Memory Monitoring:**
```python
# Check memory usage
info = r.info('memory')
print(f"Used memory: {info['used_memory_human']}")
print(f"Max memory: {info['maxmemory_human']}")

# Memory usage by key pattern
def analyze_memory_usage(pattern='*'):
    keys = r.keys(pattern)
    total_memory = 0
    for key in keys:
        memory = r.memory_usage(key)
        total_memory += memory
        print(f"{key}: {memory} bytes")
    return total_memory
```

## Data Structures & Operations (16-30)

### 4. How do you implement a distributed cache with Redis?
**Answer**: 
Redis serves as an excellent distributed cache with various patterns and strategies.

**Basic Caching Pattern:**
```python
import json
import hashlib
from datetime import timedelta

class RedisCache:
    def __init__(self, redis_client, default_ttl=3600):
        self.redis = redis_client
        self.default_ttl = default_ttl
    
    def get(self, key):
        """Get value from cache"""
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key, value, ttl=None):
        """Set value in cache with TTL"""
        ttl = ttl or self.default_ttl
        serialized = json.dumps(value)
        self.redis.setex(key, ttl, serialized)
    
    def delete(self, key):
        """Delete key from cache"""
        self.redis.delete(key)
    
    def get_or_set(self, key, fetch_func, ttl=None):
        """Get from cache or fetch and cache"""
        value = self.get(key)
        if value is None:
            value = fetch_func()
            self.set(key, value, ttl)
        return value

# Usage example
cache = RedisCache(r)

def expensive_database_query(user_id):
    # Simulate expensive operation
    return {"user_id": user_id, "profile": "data"}

# Cache database query results
user_data = cache.get_or_set(
    f"user_profile:{user_id}",
    lambda: expensive_database_query(user_id),
    ttl=1800  # 30 minutes
)
```

**Cache-Aside Pattern:**
```python
def get_user_profile(user_id):
    cache_key = f"user:{user_id}"
    
    # Try cache first
    cached_data = r.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # Cache miss - fetch from database
    user_data = fetch_from_database(user_id)
    
    # Store in cache
    r.setex(cache_key, 3600, json.dumps(user_data))
    
    return user_data

def update_user_profile(user_id, profile_data):
    # Update database
    update_database(user_id, profile_data)
    
    # Invalidate cache
    r.delete(f"user:{user_id}")
```

### 5. How do you implement real-time analytics with Redis?
**Answer**: 
Redis provides excellent support for real-time analytics through various data structures.

**Real-time Counters:**
```python
from datetime import datetime, timedelta

class RealTimeAnalytics:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def track_event(self, event_type, user_id=None, metadata=None):
        """Track an event occurrence"""
        timestamp = datetime.now()
        
        # Increment global counter
        self.redis.incr(f"events:{event_type}:total")
        
        # Increment hourly counter
        hour_key = timestamp.strftime("%Y-%m-%d:%H")
        self.redis.incr(f"events:{event_type}:hourly:{hour_key}")
        self.redis.expire(f"events:{event_type}:hourly:{hour_key}", 86400)  # 24 hours
        
        # Track unique users (HyperLogLog)
        if user_id:
            self.redis.pfadd(f"unique_users:{event_type}:{hour_key}", user_id)
            self.redis.expire(f"unique_users:{event_type}:{hour_key}", 86400)
    
    def get_event_stats(self, event_type, hours_back=24):
        """Get event statistics for the last N hours"""
        stats = {}
        current_time = datetime.now()
        
        for i in range(hours_back):
            hour = current_time - timedelta(hours=i)
            hour_key = hour.strftime("%Y-%m-%d:%H")
            
            count = self.redis.get(f"events:{event_type}:hourly:{hour_key}")
            unique_users = self.redis.pfcount(f"unique_users:{event_type}:{hour_key}")
            
            stats[hour_key] = {
                'count': int(count) if count else 0,
                'unique_users': unique_users
            }
        
        return stats

# Usage
analytics = RealTimeAnalytics(r)

# Track events
analytics.track_event('page_view', user_id='user123')
analytics.track_event('purchase', user_id='user456')

# Get statistics
stats = analytics.get_event_stats('page_view', hours_back=12)
```

**Sliding Window Analytics:**
```python
def track_api_requests(endpoint, user_id):
    """Track API requests with sliding window"""
    current_time = int(time.time())
    window_size = 3600  # 1 hour window
    
    # Use sorted set for sliding window
    key = f"api_requests:{endpoint}:{user_id}"
    
    # Add current request
    r.zadd(key, {current_time: current_time})
    
    # Remove old entries outside window
    r.zremrangebyscore(key, 0, current_time - window_size)
    
    # Set expiration
    r.expire(key, window_size)
    
    # Get request count in window
    request_count = r.zcard(key)
    
    return request_count

def get_top_endpoints(limit=10):
    """Get top API endpoints by request count"""
    pattern = "api_requests:*"
    keys = r.keys(pattern)
    
    endpoint_counts = {}
    for key in keys:
        endpoint = key.decode().split(':')[1]
        count = r.zcard(key)
        endpoint_counts[endpoint] = endpoint_counts.get(endpoint, 0) + count
    
    # Sort by count
    return sorted(endpoint_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
```

## Performance & Optimization (31-45)

### 6. How do you optimize Redis performance for high-throughput applications?
**Answer**: 
Multiple strategies for optimizing Redis performance in high-throughput scenarios.

**Connection Pooling:**
```python
import redis.connection

# Configure connection pool
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=20,
    retry_on_timeout=True,
    socket_keepalive=True,
    socket_keepalive_options={}
)

r = redis.Redis(connection_pool=pool)

# Use pipelining for batch operations
def batch_operations():
    pipe = r.pipeline()
    
    # Queue multiple operations
    for i in range(1000):
        pipe.set(f"key:{i}", f"value:{i}")
        pipe.expire(f"key:{i}", 3600)
    
    # Execute all operations at once
    results = pipe.execute()
    return results
```

**Lua Scripts for Atomic Operations:**
```python
# Lua script for atomic rate limiting
rate_limit_script = """
local key = KEYS[1]
local window = tonumber(ARGV[1])
local limit = tonumber(ARGV[2])
local current_time = tonumber(ARGV[3])

-- Remove expired entries
redis.call('ZREMRANGEBYSCORE', key, 0, current_time - window)

-- Get current count
local current_count = redis.call('ZCARD', key)

if current_count < limit then
    -- Add current request
    redis.call('ZADD', key, current_time, current_time)
    redis.call('EXPIRE', key, window)
    return {1, limit - current_count - 1}
else
    return {0, 0}
end
"""

# Register script
rate_limit_sha = r.script_load(rate_limit_script)

def check_rate_limit(user_id, window=3600, limit=1000):
    """Check if user is within rate limit"""
    key = f"rate_limit:{user_id}"
    current_time = int(time.time())
    
    result = r.evalsha(rate_limit_sha, 1, key, window, limit, current_time)
    allowed, remaining = result
    
    return bool(allowed), remaining
```

**Memory Optimization:**
```python
# Use appropriate data structures
def optimize_memory_usage():
    # Use hashes for objects instead of multiple keys
    # Instead of:
    # r.set('user:1000:name', 'John')
    # r.set('user:1000:email', 'john@example.com')
    
    # Use:
    r.hset('user:1000', mapping={
        'name': 'John',
        'email': 'john@example.com'
    })
    
    # Use sets for unique collections
    r.sadd('active_users', 'user1', 'user2', 'user3')
    
    # Use sorted sets for rankings
    r.zadd('leaderboard', {'player1': 1000, 'player2': 950})
```

### 7. How do you implement distributed locking with Redis?
**Answer**: 
Redis can implement distributed locks for coordinating access across multiple processes.

**Simple Distributed Lock:**
```python
import time
import uuid

class RedisLock:
    def __init__(self, redis_client, key, timeout=10, retry_delay=0.1):
        self.redis = redis_client
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.retry_delay = retry_delay
        self.identifier = str(uuid.uuid4())
    
    def acquire(self):
        """Acquire the lock"""
        end_time = time.time() + self.timeout
        
        while time.time() < end_time:
            # Try to acquire lock
            if self.redis.set(self.key, self.identifier, nx=True, ex=self.timeout):
                return True
            
            time.sleep(self.retry_delay)
        
        return False
    
    def release(self):
        """Release the lock"""
        # Lua script for atomic release
        release_script = """
        if redis.call('GET', KEYS[1]) == ARGV[1] then
            return redis.call('DEL', KEYS[1])
        else
            return 0
        end
        """
        
        return self.redis.eval(release_script, 1, self.key, self.identifier)
    
    def __enter__(self):
        if self.acquire():
            return self
        raise Exception("Could not acquire lock")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# Usage
def critical_section():
    with RedisLock(r, 'resource_123', timeout=30):
        # Only one process can execute this at a time
        print("Performing critical operation...")
        time.sleep(5)
        print("Critical operation completed")
```

**Redlock Algorithm (Multiple Redis Instances):**
```python
class Redlock:
    def __init__(self, redis_instances, key, ttl=10000):
        self.redis_instances = redis_instances
        self.key = key
        self.ttl = ttl  # milliseconds
        self.identifier = str(uuid.uuid4())
        self.quorum = len(redis_instances) // 2 + 1
    
    def acquire(self):
        """Acquire lock using Redlock algorithm"""
        start_time = int(time.time() * 1000)
        acquired_locks = 0
        
        for redis_instance in self.redis_instances:
            try:
                # Try to acquire lock on this instance
                if redis_instance.set(
                    self.key, 
                    self.identifier, 
                    px=self.ttl, 
                    nx=True
                ):
                    acquired_locks += 1
            except:
                # Instance unavailable
                continue
        
        # Check if we have quorum
        elapsed_time = int(time.time() * 1000) - start_time
        validity_time = self.ttl - elapsed_time - 100  # drift compensation
        
        if acquired_locks >= self.quorum and validity_time > 0:
            return True
        else:
            # Release acquired locks
            self.release()
            return False
    
    def release(self):
        """Release lock from all instances"""
        release_script = """
        if redis.call('GET', KEYS[1]) == ARGV[1] then
            return redis.call('DEL', KEYS[1])
        else
            return 0
        end
        """
        
        for redis_instance in self.redis_instances:
            try:
                redis_instance.eval(release_script, 1, self.key, self.identifier)
            except:
                continue
```

## Persistence & Durability (46-60)

### 8. Explain Redis persistence mechanisms and when to use each.
**Answer**: 
Redis offers two persistence mechanisms: RDB snapshots and AOF (Append Only File).

**RDB (Redis Database) Snapshots:**
```bash
# redis.conf RDB configuration
save 900 1      # Save if at least 1 key changed in 900 seconds
save 300 10     # Save if at least 10 keys changed in 300 seconds
save 60 10000   # Save if at least 10000 keys changed in 60 seconds

# Compression and checksums
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /var/lib/redis
```

**AOF (Append Only File):**
```bash
# redis.conf AOF configuration
appendonly yes
appendfilename "appendonly.aof"

# Fsync policy
appendfsync everysec  # Options: always, everysec, no

# AOF rewrite configuration
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

**Python Configuration:**
```python
def configure_persistence():
    # Force RDB snapshot
    r.bgsave()
    
    # Check last save time
    last_save = r.lastsave()
    print(f"Last save: {last_save}")
    
    # Force AOF rewrite
    r.bgrewriteaof()
    
    # Get persistence info
    info = r.info('persistence')
    print(f"RDB changes since last save: {info['rdb_changes_since_last_save']}")
    print(f"AOF enabled: {info['aof_enabled']}")

# Backup strategy
def backup_redis():
    """Create backup of Redis data"""
    # Trigger background save
    r.bgsave()
    
    # Wait for save to complete
    while r.info('persistence')['rdb_bgsave_in_progress']:
        time.sleep(1)
    
    # Copy RDB file to backup location
    import shutil
    shutil.copy('/var/lib/redis/dump.rdb', '/backup/redis-backup.rdb')
```

### 9. How do you handle Redis failover and high availability?
**Answer**: 
Redis provides several mechanisms for high availability and failover.

**Redis Sentinel Configuration:**
```python
import redis.sentinel

# Sentinel configuration
sentinels = [
    ('sentinel1.example.com', 26379),
    ('sentinel2.example.com', 26379),
    ('sentinel3.example.com', 26379)
]

# Create sentinel connection
sentinel = redis.sentinel.Sentinel(sentinels, socket_timeout=0.1)

# Get master and slave connections
master = sentinel.master_for('mymaster', socket_timeout=0.1)
slave = sentinel.slave_for('mymaster', socket_timeout=0.1)

# Use master for writes, slave for reads
def write_data(key, value):
    master.set(key, value)

def read_data(key):
    try:
        return slave.get(key)
    except:
        # Fallback to master if slave unavailable
        return master.get(key)
```

**Health Monitoring:**
```python
def monitor_redis_health():
    """Monitor Redis instance health"""
    try:
        # Check connectivity
        response = r.ping()
        if not response:
            raise Exception("Redis ping failed")
        
        # Check memory usage
        info = r.info('memory')
        memory_usage = info['used_memory'] / info['maxmemory'] * 100
        if memory_usage > 90:
            print(f"WARNING: High memory usage: {memory_usage}%")
        
        # Check connected clients
        clients = info['connected_clients']
        if clients > 1000:
            print(f"WARNING: High client count: {clients}")
        
        # Check replication lag
        repl_info = r.info('replication')
        if repl_info['role'] == 'slave':
            lag = repl_info.get('master_last_io_seconds_ago', 0)
            if lag > 5:
                print(f"WARNING: Replication lag: {lag} seconds")
        
        return True
        
    except Exception as e:
        print(f"Redis health check failed: {e}")
        return False
```

## Clustering & High Availability (61-75)

### 10. How does Redis Cluster work and when should you use it?
**Answer**: 
Redis Cluster provides horizontal scaling and automatic failover.

**Redis Cluster Setup:**
```python
from rediscluster import RedisCluster

# Cluster nodes
startup_nodes = [
    {"host": "redis-node1.example.com", "port": "7000"},
    {"host": "redis-node2.example.com", "port": "7000"},
    {"host": "redis-node3.example.com", "port": "7000"},
    {"host": "redis-node4.example.com", "port": "7000"},
    {"host": "redis-node5.example.com", "port": "7000"},
    {"host": "redis-node6.example.com", "port": "7000"}
]

# Create cluster connection
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# Cluster operations
def cluster_operations():
    # Set data (automatically sharded)
    rc.set('user:1000', 'John Doe')
    rc.set('user:2000', 'Jane Smith')
    
    # Get data
    user1 = rc.get('user:1000')
    user2 = rc.get('user:2000')
    
    # Hash tags for related keys
    rc.set('user:{1000}:profile', 'profile_data')
    rc.set('user:{1000}:settings', 'settings_data')
    # Both keys will be on same node due to {1000} hash tag
```

**Cluster Monitoring:**
```python
def monitor_cluster():
    """Monitor Redis Cluster health"""
    try:
        # Get cluster info
        cluster_info = rc.cluster_info()
        print(f"Cluster state: {cluster_info['cluster_state']}")
        print(f"Cluster slots assigned: {cluster_info['cluster_slots_assigned']}")
        
        # Get cluster nodes
        nodes = rc.cluster_nodes()
        for node_id, node_info in nodes.items():
            print(f"Node {node_id}: {node_info['flags']} - {node_info['host']}:{node_info['port']}")
        
        # Check slot distribution
        slots = rc.cluster_slots()
        for slot_range in slots:
            start_slot, end_slot = slot_range[0], slot_range[1]
            master = slot_range[2]
            print(f"Slots {start_slot}-{end_slot}: {master[0]}:{master[1]}")
        
    except Exception as e:
        print(f"Cluster monitoring failed: {e}")
```

### 11. How do you implement data partitioning strategies in Redis?
**Answer**: 
Various partitioning strategies for distributing data across Redis instances.

**Hash-based Partitioning:**
```python
import hashlib

class HashPartitioner:
    def __init__(self, redis_instances):
        self.redis_instances = redis_instances
        self.num_instances = len(redis_instances)
    
    def get_instance(self, key):
        """Get Redis instance for a key using hash partitioning"""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        instance_index = hash_value % self.num_instances
        return self.redis_instances[instance_index]
    
    def set(self, key, value, **kwargs):
        """Set value in appropriate partition"""
        instance = self.get_instance(key)
        return instance.set(key, value, **kwargs)
    
    def get(self, key):
        """Get value from appropriate partition"""
        instance = self.get_instance(key)
        return instance.get(key)
    
    def delete(self, key):
        """Delete key from appropriate partition"""
        instance = self.get_instance(key)
        return instance.delete(key)

# Usage
redis_instances = [
    redis.Redis(host='redis1.example.com', port=6379),
    redis.Redis(host='redis2.example.com', port=6379),
    redis.Redis(host='redis3.example.com', port=6379)
]

partitioner = HashPartitioner(redis_instances)

# Data automatically goes to correct partition
partitioner.set('user:1000', 'John Doe')
partitioner.set('user:2000', 'Jane Smith')
```

**Consistent Hashing:**
```python
import bisect
import hashlib

class ConsistentHashRing:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def add_node(self, node):
        """Add a node to the hash ring"""
        for i in range(self.replicas):
            key = self.hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        
        self.sorted_keys.sort()
    
    def remove_node(self, node):
        """Remove a node from the hash ring"""
        for i in range(self.replicas):
            key = self.hash(f"{node}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)
    
    def get_node(self, key):
        """Get the node responsible for a key"""
        if not self.ring:
            return None
        
        hash_key = self.hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_key)
        
        if idx == len(self.sorted_keys):
            idx = 0
        
        return self.ring[self.sorted_keys[idx]]
    
    def hash(self, key):
        """Hash function"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

# Usage with Redis instances
nodes = ['redis1:6379', 'redis2:6379', 'redis3:6379']
hash_ring = ConsistentHashRing(nodes)

def get_redis_client(node):
    host, port = node.split(':')
    return redis.Redis(host=host, port=int(port))

def distributed_set(key, value):
    node = hash_ring.get_node(key)
    client = get_redis_client(node)
    return client.set(key, value)

def distributed_get(key):
    node = hash_ring.get_node(key)
    client = get_redis_client(node)
    return client.get(key)
```

## Security & Administration (76-90)

### 12. How do you secure Redis in production environments?
**Answer**: 
Redis security involves multiple layers of protection.

**Authentication and Authorization:**
```bash
# redis.conf security settings
requirepass your_strong_password_here

# ACL (Access Control Lists) - Redis 6+
user default off
user app_user on >app_password ~cached:* +@read +@write -@dangerous
user admin_user on >admin_password ~* +@all
```

**Python Security Implementation:**
```python
# Secure connection with authentication
r = redis.Redis(
    host='redis.example.com',
    port=6379,
    password='your_strong_password',
    ssl=True,
    ssl_cert_reqs='required',
    ssl_ca_certs='/path/to/ca.crt',
    ssl_certfile='/path/to/client.crt',
    ssl_keyfile='/path/to/client.key'
)

# Connection with ACL user
r_app = redis.Redis(
    host='redis.example.com',
    port=6379,
    username='app_user',
    password='app_password'
)

def secure_operations():
    """Demonstrate secure Redis operations"""
    try:
        # Test connection
        r.ping()
        
        # Use connection pooling with authentication
        pool = redis.ConnectionPool(
            host='redis.example.com',
            port=6379,
            password='your_password',
            max_connections=10
        )
        
        secure_redis = redis.Redis(connection_pool=pool)
        
        # Perform operations
        secure_redis.set('secure_key', 'secure_value')
        
    except redis.AuthenticationError:
        print("Authentication failed")
    except redis.ConnectionError:
        print("Connection failed")
```

**Network Security:**
```python
# IP binding and firewall rules
def configure_network_security():
    """Network security configuration"""
    # In redis.conf:
    # bind 127.0.0.1 10.0.0.100  # Bind to specific IPs only
    # protected-mode yes          # Enable protected mode
    # port 0                      # Disable TCP port
    # unixsocket /tmp/redis.sock  # Use Unix socket instead
    
    # Connect via Unix socket
    r_unix = redis.Redis(unix_socket_path='/tmp/redis.sock')
    
    return r_unix
```

### 13. How do you monitor and troubleshoot Redis performance issues?
**Answer**: 
Comprehensive monitoring and troubleshooting strategies for Redis.

**Performance Monitoring:**
```python
import time
from datetime import datetime

class RedisMonitor:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def get_performance_metrics(self):
        """Collect comprehensive performance metrics"""
        info = self.redis.info()
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'memory': {
                'used_memory': info['used_memory'],
                'used_memory_human': info['used_memory_human'],
                'used_memory_peak': info['used_memory_peak'],
                'memory_fragmentation_ratio': info.get('mem_fragmentation_ratio', 0)
            },
            'clients': {
                'connected_clients': info['connected_clients'],
                'blocked_clients': info['blocked_clients'],
                'client_recent_max_input_buffer': info.get('client_recent_max_input_buffer', 0)
            },
            'operations': {
                'total_commands_processed': info['total_commands_processed'],
                'instantaneous_ops_per_sec': info['instantaneous_ops_per_sec'],
                'keyspace_hits': info['keyspace_hits'],
                'keyspace_misses': info['keyspace_misses']
            },
            'persistence': {
                'rdb_changes_since_last_save': info['rdb_changes_since_last_save'],
                'rdb_last_save_time': info['rdb_last_save_time'],
                'aof_enabled': info.get('aof_enabled', 0)
            }
        }
        
        # Calculate hit ratio
        hits = metrics['operations']['keyspace_hits']
        misses = metrics['operations']['keyspace_misses']
        total_requests = hits + misses
        
        if total_requests > 0:
            metrics['operations']['hit_ratio'] = hits / total_requests * 100
        else:
            metrics['operations']['hit_ratio'] = 0
        
        return metrics
    
    def check_slow_queries(self):
        """Check for slow queries"""
        try:
            # Get slow log entries
            slow_log = self.redis.slowlog_get(10)
            
            slow_queries = []
            for entry in slow_log:
                slow_queries.append({
                    'id': entry['id'],
                    'start_time': entry['start_time'],
                    'duration': entry['duration'],
                    'command': ' '.join(entry['command'])
                })
            
            return slow_queries
        except:
            return []
    
    def analyze_memory_usage(self):
        """Analyze memory usage patterns"""
        info = self.redis.info('memory')
        
        analysis = {
            'total_system_memory': info.get('total_system_memory', 0),
            'used_memory': info['used_memory'],
            'used_memory_rss': info['used_memory_rss'],
            'used_memory_peak': info['used_memory_peak'],
            'mem_fragmentation_ratio': info.get('mem_fragmentation_ratio', 1.0),
            'allocator_allocated': info.get('allocator_allocated', 0),
            'allocator_active': info.get('allocator_active', 0)
        }
        
        # Memory efficiency analysis
        if analysis['mem_fragmentation_ratio'] > 1.5:
            analysis['warning'] = "High memory fragmentation detected"
        
        if analysis['used_memory_rss'] > analysis['used_memory'] * 1.5:
            analysis['warning'] = "High RSS memory usage"
        
        return analysis

# Usage
monitor = RedisMonitor(r)

def continuous_monitoring():
    """Continuous monitoring loop"""
    while True:
        metrics = monitor.get_performance_metrics()
        slow_queries = monitor.check_slow_queries()
        memory_analysis = monitor.analyze_memory_usage()
        
        # Log metrics
        print(f"Ops/sec: {metrics['operations']['instantaneous_ops_per_sec']}")
        print(f"Hit ratio: {metrics['operations']['hit_ratio']:.2f}%")
        print(f"Memory usage: {metrics['memory']['used_memory_human']}")
        
        # Alert on issues
        if metrics['operations']['hit_ratio'] < 80:
            print("WARNING: Low cache hit ratio")
        
        if slow_queries:
            print(f"WARNING: {len(slow_queries)} slow queries detected")
        
        time.sleep(60)  # Monitor every minute
```

## Integration & Architecture (91-100)

### 14. How do you integrate Redis with data pipelines and streaming systems?
**Answer**: 
Redis integrates seamlessly with modern data pipeline architectures.

**Apache Kafka + Redis Integration:**
```python
from kafka import KafkaConsumer, KafkaProducer
import json

class KafkaRedisProcessor:
    def __init__(self, redis_client, kafka_config):
        self.redis = redis_client
        self.kafka_config = kafka_config
        self.consumer = KafkaConsumer(**kafka_config['consumer'])
        self.producer = KafkaProducer(**kafka_config['producer'])
    
    def process_events(self):
        """Process Kafka events and update Redis"""
        for message in self.consumer:
            try:
                event = json.loads(message.value.decode('utf-8'))
                
                # Process different event types
                if event['type'] == 'user_activity':
                    self.update_user_activity(event)
                elif event['type'] == 'purchase':
                    self.update_purchase_metrics(event)
                elif event['type'] == 'page_view':
                    self.update_page_views(event)
                
            except Exception as e:
                print(f"Error processing event: {e}")
    
    def update_user_activity(self, event):
        """Update user activity in Redis"""
        user_id = event['user_id']
        timestamp = event['timestamp']
        
        # Update last seen
        self.redis.hset(f"user:{user_id}", "last_seen", timestamp)
        
        # Add to recent activity
        self.redis.lpush(f"user:{user_id}:activity", json.dumps(event))
        self.redis.ltrim(f"user:{user_id}:activity", 0, 99)  # Keep last 100
        
        # Update daily active users
        date = timestamp.split('T')[0]
        self.redis.sadd(f"active_users:{date}", user_id)
        self.redis.expire(f"active_users:{date}", 86400 * 7)  # Keep for 7 days
    
    def update_purchase_metrics(self, event):
        """Update purchase metrics in Redis"""
        # Real-time revenue tracking
        amount = event['amount']
        self.redis.incrbyfloat("revenue:total", amount)
        
        # Hourly revenue
        hour = event['timestamp'][:13]  # YYYY-MM-DDTHH
        self.redis.incrbyfloat(f"revenue:hourly:{hour}", amount)
        self.redis.expire(f"revenue:hourly:{hour}", 86400)
        
        # Product popularity
        product_id = event['product_id']
        self.redis.zincrby("popular_products", 1, product_id)

# Spark Streaming + Redis Integration
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def spark_redis_integration():
    """Integrate Spark Streaming with Redis"""
    spark = SparkSession.builder \
        .appName("SparkRedisIntegration") \
        .config("spark.redis.host", "localhost") \
        .config("spark.redis.port", "6379") \
        .getOrCreate()
    
    # Read from Kafka
    kafka_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "user_events") \
        .load()
    
    # Parse JSON data
    parsed_df = kafka_df.select(
        from_json(col("value").cast("string"), event_schema).alias("data")
    ).select("data.*")
    
    # Aggregate data
    aggregated_df = parsed_df \
        .groupBy(
            window(col("timestamp"), "1 minute"),
            col("event_type")
        ) \
        .agg(
            count("*").alias("event_count"),
            countDistinct("user_id").alias("unique_users")
        )
    
    # Write to Redis
    def write_to_redis(df, epoch_id):
        for row in df.collect():
            key = f"metrics:{row.event_type}:{row.window.start}"
            value = {
                "count": row.event_count,
                "unique_users": row.unique_users,
                "timestamp": str(row.window.start)
            }
            r.hset(key, mapping=value)
            r.expire(key, 3600)  # 1 hour TTL
    
    # Start streaming query
    query = aggregated_df.writeStream \
        .foreachBatch(write_to_redis) \
        .start()
    
    query.awaitTermination()
```

### 15. How do you design Redis architecture for microservices?
**Answer**: 
Redis architecture patterns for microservices environments.

**Service-Specific Redis Instances:**
```python
class MicroserviceRedisManager:
    def __init__(self):
        self.services = {
            'user_service': redis.Redis(host='redis-users.internal', port=6379, db=0),
            'order_service': redis.Redis(host='redis-orders.internal', port=6379, db=0),
            'inventory_service': redis.Redis(host='redis-inventory.internal', port=6379, db=0),
            'session_service': redis.Redis(host='redis-sessions.internal', port=6379, db=0)
        }
        
        # Shared cache for cross-service data
        self.shared_cache = redis.Redis(host='redis-shared.internal', port=6379, db=0)
    
    def get_service_cache(self, service_name):
        """Get Redis instance for specific service"""
        return self.services.get(service_name)
    
    def get_shared_cache(self):
        """Get shared Redis instance"""
        return self.shared_cache

# User Service Redis Operations
class UserServiceCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.prefix = "user_service"
    
    def cache_user_profile(self, user_id, profile_data, ttl=3600):
        """Cache user profile data"""
        key = f"{self.prefix}:profile:{user_id}"
        self.redis.hset(key, mapping=profile_data)
        self.redis.expire(key, ttl)
    
    def get_user_profile(self, user_id):
        """Get cached user profile"""
        key = f"{self.prefix}:profile:{user_id}"
        return self.redis.hgetall(key)
    
    def cache_user_permissions(self, user_id, permissions):
        """Cache user permissions"""
        key = f"{self.prefix}:permissions:{user_id}"
        self.redis.sadd(key, *permissions)
        self.redis.expire(key, 1800)  # 30 minutes
    
    def check_user_permission(self, user_id, permission):
        """Check if user has specific permission"""
        key = f"{self.prefix}:permissions:{user_id}"
        return self.redis.sismember(key, permission)

# Cross-Service Communication Cache
class CrossServiceCache:
    def __init__(self, shared_redis):
        self.redis = shared_redis
    
    def publish_user_update(self, user_id, update_data):
        """Publish user update to other services"""
        message = {
            'user_id': user_id,
            'timestamp': time.time(),
            'data': update_data
        }
        
        # Publish to channel
        self.redis.publish('user_updates', json.dumps(message))
        
        # Cache for services that missed the event
        key = f"user_updates:{user_id}"
        self.redis.lpush(key, json.dumps(message))
        self.redis.ltrim(key, 0, 9)  # Keep last 10 updates
        self.redis.expire(key, 3600)
    
    def subscribe_to_updates(self, channels):
        """Subscribe to cross-service updates"""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channels)
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                yield json.loads(message['data'])

# Circuit Breaker Pattern with Redis
class RedisCircuitBreaker:
    def __init__(self, redis_client, service_name, failure_threshold=5, timeout=60):
        self.redis = redis_client
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_key = f"circuit_breaker:{service_name}:failures"
        self.state_key = f"circuit_breaker:{service_name}:state"
    
    def call_service(self, service_func, *args, **kwargs):
        """Call service with circuit breaker protection"""
        state = self.get_state()
        
        if state == 'OPEN':
            raise Exception(f"Circuit breaker OPEN for {self.service_name}")
        
        try:
            result = service_func(*args, **kwargs)
            self.record_success()
            return result
        except Exception as e:
            self.record_failure()
            raise e
    
    def record_failure(self):
        """Record service failure"""
        failures = self.redis.incr(self.failure_key)
        self.redis.expire(self.failure_key, self.timeout)
        
        if failures >= self.failure_threshold:
            self.redis.set(self.state_key, 'OPEN', ex=self.timeout)
    
    def record_success(self):
        """Record service success"""
        self.redis.delete(self.failure_key)
        self.redis.set(self.state_key, 'CLOSED')
    
    def get_state(self):
        """Get circuit breaker state"""
        state = self.redis.get(self.state_key)
        return state.decode() if state else 'CLOSED'
```

---

## 🎯 **Summary**

This comprehensive guide covers Redis's essential concepts for data engineering interviews. Key areas include:

- **In-memory data structures** for high-performance applications
- **Caching strategies** and distributed cache patterns
- **Real-time analytics** with counters, sets, and streams
- **Persistence mechanisms** for durability
- **Clustering and sharding** for horizontal scaling
- **Security and monitoring** for production environments
- **Integration patterns** with data pipelines and microservices

**Interview Preparation Tips:**
1. **Master data structures** - Know when to use each type
2. **Understand persistence trade-offs** - RDB vs AOF scenarios
3. **Practice clustering concepts** - Sharding and high availability
4. **Know performance optimization** - Memory management and monitoring
5. **Study integration patterns** - How Redis fits in modern architectures