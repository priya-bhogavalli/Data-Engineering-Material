# MySQL - Key Concepts

## Overview
MySQL is an open-source relational database management system (RDBMS) that uses Structured Query Language (SQL) for database operations.

## Core Features
- **ACID compliance**: Atomicity, Consistency, Isolation, Durability
- **Multi-version concurrency control**: MVCC for concurrent access
- **Storage engines**: InnoDB, MyISAM, Memory, Archive
- **Replication**: Master-slave and master-master replication
- **Partitioning**: Horizontal partitioning for large tables
- **Full-text indexing**: Built-in full-text search capabilities

## Storage Engines
- **InnoDB**: Default engine with ACID compliance, foreign keys, row-level locking
- **MyISAM**: Fast but no transactions, table-level locking
- **Memory**: In-memory storage for temporary data
- **Archive**: Compressed storage for archival data
- **NDB**: Clustered storage engine for MySQL Cluster
- **Federated**: Access remote MySQL servers

## Replication Types
- **Asynchronous replication**: Default replication mode
- **Semi-synchronous replication**: Waits for acknowledgment from slaves
- **Group replication**: Multi-master replication with conflict detection
- **Binary log replication**: Statement-based, row-based, or mixed
- **GTID replication**: Global Transaction Identifier based replication

## Performance Features
- **Query cache**: Cache SELECT query results
- **Index optimization**: B-tree, hash, and full-text indexes
- **Partitioning**: Range, list, hash, and key partitioning
- **Connection pooling**: Manage database connections efficiently
- **Query optimization**: Cost-based query optimizer
- **Performance schema**: Built-in performance monitoring