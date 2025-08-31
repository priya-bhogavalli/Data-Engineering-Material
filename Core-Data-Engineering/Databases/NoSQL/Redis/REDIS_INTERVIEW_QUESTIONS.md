# ⚡ Redis Interview Questions for Data Engineering

## 📋 Table of Contents
1. [Basic Redis Concepts](#basic-redis-concepts)
2. [Data Structures](#data-structures)
3. [Performance and Memory](#performance-and-memory)
4. [Persistence and Durability](#persistence-and-durability)
5. [Clustering and High Availability](#clustering-and-high-availability)
6. [Data Engineering Use Cases](#data-engineering-use-cases)
7. [Advanced Conceptual Questions](#advanced-conceptual-questions)
8. [Enterprise Architecture Questions](#enterprise-architecture-questions)
9. [Performance & Optimization Questions](#performance--optimization-questions)

---

## Table of Contents

1. [Basic Redis Concepts](#basic-redis-concepts)
2. [Data Structures](#data-structures)
3. [Performance and Memory](#performance-and-memory)
4. [Persistence and Durability](#persistence-and-durability)
5. [Clustering and High Availability](#clustering-and-high-availability)
6. [Data Engineering Use Cases](#data-engineering-use-cases)

---

## Basic Redis Concepts

### Q1: What is Redis and what makes it different from other databases?

**Answer:**
Redis (Remote Dictionary Server) is an in-memory data structure store used as database, cache, and message broker. It's known for extremely fast performance due to in-memory storage.

**Key Characteristics:**
- **In-Memory**: All data stored in RAM for speed
- **Data Structures**: Rich set of data types beyond key-value
- **Single-Threaded**: Uses event loop for concurrency
- **Persistence Options**: RDB snapshots and AOF logging
- **Atomic Operations**: All operations are atomic

**Code Example:**
```bash
# Basic Redis operations
redis-cli

# String operations
SET user:1001:name "John Doe"
GET user:1001:name
# Output: "John Doe"

# Expiration
SETEX session:abc123 3600 "user_data"
TTL session:abc123
# Output: 3599 (seconds remaining)

# Atomic increment
SET counter 0
INCR counter
INCR counter
GET counter
# Output: "2"
```

### Q2: Explain Redis's single-threaded architecture and its implications.

**Answer:**
Redis uses a single-threaded event loop for processing commands, which eliminates the need for locks and ensures atomic operations, but limits CPU utilization to one core.

**Implications:**
- **Pros**: No race conditions, atomic operations, simple architecture
- **Cons**: CPU-bound operations can block, limited to single core
- **Mitigation**: Use Redis Cluster for scaling, avoid expensive operations

**Code Example:**
```python
import redis
import time
import threading

# Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# Atomic operations example
def increment_counter(counter_name, times):
    for i in range(times):
        # This is atomic - no race conditions
        r.incr(counter_name)

# Multiple threads incrementing same counter
threads = []
for i in range(5):
    t = threading.Thread(target=increment_counter, args=('shared_counter', 100))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final counter value: {r.get('shared_counter')}")
# Output: Final counter value: 500 (always consistent)
```

### Q3: What are the different Redis deployment modes?

**Answer:**
Redis supports multiple deployment modes for different scalability and availability requirements.

**Deployment Modes:**
- **Standalone**: Single Redis instance
- **Master-Slave Replication**: Read scaling with replicas
- **Redis Sentinel**: High availability with automatic failover
- **Redis Cluster**: Horizontal scaling with sharding

**Code Example:**
```python
import redis
from redis.sentinel import Sentinel

# Standalone connection
standalone = redis.Redis(host='localhost', port=6379)

# Sentinel configuration for HA
sentinel = Sentinel([('localhost', 26379)])
master = sentinel.master_for('mymaster', socket_timeout=0.1)
slave = sentinel.slave_for('mymaster', socket_timeout=0.1)

# Cluster connection
from rediscluster import RedisCluster
startup_nodes = [
    {"host": "127.0.0.1", "port": "7000"},
    {"host": "127.0.0.1", "port": "7001"},
    {"host": "127.0.0.1", "port": "7002"}
]
cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
```

## Data Structures

### Q4: Explain Redis data structures and provide use cases for each.

**Answer:**
Redis supports multiple data structures, each optimized for specific use cases and operations.

**Data Structures:**
- **Strings**: Simple key-value, counters, caching
- **Lists**: Queues, stacks, activity feeds
- **Sets**: Unique collections, tags, relationships
- **Sorted Sets**: Leaderboards, rankings, time-series
- **Hashes**: Objects, user profiles
- **Streams**: Event sourcing, message queues
- **Bitmaps**: Analytics, user tracking
- **HyperLogLog**: Cardinality estimation

**Code Example:**
```bash
# Strings - Caching and counters
SET cache:user:1001 '{"name":"John","email":"john@example.com"}'
INCR page_views:homepage

# Lists - Message queues
LPUSH task_queue "process_order_123"
RPOP task_queue

# Sets - Tags and relationships
SADD user:1001:tags "developer" "python" "redis"
SINTER user:1001:tags user:1002:tags  # Common interests

# Sorted Sets - Leaderboards
ZADD leaderboard 1500 "player1" 1200 "player2" 1800 "player3"
ZREVRANGE leaderboard 0 2 WITHSCORES  # Top 3 players

# Hashes - User profiles
HSET user:1001 name "John Doe" email "john@example.com" age 30
HGETALL user:1001

# Streams - Event logging
XADD events * action "user_login" user_id 1001 timestamp 1640995200

# Bitmaps - Daily active users
SETBIT daily_active:2023-01-15 1001 1
BITCOUNT daily_active:2023-01-15

# HyperLogLog - Unique visitors
PFADD unique_visitors:2023-01-15 "user1001" "user1002" "user1003"
PFCOUNT unique_visitors:2023-01-15
```

### Q5: How do you implement a distributed lock using Redis?

**Answer:**
Distributed locks prevent multiple processes from accessing shared resources simultaneously. Redis provides atomic operations for implementing locks.

**Implementation Approaches:**
- **Simple Lock**: SET with NX and EX options
- **Redlock Algorithm**: Multiple Redis instances for reliability
- **Lua Scripts**: Atomic lock operations

**Code Example:**
```python
import redis
import time
import uuid

class RedisDistributedLock:
    def __init__(self, redis_client, key, timeout=10):
        self.redis = redis_client
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.identifier = str(uuid.uuid4())
    
    def acquire(self):
        """Acquire lock with timeout"""
        end_time = time.time() + self.timeout
        
        while time.time() < end_time:
            # Try to acquire lock
            if self.redis.set(self.key, self.identifier, nx=True, ex=self.timeout):
                return True
            time.sleep(0.001)  # Small delay
        
        return False
    
    def release(self):
        """Release lock safely using Lua script"""
        lua_script = """
        if redis.call("GET", KEYS[1]) == ARGV[1] then
            return redis.call("DEL", KEYS[1])
        else
            return 0
        end
        """
        return self.redis.eval(lua_script, 1, self.key, self.identifier)

# Usage example
r = redis.Redis()
lock = RedisDistributedLock(r, "critical_section", timeout=30)

if lock.acquire():
    try:
        # Critical section - only one process can execute this
        print("Processing critical operation...")
        time.sleep(5)
        
        # Simulate work
        r.incr("shared_counter")
        
    finally:
        lock.release()
        print("Lock released")
else:
    print("Could not acquire lock")

# Output: Processing critical operation...
# Output: Lock released
```

### Q6: How do you implement a rate limiter using Redis?

**Answer:**
Rate limiting controls the number of requests a client can make within a time window. Redis provides efficient implementations using various algorithms.

**Algorithms:**
- **Fixed Window**: Simple counter per time window
- **Sliding Window**: More accurate using sorted sets
- **Token Bucket**: Allows bursts with gradual refill

**Code Example:**
```python
import redis
import time
from datetime import datetime, timedelta

class RedisRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def fixed_window_limiter(self, key, limit, window_seconds):
        """Fixed window rate limiter"""
        current_window = int(time.time() // window_seconds)
        window_key = f"rate_limit:{key}:{current_window}"
        
        # Lua script for atomic increment and check
        lua_script = """
        local current = redis.call('INCR', KEYS[1])
        if current == 1 then
            redis.call('EXPIRE', KEYS[1], ARGV[2])
        end
        return current
        """
        
        current_count = self.redis.eval(
            lua_script, 1, window_key, limit, window_seconds
        )
        
        return current_count <= limit, current_count
    
    def sliding_window_limiter(self, key, limit, window_seconds):
        """Sliding window rate limiter using sorted sets"""
        now = time.time()
        window_start = now - window_seconds
        
        pipe = self.redis.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(f"rate_limit:{key}", 0, window_start)
        
        # Count current requests
        pipe.zcard(f"rate_limit:{key}")
        
        # Add current request
        pipe.zadd(f"rate_limit:{key}", {str(now): now})
        
        # Set expiration
        pipe.expire(f"rate_limit:{key}", window_seconds + 1)
        
        results = pipe.execute()
        current_count = results[1] + 1  # +1 for current request
        
        return current_count <= limit, current_count
    
    def token_bucket_limiter(self, key, capacity, refill_rate, refill_period):
        """Token bucket rate limiter"""
        now = time.time()
        bucket_key = f"token_bucket:{key}"
        
        lua_script = """
        local bucket = redis.call('HMGET', KEYS[1], 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1]) or ARGV[1]  -- capacity
        local last_refill = tonumber(bucket[2]) or ARGV[4]  -- now
        
        local now = tonumber(ARGV[4])
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local refill_period = tonumber(ARGV[3])
        
        -- Calculate tokens to add
        local time_passed = now - last_refill
        local tokens_to_add = math.floor(time_passed / refill_period) * refill_rate
        tokens = math.min(capacity, tokens + tokens_to_add)
        
        local allowed = 0
        if tokens >= 1 then
            tokens = tokens - 1
            allowed = 1
        end
        
        -- Update bucket
        redis.call('HMSET', KEYS[1], 'tokens', tokens, 'last_refill', now)
        redis.call('EXPIRE', KEYS[1], 3600)
        
        return {allowed, tokens}
        """
        
        result = self.redis.eval(
            lua_script, 1, bucket_key, 
            capacity, refill_rate, refill_period, now
        )
        
        return bool(result[0]), result[1]

# Usage examples
r = redis.Redis()
limiter = RedisRateLimiter(r)

# Fixed window: 10 requests per minute
allowed, count = limiter.fixed_window_limiter("user:1001", 10, 60)
print(f"Fixed window - Allowed: {allowed}, Count: {count}")

# Sliding window: 5 requests per 30 seconds
allowed, count = limiter.sliding_window_limiter("api:endpoint", 5, 30)
print(f"Sliding window - Allowed: {allowed}, Count: {count}")

# Token bucket: 10 capacity, 1 token per second
allowed, tokens = limiter.token_bucket_limiter("service:api", 10, 1, 1)
print(f"Token bucket - Allowed: {allowed}, Tokens: {tokens}")
```

## Performance and Memory

### Q7: How do you optimize Redis memory usage?

**Answer:**
Redis memory optimization involves choosing appropriate data structures, configuring memory policies, and monitoring usage patterns.

**Optimization Strategies:**
- **Data Structure Selection**: Choose most efficient structure
- **Memory Policies**: Configure eviction policies
- **Compression**: Use hash-max-ziplist settings
- **Expiration**: Set TTL for temporary data
- **Memory Analysis**: Use MEMORY commands

**Code Example:**
```bash
# Memory analysis commands
MEMORY USAGE mykey
MEMORY STATS
INFO memory

# Efficient data structures
# Instead of individual keys for user fields:
# SET user:1001:name "John"
# SET user:1001:email "john@example.com"

# Use hash (more memory efficient):
HSET user:1001 name "John" email "john@example.com" age 30

# Configure memory policies in redis.conf
# maxmemory 2gb
# maxmemory-policy allkeys-lru

# Compression settings for small hashes
# hash-max-ziplist-entries 512
# hash-max-ziplist-value 64
```

```python
import redis

def analyze_memory_usage(redis_client):
    """Analyze Redis memory usage"""
    info = redis_client.info('memory')
    
    print("Memory Usage Analysis:")
    print(f"Used Memory: {info['used_memory_human']}")
    print(f"Used Memory RSS: {info['used_memory_rss_human']}")
    print(f"Memory Fragmentation Ratio: {info['mem_fragmentation_ratio']}")
    print(f"Evicted Keys: {info.get('evicted_keys', 0)}")
    
    # Sample key memory usage
    sample_keys = redis_client.randomkey()
    if sample_keys:
        memory_usage = redis_client.memory_usage(sample_keys)
        print(f"Sample key '{sample_keys}' uses {memory_usage} bytes")

# Memory-efficient data modeling
def efficient_user_storage(redis_client, user_id, user_data):
    """Store user data efficiently using hashes"""
    key = f"user:{user_id}"
    
    # Use hash instead of multiple string keys
    redis_client.hset(key, mapping=user_data)
    
    # Set expiration if appropriate
    redis_client.expire(key, 86400)  # 24 hours

# Usage
r = redis.Redis()
analyze_memory_usage(r)

user_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'last_login': '2023-01-15T10:30:00Z'
}
efficient_user_storage(r, 1001, user_data)
```

### Q8: How do you monitor and troubleshoot Redis performance issues?

**Answer:**
Redis performance monitoring involves tracking key metrics, analyzing slow operations, and understanding bottlenecks.

**Key Metrics:**
- **Latency**: Command execution time
- **Throughput**: Operations per second
- **Memory Usage**: RAM consumption and fragmentation
- **Connection Count**: Active client connections
- **Hit Rate**: Cache effectiveness

**Code Example:**
```python
import redis
import time
import statistics

class RedisMonitor:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def measure_latency(self, command_func, iterations=1000):
        """Measure command latency"""
        latencies = []
        
        for _ in range(iterations):
            start = time.perf_counter()
            command_func()
            end = time.perf_counter()
            latencies.append((end - start) * 1000)  # Convert to ms
        
        return {
            'avg_latency': statistics.mean(latencies),
            'p95_latency': statistics.quantiles(latencies, n=20)[18],  # 95th percentile
            'p99_latency': statistics.quantiles(latencies, n=100)[98]  # 99th percentile
        }
    
    def get_performance_stats(self):
        """Get comprehensive performance statistics"""
        info = self.redis.info()
        
        stats = {
            'connected_clients': info['connected_clients'],
            'used_memory_human': info['used_memory_human'],
            'mem_fragmentation_ratio': info['mem_fragmentation_ratio'],
            'total_commands_processed': info['total_commands_processed'],
            'instantaneous_ops_per_sec': info['instantaneous_ops_per_sec'],
            'keyspace_hits': info.get('keyspace_hits', 0),
            'keyspace_misses': info.get('keyspace_misses', 0)
        }
        
        # Calculate hit rate
        hits = stats['keyspace_hits']
        misses = stats['keyspace_misses']
        if hits + misses > 0:
            stats['hit_rate'] = hits / (hits + misses) * 100
        else:
            stats['hit_rate'] = 0
        
        return stats
    
    def monitor_slow_log(self, count=10):
        """Monitor slow operations"""
        slow_log = self.redis.slowlog_get(count)
        
        print("Slow Log Analysis:")
        for entry in slow_log:
            print(f"Duration: {entry['duration']}μs, "
                  f"Command: {' '.join(entry['command'])}")
    
    def continuous_monitoring(self, interval=5, duration=60):
        """Continuous performance monitoring"""
        end_time = time.time() + duration
        
        print("Starting continuous monitoring...")
        while time.time() < end_time:
            stats = self.get_performance_stats()
            
            print(f"\n--- {time.strftime('%H:%M:%S')} ---")
            print(f"OPS/sec: {stats['instantaneous_ops_per_sec']}")
            print(f"Clients: {stats['connected_clients']}")
            print(f"Memory: {stats['used_memory_human']}")
            print(f"Hit Rate: {stats['hit_rate']:.2f}%")
            print(f"Fragmentation: {stats['mem_fragmentation_ratio']:.2f}")
            
            time.sleep(interval)

# Usage example
r = redis.Redis()
monitor = RedisMonitor(r)

# Measure GET operation latency
def test_get():
    r.get('test_key')

latency_stats = monitor.measure_latency(test_get)
print(f"GET Latency - Avg: {latency_stats['avg_latency']:.2f}ms, "
      f"P95: {latency_stats['p95_latency']:.2f}ms")

# Get performance statistics
stats = monitor.get_performance_stats()
print(f"Current OPS: {stats['instantaneous_ops_per_sec']}")
print(f"Hit Rate: {stats['hit_rate']:.2f}%")

# Monitor slow operations
monitor.monitor_slow_log()
```

## Persistence and Durability

### Q9: Explain Redis persistence mechanisms and when to use each.

**Answer:**
Redis offers two persistence mechanisms to ensure data durability: RDB snapshots and AOF (Append Only File) logging.

**Persistence Types:**
- **RDB**: Point-in-time snapshots, compact, fast recovery
- **AOF**: Log of write operations, better durability, larger files
- **Hybrid**: Combination of both for optimal balance

**Code Example:**
```bash
# RDB Configuration (redis.conf)
# Save snapshot if at least 1 key changed in 900 seconds
save 900 1
# Save snapshot if at least 10 keys changed in 300 seconds  
save 300 10
# Save snapshot if at least 10000 keys changed in 60 seconds
save 60 10000

# Manual snapshot
BGSAVE
LASTSAVE

# AOF Configuration
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec  # Options: always, everysec, no

# AOF rewrite (compaction)
BGREWRITEAOF
```

```python
import redis
import time

def backup_strategy_example():
    """Example of implementing backup strategy"""
    r = redis.Redis()
    
    # Check last save time
    last_save = r.lastsave()
    current_time = int(time.time())
    
    # If last save was more than 1 hour ago, trigger backup
    if current_time - last_save > 3600:
        print("Triggering background save...")
        r.bgsave()
        
        # Wait for save to complete
        while r.lastsave() == last_save:
            time.sleep(1)
        
        print("Backup completed")
    
    # Check AOF rewrite status
    info = r.info('persistence')
    if info.get('aof_rewrite_in_progress', 0) == 0:
        aof_size = info.get('aof_current_size', 0)
        aof_base_size = info.get('aof_base_size', 0)
        
        # Trigger rewrite if AOF grew significantly
        if aof_size > aof_base_size * 2:
            print("Triggering AOF rewrite...")
            r.bgrewriteaof()

backup_strategy_example()
```

## Clustering and High Availability

### Q10: How does Redis Cluster work and when should you use it?

**Answer:**
Redis Cluster provides horizontal scaling and high availability through automatic sharding across multiple nodes with built-in failover capabilities.

**Key Features:**
- **Automatic Sharding**: Data distributed across 16384 hash slots
- **High Availability**: Master-slave replication with automatic failover
- **No Single Point of Failure**: Decentralized architecture
- **Linear Scaling**: Add nodes to increase capacity

**Code Example:**
```python
from rediscluster import RedisCluster

# Cluster setup
startup_nodes = [
    {"host": "127.0.0.1", "port": "7000"},
    {"host": "127.0.0.1", "port": "7001"},
    {"host": "127.0.0.1", "port": "7002"},
    {"host": "127.0.0.1", "port": "7003"},
    {"host": "127.0.0.1", "port": "7004"},
    {"host": "127.0.0.1", "port": "7005"}
]

# Connect to cluster
rc = RedisCluster(
    startup_nodes=startup_nodes,
    decode_responses=True,
    skip_full_coverage_check=True
)

# Cluster operations work like regular Redis
rc.set("user:1001", "John Doe")
rc.set("user:1002", "Jane Smith")

# Keys are automatically distributed across nodes
print(f"user:1001 value: {rc.get('user:1001')}")
print(f"user:1002 value: {rc.get('user:1002')}")

# Cluster information
def analyze_cluster(cluster_client):
    """Analyze cluster distribution and health"""
    nodes = cluster_client.cluster_nodes()
    
    print("Cluster Nodes:")
    for node_id, node_info in nodes.items():
        print(f"Node {node_id[:8]}: {node_info['host']}:{node_info['port']} "
              f"- Role: {node_info['flags']}")
    
    # Check cluster slots distribution
    slots = cluster_client.cluster_slots()
    print(f"\nSlot Distribution: {len(slots)} slot ranges")
    
    # Test failover scenario
    try:
        # This will work even if some nodes are down
        cluster_client.set("test:failover", "data")
        print("Cluster is healthy - write operation successful")
    except Exception as e:
        print(f"Cluster issue detected: {e}")

analyze_cluster(rc)
```

## Data Engineering Use Cases

### Q11: How do you implement a real-time leaderboard system using Redis?

**Answer:**
Real-time leaderboards require fast updates and queries for rankings. Redis Sorted Sets provide optimal performance for this use case.

**Code Example:**
```python
import redis
import time
from datetime import datetime, timedelta

class RedisLeaderboard:
    def __init__(self, redis_client, leaderboard_name):
        self.redis = redis_client
        self.key = f"leaderboard:{leaderboard_name}"
        self.daily_key = f"leaderboard:daily:{leaderboard_name}"
    
    def update_score(self, player_id, score):
        """Update player score (increment)"""
        pipe = self.redis.pipeline()
        
        # Update all-time leaderboard
        pipe.zincrby(self.key, score, player_id)
        
        # Update daily leaderboard
        today = datetime.now().strftime("%Y-%m-%d")
        daily_key = f"{self.daily_key}:{today}"
        pipe.zincrby(daily_key, score, player_id)
        pipe.expire(daily_key, 86400 * 7)  # Keep for 7 days
        
        results = pipe.execute()
        return results[0]  # New total score
    
    def get_top_players(self, count=10, with_scores=True):
        """Get top N players"""
        if with_scores:
            return self.redis.zrevrange(self.key, 0, count-1, withscores=True)
        return self.redis.zrevrange(self.key, 0, count-1)
    
    def get_player_rank(self, player_id):
        """Get player's current rank (1-based)"""
        rank = self.redis.zrevrank(self.key, player_id)
        return rank + 1 if rank is not None else None
    
    def get_player_score(self, player_id):
        """Get player's current score"""
        return self.redis.zscore(self.key, player_id)
    
    def get_players_around(self, player_id, range_size=5):
        """Get players around a specific player"""
        rank = self.redis.zrevrank(self.key, player_id)
        if rank is None:
            return []
        
        start = max(0, rank - range_size)
        end = rank + range_size
        
        return self.redis.zrevrange(
            self.key, start, end, withscores=True
        )
    
    def get_daily_leaderboard(self, date=None):
        """Get daily leaderboard for specific date"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        daily_key = f"{self.daily_key}:{date}"
        return self.redis.zrevrange(daily_key, 0, 9, withscores=True)

# Usage example
r = redis.Redis()
leaderboard = RedisLeaderboard(r, "game_scores")

# Simulate game events
players = ["alice", "bob", "charlie", "diana", "eve"]
for i in range(100):
    import random
    player = random.choice(players)
    score = random.randint(10, 100)
    
    new_total = leaderboard.update_score(player, score)
    print(f"{player} scored {score}, total: {new_total}")

# Get leaderboard results
print("\nTop 5 Players:")
top_players = leaderboard.get_top_players(5)
for i, (player, score) in enumerate(top_players, 1):
    print(f"{i}. {player}: {int(score)}")

# Get specific player info
alice_rank = leaderboard.get_player_rank("alice")
alice_score = leaderboard.get_player_score("alice")
print(f"\nAlice - Rank: {alice_rank}, Score: {int(alice_score)}")

# Get players around Alice
around_alice = leaderboard.get_players_around("alice", 2)
print(f"\nPlayers around Alice:")
for player, score in around_alice:
    print(f"{player}: {int(score)}")
```

### Q12: How do you implement session management using Redis?

**Answer:**
Session management requires fast access, automatic expiration, and scalability across multiple application servers. Redis is ideal for this use case.

**Code Example:**
```python
import redis
import json
import uuid
import time
from datetime import datetime, timedelta

class RedisSessionManager:
    def __init__(self, redis_client, session_timeout=3600):
        self.redis = redis_client
        self.timeout = session_timeout
        self.prefix = "session:"
    
    def create_session(self, user_id, user_data=None):
        """Create new session"""
        session_id = str(uuid.uuid4())
        session_key = f"{self.prefix}{session_id}"
        
        session_data = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'data': user_data or {}
        }
        
        # Store session with expiration
        self.redis.setex(
            session_key, 
            self.timeout, 
            json.dumps(session_data)
        )
        
        return session_id
    
    def get_session(self, session_id):
        """Retrieve and refresh session"""
        session_key = f"{self.prefix}{session_id}"
        
        # Get session data
        session_json = self.redis.get(session_key)
        if not session_json:
            return None
        
        session_data = json.loads(session_json)
        
        # Update last accessed time and refresh TTL
        session_data['last_accessed'] = datetime.now().isoformat()
        
        self.redis.setex(
            session_key,
            self.timeout,
            json.dumps(session_data)
        )
        
        return session_data
    
    def update_session(self, session_id, data):
        """Update session data"""
        session_data = self.get_session(session_id)
        if not session_data:
            return False
        
        # Merge new data
        session_data['data'].update(data)
        session_data['last_accessed'] = datetime.now().isoformat()
        
        session_key = f"{self.prefix}{session_id}"
        self.redis.setex(
            session_key,
            self.timeout,
            json.dumps(session_data)
        )
        
        return True
    
    def delete_session(self, session_id):
        """Delete session (logout)"""
        session_key = f"{self.prefix}{session_id}"
        return self.redis.delete(session_key) > 0
    
    def get_user_sessions(self, user_id):
        """Get all sessions for a user"""
        pattern = f"{self.prefix}*"
        sessions = []
        
        for key in self.redis.scan_iter(match=pattern):
            session_data = self.redis.get(key)
            if session_data:
                data = json.loads(session_data)
                if data.get('user_id') == user_id:
                    sessions.append({
                        'session_id': key.decode().replace(self.prefix, ''),
                        'created_at': data['created_at'],
                        'last_accessed': data['last_accessed']
                    })
        
        return sessions
    
    def cleanup_expired_sessions(self):
        """Manual cleanup of expired sessions (Redis handles this automatically)"""
        pattern = f"{self.prefix}*"
        expired_count = 0
        
        for key in self.redis.scan_iter(match=pattern):
            ttl = self.redis.ttl(key)
            if ttl == -2:  # Key doesn't exist (expired)
                expired_count += 1
        
        return expired_count

# Usage example
r = redis.Redis()
session_manager = RedisSessionManager(r, session_timeout=1800)  # 30 minutes

# Create session
user_data = {
    'username': 'john_doe',
    'email': 'john@example.com',
    'preferences': {'theme': 'dark', 'language': 'en'}
}

session_id = session_manager.create_session(
    user_id=1001, 
    user_data=user_data
)
print(f"Created session: {session_id}")

# Retrieve session
session = session_manager.get_session(session_id)
print(f"Retrieved session for user: {session['user_id']}")

# Update session
session_manager.update_session(session_id, {
    'last_page': '/dashboard',
    'cart_items': ['item1', 'item2']
})

# Get updated session
updated_session = session_manager.get_session(session_id)
print(f"Updated session data: {updated_session['data']}")

# List user sessions
user_sessions = session_manager.get_user_sessions(1001)
print(f"User has {len(user_sessions)} active sessions")

# Logout (delete session)
session_manager.delete_session(session_id)
print("Session deleted")
```

### Q13: How do you implement a message queue system using Redis?

**Answer:**
Redis can implement various message queue patterns using Lists, Streams, or Pub/Sub depending on requirements for persistence, acknowledgment, and delivery guarantees.

**Code Example:**
```python
import redis
import json
import time
import threading
from datetime import datetime

class RedisMessageQueue:
    def __init__(self, redis_client, queue_name):
        self.redis = redis_client
        self.queue_name = queue_name
        self.queue_key = f"queue:{queue_name}"
        self.processing_key = f"processing:{queue_name}"
        self.failed_key = f"failed:{queue_name}"
    
    def enqueue(self, message, priority=0):
        """Add message to queue"""
        message_data = {
            'id': f"{int(time.time() * 1000)}_{priority}",
            'payload': message,
            'enqueued_at': datetime.now().isoformat(),
            'attempts': 0,
            'priority': priority
        }
        
        # Use sorted set for priority queue
        self.redis.zadd(
            self.queue_key, 
            {json.dumps(message_data): priority}
        )
        
        return message_data['id']
    
    def dequeue(self, timeout=10):
        """Get message from queue with timeout"""
        # Atomic pop from sorted set (highest priority first)
        result = self.redis.bzpopmax(self.queue_key, timeout=timeout)
        
        if result:
            queue_name, message_json, priority = result
            message_data = json.loads(message_json)
            
            # Move to processing queue
            processing_key = f"{self.processing_key}:{message_data['id']}"
            self.redis.setex(processing_key, 300, message_json)  # 5 min timeout
            
            return message_data
        
        return None
    
    def acknowledge(self, message_id):
        """Acknowledge message processing completion"""
        processing_key = f"{self.processing_key}:{message_id}"
        return self.redis.delete(processing_key) > 0
    
    def reject(self, message_id, reason=None):
        """Reject message and move to failed queue"""
        processing_key = f"{self.processing_key}:{message_id}"
        message_json = self.redis.get(processing_key)
        
        if message_json:
            message_data = json.loads(message_json)
            message_data['failed_at'] = datetime.now().isoformat()
            message_data['failure_reason'] = reason
            
            # Move to failed queue
            self.redis.lpush(self.failed_key, json.dumps(message_data))
            self.redis.delete(processing_key)
            
            return True
        
        return False
    
    def retry_failed_messages(self, max_attempts=3):
        """Retry failed messages"""
        retried = 0
        
        while True:
            message_json = self.redis.rpop(self.failed_key)
            if not message_json:
                break
            
            message_data = json.loads(message_json)
            message_data['attempts'] += 1
            
            if message_data['attempts'] <= max_attempts:
                # Re-enqueue with lower priority
                self.redis.zadd(
                    self.queue_key,
                    {json.dumps(message_data): message_data['priority'] - 1}
                )
                retried += 1
            else:
                # Move to dead letter queue
                dead_letter_key = f"dead_letter:{self.queue_name}"
                self.redis.lpush(dead_letter_key, message_json)
        
        return retried
    
    def get_queue_stats(self):
        """Get queue statistics"""
        return {
            'pending': self.redis.zcard(self.queue_key),
            'processing': len(list(self.redis.scan_iter(
                match=f"{self.processing_key}:*"
            ))),
            'failed': self.redis.llen(self.failed_key),
            'dead_letter': self.redis.llen(f"dead_letter:{self.queue_name}")
        }

# Worker implementation
class QueueWorker:
    def __init__(self, queue, worker_id):
        self.queue = queue
        self.worker_id = worker_id
        self.running = False
    
    def process_message(self, message):
        """Process individual message"""
        print(f"Worker {self.worker_id} processing: {message['payload']}")
        
        # Simulate processing
        time.sleep(1)
        
        # Simulate occasional failures
        import random
        if random.random() < 0.1:  # 10% failure rate
            raise Exception("Processing failed")
        
        return True
    
    def start(self):
        """Start worker loop"""
        self.running = True
        print(f"Worker {self.worker_id} started")
        
        while self.running:
            try:
                message = self.queue.dequeue(timeout=5)
                if message:
                    try:
                        self.process_message(message)
                        self.queue.acknowledge(message['id'])
                        print(f"Message {message['id']} completed")
                    
                    except Exception as e:
                        self.queue.reject(message['id'], str(e))
                        print(f"Message {message['id']} failed: {e}")
                
            except KeyboardInterrupt:
                self.running = False
                break
        
        print(f"Worker {self.worker_id} stopped")

# Usage example
r = redis.Redis()
queue = RedisMessageQueue(r, "task_queue")

# Producer: Add messages to queue
messages = [
    {"task": "send_email", "recipient": "user@example.com"},
    {"task": "process_payment", "amount": 99.99},
    {"task": "generate_report", "report_id": "RPT001"}
]

for i, msg in enumerate(messages):
    priority = 10 - i  # Higher number = higher priority
    msg_id = queue.enqueue(msg, priority=priority)
    print(f"Enqueued message {msg_id} with priority {priority}")

# Consumer: Process messages
def run_worker(worker_id):
    worker = QueueWorker(queue, worker_id)
    worker.start()

# Start multiple workers
workers = []
for i in range(3):
    worker_thread = threading.Thread(target=run_worker, args=[f"worker-{i}"])
    worker_thread.daemon = True
    worker_thread.start()
    workers.append(worker_thread)

# Monitor queue
time.sleep(2)
stats = queue.get_queue_stats()
print(f"Queue stats: {stats}")

# Retry failed messages
retried = queue.retry_failed_messages()
print(f"Retried {retried} failed messages")
```

---

---

## 🎯 **Advanced Conceptual Questions**

### Q14: Explain Redis's memory management and eviction policies
**Answer:**
Redis manages memory through configurable eviction policies when maxmemory limit is reached.

**Eviction Policies:**
- **noeviction**: Return errors when memory limit reached
- **allkeys-lru**: Remove least recently used keys
- **allkeys-lfu**: Remove least frequently used keys
- **volatile-lru**: Remove LRU keys with expire set
- **volatile-lfu**: Remove LFU keys with expire set
- **allkeys-random**: Remove random keys
- **volatile-random**: Remove random keys with expire set
- **volatile-ttl**: Remove keys with shortest TTL

**Code Example:**
```bash
# Configure memory limit and policy
CONFIG SET maxmemory 100mb
CONFIG SET maxmemory-policy allkeys-lru

# Monitor memory usage
INFO memory
MEMORY USAGE mykey
```

```python
import redis

def memory_management_demo():
    r = redis.Redis()
    
    # Set memory limit (100MB)
    r.config_set('maxmemory', '100mb')
    r.config_set('maxmemory-policy', 'allkeys-lru')
    
    # Monitor memory usage
    info = r.info('memory')
    print(f"Used memory: {info['used_memory_human']}")
    print(f"Max memory: {info.get('maxmemory_human', 'unlimited')}")
    
    # Test eviction behavior
    for i in range(1000):
        # Create keys with different access patterns
        r.set(f"frequent:{i}", f"data_{i}")
        if i % 10 == 0:
            # Access some keys more frequently
            r.get(f"frequent:{i}")
    
    # Check which keys survived eviction
    surviving_keys = r.keys("frequent:*")
    print(f"Surviving keys: {len(surviving_keys)}")

memory_management_demo()
```

### Q15: How does Redis handle concurrent access and thread safety?
**Answer:**
Redis uses single-threaded execution for commands, ensuring atomic operations without explicit locking.

**Concurrency Model:**
- **Single-threaded command processing**: No race conditions
- **Event-driven I/O**: Handle multiple clients efficiently
- **Atomic operations**: All Redis commands are atomic
- **Transactions**: MULTI/EXEC for atomic command sequences
- **Lua scripts**: Atomic execution of complex operations

**Code Example:**
```python
import redis
import threading
import time

def demonstrate_atomicity():
    r = redis.Redis()
    r.set('counter', 0)
    
    def increment_counter(thread_id, iterations):
        for i in range(iterations):
            # This is atomic - no race conditions possible
            current = r.incr('counter')
            print(f"Thread {thread_id}: {current}")
    
    # Start multiple threads
    threads = []
    for i in range(5):
        t = threading.Thread(
            target=increment_counter, 
            args=(i, 10)
        )
        threads.append(t)
        t.start()
    
    # Wait for completion
    for t in threads:
        t.join()
    
    final_value = r.get('counter')
    print(f"Final counter value: {final_value}")  # Always 50

# Transaction example
def atomic_transfer(r, from_account, to_account, amount):
    """Atomic money transfer using transactions"""
    with r.pipeline() as pipe:
        while True:
            try:
                # Watch accounts for changes
                pipe.watch(from_account, to_account)
                
                # Check balances
                from_balance = float(pipe.get(from_account) or 0)
                to_balance = float(pipe.get(to_account) or 0)
                
                if from_balance < amount:
                    raise ValueError("Insufficient funds")
                
                # Start transaction
                pipe.multi()
                pipe.set(from_account, from_balance - amount)
                pipe.set(to_account, to_balance + amount)
                
                # Execute atomically
                pipe.execute()
                break
                
            except redis.WatchError:
                # Retry if accounts were modified
                continue

demonstrate_atomicity()
```

### Q16: What are Redis Modules and how do they extend functionality?
**Answer:**
Redis Modules allow extending Redis with custom data types, commands, and functionality using C API.

**Popular Modules:**
- **RedisJSON**: JSON data type support
- **RedisSearch**: Full-text search capabilities
- **RedisGraph**: Graph database functionality
- **RedisTimeSeries**: Time-series data handling
- **RedisBloom**: Probabilistic data structures

**Code Example:**
```python
import redis
import json

# RedisJSON module example
def redis_json_demo():
    # Requires RedisJSON module loaded
    r = redis.Redis(decode_responses=True)
    
    # Store JSON document
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "preferences": {
            "theme": "dark",
            "notifications": True
        },
        "scores": [85, 92, 78]
    }
    
    # JSON.SET command
    r.execute_command('JSON.SET', 'user:1001', '.', json.dumps(user_data))
    
    # JSON.GET command
    result = r.execute_command('JSON.GET', 'user:1001')
    print(f"User data: {result}")
    
    # Update nested field
    r.execute_command('JSON.SET', 'user:1001', '.preferences.theme', '"light"')
    
    # Get specific field
    theme = r.execute_command('JSON.GET', 'user:1001', '.preferences.theme')
    print(f"Theme: {theme}")
    
    # Array operations
    r.execute_command('JSON.ARRAPPEND', 'user:1001', '.scores', '95')
    scores = r.execute_command('JSON.GET', 'user:1001', '.scores')
    print(f"Updated scores: {scores}")

# RedisSearch module example
def redis_search_demo():
    r = redis.Redis(decode_responses=True)
    
    # Create search index
    try:
        r.execute_command(
            'FT.CREATE', 'products_idx',
            'ON', 'HASH',
            'PREFIX', '1', 'product:',
            'SCHEMA',
            'name', 'TEXT', 'WEIGHT', '5.0',
            'description', 'TEXT',
            'price', 'NUMERIC', 'SORTABLE',
            'category', 'TAG', 'SORTABLE'
        )
    except:
        pass  # Index might already exist
    
    # Add products
    products = [
        {
            'name': 'iPhone 13',
            'description': 'Latest Apple smartphone with advanced features',
            'price': 999,
            'category': 'electronics'
        },
        {
            'name': 'MacBook Pro',
            'description': 'Professional laptop for developers',
            'price': 2499,
            'category': 'electronics'
        }
    ]
    
    for i, product in enumerate(products, 1):
        r.hset(f'product:{i}', mapping=product)
    
    # Search products
    results = r.execute_command(
        'FT.SEARCH', 'products_idx',
        'Apple',
        'LIMIT', '0', '10'
    )
    print(f"Search results: {results}")

# redis_json_demo()  # Requires RedisJSON module
# redis_search_demo()  # Requires RedisSearch module
```

---

## 🏢 **Enterprise Architecture Questions**

### Q17: How do you design Redis for microservices architecture?
**Answer:**
Design Redis deployment strategy considering service isolation, data consistency, and scaling requirements.

**Architecture Patterns:**
- **Shared Redis**: Single cluster for multiple services
- **Service-specific Redis**: Dedicated instances per service
- **Hybrid Approach**: Mix based on requirements
- **Cache-aside Pattern**: Application manages cache
- **Write-through/Write-behind**: Automatic cache updates

**Code Example:**
```python
import redis
import json
from abc import ABC, abstractmethod

class CacheStrategy(ABC):
    @abstractmethod
    def get(self, key):
        pass
    
    @abstractmethod
    def set(self, key, value, ttl=None):
        pass

class CacheAsideStrategy(CacheStrategy):
    def __init__(self, redis_client, data_source):
        self.redis = redis_client
        self.data_source = data_source
    
    def get(self, key):
        # Try cache first
        cached_value = self.redis.get(key)
        if cached_value:
            return json.loads(cached_value)
        
        # Fetch from data source
        value = self.data_source.get(key)
        if value:
            # Store in cache
            self.redis.setex(key, 3600, json.dumps(value))
        
        return value
    
    def set(self, key, value, ttl=3600):
        # Update data source
        self.data_source.set(key, value)
        
        # Update cache
        self.redis.setex(key, ttl, json.dumps(value))

class WriteThroughStrategy(CacheStrategy):
    def __init__(self, redis_client, data_source):
        self.redis = redis_client
        self.data_source = data_source
    
    def get(self, key):
        # Always try cache first
        cached_value = self.redis.get(key)
        if cached_value:
            return json.loads(cached_value)
        
        # If not in cache, fetch from source and cache it
        value = self.data_source.get(key)
        if value:
            self.redis.setex(key, 3600, json.dumps(value))
        
        return value
    
    def set(self, key, value, ttl=3600):
        # Write to both cache and data source atomically
        try:
            self.data_source.set(key, value)
            self.redis.setex(key, ttl, json.dumps(value))
        except Exception as e:
            # Rollback if needed
            self.redis.delete(key)
            raise e

# Service-specific Redis configuration
class MicroserviceRedisConfig:
    def __init__(self, service_name, redis_config):
        self.service_name = service_name
        self.redis_config = redis_config
        self.redis_client = self._create_client()
    
    def _create_client(self):
        return redis.Redis(
            host=self.redis_config['host'],
            port=self.redis_config['port'],
            db=self.redis_config.get('db', 0),
            password=self.redis_config.get('password'),
            decode_responses=True
        )
    
    def get_cache_key(self, key):
        return f"{self.service_name}:{key}"
    
    def get(self, key):
        return self.redis_client.get(self.get_cache_key(key))
    
    def set(self, key, value, ttl=3600):
        return self.redis_client.setex(
            self.get_cache_key(key), ttl, value
        )

# Usage in microservices
user_service_redis = MicroserviceRedisConfig(
    'user_service',
    {'host': 'redis-user.internal', 'port': 6379, 'db': 0}
)

order_service_redis = MicroserviceRedisConfig(
    'order_service', 
    {'host': 'redis-order.internal', 'port': 6379, 'db': 0}
)

# Each service uses its own namespace
user_service_redis.set('profile:1001', '{"name": "John"}')
order_service_redis.set('order:1001', '{"total": 99.99}')
```

### Q18: How do you implement Redis security best practices?
**Answer:**
Implement comprehensive security through authentication, authorization, encryption, and network isolation.

**Security Measures:**
- **Authentication**: Password protection and ACLs
- **Authorization**: User-based access control
- **Encryption**: TLS for data in transit
- **Network Security**: VPC, firewalls, private networks
- **Command Restrictions**: Disable dangerous commands

**Code Example:**
```bash
# Redis ACL configuration
# Create users with specific permissions
ACL SETUSER analyst on >analyst_password ~cached:* +@read -@dangerous
ACL SETUSER app_user on >app_password ~app:* +@all -flushdb -flushall -shutdown
ACL SETUSER admin on >admin_password ~* +@all

# List users
ACL LIST

# Check current user
ACL WHOAMI

# Redis configuration for security
# redis.conf
# requirepass your_strong_password
# rename-command FLUSHDB ""
# rename-command FLUSHALL ""
# rename-command DEBUG ""
# bind 127.0.0.1 10.0.0.1
# protected-mode yes
# port 0
# tls-port 6380
# tls-cert-file /path/to/redis.crt
# tls-key-file /path/to/redis.key
```

```python
import redis
import ssl

class SecureRedisConnection:
    def __init__(self, host, port, username, password, use_tls=True):
        self.connection_params = {
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'decode_responses': True
        }
        
        if use_tls:
            self.connection_params.update({
                'ssl': True,
                'ssl_cert_reqs': ssl.CERT_REQUIRED,
                'ssl_ca_certs': '/path/to/ca.crt',
                'ssl_certfile': '/path/to/client.crt',
                'ssl_keyfile': '/path/to/client.key'
            })
        
        self.client = redis.Redis(**self.connection_params)
    
    def test_connection(self):
        try:
            self.client.ping()
            print("Secure connection established")
            
            # Test ACL permissions
            current_user = self.client.acl_whoami()
            print(f"Connected as user: {current_user}")
            
            return True
        except redis.AuthenticationError:
            print("Authentication failed")
            return False
        except redis.ConnectionError:
            print("Connection failed")
            return False
    
    def safe_execute(self, command, *args):
        """Execute command with error handling"""
        try:
            return self.client.execute_command(command, *args)
        except redis.ResponseError as e:
            if "NOPERM" in str(e):
                print(f"Permission denied for command: {command}")
            else:
                print(f"Command error: {e}")
            return None

# Usage with different user roles
analyst_conn = SecureRedisConnection(
    'redis.internal', 6380, 'analyst', 'analyst_password'
)

app_conn = SecureRedisConnection(
    'redis.internal', 6380, 'app_user', 'app_password'
)

# Test permissions
if analyst_conn.test_connection():
    # Analyst can only read cached data
    analyst_conn.safe_execute('GET', 'cached:user:1001')
    analyst_conn.safe_execute('FLUSHDB')  # This will fail

if app_conn.test_connection():
    # App user can read/write app data
    app_conn.safe_execute('SET', 'app:session:123', 'data')
    app_conn.safe_execute('GET', 'app:session:123')
```

---

## 📊 **Performance & Optimization Questions**

### Q19: How do you implement Redis caching strategies for optimal performance?
**Answer:**
Implement appropriate caching patterns based on data access patterns, consistency requirements, and performance goals.

**Caching Patterns:**
- **Cache-Aside**: Application manages cache
- **Write-Through**: Synchronous cache updates
- **Write-Behind**: Asynchronous cache updates
- **Refresh-Ahead**: Proactive cache refresh
- **Circuit Breaker**: Fallback on cache failures

**Code Example:**
```python
import redis
import time
import threading
from functools import wraps
from datetime import datetime, timedelta

class AdvancedCacheManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.stats = {
            'hits': 0,
            'misses': 0,
            'errors': 0
        }
        self._lock = threading.Lock()
    
    def cache_with_refresh_ahead(self, key, fetch_func, ttl=3600, refresh_threshold=0.8):
        """Cache with proactive refresh before expiration"""
        try:
            # Get value and TTL
            pipe = self.redis.pipeline()
            pipe.get(key)
            pipe.ttl(key)
            cached_value, remaining_ttl = pipe.execute()
            
            if cached_value:
                self.stats['hits'] += 1
                
                # Check if refresh is needed
                if remaining_ttl > 0 and remaining_ttl < (ttl * refresh_threshold):
                    # Refresh in background
                    threading.Thread(
                        target=self._background_refresh,
                        args=(key, fetch_func, ttl)
                    ).start()
                
                return cached_value
            
            # Cache miss - fetch and store
            self.stats['misses'] += 1
            value = fetch_func()
            self.redis.setex(key, ttl, value)
            return value
            
        except Exception as e:
            self.stats['errors'] += 1
            # Fallback to direct fetch
            return fetch_func()
    
    def _background_refresh(self, key, fetch_func, ttl):
        """Background refresh of cache entry"""
        try:
            value = fetch_func()
            self.redis.setex(key, ttl, value)
        except Exception:
            pass  # Silent failure for background refresh
    
    def multi_level_cache(self, l1_key, l2_key, fetch_func, l1_ttl=300, l2_ttl=3600):
        """Two-level caching strategy"""
        # Level 1: Short TTL, frequently accessed
        l1_value = self.redis.get(l1_key)
        if l1_value:
            return l1_value
        
        # Level 2: Longer TTL, less frequently accessed
        l2_value = self.redis.get(l2_key)
        if l2_value:
            # Promote to L1
            self.redis.setex(l1_key, l1_ttl, l2_value)
            return l2_value
        
        # Fetch from source
        value = fetch_func()
        
        # Store in both levels
        pipe = self.redis.pipeline()
        pipe.setex(l1_key, l1_ttl, value)
        pipe.setex(l2_key, l2_ttl, value)
        pipe.execute()
        
        return value
    
    def cache_with_circuit_breaker(self, key, fetch_func, ttl=3600, 
                                 failure_threshold=5, recovery_timeout=60):
        """Cache with circuit breaker pattern"""
        circuit_key = f"circuit:{key}"
        
        # Check circuit breaker state
        circuit_info = self.redis.hgetall(circuit_key)
        if circuit_info:
            failures = int(circuit_info.get('failures', 0))
            last_failure = float(circuit_info.get('last_failure', 0))
            
            # Circuit is open (too many failures)
            if failures >= failure_threshold:
                if time.time() - last_failure < recovery_timeout:
                    # Return stale cache if available
                    stale_value = self.redis.get(f"stale:{key}")
                    if stale_value:
                        return stale_value
                    raise Exception("Circuit breaker open, no stale data")
        
        try:
            # Try to get from cache
            cached_value = self.redis.get(key)
            if cached_value:
                return cached_value
            
            # Fetch from source
            value = fetch_func()
            
            # Store in cache and stale backup
            pipe = self.redis.pipeline()
            pipe.setex(key, ttl, value)
            pipe.setex(f"stale:{key}", ttl * 2, value)  # Longer TTL for stale
            pipe.delete(circuit_key)  # Reset circuit breaker
            pipe.execute()
            
            return value
            
        except Exception as e:
            # Record failure
            pipe = self.redis.pipeline()
            pipe.hincrby(circuit_key, 'failures', 1)
            pipe.hset(circuit_key, 'last_failure', time.time())
            pipe.expire(circuit_key, recovery_timeout * 2)
            pipe.execute()
            
            # Try to return stale data
            stale_value = self.redis.get(f"stale:{key}")
            if stale_value:
                return stale_value
            
            raise e
    
    def get_cache_stats(self):
        """Get cache performance statistics"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hit_rate': hit_rate,
            'total_requests': total_requests,
            **self.stats
        }

# Usage examples
r = redis.Redis()
cache_manager = AdvancedCacheManager(r)

def expensive_database_query(user_id):
    """Simulate expensive database operation"""
    time.sleep(0.1)  # Simulate delay
    return f"User data for {user_id}"

# Refresh-ahead caching
user_data = cache_manager.cache_with_refresh_ahead(
    'user:1001',
    lambda: expensive_database_query(1001),
    ttl=300,
    refresh_threshold=0.8
)

# Multi-level caching
user_profile = cache_manager.multi_level_cache(
    'l1:profile:1001',  # L1 cache
    'l2:profile:1001',  # L2 cache
    lambda: expensive_database_query(1001),
    l1_ttl=60,   # 1 minute
    l2_ttl=3600  # 1 hour
)

# Circuit breaker caching
try:
    api_data = cache_manager.cache_with_circuit_breaker(
        'api:external:data',
        lambda: expensive_database_query('external'),
        ttl=300,
        failure_threshold=3,
        recovery_timeout=30
    )
except Exception as e:
    print(f"Circuit breaker activated: {e}")

# Check performance
stats = cache_manager.get_cache_stats()
print(f"Cache hit rate: {stats['hit_rate']:.2f}%")
```

---

## Key Takeaways

1. **In-Memory Performance**: Redis excels at microsecond latency due to in-memory storage and single-threaded architecture
2. **Data Structure Mastery**: Choose optimal Redis data types (Strings, Lists, Sets, Sorted Sets, Hashes, Streams) for specific use cases
3. **Memory Management**: Configure appropriate eviction policies and monitor memory usage patterns
4. **Persistence Strategy**: Balance RDB snapshots and AOF logging based on durability vs performance requirements
5. **Scaling Architecture**: Use replication for read scaling, clustering for horizontal scaling, Sentinel for high availability
6. **Concurrency Model**: Leverage Redis's atomic operations and single-threaded nature for thread-safe operations
7. **Advanced Patterns**: Implement distributed locks, rate limiting, message queues, and leaderboards efficiently
8. **Caching Strategies**: Apply cache-aside, write-through, refresh-ahead patterns based on access patterns
9. **Security Implementation**: Use ACLs, TLS encryption, and network isolation for production deployments
10. **Performance Monitoring**: Track latency, throughput, memory usage, and hit rates for optimization
11. **Module Extensions**: Leverage RedisJSON, RedisSearch, RedisGraph for specialized functionality
12. **Enterprise Integration**: Design Redis architecture for microservices with proper isolation and consistency
13. **Circuit Breaker Pattern**: Implement fallback mechanisms for high availability
14. **Multi-level Caching**: Use L1/L2 cache hierarchies for optimal performance
15. **Operational Excellence**: Monitor slow operations, configure alerts, and implement backup strategies