# Redis (In-Memory) - Key Concepts

## Overview
Redis is an in-memory data structure store used as database, cache, and message broker, supporting various data structures with atomic operations and persistence options.

## Core Data Structures

### Basic Types
- **Strings**: Binary-safe strings up to 512MB
- **Hashes**: Field-value pairs (like objects)
- **Lists**: Ordered collections of strings
- **Sets**: Unordered collections of unique strings
- **Sorted Sets**: Sets ordered by score

### Advanced Types
- **Bitmaps**: Bit-level operations on strings
- **HyperLogLog**: Probabilistic cardinality estimation
- **Geospatial**: Location-based data and queries
- **Streams**: Log-like data structure for messaging

## Memory Management

### Persistence Options
- **RDB**: Point-in-time snapshots
- **AOF**: Append-only file logging
- **Hybrid**: Combination of RDB and AOF
- **No persistence**: Pure in-memory mode

### Memory Optimization
- **Expiration**: TTL for automatic key removal
- **Eviction Policies**: LRU, LFU, random eviction
- **Memory Efficiency**: Optimized data structures
- **Compression**: String and hash compression

## High Availability

### Replication
- **Master-Slave**: Asynchronous replication
- **Read Replicas**: Scale read operations
- **Automatic Failover**: Redis Sentinel
- **Chain Replication**: Multi-level replication

### Clustering
- **Redis Cluster**: Automatic sharding
- **Hash Slots**: 16384 slots for data distribution
- **Gossip Protocol**: Node discovery and health
- **Resharding**: Online cluster reconfiguration

## Performance Features

### Atomic Operations
- **Single-threaded**: Eliminates race conditions
- **Transactions**: MULTI/EXEC for atomicity
- **Lua Scripts**: Server-side scripting
- **Pipelining**: Batch multiple commands

### Pub/Sub Messaging
- **Channels**: Topic-based messaging
- **Pattern Matching**: Wildcard subscriptions
- **Streams**: Advanced messaging with consumer groups
- **Blocking Operations**: Efficient polling

## Use Cases
- **Caching**: Application and session caching
- **Real-time Analytics**: Counters and metrics
- **Message Queues**: Task queues and pub/sub
- **Session Storage**: Web session management
- **Leaderboards**: Gaming and ranking systems