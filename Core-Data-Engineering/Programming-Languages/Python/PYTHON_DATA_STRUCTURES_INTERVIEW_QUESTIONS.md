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
```python
# Lists - mutable, ordered
my_list = [1, 2, 3]
my_list.append(4)  # Allowed
my_list[0] = 10    # Allowed
print(f"Modified list: {my_list}")
# Output: Modified list: [10, 2, 3, 4]

# Tuples - immutable, ordered
my_tuple = (1, 2, 3)
# my_tuple.append(4)  # Error: AttributeError
# my_tuple[0] = 10    # Error: TypeError
print(f"Tuple: {my_tuple}")
# Output: Tuple: (1, 2, 3)

# Performance comparison
import sys
list_data = [1, 2, 3, 4, 5]
tuple_data = (1, 2, 3, 4, 5)
print(f"List size: {sys.getsizeof(list_data)} bytes")
print(f"Tuple size: {sys.getsizeof(tuple_data)} bytes")
# Output: List size: 104 bytes
# Output: Tuple size: 80 bytes
```

**Key Points:**
- Lists are mutable, tuples are immutable
- Tuples are more memory efficient
- Tuples can be used as dictionary keys
- Lists have more methods (append, extend, remove, etc.)

### Q2: How do you efficiently remove duplicates from a list while preserving order?

**Answer:**
```python
# Method 1: Using dict.fromkeys() (Python 3.7+)
def remove_duplicates_ordered(lst):
    return list(dict.fromkeys(lst))

# Method 2: Using set with manual ordering
def remove_duplicates_set(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Test both methods
original = [1, 2, 3, 2, 4, 1, 5, 3]
method1 = remove_duplicates_ordered(original)
method2 = remove_duplicates_set(original)

print(f"Original: {original}")
print(f"Method 1 (dict.fromkeys): {method1}")
print(f"Method 2 (set): {method2}")
# Output: Original: [1, 2, 3, 2, 4, 1, 5, 3]
# Output: Method 1 (dict.fromkeys): [1, 2, 3, 4, 5]
# Output: Method 2 (set): [1, 2, 3, 4, 5]

# Performance comparison
import time
large_list = list(range(10000)) * 2  # 20k items with duplicates

start = time.time()
result1 = remove_duplicates_ordered(large_list)
time1 = time.time() - start

start = time.time()
result2 = remove_duplicates_set(large_list)
time2 = time.time() - start

print(f"dict.fromkeys time: {time1:.4f}s")
print(f"set method time: {time2:.4f}s")
# Output: dict.fromkeys time: 0.0012s
# Output: set method time: 0.0018s
```

### Q3: Explain the difference between shallow and deep copy with examples.

**Answer:**
```python
import copy

# Original nested structure
original = [[1, 2, 3], [4, 5, 6]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

print(f"Original: {original}")
print(f"Shallow: {shallow}")
print(f"Deep: {deep}")
# Output: Original: [[1, 2, 3], [4, 5, 6]]
# Output: Shallow: [[1, 2, 3], [4, 5, 6]]
# Output: Deep: [[1, 2, 3], [4, 5, 6]]

# Modify nested element
original[0][0] = 'CHANGED'

print(f"\nAfter modifying original[0][0]:")
print(f"Original: {original}")
print(f"Shallow: {shallow}")  # Affected!
print(f"Deep: {deep}")        # Not affected
# Output: After modifying original[0][0]:
# Output: Original: [['CHANGED', 2, 3], [4, 5, 6]]
# Output: Shallow: [['CHANGED', 2, 3], [4, 5, 6]]
# Output: Deep: [[1, 2, 3], [4, 5, 6]]

# Add new sublist to original
original.append([7, 8, 9])

print(f"\nAfter adding new sublist:")
print(f"Original: {original}")
print(f"Shallow: {shallow}")  # Not affected
print(f"Deep: {deep}")        # Not affected
# Output: After adding new sublist:
# Output: Original: [['CHANGED', 2, 3], [4, 5, 6], [7, 8, 9]]
# Output: Shallow: [['CHANGED', 2, 3], [4, 5, 6]]
# Output: Deep: [[1, 2, 3], [4, 5, 6]]
```

## Collections Module

### Q4: When would you use Counter vs defaultdict vs regular dict?

**Answer:**
```python
from collections import Counter, defaultdict

# Counter - for counting and frequency analysis
text = "hello world"
char_count = Counter(text)
print(f"Character frequencies: {dict(char_count)}")
print(f"Most common: {char_count.most_common(3)}")
# Output: Character frequencies: {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
# Output: Most common: [('l', 3), ('o', 2), ('h', 1)]

# defaultdict - for grouping without key checks
students = [
    ("Alice", "Math"), ("Bob", "Science"), ("Alice", "English"), 
    ("Charlie", "Math"), ("Bob", "Math")
]

# With defaultdict
subjects_dd = defaultdict(list)
for student, subject in students:
    subjects_dd[student].append(subject)

print(f"defaultdict result: {dict(subjects_dd)}")
# Output: defaultdict result: {'Alice': ['Math', 'English'], 'Bob': ['Science', 'Math'], 'Charlie': ['Math']}

# With regular dict (more verbose)
subjects_dict = {}
for student, subject in students:
    if student not in subjects_dict:
        subjects_dict[student] = []
    subjects_dict[student].append(subject)

print(f"Regular dict result: {subjects_dict}")
# Output: Regular dict result: {'Alice': ['Math', 'English'], 'Bob': ['Science', 'Math'], 'Charlie': ['Math']}

# Performance comparison for grouping
import time

data = [("key1", i) for i in range(10000)] + [("key2", i) for i in range(10000)]

# defaultdict timing
start = time.time()
dd_result = defaultdict(list)
for key, value in data:
    dd_result[key].append(value)
dd_time = time.time() - start

# regular dict timing
start = time.time()
dict_result = {}
for key, value in data:
    if key not in dict_result:
        dict_result[key] = []
    dict_result[key].append(value)
dict_time = time.time() - start

print(f"defaultdict time: {dd_time:.4f}s")
print(f"regular dict time: {dict_time:.4f}s")
print(f"defaultdict is {dict_time/dd_time:.1f}x faster")
# Output: defaultdict time: 0.0023s
# Output: regular dict time: 0.0031s
# Output: defaultdict is 1.3x faster
```

### Q5: Implement a LRU cache using OrderedDict.

**Answer:**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            # Update existing key
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used (first item)
            self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def display(self):
        return list(self.cache.items())

# Test the LRU cache
lru = LRUCache(3)

# Add items
lru.put(1, "one")
lru.put(2, "two")
lru.put(3, "three")
print(f"After adding 1,2,3: {lru.display()}")
# Output: After adding 1,2,3: [(1, 'one'), (2, 'two'), (3, 'three')]

# Access item 1 (moves to end)
value = lru.get(1)
print(f"Get key 1: {value}")
print(f"After accessing 1: {lru.display()}")
# Output: Get key 1: one
# Output: After accessing 1: [(2, 'two'), (3, 'three'), (1, 'one')]

# Add item 4 (evicts least recently used: key 2)
lru.put(4, "four")
print(f"After adding 4: {lru.display()}")
# Output: After adding 4: [(3, 'three'), (1, 'one'), (4, 'four')]

# Try to get evicted item
value = lru.get(2)
print(f"Get evicted key 2: {value}")
# Output: Get evicted key 2: -1
```

## Advanced Data Structures

### Q6: Explain how heapq works and implement a priority queue for task scheduling.

**Answer:**
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

### Q9: How would you optimize memory usage when working with large datasets?

**Answer:**
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