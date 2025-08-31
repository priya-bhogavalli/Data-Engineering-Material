# Memcached - Key Concepts

## Overview
Memcached is a high-performance, distributed memory caching system designed to speed up dynamic web applications by alleviating database load through caching frequently accessed data in RAM.

## Core Concepts

### Architecture
- **Client-Server Model**: Clients connect to memcached servers
- **Distributed**: Data distributed across multiple servers
- **No Replication**: Each key stored on only one server
- **Hash-based Distribution**: Consistent hashing for key distribution

### Key Features
- **In-Memory Storage**: All data stored in RAM
- **Key-Value Store**: Simple key-value data model
- **LRU Eviction**: Least Recently Used eviction policy
- **Multi-threaded**: Handles multiple concurrent connections
- **Protocol**: Simple text and binary protocols

### Data Types
- **Strings**: Only data type supported
- **Expiration**: TTL (Time To Live) for automatic expiration
- **Flags**: 32-bit unsigned integer for client use

### Operations
- **SET**: Store key-value pair
- **GET**: Retrieve value by key
- **DELETE**: Remove key-value pair
- **ADD**: Store only if key doesn't exist
- **REPLACE**: Store only if key exists
- **INCR/DECR**: Increment/decrement numeric values

### Memory Management
- **Slab Allocation**: Memory organized in slabs of different sizes
- **Page Size**: Default 1MB pages
- **Growth Factor**: Controls slab size progression (default 1.25)
- **Memory Limit**: Configurable maximum memory usage

### Limitations
- **No Persistence**: Data lost on restart
- **No Replication**: Single point of failure per key
- **No Authentication**: Basic security model
- **String Only**: Limited data type support

## Use Cases
- **Web Application Caching**: Session data, page fragments
- **Database Query Caching**: Expensive query results
- **API Response Caching**: External API call results
- **Computed Data**: Expensive calculations
- **User Sessions**: Session storage for web applications

## Best Practices
- **Key Naming**: Use consistent, descriptive key names
- **Expiration**: Set appropriate TTL values
- **Memory Monitoring**: Monitor memory usage and hit rates
- **Connection Pooling**: Reuse connections efficiently
- **Consistent Hashing**: Use for server distribution