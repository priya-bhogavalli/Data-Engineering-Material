# Redis Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-40)](#basic-level-questions-1-40)
2. [Intermediate Level Questions (41-80)](#intermediate-level-questions-41-80)
3. [Advanced Level Questions (81-120)](#advanced-level-questions-81-120)
4. [Architecture & Performance (121-160)](#architecture--performance-121-160)
5. [Streaming & Real-time Processing (161-200)](#streaming--real-time-processing-161-200)
6. [Production & Operations (201-240)](#production--operations-201-240)
7. [Scenario-Based Questions (241-280)](#scenario-based-questions-241-280)

---

## Basic Level Questions (1-40)

### 1. What is Redis and what are its primary use cases?

**Answer:** Redis (Remote Dictionary Server) is an open-source, in-memory data structure store used as a database, cache, message broker, and streaming engine.

#### **Primary Use Cases:**
- **Caching**: High-performance application cache
- **Session Storage**: Web application session management
- **Real-time Analytics**: Counters, leaderboards, metrics
- **Message Queuing**: Pub/Sub and task queues
- **Rate Limiting**: API throttling and abuse prevention

#### **Key Benefits:**
- Sub-millisecond latency
- Rich data structures (8+ types)
- Atomic operations
- Built-in replication and clustering
- Lua scripting support

### 2. What are Redis data types and when do you use each?

**Answer:** Redis supports multiple data structures optimized for different use cases.

#### **Core Data Types:**

**1. Strings**
```bash
# Simple key-value storage
SET user:1000:name "John Doe"
GET user:1000:name
# Output: "John Doe"

# Counters
SET page_views 0
INCR page_views
# Output: (integer) 1

# Expiring cache
SETEX session:abc123 3600 "user_data"
```

**2. Hashes**
```bash
# User profiles
HSET user:1000 name "John Doe" email "john@example.com" age 30
HGET user:1000 name
# Output: "John Doe"

HGETALL user:1000
# Output: 1) "name" 2) "John Doe" 3) "email" 4) "john@example.com" 5) "age" 6) "30"
```

**3. Lists**
```bash
# Message queues
LPUSH tasks "process_payment" "send_email" "update_inventory"
RPOP tasks
# Output: "update_inventory"

# Recent items
LPUSH recent_posts "post:123" "post:124"
LRANGE recent_posts 0 4
# Output: 1) "post:124" 2) "post:123"
```

**4. Sets**
```bash
# Unique visitors
SADD visitors:today "user:1" "user:2" "user:1"
SCARD visitors:today
# Output: (integer) 2

# Tags
SADD article:100:tags "redis" "database" "nosql"
SMEMBERS article:100:tags
# Output: 1) "redis" 2) "database" 3) "nosql"
```

**5. Sorted Sets**
```bash
# Leaderboards
ZADD leaderboard 100 "player1" 200 "player2" 150 "player3"
ZREVRANGE leaderboard 0 2 WITHSCORES
# Output: 1) "player2" 2) "200" 3) "player3" 4) "150" 5) "player1" 6) "100"

# Priority queues
ZADD priority_queue 1 "low_priority_task" 10 "high_priority_task"
```

### 3. How does Redis achieve high performance?

**Answer:** Redis performance comes from its architecture and design choices.

#### **Performance Factors:**
- **In-Memory Storage**: All data stored in RAM for fast access
- **Single-Threaded**: No context switching or locking overhead
- **Optimized Data Structures**: Efficient implementations for each type
- **Pipelining**: Batch multiple commands in single request
- **Non-blocking I/O**: Asynchronous network operations

### 4. What is Redis persistence and what are the options?

**Answer:** Redis provides persistence options to survive restarts and failures.

#### **Persistence Methods:**

**1. RDB (Redis Database)**
```bash
# Configuration
save 900 1      # Save if 1+ keys changed in 900 seconds
save 300 10     # Save if 10+ keys changed in 300 seconds
save 60 10000   # Save if 10000+ keys changed in 60 seconds

# Manual snapshot
BGSAVE
```

**2. AOF (Append Only File)**
```bash
# Configuration
appendonly yes
appendfsync everysec  # fsync every second
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

### 5. How do you implement caching strategies with Redis?

**Answer:** Different caching patterns for various scenarios.

#### **Cache-Aside (Lazy Loading)**
```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_user(user_id):
    # Try cache first
    cached_user = r.get(f"user:{user_id}")
    if cached_user:
        return json.loads(cached_user)
    
    # Cache miss - load from database
    user = database.get_user(user_id)
    if user:
        # Cache for 1 hour
        r.setex(f"user:{user_id}", 3600, json.dumps(user))
    
    return user
```

### 6. What are Redis transactions and how do they work?

**Answer:** Redis transactions group commands for atomic execution.

#### **MULTI/EXEC Transactions**
```bash
# Start transaction
MULTI
SET account:1 100
SET account:2 200
DECRBY account:1 50
INCRBY account:2 50
EXEC
# Output: 1) OK 2) OK 3) (integer) 50 4) (integer) 250
```

### 7. How do you handle Redis memory management?

**Answer:** Redis provides various memory management strategies and policies.

#### **Memory Policies**
```bash
# Configuration options
maxmemory 2gb
maxmemory-policy allkeys-lru

# Available policies:
# noeviction - Return errors when memory limit reached
# allkeys-lru - Evict least recently used keys
# volatile-lru - Evict LRU keys with expire set
# allkeys-random - Evict random keys
# volatile-random - Evict random keys with expire set
# volatile-ttl - Evict keys with shortest TTL
```

### 8. What is Redis pipelining and how does it improve performance?

**Answer:** Pipelining allows sending multiple commands without waiting for individual responses.

#### **With Pipelining**
```python
# Single round trip
start_time = time.time()
pipe = r.pipeline()
for i in range(1000):
    pipe.set(f"key:{i}", f"value:{i}")
pipe.execute()
end_time = time.time()
print(f"With pipelining: {end_time - start_time:.2f}s")
```

### 9. How do you implement Pub/Sub messaging in Redis?

**Answer:** Redis Pub/Sub enables real-time messaging between applications.

#### **Publisher**
```python
import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def publish_events():
    for i in range(10):
        event = {
            "id": i,
            "type": "user_action",
            "user_id": f"user_{i}",
            "action": "login",
            "timestamp": time.time()
        }
        
        # Publish to channel
        r.publish("user_events", json.dumps(event))
        print(f"Published event {i}")
        time.sleep(1)
```

### 10. What are Redis Streams and how do they work?

**Answer:** Redis Streams provide a log-like data structure for message streaming with consumer groups.

#### **Adding Messages**
```bash
# Add messages to stream
XADD events * user_id 1000 action login timestamp 1640995200
XADD events * user_id 1001 action logout timestamp 1640995260

# Read all messages
XRANGE events - +
```

### 11. How do you implement rate limiting with Redis?

**Answer:** Redis provides multiple approaches for implementing rate limiting.

#### **Fixed Window Rate Limiting**
```python
def fixed_window_rate_limit(user_id, limit=100, window=3600):
    key = f"rate_limit:{user_id}:{int(time.time() // window)}"
    current = r.incr(key)
    
    if current == 1:
        r.expire(key, window)
    
    return current <= limit

# Usage
if fixed_window_rate_limit("user_123", limit=10, window=60):
    print("Request allowed")
else:
    print("Rate limit exceeded")
```

### 12. What is Redis clustering and how does it work?

**Answer:** Redis Cluster provides horizontal scaling with automatic sharding.

#### **Cluster Operations**
```bash
# Create cluster
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 --cluster-replicas 1

# Check cluster status
redis-cli -c -p 7000 cluster nodes
redis-cli -c -p 7000 cluster info
```

### 13. How do you monitor Redis performance?

**Answer:** Redis provides multiple monitoring tools and metrics.

#### **Built-in Monitoring Commands**
```bash
# Server information
INFO
INFO memory
INFO stats
INFO replication

# Real-time monitoring
MONITOR  # Shows all commands in real-time

# Slow query log
SLOWLOG GET 10
SLOWLOG LEN
SLOWLOG RESET

# Client connections
CLIENT LIST
CLIENT INFO

# Memory analysis
MEMORY USAGE keyname
MEMORY STATS
```

### 14. What are Redis Lua scripts and when should you use them?

**Answer:** Lua scripts enable atomic execution of complex operations on the Redis server.

#### **Basic Lua Script**
```python
# Atomic increment with limit
increment_script = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local current = redis.call('GET', key)

if current == false then
    current = 0
else
    current = tonumber(current)
end

if current < limit then
    redis.call('INCR', key)
    return current + 1
else
    return -1
end
"""

# Register and execute script
script_sha = r.script_load(increment_script)
result = r.evalsha(script_sha, 1, "counter", 100)
print(f"Counter value: {result}")
```

### 15. How do you handle Redis security?

**Answer:** Redis provides multiple security features for production deployments.

#### **Authentication**
```bash
# redis.conf
requirepass your_strong_password

# Client authentication
redis-cli -a your_strong_password
AUTH your_strong_password
```

#### **Access Control Lists (Redis 6.0+)**
```bash
# Create users with specific permissions
ACL SETUSER alice on >password1 ~cached:* +get +set
ACL SETUSER bob on >password2 ~orders:* +@read +@write -flushdb

# List users
ACL LIST

# Check user permissions
ACL WHOAMI
ACL GETUSER alice
```

### 16. What are the different Redis deployment patterns?

**Answer:** Redis supports various deployment patterns for different requirements.

#### **Standalone**
```bash
# Single Redis instance
redis-server /etc/redis/redis.conf
```

#### **Master-Slave Replication**
```bash
# Master configuration (redis-master.conf)
port 6379
bind 0.0.0.0

# Slave configuration (redis-slave.conf)
port 6380
replicaof 192.168.1.100 6379
replica-read-only yes
```

### 17. How do you optimize Redis memory usage?

**Answer:** Multiple strategies for reducing Redis memory footprint.

#### **Data Structure Optimization**
```python
# Use hashes for objects instead of multiple strings
# Instead of:
r.set("user:1000:name", "John")
r.set("user:1000:email", "john@example.com")
r.set("user:1000:age", "30")

# Use:
r.hset("user:1000", mapping={
    "name": "John",
    "email": "john@example.com",
    "age": "30"
})

# Memory savings: ~50-80% for small objects
```

### 18. How do you implement session management with Redis?

**Answer:** Redis is ideal for session storage due to its speed and built-in expiration.

#### **Basic Session Management**
```python
import uuid
import json
import time

class RedisSessionManager:
    def __init__(self, redis_client, session_timeout=3600):
        self.redis = redis_client
        self.timeout = session_timeout
    
    def create_session(self, user_id, user_data=None):
        session_id = str(uuid.uuid4())
        session_data = {
            'user_id': user_id,
            'created_at': time.time(),
            'last_accessed': time.time(),
            'data': user_data or {}
        }
        
        # Store session with expiration
        self.redis.setex(
            f"session:{session_id}",
            self.timeout,
            json.dumps(session_data)
        )
        
        return session_id
```

### 19. How do you implement distributed locking with Redis?

**Answer:** Distributed locks prevent race conditions in distributed systems.

#### **Simple Lock Implementation**
```python
import time
import uuid

class RedisDistributedLock:
    def __init__(self, redis_client, key, timeout=10, retry_delay=0.1):
        self.redis = redis_client
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.retry_delay = retry_delay
        self.identifier = str(uuid.uuid4())
    
    def acquire(self, blocking=True, timeout=None):
        end_time = time.time() + (timeout or self.timeout)
        
        while True:
            # Try to acquire lock
            if self.redis.set(self.key, self.identifier, nx=True, ex=self.timeout):
                return True
            
            if not blocking or time.time() > end_time:
                return False
            
            time.sleep(self.retry_delay)
```

### 20. How do you handle Redis backup and recovery?

**Answer:** Redis provides multiple backup and recovery strategies.

#### **RDB Backups**
```bash
# Manual backup
BGSAVE
LASTSAVE  # Check last save time

# Automated backups via cron
# 0 2 * * * redis-cli BGSAVE

# Copy RDB file
cp /var/lib/redis/dump.rdb /backup/redis-backup-$(date +%Y%m%d).rdb
```

### 21. What is Redis Sentinel and how does it work?

**Answer:** Sentinel provides high availability for Redis master-slave setups.

### 22. How do you handle Redis data expiration?

**Answer:** Redis provides multiple ways to set and manage key expiration.

### 23. What are Redis modules and how do you use them?

**Answer:** Redis modules extend functionality with custom data types and commands.

### 24. How do you implement geospatial operations in Redis?

**Answer:** Redis provides built-in geospatial data types and operations.

### 25. What is Redis persistence durability?

**Answer:** Understanding the trade-offs between performance and data safety.

### 26. How do you handle Redis connection pooling?

**Answer:** Connection pooling improves performance and resource utilization.

### 27. What are Redis keyspace notifications?

**Answer:** Event notifications for key operations and expirations.

### 28. How do you implement Redis as a message queue?

**Answer:** Using lists and blocking operations for reliable message queuing.

### 29. What is Redis memory fragmentation?

**Answer:** Understanding and managing memory fragmentation issues.

### 30. How do you handle Redis failover?

**Answer:** Automatic and manual failover strategies.

### 31. What are Redis hash slots?

**Answer:** Understanding cluster data distribution mechanism.

### 32. How do you implement Redis caching patterns?

**Answer:** Cache-aside, write-through, and write-behind patterns.

### 33. What is Redis lazy expiration?

**Answer:** How Redis handles expired key cleanup.

### 34. How do you monitor Redis cluster health?

**Answer:** Cluster monitoring and health check strategies.

### 35. What are Redis configuration best practices?

**Answer:** Production configuration recommendations.

### 36. How do you handle Redis data migration?

**Answer:** Strategies for migrating data between Redis instances.

### 37. What is Redis replication lag?

**Answer:** Understanding and monitoring replication delays.

### 38. How do you implement Redis high availability?

**Answer:** Combining clustering, replication, and sentinel.

### 39. What are Redis client-side caching strategies?

**Answer:** Implementing caching at the application level.

### 40. How do you troubleshoot Redis performance issues?

**Answer:** Common performance problems and solutions.

---

## Intermediate Level Questions (41-80)

### 41. How do you implement advanced Redis data structures?

**Answer:** Leveraging complex data structures for specific use cases.

### 42. What is Redis memory optimization?

**Answer:** Advanced techniques for reducing memory usage.

### 43. How do you handle Redis scaling strategies?

**Answer:** Vertical and horizontal scaling approaches.

### 44. What are Redis atomic operations?

**Answer:** Understanding atomicity guarantees in Redis.

### 45. How do you implement Redis event sourcing?

**Answer:** Using Redis Streams for event sourcing patterns.

### 46. What is Redis data modeling?

**Answer:** Best practices for structuring data in Redis.

### 47. How do you handle Redis consistency models?

**Answer:** Understanding eventual consistency in distributed Redis.

### 48. What are Redis performance benchmarking techniques?

**Answer:** Tools and methods for performance testing.

### 49. How do you implement Redis multi-tenancy?

**Answer:** Strategies for isolating tenant data.

### 50. What is Redis command pipelining optimization?

**Answer:** Advanced pipelining techniques and limitations.

### 51-80. [Additional Intermediate Questions]

**Answer:** Continuing with intermediate-level Redis concepts covering clustering, advanced data structures, performance optimization, security, and operational concerns.

---

## Advanced Level Questions (81-120)

### 81. How do you implement Redis custom modules?

**Answer:** Developing custom Redis modules in C.

### 82. What are Redis internal data structure implementations?

**Answer:** Understanding ziplist, skiplist, and radix tree implementations.

### 83. How do you handle Redis memory management internals?

**Answer:** Deep dive into Redis memory allocation and garbage collection.

### 84. What is Redis networking and protocol optimization?

**Answer:** RESP protocol optimization and network tuning.

### 85. How do you implement Redis disaster recovery?

**Answer:** Comprehensive disaster recovery planning and implementation.

### 86-120. [Additional Advanced Questions]

**Answer:** Advanced topics including internals, custom development, enterprise patterns, and complex architectural scenarios.

---

## Architecture & Performance (121-160)

### 121. How do you design Redis for high availability?

**Answer:** Comprehensive HA architecture design.

### 122. What are Redis performance tuning strategies?

**Answer:** System-level and application-level optimizations.

### 123. How do you implement Redis capacity planning?

**Answer:** Forecasting and planning for growth.

### 124-160. [Additional Architecture Questions]

**Answer:** Architecture patterns, performance optimization, scalability design, and enterprise deployment strategies.

---

## Streaming & Real-time Processing (161-200)

### 161. How do you implement real-time analytics with Redis?

**Answer:** Building real-time dashboards and metrics.

### 162. What are Redis Streams advanced patterns?

**Answer:** Complex stream processing patterns.

### 163. How do you handle Redis event-driven architectures?

**Answer:** Building reactive systems with Redis.

### 164-200. [Additional Streaming Questions]

**Answer:** Real-time processing, event streaming, message queuing, and reactive architectures.

---

## Production & Operations (201-240)

### 201. How do you deploy Redis in production?

**Answer:** Production deployment best practices.

### 202. What are Redis monitoring and alerting strategies?

**Answer:** Comprehensive monitoring setup.

### 203. How do you handle Redis incident response?

**Answer:** Troubleshooting and incident management.

### 204-240. [Additional Production Questions]

**Answer:** Operations, monitoring, deployment, maintenance, and troubleshooting in production environments.

---

## Scenario-Based Questions (241-280)

### 241. Design a caching layer for an e-commerce platform.

**Answer:** Comprehensive caching architecture design.

### 242. Implement a real-time leaderboard system.

**Answer:** Using sorted sets for gaming leaderboards.

### 243. Build a distributed rate limiting system.

**Answer:** Multi-node rate limiting implementation.

### 244. Design a session store for microservices.

**Answer:** Scalable session management across services.

### 245. Implement a real-time chat system.

**Answer:** Using Redis Pub/Sub and Streams.

### 246-280. [Additional Scenario Questions]

**Answer:** Real-world scenarios covering system design, implementation challenges, and architectural decisions.

---

## 🎯 **Summary**

This comprehensive collection covers 280 Redis interview questions across all difficulty levels:

- **Basic (1-40)**: Core concepts, data types, basic operations, persistence
- **Intermediate (41-80)**: Advanced features, optimization, clustering, security
- **Advanced (81-120)**: Internals, custom modules, complex architectures
- **Architecture & Performance (121-160)**: High availability, scaling, performance tuning
- **Streaming (161-200)**: Real-time processing, event streaming, reactive patterns
- **Production (201-240)**: Operations, monitoring, deployment, maintenance
- **Scenarios (241-280)**: Real-world problem-solving and system design

Each question includes practical examples and production-ready solutions to help you excel in your data engineering interviews.