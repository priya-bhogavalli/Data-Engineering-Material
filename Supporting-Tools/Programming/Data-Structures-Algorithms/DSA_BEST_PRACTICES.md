# Data Structures & Algorithms Best Practices

## Problem-Solving Framework

### 1. UMPIRE Method
**U**nderstand → **M**atch → **P**lan → **I**mplement → **R**eview → **E**valuate

#### Understand
- Read the problem carefully
- Identify inputs, outputs, and constraints
- Consider edge cases
- Ask clarifying questions

```python
# Example: Two Sum Problem
def understand_two_sum():
    """
    Problem: Find two numbers that add up to target
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1] (indices of 2 and 7)
    
    Constraints:
    - Each input has exactly one solution
    - Can't use same element twice
    - Return indices, not values
    
    Edge cases:
    - Empty array
    - Array with one element
    - No solution (though problem states there's always one)
    - Negative numbers
    - Duplicate numbers
    """
    pass
```

#### Match
- Identify the problem pattern
- Choose appropriate data structures and algorithms

```python
# Common patterns for Two Sum:
# 1. Brute Force - O(n²)
# 2. Hash Table - O(n)
# 3. Two Pointers (if sorted) - O(n log n)

def match_pattern():
    """
    Two Sum matches:
    - Hash Table pattern (complement lookup)
    - Array traversal pattern
    - Index tracking requirement
    """
    pass
```

#### Plan
- Write pseudocode
- Consider time/space complexity
- Think about edge cases

```python
def plan_two_sum():
    """
    Plan for Hash Table approach:
    1. Create hash table to store {value: index}
    2. For each number in array:
       a. Calculate complement = target - current_number
       b. If complement exists in hash table:
          - Return [hash_table[complement], current_index]
       c. Otherwise, add current number to hash table
    
    Time: O(n), Space: O(n)
    """
    pass
```

### 2. Code Quality Best Practices

#### Clean Code Principles
```python
# Bad: Unclear variable names and logic
def solve(a, t):
    d = {}
    for i in range(len(a)):
        c = t - a[i]
        if c in d:
            return [d[c], i]
        d[a[i]] = i
    return []

# Good: Clear names and structure
def two_sum(nums, target):
    """
    Find two numbers in array that sum to target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List of two indices whose values sum to target
    
    Raises:
        ValueError: If no solution exists
    """
    complement_map = {}
    
    for current_index, current_num in enumerate(nums):
        complement = target - current_num
        
        if complement in complement_map:
            return [complement_map[complement], current_index]
        
        complement_map[current_num] = current_index
    
    raise ValueError("No two sum solution exists")
```

#### Error Handling
```python
def robust_binary_search(arr, target):
    """Binary search with proper error handling."""
    if not arr:
        raise ValueError("Array cannot be empty")
    
    if not isinstance(target, (int, float)):
        raise TypeError("Target must be a number")
    
    # Check if array is sorted
    if not all(arr[i] <= arr[i+1] for i in range(len(arr)-1)):
        raise ValueError("Array must be sorted for binary search")
    
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

#### Input Validation
```python
def validate_inputs(func):
    """Decorator for input validation."""
    def wrapper(*args, **kwargs):
        # Add validation logic here
        return func(*args, **kwargs)
    return wrapper

@validate_inputs
def merge_sorted_arrays(arr1, arr2):
    """Merge two sorted arrays with validation."""
    if not isinstance(arr1, list) or not isinstance(arr2, list):
        raise TypeError("Both inputs must be lists")
    
    if not all(isinstance(x, (int, float)) for x in arr1 + arr2):
        raise TypeError("All elements must be numbers")
    
    # Implementation here
    result = []
    i = j = 0
    
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    
    return result
```

## Performance Optimization

### 1. Time Complexity Optimization

#### Choose Right Data Structure
```python
# Bad: Using list for frequent lookups - O(n)
def find_duplicates_slow(nums):
    duplicates = []
    for i, num in enumerate(nums):
        if num in nums[:i]:  # O(n) lookup each time
            duplicates.append(num)
    return duplicates

# Good: Using set for O(1) lookups
def find_duplicates_fast(nums):
    seen = set()
    duplicates = set()
    
    for num in nums:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)
```

#### Avoid Unnecessary Operations
```python
# Bad: Recalculating same values
def fibonacci_slow(n):
    if n <= 1:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)  # Exponential time

# Good: Memoization
def fibonacci_fast(n, memo={}):
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_fast(n-1, memo) + fibonacci_fast(n-2, memo)
    return memo[n]

# Better: Iterative approach
def fibonacci_optimal(n):
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1
```

### 2. Space Complexity Optimization

#### In-place Operations
```python
# Space-inefficient: Creating new array
def reverse_array_new(arr):
    return arr[::-1]  # O(n) extra space

# Space-efficient: In-place reversal
def reverse_array_inplace(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    
    return arr  # O(1) extra space
```

#### Generator for Large Datasets
```python
# Memory-inefficient: Loading all data
def process_large_file_bad(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()  # Loads entire file into memory
    
    processed = []
    for line in lines:
        processed.append(process_line(line))
    
    return processed

# Memory-efficient: Using generators
def process_large_file_good(filename):
    with open(filename, 'r') as f:
        for line in f:  # Processes one line at a time
            yield process_line(line.strip())

def process_line(line):
    return line.upper()
```

## Testing Best Practices

### 1. Comprehensive Test Cases

#### Edge Cases Testing
```python
import unittest

class TestBinarySearch(unittest.TestCase):
    def setUp(self):
        self.binary_search = binary_search
    
    def test_normal_cases(self):
        """Test normal functionality."""
        arr = [1, 3, 5, 7, 9, 11]
        self.assertEqual(self.binary_search(arr, 5), 2)
        self.assertEqual(self.binary_search(arr, 1), 0)
        self.assertEqual(self.binary_search(arr, 11), 5)
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Empty array
        self.assertEqual(self.binary_search([], 5), -1)
        
        # Single element - found
        self.assertEqual(self.binary_search([5], 5), 0)
        
        # Single element - not found
        self.assertEqual(self.binary_search([5], 3), -1)
        
        # Target not in array
        arr = [1, 3, 5, 7, 9]
        self.assertEqual(self.binary_search(arr, 4), -1)
        self.assertEqual(self.binary_search(arr, 0), -1)
        self.assertEqual(self.binary_search(arr, 10), -1)
    
    def test_boundary_conditions(self):
        """Test boundary conditions."""
        arr = [1, 2, 3, 4, 5]
        
        # First element
        self.assertEqual(self.binary_search(arr, 1), 0)
        
        # Last element
        self.assertEqual(self.binary_search(arr, 5), 4)
        
        # Middle element
        self.assertEqual(self.binary_search(arr, 3), 2)
```

#### Property-Based Testing
```python
import random
from hypothesis import given, strategies as st

class TestSortingAlgorithm(unittest.TestCase):
    
    @given(st.lists(st.integers()))
    def test_sort_properties(self, arr):
        """Test sorting algorithm properties."""
        original_length = len(arr)
        original_elements = sorted(arr)  # Python's built-in sort for comparison
        
        result = quick_sort(arr.copy())
        
        # Property 1: Length should be preserved
        self.assertEqual(len(result), original_length)
        
        # Property 2: Result should be sorted
        self.assertEqual(result, sorted(result))
        
        # Property 3: Same elements should be present
        self.assertEqual(sorted(result), original_elements)
    
    @given(st.lists(st.integers(), min_size=1))
    def test_sort_non_empty(self, arr):
        """Test sorting with non-empty arrays."""
        result = quick_sort(arr)
        
        # Should be sorted
        for i in range(len(result) - 1):
            self.assertLessEqual(result[i], result[i + 1])
```

### 2. Performance Testing

#### Benchmarking
```python
import time
import random
from functools import wraps

def benchmark(func):
    """Decorator to benchmark function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds")
        return result
    
    return wrapper

@benchmark
def test_sorting_performance():
    """Compare different sorting algorithms."""
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        arr = [random.randint(1, 1000) for _ in range(size)]
        
        print(f"\nTesting with array size: {size}")
        
        # Test different algorithms
        bubble_sort(arr.copy())
        merge_sort(arr.copy())
        quick_sort(arr.copy())
```

## Data Engineering Specific Best Practices

### 1. Memory-Efficient Processing

#### Streaming Data Processing
```python
def process_large_dataset_streaming(data_source):
    """Process large dataset without loading everything into memory."""
    
    def chunk_processor(chunk_size=1000):
        chunk = []
        
        for record in data_source:
            chunk.append(record)
            
            if len(chunk) >= chunk_size:
                yield process_chunk(chunk)
                chunk = []
        
        # Process remaining records
        if chunk:
            yield process_chunk(chunk)
    
    # Process chunks and aggregate results
    total_processed = 0
    for processed_chunk in chunk_processor():
        total_processed += len(processed_chunk)
        # Write chunk to output or further processing
        write_chunk_to_output(processed_chunk)
    
    return total_processed

def process_chunk(chunk):
    """Process a chunk of data."""
    return [transform_record(record) for record in chunk]

def transform_record(record):
    """Transform individual record."""
    # Apply transformations
    return record
```

#### External Sorting for Large Files
```python
import heapq
import tempfile
import os

def external_sort(input_file, output_file, chunk_size=1000000):
    """Sort large file that doesn't fit in memory."""
    
    # Phase 1: Split into sorted chunks
    chunk_files = []
    
    with open(input_file, 'r') as f:
        chunk_num = 0
        
        while True:
            chunk = []
            
            # Read chunk
            for _ in range(chunk_size):
                line = f.readline()
                if not line:
                    break
                chunk.append(line.strip())
            
            if not chunk:
                break
            
            # Sort chunk and write to temporary file
            chunk.sort()
            chunk_file = f"temp_chunk_{chunk_num}.txt"
            chunk_files.append(chunk_file)
            
            with open(chunk_file, 'w') as cf:
                for item in chunk:
                    cf.write(f"{item}\n")
            
            chunk_num += 1
    
    # Phase 2: Merge sorted chunks
    merge_sorted_files(chunk_files, output_file)
    
    # Cleanup temporary files
    for chunk_file in chunk_files:
        os.remove(chunk_file)

def merge_sorted_files(file_list, output_file):
    """Merge multiple sorted files into one sorted file."""
    file_handles = []
    heap = []
    
    try:
        # Open all files and initialize heap
        for i, filename in enumerate(file_list):
            f = open(filename, 'r')
            file_handles.append(f)
            
            line = f.readline().strip()
            if line:
                heapq.heappush(heap, (line, i))
        
        # Merge files
        with open(output_file, 'w') as out_f:
            while heap:
                value, file_idx = heapq.heappop(heap)
                out_f.write(f"{value}\n")
                
                # Read next line from same file
                next_line = file_handles[file_idx].readline().strip()
                if next_line:
                    heapq.heappush(heap, (next_line, file_idx))
    
    finally:
        # Close all file handles
        for f in file_handles:
            f.close()
```

### 2. Fault Tolerance

#### Retry Logic with Exponential Backoff
```python
import time
import random
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """Decorator for retry logic with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise e
                    
                    # Calculate delay with jitter
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    jitter = random.uniform(0, 0.1) * delay
                    time.sleep(delay + jitter)
                    
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def unreliable_data_fetch(url):
    """Simulate unreliable data fetching."""
    # This might fail due to network issues
    import requests
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

#### Circuit Breaker Pattern
```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=30)

def protected_api_call():
    return circuit_breaker.call(unreliable_data_fetch, "https://api.example.com/data")
```

### 3. Monitoring and Observability

#### Performance Metrics Collection
```python
import time
from collections import defaultdict
from contextlib import contextmanager

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
    
    @contextmanager
    def timer(self, operation_name):
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.metrics[f"{operation_name}_duration"].append(duration)
            self.counters[f"{operation_name}_count"] += 1
    
    def increment_counter(self, counter_name):
        self.counters[counter_name] += 1
    
    def get_stats(self):
        stats = {}
        
        for metric_name, values in self.metrics.items():
            if values:
                stats[metric_name] = {
                    'count': len(values),
                    'avg': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values)
                }
        
        stats.update(dict(self.counters))
        return stats

# Usage
monitor = PerformanceMonitor()

def monitored_data_processing(data):
    with monitor.timer("data_processing"):
        # Process data
        processed_data = []
        
        for record in data:
            with monitor.timer("record_processing"):
                try:
                    processed_record = process_record(record)
                    processed_data.append(processed_record)
                    monitor.increment_counter("records_processed")
                except Exception as e:
                    monitor.increment_counter("processing_errors")
                    raise
    
    return processed_data
```

Remember: The key to mastering DSA is consistent practice and understanding the underlying principles rather than memorizing solutions. Focus on problem patterns and choose the right tool for each specific use case.