# Redis (In-Memory) - Interview Questions

## Basic Questions

### 1. What is Redis and what are its main use cases?
**Answer:** Redis is an in-memory data structure store used as database, cache, and message broker. Main use cases:
- **Caching**: Application data and session caching
- **Real-time analytics**: Counters, metrics, leaderboards
- **Message queues**: Task queues and pub/sub messaging
- **Session storage**: Web application session management
- **Rate limiting**: API rate limiting and throttling

### 2. What data structures does Redis support?
**Answer:** Redis supports multiple data structures:
- **Strings**: Binary-safe strings (text, numbers, serialized objects)
- **Hashes**: Field-value pairs (like objects/dictionaries)
- **Lists**: Ordered collections (queues, stacks)
- **Sets**: Unordered unique collections
- **Sorted Sets**: Sets ordered by score
- **Bitmaps**: Bit-level operations
- **HyperLogLog**: Cardinality estimation
- **Streams**: Log-like messaging

### 3. How does Redis handle persistence?
**Answer:** Redis offers multiple persistence options:
- **RDB**: Point-in-time snapshots at intervals
- **AOF**: Append-only file logging every write
- **Hybrid**: RDB snapshots + AOF for recent changes
- **No persistence**: Pure in-memory for maximum performance

## Intermediate Questions

### 4. Explain Redis clustering and how data is distributed.
**Answer:** Redis Cluster provides automatic sharding:
- **Hash slots**: 16384 slots distribute data across nodes
- **CRC16**: Hash function determines slot assignment
- **Master-slave**: Each master has replica nodes
- **Gossip protocol**: Nodes communicate cluster state
- **Client-side routing**: Clients route requests to correct nodes

### 5. What are Redis transactions and how do they work?
**Answer:** Redis transactions use MULTI/EXEC:
```redis
MULTI
SET key1 "value1"
INCR counter
EXEC
```
- **Atomic**: All commands execute or none
- **Isolation**: Commands queued until EXEC
- **No rollback**: Failed commands don't rollback others
- **WATCH**: Optimistic locking for conditional execution

### 6. How does Redis handle memory management and eviction?
**Answer:** Redis memory management includes:
- **Max memory**: Configurable memory limit
- **Eviction policies**: LRU, LFU, random, TTL-based
- **Expiration**: Automatic key expiration with TTL
- **Memory optimization**: Efficient data structure encoding
- **Monitoring**: Memory usage tracking and alerts

## Advanced Questions

### 7. How would you implement a distributed lock using Redis?
**Answer:**
```python
import redis
import time
import uuid

def acquire_lock(redis_client, key, timeout=10):
    identifier = str(uuid.uuid4())
    end = time.time() + timeout
    
    while time.time() < end:
        if redis_client.set(key, identifier, nx=True, ex=timeout):
            return identifier
        time.sleep(0.001)
    return False

def release_lock(redis_client, key, identifier):
    lua_script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    return redis_client.eval(lua_script, 1, key, identifier)
```

### 8. How do you implement rate limiting with Redis?
**Answer:** Sliding window rate limiting:
```python
def is_allowed(redis_client, user_id, limit=100, window=3600):
    key = f"rate_limit:{user_id}"
    current_time = int(time.time())
    
    pipe = redis_client.pipeline()
    pipe.zremrangebyscore(key, 0, current_time - window)
    pipe.zcard(key)
    pipe.zadd(key, {str(uuid.uuid4()): current_time})
    pipe.expire(key, window)
    
    results = pipe.execute()
    current_requests = results[1]
    
    return current_requests < limit
```

### 9. What are Redis Streams and how do they compare to Kafka?
**Answer:** Redis Streams provide log-like messaging:
- **Append-only**: Messages added with auto-generated IDs
- **Consumer groups**: Multiple consumers process messages
- **Acknowledgments**: Track message processing
- **Persistence**: Messages persist until explicitly deleted

Comparison with Kafka:
- **Simpler**: Easier setup and operation
- **Lower latency**: In-memory processing
- **Limited durability**: Less robust than Kafka's disk-based storage
- **Smaller scale**: Better for moderate throughput scenarios

### 10. How do you monitor and troubleshoot Redis performance?
**Answer:** Redis monitoring strategies:
- **INFO command**: Comprehensive server statistics
- **MONITOR**: Real-time command monitoring
- **SLOWLOG**: Track slow-running commands
- **Memory analysis**: MEMORY USAGE and MEMORY DOCTOR
- **Client connections**: CLIENT LIST and CLIENT TRACKING

Key metrics to monitor:
- Memory usage and fragmentation
- Hit/miss ratios for caching
- Command latency and throughput
- Replication lag
- Evicted keys and expired keys