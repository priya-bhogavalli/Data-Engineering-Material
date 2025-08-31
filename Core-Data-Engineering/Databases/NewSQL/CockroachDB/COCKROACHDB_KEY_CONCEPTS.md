# CockroachDB - Key Concepts

## Overview
CockroachDB is a distributed SQL database built for cloud-native applications that provides ACID transactions, horizontal scaling, and strong consistency across multiple regions.

## Core Concepts

### Architecture
- **Distributed**: Data distributed across multiple nodes
- **Shared-Nothing**: Each node is independent
- **Multi-Region**: Global deployment with local latency
- **Cloud-Native**: Designed for containerized environments

### ACID Properties
- **Atomicity**: All-or-nothing transactions
- **Consistency**: Strong consistency guarantees
- **Isolation**: Serializable isolation by default
- **Durability**: Data persisted across node failures

### Scaling Model
- **Horizontal Scaling**: Add nodes to increase capacity
- **Automatic Rebalancing**: Data automatically redistributed
- **No Sharding Complexity**: Transparent to applications
- **Linear Performance**: Performance scales with nodes

### Consistency Model
- **Strong Consistency**: Linearizable reads and writes
- **Consensus Protocol**: Uses Raft for consistency
- **Multi-Version Concurrency Control (MVCC)**: Snapshot isolation
- **Clock Synchronization**: Hybrid logical clocks

### Data Distribution
- **Ranges**: Data split into contiguous key ranges
- **Replicas**: Each range replicated 3+ times
- **Leaseholder**: One replica handles reads/writes
- **Followers**: Other replicas for fault tolerance

### SQL Compatibility
- **PostgreSQL Wire Protocol**: Compatible with PostgreSQL drivers
- **Standard SQL**: Supports most SQL features
- **Transactions**: Full ACID transaction support
- **Joins**: Distributed joins across nodes

### Fault Tolerance
- **Node Failures**: Survives individual node failures
- **Network Partitions**: Continues operating during splits
- **Automatic Recovery**: Failed nodes automatically recovered
- **Zero-Downtime Upgrades**: Rolling upgrades without downtime

## Key Features

### Multi-Region Deployment
- **Geo-Partitioning**: Data locality for compliance
- **Follow-the-Workload**: Data moves closer to users
- **Regional Tables**: Pin tables to specific regions
- **Zone Configurations**: Control replica placement

### Performance Features
- **Vectorized Execution**: Columnar query processing
- **Cost-Based Optimizer**: Intelligent query planning
- **Parallel Processing**: Distributed query execution
- **Caching**: Multiple levels of caching

### Operational Features
- **Admin UI**: Built-in monitoring and management
- **Metrics**: Comprehensive performance metrics
- **Backup/Restore**: Point-in-time recovery
- **Change Data Capture**: Stream changes to external systems

## Use Cases
- **Global Applications**: Multi-region deployments
- **Financial Services**: ACID compliance requirements
- **E-commerce**: High availability and consistency
- **SaaS Applications**: Multi-tenant architectures
- **Real-time Analytics**: Consistent analytical queries