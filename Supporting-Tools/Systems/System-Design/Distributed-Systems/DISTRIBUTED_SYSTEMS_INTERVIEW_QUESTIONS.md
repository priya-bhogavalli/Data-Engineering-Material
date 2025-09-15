# Distributed Systems - Interview Questions

## Basic Level Questions

### 1. What is a distributed system and what are its key characteristics?
**Answer:** A distributed system is a collection of independent computers that appears to users as a single coherent system. Key characteristics include:
- **Concurrency**: Multiple processes executing simultaneously
- **No global clock**: Lack of synchronized time across nodes
- **Independent failures**: Components can fail independently
- **Scalability**: Ability to handle increased load by adding resources
- **Transparency**: Users see the system as a single entity
- **Fault tolerance**: System continues operating despite failures

### 2. Explain the CAP theorem and its implications.
**Answer:** The CAP theorem states that in a distributed system, you can only guarantee two of the following three properties:
- **Consistency**: All nodes see the same data simultaneously
- **Availability**: System remains operational and responsive
- **Partition tolerance**: System continues despite network failures

**Implications:**
- **CP Systems**: Sacrifice availability for consistency (e.g., traditional RDBMS)
- **AP Systems**: Sacrifice consistency for availability (e.g., DNS, web caches)
- **CA Systems**: Only possible without network partitions (not truly distributed)

### 3. What is eventual consistency and when is it used?
**Answer:** Eventual consistency guarantees that if no new updates are made, all replicas will eventually converge to the same value. Characteristics:
- **Weak consistency model**: Temporary inconsistencies are allowed
- **Convergence guarantee**: All replicas eventually agree
- **High availability**: System remains available during inconsistencies
- **Use cases**: Social media feeds, DNS, shopping carts, collaborative editing
- **Examples**: Amazon DynamoDB, Cassandra, CouchDB

### 4. Explain the difference between horizontal and vertical scaling.
**Answer:**
**Vertical Scaling (Scale Up):**
- Adding more power (CPU, RAM) to existing machines
- Simpler to implement and manage
- Limited by hardware constraints
- Single point of failure
- Examples: Upgrading server hardware

**Horizontal Scaling (Scale Out):**
- Adding more machines to the resource pool
- Better fault tolerance and theoretically unlimited scaling
- More complex to implement and manage
- Requires distributed system design
- Examples: Adding more web servers, database sharding

### 5. What are the main challenges in distributed systems?
**Answer:** Key challenges include:
- **Network failures**: Partial failures, network partitions, message loss
- **Concurrency**: Race conditions, deadlocks, coordination
- **Consistency**: Maintaining data consistency across nodes
- **Fault tolerance**: Handling node failures gracefully
- **Security**: Distributed authentication, authorization, encryption
- **Performance**: Latency, throughput, load balancing
- **Complexity**: Debugging, monitoring, deployment

## Intermediate Level Questions

### 6. Explain different consistency models in distributed systems.
**Answer:** Consistency models define the behavior of reads and writes:

**Strong Consistency:**
- **Linearizability**: Operations appear instantaneous at some point between start and end
- **Sequential consistency**: All processes see operations in the same order
- **Causal consistency**: Causally related operations are seen in the same order

**Weak Consistency:**
- **Eventual consistency**: Replicas converge eventually
- **Read-your-writes**: Process reads its own writes
- **Monotonic reads**: Successive reads return same or newer values
- **Monotonic writes**: Writes are applied in order

### 7. What is the Byzantine Generals Problem and how is it solved?
**Answer:** The Byzantine Generals Problem addresses consensus in the presence of malicious or faulty nodes that may send conflicting information.

**Problem**: Achieving agreement when some nodes may be Byzantine (arbitrary failures)
**Solutions:**
- **Byzantine Fault Tolerance (BFT)**: Algorithms that tolerate up to f Byzantine failures with 3f+1 total nodes
- **Practical BFT (pBFT)**: Efficient BFT algorithm for permissioned networks
- **Proof of Work**: Used in Bitcoin to achieve consensus in permissionless networks
- **Proof of Stake**: Alternative consensus mechanism with lower energy consumption

### 8. Explain the concept of vector clocks and their use in distributed systems.
**Answer:** Vector clocks are a mechanism for capturing causal relationships between events in distributed systems:

**Structure**: Each process maintains a vector of logical timestamps
**Rules**:
- Increment own clock on local events
- Include vector clock in messages
- Update clock on message receipt (element-wise maximum + increment own)

**Uses**:
- Detecting causal relationships between events
- Implementing causal consistency
- Conflict detection in distributed databases
- Debugging distributed systems

**Example**: Process A: [2,0,1], Process B: [1,3,2] → No causal relationship

### 9. What is sharding and what are the different sharding strategies?
**Answer:** Sharding is partitioning data across multiple databases or servers:

**Strategies:**
1. **Range-based**: Partition by value ranges (e.g., A-M, N-Z)
   - Pros: Simple, range queries efficient
   - Cons: Hotspots, uneven distribution

2. **Hash-based**: Use hash function to determine shard
   - Pros: Even distribution, no hotspots
   - Cons: Range queries difficult, resharding complex

3. **Directory-based**: Lookup service maps keys to shards
   - Pros: Flexible, easy resharding
   - Cons: Additional complexity, lookup overhead

4. **Composite**: Combine multiple strategies
   - Example: Hash + range for time-series data

### 10. Explain the concept of consensus algorithms and compare Raft and Paxos.
**Answer:** Consensus algorithms ensure multiple nodes agree on a single value despite failures:

**Raft:**
- **Leader-based**: Single leader handles all client requests
- **Simpler**: Easier to understand and implement
- **Log replication**: Leader replicates log entries to followers
- **Leader election**: Randomized timeouts for leader election
- **Use cases**: etcd, Consul, CockroachDB

**Paxos:**
- **More complex**: Harder to understand and implement correctly
- **Multi-Paxos**: Optimization for multiple consensus instances
- **Theoretical foundation**: Proven correctness properties
- **Flexible**: Various optimizations and variants
- **Use cases**: Google Chubby, Apache Cassandra (modified)

## Advanced Level Questions

### 11. Design a distributed cache system like Redis Cluster.
**Answer:** Distributed cache system design:
```
Architecture Components:
1. Cluster Topology
   - Hash slot-based partitioning (16384 slots)
   - Consistent hashing for even distribution
   - Master-slave replication for availability

2. Data Distribution
   - CRC16 hash function for key mapping
   - Automatic resharding during cluster changes
   - Migration of slots between nodes

3. Consistency Model
   - Eventual consistency for replicas
   - Strong consistency for master writes
   - Configurable consistency levels

4. Failure Handling
   - Automatic failover to slaves
   - Split-brain prevention
   - Cluster membership management

Implementation Details:
- Gossip protocol for cluster communication
- Redis Sentinel for monitoring and failover
- Client-side routing with cluster topology
- Backup and restore mechanisms
```

### 12. How would you design a distributed message queue system?
**Answer:** Distributed message queue design:
```
Core Components:
1. Broker Cluster
   - Multiple broker nodes for scalability
   - Leader election for partition management
   - Load balancing across brokers

2. Topic Partitioning
   - Horizontal partitioning for scalability
   - Configurable replication factor
   - Ordered delivery within partitions

3. Producer Design
   - Batching for throughput optimization
   - Acknowledgment modes (fire-and-forget, sync, async)
   - Retry mechanisms with exponential backoff

4. Consumer Design
   - Consumer groups for parallel processing
   - Offset management and commit strategies
   - Rebalancing during consumer changes

Features:
- Persistent storage with configurable retention
- Exactly-once delivery semantics
- Dead letter queues for failed messages
- Monitoring and metrics collection

Technologies: Apache Kafka, Apache Pulsar, Amazon SQS
```

### 13. Explain how you would implement distributed transactions.
**Answer:** Distributed transaction implementation:
```
Two-Phase Commit (2PC):
Phase 1 - Prepare:
- Coordinator asks all participants to prepare
- Participants vote yes/no and lock resources
- Coordinator collects all votes

Phase 2 - Commit/Abort:
- If all yes: coordinator sends commit
- If any no: coordinator sends abort
- Participants execute decision and release locks

Limitations:
- Blocking protocol (coordinator failure)
- Not partition tolerant
- Performance overhead

Alternatives:
1. Saga Pattern
   - Sequence of local transactions
   - Compensating actions for rollback
   - Choreography or orchestration

2. Event Sourcing
   - Immutable event log
   - Eventual consistency
   - Replay for recovery

3. CQRS (Command Query Responsibility Segregation)
   - Separate read and write models
   - Eventual consistency between models
   - Optimized for specific use cases
```

### 14. Design a distributed file system like HDFS or GFS.
**Answer:** Distributed file system design:
```
Architecture:
1. Master Node (NameNode)
   - Metadata management (file system namespace)
   - Block location tracking
   - Replication management
   - Client request coordination

2. Data Nodes
   - Block storage and retrieval
   - Heartbeat and block reports to master
   - Data replication and recovery
   - Local storage management

3. Client Interface
   - File system API (create, read, write, delete)
   - Block-level operations
   - Caching and prefetching

Key Features:
1. Large File Optimization
   - Large block sizes (64MB-256MB)
   - Sequential access patterns
   - Write-once, read-many model

2. Fault Tolerance
   - Block replication (default 3 replicas)
   - Automatic failure detection
   - Re-replication on node failure

3. Scalability
   - Horizontal scaling of data nodes
   - Namespace federation for large clusters
   - Load balancing across nodes

Consistency Model:
- Strong consistency for metadata
- Relaxed consistency for data blocks
- Append-only writes for simplicity
```

### 15. How would you design a globally distributed database system?
**Answer:** Global distributed database design:
```
Architecture Layers:
1. Global Distribution
   - Multi-region deployment
   - Data locality optimization
   - Cross-region replication

2. Partitioning Strategy
   - Geographic partitioning
   - Functional partitioning
   - Hybrid approaches

3. Consistency Management
   - Regional strong consistency
   - Global eventual consistency
   - Conflict resolution strategies

4. Transaction Management
   - Local transactions within regions
   - Cross-region coordination protocols
   - Compensation-based approaches

Technical Challenges:
1. Network Latency
   - WAN optimization techniques
   - Caching strategies
   - Asynchronous replication

2. Partition Tolerance
   - Split-brain prevention
   - Quorum-based decisions
   - Graceful degradation

3. Data Sovereignty
   - Compliance with local regulations
   - Data residency requirements
   - Encryption and privacy

Examples: Google Spanner, Amazon Aurora Global, CockroachDB
```

## Scenario-Based Questions

### 16. You're designing a real-time chat application for millions of users. How would you handle message delivery and consistency?
**Answer:** Real-time chat system design:
```
Architecture:
1. Connection Management
   - WebSocket servers for real-time connections
   - Connection pooling and load balancing
   - Horizontal scaling of connection servers

2. Message Routing
   - Message broker for reliable delivery
   - Topic-based routing by chat room/user
   - Message ordering within conversations

3. Storage Strategy
   - Message persistence for reliability
   - Sharding by user ID or chat room
   - Hot/cold data separation

4. Delivery Guarantees
   - At-least-once delivery semantics
   - Idempotency for duplicate handling
   - Offline message queuing

Consistency Model:
- Causal consistency for message ordering
- Eventual consistency for presence status
- Strong consistency for critical operations

Scalability Features:
- Auto-scaling based on connection count
- Geographic distribution for global users
- CDN for media content delivery
```

### 17. Design a distributed system for processing real-time financial transactions with ACID guarantees.
**Answer:** Financial transaction processing system:
```
Requirements:
- ACID properties for all transactions
- Sub-second response times
- 99.99% availability
- Regulatory compliance

Architecture:
1. Transaction Processing
   - Distributed transaction coordinator
   - Two-phase commit for ACID guarantees
   - Optimistic concurrency control

2. Data Management
   - Partitioned by account or region
   - Synchronous replication for consistency
   - Write-ahead logging for durability

3. Fault Tolerance
   - Active-passive failover
   - Automatic leader election
   - Circuit breakers for cascading failures

4. Performance Optimization
   - In-memory processing for hot data
   - Batch processing for non-critical operations
   - Hardware acceleration (FPGA/GPU)

Consistency Strategy:
- Strong consistency for account balances
- Linearizability for transaction ordering
- Snapshot isolation for read operations

Compliance Features:
- Immutable audit logs
- Real-time fraud detection
- Regulatory reporting capabilities
```

### 18. How would you handle a network partition in a distributed system serving critical user data?
**Answer:** Network partition handling strategy:
```
Detection:
1. Failure Detection
   - Heartbeat mechanisms
   - Timeout-based detection
   - Network monitoring tools

2. Partition Identification
   - Quorum-based decisions
   - Majority partition identification
   - Minority partition isolation

Response Strategies:
1. Availability-First (AP)
   - Continue serving requests in all partitions
   - Accept temporary inconsistencies
   - Implement conflict resolution

2. Consistency-First (CP)
   - Only majority partition serves writes
   - Minority partitions become read-only
   - Maintain strong consistency

3. Hybrid Approach
   - Critical data: consistency-first
   - Non-critical data: availability-first
   - Graceful degradation of features

Recovery Process:
1. Partition Healing
   - Automatic detection of network recovery
   - Data synchronization between partitions
   - Conflict resolution and merging

2. Consistency Restoration
   - Vector clock comparison
   - Last-writer-wins or custom resolution
   - Manual intervention for complex conflicts
```

### 19. Design a system to handle Black Friday-scale traffic spikes (100x normal load).
**Answer:** Traffic spike handling system:
```
Preparation:
1. Capacity Planning
   - Historical traffic analysis
   - Load testing and benchmarking
   - Resource provisioning strategies

2. Auto-Scaling Infrastructure
   - Horizontal pod autoscaling (Kubernetes)
   - Cloud auto-scaling groups
   - Predictive scaling based on patterns

Response Strategy:
1. Load Distribution
   - Global load balancers with geographic routing
   - CDN for static content and caching
   - Queue-based request handling

2. Service Degradation
   - Feature flags for non-essential features
   - Circuit breakers for failing services
   - Graceful degradation of user experience

3. Data Management
   - Read replicas for query distribution
   - Caching layers (Redis, Memcached)
   - Eventual consistency for non-critical data

4. Monitoring and Alerting
   - Real-time metrics and dashboards
   - Automated alerting and response
   - Capacity monitoring and scaling triggers

Technologies:
- Kubernetes for container orchestration
- Istio service mesh for traffic management
- Prometheus/Grafana for monitoring
- Apache Kafka for event streaming
```

### 20. You need to migrate a monolithic application to microservices while maintaining zero downtime. How would you approach this?
**Answer:** Zero-downtime microservices migration:
```
Migration Strategy:
1. Strangler Fig Pattern
   - Gradually replace monolith components
   - Route traffic between old and new systems
   - Incremental migration approach

2. Database Decomposition
   - Shared database initially
   - Gradual data migration
   - Event-driven synchronization

3. API Gateway Implementation
   - Centralized routing and load balancing
   - Version management and backward compatibility
   - Circuit breakers and rate limiting

Migration Phases:
Phase 1: Infrastructure Setup
- Container orchestration platform
- Service mesh implementation
- Monitoring and logging systems

Phase 2: Service Extraction
- Identify bounded contexts
- Extract services one by one
- Implement inter-service communication

Phase 3: Data Migration
- Database per service pattern
- Event sourcing for data synchronization
- Gradual cutover strategies

Phase 4: Traffic Migration
- Blue-green deployments
- Canary releases for risk mitigation
- Feature flags for rollback capability

Risk Mitigation:
- Comprehensive testing strategies
- Rollback procedures at each phase
- Performance monitoring and alerting
- Gradual traffic shifting (1%, 10%, 50%, 100%)
```