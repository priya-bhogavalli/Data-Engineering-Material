# Time and Space Complexity Guide for Data Engineering

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [Big O Notation](#big-o-notation)
3. [Time Complexity](#time-complexity)
4. [Space Complexity](#space-complexity)
5. [Common Complexities](#common-complexities)
6. [Data Structure Complexities](#data-structure-complexities)
7. [Algorithm Complexities](#algorithm-complexities)
8. [Data Engineering Specific Examples](#data-engineering-specific-examples)
9. [Optimization Strategies](#optimization-strategies)
10. [Real-World Applications](#real-world-applications)

---

## 🎯 Introduction

Time and space complexity analysis is crucial for data engineers to:
- Design efficient data pipelines
- Optimize ETL processes
- Choose appropriate data structures
- Scale systems effectively
- Minimize resource consumption

## 📊 Big O Notation

Big O notation describes the upper bound of algorithm performance as input size grows.

### Common Big O Classifications
```
O(1)        - Constant time
O(log n)    - Logarithmic time
O(n)        - Linear time
O(n log n)  - Linearithmic time
O(n²)       - Quadratic time
O(n³)       - Cubic time
O(2ⁿ)       - Exponential time
O(n!)       - Factorial time
```

### Growth Rate Comparison
```
Input Size (n) | O(1) | O(log n) | O(n) | O(n log n) | O(n²) | O(2ⁿ)
1              | 1    | 1        | 1    | 1          | 1     | 2
10             | 1    | 3        | 10   | 33         | 100   | 1,024
100            | 1    | 7        | 100  | 664        | 10K   | 1.3×10³⁰
1,000          | 1    | 10       | 1K   | 9,966      | 1M    | ∞
1,000,000      | 1    | 20       | 1M   | 19.9M      | 1T    | ∞
```

## ⏱️ Time Complexity

Time complexity measures how execution time increases with input size.

### Analysis Rules
1. **Drop constants**: O(2n) → O(n)
2. **Drop lower-order terms**: O(n² + n) → O(n²)
3. **Consider worst case**: Focus on maximum possible operations
4. **Different inputs use different variables**: O(a + b) not O(n)

### Examples with Code

#### O(1) - Constant Time
```python
def get_first_element(arr):
    return arr[0] if arr else None
# Always takes same time regardless of array size
```

#### O(n) - Linear Time
```python
def find_max(arr):
    max_val = arr[0]
    for num in arr:  # n operations
        if num > max_val:
            max_val = num
    return max_val
# Time increases linearly with array size
```

#### O(n²) - Quadratic Time
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):        # n iterations
        for j in range(n-1):  # n iterations each
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
# Total: n × n = n² operations
```

#### O(log n) - Logarithmic Time
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
# Halves search space each iteration
```

## 💾 Space Complexity

Space complexity measures memory usage as input size grows.

### Types of Space Usage
1. **Input Space**: Memory for input data
2. **Auxiliary Space**: Extra memory used by algorithm
3. **Total Space**: Input + Auxiliary space

### Examples

#### O(1) - Constant Space
```python
def reverse_array_inplace(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
# Only uses two variables regardless of input size
```

#### O(n) - Linear Space
```python
def reverse_array_new(arr):
    return arr[::-1]  # Creates new array of size n
# Space usage grows linearly with input size
```

#### O(n) - Recursive Space
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
# Call stack grows to depth n
```

## 📈 Common Complexities

### Time Complexity Patterns

| Pattern | Complexity | Example |
|---------|------------|---------|
| Single loop | O(n) | Linear search |
| Nested loops | O(n²) | Bubble sort |
| Divide and conquer | O(n log n) | Merge sort |
| Binary operations | O(log n) | Binary search |
| Recursive with memoization | O(n) | Dynamic programming |
| Backtracking | O(2ⁿ) | Subset generation |

### Space Complexity Patterns

| Pattern | Complexity | Example |
|---------|------------|---------|
| Fixed variables | O(1) | In-place algorithms |
| Single array/list | O(n) | Copying data |
| 2D array | O(n²) | Matrix operations |
| Recursive calls | O(depth) | Tree traversal |
| Hash table | O(n) | Caching results |

## 🗃️ Data Structure Complexities

### Array/List Operations
| Operation | Time | Space |
|-----------|------|-------|
| Access by index | O(1) | O(1) |
| Search | O(n) | O(1) |
| Insert at end | O(1) | O(1) |
| Insert at beginning | O(n) | O(1) |
| Delete | O(n) | O(1) |

### Hash Table/Dictionary
| Operation | Average | Worst Case | Space |
|-----------|---------|------------|-------|
| Search | O(1) | O(n) | O(n) |
| Insert | O(1) | O(n) | O(n) |
| Delete | O(1) | O(n) | O(1) |

### Binary Search Tree
| Operation | Average | Worst Case | Space |
|-----------|---------|------------|-------|
| Search | O(log n) | O(n) | O(1) |
| Insert | O(log n) | O(n) | O(1) |
| Delete | O(log n) | O(n) | O(1) |

### Heap
| Operation | Time | Space |
|-----------|------|-------|
| Find min/max | O(1) | O(1) |
| Insert | O(log n) | O(1) |
| Delete min/max | O(log n) | O(1) |
| Build heap | O(n) | O(1) |

## 🔄 Algorithm Complexities

### Sorting Algorithms
| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |

### Search Algorithms
| Algorithm | Time | Space | Requirements |
|-----------|------|-------|--------------|
| Linear Search | O(n) | O(1) | None |
| Binary Search | O(log n) | O(1) | Sorted array |
| Hash Table Lookup | O(1) avg | O(n) | Hash function |

### Graph Algorithms
| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | O(V + E) | O(V) | Shortest path |
| DFS | O(V + E) | O(V) | Connectivity |
| Dijkstra | O((V + E) log V) | O(V) | Weighted shortest path |

## 🏭 Data Engineering Specific Examples

### ETL Pipeline Complexity Analysis

#### Data Loading - O(n)
```python
def load_csv_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:  # O(n) where n = number of rows
            data.append(parse_line(line))
    return data
# Time: O(n), Space: O(n)
```

#### Data Transformation - O(n)
```python
def transform_records(records):
    transformed = []
    for record in records:  # O(n)
        transformed_record = {
            'id': record['id'],
            'name': record['name'].upper(),
            'email': record['email'].lower(),
            'age': int(record['age'])
        }
        transformed.append(transformed_record)
    return transformed
# Time: O(n), Space: O(n)
```

#### Data Aggregation - O(n)
```python
def calculate_metrics(transactions):
    metrics = {}
    for transaction in transactions:  # O(n)
        customer_id = transaction['customer_id']
        amount = transaction['amount']
        
        if customer_id not in metrics:
            metrics[customer_id] = {'total': 0, 'count': 0}
        
        metrics[customer_id]['total'] += amount
        metrics[customer_id]['count'] += 1
    
    return metrics
# Time: O(n), Space: O(k) where k = unique customers
```

### Database Query Complexity

#### Index Lookup - O(log n)
```sql
-- B-tree index lookup
SELECT * FROM customers WHERE customer_id = 12345;
-- Time: O(log n), Space: O(1)
```

#### Full Table Scan - O(n)
```sql
-- No index available
SELECT * FROM customers WHERE email LIKE '%@gmail.com';
-- Time: O(n), Space: O(1)
```

#### Join Operations - O(n × m)
```sql
-- Nested loop join (worst case)
SELECT c.name, o.amount 
FROM customers c 
JOIN orders o ON c.id = o.customer_id;
-- Time: O(n × m), Space: O(1)
```

### Big Data Processing Complexity

#### MapReduce Word Count
```python
# Map phase - O(n)
def map_phase(documents):
    word_counts = []
    for doc in documents:  # O(n) documents
        for word in doc.split():  # O(w) words per doc
            word_counts.append((word, 1))
    return word_counts
# Time: O(n × w), Space: O(n × w)

# Reduce phase - O(n log n)
def reduce_phase(word_counts):
    from collections import defaultdict
    result = defaultdict(int)
    
    # Group by key (sorting) - O(n log n)
    word_counts.sort(key=lambda x: x[0])
    
    # Sum values - O(n)
    for word, count in word_counts:
        result[word] += count
    
    return result
# Time: O(n log n), Space: O(k) where k = unique words
```

### Streaming Data Processing

#### Sliding Window - O(w)
```python
from collections import deque

class SlidingWindowAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.window = deque()
        self.sum = 0
    
    def add_value(self, value):
        # Add new value - O(1)
        self.window.append(value)
        self.sum += value
        
        # Remove old values if window exceeds size - O(1)
        if len(self.window) > self.window_size:
            old_value = self.window.popleft()
            self.sum -= old_value
    
    def get_average(self):
        # Calculate average - O(1)
        return self.sum / len(self.window) if self.window else 0

# Time per operation: O(1), Space: O(w) where w = window size
```

## 🚀 Optimization Strategies

### Time Optimization Techniques

#### 1. Use Appropriate Data Structures
```python
# Slow: O(n) lookup in list
def find_user_slow(users_list, user_id):
    for user in users_list:  # O(n)
        if user['id'] == user_id:
            return user
    return None

# Fast: O(1) lookup in hash table
def find_user_fast(users_dict, user_id):
    return users_dict.get(user_id)  # O(1)
```

#### 2. Avoid Nested Loops
```python
# Slow: O(n²)
def find_common_elements_slow(list1, list2):
    common = []
    for item1 in list1:      # O(n)
        for item2 in list2:  # O(m)
            if item1 == item2:
                common.append(item1)
    return common

# Fast: O(n + m)
def find_common_elements_fast(list1, list2):
    set1 = set(list1)       # O(n)
    common = []
    for item in list2:      # O(m)
        if item in set1:    # O(1)
            common.append(item)
    return common
```

#### 3. Use Caching/Memoization
```python
# Without memoization: O(2ⁿ)
def fibonacci_slow(n):
    if n <= 1:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

# With memoization: O(n)
def fibonacci_fast(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_fast(n-1, memo) + fibonacci_fast(n-2, memo)
    return memo[n]
```

### Space Optimization Techniques

#### 1. In-Place Operations
```python
# Extra space: O(n)
def reverse_new_array(arr):
    return arr[::-1]

# In-place: O(1)
def reverse_in_place(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

#### 2. Generators for Large Datasets
```python
# Memory intensive: O(n)
def process_large_file_list(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(process_line(line))
    return lines

# Memory efficient: O(1)
def process_large_file_generator(filename):
    with open(filename) as f:
        for line in f:
            yield process_line(line)
```

## 🌍 Real-World Applications

### Data Pipeline Optimization

#### Batch Processing
```python
# Process records in batches to balance memory usage
def process_large_dataset(data_source, batch_size=1000):
    batch = []
    for record in data_source:
        batch.append(record)
        
        if len(batch) >= batch_size:
            process_batch(batch)  # O(batch_size)
            batch = []  # Reset batch
    
    # Process remaining records
    if batch:
        process_batch(batch)

# Time: O(n), Space: O(batch_size)
```

#### Parallel Processing
```python
from multiprocessing import Pool

def parallel_data_processing(data_chunks, num_processes=4):
    with Pool(num_processes) as pool:
        results = pool.map(process_chunk, data_chunks)
    return results

# Time: O(n/p) where p = number of processes
# Space: O(n) total, O(n/p) per process
```

### Database Performance

#### Query Optimization
```sql
-- Slow: Full table scan O(n)
SELECT * FROM orders WHERE order_date > '2023-01-01';

-- Fast: Index scan O(log n)
CREATE INDEX idx_order_date ON orders(order_date);
SELECT * FROM orders WHERE order_date > '2023-01-01';
```

#### Partitioning Strategy
```sql
-- Partition by date for time-series data
CREATE TABLE orders_partitioned (
    order_id INT,
    order_date DATE,
    amount DECIMAL
) PARTITION BY RANGE (order_date);

-- Query only relevant partitions: O(n/p) where p = partitions
SELECT * FROM orders_partitioned 
WHERE order_date BETWEEN '2023-01-01' AND '2023-01-31';
```

### Streaming Analytics

#### Real-time Aggregation
```python
class RealTimeMetrics:
    def __init__(self):
        self.counters = {}
        self.sums = {}
    
    def update_metric(self, key, value):
        # O(1) operations
        self.counters[key] = self.counters.get(key, 0) + 1
        self.sums[key] = self.sums.get(key, 0) + value
    
    def get_average(self, key):
        # O(1) calculation
        if key in self.counters and self.counters[key] > 0:
            return self.sums[key] / self.counters[key]
        return 0

# Time per operation: O(1)
# Space: O(k) where k = unique keys
```

## 📚 Key Takeaways

### For Data Engineers:

1. **Choose the right data structure** for your use case
2. **Analyze complexity** before implementing solutions
3. **Consider both time and space** trade-offs
4. **Use indexing** for frequent lookups
5. **Implement caching** for expensive operations
6. **Process data in batches** for large datasets
7. **Leverage parallel processing** when possible
8. **Monitor performance** in production systems

### Common Pitfalls:

1. **Premature optimization** - Profile first, optimize second
2. **Ignoring space complexity** - Memory can be more expensive than time
3. **Not considering average case** - Focus on typical scenarios
4. **Over-engineering** - Simple solutions often work best
5. **Forgetting about constants** - Big O hides constant factors

### Best Practices:

1. **Measure actual performance** with real data
2. **Use appropriate tools** for profiling
3. **Document complexity** in code comments
4. **Test with various input sizes**
5. **Consider scalability** from the beginning
6. **Balance readability** with performance
7. **Keep learning** about new algorithms and techniques

---

*Remember: The best algorithm is the one that solves your specific problem efficiently within your constraints.*