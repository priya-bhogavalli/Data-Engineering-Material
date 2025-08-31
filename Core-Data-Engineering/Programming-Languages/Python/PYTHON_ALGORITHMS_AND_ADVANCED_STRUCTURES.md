# Python Algorithms and Advanced Data Structures for Data Engineering

## Table of Contents

1. [Algorithm Fundamentals](#algorithm-fundamentals)
   - [Time and Space Complexity](#time-and-space-complexity)
   - [Big O Notation](#big-o-notation)
2. [Searching Algorithms](#searching-algorithms)
   - [Binary Search](#binary-search)
   - [Hash-based Search](#hash-based-search)
3. [Sorting Algorithms](#sorting-algorithms)
   - [Built-in Sorting](#built-in-sorting)
   - [Custom Sorting](#custom-sorting)
4. [Graph Algorithms](#graph-algorithms)
   - [Graph Representation](#graph-representation)
   - [BFS and DFS](#bfs-and-dfs)
5. [Streaming Algorithms](#streaming-algorithms)
   - [Reservoir Sampling](#reservoir-sampling)
   - [Count-Min Sketch](#count-min-sketch)
   - [HyperLogLog](#hyperloglog)
6. [Advanced Data Structures](#advanced-data-structures)
   - [Trie (Prefix Tree)](#trie-prefix-tree)
   - [Union-Find](#union-find)
7. [Data Engineering Patterns](#data-engineering-patterns)
   - [Sliding Window](#sliding-window)
   - [Two Pointers](#two-pointers)

---

## Algorithm Fundamentals

### Time and Space Complexity

**Big O Notation for Data Engineering**:

| Complexity | Example | Data Engineering Use Case |
|------------|---------|---------------------------|
| O(1) | Hash lookup | Cache access, dictionary lookup |
| O(log n) | Binary search | Searching sorted data |
| O(n) | Linear scan | Data validation, filtering |
| O(n log n) | Merge sort | Sorting large datasets |
| O(n²) | Nested loops | Avoid in production! |

```python
import time
from typing import List

def complexity_examples():
    """Demonstrate different time complexities."""
    
    # O(1) - Constant time
    def hash_lookup(data_dict: dict, key: str):
        return data_dict.get(key)
    
    # O(log n) - Binary search
    def binary_search(arr: List[int], target: int) -> int:
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
    
    # O(n) - Linear scan
    def find_max(data: List[int]) -> int:
        max_val = data[0]
        for val in data:
            if val > max_val:
                max_val = val
        return max_val
    
    # Test with different sizes
    sizes = [1000, 10000, 100000]
    
    for size in sizes:
        data = list(range(size))
        data_dict = {i: f"value_{i}" for i in range(size)}
        
        # O(1) operation
        start = time.time()
        result = hash_lookup(data_dict, size // 2)
        o1_time = time.time() - start
        
        # O(log n) operation
        start = time.time()
        result = binary_search(data, size // 2)
        olog_time = time.time() - start
        
        # O(n) operation
        start = time.time()
        result = find_max(data)
        on_time = time.time() - start
        
        print(f"Size {size:6d}: O(1)={o1_time:.6f}s, O(log n)={olog_time:.6f}s, O(n)={on_time:.6f}s")

complexity_examples()
# Output: Size   1000: O(1)=0.000001s, O(log n)=0.000008s, O(n)=0.000089s
# Output: Size  10000: O(1)=0.000001s, O(log n)=0.000009s, O(n)=0.000856s
# Output: Size 100000: O(1)=0.000001s, O(log n)=0.000011s, O(n)=0.008234s
```

## Searching Algorithms

### Binary Search

```python
def binary_search_variations():
    """Binary search patterns for data engineering."""
    
    def find_first_occurrence(arr: List[int], target: int) -> int:
        """Find first occurrence of target."""
        left, right = 0, len(arr) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                result = mid
                right = mid - 1  # Continue searching left
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result
    
    def find_insertion_point(arr: List[int], target: int) -> int:
        """Find where to insert target to maintain sorted order."""
        left, right = 0, len(arr)
        while left < right:
            mid = (left + right) // 2
            if arr[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left
    
    # Time-series data search example
    timestamps = [1000, 1100, 1200, 1300, 1400, 1500]
    values = [23.5, 24.1, 23.8, 25.2, 24.7, 23.9]
    
    # Find data in time range
    start_time, end_time = 1150, 1350
    start_idx = find_insertion_point(timestamps, start_time)
    end_idx = find_insertion_point(timestamps, end_time + 1)
    
    range_data = list(zip(timestamps[start_idx:end_idx], values[start_idx:end_idx]))
    print(f"Data in range {start_time}-{end_time}: {range_data}")
    # Output: Data in range 1150-1350: [(1200, 23.8), (1300, 25.2)]

binary_search_variations()
```

## Sorting Algorithms

### Custom Sorting for Data Engineering

```python
def data_engineering_sorting():
    """Sorting patterns common in data processing."""
    
    # Sample data
    transactions = [
        {"id": 1, "amount": 100.0, "timestamp": 1000, "user_id": "user1"},
        {"id": 2, "amount": 250.0, "timestamp": 1001, "user_id": "user2"},
        {"id": 3, "amount": 75.0, "timestamp": 999, "user_id": "user1"},
    ]
    
    # Sort by timestamp (chronological processing)
    by_time = sorted(transactions, key=lambda x: x["timestamp"])
    print("Sorted by timestamp:")
    for txn in by_time:
        print(f"  {txn['timestamp']}: ${txn['amount']}")
    # Output: Sorted by timestamp:
    # Output:   999: $75.0
    # Output:   1000: $100.0
    # Output:   1001: $250.0
    
    # Sort by multiple criteria (user_id, then amount desc)
    by_user_amount = sorted(transactions, 
                           key=lambda x: (x["user_id"], -x["amount"]))
    print("\nSorted by user_id, then amount (desc):")
    for txn in by_user_amount:
        print(f"  {txn['user_id']}: ${txn['amount']}")
    # Output: Sorted by user_id, then amount (desc):
    # Output:   user1: $100.0
    # Output:   user1: $75.0
    # Output:   user2: $250.0
    
    # Top-K sorting (most efficient for large datasets)
    import heapq
    top_3_amounts = heapq.nlargest(3, transactions, key=lambda x: x["amount"])
    print(f"\nTop 3 by amount: {[t['amount'] for t in top_3_amounts]}")
    # Output: Top 3 by amount: [250.0, 100.0, 75.0]

data_engineering_sorting()
```

## Graph Algorithms

### Graph Representation and Traversal

```python
from collections import defaultdict, deque

class DataPipelineGraph:
    """Graph for representing data pipeline dependencies."""
    
    def __init__(self):
        self.graph = defaultdict(list)
        self.nodes = set()
    
    def add_dependency(self, source: str, target: str):
        """Add dependency: target depends on source."""
        self.graph[source].append(target)
        self.nodes.add(source)
        self.nodes.add(target)
    
    def topological_sort(self) -> List[str]:
        """Get execution order for pipeline stages."""
        in_degree = {node: 0 for node in self.nodes}
        
        # Calculate in-degrees
        for node in self.nodes:
            for neighbor in self.graph[node]:
                in_degree[neighbor] += 1
        
        # Start with nodes having no dependencies
        queue = deque([node for node in self.nodes if in_degree[node] == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            # Remove this node and update dependencies
            for neighbor in self.graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result if len(result) == len(self.nodes) else []
    
    def find_dependencies(self, target: str) -> List[str]:
        """Find all stages that target depends on (BFS)."""
        if target not in self.nodes:
            return []
        
        # Reverse graph to find dependencies
        reverse_graph = defaultdict(list)
        for source in self.graph:
            for dest in self.graph[source]:
                reverse_graph[dest].append(source)
        
        visited = set()
        queue = deque([target])
        dependencies = []
        
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                if node != target:  # Don't include target itself
                    dependencies.append(node)
                
                for dependency in reverse_graph[node]:
                    if dependency not in visited:
                        queue.append(dependency)
        
        return dependencies

# Example: Data pipeline dependency management
pipeline = DataPipelineGraph()

# Define pipeline stages and dependencies
dependencies = [
    ("extract_raw", "clean_data"),
    ("clean_data", "validate_data"),
    ("validate_data", "transform_data"),
    ("transform_data", "load_warehouse"),
    ("clean_data", "backup_raw"),  # Parallel branch
    ("backup_raw", "archive_data")
]

for source, target in dependencies:
    pipeline.add_dependency(source, target)

# Get execution order
execution_order = pipeline.topological_sort()
print(f"Pipeline execution order: {execution_order}")
# Output: Pipeline execution order: ['extract_raw', 'clean_data', 'validate_data', 'backup_raw', 'transform_data', 'archive_data', 'load_warehouse']

# Find what load_warehouse depends on
deps = pipeline.find_dependencies("load_warehouse")
print(f"load_warehouse depends on: {deps}")
# Output: load_warehouse depends on: ['transform_data', 'validate_data', 'clean_data', 'extract_raw']
```

## Streaming Algorithms

### Reservoir Sampling

```python
import random

def reservoir_sampling(stream, k: int):
    """Sample k items uniformly from stream of unknown size."""
    reservoir = []
    
    for i, item in enumerate(stream):
        if len(reservoir) < k:
            reservoir.append(item)
        else:
            # Replace with probability k/(i+1)
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item
    
    return reservoir

# Example: Sample from large dataset
large_dataset = [f"record_{i}" for i in range(100000)]
sample = reservoir_sampling(large_dataset, 100)
print(f"Sampled {len(sample)} records from {len(large_dataset)} total")
# Output: Sampled 100 records from 100000 total
```

### Count-Min Sketch

```python
class CountMinSketch:
    """Approximate frequency counting for streams."""
    
    def __init__(self, width: int = 1000, depth: int = 5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
    
    def _hash(self, item: str, seed: int) -> int:
        return hash(f"{item}_{seed}") % self.width
    
    def add(self, item: str, count: int = 1):
        """Add item to sketch."""
        for i in range(self.depth):
            j = self._hash(item, i)
            self.table[i][j] += count
    
    def estimate(self, item: str) -> int:
        """Estimate frequency of item."""
        return min(
            self.table[i][self._hash(item, i)]
            for i in range(self.depth)
        )

# Example: Track page view frequencies
cms = CountMinSketch()

# Simulate page views
page_views = ["home"] * 1000 + ["about"] * 500 + ["contact"] * 200
random.shuffle(page_views)

for page in page_views:
    cms.add(page)

# Estimate frequencies
for page in ["home", "about", "contact"]:
    estimated = cms.estimate(page)
    actual = page_views.count(page)
    print(f"{page}: actual={actual}, estimated={estimated}")
# Output: home: actual=1000, estimated=1000
# Output: about: actual=500, estimated=500
# Output: contact: actual=200, estimated=200
```

## Advanced Data Structures

### Trie (Prefix Tree)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_word = False
        self.frequency = 0

class Trie:
    """Trie for autocomplete and prefix matching."""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str, frequency: int = 1):
        """Insert word with frequency."""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_word = True
        node.frequency += frequency
    
    def search_prefix(self, prefix: str) -> List[str]:
        """Find all words with given prefix."""
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all words from this node
        words = []
        self._collect_words(node, prefix.lower(), words)
        
        # Sort by frequency (descending)
        words.sort(key=lambda x: x[1], reverse=True)
        return [word for word, freq in words]
    
    def _collect_words(self, node: TrieNode, prefix: str, words: List):
        if node.is_end_word:
            words.append((prefix, node.frequency))
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, words)

# Example: Search query autocomplete
trie = Trie()

# Add search queries with frequencies
queries = [
    ("python tutorial", 1000),
    ("python data structures", 800),
    ("python algorithms", 600),
    ("java tutorial", 500),
    ("javascript basics", 400)
]

for query, freq in queries:
    trie.insert(query, freq)

# Get suggestions for "python"
suggestions = trie.search_prefix("python")
print(f"Suggestions for 'python': {suggestions}")
# Output: Suggestions for 'python': ['python tutorial', 'python data structures', 'python algorithms']
```

## Data Engineering Patterns

### Sliding Window

```python
from collections import deque

class SlidingWindow:
    """Sliding window for stream processing."""
    
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window = deque()
        self.sum = 0
    
    def add(self, value: float) -> dict:
        """Add value and return window statistics."""
        # Remove old values outside window
        if len(self.window) >= self.window_size:
            old_value = self.window.popleft()
            self.sum -= old_value
        
        # Add new value
        self.window.append(value)
        self.sum += value
        
        return {
            'count': len(self.window),
            'sum': self.sum,
            'average': self.sum / len(self.window),
            'min': min(self.window),
            'max': max(self.window)
        }

# Example: Real-time metrics
window = SlidingWindow(5)
metrics = [23.5, 24.1, 23.8, 25.2, 24.7, 23.9, 24.3]

print("Sliding window metrics:")
for i, metric in enumerate(metrics):
    stats = window.add(metric)
    print(f"Value {i+1}: {metric} -> Avg: {stats['average']:.2f}")
# Output: Sliding window metrics:
# Output: Value 1: 23.5 -> Avg: 23.50
# Output: Value 2: 24.1 -> Avg: 23.80
# Output: Value 3: 23.8 -> Avg: 23.80
# Output: Value 4: 25.2 -> Avg: 24.15
# Output: Value 5: 24.7 -> Avg: 24.26
# Output: Value 6: 23.9 -> Avg: 24.34
# Output: Value 7: 24.3 -> Avg: 24.38
```

### Two Pointers Technique

```python
def two_pointers_examples():
    """Two pointers technique for data processing."""
    
    def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
        """Merge two sorted arrays efficiently."""
        result = []
        i = j = 0
        
        while i < len(arr1) and j < len(arr2):
            if arr1[i] <= arr2[j]:
                result.append(arr1[i])
                i += 1
            else:
                result.append(arr2[j])
                j += 1
        
        # Add remaining elements
        result.extend(arr1[i:])
        result.extend(arr2[j:])
        return result
    
    def find_pairs_with_sum(arr: List[int], target: int) -> List[tuple]:
        """Find all pairs that sum to target."""
        arr.sort()  # Two pointers requires sorted array
        pairs = []
        left, right = 0, len(arr) - 1
        
        while left < right:
            current_sum = arr[left] + arr[right]
            if current_sum == target:
                pairs.append((arr[left], arr[right]))
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return pairs
    
    # Example: Merge sorted transaction logs
    log1 = [1000, 1002, 1005, 1008]  # Timestamps from server 1
    log2 = [1001, 1003, 1006, 1009]  # Timestamps from server 2
    
    merged_logs = merge_sorted_arrays(log1, log2)
    print(f"Merged logs: {merged_logs}")
    # Output: Merged logs: [1000, 1001, 1002, 1003, 1005, 1006, 1008, 1009]
    
    # Example: Find transaction pairs that sum to specific amount
    amounts = [100, 200, 300, 400, 500]
    target_sum = 600
    
    pairs = find_pairs_with_sum(amounts, target_sum)
    print(f"Pairs summing to {target_sum}: {pairs}")
    # Output: Pairs summing to 600: [(100, 500), (200, 400)]

two_pointers_examples()
```

## Performance Guidelines

### Algorithm Selection Matrix

| Data Size | Search | Sort | Distinct Count | Frequency Count |
|-----------|--------|------|----------------|-----------------|
| < 1K | Linear | Any | Set | Counter |
| 1K - 1M | Binary/Hash | Timsort | Set | Counter |
| > 1M | Hash/Index | External | HyperLogLog | Count-Min Sketch |

### Memory vs Time Tradeoffs

```python
def performance_comparison():
    """Compare different approaches for common tasks."""
    
    # Task: Find duplicates in large dataset
    data = list(range(100000)) + list(range(50000))  # 50K duplicates
    
    # Method 1: Set-based (fast, more memory)
    start = time.time()
    seen = set()
    duplicates_set = []
    for item in data:
        if item in seen:
            duplicates_set.append(item)
        else:
            seen.add(item)
    set_time = time.time() - start
    
    # Method 2: Sorting-based (slower, less memory)
    start = time.time()
    sorted_data = sorted(data)
    duplicates_sort = []
    for i in range(1, len(sorted_data)):
        if sorted_data[i] == sorted_data[i-1]:
            duplicates_sort.append(sorted_data[i])
    sort_time = time.time() - start
    
    print(f"Set method: {set_time:.4f}s, {len(duplicates_set)} duplicates")
    print(f"Sort method: {sort_time:.4f}s, {len(duplicates_sort)} duplicates")
    print(f"Speed ratio: {sort_time/set_time:.1f}x")
    # Output: Set method: 0.0123s, 50000 duplicates
    # Output: Sort method: 0.0456s, 50000 duplicates
    # Output: Speed ratio: 3.7x

performance_comparison()
```

This document provides essential algorithms and advanced data structures specifically tailored for data engineering use cases, with practical examples and performance considerations.