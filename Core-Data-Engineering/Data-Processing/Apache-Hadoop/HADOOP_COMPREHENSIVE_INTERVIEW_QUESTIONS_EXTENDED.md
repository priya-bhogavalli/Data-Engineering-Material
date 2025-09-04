# Apache Hadoop Extended Interview Questions & Answers

## 📋 Table of Contents
1. [Advanced HDFS Architecture](#advanced-hdfs-architecture)
2. [MapReduce Deep Dive](#mapreduce-deep-dive)
3. [YARN Resource Management](#yarn-resource-management)
4. [Performance Optimization](#performance-optimization)
5. [Security & Governance](#security--governance)
6. [Operations & Monitoring](#operations--monitoring)
7. [Ecosystem Integration](#ecosystem-integration)
8. [Troubleshooting](#troubleshooting)

---

## Advanced HDFS Architecture

### 1. Explain HDFS Federation and its benefits for large-scale deployments.

**Answer:**
HDFS Federation allows multiple independent Namenodes to manage different portions of the filesystem namespace:

**Federation Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│                    HDFS Federation                      │
├─────────────────┬─────────────────┬─────────────────────┤
│   Namespace 1   │   Namespace 2   │   Namespace 3       │
│   NameNode 1    │   NameNode 2    │   NameNode 3        │
│   /user         │   /data         │   /tmp              │
│   /home         │   /warehouse    │   /logs             │
└─────────────────┴─────────────────┴─────────────────────┘
│                                                         │
├─────────────────────────────────────────────────────────┤
│              Shared DataNode Pool                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │DataNode1│  │DataNode2│  │DataNode3│  │DataNode4│   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Configuration Example:**
```xml
<!-- core-site.xml -->
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://mycluster</value>
    </property>
</configuration>

<!-- hdfs-site.xml -->
<configuration>
    <!-- NameService 1 -->
    <property>
        <name>dfs.nameservices</name>
        <value>ns1,ns2,ns3</value>
    </property>
    
    <property>
        <name>dfs.namenode.rpc-address.ns1</name>
        <value>namenode1:8020</value>
    </property>
    
    <property>
        <name>dfs.namenode.http-address.ns1</name>
        <value>namenode1:50070</value>
    </property>
    
    <!-- NameService 2 -->
    <property>
        <name>dfs.namenode.rpc-address.ns2</name>
        <value>namenode2:8020</value>
    </property>
    
    <!-- ViewFS configuration -->
    <property>
        <name>fs.viewfs.mounttable.mycluster.link./user</name>
        <value>hdfs://ns1/user</value>
    </property>
    
    <property>
        <name>fs.viewfs.mounttable.mycluster.link./data</name>
        <value>hdfs://ns2/data</value>
    </property>
</configuration>
```

**Benefits:**
- **Scalability**: Multiple Namenodes eliminate single point of bottleneck
- **Isolation**: Different applications can use separate namespaces
- **Performance**: Parallel metadata operations
- **Availability**: Failure of one Namenode doesn't affect others

### 2. How does HDFS handle small files problem and what are the solutions?

**Answer:**
Small files create significant overhead in HDFS due to metadata storage:

**Problem Analysis:**
```bash
# Check file size distribution
hdfs fsck / -files -blocks -locations | grep "repl=" | \
awk '{print $1}' | sort -n | uniq -c

# Find small files
hdfs dfs -find / -size -1048576  # Files smaller than 1MB

# Memory usage calculation
# Each file/block uses ~150 bytes of NameNode memory
# 1 million small files = ~150MB NameNode memory
```

**Solution 1: HAR (Hadoop Archive) Files:**
```bash
# Create HAR file
hadoop archive -archiveName small_files.har \
    -p /input/small_files \
    /output/archives

# List HAR contents
hdfs dfs -ls har:///output/archives/small_files.har

# Access files in HAR
hdfs dfs -cat har:///output/archives/small_files.har/file1.txt
```

**Solution 2: SequenceFiles:**
```java
// Create SequenceFile from small files
public class SmallFilesToSequenceFile {
    public static void main(String[] args) throws IOException {
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        
        Path outputPath = new Path("/output/small_files.seq");
        SequenceFile.Writer writer = SequenceFile.createWriter(
            fs, conf, outputPath, 
            Text.class, BytesWritable.class,
            SequenceFile.CompressionType.BLOCK
        );
        
        // Read small files and write to SequenceFile
        FileStatus[] files = fs.listStatus(new Path("/input/small_files"));
        for (FileStatus file : files) {
            if (file.isFile()) {
                FSDataInputStream in = fs.open(file.getPath());
                byte[] buffer = new byte[(int) file.getLen()];
                in.readFully(buffer);
                in.close();
                
                writer.append(
                    new Text(file.getPath().getName()),
                    new BytesWritable(buffer)
                );
            }
        }
        writer.close();
    }
}
```

**Solution 3: CombineFileInputFormat:**
```java
// MapReduce job for processing small files
public class SmallFileProcessor extends Configured implements Tool {
    
    public static class SmallFileMapper 
            extends Mapper<LongWritable, Text, Text, IntWritable> {
        
        @Override
        protected void map(LongWritable key, Text value, Context context) 
                throws IOException, InterruptedException {
            // Process multiple small files in single mapper
            String[] words = value.toString().split("\\s+");
            for (String word : words) {
                context.write(new Text(word), new IntWritable(1));
            }
        }
    }
    
    @Override
    public int run(String[] args) throws Exception {
        Job job = Job.getInstance(getConf(), "small-file-processor");
        job.setJarByClass(SmallFileProcessor.class);
        
        // Use CombineFileInputFormat
        job.setInputFormatClass(CombineTextInputFormat.class);
        CombineTextInputFormat.setMaxInputSplitSize(job, 67108864); // 64MB
        CombineTextInputFormat.setMinInputSplitSize(job, 1);
        
        job.setMapperClass(SmallFileMapper.class);
        job.setReducerClass(IntSumReducer.class);
        
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
        return job.waitForCompletion(true) ? 0 : 1;
    }
}
```

### 3. Explain HDFS Erasure Coding and its advantages over replication.

**Answer:**
Erasure Coding provides fault tolerance with lower storage overhead than replication:

**Traditional Replication vs Erasure Coding:**
```
Traditional Replication (3x):
Original Data: 100GB
Storage Used: 300GB (200% overhead)
Fault Tolerance: Can lose 2 replicas

Erasure Coding (6+3):
Original Data: 100GB  
Storage Used: 150GB (50% overhead)
Fault Tolerance: Can lose 3 blocks
```

**Enable Erasure Coding:**
```bash
# Enable EC on HDFS
hdfs ec -enablePolicy -policy RS-6-3-1024k

# List available policies
hdfs ec -listPolicies

# Set EC policy on directory
hdfs ec -setPolicy -path /data/warehouse -policy RS-6-3-1024k

# Check EC policy
hdfs ec -getPolicy -path /data/warehouse

# Verify EC status
hdfs fsck /data/warehouse -files -blocks -locations
```

**EC Policy Configuration:**
```xml
<!-- hdfs-site.xml -->
<configuration>
    <property>
        <name>dfs.namenode.ec.policies.enabled</name>
        <value>RS-6-3-1024k,RS-10-4-1024k,XOR-2-1-1024k</value>
    </property>
    
    <property>
        <name>dfs.datanode.ec.reconstruction.stripedread.timeout.millis</name>
        <value>5000</value>
    </property>
    
    <property>
        <name>dfs.datanode.ec.reconstruction.stripedread.buffer.size</name>
        <value>65536</value>
    </property>
</configuration>
```

**EC Performance Considerations:**
```java
// Reading EC files requires coordination across multiple DataNodes
public class ECFileReader {
    public void readECFile(String path) throws IOException {
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        
        Path ecPath = new Path(path);
        FSDataInputStream in = fs.open(ecPath);
        
        // EC reads may have higher latency due to reconstruction
        byte[] buffer = new byte[1024 * 1024]; // 1MB buffer
        int bytesRead = in.read(buffer);
        
        // For better performance, use larger read buffers
        // and sequential access patterns
        in.close();
    }
}
```

---

## MapReduce Deep Dive

### 4. Explain MapReduce optimization techniques for large-scale data processing.

**Answer:**
Multiple optimization strategies for MapReduce performance:

**Input Split Optimization:**
```java
// Custom InputFormat for optimal split size
public class OptimizedTextInputFormat extends TextInputFormat {
    
    @Override
    protected boolean isSplitable(JobContext context, Path filename) {
        // Make compressed files splittable if using splittable codec
        CompressionCodec codec = new CompressionCodecFactory(
            context.getConfiguration()).getCodec(filename);
        
        if (codec != null && codec instanceof SplittableCompressionCodec) {
            return true;
        }
        return super.isSplitable(context, filename);
    }
    
    @Override
    public List<InputSplit> getSplits(JobContext job) throws IOException {
        // Custom split logic for optimal parallelism
        long minSize = Math.max(getFormatMinSplitSize(), 
                               getMinSplitSize(job));
        long maxSize = getMaxSplitSize(job);
        
        // Adjust split size based on cluster capacity
        int numNodes = job.getConfiguration().getInt("mapreduce.job.num.nodes", 10);
        long idealSplitSize = Math.max(minSize, 
            getTotalInputSize(job) / (numNodes * 2)); // 2 maps per node
        
        return generateSplits(job, Math.min(idealSplitSize, maxSize));
    }
}
```

**Combiner Optimization:**
```java
// Efficient combiner for reducing shuffle data
public class OptimizedCombiner extends Reducer<Text, IntWritable, Text, IntWritable> {
    
    private IntWritable result = new IntWritable();
    
    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, 
                         Context context) throws IOException, InterruptedException {
        
        int sum = 0;
        int count = 0;
        
        for (IntWritable value : values) {
            sum += value.get();
            count++;
            
            // Limit combiner processing to avoid memory issues
            if (count > 10000) {
                result.set(sum);
                context.write(key, result);
                sum = 0;
                count = 0;
            }
        }
        
        if (count > 0) {
            result.set(sum);
            context.write(key, result);
        }
    }
}
```

**Memory Management:**
```xml
<!-- mapred-site.xml optimizations -->
<configuration>
    <!-- Map task memory -->
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>2048</value>
    </property>
    
    <property>
        <name>mapreduce.map.java.opts</name>
        <value>-Xmx1638m -XX:+UseG1GC</value>
    </property>
    
    <!-- Reduce task memory -->
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>4096</value>
    </property>
    
    <property>
        <name>mapreduce.reduce.java.opts</name>
        <value>-Xmx3276m -XX:+UseG1GC</value>
    </property>
    
    <!-- Sort buffer optimization -->
    <property>
        <name>mapreduce.task.io.sort.mb</name>
        <value>512</value>
    </property>
    
    <property>
        <name>mapreduce.map.sort.spill.percent</name>
        <value>0.8</value>
    </property>
    
    <!-- Shuffle optimization -->
    <property>
        <name>mapreduce.reduce.shuffle.parallelcopies</name>
        <value>20</value>
    </property>
    
    <property>
        <name>mapreduce.reduce.shuffle.input.buffer.percent</name>
        <value>0.7</value>
    </property>
</configuration>
```

**Compression Optimization:**
```java
// Configure compression for intermediate and output data
public class CompressionOptimizedJob {
    
    public static void configureCompression(Job job) {
        Configuration conf = job.getConfiguration();
        
        // Enable map output compression
        conf.setBoolean("mapreduce.map.output.compress", true);
        conf.setClass("mapreduce.map.output.compress.codec", 
                     SnappyCodec.class, CompressionCodec.class);
        
        // Enable output compression
        FileOutputFormat.setCompressOutput(job, true);
        FileOutputFormat.setOutputCompressorClass(job, GzipCodec.class);
        
        // Enable intermediate compression
        conf.setBoolean("mapreduce.compress.map.output", true);
        conf.setClass("mapreduce.map.output.compression.codec",
                     LzoCodec.class, CompressionCodec.class);
    }
}
```

### 5. How do you handle data skew in MapReduce jobs?

**Answer:**
Data skew occurs when certain keys have disproportionately more data:

**Identify Data Skew:**
```java
// Skew detection mapper
public class SkewDetectionMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    
    private Map<String, Integer> keyCount = new HashMap<>();
    private int threshold = 10000;
    
    @Override
    protected void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        String[] fields = value.toString().split(",");
        String groupKey = fields[0]; // Assuming first field is group key
        
        keyCount.put(groupKey, keyCount.getOrDefault(groupKey, 0) + 1);
        
        // Emit warning for skewed keys
        if (keyCount.get(groupKey) > threshold) {
            context.getCounter("SKEW", "SKEWED_KEYS").increment(1);
            context.write(new Text("SKEWED_KEY"), new IntWritable(1));
        }
        
        context.write(new Text(groupKey), new IntWritable(1));
    }
}
```

**Salting Technique:**
```java
// Two-phase aggregation with salting
public class SaltingMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    
    private Random random = new Random();
    private int saltRange = 10; // Number of salt values
    
    @Override
    protected void map(LongWritable key, Text value, Context context) 
            throws IOException, InterruptedException {
        
        String[] fields = value.toString().split(",");
        String originalKey = fields[0];
        int amount = Integer.parseInt(fields[1]);
        
        // Add salt to distribute skewed keys
        int salt = random.nextInt(saltRange);
        String saltedKey = originalKey + "_" + salt;
        
        context.write(new Text(saltedKey), new IntWritable(amount));
    }
}

// First reducer: Partial aggregation
public class PartialAggregationReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    
    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) 
            throws IOException, InterruptedException {
        
        int sum = 0;
        for (IntWritable value : values) {
            sum += value.get();
        }
        
        // Remove salt from key
        String originalKey = key.toString().split("_")[0];
        context.write(new Text(originalKey), new IntWritable(sum));
    }
}

// Second reducer: Final aggregation
public class FinalAggregationReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    
    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) 
            throws IOException, InterruptedException {
        
        int finalSum = 0;
        for (IntWritable value : values) {
            finalSum += value.get();
        }
        
        context.write(key, new IntWritable(finalSum));
    }
}
```

**Custom Partitioner for Skew:**
```java
// Skew-aware partitioner
public class SkewAwarePartitioner extends Partitioner<Text, IntWritable> {
    
    private Set<String> skewedKeys = new HashSet<>();
    
    @Override
    public void setConf(Configuration conf) {
        super.setConf(conf);
        
        // Load skewed keys from configuration or external file
        String[] keys = conf.getStrings("skewed.keys", new String[0]);
        skewedKeys.addAll(Arrays.asList(keys));
    }
    
    @Override
    public int getPartition(Text key, IntWritable value, int numPartitions) {
        String keyStr = key.toString();
        
        if (skewedKeys.contains(keyStr)) {
            // Distribute skewed keys across multiple partitions
            return Math.abs(keyStr.hashCode() + value.hashCode()) % numPartitions;
        } else {
            // Normal partitioning for non-skewed keys
            return Math.abs(keyStr.hashCode()) % numPartitions;
        }
    }
}
```

---

## YARN Resource Management

### 6. Explain YARN capacity scheduler and how to configure it for multi-tenant environments.

**Answer:**
Capacity Scheduler provides hierarchical resource allocation with guaranteed capacity:

**Capacity Scheduler Configuration:**
```xml
<!-- capacity-scheduler.xml -->
<configuration>
    <!-- Root queue configuration -->
    <property>
        <name>yarn.scheduler.capacity.root.queues</name>
        <value>production,development,adhoc</value>
    </property>
    
    <!-- Production queue (60% capacity) -->
    <property>
        <name>yarn.scheduler.capacity.root.production.capacity</name>
        <value>60</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.production.maximum-capacity</name>
        <value>80</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.production.queues</name>
        <value>etl,analytics</value>
    </property>
    
    <!-- ETL sub-queue (40% of production) -->
    <property>
        <name>yarn.scheduler.capacity.root.production.etl.capacity</name>
        <value>40</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.production.etl.user-limit-factor</name>
        <value>2</value>
    </property>
    
    <!-- Analytics sub-queue (60% of production) -->
    <property>
        <name>yarn.scheduler.capacity.root.production.analytics.capacity</name>
        <value>60</value>
    </property>
    
    <!-- Development queue (25% capacity) -->
    <property>
        <name>yarn.scheduler.capacity.root.development.capacity</name>
        <value>25</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.development.maximum-capacity</name>
        <value>40</value>
    </property>
    
    <!-- Ad-hoc queue (15% capacity) -->
    <property>
        <name>yarn.scheduler.capacity.root.adhoc.capacity</name>
        <value>15</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.adhoc.maximum-capacity</name>
        <value>30</value>
    </property>
    
    <!-- Access Control Lists -->
    <property>
        <name>yarn.scheduler.capacity.root.production.etl.acl_submit_applications</name>
        <value>etl_users,etl_admin</value>
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.production.analytics.acl_submit_applications</name>
        <value>analytics_team,data_scientists</value>
    </property>
    
    <!-- Resource limits -->
    <property>
        <name>yarn.scheduler.capacity.root.production.etl.maximum-application-lifetime</name>
        <value>86400</value> <!-- 24 hours -->
    </property>
    
    <property>
        <name>yarn.scheduler.capacity.root.adhoc.maximum-application-lifetime</name>
        <value>3600</value> <!-- 1 hour -->
    </property>
</configuration>
```

**Queue Management Commands:**
```bash
# Refresh queue configuration
yarn rmadmin -refreshQueues

# Check queue status
yarn queue -status production.etl

# List all queues
yarn queue -list

# Submit job to specific queue
hadoop jar myapp.jar MyJob -Dmapreduce.job.queuename=production.etl

# Monitor queue usage
yarn top

# Get queue information
yarn application -list -appStates RUNNING -appTypes MAPREDUCE
```

**Dynamic Queue Management:**
```java
// Programmatically submit to specific queue
public class QueueAwareJobSubmission {
    
    public void submitJobToQueue(String queueName, String jarPath, String mainClass) 
            throws Exception {
        
        Configuration conf = new Configuration();
        conf.set("mapreduce.job.queuename", queueName);
        
        // Set resource requirements based on queue
        if (queueName.contains("production")) {
            conf.setInt("mapreduce.map.memory.mb", 4096);
            conf.setInt("mapreduce.reduce.memory.mb", 8192);
        } else if (queueName.contains("development")) {
            conf.setInt("mapreduce.map.memory.mb", 2048);
            conf.setInt("mapreduce.reduce.memory.mb", 4096);
        }
        
        Job job = Job.getInstance(conf, "Queue-aware job");
        job.setJarByClass(this.getClass());
        
        // Submit job
        job.waitForCompletion(true);
    }
}
```

### 7. How do you implement resource isolation and fair sharing in YARN?

**Answer:**
YARN provides multiple mechanisms for resource isolation and fair sharing:

**Fair Scheduler Configuration:**
```xml
<!-- fair-scheduler.xml -->
<allocations>
    <!-- Default queue settings -->
    <defaultQueueSchedulingPolicy>fair</defaultQueueSchedulingPolicy>
    <defaultMinSharePreemptionTimeout>600</defaultMinSharePreemptionTimeout>
    <defaultFairSharePreemptionTimeout>600</defaultFairSharePreemptionTimeout>
    
    <!-- Queue definitions -->
    <queue name="production">
        <minResources>10240 mb,10 vcores</minResources>
        <maxResources>51200 mb,50 vcores</maxResources>
        <maxRunningApps>20</maxRunningApps>
        <weight>3.0</weight>
        <schedulingPolicy>fair</schedulingPolicy>
        
        <queue name="etl">
            <minResources>4096 mb,4 vcores</minResources>
            <maxResources>20480 mb,20 vcores</maxResources>
            <weight>2.0</weight>
        </queue>
        
        <queue name="analytics">
            <minResources>6144 mb,6 vcores</minResources>
            <maxResources>30720 mb,30 vcores</maxResources>
            <weight>1.0</weight>
        </queue>
    </queue>
    
    <queue name="development">
        <minResources>2048 mb,2 vcores</minResources>
        <maxResources>10240 mb,10 vcores</maxResources>
        <maxRunningApps>10</maxRunningApps>
        <weight>1.0</weight>
    </queue>
    
    <!-- User limits -->
    <user name="etl_user">
        <maxRunningApps>5</maxRunningApps>
    </user>
    
    <!-- Queue placement policy -->
    <queuePlacementPolicy>
        <rule name="specified" create="false"/>
        <rule name="primaryGroup" create="false"/>
        <rule name="default" queue="development"/>
    </queuePlacementPolicy>
</allocations>
```

**Node Labels for Resource Isolation:**
```bash
# Add node labels
yarn rmadmin -addToClusterNodeLabels "gpu,ssd,memory_intensive"

# Assign labels to nodes
yarn rmadmin -replaceLabelsOnNode "node1:8041=gpu,ssd node2:8041=memory_intensive"

# Configure queue to use specific labels
```

```xml
<!-- Queue with node label -->
<property>
    <name>yarn.scheduler.capacity.root.gpu_queue.accessible-node-labels</name>
    <value>gpu</value>
</property>

<property>
    <name>yarn.scheduler.capacity.root.gpu_queue.accessible-node-labels.gpu.capacity</name>
    <value>100</value>
</property>
```

**Container Resource Isolation:**
```xml
<!-- yarn-site.xml -->
<configuration>
    <!-- Enable CGroups for CPU isolation -->
    <property>
        <name>yarn.nodemanager.container-executor.class</name>
        <value>org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor</value>
    </property>
    
    <property>
        <name>yarn.nodemanager.linux-container-executor.cgroups.hierarchy</name>
        <value>/sys/fs/cgroup</value>
    </property>
    
    <property>
        <name>yarn.nodemanager.linux-container-executor.cgroups.mount</name>
        <value>true</value>
    </property>
    
    <property>
        <name>yarn.nodemanager.linux-container-executor.cgroups.mount-path</name>
        <value>/sys/fs/cgroup</value>
    </property>
    
    <!-- Memory enforcement -->
    <property>
        <name>yarn.nodemanager.pmem-check-enabled</name>
        <value>true</value>
    </property>
    
    <property>
        <name>yarn.nodemanager.vmem-check-enabled</name>
        <value>false</value>
    </property>
    
    <!-- CPU isolation -->
    <property>
        <name>yarn.nodemanager.resource.cpu-vcores</name>
        <value>8</value>
    </property>
    
    <property>
        <name>yarn.scheduler.maximum-allocation-vcores</name>
        <value>4</value>
    </property>
</configuration>
```

---

## Performance Optimization

### 8. How do you optimize Hadoop cluster performance for different workload types?

**Answer:**
Different workloads require specific optimization strategies:

**Batch Processing Optimization:**
```xml
<!-- mapred-site.xml for batch workloads -->
<configuration>
    <!-- Large block size for sequential reads -->
    <property>
        <name>dfs.blocksize</name>
        <value>268435456</value> <!-- 256MB -->
    </property>
    
    <!-- Optimize for throughput -->
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>4096</value>
    </property>
    
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>8192</value>
    </property>
    
    <!-- Larger sort buffer -->
    <property>
        <name>mapreduce.task.io.sort.mb</name>
        <value>1024</value>
    </property>
    
    <!-- Enable compression -->
    <property>
        <name>mapreduce.map.output.compress</name>
        <value>true</value>
    </property>
    
    <property>
        <name>mapreduce.map.output.compress.codec</name>
        <value>org.apache.hadoop.io.compress.SnappyCodec</value>
    </property>
</configuration>
```

**Interactive Query Optimization:**
```xml
<!-- hdfs-site.xml for low-latency access -->
<configuration>
    <!-- Smaller block size for random access -->
    <property>
        <name>dfs.blocksize</name>
        <value>67108864</value> <!-- 64MB -->
    </property>
    
    <!-- Enable short-circuit reads -->
    <property>
        <name>dfs.client.read.shortcircuit</name>
        <value>true</value>
    </property>
    
    <property>
        <name>dfs.domain.socket.path</name>
        <value>/var/lib/hadoop-hdfs/dn_socket</value>
    </property>
    
    <!-- Enable caching -->
    <property>
        <name>dfs.datanode.max.locked.memory</name>
        <value>4294967296</value> <!-- 4GB -->
    </property>
    
    <!-- Optimize for random reads -->
    <property>
        <name>dfs.client.cache.readahead</name>
        <value>4194304</value> <!-- 4MB -->
    </property>
</configuration>
```

**Memory-Intensive Workload Optimization:**
```bash
#!/bin/bash
# Cluster tuning script for memory-intensive workloads

# Increase heap sizes
export HADOOP_HEAPSIZE=8192
export YARN_HEAPSIZE=8192
export HADOOP_NAMENODE_HEAPSIZE=16384
export HADOOP_DATANODE_HEAPSIZE=4096

# JVM tuning
export HADOOP_NAMENODE_OPTS="-XX:+UseG1GC -XX:+UseStringDeduplication -XX:MaxGCPauseMillis=200"
export HADOOP_DATANODE_OPTS="-XX:+UseParallelGC -XX:ParallelGCThreads=4"

# OS-level optimizations
echo 'vm.swappiness=1' >> /etc/sysctl.conf
echo 'vm.overcommit_memory=1' >> /etc/sysctl.conf
echo 'net.core.somaxconn=32768' >> /etc/sysctl.conf

# Disable transparent huge pages
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
```

**Network Optimization:**
```xml
<!-- core-site.xml -->
<configuration>
    <!-- Increase buffer sizes -->
    <property>
        <name>io.file.buffer.size</name>
        <value>131072</value> <!-- 128KB -->
    </property>
    
    <!-- Network timeouts -->
    <property>
        <name>ipc.client.connect.timeout</name>
        <value>20000</value>
    </property>
    
    <property>
        <name>ipc.client.connect.max.retries</name>
        <value>50</value>
    </property>
</configuration>
```

### 9. How do you implement data locality optimization in Hadoop?

**Answer:**
Data locality is crucial for Hadoop performance:

**HDFS Placement Policy:**
```java
// Custom block placement policy
public class CustomBlockPlacementPolicy extends BlockPlacementPolicyDefault {
    
    @Override
    public DatanodeStorageInfo[] chooseTarget(String srcPath,
                                            int numOfReplicas,
                                            Node writer,
                                            List<DatanodeStorageInfo> chosenNodes,
                                            boolean returnChosenNodes,
                                            Set<Node> excludedNodes,
                                            long blocksize,
                                            StorageType storageType) {
        
        // Custom logic for replica placement
        // 1. First replica on same rack as writer
        // 2. Second replica on different rack
        // 3. Third replica on same rack as second
        
        return super.chooseTarget(srcPath, numOfReplicas, writer, 
                                chosenNodes, returnChosenNodes, 
                                excludedNodes, blocksize, storageType);
    }
    
    @Override
    protected void chooseRemoteRack(int numOfReplicas,
                                  DatanodeDescriptor localMachine,
                                  Set<Node> excludedNodes,
                                  long blocksize,
                                  int maxReplicasPerRack,
                                  List<DatanodeStorageInfo> results,
                                  boolean avoidStaleNodes,
                                  StorageType storageType) {
        
        // Prefer racks with higher bandwidth or specific characteristics
        super.chooseRemoteRack(numOfReplicas, localMachine, excludedNodes,
                             blocksize, maxReplicasPerRack, results,
                             avoidStaleNodes, storageType);
    }
}
```

**Rack Awareness Configuration:**
```xml
<!-- core-site.xml -->
<configuration>
    <property>
        <name>net.topology.script.file.name</name>
        <value>/etc/hadoop/conf/topology.sh</value>
    </property>
    
    <property>
        <name>net.topology.script.number.args</name>
        <value>100</value>
    </property>
</configuration>
```

**Topology Script:**
```bash
#!/bin/bash
# topology.sh - Maps IP addresses to rack locations

while [ $# -gt 0 ] ; do
    nodeArg=$1
    exec< /etc/hadoop/conf/topology.data
    result=""
    while read line ; do
        ar=( $line )
        if [ "${ar[0]}" = "$nodeArg" ] ; then
            result="${ar[1]}"
        fi
    done
    shift
    if [ -z "$result" ] ; then
        echo -n "/default-rack "
    else
        echo -n "$result "
    fi
done
```

**MapReduce Data Locality:**
```java
// Custom InputFormat for better data locality
public class LocalityAwareInputFormat extends TextInputFormat {
    
    @Override
    public List<InputSplit> getSplits(JobContext job) throws IOException {
        List<InputSplit> splits = super.getSplits(job);
        
        // Sort splits by locality preference
        Collections.sort(splits, new Comparator<InputSplit>() {
            @Override
            public int compare(InputSplit s1, InputSplit s2) {
                try {
                    FileSplit fs1 = (FileSplit) s1;
                    FileSplit fs2 = (FileSplit) s2;
                    
                    // Prefer splits with more local blocks
                    String[] locations1 = fs1.getLocations();
                    String[] locations2 = fs2.getLocations();
                    
                    return Integer.compare(locations2.length, locations1.length);
                } catch (Exception e) {
                    return 0;
                }
            }
        });
        
        return splits;
    }
}
```

**Monitoring Data Locality:**
```bash
# Check data locality metrics
yarn logs -applicationId application_1234567890123_0001 | grep "Data-local\|Rack-local\|Off-switch"

# HDFS block location report
hdfs fsck /data/warehouse -files -blocks -locations | grep "repl="

# MapReduce job locality statistics
mapred job -counter job_1234567890123_0001 \
    org.apache.hadoop.mapreduce.JobCounter \
    DATA_LOCAL_MAPS
```

---

## Security & Governance

### 10. How do you implement comprehensive security in a Hadoop cluster?

**Answer:**
Hadoop security involves multiple layers of protection:

**Kerberos Authentication:**
```bash
# Create Kerberos principals
kadmin.local -q "addprinc -randkey hdfs/namenode.example.com@EXAMPLE.COM"
kadmin.local -q "addprinc -randkey yarn/resourcemanager.example.com@EXAMPLE.COM"
kadmin.local -q "addprinc -randkey mapred/jobhistory.example.com@EXAMPLE.COM"

# Create keytab files
kadmin.local -q "ktadd -k /etc/hadoop/conf/hdfs.keytab hdfs/namenode.example.com@EXAMPLE.COM"
kadmin.local -q "ktadd -k /etc/hadoop/conf/yarn.keytab yarn/resourcemanager.example.com@EXAMPLE.COM"

# Set proper permissions
chown hdfs:hadoop /etc/hadoop/conf/hdfs.keytab
chmod 400 /etc/hadoop/conf/hdfs.keytab
```

**Core Security Configuration:**
```xml
<!-- core-site.xml -->
<configuration>
    <!-- Enable Kerberos -->
    <property>
        <name>hadoop.security.authentication</name>
        <value>kerberos</value>
    </property>
    
    <property>
        <name>hadoop.security.authorization</name>
        <value>true</value>
    </property>
    
    <!-- RPC encryption -->
    <property>
        <name>hadoop.rpc.protection</name>
        <value>privacy</value>
    </property>
    
    <!-- HTTP authentication -->
    <property>
        <name>hadoop.http.authentication.type</name>
        <value>kerberos</value>
    </property>
    
    <property>
        <name>hadoop.http.authentication.kerberos.principal</name>
        <value>HTTP/_HOST@EXAMPLE.COM</value>
    </property>
    
    <property>
        <name>hadoop.http.authentication.kerberos.keytab</name>
        <value>/etc/hadoop/conf/http.keytab</value>
    </property>
</configuration>
```

**HDFS Security:**
```xml
<!-- hdfs-site.xml -->
<configuration>
    <!-- NameNode security -->
    <property>
        <name>dfs.namenode.kerberos.principal</name>
        <value>hdfs/_HOST@EXAMPLE.COM</value>
    </property>
    
    <property>
        <name>dfs.namenode.keytab.file</name>
        <value>/etc/hadoop/conf/hdfs.keytab</value>
    </property>
    
    <!-- DataNode security -->
    <property>
        <name>dfs.datanode.kerberos.principal</name>
        <value>hdfs/_HOST@EXAMPLE.COM</value>
    </property>
    
    <property>
        <name>dfs.datanode.keytab.file</name>
        <value>/etc/hadoop/conf/hdfs.keytab</value>
    </property>
    
    <!-- Enable encryption -->
    <property>
        <name>dfs.encrypt.data.transfer</name>
        <value>true</value>
    </property>
    
    <property>
        <name>dfs.encrypt.data.transfer.algorithm</name>
        <value>3des</value>
    </property>
    
    <!-- Block access tokens -->
    <property>
        <name>dfs.block.access.token.enable</name>
        <value>true</value>
    </property>
    
    <!-- Permissions -->
    <property>
        <name>dfs.permissions.enabled</name>
        <value>true</value>
    </property>
    
    <property>
        <name>dfs.permissions.superusergroup</name>
        <value>hdfs</value>
    </property>
</configuration>
```

**Encryption at Rest:**
```bash
# Create encryption zone
hadoop key create mykey -size 256
hdfs crypto -createZone -keyName mykey -path /encrypted

# Copy data to encrypted zone
hdfs dfs -cp /data/sensitive /encrypted/

# Verify encryption
hdfs crypto -listZones
```

**Ranger Integration:**
```xml
<!-- ranger-hdfs-security.xml -->
<configuration>
    <property>
        <name>xasecure.hdfs.policymgr.url</name>
        <value>http://ranger-admin:6080</value>
    </property>
    
    <property>
        <name>xasecure.hdfs.policymgr.url.lazyload</name>
        <value>true</value>
    </property>
    
    <property>
        <name>xasecure.hdfs.policymgr.url.reload.interval.seconds</name>
        <value>30</value>
    </property>
</configuration>
```

---

## 🎯 Key Takeaways

1. **HDFS Architecture**: Understanding Federation, Erasure Coding, and small files optimization
2. **MapReduce Optimization**: Input splits, combiners, compression, and skew handling
3. **YARN Resource Management**: Capacity scheduling, fair sharing, and resource isolation
4. **Performance Tuning**: Workload-specific optimizations and data locality
5. **Security**: Comprehensive Kerberos, encryption, and authorization
6. **Operations**: Monitoring, troubleshooting, and maintenance procedures
7. **Ecosystem Integration**: Working with Spark, Hive, and other tools

---

*This extended guide covers advanced Hadoop concepts essential for senior data engineering roles. Focus on understanding the architectural decisions, performance optimization techniques, and operational best practices for production deployments.*