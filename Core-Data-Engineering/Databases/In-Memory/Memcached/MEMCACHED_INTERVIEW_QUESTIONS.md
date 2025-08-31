# Memcached - Interview Questions

## Basic Questions

### 1. What is Memcached and what is it used for?
**Answer:** Memcached is a high-performance, distributed memory caching system that stores data in RAM to reduce database load and improve application performance. It's commonly used for caching database query results, session data, and computed values in web applications.

### 2. How does Memcached differ from Redis?
**Answer:**
- **Data Types**: Memcached only supports strings; Redis supports multiple data types
- **Persistence**: Memcached has no persistence; Redis offers persistence options
- **Replication**: Memcached has no built-in replication; Redis supports master-slave replication
- **Memory Usage**: Memcached is more memory efficient for simple key-value storage
- **Operations**: Redis supports more complex operations and data structures

### 3. Explain Memcached's memory management system.
**Answer:** Memcached uses slab allocation:
- Memory is divided into slabs of different sizes
- Each slab contains chunks of the same size
- Growth factor (default 1.25) determines size progression
- LRU eviction removes least recently used items when memory is full
- No memory fragmentation due to fixed chunk sizes

## Intermediate Questions

### 4. How does Memcached distribute data across multiple servers?
**Answer:** Memcached uses consistent hashing:
- Client libraries hash the key to determine which server to use
- No server-to-server communication required
- Adding/removing servers affects minimal key redistribution
- Each key is stored on exactly one server (no replication)

### 5. What happens when a Memcached server fails?
**Answer:**
- Keys stored on the failed server become unavailable
- Cache misses occur for those keys
- Application falls back to original data source (database)
- No data loss since Memcached is a cache, not primary storage
- Client libraries can detect failure and route around it

### 6. Explain the different Memcached operations and when to use them.
**Answer:**
- **SET**: Store key-value pair (overwrites existing)
- **ADD**: Store only if key doesn't exist (prevents overwrites)
- **REPLACE**: Store only if key exists (updates existing)
- **GET**: Retrieve value by key
- **DELETE**: Remove key-value pair
- **INCR/DECR**: Atomic increment/decrement for counters

## Advanced Questions

### 7. How would you optimize Memcached performance?
**Answer:**
- **Connection Pooling**: Reuse connections to reduce overhead
- **Key Design**: Use short, consistent key names
- **Batch Operations**: Use multi-get for multiple keys
- **Memory Tuning**: Adjust slab sizes based on data patterns
- **Monitoring**: Track hit rates, memory usage, and evictions
- **Network**: Use persistent connections and consider compression

### 8. What are the security considerations with Memcached?
**Answer:**
- **Network Security**: Deploy in private networks/VPCs
- **Firewall Rules**: Restrict access to port 11211
- **No Authentication**: Memcached has no built-in authentication
- **Data Sensitivity**: Don't cache sensitive data without encryption
- **SASL Support**: Some versions support SASL authentication
- **Monitoring**: Log access patterns for security auditing

### 9. How would you implement cache warming strategies?
**Answer:**
```python
# Proactive cache warming
def warm_cache():
    popular_keys = get_popular_keys()
    for key in popular_keys:
        if not memcache.get(key):
            data = fetch_from_database(key)
            memcache.set(key, data, expiration=3600)

# Lazy loading with cache-aside pattern
def get_user_data(user_id):
    cache_key = f"user:{user_id}"
    data = memcache.get(cache_key)
    if not data:
        data = database.get_user(user_id)
        memcache.set(cache_key, data, expiration=1800)
    return data
```

### 10. How would you monitor and troubleshoot Memcached performance issues?
**Answer:**
Key metrics to monitor:
- **Hit Rate**: Percentage of successful cache hits
- **Memory Usage**: Current memory consumption vs. limit
- **Evictions**: Number of items evicted due to memory pressure
- **Connections**: Current and maximum connections
- **Commands**: GET/SET operation rates

Troubleshooting steps:
- Check hit rates (low rates indicate cache misses)
- Monitor eviction rates (high rates suggest insufficient memory)
- Analyze key distribution across servers
- Review application caching patterns
- Use tools like `memcached-tool` for server statistics