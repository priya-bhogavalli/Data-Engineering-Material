# Apache ZooKeeper - Comprehensive Interview Questions & Answers

## 📋 Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Architecture & Components](#architecture--components)
3. [Data Model & Operations](#data-model--operations)
4. [Consensus & Leader Election](#consensus--leader-election)
5. [Performance & Scalability](#performance--scalability)
6. [Security & Access Control](#security--access-control)
7. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
8. [Integration & Use Cases](#integration--use-cases)
9. [Advanced Topics](#advanced-topics)
10. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Concepts

### 1. What is Apache ZooKeeper and what problems does it solve?

**Answer:**
Apache ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services in distributed systems.

**Problems it solves:**
- **Configuration Management**: Centralized configuration for distributed applications
- **Naming Service**: Hierarchical namespace for distributed resources
- **Synchronization**: Distributed locks, barriers, and queues
- **Group Membership**: Service discovery and cluster membership
- **Leader Election**: Automatic failover and leader selection
- **Notification Service**: Event-driven updates across distributed systems

**Key Benefits:**
- High availability and fault tolerance
- Strong consistency guarantees
- Simple programming model
- High performance for read-heavy workloads

### 2. Explain ZooKeeper's data model and znodes.

**Answer:**
ZooKeeper uses a hierarchical namespace similar to a file system, composed of znodes (ZooKeeper nodes).

**Znode Types:**
```
/app
├── /config
│   ├── database_url (persistent)
│   └── cache_size (persistent)
├── /services
│   ├── /web-server-1 (ephemeral)
│   └── /web-server-2 (ephemeral)
└── /locks
    └── /resource-lock (ephemeral sequential)
```

**Znode Categories:**
- **Persistent**: Remain until explicitly deleted
- **Ephemeral**: Deleted when client session ends
- **Sequential**: Automatically appended with sequence number
- **Container**: Deleted when last child is removed (ZK 3.5+)
- **TTL**: Time-to-live nodes (ZK 3.5+)

**Znode Properties:**
- Data (up to 1MB, typically small)
- ACL (Access Control List)
- Stat structure (version, timestamps, etc.)
- Children list

### 3. What are the different types of znodes in ZooKeeper?

**Answer:**

| Type | Description | Use Case | Lifecycle |
|------|-------------|----------|-----------|
| **Persistent** | Survives client disconnection | Configuration, metadata | Manual deletion |
| **Ephemeral** | Deleted when session ends | Service registration, locks | Session-based |
| **Persistent Sequential** | Persistent + auto sequence | Queues, ordering | Manual deletion |
| **Ephemeral Sequential** | Ephemeral + auto sequence | Leader election, barriers | Session-based |

**Examples:**
```bash
# Persistent znode
create /config/database "jdbc:mysql://localhost:3306/db"

# Ephemeral znode
create -e /services/web-server-1 "192.168.1.100:8080"

# Sequential znode
create -s /queue/task- "process-data"
# Creates: /queue/task-0000000001
```

### 4. Explain ZooKeeper's consistency model.

**Answer:**
ZooKeeper provides **sequential consistency** with the following guarantees:

**Consistency Guarantees:**
1. **Sequential Consistency**: All clients see operations in the same order
2. **Atomicity**: Operations either succeed completely or fail completely
3. **Monotonic Read Consistency**: Client never sees older data after newer data
4. **Monotonic Write Consistency**: Client writes are applied in order

**Important Notes:**
- **Not linearizable**: Reads may return stale data
- **Eventually consistent**: All nodes eventually converge
- **Strong consistency for writes**: All writes go through leader

**Example:**
```java
// Client A writes
zk.setData("/config/version", "v2".getBytes(), -1);

// Client B might still read "v1" briefly
byte[] data = zk.getData("/config/version", false, null);

// But sync() ensures latest data
zk.sync("/config/version", null, null);
data = zk.getData("/config/version", false, null); // Now returns "v2"
```

---

## Architecture & Components

### 5. Describe ZooKeeper's architecture and the role of each component.

**Answer:**

**ZooKeeper Ensemble Architecture:**
```
Client Applications
        ↓
    ZooKeeper Client Library
        ↓
┌─────────────────────────────┐
│     ZooKeeper Ensemble      │
│  ┌─────┐  ┌─────┐  ┌─────┐  │
│  │ ZK1 │  │ ZK2 │  │ ZK3 │  │
│  │(F)  │  │(L)  │  │(F)  │  │
│  └─────┘  └─────┘  └─────┘  │
└─────────────────────────────┘
```

**Components:**
1. **ZooKeeper Server**: Core service instance
2. **Leader**: Handles all write operations
3. **Followers**: Handle read operations, participate in voting
4. **Observers**: Handle reads only, don't vote (optional)
5. **Client**: Applications connecting to ZooKeeper

**Key Processes:**
- **Request Processor**: Handles client requests
- **Atomic Broadcast**: Ensures ordered message delivery (ZAB protocol)
- **Replica Database**: In-memory data tree with transaction logs

### 6. What is the ZAB (ZooKeeper Atomic Broadcast) protocol?

**Answer:**
ZAB is ZooKeeper's consensus protocol ensuring atomic broadcast of state changes.

**ZAB Phases:**
1. **Discovery**: Find most recent leader and establish epoch
2. **Synchronization**: Sync followers with leader's state
3. **Broadcast**: Normal operation, leader broadcasts proposals

**ZAB Process:**
```
Leader Election → Discovery → Synchronization → Broadcast
     ↑                                            ↓
     └──────── Leader Failure ←──────────────────┘
```

**Transaction Flow:**
1. Client sends write request to leader
2. Leader creates proposal with ZXID (ZooKeeper Transaction ID)
3. Leader sends proposal to all followers
4. Followers acknowledge proposal
5. Leader commits when majority acknowledges
6. Leader sends commit to all followers

**ZXID Structure:**
```
ZXID = <epoch><counter>
Example: 0x100000001 = epoch 1, transaction 1
```

### 7. How does leader election work in ZooKeeper?

**Answer:**

**Leader Election Process:**
1. **Fast Leader Election (FLE)** - Default algorithm
2. Each server votes for itself initially
3. Servers exchange votes and update based on:
   - Higher ZXID (most recent data)
   - Higher server ID (tie-breaker)
4. Server with majority votes becomes leader

**Election Criteria (Priority Order):**
1. **Epoch**: Higher epoch wins
2. **ZXID**: Higher transaction ID wins
3. **Server ID**: Higher ID wins (tie-breaker)

**Example Election:**
```
Server 1: ZXID=0x200000005, ID=1
Server 2: ZXID=0x200000005, ID=2  ← Winner (same ZXID, higher ID)
Server 3: ZXID=0x200000003, ID=3
```

**States During Election:**
- **LOOKING**: Searching for leader
- **FOLLOWING**: Following elected leader
- **LEADING**: Acting as leader
- **OBSERVING**: Observer mode (non-voting)

---

## Data Model & Operations

### 8. What are the main ZooKeeper operations and their characteristics?

**Answer:**

**Core Operations:**

| Operation | Description | Consistency | Use Case |
|-----------|-------------|-------------|----------|
| `create` | Create znode | Strong | Resource creation |
| `delete` | Delete znode | Strong | Cleanup, locks |
| `exists` | Check existence | Weak | Monitoring |
| `getData` | Read data | Weak | Configuration |
| `setData` | Write data | Strong | Updates |
| `getChildren` | List children | Weak | Discovery |
| `sync` | Force consistency | Strong | Ensure latest data |

**Operation Examples:**
```java
// Create with ACL and mode
zk.create("/config/db", data, ZooDefs.Ids.OPEN_ACL_UNSAFE, 
          CreateMode.PERSISTENT);

// Conditional update with version
zk.setData("/config/db", newData, currentVersion);

// Watch for changes
zk.getData("/config/db", new Watcher() {
    public void process(WatchedEvent event) {
        // Handle change
    }
}, null);
```

### 9. Explain ZooKeeper watches and their behavior.

**Answer:**

**Watch Characteristics:**
- **One-time triggers**: Must be reset after firing
- **Ordered**: Delivered in order of operations
- **Asynchronous**: Non-blocking notifications

**Watch Types:**
1. **Data watches**: `getData()`, `exists()`
2. **Child watches**: `getChildren()`

**Watch Events:**
```java
public enum EventType {
    NodeCreated,      // exists() watch
    NodeDeleted,      // getData(), exists() watches
    NodeDataChanged,  // getData(), exists() watches
    NodeChildrenChanged // getChildren() watch
}
```

**Watch Implementation:**
```java
// Set watch
Stat stat = zk.exists("/config/db", new Watcher() {
    public void process(WatchedEvent event) {
        if (event.getType() == Event.EventType.NodeDataChanged) {
            // Re-read data and reset watch
            try {
                byte[] data = zk.getData("/config/db", this, null);
                processConfigChange(data);
            } catch (Exception e) {
                // Handle error
            }
        }
    }
});
```

### 10. How do you implement distributed locks using ZooKeeper?

**Answer:**

**Lock Implementation Pattern:**
```java
public class DistributedLock {
    private ZooKeeper zk;
    private String lockPath;
    private String currentLockNode;
    
    public void acquireLock() throws Exception {
        // Create ephemeral sequential node
        currentLockNode = zk.create(lockPath + "/lock-", 
                                   new byte[0], 
                                   ZooDefs.Ids.OPEN_ACL_UNSAFE,
                                   CreateMode.EPHEMERAL_SEQUENTIAL);
        
        while (true) {
            List<String> children = zk.getChildren(lockPath, false);
            Collections.sort(children);
            
            String lockName = currentLockNode.substring(
                currentLockNode.lastIndexOf('/') + 1);
            
            if (lockName.equals(children.get(0))) {
                // We have the lock
                return;
            }
            
            // Watch the previous node
            String previousNode = null;
            for (int i = 1; i < children.size(); i++) {
                if (children.get(i).equals(lockName)) {
                    previousNode = children.get(i - 1);
                    break;
                }
            }
            
            if (previousNode != null) {
                CountDownLatch latch = new CountDownLatch(1);
                Stat stat = zk.exists(lockPath + "/" + previousNode, 
                    new Watcher() {
                        public void process(WatchedEvent event) {
                            latch.countDown();
                        }
                    });
                
                if (stat != null) {
                    latch.await(); // Wait for previous node to be deleted
                }
            }
        }
    }
    
    public void releaseLock() throws Exception {
        zk.delete(currentLockNode, -1);
    }
}
```

---

## Performance & Scalability

### 11. What are ZooKeeper's performance characteristics and limitations?

**Answer:**

**Performance Characteristics:**
- **Read throughput**: Scales with ensemble size
- **Write throughput**: Limited by leader capacity
- **Latency**: Typically 1-2ms for reads, 2-10ms for writes
- **Data size**: 1MB per znode limit

**Scalability Patterns:**
```
Read Performance:  Client → Any Server (Fast)
Write Performance: Client → Leader → Followers (Slower)

Ensemble Size vs Performance:
3 servers: ~10K writes/sec, ~100K reads/sec
5 servers: ~8K writes/sec, ~150K reads/sec
7 servers: ~6K writes/sec, ~200K reads/sec
```

**Limitations:**
- **Write bottleneck**: Single leader handles all writes
- **Memory bound**: All data must fit in memory
- **Network sensitive**: Requires low-latency network
- **Not for large data**: 1MB znode limit

**Optimization Strategies:**
- Use observers for read scaling
- Minimize watch usage
- Batch operations when possible
- Keep data small
- Use appropriate ensemble size (3-7 servers)

### 12. How do you monitor ZooKeeper performance and health?

**Answer:**

**Key Metrics to Monitor:**

**1. Server Metrics:**
```bash
# Four Letter Words (4lw) commands
echo "stat" | nc localhost 2181  # Server statistics
echo "conf" | nc localhost 2181  # Configuration
echo "envi" | nc localhost 2181  # Environment
echo "ruok" | nc localhost 2181  # Health check
```

**2. JMX Metrics:**
```java
// Key JMX beans
org.apache.ZooKeeperService:name0=ReplicatedServer_id1
- OutstandingRequests
- AvgRequestLatency
- MaxRequestLatency
- PacketsReceived/Sent
- NumAliveConnections
```

**3. Log Analysis:**
```bash
# Monitor ZooKeeper logs
tail -f zookeeper.log | grep -E "(WARN|ERROR|Leader|Follower)"

# Transaction log analysis
java -cp zookeeper.jar org.apache.zookeeper.server.LogFormatter log.1
```

**4. Health Check Script:**
```bash
#!/bin/bash
ZK_HOST="localhost:2181"

# Check if ZooKeeper is responding
RUOK=$(echo "ruok" | nc $ZK_HOST 2>/dev/null)
if [ "$RUOK" != "imok" ]; then
    echo "ZooKeeper not responding"
    exit 1
fi

# Check leader election
STAT=$(echo "stat" | nc $ZK_HOST 2>/dev/null)
if echo "$STAT" | grep -q "Mode: standalone\|Mode: leader\|Mode: follower"; then
    echo "ZooKeeper healthy"
else
    echo "ZooKeeper in unknown state"
    exit 1
fi
```

---

## Security & Access Control

### 13. How does ZooKeeper handle authentication and authorization?

**Answer:**

**Authentication Schemes:**
1. **digest**: Username/password
2. **sasl**: SASL authentication (Kerberos)
3. **ip**: IP address-based
4. **x509**: Certificate-based

**ACL (Access Control List) Structure:**
```java
// ACL format: scheme:id:permissions
ACL acl = new ACL(ZooDefs.Perms.ALL, new Id("digest", "user:password"));

// Permissions
CREATE (c) - create child nodes
READ (r)   - read node data and list children
WRITE (w)  - write node data
DELETE (d) - delete child nodes
ADMIN (a)  - set ACL permissions
```

**Security Implementation:**
```java
// Add authentication
zk.addAuthInfo("digest", "user:password".getBytes());

// Create node with ACL
List<ACL> acls = Arrays.asList(
    new ACL(ZooDefs.Perms.ALL, new Id("digest", "admin:secret")),
    new ACL(ZooDefs.Perms.READ, new Id("world", "anyone"))
);

zk.create("/secure/config", data, acls, CreateMode.PERSISTENT);
```

**SASL/Kerberos Setup:**
```properties
# jaas.conf
Server {
    com.sun.security.auth.module.Krb5LoginModule required
    useKeyTab=true
    keyTab="/path/to/zookeeper.keytab"
    storeKey=true
    useTicketCache=false
    principal="zookeeper/hostname@REALM";
};
```

### 14. What are best practices for ZooKeeper security?

**Answer:**

**Security Best Practices:**

**1. Network Security:**
```bash
# Enable SSL/TLS
secureClientPort=2182
ssl.keyStore.location=/path/to/keystore.jks
ssl.trustStore.location=/path/to/truststore.jks
```

**2. Authentication:**
```java
// Always use authentication for sensitive data
zk.addAuthInfo("digest", "username:password".getBytes());

// Use SASL for enterprise environments
System.setProperty("java.security.auth.login.config", "/path/to/jaas.conf");
```

**3. Authorization:**
```java
// Principle of least privilege
List<ACL> restrictedACL = Arrays.asList(
    new ACL(ZooDefs.Perms.READ | ZooDefs.Perms.WRITE, 
            new Id("digest", "app:password")),
    new ACL(ZooDefs.Perms.ALL, 
            new Id("digest", "admin:adminpass"))
);
```

**4. Network Isolation:**
- Use private networks for ZooKeeper ensemble
- Firewall rules to restrict access
- VPN for remote access

**5. Monitoring:**
- Log all authentication attempts
- Monitor failed connections
- Alert on unusual access patterns

---

## Integration & Use Cases

### 15. How is ZooKeeper used in Apache Kafka?

**Answer:**

**Kafka's ZooKeeper Usage:**

**1. Metadata Management:**
```
/brokers/ids/0          # Broker registration
/brokers/topics/mytopic # Topic metadata
/config/topics/mytopic  # Topic configuration
/admin/delete_topics    # Topic deletion
```

**2. Controller Election:**
```java
// Kafka controller election using ZooKeeper
/controller → {"version":1,"brokerid":0,"timestamp":"1234567890"}
```

**3. Consumer Group Coordination (Legacy):**
```
/consumers/mygroup/ids/consumer-1     # Consumer registration
/consumers/mygroup/offsets/topic/0    # Offset storage
/consumers/mygroup/owners/topic/0     # Partition ownership
```

**4. Configuration Management:**
```bash
# Dynamic configuration changes
kafka-configs.sh --zookeeper localhost:2181 \
  --entity-type topics --entity-name mytopic \
  --alter --add-config retention.ms=86400000
```

**Note**: Kafka is moving away from ZooKeeper dependency with KRaft (Kafka Raft) in newer versions.

### 16. Describe common ZooKeeper use cases in distributed systems.

**Answer:**

**1. Service Discovery:**
```java
// Service registration
public void registerService(String serviceName, String address) {
    String servicePath = "/services/" + serviceName;
    zk.create(servicePath + "/" + address, 
              address.getBytes(),
              ZooDefs.Ids.OPEN_ACL_UNSAFE,
              CreateMode.EPHEMERAL_SEQUENTIAL);
}

// Service discovery
public List<String> discoverServices(String serviceName) {
    return zk.getChildren("/services/" + serviceName, true);
}
```

**2. Configuration Management:**
```java
// Centralized configuration
public class ConfigManager {
    public void updateConfig(String key, String value) {
        zk.setData("/config/" + key, value.getBytes(), -1);
    }
    
    public String getConfig(String key) {
        byte[] data = zk.getData("/config/" + key, true, null);
        return new String(data);
    }
}
```

**3. Distributed Barriers:**
```java
// Barrier implementation
public class DistributedBarrier {
    public void enter() throws Exception {
        zk.create(barrierPath + "/" + name, 
                  new byte[0], 
                  ZooDefs.Ids.OPEN_ACL_UNSAFE,
                  CreateMode.EPHEMERAL);
        
        while (true) {
            List<String> children = zk.getChildren(barrierPath, true);
            if (children.size() >= barrierSize) {
                break; // Barrier reached
            }
            wait(); // Wait for more participants
        }
    }
}
```

**4. Leader Election:**
```java
// Simple leader election
public class LeaderElection {
    public void electLeader() throws Exception {
        String leaderPath = zk.create("/election/leader-", 
                                     new byte[0],
                                     ZooDefs.Ids.OPEN_ACL_UNSAFE,
                                     CreateMode.EPHEMERAL_SEQUENTIAL);
        
        List<String> children = zk.getChildren("/election", false);
        Collections.sort(children);
        
        if (leaderPath.endsWith(children.get(0))) {
            // I am the leader
            becomeLeader();
        } else {
            // Watch the previous node
            watchPreviousNode();
        }
    }
}
```

---

## Advanced Topics

### 17. What are ZooKeeper observers and when should you use them?

**Answer:**

**ZooKeeper Observers:**
- **Non-voting members** of the ensemble
- **Handle read requests** but don't participate in leader election
- **Improve read scalability** without affecting write performance

**When to Use Observers:**
1. **Geographic distribution**: Observers in remote data centers
2. **Read scaling**: When you need more read capacity
3. **Odd ensemble size**: Maintain fault tolerance with even total servers

**Configuration:**
```properties
# zoo.cfg
server.1=zk1:2888:3888:participant
server.2=zk2:2888:3888:participant  
server.3=zk3:2888:3888:participant
server.4=zk4:2888:3888:observer
server.5=zk5:2888:3888:observer
```

**Benefits:**
- Increased read throughput
- Better geographic distribution
- No impact on write performance
- Faster client failover

**Limitations:**
- Don't contribute to quorum
- Slightly higher latency for writes
- More complex deployment

### 18. How do you handle ZooKeeper ensemble failures and recovery?

**Answer:**

**Failure Scenarios & Recovery:**

**1. Single Server Failure:**
```bash
# Automatic handling - no action needed
# Ensemble continues with remaining servers
# Failed server rejoins automatically when restarted
```

**2. Majority Failure (Split Brain):**
```bash
# Ensemble becomes read-only
# Manual intervention required
# Steps:
1. Stop all servers
2. Identify server with highest ZXID
3. Start servers one by one
4. Verify leader election
```

**3. Data Corruption:**
```bash
# Recovery from transaction logs
cd $ZK_DATA_DIR
java -cp zookeeper.jar org.apache.zookeeper.server.LogFormatter log.1

# Restore from snapshot
cp snapshot.latest snapshot.restore
```

**4. Complete Cluster Loss:**
```bash
# Disaster recovery steps:
1. Restore from backup
2. Update myid files
3. Clean transaction logs if needed
4. Start ensemble
5. Verify data integrity
```

**Recovery Best Practices:**
- Regular backups of data directory
- Monitor disk space and I/O
- Use separate disks for logs and snapshots
- Implement proper alerting
- Document recovery procedures

### 19. What are the differences between ZooKeeper and other coordination services?

**Answer:**

**ZooKeeper vs Alternatives:**

| Feature | ZooKeeper | etcd | Consul | Redis |
|---------|-----------|------|--------|-------|
| **Consistency** | Sequential | Linearizable | Strong | Eventual |
| **Protocol** | ZAB | Raft | Raft | Custom |
| **Data Model** | Hierarchical | Key-Value | Key-Value | Data Structures |
| **Language** | Java | Go | Go | C |
| **Use Cases** | General coordination | Kubernetes | Service mesh | Caching, queues |

**When to Choose ZooKeeper:**
- **Mature ecosystem**: Hadoop, Kafka, Storm
- **Complex coordination**: Multiple coordination primitives needed
- **Java environment**: Easy integration with Java applications
- **Proven stability**: Long track record in production

**When to Consider Alternatives:**
- **etcd**: Kubernetes environments, simpler key-value needs
- **Consul**: Service discovery with health checking
- **Redis**: High-performance caching with coordination features

### 20. How do you optimize ZooKeeper for high availability?

**Answer:**

**High Availability Strategies:**

**1. Ensemble Sizing:**
```bash
# Optimal sizes for different fault tolerance
3 servers: Tolerates 1 failure (minimum production)
5 servers: Tolerates 2 failures (recommended)
7 servers: Tolerates 3 failures (high availability)
```

**2. Geographic Distribution:**
```
Data Center 1: Server 1, Server 2
Data Center 2: Server 3, Observer 1
Data Center 3: Observer 2, Observer 3
```

**3. Hardware Optimization:**
```bash
# Dedicated disks
dataDir=/ssd/zookeeper/data      # Fast SSD for snapshots
dataLogDir=/ssd/zookeeper/logs   # Separate SSD for transaction logs

# Memory sizing
-Xmx4g -Xms4g  # Sufficient heap for data + overhead
```

**4. Network Configuration:**
```properties
# zoo.cfg optimizations
tickTime=2000                    # Heartbeat interval
initLimit=10                     # Follower connection timeout
syncLimit=5                      # Follower sync timeout
maxClientCnxns=60               # Client connection limit
autopurge.snapRetainCount=10    # Snapshot retention
autopurge.purgeInterval=1       # Cleanup interval
```

**5. Monitoring & Alerting:**
```bash
# Critical alerts
- Server down
- Leader election in progress
- High latency (>100ms)
- Disk space low (<20%)
- Memory usage high (>80%)
```

---

## Scenario-Based Questions

### 21. Design a distributed configuration management system using ZooKeeper.

**Answer:**

**System Architecture:**
```
Applications → Config Client → ZooKeeper Ensemble
                    ↓
              Local Cache + Watchers
```

**Implementation:**
```java
public class DistributedConfigManager {
    private ZooKeeper zk;
    private Map<String, String> localCache = new ConcurrentHashMap<>();
    private Map<String, List<ConfigListener>> listeners = new ConcurrentHashMap<>();
    
    public void initialize() throws Exception {
        zk = new ZooKeeper("zk1:2181,zk2:2181,zk3:2181", 
                          3000, new DefaultWatcher());
        
        // Ensure config root exists
        if (zk.exists("/config", false) == null) {
            zk.create("/config", new byte[0], 
                     ZooDefs.Ids.OPEN_ACL_UNSAFE, 
                     CreateMode.PERSISTENT);
        }
        
        // Load initial configuration
        loadAllConfigs();
    }
    
    public String getConfig(String key) {
        return localCache.get(key);
    }
    
    public void setConfig(String key, String value) throws Exception {
        String path = "/config/" + key;
        
        if (zk.exists(path, false) != null) {
            zk.setData(path, value.getBytes(), -1);
        } else {
            zk.create(path, value.getBytes(), 
                     ZooDefs.Ids.OPEN_ACL_UNSAFE, 
                     CreateMode.PERSISTENT);
        }
    }
    
    public void watchConfig(String key, ConfigListener listener) {
        listeners.computeIfAbsent(key, k -> new ArrayList<>()).add(listener);
        
        try {
            String path = "/config/" + key;
            zk.getData(path, new Watcher() {
                public void process(WatchedEvent event) {
                    if (event.getType() == Event.EventType.NodeDataChanged) {
                        handleConfigChange(key);
                    }
                }
            }, null);
        } catch (Exception e) {
            // Handle error
        }
    }
    
    private void handleConfigChange(String key) {
        try {
            String path = "/config/" + key;
            byte[] data = zk.getData(path, true, null);
            String value = new String(data);
            
            localCache.put(key, value);
            
            // Notify listeners
            List<ConfigListener> keyListeners = listeners.get(key);
            if (keyListeners != null) {
                for (ConfigListener listener : keyListeners) {
                    listener.onConfigChanged(key, value);
                }
            }
        } catch (Exception e) {
            // Handle error
        }
    }
}

interface ConfigListener {
    void onConfigChanged(String key, String value);
}
```

**Features:**
- **Local caching** for performance
- **Watch-based updates** for real-time changes
- **Listener pattern** for application notifications
- **Hierarchical configuration** support

### 22. How would you implement a distributed work queue using ZooKeeper?

**Answer:**

**Work Queue Design:**
```
/queue
├── /tasks
│   ├── task-0000000001 (persistent sequential)
│   ├── task-0000000002 (persistent sequential)
│   └── task-0000000003 (persistent sequential)
├── /processing
│   ├── worker1-task-0000000001 (ephemeral)
│   └── worker2-task-0000000002 (ephemeral)
└── /completed
    └── task-0000000001 (persistent)
```

**Implementation:**
```java
public class DistributedWorkQueue {
    private ZooKeeper zk;
    private String queuePath = "/queue";
    private String tasksPath = queuePath + "/tasks";
    private String processingPath = queuePath + "/processing";
    private String completedPath = queuePath + "/completed";
    private String workerId;
    
    public void initialize() throws Exception {
        // Create queue structure
        createPath(queuePath);
        createPath(tasksPath);
        createPath(processingPath);
        createPath(completedPath);
        
        workerId = InetAddress.getLocalHost().getHostName() + "-" + 
                   Thread.currentThread().getId();
    }
    
    // Producer: Add task to queue
    public String submitTask(String taskData) throws Exception {
        return zk.create(tasksPath + "/task-", 
                        taskData.getBytes(),
                        ZooDefs.Ids.OPEN_ACL_UNSAFE,
                        CreateMode.PERSISTENT_SEQUENTIAL);
    }
    
    // Consumer: Get next task
    public Task getNextTask() throws Exception {
        while (true) {
            List<String> tasks = zk.getChildren(tasksPath, false);
            
            if (tasks.isEmpty()) {
                // Wait for new tasks
                zk.getChildren(tasksPath, new Watcher() {
                    public void process(WatchedEvent event) {
                        synchronized (this) {
                            notifyAll();
                        }
                    }
                });
                
                synchronized (this) {
                    wait();
                }
                continue;
            }
            
            // Get oldest task
            Collections.sort(tasks);
            String taskName = tasks.get(0);
            String taskPath = tasksPath + "/" + taskName;
            
            try {
                // Atomically move task to processing
                byte[] data = zk.getData(taskPath, false, null);
                String processingNode = processingPath + "/" + workerId + "-" + taskName;
                
                zk.create(processingNode, data, 
                         ZooDefs.Ids.OPEN_ACL_UNSAFE, 
                         CreateMode.EPHEMERAL);
                
                zk.delete(taskPath, -1);
                
                return new Task(taskName, new String(data), processingNode);
                
            } catch (KeeperException.NodeExistsException e) {
                // Task already taken, try next
                continue;
            } catch (KeeperException.NoNodeException e) {
                // Task already processed, try next
                continue;
            }
        }
    }
    
    // Complete task processing
    public void completeTask(Task task) throws Exception {
        // Move to completed
        zk.create(completedPath + "/" + task.getName(), 
                 task.getData().getBytes(),
                 ZooDefs.Ids.OPEN_ACL_UNSAFE,
                 CreateMode.PERSISTENT);
        
        // Remove from processing
        zk.delete(task.getProcessingNode(), -1);
    }
    
    // Handle worker failure - tasks return to queue
    public void handleWorkerFailure() {
        // Ephemeral processing nodes automatically deleted
        // Implement cleanup job to move orphaned tasks back to queue
    }
}

class Task {
    private String name;
    private String data;
    private String processingNode;
    
    // Constructor and getters
}
```

**Features:**
- **FIFO ordering** with sequential znodes
- **Atomic task claiming** to prevent double processing
- **Failure handling** with ephemeral processing nodes
- **Scalable** - multiple producers and consumers

### 23. Design a service discovery system with health checking using ZooKeeper.

**Answer:**

**Service Discovery Architecture:**
```
/services
├── /web-service
│   ├── instance-1 (ephemeral) → {"host":"192.168.1.10","port":8080,"health":"healthy"}
│   └── instance-2 (ephemeral) → {"host":"192.168.1.11","port":8080,"health":"healthy"}
├── /database-service
│   └── instance-1 (ephemeral) → {"host":"192.168.1.20","port":5432,"health":"healthy"}
└── /cache-service
    ├── instance-1 (ephemeral) → {"host":"192.168.1.30","port":6379,"health":"healthy"}
    └── instance-2 (ephemeral) → {"host":"192.168.1.31","port":6379,"health":"degraded"}
```

**Implementation:**
```java
public class ServiceDiscovery {
    private ZooKeeper zk;
    private String servicesPath = "/services";
    private ScheduledExecutorService healthChecker;
    private Map<String, ServiceInstance> localServices = new ConcurrentHashMap<>();
    
    public void initialize() throws Exception {
        zk = new ZooKeeper("zk1:2181,zk2:2181,zk3:2181", 3000, null);
        healthChecker = Executors.newScheduledThreadPool(2);
        
        // Create services root
        if (zk.exists(servicesPath, false) == null) {
            zk.create(servicesPath, new byte[0], 
                     ZooDefs.Ids.OPEN_ACL_UNSAFE, 
                     CreateMode.PERSISTENT);
        }
    }
    
    // Register service instance
    public void registerService(String serviceName, ServiceInstance instance) 
            throws Exception {
        String servicePath = servicesPath + "/" + serviceName;
        
        // Create service path if not exists
        if (zk.exists(servicePath, false) == null) {
            zk.create(servicePath, new byte[0], 
                     ZooDefs.Ids.OPEN_ACL_UNSAFE, 
                     CreateMode.PERSISTENT);
        }
        
        // Register instance as ephemeral sequential node
        String instanceData = objectMapper.writeValueAsString(instance);
        String instancePath = zk.create(servicePath + "/instance-", 
                                       instanceData.getBytes(),
                                       ZooDefs.Ids.OPEN_ACL_UNSAFE,
                                       CreateMode.EPHEMERAL_SEQUENTIAL);
        
        instance.setZkPath(instancePath);
        localServices.put(instancePath, instance);
        
        // Start health checking
        startHealthCheck(instance);
    }
    
    // Discover service instances
    public List<ServiceInstance> discoverService(String serviceName) 
            throws Exception {
        String servicePath = servicesPath + "/" + serviceName;
        List<ServiceInstance> instances = new ArrayList<>();
        
        if (zk.exists(servicePath, false) == null) {
            return instances; // Service not found
        }
        
        List<String> children = zk.getChildren(servicePath, true);
        
        for (String child : children) {
            try {
                byte[] data = zk.getData(servicePath + "/" + child, false, null);
                ServiceInstance instance = objectMapper.readValue(data, 
                                                                  ServiceInstance.class);
                
                // Only return healthy instances
                if ("healthy".equals(instance.getHealth())) {
                    instances.add(instance);
                }
            } catch (Exception e) {
                // Skip invalid instances
            }
        }
        
        return instances;
    }
    
    // Watch for service changes
    public void watchService(String serviceName, ServiceChangeListener listener) 
            throws Exception {
        String servicePath = servicesPath + "/" + serviceName;
        
        zk.getChildren(servicePath, new Watcher() {
            public void process(WatchedEvent event) {
                if (event.getType() == Event.EventType.NodeChildrenChanged) {
                    try {
                        List<ServiceInstance> instances = discoverService(serviceName);
                        listener.onServiceChanged(serviceName, instances);
                        
                        // Re-register watch
                        watchService(serviceName, listener);
                    } catch (Exception e) {
                        // Handle error
                    }
                }
            }
        });
    }
    
    // Health checking
    private void startHealthCheck(ServiceInstance instance) {
        healthChecker.scheduleWithFixedDelay(() -> {
            try {
                HealthStatus status = performHealthCheck(instance);
                instance.setHealth(status.toString().toLowerCase());
                
                // Update ZooKeeper with new health status
                String instanceData = objectMapper.writeValueAsString(instance);
                zk.setData(instance.getZkPath(), instanceData.getBytes(), -1);
                
            } catch (Exception e) {
                // Mark as unhealthy on check failure
                instance.setHealth("unhealthy");
                try {
                    String instanceData = objectMapper.writeValueAsString(instance);
                    zk.setData(instance.getZkPath(), instanceData.getBytes(), -1);
                } catch (Exception ex) {
                    // Log error
                }
            }
        }, 0, 30, TimeUnit.SECONDS);
    }
    
    private HealthStatus performHealthCheck(ServiceInstance instance) {
        // Implement actual health check logic
        // HTTP endpoint, database connection, etc.
        try {
            URL url = new URL("http://" + instance.getHost() + ":" + 
                             instance.getPort() + "/health");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);
            
            int responseCode = conn.getResponseCode();
            return responseCode == 200 ? HealthStatus.HEALTHY : HealthStatus.UNHEALTHY;
        } catch (Exception e) {
            return HealthStatus.UNHEALTHY;
        }
    }
}

class ServiceInstance {
    private String host;
    private int port;
    private String health;
    private String zkPath;
    private Map<String, String> metadata;
    
    // Constructors, getters, setters
}

enum HealthStatus {
    HEALTHY, DEGRADED, UNHEALTHY
}

interface ServiceChangeListener {
    void onServiceChanged(String serviceName, List<ServiceInstance> instances);
}
```

**Features:**
- **Automatic registration/deregistration** with ephemeral nodes
- **Health checking** with periodic updates
- **Service watching** for real-time updates
- **Metadata support** for additional service information
- **Load balancer integration** ready

---

## Summary

This comprehensive guide covers ZooKeeper's core concepts, architecture, operations, and real-world applications. Key takeaways:

1. **Coordination Service**: ZooKeeper provides essential distributed coordination primitives
2. **Consistency Model**: Sequential consistency with strong write consistency
3. **Architecture**: Leader-follower model with ZAB consensus protocol
4. **Use Cases**: Configuration management, service discovery, distributed locks, leader election
5. **Performance**: Read-scalable, write-limited, memory-bound
6. **Integration**: Widely used in Hadoop ecosystem (Kafka, Storm, etc.)

Understanding these concepts and patterns will help you effectively use ZooKeeper in distributed systems and handle related interview questions with confidence.