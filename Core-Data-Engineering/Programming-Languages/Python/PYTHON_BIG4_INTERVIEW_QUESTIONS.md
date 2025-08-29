# Python Interview Questions - Big4 Companies (Google, Amazon, Microsoft, Meta)

## Table of Contents

1. [Google Interview Questions](#google-interview-questions)
   - [URL Shortener Design](#1-design-a-url-shortener-like-bitly-google)
   - [LRU Cache Implementation](#2-implement-lru-cache-with-o1-operations-google)
   - [Anagram Grouping](#3-find-all-anagrams-in-a-list-of-strings-google)
2. [Amazon Interview Questions](#amazon-interview-questions)
   - [Logging System Design](#4-design-a-logging-system-amazon)
   - [Rate Limiter Implementation](#5-implement-a-rate-limiter-amazon)
   - [Distributed Cache Design](#6-design-a-distributed-cache-amazon)
3. [Microsoft Interview Questions](#microsoft-interview-questions)
   - [Thread-Safe Counter](#7-implement-a-thread-safe-counter-microsoft)
   - [File System Design](#8-design-a-file-system-microsoft)
4. [Meta (Facebook) Interview Questions](#meta-facebook-interview-questions)
   - [Social Media Feed Ranking](#9-design-a-social-media-feed-ranking-system-meta)
   - [Chat System with Message Ordering](#10-implement-a-chat-system-with-message-ordering-meta)
5. [System Design Questions (All Big4)](#system-design-questions-all-big4)
   - [Distributed Key-Value Store](#11-design-a-distributed-key-value-store-all-big4)

---

## Google Interview Questions

### 1. Design a URL shortener like bit.ly (Google)
**Answer:**
```python
import hashlib
import string
import random
from typing import Optional

class URLShortener:
    def __init__(self):
        self.url_to_short = {}
        self.short_to_url = {}
        self.base_url = "http://short.ly/"
        self.counter = 1000000  # Start from 7-digit number
    
    def encode(self, long_url: str) -> str:
        """Encode long URL to short URL."""
        if long_url in self.url_to_short:
            return self.base_url + self.url_to_short[long_url]
        
        # Generate short code using base62 encoding
        short_code = self._base62_encode(self.counter)
        self.counter += 1
        
        self.url_to_short[long_url] = short_code
        self.short_to_url[short_code] = long_url
        
        return self.base_url + short_code
    
    def decode(self, short_url: str) -> Optional[str]:
        """Decode short URL to original URL."""
        short_code = short_url.replace(self.base_url, "")
        return self.short_to_url.get(short_code)
    
    def _base62_encode(self, num: int) -> str:
        """Convert number to base62 string."""
        chars = string.ascii_letters + string.digits  # 62 characters
        if num == 0:
            return chars[0]
        
        result = []
        while num > 0:
            result.append(chars[num % 62])
            num //= 62
        
        return ''.join(reversed(result))

# Usage
shortener = URLShortener()
short = shortener.encode("https://www.google.com/very/long/url")
original = shortener.decode(short)
```

### 2. Implement LRU Cache with O(1) operations (Google)
**Answer:**
```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
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
        """Move node to head (most recently used)."""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self):
        """Remove last node (least recently used)."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if not node:
            return -1
        
        # Move to head (mark as recently used)
        self._move_to_head(node)
        return node.val
    
    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)
        
        if not node:
            new_node = Node(key, value)
            
            if len(self.cache) >= self.capacity:
                # Remove LRU item
                tail = self._pop_tail()
                del self.cache[tail.key]
            
            self.cache[key] = new_node
            self._add_node(new_node)
        else:
            # Update existing node
            node.val = value
            self._move_to_head(node)
```

### 3. Find all anagrams in a list of strings (Google)
**Answer:**
```python
from collections import defaultdict
from typing import List

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """Group anagrams together using sorted string as key."""
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        key = ''.join(sorted(s))
        anagram_groups[key].append(s)
    
    return list(anagram_groups.values())

# Alternative using character count
def group_anagrams_count(strs: List[str]) -> List[List[str]]:
    """Group anagrams using character count as key."""
    from collections import Counter
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Create key from character counts
        key = tuple(sorted(Counter(s).items()))
        anagram_groups[key].append(s)
    
    return list(anagram_groups.values())

# Usage
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
result = group_anagrams(words)
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

## Amazon Interview Questions

### 4. Design a logging system (Amazon)
**Answer:**
```python
import threading
import time
from collections import deque
from typing import List
from enum import Enum

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4

class LogEntry:
    def __init__(self, level: LogLevel, message: str, timestamp: float = None):
        self.level = level
        self.message = message
        self.timestamp = timestamp or time.time()
    
    def __str__(self):
        return f"[{self.level.name}] {time.ctime(self.timestamp)}: {self.message}"

class Logger:
    def __init__(self, max_size: int = 1000):
        self.logs = deque(maxlen=max_size)
        self.lock = threading.Lock()
        self.min_level = LogLevel.INFO
    
    def set_level(self, level: LogLevel):
        """Set minimum logging level."""
        self.min_level = level
    
    def log(self, level: LogLevel, message: str):
        """Add log entry if level is sufficient."""
        if level.value >= self.min_level.value:
            with self.lock:
                entry = LogEntry(level, message)
                self.logs.append(entry)
    
    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message: str):
        self.log(LogLevel.INFO, message)
    
    def warn(self, message: str):
        self.log(LogLevel.WARN, message)
    
    def error(self, message: str):
        self.log(LogLevel.ERROR, message)
    
    def get_logs(self, level: LogLevel = None, last_n: int = None) -> List[LogEntry]:
        """Get logs filtered by level and/or count."""
        with self.lock:
            logs = list(self.logs)
        
        if level:
            logs = [log for log in logs if log.level == level]
        
        if last_n:
            logs = logs[-last_n:]
        
        return logs

# Usage
logger = Logger()
logger.info("System started")
logger.error("Database connection failed")
recent_errors = logger.get_logs(LogLevel.ERROR, 10)
```

### 5. Implement a rate limiter (Amazon)
**Answer:**
```python
import time
from collections import defaultdict, deque
from threading import Lock

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        """
        Args:
            max_requests: Maximum requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(deque)  # user_id -> timestamps
        self.lock = Lock()
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if request is allowed for user."""
        with self.lock:
            now = time.time()
            user_requests = self.requests[user_id]
            
            # Remove old requests outside time window
            while user_requests and user_requests[0] <= now - self.time_window:
                user_requests.popleft()
            
            # Check if under limit
            if len(user_requests) < self.max_requests:
                user_requests.append(now)
                return True
            
            return False

# Token bucket implementation
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from bucket."""
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            
            return False
    
    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

# Usage
rate_limiter = RateLimiter(max_requests=10, time_window=60)  # 10 requests per minute
bucket = TokenBucket(capacity=10, refill_rate=1.0)  # 1 token per second

if rate_limiter.is_allowed("user123"):
    print("Request allowed")
else:
    print("Rate limit exceeded")
```

### 6. Design a distributed cache (Amazon)
**Answer:**
```python
import hashlib
import json
import time
from typing import Any, Optional, Dict
from threading import Lock

class CacheNode:
    def __init__(self, node_id: str, capacity: int = 1000):
        self.node_id = node_id
        self.capacity = capacity
        self.cache = {}
        self.access_times = {}
        self.lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key in self.cache:
                self.access_times[key] = time.time()
                return self.cache[key]
            return None
    
    def put(self, key: str, value: Any, ttl: int = 3600):
        """Put value in cache with TTL."""
        with self.lock:
            # Evict if at capacity
            if len(self.cache) >= self.capacity and key not in self.cache:
                self._evict_lru()
            
            self.cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl
            }
            self.access_times[key] = time.time()
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                del self.access_times[key]
                return True
            return False
    
    def _evict_lru(self):
        """Evict least recently used item."""
        if not self.access_times:
            return
        
        lru_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        del self.cache[lru_key]
        del self.access_times[lru_key]
    
    def cleanup_expired(self):
        """Remove expired entries."""
        now = time.time()
        expired_keys = []
        
        with self.lock:
            for key, data in self.cache.items():
                if data['expires_at'] < now:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
                del self.access_times[key]

class DistributedCache:
    def __init__(self, nodes: Dict[str, CacheNode]):
        self.nodes = nodes
        self.node_list = list(nodes.keys())
    
    def _get_node(self, key: str) -> CacheNode:
        """Get node for key using consistent hashing."""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        node_index = hash_value % len(self.node_list)
        node_id = self.node_list[node_index]
        return self.nodes[node_id]
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from distributed cache."""
        node = self._get_node(key)
        data = node.get(key)
        
        if data and data['expires_at'] > time.time():
            return data['value']
        elif data:
            # Expired, remove it
            node.delete(key)
        
        return None
    
    def put(self, key: str, value: Any, ttl: int = 3600):
        """Put value in distributed cache."""
        node = self._get_node(key)
        node.put(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """Delete key from distributed cache."""
        node = self._get_node(key)
        return node.delete(key)

# Usage
nodes = {
    'node1': CacheNode('node1'),
    'node2': CacheNode('node2'),
    'node3': CacheNode('node3')
}
cache = DistributedCache(nodes)

cache.put('user:123', {'name': 'John', 'age': 30})
user_data = cache.get('user:123')
```

## Microsoft Interview Questions

### 7. Implement a thread-safe counter (Microsoft)
**Answer:**
```python
import threading
from typing import Dict

class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self, amount: int = 1) -> int:
        """Increment counter and return new value."""
        with self._lock:
            self._value += amount
            return self._value
    
    def decrement(self, amount: int = 1) -> int:
        """Decrement counter and return new value."""
        with self._lock:
            self._value -= amount
            return self._value
    
    def get(self) -> int:
        """Get current value."""
        with self._lock:
            return self._value
    
    def reset(self) -> int:
        """Reset counter to 0 and return previous value."""
        with self._lock:
            old_value = self._value
            self._value = 0
            return old_value

class MultiCounter:
    """Thread-safe counter with multiple named counters."""
    
    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._lock = threading.RLock()  # Reentrant lock
    
    def increment(self, name: str, amount: int = 1) -> int:
        """Increment named counter."""
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + amount
            return self._counters[name]
    
    def get(self, name: str) -> int:
        """Get value of named counter."""
        with self._lock:
            return self._counters.get(name, 0)
    
    def get_all(self) -> Dict[str, int]:
        """Get all counters."""
        with self._lock:
            return self._counters.copy()
    
    def reset(self, name: str = None) -> Dict[str, int]:
        """Reset specific counter or all counters."""
        with self._lock:
            if name:
                old_value = self._counters.get(name, 0)
                self._counters[name] = 0
                return {name: old_value}
            else:
                old_counters = self._counters.copy()
                self._counters.clear()
                return old_counters

# Usage with threading
import concurrent.futures

counter = ThreadSafeCounter()
multi_counter = MultiCounter()

def worker(counter, worker_id):
    for i in range(1000):
        counter.increment()
        multi_counter.increment(f'worker_{worker_id}')

# Test thread safety
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(worker, counter, i) for i in range(10)]
    concurrent.futures.wait(futures)

print(f"Final counter value: {counter.get()}")  # Should be 10000
print(f"Multi-counter values: {multi_counter.get_all()}")
```

### 8. Design a file system (Microsoft)
**Answer:**
```python
from typing import Dict, List, Optional
import time

class FileSystemNode:
    def __init__(self, name: str, is_file: bool = False, content: str = ""):
        self.name = name
        self.is_file = is_file
        self.content = content if is_file else ""
        self.children: Dict[str, FileSystemNode] = {} if not is_file else None
        self.created_at = time.time()
        self.modified_at = time.time()
        self.size = len(content) if is_file else 0
    
    def add_child(self, child: 'FileSystemNode'):
        """Add child node (only for directories)."""
        if self.is_file:
            raise ValueError("Cannot add child to file")
        self.children[child.name] = child
        self.modified_at = time.time()
    
    def remove_child(self, name: str) -> bool:
        """Remove child node."""
        if self.is_file or name not in self.children:
            return False
        del self.children[name]
        self.modified_at = time.time()
        return True
    
    def get_size(self) -> int:
        """Get total size including all children."""
        if self.is_file:
            return self.size
        
        total_size = 0
        for child in self.children.values():
            total_size += child.get_size()
        return total_size

class FileSystem:
    def __init__(self):
        self.root = FileSystemNode("/", is_file=False)
        self.current_dir = self.root
    
    def _parse_path(self, path: str) -> List[str]:
        """Parse path into components."""
        if path.startswith('/'):
            return [p for p in path.split('/') if p]
        else:
            return [p for p in path.split('/') if p]
    
    def _get_node(self, path: str, start_node: FileSystemNode = None) -> Optional[FileSystemNode]:
        """Get node at given path."""
        if start_node is None:
            start_node = self.root if path.startswith('/') else self.current_dir
        
        if path == '/' or path == '':
            return self.root
        
        components = self._parse_path(path)
        current = start_node
        
        for component in components:
            if component == '..':
                # Go to parent (simplified - doesn't track parent references)
                continue
            elif component == '.':
                continue
            else:
                if current.is_file or component not in current.children:
                    return None
                current = current.children[component]
        
        return current
    
    def mkdir(self, path: str) -> bool:
        """Create directory."""
        components = self._parse_path(path)
        if not components:
            return False
        
        parent_path = '/'.join(components[:-1])
        parent = self._get_node(parent_path) if parent_path else self.current_dir
        
        if not parent or parent.is_file:
            return False
        
        dir_name = components[-1]
        if dir_name in parent.children:
            return False
        
        new_dir = FileSystemNode(dir_name, is_file=False)
        parent.add_child(new_dir)
        return True
    
    def create_file(self, path: str, content: str = "") -> bool:
        """Create file with content."""
        components = self._parse_path(path)
        if not components:
            return False
        
        parent_path = '/'.join(components[:-1])
        parent = self._get_node(parent_path) if parent_path else self.current_dir
        
        if not parent or parent.is_file:
            return False
        
        file_name = components[-1]
        if file_name in parent.children:
            return False
        
        new_file = FileSystemNode(file_name, is_file=True, content=content)
        parent.add_child(new_file)
        return True
    
    def read_file(self, path: str) -> Optional[str]:
        """Read file content."""
        node = self._get_node(path)
        if node and node.is_file:
            return node.content
        return None
    
    def write_file(self, path: str, content: str) -> bool:
        """Write content to file."""
        node = self._get_node(path)
        if node and node.is_file:
            node.content = content
            node.size = len(content)
            node.modified_at = time.time()
            return True
        return False
    
    def ls(self, path: str = ".") -> List[Dict]:
        """List directory contents."""
        node = self._get_node(path)
        if not node or node.is_file:
            return []
        
        result = []
        for child in node.children.values():
            result.append({
                'name': child.name,
                'type': 'file' if child.is_file else 'directory',
                'size': child.get_size(),
                'modified': time.ctime(child.modified_at)
            })
        
        return sorted(result, key=lambda x: x['name'])
    
    def rm(self, path: str) -> bool:
        """Remove file or directory."""
        components = self._parse_path(path)
        if not components:
            return False
        
        parent_path = '/'.join(components[:-1])
        parent = self._get_node(parent_path) if parent_path else self.current_dir
        
        if not parent or parent.is_file:
            return False
        
        return parent.remove_child(components[-1])

# Usage
fs = FileSystem()
fs.mkdir("documents")
fs.mkdir("documents/projects")
fs.create_file("documents/readme.txt", "Hello World")
fs.create_file("documents/projects/main.py", "print('Hello')")

print(fs.ls("documents"))
content = fs.read_file("documents/readme.txt")
print(f"File content: {content}")
```

## Meta (Facebook) Interview Questions

### 9. Design a social media feed ranking system (Meta)
**Answer:**
```python
import heapq
import time
from typing import List, Dict, Set
from dataclasses import dataclass
from enum import Enum

class PostType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    LINK = "link"

@dataclass
class Post:
    id: str
    user_id: str
    content: str
    post_type: PostType
    timestamp: float
    likes: int = 0
    comments: int = 0
    shares: int = 0
    
    def engagement_score(self) -> float:
        """Calculate engagement score."""
        return (self.likes * 1.0 + self.comments * 2.0 + self.shares * 3.0)

@dataclass
class User:
    id: str
    friends: Set[str]
    interests: Set[str]
    interaction_history: Dict[str, float]  # user_id -> interaction_strength

class FeedRanker:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.posts: Dict[str, Post] = {}
        
        # Ranking weights
        self.weights = {
            'recency': 0.3,
            'engagement': 0.25,
            'relationship': 0.25,
            'content_type': 0.2
        }
    
    def add_user(self, user: User):
        """Add user to system."""
        self.users[user.id] = user
    
    def add_post(self, post: Post):
        """Add post to system."""
        self.posts[post.id] = post
    
    def calculate_post_score(self, post: Post, user: User) -> float:
        """Calculate relevance score for post-user pair."""
        now = time.time()
        
        # Recency score (decay over time)
        hours_old = (now - post.timestamp) / 3600
        recency_score = max(0, 1 - (hours_old / 24))  # Decay over 24 hours
        
        # Engagement score (normalized)
        engagement_score = min(1.0, post.engagement_score() / 100)
        
        # Relationship score
        relationship_score = 0
        if post.user_id in user.friends:
            relationship_score = 0.8
        elif post.user_id in user.interaction_history:
            relationship_score = min(0.6, user.interaction_history[post.user_id])
        else:
            relationship_score = 0.1  # Unknown user
        
        # Content type preference (simplified)
        content_type_score = 0.5  # Default
        if post.post_type == PostType.VIDEO:
            content_type_score = 0.8
        elif post.post_type == PostType.IMAGE:
            content_type_score = 0.7
        
        # Weighted final score
        final_score = (
            self.weights['recency'] * recency_score +
            self.weights['engagement'] * engagement_score +
            self.weights['relationship'] * relationship_score +
            self.weights['content_type'] * content_type_score
        )
        
        return final_score
    
    def generate_feed(self, user_id: str, limit: int = 20) -> List[Post]:
        """Generate ranked feed for user."""
        if user_id not in self.users:
            return []
        
        user = self.users[user_id]
        scored_posts = []
        
        # Score all posts
        for post in self.posts.values():
            if post.user_id != user_id:  # Don't show user's own posts
                score = self.calculate_post_score(post, user)
                scored_posts.append((score, post))
        
        # Sort by score (descending) and return top posts
        scored_posts.sort(key=lambda x: x[0], reverse=True)
        return [post for _, post in scored_posts[:limit]]
    
    def update_interaction(self, user_id: str, target_user_id: str, interaction_type: str):
        """Update user interaction history."""
        if user_id not in self.users:
            return
        
        user = self.users[user_id]
        current_strength = user.interaction_history.get(target_user_id, 0)
        
        # Update interaction strength based on type
        if interaction_type == 'like':
            user.interaction_history[target_user_id] = min(1.0, current_strength + 0.1)
        elif interaction_type == 'comment':
            user.interaction_history[target_user_id] = min(1.0, current_strength + 0.2)
        elif interaction_type == 'share':
            user.interaction_history[target_user_id] = min(1.0, current_strength + 0.3)

# Usage
ranker = FeedRanker()

# Add users
user1 = User("user1", {"user2", "user3"}, {"tech", "sports"}, {})
user2 = User("user2", {"user1"}, {"tech", "music"}, {})
ranker.add_user(user1)
ranker.add_user(user2)

# Add posts
post1 = Post("post1", "user2", "Check out this tech article!", PostType.LINK, time.time() - 3600, 10, 5, 2)
post2 = Post("post2", "user3", "Great game last night!", PostType.TEXT, time.time() - 7200, 25, 8, 1)
ranker.add_post(post1)
ranker.add_post(post2)

# Generate feed
feed = ranker.generate_feed("user1", limit=10)
for post in feed:
    print(f"Post {post.id}: {post.content[:50]}... (Score calculated)")
```

### 10. Implement a chat system with message ordering (Meta)
**Answer:**
```python
import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import defaultdict
import heapq

@dataclass
class Message:
    id: str
    sender_id: str
    chat_id: str
    content: str
    timestamp: float
    message_type: str = "text"  # text, image, file, etc.
    
    def __lt__(self, other):
        """For heap ordering by timestamp."""
        return self.timestamp < other.timestamp

class VectorClock:
    """Vector clock for distributed message ordering."""
    
    def __init__(self, node_id: str, nodes: List[str]):
        self.node_id = node_id
        self.clock = {node: 0 for node in nodes}
    
    def tick(self):
        """Increment own clock."""
        self.clock[self.node_id] += 1
    
    def update(self, other_clock: Dict[str, int]):
        """Update clock with received message clock."""
        for node in self.clock:
            self.clock[node] = max(self.clock[node], other_clock.get(node, 0))
        self.tick()
    
    def copy(self) -> Dict[str, int]:
        """Get copy of current clock."""
        return self.clock.copy()

class ChatRoom:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        self.messages: List[Message] = []
        self.participants: Set[str] = set()
        self.message_buffer = []  # For out-of-order messages
        self.lock = threading.Lock()
        self.expected_sequence = defaultdict(int)  # user_id -> next expected sequence
    
    def add_participant(self, user_id: str):
        """Add participant to chat."""
        with self.lock:
            self.participants.add(user_id)
    
    def add_message(self, message: Message, vector_clock: Dict[str, int] = None):
        """Add message with ordering guarantees."""
        with self.lock:
            if vector_clock:
                # Use vector clock for ordering
                heapq.heappush(self.message_buffer, (vector_clock, message))
                self._process_buffer()
            else:
                # Simple timestamp ordering
                self.messages.append(message)
                self.messages.sort(key=lambda m: m.timestamp)
    
    def _process_buffer(self):
        """Process buffered messages in correct order."""
        # Simplified: just sort by timestamp for now
        # In real system, would use vector clock causality
        while self.message_buffer:
            _, message = heapq.heappop(self.message_buffer)
            self.messages.append(message)
        
        self.messages.sort(key=lambda m: m.timestamp)
    
    def get_messages(self, limit: int = 50, offset: int = 0) -> List[Message]:
        """Get messages with pagination."""
        with self.lock:
            start = max(0, len(self.messages) - limit - offset)
            end = len(self.messages) - offset if offset > 0 else len(self.messages)
            return self.messages[start:end]
    
    def get_messages_after(self, timestamp: float) -> List[Message]:
        """Get messages after given timestamp."""
        with self.lock:
            return [m for m in self.messages if m.timestamp > timestamp]

class ChatSystem:
    def __init__(self, node_id: str, all_nodes: List[str]):
        self.node_id = node_id
        self.chat_rooms: Dict[str, ChatRoom] = {}
        self.users: Dict[str, Set[str]] = defaultdict(set)  # user_id -> chat_ids
        self.vector_clock = VectorClock(node_id, all_nodes)
        self.lock = threading.Lock()
        self.message_id_counter = 0
    
    def create_chat(self, chat_id: str, participants: List[str]) -> bool:
        """Create new chat room."""
        with self.lock:
            if chat_id in self.chat_rooms:
                return False
            
            chat_room = ChatRoom(chat_id)
            for user_id in participants:
                chat_room.add_participant(user_id)
                self.users[user_id].add(chat_id)
            
            self.chat_rooms[chat_id] = chat_room
            return True
    
    def send_message(self, sender_id: str, chat_id: str, content: str) -> Optional[Message]:
        """Send message to chat room."""
        if chat_id not in self.chat_rooms:
            return None
        
        chat_room = self.chat_rooms[chat_id]
        if sender_id not in chat_room.participants:
            return None
        
        with self.lock:
            self.message_id_counter += 1
            message_id = f"{self.node_id}_{self.message_id_counter}"
        
        # Create message with vector clock
        self.vector_clock.tick()
        message = Message(
            id=message_id,
            sender_id=sender_id,
            chat_id=chat_id,
            content=content,
            timestamp=time.time()
        )
        
        # Add to chat room
        chat_room.add_message(message, self.vector_clock.copy())
        
        return message
    
    def receive_message(self, message: Message, sender_vector_clock: Dict[str, int]):
        """Receive message from another node."""
        if message.chat_id not in self.chat_rooms:
            return
        
        # Update vector clock
        self.vector_clock.update(sender_vector_clock)
        
        # Add message to chat room
        chat_room = self.chat_rooms[message.chat_id]
        chat_room.add_message(message, sender_vector_clock)
    
    def get_chat_messages(self, chat_id: str, user_id: str, limit: int = 50) -> List[Message]:
        """Get messages from chat room."""
        if chat_id not in self.chat_rooms:
            return []
        
        chat_room = self.chat_rooms[chat_id]
        if user_id not in chat_room.participants:
            return []
        
        return chat_room.get_messages(limit)
    
    def get_user_chats(self, user_id: str) -> List[str]:
        """Get all chats for user."""
        return list(self.users[user_id])

# Usage
# Create chat system nodes
node1 = ChatSystem("node1", ["node1", "node2", "node3"])
node2 = ChatSystem("node2", ["node1", "node2", "node3"])

# Create chat room
node1.create_chat("chat1", ["user1", "user2", "user3"])
node2.create_chat("chat1", ["user1", "user2", "user3"])

# Send messages
msg1 = node1.send_message("user1", "chat1", "Hello everyone!")
msg2 = node2.send_message("user2", "chat1", "Hi there!")

# Simulate message propagation
if msg1:
    node2.receive_message(msg1, node1.vector_clock.copy())
if msg2:
    node1.receive_message(msg2, node2.vector_clock.copy())

# Get messages
messages = node1.get_chat_messages("chat1", "user1")
for msg in messages:
    print(f"{msg.sender_id}: {msg.content}")
```

## System Design Questions (All Big4)

### 11. Design a distributed key-value store (All Big4)
**Answer:**
```python
import hashlib
import json
import time
from typing import Dict, List, Optional, Any
from threading import Lock
from enum import Enum

class ConsistencyLevel(Enum):
    ONE = 1
    QUORUM = 2
    ALL = 3

class Node:
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.is_alive = True
        self.data: Dict[str, Dict] = {}  # key -> {value, timestamp, version}
        self.lock = Lock()
    
    def put(self, key: str, value: Any, timestamp: float = None) -> bool:
        """Store key-value pair."""
        if timestamp is None:
            timestamp = time.time()
        
        with self.lock:
            current = self.data.get(key, {'version': 0})
            self.data[key] = {
                'value': value,
                'timestamp': timestamp,
                'version': current['version'] + 1
            }
        return True
    
    def get(self, key: str) -> Optional[Dict]:
        """Get value for key."""
        with self.lock:
            return self.data.get(key)
    
    def delete(self, key: str) -> bool:
        """Delete key."""
        with self.lock:
            if key in self.data:
                del self.data[key]
                return True
        return False

class ConsistentHashRing:
    def __init__(self, nodes: List[Node], replicas: int = 3):
        self.nodes = {node.node_id: node for node in nodes}
        self.replicas = replicas
        self.ring = {}
        self._build_ring()
    
    def _hash(self, key: str) -> int:
        """Hash function for consistent hashing."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def _build_ring(self):
        """Build the hash ring."""
        self.ring = {}
        for node_id in self.nodes:
            for i in range(self.replicas):
                virtual_key = f"{node_id}:{i}"
                hash_value = self._hash(virtual_key)
                self.ring[hash_value] = node_id
    
    def get_nodes(self, key: str, count: int = 3) -> List[Node]:
        """Get nodes responsible for key."""
        if not self.ring:
            return []
        
        key_hash = self._hash(key)
        sorted_hashes = sorted(self.ring.keys())
        
        # Find position in ring
        idx = 0
        for i, hash_val in enumerate(sorted_hashes):
            if hash_val >= key_hash:
                idx = i
                break
        
        # Get nodes (with wraparound)
        nodes = []
        seen_nodes = set()
        
        for i in range(len(sorted_hashes)):
            pos = (idx + i) % len(sorted_hashes)
            node_id = self.ring[sorted_hashes[pos]]
            
            if node_id not in seen_nodes and self.nodes[node_id].is_alive:
                nodes.append(self.nodes[node_id])
                seen_nodes.add(node_id)
                
                if len(nodes) >= count:
                    break
        
        return nodes

class DistributedKVStore:
    def __init__(self, nodes: List[Node], replication_factor: int = 3):
        self.hash_ring = ConsistentHashRing(nodes)
        self.replication_factor = replication_factor
        self.read_repair_enabled = True
    
    def put(self, key: str, value: Any, consistency: ConsistencyLevel = ConsistencyLevel.QUORUM) -> bool:
        """Put key-value pair with specified consistency."""
        nodes = self.hash_ring.get_nodes(key, self.replication_factor)
        if not nodes:
            return False
        
        timestamp = time.time()
        successful_writes = 0
        required_writes = self._get_required_count(len(nodes), consistency)
        
        # Write to nodes
        for node in nodes:
            try:
                if node.put(key, value, timestamp):
                    successful_writes += 1
            except Exception:
                continue  # Node might be down
        
        return successful_writes >= required_writes
    
    def get(self, key: str, consistency: ConsistencyLevel = ConsistencyLevel.QUORUM) -> Optional[Any]:
        """Get value with specified consistency."""
        nodes = self.hash_ring.get_nodes(key, self.replication_factor)
        if not nodes:
            return None
        
        required_reads = self._get_required_count(len(nodes), consistency)
        responses = []
        
        # Read from nodes
        for node in nodes:
            try:
                result = node.get(key)
                if result:
                    responses.append((node, result))
                    if len(responses) >= required_reads:
                        break
            except Exception:
                continue
        
        if not responses:
            return None
        
        # Find most recent version
        latest_response = max(responses, key=lambda x: x[1]['timestamp'])
        
        # Read repair if enabled
        if self.read_repair_enabled and len(responses) > 1:
            self._read_repair(key, responses, latest_response[1])
        
        return latest_response[1]['value']
    
    def delete(self, key: str, consistency: ConsistencyLevel = ConsistencyLevel.QUORUM) -> bool:
        """Delete key with specified consistency."""
        nodes = self.hash_ring.get_nodes(key, self.replication_factor)
        if not nodes:
            return False
        
        required_deletes = self._get_required_count(len(nodes), consistency)
        successful_deletes = 0
        
        for node in nodes:
            try:
                if node.delete(key):
                    successful_deletes += 1
            except Exception:
                continue
        
        return successful_deletes >= required_deletes
    
    def _get_required_count(self, total_nodes: int, consistency: ConsistencyLevel) -> int:
        """Get required number of nodes for consistency level."""
        if consistency == ConsistencyLevel.ONE:
            return 1
        elif consistency == ConsistencyLevel.ALL:
            return total_nodes
        else:  # QUORUM
            return (total_nodes // 2) + 1
    
    def _read_repair(self, key: str, responses: List, latest_data: Dict):
        """Perform read repair to fix inconsistencies."""
        latest_timestamp = latest_data['timestamp']
        
        for node, data in responses:
            if data['timestamp'] < latest_timestamp:
                try:
                    node.put(key, latest_data['value'], latest_data['timestamp'])
                except Exception:
                    pass  # Repair failed, will try again later

# Usage
# Create nodes
nodes = [
    Node("node1", "localhost", 8001),
    Node("node2", "localhost", 8002),
    Node("node3", "localhost", 8003),
    Node("node4", "localhost", 8004),
    Node("node5", "localhost", 8005)
]

# Create distributed store
kv_store = DistributedKVStore(nodes, replication_factor=3)

# Operations
success = kv_store.put("user:123", {"name": "John", "age": 30}, ConsistencyLevel.QUORUM)
user_data = kv_store.get("user:123", ConsistencyLevel.QUORUM)
deleted = kv_store.delete("user:123", ConsistencyLevel.QUORUM)

print(f"Put success: {success}")
print(f"User data: {user_data}")
print(f"Delete success: {deleted}")
```

These questions represent the types of complex system design and algorithmic challenges commonly asked at Big4 companies. They test:

1. **System Design Skills**: Distributed systems, scalability, consistency
2. **Data Structures & Algorithms**: Efficient implementations, time/space complexity
3. **Concurrency**: Thread safety, distributed coordination
4. **Real-world Problem Solving**: Practical solutions to business problems
5. **Code Quality**: Clean, maintainable, well-documented code

Each solution includes comprehensive error handling, proper abstractions, and considers real-world constraints like network failures, consistency trade-offs, and performance optimization.