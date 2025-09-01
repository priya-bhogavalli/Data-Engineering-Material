# Distributed Systems - Key Concepts

## Overview
Distributed systems are collections of independent computers that appear to users as a single coherent system, designed to achieve scalability, fault tolerance, and performance.

## Core Principles

### CAP Theorem
- **Consistency**: All nodes see same data simultaneously
- **Availability**: System remains operational
- **Partition Tolerance**: System continues despite network failures
- **Trade-offs**: Can only guarantee two of three
- **Real-world**: Choose CP or AP systems

### ACID vs BASE
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **BASE**: Basically Available, Soft state, Eventual consistency
- **Strong consistency**: ACID properties
- **Eventual consistency**: BASE properties
- **Use cases**: Different application requirements

## Consistency Models

### Strong Consistency
- **Linearizability**: Operations appear instantaneous
- **Sequential consistency**: Program order preservation
- **Causal consistency**: Cause-effect relationships
- **Implementation**: Consensus algorithms
- **Trade-offs**: Performance vs consistency

### Eventual Consistency
- **Convergence**: All replicas eventually consistent
- **Conflict resolution**: Handle concurrent updates
- **Vector clocks**: Track causality
- **CRDTs**: Conflict-free replicated data types
- **Applications**: Social media, DNS

## Distributed Algorithms

### Consensus Algorithms
- **Raft**: Leader-based consensus
- **Paxos**: Byzantine fault tolerance
- **PBFT**: Practical Byzantine fault tolerance
- **Use cases**: Leader election, state replication
- **Properties**: Safety and liveness

### Distributed Hash Tables
- **Consistent hashing**: Load distribution
- **Chord**: Finger table routing
- **Kademlia**: XOR metric routing
- **Applications**: P2P networks, distributed storage
- **Properties**: Scalability and fault tolerance

## Fault Tolerance

### Failure Types
- **Crash failures**: Node stops responding
- **Omission failures**: Messages not sent/received
- **Timing failures**: Performance degradation
- **Byzantine failures**: Arbitrary behavior
- **Network partitions**: Communication failures

### Fault Tolerance Techniques
- **Replication**: Data redundancy
- **Checkpointing**: State snapshots
- **Recovery**: Failure detection and repair
- **Circuit breakers**: Prevent cascade failures
- **Bulkheads**: Isolate failures

## Scalability Patterns

### Horizontal Scaling
- **Sharding**: Data partitioning
- **Load balancing**: Request distribution
- **Microservices**: Service decomposition
- **Stateless design**: No server affinity
- **Auto-scaling**: Dynamic capacity

### Vertical Scaling
- **Resource increase**: CPU, memory, storage
- **Limitations**: Hardware constraints
- **Cost**: Exponential increase
- **Simplicity**: No architectural changes
- **Temporary solution**: Scale-up limits

## Communication Patterns

### Synchronous Communication
- **Request-response**: Direct communication
- **RPC**: Remote procedure calls
- **REST APIs**: HTTP-based services
- **GraphQL**: Query language
- **Trade-offs**: Coupling vs simplicity

### Asynchronous Communication
- **Message queues**: Decoupled communication
- **Event streaming**: Real-time data flow
- **Pub/Sub**: Publisher-subscriber pattern
- **Event sourcing**: Event-driven architecture
- **Benefits**: Loose coupling, scalability

## Data Management

### Data Partitioning
- **Horizontal**: Row-based partitioning
- **Vertical**: Column-based partitioning
- **Functional**: Service-based partitioning
- **Hash-based**: Consistent hashing
- **Range-based**: Key range partitioning

### Data Replication
- **Master-slave**: Single writer, multiple readers
- **Master-master**: Multiple writers
- **Quorum**: Majority consensus
- **Conflict resolution**: Handle concurrent writes
- **Consistency levels**: Tunable consistency

## Performance Optimization
- **Caching**: Reduce latency
- **CDNs**: Geographic distribution
- **Connection pooling**: Resource reuse
- **Batch processing**: Throughput optimization
- **Monitoring**: Performance tracking