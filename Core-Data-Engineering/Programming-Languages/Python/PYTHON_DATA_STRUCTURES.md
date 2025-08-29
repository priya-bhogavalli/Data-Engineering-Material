# Python Data Structures for Data Engineering

## Built-in Data Structures

### 1. Lists
**Description**: Ordered, mutable collections that can store any data type. Perfect for sequences where order matters and you need to modify the data.

**Real-time Data Engineering Use Cases**:
- Processing streaming log entries in chronological order
- Storing batch records for ETL processing
- Maintaining processing queues for data pipelines
- Collecting validation errors during data quality checks

```python
# Real Example: Processing streaming log entries
log_entries = []

# Streaming data ingestion
new_entry = {"timestamp": "2024-01-15 10:30:00", "level": "ERROR", "message": "DB connection failed"}
log_entries.append(new_entry)  # Add new log entry

# Batch processing - process in chunks
batch_size = 1000
for i in range(0, len(log_entries), batch_size):
    batch = log_entries[i:i + batch_size]
    process_log_batch(batch)

# Data quality - remove invalid entries
valid_entries = [entry for entry in log_entries if entry.get("timestamp")]
```

### 2. Tuples
**Description**: Ordered, immutable collections ideal for fixed data structures. Use when data shouldn't change after creation.

**Real-time Data Engineering Use Cases**:
- Database connection parameters (host, port, database, user)
- Coordinate pairs for geospatial data
- Configuration settings that shouldn't be modified
- Return multiple values from functions

```python
# Real Example: Database connection configuration
db_config = ("prod-db.company.com", 5432, "analytics_db", "readonly_user")
host, port, database, user = db_config  # Unpacking for connection

# Geospatial data processing
store_locations = [
    (40.7128, -74.0060, "NYC Store"),    # lat, lng, name
    (34.0522, -118.2437, "LA Store"),
    (41.8781, -87.6298, "Chicago Store")
]

# Processing coordinates
for lat, lng, name in store_locations:
    distance = calculate_distance_from_warehouse(lat, lng)
    print(f"{name}: {distance} miles")
```

### 3. Dictionaries
**Description**: Key-value pairs providing fast lookups. Essential for data mapping, configuration, and JSON-like data structures.

**Real-time Data Engineering Use Cases**:
- API response parsing and data transformation
- Configuration management for data pipelines
- Data aggregation and grouping operations
- Caching frequently accessed data
- Mapping reference data (user_id -> user_info)

```python
# Real Example: User activity aggregation
user_sessions = {}

# Process streaming user events
event = {"user_id": 12345, "action": "page_view", "timestamp": "2024-01-15T10:30:00"}
user_id = event["user_id"]

# Aggregate user activity
if user_id not in user_sessions:
    user_sessions[user_id] = {"page_views": 0, "purchases": 0, "last_seen": None}

user_sessions[user_id]["page_views"] += 1
user_sessions[user_id]["last_seen"] = event["timestamp"]

# Configuration for data pipeline
pipeline_config = {
    "source": {"type": "kafka", "topic": "user_events", "batch_size": 1000},
    "transform": {"dedupe": True, "validate": True},
    "sink": {"type": "s3", "bucket": "analytics-data", "format": "parquet"}
}

# Safe configuration access
batch_size = pipeline_config.get("source", {}).get("batch_size", 100)
```

### 4. Sets
**Description**: Unordered collections of unique elements. Extremely fast for membership testing and set operations.

**Real-time Data Engineering Use Cases**:
- Data deduplication in streaming pipelines
- Finding common/different elements between datasets
- User segmentation and audience analysis
- Tracking processed record IDs to avoid reprocessing
- Data quality checks for unique constraints

```python
# Real Example: Real-time deduplication
processed_order_ids = set()

# Stream processing - avoid duplicate orders
incoming_order = {"order_id": "ORD-12345", "amount": 99.99}
order_id = incoming_order["order_id"]

if order_id not in processed_order_ids:
    process_order(incoming_order)
    processed_order_ids.add(order_id)
else:
    log_duplicate_order(order_id)

# User segmentation analysis
premium_users = {101, 102, 103, 105, 108}
active_users = {101, 104, 105, 106, 107, 108}

# Business insights
premium_active = premium_users & active_users      # {101, 105, 108}
inactive_premium = premium_users - active_users    # {102, 103}
active_non_premium = active_users - premium_users  # {104, 106, 107}

print(f"Premium active users: {len(premium_active)}")
print(f"Churn risk (inactive premium): {len(inactive_premium)}")
```

### 5. Strings
**Description**: Immutable sequences of characters. Essential for text processing, data cleaning, and format transformations.

**Real-time Data Engineering Use Cases**:
- Log parsing and text extraction
- Data cleaning and standardization
- SQL query building and templating
- File path manipulation
- Data format conversion (CSV, JSON parsing)

```python
# Real Example: Log parsing and data cleaning
raw_log = "2024-01-15 10:30:45 [ERROR] Database connection failed - host: db.prod.com:5432"

# Extract structured data from log
parts = raw_log.split(" ", 2)  # Split into timestamp, level, message
timestamp = parts[0] + " " + parts[1]
level = parts[2].split("]")[0][1:]  # Extract ERROR from [ERROR]
message = parts[2].split("] ", 1)[1]  # Get message after ]

# Data standardization
user_input = "  JOHN.DOE@COMPANY.COM  "
clean_email = user_input.strip().lower()  # "john.doe@company.com"

# SQL query building
table_name = "user_events"
date_filter = "2024-01-15"
query = f"SELECT * FROM {table_name} WHERE event_date = '{date_filter}'"

# CSV data cleaning
csv_row = "John,Doe,25,New York,NY"
fields = [field.strip() for field in csv_row.split(",")]
first_name, last_name, age, city, state = fields
```

## Collections Module

### 1. Counter
**Description**: Specialized dictionary for counting hashable objects. Perfect for frequency analysis and statistics.

**Real-time Data Engineering Use Cases**:
- Event frequency analysis in streaming data
- Error rate monitoring and alerting
- User behavior analytics (page views, clicks)
- Data quality metrics (null counts, duplicate detection)
- A/B testing result aggregation

```python
from collections import Counter

# Real Example: Real-time error monitoring
error_counter = Counter()

# Process streaming error logs
error_logs = [
    "DatabaseConnectionError", "TimeoutError", "DatabaseConnectionError",
    "ValidationError", "TimeoutError", "DatabaseConnectionError"
]

for error in error_logs:
    error_counter[error] += 1

# Alert on high error rates
if error_counter["DatabaseConnectionError"] > 5:
    send_alert("High database connection errors detected")

# Top errors for dashboard
top_errors = error_counter.most_common(3)
print(f"Top errors: {top_errors}")  # [('DatabaseConnectionError', 3), ('TimeoutError', 2), ...]

# User engagement analytics
page_views = Counter()
user_actions = ["home", "product", "cart", "home", "product", "checkout"]
page_views.update(user_actions)

conversion_rate = page_views["checkout"] / page_views["home"] * 100
```

### 2. defaultdict
**Description**: Dictionary that automatically creates missing values with a default factory function. Eliminates key existence checks.

**Real-time Data Engineering Use Cases**:
- Grouping streaming data by categories
- Building aggregation pipelines without initialization
- User session tracking and analytics
- Multi-dimensional data aggregation
- Building nested data structures on-the-fly

```python
from collections import defaultdict

# Real Example: User session analytics
user_sessions = defaultdict(lambda: {"page_views": 0, "session_duration": 0, "purchases": 0})

# Process streaming user events
events = [
    {"user_id": 123, "event": "page_view", "page": "home"},
    {"user_id": 456, "event": "page_view", "page": "product"},
    {"user_id": 123, "event": "purchase", "amount": 99.99}
]

for event in events:
    user_id = event["user_id"]
    if event["event"] == "page_view":
        user_sessions[user_id]["page_views"] += 1
    elif event["event"] == "purchase":
        user_sessions[user_id]["purchases"] += 1

# Sales analytics by region and product
sales_data = defaultdict(lambda: defaultdict(float))
transactions = [
    {"region": "US", "product": "laptop", "amount": 1200},
    {"region": "EU", "product": "laptop", "amount": 1100},
    {"region": "US", "product": "mouse", "amount": 25}
]

for txn in transactions:
    sales_data[txn["region"]][txn["product"]] += txn["amount"]

print(f"US laptop sales: ${sales_data['US']['laptop']}")
```

### 3. OrderedDict
**Description**: Dictionary that maintains insertion order with additional ordering methods. Useful for ordered processing and LRU caches.

**Real-time Data Engineering Use Cases**:
- Maintaining processing order in data pipelines
- Building LRU (Least Recently Used) caches
- Configuration files where order matters
- Time-series data with ordered timestamps
- Pipeline stage execution tracking

```python
from collections import OrderedDict

# Real Example: LRU Cache for database queries
class QueryCache:
    def __init__(self, max_size=100):
        self.cache = OrderedDict()
        self.max_size = max_size
    
    def get(self, query):
        if query in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(query)
            return self.cache[query]
        return None
    
    def put(self, query, result):
        if query in self.cache:
            self.cache.move_to_end(query)
        else:
            if len(self.cache) >= self.max_size:
                # Remove least recently used
                self.cache.popitem(last=False)
        self.cache[query] = result

# Pipeline stage tracking
pipeline_stages = OrderedDict([
    ("extract", {"status": "completed", "duration": 2.3}),
    ("transform", {"status": "running", "duration": None}),
    ("load", {"status": "pending", "duration": None})
])

# Process stages in order
for stage_name, stage_info in pipeline_stages.items():
    if stage_info["status"] == "pending":
        execute_stage(stage_name)
        break
```

### 4. deque
**Description**: Double-ended queue optimized for fast appends/pops from both ends. Perfect for sliding windows and buffering.

**Real-time Data Engineering Use Cases**:
- Sliding window calculations (moving averages, recent events)
- Stream buffering and rate limiting
- Undo/redo functionality in data processing
- Recent activity tracking
- Queue-based task processing

```python
from collections import deque

# Real Example: Sliding window for real-time metrics
class MetricsWindow:
    def __init__(self, window_size=100):
        self.window = deque(maxlen=window_size)  # Auto-removes old items
        self.sum = 0
    
    def add_metric(self, value):
        if len(self.window) == self.window.maxlen:
            # Remove oldest value from sum
            self.sum -= self.window[0]
        
        self.window.append(value)
        self.sum += value
    
    def get_average(self):
        return self.sum / len(self.window) if self.window else 0

# Real-time response time monitoring
response_times = MetricsWindow(window_size=50)

# Process incoming API response times
for response_time in [120, 95, 200, 85, 150]:
    response_times.add_metric(response_time)
    avg_response = response_times.get_average()
    
    if avg_response > 100:
        print(f"Alert: High average response time: {avg_response:.1f}ms")

# Stream processing buffer
stream_buffer = deque(maxlen=1000)

# Buffer incoming events for batch processing
event = {"user_id": 123, "action": "click", "timestamp": "2024-01-15T10:30:00"}
stream_buffer.append(event)

# Process when buffer is full
if len(stream_buffer) == stream_buffer.maxlen:
    batch_process(list(stream_buffer))
    stream_buffer.clear()
```

### 5. namedtuple
**Description**: Immutable objects with named fields. Lightweight alternative to classes for simple data containers.

**Real-time Data Engineering Use Cases**:
- Structured data records in pipelines
- Configuration objects that shouldn't change
- Return multiple values from functions clearly
- Database row representations
- API response parsing into structured objects

```python
from collections import namedtuple

# Real Example: Structured data processing
LogEntry = namedtuple("LogEntry", ["timestamp", "level", "service", "message", "user_id"])
Metric = namedtuple("Metric", ["name", "value", "timestamp", "tags"])

# Parse log entries into structured format
raw_log = "2024-01-15T10:30:00 ERROR auth-service Login failed user_id=12345"
parts = raw_log.split()
log_entry = LogEntry(
    timestamp=parts[0],
    level=parts[1],
    service=parts[2],
    message=" ".join(parts[3:-1]),
    user_id=parts[-1].split("=")[1]
)

# Easy access to structured data
if log_entry.level == "ERROR" and log_entry.service == "auth-service":
    alert_security_team(log_entry.user_id, log_entry.message)

# Database query results
UserStats = namedtuple("UserStats", ["user_id", "total_orders", "total_spent", "last_login"])

def get_user_analytics(user_id):
    # Query database
    row = db.execute("SELECT user_id, total_orders, total_spent, last_login FROM user_stats WHERE user_id = ?", [user_id])
    return UserStats(*row) if row else None

# Clean function returns
user_stats = get_user_analytics(12345)
if user_stats and user_stats.total_spent > 1000:
    add_to_vip_program(user_stats.user_id)
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