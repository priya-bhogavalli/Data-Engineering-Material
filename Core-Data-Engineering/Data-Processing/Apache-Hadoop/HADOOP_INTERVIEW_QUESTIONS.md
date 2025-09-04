# Apache Hadoop Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#core-concepts)
2. [HDFS Architecture](#hdfs-architecture)
3. [MapReduce Framework](#mapreduce-framework)
4. [YARN Resource Management](#yarn-resource-management)
5. [Performance & Optimization](#performance--optimization)

---

## Core Concepts

### 1. What is Apache Hadoop and what problems does it solve?

**Answer:**
Apache Hadoop is an open-source framework for distributed storage and processing of large datasets across clusters of commodity hardware.

**Core Problems Solved:**
- **Big Data Storage**: Store petabytes of data across distributed systems
- **Fault Tolerance**: Handle hardware failures gracefully
- **Scalability**: Scale horizontally by adding more nodes
- **Cost Efficiency**: Use commodity hardware instead of expensive servers

**Hadoop Ecosystem:**
```
Hadoop Core:
├── HDFS (Storage)
├── MapReduce (Processing)
└── YARN (Resource Management)

Ecosystem Tools:
├── Hive (SQL-like queries)
├── Pig (Data flow scripting)
├── HBase (NoSQL database)
├── Spark (In-memory processing)
└── Kafka (Stream processing)
```

### 2. Explain Hadoop's architecture and core components.

**Answer:**
Hadoop follows a master-slave architecture with distributed storage and processing.

**Architecture Overview:**
```
Master Nodes:
├── NameNode (HDFS metadata)
├── ResourceManager (YARN)
└── JobHistoryServer

Worker Nodes:
├── DataNode (HDFS storage)
├── NodeManager (YARN containers)
└── TaskTracker (MapReduce tasks)
```

**Component Interactions:**
```python
# Data flow example
# 1. Client submits job to ResourceManager
# 2. ResourceManager allocates containers on NodeManagers
# 3. ApplicationMaster coordinates task execution
# 4. Tasks read/write data from/to HDFS via DataNodes
# 5. Results aggregated and returned to client
```

---

## HDFS Architecture

### 3. How does HDFS handle data storage and replication?

**Answer:**
HDFS uses a distributed file system with configurable replication for fault tolerance.

**Storage Architecture:**
```
HDFS Block Structure:
├── Default block size: 128MB (configurable)
├── Replication factor: 3 (configurable)
└── Blocks distributed across DataNodes

Example:
File: customer_data.csv (500MB)
├── Block 1 (128MB) → DataNode1, DataNode2, DataNode3
├── Block 2 (128MB) → DataNode2, DataNode3, DataNode4
├── Block 3 (128MB) → DataNode3, DataNode4, DataNode1
└── Block 4 (116MB) → DataNode4, DataNode1, DataNode2
```

**Replication Strategy:**
```xml
<!-- hdfs-site.xml -->
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>dfs.blocksize</name>
        <value>134217728</value> <!-- 128MB -->
    </property>
</configuration>
```

**Rack Awareness:**
```bash
# Configure rack awareness
# First replica: Same node as client
# Second replica: Different rack
# Third replica: Same rack as second, different node

# Example topology
/rack1/node1 (client) → Block stored here
/rack2/node3 → Second replica
/rack2/node4 → Third replica
```

### 4. How does the NameNode manage metadata and handle failures?

**Answer:**
NameNode maintains file system metadata in memory and uses multiple mechanisms for fault tolerance.

**Metadata Management:**
```
NameNode Memory:
├── Namespace (file/directory structure)
├── Block locations (which DataNodes have which blocks)
├── File permissions and ownership
└── Block metadata (size, timestamps)

Persistent Storage:
├── fsimage (namespace snapshot)
├── edits log (transaction log)
└── Secondary NameNode (checkpoint creation)
```

**High Availability Setup:**
```xml
<!-- hdfs-site.xml for HA -->
<configuration>
    <property>
        <name>dfs.nameservices</name>
        <value>mycluster</value>
    </property>
    <property>
        <name>dfs.ha.namenodes.mycluster</name>
        <value>nn1,nn2</value>
    </property>
    <property>
        <name>dfs.namenode.rpc-address.mycluster.nn1</name>
        <value>namenode1:8020</value>
    </property>
    <property>
        <name>dfs.namenode.rpc-address.mycluster.nn2</name>
        <value>namenode2:8020</value>
    </property>
</configuration>
```

**Failure Recovery:**
```bash
# Manual failover
hdfs haadmin -transitionToActive nn2

# Automatic failover with ZooKeeper
hdfs zkfc -formatZK
```

---

## MapReduce Framework

### 5. Explain the MapReduce programming model with a practical example.

**Answer:**
MapReduce is a programming model for processing large datasets in parallel across distributed systems.

**Word Count Example:**
```java
// Mapper class
public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
    
    public void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        String[] words = value.toString().toLowerCase().split("\\s+");
        for (String w : words) {
            word.set(w);
            context.write(word, one);
        }
    }
}

// Reducer class
public class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();
    
    public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        
        int sum = 0;
        for (IntWritable value : values) {
            sum += value.get();
        }
        result.set(sum);
        context.write(key, result);
    }
}

// Driver class
public class WordCount {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        
        job.setJarByClass(WordCount.class);
        job.setMapperClass(WordCountMapper.class);
        job.setCombinerClass(WordCountReducer.class);
        job.setReducerClass(WordCountReducer.class);
        
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

**Execution Flow:**
```
Input: "hello world hello hadoop"
├── Map Phase:
│   ├── (hello, 1), (world, 1), (hello, 1), (hadoop, 1)
├── Shuffle & Sort:
│   ├── (hadoop, [1])
│   ├── (hello, [1, 1])
│   └── (world, [1])
└── Reduce Phase:
    ├── (hadoop, 1)
    ├── (hello, 2)
    └── (world, 1)
```

### 6. How do you optimize MapReduce job performance?

**Answer:**
Multiple optimization strategies can improve MapReduce performance:

**Input Optimization:**
```java
// Custom InputFormat for better data locality
public class OptimizedInputFormat extends FileInputFormat<LongWritable, Text> {
    @Override
    protected boolean isSplitable(JobContext context, Path filename) {
        // Make files splitable for better parallelism
        return true;
    }
    
    @Override
    public RecordReader<LongWritable, Text> createRecordReader(
            InputSplit split, TaskAttemptContext context) {
        return new OptimizedRecordReader();
    }
}

// Configure input split size
Configuration conf = new Configuration();
conf.setLong("mapreduce.input.fileinputformat.split.minsize", 128 * 1024 * 1024); // 128MB
conf.setLong("mapreduce.input.fileinputformat.split.maxsize", 256 * 1024 * 1024); // 256MB
```

**Memory and CPU Tuning:**
```xml
<!-- mapred-site.xml -->
<configuration>
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>2048</value>
    </property>
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>4096</value>
    </property>
    <property>
        <name>mapreduce.map.java.opts</name>
        <value>-Xmx1638m</value>
    </property>
    <property>
        <name>mapreduce.reduce.java.opts</name>
        <value>-Xmx3276m</value>
    </property>
</configuration>
```

**Combiner Usage:**
```java
// Use combiner to reduce network traffic
job.setCombinerClass(WordCountReducer.class);

// Custom combiner for complex aggregations
public class SumCombiner extends Reducer<Text, IntWritable, Text, IntWritable> {
    public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable value : values) {
            sum += value.get();
        }
        context.write(key, new IntWritable(sum));
    }
}
```

---

## YARN Resource Management

### 7. How does YARN manage resources and schedule jobs?

**Answer:**
YARN (Yet Another Resource Negotiator) provides resource management and job scheduling for Hadoop clusters.

**YARN Architecture:**
```
ResourceManager (Master):
├── Scheduler (allocates resources)
├── ApplicationsManager (manages applications)
└── Resource Tracker (monitors nodes)

NodeManager (Worker):
├── Container Manager (manages containers)
├── Node Health Checker (monitors node health)
└── Log Aggregation (collects logs)

ApplicationMaster (Per Application):
├── Resource negotiation
├── Task scheduling
└── Progress monitoring
```

**Resource Allocation:**
```xml
<!-- yarn-site.xml -->
<configuration>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>8192</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>4</value>
    </property>
    <property>
        <name>yarn.scheduler.maximum-allocation-mb</name>
        <value>4096</value>
    </property>
</configuration>
```

### 8. How do you configure YARN schedulers for different workloads?

**Answer:**
YARN supports multiple schedulers for different use cases and workload patterns.

**Capacity Scheduler:**
```xml
<!-- capacity-scheduler.xml -->
<configuration>
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

**Fair Scheduler:**
```xml
<!-- fair-scheduler.xml -->
<allocations>
    <queue name="data-engineering">
        <minResources>2048mb,2vcores</minResources>
        <maxResources>8192mb,8vcores</maxResources>
        <weight>2.0</weight>
    </queue>
    <queue name="analytics">
        <minResources>1024mb,1vcores</minResources>
        <maxResources>4096mb,4vcores</maxResources>
        <weight>1.0</weight>
    </queue>
</allocations>
```

**Queue Management:**
```bash
# Submit job to specific queue
hadoop jar wordcount.jar WordCount \
  -Dmapreduce.job.queuename=data-engineering \
  input output

# Monitor queue status
yarn queue -status data-engineering
```

---

## Performance & Optimization

### 9. How do you monitor and troubleshoot Hadoop cluster performance?

**Answer:**
Comprehensive monitoring approach for Hadoop clusters:

**Cluster Monitoring:**
```bash
# HDFS health check
hdfs dfsadmin -report
hdfs fsck / -files -blocks -locations

# YARN resource monitoring
yarn node -list
yarn application -list
yarn logs -applicationId application_123456789

# MapReduce job monitoring
mapred job -list
mapred job -status job_123456789
```

**Performance Metrics:**
```python
# Custom monitoring script
import subprocess
import json

def get_hdfs_metrics():
    result = subprocess.run(['hdfs', 'dfsadmin', '-report'], 
                          capture_output=True, text=True)
    
    metrics = {}
    for line in result.stdout.split('\n'):
        if 'DFS Used%' in line:
            metrics['dfs_used_percent'] = float(line.split(':')[1].strip().rstrip('%'))
        elif 'DFS Remaining' in line:
            metrics['dfs_remaining'] = line.split(':')[1].strip()
    
    return metrics

def get_yarn_metrics():
    result = subprocess.run(['yarn', 'node', '-list'], 
                          capture_output=True, text=True)
    
    total_nodes = 0
    healthy_nodes = 0
    
    for line in result.stdout.split('\n')[1:]:  # Skip header
        if line.strip():
            total_nodes += 1
            if 'RUNNING' in line:
                healthy_nodes += 1
    
    return {
        'total_nodes': total_nodes,
        'healthy_nodes': healthy_nodes,
        'health_percentage': (healthy_nodes / total_nodes) * 100 if total_nodes > 0 else 0
    }
```

### 10. How do you optimize Hadoop for different data processing patterns?

**Answer:**
Optimization strategies vary based on workload characteristics:

**Small Files Problem:**
```bash
# Combine small files using HAR (Hadoop Archive)
hadoop archive -archiveName customer_data.har \
  -p /input/small_files /output/archives

# Use SequenceFile for small files
hadoop jar hadoop-examples.jar teragen 1000000 /tmp/teragen-input
hadoop jar hadoop-examples.jar terasort /tmp/teragen-input /tmp/terasort-output
```

**Large File Processing:**
```xml
<!-- Optimize for large files -->
<configuration>
    <property>
        <name>dfs.blocksize</name>
        <value>268435456</value> <!-- 256MB for large files -->
    </property>
    <property>
        <name>mapreduce.input.fileinputformat.split.maxsize</name>
        <value>268435456</value>
    </property>
</configuration>
```

**Memory-Intensive Workloads:**
```java
// Configure for memory-intensive processing
Configuration conf = new Configuration();
conf.setInt("mapreduce.map.memory.mb", 4096);
conf.setInt("mapreduce.reduce.memory.mb", 8192);
conf.set("mapreduce.map.java.opts", "-Xmx3276m");
conf.set("mapreduce.reduce.java.opts", "-Xmx6553m");

// Enable map-side join for large datasets
conf.setBoolean("mapreduce.job.reduces", false);
conf.setClass("mapreduce.job.inputformat.class", 
              CompositeInputFormat.class, InputFormat.class);
```

**I/O Optimization:**
```xml
<!-- Compression configuration -->
<configuration>
    <property>
        <name>mapreduce.map.output.compress</name>
        <value>true</value>
    </property>
    <property>
        <name>mapreduce.map.output.compress.codec</name>
        <value>org.apache.hadoop.io.compress.SnappyCodec</value>
    </property>
    <property>
        <name>mapreduce.output.fileoutputformat.compress</name>
        <value>true</value>
    </property>
</configuration>
```

---

## Summary

Apache Hadoop provides the foundation for big data processing through:

1. **Distributed Storage**: HDFS for fault-tolerant data storage
2. **Parallel Processing**: MapReduce for distributed computation
3. **Resource Management**: YARN for cluster resource allocation
4. **Scalability**: Horizontal scaling across commodity hardware
5. **Ecosystem Integration**: Foundation for tools like Spark, Hive, and HBase