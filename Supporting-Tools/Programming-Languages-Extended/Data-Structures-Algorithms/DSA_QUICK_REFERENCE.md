# Data Structures & Algorithms Quick Reference

## Time & Space Complexity Cheat Sheet

### Big O Notation
- **O(1)** - Constant time
- **O(log n)** - Logarithmic time
- **O(n)** - Linear time
- **O(n log n)** - Linearithmic time
- **O(n²)** - Quadratic time
- **O(2^n)** - Exponential time

### Common Data Structures

| Data Structure | Access | Search | Insertion | Deletion | Space |
|----------------|--------|--------|-----------|----------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Table | O(1) | O(1) | O(1) | O(1) | O(n) |
| Binary Search Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Heap | O(1) | O(n) | O(log n) | O(log n) | O(n) |

### Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |

## Essential Data Structures

### Array/List
```python
# Basic operations
arr = [1, 2, 3, 4, 5]
arr.append(6)        # O(1) amortized
arr.insert(0, 0)     # O(n)
arr.pop()            # O(1)
arr.pop(0)           # O(n)
arr[2]               # O(1) access
```

### Stack (LIFO)
```python
stack = []
stack.append(item)   # push - O(1)
stack.pop()          # pop - O(1)
stack[-1]            # peek - O(1)
len(stack) == 0      # is_empty - O(1)
```

### Queue (FIFO)
```python
from collections import deque
queue = deque()
queue.append(item)   # enqueue - O(1)
queue.popleft()      # dequeue - O(1)
queue[0]             # front - O(1)
len(queue) == 0      # is_empty - O(1)
```

### Hash Table/Dictionary
```python
hash_table = {}
hash_table[key] = value  # O(1) average
value = hash_table[key]  # O(1) average
del hash_table[key]      # O(1) average
key in hash_table        # O(1) average
```

### Set
```python
s = set()
s.add(item)          # O(1) average
s.remove(item)       # O(1) average
item in s            # O(1) average
s1.union(s2)         # O(len(s1) + len(s2))
s1.intersection(s2)  # O(min(len(s1), len(s2)))
```

### Heap (Priority Queue)
```python
import heapq
heap = []
heapq.heappush(heap, item)  # O(log n)
heapq.heappop(heap)         # O(log n)
heap[0]                     # peek min - O(1)
heapq.heapify(list)         # O(n)
```

## Essential Algorithms

### Binary Search
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### Two Pointers
```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

### Sliding Window
```python
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum = window_sum - arr[i-k] + arr[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### DFS (Depth-First Search)
```python
def dfs_recursive(graph, node, visited):
    visited.add(node)
    result = [node]
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            stack.extend(graph[node])
    
    return result
```

### BFS (Breadth-First Search)
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    result = []
    
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result
```

### Quick Sort
```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)
```

### Merge Sort
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

## Common Patterns

### Frequency Counter
```python
from collections import Counter

def char_frequency(s):
    return Counter(s)

def most_common_char(s):
    counter = Counter(s)
    return counter.most_common(1)[0]
```

### Prefix Sum
```python
def prefix_sum(arr):
    prefix = [0]
    for num in arr:
        prefix.append(prefix[-1] + num)
    return prefix

def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

### Union-Find (Disjoint Set)
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        return True
```

### Trie (Prefix Tree)
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
```

## Problem-Solving Strategies

### 1. Understand the Problem
- Read carefully and identify inputs/outputs
- Consider edge cases
- Ask clarifying questions

### 2. Choose the Right Approach
- **Brute Force**: Try all possibilities
- **Divide & Conquer**: Break into subproblems
- **Dynamic Programming**: Overlapping subproblems
- **Greedy**: Make locally optimal choices
- **Backtracking**: Try and undo choices

### 3. Common Problem Types

**Array/String Problems**:
- Two pointers, sliding window
- Prefix sums, frequency counting
- Sorting and searching

**Tree Problems**:
- DFS/BFS traversal
- Recursive solutions
- Level-order processing

**Graph Problems**:
- DFS/BFS for connectivity
- Shortest path algorithms
- Topological sorting

**Dynamic Programming**:
- Identify overlapping subproblems
- Define state and transitions
- Bottom-up or top-down approach

### 4. Optimization Techniques
- Use appropriate data structures
- Avoid unnecessary operations
- Consider space-time tradeoffs
- Use built-in functions when appropriate

## Data Engineering Specific Applications

### Stream Processing
```python
# Sliding window for stream analytics
class SlidingWindowCounter:
    def __init__(self, window_size):
        self.window = deque()
        self.window_size = window_size
        self.count = 0
    
    def add(self, timestamp, value):
        # Remove old entries
        while (self.window and 
               timestamp - self.window[0][0] >= self.window_size):
            _, old_value = self.window.popleft()
            self.count -= old_value
        
        # Add new entry
        self.window.append((timestamp, value))
        self.count += value
        
        return self.count
```

### Batch Processing
```python
# Merge sorted files
def merge_sorted_files(files):
    import heapq
    
    heap = []
    file_iterators = []
    
    # Initialize heap with first element from each file
    for i, file in enumerate(files):
        iterator = iter(file)
        try:
            first_item = next(iterator)
            heapq.heappush(heap, (first_item, i))
            file_iterators.append(iterator)
        except StopIteration:
            file_iterators.append(None)
    
    result = []
    while heap:
        value, file_idx = heapq.heappop(heap)
        result.append(value)
        
        # Get next item from same file
        if file_iterators[file_idx]:
            try:
                next_item = next(file_iterators[file_idx])
                heapq.heappush(heap, (next_item, file_idx))
            except StopIteration:
                file_iterators[file_idx] = None
    
    return result
```

### Caching Strategies
```python
# LRU Cache implementation
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
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used
            self.cache.popitem(last=False)
        
        self.cache[key] = value
```

Remember: Practice is key to mastering DSA. Focus on understanding patterns rather than memorizing solutions.