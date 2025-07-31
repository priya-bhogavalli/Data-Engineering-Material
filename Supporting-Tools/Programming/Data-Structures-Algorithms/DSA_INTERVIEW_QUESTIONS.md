# Data Structures & Algorithms Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. Explain the difference between Array and Linked List
**Answer**: Arrays store elements in contiguous memory locations with fixed size, while linked lists store elements in nodes connected by pointers with dynamic size.

**Key Differences**:
- **Memory**: Arrays use contiguous memory, linked lists use scattered memory
- **Access Time**: Arrays O(1) random access, linked lists O(n) sequential access
- **Insertion/Deletion**: Arrays O(n) for middle operations, linked lists O(1) if position known
- **Memory Overhead**: Arrays have no extra memory, linked lists need pointer storage

```python
# Array implementation
class Array:
    def __init__(self, capacity):
        self.data = [None] * capacity
        self.size = 0
        self.capacity = capacity
    
    def get(self, index):
        if 0 <= index < self.size:
            return self.data[index]
        raise IndexError("Index out of bounds")
    
    def insert(self, index, value):
        if self.size >= self.capacity:
            raise OverflowError("Array is full")
        
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i-1]
        
        self.data[index] = value
        self.size += 1

# Linked List implementation
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def insert_at_beginning(self, val):
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def delete_value(self, val):
        if not self.head:
            return False
        
        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next and current.next.val != val:
            current = current.next
        
        if current.next:
            current.next = current.next.next
            self.size -= 1
            return True
        
        return False
```

### 2. What is a Stack and how would you implement it?
**Answer**: A Stack is a LIFO (Last In, First Out) data structure that supports push, pop, and peek operations.

```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to top of stack - O(1)"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """Return top item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        """Check if stack is empty - O(1)"""
        return len(self.items) == 0
    
    def size(self):
        """Return number of items - O(1)"""
        return len(self.items)

# Data engineering use case: Processing nested data
def validate_json_brackets(json_string):
    """Validate if JSON has balanced brackets using stack."""
    stack = Stack()
    brackets = {'(': ')', '[': ']', '{': '}'}
    
    for char in json_string:
        if char in brackets:
            stack.push(char)
        elif char in brackets.values():
            if stack.is_empty():
                return False
            if brackets[stack.pop()] != char:
                return False
    
    return stack.is_empty()
```

### 3. Explain Queue and its applications in data processing
**Answer**: A Queue is a FIFO (First In, First Out) data structure used for managing data in order of arrival.

```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        """Add item to rear of queue - O(1)"""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return front item - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.popleft()
    
    def front(self):
        """Return front item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return len(self.items) == 0
    
    def size(self):
        """Return number of items - O(1)"""
        return len(self.items)

# Data engineering application: Task scheduling
class TaskScheduler:
    def __init__(self):
        self.task_queue = Queue()
        self.processing = False
    
    def add_task(self, task):
        """Add task to processing queue."""
        self.task_queue.enqueue(task)
        print(f"Task {task} added to queue")
    
    def process_tasks(self):
        """Process all tasks in FIFO order."""
        while not self.task_queue.is_empty():
            current_task = self.task_queue.dequeue()
            print(f"Processing task: {current_task}")
            # Simulate task processing
            time.sleep(1)
```

### 4. What is Binary Search and when would you use it?
**Answer**: Binary Search is an efficient algorithm for finding an element in a sorted array with O(log n) time complexity.

```python
def binary_search(arr, target):
    """
    Binary search implementation for sorted array.
    Returns index of target if found, -1 otherwise.
    """
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

def binary_search_recursive(arr, target, left=0, right=None):
    """Recursive implementation of binary search."""
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

# Data engineering use case: Finding data in sorted datasets
class DataIndex:
    def __init__(self, sorted_data):
        self.data = sorted_data
        self.keys = sorted(sorted_data.keys())
    
    def find_record(self, key):
        """Find record by key using binary search."""
        index = binary_search(self.keys, key)
        if index != -1:
            return self.data[self.keys[index]]
        return None
    
    def find_range(self, start_key, end_key):
        """Find all records in key range."""
        start_idx = self.find_first_occurrence(start_key)
        end_idx = self.find_last_occurrence(end_key)
        
        if start_idx == -1 or end_idx == -1:
            return []
        
        return [self.data[self.keys[i]] for i in range(start_idx, end_idx + 1)]
```

### 5. Explain Hash Tables and collision resolution
**Answer**: Hash Tables use hash functions to map keys to array indices for O(1) average-case access time.

```python
class HashTable:
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]  # Chaining for collision resolution
    
    def _hash(self, key):
        """Simple hash function."""
        return hash(key) % self.capacity
    
    def put(self, key, value):
        """Insert or update key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self.size += 1
        
        # Resize if load factor > 0.75
        if self.size > self.capacity * 0.75:
            self._resize()
    
    def get(self, key):
        """Retrieve value by key."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        raise KeyError(f"Key '{key}' not found")
    
    def delete(self, key):
        """Remove key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return v
        
        raise KeyError(f"Key '{key}' not found")
    
    def _resize(self):
        """Resize hash table when load factor is high."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        
        # Rehash all existing items
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

# Data engineering use case: Caching processed data
class DataCache:
    def __init__(self, max_size=1000):
        self.cache = HashTable()
        self.max_size = max_size
        self.access_order = []  # For LRU eviction
    
    def get_processed_data(self, data_key):
        """Get cached processed data or None if not found."""
        try:
            data = self.cache.get(data_key)
            # Move to end for LRU
            self.access_order.remove(data_key)
            self.access_order.append(data_key)
            return data
        except KeyError:
            return None
    
    def cache_processed_data(self, data_key, processed_data):
        """Cache processed data with LRU eviction."""
        if self.cache.size >= self.max_size:
            # Evict least recently used
            lru_key = self.access_order.pop(0)
            self.cache.delete(lru_key)
        
        self.cache.put(data_key, processed_data)
        self.access_order.append(data_key)
```

## Intermediate Level Questions (3-5 years experience)

### 6. Implement a Binary Search Tree with basic operations
**Answer**: BST maintains sorted order with left subtree < root < right subtree property.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        """Insert value into BST - O(log n) average, O(n) worst case."""
        self.root = self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        if not node:
            return TreeNode(val)
        
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        
        return node
    
    def search(self, val):
        """Search for value in BST - O(log n) average."""
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node, val):
        if not node or node.val == val:
            return node
        
        if val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def delete(self, val):
        """Delete value from BST - O(log n) average."""
        self.root = self._delete_recursive(self.root, val)
    
    def _delete_recursive(self, node, val):
        if not node:
            return node
        
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node to be deleted found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Node with two children
            min_node = self._find_min(node.right)
            node.val = min_node.val
            node.right = self._delete_recursive(node.right, min_node.val)
        
        return node
    
    def _find_min(self, node):
        """Find minimum value node in subtree."""
        while node.left:
            node = node.left
        return node
    
    def inorder_traversal(self):
        """Return sorted list of values - O(n)."""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)

# Data engineering use case: Indexing for range queries
class DataRangeIndex:
    def __init__(self):
        self.bst = BinarySearchTree()
        self.data_map = {}  # Maps values to actual data records
    
    def add_record(self, key, data):
        """Add data record with indexable key."""
        self.bst.insert(key)
        self.data_map[key] = data
    
    def find_records_in_range(self, min_key, max_key):
        """Find all records with keys in range [min_key, max_key]."""
        all_keys = self.bst.inorder_traversal()
        result = []
        
        for key in all_keys:
            if min_key <= key <= max_key:
                result.append(self.data_map[key])
            elif key > max_key:
                break
        
        return result
```

### 7. Explain different sorting algorithms and their use cases
**Answer**: Different sorting algorithms have different time/space complexities and are suitable for different scenarios.

```python
def bubble_sort(arr):
    """
    Bubble Sort - O(n²) time, O(1) space
    Good for: Small datasets, educational purposes
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # Optimization: early termination
            break
    return arr

def merge_sort(arr):
    """
    Merge Sort - O(n log n) time, O(n) space
    Good for: Large datasets, stable sorting, external sorting
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays."""
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

def quick_sort(arr):
    """
    Quick Sort - O(n log n) average, O(n²) worst case, O(log n) space
    Good for: General purpose, in-place sorting
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

def heap_sort(arr):
    """
    Heap Sort - O(n log n) time, O(1) space
    Good for: Guaranteed O(n log n), priority queue applications
    """
    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr

# Data engineering use case: Sorting large datasets
class DataSorter:
    def __init__(self):
        self.algorithms = {
            'merge': merge_sort,
            'quick': quick_sort,
            'heap': heap_sort
        }
    
    def sort_data(self, data, algorithm='merge', key_func=None):
        """Sort data using specified algorithm."""
        if key_func:
            # Sort by custom key function
            data_with_keys = [(key_func(item), item) for item in data]
            sorted_data = self.algorithms[algorithm](data_with_keys)
            return [item for key, item in sorted_data]
        else:
            return self.algorithms[algorithm](data.copy())
    
    def external_sort(self, large_dataset, chunk_size=1000):
        """Sort dataset too large for memory using external sorting."""
        # Split into chunks, sort each chunk
        sorted_chunks = []
        for i in range(0, len(large_dataset), chunk_size):
            chunk = large_dataset[i:i + chunk_size]
            sorted_chunk = merge_sort(chunk)
            sorted_chunks.append(sorted_chunk)
        
        # Merge all sorted chunks
        while len(sorted_chunks) > 1:
            merged_chunks = []
            for i in range(0, len(sorted_chunks), 2):
                if i + 1 < len(sorted_chunks):
                    merged = merge(sorted_chunks[i], sorted_chunks[i + 1])
                else:
                    merged = sorted_chunks[i]
                merged_chunks.append(merged)
            sorted_chunks = merged_chunks
        
        return sorted_chunks[0] if sorted_chunks else []
```

### 8. Implement a Graph and explain BFS vs DFS
**Answer**: Graphs represent relationships between entities. BFS explores level by level, DFS explores as deep as possible first.

```python
from collections import defaultdict, deque

class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v, weight=1):
        """Add edge between vertices u and v."""
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def bfs(self, start):
        """
        Breadth-First Search - explores level by level
        Time: O(V + E), Space: O(V)
        Use cases: Shortest path, level-order traversal
        """
        visited = set()
        queue = deque([start])
        result = []
        
        visited.add(start)
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def dfs(self, start):
        """
        Depth-First Search - explores as deep as possible
        Time: O(V + E), Space: O(V)
        Use cases: Topological sort, cycle detection, pathfinding
        """
        visited = set()
        result = []
        
        def dfs_recursive(vertex):
            visited.add(vertex)
            result.append(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start)
        return result
    
    def shortest_path(self, start, end):
        """Find shortest path using BFS (unweighted graph)."""
        if start == end:
            return [start]
        
        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None  # No path found
    
    def has_cycle(self):
        """Detect cycle in graph using DFS."""
        visited = set()
        rec_stack = set()
        
        def has_cycle_util(vertex):
            visited.add(vertex)
            rec_stack.add(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    if has_cycle_util(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(vertex)
            return False
        
        for vertex in self.graph:
            if vertex not in visited:
                if has_cycle_util(vertex):
                    return True
        
        return False

# Data engineering use case: Dependency resolution
class TaskDependencyGraph:
    def __init__(self):
        self.graph = Graph(directed=True)
        self.tasks = {}
    
    def add_task(self, task_id, task_data):
        """Add task to dependency graph."""
        self.tasks[task_id] = task_data
    
    def add_dependency(self, task_id, depends_on):
        """Add dependency: task_id depends on depends_on."""
        self.graph.add_edge(depends_on, task_id)
    
    def get_execution_order(self):
        """Get topological order for task execution."""
        in_degree = defaultdict(int)
        
        # Calculate in-degrees
        for vertex in self.graph.graph:
            for neighbor, _ in self.graph.graph[vertex]:
                in_degree[neighbor] += 1
        
        # Find vertices with no incoming edges
        queue = deque([v for v in self.tasks.keys() if in_degree[v] == 0])
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in self.graph.graph[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(self.tasks):
            raise ValueError("Circular dependency detected")
        
        return result
```

### 9. Explain Dynamic Programming with examples
**Answer**: Dynamic Programming solves complex problems by breaking them into simpler subproblems and storing results to avoid redundant calculations.

```python
def fibonacci_dp(n):
    """
    Fibonacci using Dynamic Programming
    Time: O(n), Space: O(n)
    """
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

def fibonacci_optimized(n):
    """
    Space-optimized Fibonacci
    Time: O(n), Space: O(1)
    """
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1

def longest_common_subsequence(text1, text2):
    """
    Find length of longest common subsequence
    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

def knapsack_01(weights, values, capacity):
    """
    0/1 Knapsack Problem using DP
    Time: O(n*W), Space: O(n*W)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w - weights[i-1]],  # Include item
                    dp[i-1][w]  # Exclude item
                )
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]

# Data engineering use case: Optimal resource allocation
class ResourceOptimizer:
    def __init__(self):
        self.memo = {}
    
    def optimize_batch_processing(self, jobs, resources, max_time):
        """
        Optimize job scheduling to maximize throughput within time limit.
        Similar to knapsack problem.
        """
        def dp(job_idx, remaining_resources, remaining_time):
            if job_idx >= len(jobs) or remaining_resources <= 0 or remaining_time <= 0:
                return 0
            
            key = (job_idx, remaining_resources, remaining_time)
            if key in self.memo:
                return self.memo[key]
            
            job = jobs[job_idx]
            
            # Option 1: Skip current job
            result = dp(job_idx + 1, remaining_resources, remaining_time)
            
            # Option 2: Process current job (if resources and time allow)
            if (job['resource_cost'] <= remaining_resources and 
                job['time_cost'] <= remaining_time):
                
                process_result = (job['value'] + 
                                dp(job_idx + 1, 
                                   remaining_resources - job['resource_cost'],
                                   remaining_time - job['time_cost']))
                result = max(result, process_result)
            
            self.memo[key] = result
            return result
        
        return dp(0, resources, max_time)
```

### 10. Implement a Trie (Prefix Tree) for string operations
**Answer**: Trie is a tree-like data structure for efficient string storage and retrieval, especially useful for prefix operations.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word_count = 0  # For counting word frequency

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert word into trie - O(m) where m is word length."""
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.word_count += 1
    
    def search(self, word):
        """Search for exact word - O(m)."""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix):
        """Check if any word starts with prefix - O(m)."""
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix):
        """Helper method to find node for given prefix."""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def get_words_with_prefix(self, prefix):
        """Get all words that start with given prefix."""
        prefix_node = self._find_node(prefix)
        if not prefix_node:
            return []
        
        words = []
        self._collect_words(prefix_node, prefix, words)
        return words
    
    def _collect_words(self, node, current_word, words):
        """Recursively collect all words from current node."""
        if node.is_end_of_word:
            words.append(current_word)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current_word + char, words)
    
    def delete(self, word):
        """Delete word from trie."""
        def _delete_recursive(node, word, index):
            if index == len(word):
                if not node.is_end_of_word:
                    return False  # Word doesn't exist
                
                node.is_end_of_word = False
                node.word_count = 0
                
                # Return True if node has no children (can be deleted)
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False  # Word doesn't exist
            
            child_node = node.children[char]
            should_delete_child = _delete_recursive(child_node, word, index + 1)
            
            if should_delete_child:
                del node.children[char]
                
                # Return True if current node can be deleted
                return (not node.is_end_of_word and 
                        len(node.children) == 0)
            
            return False
        
        _delete_recursive(self.root, word, 0)

# Data engineering use case: Auto-completion and search suggestions
class SearchSuggestionEngine:
    def __init__(self):
        self.trie = Trie()
        self.popularity_scores = {}
    
    def add_search_term(self, term, popularity_score=1):
        """Add search term with popularity score."""
        self.trie.insert(term.lower())
        self.popularity_scores[term.lower()] = popularity_score
    
    def get_suggestions(self, prefix, max_suggestions=10):
        """Get search suggestions for given prefix."""
        suggestions = self.trie.get_words_with_prefix(prefix.lower())
        
        # Sort by popularity score
        suggestions.sort(
            key=lambda x: self.popularity_scores.get(x, 0), 
            reverse=True
        )
        
        return suggestions[:max_suggestions]
    
    def update_popularity(self, term, score_increment=1):
        """Update popularity score when term is searched."""
        term_lower = term.lower()
        if self.trie.search(term_lower):
            self.popularity_scores[term_lower] = (
                self.popularity_scores.get(term_lower, 0) + score_increment
            )

# Usage example
def demonstrate_trie():
    engine = SearchSuggestionEngine()
    
    # Add search terms
    terms = [
        ("data engineering", 100),
        ("data science", 95),
        ("data analysis", 80),
        ("database design", 70),
        ("data warehouse", 85),
        ("data pipeline", 90)
    ]
    
    for term, score in terms:
        engine.add_search_term(term, score)
    
    # Get suggestions
    suggestions = engine.get_suggestions("data", 5)
    print(f"Suggestions for 'data': {suggestions}")
    
    # Update popularity and get new suggestions
    engine.update_popularity("data analysis", 20)
    new_suggestions = engine.get_suggestions("data", 5)
    print(f"Updated suggestions: {new_suggestions}")
```

This comprehensive set covers fundamental data structures and algorithms with practical data engineering applications, progressing from basic concepts to more advanced topics with real-world use cases.