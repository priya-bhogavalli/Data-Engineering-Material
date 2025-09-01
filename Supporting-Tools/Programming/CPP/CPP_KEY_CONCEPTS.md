# C++ Programming - Key Concepts

## Overview
C++ is an object-oriented programming language that extends C with classes, objects, inheritance, and generic programming features while maintaining low-level control and performance.

## Object-Oriented Programming

### Classes & Objects
- **Class Definition**: Blueprint for objects
- **Object Instantiation**: Creating class instances
- **Member Variables**: Object state storage
- **Member Functions**: Object behavior methods
- **Access Specifiers**: public, private, protected

### Encapsulation
- **Data Hiding**: Private member protection
- **Getter/Setter**: Controlled data access
- **Interface Design**: Public method contracts
- **Implementation Hiding**: Internal complexity abstraction
- **Const Correctness**: Immutable object guarantees

### Inheritance
- **Base Classes**: Parent class definitions
- **Derived Classes**: Child class extensions
- **Virtual Functions**: Runtime polymorphism
- **Abstract Classes**: Pure virtual functions
- **Multiple Inheritance**: Multiple parent classes

### Polymorphism
- **Virtual Functions**: Dynamic method dispatch
- **Function Overloading**: Same name, different parameters
- **Operator Overloading**: Custom operator behavior
- **Templates**: Compile-time polymorphism
- **Runtime Type Information**: Dynamic type checking

## Memory Management

### Dynamic Allocation
- **new/delete**: Object allocation/deallocation
- **new[]/delete[]**: Array allocation/deallocation
- **Smart Pointers**: Automatic memory management
- **RAII**: Resource Acquisition Is Initialization
- **Memory Leaks**: Prevention and detection

### Smart Pointers (C++11+)
- **unique_ptr**: Exclusive ownership
- **shared_ptr**: Shared ownership with reference counting
- **weak_ptr**: Non-owning weak references
- **make_unique/make_shared**: Safe pointer creation
- **Custom Deleters**: Specialized cleanup functions

## Templates & Generic Programming

### Function Templates
- **Template Parameters**: Generic type placeholders
- **Template Instantiation**: Compiler code generation
- **Template Specialization**: Specific type implementations
- **Variadic Templates**: Variable argument templates
- **SFINAE**: Substitution Failure Is Not An Error

### Class Templates
- **Generic Classes**: Type-parameterized classes
- **Template Inheritance**: Template-based inheritance
- **Template Friends**: Friend function templates
- **Partial Specialization**: Specialized template variants
- **Template Metaprogramming**: Compile-time computation

## Standard Template Library (STL)

### Containers
- **vector**: Dynamic arrays
- **list**: Doubly-linked lists
- **map/unordered_map**: Key-value associations
- **set/unordered_set**: Unique element collections
- **queue/stack**: FIFO/LIFO containers

### Iterators
- **Iterator Types**: Input, output, forward, bidirectional, random access
- **Iterator Operations**: Traversal and manipulation
- **Range-based Loops**: Simplified iteration syntax
- **Iterator Invalidation**: Container modification effects
- **Custom Iterators**: User-defined iteration logic

### Algorithms
- **Sorting**: sort(), stable_sort(), partial_sort()
- **Searching**: find(), binary_search(), lower_bound()
- **Transformation**: transform(), for_each()
- **Numeric**: accumulate(), inner_product()
- **Set Operations**: set_union(), set_intersection()

## Modern C++ Features

### C++11 Features
- **Auto Keyword**: Type deduction
- **Range-based Loops**: Simplified iteration
- **Lambda Expressions**: Anonymous functions
- **Move Semantics**: Efficient resource transfer
- **Nullptr**: Type-safe null pointer

### C++14/17/20 Features
- **Generic Lambdas**: Template lambda expressions
- **Structured Bindings**: Multiple variable assignment
- **Concepts**: Template constraints
- **Coroutines**: Cooperative multitasking
- **Modules**: Improved compilation model

## Exception Handling
- **try/catch**: Exception handling blocks
- **throw**: Exception generation
- **Exception Classes**: Standard exception hierarchy
- **RAII**: Exception-safe resource management
- **noexcept**: Exception specification

## Best Practices
- **RAII**: Resource management principles
- **Const Correctness**: Immutability guarantees
- **Move Semantics**: Efficient resource handling
- **Template Design**: Generic programming patterns
- **Modern C++**: Leverage latest language features