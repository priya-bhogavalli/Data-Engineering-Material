# Apache Hadoop Key Concepts for Data Engineering

## 🏘️ Real-World Analogy: Hadoop as a Distributed Village Workshop System

> **Think of Hadoop as a village of specialized workshops that work together to handle massive construction projects that no single workshop could complete alone**

### 🎯 **The Analogy**
Hadoop is like a village of interconnected workshops where each workshop specializes in different tasks, but they all coordinate to complete large-scale projects. Just as a village can handle projects too big for any single workshop by distributing the work and sharing resources, Hadoop processes datasets too large for any single computer by distributing the work across many machines.

### 🔗 **Technical Mapping**
| Hadoop Concept | Village Workshop Equivalent | Why This Works |
|----------------|----------------------------|----------------|
| **HDFS (Distributed File System)** | Village storage warehouses with backup copies | Stores materials (data) across multiple locations with redundancy |
| **NameNode** | Village coordinator with master inventory | Knows where every piece of material is stored |
| **DataNodes** | Individual storage warehouses | Actually store the materials (data blocks) |
| **MapReduce** | Two-phase workshop process: preparation + assembly | Break work into manageable pieces, then combine results |
| **YARN** | Village resource manager | Allocates workers and tools to different projects |
| **Blocks** | Standardized material containers | Split large materials into manageable, uniform pieces |
| **Replication** | Multiple backup copies in different warehouses | Ensure materials aren't lost if one warehouse fails |
| **Cluster** | The entire village of workshops | All the computers working together |

### 💼 **Business Value**
- **Massive Scale**: Like a village handling projects no single workshop could manage
- **Cost-Effective**: Uses standard workshops (commodity hardware) instead of expensive specialized facilities
- **Fault Tolerant**: If one workshop fails, others continue with backup materials
- **Flexible**: Can handle different types of projects (structured/unstructured data)
- **Scalable**: Add more workshops to handle bigger projects

### 🏗️ **How It Works in Practice**
```
Traditional Single Computer vs Hadoop Village:
❌ Single Computer: One workshop trying to build an entire city
✅ Hadoop: Village of workshops, each building parts, then assembling together

Example - Processing 1TB of log files:
- Traditional: One computer works for days/weeks
- Hadoop: 100 computers each process 10GB in parallel, finish in hours
```

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [HDFS (Hadoop Distributed File System)](#hdfs-hadoop-distributed-file-system)
   - [MapReduce](#mapreduce)
   - [YARN (Yet Another Resource Negotiator)](#yarn-yet-another-resource-negotiator)
3. [Hadoop Architecture](#-hadoop-architecture)
4. [HDFS Deep Dive](#-hdfs-deep-dive)
5. [MapReduce Framework](#-mapreduce-framework)
6. [YARN Resource Management](#-yarn-resource-management)
7. [Hadoop Ecosystem](#-hadoop-ecosystem)
8. [Performance Optimization](#-performance-optimization)
9. [Configuration](#️-configuration)
10. [When to Use Hadoop](#-when-to-use-hadoop)
11. [Interview Focus Areas](#-interview-focus-areas)
12. [Quick References](#-quick-references)

---

## 🏘️ Real-World Analogy: Hadoop as a Village Storage Cooperative

> **Think of Apache Hadoop as a village cooperative where everyone contributes storage space and helps process the community's data together**

### 🎯 **The Analogy**
Hadoop is like a village where every household (server) contributes storage space to create a massive community warehouse. When someone needs to process large amounts of data, the entire village works together - some houses store the data, others help process it, and everyone coordinates to get the job done efficiently.

### 🔗 **Technical Mapping**
| Hadoop Concept | Village Equivalent | Why This Works |
|----------------|-------------------|----------------|
| **HDFS** | Community storage warehouse with multiple buildings | Distributed storage across many locations |
| **MapReduce** | Village work parties that divide big tasks | Everyone helps process large jobs together |
| **YARN** | Village coordinator who assigns work | Resource manager that allocates tasks efficiently |
| **NameNode** | Village record keeper | Knows where everything is stored |
| **DataNodes** | Individual storage buildings | Each house contributes storage space |
| **Replication** | Keeping copies in 3 different buildings | Backup copies ensure nothing is lost |
| **Commodity Hardware** | Using regular houses, not mansions | Cost-effective approach using standard equipment |

### 💼 **Business Value**
- **Cost-Effective**: Like a village cooperative, everyone shares costs instead of buying expensive individual solutions
- **Scalable**: Easy to add more houses (servers) to the village as it grows
- **Reliable**: If one house has problems, the village still functions with backup copies
- **Democratic**: No single point of failure - the village works together

---

## 🎯 Overview

Apache Hadoop is an open-source framework for distributed storage and processing of large datasets across clusters of commodity hardware using simple programming models.

**Key Benefits:**
- **Scalability**: Scales from single servers to thousands of machines
- **Fault Tolerance**: Handles hardware failures gracefully
- **Cost-Effective**: Uses commodity hardware instead of expensive specialized systems
- **Flexibility**: Processes structured, semi-structured, and unstructured data

## 📦 Core Components

### HDFS (Hadoop Distributed File System)
> **Like the village's distributed warehouse system with a master catalog**

**Definition**: Distributed file system designed to store very large files across multiple machines with high fault tolerance.

**Key Characteristics**:
- **Write-once, read-many**: *Like storing items in the warehouse once, then many people can access them*
- **Block-based storage**: *Files split into blocks (default 128MB) - like breaking large items into smaller pieces for easier storage*
- **Replication**: *Each block replicated 3 times by default - like keeping backup copies in 3 different buildings*
- **Master-slave architecture**: *NameNode (village record keeper) manages metadata, DataNodes (storage buildings) store actual data*

```bash
# HDFS basic commands
hdfs dfs -ls /                    # List root directory
hdfs dfs -put local.txt /hdfs/    # Upload file to HDFS
hdfs dfs -get /hdfs/file.txt .    # Download file from HDFS
hdfs dfs -cat /hdfs/file.txt      # Display file contents
```

### MapReduce
**Definition**: Programming model for processing large datasets in parallel across a Hadoop cluster.

**Key Phases**:
- **Map**: Process input data and emit key-value pairs
- **Shuffle & Sort**: Group and sort intermediate data by key
- **Reduce**: Aggregate values for each key to produce final output

```java
// MapReduce WordCount example
public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
    
    public void map(LongWritable key, Text value, Context context) {
        String[] words = value.toString().split("\\s+");
        for (String w : words) {
            word.set(w);
            context.write(word, one);
        }
    }
}
```

### YARN (Yet Another Resource Negotiator)
**Definition**: Resource management and job scheduling system for Hadoop 2.x and later.

**Key Components**:
- **ResourceManager**: Global resource scheduler
- **NodeManager**: Per-node resource manager
- **ApplicationMaster**: Per-application resource negotiator
- **Container**: Resource allocation unit (CPU, memory)

## 🏧 Hadoop Architecture

### Hadoop 1.x Architecture
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              HADOOP 1.x CLUSTER                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐                    ┌─────────────────────────────────────┐ │
│  │   NAMENODE      │                    │           JOBTRACKER                │ │
│  │                 │                    │                                     │ │
│  │ • Metadata Mgmt │                    │ • Job Scheduling                    │ │
│  │ • Block Mapping │                    │ • Task Monitoring                   │ │
│  │ • Namespace     │                    │ • Resource Management               │ │
│  │ • Replication   │                    │ • Fault Tolerance                   │ │
│  └─────────────────┘                    └─────────────────────────────────────┘ │
│           │                                                │                    │
│           │                                                │                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           SLAVE NODES                                       │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │   DATANODE 1    │  │   DATANODE 2    │  │   DATANODE N    │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │Data Storage │ │  │ │Data Storage │ │  │ │Data Storage │ │             │ │
│  │ │ │Block Mgmt   │ │  │ │Block Mgmt   │ │  │ │Block Mgmt   │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │TaskTracker  │ │  │ │TaskTracker  │ │  │ │TaskTracker  │ │             │ │
│  │ │ │Map Tasks    │ │  │ │Map Tasks    │ │  │ │Map Tasks    │ │             │ │
│  │ │ │Reduce Tasks │ │  │ │Reduce Tasks │ │  │ │Reduce Tasks │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Hadoop 2.x Architecture (with YARN)
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              HADOOP 2.x CLUSTER                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐                    ┌─────────────────────────────────────┐ │
│  │   NAMENODE      │                    │        RESOURCE MANAGER             │ │
│  │                 │                    │                                     │ │
│  │ • Metadata Mgmt │                    │ • Global Resource Scheduling        │ │
│  │ • Block Mapping │                    │ • Application Management            │ │
│  │ • Namespace     │                    │ • Cluster Resource Allocation       │ │
│  │ • Replication   │                    │ • Multi-tenancy Support             │ │
│  └─────────────────┘                    └─────────────────────────────────────┘ │
│           │                                                │                    │
│           │                                                │                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           WORKER NODES                                      │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │   NODE 1        │  │   NODE 2        │  │   NODE N        │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │  DATANODE   │ │  │ │  DATANODE   │ │  │ │  DATANODE   │ │             │ │
│  │ │ │Data Storage │ │  │ │Data Storage │ │  │ │Data Storage │ │             │ │
│  │ │ │Block Mgmt   │ │  │ │Block Mgmt   │ │  │ │Block Mgmt   │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │NODE MANAGER │ │  │ │NODE MANAGER │ │  │ │NODE MANAGER │ │             │ │
│  │ │ │Resource Mgmt│ │  │ │Resource Mgmt│ │  │ │Resource Mgmt│ │             │ │
│  │ │ │Container Mgmt│ │  │ │Container Mgmt│ │  │ │Container Mgmt│ │             │ │
│  │ │ │             │ │  │ │             │ │  │ │             │ │             │ │
│  │ │ │┌──────────┐ │ │  │ │┌──────────┐ │ │  │ │┌──────────┐ │ │             │ │
│  │ │ ││Container1│ │ │  │ ││Container1│ │ │  │ ││Container1│ │ │             │ │
│  │ │ ││Container2│ │ │  │ ││Container2│ │ │  │ ││Container2│ │ │             │ │
│  │ │ ││Container3│ │ │  │ ││Container3│ │ │  │ ││Container3│ │ │             │ │
│  │ │ │└──────────┘ │ │  │ │└──────────┘ │ │  │ │└──────────┘ │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘

                              APPLICATION FLOW
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. Client submits application to ResourceManager                               │
│  2. ResourceManager allocates ApplicationMaster container                       │
│  3. ApplicationMaster negotiates resources with ResourceManager                 │
│  4. ApplicationMaster requests containers from NodeManagers                     │
│  5. Containers execute application tasks                                        │
│  6. ApplicationMaster monitors task progress and handles failures               │
│  7. ApplicationMaster reports completion to ResourceManager                     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🗄️ HDFS Deep Dive

### HDFS Architecture Components

**NameNode (Master)**:
- Stores filesystem metadata (namespace, block locations)
- Manages file system operations (create, delete, rename)
- Maintains block-to-DataNode mapping
- Handles client requests for file operations

**DataNode (Slave)**:
- Stores actual data blocks
- Serves read/write requests from clients
- Performs block creation, deletion, and replication
- Sends heartbeats and block reports to NameNode

**Secondary NameNode**:
- Assists NameNode with checkpointing
- Merges fsimage and edits log periodically
- Not a backup or failover solution

### HDFS Block Management

```bash
# Check block size and replication
hdfs fsck /path/to/file -files -blocks -locations

# Set replication factor
hdfs dfs -setrep 2 /path/to/file

# Check HDFS health
hdfs fsck /

# View NameNode status
hdfs dfsadmin -report
```

### HDFS Read Process
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              HDFS READ PROCESS                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    1. Open File    ┌─────────────┐                            │
│  │   CLIENT    │ ──────────────────► │  NAMENODE   │                            │
│  │             │                     │             │                            │
│  │             │ ◄────────────────── │             │                            │
│  │             │  2. Block Locations │             │                            │
│  └─────────────┘                     └─────────────┘                            │
│         │                                                                       │
│         │ 3. Read Data                                                          │
│         ▼                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           DATANODES                                         │ │
│  │                                                                             │ │
│  │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │ │
│  │ │ DATANODE 1  │  │ DATANODE 2  │  │ DATANODE 3  │  │ DATANODE 4  │         │ │
│  │ │             │  │             │  │             │  │             │         │ │
│  │ │ Block A     │  │ Block B     │  │ Block A     │  │ Block B     │         │ │
│  │ │ Block C     │  │ Block A     │  │ Block C     │  │ Block C     │         │ │
│  │ └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  4. Client reads blocks in sequence from closest DataNodes                     │
│  5. If DataNode fails, client automatically switches to replica                │
│  6. Client assembles blocks into complete file                                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 MapReduce Framework

### MapReduce Job Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           MAPREDUCE JOB EXECUTION                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    1. Submit Job    ┌─────────────────┐                       │
│  │   CLIENT    │ ──────────────────► │ RESOURCE MANAGER│                       │
│  │             │                     │                 │                       │
│  │             │                     │ 2. Allocate AM  │                       │
│  │             │                     │    Container    │                       │
│  └─────────────┘                     └─────────────────┘                       │
│                                               │                                 │
│                                               ▼                                 │
│                                    ┌─────────────────┐                         │
│                                    │ APPLICATION     │                         │
│                                    │ MASTER (AM)     │                         │
│                                    │                 │                         │
│                                    │ 3. Request      │                         │
│                                    │    Containers   │                         │
│                                    └─────────────────┘                         │
│                                               │                                 │
│                                               ▼                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           WORKER NODES                                      │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │   NODE 1        │  │   NODE 2        │  │   NODE 3        │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │Map Container│ │  │ │Map Container│ │  │ │Reduce       │ │             │ │
│  │ │ │             │ │  │ │             │ │  │Container    │ │             │ │
│  │ │ │Input Split 1│ │  │ │Input Split 2│ │  │             │ │             │ │
│  │ │ │             │ │  │ │             │ │  │Final Output │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │             │ │             │ │
│  │ │        │        │  │        │        │  │ └─────────────┘ │             │ │
│  │ │        ▼        │  │        ▼        │  │        ▲        │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │        │        │             │ │
│  │ │ │Intermediate │ │  │ │Intermediate │ │  │        │        │             │ │
│  │ │ │Key-Value    │ │  │ │Key-Value    │ │  │ Shuffle & Sort  │             │ │
│  │ │ │Pairs        │ │  │ │Pairs        │ │  │        │        │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │        │        │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  4. Map tasks process input splits and generate intermediate key-value pairs   │
│  5. Shuffle phase groups intermediate data by key                              │
│  6. Reduce tasks process grouped data and generate final output                │
│  7. ApplicationMaster monitors progress and handles failures                   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### MapReduce Programming Model

```java
// Mapper Class
public class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
    
    public void map(Object key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        // Convert to lowercase and split into words
        StringTokenizer itr = new StringTokenizer(value.toString().toLowerCase());
        
        while (itr.hasMoreTokens()) {
            word.set(itr.nextToken());
            context.write(word, one);  // Emit (word, 1)
        }
    }
}

// Reducer Class
public class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();
    
    public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();
        }
        
        result.set(sum);
        context.write(key, result);  // Emit (word, total_count)
    }
}

// Driver Class
public class WordCount {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        
        job.setJarByFile(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

## 🎯 YARN Resource Management

### YARN Components

**ResourceManager**:
- Global resource scheduler and arbitrator
- Manages cluster resources across applications
- Handles application submission and monitoring
- Provides web UI for cluster monitoring

**NodeManager**:
- Per-node agent managing containers
- Monitors resource usage (CPU, memory, disk)
- Reports node health to ResourceManager
- Launches and monitors containers

**ApplicationMaster**:
- Per-application process managing application lifecycle
- Negotiates resources with ResourceManager
- Monitors task progress and handles failures
- Coordinates with NodeManagers for container allocation

**Container**:
- Resource allocation unit (CPU cores, memory)
- Execution environment for application tasks
- Isolated process space with resource limits

### YARN Schedulers

```xml
<!-- Capacity Scheduler Configuration -->
<configuration>
    <property>
        <name>yarn.resourcemanager.scheduler.class</name>
        <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.queues</name>
        <value>production,development,adhoc</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.production.capacity</name>
        <value>60</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.development.capacity</name>
        <value>30</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.adhoc.capacity</name>
        <value>10</value>
    </property>
</configuration>
```

## 🌐 Hadoop Ecosystem

### Core Ecosystem Components

**Data Storage**:
- **HDFS**: Distributed file system
- **HBase**: NoSQL database on HDFS
- **Kudu**: Columnar storage for analytics

**Data Processing**:
- **MapReduce**: Batch processing framework
- **Spark**: In-memory processing engine
- **Tez**: Directed acyclic graph (DAG) framework

**Data Access**:
- **Hive**: SQL-like query language
- **Pig**: High-level data flow language
- **Impala**: Real-time SQL queries

**Data Integration**:
- **Sqoop**: RDBMS to Hadoop data transfer
- **Flume**: Log data collection
- **Kafka**: Real-time data streaming

**Coordination & Management**:
- **ZooKeeper**: Distributed coordination service
- **Oozie**: Workflow scheduler
- **Ambari**: Cluster management and monitoring

## ⚡ Performance Optimization

### HDFS Optimization

```bash
# Optimize block size for large files
hdfs dfsadmin -setDefaultBlockSize 268435456  # 256MB

# Balance DataNode storage
hdfs balancer -threshold 10

# Optimize replication factor
hdfs dfs -setrep 2 /path/to/large/files

# Enable short-circuit reads
echo "dfs.client.read.shortcircuit=true" >> hdfs-site.xml
```

### MapReduce Optimization

```xml
<!-- MapReduce Performance Tuning -->
<configuration>
    <!-- Increase map memory -->
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>2048</value>
    </property>
    
    <!-- Increase reduce memory -->
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>4096</value>
    </property>
    
    <!-- Enable map output compression -->
    <property>
        <name>mapreduce.map.output.compress</name>
        <value>true</value>
    </property>
    
    <!-- Set compression codec -->
    <property>
        <name>mapreduce.map.output.compress.codec</name>
        <value>org.apache.hadoop.io.compress.SnappyCodec</value>
    </property>
    
    <!-- Optimize shuffle -->
    <property>
        <name>mapreduce.task.io.sort.mb</name>
        <value>512</value>
    </property>
</configuration>
```

### YARN Optimization

```xml
<!-- YARN Resource Configuration -->
<configuration>
    <!-- Set maximum memory per container -->
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>8192</value>
    </property>
    
    <!-- Set maximum CPU cores per container -->
    <property>
        <name>yarn.scheduler.maximum-allocation-vcores</name>
        <value>4</value>
    </property>
    
    <!-- Enable preemption -->
    <property>
        <name>yarn.resourcemanager.scheduler.monitor.enable</name>
        <value>true</value>
    </property>
</configuration>
```

## 🛠️ Configuration

### Core Configuration Files

**core-site.xml**:
```xml
<configuration>
    <!-- Default filesystem -->
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://namenode:9000</value>
    </property>
    
    <!-- Temporary directory -->
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/opt/hadoop/tmp</value>
    </property>
</configuration>
```

**hdfs-site.xml**:
```xml
<configuration>
    <!-- Replication factor -->
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    
    <!-- Block size -->
    <property>
        <name>dfs.blocksize</name>
        <value>134217728</value> <!-- 128MB -->
    </property>
    
    <!-- NameNode directories -->
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/opt/hadoop/hdfs/namenode</value>
    </property>
    
    <!-- DataNode directories -->
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/opt/hadoop/hdfs/datanode</value>
    </property>
</configuration>
```

**yarn-site.xml**:
```xml
<configuration>
    <!-- ResourceManager hostname -->
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>resourcemanager</value>
    </property>
    
    <!-- NodeManager auxiliary services -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    
    <!-- NodeManager memory -->
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>8192</value>
    </property>
    
    <!-- NodeManager CPU cores -->
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>4</value>
    </property>
</configuration>
```

## 📊 When to Use Hadoop

**Ideal Use Cases**:
- **Batch Processing**: Large-scale ETL operations
- **Data Archival**: Long-term storage of historical data
- **Log Processing**: Analysis of web logs, application logs
- **Data Warehousing**: Building enterprise data warehouses
- **Scientific Computing**: Processing large datasets in research

**Not Ideal For**:
- **Real-time Processing**: Use Spark Streaming or Kafka instead
- **Small Data**: Overhead not justified for small datasets
- **Interactive Queries**: Use Spark or Presto for faster queries
- **Graph Processing**: Use specialized graph databases

## 🎯 Interview Focus Areas

1. **Architecture**: HDFS, MapReduce, YARN components and interactions
2. **Fault Tolerance**: How Hadoop handles node failures and data recovery
3. **Data Locality**: Importance of processing data where it's stored
4. **Block Management**: HDFS block size, replication, and distribution
5. **Resource Management**: YARN schedulers and resource allocation
6. **Performance Tuning**: Optimization techniques for different workloads
7. **Ecosystem Integration**: How Hadoop works with Hive, Spark, HBase
8. **Scalability**: Horizontal scaling and cluster management
9. **Security**: Kerberos authentication, authorization, encryption
10. **Monitoring**: Cluster health monitoring and troubleshooting

## 📚 Quick References

- [Hadoop Documentation](https://hadoop.apache.org/docs/)
- [HDFS Architecture Guide](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [MapReduce Tutorial](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)
- [YARN Architecture](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html)
- [Hadoop Commands Reference](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/CommandsManual.html)