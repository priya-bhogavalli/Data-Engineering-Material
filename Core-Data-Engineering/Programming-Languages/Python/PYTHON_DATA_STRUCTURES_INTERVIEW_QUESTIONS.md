# Python Data Structures Interview Questions

## Table of Contents

1. [Basic Data Structures](#basic-data-structures)
2. [Collections Module](#collections-module)
3. [Advanced Data Structures](#advanced-data-structures)
4. [Performance and Optimization](#performance-and-optimization)
5. [Real-World Scenarios](#real-world-scenarios)
6. [Coding Challenges](#coding-challenges)

---

## Basic Data Structures

### Q1: What are the key differences between lists and tuples in Python?

**Answer:**
Lists are mutable sequences that can be modified after creation, while tuples are immutable sequences that cannot be changed. Tuples are more memory-efficient and can be used as dictionary keys due to their immutability.

**Code Example:**
```python
# Lists - mutable, ordered
my_list = [1, 2, 3]
my_list.append(4)
my_list[0] = 10
print(f"Modified list: {my_list}")
# Output: [10, 2, 3, 4]

# Tuples - immutable, ordered
my_tuple = (1, 2, 3)
# my_tuple[0] = 10  # TypeError
print(f"Tuple: {my_tuple}")
# Output: (1, 2, 3)

# Memory comparison
import sys
list_data = [1, 2, 3, 4, 5]
tuple_data = (1, 2, 3, 4, 5)
print(f"List: {sys.getsizeof(list_data)} bytes")
print(f"Tuple: {sys.getsizeof(tuple_data)} bytes")
# Output: List: 104 bytes, Tuple: 80 bytes
```

**Key Points:**
- Lists: mutable, more methods (append, extend, remove)
- Tuples: immutable, memory efficient, hashable (can be dict keys)
- Use tuples for fixed data, lists for dynamic collections

### Q2: How do you efficiently remove duplicates from a list while preserving order?

**Answer:**
Use `dict.fromkeys()` for Python 3.7+ or manual tracking with a set. The dict method is faster due to C implementation.

**Code Example:**
```python
# Method 1: dict.fromkeys() (Python 3.7+)
def remove_duplicates_dict(lst):
    return list(dict.fromkeys(lst))

# Method 2: Set tracking
def remove_duplicates_set(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Test
original = [1, 2, 3, 2, 4, 1, 5]
print(f"Original: {original}")
print(f"Dict method: {remove_duplicates_dict(original)}")
print(f"Set method: {remove_duplicates_set(original)}")
# Output: [1, 2, 3, 4, 5]
```

### Q3: Explain shallow vs deep copy with examples.

**Answer:**
Shallow copy creates a new object but references nested objects. Deep copy creates independent copies of all nested objects.

**Code Example:**
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

# Modify nested element
original[0][0] = 'X'

print(f"Original: {original}")
print(f"Shallow: {shallow}")   # Affected!
print(f"Deep: {deep}")        # Not affected
# Output: Original: [['X', 2], [3, 4]]
# Output: Shallow: [['X', 2], [3, 4]]
# Output: Deep: [[1, 2], [3, 4]]
```

### Q4: What's the difference between `is` and `==` operators?

**Answer:**
`is` checks object identity (same memory location), `==` checks value equality.

**Code Example:**
```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"a == b: {a == b}")  # True (same values)
print(f"a is b: {a is b}")  # False (different objects)
print(f"a is c: {a is c}")  # True (same object)

# Small integers are cached
x = 256
y = 256
print(f"x is y: {x is y}")  # True (cached)

x = 257
y = 257
print(f"x is y: {x is y}")  # False (not cached)
```

### Q5: How do sets work internally and when should you use them?

**Answer:**
Sets use hash tables for O(1) average lookup, insertion, and deletion. Use for membership testing, removing duplicates, and set operations.

**Code Example:**
```python
# Set operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(f"Union: {set1 | set2}")
print(f"Intersection: {set1 & set2}")
print(f"Difference: {set1 - set2}")
print(f"Symmetric difference: {set1 ^ set2}")
# Output: Union: {1, 2, 3, 4, 5, 6}
# Output: Intersection: {3, 4}
# Output: Difference: {1, 2}
# Output: Symmetric difference: {1, 2, 5, 6}

# Performance comparison
import time
large_list = list(range(10000))
large_set = set(range(10000))

# List membership test
start = time.time()
9999 in large_list
list_time = time.time() - start

# Set membership test
start = time.time()
9999 in large_set
set_time = time.time() - start

print(f"List lookup: {list_time:.6f}s")
print(f"Set lookup: {set_time:.6f}s")
print(f"Set is {list_time/set_time:.0f}x faster")
```

## Collections Module

### Q6: When would you use Counter vs defaultdict vs regular dict?

**Answer:**
- **Counter**: Frequency counting and statistical operations
- **defaultdict**: Automatic initialization of missing keys
- **dict**: General key-value storage with explicit control

**Code Example:**
```python
from collections import Counter, defaultdict

# Counter for frequency analysis
text = "hello world"
char_count = Counter(text)
print(f"Most common: {char_count.most_common(3)}")
# Output: [('l', 3), ('o', 2), ('h', 1)]

# defaultdict for grouping
students = [("Alice", "Math"), ("Bob", "Science"), ("Alice", "English")]

# With defaultdict
subjects_dd = defaultdict(list)
for student, subject in students:
    subjects_dd[student].append(subject)

# With regular dict (more verbose)
subjects_dict = {}
for student, subject in students:
    if student not in subjects_dict:
        subjects_dict[student] = []
    subjects_dict[student].append(subject)

print(f"defaultdict: {dict(subjects_dd)}")
print(f"regular dict: {subjects_dict}")
# Both output: {'Alice': ['Math', 'English'], 'Bob': ['Science']}
```

### Q7: Implement an LRU cache using OrderedDict.

**Answer:**
LRU cache evicts least recently used items when capacity is exceeded. OrderedDict provides O(1) operations with `move_to_end()`.

**Code Example:**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)  # Mark as recently used
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Remove oldest
        self.cache[key] = value

# Test
lru = LRUCache(2)
lru.put(1, "one")
lru.put(2, "two")
print(lru.get(1))      # "one"
lru.put(3, "three")   # Evicts key 2
print(lru.get(2))      # -1 (not found)
print(lru.get(3))      # "three"
```

### Q8: What is namedtuple and when should you use it?

**Answer:**
namedtuple creates tuple subclasses with named fields. Use for lightweight, immutable data structures with field access by name.

**Code Example:**
```python
from collections import namedtuple

# Define Point namedtuple
Point = namedtuple('Point', ['x', 'y'])

# Create instances
p1 = Point(1, 2)
p2 = Point(x=3, y=4)

print(f"p1: {p1}")
print(f"p1.x: {p1.x}, p1.y: {p1.y}")
print(f"p1[0]: {p1[0]}")  # Still works like tuple

# Immutable
# p1.x = 5  # AttributeError

# Methods
print(f"p1._asdict(): {p1._asdict()}")
print(f"p1._replace(x=10): {p1._replace(x=10)}")

# Memory efficient compared to class
import sys
class RegularPoint:
    def __init__(self, x, y):
        self.x, self.y = x, y

regular = RegularPoint(1, 2)
named = Point(1, 2)

print(f"Regular class: {sys.getsizeof(regular.__dict__)} bytes")
print(f"namedtuple: {sys.getsizeof(named)} bytes")
```

## Advanced Data Structures

### Q9: Implement a priority queue using heapq.

**Answer:**
heapq implements a binary min-heap. For priority queues, use tuples where first element is priority (lower = higher priority).

**Code Example:**
```python
import heapq
from dataclasses import dataclass

@dataclass
class Task:
    priority: int
    name: str
    
    def __lt__(self, other):
        return self.priority < other.priority

class PriorityQueue:
    def __init__(self):
        self.heap = []
    
    def push(self, item, priority):
        heapq.heappush(self.heap, Task(priority, item))
    
    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)
        return None
    
    def peek(self):
        return self.heap[0] if self.heap else None

# Test
pq = PriorityQueue()
pq.push("Low priority", 3)
pq.push("High priority", 1)
pq.push("Medium priority", 2)

while pq.heap:
    task = pq.pop()
    print(f"{task.name} (priority: {task.priority})")
# Output: High priority (priority: 1)
# Output: Medium priority (priority: 2)
# Output: Low priority (priority: 3)
```

### Q10: Implement sliding window maximum using deque.

**Answer:**
Use deque to maintain indices of potential maximums in decreasing order. This achieves O(n) time complexity.

**Code Example:**
```python
from collections import deque

def sliding_window_maximum(nums, k):
    if not nums or k == 0:
        return []
    
    dq = deque()  # Store indices
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices with smaller values
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Test
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
result = sliding_window_maximum(nums, k)
print(f"Array: {nums}")
print(f"Window size: {k}")
print(f"Maximums: {result}")
# Output: [3, 3, 5, 5, 6, 7]
```

### Q11: Create a Trie for autocomplete functionality.

**Answer:**
Trie (prefix tree) stores strings character by character. Each node represents a character, paths form words.

**Code Example:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, freq=1):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += freq
    
    def search(self, word):
        node = self._find_node(word.lower())
        return node is not None and node.is_end
    
    def _find_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def get_suggestions(self, prefix, limit=5):
        node = self._find_node(prefix.lower())
        if not node:
            return []
        
        suggestions = []
        self._collect_words(node, prefix.lower(), suggestions)
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [word for word, freq in suggestions[:limit]]
    
    def _collect_words(self, node, prefix, suggestions):
        if node.is_end:
            suggestions.append((prefix, node.frequency))
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, suggestions)

# Test
trie = Trie()
words = [("python", 100), ("programming", 80), ("program", 60), 
         ("project", 70), ("problem", 50)]

for word, freq in words:
    trie.insert(word, freq)

print(f"Suggestions for 'pro': {trie.get_suggestions('pro')}")
# Output: ['programming', 'project', 'program', 'problem']
```

## Performance and Optimization

### Q12: Compare time complexity of operations on different data structures.

**Answer:**
Understanding time complexity helps choose the right data structure for specific operations.

**Code Example:**
```python
import time

def benchmark_operation(operation, iterations=10000):
    start = time.time()
    for _ in range(iterations):
        operation()
    return (time.time() - start) / iterations

# Test data
data_list = list(range(1000))
data_set = set(range(1000))
data_dict = {i: i for i in range(1000)}

# Search operations
search_item = 999

list_search = benchmark_operation(lambda: search_item in data_list)
set_search = benchmark_operation(lambda: search_item in data_set)
dict_search = benchmark_operation(lambda: search_item in data_dict)

print("Search Time Complexity:")
print(f"List (O(n)): {list_search:.8f}s")
print(f"Set (O(1)): {set_search:.8f}s")
print(f"Dict (O(1)): {dict_search:.8f}s")

# Insert operations
list_append = benchmark_operation(lambda: data_list.append(1001))
list_insert = benchmark_operation(lambda: data_list.insert(0, 1001))
set_add = benchmark_operation(lambda: data_set.add(1001))

print("\nInsert Time Complexity:")
print(f"List append (O(1)): {list_append:.8f}s")
print(f"List insert at start (O(n)): {list_insert:.8f}s")
print(f"Set add (O(1)): {set_add:.8f}s")
```

**Time Complexity Summary:**

| Operation | List | Set | Dict | Tuple |
|-----------|------|-----|------|-------|
| Access by index | O(1) | N/A | N/A | O(1) |
| Search | O(n) | O(1) | O(1) | O(n) |
| Insert at end | O(1) | O(1) | O(1) | N/A |
| Insert at start | O(n) | O(1) | O(1) | N/A |
| Delete | O(n) | O(1) | O(1) | N/A |

### Q13: How to optimize memory usage for large datasets?

**Answer:**
Use generators, arrays, slots, and chunked processing to reduce memory footprint.

**Code Example:**
```python
import sys
from array import array

# Memory comparison
regular_list = [i for i in range(100000)]
int_array = array('i', range(100000))
generator = (i for i in range(100000))

print("Memory Usage:")
print(f"List: {sys.getsizeof(regular_list):,} bytes")
print(f"Array: {sys.getsizeof(int_array):,} bytes")
print(f"Generator: {sys.getsizeof(generator):,} bytes")

# Using __slots__ for memory-efficient classes
class RegularClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedClass:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

regular = RegularClass(1, 2)
slotted = SlottedClass(1, 2)

print(f"\nClass Memory:")
print(f"Regular: {sys.getsizeof(regular.__dict__)} bytes")
print(f"Slotted: {sys.getsizeof(slotted)} bytes")

# Chunked processing for large datasets
def process_large_data(data_generator, chunk_size=1000):
    chunk = []
    for item in data_generator:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

# Example usage
for chunk in process_large_data(range(5500), 2000):
    print(f"Processing chunk of {len(chunk)} items")
# Output: Processing chunk of 2000 items
# Output: Processing chunk of 2000 items
# Output: Processing chunk of 1500 items
```

## Real-World Scenarios

### Q14: Design a data structure for real-time analytics.

**Answer:**
Combine multiple data structures for different access patterns: deque for time windows, defaultdict for grouping, Counter for aggregations.

**Code Example:**
```python
from collections import defaultdict, deque, Counter
import time
import threading

class RealTimeAnalytics:
    def __init__(self, window_minutes=60):
        self.window_size = window_minutes * 60
        self.events = deque()
        self.user_sessions = defaultdict(lambda: {
            'events': deque(),
            'first_seen': None,
            'last_seen': None
        })
        self.event_counts = Counter()
        self.lock = threading.Lock()
    
    def add_event(self, user_id, event_type, data=None):
        timestamp = time.time()
        event = {
            'user_id': user_id,
            'event_type': event_type,
            'timestamp': timestamp,
            'data': data or {}
        }
        
        with self.lock:
            self.events.append((timestamp, event))
            
            # Update user session
            session = self.user_sessions[user_id]
            session['events'].append(event)
            if session['first_seen'] is None:
                session['first_seen'] = timestamp
            session['last_seen'] = timestamp
            
            self.event_counts[event_type] += 1
            self._cleanup_old_data(timestamp)
    
    def _cleanup_old_data(self, current_time):
        cutoff = current_time - self.window_size
        
        # Clean main events
        while self.events and self.events[0][0] < cutoff:
            self.events.popleft()
        
        # Clean user sessions
        for user_id, session in list(self.user_sessions.items()):
            while session['events'] and session['events'][0]['timestamp'] < cutoff:
                session['events'].popleft()
            if not session['events']:
                del self.user_sessions[user_id]
    
    def get_stats(self):
        with self.lock:
            return {
                'active_users': len(self.user_sessions),
                'total_events': len(self.events),
                'event_types': dict(self.event_counts)
            }

# Test
analytics = RealTimeAnalytics(window_minutes=5)

events = [
    ("user1", "page_view", {"page": "home"}),
    ("user1", "click", {"button": "signup"}),
    ("user2", "page_view", {"page": "products"}),
    ("user1", "signup", {"method": "email"})
]

for user_id, event_type, data in events:
    analytics.add_event(user_id, event_type, data)

print(analytics.get_stats())
# Output: {'active_users': 2, 'total_events': 4, 'event_types': {'page_view': 2, 'click': 1, 'signup': 1}}
```

## Coding Challenges

### Q15: Implement a data structure supporting insert, delete, and getRandom in O(1).

**Answer:**
Use array for storage and hash map for index tracking. Swap with last element for O(1) deletion.

**Code Example:**
```python
import random

class RandomizedSet:
    def __init__(self):
        self.data = []
        self.indices = {}
    
    def insert(self, val):
        if val in self.indices:
            return False
        
        self.indices[val] = len(self.data)
        self.data.append(val)
        return True
    
    def remove(self, val):
        if val not in self.indices:
            return False
        
        # Swap with last element
        index = self.indices[val]
        last_val = self.data[-1]
        
        self.data[index] = last_val
        self.indices[last_val] = index
        
        # Remove last element
        self.data.pop()
        del self.indices[val]
        return True
    
    def getRandom(self):
        return random.choice(self.data) if self.data else None

# Test
rs = RandomizedSet()
print(rs.insert(1))    # True
print(rs.insert(2))    # True
print(rs.insert(1))    # False (already exists)
print(rs.remove(1))    # True
print(rs.getRandom())  # 2 (only element left)
```

### Q16: Design a cache with TTL (Time To Live) functionality.

**Answer:**
Combine dictionary for storage with heap for TTL tracking. Clean expired entries lazily or with background cleanup.

**Code Example:**
```python
import time
import heapq
from threading import Lock

class TTLCache:
    def __init__(self, default_ttl=300):
        self.cache = {}
        self.expiry_heap = []  # (expiry_time, key)
        self.default_ttl = default_ttl
        self.lock = Lock()
    
    def put(self, key, value, ttl=None):
        ttl = ttl or self.default_ttl
        expiry_time = time.time() + ttl
        
        with self.lock:
            self.cache[key] = (value, expiry_time)
            heapq.heappush(self.expiry_heap, (expiry_time, key))
            self._cleanup_expired()
    
    def get(self, key):
        with self.lock:
            self._cleanup_expired()
            if key in self.cache:
                value, expiry_time = self.cache[key]
                if time.time() < expiry_time:
                    return value
                else:
                    del self.cache[key]
            return None
    
    def _cleanup_expired(self):
        current_time = time.time()
        while self.expiry_heap and self.expiry_heap[0][0] <= current_time:
            expiry_time, key = heapq.heappop(self.expiry_heap)
            if key in self.cache:
                stored_expiry = self.cache[key][1]
                if stored_expiry <= current_time:
                    del self.cache[key]
    
    def size(self):
        with self.lock:
            self._cleanup_expired()
            return len(self.cache)

# Test
cache = TTLCache(default_ttl=2)
cache.put("key1", "value1", ttl=1)
cache.put("key2", "value2", ttl=3)

print(f"Immediate: {cache.get('key1')}")  # value1
time.sleep(1.5)
print(f"After 1.5s: {cache.get('key1')}")  # None (expired)
print(f"After 1.5s: {cache.get('key2')}")  # value2 (still valid)
```

---

## Summary

This comprehensive guide covers essential Python data structures concepts for data engineering interviews:

**Key Takeaways:**
1. **Choose the right structure**: Lists for ordered mutable data, sets for uniqueness, dicts for key-value mapping
2. **Understand time complexity**: O(1) for hash-based operations, O(n) for linear searches
3. **Memory optimization**: Use generators, arrays, and slots for large datasets
4. **Collections module**: Leverage Counter, defaultdict, OrderedDict for specialized use cases
5. **Advanced structures**: Implement heaps, tries, and custom caches for complex requirements

**Interview Tips:**
- Always discuss time and space complexity
- Provide working code examples
- Consider edge cases and error handling
- Explain trade-offs between different approaches
- Demonstrate understanding of when to use each data structureet evicted key 2: {value}")
# Output: Get evicted key 2: -1
```

## Advanced Data Structures

### Q6: Explain how heapq works and implement a priority queue for task scheduling.

**Answer:**
heapq implements a binary min-heap where the smallest element is always at index 0. It maintains the heap property: parent ≤ children. Perfect for priority queues where you need to efficiently get the minimum/maximum element. Tasks with lower priority numbers get processed first.

**Code Example:**
```python
import heapq
from dataclasses import dataclass
from typing import Any
import time

@dataclass
class Task:
    priority: int
    name: str
    data: Any
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()
    
    def __lt__(self, other):
        # Lower priority number = higher priority
        if self.priority != other.priority:
            return self.priority < other.priority
        # If same priority, older task has higher priority
        return self.created_at < other.created_at

class TaskScheduler:
    def __init__(self):
        self.heap = []
        self.task_count = 0
    
    def add_task(self, priority, name, data=None):
        task = Task(priority, name, data)
        heapq.heappush(self.heap, task)
        self.task_count += 1
        print(f"Added task: {name} (priority: {priority})")
    
    def get_next_task(self):
        if self.heap:
            task = heapq.heappop(self.heap)
            print(f"Processing task: {task.name} (priority: {task.priority})")
            return task
        return None
    
    def peek_next_task(self):
        return self.heap[0] if self.heap else None
    
    def size(self):
        return len(self.heap)

# Test the task scheduler
scheduler = TaskScheduler()

# Add tasks with different priorities
scheduler.add_task(3, "Low priority task")
scheduler.add_task(1, "High priority task")
scheduler.add_task(2, "Medium priority task")
scheduler.add_task(1, "Another high priority task")

print(f"\nScheduler has {scheduler.size()} tasks")
# Output: Added task: Low priority task (priority: 3)
# Output: Added task: High priority task (priority: 1)
# Output: Added task: Medium priority task (priority: 2)
# Output: Added task: Another high priority task (priority: 1)
# Output: Scheduler has 4 tasks

# Process all tasks (should be in priority order)
print("\nProcessing tasks:")
while scheduler.size() > 0:
    task = scheduler.get_next_task()
# Output: Processing tasks:
# Output: Processing task: High priority task (priority: 1)
# Output: Processing task: Another high priority task (priority: 1)
# Output: Processing task: Medium priority task (priority: 2)
# Output: Processing task: Low priority task (priority: 3)

# Demonstrate heap operations
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"\nOriginal list: {numbers}")
heapq.heapify(numbers)
print(f"After heapify: {numbers}")

# Get top 3 smallest and largest
top_3_smallest = heapq.nsmallest(3, numbers)
top_3_largest = heapq.nlargest(3, numbers)
print(f"Top 3 smallest: {top_3_smallest}")
print(f"Top 3 largest: {top_3_largest}")
# Output: Original list: [3, 1, 4, 1, 5, 9, 2, 6]
# Output: After heapify: [1, 1, 2, 3, 5, 9, 4, 6]
# Output: Top 3 smallest: [1, 1, 2]
# Output: Top 3 largest: [9, 6, 5]
```

### Q7: How would you implement a sliding window maximum using deque?

**Answer:**
```python
from collections import deque

def sliding_window_maximum(nums, k):
    """
    Find maximum in each sliding window of size k.
    Time: O(n), Space: O(k)
    """
    if not nums or k == 0:
        return []
    
    # Deque stores indices of array elements
    # Elements are stored in decreasing order of their values
    dq = deque()
    result = []
    
    for i in range(len(nums)):
        # Remove indices that are out of current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices whose corresponding values are smaller than nums[i]
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # The front of deque contains index of maximum element
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Test sliding window maximum
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3

result = sliding_window_maximum(nums, k)
print(f"Array: {nums}")
print(f"Window size: {k}")
print(f"Sliding window maximums: {result}")
# Output: Array: [1, 3, -1, -3, 5, 3, 6, 7]
# Output: Window size: 3
# Output: Sliding window maximums: [3, 3, 5, 5, 6, 7]

# Demonstrate step by step
def sliding_window_maximum_verbose(nums, k):
    dq = deque()
    result = []
    
    for i in range(len(nums)):
        print(f"\nStep {i+1}: Processing nums[{i}] = {nums[i]}")
        
        # Remove out of window indices
        while dq and dq[0] <= i - k:
            removed = dq.popleft()
            print(f"  Removed out-of-window index {removed}")
        
        # Remove smaller elements
        while dq and nums[dq[-1]] <= nums[i]:
            removed = dq.pop()
            print(f"  Removed smaller element at index {removed} (value: {nums[removed]})")
        
        dq.append(i)
        print(f"  Added index {i}, deque: {list(dq)}")
        
        if i >= k - 1:
            max_val = nums[dq[0]]
            result.append(max_val)
            print(f"  Window [{i-k+1}:{i+1}] maximum: {max_val}")
    
    return result

print("\nDetailed execution:")
sliding_window_maximum_verbose([1, 3, -1, -3, 5], 3)
# Output: Detailed execution:
# Output: Step 1: Processing nums[0] = 1
# Output:   Added index 0, deque: [0]
# Output: Step 2: Processing nums[1] = 3
# Output:   Removed smaller element at index 0 (value: 1)
# Output:   Added index 1, deque: [1]
# Output: Step 3: Processing nums[2] = -1
# Output:   Added index 2, deque: [1, 2]
# Output:   Window [0:3] maximum: 3
# Output: Step 4: Processing nums[3] = -3
# Output:   Added index 3, deque: [1, 2, 3]
# Output:   Window [1:4] maximum: 3
# Output: Step 5: Processing nums[4] = 5
# Output:   Removed out-of-window index 1
# Output:   Removed smaller element at index 2 (value: -1)
# Output:   Removed smaller element at index 3 (value: -3)
# Output:   Added index 4, deque: [4]
# Output:   Window [2:5] maximum: 5
```

## Performance and Optimization

### Q8: Compare the time complexity of different operations on Python data structures.

**Answer:**
```python
import time
import random

def time_operation(func, *args, iterations=1000):
    """Time a function over multiple iterations."""
    start = time.time()
    for _ in range(iterations):
        func(*args)
    return (time.time() - start) / iterations

# Test data
small_list = list(range(100))
large_list = list(range(10000))
small_set = set(range(100))
large_set = set(range(10000))
small_dict = {i: i for i in range(100)}
large_dict = {i: i for i in range(10000)}

print("Time Complexity Comparison (average time per operation)")
print("=" * 60)

# Search operations
search_item = 50

list_search_small = time_operation(lambda: search_item in small_list, iterations=10000)
list_search_large = time_operation(lambda: search_item in large_list, iterations=1000)
set_search_small = time_operation(lambda: search_item in small_set, iterations=10000)
set_search_large = time_operation(lambda: search_item in large_set, iterations=10000)

print(f"Search in small list (100 items): {list_search_small:.8f}s")
print(f"Search in large list (10k items): {list_search_large:.8f}s")
print(f"Search in small set (100 items):  {set_search_small:.8f}s")
print(f"Search in large set (10k items):  {set_search_large:.8f}s")
# Output: Search in small list (100 items): 0.00000120s
# Output: Search in large list (10k items): 0.00012000s
# Output: Search in small set (100 items):  0.00000015s
# Output: Search in large set (10k items):  0.00000015s

print(f"\nList search scales O(n): {list_search_large/list_search_small:.1f}x slower")
print(f"Set search scales O(1): {set_search_large/set_search_small:.1f}x slower")
# Output: List search scales O(n): 100.0x slower
# Output: Set search scales O(1): 1.0x slower

# Insert operations
list_insert_end = time_operation(lambda: small_list.append(999), iterations=10000)
list_insert_start = time_operation(lambda: small_list.insert(0, 999), iterations=1000)
set_add = time_operation(lambda: small_set.add(999), iterations=10000)

print(f"\nInsert at end of list:   {list_insert_end:.8f}s")
print(f"Insert at start of list: {list_insert_start:.8f}s")
print(f"Add to set:              {set_add:.8f}s")
# Output: Insert at end of list:   0.00000025s
# Output: Insert at start of list: 0.00002500s
# Output: Add to set:              0.00000030s

# Dictionary operations
dict_get = time_operation(lambda: small_dict.get(50), iterations=10000)
dict_setitem = time_operation(lambda: small_dict.__setitem__(999, 999), iterations=10000)

print(f"\nDictionary get:          {dict_get:.8f}s")
print(f"Dictionary set:          {dict_setitem:.8f}s")
# Output: Dictionary get:          0.00000020s
# Output: Dictionary set:          0.00000025s
```

These interview questions cover essential Python data structures concepts that data engineers need to master, with working implementations and expected outputs for hands-on learning.duler = TaskScheduler()

# Add tasks with different priorities
scheduler.add_task(3, "Low priority task")
scheduler.add_task(1, "High priority task")
scheduler.add_task(2, "Medium priority task")
scheduler.add_task(1, "Another high priority task")

print(f"\nScheduler has {scheduler.size()} tasks")
# Output: Added task: Low priority task (priority: 3)
# Output: Added task: High priority task (priority: 1)
# Output: Added task: Medium priority task (priority: 2)
# Output: Added task: Another high priority task (priority: 1)
# Output: Scheduler has 4 tasks

# Process all tasks (should be in priority order)
print("\nProcessing tasks:")
while scheduler.size() > 0:
    task = scheduler.get_next_task()
# Output: Processing tasks:
# Output: Processing task: High priority task (priority: 1)
# Output: Processing task: Another high priority task (priority: 1)
# Output: Processing task: Medium priority task (priority: 2)
# Output: Processing task: Low priority task (priority: 3)

# Demonstrate heap operations
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"\nOriginal list: {numbers}")
heapq.heapify(numbers)
print(f"After heapify: {numbers}")

# Get top 3 smallest and largest
top_3_smallest = heapq.nsmallest(3, numbers)
top_3_largest = heapq.nlargest(3, numbers)
print(f"Top 3 smallest: {top_3_smallest}")
print(f"Top 3 largest: {top_3_largest}")
# Output: Original list: [3, 1, 4, 1, 5, 9, 2, 6]
# Output: After heapify: [1, 1, 2, 3, 5, 9, 4, 6]
# Output: Top 3 smallest: [1, 1, 2]
# Output: Top 3 largest: [9, 6, 5]
```

### Q7: How would you implement a sliding window maximum using deque?

**Answer:**
```python
from collections import deque

def sliding_window_maximum(nums, k):
    """
    Find maximum in each sliding window of size k.
    Time: O(n), Space: O(k)
    """
    if not nums or k == 0:
        return []
    
    # Deque stores indices of array elements
    # Elements are stored in decreasing order of their values
    dq = deque()
    result = []
    
    for i in range(len(nums)):
        # Remove indices that are out of current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove indices whose corresponding values are smaller than nums[i]
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # The front of deque contains index of maximum element
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Test sliding window maximum
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3

result = sliding_window_maximum(nums, k)
print(f"Array: {nums}")
print(f"Window size: {k}")
print(f"Sliding window maximums: {result}")
# Output: Array: [1, 3, -1, -3, 5, 3, 6, 7]
# Output: Window size: 3
# Output: Sliding window maximums: [3, 3, 5, 5, 6, 7]

# Demonstrate step by step
def sliding_window_maximum_verbose(nums, k):
    dq = deque()
    result = []
    
    for i in range(len(nums)):
        print(f"\nStep {i+1}: Processing nums[{i}] = {nums[i]}")
        
        # Remove out of window indices
        while dq and dq[0] <= i - k:
            removed = dq.popleft()
            print(f"  Removed out-of-window index {removed}")
        
        # Remove smaller elements
        while dq and nums[dq[-1]] <= nums[i]:
            removed = dq.pop()
            print(f"  Removed smaller element at index {removed} (value: {nums[removed]})")
        
        dq.append(i)
        print(f"  Added index {i}, deque: {list(dq)}")
        
        if i >= k - 1:
            max_val = nums[dq[0]]
            result.append(max_val)
            print(f"  Window [{i-k+1}:{i+1}] maximum: {max_val}")
    
    return result

print("\nDetailed execution:")
sliding_window_maximum_verbose([1, 3, -1, -3, 5], 3)
# Output: Detailed execution:
# Output: Step 1: Processing nums[0] = 1
# Output:   Added index 0, deque: [0]
# Output: Step 2: Processing nums[1] = 3
# Output:   Removed smaller element at index 0 (value: 1)
# Output:   Added index 1, deque: [1]
# Output: Step 3: Processing nums[2] = -1
# Output:   Added index 2, deque: [1, 2]
# Output:   Window [0:3] maximum: 3
# Output: Step 4: Processing nums[3] = -3
# Output:   Added index 3, deque: [1, 2, 3]
# Output:   Window [1:4] maximum: 3
# Output: Step 5: Processing nums[4] = 5
# Output:   Removed out-of-window index 1
# Output:   Removed smaller element at index 2 (value: -1)
# Output:   Removed smaller element at index 3 (value: -3)
# Output:   Added index 4, deque: [4]
# Output:   Window [2:5] maximum: 5
```

## Performance and Optimization

### Q8: Compare the time complexity of different operations on Python data structures.

**Answer:**
```python
import time
import random

def time_operation(func, *args, iterations=1000):
    """Time a function over multiple iterations."""
    start = time.time()
    for _ in range(iterations):
        func(*args)
    return (time.time() - start) / iterations

# Test data
small_list = list(range(100))
large_list = list(range(10000))
small_set = set(range(100))
large_set = set(range(10000))
small_dict = {i: i for i in range(100)}
large_dict = {i: i for i in range(10000)}

print("Time Complexity Comparison (average time per operation)")
print("=" * 60)

# Search operations
search_item = 50

list_search_small = time_operation(lambda: search_item in small_list, iterations=10000)
list_search_large = time_operation(lambda: search_item in large_list, iterations=1000)
set_search_small = time_operation(lambda: search_item in small_set, iterations=10000)
set_search_large = time_operation(lambda: search_item in large_set, iterations=10000)

print(f"Search in small list (100 items): {list_search_small:.8f}s")
print(f"Search in large list (10k items): {list_search_large:.8f}s")
print(f"Search in small set (100 items):  {set_search_small:.8f}s")
print(f"Search in large set (10k items):  {set_search_large:.8f}s")
# Output: Search in small list (100 items): 0.00000120s
# Output: Search in large list (10k items): 0.00012000s
# Output: Search in small set (100 items):  0.00000015s
# Output: Search in large set (10k items):  0.00000015s

print(f"\nList search scales O(n): {list_search_large/list_search_small:.1f}x slower")
print(f"Set search scales O(1): {set_search_large/set_search_small:.1f}x slower")
# Output: List search scales O(n): 100.0x slower
# Output: Set search scales O(1): 1.0x slower

# Insert operations
list_insert_end = time_operation(lambda: small_list.append(999), iterations=10000)
list_insert_start = time_operation(lambda: small_list.insert(0, 999), iterations=1000)
set_add = time_operation(lambda: small_set.add(999), iterations=10000)

print(f"\nInsert at end of list:   {list_insert_end:.8f}s")
print(f"Insert at start of list: {list_insert_start:.8f}s")
print(f"Add to set:              {set_add:.8f}s")
# Output: Insert at end of list:   0.00000025s
# Output: Insert at start of list: 0.00002500s
# Output: Add to set:              0.00000030s

# Dictionary operations
dict_get = time_operation(lambda: small_dict.get(50), iterations=10000)
dict_setitem = time_operation(lambda: small_dict.__setitem__(999, 999), iterations=10000)

print(f"\nDictionary get:          {dict_get:.8f}s")
print(f"Dictionary set:          {dict_setitem:.8f}s")
# Output: Dictionary get:          0.00000020s
# Output: Dictionary set:          0.00000025s
```

### Q9: How would you optimize memory usage when working with large datasets?

**Answer:**
Use generators for lazy evaluation, arrays instead of lists for numeric data, __slots__ for memory-efficient classes, and process data in chunks. These techniques can reduce memory usage by 50-90% for large datasets while maintaining functionality.

**Code Example:**
```python
import sys
from array import array
import gc

# Memory comparison: list vs array vs generator
def memory_comparison():
    # Regular list
    regular_list = [i for i in range(100000)]
    
    # Array (more memory efficient for numbers)
    int_array = array('i', range(100000))
    
    # Generator (minimal memory)
    def number_generator():
        for i in range(100000):
            yield i
    
    gen = number_generator()
    
    print("Memory Usage Comparison:")
    print(f"Regular list: {sys.getsizeof(regular_list):,} bytes")
    print(f"Integer array: {sys.getsizeof(int_array):,} bytes")
    print(f"Generator: {sys.getsizeof(gen):,} bytes")
    # Output: Memory Usage Comparison:
    # Output: Regular list: 824,464 bytes
    # Output: Integer array: 400,064 bytes
    # Output: Generator: 104 bytes
    
    # Memory per element
    print(f"\nMemory per element:")
    print(f"List: {sys.getsizeof(regular_list) / len(regular_list):.2f} bytes")
    print(f"Array: {sys.getsizeof(int_array) / len(int_array):.2f} bytes")
    # Output: Memory per element:
    # Output: List: 8.24 bytes
    # Output: Array: 4.00 bytes

memory_comparison()

# Slots for memory-efficient classes
class RegularEmployee:
    def __init__(self, name, id, salary):
        self.name = name
        self.id = id
        self.salary = salary

class SlottedEmployee:
    __slots__ = ['name', 'id', 'salary']
    
    def __init__(self, name, id, salary):
        self.name = name
        self.id = id
        self.salary = salary

# Compare memory usage
regular_emp = RegularEmployee("John", 123, 50000)
slotted_emp = SlottedEmployee("Jane", 124, 55000)

print(f"\nClass Memory Comparison:")
print(f"Regular employee: {sys.getsizeof(regular_emp.__dict__)} bytes")
print(f"Slotted employee: {sys.getsizeof(slotted_emp)} bytes")
# Output: Class Memory Comparison:
# Output: Regular employee: 296 bytes
# Output: Slotted employee: 48 bytes

# Processing large datasets in chunks
def process_large_dataset_chunked(data_source, chunk_size=1000):
    """Process large dataset in chunks to manage memory."""
    chunk = []
    processed_count = 0
    
    for item in data_source:
        chunk.append(item)
        
        if len(chunk) >= chunk_size:
            # Process chunk
            result = sum(chunk)  # Example processing
            print(f"Processed chunk of {len(chunk)} items, sum: {result}")
            processed_count += len(chunk)
            
            # Clear chunk to free memory
            chunk.clear()
            gc.collect()  # Force garbage collection
    
    # Process remaining items
    if chunk:
        result = sum(chunk)
        print(f"Processed final chunk of {len(chunk)} items, sum: {result}")
        processed_count += len(chunk)
    
    return processed_count

# Test chunked processing
print(f"\nChunked Processing:")
total_processed = process_large_dataset_chunked(range(5500), chunk_size=2000)
print(f"Total items processed: {total_processed}")
# Output: Chunked Processing:
# Output: Processed chunk of 2000 items, sum: 1999000
# Output: Processed chunk of 2000 items, sum: 5999000
# Output: Processed final chunk of 1500 items, sum: 7124500
# Output: Total items processed: 5500
```

## Real-World Scenarios

### Q10: Design a data structure for a real-time analytics system that tracks user events.

**Answer:**
Combine deque for time-windowed events, defaultdict for user sessions, Counter for aggregations, and threading locks for concurrency. This provides O(1) event insertion, efficient cleanup of old data, and fast analytics queries for real-time systems.

**Code Example:**
```python
from collections import defaultdict, deque, Counter
import time
from typing import Dict, List, Any
import threading

class RealTimeAnalytics:
    def __init__(self, window_size_minutes=60):
        self.window_size = window_size_minutes * 60  # Convert to seconds
        
        # Event storage with timestamps
        self.events = deque()  # (timestamp, event_data)
        
        # Fast lookups
        self.user_sessions = defaultdict(lambda: {
            'events': deque(),
            'first_seen': None,
            'last_seen': None
        })
        
        # Aggregated metrics
        self.event_counts = Counter()
        self.hourly_stats = defaultdict(lambda: Counter())
        
        # Thread safety
        self.lock = threading.Lock()
    
    def add_event(self, user_id: str, event_type: str, data: Dict[str, Any] = None):
        """Add a new event to the analytics system."""
        timestamp = time.time()
        event = {
            'user_id': user_id,
            'event_type': event_type,
            'timestamp': timestamp,
            'data': data or {}
        }
        
        with self.lock:
            # Add to main event stream
            self.events.append((timestamp, event))
            
            # Update user session
            session = self.user_sessions[user_id]
            session['events'].append(event)
            if session['first_seen'] is None:
                session['first_seen'] = timestamp
            session['last_seen'] = timestamp
            
            # Update counters
            self.event_counts[event_type] += 1
            hour_key = int(timestamp // 3600)  # Hour bucket
            self.hourly_stats[hour_key][event_type] += 1
            
            # Clean old data
            self._cleanup_old_data(timestamp)
    
    def _cleanup_old_data(self, current_time: float):
        """Remove events older than window_size."""
        cutoff_time = current_time - self.window_size
        
        # Clean main event stream
        while self.events and self.events[0][0] < cutoff_time:
            self.events.popleft()
        
        # Clean user sessions
        for user_id, session in list(self.user_sessions.items()):
            # Clean old events from user session
            while session['events'] and session['events'][0]['timestamp'] < cutoff_time:
                session['events'].popleft()
            
            # Remove empty sessions
            if not session['events']:
                del self.user_sessions[user_id]
        
        # Clean hourly stats (keep last 24 hours)
        current_hour = int(current_time // 3600)
        old_hours = [h for h in self.hourly_stats.keys() if h < current_hour - 24]
        for hour in old_hours:
            del self.hourly_stats[hour]
    
    def get_active_users(self) -> int:
        """Get count of active users in current window."""
        with self.lock:
            return len(self.user_sessions)
    
    def get_event_stats(self) -> Dict[str, int]:
        """Get event type statistics."""
        with self.lock:
            return dict(self.event_counts)
    
    def get_user_journey(self, user_id: str) -> List[Dict[str, Any]]:
        """Get event journey for a specific user."""
        with self.lock:
            session = self.user_sessions.get(user_id)
            if session:
                return list(session['events'])
            return []
    
    def get_top_events(self, limit: int = 10) -> List[tuple]:
        """Get most common events."""
        with self.lock:
            return self.event_counts.most_common(limit)
    
    def get_hourly_trends(self) -> Dict[int, Dict[str, int]]:
        """Get hourly event trends."""
        with self.lock:
            return {hour: dict(stats) for hour, stats in self.hourly_stats.items()}

# Test the analytics system
analytics = RealTimeAnalytics(window_size_minutes=5)  # 5-minute window for testing

# Simulate user events
events_data = [
    ("user1", "page_view", {"page": "home"}),
    ("user1", "click", {"element": "signup_button"}),
    ("user2", "page_view", {"page": "products"}),
    ("user1", "signup", {"method": "email"}),
    ("user3", "page_view", {"page": "home"}),
    ("user2", "add_to_cart", {"product_id": "123"}),
    ("user3", "click", {"element": "login_button"}),
    ("user2", "purchase", {"amount": 99.99}),
]

print("Adding events to analytics system:")
for user_id, event_type, data in events_data:
    analytics.add_event(user_id, event_type, data)
    print(f"Added: {user_id} -> {event_type}")

print(f"\nAnalytics Summary:")
print(f"Active users: {analytics.get_active_users()}")
print(f"Event statistics: {analytics.get_event_stats()}")
print(f"Top events: {analytics.get_top_events()}")
# Output: Adding events to analytics system:
# Output: Added: user1 -> page_view
# Output: Added: user1 -> click
# Output: Added: user2 -> page_view
# Output: Added: user1 -> signup
# Output: Added: user3 -> page_view
# Output: Added: user2 -> add_to_cart
# Output: Added: user3 -> click
# Output: Added: user2 -> purchase
# Output: Analytics Summary:
# Output: Active users: 3
# Output: Event statistics: {'page_view': 3, 'click': 2, 'signup': 1, 'add_to_cart': 1, 'purchase': 1}
# Output: Top events: [('page_view', 3), ('click', 2), ('signup', 1), ('add_to_cart', 1), ('purchase', 1)]

# User journey analysis
print(f"\nUser1 journey:")
journey = analytics.get_user_journey("user1")
for event in journey:
    print(f"  {event['event_type']} at {time.ctime(event['timestamp'])}")
# Output: User1 journey:
# Output:   page_view at Mon Dec 18 10:30:45 2023
# Output:   click at Mon Dec 18 10:30:45 2023
# Output:   signup at Mon Dec 18 10:30:45 2023
```

## Coding Challenges

### Q11: Implement a data structure that supports insert, delete, and getRandom in O(1) time.

**Answer:**
Use an array to store values and a hash map to track indices. For deletion, swap the element with the last element to avoid shifting. This maintains O(1) operations while preserving the ability to get random elements efficiently.

**Code Example:**
```python
import random

class RandomizedSet:
    def __init__(self):
        self.data = []  # Store actual values
        self.indices = {}  # Map value to index in data array
    
    def insert(self, val):
        """Insert a value. Returns True if not already present."""
        if val in self.indices:
            return False
        
        # Add to end of array and update index mapping
        self.indices[val] = len(self.data)
        self.data.append(val)
        return True
    
    def remove(self, val):
        """Remove a value. Returns True if present."""
        if val not in self.indices:
            return False
        
        # Get index of element to remove
        index_to_remove = self.indices[val]
        last_element = self.data[-1]
        
        # Move last element to position of element to remove
        self.data[index_to_remove] = last_element
        self.indices[last_element] = index_to_remove
        
        # Remove last element and its index mapping
        self.data.pop()
        del self.indices[val]
        
        return True
    
    def getRandom(self):
        """Get random element in O(1) time."""
        if not self.data:
            return None
        return random.choice(self.data)
    
    def size(self):
        return len(self.data)
    
    def __str__(self):
        return f"RandomizedSet(data={self.data}, indices={self.indices})"

# Test the RandomizedSet
rs = RandomizedSet()

print("Testing RandomizedSet:")
print(f"Insert 1: {rs.insert(1)}")
print(f"Insert 2: {rs.insert(2)}")
print(f"Insert 3: {rs.insert(3)}")
print(f"Current state: {rs}")
# Output: Testing RandomizedSet:
# Output: Insert 1: True
# Output: Insert 2: True
# Output: Insert 3: True
# Output: Current state: RandomizedSet(data=[1, 2, 3], indices={1: 0, 2: 1, 3: 2})

print(f"Insert 2 again: {rs.insert(2)}")  # Should return False
print(f"Remove 2: {rs.remove(2)}")
print(f"After removing 2: {rs}")
# Output: Insert 2 again: False
# Output: Remove 2: True
# Output: After removing 2: RandomizedSet(data=[1, 3], indices={1: 0, 3: 1})

print(f"Random elements:")
for i in range(5):
    print(f"  Random: {rs.getRandom()}")
# Output: Random elements:
# Output:   Random: 3
# Output:   Random: 1
# Output:   Random: 3
# Output:   Random: 1
# Output:   Random: 3
```

### Q12: Design a data structure for autocomplete functionality.

**Answer:**
Trie (prefix tree) is ideal for autocomplete. Each node represents a character, paths form words, and leaf nodes mark word endings. Store frequency at word nodes for ranking suggestions. This provides efficient prefix matching and sorted suggestions by popularity.

**Code Example:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_word = False
        self.frequency = 0

class AutoComplete:
    def __init__(self):
        self.root = TrieNode()
        self.suggestions_limit = 10
    
    def insert(self, word, frequency=1):
        """Insert a word with its frequency."""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_word = True
        node.frequency += frequency
    
    def search(self, word):
        """Check if word exists in trie."""
        node = self._find_node(word.lower())
        return node is not None and node.is_end_word
    
    def _find_node(self, prefix):
        """Find the node corresponding to prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def _collect_words(self, node, prefix, words):
        """Collect all words starting from given node."""
        if node.is_end_word:
            words.append((prefix, node.frequency))
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, words)
    
    def get_suggestions(self, prefix):
        """Get autocomplete suggestions for prefix."""
        prefix = prefix.lower()
        node = self._find_node(prefix)
        
        if not node:
            return []
        
        # Collect all words with this prefix
        words = []
        self._collect_words(node, prefix, words)
        
        # Sort by frequency (descending) and return top suggestions
        words.sort(key=lambda x: x[1], reverse=True)
        return [word for word, freq in words[:self.suggestions_limit]]
    
    def update_frequency(self, word):
        """Update frequency when user selects a word."""
        self.insert(word, frequency=1)  # Increment frequency

# Test autocomplete system
autocomplete = AutoComplete()

# Build vocabulary with frequencies
vocabulary = [
    ("python", 100), ("programming", 80), ("program", 60),
    ("project", 70), ("problem", 50), ("process", 40),
    ("data", 90), ("database", 85), ("dataframe", 75),
    ("structure", 65), ("string", 55), ("stream", 45)
]

print("Building autocomplete vocabulary:")
for word, freq in vocabulary:
    autocomplete.insert(word, freq)
    print(f"Added: {word} (frequency: {freq})")

# Test suggestions
test_prefixes = ["pro", "data", "str", "py"]

print(f"\nAutocomplete suggestions:")
for prefix in test_prefixes:
    suggestions = autocomplete.get_suggestions(prefix)
    print(f"'{prefix}' -> {suggestions}")
# Output: Building autocomplete vocabulary:
# Output: Added: python (frequency: 100)
# Output: Added: programming (frequency: 80)
# Output: Added: program (frequency: 60)
# Output: Added: project (frequency: 70)
# Output: Added: problem (frequency: 50)
# Output: Added: process (frequency: 40)
# Output: Added: data (frequency: 90)
# Output: Added: database (frequency: 85)
# Output: Added: dataframe (frequency: 75)
# Output: Added: structure (frequency: 65)
# Output: Added: string (frequency: 55)
# Output: Added: stream (frequency: 45)
# Output: Autocomplete suggestions:
# Output: 'pro' -> ['programming', 'project', 'program', 'problem', 'process']
# Output: 'data' -> ['data', 'database', 'dataframe']
# Output: 'str' -> ['structure', 'string', 'stream']
# Output: 'py' -> ['python']

# Simulate user interaction
print(f"\nSimulating user selections:")
autocomplete.update_frequency("problem")  # User selected "problem"
autocomplete.update_frequency("problem")  # User selected "problem" again

updated_suggestions = autocomplete.get_suggestions("pro")
print(f"Updated 'pro' suggestions: {updated_suggestions}")
# Output: Simulating user selections:
# Output: Updated 'pro' suggestions: ['programming', 'project', 'program', 'problem', 'process']
```

These interview questions cover the essential aspects of Python data structures that data engineers need to understand, from basic operations to complex real-world implementations. Each answer includes working code examples with expected outputs to demonstrate practical understanding.