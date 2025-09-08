# Python Interview Questions for Data Engineering

## 📋 Quick Navigation

### 🎯 **By Difficulty Level**
- **🟢 Fundamentals**: [Python Basics](#fundamentals) | [Memory & GC](#memory-management) | [Data Types](#data-types)
- **🟡 Intermediate**: [OOP Concepts](#oop-concepts) | [Concurrency](#concurrency) | [Advanced Features](#advanced-features)
- **🔴 Advanced**: [Design Patterns](#design-patterns) | [Performance](#performance) | [Production Code](#production)
- **💼 Data Engineering**: [Large Data](#large-data-processing) | [Databases](#database-connections) | [Pipelines](#data-pipelines)

### 📚 **By Topic Category**
- **Language Core**: [Syntax & Semantics](#language-core) | [Memory Model](#memory-model) | [Object Model](#object-model)
- **Data Processing**: [File Handling](#file-processing) | [Streaming](#streaming-data) | [Parallel Processing](#parallel-processing)
- **System Integration**: [APIs](#api-integration) | [Databases](#database-integration) | [Error Handling](#error-handling)

### ⚡ **Quick Reference**
- [Interview Checklist](#interview-checklist) | [Code Templates](#code-templates) | [Performance Tips](#performance-tips)

---

## 📊 Interview Question Categories

### 🟢 Fundamentals
1. [Python 2 vs Python 3](#1-python-2-vs-python-3)
2. [Memory Management & GC](#2-memory-management--garbage-collection)
3. [is vs == Operators](#3-is-vs--operators)
4. [Lists vs Tuples](#4-lists-vs-tuples)
5. [List Comprehensions vs Generators](#5-list-comprehensions-vs-generators)

### 🟡 Intermediate
6. [Decorators](#6-decorators)
7. [*args and **kwargs](#7-args-and-kwargs)
8. [Global Interpreter Lock (GIL)](#8-global-interpreter-lock-gil)
9. [Method Resolution Order (MRO)](#9-method-resolution-order-mro)
10. [Deep vs Shallow Copy](#10-deep-vs-shallow-copy)

### 🔴 Advanced
11. [Singleton Pattern](#11-singleton-pattern)
12. [Context Managers](#12-context-managers)
13. [Iterators vs Generators](#13-iterators-vs-generators)
14. [Thread-Safe Patterns](#14-thread-safe-patterns)

### 💼 Data Engineering Specific
15. [Large File Processing](#15-large-file-processing)
16. [Database Connections](#16-database-connections)
17. [Async/Await for Data Engineering](#17-asyncawait-for-data-engineering)
18. [Performance Optimization](#18-performance-optimization)
19. [Error Handling & Logging](#19-error-handling--logging)

### 🧩 Coding Challenges
20. [LRU Cache Implementation](#20-lru-cache-implementation)
21. [Most Frequent Elements](#21-most-frequent-elements)
22. [Data Pipeline with Monitoring](#22-data-pipeline-with-monitoring)

### 📚 Study Resources
- [Study Guide & Key Takeaways](#study-guide--key-takeaways)
- [Interview Preparation Checklist](#interview-preparation-checklist)
- [Performance Optimization Guide](#performance-optimization-guide)

---

## 🎯 Essential Concepts Summary

### 🔑 **Must-Know for Data Engineering Interviews**
- **Memory Management**: Reference counting, GC, memory optimization for large datasets
- **GIL Impact**: When to use threading vs multiprocessing vs async/await
- **Data Structures**: Lists vs tuples, generators vs comprehensions, appropriate data structure selection
- **Error Handling**: Production-ready exception handling, logging, retry mechanisms
- **Performance**: Profiling, optimization techniques, scaling strategies
- **Concurrency**: Threading, multiprocessing, async programming for I/O-bound tasks

### 📊 **Interview Success Metrics**
- **Fundamentals**: 90%+ accuracy on basic Python concepts
- **Problem Solving**: Systematic approach to coding challenges
- **Code Quality**: Clean, readable, maintainable solutions
- **Production Awareness**: Understanding of real-world constraints and trade-offs

---

## 🟢 Fundamentals

### 1. What are the key differences between Python 2 and Python 3?

### 🎯 **Theoretical Foundation**

#### **Core Concepts**
- **Backward Compatibility Breaking**: Python 3 intentionally broke compatibility to fix fundamental design flaws
- **Unicode-First Design**: Native Unicode support eliminates encoding issues
- **Improved Language Consistency**: Unified approach to division, print function, and iterators
- **Memory Efficiency**: Better memory management through iterator-based built-ins

#### **Historical Context**
- **Released 2008**: Python 3.0 marked a major language evolution milestone
- **10-Year Transition**: Extended migration period from Python 2 to 3
- **End of Life 2020**: Python 2.7 reached end-of-life, forcing enterprise migrations
- **Lessons Learned**: Influenced how other languages handle major version transitions

#### **Architectural Principles**
- **"There should be one obvious way to do it"**: Zen of Python principle applied to language design
- **Future-Proofing**: Design decisions made to support long-term language evolution
- **Performance vs Compatibility**: Trade-offs between breaking changes and performance improvements
- **Developer Experience**: Prioritizing clarity and consistency over backward compatibility



### 📊 **Comparative Analysis**

#### **Technology Comparison Matrix**
| Feature | Python | Java | Scala | R |
|---------|---------------|--------|--------|--------|
| **Performance** | High performance characteristics | Comparative performance analysis needed | Comparative performance analysis needed | Comparative performance analysis needed |
| **Scalability** | Scalability characteristics | Scalability comparison needed | Scalability comparison needed | Scalability comparison needed |
| **Cost (TCO)** | $0 (Open Source) | Cost comparison needed | Cost comparison needed | Cost comparison needed |
| **Learning Curve** | Low | Learning curve comparison needed | Learning curve comparison needed | Learning curve comparison needed |
| **Community Support** | Very High (Top 3 programming languages) | Community comparison needed | Community comparison needed | Community comparison needed |
| **Enterprise Features** | Enterprise feature analysis needed | Enterprise feature comparison needed | Enterprise feature comparison needed | Enterprise feature comparison needed |

#### **Decision Framework**
```mermaid
graph TD
    A[Requirements Analysis] --> B{Data Volume?}
    B -->|Small| C[Python]
    B -->|Medium| D[Consider Alternatives]
    B -->|Large| E[Distributed Solution]
    
    C --> F{Performance Needs?}
    D --> F
    E --> F
    
    F -->|High| G[Optimized Solution]
    F -->|Standard| H[Standard Solution]
```

#### **Use Case Scenarios**
- **Choose Python when:**
    - Data analysis and machine learning
  - Web development (Django, Flask)
  - Automation and scripting

- **Consider alternatives when:**
  Specific scenarios requiring alternatives

- **Avoid Python when:**
    - Global Interpreter Lock (GIL) limits threading
  - Slower execution compared to compiled languages



#### **Performance Benchmarks**
```
Benchmark Results (Industry Standard Dataset):
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Metric          │ Python │ Java       │ Scala       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Throughput      │ Benchmark needed │ Benchmark needed │ Benchmark needed │
│ Latency (p95)   │ Benchmark needed │ Benchmark needed │ Benchmark needed │
│ Memory Usage    │ High: 2-10x more than compiled languages │ Benchmark needed │ Benchmark needed │
│ CPU Utilization │ CPU utilization data needed │ CPU utilization data needed │ CPU utilization data needed │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```



#### **Cost Analysis**
```
Total Cost of Ownership (3-year projection):
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Cost Component  │ Python │ Java       │ Scala       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Licensing       │ $0 (Open Source) │ Cost analysis needed │ Cost analysis needed │
│ Infrastructure  │ Cost analysis needed │ Cost analysis needed │ Cost analysis needed │
│ Operations      │ Cost analysis needed │ Cost analysis needed │ Cost analysis needed │
│ Training        │ Low (easy to learn) │ Cost analysis needed │ Cost analysis needed │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ **TOTAL**       │ **Total cost calculation needed** │ **Total cost calculation needed** │ **Total cost calculation needed** │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```



### 🌍 **Real-World Applications**

#### **Industry Use Cases**
  - Data analysis and machine learning
  - Web development (Django, Flask)
  - Automation and scripting
  - Scientific computing
  - ETL and data pipelines

#### **Production Considerations**
Key considerations when deploying Python in production environments

#### **Case Studies**
Real-world case studies of Python implementations



### 🔮 **Future Trends & Evolution**

#### **Emerging Developments**
Latest developments in Python ecosystem

#### **Industry Direction**
Future direction of Programming Language technologies

#### **Skills Evolution Requirements**
Evolving skill requirements for Python professionals


### 📚 **Further Reading**
- [Official Python Documentation](#python-docs)
- [Performance Optimization Guide](#python-performance)
- [Best Practices and Patterns](#python-patterns)
- [Community Resources](#python-community)
- [Certification Paths](#python-certification)

### **Enhanced Answer**

**Answer:**
Python 3 was released in 2008 as a major revision that broke backward compatibility to fix fundamental design issues in Python 2. Understanding these differences is crucial for data engineers working with legacy systems or migrating codebases.

**Historical Context & Impact:**
- **10-Year Transition Period**: The longest migration in programming language history
- **End-of-Life 2020**: Python 2.7 reached end-of-life, forcing enterprise migrations
- **Ecosystem Evolution**: Libraries gradually dropped Python 2 support
- **Performance Improvements**: Python 3 introduced significant optimizations

**Key Differences:**

**Print Statement vs Function:**
- **Python 2**: `print` is a statement: `print "hello", "world"`
- **Python 3**: `print()` is a function: `print("hello", "world")`
- **Impact**: Function syntax allows better control and redirection

**Division Behavior:**
- **Python 2**: `/` performs integer division for integers: `5/2 = 2`
- **Python 3**: `/` always returns float: `5/2 = 2.5`, use `//` for integer division
- **Impact**: Prevents silent bugs in mathematical calculations

**Unicode Handling:**
- **Python 2**: Strings are bytes by default, Unicode requires `u"string"` prefix
- **Python 3**: Strings are Unicode by default, bytes require `b"string"` prefix
- **Impact**: Better internationalization and text processing

**Range Function:**
- **Python 2**: `range()` returns list, `xrange()` returns iterator
- **Python 3**: `range()` returns iterator (like Python 2's `xrange()`)
- **Impact**: Memory efficiency for large ranges

**Input Function:**
- **Python 2**: `input()` evaluates input, `raw_input()` returns string
- **Python 3**: `input()` always returns string (safer)
- **Impact**: Eliminates security risks from evaluating user input

**Why This Matters for Data Engineering:**
- **Legacy Systems**: Many data systems still run Python 2 code
- **Migration Planning**: Understanding differences helps in upgrade strategies
- **Library Compatibility**: Some data tools may have version-specific requirements
- **Performance**: Python 3 has better performance and memory usage
- **Security**: Python 2 no longer receives security updates
- **Modern Libraries**: New data engineering tools require Python 3.6+
- **Type Hints**: Python 3.5+ type annotations improve code quality
- **f-strings**: Python 3.6+ f-string formatting is more efficient

```python
# Python 2 vs Python 3 examples

# Print differences
# Python 2: print "Hello", "World"  # Statement
# Python 3:
print("Hello", "World")  # Function
print("Data:", 42, sep="-", end="\n\n")  # More control

# Division differences
print("Division in Python 3:")
print(f"5/2 = {5/2}")      # 2.5 (float division)
print(f"5//2 = {5//2}")    # 2 (integer division)
print(f"5%2 = {5%2}")      # 1 (modulo)

# Unicode handling
text = "Hello, 世界"  # Unicode by default in Python 3
bytes_data = b"Hello"  # Explicit bytes
print(f"Text: {text}, Type: {type(text)}")
print(f"Bytes: {bytes_data}, Type: {type(bytes_data)}")

# Range behavior
large_range = range(1000000)  # Memory efficient iterator
print(f"Range type: {type(large_range)}")
print(f"Range size in memory: {large_range.__sizeof__()} bytes")

# Input function (Python 3 behavior)
# user_input = input("Enter a number: ")  # Always returns string
# print(f"You entered: {user_input} (type: {type(user_input)})")

# String formatting improvements in Python 3
name = "Alice"
age = 30
# Old style (works in both)
print("Name: %s, Age: %d" % (name, age))
# New style (Python 2.7+ and 3)
print("Name: {}, Age: {}".format(name, age))
# f-strings (Python 3.6+)
print(f"Name: {name}, Age: {age}")

# Exception handling syntax
try:
    result = 10 / 0
except ZeroDivisionError as e:  # 'as' syntax (Python 3)
    print(f"Error: {e}")
# Python 2 used: except ZeroDivisionError, e:

# Iterator behavior
data = [1, 2, 3, 4, 5]
# Python 3: map, filter, zip return iterators (memory efficient)
mapped = map(lambda x: x*2, data)
filtered = filter(lambda x: x > 2, data)
print(f"Map result: {list(mapped)}")
print(f"Filter result: {list(filtered)}")
```


### 2. Explain Python's memory management and garbage collection.
**Answer:**
Python's memory management is crucial for data engineering applications that process large datasets. Understanding how Python manages memory helps optimize performance and prevent memory leaks in long-running data pipelines.


### 🎯 **Theoretical Foundation**

#### **Core Concepts**
  - Readable and maintainable syntax
  - Extensive library ecosystem
  - Strong data science/ML support

#### **Historical Context**
Evolution of Programming Language technologies leading to Python

#### **Architectural Principles**
Key architectural decisions in Python design

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying Python operations



### 📊 **Comparative Analysis**

#### **Technology Comparison Matrix**
| Feature | Python | Java | Scala | R |
|---------|---------------|--------|--------|--------|
| **Performance** | High performance characteristics | Comparative performance analysis needed | Comparative performance analysis needed | Comparative performance analysis needed |
| **Scalability** | Scalability characteristics | Scalability comparison needed | Scalability comparison needed | Scalability comparison needed |
| **Cost (TCO)** | $0 (Open Source) | Cost comparison needed | Cost comparison needed | Cost comparison needed |
| **Learning Curve** | Low | Learning curve comparison needed | Learning curve comparison needed | Learning curve comparison needed |
| **Community Support** | Very High (Top 3 programming languages) | Community comparison needed | Community comparison needed | Community comparison needed |
| **Enterprise Features** | Enterprise feature analysis needed | Enterprise feature comparison needed | Enterprise feature comparison needed | Enterprise feature comparison needed |

#### **Decision Framework**
```mermaid
graph TD
    A[Requirements Analysis] --> B{Data Volume?}
    B -->|Small| C[Python]
    B -->|Medium| D[Consider Alternatives]
    B -->|Large| E[Distributed Solution]
    
    C --> F{Performance Needs?}
    D --> F
    E --> F
    
    F -->|High| G[Optimized Solution]
    F -->|Standard| H[Standard Solution]
```

#### **Use Case Scenarios**
- **Choose Python when:**
    - Data analysis and machine learning
  - Web development (Django, Flask)
  - Automation and scripting

- **Consider alternatives when:**
  Specific scenarios requiring alternatives

- **Avoid Python when:**
    - Global Interpreter Lock (GIL) limits threading
  - Slower execution compared to compiled languages



#### **Performance Benchmarks**
```
Benchmark Results (Industry Standard Dataset):
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Metric          │ Python │ Java       │ Scala       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Throughput      │ Benchmark needed │ Benchmark needed │ Benchmark needed │
│ Latency (p95)   │ Benchmark needed │ Benchmark needed │ Benchmark needed │
│ Memory Usage    │ High: 2-10x more than compiled languages │ Benchmark needed │ Benchmark needed │
│ CPU Utilization │ CPU utilization data needed │ CPU utilization data needed │ CPU utilization data needed │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```



#### **Cost Analysis**
```
Total Cost of Ownership (3-year projection):
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Cost Component  │ Python │ Java       │ Scala       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Licensing       │ $0 (Open Source) │ Cost analysis needed │ Cost analysis needed │
│ Infrastructure  │ Cost analysis needed │ Cost analysis needed │ Cost analysis needed │
│ Operations      │ Cost analysis needed │ Cost analysis needed │ Cost analysis needed │
│ Training        │ Low (easy to learn) │ Cost analysis needed │ Cost analysis needed │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ **TOTAL**       │ **Total cost calculation needed** │ **Total cost calculation needed** │ **Total cost calculation needed** │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```



### 🌍 **Real-World Applications**

#### **Industry Use Cases**
  - Data analysis and machine learning
  - Web development (Django, Flask)
  - Automation and scripting
  - Scientific computing
  - ETL and data pipelines

#### **Production Considerations**
Key considerations when deploying Python in production environments

#### **Case Studies**
Real-world case studies of Python implementations



### 🔮 **Future Trends & Evolution**

#### **Emerging Developments**
Latest developments in Python ecosystem

#### **Industry Direction**
Future direction of Programming Language technologies

#### **Skills Evolution Requirements**
Evolving skill requirements for Python professionals


### 📚 **Further Reading**
- [Official Python Documentation](#python-docs)
- [Performance Optimization Guide](#python-performance)
- [Best Practices and Patterns](#python-patterns)
- [Community Resources](#python-community)
- [Certification Paths](#python-certification)

### **Enhanced Answer**


**Python Memory Management Components:**

**1. Reference Counting (Primary Mechanism):**
- Every object has a reference count tracking how many variables point to it
- When count reaches zero, object is immediately deallocated
- Fast and deterministic for most objects
- Cannot handle circular references

**2. Cycle Detection (Garbage Collector):**
- Detects and cleans up circular references
- Runs periodically when allocation thresholds are reached
- Uses mark-and-sweep algorithm
- Can be manually triggered with `gc.collect()`

**3. Memory Pools (PyMalloc):**
- Optimizes allocation of small objects (<512 bytes)
- Reduces memory fragmentation
- Faster allocation/deallocation than system malloc
- Pools organized by object size

**4. Generational Garbage Collection:**
- Objects categorized into generations (0, 1, 2)
- Younger objects collected more frequently
- Based on observation that most objects die young
- Improves GC performance

**Why This Matters for Data Engineering:**
- **Large Datasets**: Understanding when objects are freed
- **Long-Running Processes**: Preventing memory leaks in pipelines
- **Performance Optimization**: Minimizing GC overhead
- **Resource Planning**: Predicting memory usage patterns

```python
import gc
import sys
import weakref
from typing import List, Any

# Demonstrate reference counting
def demonstrate_reference_counting():
    """Show how reference counting works."""
    print("=== Reference Counting Demo ===")
    
    # Create an object
    data = [1, 2, 3, 4, 5]
    print(f"Initial ref count: {sys.getrefcount(data)}")
    
    # Add references
    ref1 = data
    print(f"After ref1: {sys.getrefcount(data)}")
    
    ref2 = data
    print(f"After ref2: {sys.getrefcount(data)}")
    
    # Remove references
    del ref1
    print(f"After del ref1: {sys.getrefcount(data)}")
    
    del ref2
    print(f"After del ref2: {sys.getrefcount(data)}")
    
    # Object still exists because 'data' variable holds reference
    print(f"Data still exists: {data}")

# Demonstrate circular references
class Node:
    """Simple node class to create circular references."""
    def __init__(self, value):
        self.value = value
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        child.parent = self  # Creates circular reference
        self.children.append(child)
    
    def __del__(self):
        print(f"Node {self.value} is being deleted")

def demonstrate_circular_references():
    """Show circular reference handling."""
    print("\n=== Circular Reference Demo ===")
    
    # Create circular reference
    parent = Node("parent")
    child = Node("child")
    parent.add_child(child)
    
    print(f"Parent refs: {sys.getrefcount(parent)}")
    print(f"Child refs: {sys.getrefcount(child)}")
    
    # Remove our references
    parent_id = id(parent)
    child_id = id(child)
    
    del parent, child
    
    # Objects still exist due to circular reference
    print("Objects deleted from local scope, but circular reference remains")
    
    # Force garbage collection
    collected = gc.collect()
    print(f"Garbage collector collected {collected} objects")

# Memory usage monitoring
def monitor_memory_usage():
    """Monitor memory usage patterns."""
    print("\n=== Memory Usage Monitoring ===")
    
    # Get initial memory info
    initial_objects = len(gc.get_objects())
    print(f"Initial objects in memory: {initial_objects}")
    
    # Create many objects
    large_list = []
    for i in range(10000):
        large_list.append({'id': i, 'data': f'item_{i}', 'values': list(range(10))})
    
    after_creation = len(gc.get_objects())
    print(f"Objects after creation: {after_creation}")
    print(f"New objects created: {after_creation - initial_objects}")
    
    # Clear references
    del large_list
    
    # Check before GC
    before_gc = len(gc.get_objects())
    print(f"Objects before GC: {before_gc}")
    
    # Force garbage collection
    collected = gc.collect()
    after_gc = len(gc.get_objects())
    
    print(f"Objects collected: {collected}")
    print(f"Objects after GC: {after_gc}")
    print(f"Objects freed: {before_gc - after_gc}")

# Garbage collection configuration
def gc_configuration():
    """Show garbage collection configuration."""
    print("\n=== Garbage Collection Configuration ===")
    
    # Get current thresholds
    thresholds = gc.get_threshold()
    print(f"GC thresholds: {thresholds}")
    print("  Generation 0: {} allocations".format(thresholds[0]))
    print("  Generation 1: {} gen0 collections".format(thresholds[1]))
    print("  Generation 2: {} gen1 collections".format(thresholds[2]))
    
    # Get current counts
    counts = gc.get_count()
    print(f"Current counts: {counts}")
    
    # Get statistics
    stats = gc.get_stats()
    for i, stat in enumerate(stats):
        print(f"Generation {i}: {stat}")

# Memory optimization techniques
class MemoryOptimizedClass:
    """Example of memory optimization techniques."""
    
    # Use __slots__ to reduce memory overhead
    __slots__ = ['id', 'name', 'value']
    
    def __init__(self, id: int, name: str, value: float):
        self.id = id
        self.name = name
        self.value = value

class RegularClass:
    """Regular class without optimization."""
    
    def __init__(self, id: int, name: str, value: float):
        self.id = id
        self.name = name
        self.value = value

def compare_memory_usage():
    """Compare memory usage of different approaches."""
    print("\n=== Memory Optimization Comparison ===")
    
    # Create instances
    optimized = MemoryOptimizedClass(1, "test", 3.14)
    regular = RegularClass(1, "test", 3.14)
    
    # Compare memory usage
    print(f"Optimized class size: {sys.getsizeof(optimized)} bytes")
    print(f"Regular class size: {sys.getsizeof(regular)} bytes")
    
    # Show __dict__ difference
    print(f"Regular class has __dict__: {hasattr(regular, '__dict__')}")
    print(f"Optimized class has __dict__: {hasattr(optimized, '__dict__')}")
    
    if hasattr(regular, '__dict__'):
        print(f"__dict__ size: {sys.getsizeof(regular.__dict__)} bytes")

# Weak references to avoid circular references
def demonstrate_weak_references():
    """Show how weak references help avoid memory leaks."""
    print("\n=== Weak References Demo ===")
    
    class Parent:
        def __init__(self, name):
            self.name = name
            self.children = []
        
        def add_child(self, child):
            child.parent = weakref.ref(self)  # Weak reference
            self.children.append(child)
        
        def __del__(self):
            print(f"Parent {self.name} deleted")
    
    class Child:
        def __init__(self, name):
            self.name = name
            self.parent = None
        
        def get_parent(self):
            if self.parent is not None:
                return self.parent()  # Call weak reference
            return None
        
        def __del__(self):
            print(f"Child {self.name} deleted")
    
    # Create parent-child relationship
    parent = Parent("Alice")
    child = Child("Bob")
    parent.add_child(child)
    
    print(f"Child's parent: {child.get_parent().name if child.get_parent() else 'None'}")
    
    # Delete parent
    del parent
    
    # Child's parent reference is now None
    print(f"Child's parent after deletion: {child.get_parent()}")
    
    del child

# Practical memory management for data engineering
def data_processing_memory_tips():
    """Memory management tips for data processing."""
    print("\n=== Data Processing Memory Tips ===")
    
    # Tip 1: Use generators for large datasets
    def process_large_dataset_bad(size):
        """Memory-intensive approach."""
        data = [i**2 for i in range(size)]  # All in memory
        return sum(data)
    
    def process_large_dataset_good(size):
        """Memory-efficient approach."""
        return sum(i**2 for i in range(size))  # Generator
    
    # Tip 2: Delete large objects explicitly
    large_data = list(range(100000))
    print(f"Large data created: {len(large_data)} items")
    
    # Process data
    result = sum(large_data)
    
    # Explicitly delete when done
    del large_data
    print("Large data deleted explicitly")
    
    # Tip 3: Use context managers for resources
    class DataProcessor:
        def __init__(self):
            self.buffer = []
        
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.buffer.clear()  # Clean up
            print("Buffer cleared in __exit__")
        
        def process(self, data):
            self.buffer.extend(data)
            return len(self.buffer)
    
    # Use with context manager
    with DataProcessor() as processor:
        result = processor.process([1, 2, 3, 4, 5])
        print(f"Processed {result} items")
    # Buffer automatically cleared

if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_reference_counting()
    demonstrate_circular_references()
    monitor_memory_usage()
    gc_configuration()
    compare_memory_usage()
    demonstrate_weak_references()
    data_processing_memory_tips()
    
    print("\n=== Memory Management Best Practices ===")
    print("1. Use generators for large datasets")
    print("2. Delete large objects explicitly when done")
    print("3. Use weak references to avoid circular references")
    print("4. Use __slots__ for classes with many instances")
    print("5. Monitor memory usage in long-running processes")
    print("6. Use context managers for resource cleanup")
    print("7. Be aware of GC thresholds and tune if necessary")
```


### 3. What is the difference between `is` and `==`?
**Answer:**
Understanding the difference between `is` and `==` is fundamental for Python developers, especially when working with data structures and object comparisons in data engineering applications. This distinction affects performance, correctness, and debugging.


### 🎯 **Theoretical Foundation**

#### **Core Concepts**
  - Readable and maintainable syntax
  - Extensive library ecosystem
  - Strong data science/ML support

#### **Historical Context**
Evolution of Programming Language technologies leading to Python

#### **Architectural Principles**
Key architectural decisions in Python design

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying Python operations



### 📊 **Comparative Analysis**

#### **Technology Comparison Matrix**
| Feature | Python | Java | Scala | R |
|---------|---------------|--------|--------|--------|
| **Performance** | High performance characteristics | Comparative performance analysis needed | Comparative performance analysis needed | Comparative performance analysis needed |
| **Scalability** | Scalability characteristics | Scalability comparison needed | Scalability comparison needed | Scalability comparison needed |
| **Cost (TCO)** | $0 (Open Source) | Cost comparison needed | Cost comparison needed | Cost comparison needed |
| **Learning Curve** | Low | Learning curve comparison needed | Learning curve comparison needed | Learning curve comparison needed |
| **Community Support** | Very High (Top 3 programming languages) | Community comparison needed | Community comparison needed | Community comparison needed |
| **Enterprise Features** | Enterprise feature analysis needed | Enterprise feature comparison needed | Enterprise feature comparison needed | Enterprise feature comparison needed |

#### **Decision Framework**
```mermaid
graph TD
    A[Requirements Analysis] --> B{Data Volume?}
    B -->|Small| C[Python]
    B -->|Medium| D[Consider Alternatives]
    B -->|Large| E[Distributed Solution]
    
    C --> F{Performance Needs?}
    D --> F
    E --> F
    
    F -->|High| G[Optimized Solution]
    F -->|Standard| H[Standard Solution]
```

#### **Use Case Scenarios**
- **Choose Python when:**
    - Data analysis and machine learning
  - Web development (Django, Flask)
  - Automation and scripting

- **Consider alternatives when:**
  Specific scenarios requiring alternatives

- **Avoid Python when:**
    - Global Interpreter Lock (GIL) limits threading
  - Slower execution compared to compiled languages



#### **Performance Benchmarks**
```
Benchmark Results (Industry Standard Dataset):
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Metric          │ Python │ Java       │ Scala       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Throughput      │ Benchmark needed │ Benchmark needed │ Benchmark needed │
│ Latency (p95)   │ Benchmark needed │ Benchmark needed │ Benchmark needed │
│ Memory Usage    │ High: 2-10x more than compiled languages │ Benchmark needed │ Benchmark needed │
│ CPU Utilization │ CPU utilization data needed │ CPU utilization data needed │ CPU utilization data needed │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```



#### **Cost Analysis**
```
Total Cost of Ownership (3-year projection):
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Cost Component  │ Python │ Java       │ Scala       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Licensing       │ $0 (Open Source) │ Cost analysis needed │ Cost analysis needed │
│ Infrastructure  │ Cost analysis needed │ Cost analysis needed │ Cost analysis needed │
│ Operations      │ Cost analysis needed │ Cost analysis needed │ Cost analysis needed │
│ Training        │ Low (easy to learn) │ Cost analysis needed │ Cost analysis needed │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ **TOTAL**       │ **Total cost calculation needed** │ **Total cost calculation needed** │ **Total cost calculation needed** │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```



### 🌍 **Real-World Applications**

#### **Industry Use Cases**
  - Data analysis and machine learning
  - Web development (Django, Flask)
  - Automation and scripting
  - Scientific computing
  - ETL and data pipelines

#### **Production Considerations**
Key considerations when deploying Python in production environments

#### **Case Studies**
Real-world case studies of Python implementations



### 🔮 **Future Trends & Evolution**

#### **Emerging Developments**
Latest developments in Python ecosystem

#### **Industry Direction**
Future direction of Programming Language technologies

#### **Skills Evolution Requirements**
Evolving skill requirements for Python professionals


### 📚 **Further Reading**
- [Official Python Documentation](#python-docs)
- [Performance Optimization Guide](#python-performance)
- [Best Practices and Patterns](#python-patterns)
- [Community Resources](#python-community)
- [Certification Paths](#python-certification)

### **Enhanced Answer**


**Key Differences:**

**`==` (Equality Operator):**
- Compares **values** of objects
- Calls the `__eq__()` method
- Can be overridden in custom classes
- Used for logical equality
- May involve computation

**`is` (Identity Operator):**
- Compares **object identity** (memory location)
- Uses `id()` function internally
- Cannot be overridden
- Faster than `==` (simple pointer comparison)
- Used for checking if two variables reference the same object

**When to Use Each:**
- **`==`**: Comparing values, data content, logical equality
- **`is`**: Checking for None, singleton objects, same object reference

**Python Object Interning:**
Python interns (caches) certain objects for efficiency:
- Small integers (-5 to 256)
- Short strings without special characters
- Empty collections (tuples, frozensets)

**Common Pitfalls:**
- Using `is` instead of `==` for value comparison
- Assuming `is` behavior for all objects
- Not understanding object interning

```python
# Basic comparison examples
def basic_comparison_examples():
    """Demonstrate basic is vs == behavior."""
    print("=== Basic Comparison Examples ===")
    
    # Lists with same content
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a  # Same object reference
    
    print(f"a = {a}, id(a) = {id(a)}")
    print(f"b = {b}, id(b) = {id(b)}")
    print(f"c = {c}, id(c) = {id(c)}")
    
    print(f"a == b: {a == b}")  # True (same values)
    print(f"a is b: {a is b}")  # False (different objects)
    print(f"a == c: {a == c}")  # True (same values)
    print(f"a is c: {a is c}")  # True (same object)

# Python object interning examples
def interning_examples():
    """Show Python's object interning behavior."""
    print("\n=== Object Interning Examples ===")
    
    # Small integers are interned
    x = 100
    y = 100
    print(f"x = {x}, y = {y}")
    print(f"x == y: {x == y}")  # True
    print(f"x is y: {x is y}")  # True (interned)
    
    # Large integers are not interned
    x = 1000
    y = 1000
    print(f"\nx = {x}, y = {y}")
    print(f"x == y: {x == y}")  # True
    print(f"x is y: {x is y}")  # May be False (not guaranteed to be interned)
    
    # String interning
    s1 = "hello"
    s2 = "hello"
    print(f"\ns1 = '{s1}', s2 = '{s2}'")
    print(f"s1 == s2: {s1 == s2}")  # True
    print(f"s1 is s2: {s1 is s2}")  # True (interned)
    
    # Strings with spaces may not be interned
    s3 = "hello world"
    s4 = "hello world"
    print(f"\ns3 = '{s3}', s4 = '{s4}'")
    print(f"s3 == s4: {s3 == s4}")  # True
    print(f"s3 is s4: {s3 is s4}")  # May be False

# None comparison (always use 'is')
def none_comparison():
    """Demonstrate proper None comparison."""
    print("\n=== None Comparison ===")
    
    value = None
    
    # Correct way to check for None
    if value is None:
        print("Value is None (correct)")
    
    # Incorrect but works (don't do this)
    if value == None:
        print("Value equals None (works but incorrect style)")
    
    # Why 'is' is preferred for None
    print(f"None == None: {None == None}")  # True
    print(f"None is None: {None is None}")  # True
    print(f"Performance: 'is' is faster than '=='")

# Custom class with __eq__ override
class DataRecord:
    """Example class showing custom equality."""
    
    def __init__(self, id: int, data: str):
        self.id = id
        self.data = data
    
    def __eq__(self, other):
        """Custom equality based on ID only."""
        if not isinstance(other, DataRecord):
            return False
        return self.id == other.id
    
    def __repr__(self):
        return f"DataRecord(id={self.id}, data='{self.data}')"

def custom_equality_example():
    """Show custom equality behavior."""
    print("\n=== Custom Equality Example ===")
    
    record1 = DataRecord(1, "first")
    record2 = DataRecord(1, "second")  # Same ID, different data
    record3 = record1  # Same object
    
    print(f"record1: {record1}")
    print(f"record2: {record2}")
    print(f"record3: {record3}")
    
    print(f"\nrecord1 == record2: {record1 == record2}")  # True (same ID)
    print(f"record1 is record2: {record1 is record2}")    # False (different objects)
    print(f"record1 == record3: {record1 == record3}")    # True (same ID)
    print(f"record1 is record3: {record1 is record3}")    # True (same object)

# Performance comparison
def performance_comparison():
    """Compare performance of is vs ==."""
    print("\n=== Performance Comparison ===")
    
    import time
    
    # Create objects for testing
    obj1 = [1, 2, 3] * 1000
    obj2 = obj1  # Same object
    obj3 = [1, 2, 3] * 1000  # Different object, same content
    
    iterations = 100000
    
    # Test 'is' performance (same object)
    start = time.time()
    for _ in range(iterations):
        result = obj1 is obj2
    is_time = time.time() - start
    
    # Test '==' performance (same object)
    start = time.time()
    for _ in range(iterations):
        result = obj1 == obj2
    eq_time_same = time.time() - start
    
    # Test '==' performance (different objects, same content)
    start = time.time()
    for _ in range(iterations):
        result = obj1 == obj3
    eq_time_diff = time.time() - start
    
    print(f"'is' comparison time: {is_time:.6f}s")
    print(f"'==' comparison (same object): {eq_time_same:.6f}s")
    print(f"'==' comparison (different objects): {eq_time_diff:.6f}s")
    print(f"'is' is {eq_time_diff/is_time:.1f}x faster than '==' for different objects")

# Common mistakes and best practices
def common_mistakes():
    """Show common mistakes and best practices."""
    print("\n=== Common Mistakes and Best Practices ===")
    
    # Mistake 1: Using 'is' for value comparison
    def check_status_wrong(status):
        if status is "active":  # Wrong!
            return True
        return False
    
    def check_status_correct(status):
        if status == "active":  # Correct!
            return True
        return False
    
    # Mistake 2: Not using 'is' for None checks
    def process_data_wrong(data):
        if data == None:  # Works but not recommended
            return "No data"
        return f"Processing {len(data)} items"
    
    def process_data_correct(data):
        if data is None:  # Correct and faster
            return "No data"
        return f"Processing {len(data)} items"
    
    # Mistake 3: Assuming 'is' behavior for mutable objects
    def create_default_list_wrong(items=None):
        if items is []:  # Wrong! [] creates new object each time
            items = []
        return items
    
    def create_default_list_correct(items=None):
        if items is None:  # Correct!
            items = []
        return items
    
    print("Best Practices:")
    print("1. Use 'is' for None, True, False comparisons")
    print("2. Use '==' for value comparisons")
    print("3. Use 'is' when checking object identity matters")
    print("4. Be aware of object interning behavior")
    print("5. Use 'is' for performance when comparing to singletons")

# Data engineering specific examples
def data_engineering_examples():
    """Examples relevant to data engineering."""
    print("\n=== Data Engineering Examples ===")
    
    # Example 1: Checking for sentinel values
    MISSING_VALUE = object()  # Unique sentinel object
    
    def process_record(record):
        for key, value in record.items():
            if value is MISSING_VALUE:  # Use 'is' for sentinel
                print(f"Missing value for {key}")
            elif value == "":
                print(f"Empty string for {key}")
            else:
                print(f"{key}: {value}")
    
    # Example 2: Caching and object reuse
    class DataCache:
        def __init__(self):
            self._cache = {}
        
        def get_data(self, key):
            if key in self._cache:
                cached_data = self._cache[key]
                # Check if it's the same object (not just equal content)
                if cached_data is not None:
                    return cached_data
            return None
        
        def set_data(self, key, data):
            self._cache[key] = data
    
    # Example 3: Configuration object comparison
    class Config:
        _instance = None
        
        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
    
    config1 = Config()
    config2 = Config()
    
    print(f"config1 is config2: {config1 is config2}")  # True (singleton)
    print(f"config1 == config2: {config1 == config2}")  # True

if __name__ == "__main__":
    basic_comparison_examples()
    interning_examples()
    none_comparison()
    custom_equality_example()
    performance_comparison()
    common_mistakes()
    data_engineering_examples()
    
    print("\n=== Summary ===")
    print("• Use '==' to compare values")
    print("• Use 'is' to compare object identity")
    print("• Always use 'is' for None, True, False")
    print("• 'is' is faster than '==' for identity checks")
    print("• Be aware of Python's object interning")
    print("• Custom classes can override '==' but not 'is'")
```


### 4. What are the key differences between lists and tuples in Python?

**Answer:**
Lists and tuples are both sequence types in Python, but they serve different purposes and have distinct characteristics that make them suitable for different use cases in data engineering applications.

**Key Differences:**

**Mutability:**
- **Lists**: Mutable - can be modified after creation (add, remove, change elements)
- **Tuples**: Immutable - cannot be changed after creation
- **Impact**: Lists for dynamic data that changes, tuples for fixed data structures

**Performance:**
- **Tuples**: Faster for iteration, indexing, and creation
- **Lists**: Slightly slower due to mutability overhead
- **Memory**: Tuples use less memory due to immutability optimizations

**Use Cases:**
- **Lists**: Dynamic collections, data that needs modification, stacks, queues
- **Tuples**: Coordinates, database records, function return values, dictionary keys
- **Data Engineering**: Tuples for schema definitions, lists for data processing

**Hashability:**
- **Tuples**: Hashable (can be dictionary keys or set elements) if all elements are hashable
- **Lists**: Not hashable (cannot be dictionary keys)

**Methods Available:**
- **Lists**: Many methods (append, extend, remove, pop, sort, etc.)
- **Tuples**: Limited methods (count, index)

**When to Use Each:**
- **Lists**: When you need to modify the collection during program execution
- **Tuples**: When you have a fixed collection that won't change

```python
import sys
import time

# Basic examples
my_list = [1, 2, 3]
my_tuple = (1, 2, 3)

# Mutability demonstration
print("=== Mutability ===")
my_list.append(4)  # Works
print(f"List after append: {my_list}")
# Output: List after append: [1, 2, 3, 4]

my_list[0] = 'changed'
print(f"List after modification: {my_list}")
# Output: List after modification: ['changed', 2, 3, 4]

print(f"Tuple: {my_tuple}")
# my_tuple.append(4)  # Error - tuples are immutable
# my_tuple[0] = 'changed'  # Error - cannot modify
# Output: Tuple: (1, 2, 3)

# Memory usage comparison
print("\n=== Memory Usage ===")
list_data = [i for i in range(1000)]
tuple_data = tuple(i for i in range(1000))

print(f"List memory: {sys.getsizeof(list_data)} bytes")
print(f"Tuple memory: {sys.getsizeof(tuple_data)} bytes")
print(f"Memory savings with tuple: {sys.getsizeof(list_data) - sys.getsizeof(tuple_data)} bytes")

# Performance comparison
print("\n=== Performance Comparison ===")
data = list(range(10000))

# List creation time
start = time.time()
for _ in range(1000):
    test_list = [1, 2, 3, 4, 5]
list_time = time.time() - start

# Tuple creation time
start = time.time()
for _ in range(1000):
    test_tuple = (1, 2, 3, 4, 5)
tuple_time = time.time() - start

print(f"List creation time: {list_time:.6f}s")
print(f"Tuple creation time: {tuple_time:.6f}s")
print(f"Tuple is {list_time/tuple_time:.2f}x faster to create")

# Iteration performance
test_list = list(range(10000))
test_tuple = tuple(range(10000))

start = time.time()
for item in test_list:
    pass
list_iter_time = time.time() - start

start = time.time()
for item in test_tuple:
    pass
tuple_iter_time = time.time() - start

print(f"List iteration time: {list_iter_time:.6f}s")
print(f"Tuple iteration time: {tuple_iter_time:.6f}s")

# Hashability demonstration
print("\n=== Hashability ===")
try:
    # Tuples can be dictionary keys
    coordinate_dict = {(0, 0): 'origin', (1, 1): 'point1'}
    print(f"Tuple as dict key works: {coordinate_dict}")
except TypeError as e:
    print(f"Tuple as dict key failed: {e}")

try:
    # Lists cannot be dictionary keys
    list_dict = {[0, 0]: 'origin'}  # This will fail
except TypeError as e:
    print(f"List as dict key failed: {e}")

# Practical data engineering examples
print("\n=== Data Engineering Use Cases ===")

# Tuple for database record (immutable structure)
user_record = ('john_doe', 'john@example.com', 25, 'active')
print(f"Database record (tuple): {user_record}")

# List for data processing (mutable collection)
data_batch = [100, 200, 300, 400, 500]
print(f"Original batch: {data_batch}")

# Process data (modify list)
processed_batch = []
for value in data_batch:
    if value > 250:
        processed_batch.append(value * 1.1)  # Apply 10% increase
    else:
        processed_batch.append(value)

print(f"Processed batch: {processed_batch}")

# Tuple for function return (multiple values)
def get_statistics(data):
    """Return statistics as tuple (immutable result)."""
    return (min(data), max(data), sum(data)/len(data))

stats = get_statistics(data_batch)
min_val, max_val, avg_val = stats  # Tuple unpacking
print(f"Statistics (min, max, avg): {stats}")

# Named tuples for structured data
from collections import namedtuple

DataPoint = namedtuple('DataPoint', ['timestamp', 'value', 'source'])
data_point = DataPoint('2023-01-01', 42.5, 'sensor_1')
print(f"Named tuple: {data_point}")
print(f"Access by name: {data_point.timestamp}, {data_point.value}")

# List methods vs tuple methods
print("\n=== Available Methods ===")
print(f"List methods: {[method for method in dir(list) if not method.startswith('_')]}")
print(f"Tuple methods: {[method for method in dir(tuple) if not method.startswith('_')]}")

# Conversion between list and tuple
print("\n=== Conversion ===")
original_list = [1, 2, 3, 4, 5]
converted_tuple = tuple(original_list)
back_to_list = list(converted_tuple)

print(f"Original list: {original_list}")
print(f"Converted to tuple: {converted_tuple}")
print(f"Back to list: {back_to_list}")
```

### 5. Explain list comprehensions vs generator expressions.

**Answer:**
List comprehensions and generator expressions are both concise ways to create sequences in Python, but they differ significantly in memory usage and evaluation strategy. Understanding this difference is crucial for data engineering when processing large datasets that may not fit in memory.

**Key Differences:**

**Evaluation Strategy:**
- **List Comprehensions**: Eager evaluation - create entire list in memory immediately
- **Generator Expressions**: Lazy evaluation - create iterator that yields items on-demand
- **Syntax**: Lists use `[]`, generators use `()`

**Memory Usage:**
- **List Comprehensions**: Memory usage grows with data size (O(n) space)
- **Generator Expressions**: Constant memory usage regardless of size (O(1) space)
- **Impact**: Generators can handle datasets larger than available RAM

**Performance Characteristics:**
- **Lists**: Faster for small datasets, support random access, can be iterated multiple times
- **Generators**: Better for large datasets, sequential access only, consumed once
- **Creation Speed**: Generators are faster to create (no immediate computation)

**When to Use Each:**
- **List Comprehensions**: Small datasets, need random access, multiple iterations, need len()
- **Generator Expressions**: Large datasets, memory constraints, single iteration, streaming data
- **Data Engineering**: Generators for ETL pipelines, lists for small lookup tables

**Advanced Concepts:**
- **Generator Chaining**: Combine multiple generators for complex pipelines
- **Memory Profiling**: Monitor memory usage to choose appropriate approach
- **Hybrid Approaches**: Use generators with batching for balanced performance

```python
import sys
import time
import tracemalloc
from typing import Iterator, List

# Basic syntax comparison
print("=== Basic Syntax ===")
# List comprehension - creates list in memory
squares_list = [x**2 for x in range(10)]
print(f"List comprehension: {squares_list}")
print(f"Type: {type(squares_list)}")

# Generator expression - lazy evaluation
squares_gen = (x**2 for x in range(10))
print(f"Generator expression: {squares_gen}")
print(f"Type: {type(squares_gen)}")
print(f"Generator content: {list(squares_gen)}")

# Memory usage comparison
print("\n=== Memory Usage Comparison ===")
small_list = [x for x in range(1000)]
small_gen = (x for x in range(1000))

print(f"Small list (1000 items): {sys.getsizeof(small_list)} bytes")
print(f"Small generator: {sys.getsizeof(small_gen)} bytes")

# Large dataset memory comparison
large_list = [x for x in range(100000)]
large_gen = (x for x in range(100000))

print(f"Large list (100k items): {sys.getsizeof(large_list)} bytes")
print(f"Large generator: {sys.getsizeof(large_gen)} bytes")
print(f"Memory savings: {sys.getsizeof(large_list) - sys.getsizeof(large_gen)} bytes")

# Performance comparison
print("\n=== Performance Comparison ===")

def time_creation(description, creation_func, iterations=1000):
    """Time the creation of data structures."""
    start = time.time()
    for _ in range(iterations):
        result = creation_func()
    end = time.time()
    print(f"{description}: {(end - start) * 1000:.2f}ms for {iterations} iterations")
    return result

# Compare creation times
time_creation("List comprehension", lambda: [x**2 for x in range(1000)])
time_creation("Generator expression", lambda: (x**2 for x in range(1000)))

# Memory profiling example
print("\n=== Memory Profiling ===")

def memory_intensive_list_processing():
    """Process data using list comprehension."""
    # Create large list in memory
    data = [x**2 for x in range(500000)]
    # Process data
    filtered = [x for x in data if x % 2 == 0]
    return sum(filtered)

def memory_efficient_generator_processing():
    """Process data using generator expressions."""
    # Create generator (no memory allocation)
    data = (x**2 for x in range(500000))
    # Chain generators for processing
    filtered = (x for x in data if x % 2 == 0)
    return sum(filtered)

# Profile memory usage
tracemalloc.start()

# List approach
snapshot1 = tracemalloc.take_snapshot()
result1 = memory_intensive_list_processing()
snapshot2 = tracemalloc.take_snapshot()

# Generator approach
snapshot3 = tracemalloc.take_snapshot()
result2 = memory_efficient_generator_processing()
snapshot4 = tracemalloc.take_snapshot()

# Calculate memory differences
list_memory = sum(stat.size for stat in snapshot2.statistics('lineno')) - sum(stat.size for stat in snapshot1.statistics('lineno'))
gen_memory = sum(stat.size for stat in snapshot4.statistics('lineno')) - sum(stat.size for stat in snapshot3.statistics('lineno'))

print(f"List approach memory: {list_memory / 1024 / 1024:.2f} MB")
print(f"Generator approach memory: {gen_memory / 1024 / 1024:.2f} MB")
print(f"Results match: {result1 == result2}")

tracemalloc.stop()

# Reusability demonstration
print("\n=== Reusability ===")
data_list = [1, 2, 3, 4, 5]
data_gen = (x for x in [1, 2, 3, 4, 5])

print("List (multiple iterations):")
print(f"First iteration: {list(data_list)}")
print(f"Second iteration: {list(data_list)}")
print(f"List length: {len(data_list)}")

print("\nGenerator (single use):")
print(f"First iteration: {list(data_gen)}")
print(f"Second iteration: {list(data_gen)}")
# print(f"Generator length: {len(data_gen)}")  # Error - generators don't have len()

# Practical data engineering examples
print("\n=== Data Engineering Use Cases ===")

# Example 1: Processing large CSV file
def process_csv_with_list(filename):
    """Memory-intensive approach using list comprehension."""
    # This would load entire file into memory
    with open(filename, 'r') as f:
        lines = [line.strip().split(',') for line in f]  # All in memory
    
    # Process all data
    processed = [row for row in lines if len(row) > 2]
    return processed

def process_csv_with_generator(filename):
    """Memory-efficient approach using generator."""
    # Generator that processes one line at a time
    def line_generator():
        with open(filename, 'r') as f:
            for line in f:
                yield line.strip().split(',')
    
    # Chain generators for processing
    processed = (row for row in line_generator() if len(row) > 2)
    return processed

# Example 2: Data transformation pipeline
def create_data_pipeline(data_source: Iterator) -> Iterator:
    """Create a memory-efficient data processing pipeline."""
    # Stage 1: Filter valid records
    valid_records = (record for record in data_source if record.get('valid', True))
    
    # Stage 2: Transform data
    transformed = (
        {
            'id': record['id'],
            'value': record['value'] * 2,
            'category': record.get('category', 'unknown').upper()
        }
        for record in valid_records
    )
    
    # Stage 3: Filter by value threshold
    filtered = (record for record in transformed if record['value'] > 100)
    
    return filtered

# Example usage of pipeline
sample_data = [
    {'id': 1, 'value': 50, 'category': 'a', 'valid': True},
    {'id': 2, 'value': 75, 'category': 'b', 'valid': True},
    {'id': 3, 'value': 25, 'category': 'c', 'valid': False},
    {'id': 4, 'value': 100, 'category': 'd', 'valid': True}
]

print("Data pipeline with generators:")
pipeline = create_data_pipeline(iter(sample_data))
for processed_record in pipeline:
    print(f"  Processed: {processed_record}")

# Example 3: Batch processing with generators
def batch_generator(iterable: Iterator, batch_size: int) -> Iterator[List]:
    """Create batches from an iterable using generators."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    # Yield remaining items
    if batch:
        yield batch

print("\nBatch processing:")
large_dataset = (x for x in range(25))  # Simulate large dataset
for i, batch in enumerate(batch_generator(large_dataset, batch_size=7)):
    print(f"  Batch {i+1}: {batch}")

# Example 4: Infinite generators
def fibonacci_generator():
    """Generate Fibonacci sequence infinitely."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def take(n: int, iterable: Iterator) -> List:
    """Take first n items from an iterator."""
    return [next(iterable) for _ in range(n)]

print("\nInfinite generator (Fibonacci):")
fib = fibonacci_generator()
first_10 = take(10, fib)
print(f"First 10 Fibonacci numbers: {first_10}")

# Performance comparison for different scenarios
print("\n=== Scenario-Based Performance ===")

# Scenario 1: Small dataset, multiple access
small_data = range(100)
print("Small dataset (100 items):")

# List - good for multiple access
start = time.time()
small_list = [x**2 for x in small_data]
for _ in range(10):
    total = sum(small_list)
list_time = time.time() - start

# Generator - recreated each time
start = time.time()
for _ in range(10):
    small_gen = (x**2 for x in small_data)
    total = sum(small_gen)
gen_time = time.time() - start

print(f"  List (multiple access): {list_time:.6f}s")
print(f"  Generator (recreated): {gen_time:.6f}s")
print(f"  List is {gen_time/list_time:.1f}x faster for multiple access")

# Scenario 2: Large dataset, single access
large_data = range(1000000)
print("\nLarge dataset (1M items):")

# List - memory intensive
start = time.time()
large_list = [x**2 for x in large_data if x % 2 == 0]
total = sum(large_list)
list_time = time.time() - start

# Generator - memory efficient
start = time.time()
large_gen = (x**2 for x in large_data if x % 2 == 0)
total = sum(large_gen)
gen_time = time.time() - start

print(f"  List (all in memory): {list_time:.6f}s")
print(f"  Generator (streaming): {gen_time:.6f}s")
print(f"  Generator is {list_time/gen_time:.1f}x faster for single pass")

# Best practices summary
print("\n=== Best Practices Summary ===")
print("Use LIST COMPREHENSIONS when:")
print("  • Dataset is small (< 10k items)")
print("  • Need random access (indexing)")
print("  • Multiple iterations required")
print("  • Need len() or other list methods")
print("  • Memory usage is not a concern")

print("\nUse GENERATOR EXPRESSIONS when:")
print("  • Dataset is large (> 100k items)")
print("  • Memory is limited")
print("  • Single iteration (streaming)")
print("  • Building data pipelines")
print("  • Processing files line by line")
print("  • Infinite sequences")
```

## 🟡 Intermediate

### 6. What are decorators and how do they work?

**Answer:**
Decorators are a powerful Python feature that allows you to modify or extend the behavior of functions or classes without permanently modifying their code. They implement the decorator pattern and are essentially functions that take another function as input and return a modified version.

**How Decorators Work:**
- **Wrapper Functions**: Decorators wrap the original function with additional functionality
- **@ Syntax**: Syntactic sugar for applying decorators cleanly
- **Function Composition**: Chain multiple decorators for complex behavior
- **Metadata Preservation**: Use `functools.wraps` to maintain original function information

**Common Use Cases in Data Engineering:**
- **Logging**: Track function calls and execution times
- **Caching**: Store expensive computation results
- **Retry Logic**: Automatically retry failed operations
- **Authentication**: Verify user permissions before execution
- **Rate Limiting**: Control API call frequency
- **Data Validation**: Validate inputs and outputs
- **Performance Monitoring**: Measure and log performance metrics

**Types of Decorators:**
- **Function Decorators**: Modify function behavior
- **Class Decorators**: Modify class behavior
- **Property Decorators**: Create computed properties
- **Static/Class Method Decorators**: Define method types

**Advanced Concepts:**
- **Decorator Factories**: Decorators that accept parameters
- **Class-based Decorators**: Using classes as decorators
- **Decorator Chaining**: Applying multiple decorators
- **Conditional Decorators**: Apply decorators based on conditions

```python
import time
import functools
import logging
from typing import Callable, Any, Dict
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic decorator example
def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    @functools.wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    """A function that takes some time to execute."""
    time.sleep(1)
    return "Done"

# Decorator with parameters (decorator factory)
def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Decorator factory for retry logic with configurable parameters."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"Max attempts ({max_attempts}) reached for {func.__name__}")
                        raise e
                    
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def unreliable_function():
    """Function that might fail randomly."""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Random connection failure")
    return "Success!"

# Caching decorator
def cache_results(max_size: int = 128):
    """Simple caching decorator with size limit."""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                print(f"Cache hit for {func.__name__}")
                return cache[key]
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            
            # Implement simple LRU by removing oldest if cache is full
            if len(cache) >= max_size:
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            cache[key] = result
            print(f"Cache miss for {func.__name__}, result cached")
            return result
        
        # Add cache inspection methods
        wrapper.cache_info = lambda: {'size': len(cache), 'max_size': max_size}
        wrapper.cache_clear = lambda: cache.clear()
        
        return wrapper
    return decorator

@cache_results(max_size=10)
def expensive_calculation(n: int) -> int:
    """Simulate expensive computation."""
    print(f"Computing factorial of {n}...")
    time.sleep(0.1)  # Simulate work
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Logging decorator
def log_calls(include_args: bool = True, include_result: bool = False):
    """Decorator to log function calls with configurable detail level."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log function entry
            log_msg = f"Calling {func.__name__}"
            if include_args:
                log_msg += f" with args={args}, kwargs={kwargs}"
            logger.info(log_msg)
            
            try:
                result = func(*args, **kwargs)
                
                # Log successful completion
                success_msg = f"Completed {func.__name__}"
                if include_result:
                    success_msg += f" -> {result}"
                logger.info(success_msg)
                
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                raise
        
        return wrapper
    return decorator

@log_calls(include_args=True, include_result=True)
def process_data(data: list, multiplier: int = 2) -> list:
    """Process data with logging."""
    return [x * multiplier for x in data]

# Class-based decorator
class RateLimiter:
    """Class-based decorator for rate limiting."""
    
    def __init__(self, max_calls: int, time_window: float):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove old calls outside time window
            self.calls = [call_time for call_time in self.calls 
                         if now - call_time < self.time_window]
            
            # Check rate limit
            if len(self.calls) >= self.max_calls:
                raise Exception(f"Rate limit exceeded: {self.max_calls} calls per {self.time_window}s")
            
            # Record this call
            self.calls.append(now)
            
            return func(*args, **kwargs)
        
        return wrapper

@RateLimiter(max_calls=3, time_window=10.0)
def api_call(endpoint: str) -> dict:
    """Simulate API call with rate limiting."""
    print(f"Making API call to {endpoint}")
    return {"status": "success", "endpoint": endpoint}

# Data validation decorator
def validate_types(**type_hints):
    """Decorator to validate function argument types."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate types
            for param_name, expected_type in type_hints.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Parameter '{param_name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(data=list, threshold=int)
def filter_data(data: list, threshold: int) -> list:
    """Filter data above threshold with type validation."""
    return [x for x in data if x > threshold]

# Performance monitoring decorator
class PerformanceMonitor:
    """Decorator class for comprehensive performance monitoring."""
    
    def __init__(self):
        self.stats: Dict[str, list] = {}
    
    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = self._get_memory_usage()
            
            try:
                result = func(*args, **kwargs)
                success = True
                error = None
            except Exception as e:
                success = False
                error = str(e)
                raise
            finally:
                end_time = time.time()
                end_memory = self._get_memory_usage()
                
                # Record performance metrics
                execution_time = end_time - start_time
                memory_delta = end_memory - start_memory
                
                if func.__name__ not in self.stats:
                    self.stats[func.__name__] = []
                
                self.stats[func.__name__].append({
                    'timestamp': datetime.now().isoformat(),
                    'execution_time': execution_time,
                    'memory_delta': memory_delta,
                    'success': success,
                    'error': error
                })
            
            return result
        
        return wrapper
    
    def _get_memory_usage(self) -> int:
        """Get current memory usage (simplified)."""
        import psutil
        import os
        process = psutil.Process(os.getpid())
        return process.memory_info().rss
    
    def get_stats(self, func_name: str = None) -> dict:
        """Get performance statistics."""
        if func_name:
            return self.stats.get(func_name, [])
        return self.stats
    
    def print_summary(self):
        """Print performance summary."""
        for func_name, calls in self.stats.items():
            successful_calls = [call for call in calls if call['success']]
            if successful_calls:
                avg_time = sum(call['execution_time'] for call in successful_calls) / len(successful_calls)
                print(f"{func_name}: {len(successful_calls)} calls, avg time: {avg_time:.4f}s")

# Usage examples
if __name__ == "__main__":
    # Performance monitoring
    monitor = PerformanceMonitor()
    
    @monitor
    def data_processing_task(size: int) -> list:
        """Simulate data processing."""
        return [i ** 2 for i in range(size)]
    
    # Test decorators
    print("=== Testing Decorators ===")
    
    # Test timing decorator
    print("\n1. Timing Decorator:")
    result = slow_function()
    print(f"Result: {result}")
    
    # Test retry decorator
    print("\n2. Retry Decorator:")
    try:
        result = unreliable_function()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Final failure: {e}")
    
    # Test caching decorator
    print("\n3. Caching Decorator:")
    print(expensive_calculation(5))  # Cache miss
    print(expensive_calculation(5))  # Cache hit
    print(expensive_calculation(6))  # Cache miss
    print(f"Cache info: {expensive_calculation.cache_info()}")
    
    # Test logging decorator
    print("\n4. Logging Decorator:")
    result = process_data([1, 2, 3, 4], multiplier=3)
    
    # Test rate limiter
    print("\n5. Rate Limiter:")
    try:
        for i in range(5):
            api_call(f"endpoint_{i}")
    except Exception as e:
        print(f"Rate limit error: {e}")
    
    # Test type validation
    print("\n6. Type Validation:")
    try:
        result = filter_data([1, 2, 3, 4, 5], 3)
        print(f"Filtered data: {result}")
        
        # This will raise TypeError
        filter_data("not a list", 3)
    except TypeError as e:
        print(f"Type validation error: {e}")
    
    # Test performance monitoring
    print("\n7. Performance Monitoring:")
    data_processing_task(1000)
    data_processing_task(5000)
    monitor.print_summary()
    
    print("\n=== Decorator Chaining Example ===")
    
    @timing_decorator
    @log_calls(include_result=False)
    @cache_results(max_size=5)
    def complex_calculation(n: int) -> int:
        """Function with multiple decorators applied."""
        time.sleep(0.1)
        return sum(i ** 2 for i in range(n))
    
    # Test chained decorators
    result1 = complex_calculation(10)  # All decorators active
    result2 = complex_calculation(10)  # Should hit cache
    
    print(f"\nResults: {result1}, {result2}")
```

### 7. Explain the difference between `*args` and `**kwargs`.
**Answer:**
`*args` and `**kwargs` are special syntax in Python that allow functions to accept variable numbers of arguments. This is essential for creating flexible APIs and wrapper functions in data engineering applications.

**Key Concepts:**
- **`*args`**: Collects extra positional arguments into a tuple
- **`**kwargs`**: Collects extra keyword arguments into a dictionary
- **Unpacking**: Can also be used to unpack sequences and dictionaries when calling functions
- **Order**: Parameters must be in order: regular args, `*args`, keyword args, `**kwargs`

**Common Use Cases:**
- **Wrapper Functions**: Decorators that need to pass through all arguments
- **API Design**: Functions that accept flexible parameters
- **Function Composition**: Combining multiple functions with different signatures
- **Configuration**: Passing configuration options dynamically

```python
# Basic usage
def example_function(*args, **kwargs):
    print("args:", args)      # Tuple of positional arguments
    print("kwargs:", kwargs)  # Dictionary of keyword arguments

example_function(1, 2, 3, name="John", age=30)
# Output: args: (1, 2, 3)
# Output: kwargs: {'name': 'John', 'age': 30}

# Practical example: Flexible data processing function
def process_data(data, *transformations, **options):
    """Process data with variable transformations and options."""
    result = data
    
    # Apply all transformation functions
    for transform in transformations:
        result = transform(result)
    
    # Apply options
    if options.get('sort', False):
        result = sorted(result)
    if options.get('unique', False):
        result = list(set(result))
    
    return result

# Usage
def double(x): return [i*2 for i in x]
def filter_even(x): return [i for i in x if i % 2 == 0]

data = [1, 2, 3, 4, 5]
result = process_data(data, double, filter_even, sort=True, unique=True)
print(result)  # [2, 4, 6, 8, 10]

# Unpacking examples
args_tuple = (1, 2, 3)
kwargs_dict = {'name': 'Alice', 'age': 25}

example_function(*args_tuple, **kwargs_dict)
# Same as: example_function(1, 2, 3, name='Alice', age=25)
```

### 8. What is the Global Interpreter Lock (GIL)?
**Answer:**
The Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes simultaneously. This is one of the most important concepts to understand for Python performance optimization.

**Key Points:**
- **Definition**: A mutex that prevents multiple threads from executing Python code simultaneously
- **Impact**: Limits true parallelism in CPU-bound tasks but doesn't affect I/O-bound tasks
- **Why it exists**: Simplifies memory management and prevents race conditions in CPython's reference counting
- **Workarounds**: Use multiprocessing for CPU-bound tasks, async/await for I/O-bound tasks, or C extensions

```python
import threading
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# CPU-bound task that shows GIL limitations
def cpu_bound_task(n):
    """CPU-intensive task that will be limited by GIL in threading."""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# I/O-bound task where GIL is released
def io_bound_task(duration):
    """I/O task where GIL is released during sleep."""
    time.sleep(duration)
    return f"Completed after {duration} seconds"

# Demonstrate GIL impact
def compare_execution_methods():
    n = 500000
    
    # Single-threaded
    start = time.time()
    [cpu_bound_task(n) for _ in range(4)]
    single_time = time.time() - start
    
    # Multi-threaded (limited by GIL)
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_bound_task, [n] * 4))
    thread_time = time.time() - start
    
    # Multi-processing (bypasses GIL)
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_bound_task, [n] * 4))
    process_time = time.time() - start
    
    print(f"Single-threaded: {single_time:.2f}s")
    print(f"Multi-threaded: {thread_time:.2f}s (GIL limited)")
    print(f"Multi-processing: {process_time:.2f}s (GIL bypassed)")
```

### 9. Explain Python's method resolution order (MRO).
**Answer:**
Method Resolution Order (MRO) determines the order in which Python searches for methods in a class hierarchy, especially important in multiple inheritance scenarios. Understanding MRO is crucial when designing complex class hierarchies in data engineering frameworks.

**Key Concepts:**
- **C3 Linearization**: Algorithm Python uses to determine MRO
- **Left-to-Right**: Python searches parent classes from left to right
- **Depth-First**: Goes deep into inheritance chain before moving to next parent
- **Diamond Problem**: MRO solves conflicts when multiple inheritance creates diamond patterns
- **`super()`**: Uses MRO to call next method in the chain

**Why MRO Matters:**
- **Predictable Behavior**: Ensures consistent method resolution
- **Multiple Inheritance**: Handles complex inheritance hierarchies safely
- **Framework Design**: Critical for plugin systems and mixins
- **Debugging**: Understanding which method gets called

```python
class A:
    def method(self): print("A")
    def common_method(self): return "A"

class B(A):
    def method(self): print("B")
    def common_method(self): return "B"

class C(A):
    def method(self): print("C")
    def common_method(self): return "C"

class D(B, C):  # Multiple inheritance
    pass

# MRO: D -> B -> C -> A -> object
print("MRO:", [cls.__name__ for cls in D.__mro__])
# Output: ['D', 'B', 'C', 'A', 'object']

d = D()
d.method()  # Calls B.method() (first in MRO after D)
# Output: B

print(d.common_method())  # Also calls B.common_method()
# Output: B

# Practical example: Data processing pipeline with mixins
class DataProcessor:
    def process(self, data):
        return f"Base processing: {data}"

class ValidationMixin:
    def process(self, data):
        print("Validating data...")
        return super().process(data)  # Uses MRO to call next method

class LoggingMixin:
    def process(self, data):
        print("Logging operation...")
        return super().process(data)

class EnhancedProcessor(ValidationMixin, LoggingMixin, DataProcessor):
    def process(self, data):
        print("Enhanced processing...")
        return super().process(data)

# MRO determines call order
processor = EnhancedProcessor()
print("MRO:", [cls.__name__ for cls in EnhancedProcessor.__mro__])
result = processor.process("test data")
# Output shows the order: Enhanced -> Validation -> Logging -> Base
```

### 10. Explain the difference between deep copy and shallow copy.
**Answer:**
Copying objects in Python is crucial for data manipulation, especially when working with nested data structures. Understanding the difference between shallow and deep copying prevents unexpected data mutations and bugs in data processing pipelines.

**Key Concepts:**
- **Shallow Copy**: Creates a new object but inserts references to objects found in the original
- **Deep Copy**: Creates a new object and recursively copies all nested objects
- **Reference Sharing**: Shallow copies share references to nested mutable objects
- **Independence**: Deep copies create completely independent object hierarchies

**When This Matters in Data Engineering:**
- **Data Transformation**: Avoiding unintended modifications to source data
- **Parallel Processing**: Ensuring thread safety when sharing data structures
- **Caching**: Creating independent copies of cached data
- **Configuration Management**: Isolating configuration changes

**Performance Considerations:**
- Shallow copying is faster and uses less memory
- Deep copying can be expensive for large, nested structures
- Consider immutable data structures when possible

```python
import copy
import time

# Basic example
original = [[1, 2, 3], [4, 5, 6]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

# Modify original
original[0][0] = 'X'
print(f"Original: {original}")
print(f"Shallow copy: {shallow}")  # Affected!
print(f"Deep copy: {deep}")       # Not affected
# Output: Original: [['X', 2, 3], [4, 5, 6]]
# Output: Shallow copy: [['X', 2, 3], [4, 5, 6]]
# Output: Deep copy: [[1, 2, 3], [4, 5, 6]]
```

## Advanced Questions

### 11. How do you implement a singleton pattern in Python?
**Answer:**
```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

### 12. Explain context managers and the `with` statement.
**Answer:**
```python
class DatabaseConnection:
    def __enter__(self):
        print("Opening connection")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        return False
```

## Data Engineering Specific Questions

### 14. How would you process a large CSV file that doesn't fit in memory?
**Answer:**
```python
import pandas as pd

def process_large_csv(filename, chunk_size=10000):
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        yield chunk.groupby('category').sum()
```

### 15. How do you handle database connections efficiently?
**Answer:**
```python
from contextlib import contextmanager

@contextmanager
def get_db_connection(pool):
    conn = pool.get_connection()
    try:
        yield conn
    finally:
        pool.return_connection(conn)
```

## Coding Challenges

### 19. Implement a LRU Cache from scratch.
**Answer:**
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        from collections import OrderedDict
        self.order = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            self.order.move_to_end(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self.order.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            oldest = next(iter(self.order))
            del self.cache[oldest]
            del self.order[oldest]
        
        self.cache[key] = value
        self.order[key] = None
```

### 20. Write a function to find the most frequent elements in a large dataset.
**Answer:**
```python
from collections import Counter

def top_k_frequent(data, k):
    counter = Counter(data)
    return counter.most_common(k)
```

### 21. Implement a data pipeline with error handling.
**Answer:**
```python
class PipelineStage:
    def __init__(self, name):
        self.name = name
    
    def process(self, data):
        raise NotImplementedError
    
    def __call__(self, data):
        try:
            return self.process(data)
        except Exception as e:
            print(f"Error in {self.name}: {e}")
            raise

class DataPipeline:
    def __init__(self, stages):
        self.stages = stages
    
    def run(self, data):
        for stage in self.stages:
            data = stage(data)
        return data
```4, 5, 6]]
# Output: Deep copy: [[1, 2, 3], [4, 5, 6]]

# Practical data engineering example
class DataPipeline:
    def __init__(self, config):
        self.config = copy.deepcopy(config)  # Ensure independence
    
    def process_batch(self, data):
        # Create independent copy for processing
        working_data = copy.deepcopy(data)
        # Process without affecting original
        return self.transform(working_data)

# Performance comparison
def performance_test():
    large_nested = [[i] * 1000 for i in range(1000)]
    
    start = time.time()
    shallow = copy.copy(large_nested)
    shallow_time = time.time() - start
    
    start = time.time()
    deep = copy.deepcopy(large_nested)
    deep_time = time.time() - start
    
    print(f"Shallow copy: {shallow_time:.4f}s")
    print(f"Deep copy: {deep_time:.4f}s")
```

### 13. What's the difference between iterators and generators?

**Core Optimization Strategies:**

1. **Algorithmic Optimization**: Choose the right algorithm and data structures first
2. **Built-in Functions**: Use Python's optimized built-ins instead of custom loops
3. **List Comprehensions**: Faster than equivalent for loops for simple operations
4. **Generator Expressions**: Memory-efficient for large datasets
5. **Caching**: Avoid redundant computations using memoization
6. **Vectorization**: Use NumPy/Pandas for numerical operations
7. **Profiling**: Identify actual bottlenecks before optimizing

**Memory Optimization:**
- Use generators for large datasets to avoid loading everything into memory
- Choose appropriate data structures (sets for membership testing, deques for queues)
- Use `__slots__` for classes with many instances
- Consider memory-mapped files for large file processing

**I/O Optimization:**
- Use buffered I/O and appropriate buffer sizes
- Batch database operations instead of individual queries
- Use connection pooling for database connections
- Implement async I/O for concurrent operations

**Concurrency and Parallelism:**
- Use multiprocessing for CPU-bound tasks (bypasses GIL)
- Use threading or asyncio for I/O-bound tasks
- Consider process pools for embarrassingly parallel problems
- Use concurrent.futures for cleaner parallel code

**When to Use External Libraries:**
- NumPy/Pandas for numerical computations
- Cython for performance-critical code sections
- Numba for JIT compilation of numerical functions
- PyPy as an alternative Python interpreter

```python
import time
import numpy as np
import pandas as pd
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor
from collections import deque, defaultdict

# 1. Use built-ins and list comprehensions
def slow_sum_squares(numbers):
    """Slow: Manual loop"""
    result = []
    for num in numbers:
        result.append(num ** 2)
    return sum(result)

def fast_sum_squares(numbers):
    """Fast: List comprehension + built-in sum"""
    return sum(num ** 2 for num in numbers)

def fastest_sum_squares(numbers):
    """Fastest: NumPy vectorization"""
    arr = np.array(numbers)
    return np.sum(arr ** 2)

# 2. Use generators for memory efficiency
def process_large_file_bad(filename):
    """Memory inefficient: Loads entire file"""
    with open(filename) as f:
        lines = f.readlines()  # Loads all into memory
    return [line.strip().upper() for line in lines]

def process_large_file_good(filename):
    """Memory efficient: Generator"""
    with open(filename) as f:
        for line in f:  # Processes one line at a time
            yield line.strip().upper()

# 3. Use caching for expensive computations
@lru_cache(maxsize=128)
def expensive_calculation(n):
    """Cached expensive function"""
    time.sleep(0.1)  # Simulate expensive operation
    return sum(i ** 2 for i in range(n))

# 4. Choose right data structures
def find_common_elements_slow(list1, list2):
    """Slow: O(n*m) complexity"""
    common = []
    for item in list1:
        if item in list2:  # Linear search in list
            common.append(item)
    return common

def find_common_elements_fast(list1, list2):
    """Fast: O(n+m) complexity using sets"""
    return list(set(list1) & set(list2))

# 5. Batch operations for databases
def insert_records_slow(cursor, records):
    """Slow: Individual inserts"""
    for record in records:
        cursor.execute("INSERT INTO table VALUES (?, ?)", record)

def insert_records_fast(cursor, records):
    """Fast: Batch insert"""
    cursor.executemany("INSERT INTO table VALUES (?, ?)", records)

# 6. Use multiprocessing for CPU-bound tasks
def cpu_intensive_task(data_chunk):
    """Simulate CPU-intensive processing"""
    return sum(x ** 2 for x in data_chunk)

def process_parallel(data, num_workers=4):
    """Process data in parallel"""
    chunk_size = len(data) // num_workers
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(cpu_intensive_task, chunks))
    
    return sum(results)

# 7. Profile and benchmark
def benchmark_functions():
    """Compare performance of different approaches"""
    data = list(range(100000))
    
    # Test different sum_squares implementations
    start = time.time()
    result1 = slow_sum_squares(data)
    slow_time = time.time() - start
    
    start = time.time()
    result2 = fast_sum_squares(data)
    fast_time = time.time() - start
    
    start = time.time()
    result3 = fastest_sum_squares(data)
    numpy_time = time.time() - start
    
    print(f"Slow (manual loop): {slow_time:.4f}s")
    print(f"Fast (comprehension): {fast_time:.4f}s")
    print(f"NumPy (vectorized): {numpy_time:.4f}s")
    print(f"Speedup: {slow_time/numpy_time:.1f}x")

# 8. Memory-efficient data processing
class DataProcessor:
    """Optimized data processor with various techniques"""
    
    def __init__(self):
        self.cache = {}
        self.buffer_size = 8192
    
    def process_csv_efficiently(self, filename):
        """Process large CSV files efficiently"""
        # Use pandas for optimized CSV reading
        chunk_size = 10000
        results = []
        
        for chunk in pd.read_csv(filename, chunksize=chunk_size):
            # Process chunk efficiently
            processed = self._process_chunk(chunk)
            results.append(processed)
        
        return pd.concat(results, ignore_index=True)
    
    def _process_chunk(self, chunk):
        """Vectorized chunk processing"""
        # Use vectorized operations instead of apply
        chunk['processed'] = chunk['value'] * 2 + chunk['offset']
        return chunk[chunk['processed'] > 0]  # Vectorized filtering

# Performance monitoring decorator
def timing_decorator(func):
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def optimized_data_pipeline(data):
    """Example of an optimized data processing pipeline"""
    # Use NumPy for numerical operations
    arr = np.array(data)
    
    # Vectorized operations
    normalized = (arr - np.mean(arr)) / np.std(arr)
    filtered = normalized[normalized > 0]
    
    # Use built-in functions
    return {
        'mean': np.mean(filtered),
        'std': np.std(filtered),
        'count': len(filtered)
    }
```4, 5, 6]]
# Output: Deep copy: [[1, 2, 3], [4, 5, 6]]

# Real-world example: Data processing pipeline
class DataProcessor:
    def __init__(self, config):
        # Deep copy to avoid config mutations
        self.config = copy.deepcopy(config)
    
    def process_batch(self, data_batch):
        # Shallow copy for performance (assuming immutable data)
        working_data = copy.copy(data_batch)
        # Process without affecting original
        return self.transform_data(working_data)

# Performance comparison
def compare_copy_performance():
    large_nested_data = [[i] * 1000 for i in range(1000)]
    
    # Shallow copy timing
    start = time.time()
    shallow_copies = [copy.copy(large_nested_data) for _ in range(100)]
    shallow_time = time.time() - start
    
    # Deep copy timing
    start = time.time()
    deep_copies = [copy.deepcopy(large_nested_data) for _ in range(100)]
    deep_time = time.time() - start
    
    print(f"Shallow copy time: {shallow_time:.4f}s")
    print(f"Deep copy time: {deep_time:.4f}s")
    print(f"Deep copy is {deep_time/shallow_time:.1f}x slower")

# Custom objects with copy behavior
class CustomData:
    def __init__(self, values):
        self.values = values
        self.metadata = {'created': time.time()}
    
    def __copy__(self):
        # Custom shallow copy behavior
        return CustomData(self.values)  # New object, same values reference
    
    def __deepcopy__(self, memo):
        # Custom deep copy behavior
        return CustomData(copy.deepcopy(self.values, memo))

# Usage with custom objects
custom_data = CustomData([[1, 2], [3, 4]])
shallow_custom = copy.copy(custom_data)
deep_custom = copy.deepcopy(custom_data)

# Modify original
custom_data.values[0][0] = 999
print(f"Original: {custom_data.values}")
print(f"Shallow: {shallow_custom.values}")  # Affected
print(f"Deep: {deep_custom.values}")        # Not affected
```

## Advanced Questions

### 11. How do you implement a singleton pattern in Python?
**Answer:**
The Singleton pattern ensures that a class has only one instance throughout the application lifecycle. This is commonly used in data engineering for managing shared resources like database connections, configuration objects, or logging systems.

**When to Use Singleton:**
- **Database Connection Pools**: Single point of connection management
- **Configuration Management**: Global application settings
- **Logging Systems**: Centralized logging instance
- **Cache Managers**: Shared cache across application
- **Resource Managers**: File handles, network connections

**Implementation Approaches:**
- **`__new__` Method**: Controls object creation
- **Decorator Pattern**: Wraps class to control instantiation
- **Metaclass**: Controls class creation itself
- **Module-Level**: Python modules are singletons by nature

**Thread Safety Considerations:**
Singletons must be thread-safe in multi-threaded applications to prevent multiple instances.

```python
import threading
from functools import wraps

# Method 1: Using __new__ (thread-safe)
class Singleton:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:  # Thread-safe
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._initialized = True
                    # Initialize here
                    self.data = "Singleton instance"

# Method 2: Decorator pattern
def singleton(cls):
    instances = {}
    lock = threading.Lock()
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class ConfigManager:
    def __init__(self):
        self.config = {"database_url": "localhost:5432"}
    
    def get_config(self, key):
        return self.config.get(key)

# Method 3: Metaclass approach
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseManager(metaclass=SingletonMeta):
    def __init__(self):
        self.connection_pool = "Database connection pool"
    
    def get_connection(self):
        return f"Connection from {self.connection_pool}"

# Method 4: Module-level singleton (Pythonic)
# In config.py file:
class _Config:
    def __init__(self):
        self.settings = {"debug": True, "max_connections": 100}
    
    def get(self, key, default=None):
        return self.settings.get(key, default)

# Create single instance at module level
config = _Config()

# Usage examples
if __name__ == "__main__":
    # Test singleton behavior
    s1 = Singleton()
    s2 = Singleton()
    print(f"Same instance: {s1 is s2}")  # True
    
    # Test with decorator
    c1 = ConfigManager()
    c2 = ConfigManager()
    print(f"Same config: {c1 is c2}")  # True
    
    # Test with metaclass
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    print(f"Same database manager: {db1 is db2}")  # True
```

### 12. Explain context managers and the `with` statement.
**Answer:**
Context managers provide a way to allocate and release resources precisely when you want to. They're most commonly used with the `with` statement to ensure proper cleanup of resources like files, database connections, or locks.

**How Context Managers Work:**
- `__enter__()`: Called when entering the `with` block
- `__exit__()`: Called when exiting the `with` block (even if an exception occurs)

```python
import time
import threading
from contextlib import contextmanager

# Built-in context manager example
with open('file.txt', 'r') as f:
    content = f.read()
# File automatically closed, even if an exception occurs

# Custom context manager class
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to database: {self.connection_string}")
        self.connection = f"Connected to {self.connection_string}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection")
        if exc_type:
            print(f"Exception occurred: {exc_val}")
            print("Rolling back transaction")
        else:
            print("Committing transaction")
        self.connection = None
        return False  # Don't suppress exceptions

# Using contextlib decorator
@contextmanager
def timer(operation_name="Operation"):
    """Context manager to time operations."""
    start = time.time()
    try:
        print(f"Starting {operation_name}...")
        yield start
    finally:
        elapsed = time.time() - start
        print(f"{operation_name} completed in {elapsed:.4f}s")

# Usage examples
with timer("Data Processing"):
    time.sleep(1)
    data = [i**2 for i in range(10000)]

# Thread-safe context manager
class ThreadSafeResource:
    def __init__(self):
        self._lock = threading.Lock()
        self._resource = "shared_resource"
    
    def __enter__(self):
        self._lock.acquire()
        return self._resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()
        return False
```

### 13. What's the difference between iterators and generators?

**Answer:**
Iterators and generators are fundamental concepts for efficient data processing in Python, especially crucial when working with large datasets that don't fit in memory. Understanding their differences helps optimize memory usage and processing performance in data engineering applications.

**Key Differences:**

**Iterators:**
- Objects implementing the iterator protocol (`__iter__()` and `__next__()`)
- Maintain explicit state between calls
- Can be created from any iterable using `iter()`
- More verbose to implement but offer fine-grained control
- Can be reset by calling `__iter__()` again (if implemented)
- Custom classes can implement complex iteration logic

**Generators:**
- Special iterators created using `yield` keyword or generator expressions
- Automatically implement iterator protocol
- State maintained implicitly by Python
- More concise and readable
- Cannot be reset - consumed once
- Function-based approach with `yield`

**Memory and Performance:**
- Both use lazy evaluation (compute values on-demand)
- Generators typically use less memory overhead
- Iterators offer more control over state management
- Both excellent for processing large datasets
- Generators have less function call overhead

**When to Use Each:**
- **Generators**: Simple iteration, data transformation pipelines, streaming data, one-time processing
- **Iterators**: Complex state management, custom iteration logic, reusable iterators, stateful processing

**Protocol Implementation:**
- **Iterators**: Must implement `__iter__()` and `__next__()` methods
- **Generators**: Python handles protocol implementation automatically

**State Management:**
- **Iterators**: Explicit state variables and logic
- **Generators**: Implicit state through function execution context

```python
import sys
import time
from typing import Iterator, Generator

# Iterator example with explicit state management
class DataFileIterator:
    """Iterator for processing large files line by line."""
    
    def __init__(self, filename: str, chunk_size: int = 1024):
        self.filename = filename
        self.chunk_size = chunk_size
        self.file_handle = None
        self.line_number = 0
    
    def __iter__(self):
        self.file_handle = open(self.filename, 'r')
        self.line_number = 0
        return self
    
    def __next__(self):
        if self.file_handle is None:
            raise StopIteration
        
        line = self.file_handle.readline()
        if not line:
            self.file_handle.close()
            self.file_handle = None
            raise StopIteration
        
        self.line_number += 1
        return {
            'line_number': self.line_number,
            'content': line.strip(),
            'length': len(line)
        }
    
    def get_current_position(self):
        """Additional method available in iterator."""
        return self.line_number

# Generator function for data processing
def process_data_stream(data_source: Iterator) -> Generator[dict, None, None]:
    """Generator that processes data from any iterator."""
    batch = []
    batch_size = 100
    
    for item in data_source:
        batch.append(item)
        
        if len(batch) >= batch_size:
            # Process batch and yield results
            processed_batch = {
                'batch_size': len(batch),
                'total_length': sum(item.get('length', 0) for item in batch),
                'items': batch
            }
            yield processed_batch
            batch = []
    
    # Yield remaining items
    if batch:
        yield {
            'batch_size': len(batch),
            'total_length': sum(item.get('length', 0) for item in batch),
            'items': batch
        }

# Generator expression for data transformation
def create_data_pipeline(numbers: Iterator[int]) -> Generator[dict, None, None]:
    """Create a data processing pipeline using generators."""
    # Filter even numbers
    evens = (x for x in numbers if x % 2 == 0)
    
    # Transform to squares
    squares = (x**2 for x in evens)
    
    # Add metadata
    enriched = ({'value': x, 'sqrt': x**0.5, 'is_perfect_square': int(x**0.5)**2 == x} 
                for x in squares)
    
    return enriched

# Performance and memory comparison
def compare_iterator_vs_generator():
    """Compare memory usage and performance."""
    
    # Large dataset simulation
    def large_dataset_iterator():
        """Iterator version."""
        class LargeDataIterator:
            def __init__(self, size):
                self.size = size
                self.current = 0
            
            def __iter__(self):
                return self
            
            def __next__(self):
                if self.current >= self.size:
                    raise StopIteration
                self.current += 1
                return self.current ** 2
        
        return LargeDataIterator(1000000)
    
    def large_dataset_generator(size: int):
        """Generator version."""
        for i in range(1, size + 1):
            yield i ** 2
    
    # Memory usage comparison
    iterator_obj = large_dataset_iterator()
    generator_obj = large_dataset_generator(1000000)
    
    print(f"Iterator memory: {sys.getsizeof(iterator_obj)} bytes")
    print(f"Generator memory: {sys.getsizeof(generator_obj)} bytes")
    
    # Performance comparison
    def time_iteration(iterable, name):
        start = time.time()
        count = sum(1 for _ in iterable)
        end = time.time()
        print(f"{name}: {count} items in {end - start:.4f}s")
    
    time_iteration(large_dataset_iterator(), "Iterator")
    time_iteration(large_dataset_generator(1000000), "Generator")

# Advanced generator patterns
def fibonacci_generator() -> Generator[int, None, None]:
    """Infinite Fibonacci sequence generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def take(n: int, iterable: Iterator) -> Generator:
    """Take first n items from any iterator."""
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item

# Practical usage examples
if __name__ == "__main__":
    # Example 1: Processing large dataset with iterator
    print("=== Iterator Example ===")
    # Note: This would work with an actual file
    # file_iterator = DataFileIterator('large_file.txt')
    # for data in file_iterator:
    #     print(f"Line {data['line_number']}: {data['content'][:50]}...")
    #     if file_iterator.get_current_position() > 5:
    #         break
    
    # Example 2: Data pipeline with generators
    print("\n=== Generator Pipeline Example ===")
    numbers = range(1, 21)  # Simulate data source
    pipeline = create_data_pipeline(iter(numbers))
    
    for result in pipeline:
        print(f"Value: {result['value']}, Perfect Square: {result['is_perfect_square']}")
    
    # Example 3: Infinite generator with limiting
    print("\n=== Infinite Generator Example ===")
    fib = fibonacci_generator()
    first_10_fibs = list(take(10, fib))
    print(f"First 10 Fibonacci numbers: {first_10_fibs}")
    
    # Example 4: Performance comparison
    print("\n=== Performance Comparison ===")
    compare_iterator_vs_generator()

# Key takeaways:
# 1. Use generators for simple, one-time iteration
# 2. Use iterators when you need state management or reusability
# 3. Both are memory-efficient for large datasets
# 4. Generators are more concise and readable
# 5. Iterators offer more control and flexibility
```

### 14. How would you implement a thread-safe singleton pattern for database connections?

**Answer:**
Implementing a thread-safe singleton for database connections is crucial in multi-threaded data engineering applications to ensure resource efficiency and prevent connection leaks. The singleton pattern ensures only one instance of the database connection manager exists throughout the application lifecycle.

**Why Thread Safety Matters:**
- **Race Conditions**: Multiple threads might create multiple instances simultaneously
- **Resource Management**: Prevents connection pool duplication
- **Memory Efficiency**: Single instance reduces memory footprint
- **Configuration Consistency**: Ensures all threads use same connection settings

**Implementation Approaches:**
- **Double-Checked Locking**: Most common and efficient approach
- **Module-Level Singleton**: Pythonic approach using module imports
- **Metaclass Approach**: Advanced technique using metaclasses
- **Decorator Pattern**: Functional approach to singleton creation

**Key Considerations:**
- **Lazy Initialization**: Create instance only when needed
- **Thread Safety**: Use locks to prevent race conditions
- **Connection Pooling**: Manage multiple database connections efficiently
- **Error Handling**: Graceful handling of connection failures
- **Configuration Management**: Support different environments

```python
import threading
import time
from typing import Optional, Dict, Any
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Method 1: Thread-safe singleton with double-checked locking
class DatabaseConnection:
    """Thread-safe singleton for database connections."""
    
    _instance: Optional['DatabaseConnection'] = None
    _lock = threading.RLock()  # Reentrant lock
    _initialized = False
    
    def __new__(cls, connection_string: str = None):
        """Create or return existing instance with thread safety."""
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, connection_string: str = None):
        """Initialize database connection (only once)."""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self.connection_string = connection_string or "sqlite:///default.db"
                    self.pool = None
                    self._connection_count = 0
                    self._max_connections = 10
                    self._active_connections = set()
                    self._stats = {
                        'connections_created': 0,
                        'connections_closed': 0,
                        'active_connections': 0
                    }
                    self._initialized = True
                    logger.info(f"Database singleton initialized with {self.connection_string}")
    
    def get_connection(self):
        """Get database connection from pool."""
        with self._lock:
            # Simulate connection creation (replace with actual DB connection)
            connection_id = f"conn_{self._connection_count}"
            self._connection_count += 1
            self._stats['connections_created'] += 1
            self._stats['active_connections'] += 1
            
            # Store active connection
            self._active_connections.add(connection_id)
            
            logger.info(f"Created connection: {connection_id}")
            return MockConnection(connection_id, self)
    
    def return_connection(self, connection_id: str):
        """Return connection to pool."""
        with self._lock:
            if connection_id in self._active_connections:
                self._active_connections.remove(connection_id)
                self._stats['connections_closed'] += 1
                self._stats['active_connections'] -= 1
                logger.info(f"Returned connection: {connection_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        with self._lock:
            return {
                **self._stats,
                'connection_string': self.connection_string,
                'active_connection_ids': list(self._active_connections)
            }
    
    @classmethod
    def reset_instance(cls):
        """Reset singleton instance (for testing)."""
        with cls._lock:
            cls._instance = None
            cls._initialized = False

class MockConnection:
    """Mock database connection for demonstration."""
    
    def __init__(self, connection_id: str, manager: DatabaseConnection):
        self.connection_id = connection_id
        self.manager = manager
        self.closed = False
    
    def execute(self, query: str):
        """Execute database query."""
        if self.closed:
            raise Exception("Connection is closed")
        return f"Executed '{query}' on {self.connection_id}"
    
    def close(self):
        """Close database connection."""
        if not self.closed:
            self.manager.return_connection(self.connection_id)
            self.closed = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Method 2: Module-level singleton (Pythonic approach)
class _DatabaseManager:
    """Private database manager class."""
    
    def __init__(self):
        self.connection_string = "sqlite:///module_singleton.db"
        self.connections = {}
        self._lock = threading.Lock()
    
    def get_connection(self, connection_id: str = "default"):
        """Get connection by ID."""
        with self._lock:
            if connection_id not in self.connections:
                self.connections[connection_id] = f"connection_to_{connection_id}"
            return self.connections[connection_id]
    
    def close_all(self):
        """Close all connections."""
        with self._lock:
            self.connections.clear()

# Create module-level singleton instance
db_manager = _DatabaseManager()

# Method 3: Metaclass-based singleton
class SingletonMeta(type):
    """Metaclass for creating singleton classes."""
    
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MetaclassDatabaseConnection(metaclass=SingletonMeta):
    """Database connection using metaclass singleton."""
    
    def __init__(self, connection_string: str = "sqlite:///metaclass.db"):
        if not hasattr(self, 'initialized'):
            self.connection_string = connection_string
            self.pool_size = 5
            self.initialized = True
            logger.info(f"Metaclass singleton initialized: {connection_string}")
    
    def connect(self):
        return f"Connected to {self.connection_string}"

# Method 4: Decorator-based singleton
def singleton(cls):
    """Decorator to make a class singleton."""
    instances = {}
    lock = threading.Lock()
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class DecoratorDatabaseConnection:
    """Database connection using decorator singleton."""
    
    def __init__(self, connection_string: str = "sqlite:///decorator.db"):
        self.connection_string = connection_string
        self.created_at = time.time()
        logger.info(f"Decorator singleton created: {connection_string}")
    
    def query(self, sql: str):
        return f"Executing '{sql}' on {self.connection_string}"

# Advanced: Thread-safe connection pool singleton
class ConnectionPoolSingleton:
    """Advanced singleton with actual connection pooling."""
    
    _instance = None
    _lock = threading.RLock()
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, connection_string: str = None, pool_size: int = 10):
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self.connection_string = connection_string or "sqlite:///pool.db"
                    self.pool_size = pool_size
                    self.available_connections = []
                    self.active_connections = set()
                    self.total_created = 0
                    self._create_initial_pool()
                    self._initialized = True
    
    def _create_initial_pool(self):
        """Create initial connection pool."""
        for i in range(self.pool_size):
            conn_id = f"pool_conn_{i}"
            self.available_connections.append(conn_id)
            self.total_created += 1
        logger.info(f"Created connection pool with {self.pool_size} connections")
    
    @contextmanager
    def get_connection(self, timeout: float = 5.0):
        """Get connection from pool with context manager."""
        connection = None
        start_time = time.time()
        
        # Wait for available connection
        while time.time() - start_time < timeout:
            with self._lock:
                if self.available_connections:
                    connection = self.available_connections.pop()
                    self.active_connections.add(connection)
                    break
            time.sleep(0.1)
        
        if connection is None:
            raise TimeoutError("No connections available within timeout")
        
        try:
            yield MockConnection(connection, self)
        finally:
            # Return connection to pool
            with self._lock:
                if connection in self.active_connections:
                    self.active_connections.remove(connection)
                    self.available_connections.append(connection)
    
    def get_pool_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics."""
        with self._lock:
            return {
                'total_connections': self.total_created,
                'available_connections': len(self.available_connections),
                'active_connections': len(self.active_connections),
                'pool_size': self.pool_size,
                'connection_string': self.connection_string
            }

# Testing and demonstration
def test_singleton_thread_safety():
    """Test singleton thread safety with multiple threads."""
    
    instances = []
    
    def create_instance(thread_id: int):
        """Create database instance in thread."""
        db = DatabaseConnection(f"sqlite:///thread_{thread_id}.db")
        instances.append(db)
        logger.info(f"Thread {thread_id} created instance: {id(db)}")
    
    # Create multiple threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=create_instance, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Verify all instances are the same
    first_instance = instances[0]
    all_same = all(instance is first_instance for instance in instances)
    
    print(f"All instances are the same: {all_same}")
    print(f"Instance IDs: {[id(instance) for instance in instances]}")
    
    return all_same

# Usage examples
if __name__ == "__main__":
    print("=== Thread-Safe Singleton Database Connection Examples ===")
    
    # Test 1: Basic singleton
    print("\n1. Basic Singleton Test:")
    db1 = DatabaseConnection("postgresql://user:pass@localhost/db")
    db2 = DatabaseConnection()  # Same instance
    print(f"Same instance: {db1 is db2}")
    print(f"Stats: {db1.get_stats()}")
    
    # Test 2: Connection usage
    print("\n2. Connection Usage:")
    with db1.get_connection() as conn:
        result = conn.execute("SELECT * FROM users")
        print(f"Query result: {result}")
    
    print(f"Updated stats: {db1.get_stats()}")
    
    # Test 3: Module-level singleton
    print("\n3. Module-Level Singleton:")
    conn1 = db_manager.get_connection("app1")
    conn2 = db_manager.get_connection("app1")
    print(f"Same connection: {conn1 == conn2}")
    
    # Test 4: Metaclass singleton
    print("\n4. Metaclass Singleton:")
    meta_db1 = MetaclassDatabaseConnection("postgresql://localhost/meta")
    meta_db2 = MetaclassDatabaseConnection("different_string")  # Same instance
    print(f"Same instance: {meta_db1 is meta_db2}")
    print(f"Connection string: {meta_db1.connection_string}")
    
    # Test 5: Decorator singleton
    print("\n5. Decorator Singleton:")
    dec_db1 = DecoratorDatabaseConnection("postgresql://localhost/decorator")
    dec_db2 = DecoratorDatabaseConnection("ignored_string")
    print(f"Same instance: {dec_db1 is dec_db2}")
    
    # Test 6: Connection pool singleton
    print("\n6. Connection Pool Singleton:")
    pool = ConnectionPoolSingleton("postgresql://localhost/pool", pool_size=3)
    
    with pool.get_connection() as conn:
        result = conn.execute("SELECT COUNT(*) FROM products")
        print(f"Pool query result: {result}")
    
    print(f"Pool stats: {pool.get_pool_stats()}")
    
    # Test 7: Thread safety
    print("\n7. Thread Safety Test:")
    # Reset singleton for clean test
    DatabaseConnection.reset_instance()
    thread_safe = test_singleton_thread_safety()
    print(f"Thread safety verified: {thread_safe}")
    
    print("\n=== Best Practices Summary ===")
    print("✓ Use double-checked locking for thread safety")
    print("✓ Implement proper connection pooling")
    print("✓ Use context managers for automatic cleanup")
    print("✓ Include comprehensive error handling")
    print("✓ Provide statistics and monitoring")
    print("✓ Support configuration management")
    print("✓ Test thread safety thoroughly")
```

## Data Engineering Specific Questions

### 15. How would you process a large CSV file that doesn't fit in memory?

**Answer:**
Processing large CSV files that exceed available memory is a common challenge in data engineering. The key is to use streaming approaches that process data in chunks rather than loading everything into memory at once.

**Core Strategies:**

**1. Chunking Approach:**
- Read file in smaller, manageable pieces
- Process each chunk independently
- Aggregate results as needed
- Memory usage remains constant regardless of file size

**2. Streaming Processing:**
- Process one line at a time
- Minimal memory footprint
- Suitable for simple transformations
- Can handle arbitrarily large files

**3. Parallel Processing:**
- Split file into multiple parts
- Process parts concurrently
- Combine results at the end
- Faster processing on multi-core systems

**4. External Libraries:**
- **Pandas**: `chunksize` parameter for chunked reading
- **Dask**: Parallel computing with pandas-like API
- **Vaex**: Out-of-core dataframe library
- **Polars**: Fast dataframe library with lazy evaluation

**When to Use Each Approach:**
- **Chunking**: General-purpose, good balance of simplicity and efficiency
- **Streaming**: Maximum memory efficiency, simple operations
- **Parallel**: CPU-intensive operations, multiple cores available
- **External Libraries**: Complex operations, existing pandas workflows

**Performance Considerations:**
- **Chunk Size**: Balance between memory usage and I/O efficiency
- **Data Types**: Optimize column types to reduce memory usage
- **Compression**: Use compressed formats when possible
- **SSD vs HDD**: Storage type affects optimal chunk sizes

```python
import pandas as pd
import csv
import json
from typing import Iterator, Dict, Any, List
import time
import os
from pathlib import Path
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

# Method 1: Pandas chunking approach
def process_large_csv_pandas(filename: str, chunk_size: int = 10000) -> Iterator[pd.DataFrame]:
    """Process large CSV using pandas chunking.
    
    Args:
        filename: Path to CSV file
        chunk_size: Number of rows per chunk
        
    Yields:
        Processed dataframe chunks
    """
    try:
        for chunk_num, chunk in enumerate(pd.read_csv(filename, chunksize=chunk_size)):
            print(f"Processing chunk {chunk_num + 1} with {len(chunk)} rows")
            
            # Example processing: clean and aggregate data
            processed_chunk = chunk.dropna()  # Remove null values
            
            # Apply transformations
            if 'amount' in processed_chunk.columns:
                processed_chunk['amount'] = pd.to_numeric(processed_chunk['amount'], errors='coerce')
            
            # Group and aggregate if needed
            if 'category' in processed_chunk.columns:
                aggregated = processed_chunk.groupby('category').agg({
                    'amount': ['sum', 'mean', 'count']
                }).round(2)
                yield aggregated
            else:
                yield processed_chunk
                
    except Exception as e:
        print(f"Error processing CSV: {e}")
        raise

# Method 2: Pure Python streaming approach
def process_csv_streaming(filename: str) -> Iterator[Dict[str, Any]]:
    """Process CSV file line by line with minimal memory usage.
    
    Args:
        filename: Path to CSV file
        
    Yields:
        Processed records as dictionaries
    """
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 1):
            try:
                # Process individual row
                processed_row = process_single_row(row)
                
                if processed_row:  # Only yield valid rows
                    yield processed_row
                    
                # Progress indicator for large files
                if row_num % 100000 == 0:
                    print(f"Processed {row_num:,} rows")
                    
            except Exception as e:
                print(f"Error processing row {row_num}: {e}")
                continue

def process_single_row(row: Dict[str, str]) -> Dict[str, Any]:
    """Process a single CSV row.
    
    Args:
        row: Dictionary representing CSV row
        
    Returns:
        Processed row or None if invalid
    """
    try:
        # Data validation and cleaning
        if not row.get('id') or not row.get('amount'):
            return None
        
        # Type conversions
        processed = {
            'id': int(row['id']),
            'amount': float(row['amount']),
            'category': row.get('category', 'unknown').strip().lower(),
            'timestamp': row.get('timestamp', ''),
            'processed_at': time.time()
        }
        
        # Business logic
        processed['amount_category'] = 'high' if processed['amount'] > 1000 else 'low'
        
        return processed
        
    except (ValueError, TypeError) as e:
        print(f"Invalid row data: {e}")
        return None

# Method 3: Parallel processing approach
def process_csv_parallel(filename: str, num_processes: int = None) -> List[Dict[str, Any]]:
    """Process large CSV using parallel processing.
    
    Args:
        filename: Path to CSV file
        num_processes: Number of processes to use
        
    Returns:
        List of aggregated results
    """
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    # Split file into chunks for parallel processing
    file_chunks = split_csv_file(filename, num_processes)
    
    # Process chunks in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(process_csv_chunk, file_chunks))
    
    # Combine results
    combined_results = []
    for result in results:
        combined_results.extend(result)
    
    # Clean up temporary files
    for chunk_file in file_chunks:
        if os.path.exists(chunk_file):
            os.remove(chunk_file)
    
    return combined_results

def split_csv_file(filename: str, num_chunks: int) -> List[str]:
    """Split CSV file into smaller chunks for parallel processing.
    
    Args:
        filename: Path to original CSV file
        num_chunks: Number of chunks to create
        
    Returns:
        List of chunk filenames
    """
    chunk_files = []
    
    with open(filename, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read header
        
        # Count total rows
        total_rows = sum(1 for _ in reader)
        infile.seek(0)
        next(reader)  # Skip header again
        
        rows_per_chunk = total_rows // num_chunks + 1
        
        for chunk_num in range(num_chunks):
            chunk_filename = f"temp_chunk_{chunk_num}.csv"
            chunk_files.append(chunk_filename)
            
            with open(chunk_filename, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)  # Write header to each chunk
                
                # Write rows to chunk
                for _ in range(rows_per_chunk):
                    try:
                        row = next(reader)
                        writer.writerow(row)
                    except StopIteration:
                        break
    
    return chunk_files

def process_csv_chunk(chunk_filename: str) -> List[Dict[str, Any]]:
    """Process a single CSV chunk.
    
    Args:
        chunk_filename: Path to chunk file
        
    Returns:
        List of processed records
    """
    results = []
    
    with open(chunk_filename, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            processed_row = process_single_row(row)
            if processed_row:
                results.append(processed_row)
    
    return results

# Method 4: Using Dask for distributed processing
def process_csv_with_dask(filename: str) -> pd.DataFrame:
    """Process large CSV using Dask for distributed computing.
    
    Args:
        filename: Path to CSV file
        
    Returns:
        Processed dataframe
    """
    try:
        import dask.dataframe as dd
        
        # Read CSV with Dask (lazy evaluation)
        df = dd.read_csv(filename)
        
        print(f"Dask dataframe shape: {df.shape[0].compute()} rows, {df.shape[1]} columns")
        
        # Perform operations (still lazy)
        processed_df = df.dropna()
        
        # Type conversions
        if 'amount' in df.columns:
            processed_df['amount'] = dd.to_numeric(processed_df['amount'], errors='coerce')
        
        # Aggregations
        if 'category' in df.columns:
            result = processed_df.groupby('category')['amount'].agg(['sum', 'mean', 'count'])
            return result.compute()  # Trigger computation
        else:
            return processed_df.compute()
            
    except ImportError:
        print("Dask not installed. Install with: pip install dask[dataframe]")
        return None
    except Exception as e:
        print(f"Error with Dask processing: {e}")
        return None

# Method 5: Memory-efficient aggregation
class CSVAggregator:
    """Memory-efficient CSV aggregator for large files."""
    
    def __init__(self):
        self.stats = {
            'total_rows': 0,
            'valid_rows': 0,
            'categories': {},
            'amount_sum': 0,
            'amount_count': 0
        }
    
    def process_file(self, filename: str, chunk_size: int = 50000) -> Dict[str, Any]:
        """Process entire file and return aggregated statistics.
        
        Args:
            filename: Path to CSV file
            chunk_size: Rows per chunk
            
        Returns:
            Aggregated statistics
        """
        start_time = time.time()
        
        for chunk in pd.read_csv(filename, chunksize=chunk_size):
            self._process_chunk(chunk)
        
        processing_time = time.time() - start_time
        
        # Calculate final statistics
        self.stats['processing_time'] = processing_time
        self.stats['average_amount'] = (
            self.stats['amount_sum'] / self.stats['amount_count'] 
            if self.stats['amount_count'] > 0 else 0
        )
        
        return self.stats
    
    def _process_chunk(self, chunk: pd.DataFrame) -> None:
        """Process a single chunk and update statistics.
        
        Args:
            chunk: Pandas dataframe chunk
        """
        self.stats['total_rows'] += len(chunk)
        
        # Clean data
        valid_chunk = chunk.dropna(subset=['amount'])
        self.stats['valid_rows'] += len(valid_chunk)
        
        if len(valid_chunk) == 0:
            return
        
        # Convert amount to numeric
        valid_chunk['amount'] = pd.to_numeric(valid_chunk['amount'], errors='coerce')
        valid_amounts = valid_chunk['amount'].dropna()
        
        # Update amount statistics
        self.stats['amount_sum'] += valid_amounts.sum()
        self.stats['amount_count'] += len(valid_amounts)
        
        # Update category statistics
        if 'category' in valid_chunk.columns:
            category_counts = valid_chunk['category'].value_counts()
            for category, count in category_counts.items():
                if category in self.stats['categories']:
                    self.stats['categories'][category] += count
                else:
                    self.stats['categories'][category] = count

# Performance comparison and benchmarking
def benchmark_csv_processing_methods(filename: str, file_size_mb: float) -> Dict[str, float]:
    """Benchmark different CSV processing methods.
    
    Args:
        filename: Path to test CSV file
        file_size_mb: File size in MB for reference
        
    Returns:
        Dictionary of method names and processing times
    """
    results = {}
    
    print(f"Benchmarking CSV processing methods on {file_size_mb:.1f}MB file...")
    
    # Method 1: Pandas chunking
    start_time = time.time()
    chunk_count = 0
    for chunk in process_large_csv_pandas(filename, chunk_size=10000):
        chunk_count += 1
    results['pandas_chunking'] = time.time() - start_time
    print(f"Pandas chunking: {results['pandas_chunking']:.2f}s ({chunk_count} chunks)")
    
    # Method 2: Streaming
    start_time = time.time()
    row_count = sum(1 for _ in process_csv_streaming(filename))
    results['streaming'] = time.time() - start_time
    print(f"Streaming: {results['streaming']:.2f}s ({row_count:,} rows)")
    
    # Method 3: Aggregator
    start_time = time.time()
    aggregator = CSVAggregator()
    stats = aggregator.process_file(filename)
    results['aggregator'] = time.time() - start_time
    print(f"Aggregator: {results['aggregator']:.2f}s ({stats['total_rows']:,} rows)")
    
    # Method 4: Dask (if available)
    try:
        start_time = time.time()
        dask_result = process_csv_with_dask(filename)
        if dask_result is not None:
            results['dask'] = time.time() - start_time
            print(f"Dask: {results['dask']:.2f}s")
    except Exception as e:
        print(f"Dask benchmark failed: {e}")
    
    return results

# Usage examples and testing
def create_sample_csv(filename: str, num_rows: int = 100000) -> None:
    """Create a sample CSV file for testing.
    
    Args:
        filename: Output filename
        num_rows: Number of rows to generate
    """
    import random
    
    categories = ['electronics', 'clothing', 'books', 'home', 'sports']
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'amount', 'category', 'timestamp'])
        
        for i in range(num_rows):
            writer.writerow([
                i + 1,
                round(random.uniform(10, 5000), 2),
                random.choice(categories),
                f"2023-01-{random.randint(1, 28):02d}"
            ])
    
    print(f"Created sample CSV with {num_rows:,} rows: {filename}")

if __name__ == "__main__":
    # Create sample data for demonstration
    sample_file = "large_sample.csv"
    create_sample_csv(sample_file, 50000)
    
    file_size = os.path.getsize(sample_file) / (1024 * 1024)  # Size in MB
    print(f"Sample file size: {file_size:.2f} MB")
    
    # Demonstrate different processing methods
    print("\n=== Processing Methods Demonstration ===")
    
    # Method 1: Pandas chunking
    print("\n1. Pandas Chunking:")
    chunk_results = []
    for i, chunk_result in enumerate(process_large_csv_pandas(sample_file, chunk_size=10000)):
        chunk_results.append(chunk_result)
        if i >= 2:  # Show first 3 chunks
            break
    print(f"Processed {len(chunk_results)} chunks")
    
    # Method 2: Streaming processing
    print("\n2. Streaming Processing:")
    streaming_count = 0
    for record in process_csv_streaming(sample_file):
        streaming_count += 1
        if streaming_count >= 5:  # Show first 5 records
            print(f"Sample record: {record}")
            break
    
    # Method 3: Aggregation
    print("\n3. Memory-Efficient Aggregation:")
    aggregator = CSVAggregator()
    final_stats = aggregator.process_file(sample_file)
    print(f"Final statistics: {json.dumps(final_stats, indent=2, default=str)}")
    
    # Benchmark all methods
    print("\n4. Performance Benchmark:")
    benchmark_results = benchmark_csv_processing_methods(sample_file, file_size)
    
    # Find fastest method
    fastest_method = min(benchmark_results, key=benchmark_results.get)
    print(f"\nFastest method: {fastest_method} ({benchmark_results[fastest_method]:.2f}s)")
    
    # Clean up
    if os.path.exists(sample_file):
        os.remove(sample_file)
    
    print("\n=== Best Practices Summary ===")
    print("✓ Use chunking for balanced memory usage and performance")
    print("✓ Stream processing for maximum memory efficiency")
    print("✓ Parallel processing for CPU-intensive operations")
    print("✓ Choose chunk size based on available memory")
    print("✓ Optimize data types to reduce memory usage")
    print("✓ Use compression for storage efficiency")
    print("✓ Monitor memory usage during processing")
    print("✓ Implement error handling for data quality issues")
```

### 15. How do you handle database connections efficiently?
**Answer:**
Efficient database connection management is crucial for data engineering applications that need to handle high throughput and maintain system stability. Poor connection management can lead to resource exhaustion, performance degradation, and application failures.

**Key Strategies for Efficient Database Connections:**

1. **Connection Pooling**: Reuse existing connections instead of creating new ones for each operation
2. **Context Managers**: Ensure connections are properly closed even when exceptions occur
3. **Connection Limits**: Set appropriate limits to prevent resource exhaustion
4. **Timeout Management**: Handle connection timeouts gracefully
5. **Health Checks**: Monitor connection health and replace stale connections
6. **Lazy Loading**: Create connections only when needed

**Why This Matters in Data Engineering:**
- **Performance**: Connection creation is expensive; pooling reduces overhead
- **Scalability**: Proper pooling allows handling more concurrent operations
- **Reliability**: Prevents connection leaks that can crash applications
- **Resource Management**: Optimizes database server resources

**Common Connection Problems:**
- **Connection Leaks**: Forgetting to close connections
- **Pool Exhaustion**: Too many concurrent connections
- **Stale Connections**: Network timeouts and disconnections
- **Resource Contention**: Database server overload
- **Transaction Deadlocks**: Improper transaction management

```python
import sqlite3
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import threading
import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConnectionConfig:
    """Database connection configuration."""
    host: str = 'localhost'
    port: int = 5432
    database: str = 'mydb'
    username: str = 'user'
    password: str = 'password'
    min_connections: int = 1
    max_connections: int = 10
    connection_timeout: int = 30
    idle_timeout: int = 300

class DatabaseConnectionManager(ABC):
    """Abstract base class for database connection management."""
    
    @abstractmethod
    def get_connection(self):
        """Get a database connection."""
        pass
    
    @abstractmethod
    def return_connection(self, conn):
        """Return a connection to the pool."""
        pass
    
    @abstractmethod
    def close_all(self):
        """Close all connections."""
        pass

class PostgreSQLConnectionPool(DatabaseConnectionManager):
    """Production-ready PostgreSQL connection pool."""
    
    def __init__(self, config: ConnectionConfig):
        self.config = config
        self._pool = None
        self._lock = threading.Lock()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool."""
        try:
            self._pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=self.config.min_connections,
                maxconn=self.config.max_connections,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
                connect_timeout=self.config.connection_timeout
            )
            logger.info(f"Initialized connection pool with {self.config.min_connections}-{self.config.max_connections} connections")
        except Exception as e:
            logger.error(f"Failed to initialize connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get connection from pool with error handling."""
        try:
            conn = self._pool.getconn()
            if conn:
                # Test connection health
                with conn.cursor() as cursor:
                    cursor.execute('SELECT 1')
                return conn
            else:
                raise Exception("No connections available in pool")
        except Exception as e:
            logger.error(f"Error getting connection: {e}")
            raise
    
    def return_connection(self, conn, close=False):
        """Return connection to pool."""
        try:
            if close or conn.closed:
                self._pool.putconn(conn, close=True)
            else:
                # Reset connection state
                conn.rollback()
                self._pool.putconn(conn)
        except Exception as e:
            logger.error(f"Error returning connection: {e}")
            # Force close problematic connection
            self._pool.putconn(conn, close=True)
    
    def close_all(self):
        """Close all connections in pool."""
        if self._pool:
            self._pool.closeall()
            logger.info("Closed all connections in pool")
    
    def get_pool_status(self) -> Dict[str, int]:
        """Get current pool status."""
        if not self._pool:
            return {'available': 0, 'used': 0, 'total': 0}
        
        # Note: These methods may not be available in all psycopg2 versions
        try:
            return {
                'available': len(self._pool._pool),
                'used': len(self._pool._used),
                'total': self.config.max_connections
            }
        except AttributeError:
            return {'status': 'Pool status not available'}

# Context manager for automatic connection management
@contextmanager
def get_db_connection(pool: DatabaseConnectionManager):
    """Context manager for safe database connection handling."""
    conn = None
    try:
        conn = pool.get_connection()
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database operation failed: {e}")
        raise
    else:
        if conn:
            conn.commit()
    finally:
        if conn:
            pool.return_connection(conn)

# High-level database operations class
class DatabaseOperations:
    """High-level database operations with connection management."""
    
    def __init__(self, connection_pool: DatabaseConnectionManager):
        self.pool = connection_pool
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """Execute SELECT query and return results."""
        with get_db_connection(self.pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
    
    def execute_command(self, command: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE command."""
        with get_db_connection(self.pool) as conn:
            with conn.cursor() as cursor:
                cursor.execute(command, params or ())
                return cursor.rowcount
    
    def execute_batch(self, command: str, params_list: list) -> int:
        """Execute batch operations efficiently."""
        total_affected = 0
        with get_db_connection(self.pool) as conn:
            with conn.cursor() as cursor:
                for params in params_list:
                    cursor.execute(command, params)
                    total_affected += cursor.rowcount
        return total_affected
    
    def execute_transaction(self, operations: list) -> bool:
        """Execute multiple operations in a transaction."""
        with get_db_connection(self.pool) as conn:
            try:
                with conn.cursor() as cursor:
                    for operation in operations:
                        query = operation['query']
                        params = operation.get('params', ())
                        cursor.execute(query, params)
                return True
            except Exception as e:
                logger.error(f"Transaction failed: {e}")
                raise

# Simple connection pool for SQLite (development/testing)
class SQLiteConnectionPool(DatabaseConnectionManager):
    """Simple SQLite connection pool for development."""
    
    def __init__(self, database_path: str, max_connections: int = 5):
        self.database_path = database_path
        self.max_connections = max_connections
        self._pool = []
        self._lock = threading.Lock()
    
    def get_connection(self):
        with self._lock:
            if self._pool:
                return self._pool.pop()
            return sqlite3.connect(self.database_path, check_same_thread=False)
    
    def return_connection(self, conn, close=False):
        with self._lock:
            if close or len(self._pool) >= self.max_connections:
                conn.close()
            else:
                # Reset connection state
                conn.rollback()
                self._pool.append(conn)
    
    def close_all(self):
        with self._lock:
            for conn in self._pool:
                conn.close()
            self._pool.clear()

# Usage examples and best practices
def example_usage():
    """Demonstrate efficient database connection usage."""
    
    # Configuration
    config = ConnectionConfig(
        host='localhost',
        database='test_db',
        username='test_user',
        password='test_pass',
        min_connections=2,
        max_connections=10
    )
    
    # For production (PostgreSQL)
    try:
        pool = PostgreSQLConnectionPool(config)
        db_ops = DatabaseOperations(pool)
        
        # Example operations
        print("=== Database Operations Example ===")
        
        # Single query
        results = db_ops.execute_query(
            "SELECT id, name FROM users WHERE active = %s", 
            (True,)
        )
        print(f"Found {len(results)} active users")
        
        # Batch operations
        user_updates = [
            ('John Doe', 1),
            ('Jane Smith', 2),
            ('Bob Johnson', 3)
        ]
        affected = db_ops.execute_batch(
            "UPDATE users SET name = %s WHERE id = %s",
            user_updates
        )
        print(f"Updated {affected} user records")
        
        # Transaction example
        transaction_ops = [
            {'query': 'INSERT INTO audit_log (action, user_id) VALUES (%s, %s)', 
             'params': ('user_update', 1)},
            {'query': 'UPDATE users SET last_modified = NOW() WHERE id = %s', 
             'params': (1,)}
        ]
        db_ops.execute_transaction(transaction_ops)
        print("Transaction completed successfully")
        
        # Pool status
        status = pool.get_pool_status()
        print(f"Pool status: {status}")
        
    except Exception as e:
        print(f"PostgreSQL example failed (expected in demo): {e}")
    
    # For development/testing (SQLite)
    print("\n=== SQLite Example ===")
    sqlite_pool = SQLiteConnectionPool(':memory:', max_connections=3)
    sqlite_ops = DatabaseOperations(sqlite_pool)
    
    # Create test table
    sqlite_ops.execute_command(
        "CREATE TABLE test_users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )
    
    # Insert test data
    test_users = [
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Charlie', 'charlie@example.com')
    ]
    
    for name, email in test_users:
        sqlite_ops.execute_command(
            "INSERT INTO test_users (name, email) VALUES (?, ?)",
            (name, email)
        )
    
    # Query data
    users = sqlite_ops.execute_query("SELECT * FROM test_users")
    print(f"Created {len(users)} test users")
    for user in users:
        print(f"  {user}")
    
    # Cleanup
    sqlite_pool.close_all()
    print("Closed all connections")

# Connection monitoring and health checks
class ConnectionMonitor:
    """Monitor database connection health and performance."""
    
    def __init__(self, pool: DatabaseConnectionManager):
        self.pool = pool
        self.stats = {
            'connections_created': 0,
            'connections_failed': 0,
            'queries_executed': 0,
            'query_errors': 0
        }
    
    def health_check(self) -> bool:
        """Perform database health check."""
        try:
            with get_db_connection(self.pool) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT 1')
                    result = cursor.fetchone()
                    return result[0] == 1
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        return self.stats.copy()

if __name__ == "__main__":
    example_usage()

# Key best practices:
# 1. Always use connection pooling in production
# 2. Use context managers for automatic cleanup
# 3. Handle connection failures gracefully
# 4. Monitor pool health and performance
# 5. Set appropriate timeouts and limits
# 6. Use transactions for data consistency
# 7. Test connection handling under load
```

### 16. Explain async/await and when to use it in data engineering.

**Answer:**
Async/await is Python's approach to asynchronous programming that enables concurrent execution of I/O-bound operations without blocking the main thread. This is particularly crucial for data engineering tasks that involve multiple API calls, file operations, database queries, or any scenario where you're waiting for external resources.

**How Async/Await Works:**

**Asynchronous Programming Concepts:**
- **Coroutines**: Functions defined with `async def` that can be paused and resumed
- **Event Loop**: Manages and executes asynchronous tasks
- **Awaitable Objects**: Objects that can be used with `await` keyword
- **Concurrency vs Parallelism**: Async provides concurrency (interleaved execution) not true parallelism

**Key Benefits for Data Engineering:**
- **I/O Efficiency**: Don't block while waiting for network/disk operations
- **Resource Utilization**: Better CPU utilization during I/O waits
- **Scalability**: Handle many concurrent operations with fewer resources
- **Responsiveness**: Applications remain responsive during long operations

**When to Use Async/Await in Data Engineering:**
- **API Integration**: Fetching data from multiple REST APIs simultaneously
- **Database Operations**: Concurrent database queries and transactions
- **File Processing**: Reading/writing multiple files concurrently
- **ETL Pipelines**: Parallel extraction from multiple sources
- **Real-time Processing**: Handling streaming data from multiple sources
- **Web Scraping**: Concurrent scraping of multiple websites
- **Message Queue Processing**: Consuming from multiple queues simultaneously

**When NOT to Use Async/Await:**
- **CPU-bound Tasks**: Use multiprocessing instead
- **Simple Sequential Operations**: Overhead may not be worth it
- **Legacy Code Integration**: May require significant refactoring
- **Debugging Complexity**: Async code can be harder to debug

**Common Patterns:**
- **Gather**: Execute multiple coroutines concurrently
- **Semaphores**: Limit concurrent operations
- **Queues**: Producer-consumer patterns
- **Context Managers**: Async resource management

```python
import asyncio
import aiohttp
import aiofiles
import time
from typing import List, Dict, Any

# Async HTTP requests with error handling
async def fetch_data(session: aiohttp.ClientSession, url: str, 
                    timeout: int = 30) -> Dict[str, Any]:
    """Fetch data from URL with timeout and error handling.
    
    Args:
        session: Aiohttp client session
        url: URL to fetch data from
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary containing response data or error information
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
            if response.status == 200:
                data = await response.json()
                return {'url': url, 'status': 'success', 'data': data}
            else:
                return {'url': url, 'status': 'error', 'error': f'HTTP {response.status}'}
    except asyncio.TimeoutError:
        return {'url': url, 'status': 'error', 'error': 'Timeout'}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}

async def fetch_multiple_apis(urls: List[str], max_concurrent: int = 10) -> List[Dict[str, Any]]:
    """Fetch data from multiple APIs concurrently with rate limiting.
    
    Args:
        urls: List of URLs to fetch
        max_concurrent: Maximum number of concurrent requests
        
    Returns:
        List of results from all API calls
    """
    # Create semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_semaphore(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        async with semaphore:
            return await fetch_data(session, url)
    
    # Configure session with connection pooling
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_with_semaphore(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle any exceptions that occurred
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            processed_results.append({
                'status': 'error', 
                'error': str(result)
            })
        else:
            processed_results.append(result)
    
    return processed_results

# Async file I/O with batch processing
async def process_files_batch(filenames: List[str], batch_size: int = 5) -> List[Dict[str, Any]]:
    """Process multiple files in batches to avoid overwhelming the system.
    
    Args:
        filenames: List of file paths to process
        batch_size: Number of files to process concurrently
        
    Returns:
        List of processing results
    """
    async def read_and_process_file(filename: str) -> Dict[str, Any]:
        """Read and process a single file."""
        try:
            async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
                content = await f.read()
                
            # Simulate processing
            word_count = len(content.split())
            line_count = len(content.splitlines())
            
            return {
                'filename': filename,
                'status': 'success',
                'word_count': word_count,
                'line_count': line_count,
                'size_bytes': len(content.encode('utf-8'))
            }
        except Exception as e:
            return {
                'filename': filename,
                'status': 'error',
                'error': str(e)
            }
    
    results = []
    
    # Process files in batches
    for i in range(0, len(filenames), batch_size):
        batch = filenames[i:i + batch_size]
        batch_tasks = [read_and_process_file(filename) for filename in batch]
        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(batch_results)
        
        # Optional: Add delay between batches to prevent overwhelming the system
        if i + batch_size < len(filenames):
            await asyncio.sleep(0.1)
    
    return results

# Async database operations
async def async_database_operations(queries: List[str]) -> List[Dict[str, Any]]:
    """Execute multiple database queries concurrently.
    
    Note: This example uses asyncpg for PostgreSQL. Adapt for your database.
    """
    import asyncpg  # pip install asyncpg
    
    async def execute_query(pool: asyncpg.Pool, query: str) -> Dict[str, Any]:
        """Execute a single query."""
        try:
            async with pool.acquire() as connection:
                result = await connection.fetch(query)
                return {
                    'query': query[:50] + '...' if len(query) > 50 else query,
                    'status': 'success',
                    'row_count': len(result),
                    'data': [dict(row) for row in result]
                }
        except Exception as e:
            return {
                'query': query[:50] + '...' if len(query) > 50 else query,
                'status': 'error',
                'error': str(e)
            }
    
    # Create connection pool
    pool = await asyncpg.create_pool(
        host='localhost',
        port=5432,
        user='username',
        password='password',
        database='dbname',
        min_size=1,
        max_size=10
    )
    
    try:
        # Execute all queries concurrently
        tasks = [execute_query(pool, query) for query in queries]
        results = await asyncio.gather(*tasks)
        return results
    finally:
        await pool.close()

# Performance comparison: sync vs async
def sync_api_calls(urls: List[str]) -> List[Dict[str, Any]]:
    """Synchronous API calls for comparison."""
    import requests
    
    results = []
    start_time = time.time()
    
    for url in urls:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                results.append({
                    'url': url,
                    'status': 'success',
                    'data': response.json()
                })
            else:
                results.append({
                    'url': url,
                    'status': 'error',
                    'error': f'HTTP {response.status_code}'
                })
        except Exception as e:
            results.append({
                'url': url,
                'status': 'error',
                'error': str(e)
            })
    
    end_time = time.time()
    print(f"Sync execution time: {end_time - start_time:.2f} seconds")
    return results

async def async_api_calls(urls: List[str]) -> List[Dict[str, Any]]:
    """Asynchronous API calls for comparison."""
    start_time = time.time()
    results = await fetch_multiple_apis(urls)
    end_time = time.time()
    print(f"Async execution time: {end_time - start_time:.2f} seconds")
    return results

# Usage examples and when to use async/await in data engineering:
if __name__ == "__main__":
    # Example URLs for testing
    test_urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://jsonplaceholder.typicode.com/posts/3',
        'https://jsonplaceholder.typicode.com/posts/4',
        'https://jsonplaceholder.typicode.com/posts/5'
    ]
    
    # Compare sync vs async performance
    print("=== Performance Comparison ===")
    
    # Sync version
    sync_results = sync_api_calls(test_urls)
    print(f"Sync results: {len([r for r in sync_results if r['status'] == 'success'])} successful")
    
    # Async version
    async_results = asyncio.run(async_api_calls(test_urls))
    print(f"Async results: {len([r for r in async_results if r['status'] == 'success'])} successful")

# When to use async/await in data engineering:
# 
# 1. **Multiple API calls**: Fetching data from multiple REST APIs simultaneously
# 2. **File I/O operations**: Reading/writing multiple files concurrently
# 3. **Database operations**: Executing multiple queries in parallel
# 4. **ETL pipelines**: When stages involve I/O-bound operations
# 5. **Real-time data processing**: Handling multiple data streams
# 6. **Web scraping**: Scraping multiple websites concurrently
# 7. **Message queue processing**: Consuming from multiple queues
# 
# Benefits:
# - Significantly faster for I/O-bound operations
# - Better resource utilization
# - Improved scalability
# - Reduced blocking time
# 
# When NOT to use:
# - CPU-bound tasks (use multiprocessing instead)
# - Simple, single-threaded operations
# - When code complexity outweighs benefits


```

### 17. How do you optimize Python code for performance?

**Answer:**
Python performance optimization is crucial for data engineering applications that process large datasets and need efficient execution. The key is understanding Python's execution model and applying the right optimization techniques based on your specific bottlenecks.

**Performance Optimization Strategy:**

**1. Profile First Approach:**
- **Identify Bottlenecks**: Use profiling tools before optimizing
- **Measure Impact**: Quantify improvements with benchmarks
- **Optimize Systematically**: Start with biggest impact, lowest effort changes
- **Monitor Production**: Track performance in real-world scenarios

**2. Common Optimization Techniques:**
- **Algorithm Optimization**: Choose better algorithms and data structures
- **Built-in Functions**: Leverage optimized C implementations
- **Memory Management**: Reduce memory allocations and copies
- **Concurrency**: Use appropriate parallelism for workload type
- **External Libraries**: Use NumPy, Pandas for numerical operations

**3. Memory Optimization:**
- Use generators for large datasets to avoid loading everything into memory
- Choose appropriate data structures (sets for membership testing, deques for queues)
- Use `__slots__` for classes with many instances
- Consider memory-mapped files for large file processing

**4. I/O Optimization:**
- Use buffered I/O and appropriate buffer sizes
- Batch database operations instead of individual queries
- Use connection pooling for database connections
- Implement async I/O for concurrent operations

**5. Concurrency and Parallelism:**
- Use multiprocessing for CPU-bound tasks (bypasses GIL)
- Use threading or asyncio for I/O-bound tasks
- Consider process pools for embarrassingly parallel problems
- Use concurrent.futures for cleaner parallel code

**6. When to Use External Libraries:**
- NumPy/Pandas for numerical computations
- Cython for performance-critical code sections
- Numba for JIT compilation of numerical functions
- PyPy as an alternative Python interpreter

```python
import time
import cProfile
import numpy as np
from functools import lru_cache
from collections import defaultdict, deque
import timeit

# 1. Profile to identify bottlenecks
def profile_code_example():
    """Example of profiling Python code to find bottlenecks."""
    
    def slow_function():
        # Inefficient operations
        result = []
        for i in range(100000):
            if i % 2 == 0:
                result.append(i ** 2)
        return result
    
    # Profile the function
    cProfile.run('slow_function()', sort='cumulative')
    
    # Memory profiling (requires memory_profiler: pip install memory-profiler)
    # @profile  # Uncomment to use line_profiler
    # def memory_intensive_function():
    #     data = [i for i in range(1000000)]
    #     return sum(data)

# 2. Use built-in functions and optimized libraries
def optimization_examples():
    """Compare slow vs fast implementations."""
    
    # Slow: Manual loop
    def slow_sum(numbers):
        total = 0
        for num in numbers:
            total += num
        return total
    
    # Fast: Built-in function
    def fast_sum(numbers):
        return sum(numbers)  # Optimized C implementation
    
    # Slow: String concatenation
    def slow_string_join(items):
        result = ""
        for item in items:
            result += str(item)
        return result
    
    # Fast: Join method
    def fast_string_join(items):
        return "".join(str(item) for item in items)
    
    # Slow: List comprehension with function calls
    def slow_processing(data):
        import math
        return [math.sqrt(x) for x in data if x > 0]
    
    # Fast: Local function reference
    def fast_processing(data):
        import math
        sqrt = math.sqrt  # Local reference avoids global lookup
        return [sqrt(x) for x in data if x > 0]
    
    return slow_sum, fast_sum, slow_string_join, fast_string_join

# 3. Choose appropriate data structures
def data_structure_optimization():
    """Examples of choosing optimal data structures."""
    
    # Use set for O(1) membership testing
    large_list = list(range(1000000))
    large_set = set(range(1000000))
    
    # Slow: O(n) lookup in list
    def slow_membership_test(item):
        return item in large_list
    
    # Fast: O(1) average case lookup in set
    def fast_membership_test(item):
        return item in large_set
    
    # Use dict for O(1) key-value lookups
    items = ['apple', 'banana', 'cherry'] * 1000
    lookup_dict = {item: index for index, item in enumerate(items)}
    
    # Use deque for efficient append/pop operations
    from collections import deque
    
    # Slow: List operations at beginning
    def slow_queue_operations():
        queue = []
        for i in range(10000):
            queue.append(i)
        while queue:
            queue.pop(0)  # O(n) operation
    
    # Fast: Deque operations
    def fast_queue_operations():
        queue = deque()
        for i in range(10000):
            queue.append(i)
        while queue:
            queue.popleft()  # O(1) operation

# 4. Use caching for expensive computations
@lru_cache(maxsize=128)
def expensive_fibonacci(n):
    """Cached Fibonacci calculation."""
    if n < 2:
        return n
    return expensive_fibonacci(n-1) + expensive_fibonacci(n-2)

# Custom cache for more control
class CustomCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_order = deque()
    
    def get(self, key, compute_func):
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        
        # Compute and cache result
        result = compute_func(key)
        
        if len(self.cache) >= self.max_size:
            # Remove least recently used
            oldest = self.access_order.popleft()
            del self.cache[oldest]
        
        self.cache[key] = result
        self.access_order.append(key)
        return result

# 5. Use NumPy for numerical operations
def numpy_optimization_examples():
    """Compare pure Python vs NumPy for numerical operations."""
    
    # Pure Python (slow)
    def python_operations(size=1000000):
        data = list(range(size))
        # Element-wise operations
        squared = [x**2 for x in data]
        filtered = [x for x in squared if x % 2 == 0]
        return sum(filtered)
    
    # NumPy (fast)
    def numpy_operations(size=1000000):
        data = np.arange(size)
        # Vectorized operations
        squared = data ** 2
        filtered = squared[squared % 2 == 0]
        return np.sum(filtered)
    
    return python_operations, numpy_operations

# 6. Use generators for memory efficiency
def memory_efficient_processing():
    """Examples of memory-efficient data processing."""
    
    # Memory-intensive: Load all data at once
    def memory_intensive_approach(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()  # Loads entire file into memory
        
        processed = []
        for line in lines:
            if line.strip():
                processed.append(line.upper().strip())
        return processed
    
    # Memory-efficient: Process line by line
    def memory_efficient_approach(filename):
        def process_lines():
            with open(filename, 'r') as f:
                for line in f:  # Generator - one line at a time
                    if line.strip():
                        yield line.upper().strip()
        return process_lines()
    
    # Batch processing generator
    def batch_processor(iterable, batch_size=1000):
        """Process data in batches to balance memory and performance."""
        batch = []
        for item in iterable:
            batch.append(item)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

# 7. Performance measurement and comparison
def performance_comparison():
    """Comprehensive performance comparison of different approaches."""
    
    # Test data
    test_data = list(range(100000))
    
    # Different implementations to compare
    implementations = {
        'List Comprehension': lambda data: [x*2 for x in data if x % 2 == 0],
        'Filter + Map': lambda data: list(map(lambda x: x*2, filter(lambda x: x % 2 == 0, data))),
        'Generator Expression': lambda data: list(x*2 for x in data if x % 2 == 0),
        'NumPy': lambda data: (np.array(data)[np.array(data) % 2 == 0] * 2).tolist()
    }
    
    results = {}
    for name, func in implementations.items():
        # Time the implementation
        execution_time = timeit.timeit(
            lambda: func(test_data),
            number=10
        ) / 10  # Average over 10 runs
        
        results[name] = execution_time
        print(f"{name}: {execution_time:.6f} seconds")
    
    # Find fastest implementation
    fastest = min(results, key=results.get)
    print(f"\nFastest implementation: {fastest}")
    
    return results

# 8. Practical optimization workflow
def optimization_workflow_example():
    """Example of systematic performance optimization workflow."""
    
    # Step 1: Baseline measurement
    def original_function(data):
        """Original, unoptimized function."""
        result = []
        for item in data:
            if isinstance(item, (int, float)) and item > 0:
                import math
                processed = math.sqrt(item) * 2
                if processed > 10:
                    result.append(processed)
        return result
    
    # Step 2: Profile and identify bottlenecks
    # (Use cProfile.run() to identify slow parts)
    
    # Step 3: Optimize step by step
    def optimized_function_v1(data):
        """First optimization: reduce function calls."""
        import math
        sqrt = math.sqrt  # Local reference
        result = []
        for item in data:
            if isinstance(item, (int, float)) and item > 0:
                processed = sqrt(item) * 2
                if processed > 10:
                    result.append(processed)
        return result
    
    def optimized_function_v2(data):
        """Second optimization: use list comprehension."""
        import math
        sqrt = math.sqrt
        return [sqrt(item) * 2 for item in data 
                if isinstance(item, (int, float)) and item > 0 and sqrt(item) * 2 > 10]
    
    def optimized_function_v3(data):
        """Third optimization: use NumPy for numerical data."""
        import numpy as np
        # Assume data is numeric (add type checking in real code)
        arr = np.array([x for x in data if isinstance(x, (int, float)) and x > 0])
        processed = np.sqrt(arr) * 2
        return processed[processed > 10].tolist()
    
    # Step 4: Benchmark all versions
    test_data = [i * 0.1 for i in range(10000)] + ['invalid', None, -5]
    
    versions = {
        'Original': original_function,
        'Optimized v1': optimized_function_v1,
        'Optimized v2': optimized_function_v2,
        'Optimized v3': optimized_function_v3
    }
    
    print("Performance Optimization Results:")
    baseline_time = None
    
    for name, func in versions.items():
        execution_time = timeit.timeit(
            lambda f=func: f(test_data),
            number=100
        ) / 100
        
        if baseline_time is None:
            baseline_time = execution_time
            speedup = 1.0
        else:
            speedup = baseline_time / execution_time
        
        print(f"{name}: {execution_time:.6f}s (speedup: {speedup:.2f}x)")

# Performance optimization checklist for data engineering:
PERFORMANCE_CHECKLIST = """
🔍 PROFILING & MEASUREMENT:
- Profile before optimizing (cProfile, line_profiler)
- Measure memory usage (memory_profiler, tracemalloc)
- Benchmark with realistic data sizes
- Monitor production performance

⚡ ALGORITHM & DATA STRUCTURES:
- Choose optimal algorithms (O(n) vs O(n²))
- Use appropriate data structures (set, dict, deque)
- Minimize nested loops
- Cache expensive computations

🐍 PYTHON-SPECIFIC OPTIMIZATIONS:
- Use built-in functions (sum, max, min)
- Prefer list comprehensions over loops
- Use local variable references in loops
- Leverage NumPy for numerical operations

💾 MEMORY OPTIMIZATION:
- Use generators for large datasets
- Process data in chunks/batches
- Avoid unnecessary data copies
- Use __slots__ for classes with many instances

🔄 CONCURRENCY:
- Use multiprocessing for CPU-bound tasks
- Use asyncio for I/O-bound tasks
- Consider threading for I/O with GIL release
- Use connection pooling for databases

📊 DATA ENGINEERING SPECIFIC:
- Stream processing for large files
- Batch operations for databases
- Vectorized operations with Pandas/NumPy
- Parallel processing with Dask/Ray
"""

if __name__ == "__main__":
    print("Python Performance Optimization Examples")
    print("=" * 50)
    
    # Run performance comparison
    performance_comparison()
    
    # Run optimization workflow example
    print("\n" + "=" * 50)
    optimization_workflow_example()
    
    # Print optimization checklist
    print("\n" + PERFORMANCE_CHECKLIST)
```

### 18. How do you handle errors and logging in production Python code?
**Answer:**
```python
import logging
import traceback
from functools import wraps
from typing import Callable, Any

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Error handling decorator with detailed logging
def handle_errors(func: Callable) -> Callable:
    """Decorator to handle and log errors comprehensively."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            logger.info(f"Starting execution of {func.__name__}")
            result = func(*args, **kwargs)
            logger.info(f"Successfully completed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            logger.error(f"Function args: {args}, kwargs: {kwargs}")
            raise
    return wrapper

# Custom exception hierarchy for better error handling
class DataProcessingError(Exception):
    """Base exception for data processing errors."""
    pass

class DataValidationError(DataProcessingError):
    """Raised when data validation fails."""
    def __init__(self, message: str, invalid_records: list = None):
        super().__init__(message)
        self.invalid_records = invalid_records or []

class DataSourceError(DataProcessingError):
    """Raised when data source is unavailable or corrupted."""
    pass

# Retry mechanism with exponential backoff
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, 
          exceptions: tuple = (Exception,)):
    """Retry decorator with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each failed attempt
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Max retry attempts ({max_attempts}) reached for {func.__name__}")
                        raise e
                    
                    logger.warning(
                        f"Attempt {attempts}/{max_attempts} failed for {func.__name__}: {str(e)}. "
                        f"Retrying in {current_delay:.2f}s..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator

# Usage example
@handle_errors
@retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(ConnectionError, TimeoutError))
def process_data(data: list) -> dict:
    """Process data with comprehensive error handling and retry logic."""
    if not data:
        raise DataValidationError("Input data cannot be empty")
    
    # Simulate processing
    processed_count = len([item for item in data if item is not None])
    
    if processed_count == 0:
        raise DataValidationError("No valid records found in input data")
    
    logger.info(f"Successfully processed {processed_count} records")
    return {"processed_count": processed_count, "status": "success"}
```

## Coding Challenges

### 19. Implement a LRU Cache from scratch.
**Answer:**
```python
from typing import Optional, Any

class Node:
    """Doubly linked list node for LRU cache."""
    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class LRUCache:
    """Least Recently Used (LRU) Cache implementation.
    
    Uses a combination of hash map and doubly linked list for O(1) operations.
    """
    
    def __init__(self, capacity: int):
        """Initialize LRU cache with given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.cache = {}  # key -> node mapping
        
        # Create dummy head and tail nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node: Node) -> None:
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node: Node) -> None:
        """Move node to head (mark as recently used)."""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self) -> Node:
        """Remove and return the last node (least recently used)."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key: Any) -> Any:
        """Get value by key and mark as recently used.
        
        Args:
            key: Key to look up
            
        Returns:
            Value associated with key, or -1 if not found
        """
        node = self.cache.get(key)
        
        if not node:
            return -1
        
        # Move accessed node to head (mark as recently used)
        self._move_to_head(node)
        return node.value
    
    def put(self, key: Any, value: Any) -> None:
        """Put key-value pair into cache.
        
        Args:
            key: Key to store
            value: Value to associate with key
        """
        node = self.cache.get(key)
        
        if not node:
            new_node = Node(key, value)
            
            if len(self.cache) >= self.capacity:
                # Remove least recently used item
                tail = self._pop_tail()
                del self.cache[tail.key]
            
            self.cache[key] = new_node
            self._add_node(new_node)
        else:
            # Update existing node
            node.value = value
            self._move_to_head(node)

# Usage example
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # Returns 1
cache.put(3, 3)      # Evicts key 2
print(cache.get(2))  # Returns -1 (not found)
```

### 20. Write a function to find the most frequent elements in a large dataset.
**Answer:**
```python
from collections import Counter, defaultdict
import heapq
from typing import List, Tuple, Iterator, Any

def top_k_frequent_basic(data: List[Any], k: int) -> List[Tuple[Any, int]]:
    """Find top k frequent elements using Counter.
    
    Time Complexity: O(n + k log n)
    Space Complexity: O(n)
    
    Args:
        data: List of elements
        k: Number of top frequent elements to return
        
    Returns:
        List of (element, frequency) tuples
    """
    counter = Counter(data)
    return counter.most_common(k)

def top_k_frequent_heap(data: List[Any], k: int) -> List[Tuple[Any, int]]:
    """Find top k frequent elements using min-heap for memory efficiency.
    
    Time Complexity: O(n + n log k)
    Space Complexity: O(n + k)
    
    Args:
        data: List of elements
        k: Number of top frequent elements to return
        
    Returns:
        List of (element, frequency) tuples
    """
    counter = Counter(data)
    
    # Use min-heap to keep only top k elements
    heap = []
    for element, freq in counter.items():
        if len(heap) < k:
            heapq.heappush(heap, (freq, element))
        elif freq > heap[0][0]:
            heapq.heapreplace(heap, (freq, element))
    
    # Convert to (element, frequency) format and sort by frequency desc
    result = [(element, freq) for freq, element in heap]
    return sorted(result, key=lambda x: x[1], reverse=True)

def top_k_frequent_streaming(data_stream: Iterator[Any], k: int, 
                           window_size: int = 1000) -> Iterator[List[Tuple[Any, int]]]:
    """Find top k frequent elements in streaming data with sliding window.
    
    Args:
        data_stream: Iterator of data elements
        k: Number of top frequent elements to return
        window_size: Size of sliding window
        
    Yields:
        List of (element, frequency) tuples for current window
    """
    window = []
    counter = Counter()
    
    for item in data_stream:
        # Add new item
        window.append(item)
        counter[item] += 1
        
        # Remove old item if window is full
        if len(window) > window_size:
            old_item = window.pop(0)
            counter[old_item] -= 1
            if counter[old_item] == 0:
                del counter[old_item]
        
        # Yield top k every 100 items (configurable)
        if len(window) % 100 == 0:
            yield counter.most_common(k)

def top_k_frequent_distributed(data: List[Any], k: int, num_partitions: int = 4) -> List[Tuple[Any, int]]:
    """Find top k frequent elements using map-reduce approach for large datasets.
    
    Args:
        data: List of elements
        k: Number of top frequent elements to return
        num_partitions: Number of partitions for parallel processing
        
    Returns:
        List of (element, frequency) tuples
    """
    from concurrent.futures import ProcessPoolExecutor
    import math
    
    def count_partition(partition_data: List[Any]) -> Counter:
        """Count frequencies in a data partition."""
        return Counter(partition_data)
    
    # Split data into partitions
    partition_size = math.ceil(len(data) / num_partitions)
    partitions = [data[i:i + partition_size] for i in range(0, len(data), partition_size)]
    
    # Process partitions in parallel
    with ProcessPoolExecutor(max_workers=num_partitions) as executor:
        partition_counters = list(executor.map(count_partition, partitions))
    
    # Merge results
    total_counter = Counter()
    for counter in partition_counters:
        total_counter.update(counter)
    
    return total_counter.most_common(k)

# Usage examples
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4] * 1000

# Basic approach
top_basic = top_k_frequent_basic(data, 3)
print(f"Top 3 (basic): {top_basic}")

# Heap approach (memory efficient)
top_heap = top_k_frequent_heap(data, 3)
print(f"Top 3 (heap): {top_heap}")

# Streaming approach
data_stream = iter(data)
for window_top_k in top_k_frequent_streaming(data_stream, 3, window_size=500):
    print(f"Current window top 3: {window_top_k}")
    break  # Just show first result

# Distributed approach
top_distributed = top_k_frequent_distributed(data, 3, num_partitions=4)
print(f"Top 3 (distributed): {top_distributed}")
```

### 21. Implement a comprehensive data pipeline with error handling and monitoring.
**Answer:**
```python
import logging
import time
import json
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading
from contextlib import contextmanager

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class PipelineStatus(Enum):
    """Enumeration of possible pipeline statuses."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class PipelineMetrics:
    """Comprehensive metrics for pipeline execution."""
    pipeline_id: str
    start_time: float = 0.0
    end_time: float = 0.0
    processed_records: int = 0
    failed_records: int = 0
    skipped_records: int = 0
    stage_metrics: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    @property
    def duration(self) -> float:
        """Calculate total execution duration."""
        return self.end_time - self.start_time if self.end_time > 0 else 0.0
    
    @property
    def total_records(self) -> int:
        """Calculate total number of records processed."""
        return self.processed_records + self.failed_records + self.skipped_records
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        total = self.total_records
        return (self.processed_records / total * 100) if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for serialization."""
        return {
            'pipeline_id': self.pipeline_id,
            'duration': self.duration,
            'processed_records': self.processed_records,
            'failed_records': self.failed_records,
            'skipped_records': self.skipped_records,
            'success_rate': self.success_rate,
            'stage_metrics': self.stage_metrics,
            'errors': self.errors,
            'warnings': self.warnings
        }

class PipelineStage(ABC):
    """Abstract base class for pipeline stages."""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """Initialize pipeline stage.
        
        Args:
            name: Unique name for the stage
            config: Configuration dictionary for the stage
        """
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"pipeline.{name}")
        self._metrics = {
            'start_time': 0.0,
            'end_time': 0.0,
            'processed_count': 0,
            'error_count': 0
        }
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data in this stage.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
        """
        pass
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data before processing.
        
        Args:
            data: Input data to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        return data is not None
    
    def validate_output(self, data: Any) -> bool:
        """Validate output data after processing.
        
        Args:
            data: Output data to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        return data is not None
    
    @contextmanager
    def _stage_timing(self):
        """Context manager for timing stage execution."""
        self._metrics['start_time'] = time.time()
        try:
            yield
        finally:
            self._metrics['end_time'] = time.time()
    
    def __call__(self, data: Any) -> Any:
        """Execute the stage with comprehensive error handling and monitoring.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
            
        Raises:
            ValueError: If input validation fails
            RuntimeError: If processing fails
        """
        with self._stage_timing():
            self.logger.info(f"Starting stage: {self.name}")
            
            # Input validation
            if not self.validate_input(data):
                self._metrics['error_count'] += 1
                raise ValueError(f"Input validation failed for stage {self.name}")
            
            try:
                # Process data
                result = self.process(data)
                
                # Output validation
                if not self.validate_output(result):
                    self._metrics['error_count'] += 1
                    raise ValueError(f"Output validation failed for stage {self.name}")
                
                self._metrics['processed_count'] += 1
                self.logger.info(f"Successfully completed stage: {self.name}")
                return result
                
            except Exception as e:
                self._metrics['error_count'] += 1
                self.logger.error(f"Error in stage {self.name}: {str(e)}")
                raise RuntimeError(f"Stage {self.name} failed: {str(e)}") from e
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get stage execution metrics."""
        duration = self._metrics['end_time'] - self._metrics['start_time']
        return {
            **self._metrics,
            'duration': duration
        }

class DataPipeline:
    """Comprehensive data processing pipeline with monitoring and error handling."""
    
    def __init__(self, pipeline_id: str, stages: List[PipelineStage], 
                 config: Dict[str, Any] = None):
        """Initialize data pipeline.
        
        Args:
            pipeline_id: Unique identifier for the pipeline
            stages: List of pipeline stages to execute
            config: Pipeline configuration
        """
        self.pipeline_id = pipeline_id
        self.stages = stages
        self.config = config or {}
        self.metrics = PipelineMetrics(pipeline_id)
        self.logger = logging.getLogger(f"pipeline.{pipeline_id}")
        self.status = PipelineStatus.PENDING
        self._lock = threading.Lock()
    
    def add_stage(self, stage: PipelineStage) -> None:
        """Add a stage to the pipeline.
        
        Args:
            stage: Pipeline stage to add
        """
        with self._lock:
            self.stages.append(stage)
    
    def run(self, data: Any) -> Any:
        """Execute the complete pipeline.
        
        Args:
            data: Input data to process
            
        Returns:
            Final processed data
            
        Raises:
            RuntimeError: If pipeline execution fails
        """
        with self._lock:
            self.status = PipelineStatus.RUNNING
            self.metrics.start_time = time.time()
            
        self.logger.info(f"Starting pipeline execution: {self.pipeline_id}")
        
        try:
            current_data = data
            
            # Execute each stage
            for stage in self.stages:
                try:
                    current_data = stage(current_data)
                    
                    # Collect stage metrics
                    stage_metrics = stage.get_metrics()
                    self.metrics.stage_metrics[stage.name] = stage_metrics
                    
                except Exception as e:
                    self.metrics.failed_records += 1
                    error_msg = f"Stage {stage.name} failed: {str(e)}"
                    self.metrics.errors.append(error_msg)
                    self.logger.error(error_msg)
                    raise
            
            # Pipeline completed successfully
            self.metrics.processed_records += 1
            self.status = PipelineStatus.SUCCESS
            self.logger.info(f"Pipeline {self.pipeline_id} completed successfully")
            
            return current_data
            
        except Exception as e:
            self.status = PipelineStatus.FAILED
            self.logger.error(f"Pipeline {self.pipeline_id} failed: {str(e)}")
            raise RuntimeError(f"Pipeline execution failed: {str(e)}") from e
            
        finally:
            self.metrics.end_time = time.time()
            self._log_final_metrics()
    
    def _log_final_metrics(self) -> None:
        """Log final pipeline metrics."""
        metrics_dict = self.metrics.to_dict()
        self.logger.info(f"Pipeline metrics: {json.dumps(metrics_dict, indent=2)}")
    
    def get_status(self) -> PipelineStatus:
        """Get current pipeline status."""
        return self.status
    
    def get_metrics(self) -> PipelineMetrics:
        """Get comprehensive pipeline metrics."""
        return self.metrics

# Example implementation of specific stages
class ExtractStage(PipelineStage):
    """Stage for extracting data from various sources."""
    
    def process(self, data: Any) -> Dict[str, Any]:
        """Extract data and add metadata.
        
        Args:
            data: Raw input data
            
        Returns:
            Dictionary with extracted data and metadata
        """
        # Simulate data extraction
        extracted_data = {
            'raw_data': data,
            'extracted_at': datetime.now().isoformat(),
            'source': self.config.get('source', 'unknown'),
            'record_count': len(data) if isinstance(data, (list, dict)) else 1
        }
        
        self.logger.info(f"Extracted {extracted_data['record_count']} records")
        return extracted_data

class TransformStage(PipelineStage):
    """Stage for transforming extracted data."""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform the extracted data.
        
        Args:
            data: Dictionary containing extracted data
            
        Returns:
            Dictionary with transformed data
        """
        raw_data = data['raw_data']
        
        # Apply transformations based on config
        transformations = self.config.get('transformations', [])
        transformed_data = raw_data
        
        for transform in transformations:
            if transform == 'uppercase' and isinstance(transformed_data, str):
                transformed_data = transformed_data.upper()
            elif transform == 'filter_nulls' and isinstance(transformed_data, list):
                transformed_data = [item for item in transformed_data if item is not None]
        
        result = {
            'transformed_data': transformed_data,
            'metadata': data,
            'transformed_at': datetime.now().isoformat(),
            'transformations_applied': transformations
        }
        
        self.logger.info(f"Applied {len(transformations)} transformations")
        return result

class LoadStage(PipelineStage):
    """Stage for loading transformed data to destination."""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Load transformed data to destination.
        
        Args:
            data: Dictionary containing transformed data
            
        Returns:
            Dictionary with load results
        """
        destination = self.config.get('destination', 'default')
        
        # Simulate loading data
        load_result = {
            'status': 'loaded',
            'destination': destination,
            'loaded_at': datetime.now().isoformat(),
            'data': data['transformed_data'],
            'metadata': data['metadata']
        }
        
        self.logger.info(f"Successfully loaded data to {destination}")
        return load_result

# Usage example
if __name__ == "__main__":
    # Create pipeline stages with configuration
    extract_stage = ExtractStage(
        name="extract",
        config={'source': 'api_endpoint'}
    )
    
    transform_stage = TransformStage(
        name="transform",
        config={'transformations': ['uppercase', 'filter_nulls']}
    )
    
    load_stage = LoadStage(
        name="load",
        config={'destination': 'data_warehouse'}
    )
    
    # Create and execute pipeline
    pipeline = DataPipeline(
        pipeline_id="etl_pipeline_001",
        stages=[extract_stage, transform_stage, load_stage],
        config={'batch_size': 1000, 'retry_count': 3}
    )
    
    # Execute pipeline with sample data
    sample_data = ["hello", "world", None, "data", "engineering"]
    
    try:
        result = pipeline.run(sample_data)
        print(f"Pipeline result: {json.dumps(result, indent=2)}")
        
        # Get and display metrics
        metrics = pipeline.get_metrics()
        print(f"\nPipeline Metrics:")
        print(f"Duration: {metrics.duration:.2f} seconds")
        print(f"Success Rate: {metrics.success_rate:.1f}%")
        print(f"Processed Records: {metrics.processed_records}")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
        metrics = pipeline.get_metrics()
        print(f"Errors: {metrics.errors}")ering:
# - Multiple API calls
# - Concurrent file processing
# - Database operations with high I/O wait
```

### 17. How do you optimize Python code for performance?
**Answer:**
```python
# 1. Use built-in functions and libraries
# Slow
result = []
for i in range(1000000):
    if i % 2 == 0:
        result.append(i * 2)

# Fast
result = [i * 2 for i in range(1000000) if i % 2 == 0]

# 2. Use NumPy for numerical operations
import numpy as np
# Slow
python_list = list(range(1000000))
result = [x * 2 for x in python_list]

# Fast
numpy_array = np.arange(1000000)
result = numpy_array * 2

# 3. Profile your code
import cProfile
cProfile.run('your_function()')

# 4. Use appropriate data structures
# Use set for membership testing
large_set = set(range(1000000))
if 500000 in large_set:  # O(1) average case
    pass

# 5. Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # Expensive computation
    return sum(i**2 for i in range(n))
```

### 18. How do you handle errors and logging in production Python code?

**Answer:**
Proper error handling and logging are critical for production data engineering systems to ensure reliability, debuggability, and maintainability. A comprehensive approach includes structured logging, custom exception hierarchies, retry mechanisms, and monitoring integration.

**Error Handling Strategy:**

**1. Exception Hierarchy:**
- **Custom Exceptions**: Create domain-specific exception classes
- **Exception Chaining**: Preserve original error context
- **Graceful Degradation**: Handle errors without crashing the system
- **Error Classification**: Distinguish between recoverable and fatal errors

**2. Logging Best Practices:**
- **Structured Logging**: Use consistent log formats with metadata
- **Log Levels**: Appropriate use of DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Contextual Information**: Include relevant data for debugging
- **Performance Impact**: Minimize logging overhead in hot paths
- **Security**: Avoid logging sensitive information

**3. Retry Mechanisms:**
- **Exponential Backoff**: Gradually increase delay between retries
- **Circuit Breaker**: Stop retrying after consecutive failures
- **Jitter**: Add randomness to prevent thundering herd
- **Selective Retry**: Only retry on specific error types

**4. Monitoring Integration:**
- **Metrics Collection**: Track error rates and patterns
- **Alerting**: Notify on critical errors or threshold breaches
- **Health Checks**: Implement endpoint monitoring
- **Distributed Tracing**: Track requests across services

**5. Production Considerations:**
- **Log Rotation**: Prevent disk space issues
- **Centralized Logging**: Aggregate logs from multiple instances
- **Error Reporting**: Integration with error tracking services
- **Performance Monitoring**: Track system performance metrics

## Coding Challenges

### 19. Implement a LRU Cache from scratch.
**Answer:**
LRU (Least Recently Used) Cache is a caching strategy that removes the least recently used items when the cache reaches its capacity. This is commonly asked in data engineering interviews as it demonstrates understanding of data structures and algorithms.

```python
from typing import Optional, Any

class Node:
    """Doubly linked list node for LRU cache."""
    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class LRUCache:
    """Efficient LRU Cache implementation using hash map + doubly linked list.
    
    Time Complexity: O(1) for both get and put operations
    Space Complexity: O(capacity)
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> node mapping
        
        # Create dummy head and tail nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node: Node) -> None:
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node: Node) -> None:
        """Move node to head (mark as recently used)."""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self) -> Node:
        """Remove and return the last node (least recently used)."""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key: Any) -> Any:
        """Get value by key and mark as recently used."""
        node = self.cache.get(key)
        if not node:
            return -1
        
        # Move accessed node to head
        self._move_to_head(node)
        return node.value
    
    def put(self, key: Any, value: Any) -> None:
        """Put key-value pair into cache."""
        node = self.cache.get(key)
        
        if not node:
            new_node = Node(key, value)
            
            if len(self.cache) >= self.capacity:
                # Remove least recently used item
                tail = self._pop_tail()
                del self.cache[tail.key]
            
            self.cache[key] = new_node
            self._add_node(new_node)
        else:
            # Update existing node
            node.value = value
            self._move_to_head(node)
    
    def display(self) -> list:
        """Display cache contents from most to least recently used."""
        result = []
        current = self.head.next
        while current != self.tail:
            result.append((current.key, current.value))
            current = current.next
        return result

# Simple LRU Cache implementation (less efficient but easier to understand)
class SimpleLRUCache:
    """Simple LRU Cache using list for ordering (O(n) operations)."""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []  # Most recent at the end
    
    def get(self, key: Any) -> Any:
        if key in self.cache:
            # Move to end (most recent)
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            # Update existing key
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used (first in order)
            oldest = self.order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)

# Usage example and testing
if __name__ == "__main__":
    # Test efficient LRU Cache
    cache = LRUCache(3)
    
    cache.put(1, "one")
    cache.put(2, "two")
    cache.put(3, "three")
    print(f"Cache after adding 1,2,3: {cache.display()}")
    
    print(f"Get key 1: {cache.get(1)}")  # Should return "one"
    print(f"Cache after accessing 1: {cache.display()}")
    
    cache.put(4, "four")  # Should evict key 2
    print(f"Cache after adding 4: {cache.display()}")
    
    print(f"Get key 2: {cache.get(2)}")  # Should return -1 (not found)
```

### 20. Write a function to find the most frequent elements in a large dataset.
**Answer:**
Finding the most frequent elements is a common data engineering task, especially when dealing with large datasets that may not fit in memory. Here are several approaches depending on the constraints:

```python
from collections import Counter, defaultdict
import heapq
from typing import List, Tuple, Iterator, Any
import time

def top_k_frequent_basic(data: List[Any], k: int) -> List[Tuple[Any, int]]:
    """Basic approach using Counter - good for small to medium datasets.
    
    Time Complexity: O(n + k log n)
    Space Complexity: O(n)
    """
    counter = Counter(data)
    return counter.most_common(k)

def top_k_frequent_heap(data: List[Any], k: int) -> List[Tuple[Any, int]]:
    """Memory-efficient approach using min-heap.
    
    Time Complexity: O(n + n log k)
    Space Complexity: O(n + k) - better when k << n
    """
    counter = Counter(data)
    
    # Use min-heap to keep only top k elements
    heap = []
    for element, freq in counter.items():
        if len(heap) < k:
            heapq.heappush(heap, (freq, element))
        elif freq > heap[0][0]:
            heapq.heapreplace(heap, (freq, element))
    
    # Convert to (element, frequency) format and sort by frequency desc
    result = [(element, freq) for freq, element in heap]
    return sorted(result, key=lambda x: x[1], reverse=True)

def top_k_frequent_streaming(data_stream: Iterator[Any], k: int, 
                           window_size: int = 1000) -> Iterator[List[Tuple[Any, int]]]:
    """For streaming data with sliding window.
    
    Useful when data is too large to fit in memory or arrives continuously.
    """
    window = []
    counter = Counter()
    
    for item in data_stream:
        # Add new item
        window.append(item)
        counter[item] += 1
        
        # Remove old item if window is full
        if len(window) > window_size:
            old_item = window.pop(0)
            counter[old_item] -= 1
            if counter[old_item] == 0:
                del counter[old_item]
        
        # Yield top k every 100 items (configurable)
        if len(window) % 100 == 0:
            yield counter.most_common(k)

def top_k_frequent_distributed(data: List[Any], k: int, num_partitions: int = 4) -> List[Tuple[Any, int]]:
    """Distributed approach for very large datasets using map-reduce pattern.
    
    Simulates distributed processing by partitioning data.
    """
    from concurrent.futures import ProcessPoolExecutor
    import math
    
    def count_partition(partition_data: List[Any]) -> Counter:
        """Count frequencies in a data partition."""
        return Counter(partition_data)
    
    # Split data into partitions
    partition_size = math.ceil(len(data) / num_partitions)
    partitions = [data[i:i + partition_size] for i in range(0, len(data), partition_size)]
    
    # Process partitions in parallel
    with ProcessPoolExecutor(max_workers=num_partitions) as executor:
        partition_counters = list(executor.map(count_partition, partitions))
    
    # Merge results (reduce phase)
    total_counter = Counter()
    for counter in partition_counters:
        total_counter.update(counter)
    
    return total_counter.most_common(k)

def top_k_frequent_approximate(data_stream: Iterator[Any], k: int, 
                             error_rate: float = 0.01) -> List[Tuple[Any, int]]:
    """Approximate algorithm using Count-Min Sketch for very large streams.
    
    Trades accuracy for memory efficiency - useful for massive datasets.
    """
    # Simplified Count-Min Sketch implementation
    import hashlib
    import math
    
    # Calculate sketch dimensions
    width = math.ceil(math.e / error_rate)
    depth = math.ceil(math.log(1 / 0.01))  # 99% confidence
    
    # Initialize sketch matrix
    sketch = [[0] * width for _ in range(depth)]
    
    # Hash functions
    def hash_func(item, seed):
        return hash(str(item) + str(seed)) % width
    
    # Track actual items for final result
    item_tracker = defaultdict(int)
    
    # Process stream
    for item in data_stream:
        # Update sketch
        for i in range(depth):
            pos = hash_func(item, i)
            sketch[i][pos] += 1
        
        # Update tracker (with sampling to save memory)
        if hash(str(item)) % 100 == 0:  # Sample 1% of items
            item_tracker[item] += 100  # Estimate actual count
    
    # Estimate frequencies and return top k
    estimated_counts = []
    for item, sampled_count in item_tracker.items():
        # Get minimum count from sketch (Count-Min Sketch estimate)
        min_count = min(sketch[i][hash_func(item, i)] for i in range(depth))
        estimated_counts.append((item, min_count))
    
    return sorted(estimated_counts, key=lambda x: x[1], reverse=True)[:k]

# Performance comparison and usage examples
def compare_methods():
    """Compare different methods for finding frequent elements."""
    # Generate test data
    import random
    data = [random.choice(['A', 'B', 'C', 'D', 'E']) for _ in range(100000)]
    k = 3
    
    methods = [
        ("Basic Counter", top_k_frequent_basic),
        ("Heap-based", top_k_frequent_heap),
        ("Distributed", lambda d, k: top_k_frequent_distributed(d, k, 4))
    ]
    
    for name, method in methods:
        start_time = time.time()
        result = method(data, k)
        end_time = time.time()
        
        print(f"{name}:")
        print(f"  Time: {end_time - start_time:.4f}s")
        print(f"  Result: {result}")
        print()

# Real-world example: Log analysis
def analyze_web_logs(log_entries: List[str], k: int = 10) -> List[Tuple[str, int]]:
    """Analyze web server logs to find most frequent IP addresses."""
    import re
    
    # Extract IP addresses from log entries
    ip_pattern = r'^(\d+\.\d+\.\d+\.\d+)'
    ip_addresses = []
    
    for log_entry in log_entries:
        match = re.match(ip_pattern, log_entry)
        if match:
            ip_addresses.append(match.group(1))
    
    return top_k_frequent_basic(ip_addresses, k)

if __name__ == "__main__":
    # Example usage
    sample_data = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple', 'date']
    
    print("Sample data:", sample_data)
    print("Top 3 frequent items:", top_k_frequent_basic(sample_data, 3))
    
    # Performance comparison
    print("\n=== Performance Comparison ===")
    compare_methods()
    
    # Streaming example
    print("\n=== Streaming Example ===")
    def sample_stream():
        import random
        for _ in range(1000):
            yield random.choice(['X', 'Y', 'Z', 'W'])
    
    stream_results = list(top_k_frequent_streaming(sample_stream(), 2, window_size=100))
    print(f"Streaming results (last window): {stream_results[-1] if stream_results else 'No results'}")
```

### 21. Implement a data pipeline with error handling and monitoring.
**Answer:**
```python
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, List, Optional
from dataclasses import dataclass

@dataclass
class PipelineMetrics:
    processed_records: int = 0
    failed_records: int = 0
    start_time: float = 0
    end_time: float = 0
    
    @property
    def duration(self):
        return self.end_time - self.start_time
    
    @property
    def success_rate(self):
        total = self.processed_records + self.failed_records
        return self.processed_records / total if total > 0 else 0

class PipelineStage(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"pipeline.{name}")
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        pass
    
    def __call__(self, data: Any) -> Any:
        self.logger.info(f"Starting stage: {self.name}")
        try:
            result = self.process(data)
            self.logger.info(f"Completed stage: {self.name}")
            return result
        except Exception as e:
            self.logger.error(f"Error in stage {self.name}: {str(e)}")
            raise

class DataPipeline:
    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages
        self.metrics = PipelineMetrics()
        self.logger = logging.getLogger("pipeline")
    
    def run(self, data: Any) -> Any:
        self.metrics.start_time = time.time()
        
        try:
            current_data = data
            for stage in self.stages:
                current_data = stage(current_data)
            
            self.metrics.processed_records += 1
            return current_data
            
        except Exception as e:
            self.metrics.failed_records += 1
            self.logger.error(f"Pipeline failed: {str(e)}")
            raise
        finally:
            self.metrics.end_time = time.time()
    
    def get_metrics(self) -> PipelineMetrics:
        return self.metrics

# Example usage
class ExtractStage(PipelineStage):
    def process(self, data):
        # Extract data from source
        return {"raw_data": data, "extracted_at": time.time()}

class TransformStage(PipelineStage):
    def process(self, data):
        # Transform data
        transformed = data["raw_data"].upper()
        return {"transformed_data": transformed, "metadata": data}

class LoadStage(PipelineStage):
    def process(self, data):
        # Load data to destination
        self.logger.info(f"Loading: {data['transformed_data']}")
        return {"status": "loaded", "data": data}

# Create and run pipeline
pipeline = DataPipeline([
    ExtractStage("extract"),
    TransformStage("transform"),
    LoadStage("load")
])

result = pipeline.run("hello world")
metrics = pipeline.get_metrics()
print(f"Success rate: {metrics.success_rate:.2%}")
```

### 22. How do you implement multiprocessing for CPU-intensive data processing tasks?

**Answer:**
Multiprocessing bypasses the GIL limitation and enables true parallelism for CPU-bound tasks, essential for large-scale data processing.

**Code Example:**
```python
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import numpy as np
from typing import List, Tuple, Any
import os

def cpu_intensive_task(data_chunk: List[int]) -> Tuple[int, float, int]:
    """Simulate CPU-intensive data processing.
    
    Args:
        data_chunk: List of integers to process
        
    Returns:
        Tuple of (sum, mean, max) of the chunk
    """
    # Simulate heavy computation
    result_sum = sum(x ** 2 for x in data_chunk)
    result_mean = sum(data_chunk) / len(data_chunk) if data_chunk else 0
    result_max = max(data_chunk) if data_chunk else 0
    
    return result_sum, result_mean, result_max

def process_large_dataset_multiprocessing(data: List[int], num_processes: int = None) -> dict:
    """Process large dataset using multiprocessing.
    
    Args:
        data: Large list of integers
        num_processes: Number of processes to use (default: CPU count)
        
    Returns:
        Dictionary with aggregated results
    """
    if num_processes is None:
        num_processes = mp.cpu_count()
    
    # Split data into chunks
    chunk_size = len(data) // num_processes
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    start_time = time.time()
    
    # Process chunks in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Submit all tasks
        future_to_chunk = {executor.submit(cpu_intensive_task, chunk): i 
                          for i, chunk in enumerate(chunks)}
        
        results = []
        for future in as_completed(future_to_chunk):
            chunk_idx = future_to_chunk[future]
            try:
                result = future.result()
                results.append((chunk_idx, result))
            except Exception as e:
                print(f"Chunk {chunk_idx} generated an exception: {e}")
    
    # Aggregate results
    total_sum = sum(result[1][0] for result in results)
    total_mean = sum(result[1][1] for result in results) / len(results)
    total_max = max(result[1][2] for result in results)
    
    end_time = time.time()
    
    return {
        'total_sum': total_sum,
        'average_mean': total_mean,
        'global_max': total_max,
        'processing_time': end_time - start_time,
        'num_processes': num_processes,
        'chunks_processed': len(results)
    }

# Shared memory example for large arrays
def process_numpy_array_shared_memory(array_size: int = 10000000) -> dict:
    """Process large NumPy array using shared memory."""
    
    def worker_function(shared_array, start_idx, end_idx, result_queue):
        """Worker function that processes part of shared array."""
        # Convert shared memory to numpy array
        np_array = np.frombuffer(shared_array.get_obj(), dtype=np.float64)
        
        # Process assigned slice
        slice_data = np_array[start_idx:end_idx]
        result = {
            'worker_id': os.getpid(),
            'start_idx': start_idx,
            'end_idx': end_idx,
            'sum': np.sum(slice_data),
            'mean': np.mean(slice_data),
            'std': np.std(slice_data)
        }
        result_queue.put(result)
    
    # Create shared memory array
    shared_array = mp.Array('d', array_size)  # 'd' for double (float64)
    
    # Initialize with random data
    np_array = np.frombuffer(shared_array.get_obj(), dtype=np.float64)
    np_array[:] = np.random.random(array_size)
    
    # Create processes
    num_processes = mp.cpu_count()
    chunk_size = array_size // num_processes
    processes = []
    result_queue = mp.Queue()
    
    start_time = time.time()
    
    # Start worker processes
    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < num_processes - 1 else array_size
        
        process = mp.Process(
            target=worker_function,
            args=(shared_array, start_idx, end_idx, result_queue)
        )
        processes.append(process)
        process.start()
    
    # Collect results
    results = []
    for _ in range(num_processes):
        results.append(result_queue.get())
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    end_time = time.time()
    
    # Aggregate results
    total_sum = sum(r['sum'] for r in results)
    weighted_mean = sum(r['mean'] * (r['end_idx'] - r['start_idx']) for r in results) / array_size
    
    return {
        'array_size': array_size,
        'total_sum': total_sum,
        'weighted_mean': weighted_mean,
        'processing_time': end_time - start_time,
        'num_processes': num_processes,
        'worker_results': results
    }

# Performance comparison
def compare_processing_methods(data_size: int = 1000000):
    """Compare single-threaded vs multiprocessing performance."""
    data = list(range(data_size))
    
    # Single-threaded processing
    start_time = time.time()
    single_result = cpu_intensive_task(data)
    single_time = time.time() - start_time
    
    # Multiprocessing
    multi_result = process_large_dataset_multiprocessing(data)
    multi_time = multi_result['processing_time']
    
    print(f"Data size: {data_size:,}")
    print(f"Single-threaded time: {single_time:.2f}s")
    print(f"Multiprocessing time: {multi_time:.2f}s")
    print(f"Speedup: {single_time / multi_time:.2f}x")
    print(f"Efficiency: {(single_time / multi_time) / mp.cpu_count() * 100:.1f}%")

if __name__ == "__main__":
    # Example usage
    compare_processing_methods(1000000)
    
    # Shared memory example
    shared_result = process_numpy_array_shared_memory(5000000)
    print(f"\nShared memory processing completed in {shared_result['processing_time']:.2f}s")
```

### 23. How do you implement custom iterators and generators for memory-efficient data processing?

**Answer:**
Custom iterators and generators enable processing of large datasets without loading everything into memory, crucial for big data applications.

**Code Example:**
```python
from typing import Iterator, Generator, Any, Optional
import csv
import json
import gzip
from pathlib import Path

class DataFileIterator:
    """Custom iterator for processing large data files line by line."""
    
    def __init__(self, file_path: str, file_type: str = 'csv', 
                 chunk_size: int = 1024, encoding: str = 'utf-8'):
        """Initialize file iterator.
        
        Args:
            file_path: Path to the data file
            file_type: Type of file ('csv', 'json', 'txt')
            chunk_size: Size of chunks to read
            encoding: File encoding
        """
        self.file_path = Path(file_path)
        self.file_type = file_type.lower()
        self.chunk_size = chunk_size
        self.encoding = encoding
        self._file_handle = None
        self._reader = None
        self._current_line = 0
    
    def __iter__(self) -> Iterator:
        """Return iterator object."""
        return self
    
    def __next__(self) -> dict:
        """Get next item from file."""
        if self._file_handle is None:
            self._open_file()
        
        try:
            if self.file_type == 'csv':
                row = next(self._reader)
                self._current_line += 1
                return dict(row)
            elif self.file_type == 'json':
                line = next(self._file_handle)
                self._current_line += 1
                return json.loads(line.strip())
            else:  # txt
                line = next(self._file_handle)
                self._current_line += 1
                return {'line_number': self._current_line, 'content': line.strip()}
                
        except StopIteration:
            self._close_file()
            raise StopIteration
    
    def _open_file(self):
        """Open file with appropriate handler."""
        if self.file_path.suffix == '.gz':
            self._file_handle = gzip.open(self.file_path, 'rt', encoding=self.encoding)
        else:
            self._file_handle = open(self.file_path, 'r', encoding=self.encoding)
        
        if self.file_type == 'csv':
            self._reader = csv.DictReader(self._file_handle)
    
    def _close_file(self):
        """Close file handle."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
            self._reader = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._close_file()

def batch_generator(iterable: Iterator, batch_size: int) -> Generator[list, None, None]:
    """Generate batches from an iterable.
    
    Args:
        iterable: Input iterable
        batch_size: Size of each batch
        
    Yields:
        Lists of items with specified batch size
    """
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    # Yield remaining items
    if batch:
        yield batch

def sliding_window_generator(iterable: Iterator, window_size: int) -> Generator[list, None, None]:
    """Generate sliding windows from an iterable.
    
    Args:
        iterable: Input iterable
        window_size: Size of sliding window
        
    Yields:
        Lists representing sliding windows
    """
    window = []
    for item in iterable:
        window.append(item)
        if len(window) > window_size:
            window.pop(0)
        if len(window) == window_size:
            yield window.copy()

class DataProcessor:
    """Memory-efficient data processor using generators."""
    
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
    
    def filter_generator(self, data_iter: Iterator, 
                        filter_func: callable) -> Generator[Any, None, None]:
        """Filter data using generator.
        
        Args:
            data_iter: Input data iterator
            filter_func: Function to filter items
            
        Yields:
            Filtered items
        """
        for item in data_iter:
            if filter_func(item):
                yield item
    
    def transform_generator(self, data_iter: Iterator, 
                          transform_func: callable) -> Generator[Any, None, None]:
        """Transform data using generator.
        
        Args:
            data_iter: Input data iterator
            transform_func: Function to transform items
            
        Yields:
            Transformed items
        """
        for item in data_iter:
            try:
                transformed = transform_func(item)
                yield transformed
            except Exception as e:
                print(f"Error transforming item {item}: {e}")
                continue
    
    def aggregate_generator(self, data_iter: Iterator, 
                          key_func: callable, 
                          agg_func: callable) -> Generator[tuple, None, None]:
        """Aggregate data using generator with grouping.
        
        Args:
            data_iter: Input data iterator
            key_func: Function to extract grouping key
            agg_func: Function to aggregate values
            
        Yields:
            Tuples of (key, aggregated_value)
        """
        current_key = None
        current_group = []
        
        for item in data_iter:
            key = key_func(item)
            
            if current_key is None:
                current_key = key
            
            if key == current_key:
                current_group.append(item)
            else:
                # Yield aggregated result for previous group
                if current_group:
                    yield current_key, agg_func(current_group)
                
                # Start new group
                current_key = key
                current_group = [item]
        
        # Yield final group
        if current_group:
            yield current_key, agg_func(current_group)
    
    def process_pipeline(self, file_path: str, 
                        filter_func: Optional[callable] = None,
                        transform_func: Optional[callable] = None,
                        aggregate_key: Optional[callable] = None,
                        aggregate_func: Optional[callable] = None) -> Generator:
        """Complete processing pipeline using generators.
        
        Args:
            file_path: Path to input file
            filter_func: Optional filter function
            transform_func: Optional transform function
            aggregate_key: Optional aggregation key function
            aggregate_func: Optional aggregation function
            
        Yields:
            Processed data items
        """
        # Start with file iterator
        data_iter = DataFileIterator(file_path, 'csv')
        
        # Apply filter if provided
        if filter_func:
            data_iter = self.filter_generator(data_iter, filter_func)
        
        # Apply transformation if provided
        if transform_func:
            data_iter = self.transform_generator(data_iter, transform_func)
        
        # Apply aggregation if provided
        if aggregate_key and aggregate_func:
            data_iter = self.aggregate_generator(data_iter, aggregate_key, aggregate_func)
        
        # Process in batches
        for batch in batch_generator(data_iter, self.batch_size):
            yield batch

# Usage examples
def example_usage():
    """Demonstrate memory-efficient data processing."""
    
    # Example 1: Process large CSV file
    def is_valid_record(record):
        """Filter function to keep only valid records."""
        return record.get('amount', 0) > 0
    
    def normalize_record(record):
        """Transform function to normalize record."""
        return {
            'id': record.get('id', ''),
            'amount': float(record.get('amount', 0)),
            'category': record.get('category', '').upper()
        }
    
    def get_category(record):
        """Key function for aggregation."""
        return record['category']
    
    def sum_amounts(records):
        """Aggregation function to sum amounts."""
        return sum(record['amount'] for record in records)
    
    # Create processor
    processor = DataProcessor(batch_size=1000)
    
    # Process data pipeline
    print("Processing data pipeline...")
    batch_count = 0
    total_records = 0
    
    try:
        for batch in processor.process_pipeline(
            'large_data.csv',
            filter_func=is_valid_record,
            transform_func=normalize_record,
            aggregate_key=get_category,
            aggregate_func=sum_amounts
        ):
            batch_count += 1
            total_records += len(batch)
            
            # Process batch (e.g., save to database)
            print(f"Processed batch {batch_count} with {len(batch)} records")
            
            # Show sample of first batch
            if batch_count == 1:
                print(f"Sample data: {batch[:3]}")
    
    except FileNotFoundError:
        print("Demo file not found, creating sample data...")
        
        # Create sample data generator
        def sample_data_generator(num_records: int = 10000):
            """Generate sample data for demonstration."""
            import random
            categories = ['A', 'B', 'C', 'D']
            
            for i in range(num_records):
                yield {
                    'id': f'ID_{i:06d}',
                    'amount': random.uniform(10, 1000),
                    'category': random.choice(categories)
                }
        
        # Process sample data
        sample_iter = sample_data_generator(10000)
        filtered_iter = processor.filter_generator(sample_iter, is_valid_record)
        transformed_iter = processor.transform_generator(filtered_iter, normalize_record)
        
        # Process in batches
        for i, batch in enumerate(batch_generator(transformed_iter, 1000)):
            print(f"Sample batch {i+1}: {len(batch)} records")
            if i >= 2:  # Process only first 3 batches for demo
                break
    
    print(f"\nTotal batches processed: {batch_count}")
    print(f"Total records processed: {total_records}")

if __name__ == "__main__":
    example_usage()
```

### 24. How do you implement thread-safe data structures and handle concurrency?

**Answer:**
Thread-safe data structures prevent race conditions in multi-threaded environments, essential for concurrent data processing applications.

**Code Example:**
```python
import threading
import queue
import time
from typing import Any, Optional, Dict, List
from collections import defaultdict, deque
from contextlib import contextmanager
import weakref

class ThreadSafeCounter:
    """Thread-safe counter with atomic operations."""
    
    def __init__(self, initial_value: int = 0):
        self._value = initial_value
        self._lock = threading.RLock()  # Reentrant lock
    
    def increment(self, amount: int = 1) -> int:
        """Atomically increment counter."""
        with self._lock:
            self._value += amount
            return self._value
    
    def decrement(self, amount: int = 1) -> int:
        """Atomically decrement counter."""
        with self._lock:
            self._value -= amount
            return self._value
    
    def get(self) -> int:
        """Get current value."""
        with self._lock:
            return self._value
    
    def set(self, value: int) -> None:
        """Set counter value."""
        with self._lock:
            self._value = value
    
    def compare_and_swap(self, expected: int, new_value: int) -> bool:
        """Atomic compare and swap operation."""
        with self._lock:
            if self._value == expected:
                self._value = new_value
                return True
            return False

class ThreadSafeDict:
    """Thread-safe dictionary wrapper."""
    
    def __init__(self):
        self._dict = {}
        self._lock = threading.RWLock() if hasattr(threading, 'RWLock') else threading.RLock()
    
    def get(self, key: Any, default: Any = None) -> Any:
        """Thread-safe get operation."""
        with self._lock:
            return self._dict.get(key, default)
    
    def set(self, key: Any, value: Any) -> None:
        """Thread-safe set operation."""
        with self._lock:
            self._dict[key] = value
    
    def update(self, other: Dict[Any, Any]) -> None:
        """Thread-safe update operation."""
        with self._lock:
            self._dict.update(other)
    
    def pop(self, key: Any, default: Any = None) -> Any:
        """Thread-safe pop operation."""
        with self._lock:
            return self._dict.pop(key, default)
    
    def keys(self) -> List[Any]:
        """Get snapshot of keys."""
        with self._lock:
            return list(self._dict.keys())
    
    def items(self) -> List[tuple]:
        """Get snapshot of items."""
        with self._lock:
            return list(self._dict.items())
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._dict)

class ThreadSafeQueue:
    """Enhanced thread-safe queue with additional features."""
    
    def __init__(self, maxsize: int = 0):
        self._queue = queue.Queue(maxsize=maxsize)
        self._stats_lock = threading.Lock()
        self._total_items_added = 0
        self._total_items_removed = 0
    
    def put(self, item: Any, block: bool = True, timeout: Optional[float] = None) -> None:
        """Put item in queue with statistics tracking."""
        self._queue.put(item, block=block, timeout=timeout)
        with self._stats_lock:
            self._total_items_added += 1
    
    def get(self, block: bool = True, timeout: Optional[float] = None) -> Any:
        """Get item from queue with statistics tracking."""
        item = self._queue.get(block=block, timeout=timeout)
        with self._stats_lock:
            self._total_items_removed += 1
        return item
    
    def qsize(self) -> int:
        """Get approximate queue size."""
        return self._queue.qsize()
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()
    
    def full(self) -> bool:
        """Check if queue is full."""
        return self._queue.full()
    
    def get_stats(self) -> Dict[str, int]:
        """Get queue statistics."""
        with self._stats_lock:
            return {
                'current_size': self.qsize(),
                'total_added': self._total_items_added,
                'total_removed': self._total_items_removed,
                'net_items': self._total_items_added - self._total_items_removed
            }

class ConnectionPool:
    """Thread-safe connection pool for database connections."""
    
    def __init__(self, create_connection_func: callable, 
                 max_connections: int = 10, 
                 timeout: float = 30.0):
        """Initialize connection pool.
        
        Args:
            create_connection_func: Function to create new connections
            max_connections: Maximum number of connections in pool
            timeout: Timeout for getting connections
        """
        self._create_connection = create_connection_func
        self._max_connections = max_connections
        self._timeout = timeout
        self._pool = queue.Queue(maxsize=max_connections)
        self._created_connections = 0
        self._lock = threading.Lock()
        self._active_connections = weakref.WeakSet()
    
    def get_connection(self):
        """Get connection from pool or create new one."""
        try:
            # Try to get existing connection
            connection = self._pool.get(block=False)
            return self._wrap_connection(connection)
        except queue.Empty:
            # Create new connection if under limit
            with self._lock:
                if self._created_connections < self._max_connections:
                    connection = self._create_connection()
                    self._created_connections += 1
                    return self._wrap_connection(connection)
            
            # Wait for available connection
            connection = self._pool.get(timeout=self._timeout)
            return self._wrap_connection(connection)
    
    def _wrap_connection(self, connection):
        """Wrap connection to automatically return to pool."""
        class PooledConnection:
            def __init__(self, conn, pool):
                self._conn = conn
                self._pool = pool
                self._returned = False
            
            def __getattr__(self, name):
                return getattr(self._conn, name)
            
            def close(self):
                if not self._returned:
                    self._pool._return_connection(self._conn)
                    self._returned = True
            
            def __enter__(self):
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                self.close()
        
        wrapped = PooledConnection(connection, self)
        self._active_connections.add(wrapped)
        return wrapped
    
    def _return_connection(self, connection):
        """Return connection to pool."""
        try:
            self._pool.put(connection, block=False)
        except queue.Full:
            # Pool is full, close connection
            if hasattr(connection, 'close'):
                connection.close()
            with self._lock:
                self._created_connections -= 1
    
    def get_stats(self) -> Dict[str, int]:
        """Get pool statistics."""
        return {
            'pool_size': self._pool.qsize(),
            'created_connections': self._created_connections,
            'max_connections': self._max_connections,
            'active_connections': len(self._active_connections)
        }

# Producer-Consumer pattern with thread safety
class ProducerConsumerSystem:
    """Thread-safe producer-consumer system for data processing."""
    
    def __init__(self, queue_size: int = 100, num_consumers: int = 3):
        self.queue = ThreadSafeQueue(maxsize=queue_size)
        self.num_consumers = num_consumers
        self.running = threading.Event()
        self.running.set()
        self.consumers = []
        self.producer_thread = None
        self.stats = ThreadSafeCounter()
    
    def producer(self, data_generator: callable):
        """Producer function that generates data."""
        try:
            for item in data_generator():
                if not self.running.is_set():
                    break
                
                self.queue.put(item, timeout=1.0)
                self.stats.increment()
                
        except queue.Full:
            print("Queue is full, producer stopping")
        except Exception as e:
            print(f"Producer error: {e}")
        finally:
            # Signal end of data
            for _ in range(self.num_consumers):
                try:
                    self.queue.put(None, timeout=1.0)  # Sentinel value
                except queue.Full:
                    pass
    
    def consumer(self, consumer_id: int, process_func: callable):
        """Consumer function that processes data."""
        processed_count = 0
        
        try:
            while self.running.is_set():
                try:
                    item = self.queue.get(timeout=1.0)
                    
                    # Check for sentinel value
                    if item is None:
                        break
                    
                    # Process item
                    result = process_func(item)
                    processed_count += 1
                    
                    if processed_count % 100 == 0:
                        print(f"Consumer {consumer_id} processed {processed_count} items")
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Consumer {consumer_id} error: {e}")
                    
        finally:
            print(f"Consumer {consumer_id} finished, processed {processed_count} items")
    
    def start(self, data_generator: callable, process_func: callable):
        """Start producer-consumer system."""
        # Start producer
        self.producer_thread = threading.Thread(
            target=self.producer,
            args=(data_generator,)
        )
        self.producer_thread.start()
        
        # Start consumers
        for i in range(self.num_consumers):
            consumer_thread = threading.Thread(
                target=self.consumer,
                args=(i, process_func)
            )
            self.consumers.append(consumer_thread)
            consumer_thread.start()
    
    def stop(self):
        """Stop producer-consumer system."""
        self.running.clear()
        
        # Wait for producer to finish
        if self.producer_thread:
            self.producer_thread.join(timeout=5.0)
        
        # Wait for consumers to finish
        for consumer in self.consumers:
            consumer.join(timeout=5.0)
        
        # Print final statistics
        queue_stats = self.queue.get_stats()
        print(f"Final stats: {queue_stats}")
        print(f"Items produced: {self.stats.get()}")

# Usage example
def example_concurrent_processing():
    """Demonstrate thread-safe concurrent processing."""
    
    def data_generator():
        """Generate sample data."""
        for i in range(1000):
            yield {'id': i, 'value': i * 2, 'timestamp': time.time()}
            time.sleep(0.001)  # Simulate data generation delay
    
    def process_item(item):
        """Process individual item."""
        # Simulate processing time
        time.sleep(0.01)
        return {
            'processed_id': item['id'],
            'result': item['value'] ** 2,
            'processed_at': time.time()
        }
    
    # Create and start system
    system = ProducerConsumerSystem(queue_size=50, num_consumers=4)
    
    print("Starting producer-consumer system...")
    system.start(data_generator, process_item)
    
    # Let it run for a while
    time.sleep(5)
    
    # Stop system
    print("Stopping system...")
    system.stop()
    
    print("System stopped.")

if __name__ == "__main__":
    example_concurrent_processing()
```

### 25. How do you implement data validation and schema enforcement in Python?

**Answer:**
Data validation ensures data quality and consistency, critical for reliable data pipelines and analytics.

**Code Example:**
```python
from typing import Any, Dict, List, Optional, Union, Type
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime, date
import re
import json
from enum import Enum

class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, field: str, value: Any, message: str):
        self.field = field
        self.value = value
        self.message = message
        super().__init__(f"Validation error for field '{field}': {message}")

class ValidationResult:
    """Result of validation operation."""
    def __init__(self):
        self.is_valid = True
        self.errors: List[ValidationError] = []
        self.warnings: List[str] = []
    
    def add_error(self, field: str, value: Any, message: str):
        """Add validation error."""
        self.is_valid = False
        self.errors.append(ValidationError(field, value, message))
    
    def add_warning(self, message: str):
        """Add validation warning."""
        self.warnings.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'is_valid': self.is_valid,
            'errors': [{
                'field': error.field,
                'value': error.value,
                'message': error.message
            } for error in self.errors],
            'warnings': self.warnings
        }

class Validator(ABC):
    """Abstract base class for validators."""
    
    @abstractmethod
    def validate(self, value: Any) -> ValidationResult:
        """Validate a value."""
        pass

class TypeValidator(Validator):
    """Validates data types."""
    
    def __init__(self, expected_type: Type, allow_none: bool = False):
        self.expected_type = expected_type
        self.allow_none = allow_none
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if value is None and self.allow_none:
            return result
        
        if not isinstance(value, self.expected_type):
            result.add_error(
                'type_check',
                value,
                f"Expected {self.expected_type.__name__}, got {type(value).__name__}"
            )
        
        return result

class RangeValidator(Validator):
    """Validates numeric ranges."""
    
    def __init__(self, min_value: Optional[Union[int, float]] = None,
                 max_value: Optional[Union[int, float]] = None,
                 inclusive: bool = True):
        self.min_value = min_value
        self.max_value = max_value
        self.inclusive = inclusive
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, (int, float)):
            result.add_error('range_check', value, "Value must be numeric")
            return result
        
        if self.min_value is not None:
            if self.inclusive and value < self.min_value:
                result.add_error('range_check', value, f"Value must be >= {self.min_value}")
            elif not self.inclusive and value <= self.min_value:
                result.add_error('range_check', value, f"Value must be > {self.min_value}")
        
        if self.max_value is not None:
            if self.inclusive and value > self.max_value:
                result.add_error('range_check', value, f"Value must be <= {self.max_value}")
            elif not self.inclusive and value >= self.max_value:
                result.add_error('range_check', value, f"Value must be < {self.max_value}")
        
        return result

class RegexValidator(Validator):
    """Validates strings against regex patterns."""
    
    def __init__(self, pattern: str, flags: int = 0):
        self.pattern = pattern
        self.regex = re.compile(pattern, flags)
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if not isinstance(value, str):
            result.add_error('regex_check', value, "Value must be a string")
            return result
        
        if not self.regex.match(value):
            result.add_error('regex_check', value, f"Value does not match pattern: {self.pattern}")
        
        return result

class LengthValidator(Validator):
    """Validates string/list length."""
    
    def __init__(self, min_length: Optional[int] = None,
                 max_length: Optional[int] = None):
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if not hasattr(value, '__len__'):
            result.add_error('length_check', value, "Value must have length")
            return result
        
        length = len(value)
        
        if self.min_length is not None and length < self.min_length:
            result.add_error('length_check', value, f"Length must be >= {self.min_length}")
        
        if self.max_length is not None and length > self.max_length:
            result.add_error('length_check', value, f"Length must be <= {self.max_length}")
        
        return result

class ChoiceValidator(Validator):
    """Validates value is in allowed choices."""
    
    def __init__(self, choices: List[Any]):
        self.choices = choices
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        if value not in self.choices:
            result.add_error('choice_check', value, f"Value must be one of: {self.choices}")
        
        return result

class DateValidator(Validator):
    """Validates date formats and ranges."""
    
    def __init__(self, date_format: str = '%Y-%m-%d',
                 min_date: Optional[date] = None,
                 max_date: Optional[date] = None):
        self.date_format = date_format
        self.min_date = min_date
        self.max_date = max_date
    
    def validate(self, value: Any) -> ValidationResult:
        result = ValidationResult()
        
        # Convert string to date if necessary
        if isinstance(value, str):
            try:
                parsed_date = datetime.strptime(value, self.date_format).date()
            except ValueError:
                result.add_error('date_format', value, f"Invalid date format, expected: {self.date_format}")
                return result
        elif isinstance(value, datetime):
            parsed_date = value.date()
        elif isinstance(value, date):
            parsed_date = value
        else:
            result.add_error('date_type', value, "Value must be a date, datetime, or date string")
            return result
        
        # Check date range
        if self.min_date and parsed_date < self.min_date:
            result.add_error('date_range', value, f"Date must be >= {self.min_date}")
        
        if self.max_date and parsed_date > self.max_date:
            result.add_error('date_range', value, f"Date must be <= {self.max_date}")
        
        return result

@dataclass
class FieldSchema:
    """Schema definition for a single field."""
    name: str
    validators: List[Validator] = field(default_factory=list)
    required: bool = True
    default: Any = None
    description: str = ""
    
    def validate(self, value: Any) -> ValidationResult:
        """Validate field value against all validators."""
        combined_result = ValidationResult()
        
        # Check if field is required
        if value is None:
            if self.required:
                combined_result.add_error(self.name, value, "Field is required")
                return combined_result
            else:
                return combined_result  # Optional field with None value is valid
        
        # Run all validators
        for validator in self.validators:
            result = validator.validate(value)
            if not result.is_valid:
                combined_result.is_valid = False
                combined_result.errors.extend(result.errors)
            combined_result.warnings.extend(result.warnings)
        
        return combined_result

class DataSchema:
    """Complete schema for data validation."""
    
    def __init__(self, name: str, fields: List[FieldSchema]):
        self.name = name
        self.fields = {field.name: field for field in fields}
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate complete data record."""
        combined_result = ValidationResult()
        
        # Check for unexpected fields
        unexpected_fields = set(data.keys()) - set(self.fields.keys())
        for field in unexpected_fields:
            combined_result.add_warning(f"Unexpected field: {field}")
        
        # Validate each field
        for field_name, field_schema in self.fields.items():
            field_value = data.get(field_name)
            
            field_result = field_schema.validate(field_value)
            if not field_result.is_valid:
                combined_result.is_valid = False
                combined_result.errors.extend(field_result.errors)
            combined_result.warnings.extend(field_result.warnings)
        
        return combined_result
    
    def validate_batch(self, data_list: List[Dict[str, Any]]) -> List[ValidationResult]:
        """Validate batch of records."""
        return [self.validate(record) for record in data_list]
    
    def clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean data by applying defaults and removing invalid fields."""
        cleaned = {}
        
        for field_name, field_schema in self.fields.items():
            if field_name in data:
                cleaned[field_name] = data[field_name]
            elif field_schema.default is not None:
                cleaned[field_name] = field_schema.default
        
        return cleaned

# Predefined common schemas
class CommonSchemas:
    """Collection of commonly used schemas."""
    
    @staticmethod
    def email_schema() -> DataSchema:
        """Schema for email validation."""
        return DataSchema('email', [
            FieldSchema(
                name='email',
                validators=[
                    TypeValidator(str),
                    RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
                    LengthValidator(max_length=254)
                ],
                description='Valid email address'
            )
        ])
    
    @staticmethod
    def user_schema() -> DataSchema:
        """Schema for user data validation."""
        return DataSchema('user', [
            FieldSchema(
                name='id',
                validators=[TypeValidator(int), RangeValidator(min_value=1)],
                description='Unique user ID'
            ),
            FieldSchema(
                name='username',
                validators=[
                    TypeValidator(str),
                    LengthValidator(min_length=3, max_length=50),
                    RegexValidator(r'^[a-zA-Z0-9_]+$')
                ],
                description='Username (alphanumeric and underscore only)'
            ),
            FieldSchema(
                name='email',
                validators=[
                    TypeValidator(str),
                    RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                ],
                description='Valid email address'
            ),
            FieldSchema(
                name='age',
                validators=[TypeValidator(int), RangeValidator(min_value=0, max_value=150)],
                required=False,
                description='User age'
            ),
            FieldSchema(
                name='status',
                validators=[ChoiceValidator(['active', 'inactive', 'suspended'])],
                default='active',
                description='User account status'
            ),
            FieldSchema(
                name='created_at',
                validators=[DateValidator()],
                description='Account creation date'
            )
        ])
    
    @staticmethod
    def transaction_schema() -> DataSchema:
        """Schema for financial transaction validation."""
        return DataSchema('transaction', [
            FieldSchema(
                name='transaction_id',
                validators=[TypeValidator(str), LengthValidator(min_length=10, max_length=50)],
                description='Unique transaction identifier'
            ),
            FieldSchema(
                name='amount',
                validators=[TypeValidator((int, float)), RangeValidator(min_value=0.01)],
                description='Transaction amount (must be positive)'
            ),
            FieldSchema(
                name='currency',
                validators=[ChoiceValidator(['USD', 'EUR', 'GBP', 'JPY', 'CAD'])],
                description='Transaction currency'
            ),
            FieldSchema(
                name='transaction_type',
                validators=[ChoiceValidator(['debit', 'credit', 'transfer'])],
                description='Type of transaction'
            ),
            FieldSchema(
                name='timestamp',
                validators=[DateValidator('%Y-%m-%d %H:%M:%S')],
                description='Transaction timestamp'
            )
        ])

# Usage examples
def example_data_validation():
    """Demonstrate comprehensive data validation."""
    
    # Create user schema
    user_schema = CommonSchemas.user_schema()
    
    # Test data
    test_users = [
        {
            'id': 1,
            'username': 'john_doe',
            'email': 'john@example.com',
            'age': 30,
            'status': 'active',
            'created_at': '2023-01-15'
        },
        {
            'id': 'invalid',  # Invalid type
            'username': 'jd',  # Too short
            'email': 'invalid-email',  # Invalid format
            'age': -5,  # Invalid range
            'status': 'unknown',  # Invalid choice
            'created_at': '2023-13-45'  # Invalid date
        },
        {
            'id': 3,
            'username': 'jane_smith',
            'email': 'jane@example.com',
            # Missing required created_at
            'extra_field': 'unexpected'  # Unexpected field
        }
    ]
    
    print("Validating user data...")
    for i, user_data in enumerate(test_users):
        print(f"\n--- User {i+1} ---")
        result = user_schema.validate(user_data)
        
        if result.is_valid:
            print("✅ Valid data")
            cleaned_data = user_schema.clean_data(user_data)
            print(f"Cleaned data: {json.dumps(cleaned_data, indent=2)}")
        else:
            print("❌ Invalid data")
            for error in result.errors:
                print(f"  Error: {error.message}")
        
        if result.warnings:
            print("⚠️  Warnings:")
            for warning in result.warnings:
                print(f"  Warning: {warning}")
    
    # Batch validation example
    print("\n=== Batch Validation ===")
    batch_results = user_schema.validate_batch(test_users)
    valid_count = sum(1 for result in batch_results if result.is_valid)
    print(f"Valid records: {valid_count}/{len(test_users)}")
    
    # Transaction schema example
    print("\n=== Transaction Validation ===")
    transaction_schema = CommonSchemas.transaction_schema()
    
    transaction_data = {
        'transaction_id': 'TXN_123456789',
        'amount': 99.99,
        'currency': 'USD',
        'transaction_type': 'debit',
        'timestamp': '2023-01-15 14:30:00'
    }
    
    result = transaction_schema.validate(transaction_data)
    if result.is_valid:
        print("✅ Transaction data is valid")
    else:
        print("❌ Transaction data is invalid")
        for error in result.errors:
            print(f"  Error: {error.message}")

if __name__ == "__main__":
    example_data_validation()
```

---

---

## 🎯 **Conceptual & Theoretical Questions**

### 26. What are Python's design principles and philosophy?
**Answer:**
Python follows the "Zen of Python" (PEP 20) principles:
- **Beautiful is better than ugly**
- **Explicit is better than implicit**
- **Simple is better than complex**
- **Readability counts**
- **There should be one obvious way to do it**

### 27. Explain Python's object model and everything being an object
**Answer:**
In Python, everything is an object with:
- **Identity**: Unique identifier (id())
- **Type**: Defines operations (type())
- **Value**: The data itself

```python
# Everything is an object
print(type(5))          # <class 'int'>
print(type(len))        # <class 'builtin_function_or_method'>
print(type(int))        # <class 'type'>
print(hasattr(5, '__add__'))  # True
```

### 28. What are metaclasses and when would you use them?
**Answer:**
Metaclasses are "classes that create classes" - they define how classes are constructed.

```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"

# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 29. How does Python's import system work?
**Answer:**
Python's import system involves:
1. **Module Search**: sys.path directories
2. **Module Loading**: Compile .py to bytecode
3. **Module Caching**: Store in sys.modules
4. **Namespace Creation**: Execute module code

### 30. What are descriptors and how do they work?
**Answer:**
Descriptors define how attribute access is handled through `__get__`, `__set__`, and `__delete__` methods.

```python
class ValidatedAttribute:
    def __init__(self, validator):
        self.validator = validator
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        obj.__dict__[self.name] = value

class Person:
    age = ValidatedAttribute(lambda x: isinstance(x, int) and x >= 0)
```

---

## 🏢 **System Design & Architecture Questions**

### 31. How would you design a scalable data processing system using Python?
**Answer:**
**Architecture Components:**
- **Message Queue**: Redis/RabbitMQ for task distribution
- **Worker Processes**: Celery for distributed processing
- **Data Storage**: PostgreSQL + Redis for caching
- **API Layer**: FastAPI for REST endpoints
- **Monitoring**: Prometheus + Grafana

### 32. Explain different Python deployment strategies
**Answer:**
**Deployment Options:**
- **Traditional**: Virtual environments + systemd
- **Containerized**: Docker + Kubernetes
- **Serverless**: AWS Lambda, Google Cloud Functions
- **Platform-as-a-Service**: Heroku, Google App Engine

### 33. How do you handle configuration management in Python applications?
**Answer:**
```python
# Using environment variables and config classes
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    host: str = os.getenv('DB_HOST', 'localhost')
    port: int = int(os.getenv('DB_PORT', '5432'))
    username: str = os.getenv('DB_USER', 'postgres')
    password: str = os.getenv('DB_PASSWORD', '')
    database: str = os.getenv('DB_NAME', 'myapp')
    
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

@dataclass
class AppConfig:
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    secret_key: str = os.getenv('SECRET_KEY', 'dev-key')
    database: DatabaseConfig = DatabaseConfig()
    redis_url: str = os.getenv('REDIS_URL', 'redis://localhost:6379')
```

---

## 🔍 **Debugging & Troubleshooting Questions**

### 34. How do you debug memory leaks in Python applications?
**Answer:**
**Tools and Techniques:**
- **memory_profiler**: Line-by-line memory usage
- **tracemalloc**: Built-in memory tracking
- **objgraph**: Object reference tracking
- **gc module**: Garbage collection analysis

```python
import tracemalloc
import gc

# Start tracing
tracemalloc.start()

# Your code here
data = [i for i in range(1000000)]

# Get memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")

# Check for circular references
print(f"Garbage collection stats: {gc.get_stats()}")
```

### 35. What are common Python performance bottlenecks and solutions?
**Answer:**
**Common Bottlenecks:**
1. **String Concatenation**: Use join() instead of +=
2. **List Operations**: Use list comprehensions, avoid repeated append()
3. **Dictionary Lookups**: Use defaultdict, consider sets for membership
4. **Function Calls**: Minimize function call overhead
5. **I/O Operations**: Use async/await, connection pooling

---

## 🧪 **Testing & Quality Assurance Questions**

### 36. How do you implement comprehensive testing strategies in Python?
**Answer:**
**Testing Pyramid:**
- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Load and stress testing

```python
import pytest
from unittest.mock import Mock, patch

class TestDataProcessor:
    @pytest.fixture
    def sample_data(self):
        return [{'id': 1, 'value': 100}, {'id': 2, 'value': 200}]
    
    def test_process_data_success(self, sample_data):
        processor = DataProcessor()
        result = processor.process(sample_data)
        assert len(result) == 2
        assert result[0]['processed'] == True
    
    @patch('requests.get')
    def test_api_call_with_mock(self, mock_get):
        mock_get.return_value.json.return_value = {'status': 'success'}
        result = fetch_data_from_api('http://example.com')
        assert result['status'] == 'success'
    
    def test_error_handling(self):
        processor = DataProcessor()
        with pytest.raises(ValueError):
            processor.process(None)
```

### 37. How do you ensure code quality in Python projects?
**Answer:**
**Code Quality Tools:**
- **Linting**: pylint, flake8, black (formatting)
- **Type Checking**: mypy, pyright
- **Security**: bandit, safety
- **Complexity**: radon, mccabe
- **Documentation**: pydocstyle

---

## 🌐 **Integration & API Questions**

### 38. How do you design and implement RESTful APIs in Python?
**Answer:**
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Data API", version="1.0.0")

class DataModel(BaseModel):
    id: int
    name: str
    value: float
    category: Optional[str] = None

class DataResponse(BaseModel):
    data: List[DataModel]
    total: int
    page: int
    per_page: int

@app.get("/data", response_model=DataResponse)
async def get_data(
    page: int = 1,
    per_page: int = 10,
    category: Optional[str] = None
):
    # Implement pagination and filtering
    filtered_data = filter_data(category) if category else get_all_data()
    paginated_data = paginate(filtered_data, page, per_page)
    
    return DataResponse(
        data=paginated_data,
        total=len(filtered_data),
        page=page,
        per_page=per_page
    )

@app.post("/data", response_model=DataModel)
async def create_data(data: DataModel):
    # Validate and create data
    created_data = create_data_record(data)
    return created_data
```

### 39. How do you handle authentication and authorization in Python web applications?
**Answer:**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required_role: str):
    def role_checker(current_user: str = Depends(verify_token)):
        user_roles = get_user_roles(current_user)
        if required_role not in user_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker

@app.get("/admin/data")
async def admin_only_endpoint(current_user: str = Depends(require_role("admin"))):
    return {"message": "Admin access granted", "user": current_user}
```

---

## 📊 **Data Engineering Specific Scenarios**

### 40. How would you implement a real-time data pipeline monitoring system?
**Answer:**
```python
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class PipelineStatus(Enum):
    RUNNING = "running"
    FAILED = "failed"
    COMPLETED = "completed"
    PAUSED = "paused"

@dataclass
class PipelineMetrics:
    pipeline_id: str
    status: PipelineStatus
    records_processed: int
    records_failed: int
    processing_rate: float  # records per second
    last_updated: datetime
    error_message: str = None

class PipelineMonitor:
    def __init__(self):
        self.pipelines: Dict[str, PipelineMetrics] = {}
        self.alerts = []
        self.logger = logging.getLogger(__name__)
    
    async def monitor_pipeline(self, pipeline_id: str):
        """Monitor a specific pipeline"""
        while True:
            try:
                metrics = await self.collect_metrics(pipeline_id)
                self.pipelines[pipeline_id] = metrics
                
                # Check for alerts
                await self.check_alerts(metrics)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error monitoring pipeline {pipeline_id}: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def collect_metrics(self, pipeline_id: str) -> PipelineMetrics:
        """Collect metrics from pipeline"""
        # Implementation would connect to actual pipeline
        # This is a mock implementation
        return PipelineMetrics(
            pipeline_id=pipeline_id,
            status=PipelineStatus.RUNNING,
            records_processed=1000,
            records_failed=5,
            processing_rate=50.0,
            last_updated=datetime.now()
        )
    
    async def check_alerts(self, metrics: PipelineMetrics):
        """Check for alert conditions"""
        # High error rate
        if metrics.records_failed > 0:
            error_rate = metrics.records_failed / (metrics.records_processed + metrics.records_failed)
            if error_rate > 0.05:  # 5% error rate threshold
                await self.send_alert(f"High error rate in {metrics.pipeline_id}: {error_rate:.2%}")
        
        # Low processing rate
        if metrics.processing_rate < 10.0:  # Less than 10 records/second
            await self.send_alert(f"Low processing rate in {metrics.pipeline_id}: {metrics.processing_rate} rec/sec")
        
        # Pipeline failure
        if metrics.status == PipelineStatus.FAILED:
            await self.send_alert(f"Pipeline {metrics.pipeline_id} failed: {metrics.error_message}")
    
    async def send_alert(self, message: str):
        """Send alert notification"""
        self.alerts.append({
            'timestamp': datetime.now(),
            'message': message,
            'severity': 'high'
        })
        self.logger.warning(f"ALERT: {message}")
        # Could integrate with Slack, email, PagerDuty, etc.
```

### 41. How do you implement data lineage tracking in Python?
**Answer:**
```python
from typing import Dict, List, Set
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class DataAsset:
    name: str
    asset_type: str  # table, file, api, etc.
    location: str
    schema: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataTransformation:
    transformation_id: str
    name: str
    inputs: List[DataAsset]
    outputs: List[DataAsset]
    transformation_logic: str
    timestamp: datetime
    owner: str

class DataLineageTracker:
    def __init__(self):
        self.assets: Dict[str, DataAsset] = {}
        self.transformations: Dict[str, DataTransformation] = {}
        self.lineage_graph: Dict[str, Set[str]] = {}  # asset -> dependent assets
    
    def register_asset(self, asset: DataAsset):
        """Register a data asset"""
        self.assets[asset.name] = asset
        if asset.name not in self.lineage_graph:
            self.lineage_graph[asset.name] = set()
    
    def register_transformation(self, transformation: DataTransformation):
        """Register a data transformation"""
        self.transformations[transformation.transformation_id] = transformation
        
        # Update lineage graph
        for input_asset in transformation.inputs:
            for output_asset in transformation.outputs:
                self.lineage_graph[input_asset.name].add(output_asset.name)
    
    def get_upstream_dependencies(self, asset_name: str) -> Set[str]:
        """Get all upstream dependencies of an asset"""
        dependencies = set()
        
        def traverse_upstream(current_asset):
            for transformation in self.transformations.values():
                for output in transformation.outputs:
                    if output.name == current_asset:
                        for input_asset in transformation.inputs:
                            if input_asset.name not in dependencies:
                                dependencies.add(input_asset.name)
                                traverse_upstream(input_asset.name)
        
        traverse_upstream(asset_name)
        return dependencies
    
    def get_downstream_dependencies(self, asset_name: str) -> Set[str]:
        """Get all downstream dependencies of an asset"""
        dependencies = set()
        
        def traverse_downstream(current_asset):
            if current_asset in self.lineage_graph:
                for dependent in self.lineage_graph[current_asset]:
                    if dependent not in dependencies:
                        dependencies.add(dependent)
                        traverse_downstream(dependent)
        
        traverse_downstream(asset_name)
        return dependencies
    
    def get_impact_analysis(self, asset_name: str) -> Dict[str, Any]:
        """Analyze impact of changes to an asset"""
        return {
            'asset': asset_name,
            'upstream_dependencies': list(self.get_upstream_dependencies(asset_name)),
            'downstream_dependencies': list(self.get_downstream_dependencies(asset_name)),
            'transformations_affected': [
                t.transformation_id for t in self.transformations.values()
                if any(inp.name == asset_name for inp in t.inputs) or
                   any(out.name == asset_name for out in t.outputs)
            ]
        }
    
    def export_lineage(self) -> str:
        """Export lineage as JSON"""
        lineage_data = {
            'assets': {name: {
                'name': asset.name,
                'type': asset.asset_type,
                'location': asset.location,
                'schema': asset.schema,
                'metadata': asset.metadata
            } for name, asset in self.assets.items()},
            'transformations': {tid: {
                'id': t.transformation_id,
                'name': t.name,
                'inputs': [inp.name for inp in t.inputs],
                'outputs': [out.name for out in t.outputs],
                'logic': t.transformation_logic,
                'timestamp': t.timestamp.isoformat(),
                'owner': t.owner
            } for tid, t in self.transformations.items()}
        }
        return json.dumps(lineage_data, indent=2)
```

---

---

## 📚 **Study Guide & Key Takeaways**

### 🎯 **Essential Python Concepts for Data Engineering**

#### **Core Language Features**
1. **Object Model**: Everything is an object with identity, type, and value
2. **Memory Management**: Reference counting + garbage collection for cycles
3. **GIL Impact**: Understand when to use threading vs multiprocessing
4. **Decorators**: Function/class modification without changing source code
5. **Context Managers**: Resource management with `__enter__` and `__exit__`
6. **Generators**: Memory-efficient iteration for large datasets

#### **Performance & Optimization**
1. **Profiling First**: Use cProfile, memory_profiler to identify bottlenecks
2. **Data Structures**: Choose appropriate structures (set for membership, dict for lookups)
3. **Built-in Functions**: Leverage optimized C implementations
4. **NumPy**: Vectorized operations for numerical computing
5. **Caching**: Use `@lru_cache` for expensive computations
6. **String Operations**: Use `join()` instead of concatenation

#### **Concurrency Patterns**
1. **Threading**: Good for I/O-bound tasks (GIL released during I/O)
2. **Multiprocessing**: Required for CPU-bound parallelism
3. **Async/Await**: Excellent for concurrent I/O operations
4. **Thread Safety**: Use locks, queues, and thread-safe data structures

#### **Data Engineering Specific**
1. **Large Dataset Processing**: Generators, chunking, streaming approaches
2. **Memory Efficiency**: Avoid loading entire datasets into memory
3. **Error Handling**: Comprehensive exception handling with retries
4. **Data Validation**: Schema enforcement and quality checks
5. **Pipeline Design**: Modular, testable, and monitorable components
6. **Configuration**: Environment-based config management

### 🔧 **Practical Implementation Patterns**

#### **Data Processing Pipeline**
```python
# Key components for production pipelines:
1. Input validation and schema enforcement
2. Error handling with detailed logging
3. Progress monitoring and metrics collection
4. Graceful failure handling and recovery
5. Resource cleanup (connections, files, etc.)
6. Performance monitoring and alerting
```

#### **Performance Optimization Checklist**
```python
# Before optimizing:
1. Profile to identify actual bottlenecks
2. Measure current performance baseline
3. Set specific performance targets
4. Test optimizations with realistic data
5. Monitor production performance
```

### 📊 **Interview Preparation Strategy**

#### **Technical Depth Levels**
1. **Basic**: Syntax, data types, control structures
2. **Intermediate**: OOP, decorators, context managers, error handling
3. **Advanced**: Metaclasses, descriptors, async programming, performance
4. **Expert**: System design, architecture patterns, production concerns

#### **Common Interview Categories**
1. **Language Fundamentals** (20%): Core Python concepts
2. **Data Structures & Algorithms** (25%): Implementation and optimization
3. **System Design** (20%): Scalable architecture patterns
4. **Data Engineering Scenarios** (25%): Real-world problem solving
5. **Code Quality & Testing** (10%): Best practices and methodologies

### 🎓 **Recommended Study Path**

#### **Week 1-2: Fundamentals**
- Python object model and memory management
- Data types, collections, and comprehensions
- Functions, decorators, and context managers
- Error handling and logging

#### **Week 3-4: Advanced Concepts**
- Concurrency: threading, multiprocessing, async/await
- Performance optimization techniques
- Testing strategies and frameworks
- Code quality tools and practices

#### **Week 5-6: Data Engineering Focus**
- Large dataset processing patterns
- Pipeline design and monitoring
- Data validation and quality assurance
- Integration with databases and APIs

#### **Week 7-8: System Design & Practice**
- Scalable architecture patterns
- Production deployment considerations
- Mock interviews and coding challenges
- Real-world project implementation

### 🚀 **Next Steps**

1. **Practice Coding**: Implement the examples in this guide
2. **Build Projects**: Create end-to-end data pipelines
3. **Read Code**: Study open-source Python projects
4. **Join Communities**: Participate in Python and data engineering forums
5. **Stay Updated**: Follow Python enhancement proposals (PEPs)

### 📖 **Additional Resources**

- **Official Documentation**: [python.org](https://docs.python.org/)
- **Performance**: "High Performance Python" by Micha Gorelick
- **Concurrency**: "Effective Python" by Brett Slatkin
- **Data Engineering**: "Designing Data-Intensive Applications" by Martin Kleppmann
- **Testing**: "Test-Driven Development with Python" by Harry Percival

---

**Remember**: The best way to master Python for data engineering is through hands-on practice with real-world datasets and production scenarios. Focus on understanding the underlying concepts rather than memorizing syntax.

---

## Interview Preparation Checklist

### 📋 **Before the Interview**
- [ ] Review all fundamental concepts (memory management, GIL, data structures)
- [ ] Practice coding challenges (LRU cache, frequent elements, data pipelines)
- [ ] Understand data engineering specific scenarios (large files, databases, async)
- [ ] Prepare questions about the role and company

### 🎯 **During the Interview**
- [ ] Think out loud while coding
- [ ] Ask clarifying questions about requirements
- [ ] Consider edge cases and error handling
- [ ] Discuss trade-offs and alternatives
- [ ] Write clean, readable code with proper variable names

### 📈 **Key Success Factors**
- **Problem-solving approach**: Break down complex problems systematically
- **Code quality**: Clean, maintainable, and well-documented solutions
- **Communication**: Clear explanation of concepts and reasoning
- **Production awareness**: Understanding of real-world constraints and scalability

---

## Performance Optimization Quick Reference

### 🔍 **Profiling Tools**
```python
import cProfile
import timeit

# Profile execution time
cProfile.run('your_function()')

# Benchmark operations
time_taken = timeit.timeit('sum([1,2,3,4,5])', number=1000000)
```

### ⚡ **Optimization Techniques**
1. **Use built-in functions** (sum, max, min, sorted)
2. **Choose right data structures** (set for membership, dict for lookups)
3. **Leverage NumPy** for numerical operations
4. **Use generators** for large datasets
5. **Cache expensive operations** with @lru_cache
6. **Profile before optimizing**

### 🎯 **Data Engineering Specific**
- **Chunking**: Process large files in pieces
- **Streaming**: One-record-at-a-time processing
- **Parallel processing**: Use multiprocessing for CPU-bound tasks
- **Async I/O**: Concurrent operations for I/O-bound tasks
- **Connection pooling**: Efficient database connections