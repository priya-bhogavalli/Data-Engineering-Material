# Python Data Engineering Examples with Outputs

# 1. List Comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(squares)
# Output: [1, 4, 9, 16, 25]

# 2. Dictionary Operations
data = {'name': 'John', 'age': 30, 'city': 'NYC'}
print(data.get('name'))
print(data.keys())
# Output: John
# Output: dict_keys(['name', 'age', 'city'])

# 3. File Reading
with open('sample.txt', 'w') as f:
    f.write('Hello\nWorld\nData')

with open('sample.txt', 'r') as f:
    lines = f.readlines()
print(lines)
# Output: ['Hello\n', 'World\n', 'Data']

# 4. JSON Processing
import json
data = {'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]}
json_str = json.dumps(data)
print(json_str)
# Output: {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

# 5. Pandas DataFrame
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(df)
# Output:
#    A  B
# 0  1  4
# 1  2  5
# 2  3  6

print(df.sum())
# Output:
# A     6
# B    15
# dtype: int64

# 6. Error Handling
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
# Output: Error: division by zero

# 7. Lambda Functions
nums = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)
# Output: [2, 4]

# 8. String Operations
text = "  Hello World  "
print(text.strip().lower().replace(' ', '_'))
# Output: hello_world