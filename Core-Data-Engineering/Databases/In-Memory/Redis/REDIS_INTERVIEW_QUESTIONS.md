# 🔴 Redis Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts (1-20)](#core-concepts-1-20)
2. [Data Structures (21-40)](#data-structures-21-40)
3. [Performance & Optimization (41-60)](#performance--optimization-41-60)
4. [Persistence & Durability (61-80)](#persistence--durability-61-80)
5. [Scaling & Operations (81-100)](#scaling--operations-81-100)

---

## 🎯 **Introduction**

Redis is an in-memory data structure store used as a database, cache, and message broker. It supports various data structures and provides high performance for real-time applications.

**Why Redis is Critical for Data Engineers:**
- **High Performance**: Sub-millisecond latency for operations
- **Rich Data Types**: Strings, hashes, lists, sets, sorted sets
- **Caching**: Reduce database load and improve response times
- **Session Storage**: Scalable session management
- **Real-time Analytics**: Fast data processing and aggregation

---

## Core Concepts (1-20)

### 1. What is Redis and what are its primary use cases?
**Answer**: Redis (Remote Dictionary Server) is an in-memory data structure store with multiple use cases.

**Primary Use Cases:**
- **Caching**: Application-level and database query caching
- **Session Storage**: Web application session management
- **Real-time Analytics**: Counters, leaderboards, analytics
- **Message Queuing**: Pub/Sub and task queues
- **Rate Limiting**: API rate limiting and throttling

```bash
# Basic Redis operations
redis-cli
127.0.0.1:6379> SET user:1000 "John Doe"
OK
127.0.0.1:6379> GET user:1000
"John Doe"
127.0.0.1:6379> EXPIRE user:1000 3600
(integer) 1
```

### 2. What are Redis data types and when do you use each?
**Answer**: Redis supports multiple data structures optimized for different use cases.

**Data Types:**
```bash
# String - Simple key-value pairs
SET counter 100
INCR counter
GET counter  # Returns 101

# Hash - Field-value pairs within a key
HSET user:1000 name "John" email "john@example.com" age 30
HGET user:1000 name
HGETALL user:1000

# List - Ordered collection of strings
LPUSH tasks "task1" "task2" "task3"
RPOP tasks
LRANGE tasks 0 -1

# Set - Unordered collection of unique strings
SADD tags "redis" "database" "cache"
SMEMBERS tags
SISMEMBER tags "redis"

# Sorted Set - Ordered set with scores
ZADD leaderboard 100 "player1" 200 "player2" 150 "player3"
ZRANGE leaderboard 0 -1 WITHSCORES
ZREVRANGE leaderboard 0 2 WITHSCORES
```

### 3. How does Redis achieve high performance?
**Answer**: Redis performance comes from its architecture and design choices.

**Performance Factors:**
- **In-Memory Storage**: All data stored in RAM
- **Single-Threaded**: No context switching overhead
- **Optimized Data Structures**: Efficient implementations
- **Pipelining**: Batch multiple commands
- **Non-blocking I/O**: Asynchronous operations

```python
# Python Redis pipelining example
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Without pipelining (multiple round trips)
r.set('key1', 'value1')
r.set('key2', 'value2')
r.set('key3', 'value3')

# With pipelining (single round trip)
pipe = r.pipeline()
pipe.set('key1', 'value1')
pipe.set('key2', 'value2')
pipe.set('key3', 'value3')
pipe.execute()
```

### 4. What is Redis persistence and what are the options?
**Answer**: Redis provides persistence options to survive restarts and failures.

**Persistence Options:**
- **RDB (Redis Database)**: Point-in-time snapshots
- **AOF (Append Only File)**: Log of write operations
- **Mixed**: Combination of RDB and AOF

```bash
# RDB configuration
save 900 1      # Save if at least 1 key changed in 900 seconds
save 300 10     # Save if at least 10 keys changed in 300 seconds
save 60 10000   # Save if at least 10000 keys changed in 60 seconds

# AOF configuration
appendonly yes
appendfsync everysec  # fsync every second
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

### 5. How do you implement caching strategies with Redis?
**Answer**: Different caching patterns for various scenarios.

**Caching Patterns:**
```python
import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)

# Cache-Aside Pattern
def get_user(user_id):
    # Try cache first
    cached_user = r.get(f"user:{user_id}")
    if cached_user:
        return json.loads(cached_user)
    
    # Cache miss - fetch from database
    user = fetch_user_from_db(user_id)
    
    # Store in cache with TTL
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user

# Write-Through Pattern
def update_user(user_id, user_data):
    # Update database
    update_user_in_db(user_id, user_data)
    
    # Update cache
    r.setex(f"user:{user_id}", 3600, json.dumps(user_data))

# Write-Behind Pattern
def update_user_async(user_id, user_data):
    # Update cache immediately
    r.setex(f"user:{user_id}", 3600, json.dumps(user_data))
    
    # Queue database update
    r.lpush("db_updates", json.dumps({
        'type': 'user_update',
        'user_id': user_id,
        'data': user_data
    }))
```

## Data Structures (21-40)

### 21. How do you implement a leaderboard using Redis sorted sets?
**Answer**: Sorted sets are perfect for leaderboards with automatic ranking.

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class Leaderboard:
    def __init__(self, name):
        self.key = f"leaderboard:{name}"
    
    def add_score(self, player, score):
        """Add or update player score"""
        r.zadd(self.key, {player: score})
    
    def get_top_players(self, count=10):
        """Get top N players"""
        return r.zrevrange(self.key, 0, count-1, withscores=True)
    
    def get_player_rank(self, player):
        """Get player's rank (0-based)"""
        rank = r.zrevrank(self.key, player)
        return rank + 1 if rank is not None else None
    
    def get_player_score(self, player):
        """Get player's score"""
        return r.zscore(self.key, player)
    
    def get_players_around(self, player, count=5):
        """Get players around a specific player"""
        rank = r.zrevrank(self.key, player)
        if rank is None:
            return []
        
        start = max(0, rank - count//2)
        end = rank + count//2
        return r.zrevrange(self.key, start, end, withscores=True)

# Usage
leaderboard = Leaderboard("game_scores")
leaderboard.add_score("player1", 1500)
leaderboard.add_score("player2", 2000)
leaderboard.add_score("player3", 1800)

top_players = leaderboard.get_top_players(3)
print(f"Top players: {top_players}")
```

### 22. How do you implement rate limiting with Redis?
**Answer**: Use Redis for efficient rate limiting algorithms.

```python
import redis
import time
from datetime import datetime, timedelta

r = redis.Redis(host='localhost', port=6379, db=0)

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def is_allowed(self, identifier):
        """Fixed window rate limiting"""
        key = f"rate_limit:{identifier}"
        current_window = int(time.time() // self.window_seconds)
        window_key = f"{key}:{current_window}"
        
        current_requests = r.incr(window_key)
        if current_requests == 1:
            r.expire(window_key, self.window_seconds)
        
        return current_requests <= self.max_requests
    
    def sliding_window_log(self, identifier):
        """Sliding window log rate limiting"""
        key = f"sliding_log:{identifier}"
        now = time.time()
        cutoff = now - self.window_seconds
        
        # Remove old entries
        r.zremrangebyscore(key, 0, cutoff)
        
        # Count current requests
        current_requests = r.zcard(key)
        
        if current_requests < self.max_requests:
            # Add current request
            r.zadd(key, {str(now): now})
            r.expire(key, self.window_seconds)
            return True
        
        return False
    
    def token_bucket(self, identifier):
        """Token bucket rate limiting"""
        key = f"token_bucket:{identifier}"
        
        # Get current state
        bucket_data = r.hmget(key, 'tokens', 'last_refill')
        tokens = float(bucket_data[0] or self.max_requests)
        last_refill = float(bucket_data[1] or time.time())
        
        # Refill tokens
        now = time.time()
        time_passed = now - last_refill
        tokens = min(self.max_requests, 
                    tokens + time_passed * (self.max_requests / self.window_seconds))
        
        if tokens >= 1:
            tokens -= 1
            r.hmset(key, {
                'tokens': tokens,
                'last_refill': now
            })
            r.expire(key, self.window_seconds * 2)
            return True
        
        return False

# Usage
limiter = RateLimiter(max_requests=100, window_seconds=3600)  # 100 requests per hour

if limiter.is_allowed("user:123"):
    print("Request allowed")
else:
    print("Rate limit exceeded")
```

### 23. How do you implement session management with Redis?
**Answer**: Redis provides scalable session storage for web applications.

```python
import redis
import json
import uuid
from datetime import datetime, timedelta

r = redis.Redis(host='localhost', port=6379, db=0)

class SessionManager:
    def __init__(self, session_timeout=3600):
        self.session_timeout = session_timeout
    
    def create_session(self, user_id, user_data=None):
        """Create new session"""
        session_id = str(uuid.uuid4())
        session_data = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'data': user_data or {}
        }
        
        session_key = f"session:{session_id}"
        r.setex(session_key, self.session_timeout, json.dumps(session_data))
        
        # Track user sessions
        user_sessions_key = f"user_sessions:{user_id}"
        r.sadd(user_sessions_key, session_id)
        r.expire(user_sessions_key, self.session_timeout)
        
        return session_id
    
    def get_session(self, session_id):
        """Get session data"""
        session_key = f"session:{session_id}"
        session_data = r.get(session_key)
        
        if session_data:
            data = json.loads(session_data)
            # Update last accessed time
            data['last_accessed'] = datetime.now().isoformat()
            r.setex(session_key, self.session_timeout, json.dumps(data))
            return data
        
        return None
    
    def update_session(self, session_id, data):
        """Update session data"""
        session_key = f"session:{session_id}"
        session_data = r.get(session_key)
        
        if session_data:
            current_data = json.loads(session_data)
            current_data['data'].update(data)
            current_data['last_accessed'] = datetime.now().isoformat()
            r.setex(session_key, self.session_timeout, json.dumps(current_data))
            return True
        
        return False
    
    def delete_session(self, session_id):
        """Delete session"""
        session_key = f"session:{session_id}"
        session_data = r.get(session_key)
        
        if session_data:
            data = json.loads(session_data)
            user_id = data['user_id']
            
            # Remove from user sessions
            user_sessions_key = f"user_sessions:{user_id}"
            r.srem(user_sessions_key, session_id)
            
            # Delete session
            r.delete(session_key)
            return True
        
        return False
    
    def get_user_sessions(self, user_id):
        """Get all sessions for a user"""
        user_sessions_key = f"user_sessions:{user_id}"
        session_ids = r.smembers(user_sessions_key)
        
        sessions = []
        for session_id in session_ids:
            session_data = self.get_session(session_id.decode())
            if session_data:
                sessions.append({
                    'session_id': session_id.decode(),
                    'data': session_data
                })
        
        return sessions

# Usage
session_manager = SessionManager(session_timeout=3600)

# Create session
session_id = session_manager.create_session("user123", {"role": "admin"})

# Get session
session_data = session_manager.get_session(session_id)
print(f"Session data: {session_data}")

# Update session
session_manager.update_session(session_id, {"last_page": "/dashboard"})
```

## Performance & Optimization (41-60)

### 41. How do you optimize Redis memory usage?
**Answer**: Multiple strategies to reduce Redis memory footprint.

```bash
# Memory optimization techniques

# 1. Use appropriate data structures
# Hash for objects with many fields
HSET user:1000 name "John" email "john@example.com" age 30

# 2. Set expiration times
SETEX cache_key 3600 "cached_value"

# 3. Use memory-efficient encodings
# Configure hash-max-ziplist-entries and hash-max-ziplist-value
hash-max-ziplist-entries 512
hash-max-ziplist-value 64

# 4. Monitor memory usage
INFO memory
MEMORY USAGE key_name

# 5. Use Redis memory optimization commands
MEMORY PURGE  # Free memory from expired keys
MEMORY STATS  # Detailed memory statistics
```

```python
# Memory-efficient data structures
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class MemoryOptimizedCache:
    def __init__(self):
        self.r = r
    
    def store_user_efficiently(self, user_id, user_data):
        """Store user data in memory-efficient hash"""
        key = f"u:{user_id}"  # Shorter key names
        
        # Use hash for structured data
        self.r.hmset(key, {
            'n': user_data['name'],      # Shorter field names
            'e': user_data['email'],
            'a': user_data['age'],
            'c': user_data['created_at']
        })
        
        # Set expiration
        self.r.expire(key, 3600)
    
    def compress_large_values(self, key, value):
        """Compress large values before storing"""
        import gzip
        import json
        
        if len(value) > 1024:  # Compress if larger than 1KB
            compressed = gzip.compress(json.dumps(value).encode())
            self.r.set(f"c:{key}", compressed)  # 'c:' prefix for compressed
        else:
            self.r.set(key, json.dumps(value))
    
    def get_compressed_value(self, key):
        """Retrieve and decompress value"""
        import gzip
        import json
        
        # Try compressed version first
        compressed_key = f"c:{key}"
        compressed_value = self.r.get(compressed_key)
        
        if compressed_value:
            return json.loads(gzip.decompress(compressed_value).decode())
        
        # Try regular version
        regular_value = self.r.get(key)
        if regular_value:
            return json.loads(regular_value)
        
        return None
```

### 42. How do you implement Redis clustering for high availability?
**Answer**: Redis clustering provides automatic sharding and high availability.

```bash
# Redis Cluster setup
# Create cluster with 6 nodes (3 masters, 3 slaves)

# Start Redis instances
redis-server --port 7000 --cluster-enabled yes --cluster-config-file nodes-7000.conf --cluster-node-timeout 5000 --appendonly yes
redis-server --port 7001 --cluster-enabled yes --cluster-config-file nodes-7001.conf --cluster-node-timeout 5000 --appendonly yes
redis-server --port 7002 --cluster-enabled yes --cluster-config-file nodes-7002.conf --cluster-node-timeout 5000 --appendonly yes
redis-server --port 7003 --cluster-enabled yes --cluster-config-file nodes-7003.conf --cluster-node-timeout 5000 --appendonly yes
redis-server --port 7004 --cluster-enabled yes --cluster-config-file nodes-7004.conf --cluster-node-timeout 5000 --appendonly yes
redis-server --port 7005 --cluster-enabled yes --cluster-config-file nodes-7005.conf --cluster-node-timeout 5000 --appendonly yes

# Create cluster
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 --cluster-replicas 1

# Check cluster status
redis-cli -c -p 7000 cluster nodes
redis-cli -c -p 7000 cluster info
```

```python
# Python Redis Cluster client
from rediscluster import RedisCluster

startup_nodes = [
    {"host": "127.0.0.1", "port": "7000"},
    {"host": "127.0.0.1", "port": "7001"},
    {"host": "127.0.0.1", "port": "7002"}
]

rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

class ClusteredCache:
    def __init__(self):
        self.rc = rc
    
    def set_with_hash_tag(self, key, value):
        """Use hash tags to ensure related keys go to same slot"""
        # Keys with same hash tag go to same node
        user_id = "123"
        self.rc.set(f"user:{{{user_id}}}:profile", value)
        self.rc.set(f"user:{{{user_id}}}:preferences", value)
        self.rc.set(f"user:{{{user_id}}}:sessions", value)
    
    def multi_key_operation(self, user_id):
        """Perform multi-key operations on same node"""
        # All keys with same hash tag are on same node
        pipe = self.rc.pipeline()
        pipe.get(f"user:{{{user_id}}}:profile")
        pipe.get(f"user:{{{user_id}}}:preferences")
        pipe.get(f"user:{{{user_id}}}:sessions")
        return pipe.execute()
```

### 43. How do you monitor Redis performance?
**Answer**: Comprehensive monitoring covers memory, CPU, network, and application metrics.

```bash
# Redis monitoring commands
INFO all                    # Complete server information
INFO memory                 # Memory usage statistics
INFO stats                  # General statistics
INFO replication           # Replication information
INFO clients               # Client connections

# Real-time monitoring
redis-cli --latency         # Latency monitoring
redis-cli --latency-history # Latency history
redis-cli --stat            # Continuous stats
redis-cli --bigkeys         # Find big keys

# Slow query log
CONFIG SET slowlog-log-slower-than 10000  # Log queries slower than 10ms
SLOWLOG GET 10              # Get last 10 slow queries
SLOWLOG RESET               # Clear slow log
```

```python
# Python monitoring script
import redis
import time
import json

r = redis.Redis(host='localhost', port=6379, db=0)

class RedisMonitor:
    def __init__(self):
        self.r = r
    
    def get_memory_stats(self):
        """Get memory usage statistics"""
        info = self.r.info('memory')
        return {
            'used_memory': info['used_memory'],
            'used_memory_human': info['used_memory_human'],
            'used_memory_peak': info['used_memory_peak'],
            'used_memory_peak_human': info['used_memory_peak_human'],
            'memory_fragmentation_ratio': info['mem_fragmentation_ratio']
        }
    
    def get_performance_stats(self):
        """Get performance statistics"""
        info = self.r.info('stats')
        return {
            'total_commands_processed': info['total_commands_processed'],
            'instantaneous_ops_per_sec': info['instantaneous_ops_per_sec'],
            'total_connections_received': info['total_connections_received'],
            'connected_clients': info['connected_clients'],
            'keyspace_hits': info['keyspace_hits'],
            'keyspace_misses': info['keyspace_misses'],
            'hit_rate': info['keyspace_hits'] / (info['keyspace_hits'] + info['keyspace_misses']) * 100
        }
    
    def get_slow_queries(self, count=10):
        """Get slow queries"""
        return self.r.slowlog_get(count)
    
    def monitor_continuously(self, interval=5):
        """Continuous monitoring"""
        while True:
            stats = {
                'timestamp': time.time(),
                'memory': self.get_memory_stats(),
                'performance': self.get_performance_stats()
            }
            
            print(json.dumps(stats, indent=2))
            time.sleep(interval)

# Usage
monitor = RedisMonitor()
memory_stats = monitor.get_memory_stats()
performance_stats = monitor.get_performance_stats()
```

## Persistence & Durability (61-80)

### 61. How do you configure Redis persistence for different scenarios?
**Answer**: Choose persistence strategy based on durability and performance requirements.

```bash
# RDB (Snapshot) Configuration
# redis.conf
save 900 1      # Save if at least 1 key changed in 900 seconds
save 300 10     # Save if at least 10 keys changed in 300 seconds  
save 60 10000   # Save if at least 10000 keys changed in 60 seconds
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /var/lib/redis

# AOF (Append Only File) Configuration
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec    # Options: always, everysec, no
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes

# Mixed persistence (Redis 4.0+)
aof-use-rdb-preamble yes
```

```python
# Backup and restore operations
import redis
import subprocess
import time

r = redis.Redis(host='localhost', port=6379, db=0)

class RedisBackup:
    def __init__(self):
        self.r = r
    
    def trigger_rdb_save(self):
        """Trigger RDB snapshot"""
        try:
            self.r.bgsave()
            print("Background save started")
            
            # Wait for save to complete
            while self.r.lastsave() == self.r.lastsave():
                time.sleep(1)
            
            print("Background save completed")
        except Exception as e:
            print(f"Error during save: {e}")
    
    def trigger_aof_rewrite(self):
        """Trigger AOF rewrite"""
        try:
            self.r.bgrewriteaof()
            print("AOF rewrite started")
        except Exception as e:
            print(f"Error during AOF rewrite: {e}")
    
    def backup_to_file(self, backup_path):
        """Create backup file"""
        # Trigger save
        self.r.bgsave()
        
        # Copy RDB file
        subprocess.run([
            'cp', '/var/lib/redis/dump.rdb', backup_path
        ])
        
        print(f"Backup created at {backup_path}")
    
    def restore_from_file(self, backup_path):
        """Restore from backup file"""
        # Stop Redis
        subprocess.run(['systemctl', 'stop', 'redis'])
        
        # Copy backup file
        subprocess.run([
            'cp', backup_path, '/var/lib/redis/dump.rdb'
        ])
        
        # Start Redis
        subprocess.run(['systemctl', 'start', 'redis'])
        
        print(f"Restored from {backup_path}")
```

### 62. How do you implement Redis replication?
**Answer**: Redis replication provides data redundancy and read scaling.

```bash
# Master configuration (redis-master.conf)
bind 0.0.0.0
port 6379
requirepass masterpassword
masterauth masterpassword

# Slave configuration (redis-slave.conf)
bind 0.0.0.0
port 6380
slaveof 127.0.0.1 6379
masterauth masterpassword
slave-read-only yes
slave-serve-stale-data yes

# Start master and slave
redis-server redis-master.conf
redis-server redis-slave.conf

# Check replication status
redis-cli -p 6379 INFO replication
redis-cli -p 6380 INFO replication
```

```python
# Python replication monitoring
import redis

class ReplicationMonitor:
    def __init__(self, master_host='localhost', master_port=6379,
                 slave_host='localhost', slave_port=6380):
        self.master = redis.Redis(host=master_host, port=master_port)
        self.slave = redis.Redis(host=slave_host, port=slave_port)
    
    def check_replication_status(self):
        """Check replication health"""
        master_info = self.master.info('replication')
        slave_info = self.slave.info('replication')
        
        return {
            'master': {
                'role': master_info['role'],
                'connected_slaves': master_info['connected_slaves'],
                'master_repl_offset': master_info['master_repl_offset']
            },
            'slave': {
                'role': slave_info['role'],
                'master_host': slave_info.get('master_host'),
                'master_port': slave_info.get('master_port'),
                'master_link_status': slave_info.get('master_link_status'),
                'slave_repl_offset': slave_info.get('slave_repl_offset')
            }
        }
    
    def check_replication_lag(self):
        """Calculate replication lag"""
        master_info = self.master.info('replication')
        slave_info = self.slave.info('replication')
        
        master_offset = master_info['master_repl_offset']
        slave_offset = slave_info.get('slave_repl_offset', 0)
        
        return master_offset - slave_offset
    
    def test_replication(self):
        """Test replication by writing to master and reading from slave"""
        import time
        
        test_key = f"replication_test_{int(time.time())}"
        test_value = "test_value"
        
        # Write to master
        self.master.set(test_key, test_value)
        
        # Wait a moment for replication
        time.sleep(0.1)
        
        # Read from slave
        slave_value = self.slave.get(test_key)
        
        # Cleanup
        self.master.delete(test_key)
        
        return slave_value.decode() == test_value if slave_value else False

# Usage
monitor = ReplicationMonitor()
status = monitor.check_replication_status()
lag = monitor.check_replication_lag()
replication_working = monitor.test_replication()
```

## Scaling & Operations (81-100)

### 81. How do you implement Redis Sentinel for high availability?
**Answer**: Redis Sentinel provides automatic failover and monitoring.

```bash
# Sentinel configuration (sentinel.conf)
port 26379
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel auth-pass mymaster masterpassword
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 10000

# Start Sentinel
redis-sentinel sentinel.conf

# Sentinel commands
redis-cli -p 26379 SENTINEL masters
redis-cli -p 26379 SENTINEL slaves mymaster
redis-cli -p 26379 SENTINEL sentinels mymaster
redis-cli -p 26379 SENTINEL failover mymaster
```

```python
# Python Sentinel client
from redis.sentinel import Sentinel

class RedisSentinelClient:
    def __init__(self, sentinels, service_name='mymaster'):
        self.sentinel = Sentinel(sentinels)
        self.service_name = service_name
    
    def get_master(self):
        """Get master connection"""
        return self.sentinel.master_for(
            self.service_name, 
            socket_timeout=0.1,
            password='masterpassword'
        )
    
    def get_slave(self):
        """Get slave connection for read operations"""
        return self.sentinel.slave_for(
            self.service_name,
            socket_timeout=0.1,
            password='masterpassword'
        )
    
    def write_operation(self, key, value):
        """Write to master"""
        master = self.get_master()
        return master.set(key, value)
    
    def read_operation(self, key):
        """Read from slave"""
        slave = self.get_slave()
        return slave.get(key)
    
    def get_sentinel_info(self):
        """Get Sentinel information"""
        return {
            'masters': self.sentinel.sentinel_masters(),
            'master_info': self.sentinel.sentinel_master(self.service_name)
        }

# Usage
sentinels = [('localhost', 26379), ('localhost', 26380), ('localhost', 26381)]
client = RedisSentinelClient(sentinels)

# Write to master
client.write_operation('key1', 'value1')

# Read from slave
value = client.read_operation('key1')
```

### 82. How do you implement Redis pub/sub for real-time messaging?
**Answer**: Redis pub/sub enables real-time messaging between applications.

```python
import redis
import threading
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)

class RedisPubSub:
    def __init__(self):
        self.r = r
        self.pubsub = self.r.pubsub()
    
    def publish_message(self, channel, message):
        """Publish message to channel"""
        return self.r.publish(channel, json.dumps(message))
    
    def subscribe_to_channel(self, channel, callback):
        """Subscribe to channel with callback"""
        self.pubsub.subscribe(channel)
        
        def listen():
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        callback(channel, data)
                    except json.JSONDecodeError:
                        callback(channel, message['data'])
        
        thread = threading.Thread(target=listen)
        thread.daemon = True
        thread.start()
        return thread
    
    def pattern_subscribe(self, pattern, callback):
        """Subscribe to pattern with callback"""
        self.pubsub.psubscribe(pattern)
        
        def listen():
            for message in self.pubsub.listen():
                if message['type'] == 'pmessage':
                    try:
                        data = json.loads(message['data'])
                        callback(message['channel'], data)
                    except json.JSONDecodeError:
                        callback(message['channel'], message['data'])
        
        thread = threading.Thread(target=listen)
        thread.daemon = True
        thread.start()
        return thread

# Real-time analytics example
class RealTimeAnalytics:
    def __init__(self):
        self.pubsub = RedisPubSub()
        self.setup_subscribers()
    
    def setup_subscribers(self):
        """Setup event subscribers"""
        # Subscribe to user events
        self.pubsub.subscribe_to_channel('user_events', self.handle_user_event)
        
        # Subscribe to all order events
        self.pubsub.pattern_subscribe('order:*', self.handle_order_event)
    
    def handle_user_event(self, channel, data):
        """Handle user events"""
        event_type = data.get('type')
        user_id = data.get('user_id')
        
        if event_type == 'login':
            # Update login counter
            r.incr(f"daily_logins:{time.strftime('%Y-%m-%d')}")
            r.sadd(f"active_users:{time.strftime('%Y-%m-%d')}", user_id)
        
        elif event_type == 'page_view':
            # Update page view counter
            page = data.get('page')
            r.incr(f"page_views:{page}:{time.strftime('%Y-%m-%d')}")
    
    def handle_order_event(self, channel, data):
        """Handle order events"""
        if 'completed' in channel:
            # Update revenue metrics
            amount = data.get('amount', 0)
            r.incrbyfloat(f"daily_revenue:{time.strftime('%Y-%m-%d')}", amount)
            
            # Update product sales
            for item in data.get('items', []):
                product_id = item.get('product_id')
                quantity = item.get('quantity', 1)
                r.incrby(f"product_sales:{product_id}", quantity)
    
    def publish_user_login(self, user_id):
        """Publish user login event"""
        event = {
            'type': 'login',
            'user_id': user_id,
            'timestamp': time.time()
        }
        self.pubsub.publish_message('user_events', event)
    
    def publish_order_completed(self, order_data):
        """Publish order completion event"""
        self.pubsub.publish_message('order:completed', order_data)

# Usage
analytics = RealTimeAnalytics()

# Simulate events
analytics.publish_user_login('user123')
analytics.publish_order_completed({
    'order_id': 'order456',
    'amount': 99.99,
    'items': [{'product_id': 'prod1', 'quantity': 2}]
})
```

---

## 🎯 **Quick Reference Commands**

```bash
# Basic operations
SET key value
GET key
DEL key
EXISTS key
EXPIRE key seconds
TTL key

# Data structures
HSET hash field value
HGET hash field
LPUSH list value
RPOP list
SADD set member
ZADD sortedset score member

# Server operations
INFO
CONFIG GET parameter
CONFIG SET parameter value
FLUSHDB
FLUSHALL
SAVE
BGSAVE

# Monitoring
MONITOR
SLOWLOG GET
CLIENT LIST
MEMORY USAGE key
```

---

**Total Questions: 100** | **Difficulty: Beginner to Expert** | **Coverage: Complete Redis Ecosystem**