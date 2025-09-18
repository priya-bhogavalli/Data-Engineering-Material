# ClickHouse - Key Concepts

## Overview
ClickHouse is a columnar database management system (DBMS) designed for online analytical processing (OLAP) with exceptional performance for analytical queries.

## Core Architecture
- **Columnar storage**: Data stored in columns for analytical workloads
- **Vectorized execution**: SIMD operations for high performance
- **Distributed architecture**: Horizontal scaling across multiple nodes
- **Real-time ingestion**: High-speed data ingestion capabilities
- **Compression**: Advanced compression algorithms
- **Parallel processing**: Multi-core query execution

## Key Features
- **High performance**: Billions of rows processed per second
- **SQL compatibility**: Standard SQL with extensions
- **Real-time analytics**: Sub-second query response times
- **Horizontal scaling**: Linear scalability across nodes
- **Data compression**: 10x compression ratios typical
- **Fault tolerance**: Built-in replication and recovery

## Storage Engines
- **MergeTree**: Primary engine for analytical workloads
- **ReplacingMergeTree**: Deduplication of records
- **SummingMergeTree**: Pre-aggregation of numeric columns
- **AggregatingMergeTree**: Complex aggregation functions
- **CollapsingMergeTree**: Handle UPDATE/DELETE operations
- **VersionedCollapsingMergeTree**: Versioned collapsing with ordering

## Data Types
- **Numeric**: Int8-Int64, UInt8-UInt64, Float32/64, Decimal
- **String**: String, FixedString
- **Date/Time**: Date, DateTime, DateTime64
- **Arrays**: Array(T) for any type T
- **Tuples**: Tuple(T1, T2, ...) for structured data
- **Nested**: Nested structures for complex data
- **Special**: UUID, IPv4, IPv6, Enum

## Distributed Features
- **Sharding**: Automatic data distribution across shards
- **Replication**: Asynchronous multi-master replication
- **Distributed tables**: Query across multiple nodes
- **Load balancing**: Automatic query load balancing
- **Fault tolerance**: Automatic failover and recovery
- **Cluster management**: ZooKeeper integration for coordination