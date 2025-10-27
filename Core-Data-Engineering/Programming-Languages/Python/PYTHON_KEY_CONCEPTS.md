# 🐍 Python Key Concepts for Data Engineering

> **The complete guide to Python for data engineering - from basics to advanced concepts**

## 📋 Table of Contents

### 🚀 **Getting Started**
1. [Why Python for Data Engineering?](#-why-python-for-data-engineering)
2. [Python Basics Made Simple](#-python-basics-made-simple)
3. [Essential Data Types](#-essential-data-types)

### 💼 **Core Skills**
4. [Working with Data](#-working-with-data)
5. [File Operations](#-file-operations)
6. [Database Connections](#-database-connections)
7. [API Integration](#-api-integration)

### 🏗️ **Advanced Concepts**
8. [Object-Oriented Programming](#-object-oriented-programming)
9. [Error Handling](#-error-handling)
10. [Best Practices](#-best-practices)
11. [Interview Preparation](#-interview-preparation)

---

## 🎯 Why Python for Data Engineering?

**Think of Python as the Swiss Army knife of data engineering** - it's versatile, reliable, and has a tool for every job.

### ✅ **What Makes Python Perfect for Data Engineering**

| **Advantage** | **What It Means** | **Real Example** |
|---------------|-------------------|------------------|
| **Simple Syntax** | Code reads like English | `if user_age > 18: process_data()` |
| **Rich Libraries** | Pre-built tools for everything | Pandas for data, Requests for APIs |
| **Easy Integration** | Connects to any system | PostgreSQL, AWS, Kafka, REST APIs |
| **Huge Community** | Solutions exist for every problem | Stack Overflow, GitHub, tutorials |
| **Scalable** | From simple scripts to enterprise systems | Netflix, Uber, Instagram use Python |

### 🔧 **Python in the Data Engineering Workflow**

```
📊 Data Sources → 🐍 Python Scripts → 🗄️ Data Storage → 📈 Analytics
     ↓                    ↓                   ↓              ↓
  APIs, Files         Extract &           Databases,      Dashboards,
  Databases          Transform            Data Lakes       Reports
```

### 📚 **Learning Path**

**🆕 New to Programming?** Start here → [Python Basics](#-python-basics-made-simple)  
**💼 Have Programming Experience?** Jump to → [Working with Data](#-working-with-data)  
**🎯 Interview Prep?** Go to → [Interview Preparation](#-interview-preparation)

### 📖 **Related Resources**
- **[Python Quick Reference](./PYTHON_QUICK_REFERENCE.md)** - Cheat sheet for daily use
- **[Python Interview Questions](./PYTHON_INTERVIEW_QUESTIONS.md)** - Practice questions with answers
- **[Python Advanced Patterns](./PYTHON_ADVANCED_DATA_ENGINEERING.md)** - Production-ready code patterns

---

## 🚀 Python Basics Made Simple

> **Think of variables as labeled boxes that hold your data**

### 📦 Variables - Your Data Containers

```python
# Variables are like labeled boxes - you put data in them
user_name = "Alice"           # Text goes in quotes
user_age = 25                 # Numbers don't need quotes  
user_salary = 75000.50        # Decimals are allowed
is_employee = True            # True/False (note the capital T/F)

# Python is smart - it figures out the type automatically
print(f"Name: {user_name} (type: {type(user_name).__name__})")
print(f"Age: {user_age} (type: {type(user_age).__name__})")
print(f"Salary: ${user_salary} (type: {type(user_salary).__name__})")
print(f"Is employee: {is_employee} (type: {type(is_employee).__name__})")

# Output:
# Name: Alice (type: str)
# Age: 25 (type: int) 
# Salary: $75000.5 (type: float)
# Is employee: True (type: bool)
```

### 📝 String Formatting - Making Text Look Nice

```python
# f-strings are the modern way (Python 3.6+)
records_processed = 1500
success_rate = 0.95

# Put variables inside {} with f at the start
message = f"Processed {records_processed} records with {success_rate:.1%} success"
print(message)
# Output: Processed 1500 records with 95.0% success

# You can do math inside f-strings
total_cost = 100
tax_rate = 0.08
final_message = f"Total with tax: ${total_cost * (1 + tax_rate):.2f}"
print(final_message)
# Output: Total with tax: $108.00
```

### 🔀 Making Decisions - If/Else Statements

> **Think of if/else like a flowchart - Python follows the path based on conditions**

```python
# Simple decision making
file_size_mb = 250

if file_size_mb < 100:
    category = "small"
    processing_time = "fast"
elif file_size_mb < 1000:  # elif = "else if"
    category = "medium" 
    processing_time = "moderate"
else:
    category = "large"
    processing_time = "slow"

print(f"File size: {file_size_mb}MB is {category} - processing will be {processing_time}")
# Output: File size: 250MB is medium - processing will be moderate
```

### 🔁 Loops - Repeating Tasks

```python
# For loop - when you know what you want to loop through
file_sizes = [50, 250, 1500, 5000]

print("Analyzing file sizes:")
for size in file_sizes:
    if size < 100:
        print(f"  {size}MB: Small file - quick to process")
    elif size < 1000:
        print(f"  {size}MB: Medium file - normal processing")
    else:
        print(f"  {size}MB: Large file - will take time")

# Output:
# Analyzing file sizes:
#   50MB: Small file - quick to process
#   250MB: Medium file - normal processing
#   1500MB: Large file - will take time
#   5000MB: Large file - will take time
```

### 🛠️ Functions - Reusable Code Blocks

> **Functions are like recipes - you define them once, then use them many times**

```python
# Simple function
def calculate_file_processing_time(file_size_mb, speed_mbps=10):
    """Calculate how long it takes to process a file"""
    processing_time = file_size_mb / speed_mbps
    return processing_time

# Using the function
small_file = calculate_file_processing_time(100)  # Uses default speed
large_file = calculate_file_processing_time(1000, speed_mbps=50)  # Custom speed

print(f"Small file (100MB): {small_file} seconds")
print(f"Large file (1000MB at 50MB/s): {large_file} seconds")
# Output:
# Small file (100MB): 10.0 seconds
# Large file (1000MB at 50MB/s): 20.0 seconds
```

---

## 📦 Essential Data Types

> **Python has different containers for different types of data - like having different boxes for different things**

### 📋 Lists - Ordered Collections You Can Change

**Think of lists like a shopping list - items in order, you can add/remove items**

```python
# Creating a list of data sources
data_sources = ["PostgreSQL", "MongoDB", "Kafka"]
print(f"Original sources: {data_sources}")
# Output: Original sources: ['PostgreSQL', 'MongoDB', 'Kafka']

# Adding items (like adding to your shopping list)
data_sources.append("Redis")              # Add one item at the end
data_sources.extend(["Elasticsearch"])    # Add multiple items
data_sources.insert(1, "MySQL")           # Insert at position 1

print(f"After additions: {data_sources}")
# Output: After additions: ['PostgreSQL', 'MySQL', 'MongoDB', 'Kafka', 'Redis', 'Elasticsearch']

# Accessing items (counting starts at 0!)
first_source = data_sources[0]    # First item
last_source = data_sources[-1]    # Last item
middle_sources = data_sources[1:3] # Items 1 and 2 (not including 3)

print(f"First: {first_source}, Last: {last_source}")
print(f"Middle items: {middle_sources}")
# Output: First: PostgreSQL, Last: Elasticsearch
# Output: Middle items: ['MySQL', 'MongoDB']
```

### 📝 Dictionaries - Key-Value Pairs

**Think of dictionaries like a phone book - you look up a name (key) to get a number (value)**

```python
# Database connection info
db_config = {
    "host": "localhost",
    "port": 5432,
    "database": "sales_data",
    "username": "data_engineer",
    "ssl_enabled": True
}

print("Database configuration:")
for key, value in db_config.items():
    print(f"  {key}: {value}")

# Output:
# Database configuration:
#   host: localhost
#   port: 5432
#   database: sales_data
#   username: data_engineer
#   ssl_enabled: True

# Accessing values safely
host = db_config.get("host", "unknown")           # Get host, default to "unknown"
timeout = db_config.get("timeout", 30)            # Get timeout, default to 30

print(f"Connecting to {host} with {timeout}s timeout")
# Output: Connecting to localhost with 30s timeout

# Adding new configuration
db_config["created_date"] = "2024-01-15"
db_config.update({"environment": "production", "backup_enabled": True})

print(f"Updated config has {len(db_config)} settings")
# Output: Updated config has 7 settings
```

### 📦 Tuples - Ordered Collections You Can't Change

**Think of tuples like coordinates (x, y) - the order matters and you can't change them**

```python
# Database connection details that shouldn't change
db_connection = ("prod-server", 5432, "analytics_db")
host, port, database = db_connection  # Unpacking

print(f"Connecting to {database} on {host}:{port}")
# Output: Connecting to analytics_db on prod-server:5432

# Tuples are immutable - you can't change them after creation
# Good for configuration that shouldn't change
api_endpoints = (
    ("users", "/api/v1/users"),
    ("orders", "/api/v1/orders"),
    ("products", "/api/v1/products")
)

for name, endpoint in api_endpoints:
    print(f"{name.title()} API: {endpoint}")
# Output:
# Users API: /api/v1/users
# Orders API: /api/v1/orders
# Products API: /api/v1/products
```

### 🎯 Sets - Unique Collections

**Think of sets like a bag of unique items - no duplicates allowed**

```python
# Remove duplicates from data
raw_user_ids = [1, 2, 3, 2, 4, 1, 5, 3]
unique_user_ids = set(raw_user_ids)

print(f"Raw IDs: {raw_user_ids}")
print(f"Unique IDs: {sorted(unique_user_ids)}")
# Output:
# Raw IDs: [1, 2, 3, 2, 4, 1, 5, 3]
# Unique IDs: [1, 2, 3, 4, 5]

# Set operations for data analysis
active_users = {1, 2, 3, 4, 5}
premium_users = {3, 4, 5, 6, 7}

# Who is both active AND premium?
both = active_users & premium_users
print(f"Active premium users: {both}")
# Output: Active premium users: {3, 4, 5}

# Who is active but NOT premium?
active_only = active_users - premium_users
print(f"Active non-premium users: {active_only}")
# Output: Active non-premium users: {1, 2}
```

---

## 💼 Working with Data

### 📊 List Comprehensions - Elegant Data Processing

**Think of list comprehensions as a compact way to transform data**

```python
# Traditional way
file_sizes_mb = [10, 250, 1500, 50, 3000]
large_files = []
for size in file_sizes_mb:
    if size > 100:
        large_files.append(size)

# List comprehension way (more Pythonic)
large_files = [size for size in file_sizes_mb if size > 100]
print(f"Large files: {large_files}")
# Output: Large files: [250, 1500, 3000]

# Transform data while filtering
file_info = [(size, "large" if size > 1000 else "medium") 
             for size in file_sizes_mb if size > 100]
print(f"File categories: {file_info}")
# Output: File categories: [(250, 'medium'), (1500, 'large'), (3000, 'large')]
```

### 🔄 Working with JSON Data

```python
import json

# Sample API response
api_response = '''
{
    "users": [
        {"id": 1, "name": "Alice", "department": "Engineering"},
        {"id": 2, "name": "Bob", "department": "Sales"}
    ],
    "total_count": 2,
    "status": "success"
}
'''

# Parse JSON
data = json.loads(api_response)

# Extract information
user_count = data["total_count"]
engineering_users = [user["name"] for user in data["users"] 
                    if user["department"] == "Engineering"]

print(f"Total users: {user_count}")
print(f"Engineering team: {engineering_users}")
# Output:
# Total users: 2
# Engineering team: ['Alice']
```

---

## 📁 File Operations

### 📖 Reading Files Safely

```python
# Always use 'with' statement - it automatically closes files

# Reading a CSV file
try:
    with open('sales_data.csv', 'r') as file:
        lines = file.readlines()
        print(f"Read {len(lines)} lines from file")
        
        # Process first few lines
        for i, line in enumerate(lines[:3]):
            print(f"Line {i+1}: {line.strip()}")
except FileNotFoundError:
    print("File not found - check the path")
except Exception as e:
    print(f"Error reading file: {e}")
```

### ✍️ Writing Files

```python
# Writing processed data
processed_data = [
    "user_id,name,processed_date",
    "1,Alice,2024-01-15",
    "2,Bob,2024-01-15"
]

with open('processed_users.csv', 'w') as file:
    for line in processed_data:
        file.write(line + '\n')
        
print("Data written successfully")
```

---

## 🗄️ Database Connections

### 🐘 PostgreSQL Example

```python
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Safe database connection with automatic cleanup"""
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="analytics",
            user="data_engineer",
            password="your_password"
        )
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Using the connection
with get_db_connection() as conn:
    cursor = conn.cursor()
    
    # Execute query
    cursor.execute("SELECT COUNT(*) FROM users WHERE active = true")
    active_users = cursor.fetchone()[0]
    
    print(f"Active users: {active_users}")
```

---

## 🌐 API Integration

### 📡 Making HTTP Requests

```python
import requests
import json

def fetch_user_data(user_id):
    """Fetch user data from API with error handling"""
    try:
        response = requests.get(
            f"https://api.example.com/users/{user_id}",
            headers={"Authorization": "Bearer your_token"},
            timeout=10
        )
        
        response.raise_for_status()  # Raises exception for bad status codes
        return response.json()
        
    except requests.exceptions.Timeout:
        print(f"Timeout fetching user {user_id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user {user_id}: {e}")
        return None

# Batch processing
user_ids = [1, 2, 3, 4, 5]
successful_fetches = 0

for user_id in user_ids:
    user_data = fetch_user_data(user_id)
    if user_data:
        successful_fetches += 1
        print(f"Fetched data for user {user_id}: {user_data.get('name', 'Unknown')}")

print(f"Successfully fetched {successful_fetches}/{len(user_ids)} users")
```

---

## 🏗️ Object-Oriented Programming

### 📦 Classes for Data Processing

```python
class DataProcessor:
    """A reusable data processing class"""
    
    def __init__(self, source_name):
        self.source_name = source_name
        self.processed_count = 0
        self.errors = []
    
    def process_record(self, record):
        """Process a single record"""
        try:
            # Simulate processing
            if 'id' not in record:
                raise ValueError("Record missing required 'id' field")
            
            # Add processing timestamp
            record['processed_at'] = '2024-01-15T10:30:00Z'
            self.processed_count += 1
            return record
            
        except Exception as e:
            self.errors.append(f"Error processing record: {e}")
            return None
    
    def get_summary(self):
        """Get processing summary"""
        return {
            'source': self.source_name,
            'processed': self.processed_count,
            'errors': len(self.errors),
            'success_rate': self.processed_count / (self.processed_count + len(self.errors)) if (self.processed_count + len(self.errors)) > 0 else 0
        }

# Using the class
processor = DataProcessor("user_data")

# Sample records
records = [
    {'id': 1, 'name': 'Alice'},
    {'name': 'Bob'},  # Missing ID - will cause error
    {'id': 3, 'name': 'Charlie'}
]

# Process records
processed_records = []
for record in records:
    result = processor.process_record(record)
    if result:
        processed_records.append(result)

# Get summary
summary = processor.get_summary()
print(f"Processing summary: {summary}")
# Output: Processing summary: {'source': 'user_data', 'processed': 2, 'errors': 1, 'success_rate': 0.6666666666666666}
```

---

## ⚠️ Error Handling

### 🛡️ Robust Error Handling Patterns

```python
def safe_divide(a, b):
    """Division with comprehensive error handling"""
    try:
        result = a / b
        return {'success': True, 'result': result, 'error': None}
    except ZeroDivisionError:
        return {'success': False, 'result': None, 'error': 'Cannot divide by zero'}
    except TypeError:
        return {'success': False, 'result': None, 'error': 'Invalid input types'}
    except Exception as e:
        return {'success': False, 'result': None, 'error': f'Unexpected error: {e}'}

# Testing different scenarios
test_cases = [(10, 2), (10, 0), (10, 'invalid'), (None, 5)]

for a, b in test_cases:
    result = safe_divide(a, b)
    if result['success']:
        print(f"{a} ÷ {b} = {result['result']}")
    else:
        print(f"Error with {a} ÷ {b}: {result['error']}")

# Output:
# 10 ÷ 2 = 5.0
# Error with 10 ÷ 0: Cannot divide by zero
# Error with 10 ÷ invalid: Invalid input types
# Error with None ÷ 5: Invalid input types
```

---

## ✨ Best Practices

### 🎯 Code Quality Guidelines

```python
# ✅ GOOD: Clear, descriptive names
def calculate_monthly_revenue(sales_data, tax_rate=0.08):
    """Calculate monthly revenue including tax"""
    total_sales = sum(sale['amount'] for sale in sales_data)
    revenue_with_tax = total_sales * (1 + tax_rate)
    return round(revenue_with_tax, 2)

# ❌ BAD: Unclear names and no documentation
def calc(data, rate=0.08):
    total = sum(x['amount'] for x in data)
    return total * (1 + rate)

# ✅ GOOD: Use constants for magic numbers
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
VALID_FILE_EXTENSIONS = ['.csv', '.json', '.parquet']

def process_file(file_path):
    """Process file with validation"""
    # Check file extension
    if not any(file_path.endswith(ext) for ext in VALID_FILE_EXTENSIONS):
        raise ValueError(f"Unsupported file type. Supported: {VALID_FILE_EXTENSIONS}")
    
    # Process with retry logic
    for attempt in range(MAX_RETRY_ATTEMPTS):
        try:
            # File processing logic here
            return "Success"
        except Exception as e:
            if attempt == MAX_RETRY_ATTEMPTS - 1:
                raise e
            print(f"Attempt {attempt + 1} failed, retrying...")
```

### 🔧 Performance Tips

```python
# ✅ GOOD: Use generators for large datasets
def process_large_dataset(file_path):
    """Memory-efficient processing using generators"""
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            # Process one line at a time
            processed_line = line.strip().upper()
            yield {'line_number': line_num, 'data': processed_line}

# ✅ GOOD: Use list comprehensions for simple transformations
user_ids = [1, 2, 3, 4, 5]
user_urls = [f"https://api.example.com/users/{uid}" for uid in user_ids]

# ✅ GOOD: Use enumerate instead of manual counters
data_sources = ['PostgreSQL', 'MongoDB', 'Redis']
for index, source in enumerate(data_sources):
    print(f"{index + 1}. {source}")
```

---

## 🎯 Interview Preparation

### 🔥 Common Python Interview Questions

#### **Q1: Explain the difference between lists and tuples**

```python
# Lists - mutable (can be changed)
data_sources = ['PostgreSQL', 'MongoDB']
data_sources.append('Redis')  # ✅ This works
print(data_sources)  # ['PostgreSQL', 'MongoDB', 'Redis']

# Tuples - immutable (cannot be changed)
db_config = ('localhost', 5432, 'production')
# db_config.append('new_item')  # ❌ This would cause an error

# When to use each:
# Lists: When data might change (user inputs, processing results)
# Tuples: When data is fixed (coordinates, configuration, database connections)
```

#### **Q2: How do you handle missing values in a dictionary?**

```python
user_data = {'name': 'Alice', 'age': 30}

# ❌ BAD: Can cause KeyError
# email = user_data['email']  # KeyError if 'email' doesn't exist

# ✅ GOOD: Safe approaches
email = user_data.get('email', 'no-email@example.com')  # Default value
department = user_data.get('department')  # Returns None if not found

# ✅ GOOD: Check if key exists
if 'phone' in user_data:
    phone = user_data['phone']
else:
    phone = 'Phone not provided'

print(f"Email: {email}, Department: {department}, Phone: {phone}")
```

#### **Q3: Write a function to remove duplicates while preserving order**

```python
def remove_duplicates_preserve_order(items):
    """Remove duplicates while keeping original order"""
    seen = set()
    result = []
    
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result

# Test the function
data = [1, 2, 3, 2, 4, 1, 5, 3]
clean_data = remove_duplicates_preserve_order(data)
print(f"Original: {data}")
print(f"Clean: {clean_data}")
# Output:
# Original: [1, 2, 3, 2, 4, 1, 5, 3]
# Clean: [1, 2, 3, 4, 5]
```

#### **Q4: How do you efficiently process large files?**

```python
def process_large_file_efficiently(file_path, batch_size=1000):
    """Process large files in batches to manage memory"""
    batch = []
    processed_count = 0
    
    with open(file_path, 'r') as file:
        for line in file:
            batch.append(line.strip())
            
            # Process when batch is full
            if len(batch) >= batch_size:
                # Process the batch
                processed_count += len(batch)
                print(f"Processed batch of {len(batch)} items. Total: {processed_count}")
                batch = []  # Clear batch
        
        # Process remaining items
        if batch:
            processed_count += len(batch)
            print(f"Processed final batch of {len(batch)} items. Total: {processed_count}")
    
    return processed_count
```

### 🎯 **Key Takeaways for Interviews**

1. **Always handle errors gracefully** - Use try/except blocks
2. **Write readable code** - Clear variable names and comments
3. **Consider memory efficiency** - Use generators for large datasets
4. **Know when to use each data type** - Lists vs tuples vs sets vs dictionaries
5. **Practice common patterns** - List comprehensions, file handling, API calls

---

## 🚀 Next Steps

### 📚 **Continue Learning**
- **[Python Interview Questions](./PYTHON_INTERVIEW_QUESTIONS.md)** - Practice with real interview questions
- **[Python Quick Reference](./PYTHON_QUICK_REFERENCE.md)** - Handy cheat sheet
- **[Pandas vs Spark](./PANDAS_VS_SPARK_INTERVIEW_QUESTIONS.md)** - When to use each tool

### 🛠️ **Practice Projects**
1. **CSV Data Processor** - Read, clean, and transform CSV files
2. **API Data Pipeline** - Fetch data from REST APIs and store in database
3. **Log File Analyzer** - Parse and analyze application logs
4. **Database ETL Script** - Extract, transform, and load data between systems

### 📖 **Advanced Topics**
- **Async Programming** - For handling multiple API calls efficiently
- **Data Classes** - Modern way to create classes for data
- **Type Hints** - Make your code more maintainable
- **Testing** - Write unit tests for your data processing functions

---

**Remember**: Python is a tool to solve problems. Focus on understanding the concepts, and the syntax will come naturally with practice! 🐍✨ great for returning multiple values from functions
def get_file_info(filename):
    # Simulate getting file information
    size_mb = 150
    last_modified = "2024-01-15"
    file_type = "CSV"
    return size_mb, last_modified, file_type  # Returns a tuple

# Unpack the returned tuple
size, date, ftype = get_file_info("sales_data.csv")
print(f"File is {size}MB, modified on {date}, type: {ftype}")
# Output: File is 150MB, modified on 2024-01-15, type: CSV
```

### 🎨 Sets - Unique Items Only

**Think of sets like a bag of unique items - no duplicates allowed**

```python
# Files we've already processed
processed_files = {"sales_jan.csv", "sales_feb.csv", "sales_mar.csv"}

# New files that arrived
new_files = {"sales_mar.csv", "sales_apr.csv", "sales_may.csv"}

print(f"Processed: {processed_files}")
print(f"New files: {new_files}")

# Find files we haven't processed yet
pending_files = new_files - processed_files
print(f"Need to process: {pending_files}")
# Output: Need to process: {'sales_may.csv', 'sales_apr.csv'}

# Find files that appear in both
duplicate_files = processed_files & new_files
print(f"Duplicates: {duplicate_files}")
# Output: Duplicates: {'sales_mar.csv'}

# All files combined (no duplicates)
all_files = processed_files | new_files
print(f"All unique files: {all_files}")
# Output: All unique files: {'sales_jan.csv', 'sales_feb.csv', 'sales_mar.csv', 'sales_apr.csv', 'sales_may.csv'}
```

---

## 💼 Working with Data

> **This is where Python shines for data engineering - processing, cleaning, and transforming data**

### 📋 Reading CSV Files (Most Common Data Format)

```python
import csv

# Sample CSV data (imagine this is in a file)
csv_data = """name,age,department,salary
Alice,28,Engineering,75000
Bob,32,Marketing,65000
Charlie,25,Engineering,70000
Diana,29,Sales,68000"""

# In real life, you'd read from a file like this:
# with open('employees.csv', 'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         print(row)

# For demo, we'll simulate reading CSV
from io import StringIO
csv_file = StringIO(csv_data)
reader = csv.DictReader(csv_file)

employees = []
for row in reader:
    # Each row is a dictionary
    employee = {
        'name': row['name'],
        'age': int(row['age']),
        'department': row['department'],
        'salary': int(row['salary'])
    }
    employees.append(employee)

print("Employee data loaded:")
for emp in employees:
    print(f"  {emp['name']}: {emp['department']}, ${emp['salary']:,}")

# Output:
# Employee data loaded:
#   Alice: Engineering, $75,000
#   Bob: Marketing, $65,000
#   Charlie: Engineering, $70,000
#   Diana: Sales, $68,000
```

### 📏 Data Analysis with Basic Python

```python
# Analyze the employee data we just loaded
print("\n=== DATA ANALYSIS ===")

# 1. Count employees by department
dept_counts = {}
for emp in employees:
    dept = emp['department']
    dept_counts[dept] = dept_counts.get(dept, 0) + 1

print("\nEmployees by department:")
for dept, count in dept_counts.items():
    print(f"  {dept}: {count} employees")

# 2. Calculate average salary by department
dept_salaries = {}
for emp in employees:
    dept = emp['department']
    if dept not in dept_salaries:
        dept_salaries[dept] = []
    dept_salaries[dept].append(emp['salary'])

print("\nAverage salary by department:")
for dept, salaries in dept_salaries.items():
    avg_salary = sum(salaries) / len(salaries)
    print(f"  {dept}: ${avg_salary:,.0f}")

# 3. Find highest and lowest paid employees
highest_paid = max(employees, key=lambda emp: emp['salary'])
lowest_paid = min(employees, key=lambda emp: emp['salary'])

print(f"\nHighest paid: {highest_paid['name']} (${highest_paid['salary']:,})")
print(f"Lowest paid: {lowest_paid['name']} (${lowest_paid['salary']:,})")

# Output:
# === DATA ANALYSIS ===
# 
# Employees by department:
#   Engineering: 2 employees
#   Marketing: 1 employees
#   Sales: 1 employees
# 
# Average salary by department:
#   Engineering: $72,500
#   Marketing: $65,000
#   Sales: $68,000
# 
# Highest paid: Alice ($75,000)
# Lowest paid: Bob ($65,000)
```

### 🗃️ Working with JSON Data (APIs and NoSQL)

```python
import json

# Sample JSON data (like what you'd get from an API)
api_response = '''
{
    "users": [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@company.com",
            "last_login": "2024-01-15T10:30:00Z",
            "preferences": {
                "theme": "dark",
                "notifications": true
            }
        },
        {
            "id": 2,
            "name": "Bob Smith",
            "email": "bob@company.com",
            "last_login": "2024-01-14T15:45:00Z",
            "preferences": {
                "theme": "light",
                "notifications": false
            }
        }
    ],
    "total_count": 2,
    "page": 1
}
'''

# Parse JSON string into Python dictionary
data = json.loads(api_response)

print("API Response Summary:")
print(f"Total users: {data['total_count']}")
print(f"Current page: {data['page']}")

print("\nUser details:")
for user in data['users']:
    name = user['name']
    email = user['email']
    theme = user['preferences']['theme']
    notifications = "enabled" if user['preferences']['notifications'] else "disabled"
    
    print(f"  {name} ({email})")
    print(f"    Theme: {theme}, Notifications: {notifications}")

# Output:
# API Response Summary:
# Total users: 2
# Current page: 1
# 
# User details:
#   Alice Johnson (alice@company.com)
#     Theme: dark, Notifications: enabled
#   Bob Smith (bob@company.com)
#     Theme: light, Notifications: disabled
```

### 📊 Data Transformation - The Heart of Data Engineering

```python
# Sample sales data that needs cleaning and transformation
raw_sales_data = [
    {"date": "2024-01-15", "product": "laptop", "price": "1200.00", "quantity": "2", "region": "NORTH"},
    {"date": "2024-01-16", "product": "mouse", "price": "25.50", "quantity": "10", "region": "south"},
    {"date": "2024-01-17", "product": "keyboard", "price": "75.00", "quantity": "5", "region": "East"},
    {"date": "2024-01-18", "product": "monitor", "price": "300.00", "quantity": "3", "region": "WEST"}
]

print("Raw data (before cleaning):")
for record in raw_sales_data[:2]:  # Show first 2 records
    print(f"  {record}")

# Clean and transform the data
cleaned_sales_data = []

for record in raw_sales_data:
    # Clean and transform each record
    cleaned_record = {
        'date': record['date'],
        'product': record['product'].lower().strip(),  # Standardize product names
        'price': float(record['price']),               # Convert to number
        'quantity': int(record['quantity']),           # Convert to number
        'region': record['region'].upper().strip(),    # Standardize regions
        'total_value': float(record['price']) * int(record['quantity'])  # Calculate total
    }
    cleaned_sales_data.append(cleaned_record)

print("\nCleaned data (after transformation):")
for record in cleaned_sales_data[:2]:  # Show first 2 records
    print(f"  {record}")

# Output:
# Raw data (before cleaning):
#   {'date': '2024-01-15', 'product': 'laptop', 'price': '1200.00', 'quantity': '2', 'region': 'NORTH'}
#   {'date': '2024-01-16', 'product': 'mouse', 'price': '25.50', 'quantity': '10', 'region': 'south'}
# 
# Cleaned data (after transformation):
#   {'date': '2024-01-15', 'product': 'laptop', 'price': 1200.0, 'quantity': 2, 'region': 'NORTH', 'total_value': 2400.0}
#   {'date': '2024-01-16', 'product': 'mouse', 'price': 25.5, 'quantity': 10, 'region': 'SOUTH', 'total_value': 255.0}
```

---

## 📁 File Operations

> **Data engineers work with files all the time - reading data, writing results, processing logs**

### 📄 Reading and Writing Text Files

```python
# Writing data to a file
sales_summary = [
    "Sales Report - January 2024",
    "=" * 30,
    "Total Sales: $15,750",
    "Number of Orders: 45",
    "Average Order Value: $350",
    "Top Product: Laptop (15 units)"
]

# Write to file (creates file if it doesn't exist)
with open('sales_report.txt', 'w') as file:
    for line in sales_summary:
        file.write(line + '\n')  # \n adds a new line

print("Sales report written to file")

# Reading from a file
print("\nReading the file back:")
with open('sales_report.txt', 'r') as file:
    content = file.read()
    print(content)

# Reading line by line (better for large files)
print("Reading line by line:")
with open('sales_report.txt', 'r') as file:
    for line_number, line in enumerate(file, 1):
        print(f"Line {line_number}: {line.strip()}")  # strip() removes \n

# Output:
# Sales report written to file
# 
# Reading the file back:
# Sales Report - January 2024
# ==============================
# Total Sales: $15,750
# Number of Orders: 45
# Average Order Value: $350
# Top Product: Laptop (15 units)
```

### 📊 Working with CSV Files

```python
import csv

# Sample employee data
employees = [
    {'name': 'Alice', 'department': 'Engineering', 'salary': 75000, 'start_date': '2022-01-15'},
    {'name': 'Bob', 'department': 'Marketing', 'salary': 65000, 'start_date': '2022-03-20'},
    {'name': 'Charlie', 'department': 'Engineering', 'salary': 80000, 'start_date': '2021-11-10'}
]

# Write to CSV file
with open('employees.csv', 'w', newline='') as file:
    fieldnames = ['name', 'department', 'salary', 'start_date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()  # Write column headers
    writer.writerows(employees)  # Write all rows

print("Employee data written to CSV")

# Read from CSV file
print("\nReading employee data:")
with open('employees.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row['name']
        dept = row['department']
        salary = int(row['salary'])  # Convert back to number
        print(f"{name} works in {dept} and earns ${salary:,}")

# Output:
# Employee data written to CSV
# 
# Reading employee data:
# Alice works in Engineering and earns $75,000
# Bob works in Marketing and earns $65,000
# Charlie works in Engineering and earns $80,000
```

---

## 🗄️ Database Connections

> **Connecting to databases is a core data engineering skill**

### 🔌 Simple Database Connection

```python
import sqlite3

# Create a simple in-memory database for demo
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary INTEGER NOT NULL
    )
''')

# Insert some data
employees_data = [
    (1, 'Alice', 'Engineering', 75000),
    (2, 'Bob', 'Marketing', 65000),
    (3, 'Charlie', 'Engineering', 80000)
]

cursor.executemany('INSERT INTO employees VALUES (?, ?, ?, ?)', employees_data)
conn.commit()

# Query the data
print("All employees:")
cursor.execute('SELECT * FROM employees')
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, Name: {row[1]}, Dept: {row[2]}, Salary: ${row[3]:,}")

# Query with filtering
print("\nEngineering employees:")
cursor.execute('SELECT name, salary FROM employees WHERE department = ?', ('Engineering',))
for row in cursor.fetchall():
    print(f"  {row[0]}: ${row[1]:,}")

# Close connection
conn.close()

# Output:
# All employees:
#   ID: 1, Name: Alice, Dept: Engineering, Salary: $75,000
#   ID: 2, Name: Bob, Dept: Marketing, Salary: $65,000
#   ID: 3, Name: Charlie, Dept: Engineering, Salary: $80,000
# 
# Engineering employees:
#   Alice: $75,000
#   Charlie: $80,000
```

---

## 🌐 API Integration

> **APIs are how systems talk to each other - essential for modern data engineering**

### 📡 Making HTTP Requests

```python
import requests
import json

# Simple GET request (getting data)
def get_user_data(user_id):
    """Get user data from a fake API"""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad status codes
        
        user_data = response.json()
        return {
            'id': user_data['id'],
            'name': user_data['name'],
            'email': user_data['email'],
            'company': user_data['company']['name']
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        return None

# Test the function
user = get_user_data(1)
if user:
    print(f"User: {user['name']} ({user['email']}) works at {user['company']}")

# Output: User: Leanne Graham (Sincere@april.biz) works at Romaguera-Crona

# POST request (sending data)
def create_post(title, body, user_id):
    """Create a new post via API"""
    url = "https://jsonplaceholder.typicode.com/posts"
    
    post_data = {
        'title': title,
        'body': body,
        'userId': user_id
    }
    
    try:
        response = requests.post(url, json=post_data)
        response.raise_for_status()
        
        created_post = response.json()
        print(f"Created post with ID: {created_post['id']}")
        return created_post
    except requests.exceptions.RequestException as e:
        print(f"Error creating post: {e}")
        return None

# Test creating a post
new_post = create_post(
    title="Data Engineering Best Practices",
    body="Always validate your data before processing...",
    user_id=1
)
```

---

## 🏗️ Object-Oriented Programming

> **Think of classes like blueprints for creating objects - useful for organizing complex data processing logic**

### 🏭 Simple Classes for Data Processing

```python
class DataProcessor:
    """Simple data processor class"""
    
    def __init__(self, name):
        self.name = name
        self.processed_count = 0
        self.error_count = 0
    
    def process_record(self, record):
        """Process a single data record"""
        try:
            # Simple processing - convert strings to uppercase
            if isinstance(record, dict):
                processed = {key: str(value).upper() if isinstance(value, str) else value 
                           for key, value in record.items()}
                self.processed_count += 1
                return processed
            else:
                self.error_count += 1
                return None
        except Exception as e:
            print(f"Error processing record: {e}")
            self.error_count += 1
            return None
    
    def get_stats(self):
        """Get processing statistics"""
        total = self.processed_count + self.error_count
        success_rate = (self.processed_count / total * 100) if total > 0 else 0
        return {
            "processor_name": self.name,
            "processed": self.processed_count,
            "errors": self.error_count,
            "success_rate": f"{success_rate:.1f}%"
        }

# Using the class
processor = DataProcessor("Sales Data Processor")

# Sample data to process
sample_records = [
    {"name": "alice", "product": "laptop", "amount": 1200},
    {"name": "bob", "product": "mouse", "amount": 25},
    "invalid_record",  # This will cause an error
    {"name": "charlie", "product": "keyboard", "amount": 75}
]

print("Processing records:")
for record in sample_records:
    result = processor.process_record(record)
    if result:
        print(f"  Processed: {result}")
    else:
        print(f"  Failed to process: {record}")

print(f"\nFinal stats: {processor.get_stats()}")

# Output:
# Processing records:
#   Processed: {'name': 'ALICE', 'product': 'LAPTOP', 'amount': 1200}
#   Processed: {'name': 'BOB', 'product': 'MOUSE', 'amount': 25}
#   Failed to process: invalid_record
#   Processed: {'name': 'CHARLIE', 'product': 'KEYBOARD', 'amount': 75}
# 
# Final stats: {'processor_name': 'Sales Data Processor', 'processed': 3, 'errors': 1, 'success_rate': '75.0%'}
```

---

## 🛡️ Error Handling

> **Things go wrong in data engineering - files missing, network issues, bad data. Handle errors gracefully!**

### 🚨 Try/Except - Catching Errors

```python
def safe_divide(a, b):
    """Safely divide two numbers"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Both inputs must be numbers!")
        return None

# Test the function
print("Testing safe division:")
print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")
print(f"10 / 'abc' = {safe_divide(10, 'abc')}")

# Output:
# Testing safe division:
# 10 / 2 = 5.0
# Error: Cannot divide by zero!
# 10 / 0 = None
# Error: Both inputs must be numbers!
# 10 / 'abc' = None
```

### 🔍 Data Validation

```python
def validate_sales_record(record):
    """
    Check if a sales record is valid for processing.
    Returns: (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields exist
    required_fields = ['date', 'product', 'price', 'quantity', 'region']
    for field in required_fields:
        if field not in record or not record[field]:
            errors.append(f"Missing or empty field: {field}")
    
    # Validate data types and ranges
    try:
        price = float(record.get('price', 0))
        if price <= 0:
            errors.append("Price must be positive")
    except (ValueError, TypeError):
        errors.append("Price must be a valid number")
    
    try:
        quantity = int(record.get('quantity', 0))
        if quantity <= 0:
            errors.append("Quantity must be positive")
    except (ValueError, TypeError):
        errors.append("Quantity must be a valid integer")
    
    # Validate region
    valid_regions = ['NORTH', 'SOUTH', 'EAST', 'WEST']
    region = record.get('region', '').upper().strip()
    if region not in valid_regions:
        errors.append(f"Region must be one of: {valid_regions}")
    
    return len(errors) == 0, errors

# Test the validation
test_records = [
    {"date": "2024-01-15", "product": "laptop", "price": "1200.00", "quantity": "2", "region": "NORTH"},
    {"date": "2024-01-16", "product": "mouse", "price": "-25.50", "quantity": "10", "region": "INVALID"},
    {"date": "2024-01-17", "product": "", "price": "75.00", "quantity": "abc", "region": "EAST"}
]

print("Validation results:")
for i, record in enumerate(test_records, 1):
    is_valid, errors = validate_sales_record(record)
    print(f"Record {i}: {'VALID' if is_valid else 'INVALID'}")
    if errors:
        for error in errors:
            print(f"  - {error}")

# Output:
# Validation results:
# Record 1: VALID
# Record 2: INVALID
#   - Price must be positive
#   - Region must be one of: ['NORTH', 'SOUTH', 'EAST', 'WEST']
# Record 3: INVALID
#   - Missing or empty field: product
#   - Quantity must be a valid integer
```

---

## 📋 Best Practices

> **Write code that your future self (and your teammates) will thank you for**

### 📝 Code Documentation

```python
def process_customer_data(customers, min_age=18, include_inactive=False):
    """
    Process customer data with filtering and validation.
    
    Args:
        customers (list): List of customer dictionaries
        min_age (int): Minimum age to include (default: 18)
        include_inactive (bool): Whether to include inactive customers (default: False)
    
    Returns:
        dict: Processing results with counts and filtered data
        
    Example:
        >>> customers = [{'name': 'Alice', 'age': 25, 'active': True}]
        >>> result = process_customer_data(customers)
        >>> print(result['processed_count'])
        1
    """
    processed_customers = []
    skipped_count = 0
    
    for customer in customers:
        # Skip if too young
        if customer.get('age', 0) < min_age:
            skipped_count += 1
            continue
            
        # Skip inactive customers unless requested
        if not include_inactive and not customer.get('active', True):
            skipped_count += 1
            continue
            
        processed_customers.append(customer)
    
    return {
        'processed_customers': processed_customers,
        'processed_count': len(processed_customers),
        'skipped_count': skipped_count,
        'total_input': len(customers)
    }

# Clear variable names
customer_database = [
    {'name': 'Alice', 'age': 25, 'active': True},
    {'name': 'Bob', 'age': 16, 'active': True},      # Too young
    {'name': 'Charlie', 'age': 30, 'active': False}  # Inactive
]

# Process with clear parameters
processing_result = process_customer_data(
    customers=customer_database,
    min_age=18,
    include_inactive=False
)

print(f"Processed {processing_result['processed_count']} out of {processing_result['total_input']} customers")
print(f"Skipped {processing_result['skipped_count']} customers")

# Output:
# Processed 1 out of 3 customers
# Skipped 2 customers
```

### 🧪 Simple Testing

```python
def test_process_customer_data():
    """Test the customer data processing function"""
    
    # Test data
    test_customers = [
        {'name': 'Alice', 'age': 25, 'active': True},
        {'name': 'Bob', 'age': 16, 'active': True},
        {'name': 'Charlie', 'age': 30, 'active': False}
    ]
    
    # Test 1: Default behavior (min_age=18, exclude inactive)
    result = process_customer_data(test_customers)
    assert result['processed_count'] == 1, f"Expected 1, got {result['processed_count']}"
    assert result['skipped_count'] == 2, f"Expected 2, got {result['skipped_count']}"
    print("✅ Test 1 passed: Default filtering works")
    
    # Test 2: Include inactive customers
    result = process_customer_data(test_customers, include_inactive=True)
    assert result['processed_count'] == 2, f"Expected 2, got {result['processed_count']}"
    assert result['skipped_count'] == 1, f"Expected 1, got {result['skipped_count']}"
    print("✅ Test 2 passed: Including inactive works")
    
    # Test 3: Lower minimum age
    result = process_customer_data(test_customers, min_age=16, include_inactive=True)
    assert result['processed_count'] == 3, f"Expected 3, got {result['processed_count']}"
    assert result['skipped_count'] == 0, f"Expected 0, got {result['skipped_count']}"
    print("✅ Test 3 passed: Lower age limit works")
    
    print("🎉 All tests passed!")

# Run the tests
test_process_customer_data()

# Output:
# ✅ Test 1 passed: Default filtering works
# ✅ Test 2 passed: Including inactive works
# ✅ Test 3 passed: Lower age limit works
# 🎉 All tests passed!
```

---

## 🎯 Interview Preparation

> **Common Python questions for data engineering interviews**

### 🔥 Essential Concepts to Master

1. **Data Types**: Lists, dictionaries, sets, tuples
2. **File I/O**: Reading CSV, JSON, text files
3. **Error Handling**: Try/except blocks
4. **Functions**: Writing reusable code
5. **Data Processing**: Filtering, transforming, aggregating
6. **APIs**: Making HTTP requests

### 💡 Common Interview Questions

**Q: What's the difference between a list and a tuple?**
```python
# List - mutable (can change)
my_list = [1, 2, 3]
my_list.append(4)  # This works
print(my_list)  # [1, 2, 3, 4]

# Tuple - immutable (cannot change)
my_tuple = (1, 2, 3)
# my_tuple.append(4)  # This would cause an error!
print(my_tuple)  # (1, 2, 3)

# Use tuples for data that shouldn't change (like coordinates)
# Use lists for data that might change (like a shopping cart)
```

**Q: How do you handle missing data?**
```python
def safe_get_value(data, key, default=None):
    """Safely get a value from a dictionary"""
    return data.get(key, default)

# Example
user_data = {"name": "Alice", "age": 25}  # Missing "email"

name = safe_get_value(user_data, "name", "Unknown")
email = safe_get_value(user_data, "email", "No email provided")

print(f"Name: {name}, Email: {email}")
# Output: Name: Alice, Email: No email provided
```

**Q: How do you process large files efficiently?**
```python
def process_large_file(filename):
    """Process a large file line by line (memory efficient)"""
    processed_count = 0
    
    with open(filename, 'r') as file:
        for line in file:  # Reads one line at a time
            # Process the line
            if line.strip():  # Skip empty lines
                processed_count += 1
                # Do something with the line
                
    return processed_count

# This approach uses minimal memory even for huge files
```

### 🚀 Practice Exercises

**Exercise 1: Data Cleaning**
```python
def clean_phone_numbers(phone_list):
    """
    Clean a list of phone numbers to standard format.
    Remove non-digits and format as XXX-XXX-XXXX
    """
    cleaned_numbers = []
    
    for phone in phone_list:
        # Remove all non-digit characters
        digits_only = ''.join(char for char in phone if char.isdigit())
        
        # Check if we have exactly 10 digits
        if len(digits_only) == 10:
            # Format as XXX-XXX-XXXX
            formatted = f"{digits_only[:3]}-{digits_only[3:6]}-{digits_only[6:]}"
            cleaned_numbers.append(formatted)
        else:
            print(f"Invalid phone number: {phone}")
    
    return cleaned_numbers

# Test it
messy_phones = ["(555) 123-4567", "555.987.6543", "5551234567", "invalid"]
clean_phones = clean_phone_numbers(messy_phones)
print(f"Cleaned phones: {clean_phones}")
# Output: Cleaned phones: ['555-123-4567', '555-987-6543', '555-123-4567']
```

**Exercise 2: Data Aggregation**
```python
def analyze_sales_data(sales_records):
    """
    Analyze sales data and return summary statistics.
    """
    if not sales_records:
        return {"error": "No data provided"}
    
    # Calculate totals
    total_sales = sum(record['amount'] for record in sales_records)
    total_orders = len(sales_records)
    average_order = total_sales / total_orders if total_orders > 0 else 0
    
    # Find best and worst performing products
    product_sales = {}
    for record in sales_records:
        product = record['product']
        amount = record['amount']
        product_sales[product] = product_sales.get(product, 0) + amount
    
    best_product = max(product_sales, key=product_sales.get) if product_sales else None
    worst_product = min(product_sales, key=product_sales.get) if product_sales else None
    
    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "average_order_value": round(average_order, 2),
        "best_product": best_product,
        "worst_product": worst_product,
        "product_breakdown": product_sales
    }

# Test with sample data
sample_sales = [
    {"product": "laptop", "amount": 1200},
    {"product": "mouse", "amount": 25},
    {"product": "laptop", "amount": 1100},
    {"product": "keyboard", "amount": 75}
]

analysis = analyze_sales_data(sample_sales)
print(f"Analysis: {analysis}")
```

---

## 🎓 Next Steps

Congratulations! You now have a solid foundation in Python for data engineering. Here's what to explore next:

### 🚀 **Immediate Next Steps**
1. **Practice**: Build small data processing scripts daily
2. **Libraries**: Learn Pandas for advanced data manipulation
3. **Databases**: Practice with PostgreSQL, MongoDB
4. **APIs**: Build projects that consume real APIs

### 📚 **Advanced Topics**
- **[Python Advanced Patterns](./PYTHON_ADVANCED_DATA_ENGINEERING.md)** - Production-ready code
- **Async Programming** - For high-performance applications
- **Testing Frameworks** - pytest, unittest
- **Cloud Integration** - AWS, Azure, GCP SDKs

### 🛠️ **Build Projects**
1. **CSV Data Processor** - Clean and analyze CSV files
2. **API Data Pipeline** - Fetch data from APIs, store in database
3. **Log File Analyzer** - Process server logs, generate reports
4. **Data Quality Checker** - Validate data files automatically

### 📖 **Keep Learning**
- Join Python communities (Reddit r/Python, Stack Overflow)
- Follow data engineering blogs and tutorials
- Practice coding challenges on HackerRank, LeetCode
- Contribute to open-source data tools

Remember: **The best way to learn Python is by building things!** Start with small projects and gradually increase complexity. Every data engineer started where you are now.

Happy coding! 🐍✨