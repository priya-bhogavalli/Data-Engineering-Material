# Data Structures & Algorithms Big4 Interview Questions

## Google Interview Questions

### 1. Design a data structure for autocomplete with billions of queries
**Scenario**: Build an autocomplete system that handles billions of queries per day with sub-millisecond response times.

**Solution**:
```python
import heapq
from collections import defaultdict

class AutocompleteSystem:
    def __init__(self):
        self.trie = {}
        self.popularity = defaultdict(int)
        self.cache = {}  # LRU cache for hot queries
    
    def add_sentence(self, sentence, frequency):
        node = self.trie
        for char in sentence:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = frequency
        self.popularity[sentence] = frequency
    
    def search(self, prefix, k=10):
        if prefix in self.cache:
            return self.cache[prefix]
        
        # Find all sentences with prefix
        node = self.trie
        for char in prefix:
            if char not in node:
                return []
            node = node[char]
        
        # Get top k suggestions using heap
        suggestions = []
        self._dfs(node, prefix, suggestions)
        
        # Return top k by frequency
        result = heapq.nlargest(k, suggestions, key=lambda x: self.popularity[x])
        self.cache[prefix] = result
        return result
    
    def _dfs(self, node, prefix, suggestions):
        if '#' in node:
            suggestions.append(prefix)
        
        for char, child in node.items():
            if char != '#':
                self._dfs(child, prefix + char, suggestions)
```

### 2. Implement distributed consistent hashing for data partitioning
**Scenario**: Design a system to distribute data across multiple servers with minimal reshuffling when servers are added/removed.

**Solution**:
```python
import hashlib
import bisect

class ConsistentHash:
    def __init__(self, replicas=150):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_server(self, server):
        for i in range(self.replicas):
            virtual_key = self._hash(f"{server}:{i}")
            self.ring[virtual_key] = server
            bisect.insort(self.sorted_keys, virtual_key)
    
    def remove_server(self, server):
        for i in range(self.replicas):
            virtual_key = self._hash(f"{server}:{i}")
            if virtual_key in self.ring:
                del self.ring[virtual_key]
                self.sorted_keys.remove(virtual_key)
    
    def get_server(self, key):
        if not self.ring:
            return None
        
        hash_key = self._hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_key)
        
        if idx == len(self.sorted_keys):
            idx = 0
        
        return self.ring[self.sorted_keys[idx]]

# Usage for data partitioning
class DistributedDataStore:
    def __init__(self):
        self.hash_ring = ConsistentHash()
        self.servers = {}
    
    def add_server(self, server_id):
        self.hash_ring.add_server(server_id)
        self.servers[server_id] = {}
    
    def put(self, key, value):
        server = self.hash_ring.get_server(key)
        self.servers[server][key] = value
    
    def get(self, key):
        server = self.hash_ring.get_server(key)
        return self.servers[server].get(key)
```

## Amazon Interview Questions

### 3. Design a system to find top K frequent items in a data stream
**Scenario**: Process millions of items per second and maintain top K most frequent items in real-time.

**Solution**:
```python
import heapq
from collections import defaultdict

class TopKFrequent:
    def __init__(self, k):
        self.k = k
        self.count = defaultdict(int)
        self.min_heap = []  # (frequency, item)
        self.heap_set = set()
    
    def add(self, item):
        self.count[item] += 1
        freq = self.count[item]
        
        # If item already in heap, we need to update
        if item in self.heap_set:
            # Remove old entry (lazy deletion)
            self.heap_set.remove(item)
        
        # Add new entry
        heapq.heappush(self.min_heap, (freq, item))
        self.heap_set.add(item)
        
        # Maintain heap size
        while len(self.min_heap) > self.k:
            old_freq, old_item = heapq.heappop(self.min_heap)
            if old_item in self.heap_set and self.count[old_item] == old_freq:
                self.heap_set.remove(old_item)
    
    def get_top_k(self):
        # Clean up stale entries
        valid_items = []
        temp_heap = []
        
        while self.min_heap:
            freq, item = heapq.heappop(self.min_heap)
            if item in self.heap_set and self.count[item] == freq:
                valid_items.append((freq, item))
                temp_heap.append((freq, item))
        
        # Restore heap
        self.min_heap = temp_heap
        heapq.heapify(self.min_heap)
        
        return sorted(valid_items, reverse=True)

# Space-efficient version using Count-Min Sketch
class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
        self.hash_functions = [
            lambda x, i=i: hash(f"{x}_{i}") % width 
            for i in range(depth)
        ]
    
    def add(self, item):
        for i in range(self.depth):
            j = self.hash_functions[i](item)
            self.table[i][j] += 1
    
    def estimate(self, item):
        return min(
            self.table[i][self.hash_functions[i](item)] 
            for i in range(self.depth)
        )
```

### 4. Implement LRU Cache with O(1) operations
**Scenario**: Design a cache that supports get and put operations in O(1) time complexity.

**Solution**:
```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> node
        
        # Create dummy head and tail
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node):
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        """Remove an existing node."""
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node):
        """Move node to head (mark as recently used)."""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self):
        """Remove last node."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key):
        node = self.cache.get(key)
        
        if node:
            # Move to head (recently used)
            self._move_to_head(node)
            return node.val
        
        return -1
    
    def put(self, key, value):
        node = self.cache.get(key)
        
        if node:
            # Update existing node
            node.val = value
            self._move_to_head(node)
        else:
            # Add new node
            new_node = Node(key, value)
            
            if len(self.cache) >= self.capacity:
                # Remove LRU item
                tail = self._pop_tail()
                del self.cache[tail.key]
            
            self.cache[key] = new_node
            self._add_node(new_node)
```

## Microsoft Interview Questions

### 5. Design a data structure for range sum queries with updates
**Scenario**: Support range sum queries and single element updates efficiently.

**Solution**:
```python
class SegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (2 * self.n)
        
        # Build tree
        for i in range(self.n):
            self.tree[self.n + i] = nums[i]
        
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    
    def update(self, index, val):
        """Update value at index - O(log n)"""
        index += self.n
        self.tree[index] = val
        
        while index > 1:
            self.tree[index // 2] = (
                self.tree[index] + self.tree[index ^ 1]
            )
            index //= 2
    
    def range_sum(self, left, right):
        """Sum of elements in range [left, right) - O(log n)"""
        left += self.n
        right += self.n
        sum_val = 0
        
        while left < right:
            if left % 2 == 1:
                sum_val += self.tree[left]
                left += 1
            if right % 2 == 1:
                right -= 1
                sum_val += self.tree[right]
            
            left //= 2
            right //= 2
        
        return sum_val

# Alternative: Fenwick Tree (Binary Indexed Tree)
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, i, delta):
        """Add delta to element at index i - O(log n)"""
        i += 1  # 1-indexed
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)
    
    def prefix_sum(self, i):
        """Sum of elements from 0 to i - O(log n)"""
        i += 1  # 1-indexed
        result = 0
        while i > 0:
            result += self.tree[i]
            i -= i & (-i)
        return result
    
    def range_sum(self, left, right):
        """Sum of elements in range [left, right] - O(log n)"""
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)
```

### 6. Implement a thread-safe data structure for concurrent access
**Scenario**: Design a concurrent hash map that supports multiple readers and writers.

**Solution**:
```python
import threading
from collections import defaultdict

class ConcurrentHashMap:
    def __init__(self, num_buckets=16):
        self.num_buckets = num_buckets
        self.buckets = [defaultdict(lambda: None) for _ in range(num_buckets)]
        self.locks = [threading.RWLock() for _ in range(num_buckets)]
    
    def _hash(self, key):
        return hash(key) % self.num_buckets
    
    def put(self, key, value):
        bucket_idx = self._hash(key)
        with self.locks[bucket_idx].write_lock():
            self.buckets[bucket_idx][key] = value
    
    def get(self, key):
        bucket_idx = self._hash(key)
        with self.locks[bucket_idx].read_lock():
            return self.buckets[bucket_idx].get(key)
    
    def remove(self, key):
        bucket_idx = self._hash(key)
        with self.locks[bucket_idx].write_lock():
            if key in self.buckets[bucket_idx]:
                del self.buckets[bucket_idx][key]
                return True
            return False

# Read-Write Lock implementation
class RWLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.RLock())
        self._readers = 0
    
    def read_lock(self):
        return ReadLock(self)
    
    def write_lock(self):
        return WriteLock(self)

class ReadLock:
    def __init__(self, rw_lock):
        self.rw_lock = rw_lock
    
    def __enter__(self):
        with self.rw_lock._read_ready:
            self.rw_lock._readers += 1
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.rw_lock._read_ready:
            self.rw_lock._readers -= 1
            if self.rw_lock._readers == 0:
                self.rw_lock._read_ready.notifyAll()

class WriteLock:
    def __init__(self, rw_lock):
        self.rw_lock = rw_lock
    
    def __enter__(self):
        self.rw_lock._read_ready.acquire()
        while self.rw_lock._readers > 0:
            self.rw_lock._read_ready.wait()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rw_lock._read_ready.release()
```

## Meta Interview Questions

### 7. Design a data structure for social network friend suggestions
**Scenario**: Efficiently find mutual friends and suggest new connections.

**Solution**:
```python
from collections import defaultdict, deque

class SocialGraph:
    def __init__(self):
        self.graph = defaultdict(set)
        self.user_data = {}
    
    def add_user(self, user_id, user_info):
        self.user_data[user_id] = user_info
    
    def add_friendship(self, user1, user2):
        self.graph[user1].add(user2)
        self.graph[user2].add(user1)
    
    def get_mutual_friends(self, user1, user2):
        """Find mutual friends between two users - O(min(d1, d2))"""
        friends1 = self.graph[user1]
        friends2 = self.graph[user2]
        return friends1.intersection(friends2)
    
    def suggest_friends(self, user_id, max_suggestions=10):
        """Suggest friends based on mutual connections - O(d^2)"""
        if user_id not in self.graph:
            return []
        
        user_friends = self.graph[user_id]
        suggestions = defaultdict(int)
        
        # Count mutual friends for each potential friend
        for friend in user_friends:
            for friend_of_friend in self.graph[friend]:
                if (friend_of_friend != user_id and 
                    friend_of_friend not in user_friends):
                    suggestions[friend_of_friend] += 1
        
        # Sort by number of mutual friends
        sorted_suggestions = sorted(
            suggestions.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [user_id for user_id, count in sorted_suggestions[:max_suggestions]]
    
    def shortest_path(self, start, end):
        """Find shortest path between users - O(V + E)"""
        if start == end:
            return [start]
        
        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)
        
        while queue:
            user, path = queue.popleft()
            
            for friend in self.graph[user]:
                if friend == end:
                    return path + [friend]
                
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, path + [friend]))
        
        return None  # No connection found

# Advanced: Using MinHash for similarity
class MinHashSimilarity:
    def __init__(self, num_hashes=100):
        self.num_hashes = num_hashes
        self.hash_functions = [
            lambda x, a=i*2+1, b=i*3+1: (a * hash(x) + b) % (2**32)
            for i in range(num_hashes)
        ]
    
    def get_signature(self, user_interests):
        """Get MinHash signature for user interests."""
        signature = [float('inf')] * self.num_hashes
        
        for interest in user_interests:
            for i, hash_func in enumerate(self.hash_functions):
                hash_val = hash_func(interest)
                signature[i] = min(signature[i], hash_val)
        
        return signature
    
    def jaccard_similarity(self, sig1, sig2):
        """Estimate Jaccard similarity from signatures."""
        matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
        return matches / len(sig1)
```

### 8. Implement a time-series database with efficient range queries
**Scenario**: Store and query time-series data with high write throughput and fast range queries.

**Solution**:
```python
import bisect
from collections import defaultdict
import time

class TimeSeriesDB:
    def __init__(self):
        self.data = defaultdict(list)  # metric_name -> [(timestamp, value)]
        self.indexes = defaultdict(list)  # metric_name -> [timestamps]
    
    def put(self, metric_name, timestamp, value):
        """Insert time-series data point - O(log n)"""
        data_points = self.data[metric_name]
        timestamps = self.indexes[metric_name]
        
        # Find insertion point
        idx = bisect.bisect_left(timestamps, timestamp)
        
        if idx < len(timestamps) and timestamps[idx] == timestamp:
            # Update existing point
            data_points[idx] = (timestamp, value)
        else:
            # Insert new point
            timestamps.insert(idx, timestamp)
            data_points.insert(idx, (timestamp, value))
    
    def get_range(self, metric_name, start_time, end_time):
        """Get data points in time range - O(log n + k)"""
        if metric_name not in self.data:
            return []
        
        timestamps = self.indexes[metric_name]
        data_points = self.data[metric_name]
        
        # Find range boundaries
        start_idx = bisect.bisect_left(timestamps, start_time)
        end_idx = bisect.bisect_right(timestamps, end_time)
        
        return data_points[start_idx:end_idx]
    
    def aggregate(self, metric_name, start_time, end_time, agg_func):
        """Aggregate data in time range."""
        data_points = self.get_range(metric_name, start_time, end_time)
        
        if not data_points:
            return None
        
        values = [value for _, value in data_points]
        
        if agg_func == 'sum':
            return sum(values)
        elif agg_func == 'avg':
            return sum(values) / len(values)
        elif agg_func == 'min':
            return min(values)
        elif agg_func == 'max':
            return max(values)
        
        return None

# Optimized version with bucketing
class BucketedTimeSeriesDB:
    def __init__(self, bucket_size=3600):  # 1 hour buckets
        self.bucket_size = bucket_size
        self.buckets = defaultdict(lambda: defaultdict(list))
    
    def _get_bucket_key(self, timestamp):
        return timestamp // self.bucket_size
    
    def put(self, metric_name, timestamp, value):
        bucket_key = self._get_bucket_key(timestamp)
        self.buckets[bucket_key][metric_name].append((timestamp, value))
        
        # Keep bucket sorted
        self.buckets[bucket_key][metric_name].sort()
    
    def get_range(self, metric_name, start_time, end_time):
        start_bucket = self._get_bucket_key(start_time)
        end_bucket = self._get_bucket_key(end_time)
        
        result = []
        
        for bucket_key in range(start_bucket, end_bucket + 1):
            if bucket_key in self.buckets:
                bucket_data = self.buckets[bucket_key][metric_name]
                
                for timestamp, value in bucket_data:
                    if start_time <= timestamp <= end_time:
                        result.append((timestamp, value))
        
        return sorted(result)
```

These Big4 questions demonstrate advanced algorithmic thinking and system design skills required for senior data engineering positions.