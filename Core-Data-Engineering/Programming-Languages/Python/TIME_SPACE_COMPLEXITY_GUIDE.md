# Time and Space Complexity Guide
**Understanding Algorithm Efficiency Through Travel Analogies**

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [What is Complexity?](#what-is-complexity)
3. [Time Complexity](#time-complexity)
4. [Space Complexity](#space-complexity)
5. [Big O Notation](#big-o-notation)
6. [Common Complexities with Travel Analogies](#common-complexities-with-travel-analogies)
7. [Python Examples by Complexity](#python-examples-by-complexity)
8. [Real-World Data Engineering Examples](#real-world-data-engineering-examples)
9. [How to Analyze Complexity](#how-to-analyze-complexity)
10. [Optimization Strategies](#optimization-strategies)

---

## Introduction

Imagine you're planning different types of trips. Some trips are quick and efficient, while others take forever and require lots of luggage. Similarly, algorithms have different efficiency characteristics - some are fast and use little memory, while others are slow and memory-hungry.

**Time Complexity** = How long your trip takes
**Space Complexity** = How much luggage you need to pack

---

## What is Complexity?

### The Travel Planning Problem

Think of complexity as answering two questions when planning a trip:

1. **"How long will this trip take?"** (Time Complexity)
2. **"How much stuff do I need to pack?"** (Space Complexity)

The answers depend on:
- **Where you're going** (input size)
- **How you're traveling** (algorithm choice)
- **What you're doing there** (problem requirements)

### Why Does It Matter?

```python
# Bad Algorithm: Like taking a horse-drawn carriage across the country
def slow_search(items, target):
    for i in range(len(items)):
        for j in range(len(items)):  # Unnecessary nested loop!
            if items[i] == target:
                return i
    return -1

# Good Algorithm: Like taking a direct flight
def fast_search(items, target):
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1

# Test with a list of cities
cities = ["New York", "London", "Tokyo", "Paris", "Sydney"]
print(fast_search(cities, "Tokyo"))  # Much faster!
```

---

## Time Complexity

### Travel Analogy: Different Ways to Visit Cities

Imagine you need to visit cities to deliver packages. The time it takes depends on your strategy:

#### O(1) - Constant Time: "Direct Flight"
```python
# Like having a private jet that goes directly to any city instantly
def get_first_city(cities):
    return cities[0]  # Always takes the same time, regardless of list size

cities_small = ["NYC", "LA"]
cities_large = ["NYC", "LA", "Chicago", "Miami", "Seattle", "Denver", "Boston"]

print(get_first_city(cities_small))   # Same speed
print(get_first_city(cities_large))   # Same speed
```

#### O(log n) - Logarithmic Time: "Smart Navigation"
```python
# Like using GPS that eliminates half the possible routes each decision
def binary_search_city(sorted_cities, target):
    left, right = 0, len(sorted_cities) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if sorted_cities[mid] == target:
            return mid
        elif sorted_cities[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Sorted list of cities
cities = ["Boston", "Chicago", "Denver", "LA", "Miami", "NYC", "Seattle"]
print(binary_search_city(cities, "Miami"))  # Very efficient even for large lists
```

#### O(n) - Linear Time: "Road Trip Visiting Each City Once"
```python
# Like driving and visiting each city exactly once
def find_city_with_most_attractions(cities_attractions):
    max_attractions = 0
    best_city = ""
    
    for city, attractions in cities_attractions.items():
        if attractions > max_attractions:
            max_attractions = attractions
            best_city = city
    
    return best_city

cities = {
    "NYC": 150,
    "LA": 120,
    "Chicago": 80,
    "Miami": 60
}
print(find_city_with_most_attractions(cities))  # Time grows with number of cities
```

#### O(n²) - Quadratic Time: "Visiting Every Pair of Cities"
```python
# Like calculating distance between every pair of cities
def find_closest_city_pairs(cities):
    closest_pairs = []
    
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            # Simulate distance calculation
            distance = abs(hash(cities[i]) - hash(cities[j])) % 1000
            closest_pairs.append((cities[i], cities[j], distance))
    
    return sorted(closest_pairs, key=lambda x: x[2])[:3]

cities = ["NYC", "LA", "Chicago", "Miami"]
print(find_closest_city_pairs(cities))  # Time grows exponentially with cities
```

#### O(2ⁿ) - Exponential Time: "Trying Every Possible Route"
```python
# Like trying every possible combination of cities to visit
def all_possible_routes(cities):
    if len(cities) <= 1:
        return [cities]
    
    routes = []
    for i in range(len(cities)):
        rest = cities[:i] + cities[i+1:]
        for route in all_possible_routes(rest):
            routes.append([cities[i]] + route)
    
    return routes

small_cities = ["NYC", "LA", "Chicago"]
print(f"Routes for {len(small_cities)} cities: {len(all_possible_routes(small_cities))}")
# Don't try with more than 4-5 cities - it explodes!
```

---

## Space Complexity

### Travel Analogy: Packing for Different Types of Trips

Space complexity is like deciding how much luggage to pack:

#### O(1) - Constant Space: "Minimalist Traveler"
```python
# Like packing only a small carry-on regardless of trip length
def count_cities_visited(cities):
    count = 0  # Only need one counter variable
    for city in cities:
        count += 1
    return count

# Uses same amount of "luggage" (memory) regardless of input size
cities_short = ["NYC", "LA"]
cities_long = ["NYC", "LA", "Chicago", "Miami", "Seattle", "Denver"]
print(count_cities_visited(cities_short))   # Same memory usage
print(count_cities_visited(cities_long))    # Same memory usage
```

#### O(n) - Linear Space: "Pack One Item Per Day"
```python
# Like packing one outfit for each day of travel
def create_itinerary(cities):
    itinerary = []  # Luggage grows with trip length
    for i, city in enumerate(cities):
        itinerary.append(f"Day {i+1}: Visit {city}")
    return itinerary

cities = ["NYC", "LA", "Chicago", "Miami"]
itinerary = create_itinerary(cities)
print(itinerary)
# Memory usage grows proportionally with number of cities
```

#### O(n²) - Quadratic Space: "Pack for Every Possible Weather Combination"
```python
# Like packing different outfits for every possible weather in every city
def weather_combinations(cities):
    weather_types = ["sunny", "rainy", "snowy", "cloudy"]
    combinations = []
    
    for city in cities:
        for weather in weather_types:
            combinations.append(f"{city}-{weather}")
    
    return combinations

cities = ["NYC", "LA", "Chicago"]
combos = weather_combinations(cities)
print(f"Total combinations: {len(combos)}")
# Memory usage grows with cities × weather types
```

---

## Big O Notation

### The Travel Time Chart

Think of Big O as a travel time estimate chart:

| Notation | Travel Analogy | Example | Growth Rate |
|----------|----------------|---------|-------------|
| **O(1)** | Teleportation | Direct access | Instant |
| **O(log n)** | Smart GPS | Binary search | Very slow growth |
| **O(n)** | Highway drive | Linear search | Steady growth |
| **O(n log n)** | Efficient tour | Good sorting | Moderate growth |
| **O(n²)** | City-to-city visits | Nested loops | Fast growth |
| **O(2ⁿ)** | Try every route | Brute force | Explosive growth |

### Visual Growth Comparison

```python
import math

def compare_growth_rates(n):
    """Compare how different complexities grow with input size"""
    print(f"For n = {n}:")
    print(f"O(1):      {1}")
    print(f"O(log n):  {math.log2(n):.1f}")
    print(f"O(n):      {n}")
    print(f"O(n log n): {n * math.log2(n):.1f}")
    print(f"O(n²):     {n**2}")
    print(f"O(2ⁿ):     {2**n if n < 20 else 'Too large!'}")
    print("-" * 30)

# See how they grow
for size in [10, 100, 1000]:
    compare_growth_rates(size)
```

---

## Common Complexities with Travel Analogies

### 1. O(1) - Constant Time: "Express Elevator"

**Analogy**: Taking an express elevator directly to your floor
**Real Example**: Accessing a specific hotel room with a key card

```python
# Hotel room access - always takes same time
def get_room_info(hotel_rooms, room_number):
    return hotel_rooms[room_number]  # Direct access

hotel = {
    101: "Single bed, city view",
    205: "Double bed, ocean view", 
    310: "Suite, mountain view"
}

print(get_room_info(hotel, 205))  # Always O(1)
```

### 2. O(log n) - Logarithmic Time: "Phone Book Search"

**Analogy**: Finding a name in a phone book by opening to the middle and eliminating half each time
**Real Example**: Finding a flight in a sorted schedule

```python
# Finding flight in sorted schedule
def find_flight(flights, target_time):
    left, right = 0, len(flights) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if flights[mid]['time'] == target_time:
            return flights[mid]
        elif flights[mid]['time'] < target_time:
            left = mid + 1
        else:
            right = mid - 1
    return None

flights = [
    {'time': '08:00', 'destination': 'NYC'},
    {'time': '10:30', 'destination': 'LA'},
    {'time': '14:15', 'destination': 'Chicago'},
    {'time': '18:45', 'destination': 'Miami'}
]

print(find_flight(flights, '14:15'))
```

### 3. O(n) - Linear Time: "Security Check Line"

**Analogy**: Going through airport security - time depends on number of people in line
**Real Example**: Checking each passenger's ticket

```python
# Checking each passenger's ticket
def validate_all_tickets(passengers):
    valid_count = 0
    for passenger in passengers:
        if passenger['ticket_valid']:
            valid_count += 1
    return valid_count

passengers = [
    {'name': 'Alice', 'ticket_valid': True},
    {'name': 'Bob', 'ticket_valid': False},
    {'name': 'Charlie', 'ticket_valid': True}
]

print(f"Valid tickets: {validate_all_tickets(passengers)}")
```

### 4. O(n²) - Quadratic Time: "Round-Robin Tournament"

**Analogy**: Every team plays every other team once
**Real Example**: Comparing every pair of travel routes

```python
# Comparing all route combinations
def compare_all_routes(cities):
    comparisons = []
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            distance = abs(len(cities[i]) - len(cities[j]))  # Simple distance
            comparisons.append(f"{cities[i]} to {cities[j]}: {distance}")
    return comparisons

cities = ["NYC", "LA", "Chicago", "Miami"]
routes = compare_all_routes(cities)
for route in routes:
    print(route)
```

---

## Python Examples by Complexity

### Data Structure Operations

```python
# Dictionary operations - O(1) average case
travel_costs = {"NYC": 500, "LA": 600, "Chicago": 400}
print(travel_costs["NYC"])  # O(1) - instant lookup

# List operations - various complexities
destinations = ["NYC", "LA", "Chicago", "Miami"]

# O(1) operations
print(destinations[0])        # Access by index
destinations.append("Boston") # Add to end

# O(n) operations  
print("Chicago" in destinations)  # Search
destinations.remove("LA")         # Remove by value
destinations.insert(0, "Seattle") # Insert at beginning

# O(n log n) operations
destinations.sort()  # Sorting

print(destinations)
```

### Algorithm Comparisons

```python
import time

def time_algorithm(func, data, *args):
    """Measure algorithm execution time"""
    start = time.time()
    result = func(data, *args)
    end = time.time()
    return result, (end - start) * 1000  # milliseconds

# Linear search - O(n)
def linear_search(cities, target):
    for i, city in enumerate(cities):
        if city == target:
            return i
    return -1

# Binary search - O(log n) - requires sorted list
def binary_search(cities, target):
    left, right = 0, len(cities) - 1
    while left <= right:
        mid = (left + right) // 2
        if cities[mid] == target:
            return mid
        elif cities[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Test with different sized datasets
small_cities = ["Boston", "Chicago", "LA", "Miami", "NYC"]
large_cities = sorted([f"City_{i}" for i in range(1000)])

print("=== Small Dataset (5 cities) ===")
result, time_taken = time_algorithm(linear_search, small_cities, "NYC")
print(f"Linear search: {time_taken:.3f}ms")

result, time_taken = time_algorithm(binary_search, small_cities, "NYC")
print(f"Binary search: {time_taken:.3f}ms")

print("\n=== Large Dataset (1000 cities) ===")
result, time_taken = time_algorithm(linear_search, large_cities, "City_500")
print(f"Linear search: {time_taken:.3f}ms")

result, time_taken = time_algorithm(binary_search, large_cities, "City_500")
print(f"Binary search: {time_taken:.3f}ms")
```

---

## Real-World Data Engineering Examples

### 1. Database Query Optimization

```python
# Simulating database operations with different complexities

class TravelDatabase:
    def __init__(self):
        self.bookings = []
        self.booking_index = {}  # O(1) lookup
    
    def add_booking(self, booking_id, passenger, destination):
        """O(1) - Adding to end of list and updating index"""
        booking = {
            'id': booking_id,
            'passenger': passenger, 
            'destination': destination
        }
        self.bookings.append(booking)
        self.booking_index[booking_id] = len(self.bookings) - 1
    
    def find_booking_slow(self, booking_id):
        """O(n) - Linear search through all bookings"""
        for booking in self.bookings:
            if booking['id'] == booking_id:
                return booking
        return None
    
    def find_booking_fast(self, booking_id):
        """O(1) - Direct index lookup"""
        if booking_id in self.booking_index:
            index = self.booking_index[booking_id]
            return self.bookings[index]
        return None
    
    def get_bookings_by_destination(self, destination):
        """O(n) - Must check all bookings"""
        result = []
        for booking in self.bookings:
            if booking['destination'] == destination:
                result.append(booking)
        return result

# Usage example
db = TravelDatabase()
db.add_booking("B001", "Alice", "NYC")
db.add_booking("B002", "Bob", "LA") 
db.add_booking("B003", "Charlie", "NYC")

print("Fast lookup:", db.find_booking_fast("B002"))
print("NYC bookings:", db.get_bookings_by_destination("NYC"))
```

### 2. Data Processing Pipeline Complexity

```python
# Different approaches to processing travel data

def process_bookings_simple(bookings):
    """O(n) - Process each booking once"""
    processed = []
    for booking in bookings:
        processed_booking = {
            'id': booking['id'],
            'passenger': booking['passenger'].upper(),
            'destination': booking['destination'],
            'processed': True
        }
        processed.append(processed_booking)
    return processed

def process_bookings_inefficient(bookings):
    """O(n²) - Inefficient nested processing"""
    processed = []
    for booking in bookings:
        # Inefficient: checking against all other bookings
        duplicate_count = 0
        for other_booking in bookings:
            if booking['passenger'] == other_booking['passenger']:
                duplicate_count += 1
        
        processed_booking = {
            'id': booking['id'],
            'passenger': booking['passenger'].upper(),
            'destination': booking['destination'],
            'duplicate_passengers': duplicate_count,
            'processed': True
        }
        processed.append(processed_booking)
    return processed

def process_bookings_optimized(bookings):
    """O(n) - Optimized with single pass and dictionary"""
    passenger_count = {}
    processed = []
    
    # First pass: count passengers - O(n)
    for booking in bookings:
        passenger = booking['passenger']
        passenger_count[passenger] = passenger_count.get(passenger, 0) + 1
    
    # Second pass: process with counts - O(n)
    for booking in bookings:
        processed_booking = {
            'id': booking['id'],
            'passenger': booking['passenger'].upper(),
            'destination': booking['destination'],
            'duplicate_passengers': passenger_count[booking['passenger']],
            'processed': True
        }
        processed.append(processed_booking)
    
    return processed

# Test data
bookings = [
    {'id': 'B001', 'passenger': 'Alice', 'destination': 'NYC'},
    {'id': 'B002', 'passenger': 'Bob', 'destination': 'LA'},
    {'id': 'B003', 'passenger': 'Alice', 'destination': 'Chicago'},
    {'id': 'B004', 'passenger': 'Charlie', 'destination': 'Miami'}
]

print("=== Processing Results ===")
result = process_bookings_optimized(bookings)
for booking in result:
    print(booking)
```

### 3. Memory Usage in Data Processing

```python
# Comparing memory usage approaches

def load_all_data_memory_heavy(file_size):
    """O(n) space - Load everything into memory"""
    data = []
    for i in range(file_size):
        record = {
            'booking_id': f'B{i:06d}',
            'passenger': f'Passenger_{i}',
            'destination': f'City_{i % 100}',
            'price': i * 10
        }
        data.append(record)
    return data

def process_data_memory_efficient(file_size):
    """O(1) space - Process one record at a time"""
    total_revenue = 0
    booking_count = 0
    
    for i in range(file_size):
        # Simulate reading one record at a time
        price = i * 10
        total_revenue += price
        booking_count += 1
        
        # Don't store the record, just process it
    
    return {
        'total_revenue': total_revenue,
        'average_price': total_revenue / booking_count if booking_count > 0 else 0,
        'booking_count': booking_count
    }

def batch_process_data(file_size, batch_size=1000):
    """O(batch_size) space - Process in chunks"""
    total_revenue = 0
    booking_count = 0
    
    for start in range(0, file_size, batch_size):
        # Process one batch at a time
        batch = []
        end = min(start + batch_size, file_size)
        
        for i in range(start, end):
            record = {
                'booking_id': f'B{i:06d}',
                'price': i * 10
            }
            batch.append(record)
        
        # Process batch
        for record in batch:
            total_revenue += record['price']
            booking_count += 1
        
        # Clear batch from memory
        batch.clear()
    
    return {
        'total_revenue': total_revenue,
        'booking_count': booking_count
    }

# Compare approaches
print("=== Memory Usage Comparison ===")
file_size = 10000

# Memory efficient approach
result = process_data_memory_efficient(file_size)
print(f"Memory efficient result: {result}")

# Batch processing approach  
result = batch_process_data(file_size, batch_size=500)
print(f"Batch processing result: {result}")
```

---

## How to Analyze Complexity

### Step-by-Step Analysis Method

```python
def analyze_algorithm_complexity():
    """
    Step-by-step guide to analyze algorithm complexity
    """
    
    print("=== How to Analyze Algorithm Complexity ===\n")
    
    print("1. IDENTIFY THE INPUT SIZE")
    print("   - What grows as the problem gets bigger?")
    print("   - Usually 'n' = number of elements\n")
    
    print("2. COUNT THE OPERATIONS")
    print("   - Look for loops, recursive calls, function calls")
    print("   - Ignore constants and lower-order terms\n")
    
    print("3. FIND THE DOMINANT TERM")
    print("   - Which operation happens most frequently?")
    print("   - This determines your Big O\n")
    
    print("4. EXAMPLES:")
    
    # Example 1: Single loop
    def example_linear(cities):
        """O(n) - visits each city once"""
        for city in cities:          # n iterations
            print(f"Visiting {city}")  # O(1) operation
        # Total: n × O(1) = O(n)
    
    print("   Single loop → O(n)")
    
    # Example 2: Nested loops
    def example_quadratic(cities):
        """O(n²) - compares every pair"""
        for city1 in cities:           # n iterations
            for city2 in cities:       # n iterations for each city1
                if city1 != city2:     # O(1) operation
                    print(f"{city1} to {city2}")
        # Total: n × n × O(1) = O(n²)
    
    print("   Nested loops → O(n²)")
    
    # Example 3: Divide and conquer
    def example_logarithmic(cities, target, left=0, right=None):
        """O(log n) - eliminates half each time"""
        if right is None:
            right = len(cities) - 1
            
        if left > right:
            return -1
            
        mid = (left + right) // 2
        if cities[mid] == target:
            return mid
        elif cities[mid] < target:
            return example_logarithmic(cities, target, mid + 1, right)
        else:
            return example_logarithmic(cities, target, left, mid - 1)
        # Each call eliminates half → O(log n)
    
    print("   Divide and conquer → O(log n)")

analyze_algorithm_complexity()
```

### Common Patterns Recognition

```python
def complexity_patterns():
    """Common code patterns and their complexities"""
    
    print("=== Common Complexity Patterns ===\n")
    
    # Pattern 1: Simple loops
    print("PATTERN 1: Simple Loops")
    def pattern_1(items):
        for item in items:        # O(n)
            print(item)           # O(1)
        # Result: O(n)
    
    # Pattern 2: Nested loops
    print("PATTERN 2: Nested Loops")  
    def pattern_2(items):
        for i in items:           # O(n)
            for j in items:       # O(n) for each i
                print(i, j)       # O(1)
        # Result: O(n²)
    
    # Pattern 3: Loop with function call
    print("PATTERN 3: Loop + Function Call")
    def expensive_function(item):
        # If this is O(k), then total becomes O(n×k)
        return item * 2
    
    def pattern_3(items):
        for item in items:                    # O(n)
            result = expensive_function(item) # O(k)
            print(result)                     # O(1)
        # Result: O(n×k)
    
    # Pattern 4: Divide and conquer
    print("PATTERN 4: Divide and Conquer")
    def pattern_4(items):
        if len(items) <= 1:
            return items
        
        mid = len(items) // 2
        left = pattern_4(items[:mid])     # T(n/2)
        right = pattern_4(items[mid:])    # T(n/2)
        return merge(left, right)         # O(n)
        # Result: O(n log n)
    
    def merge(left, right):
        # Simple merge - O(n)
        return sorted(left + right)

complexity_patterns()
```

---

## Optimization Strategies

### Travel Planning Optimization Examples

```python
# Optimization Strategy 1: Use Better Data Structures
print("=== Optimization Strategy 1: Better Data Structures ===")

# Slow: Using list for lookups - O(n)
def find_hotel_slow(hotels_list, hotel_name):
    for hotel in hotels_list:
        if hotel['name'] == hotel_name:
            return hotel
    return None

# Fast: Using dictionary for lookups - O(1)
def find_hotel_fast(hotels_dict, hotel_name):
    return hotels_dict.get(hotel_name)

hotels_list = [
    {'name': 'Grand Hotel', 'price': 200},
    {'name': 'Budget Inn', 'price': 80},
    {'name': 'Luxury Resort', 'price': 500}
]

hotels_dict = {
    'Grand Hotel': {'price': 200},
    'Budget Inn': {'price': 80}, 
    'Luxury Resort': {'price': 500}
}

print("List lookup:", find_hotel_slow(hotels_list, 'Budget Inn'))
print("Dict lookup:", find_hotel_fast(hotels_dict, 'Budget Inn'))

# Optimization Strategy 2: Avoid Unnecessary Work
print("\n=== Optimization Strategy 2: Avoid Unnecessary Work ===")

# Inefficient: Recalculating same values
def calculate_trip_cost_slow(destinations, base_cost):
    total = 0
    for dest in destinations:
        # Recalculating expensive operation each time
        tax_rate = len(dest) * 0.01  # Simulated expensive calculation
        cost_with_tax = base_cost * (1 + tax_rate)
        total += cost_with_tax
    return total

# Efficient: Cache expensive calculations
def calculate_trip_cost_fast(destinations, base_cost):
    tax_cache = {}
    total = 0
    
    for dest in destinations:
        if dest not in tax_cache:
            tax_cache[dest] = len(dest) * 0.01  # Calculate once
        
        cost_with_tax = base_cost * (1 + tax_cache[dest])
        total += cost_with_tax
    return total

destinations = ["New York", "Los Angeles", "Chicago", "New York", "Los Angeles"]
print("Slow calculation:", calculate_trip_cost_slow(destinations, 100))
print("Fast calculation:", calculate_trip_cost_fast(destinations, 100))

# Optimization Strategy 3: Use Built-in Functions
print("\n=== Optimization Strategy 3: Use Built-in Functions ===")

# Slow: Manual implementation
def find_max_price_slow(hotels):
    max_price = 0
    for hotel in hotels:
        if hotel['price'] > max_price:
            max_price = hotel['price']
    return max_price

# Fast: Built-in function
def find_max_price_fast(hotels):
    return max(hotel['price'] for hotel in hotels)

hotels = [
    {'name': 'Hotel A', 'price': 150},
    {'name': 'Hotel B', 'price': 200},
    {'name': 'Hotel C', 'price': 120}
]

print("Manual max:", find_max_price_slow(hotels))
print("Built-in max:", find_max_price_fast(hotels))
```

### Memory Optimization Techniques

```python
print("=== Memory Optimization Techniques ===")

# Technique 1: Generators vs Lists
def create_itinerary_memory_heavy(days):
    """O(n) space - stores all days in memory"""
    itinerary = []
    for day in range(1, days + 1):
        itinerary.append(f"Day {day}: Explore city")
    return itinerary

def create_itinerary_memory_light(days):
    """O(1) space - generates days on demand"""
    for day in range(1, days + 1):
        yield f"Day {day}: Explore city"

print("Memory heavy approach:")
heavy_itinerary = create_itinerary_memory_heavy(5)
print(heavy_itinerary)

print("\nMemory light approach:")
light_itinerary = create_itinerary_memory_light(5)
for day in light_itinerary:
    print(day)

# Technique 2: In-place operations
def sort_destinations_new_list(destinations):
    """O(n) extra space - creates new list"""
    return sorted(destinations)

def sort_destinations_in_place(destinations):
    """O(1) extra space - modifies original"""
    destinations.sort()
    return destinations

destinations = ["Paris", "London", "Tokyo", "New York"]
print("\nNew list sort:", sort_destinations_new_list(destinations.copy()))
print("In-place sort:", sort_destinations_in_place(destinations.copy()))
```

---

## Quick Reference Guide

### Complexity Cheat Sheet

```python
def complexity_cheat_sheet():
    """Quick reference for common operations"""
    
    complexities = {
        "Data Structure Operations": {
            "List": {
                "Access by index": "O(1)",
                "Search by value": "O(n)", 
                "Insert at end": "O(1)",
                "Insert at beginning": "O(n)",
                "Delete by index": "O(n)",
                "Sort": "O(n log n)"
            },
            "Dictionary": {
                "Access by key": "O(1) average",
                "Insert": "O(1) average",
                "Delete": "O(1) average",
                "Search": "O(1) average"
            },
            "Set": {
                "Add element": "O(1) average",
                "Remove element": "O(1) average", 
                "Check membership": "O(1) average"
            }
        },
        
        "Common Algorithms": {
            "Linear Search": "O(n)",
            "Binary Search": "O(log n)",
            "Bubble Sort": "O(n²)",
            "Quick Sort": "O(n log n) average",
            "Merge Sort": "O(n log n)",
            "Hash Table Lookup": "O(1) average"
        },
        
        "Loop Patterns": {
            "Single loop": "O(n)",
            "Nested loops": "O(n²)", 
            "Triple nested": "O(n³)",
            "Loop + binary search": "O(n log n)",
            "Recursive divide": "O(log n)"
        }
    }
    
    for category, items in complexities.items():
        print(f"\n=== {category} ===")
        for operation, complexity in items.items():
            if isinstance(complexity, dict):
                print(f"\n{operation}:")
                for sub_op, sub_complexity in complexity.items():
                    print(f"  {sub_op}: {sub_complexity}")
            else:
                print(f"{operation}: {complexity}")

complexity_cheat_sheet()
```

### When to Optimize

```python
def optimization_decision_guide():
    """Guide for deciding when to optimize"""
    
    print("=== When Should You Optimize? ===\n")
    
    guidelines = [
        {
            "scenario": "Small datasets (< 1000 items)",
            "recommendation": "Don't optimize unless necessary",
            "reason": "Performance difference negligible"
        },
        {
            "scenario": "Medium datasets (1K - 100K items)", 
            "recommendation": "Consider O(n²) → O(n log n) optimizations",
            "reason": "Noticeable performance gains"
        },
        {
            "scenario": "Large datasets (> 100K items)",
            "recommendation": "Optimize aggressively, consider O(n) → O(1) improvements",
            "reason": "Critical for user experience"
        },
        {
            "scenario": "Real-time systems",
            "recommendation": "Optimize for consistent performance",
            "reason": "Predictable response times required"
        },
        {
            "scenario": "Memory-constrained environments",
            "recommendation": "Optimize space complexity first",
            "reason": "Memory limits more critical than speed"
        }
    ]
    
    for guideline in guidelines:
        print(f"Scenario: {guideline['scenario']}")
        print(f"Recommendation: {guideline['recommendation']}")
        print(f"Reason: {guideline['reason']}\n")

optimization_decision_guide()
```

---

## Summary

### Key Takeaways

1. **Time Complexity** = How execution time grows with input size
2. **Space Complexity** = How memory usage grows with input size  
3. **Big O Notation** = Upper bound on growth rate
4. **Common Patterns**:
   - O(1): Direct access, hash lookups
   - O(log n): Binary search, balanced trees
   - O(n): Single loops, linear search
   - O(n log n): Efficient sorting algorithms
   - O(n²): Nested loops, comparing all pairs
   - O(2ⁿ): Exponential algorithms (avoid!)

### Travel Analogy Summary

| Complexity | Travel Analogy | When to Use |
|------------|----------------|-------------|
| **O(1)** | Direct flight | Accessing known data |
| **O(log n)** | Smart GPS navigation | Searching sorted data |
| **O(n)** | Road trip visiting each city | Processing all items once |
| **O(n log n)** | Efficient tour planning | Sorting, divide-and-conquer |
| **O(n²)** | Visiting every city pair | Comparing all combinations |
| **O(2ⁿ)** | Trying every possible route | Brute force (last resort) |

### Final Tips

1. **Measure, don't guess** - Profile your code to find real bottlenecks
2. **Optimize the right thing** - Focus on the most frequently used operations
3. **Consider trade-offs** - Sometimes space-time trade-offs are worth it
4. **Use appropriate data structures** - Choose the right tool for the job
5. **Don't premature optimize** - Write clear code first, optimize when needed

Remember: **"Premature optimization is the root of all evil"** - Donald Knuth

Focus on writing correct, readable code first. Optimize only when you have evidence that performance is actually a problem!