# Redis Key Concepts

## 🎯 What is Redis?
In-memory data structure store used as database, cache, and message broker with sub-millisecond latency.

## 🏗️ Core Data Types

### String
```bash
# Set/Get
SET user:1:name "John Doe"
GET user:1:name

# Increment
INCR page_views
INCRBY score 10
```

### Hash
```bash
# Hash operations
HSET user:1 name "John" age 30 email "john@example.com"
HGET user:1 name
HGETALL user:1
```

### List
```bash
# List operations
LPUSH tasks "task1" "task2"
RPOP tasks
LRANGE tasks 0 -1
```

### Set
```bash
# Set operations
SADD tags "redis" "database" "cache"
SMEMBERS tags
SINTER set1 set2
```

### Sorted Set
```bash
# Sorted set operations
ZADD leaderboard 100 "player1" 200 "player2"
ZRANGE leaderboard 0 -1 WITHSCORES
ZREVRANK leaderboard "player1"
```

## 🔧 Advanced Features

### Pub/Sub
```bash
# Publisher
PUBLISH news "Breaking news update"

# Subscriber
SUBSCRIBE news
PSUBSCRIBE news:*
```

### Transactions
```bash
MULTI
SET key1 "value1"
INCR counter
EXEC
```

### Lua Scripting
```lua
-- Atomic increment with limit
local current = redis.call('GET', KEYS[1])
if current == false or tonumber(current) < tonumber(ARGV[1]) then
    return redis.call('INCR', KEYS[1])
else
    return current
end
```

## 🚀 Performance Features

### Persistence Options
```bash
# RDB Snapshots
SAVE 900 1    # Save if 1 key changed in 900 seconds
BGSAVE       # Background save

# AOF (Append Only File)
appendonly yes
appendfsync everysec
```

### Memory Optimization
```bash
# Memory usage
MEMORY USAGE key
MEMORY STATS

# Expiration
EXPIRE key 3600
TTL key
```

## 🔧 Clustering & Replication

### Redis Cluster
```bash
# Cluster setup
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  --cluster-replicas 1
```

### Master-Slave Replication
```bash
# Slave configuration
SLAVEOF 192.168.1.100 6379
SLAVE-READ-ONLY yes
```

## 🎯 Common Use Cases

### Caching
```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Cache with expiration
r.setex('user:1:profile', 3600, json.dumps(user_data))

# Get cached data
cached_data = r.get('user:1:profile')
```

### Session Storage
```python
# Store session
r.hset(f'session:{session_id}', mapping={
    'user_id': user_id,
    'login_time': timestamp,
    'permissions': json.dumps(permissions)
})
r.expire(f'session:{session_id}', 1800)  # 30 minutes
```

### Rate Limiting
```python
def rate_limit(user_id, limit=100, window=3600):
    key = f'rate_limit:{user_id}'
    current = r.incr(key)
    if current == 1:
        r.expire(key, window)
    return current <= limit
```

## 🔒 Security & Best Practices

### Security Configuration
```bash
# Authentication
requirepass your_secure_password

# Disable dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""

# Bind to specific interface
bind 127.0.0.1
```

### Best Practices
- Use connection pooling
- Implement proper key naming conventions
- Monitor memory usage
- Set appropriate expiration times
- Use pipelining for bulk operations
- Implement proper error handling

## 🎯 Use Cases
- Application caching
- Session management
- Real-time analytics
- Leaderboards and counters
- Message queuing
- Geospatial applications

## ⚠️ Considerations
- Data volatility (in-memory)
- Memory limitations
- Single-threaded nature
- Persistence trade-offs
- Network latency impact