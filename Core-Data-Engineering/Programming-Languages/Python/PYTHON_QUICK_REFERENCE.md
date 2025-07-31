# Python Quick Reference

## Essential Syntax

### Variables and Data Types
```python
# Basic data types with examples
name = "John"                              # str - text data
age = 30                                   # int - whole numbers
height = 5.9                              # float - decimal numbers
is_active = True                          # bool - True/False values
items = [1, 2, 3]                         # list - ordered, mutable collection
coords = (10, 20)                         # tuple - ordered, immutable collection
person = {"name": "John", "age": 30}      # dict - key-value pairs
unique_items = {1, 2, 3}                  # set - unordered, unique elements
data = None                               # NoneType - represents absence of value

# Type checking and conversion
type(name)                                # <class 'str'> - get object type
isinstance(age, int)                      # True - check if object is instance of type
str(age)                                  # "30" - convert to string
int("42")                                 # 42 - convert string to integer
float("3.14")                            # 3.14 - convert to float
bool(1)                                   # True - convert to boolean
list("abc")                               # ['a', 'b', 'c'] - convert to list
tuple([1, 2, 3])                          # (1, 2, 3) - convert to tuple

# Advanced type hints (Python 3.5+)
from typing import List, Dict, Optional, Union

def process_data(items: List[int], config: Dict[str, str]) -> Optional[str]:
    """Function with type hints for better code documentation."""
    pass
```

### String Operations
```python
# String formatting methods (most to least preferred)
name = "John"
age = 30
salary = 50000.75

# f-strings (Python 3.6+) - most readable and efficient
f"Hello {name}, you are {age}"                    # "Hello John, you are 30"
f"Salary: ${salary:,.2f}"                         # "Salary: $50,000.75" - with formatting
f"Name: {name.upper():<10} Age: {age:>3}"         # "Name: JOHN       Age:  30" - alignment

# .format() method - good for templates
"Hello {}, you are {}".format(name, age)          # positional arguments
"Hello {name}, you are {age}".format(name=name, age=age)  # keyword arguments
"Value: {:.2%}".format(0.1234)                    # "Value: 12.34%" - percentage formatting

# % formatting (legacy) - avoid in new code
"Hello %s, you are %d" % (name, age)              # old style formatting

# String methods for data cleaning and processing
text = "  Hello World  "
text.strip()                    # "Hello World" - remove leading/trailing whitespace
text.lstrip()                   # "Hello World  " - remove leading whitespace only
text.rstrip()                   # "  Hello World" - remove trailing whitespace only
text.lower()                    # "  hello world  " - convert to lowercase
text.upper()                    # "  HELLO WORLD  " - convert to uppercase
text.title()                    # "  Hello World  " - title case
text.capitalize()               # "  hello world  " - capitalize first letter
text.replace("Hello", "Hi")     # "  Hi World  " - replace substring
text.replace(" ", "_")          # "__Hello_World__" - replace all spaces

# String splitting and joining
text.split()                    # ["Hello", "World"] - split on whitespace
text.split("l")                 # ['  He', '', 'o Wor', 'd  '] - split on character
"a,b,c".split(",")              # ['a', 'b', 'c'] - split on delimiter
"_".join(["a", "b", "c"])       # "a_b_c" - join list with separator
", ".join(["apple", "banana"])  # "apple, banana" - join with custom separator

# String searching and validation
text = "Hello World"
text.startswith("Hello")        # True - check if starts with substring
text.endswith("World")          # True - check if ends with substring
"World" in text                 # True - check if substring exists
text.find("World")              # 6 - find index of substring (-1 if not found)
text.index("World")             # 6 - find index (raises ValueError if not found)
text.count("l")                 # 3 - count occurrences of substring

# String validation methods
"123".isdigit()                 # True - all characters are digits
"abc".isalpha()                 # True - all characters are letters
"abc123".isalnum()              # True - all characters are alphanumeric
"   ".isspace()                 # True - all characters are whitespace
"Hello World".istitle()         # True - string is in title case

# Advanced string operations for data engineering
import re

# Regular expressions for pattern matching
email = "user@example.com"
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
re.match(email_pattern, email)  # Match object if valid email, None otherwise

# Extract numbers from string
text_with_numbers = "Price: $123.45, Quantity: 10"
numbers = re.findall(r'\d+\.?\d*', text_with_numbers)  # ['123.45', '10']

# Clean and normalize text data
def clean_text(text: str) -> str:
    """Clean text data for processing."""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters (keep alphanumeric and spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower()

clean_text("  Hello,   World!!!  ")  # "hello world"

# String encoding/decoding for file operations
text = "Hello, 世界"  # text with unicode characters
encoded = text.encode('utf-8')      # b'Hello, \xe4\xb8\x96\xe7\x95\x8c'
decoded = encoded.decode('utf-8')   # "Hello, 世界"

# Handle encoding errors gracefully
bad_bytes = b'\xff\xfe'  # invalid UTF-8
safe_text = bad_bytes.decode('utf-8', errors='ignore')  # ignore invalid bytes
replace_text = bad_bytes.decode('utf-8', errors='replace')  # replace with �
```

### Lists and List Comprehensions
```python
# List creation and basic operations
nums = [1, 2, 3, 4, 5]                    # Create list
empty_list = []                           # Empty list
repeated = [0] * 5                        # [0, 0, 0, 0, 0] - repeat elements
range_list = list(range(1, 6))            # [1, 2, 3, 4, 5] - from range

# Adding elements
nums.append(6)                            # [1, 2, 3, 4, 5, 6] - add single element
nums.extend([7, 8])                       # [1, 2, 3, 4, 5, 6, 7, 8] - add multiple
nums.insert(0, 0)                         # [0, 1, 2, 3, 4, 5, 6, 7, 8] - insert at index
nums += [9, 10]                           # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] - concatenate

# Removing elements
nums.remove(3)                            # Remove first occurrence of value
popped = nums.pop()                       # Remove and return last item
first = nums.pop(0)                       # Remove and return item at index
del nums[1]                               # Delete item at index
nums.clear()                              # Remove all elements

# List information and searching
nums = [1, 2, 3, 2, 4, 2, 5]
len(nums)                                 # 7 - number of elements
nums.count(2)                             # 3 - count occurrences
nums.index(3)                             # 2 - find index of first occurrence
3 in nums                                 # True - check membership
max(nums)                                 # 5 - maximum value
min(nums)                                 # 1 - minimum value
sum(nums)                                 # 19 - sum of all elements

# List sorting and reversing
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()                               # [1, 1, 2, 3, 4, 5, 6, 9] - sort in place
sorted_desc = sorted(nums, reverse=True)  # [9, 6, 5, 4, 3, 2, 1, 1] - return new sorted list
nums.reverse()                            # Reverse in place
reversed_list = list(reversed(nums))      # Return new reversed list

# Custom sorting
words = ["apple", "pie", "banana", "cherry"]
words.sort(key=len)                       # ['pie', 'apple', 'banana', 'cherry'] - sort by length
words.sort(key=str.lower)                 # Sort case-insensitive

# Advanced sorting with lambda
students = [('Alice', 85), ('Bob', 90), ('Charlie', 78)]
students.sort(key=lambda x: x[1])         # Sort by grade (second element)

# List comprehensions - basic
squares = [x**2 for x in range(10)]                    # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
evens = [x for x in range(20) if x % 2 == 0]          # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
uppercase = [word.upper() for word in ['hello', 'world']]  # ['HELLO', 'WORLD']

# List comprehensions - advanced
# Nested comprehensions for matrix operations
matrix = [[i*j for j in range(3)] for i in range(3)]  # [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
flattened = [item for row in matrix for item in row]  # [0, 0, 0, 0, 1, 2, 0, 2, 4]

# Conditional comprehensions
data = [1, -2, 3, -4, 5, -6]
positive = [x for x in data if x > 0]                 # [1, 3, 5]
abs_values = [abs(x) for x in data]                   # [1, 2, 3, 4, 5, 6]
conditional = [x if x > 0 else 0 for x in data]       # [1, 0, 3, 0, 5, 0]

# Dictionary and set comprehensions
square_dict = {x: x**2 for x in range(5)}            # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
even_set = {x for x in range(10) if x % 2 == 0}      # {0, 2, 4, 6, 8}

# List slicing - comprehensive guide
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Basic slicing: list[start:end:step]
nums[1:4]              # [1, 2, 3] - elements from index 1 to 3
nums[:3]               # [0, 1, 2] - first 3 elements
nums[3:]               # [3, 4, 5, 6, 7, 8, 9] - from index 3 to end
nums[:]                # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] - copy entire list

# Negative indexing
nums[-1]               # 9 - last element
nums[-3:]              # [7, 8, 9] - last 3 elements
nums[:-2]              # [0, 1, 2, 3, 4, 5, 6, 7] - all except last 2
nums[-5:-2]            # [5, 6, 7] - slice with negative indices

# Step slicing
nums[::2]              # [0, 2, 4, 6, 8] - every 2nd element
nums[1::2]             # [1, 3, 5, 7, 9] - every 2nd element starting from index 1
nums[::-1]             # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] - reverse list
nums[8:2:-2]           # [8, 6, 4] - reverse slice with step

# List copying (important for data integrity)
original = [1, 2, [3, 4]]
shallow_copy = original.copy()        # or original[:] or list(original)
deep_copy = copy.deepcopy(original)   # for nested structures

# Modify original to see difference
original[0] = 'changed'
original[2][0] = 'nested_changed'
print(f"Original: {original}")        # ['changed', 2, ['nested_changed', 4]]
print(f"Shallow: {shallow_copy}")     # [1, 2, ['nested_changed', 4]] - nested change affects both
print(f"Deep: {deep_copy}")           # [1, 2, [3, 4]] - completely independent

# List operations for data processing
import operator
from functools import reduce

# Functional programming with lists
numbers = [1, 2, 3, 4, 5]

# Map, filter, reduce
squared = list(map(lambda x: x**2, numbers))          # [1, 4, 9, 16, 25]
even_nums = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
product = reduce(operator.mul, numbers)               # 120 (1*2*3*4*5)

# Zip for parallel iteration
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
scores = [85, 90, 78]

# Combine multiple lists
combined = list(zip(names, ages, scores))             # [('Alice', 25, 85), ('Bob', 30, 90), ('Charlie', 35, 78)]

# Unzip (transpose)
names2, ages2, scores2 = zip(*combined)               # Separate back into individual lists

# Enumerate for index-value pairs
for i, name in enumerate(names):
    print(f"{i}: {name}")                             # 0: Alice, 1: Bob, 2: Charlie

# List performance considerations
# Use deque for frequent insertions/deletions at beginning
from collections import deque

# Inefficient for large lists
large_list = list(range(100000))
large_list.insert(0, 'new_item')  # O(n) operation

# Efficient alternative
large_deque = deque(range(100000))
large_deque.appendleft('new_item')  # O(1) operation
```

### Dictionaries
```python
# Dictionary creation methods
person = {"name": "John", "age": 30}              # Literal syntax
empty_dict = {}                                   # Empty dictionary
from_keys = dict.fromkeys(['a', 'b', 'c'], 0)    # {'a': 0, 'b': 0, 'c': 0}
from_pairs = dict([('name', 'John'), ('age', 30)]) # From list of tuples
from_kwargs = dict(name='John', age=30)           # From keyword arguments

# Adding and updating elements
person["city"] = "NYC"                            # Add new key-value pair
person["age"] = 31                                # Update existing value
person.update({"country": "USA", "job": "Engineer"})  # Update multiple
person.update(salary=50000)                      # Update with keyword args

# Accessing values safely
age = person.get("age")                           # 31 - returns None if key doesn't exist
age_default = person.get("height", 0)             # 0 - returns default if key doesn't exist
salary = person.setdefault("salary", 45000)       # Get or set default value

# Dictionary views (dynamic - reflect changes)
keys = person.keys()                              # dict_keys(['name', 'age', 'city', ...])
values = person.values()                          # dict_values(['John', 31, 'NYC', ...])
items = person.items()                            # dict_items([('name', 'John'), ...])

# Converting views to lists (static snapshot)
key_list = list(person.keys())                    # ['name', 'age', 'city', ...]
value_list = list(person.values())                # ['John', 31, 'NYC', ...]
item_list = list(person.items())                  # [('name', 'John'), ('age', 31), ...]

# Removing elements
del person["city"]                                # Remove key (raises KeyError if not found)
age = person.pop("age")                           # Remove and return value
height = person.pop("height", 0)                  # Remove with default if key doesn't exist
name, value = person.popitem()                    # Remove and return arbitrary key-value pair
person.clear()                                    # Remove all elements

# Dictionary membership and information
person = {"name": "John", "age": 30, "city": "NYC"}
"name" in person                                  # True - check if key exists
"John" in person.values()                         # True - check if value exists
len(person)                                       # 3 - number of key-value pairs
bool(person)                                      # True - False only if empty

# Dictionary comprehensions - powerful for data transformation
numbers = [1, 2, 3, 4, 5]
squares = {x: x**2 for x in numbers}              # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
even_squares = {x: x**2 for x in numbers if x % 2 == 0}  # {2: 4, 4: 16}

# Filter existing dictionary
original = {"name": "John", "age": 30, "city": "NYC", "country": "USA"}
string_only = {k: v for k, v in original.items() if isinstance(v, str)}
# {'name': 'John', 'city': 'NYC', 'country': 'USA'}

# Transform values
upper_values = {k: v.upper() if isinstance(v, str) else v for k, v in original.items()}
# {'name': 'JOHN', 'age': 30, 'city': 'NYC', 'country': 'USA'}

# Nested dictionaries for complex data structures
employees = {
    "emp001": {
        "name": "John Doe",
        "department": "Engineering",
        "salary": 75000,
        "skills": ["Python", "SQL", "AWS"]
    },
    "emp002": {
        "name": "Jane Smith",
        "department": "Data Science",
        "salary": 80000,
        "skills": ["Python", "R", "Machine Learning"]
    }
}

# Accessing nested data
john_salary = employees["emp001"]["salary"]        # 75000
jane_skills = employees["emp002"]["skills"]        # ['Python', 'R', 'Machine Learning']

# Safe nested access with get()
john_bonus = employees.get("emp001", {}).get("bonus", 0)  # 0 (doesn't exist)

# Dictionary merging (Python 3.5+)
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
dict3 = {"b": 20, "e": 5}  # Note: 'b' will override

# Method 1: Using ** unpacking
merged = {**dict1, **dict2, **dict3}              # {'a': 1, 'b': 20, 'c': 3, 'd': 4, 'e': 5}

# Method 2: Using | operator (Python 3.9+)
merged = dict1 | dict2 | dict3                    # Same result

# Method 3: Using update() (modifies original)
result = dict1.copy()
result.update(dict2)
result.update(dict3)

# Advanced dictionary operations
from collections import defaultdict, Counter, OrderedDict

# defaultdict - automatically creates missing values
dd = defaultdict(list)                            # Default factory: list
dd['fruits'].append('apple')                      # Creates list automatically
dd['fruits'].append('banana')
dd['vegetables'].append('carrot')
# defaultdict(<class 'list'>, {'fruits': ['apple', 'banana'], 'vegetables': ['carrot']})

# Counter - specialized dict for counting
text = "hello world"
letter_count = Counter(text)                      # Counter({'l': 3, 'o': 2, 'h': 1, ...})
most_common = letter_count.most_common(3)         # [('l', 3), ('o', 2), ('h', 1)]

# OrderedDict - maintains insertion order (less needed in Python 3.7+)
od = OrderedDict([('first', 1), ('second', 2), ('third', 3)])
od.move_to_end('first')                           # Move key to end

# Dictionary performance and best practices
# Use dict for O(1) average case lookups
lookup_table = {item: index for index, item in enumerate(large_list)}

# Group data using dictionaries
data = [('apple', 'fruit'), ('carrot', 'vegetable'), ('banana', 'fruit')]
grouped = {}
for item, category in data:
    if category not in grouped:
        grouped[category] = []
    grouped[category].append(item)
# {'fruit': ['apple', 'banana'], 'vegetable': ['carrot']}

# More elegant grouping with defaultdict
from collections import defaultdict
grouped = defaultdict(list)
for item, category in data:
    grouped[category].append(item)

# Dictionary sorting
scores = {'Alice': 85, 'Bob': 90, 'Charlie': 78, 'Diana': 92}

# Sort by keys
sorted_by_key = dict(sorted(scores.items()))      # Alphabetical by name

# Sort by values
sorted_by_score = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
# {'Diana': 92, 'Bob': 90, 'Alice': 85, 'Charlie': 78}

# Get top N items
top_3 = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3])

# Dictionary as a switch/case alternative
def process_data(data_type, data):
    """Process data based on type using dictionary dispatch."""
    processors = {
        'csv': lambda d: d.split(','),
        'json': lambda d: json.loads(d),
        'text': lambda d: d.strip().split(),
        'number': lambda d: float(d)
    }
    
    processor = processors.get(data_type, lambda d: d)  # Default: return as-is
    return processor(data)

# Usage
result = process_data('csv', 'a,b,c')             # ['a', 'b', 'c']
```

## Control Flow

### Conditionals
```python
# if/elif/else
if age < 18:
    status = "minor"
elif age < 65:
    status = "adult"
else:
    status = "senior"

# Ternary operator
status = "adult" if age >= 18 else "minor"

# Multiple conditions
if 18 <= age < 65 and is_active:
    print("Working age")
```

### Loops
```python
# for loops
for i in range(5):              # 0 to 4
    print(i)

for i in range(1, 6):           # 1 to 5
    print(i)

for i in range(0, 10, 2):       # 0, 2, 4, 6, 8
    print(i)

for item in ["a", "b", "c"]:
    print(item)

for i, item in enumerate(["a", "b", "c"]):
    print(f"{i}: {item}")

# while loops
count = 0
while count < 5:
    print(count)
    count += 1

# Loop control
for i in range(10):
    if i == 3:
        continue    # Skip to next iteration
    if i == 7:
        break       # Exit loop
    print(i)
```

## Functions

### Basic Functions
```python
def greet(name, greeting="Hello"):
    """Greet a person with optional greeting."""
    return f"{greeting}, {name}!"

# Function calls
greet("John")                    # "Hello, John!"
greet("Jane", "Hi")             # "Hi, Jane!"
greet(greeting="Hey", name="Bob")  # "Hey, Bob!"
```

### Advanced Function Features
```python
# *args and **kwargs
def flexible_function(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

flexible_function(1, 2, 3, name="John", age=30)

# Lambda functions
square = lambda x: x**2
numbers = [1, 2, 3, 4, 5]
squared = list(map(square, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Decorators
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time: {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

## Classes and Objects

### Basic Classes
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, I'm {self.name}"
    
    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"
    
    def __repr__(self):
        return f"Person('{self.name}', {self.age})"

# Usage
person = Person("John", 30)
print(person.greet())
print(str(person))
```

### Inheritance
```python
class Employee(Person):
    def __init__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title
    
    def work(self):
        return f"{self.name} is working as {self.job_title}"

employee = Employee("Jane", 25, "Developer")
print(employee.greet())  # Inherited method
print(employee.work())   # New method
```

## File Operations

### Reading and Writing Files
```python
# Reading files
with open('file.txt', 'r') as f:
    content = f.read()          # Read entire file
    
with open('file.txt', 'r') as f:
    lines = f.readlines()       # Read all lines as list

with open('file.txt', 'r') as f:
    for line in f:              # Read line by line
        print(line.strip())

# Writing files
with open('output.txt', 'w') as f:
    f.write("Hello World\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Appending to files
with open('log.txt', 'a') as f:
    f.write("New log entry\n")
```

### Working with CSV and JSON
```python
import csv
import json

# CSV operations
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Age'])
    writer.writerow(['John', 30])

# JSON operations
data = {"name": "John", "age": 30}
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('data.json', 'r') as f:
    loaded_data = json.load(f)
```

## Error Handling

### Try/Except Blocks
```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
else:
    print("No errors occurred")
finally:
    print("This always runs")

# Multiple exceptions
try:
    # Some operation
    pass
except (ValueError, TypeError) as e:
    print(f"Value or Type error: {e}")

# Custom exceptions
class CustomError(Exception):
    pass

def risky_function():
    raise CustomError("Something went wrong")

try:
    risky_function()
except CustomError as e:
    print(f"Custom error: {e}")
```

## Common Built-in Functions

### Useful Built-ins
```python
# Math functions
abs(-5)                # 5
min([1, 2, 3])        # 1
max([1, 2, 3])        # 3
sum([1, 2, 3])        # 6
round(3.14159, 2)     # 3.14

# Type conversions
int("123")            # 123
float("3.14")         # 3.14
str(123)              # "123"
list("abc")           # ['a', 'b', 'c']
tuple([1, 2, 3])      # (1, 2, 3)

# Sequence functions
len([1, 2, 3])        # 3
sorted([3, 1, 2])     # [1, 2, 3]
reversed([1, 2, 3])   # [3, 2, 1]
enumerate(['a', 'b']) # [(0, 'a'), (1, 'b')]
zip([1, 2], ['a', 'b'])  # [(1, 'a'), (2, 'b')]

# Functional programming
map(str.upper, ['a', 'b'])     # ['A', 'B']
filter(lambda x: x > 0, [-1, 0, 1, 2])  # [1, 2]
all([True, True, False])       # False
any([True, False, False])      # True
```

## Data Engineering Essentials

### Working with Pandas
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Creating DataFrames - multiple methods
# From dictionary
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob', 'Alice'],
    'age': [30, 25, 35, 28],
    'city': ['NYC', 'LA', 'Chicago', 'NYC'],
    'salary': [75000, 80000, 70000, 85000],
    'join_date': ['2020-01-15', '2019-06-20', '2021-03-10', '2020-11-05']
})

# From CSV with comprehensive options
df_csv = pd.read_csv('data.csv', 
                     sep=',',                    # Delimiter
                     header=0,                   # Header row
                     index_col=0,                # Index column
                     dtype={'id': str},          # Specify data types
                     parse_dates=['date_col'],   # Parse dates
                     na_values=['NULL', 'N/A'],  # Custom null values
                     encoding='utf-8',           # File encoding
                     chunksize=10000)            # Read in chunks

# DataFrame inspection and information
df.head(3)                     # First 3 rows
df.tail(3)                     # Last 3 rows
df.sample(2)                   # Random 2 rows
df.info()                      # DataFrame structure and memory usage
df.describe()                  # Statistical summary for numeric columns
df.describe(include='all')     # Summary for all columns
df.shape                       # (rows, columns) tuple
df.columns.tolist()            # Column names as list
df.dtypes                      # Data types of each column
df.index                       # Index information
df.memory_usage(deep=True)     # Memory usage per column

# Data selection and filtering
# Column selection
names = df['name']                              # Single column (Series)
subset = df[['name', 'age']]                    # Multiple columns (DataFrame)
first_three_cols = df.iloc[:, :3]               # First 3 columns

# Row selection
first_row = df.iloc[0]                          # First row by position
first_row_label = df.loc[0]                     # First row by label
multiple_rows = df.iloc[1:3]                    # Rows 1-2

# Boolean indexing (filtering)
high_earners = df[df['salary'] > 75000]         # Filter by condition
nyc_employees = df[df['city'] == 'NYC']         # Filter by exact match
complex_filter = df[(df['age'] > 25) & (df['salary'] > 70000)]  # Multiple conditions
isin_filter = df[df['city'].isin(['NYC', 'LA'])]  # Filter by list of values

# String operations on columns
df['name_upper'] = df['name'].str.upper()       # Convert to uppercase
df['name_length'] = df['name'].str.len()        # String length
contains_filter = df[df['name'].str.contains('J')]  # Contains pattern

# Date operations
df['join_date'] = pd.to_datetime(df['join_date'])  # Convert to datetime
df['years_employed'] = (datetime.now() - df['join_date']).dt.days / 365.25
df['join_year'] = df['join_date'].dt.year        # Extract year
df['join_month'] = df['join_date'].dt.month      # Extract month

# Handling missing data
df_with_nulls = df.copy()
df_with_nulls.loc[1, 'salary'] = np.nan         # Introduce null value

# Check for missing data
df_with_nulls.isnull().sum()                    # Count nulls per column
df_with_nulls.notnull().all()                   # Check if any column has nulls

# Handle missing data
df_dropped = df_with_nulls.dropna()             # Drop rows with any null
df_filled = df_with_nulls.fillna(0)             # Fill nulls with 0
df_forward_fill = df_with_nulls.fillna(method='ffill')  # Forward fill
df_interpolated = df_with_nulls.interpolate()   # Interpolate missing values

# Grouping and aggregation - comprehensive
# Basic grouping
city_stats = df.groupby('city').agg({
    'age': ['mean', 'min', 'max', 'std'],
    'salary': ['mean', 'sum', 'count']
})

# Multiple grouping columns
complex_grouping = df.groupby(['city', df['age'] > 30]).agg({
    'salary': 'mean',
    'name': 'count'
})

# Custom aggregation functions
def salary_range(series):
    return series.max() - series.min()

custom_agg = df.groupby('city').agg({
    'salary': [salary_range, 'mean'],
    'age': lambda x: x.quantile(0.75)  # 75th percentile
})

# Transform and apply
df['salary_rank'] = df.groupby('city')['salary'].rank(ascending=False)
df['salary_pct_of_city'] = df['salary'] / df.groupby('city')['salary'].transform('sum')

# Data manipulation and transformation
# Sorting
df_sorted = df.sort_values('salary', ascending=False)  # Sort by salary desc
df_multi_sort = df.sort_values(['city', 'age'])        # Sort by multiple columns

# Adding and modifying columns
df['bonus'] = df['salary'] * 0.1                       # Calculate bonus
df['total_comp'] = df['salary'] + df['bonus']          # Total compensation
df['age_group'] = pd.cut(df['age'], bins=[0, 30, 40, 100], 
                        labels=['Young', 'Middle', 'Senior'])  # Binning

# Conditional column creation
df['performance'] = np.where(df['salary'] > 75000, 'High', 'Standard')
df['city_size'] = df['city'].map({'NYC': 'Large', 'LA': 'Large', 'Chicago': 'Medium'})

# Merging and joining DataFrames
df_departments = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob'],
    'department': ['Engineering', 'Data Science', 'Marketing']
})

# Different types of joins
inner_join = pd.merge(df, df_departments, on='name', how='inner')  # Inner join
left_join = pd.merge(df, df_departments, on='name', how='left')    # Left join
outer_join = pd.merge(df, df_departments, on='name', how='outer')  # Outer join

# Concatenating DataFrames
df1 = df.iloc[:2]  # First 2 rows
df2 = df.iloc[2:]  # Remaining rows
concatenated = pd.concat([df1, df2], ignore_index=True)  # Vertical concat
horizontal = pd.concat([df, df_departments.set_index('name')], axis=1)  # Horizontal

# Pivot tables and reshaping
pivot_table = df.pivot_table(
    values='salary',
    index='city',
    columns='age_group',
    aggfunc='mean',
    fill_value=0
)

# Melting (wide to long format)
df_melted = pd.melt(df, 
                   id_vars=['name', 'city'],
                   value_vars=['age', 'salary'],
                   var_name='metric',
                   value_name='value')

# Performance optimization
# Use categorical data for repeated strings
df['city'] = df['city'].astype('category')  # Saves memory

# Vectorized operations (faster than loops)
df['salary_normalized'] = (df['salary'] - df['salary'].mean()) / df['salary'].std()

# Efficient data types
df['age'] = df['age'].astype('int8')        # Use smaller int type if possible
df['salary'] = df['salary'].astype('int32') # Appropriate size for salary values

# Export data
df.to_csv('output.csv', index=False)        # Export to CSV
df.to_json('output.json', orient='records') # Export to JSON
df.to_excel('output.xlsx', sheet_name='employees')  # Export to Excel
df.to_parquet('output.parquet')             # Export to Parquet (efficient)
```

### Working with NumPy
```python
import numpy as np

# Creating arrays
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros((3, 3))
ones = np.ones((2, 4))
random_arr = np.random.random((3, 3))

# Array operations
arr * 2                       # Element-wise multiplication
arr + 10                      # Element-wise addition
np.sqrt(arr)                  # Element-wise square root
arr.sum()                     # Sum all elements
arr.mean()                    # Mean of all elements
arr.std()                     # Standard deviation

# Array indexing and slicing
arr[0]                        # First element
arr[-1]                       # Last element
arr[1:4]                      # Elements 1 to 3
arr[arr > 3]                  # Boolean indexing
```

### Database Operations
```python
import sqlite3
import pandas as pd
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import logging

# Context manager for database connections (ensures proper cleanup)
@contextmanager
def get_db_connection(db_path: str):
    """Context manager for database connections with automatic cleanup."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

# SQLite operations with comprehensive error handling
def create_tables(db_path: str):
    """Create database tables with proper schema."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Create users table with constraints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK(length(name) > 0),
                email TEXT UNIQUE NOT NULL,
                age INTEGER CHECK(age >= 0 AND age <= 150),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create orders table with foreign key
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)')
        
        conn.commit()
        logging.info("Database tables created successfully")

# Insert operations with validation
def insert_user(db_path: str, name: str, email: str, age: int) -> Optional[int]:
    """Insert a new user and return the user ID."""
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age)
            )
            user_id = cursor.lastrowid
            conn.commit()
            logging.info(f"User {name} inserted with ID {user_id}")
            return user_id
    except sqlite3.IntegrityError as e:
        logging.error(f"Failed to insert user {name}: {e}")
        return None

def bulk_insert_users(db_path: str, users: List[Dict[str, Any]]) -> int:
    """Bulk insert users for better performance."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Prepare data for bulk insert
        user_data = [(user['name'], user['email'], user['age']) for user in users]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)",
            user_data
        )
        
        rows_affected = cursor.rowcount
        conn.commit()
        logging.info(f"Bulk inserted {rows_affected} users")
        return rows_affected

# Query operations with different fetch methods
def get_user_by_id(db_path: str, user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID, return as dictionary."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)  # Convert Row object to dict
        return None

def get_users_by_age_range(db_path: str, min_age: int, max_age: int) -> List[Dict[str, Any]]:
    """Get users within age range."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE age BETWEEN ? AND ? ORDER BY age",
            (min_age, max_age)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

# Complex queries with joins
def get_user_orders_summary(db_path: str) -> List[Dict[str, Any]]:
    """Get user order summary with joins and aggregation."""
    query = '''
        SELECT 
            u.id,
            u.name,
            u.email,
            COUNT(o.id) as total_orders,
            COALESCE(SUM(o.quantity * o.price), 0) as total_spent,
            MAX(o.order_date) as last_order_date
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        GROUP BY u.id, u.name, u.email
        ORDER BY total_spent DESC
    '''
    
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

# Update and delete operations
def update_user_email(db_path: str, user_id: int, new_email: str) -> bool:
    """Update user email with validation."""
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET email = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_email, user_id)
            )
            
            if cursor.rowcount > 0:
                conn.commit()
                logging.info(f"Updated email for user {user_id}")
                return True
            else:
                logging.warning(f"No user found with ID {user_id}")
                return False
                
    except sqlite3.IntegrityError as e:
        logging.error(f"Failed to update email: {e}")
        return False

def delete_inactive_users(db_path: str, days_inactive: int) -> int:
    """Delete users who haven't placed orders in specified days."""
    query = '''
        DELETE FROM users 
        WHERE id NOT IN (
            SELECT DISTINCT user_id 
            FROM orders 
            WHERE order_date > datetime('now', '-{} days')
        )
    '''.format(days_inactive)
    
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        deleted_count = cursor.rowcount
        conn.commit()
        logging.info(f"Deleted {deleted_count} inactive users")
        return deleted_count

# Transaction management
def transfer_order(db_path: str, from_user_id: int, to_user_id: int, order_id: int) -> bool:
    """Transfer order between users using transaction."""
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # Start transaction (implicit with context manager)
            # Verify both users exist
            cursor.execute("SELECT COUNT(*) FROM users WHERE id IN (?, ?)", 
                         (from_user_id, to_user_id))
            if cursor.fetchone()[0] != 2:
                raise ValueError("One or both users do not exist")
            
            # Verify order belongs to from_user
            cursor.execute("SELECT user_id FROM orders WHERE id = ?", (order_id,))
            result = cursor.fetchone()
            if not result or result[0] != from_user_id:
                raise ValueError("Order does not belong to source user")
            
            # Transfer the order
            cursor.execute(
                "UPDATE orders SET user_id = ? WHERE id = ?",
                (to_user_id, order_id)
            )
            
            conn.commit()  # Commit transaction
            logging.info(f"Order {order_id} transferred from user {from_user_id} to {to_user_id}")
            return True
            
    except Exception as e:
        logging.error(f"Failed to transfer order: {e}")
        return False

# Integration with Pandas for data analysis
def analyze_sales_data(db_path: str) -> pd.DataFrame:
    """Analyze sales data using pandas integration."""
    query = '''
        SELECT 
            DATE(o.order_date) as order_date,
            u.name as customer_name,
            o.product_name,
            o.quantity,
            o.price,
            (o.quantity * o.price) as total_amount
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.order_date DESC
    '''
    
    with get_db_connection(db_path) as conn:
        df = pd.read_sql_query(query, conn)
        
        # Add calculated columns
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['month'] = df['order_date'].dt.to_period('M')
        
        return df

# Database connection pooling for high-performance applications
class DatabasePool:
    """Simple database connection pool for SQLite."""
    
    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self.max_connections = max_connections
        self.pool = []
        self.in_use = set()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get connection from pool or create new one."""
        if self.pool:
            conn = self.pool.pop()
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
        
        self.in_use.add(conn)
        return conn
    
    def return_connection(self, conn: sqlite3.Connection):
        """Return connection to pool."""
        if conn in self.in_use:
            self.in_use.remove(conn)
            
            if len(self.pool) < self.max_connections:
                self.pool.append(conn)
            else:
                conn.close()
    
    def close_all(self):
        """Close all connections in pool."""
        for conn in self.pool:
            conn.close()
        for conn in self.in_use:
            conn.close()
        self.pool.clear()
        self.in_use.clear()

# Usage examples
if __name__ == "__main__":
    db_path = "example.db"
    
    # Initialize database
    create_tables(db_path)
    
    # Insert sample data
    users = [
        {'name': 'John Doe', 'email': 'john@example.com', 'age': 30},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25},
        {'name': 'Bob Johnson', 'email': 'bob@example.com', 'age': 35}
    ]
    bulk_insert_users(db_path, users)
    
    # Query data
    young_users = get_users_by_age_range(db_path, 20, 30)
    print(f"Found {len(young_users)} young users")
    
    # Analyze with pandas
    # sales_df = analyze_sales_data(db_path)
    # print(sales_df.groupby('month')['total_amount'].sum())

# PostgreSQL example using psycopg2
# pip install psycopg2-binary
'''
import psycopg2
from psycopg2.extras import RealDictCursor

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="username",
    password="password",
    port="5432"
)

# Use RealDictCursor for dictionary-like results
with conn.cursor(cursor_factory=RealDictCursor) as cursor:
    cursor.execute("SELECT * FROM users WHERE age > %s", (25,))
    results = cursor.fetchall()
    for row in results:
        print(f"Name: {row['name']}, Age: {row['age']}")

conn.close()
'''

# SQLAlchemy ORM example (more advanced)
# pip install sqlalchemy
'''
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create engine and session
engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# ORM operations
new_user = User(name='Alice', email='alice@example.com')
session.add(new_user)
session.commit()

# Query with ORM
users = session.query(User).filter(User.name.like('%Alice%')).all()
for user in users:
    print(f"User: {user.name}, Email: {user.email}")

session.close()
'''
```

### API Requests
```python
import requests
import json

# GET request
response = requests.get('https://api.example.com/data')
if response.status_code == 200:
    data = response.json()
    print(data)

# POST request
payload = {'key': 'value'}
response = requests.post('https://api.example.com/data', 
                        json=payload,
                        headers={'Content-Type': 'application/json'})

# Error handling
try:
    response = requests.get('https://api.example.com/data', timeout=5)
    response.raise_for_status()  # Raises exception for bad status codes
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### Logging
```python
import logging

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log messages
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Log with variables
name = "John"
age = 30
logger.info(f"User {name} is {age} years old")
```

## Performance Tips

### Memory and Speed Optimization
```python
# Use generators for large datasets
def read_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Use list comprehensions instead of loops
# Slow
result = []
for i in range(1000):
    if i % 2 == 0:
        result.append(i * 2)

# Fast
result = [i * 2 for i in range(1000) if i % 2 == 0]

# Use appropriate data structures
# Use set for membership testing
large_set = set(range(1000000))
if 500000 in large_set:  # O(1) average case
    pass

# Use dict for lookups
lookup = {item: index for index, item in enumerate(items)}

# Profile your code
import cProfile
cProfile.run('your_function()')

# Time specific operations
import time
start = time.time()
# Your code here
end = time.time()
print(f"Execution time: {end - start:.4f} seconds")
```