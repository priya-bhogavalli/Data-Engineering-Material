# CouchDB - Key Concepts

## Overview
Apache CouchDB is a document-oriented NoSQL database that uses JSON for documents, HTTP for API, and JavaScript for MapReduce queries with multi-master replication.

## Core Concepts

### Document Model
- **JSON Documents**: Native JSON document storage
- **Schema-free**: No predefined schema required
- **Document ID**: Unique identifier for each document
- **Revisions**: Built-in document versioning

### HTTP API
- **RESTful**: All operations via HTTP methods
- **GET**: Retrieve documents
- **PUT**: Create/update documents
- **DELETE**: Remove documents
- **POST**: Bulk operations

### ACID Properties
- **Atomicity**: Document-level atomicity
- **Consistency**: Eventually consistent
- **Isolation**: MVCC for concurrent access
- **Durability**: Append-only B-tree storage

### Replication
- **Multi-master**: Bidirectional replication
- **Conflict Resolution**: Automatic conflict detection
- **Continuous**: Real-time synchronization
- **Filtered**: Selective document replication

### Views and Indexing
- **MapReduce Views**: JavaScript-based indexing
- **Mango Queries**: Declarative query language
- **Secondary Indexes**: Custom indexing strategies
- **Built-in Reduce**: Common aggregation functions

## Key Features

### Offline-First
- **Local Storage**: Works without network
- **Sync When Available**: Automatic synchronization
- **Conflict Resolution**: Handles offline conflicts
- **Mobile Support**: Ideal for mobile applications

### Web-Native
- **HTTP Protocol**: Direct browser access
- **CORS Support**: Cross-origin requests
- **JSON**: Native web data format
- **REST API**: Standard web interfaces

### Fault Tolerance
- **Crash-Only Design**: Safe unexpected shutdowns
- **Incremental Replication**: Efficient sync
- **Automatic Recovery**: Self-healing capabilities
- **No Single Point of Failure**: Distributed architecture

## Use Cases
- **Mobile Applications**: Offline-first mobile apps
- **Content Management**: Document-based CMS
- **Real-time Collaboration**: Multi-user editing
- **IoT Applications**: Sensor data collection
- **Distributed Systems**: Multi-datacenter deployments