# System Design Interview Questions & Answers

## Table of Contents
1. [System Design Fundamentals](#system-design-fundamentals)
2. [Scalability & Performance](#scalability--performance)
3. [Database Design](#database-design)
4. [Caching Strategies](#caching-strategies)
5. [Load Balancing](#load-balancing)
6. [Microservices Architecture](#microservices-architecture)
7. [Data Pipeline Design](#data-pipeline-design)

---

## System Design Fundamentals

### 1. How do you approach a system design interview question?

**Answer:**
**Step-by-Step Approach:**

**1. Clarify Requirements (5-10 minutes)**
- Functional requirements: What should the system do?
- Non-functional requirements: Scale, performance, availability
- Constraints: Budget, timeline, technology preferences

**2. Estimate Scale (5 minutes)**
- Users: Daily/Monthly active users
- Data: Storage requirements, read/write ratio
- Traffic: Requests per second, peak load

**3. High-Level Design (10-15 minutes)**
- Major components and their interactions
- API design
- Database schema (high-level)

**4. Detailed Design (15-20 minutes)**
- Deep dive into critical components
- Database design
- Caching strategy
- Load balancing

**5. Scale the Design (10-15 minutes)**
- Identify bottlenecks
- Scaling strategies
- Monitoring and alerting

**Example Framework:**
```
Requirements:
- Design a URL shortener like bit.ly
- 100M URLs shortened per day
- 10:1 read/write ratio
- 99.9% availability

Scale Estimation:
- Write: 100M/day = 1,200 QPS
- Read: 12,000 QPS
- Storage: 100M * 365 * 5 years * 500 bytes = ~100TB
```

### 2. What are the key principles of scalable system design?

**Answer:**
**Core Principles:**

**1. Scalability**
- Horizontal scaling over vertical scaling
- Stateless services
- Database sharding and replication

**2. Reliability**
- Fault tolerance and redundancy
- Circuit breakers and timeouts
- Graceful degradation

**3. Availability**
- Load balancing and failover
- Geographic distribution
- Health checks and monitoring

**4. Consistency**
- CAP theorem considerations
- Eventual consistency vs strong consistency
- Data synchronization strategies

**5. Performance**
- Caching at multiple levels
- Asynchronous processing
- Content delivery networks (CDN)

**Example Architecture:**
```
[Client] -> [Load Balancer] -> [API Gateway] -> [Microservices]
                                                      |
[CDN] -> [Cache Layer] -> [Database Cluster] -> [Message Queue]
```

### 3. Explain the CAP theorem and its implications.

**Answer:**
**CAP Theorem:**
In a distributed system, you can only guarantee two of the following three properties:

**Consistency (C):** All nodes see the same data simultaneously
**Availability (A):** System remains operational
**Partition Tolerance (P):** System continues despite network failures

**Real-World Examples:**

**CP Systems (Consistency + Partition Tolerance):**
- Traditional RDBMS with ACID properties
- MongoDB with strong consistency
- HBase, Redis Cluster

```sql
-- Strong consistency example
BEGIN TRANSACTION;
UPDATE account SET balance = balance - 100 WHERE id = 1;
UPDATE account SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

**AP Systems (Availability + Partition Tolerance):**
- Cassandra, DynamoDB
- DNS systems
- Web caches

**CA Systems (Consistency + Availability):**
- Single-node databases
- Traditional monolithic applications

**Practical Implications:**
```python
# Eventual consistency example
def transfer_money(from_account, to_account, amount):
    # Write to multiple replicas asynchronously
    write_to_replica_1(from_account, -amount)
    write_to_replica_2(to_account, +amount)
    
    # Eventually consistent - may take time to propagate
    schedule_consistency_check(from_account, to_account)
```

---

## Scalability & Performance

### 4. How do you design a system to handle millions of requests per second?

**Answer:**
**Multi-Layer Scaling Strategy:**

**1. Load Balancing:**
```nginx
# Nginx load balancer configuration
upstream backend {
    least_conn;
    server web1.example.com weight=3;
    server web2.example.com weight=2;
    server web3.example.com weight=1;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**2. Horizontal Scaling:**
```yaml
# Kubernetes auto-scaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 10
  maxReplicas: 100
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**3. Caching Strategy:**
```python
# Multi-level caching
import redis
import memcached

class CacheManager:
    def __init__(self):
        self.l1_cache = {}  # In-memory cache
        self.l2_cache = redis.Redis()  # Redis cache
        self.l3_cache = memcached.Client()  # Distributed cache
    
    def get(self, key):
        # Check L1 cache first
        if key in self.l1_cache:
            return self.l1_cache[key]
        
        # Check L2 cache
        value = self.l2_cache.get(key)
        if value:
            self.l1_cache[key] = value
            return value
        
        # Check L3 cache
        value = self.l3_cache.get(key)
        if value:
            self.l2_cache.set(key, value, 3600)
            self.l1_cache[key] = value
            return value
        
        return None
```

**4. Database Optimization:**
```sql
-- Read replicas for scaling reads
-- Master-slave replication
CREATE REPLICA DATABASE read_replica_1 FROM master_db;
CREATE REPLICA DATABASE read_replica_2 FROM master_db;

-- Sharding for scaling writes
-- Horizontal partitioning by user_id
CREATE TABLE users_shard_1 AS SELECT * FROM users WHERE user_id % 4 = 0;
CREATE TABLE users_shard_2 AS SELECT * FROM users WHERE user_id % 4 = 1;
CREATE TABLE users_shard_3 AS SELECT * FROM users WHERE user_id % 4 = 2;
CREATE TABLE users_shard_4 AS SELECT * FROM users WHERE user_id % 4 = 3;
```

### 5. What are the different types of load balancing algorithms?

**Answer:**
**Load Balancing Algorithms:**

**1. Round Robin:**
```python
class RoundRobinBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server
```

**2. Weighted Round Robin:**
```python
class WeightedRoundRobinBalancer:
    def __init__(self, servers_weights):
        self.servers = []
        for server, weight in servers_weights.items():
            self.servers.extend([server] * weight)
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server
```

**3. Least Connections:**
```python
class LeastConnectionsBalancer:
    def __init__(self, servers):
        self.servers = {server: 0 for server in servers}
    
    def get_server(self):
        return min(self.servers, key=self.servers.get)
    
    def add_connection(self, server):
        self.servers[server] += 1
    
    def remove_connection(self, server):
        self.servers[server] -= 1
```

**4. IP Hash:**
```python
import hashlib

class IPHashBalancer:
    def __init__(self, servers):
        self.servers = servers
    
    def get_server(self, client_ip):
        hash_value = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        return self.servers[hash_value % len(self.servers)]
```

**5. Consistent Hashing:**
```python
import hashlib
import bisect

class ConsistentHashBalancer:
    def __init__(self, servers, replicas=3):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
        
        for server in servers:
            self.add_server(server)
    
    def add_server(self, server):
        for i in range(self.replicas):
            key = self.hash(f"{server}:{i}")
            self.ring[key] = server
            bisect.insort(self.sorted_keys, key)
    
    def get_server(self, key):
        if not self.ring:
            return None
        
        hash_key = self.hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_key)
        if idx == len(self.sorted_keys):
            idx = 0
        
        return self.ring[self.sorted_keys[idx]]
    
    def hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

---

## Database Design

### 6. How do you design a database schema for a social media platform?

**Answer:**
**Core Entities and Relationships:**

```sql
-- Users table
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    bio TEXT,
    profile_picture_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Posts table
CREATE TABLE posts (
    post_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content TEXT,
    image_urls JSON,
    post_type ENUM('text', 'image', 'video', 'link') DEFAULT 'text',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Followers/Following relationship
CREATE TABLE user_relationships (
    follower_id BIGINT,
    following_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, following_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_id),
    FOREIGN KEY (following_id) REFERENCES users(user_id)
);

-- Likes table
CREATE TABLE post_likes (
    user_id BIGINT,
    post_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

-- Comments table
CREATE TABLE comments (
    comment_id BIGINT PRIMARY KEY,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    parent_comment_id BIGINT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id)
);
```

**Indexing Strategy:**
```sql
-- Performance indexes
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
CREATE INDEX idx_user_relationships_follower ON user_relationships(follower_id);
CREATE INDEX idx_user_relationships_following ON user_relationships(following_id);
CREATE INDEX idx_post_likes_post ON post_likes(post_id);
CREATE INDEX idx_comments_post ON comments(post_id, created_at);
```

**Sharding Strategy:**
```python
# Shard by user_id for better data locality
def get_shard(user_id, num_shards=16):
    return f"shard_{user_id % num_shards}"

def get_user_posts(user_id):
    shard = get_shard(user_id)
    query = f"SELECT * FROM {shard}.posts WHERE user_id = %s ORDER BY created_at DESC"
    return execute_query(query, [user_id])
```

### 7. How do you handle database scaling for read-heavy vs write-heavy workloads?

**Answer:**

**Read-Heavy Workloads:**

**1. Read Replicas:**
```python
class DatabaseRouter:
    def __init__(self):
        self.master = connect_to_master()
        self.read_replicas = [
            connect_to_replica('replica1'),
            connect_to_replica('replica2'),
            connect_to_replica('replica3')
        ]
        self.replica_index = 0
    
    def read_query(self, query, params):
        replica = self.read_replicas[self.replica_index]
        self.replica_index = (self.replica_index + 1) % len(self.read_replicas)
        return replica.execute(query, params)
    
    def write_query(self, query, params):
        return self.master.execute(query, params)
```

**2. Caching Layer:**
```python
import redis

class CachedDatabase:
    def __init__(self):
        self.db = DatabaseRouter()
        self.cache = redis.Redis()
    
    def get_user(self, user_id):
        cache_key = f"user:{user_id}"
        cached_user = self.cache.get(cache_key)
        
        if cached_user:
            return json.loads(cached_user)
        
        user = self.db.read_query(
            "SELECT * FROM users WHERE user_id = %s", 
            [user_id]
        )
        
        if user:
            self.cache.setex(cache_key, 3600, json.dumps(user))
        
        return user
```

**Write-Heavy Workloads:**

**1. Database Sharding:**
```python
class ShardedDatabase:
    def __init__(self, shards):
        self.shards = shards
    
    def get_shard(self, key):
        shard_id = hash(key) % len(self.shards)
        return self.shards[shard_id]
    
    def insert_post(self, user_id, post_data):
        shard = self.get_shard(user_id)
        return shard.execute(
            "INSERT INTO posts (user_id, content, created_at) VALUES (%s, %s, %s)",
            [user_id, post_data['content'], datetime.now()]
        )
```

**2. Write Buffering:**
```python
import asyncio
from collections import defaultdict

class WriteBuffer:
    def __init__(self, batch_size=1000, flush_interval=5):
        self.buffer = defaultdict(list)
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.start_flush_timer()
    
    def add_write(self, table, data):
        self.buffer[table].append(data)
        
        if len(self.buffer[table]) >= self.batch_size:
            self.flush_table(table)
    
    def flush_table(self, table):
        if self.buffer[table]:
            batch_insert(table, self.buffer[table])
            self.buffer[table].clear()
    
    async def start_flush_timer(self):
        while True:
            await asyncio.sleep(self.flush_interval)
            for table in self.buffer:
                self.flush_table(table)
```

---

## Caching Strategies

### 8. What are the different caching patterns and when to use them?

**Answer:**

**1. Cache-Aside (Lazy Loading):**
```python
def get_user_cache_aside(user_id):
    # Check cache first
    user = cache.get(f"user:{user_id}")
    if user:
        return user
    
    # Cache miss - fetch from database
    user = database.get_user(user_id)
    if user:
        cache.set(f"user:{user_id}", user, ttl=3600)
    
    return user

def update_user_cache_aside(user_id, user_data):
    # Update database
    database.update_user(user_id, user_data)
    
    # Invalidate cache
    cache.delete(f"user:{user_id}")
```

**2. Write-Through:**
```python
def update_user_write_through(user_id, user_data):
    # Update database first
    database.update_user(user_id, user_data)
    
    # Update cache
    cache.set(f"user:{user_id}", user_data, ttl=3600)
    
    return user_data
```

**3. Write-Behind (Write-Back):**
```python
class WriteBehindCache:
    def __init__(self):
        self.cache = {}
        self.dirty_keys = set()
        self.write_queue = asyncio.Queue()
    
    def set(self, key, value):
        self.cache[key] = value
        self.dirty_keys.add(key)
        self.write_queue.put_nowait(key)
    
    async def background_writer(self):
        while True:
            key = await self.write_queue.get()
            if key in self.dirty_keys:
                value = self.cache[key]
                await database.update_async(key, value)
                self.dirty_keys.discard(key)
```

**4. Refresh-Ahead:**
```python
import asyncio
from datetime import datetime, timedelta

class RefreshAheadCache:
    def __init__(self, refresh_threshold=0.8):
        self.cache = {}
        self.metadata = {}
        self.refresh_threshold = refresh_threshold
    
    def get(self, key):
        if key in self.cache:
            # Check if refresh is needed
            meta = self.metadata[key]
            age = (datetime.now() - meta['created']).total_seconds()
            
            if age > (meta['ttl'] * self.refresh_threshold):
                # Trigger background refresh
                asyncio.create_task(self.refresh_key(key))
            
            return self.cache[key]
        
        # Cache miss
        return self.load_and_cache(key)
    
    async def refresh_key(self, key):
        new_value = await database.get_async(key)
        self.cache[key] = new_value
        self.metadata[key] = {
            'created': datetime.now(),
            'ttl': 3600
        }
```

### 9. How do you handle cache invalidation in a distributed system?

**Answer:**

**1. Time-Based Expiration:**
```python
# Simple TTL approach
cache.setex("user:123", 3600, user_data)  # Expire in 1 hour
```

**2. Event-Based Invalidation:**
```python
import redis

class EventBasedCache:
    def __init__(self):
        self.cache = redis.Redis()
        self.pubsub = self.cache.pubsub()
        self.pubsub.subscribe('cache_invalidation')
    
    def invalidate_user(self, user_id):
        # Remove from local cache
        self.cache.delete(f"user:{user_id}")
        
        # Notify other instances
        self.cache.publish('cache_invalidation', f"user:{user_id}")
    
    def listen_for_invalidations(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                key = message['data'].decode()
                self.cache.delete(key)
```

**3. Version-Based Invalidation:**
```python
class VersionedCache:
    def __init__(self):
        self.cache = redis.Redis()
        self.version_store = redis.Redis(db=1)
    
    def get(self, key):
        current_version = self.version_store.get(f"version:{key}")
        cached_data = self.cache.hgetall(key)
        
        if cached_data and cached_data.get('version') == current_version:
            return cached_data['data']
        
        # Cache miss or stale data
        fresh_data = database.get(key)
        new_version = str(int(current_version or 0) + 1)
        
        self.cache.hset(key, mapping={
            'data': fresh_data,
            'version': new_version
        })
        self.version_store.set(f"version:{key}", new_version)
        
        return fresh_data
    
    def invalidate(self, key):
        current_version = self.version_store.get(f"version:{key}")
        new_version = str(int(current_version or 0) + 1)
        self.version_store.set(f"version:{key}", new_version)
```

**4. Cache Tags:**
```python
class TaggedCache:
    def __init__(self):
        self.cache = redis.Redis()
    
    def set_with_tags(self, key, value, tags, ttl=3600):
        # Store the actual data
        self.cache.setex(key, ttl, value)
        
        # Associate with tags
        for tag in tags:
            self.cache.sadd(f"tag:{tag}", key)
            self.cache.expire(f"tag:{tag}", ttl)
    
    def invalidate_by_tag(self, tag):
        # Get all keys with this tag
        keys = self.cache.smembers(f"tag:{tag}")
        
        if keys:
            # Delete all associated keys
            self.cache.delete(*keys)
            # Delete the tag set
            self.cache.delete(f"tag:{tag}")

# Usage
cache.set_with_tags(
    "user:123", 
    user_data, 
    tags=["user", "profile", "user:123"], 
    ttl=3600
)

# Invalidate all user-related cache
cache.invalidate_by_tag("user")
```

---

## Load Balancing

### 10. How do you design a load balancer for a global application?

**Answer:**

**Multi-Layer Load Balancing Architecture:**

**1. DNS-Based Load Balancing:**
```python
# GeoDNS routing
class GeoDNSRouter:
    def __init__(self):
        self.regions = {
            'us-east': ['52.1.1.1', '52.1.1.2'],
            'us-west': ['54.2.2.1', '54.2.2.2'],
            'eu-west': ['35.3.3.1', '35.3.3.2'],
            'asia-pacific': ['13.4.4.1', '13.4.4.2']
        }
    
    def resolve(self, client_ip):
        region = self.get_closest_region(client_ip)
        return self.regions[region]
    
    def get_closest_region(self, client_ip):
        # Simplified geolocation logic
        if client_ip.startswith('192.168'):
            return 'us-east'
        # Add more sophisticated geolocation
        return 'us-east'
```

**2. Application Load Balancer:**
```yaml
# AWS ALB configuration
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

**3. Health Checks and Failover:**
```python
import asyncio
import aiohttp

class HealthChecker:
    def __init__(self, servers, check_interval=30):
        self.servers = servers
        self.healthy_servers = set(servers)
        self.check_interval = check_interval
    
    async def health_check(self, server):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{server}/health", timeout=5) as response:
                    return response.status == 200
        except:
            return False
    
    async def monitor_health(self):
        while True:
            tasks = [self.health_check(server) for server in self.servers]
            results = await asyncio.gather(*tasks)
            
            for server, is_healthy in zip(self.servers, results):
                if is_healthy:
                    self.healthy_servers.add(server)
                else:
                    self.healthy_servers.discard(server)
            
            await asyncio.sleep(self.check_interval)
    
    def get_healthy_servers(self):
        return list(self.healthy_servers)
```

**4. Session Affinity:**
```python
class StickySessionBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.session_map = {}
    
    def get_server(self, session_id):
        if session_id in self.session_map:
            return self.session_map[session_id]
        
        # Assign new session to least loaded server
        server = min(self.servers, key=lambda s: self.get_load(s))
        self.session_map[session_id] = server
        return server
    
    def get_load(self, server):
        return sum(1 for s in self.session_map.values() if s == server)
```

---

## Microservices Architecture

### 11. How do you design communication between microservices?

**Answer:**

**1. Synchronous Communication (REST/gRPC):**
```python
# REST API communication
import requests
import asyncio
import aiohttp

class UserService:
    def __init__(self, base_url):
        self.base_url = base_url
    
    async def get_user(self, user_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/users/{user_id}") as response:
                if response.status == 200:
                    return await response.json()
                return None
    
    async def create_user(self, user_data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/users", json=user_data) as response:
                return await response.json()

# Circuit breaker pattern
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            
            raise e
```

**2. Asynchronous Communication (Message Queues):**
```python
import asyncio
import aioamqp

class MessageBroker:
    def __init__(self, connection_url):
        self.connection_url = connection_url
        self.connection = None
        self.channel = None
    
    async def connect(self):
        self.connection = await aioamqp.connect(self.connection_url)
        self.channel = await self.connection.channel()
    
    async def publish(self, exchange, routing_key, message):
        await self.channel.publish(
            json.dumps(message),
            exchange_name=exchange,
            routing_key=routing_key
        )
    
    async def consume(self, queue_name, callback):
        await self.channel.queue_declare(queue_name=queue_name)
        await self.channel.basic_consume(callback, queue_name=queue_name)

# Event-driven architecture
class OrderService:
    def __init__(self, message_broker):
        self.broker = message_broker
    
    async def create_order(self, order_data):
        # Create order in database
        order = await self.save_order(order_data)
        
        # Publish order created event
        await self.broker.publish(
            exchange='orders',
            routing_key='order.created',
            message={
                'order_id': order['id'],
                'user_id': order['user_id'],
                'total_amount': order['total_amount'],
                'timestamp': datetime.now().isoformat()
            }
        )
        
        return order

class InventoryService:
    def __init__(self, message_broker):
        self.broker = message_broker
    
    async def handle_order_created(self, message):
        order_data = json.loads(message.body)
        
        # Reserve inventory
        await self.reserve_inventory(order_data['order_id'])
        
        # Publish inventory reserved event
        await self.broker.publish(
            exchange='inventory',
            routing_key='inventory.reserved',
            message={
                'order_id': order_data['order_id'],
                'status': 'reserved'
            }
        )
```

**3. Service Discovery:**
```python
import consul

class ServiceRegistry:
    def __init__(self):
        self.consul = consul.Consul()
    
    def register_service(self, name, address, port, health_check_url):
        self.consul.agent.service.register(
            name=name,
            service_id=f"{name}-{address}-{port}",
            address=address,
            port=port,
            check=consul.Check.http(health_check_url, interval="10s")
        )
    
    def discover_service(self, service_name):
        services = self.consul.health.service(service_name, passing=True)[1]
        return [(s['Service']['Address'], s['Service']['Port']) for s in services]

# Usage
registry = ServiceRegistry()
registry.register_service(
    name='user-service',
    address='10.0.1.100',
    port=8080,
    health_check_url='http://10.0.1.100:8080/health'
)

# Discover services
user_service_instances = registry.discover_service('user-service')
```

---

## Data Pipeline Design

### 12. How do you design a real-time data processing pipeline?

**Answer:**

**Lambda Architecture:**
```python
# Batch Layer (Historical Data)
from pyspark.sql import SparkSession

class BatchProcessor:
    def __init__(self):
        self.spark = SparkSession.builder.appName("BatchProcessor").getOrCreate()
    
    def process_daily_batch(self, date):
        # Read data from data lake
        raw_data = self.spark.read.parquet(f"s3://data-lake/events/date={date}")
        
        # Process and aggregate
        aggregated = raw_data.groupBy("user_id", "event_type").count()
        
        # Write to batch views
        aggregated.write.mode("overwrite").parquet(f"s3://batch-views/date={date}")

# Speed Layer (Real-time Data)
import asyncio
from kafka import KafkaConsumer, KafkaProducer

class StreamProcessor:
    def __init__(self):
        self.consumer = KafkaConsumer('events', bootstrap_servers=['localhost:9092'])
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    
    async def process_stream(self):
        for message in self.consumer:
            event = json.loads(message.value)
            
            # Real-time processing
            processed_event = self.transform_event(event)
            
            # Update real-time views
            await self.update_realtime_view(processed_event)
            
            # Forward to downstream systems
            self.producer.send('processed_events', json.dumps(processed_event))
    
    def transform_event(self, event):
        # Add timestamp, enrich data, etc.
        event['processed_at'] = datetime.now().isoformat()
        return event

# Serving Layer
class ServingLayer:
    def __init__(self):
        self.batch_store = connect_to_batch_store()
        self.realtime_store = connect_to_realtime_store()
    
    def get_user_stats(self, user_id, start_date, end_date):
        # Get batch data (older than 1 hour)
        batch_data = self.batch_store.query(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date - timedelta(hours=1)
        )
        
        # Get real-time data (last 1 hour)
        realtime_data = self.realtime_store.query(
            user_id=user_id,
            start_time=end_date - timedelta(hours=1),
            end_time=end_date
        )
        
        # Merge results
        return self.merge_results(batch_data, realtime_data)
```

**Kappa Architecture (Stream-Only):**
```python
from kafka import KafkaConsumer
import redis

class KappaProcessor:
    def __init__(self):
        self.consumer = KafkaConsumer('events')
        self.state_store = redis.Redis()
        self.output_topic = KafkaProducer()
    
    def process_events(self):
        for message in self.consumer:
            event = json.loads(message.value)
            
            # Update state
            self.update_state(event)
            
            # Generate output
            result = self.compute_result(event)
            
            # Send to output topic
            self.output_topic.send('results', json.dumps(result))
    
    def update_state(self, event):
        key = f"user:{event['user_id']}:count"
        self.state_store.incr(key)
        self.state_store.expire(key, 86400)  # 24 hour TTL
    
    def compute_result(self, event):
        count = self.state_store.get(f"user:{event['user_id']}:count")
        return {
            'user_id': event['user_id'],
            'event_count': int(count or 0),
            'timestamp': datetime.now().isoformat()
        }
```

### 13. How do you ensure data quality in a large-scale data pipeline?

**Answer:**

**Data Quality Framework:**
```python
from great_expectations import DataContext
import pandas as pd

class DataQualityChecker:
    def __init__(self):
        self.context = DataContext()
    
    def validate_batch(self, df, expectation_suite_name):
        # Create batch
        batch = self.context.get_batch(
            {"dataset": df},
            expectation_suite_name
        )
        
        # Run validation
        results = self.context.run_validation_operator(
            "action_list_operator",
            assets_to_validate=[batch]
        )
        
        return results
    
    def create_expectations(self, df, table_name):
        # Automatic expectation generation
        suite = self.context.create_expectation_suite(
            expectation_suite_name=f"{table_name}_suite"
        )
        
        # Add expectations
        batch = self.context.get_batch({"dataset": df}, suite)
        
        # Column existence
        for column in df.columns:
            batch.expect_column_to_exist(column)
        
        # Null checks for critical columns
        critical_columns = ['id', 'timestamp', 'user_id']
        for column in critical_columns:
            if column in df.columns:
                batch.expect_column_values_to_not_be_null(column)
        
        # Data type checks
        for column, dtype in df.dtypes.items():
            if dtype == 'int64':
                batch.expect_column_values_to_be_of_type(column, 'int')
            elif dtype == 'float64':
                batch.expect_column_values_to_be_of_type(column, 'float')
        
        # Save suite
        batch.save_expectation_suite()

# Data profiling
class DataProfiler:
    def profile_dataset(self, df):
        profile = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'null_counts': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'duplicate_rows': df.duplicated().sum()
        }
        
        # Statistical summary for numeric columns
        numeric_columns = df.select_dtypes(include=['number']).columns
        for col in numeric_columns:
            profile[f'{col}_stats'] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'outliers': self.detect_outliers(df[col])
            }
        
        return profile
    
    def detect_outliers(self, series):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return ((series < lower_bound) | (series > upper_bound)).sum()

# Data lineage tracking
class DataLineageTracker:
    def __init__(self):
        self.lineage_graph = {}
    
    def track_transformation(self, input_datasets, output_dataset, transformation_info):
        self.lineage_graph[output_dataset] = {
            'inputs': input_datasets,
            'transformation': transformation_info,
            'timestamp': datetime.now().isoformat(),
            'schema': self.get_schema(output_dataset)
        }
    
    def get_upstream_dependencies(self, dataset):
        dependencies = []
        if dataset in self.lineage_graph:
            for input_dataset in self.lineage_graph[dataset]['inputs']:
                dependencies.append(input_dataset)
                dependencies.extend(self.get_upstream_dependencies(input_dataset))
        return list(set(dependencies))
    
    def get_downstream_dependencies(self, dataset):
        dependencies = []
        for output_dataset, info in self.lineage_graph.items():
            if dataset in info['inputs']:
                dependencies.append(output_dataset)
                dependencies.extend(self.get_downstream_dependencies(output_dataset))
        return list(set(dependencies))
```

---

## Summary

System design interviews require a structured approach combining:

1. **Requirements Analysis**: Clear understanding of functional and non-functional requirements
2. **Scalability Planning**: Horizontal scaling, load balancing, and caching strategies
3. **Database Design**: Appropriate data modeling and scaling techniques
4. **Architecture Patterns**: Microservices, event-driven architecture, and communication patterns
5. **Data Pipeline Design**: Real-time and batch processing architectures
6. **Quality Assurance**: Monitoring, testing, and data quality frameworks

Success depends on demonstrating trade-off analysis, scalability thinking, and practical implementation knowledge while maintaining focus on business requirements and constraints.