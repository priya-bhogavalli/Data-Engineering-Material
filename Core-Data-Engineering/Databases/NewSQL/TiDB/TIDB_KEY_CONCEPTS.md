# TiDB - Key Concepts

## Overview
TiDB is an open-source, distributed SQL database that supports Hybrid Transactional/Analytical Processing (HTAP) workloads with MySQL compatibility and horizontal scalability.

## Core Architecture

### Components
- **TiDB Server**: Stateless SQL layer (MySQL compatible)
- **TiKV**: Distributed key-value storage engine
- **PD (Placement Driver)**: Cluster metadata and scheduling
- **TiFlash**: Columnar storage for analytical workloads

### HTAP Architecture
- **OLTP**: Row-based storage in TiKV for transactions
- **OLAP**: Columnar storage in TiFlash for analytics
- **Real-time Sync**: Automatic data synchronization between stores
- **Unified SQL**: Single interface for both workloads

### Distributed Storage
- **Region**: Basic unit of data distribution (96MB default)
- **Raft Groups**: Each region replicated using Raft consensus
- **Multi-Raft**: Multiple Raft groups per node
- **Auto-Sharding**: Automatic data partitioning and rebalancing

## Key Features

### MySQL Compatibility
- **Protocol**: MySQL wire protocol compatibility
- **SQL**: Supports most MySQL SQL syntax
- **Drivers**: Works with existing MySQL drivers
- **Migration**: Easy migration from MySQL

### ACID Properties
- **Distributed Transactions**: ACID across multiple nodes
- **Snapshot Isolation**: Default isolation level
- **Optimistic Concurrency**: Optimistic transaction model
- **Two-Phase Commit**: Ensures transaction atomicity

### Scalability
- **Horizontal Scaling**: Add nodes to increase capacity
- **Elastic**: Scale compute and storage independently
- **Auto-Rebalancing**: Automatic load distribution
- **Linear Performance**: Performance scales with cluster size

### High Availability
- **Multi-Replica**: Data replicated across multiple nodes
- **Automatic Failover**: Leader election via Raft
- **Cross-AZ Deployment**: Deploy across availability zones
- **Zero-Downtime**: Rolling upgrades without downtime

## Storage Engines

### TiKV (Row Store)
- **LSM-Tree**: Log-structured merge tree storage
- **RocksDB**: Built on RocksDB storage engine
- **MVCC**: Multi-version concurrency control
- **Distributed**: Horizontally scalable key-value store

### TiFlash (Column Store)
- **Columnar**: Optimized for analytical queries
- **Real-time Sync**: Asynchronous replication from TiKV
- **MPP**: Massively parallel processing
- **Compression**: Efficient data compression

## Transaction Model

### Optimistic Concurrency
- **Read Phase**: Read data without locks
- **Validation Phase**: Check for conflicts at commit
- **Write Phase**: Apply changes if no conflicts
- **Retry Logic**: Automatic retry on conflicts

### Pessimistic Concurrency
- **Lock-based**: Acquire locks during execution
- **MySQL Compatible**: Similar to MySQL behavior
- **Deadlock Detection**: Automatic deadlock resolution
- **Configurable**: Can switch between models

## Placement Rules
- **Flexible Placement**: Control data placement across nodes
- **Compliance**: Meet data residency requirements
- **Performance**: Optimize for access patterns
- **Cost**: Balance performance and cost

## Use Cases
- **HTAP Workloads**: Mixed transactional and analytical
- **MySQL Migration**: Scaling existing MySQL applications
- **Real-time Analytics**: Analytics on fresh transactional data
- **Multi-tenant SaaS**: Scalable multi-tenant applications
- **Financial Services**: ACID compliance with scale