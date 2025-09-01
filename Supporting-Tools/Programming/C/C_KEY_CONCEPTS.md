# C Programming - Key Concepts

## Overview
C is a general-purpose, procedural programming language that provides low-level access to memory and system resources, making it ideal for system programming and embedded systems.

## Core Language Features

### Data Types
- **Basic Types**: int, char, float, double
- **Modifiers**: short, long, signed, unsigned
- **Derived Types**: arrays, pointers, structures, unions
- **Void Type**: Represents no value
- **Size Operators**: sizeof() for memory requirements

### Memory Management
- **Stack**: Automatic variable storage
- **Heap**: Dynamic memory allocation
- **malloc/free**: Dynamic memory functions
- **calloc/realloc**: Advanced allocation functions
- **Memory Leaks**: Proper cleanup practices

### Pointers
- **Address Operators**: & (address-of), * (dereference)
- **Pointer Arithmetic**: Navigate memory addresses
- **Function Pointers**: Store function addresses
- **Void Pointers**: Generic pointer type
- **Pointer Arrays**: Arrays of pointer variables

## Control Structures

### Conditional Statements
- **if/else**: Basic conditional execution
- **switch/case**: Multi-way branching
- **Ternary Operator**: Conditional expressions
- **Logical Operators**: &&, ||, !
- **Comparison Operators**: ==, !=, <, >, <=, >=

### Loops
- **for**: Counter-controlled loops
- **while**: Condition-controlled loops
- **do-while**: Post-test loops
- **break/continue**: Loop control statements
- **Nested Loops**: Loops within loops

## Functions & Scope

### Function Definition
- **Return Types**: Function output specification
- **Parameters**: Input value passing
- **Local Variables**: Function-scoped variables
- **Static Variables**: Persistent local variables
- **Recursion**: Functions calling themselves

### Scope Rules
- **Global Scope**: File-level visibility
- **Local Scope**: Block-level visibility
- **Function Scope**: Function parameter visibility
- **Static Scope**: Limited global visibility
- **External Linkage**: Cross-file visibility

## Advanced Features

### Structures & Unions
- **struct**: Grouped data elements
- **union**: Overlapping memory storage
- **typedef**: Type aliasing
- **Bit Fields**: Compact data storage
- **Nested Structures**: Structures within structures

### File I/O
- **FILE Pointer**: File handle management
- **fopen/fclose**: File opening and closing
- **fread/fwrite**: Binary file operations
- **fprintf/fscanf**: Formatted file I/O
- **Error Handling**: File operation validation

### Preprocessor
- **#include**: Header file inclusion
- **#define**: Macro definitions
- **#ifdef/#endif**: Conditional compilation
- **#pragma**: Compiler directives
- **Macro Functions**: Parameterized macros

## System Programming

### System Calls
- **Process Management**: fork(), exec(), wait()
- **File Operations**: open(), read(), write(), close()
- **Memory Management**: mmap(), munmap()
- **Signal Handling**: signal(), sigaction()
- **Inter-process Communication**: pipes, shared memory

### Low-level Operations
- **Bit Manipulation**: Bitwise operators
- **Hardware Interface**: Direct hardware access
- **Assembly Integration**: Inline assembly code
- **Interrupt Handling**: System interrupt processing
- **Device Drivers**: Hardware abstraction

## Best Practices
- **Memory Safety**: Prevent buffer overflows
- **Error Checking**: Validate function returns
- **Code Organization**: Modular design principles
- **Documentation**: Clear code comments
- **Testing**: Unit and integration testing