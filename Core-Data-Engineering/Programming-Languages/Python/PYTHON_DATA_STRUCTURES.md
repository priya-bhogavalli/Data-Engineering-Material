# Python Data Structures

## Built-in Data Structures

### 1. Lists
**Ordered, mutable collection**
```python
# Creation
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# Operations
numbers.append(6)           # Add to end
numbers.insert(0, 0)        # Insert at index
numbers.remove(3)           # Remove first occurrence
popped = numbers.pop()      # Remove and return last
numbers[1:3] = [10, 20]     # Slice assignment
```

### 2. Tuples
**Ordered, immutable collection**
```python
# Creation
coordinates = (10, 20)
single_item = (42,)         # Note the comma

# Operations
x, y = coordinates          # Unpacking
length = len(coordinates)
index = coordinates.index(10)
```

### 3. Dictionaries
**Key-value pairs, mutable**
```python
# Creation
person = {"name": "Alice", "age": 30}
person = dict(name="Alice", age=30)

# Operations
person["city"] = "NYC"      # Add/update
age = person.get("age", 0)  # Safe access
del person["age"]           # Delete key
keys = person.keys()
values = person.values()
items = person.items()
```

### 4. Sets
**Unordered, unique elements**
```python
# Creation
numbers = {1, 2, 3, 4, 5}
unique_chars = set("hello")

# Operations
numbers.add(6)              # Add element
numbers.remove(3)           # Remove (raises error if not found)
numbers.discard(10)         # Remove (no error if not found)
union = numbers | {7, 8}    # Union
intersection = numbers & {1, 2, 6}  # Intersection
```

### 5. Strings
**Immutable sequence of characters**
```python
# Creation
text = "Hello World"
multiline = """Line 1
Line 2"""

# Operations
words = text.split()        # Split into list
joined = " ".join(words)    # Join list into string
upper = text.upper()
replaced = text.replace("World", "Python")
```

## Collections Module

### 1. Counter
**Count hashable objects**
```python
from collections import Counter

# Count elements
counts = Counter([1, 2, 2, 3, 3, 3])
word_counts = Counter("hello world".split())

# Operations
most_common = counts.most_common(2)  # [(3, 3), (2, 2)]
counts.update([1, 1, 4])            # Add more counts
```

### 2. defaultdict
**Dictionary with default values**
```python
from collections import defaultdict

# Group items
groups = defaultdict(list)
for item in ["apple", "banana", "apricot"]:
    groups[item[0]].append(item)

# Count items
counts = defaultdict(int)
for char in "hello":
    counts[char] += 1
```

### 3. OrderedDict
**Dictionary that remembers insertion order**
```python
from collections import OrderedDict

# Maintain order (Python 3.7+ dicts are ordered by default)
ordered = OrderedDict([("first", 1), ("second", 2)])
ordered.move_to_end("first")        # Move to end
```

### 4. deque
**Double-ended queue**
```python
from collections import deque

# Creation
queue = deque([1, 2, 3])

# Operations
queue.appendleft(0)         # Add to left
queue.append(4)             # Add to right
left = queue.popleft()      # Remove from left
right = queue.pop()         # Remove from right
queue.rotate(1)             # Rotate right
```

### 5. namedtuple
**Tuple with named fields**
```python
from collections import namedtuple

# Creation
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)

# Access
print(p.x, p.y)            # Named access
print(p[0], p[1])          # Index access
```

## Advanced Data Structures

### 1. Heap (heapq)
**Priority queue implementation**
```python
import heapq

# Min heap
heap = [3, 1, 4, 1, 5]
heapq.heapify(heap)         # Convert to heap
heapq.heappush(heap, 2)     # Add element
smallest = heapq.heappop(heap)  # Remove smallest

# Max heap (negate values)
max_heap = [-x for x in [3, 1, 4]]
heapq.heapify(max_heap)
```

### 2. Queue
**FIFO queue**
```python
from queue import Queue, LifoQueue, PriorityQueue

# FIFO Queue
q = Queue()
q.put(1)
item = q.get()

# LIFO Queue (Stack)
stack = LifoQueue()
stack.put(1)
item = stack.get()

# Priority Queue
pq = PriorityQueue()
pq.put((1, "high priority"))
pq.put((5, "low priority"))
priority, item = pq.get()
```

### 3. Array (array module)
**Efficient arrays of numeric values**
```python
import array

# Creation
numbers = array.array('i', [1, 2, 3, 4])  # 'i' for integers
floats = array.array('f', [1.1, 2.2, 3.3])  # 'f' for floats

# Operations
numbers.append(5)
numbers.extend([6, 7])
```

### 4. Enum
**Enumerated constants**
```python
from enum import Enum, auto

class Status(Enum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

# Usage
current_status = Status.PENDING
```

## Data Structure Comparison

| Structure | Ordered | Mutable | Duplicates | Use Case |
|-----------|---------|---------|------------|----------|
| List | ✓ | ✓ | ✓ | General purpose, sequences |
| Tuple | ✓ | ✗ | ✓ | Immutable sequences, coordinates |
| Dict | ✓* | ✓ | ✗ (keys) | Key-value mapping |
| Set | ✗ | ✓ | ✗ | Unique elements, set operations |
| String | ✓ | ✗ | ✓ | Text processing |
| deque | ✓ | ✓ | ✓ | Double-ended operations |
| Counter | ✗ | ✓ | N/A | Counting elements |

*Ordered since Python 3.7

## Performance Characteristics

### Time Complexity (Big O)

| Operation | List | Dict | Set | deque |
|-----------|------|------|-----|-------|
| Access | O(1) | O(1) | N/A | O(1) |
| Search | O(n) | O(1) | O(1) | O(n) |
| Insert | O(n) | O(1) | O(1) | O(1) |
| Delete | O(n) | O(1) | O(1) | O(1) |
| Append | O(1) | N/A | N/A | O(1) |

## Common Patterns

### 1. List Comprehensions
```python
# Basic
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Nested
matrix = [[i*j for j in range(3)] for i in range(3)]
```

### 2. Dictionary Comprehensions
```python
# Basic
squares = {x: x**2 for x in range(5)}

# From lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
mapping = {k: v for k, v in zip(keys, values)}
```

### 3. Set Operations
```python
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

union = set1 | set2           # {1, 2, 3, 4, 5, 6}
intersection = set1 & set2    # {3, 4}
difference = set1 - set2      # {1, 2}
symmetric_diff = set1 ^ set2  # {1, 2, 5, 6}
```

## Best Practices

1. **Choose the right structure**:
   - Use `list` for ordered, mutable sequences
   - Use `tuple` for immutable sequences
   - Use `dict` for key-value mappings
   - Use `set` for unique elements and set operations

2. **Memory efficiency**:
   - Use `tuple` instead of `list` when data won't change
   - Use `set` for membership testing instead of `list`
   - Use `deque` for frequent insertions/deletions at both ends

3. **Performance optimization**:
   - Use `dict.get()` instead of checking `if key in dict`
   - Use `collections.Counter` for counting operations
   - Use `collections.defaultdict` to avoid key existence checks

4. **Code readability**:
   - Use `namedtuple` for simple data containers
   - Use comprehensions for simple transformations
   - Use appropriate data structure methods (`append`, `extend`, `update`)