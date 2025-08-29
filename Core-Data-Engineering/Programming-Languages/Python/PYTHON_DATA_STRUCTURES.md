# Python Data Structures for Data Engineering

## Table of Contents

1. [Built-in Data Structures](#built-in-data-structures)
   - [Lists](#1-lists)
   - [Tuples](#2-tuples)
   - [Dictionaries](#3-dictionaries)
   - [Sets](#4-sets)
   - [Strings](#5-strings)
2. [Collections Module](#collections-module)
   - [Counter](#1-counter)
   - [defaultdict](#2-defaultdict)
   - [OrderedDict](#3-ordereddict)
   - [deque](#4-deque)
   - [namedtuple](#5-namedtuple)
3. [Advanced Data Structures](#advanced-data-structures)
   - [Heap (heapq)](#1-heap-heapq)
   - [Queue](#task-queue-for-data-processing)
   - [Array (array module)](#3-array-array-module)
   - [Enum](#4-enum)
4. [Data Structure Comparison](#data-structure-comparison)
5. [Performance Characteristics](#performance-characteristics)
6. [Common Patterns](#common-patterns)
7. [Best Practices](#best-practices)

---

## Built-in Data Structures

### 1. Numeric Types (int, float)
**Description**: Fundamental numeric data types for mathematical operations and calculations. Essential for data analysis, metrics, and computations.

**Basic Operations**:
```python
# Integer operations
count = 42
total_records = 1_000_000  # Underscore for readability
binary_num = 0b1010        # Binary: 10
hex_num = 0xFF             # Hexadecimal: 255

print(f"Count: {count}")
print(f"Total records: {total_records:,}")
print(f"Binary {binary_num}, Hex {hex_num}")
# Output: Count: 42
# Output: Total records: 1,000,000
# Output: Binary 10, Hex 255

# Float operations
temperature = 23.5
percentage = 0.85
scientific = 1.23e-4       # Scientific notation

print(f"Temperature: {temperature}°C")
print(f"Percentage: {percentage:.1%}")
print(f"Scientific: {scientific}")
# Output: Temperature: 23.5°C
# Output: Percentage: 85.0%
# Output: Scientific: 0.000123

# Type checking and conversion
value = "123"
if value.isdigit():
    num_value = int(value)
    print(f"Converted to int: {num_value}")

float_str = "45.67"
float_value = float(float_str)
print(f"Converted to float: {float_value}")
# Output: Converted to int: 123
# Output: Converted to float: 45.67
```

**Real-time Data Engineering Use Cases**:
- Calculating metrics and KPIs (revenue, conversion rates)
- Processing sensor data and measurements
- Aggregating counts and sums in data pipelines
- Financial calculations and monetary values
- Performance metrics and timing measurements

```python
# Real Example: Sales metrics calculation
class SalesMetrics:
    def __init__(self):
        self.total_revenue = 0.0
        self.order_count = 0
        self.customer_count = 0
    
    def add_order(self, amount: float, is_new_customer: bool = False):
        self.total_revenue += amount
        self.order_count += 1
        if is_new_customer:
            self.customer_count += 1
    
    def get_metrics(self) -> dict:
        avg_order_value = self.total_revenue / self.order_count if self.order_count > 0 else 0.0
        return {
            'total_revenue': round(self.total_revenue, 2),
            'order_count': self.order_count,
            'avg_order_value': round(avg_order_value, 2),
            'new_customers': self.customer_count
        }

# Process daily sales
sales = SalesMetrics()
sales.add_order(99.99, is_new_customer=True)
sales.add_order(149.50)
sales.add_order(75.25, is_new_customer=True)

metrics = sales.get_metrics()
print(f"Daily metrics: {metrics}")
# Output: Daily metrics: {'total_revenue': 324.74, 'order_count': 3, 'avg_order_value': 108.25, 'new_customers': 2}

# Data quality checks with numeric validation
def validate_numeric_data(data: dict) -> bool:
    """Validate that numeric fields are within expected ranges."""
    validations = {
        'age': lambda x: isinstance(x, int) and 0 <= x <= 120,
        'salary': lambda x: isinstance(x, (int, float)) and x >= 0,
        'score': lambda x: isinstance(x, (int, float)) and 0.0 <= x <= 100.0
    }
    
    for field, validator in validations.items():
        if field in data and not validator(data[field]):
            print(f"Validation failed for {field}: {data[field]}")
            return False
    return True

# Test data validation
test_records = [
    {'age': 25, 'salary': 50000.0, 'score': 85.5},  # Valid
    {'age': -5, 'salary': 60000.0, 'score': 92.0},  # Invalid age
    {'age': 30, 'salary': -1000, 'score': 78.0}     # Invalid salary
]

for i, record in enumerate(test_records, 1):
    is_valid = validate_numeric_data(record)
    print(f"Record {i}: {'Valid' if is_valid else 'Invalid'}")
# Output: Record 1: Valid
# Output: Validation failed for age: -5
# Output: Record 2: Invalid
# Output: Validation failed for salary: -1000
# Output: Record 3: Invalid
```

### 2. NoneType
**Description**: Represents the absence of a value. Critical for handling missing data, optional parameters, and null values in data processing.

**Basic Operations**:
```python
# None as default value
def process_data(data, config=None):
    if config is None:
        config = {'batch_size': 1000, 'validate': True}
    return f"Processing with config: {config}"

result1 = process_data([1, 2, 3])
result2 = process_data([1, 2, 3], {'batch_size': 500})
print(result1)
print(result2)
# Output: Processing with config: {'batch_size': 1000, 'validate': True}
# Output: Processing with config: {'batch_size': 500}

# None checking patterns
user_data = {'name': 'Alice', 'email': None, 'age': 30}

# Safe access with None check
email = user_data.get('email')
if email is not None:
    send_email(email)
else:
    print("No email provided")
# Output: No email provided

# Using None in data filtering
values = [1, None, 3, None, 5, 0, 7]
filtered = [x for x in values if x is not None]
print(f"Original: {values}")
print(f"Filtered: {filtered}")
# Output: Original: [1, None, 3, None, 5, 0, 7]
# Output: Filtered: [1, 3, 5, 0, 7]

# None vs False/0 distinction
test_values = [None, False, 0, '', []]
for value in test_values:
    print(f"{repr(value):8} -> is None: {value is None}, is falsy: {not value}")
# Output: None     -> is None: True, is falsy: True
# Output: False    -> is None: False, is falsy: True
# Output: 0        -> is None: False, is falsy: True
# Output: ''       -> is None: False, is falsy: True
# Output: []       -> is None: False, is falsy: True
```

**Real-time Data Engineering Use Cases**:
- Handling missing values in datasets
- Optional configuration parameters
- Database NULL value representation
- API response parsing with missing fields
- Data validation and quality checks
- Default value initialization

```python
# Real Example: Data cleaning with None handling
class DataCleaner:
    def __init__(self):
        self.null_count = 0
        self.cleaned_records = []
    
    def clean_record(self, record: dict) -> dict:
        """Clean a data record, handling None values appropriately."""
        cleaned = {}
        
        for field, value in record.items():
            if value is None:
                self.null_count += 1
                # Apply field-specific null handling
                if field == 'age':
                    cleaned[field] = 0  # Default age
                elif field == 'email':
                    cleaned[field] = 'unknown@example.com'
                elif field == 'score':
                    cleaned[field] = None  # Keep as None for later imputation
                else:
                    cleaned[field] = value
            else:
                cleaned[field] = value
        
        return cleaned
    
    def process_batch(self, records: list) -> list:
        """Process a batch of records with None handling."""
        for record in records:
            cleaned = self.clean_record(record)
            if self._is_valid_record(cleaned):
                self.cleaned_records.append(cleaned)
        
        return self.cleaned_records
    
    def _is_valid_record(self, record: dict) -> bool:
        """Validate that record has required non-None fields."""
        required_fields = ['name', 'age']
        return all(record.get(field) is not None for field in required_fields)
    
    def get_stats(self) -> dict:
        return {
            'null_values_found': self.null_count,
            'records_processed': len(self.cleaned_records),
            'null_percentage': (self.null_count / (len(self.cleaned_records) * 4)) * 100 if self.cleaned_records else 0
        }

# Process data with missing values
raw_data = [
    {'name': 'Alice', 'age': 30, 'email': 'alice@example.com', 'score': 85.5},
    {'name': 'Bob', 'age': None, 'email': None, 'score': 92.0},
    {'name': None, 'age': 25, 'email': 'charlie@example.com', 'score': None},
    {'name': 'Diana', 'age': 28, 'email': 'diana@example.com', 'score': 78.5}
]

cleaner = DataCleaner()
cleaned_data = cleaner.process_batch(raw_data)
stats = cleaner.get_stats()

print(f"Cleaned {len(cleaned_data)} records:")
for record in cleaned_data:
    print(f"  {record}")
print(f"\nStats: {stats}")
# Output: Cleaned 3 records:
# Output:   {'name': 'Alice', 'age': 30, 'email': 'alice@example.com', 'score': 85.5}
# Output:   {'name': 'Bob', 'age': 0, 'email': 'unknown@example.com', 'score': 92.0}
# Output:   {'name': 'Diana', 'age': 28, 'email': 'diana@example.com', 'score': 78.5}
# Output: Stats: {'null_values_found': 4, 'records_processed': 3, 'null_percentage': 33.33}

# API response handling with None values
def parse_api_response(response_data: dict) -> dict:
    """Parse API response handling None/missing fields gracefully."""
    return {
        'user_id': response_data.get('id'),
        'username': response_data.get('username', 'anonymous'),
        'email': response_data.get('email'),  # Keep None if missing
        'last_login': response_data.get('last_login'),
        'is_active': response_data.get('active', True),  # Default to True
        'profile_complete': response_data.get('profile') is not None
    }

# Test API response parsing
api_responses = [
    {'id': 123, 'username': 'alice', 'email': 'alice@example.com', 'active': True},
    {'id': 124, 'username': 'bob'},  # Missing email, active, last_login
    {'id': 125, 'email': 'charlie@example.com', 'profile': {'bio': 'Developer'}}  # Missing username
]

for response in api_responses:
    parsed = parse_api_response(response)
    print(f"Parsed: {parsed}")
# Output: Parsed: {'user_id': 123, 'username': 'alice', 'email': 'alice@example.com', 'last_login': None, 'is_active': True, 'profile_complete': False}
# Output: Parsed: {'user_id': 124, 'username': 'bob', 'email': None, 'last_login': None, 'is_active': True, 'profile_complete': False}
# Output: Parsed: {'user_id': 125, 'username': 'anonymous', 'email': 'charlie@example.com', 'last_login': None, 'is_active': True, 'profile_complete': True}
```

### 3. Lists
**Description**: Ordered, mutable collections that can store any data type. Perfect for sequences where order matters and you need to modify the data.

**Basic Operations**:
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

print(f"Numbers after operations: {numbers}")
print(f"Popped element: {popped}")
# Output: Numbers after operations: [0, 1, 10, 20, 4, 5]
# Output: Popped element: 6

# List comprehensions
squares = [x**2 for x in range(10)]
filtered = [x for x in numbers if x > 5]
```

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
    print(f"Processing batch {i//batch_size + 1} with {len(batch)} entries")

print(f"Total log entries: {len(log_entries)}")
# Output: Processing batch 1 with 1 entries
# Output: Total log entries: 1

# Data quality - remove invalid entries
valid_entries = [entry for entry in log_entries if entry.get("timestamp")]
```

### 2. Tuples
**Description**: Ordered, immutable collections ideal for fixed data structures. Use when data shouldn't change after creation.

**Basic Operations**:
```python
# Creation
coordinates = (10, 20)
single_item = (42,)         # Note the comma

# Operations
x, y = coordinates          # Unpacking
length = len(coordinates)
index = coordinates.index(10)

print(f"Coordinates: {coordinates}")
print(f"Unpacked - x: {x}, y: {y}")
print(f"Length: {length}, Index of 10: {index}")
# Output: Coordinates: (10, 20)
# Output: Unpacked - x: 10, y: 20
# Output: Length: 2, Index of 10: 0

# Named tuples
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(p.x, p.y)            # Named access
```

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
    distance = abs(lat - 40.0) + abs(lng + 74.0)  # Simple distance calculation
    print(f"{name}: {distance:.1f} miles")

# Output: NYC Store: 0.7 miles
# Output: LA Store: 50.2 miles
# Output: Chicago Store: 14.9 miles
```

### 3. Dictionaries
**Description**: Key-value pairs providing fast lookups. Essential for data mapping, configuration, and JSON-like data structures.

**Basic Operations**:
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

# Dictionary comprehensions
squared_dict = {x: x**2 for x in range(5)}
filtered = {k: v for k, v in person.items() if isinstance(v, str)}
```

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

print(user_sessions)
# Output: {12345: {'page_views': 1, 'purchases': 0, 'last_seen': '2024-01-15T10:30:00'}}

# Configuration for data pipeline
pipeline_config = {
    "source": {"type": "kafka", "topic": "user_events", "batch_size": 1000},
    "transform": {"dedupe": True, "validate": True},
    "sink": {"type": "s3", "bucket": "analytics-data", "format": "parquet"}
}

# Safe configuration access
batch_size = pipeline_config.get("source", {}).get("batch_size", 100)

print(f"Batch size: {batch_size}")
# Output: Batch size: 1000
```

### 4. Sets
**Description**: Unordered collections of unique elements. Extremely fast for membership testing and set operations.

**Basic Operations**:
```python
# Creation
numbers = {1, 2, 3, 4, 5}
unique_chars = set("hello")

# Operations
numbers.add(6)              # Add element
numbers.remove(3)           # Remove (raises error if not found)
numbers.discard(10)         # Remove (no error if not found)

print(f"Numbers after operations: {numbers}")
print(f"Unique chars: {unique_chars}")
# Output: Numbers after operations: {1, 2, 4, 5, 6}
# Output: Unique chars: {'e', 'h', 'l', 'o'}

# Set operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
union = set1 | set2             # {1, 2, 3, 4, 5, 6}
intersection = set1 & set2      # {3, 4}
difference = set1 - set2        # {1, 2}

print(f"Union: {union}")
print(f"Intersection: {intersection}")
print(f"Difference: {difference}")
# Output: Union: {1, 2, 3, 4, 5, 6}
# Output: Intersection: {3, 4}
# Output: Difference: {1, 2}
```

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
    print(f"Processing new order: {order_id}")
    processed_order_ids.add(order_id)
else:
    print(f"Duplicate order detected: {order_id}")

print(f"Processed orders: {processed_order_ids}")
# Output: Processing new order: ORD-12345
# Output: Processed orders: {'ORD-12345'}

# User segmentation analysis
premium_users = {101, 102, 103, 105, 108}
active_users = {101, 104, 105, 106, 107, 108}

# Business insights
premium_active = premium_users & active_users      # {101, 105, 108}
inactive_premium = premium_users - active_users    # {102, 103}
active_non_premium = active_users - premium_users  # {104, 106, 107}

print(f"Premium active users: {len(premium_active)}")
print(f"Churn risk (inactive premium): {len(inactive_premium)}")
# Output: Premium active users: 3
# Output: Churn risk (inactive premium): 2
```

### 5. Strings
**Description**: Immutable sequences of characters. Essential for text processing, data cleaning, and format transformations.

**Basic Operations**:
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
stripped = "  hello  ".strip()  # Remove whitespace

# String formatting
name = "Alice"
age = 30
formatted = f"Name: {name}, Age: {age}"  # f-strings
```

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

print(f"Timestamp: {timestamp}")
print(f"Level: {level}")
print(f"Message: {message}")
# Output: Timestamp: 2024-01-15 10:30:45
# Output: Level: ERROR
# Output: Message: Database connection failed - host: db.prod.com:5432

# Data standardization
user_input = "  JOHN.DOE@COMPANY.COM  "
clean_email = user_input.strip().lower()

print(f"Clean email: {clean_email}")
# Output: Clean email: john.doe@company.com

# SQL query building
table_name = "user_events"
date_filter = "2024-01-15"
query = f"SELECT * FROM {table_name} WHERE event_date = '{date_filter}'"

print(f"Generated query: {query}")
# Output: Generated query: SELECT * FROM user_events WHERE event_date = '2024-01-15'

# CSV data cleaning
csv_row = "John,Doe,25,New York,NY"
fields = [field.strip() for field in csv_row.split(",")]
first_name, last_name, age, city, state = fields

print(f"Original CSV: {csv_row}")
print(f"Parsed fields: {fields}")
print(f"Parsed: {first_name} {last_name}, {age}, {city}, {state}")
# Output: Original CSV: John,Doe,25,New York,NY
# Output: Parsed fields: ['John', 'Doe', '25', 'New York', 'NY']
# Output: Parsed: John Doe, 25, New York, NY
```

## Collections Module

### 1. Counter
**Description**: Specialized dictionary for counting hashable objects. Perfect for frequency analysis and statistics.

**Basic Operations**:
```python
from collections import Counter

# Count elements
counts = Counter([1, 2, 2, 3, 3, 3])
word_counts = Counter("hello world".split())

# Operations
most_common = counts.most_common(2)  # [(3, 3), (2, 2)]
counts.update([1, 1, 4])            # Add more counts
total = sum(counts.values())         # Total count

print(f"Counts: {dict(counts)}")
print(f"Most common: {most_common}")
print(f"Word counts: {dict(word_counts)}")
print(f"Total: {total}")
# Output: Counts: {1: 3, 2: 2, 3: 3, 4: 1}
# Output: Most common: [(3, 3), (1, 3)]
# Output: Word counts: {'hello': 1, 'world': 1}
# Output: Total: 9
```

**Real-time Data Engineering Use Cases**:
- Event frequency analysis in streaming data
- Error rate monitoring and alerting
- User behavior analytics (page views, clicks)
- Data quality metrics (null counts, duplicate detection)
- A/B testing result aggregation

```python
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
if error_counter["DatabaseConnectionError"] > 2:
    print("ALERT: High database connection errors detected")

print(f"Error counts: {dict(error_counter)}")
# Output: ALERT: High database connection errors detected
# Output: Error counts: {'DatabaseConnectionError': 3, 'TimeoutError': 2, 'ValidationError': 1}

# Top errors for dashboard
top_errors = error_counter.most_common(3)
print(f"Top errors: {top_errors}")
# Output: Top errors: [('DatabaseConnectionError', 3), ('TimeoutError', 2), ('ValidationError', 1)]

# User engagement analytics
page_views = Counter()
user_actions = ["home", "product", "cart", "home", "product", "checkout"]
page_views.update(user_actions)

conversion_rate = page_views["checkout"] / page_views["home"] * 100

print(f"Page views: {dict(page_views)}")
print(f"Conversion rate: {conversion_rate:.1f}%")
# Output: Page views: {'home': 2, 'product': 2, 'cart': 1, 'checkout': 1}
# Output: Conversion rate: 50.0%
```

### 2. defaultdict
**Description**: Dictionary that automatically creates missing values with a default factory function. Eliminates key existence checks.

**Basic Operations**:
```python
from collections import defaultdict

# Group items
groups = defaultdict(list)
for item in ["apple", "banana", "apricot"]:
    groups[item[0]].append(item)

print(dict(groups))
# Output: {'a': ['apple', 'apricot'], 'b': ['banana']}

# Count items
counts = defaultdict(int)
for char in "hello":
    counts[char] += 1

print(dict(counts))
# Output: {'h': 1, 'e': 1, 'l': 2, 'o': 1}

# Nested defaultdict
nested = defaultdict(lambda: defaultdict(int))
nested['users']['active'] = 150
nested['users']['inactive'] = 25
nested['orders']['pending'] = 45

print(dict(nested))
# Output: {'users': defaultdict(<class 'int'>, {'active': 150, 'inactive': 25}), 
#          'orders': defaultdict(<class 'int'>, {'pending': 45})}
```

**Real-time Data Engineering Use Cases**:
- Grouping streaming data by categories
- Building aggregation pipelines without initialization
- User session tracking and analytics
- Multi-dimensional data aggregation
- Building nested data structures on-the-fly

```python
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

print(f"User sessions: {dict(user_sessions)}")
# Output: User sessions: {123: {'page_views': 1, 'session_duration': 0, 'purchases': 1}, 456: {'page_views': 1, 'session_duration': 0, 'purchases': 0}}

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
print(f"All sales data: {dict(sales_data)}")
# Output: US laptop sales: $1200.0
# Output: All sales data: {'US': defaultdict(<class 'float'>, {'laptop': 1200.0, 'mouse': 25.0}), 'EU': defaultdict(<class 'float'>, {'laptop': 1100.0})}
```

### 3. OrderedDict
**Description**: Dictionary that maintains insertion order with additional ordering methods. Useful for ordered processing and LRU caches.

**Basic Operations**:
```python
from collections import OrderedDict

# Maintain order (Python 3.7+ dicts are ordered by default)
ordered = OrderedDict([("first", 1), ("second", 2), ("third", 3)])
print(f"Original: {list(ordered.items())}")

ordered.move_to_end("first")        # Move to end
print(f"After move_to_end: {list(ordered.items())}")

removed = ordered.popitem(last=False)         # Remove from beginning
print(f"After popitem: {list(ordered.items())}")
print(f"Removed item: {removed}")

# Output: Original: [('first', 1), ('second', 2), ('third', 3)]
# Output: After move_to_end: [('second', 2), ('third', 3), ('first', 1)]
# Output: After popitem: [('third', 3), ('first', 1)]
# Output: Removed item: ('second', 2)
```

**Real-time Data Engineering Use Cases**:
- Maintaining processing order in data pipelines
- Building LRU (Least Recently Used) caches
- Configuration files where order matters
- Time-series data with ordered timestamps
- Pipeline stage execution tracking

```python
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
                # Remove least recently used (first item)
                self.cache.popitem(last=False)
        self.cache[query] = result

# Usage example
cache = QueryCache(max_size=3)
cache.put("SELECT * FROM users", [{"id": 1, "name": "Alice"}])
cache.put("SELECT * FROM orders", [{"id": 101, "amount": 99.99}])
cache.put("SELECT * FROM products", [{"id": 201, "name": "Laptop"}])

print(list(cache.cache.keys()))
# Output: ['SELECT * FROM users', 'SELECT * FROM orders', 'SELECT * FROM products']

# Access first query (moves to end)
result = cache.get("SELECT * FROM users")
print(list(cache.cache.keys()))
# Output: ['SELECT * FROM orders', 'SELECT * FROM products', 'SELECT * FROM users']

# Add new query (removes least recently used)
cache.put("SELECT * FROM logs", [{"id": 301, "message": "Error"}])
print(list(cache.cache.keys()))
# Output: ['SELECT * FROM products', 'SELECT * FROM users', 'SELECT * FROM logs']
```

### 4. deque (Double-ended queue)
**Description**: Optimized list-like container with fast appends and pops from both ends. Perfect for queues and sliding windows.

**Basic Operations**:
```python
from collections import deque

# Creation
queue = deque([1, 2, 3])
queue = deque(maxlen=5)  # Fixed-size queue

# Operations
queue.append(4)         # Add to right
queue.appendleft(0)     # Add to left
queue.pop()             # Remove from right
queue.popleft()         # Remove from left
queue.rotate(1)         # Rotate elements
```

**Real-time Data Engineering Use Cases**:
- Sliding window calculations in streaming data
- Rate limiting and throttling mechanisms
- Recent events tracking (last N items)
- Breadth-first search in graph processing
- Buffer management in data pipelines

```python
# Real Example: Sliding window for real-time metrics
class SlidingWindowMetrics:
    def __init__(self, window_size=100):
        self.window = deque(maxlen=window_size)
        self.sum = 0
    
    def add_value(self, value):
        if len(self.window) == self.window.maxlen:
            # Remove oldest value from sum
            self.sum -= self.window[0]
        
        self.window.append(value)
        self.sum += value
    
    def get_average(self):
        return self.sum / len(self.window) if self.window else 0

# Usage for response time monitoring
response_times = SlidingWindowMetrics(window_size=10)

# Simulate incoming response times
for time_ms in [120, 95, 200, 85, 150, 110, 300, 90, 180, 75, 250]:
    response_times.add_value(time_ms)
    avg = response_times.get_average()
    print(f"Response time: {time_ms}ms, Rolling avg: {avg:.1f}ms")

# Output:
# Response time: 120ms, Rolling avg: 120.0ms
# Response time: 95ms, Rolling avg: 107.5ms
# Response time: 200ms, Rolling avg: 138.3ms
# ...
# Response time: 250ms, Rolling avg: 153.5ms (last 10 values)

# Rate limiting example
class RateLimiter:
    def __init__(self, max_requests=100, time_window=60):
        self.max_requests = max_requests
        self.requests = deque()
    
    def is_allowed(self, current_time):
        # Remove old requests outside time window
        while self.requests and current_time - self.requests[0] > 60:
            self.requests.popleft()
        
        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
        return False

# Usage
limiter = RateLimiter(max_requests=5, time_window=60)
for i in range(7):
    allowed = limiter.is_allowed(i)
    print(f"Request {i}: {'Allowed' if allowed else 'Rate limited'}")

# Output:
# Request 0: Allowed
# Request 1: Allowed
# Request 2: Allowed
# Request 3: Allowed
# Request 4: Allowed
# Request 5: Rate limited
# Request 6: Rate limited
```

## Advanced Data Structure Patterns

### 1. Nested Data Structures
```python
# Complex nested structure for user analytics
user_analytics = defaultdict(lambda: {
    'sessions': defaultdict(lambda: {
        'page_views': 0,
        'duration': 0,
        'events': []
    }),
    'total_purchases': 0,
    'preferences': set()
})

# Usage
user_id = "user_123"
session_id = "session_456"

user_analytics[user_id]['sessions'][session_id]['page_views'] += 1
user_analytics[user_id]['sessions'][session_id]['events'].append('login')
user_analytics[user_id]['preferences'].add('electronics')

print(f"User {user_id} page views in session {session_id}: "
      f"{user_analytics[user_id]['sessions'][session_id]['page_views']}")
# Output: User user_123 page views in session session_456: 1

print(f"User preferences: {user_analytics[user_id]['preferences']}")
# Output: User preferences: {'electronics'}
```

### 2. Data Pipeline Patterns
```python
# ETL pipeline state management
class PipelineState:
    def __init__(self):
        self.processed_files = set()
        self.error_counts = Counter()
        self.stage_metrics = defaultdict(lambda: {
            'processed': 0,
            'errors': 0,
            'duration': 0
        })
        self.recent_errors = deque(maxlen=100)
    
    def record_file_processed(self, filename):
        self.processed_files.add(filename)
    
    def record_error(self, stage, error_type, error_msg):
        self.error_counts[error_type] += 1
        self.stage_metrics[stage]['errors'] += 1
        self.recent_errors.append({
            'timestamp': time.time(),
            'stage': stage,
            'error': error_type,
            'message': error_msg
        })
    
    def get_health_status(self):
        total_processed = sum(metrics['processed'] for metrics in self.stage_metrics.values())
        total_errors = sum(metrics['errors'] for metrics in self.stage_metrics.values())
        error_rate = (total_errors / total_processed * 100) if total_processed > 0 else 0
        
        return {
            'files_processed': len(self.processed_files),
            'total_records': total_processed,
            'error_rate': f"{error_rate:.2f}%",
            'top_errors': self.error_counts.most_common(3)
        }

# Usage example
pipeline = PipelineState()
pipeline.record_file_processed("data_2024_01_15.csv")
pipeline.stage_metrics['extract']['processed'] += 1000
pipeline.record_error('transform', 'ValidationError', 'Invalid date format')

health = pipeline.get_health_status()
print(f"Pipeline health: {health}")
# Output: Pipeline health: {'files_processed': 1, 'total_records': 1000, 
#                          'error_rate': '0.10%', 'top_errors': [('ValidationError', 1)]}
```

## Performance Considerations

### Time Complexity Summary
| Operation | List | Dict | Set | deque |
|-----------|------|------|-----|-------|
| Access by index | O(1) | N/A | N/A | O(1) |
| Search | O(n) | O(1) | O(1) | O(n) |
| Insert at end | O(1) | O(1) | O(1) | O(1) |
| Insert at beginning | O(n) | N/A | N/A | O(1) |
| Delete | O(n) | O(1) | O(1) | O(1) |

### Memory Usage Tips
```python
# Use generators for large datasets
def process_large_file(filename):
    with open(filename) as f:
        for line in f:  # Generator - processes one line at a time
            yield process_line(line)

# Use slots for memory-efficient classes
class Transaction:
    __slots__ = ['id', 'amount', 'timestamp', 'user_id']
    
    def __init__(self, id, amount, timestamp, user_id):
        self.id = id
        self.amount = amount
        self.timestamp = timestamp
        self.user_id = user_id

# Use appropriate data structures
# For membership testing: set() instead of list
# For counting: Counter() instead of dict
# For ordered data: deque() instead of list for frequent insertions/deletions
```

## Best Practices for Data Engineering

1. **Choose the right data structure** based on your access patterns
2. **Use defaultdict** to eliminate key existence checks
3. **Use Counter** for frequency analysis instead of manual counting
4. **Use deque** for sliding windows and queues
5. **Use sets** for fast membership testing and deduplication
6. **Consider memory usage** for large-scale data processing
7. **Profile your code** to identify bottlenecks
8. **Use type hints** for better code documentation and IDE support

```python
from typing import Dict, List, Set, Counter as CounterType
from collections import defaultdict, Counter, deque

def analyze_user_behavior(events: List[Dict]) -> Dict[str, any]:
    """Analyze user behavior from event stream."""
    user_sessions: Dict[str, Dict] = defaultdict(lambda: {
        'page_views': 0,
        'unique_pages': set(),
        'session_duration': 0
    })
    
    event_counts: CounterType[str] = Counter()
    recent_events: deque = deque(maxlen=1000)
    
    for event in events:
        user_id = event['user_id']
        event_type = event['event_type']
        
        # Update counters
        event_counts[event_type] += 1
        recent_events.append(event)
        
        # Update user session data
        if event_type == 'page_view':
            user_sessions[user_id]['page_views'] += 1
            user_sessions[user_id]['unique_pages'].add(event['page'])
    
    return {
        'total_users': len(user_sessions),
        'event_distribution': dict(event_counts.most_common()),
        'avg_pages_per_user': sum(data['page_views'] for data in user_sessions.values()) / len(user_sessions)
    }

# Example usage
events = [
    {'user_id': 'user1', 'event_type': 'page_view', 'page': 'home'},
    {'user_id': 'user1', 'event_type': 'click', 'element': 'button'},
    {'user_id': 'user2', 'event_type': 'page_view', 'page': 'products'}
]

result = analyze_user_behavior(events)
print(f"Analysis result: {result}")
# Output: Analysis result: {'total_users': 2, 'event_distribution': {'page_view': 2, 'click': 1}, 'avg_pages_per_user': 1.0}
```

---

## Interview Questions

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
```

### Q3: When would you use Counter vs defaultdict vs regular dict?

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
students = [("Alice", "Math"), ("Bob", "Science"), ("Alice", "English")]

subjects_dd = defaultdict(list)
for student, subject in students:
    subjects_dd[student].append(subject)

print(f"defaultdict result: {dict(subjects_dd)}")
# Output: defaultdict result: {'Alice': ['Math', 'English'], 'Bob': ['Science']}
```

### Q4: Implement a LRU cache using OrderedDict.

**Answer:**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

# Test the LRU cache
lru = LRUCache(3)
lru.put(1, "one")
lru.put(2, "two")
lru.put(3, "three")
print(f"Cache: {list(lru.cache.items())}")
# Output: Cache: [(1, 'one'), (2, 'two'), (3, 'three')]

lru.get(1)  # Access key 1
print(f"After accessing 1: {list(lru.cache.items())}")
# Output: After accessing 1: [(2, 'two'), (3, 'three'), (1, 'one')]

lru.put(4, "four")  # Evicts key 2
print(f"After adding 4: {list(lru.cache.items())}")
# Output: After adding 4: [(3, 'three'), (1, 'one'), (4, 'four')]
```

### Q5: How would you implement a sliding window maximum using deque?

**Answer:**
```python
from collections import deque

def sliding_window_maximum(nums, k):
    """Find maximum in each sliding window of size k."""
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
```

### Q6: Design a data structure that supports insert, delete, and getRandom in O(1) time.

**Answer:**
```python
import random

class RandomizedSet:
    def __init__(self):
        self.data = []  # Store actual values
        self.indices = {}  # Map value to index
    
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
        index_to_remove = self.indices[val]
        last_element = self.data[-1]
        
        self.data[index_to_remove] = last_element
        self.indices[last_element] = index_to_remove
        
        # Remove last element
        self.data.pop()
        del self.indices[val]
        return True
    
    def getRandom(self):
        return random.choice(self.data) if self.data else None

# Test RandomizedSet
rs = RandomizedSet()
print(f"Insert 1: {rs.insert(1)}")
print(f"Insert 2: {rs.insert(2)}")
print(f"Insert 3: {rs.insert(3)}")
print(f"Data: {rs.data}")
# Output: Insert 1: True
# Output: Insert 2: True
# Output: Insert 3: True
# Output: Data: [1, 2, 3]

print(f"Remove 2: {rs.remove(2)}")
print(f"Data after removal: {rs.data}")
# Output: Remove 2: True
# Output: Data after removal: [1, 3]
```

### Q7: Compare time complexity of operations on different data structures.

**Answer:**
```python
import time

def time_operation(func, iterations=10000):
    start = time.time()
    for _ in range(iterations):
        func()
    return (time.time() - start) / iterations

# Test data
small_list = list(range(100))
large_list = list(range(10000))
small_set = set(range(100))
large_set = set(range(10000))

# Search operations
search_item = 50

list_search_small = time_operation(lambda: search_item in small_list)
list_search_large = time_operation(lambda: search_item in large_list, 1000)
set_search_small = time_operation(lambda: search_item in small_set)
set_search_large = time_operation(lambda: search_item in large_set)

print(f"Search in small list: {list_search_small:.8f}s")
print(f"Search in large list: {list_search_large:.8f}s")
print(f"Search in small set: {set_search_small:.8f}s")
print(f"Search in large set: {set_search_large:.8f}s")
# Output: Search in small list: 0.00000120s
# Output: Search in large list: 0.00012000s
# Output: Search in small set: 0.00000015s
# Output: Search in large set: 0.00000015s

print(f"List search scales O(n): {list_search_large/list_search_small:.1f}x")
print(f"Set search scales O(1): {set_search_large/set_search_small:.1f}x")
# Output: List search scales O(n): 100.0x
# Output: Set search scales O(1): 1.0x
```

### Q8: Design an autocomplete system using Trie.

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
    
    def insert(self, word, frequency=1):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_word = True
        node.frequency += frequency
    
    def get_suggestions(self, prefix, limit=5):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all words with this prefix
        words = []
        self._collect_words(node, prefix.lower(), words)
        
        # Sort by frequency and return top suggestions
        words.sort(key=lambda x: x[1], reverse=True)
        return [word for word, freq in words[:limit]]
    
    def _collect_words(self, node, prefix, words):
        if node.is_end_word:
            words.append((prefix, node.frequency))
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, words)

# Test autocomplete
autocomplete = AutoComplete()
vocabulary = [("python", 100), ("programming", 80), ("program", 60), ("project", 70)]

for word, freq in vocabulary:
    autocomplete.insert(word, freq)

suggestions = autocomplete.get_suggestions("pro")
print(f"Suggestions for 'pro': {suggestions}")
# Output: Suggestions for 'pro': ['programming', 'project', 'program']
```

### Performance Guidelines

| Operation | Best Choice | Time Complexity | Use Case |
|-----------|-------------|-----------------|----------|
| Membership testing | set | O(1) | Checking if item exists |
| Counting items | Counter | O(1) per item | Frequency analysis |
| Ordered insertion | list | O(1) at end | Sequential processing |
| Key-value lookup | dict | O(1) average | Fast data retrieval |
| Priority processing | heapq | O(log n) | Task scheduling |
| Sliding windows | deque | O(1) both ends | Stream processing |
| Grouping data | defaultdict | O(1) per group | Data aggregation |
``` to end (most recently used)
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

**Basic Operations**:
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

print(f"Queue after operations: {list(queue)}")
print(f"Left removed: {left}, Right removed: {right}")
# Output: Queue after operations: [3, 1, 2]
# Output: Left removed: 0, Right removed: 4
```

**Real-time Data Engineering Use Cases**:
- Sliding window calculations (moving averages, recent events)
- Stream buffering and rate limiting
- Undo/redo functionality in data processing
- Recent activity tracking
- Queue-based task processing

```python
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

**Basic Operations**:
```python
from collections import namedtuple

# Creation
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)

# Access
print(p.x, p.y)            # Named access
print(p[0], p[1])          # Index access

# Convert to dict
point_dict = p._asdict()
```

**Real-time Data Engineering Use Cases**:
- Structured data records in pipelines
- Configuration objects that shouldn't change
- Return multiple values from functions clearly
- Database row representations
- API response parsing into structured objects

```python
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
**Description**: Binary heap implementation providing O(log n) insertion/deletion. Essential for priority-based processing and finding top-K elements.

**Basic Operations**:
```python
import heapq

# Min heap
heap = [3, 1, 4, 1, 5]
print(f"Original list: {heap}")
heapq.heapify(heap)         # Convert to heap
print(f"After heapify: {heap}")
heapq.heappush(heap, 2)     # Add element
print(f"After push(2): {heap}")
smallest = heapq.heappop(heap)  # Remove smallest
print(f"Smallest removed: {smallest}")
print(f"Heap after pop: {heap}")
# Output: Original list: [3, 1, 4, 1, 5]
# Output: After heapify: [1, 1, 4, 3, 5]
# Output: After push(2): [1, 1, 2, 3, 5, 4]
# Output: Smallest removed: 1
# Output: Heap after pop: [1, 3, 2, 4, 5]

# Top K elements
data = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
top_k = heapq.nlargest(3, data)
bottom_k = heapq.nsmallest(3, data)
print(f"Data: {data}")
print(f"Top 3 largest: {top_k}")
print(f"Top 3 smallest: {bottom_k}")
# Output: Data: [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
# Output: Top 3 largest: [42, 37, 23]
# Output: Top 3 smallest: [-4, 1, 2]
```

**Real-time Data Engineering Use Cases**:
- Priority-based task scheduling in data pipelines
- Finding top-K most frequent items in streams
- Monitoring system alerts by severity
- Load balancing based on server capacity
- Real-time recommendation systems

```python
# Real Example: Priority-based data processing
class PriorityTask:
    def __init__(self, priority, task_id, data):
        self.priority = priority
        self.task_id = task_id
        self.data = data
    
    def __lt__(self, other):
        return self.priority < other.priority  # Lower number = higher priority

# Task queue for data processing
task_queue = []
heapq.heappush(task_queue, PriorityTask(1, "critical_etl", {"table": "orders"}))
heapq.heappush(task_queue, PriorityTask(5, "daily_report", {"report": "sales"}))

# Process tasks by priority
while task_queue:
    task = heapq.heappop(task_queue)
    print(f"Processing: {task.task_id} (priority: {task.priority})")

# Real-time top-K analysis
top_products = []
for sale in daily_sales:
    if len(top_products) < 5:
        heapq.heappush(top_products, (sale["quantity"], sale["product_id"]))
    elif sale["quantity"] > top_products[0][0]:
        heapq.heapreplace(top_products, (sale["quantity"], sale["product_id"]))
```

### 2. Queue
**Description**: Thread-safe queue implementations for concurrent data processing. Essential for producer-consumer patterns and multi-threaded pipelines.

**Basic Operations**:
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

**Real-time Data Engineering Use Cases**:
- Multi-threaded data processing pipelines
- Producer-consumer patterns for stream processing
- Task distribution across worker threads
- Rate limiting and buffering in data ingestion
- Coordinating parallel ETL processes

```python
# Real Example: Multi-threaded data processing
class DataProcessor:
    def __init__(self, num_workers=4):
        self.input_queue = Queue(maxsize=1000)  # Bounded queue for backpressure
        self.output_queue = Queue()
    
    def worker(self):
        while True:
            data = self.input_queue.get()
            if data is None:  # Shutdown signal
                break
            processed = self.transform_data(data)
            self.output_queue.put(processed)
            self.input_queue.task_done()
    
    def transform_data(self, data):
        return {"processed": data, "timestamp": time.time()}

# Priority-based alert processing
alert_queue = PriorityQueue()
alert_queue.put((1, "CRITICAL: Database down"))
alert_queue.put((3, "WARNING: High CPU usage"))

while not alert_queue.empty():
    priority, message = alert_queue.get()
    handle_alert(priority, message)

# LIFO for undo operations
undo_stack = LifoQueue()
undo_stack.put(("operation", data_backup))
```

### 3. Array (array module)
**Description**: Memory-efficient arrays for homogeneous numeric data. Much more space-efficient than lists for large numeric datasets.

**Basic Operations**:
```python
import array

# Creation
numbers = array.array('i', [1, 2, 3, 4])  # 'i' for integers
floats = array.array('f', [1.1, 2.2, 3.3])  # 'f' for floats

# Operations
numbers.append(5)
numbers.extend([6, 7])

# Binary file operations
with open('data.bin', 'wb') as f:
    numbers.tofile(f)
```

**Real-time Data Engineering Use Cases**:
- Processing large numeric datasets (sensor data, financial data)
- Memory-efficient storage of time series data
- Interfacing with C libraries and binary data
- High-performance numeric computations
- Reducing memory footprint in data-intensive applications

```python
# Real Example: Sensor data processing
class SensorDataBuffer:
    def __init__(self):
        self.readings = array.array('f')  # 4 bytes per reading vs 28 for list
        self.timestamps = array.array('L')  # Unsigned long for timestamps
    
    def add_reading(self, value, timestamp):
        self.readings.append(float(value))
        self.timestamps.append(int(timestamp))
    
    def get_average(self):
        return sum(self.readings) / len(self.readings) if self.readings else 0

# Process IoT sensor data
temp_sensor = SensorDataBuffer()
sensor_readings = [(23.5, 1642248000), (24.1, 1642248060), (23.8, 1642248120)]

for temp, timestamp in sensor_readings:
    temp_sensor.add_reading(temp, timestamp)

avg_temp = temp_sensor.get_average()
print(f"Average temperature: {avg_temp:.1f}°C")

# Memory efficiency comparison
import sys
list_data = [1.0] * 100000
array_data = array.array('f', [1.0] * 100000)
print(f"List: {sys.getsizeof(list_data):,} bytes")
print(f"Array: {sys.getsizeof(array_data):,} bytes")  # ~75% less memory
```

### 4. Enum
**Description**: Enumerated constants that provide readable, type-safe alternatives to magic numbers and strings. Essential for maintaining data integrity.

**Basic Operations**:
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
print(current_status.name)   # "PENDING"
print(current_status.value)  # 1
```

**Real-time Data Engineering Use Cases**:
- Data pipeline status tracking
- Data quality validation states
- ETL process stages and outcomes
- API response status codes
- Configuration options and feature flags

```python
# Real Example: Data pipeline status management
class PipelineStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class ProcessingStage(Enum):
    EXTRACT = auto()
    VALIDATE = auto()
    TRANSFORM = auto()
    LOAD = auto()

# Pipeline execution tracking
class DataPipelineRun:
    def __init__(self, pipeline_id):
        self.pipeline_id = pipeline_id
        self.status = PipelineStatus.PENDING
        self.current_stage = None
    
    def start_stage(self, stage: ProcessingStage):
        self.current_stage = stage
        self.status = PipelineStatus.RUNNING
        print(f"Pipeline {self.pipeline_id}: Starting {stage.name}")

# Configuration management
class Environment(Enum):
    DEV = "development"
    STAGING = "staging"
    PROD = "production"

def get_database_config(env: Environment):
    configs = {
        Environment.DEV: {"host": "dev-db", "pool_size": 5},
        Environment.PROD: {"host": "prod-db", "pool_size": 50}
    }
    return configs[env]

# Type-safe configuration
config = get_database_config(Environment.PROD)
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