# Apache Hadoop Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Architecture & Performance (91-120)](#architecture--performance-91-120)
5. [HDFS & Storage (121-150)](#hdfs--storage-121-150)
6. [MapReduce & YARN (151-180)](#mapreduce--yarn-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is Apache Hadoop and what are its core components?

**Answer:** Apache Hadoop is an open-source framework for distributed storage and processing of large datasets across clusters of commodity hardware.

**Core Components:**
- **HDFS (Hadoop Distributed File System)**: Distributed storage system
- **MapReduce**: Programming model for distributed processing
- **YARN (Yet Another Resource Negotiator)**: Resource management and job scheduling

### 2. Explain HDFS architecture and its key components.

**Answer:** HDFS follows a master-slave architecture with fault tolerance through replication.

**Key Components:**
- **NameNode**: Master node storing metadata and namespace
- **DataNode**: Slave nodes storing actual data blocks
- **Secondary NameNode**: Assists NameNode with checkpointing

### 3. What is a block in HDFS and what is the default block size?

**Answer:** A block is the minimum unit of data storage in HDFS.

**Characteristics:**
- **Default Size**: 128MB (configurable)
- **Replication**: 3 copies by default
- **Distribution**: Blocks spread across multiple DataNodes

### 4. How does HDFS achieve fault tolerance?

**Answer:** HDFS achieves fault tolerance through data replication and automatic recovery.

**Mechanisms:**
- **Block Replication**: Multiple copies of each block
- **Heartbeat Monitoring**: DataNodes send regular heartbeats
- **Automatic Recovery**: Failed blocks re-replicated automatically

### 5. What is MapReduce and explain its phases?

**Answer:** MapReduce is a programming model for processing large datasets in parallel.

**Phases:**
- **Map**: Process input data and emit key-value pairs
- **Shuffle & Sort**: Group and sort intermediate data
- **Reduce**: Aggregate values for each key

### 6. What is YARN and why was it introduced?

**Answer:** YARN is Hadoop's resource management system introduced in Hadoop 2.0.

**Benefits:**
- **Multi-tenancy**: Multiple applications can run simultaneously
- **Resource Efficiency**: Better resource utilization
- **Scalability**: Supports various processing frameworks

### 7. Explain the difference between NameNode and DataNode.

**Answer:** NameNode and DataNode have different roles in HDFS architecture.

**NameNode:**
- Stores metadata and filesystem namespace
- Manages block locations and replication
- Single point of coordination

**DataNode:**
- Stores actual data blocks
- Serves read/write requests
- Reports block status to NameNode

### 8. What is rack awareness in Hadoop?

**Answer:** Rack awareness is Hadoop's knowledge of network topology for optimal data placement.

**Benefits:**
- **Fault Tolerance**: Replicas placed across different racks
- **Network Efficiency**: Reduces cross-rack network traffic
- **Performance**: Improves data locality

### 9. How does Hadoop handle small files problem?

**Answer:** Small files create overhead in HDFS due to metadata storage.

**Solutions:**
- **HAR Files**: Hadoop Archive files
- **SequenceFiles**: Combine small files into larger ones
- **CombineFileInputFormat**: Process multiple small files in single mapper

### 10. What is data locality in Hadoop?

**Answer:** Data locality means processing data where it's stored to minimize network overhead.

**Levels:**
- **Node-local**: Task runs on same node as data
- **Rack-local**: Task runs on same rack as data
- **Off-switch**: Task runs on different rack

### 11. Explain Hadoop's write-once, read-many model.

**Answer:** HDFS is designed for write-once, read-many access patterns.

**Characteristics:**
- **Immutable Files**: Files cannot be modified after creation
- **Append Support**: Limited append operations available
- **Optimized Reads**: Designed for high-throughput reads

### 12. What is the role of Secondary NameNode?

**Answer:** Secondary NameNode assists the primary NameNode with checkpointing.

**Functions:**
- **Checkpoint Creation**: Merges fsimage and edits log
- **Backup**: Maintains backup of namespace
- **Not a Failover**: Cannot replace failed NameNode

### 13. How does MapReduce handle failures?

**Answer:** MapReduce provides fault tolerance through task retry and speculative execution.

**Mechanisms:**
- **Task Retry**: Failed tasks automatically retried
- **Speculative Execution**: Slow tasks re-executed on other nodes
- **Data Recovery**: Input data re-read from HDFS replicas

### 14. What are the different schedulers in YARN?

**Answer:** YARN provides multiple schedulers for resource allocation.

**Types:**
- **FIFO Scheduler**: First-in-first-out scheduling
- **Capacity Scheduler**: Hierarchical queues with guaranteed capacity
- **Fair Scheduler**: Fair sharing of resources among applications

### 15. Explain the concept of replication factor in HDFS.

**Answer:** Replication factor determines how many copies of each block are stored.

**Default Configuration:**
- **Replication Factor**: 3
- **Placement Strategy**: One replica on local node, one on different rack
- **Configurable**: Can be set per file or globally