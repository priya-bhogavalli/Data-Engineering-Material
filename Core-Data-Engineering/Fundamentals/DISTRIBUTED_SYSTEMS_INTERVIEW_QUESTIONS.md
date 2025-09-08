# 🌐 Distributed Systems Interview Questions & Answers

## Table of Contents
1. [CAP Theorem](#cap-theorem)
2. [Consistency Models](#consistency-models)
3. [Consensus Algorithms](#consensus-algorithms)
4. [Fault Tolerance](#fault-tolerance)
5. [Replication Strategies](#replication-strategies)
6. [Distributed Storage](#distributed-storage)
7. [Time and Ordering](#time-and-ordering)
8. [Distributed Transactions](#distributed-transactions)

---

## CAP Theorem

### 1. What is the CAP theorem and explain its three components?

**Answer:**
The CAP theorem, also known as Brewer's theorem, states that in a distributed data store, it is impossible to simultaneously provide all three of the following guarantees:

**Consistency (C):** All nodes see the same data at the same time
- Every read receives the most recent write or an error
- All nodes have the same view of data simultaneously

**Availability (A):** The system remains operational
- Every request receives a response (success or failure)
- System continues to function despite node failures

**Partition Tolerance (P):** System continues despite network failures
- System continues to operate despite arbitrary message loss
- Network partitions don't bring down the entire system

**Mathematical Expression:** |{C, A, P}| ≤ 2

**Real-world Example:**
```
Bank Transfer Scenario:
- Account A: $1000
- Account B: $500
- Transfer $200 from A to B

During network partition:
- CP System: Reject transaction to maintain consistency
- AP System: Allow transaction, risk temporary inconsistency
```

### 2. Give examples of CP, AP, and CA systems with justifications.

**Answer:**

**CP Systems (Consistency + Partition Tolerance):**
- **MongoDB with strong consistency**
  - Chooses consistency over availability during partitions
  - Primary-secondary replication with read/write to primary only
  
- **HBase**
  - Strong consistency through single master architecture
  - Becomes unavailable if master fails during partition

- **Redis Cluster**
  - Maintains consistency by rejecting writes during partitions
  - Uses consensus for cluster membership

**AP Systems (Availability + Partition Tolerance):**
- **Cassandra**
  - Eventually consistent, highly available
  - Accepts writes even during partitions
  - Uses tunable consistency levels

- **DynamoDB**
  - Eventually consistent reads by default
  - Always available for reads/writes
  - Conflict resolution through timestamps

- **DNS System**
  - Highly available, eventually consistent
  - Cached responses may be stale but system remains operational

**CA Systems (Consistency + Availability):**
- **Traditional RDBMS (PostgreSQL, MySQL)**
  - ACID properties ensure consistency
  - High availability through replication
  - Cannot handle network partitions gracefully

- **Single-node systems**
  - No network partitions to worry about
  - Can provide both consistency and availability

### 3. How does the PACELC theorem extend the CAP theorem?

**Answer:**
PACELC theorem extends CAP by considering system behavior during normal operation (no partitions):

**PACELC Formula:** 
- **P**artition → choose **A**vailability or **C**onsistency
- **E**lse → choose **L**atency or **C**onsistency

**Examples:**

**PA/EL Systems:**
```
Cassandra:
- During partition: Choose Availability over Consistency
- Normal operation: Choose Latency over Consistency
- Eventually consistent, low latency reads
```

**PC/EC Systems:**
```
HBase:
- During partition: Choose Consistency over Availability  
- Normal operation: Choose Consistency over Latency
- Strong consistency, higher latency
```

**PA/EC Systems:**
```
MongoDB:
- During partition: Choose Availability (with read preference)
- Normal operation: Choose Consistency over Latency
- Configurable consistency levels
```

### 4. How do you choose between consistency and availability in practice?

**Answer:**

**Choose Consistency (CP) when:**
- Financial transactions (banking, payments)
- Inventory management
- User authentication systems
- Critical business data

```python
# Banking example - must be consistent
def transfer_money(from_account, to_account, amount):
    with transaction():
        if get_balance(from_account) >= amount:
            debit(from_account, amount)
            credit(to_account, amount)
            return True
        else:
            raise InsufficientFundsError()
```

**Choose Availability (AP) when:**
- Social media feeds
- Content delivery
- Analytics and logging
- User preferences

```python
# Social media feed - availability preferred
def get_user_feed(user_id):
    try:
        # Try to get latest feed
        return get_fresh_feed(user_id)
    except ServiceUnavailable:
        # Fallback to cached/stale data
        return get_cached_feed(user_id)
```

**Hybrid Approaches:**
```python
# Different consistency for different operations
class ECommerceSystem:
    def update_inventory(self, product_id, quantity):
        # Strong consistency for inventory
        return self.consistent_store.update(product_id, quantity)
    
    def update_user_preferences(self, user_id, preferences):
        # Eventual consistency for preferences
        return self.available_store.update(user_id, preferences)
```

---

## Consistency Models

### 5. Explain different consistency models in distributed systems.

**Answer:**

**Strong Consistency Models:**

**1. Linearizability:**
```
Operations appear to execute atomically at some point between start and completion
Timeline: [Read(x)=1] [Write(x,2)] [Read(x)=2]
All nodes see operations in same order
```

**2. Sequential Consistency:**
```
Operations appear in some sequential order consistent with program order
Node A: Write(x,1), Write(x,2)
Node B: Read(x)=2, Read(x)=1 ❌ (violates program order)
Node B: Read(x)=1, Read(x)=2 ✅ (valid)
```

**Weak Consistency Models:**

**3. Eventual Consistency:**
```python
# Amazon DynamoDB example
def update_user_profile(user_id, data):
    # Write to primary region
    primary_db.put_item(user_id, data)
    
    # Asynchronously replicate to other regions
    async_replicate_to_regions(user_id, data)
    
    # Reads may return stale data temporarily
    # But will eventually converge
```

**4. Causal Consistency:**
```
If event A causally precedes event B, all nodes see A before B
User posts message → User edits message
All nodes see original before edit
```

**5. Session Consistency:**
```python
class SessionConsistentStore:
    def __init__(self):
        self.session_versions = {}
    
    def read(self, key, session_id):
        min_version = self.session_versions.get(session_id, 0)
        return self.read_with_min_version(key, min_version)
    
    def write(self, key, value, session_id):
        version = self.write_with_version(key, value)
        self.session_versions[session_id] = version
```

### 6. How do you implement eventual consistency in practice?

**Answer:**

**1. Vector Clocks for Conflict Detection:**
```python
class VectorClock:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.clock = {node: 0 for node in nodes}
    
    def tick(self):
        self.clock[self.node_id] += 1
    
    def update(self, other_clock):
        for node in self.clock:
            self.clock[node] = max(self.clock[node], other_clock.get(node, 0))
        self.tick()
    
    def compare(self, other):
        # Returns: 'before', 'after', 'concurrent'
        self_before = all(self.clock[n] <= other.get(n, 0) for n in self.clock)
        other_before = all(other.get(n, 0) <= self.clock[n] for n in self.clock)
        
        if self_before and not other_before:
            return 'before'
        elif other_before and not self_before:
            return 'after'
        else:
            return 'concurrent'
```

**2. Conflict-Free Replicated Data Types (CRDTs):**
```python
# G-Counter (Grow-only Counter)
class GCounter:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.counters = {node: 0 for node in nodes}
    
    def increment(self):
        self.counters[self.node_id] += 1
    
    def value(self):
        return sum(self.counters.values())
    
    def merge(self, other):
        for node in self.counters:
            self.counters[node] = max(
                self.counters[node], 
                other.counters.get(node, 0)
            )

# PN-Counter (Increment/Decrement Counter)
class PNCounter:
    def __init__(self, node_id, nodes):
        self.p_counter = GCounter(node_id, nodes)  # Positive
        self.n_counter = GCounter(node_id, nodes)  # Negative
    
    def increment(self):
        self.p_counter.increment()
    
    def decrement(self):
        self.n_counter.increment()
    
    def value(self):
        return self.p_counter.value() - self.n_counter.value()
```

---

## Consensus Algorithms

### 7. Explain the Raft consensus algorithm and its phases.

**Answer:**

**Raft Overview:**
Raft is a consensus algorithm designed to be more understandable than Paxos while providing the same guarantees.

**Node States:**
- **Leader:** Handles all client requests, sends heartbeats
- **Follower:** Passive, responds to leader and candidate requests  
- **Candidate:** Seeks votes to become leader

**Phase 1: Leader Election**
```python
class RaftNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.state = 'follower'
        self.current_term = 0
        self.voted_for = None
        self.election_timeout = random.randint(150, 300)  # ms
    
    def start_election(self):
        self.state = 'candidate'
        self.current_term += 1
        self.voted_for = self.node_id
        votes_received = 1  # Vote for self
        
        for peer in self.peers:
            if self.request_vote(peer):
                votes_received += 1
        
        if votes_received > len(self.peers) // 2:
            self.become_leader()
    
    def request_vote(self, peer):
        # Send RequestVote RPC
        return peer.handle_vote_request(
            term=self.current_term,
            candidate_id=self.node_id,
            last_log_index=len(self.log) - 1,
            last_log_term=self.log[-1].term if self.log else 0
        )
```

**Phase 2: Log Replication**
```python
def append_entries(self, entries):
    """Leader replicates entries to followers"""
    success_count = 1  # Leader counts as success
    
    for follower in self.followers:
        if self.send_append_entries(follower, entries):
            success_count += 1
    
    # Commit if majority acknowledges
    if success_count > len(self.peers) // 2:
        self.commit_entries(entries)
        return True
    return False

def send_append_entries(self, follower, entries):
    return follower.handle_append_entries(
        term=self.current_term,
        leader_id=self.node_id,
        prev_log_index=self.get_prev_log_index(follower),
        prev_log_term=self.get_prev_log_term(follower),
        entries=entries,
        leader_commit=self.commit_index
    )
```

**Safety Properties:**
- **Election Safety:** At most one leader per term
- **Leader Append-Only:** Leader never overwrites log entries
- **Log Matching:** If two logs contain entry with same index and term, logs are identical up to that index

### 8. Compare Raft vs Paxos consensus algorithms.

**Answer:**

| Aspect | Raft | Paxos |
|--------|------|-------|
| **Understandability** | Designed for clarity | Complex, hard to understand |
| **Leader Election** | Strong leader model | No designated leader |
| **Log Structure** | Strongly consistent log | More flexible |
| **Implementation** | Easier to implement | Notoriously difficult |
| **Performance** | Good for most cases | Can be optimized for specific cases |

**Raft Advantages:**
```python
# Raft: Simple leader-based approach
class RaftCluster:
    def client_request(self, request):
        if self.state == 'leader':
            return self.handle_request(request)
        else:
            return self.redirect_to_leader(request)
```

**Paxos Advantages:**
```python
# Paxos: More flexible, can handle multiple proposers
class PaxosNode:
    def propose(self, value):
        # Phase 1: Prepare
        proposal_id = self.generate_proposal_id()
        promises = self.send_prepare(proposal_id)
        
        # Phase 2: Accept
        if len(promises) > len(self.nodes) // 2:
            return self.send_accept(proposal_id, value)
```

**When to use each:**
- **Raft:** Most distributed systems, easier maintenance
- **Paxos:** High-performance systems, complex requirements

---

## Fault Tolerance

### 9. What are the different types of failures in distributed systems?

**Answer:**

**1. Crash Failures (Fail-Stop):**
```python
# Node stops responding completely
class FailStopNode:
    def __init__(self):
        self.is_alive = True
    
    def crash(self):
        self.is_alive = False
        # Node stops all operations
    
    def process_request(self, request):
        if not self.is_alive:
            # No response - node is dead
            return None
        return self.handle_request(request)
```

**2. Omission Failures:**
```python
# Node fails to send/receive some messages
class OmissionFailureNode:
    def __init__(self, drop_rate=0.1):
        self.drop_rate = drop_rate
    
    def send_message(self, message, destination):
        if random.random() < self.drop_rate:
            # Message dropped
            return False
        return destination.receive(message)
```

**3. Timing Failures:**
```python
# Node responds too slowly
class TimingFailureNode:
    def __init__(self, delay_factor=2.0):
        self.delay_factor = delay_factor
    
    def process_request(self, request):
        # Simulate slow processing
        time.sleep(self.normal_processing_time * self.delay_factor)
        return self.handle_request(request)
```

**4. Byzantine Failures:**
```python
# Node behaves arbitrarily/maliciously
class ByzantineNode:
    def __init__(self, is_malicious=False):
        self.is_malicious = is_malicious
    
    def process_request(self, request):
        if self.is_malicious:
            # Send different responses to different nodes
            return self.generate_malicious_response(request)
        return self.handle_request(request)
```

### 10. How do you implement Byzantine Fault Tolerance?

**Answer:**

**PBFT (Practical Byzantine Fault Tolerance):**

**Requirements:** n ≥ 3f + 1 nodes to tolerate f Byzantine failures

```python
class PBFTNode:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes
        self.view = 0
        self.sequence_number = 0
        self.state = 'normal'
        
    def client_request(self, request):
        if self.is_primary():
            return self.handle_as_primary(request)
        else:
            return self.forward_to_primary(request)
    
    def handle_as_primary(self, request):
        # Phase 1: Pre-prepare
        self.sequence_number += 1
        pre_prepare_msg = {
            'view': self.view,
            'sequence': self.sequence_number,
            'digest': self.hash(request),
            'request': request
        }
        
        self.broadcast_to_backups('pre-prepare', pre_prepare_msg)
        
        # Wait for prepare messages
        prepare_count = self.wait_for_prepares(self.sequence_number)
        
        if prepare_count >= 2 * self.f():  # 2f prepares needed
            # Phase 2: Commit
            commit_msg = {
                'view': self.view,
                'sequence': self.sequence_number,
                'digest': self.hash(request)
            }
            self.broadcast('commit', commit_msg)
            
            # Wait for commit messages
            commit_count = self.wait_for_commits(self.sequence_number)
            
            if commit_count >= 2 * self.f():  # 2f commits needed
                return self.execute_request(request)
        
        return None
    
    def f(self):
        """Maximum number of Byzantine failures tolerated"""
        return (len(self.nodes) - 1) // 3
```

**Blockchain Consensus (Proof of Work):**
```python
class BlockchainNode:
    def __init__(self):
        self.blockchain = [self.genesis_block()]
        self.difficulty = 4  # Number of leading zeros required
    
    def mine_block(self, transactions):
        previous_hash = self.blockchain[-1]['hash']
        nonce = 0
        
        while True:
            block = {
                'transactions': transactions,
                'previous_hash': previous_hash,
                'nonce': nonce,
                'timestamp': time.time()
            }
            
            block_hash = self.calculate_hash(block)
            
            if block_hash.startswith('0' * self.difficulty):
                block['hash'] = block_hash
                return block
            
            nonce += 1
    
    def validate_chain(self, chain):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i-1]
            
            # Validate hash
            if current_block['hash'] != self.calculate_hash(current_block):
                return False
            
            # Validate link to previous block
            if current_block['previous_hash'] != previous_block['hash']:
                return False
        
        return True
```

---

## Replication Strategies

### 11. Compare different replication strategies and their trade-offs.

**Answer:**

**1. Master-Slave Replication:**
```python
class MasterSlaveReplication:
    def __init__(self):
        self.master = MasterNode()
        self.slaves = [SlaveNode() for _ in range(3)]
    
    def write(self, key, value):
        # All writes go to master
        result = self.master.write(key, value)
        
        # Asynchronously replicate to slaves
        for slave in self.slaves:
            asyncio.create_task(slave.replicate(key, value))
        
        return result
    
    def read(self, key):
        # Reads can go to any slave (eventual consistency)
        slave = random.choice(self.slaves)
        return slave.read(key)
```

**Pros:** Simple, good read scalability
**Cons:** Single point of failure, potential data loss

**2. Master-Master Replication:**
```python
class MasterMasterReplication:
    def __init__(self):
        self.masters = [MasterNode(i) for i in range(2)]
    
    def write(self, key, value):
        # Write to local master
        master = self.get_local_master()
        result = master.write(key, value)
        
        # Replicate to other masters
        for other_master in self.masters:
            if other_master != master:
                other_master.replicate(key, value, source=master.id)
        
        return result
    
    def resolve_conflicts(self, key):
        # Last-writer-wins strategy
        versions = [master.get_version(key) for master in self.masters]
        latest_version = max(versions, key=lambda v: v.timestamp)
        
        # Propagate winning version
        for master in self.masters:
            master.update(key, latest_version.value)
```

**Pros:** No single point of failure, write scalability
**Cons:** Conflict resolution complexity

**3. Quorum-Based Replication:**
```python
class QuorumReplication:
    def __init__(self, nodes, read_quorum, write_quorum):
        self.nodes = nodes
        self.R = read_quorum  # Read quorum size
        self.W = write_quorum  # Write quorum size
        self.N = len(nodes)   # Total replicas
    
    def write(self, key, value):
        # Write to W nodes
        successful_writes = 0
        for node in random.sample(self.nodes, self.W):
            if node.write(key, value):
                successful_writes += 1
        
        return successful_writes >= self.W
    
    def read(self, key):
        # Read from R nodes
        responses = []
        for node in random.sample(self.nodes, self.R):
            response = node.read(key)
            if response:
                responses.append(response)
        
        if len(responses) >= self.R:
            # Return most recent version
            return max(responses, key=lambda r: r.timestamp)
        
        return None
```

**Consistency Guarantee:** R + W > N ensures strong consistency

### 12. How do you handle split-brain scenarios?

**Answer:**

**Split-brain:** Network partition causes multiple nodes to believe they are the leader/master.

**Prevention Strategies:**

**1. Quorum-Based Leadership:**
```python
class QuorumLeader:
    def __init__(self, node_id, cluster_size):
        self.node_id = node_id
        self.cluster_size = cluster_size
        self.quorum_size = (cluster_size // 2) + 1
    
    def attempt_leadership(self):
        votes = self.request_votes_from_peers()
        
        if len(votes) >= self.quorum_size:
            self.become_leader()
            return True
        else:
            self.remain_follower()
            return False
    
    def can_serve_requests(self):
        # Only serve if can communicate with majority
        reachable_nodes = self.count_reachable_nodes()
        return reachable_nodes >= self.quorum_size
```

**2. Witness/Arbitrator Nodes:**
```python
class WitnessNode:
    def __init__(self):
        self.current_leader = None
        self.leader_lease_expiry = None
    
    def grant_leadership(self, node_id, lease_duration):
        current_time = time.time()
        
        if (self.current_leader is None or 
            current_time > self.leader_lease_expiry):
            
            self.current_leader = node_id
            self.leader_lease_expiry = current_time + lease_duration
            return True
        
        return False
    
    def is_leader_valid(self, node_id):
        return (self.current_leader == node_id and 
                time.time() < self.leader_lease_expiry)
```

**3. Fencing Mechanisms:**
```python
class FencingCoordinator:
    def __init__(self):
        self.generation_number = 0
        self.active_leader = None
    
    def acquire_leadership(self, node_id):
        self.generation_number += 1
        self.active_leader = node_id
        
        # Return fencing token
        return {
            'leader_id': node_id,
            'generation': self.generation_number,
            'timestamp': time.time()
        }
    
    def validate_operation(self, operation, fencing_token):
        # Reject operations from old leaders
        if fencing_token['generation'] < self.generation_number:
            raise StaleLeaderError("Operation from old leader rejected")
        
        return self.execute_operation(operation)
```

---

## Time and Ordering

### 13. Explain logical clocks and their use in distributed systems.

**Answer:**

**Lamport Timestamps:**
```python
class LamportClock:
    def __init__(self):
        self.time = 0
    
    def tick(self):
        """Increment clock for local event"""
        self.time += 1
        return self.time
    
    def send_message(self, message):
        """Include timestamp when sending message"""
        timestamp = self.tick()
        return {
            'content': message,
            'timestamp': timestamp
        }
    
    def receive_message(self, message_with_timestamp):
        """Update clock when receiving message"""
        received_time = message_with_timestamp['timestamp']
        self.time = max(self.time, received_time) + 1
        return message_with_timestamp['content']

# Usage example
node_a = LamportClock()
node_b = LamportClock()

# Node A sends message
msg = node_a.send_message("Hello")  # timestamp: 1

# Node B receives and processes
node_b.receive_message(msg)  # B's time becomes max(0, 1) + 1 = 2
```

**Vector Clocks:**
```python
class VectorClock:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes
        self.clock = {node: 0 for node in nodes}
    
    def tick(self):
        """Increment own component"""
        self.clock[self.node_id] += 1
    
    def send_message(self, message):
        self.tick()
        return {
            'content': message,
            'vector_clock': self.clock.copy()
        }
    
    def receive_message(self, message_with_clock):
        received_clock = message_with_clock['vector_clock']
        
        # Update each component to maximum
        for node in self.nodes:
            self.clock[node] = max(
                self.clock[node], 
                received_clock.get(node, 0)
            )
        
        # Increment own component
        self.tick()
        
        return message_with_clock['content']
    
    def happens_before(self, other_clock):
        """Check if this event happened before other"""
        return (all(self.clock[node] <= other_clock.get(node, 0) 
                   for node in self.nodes) and
                any(self.clock[node] < other_clock.get(node, 0) 
                   for node in self.nodes))
    
    def concurrent_with(self, other_clock):
        """Check if events are concurrent"""
        return (not self.happens_before(other_clock) and
                not other_clock.happens_before(self.clock))
```

### 14. How do you achieve global ordering in distributed systems?

**Answer:**

**1. Total Order Broadcast:**
```python
class TotalOrderBroadcast:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes
        self.sequence_number = 0
        self.pending_messages = {}
        self.delivered_messages = set()
    
    def broadcast(self, message):
        # Use consensus to agree on sequence number
        self.sequence_number += 1
        sequenced_message = {
            'content': message,
            'sequence': self.sequence_number,
            'sender': self.node_id
        }
        
        # Run consensus on this message
        if self.consensus_on_message(sequenced_message):
            self.deliver_message(sequenced_message)
            return True
        return False
    
    def deliver_message(self, message):
        """Deliver messages in sequence number order"""
        seq = message['sequence']
        
        if seq not in self.delivered_messages:
            self.pending_messages[seq] = message
            
            # Deliver all consecutive messages
            while self.next_sequence in self.pending_messages:
                msg = self.pending_messages.pop(self.next_sequence)
                self.application_deliver(msg)
                self.delivered_messages.add(self.next_sequence)
                self.next_sequence += 1
```

**2. Hybrid Logical Clocks (HLC):**
```python
class HybridLogicalClock:
    def __init__(self):
        self.logical_time = 0
        self.physical_time = 0
    
    def now(self):
        """Get current HLC timestamp"""
        current_physical = int(time.time() * 1000)  # milliseconds
        
        if current_physical > self.physical_time:
            self.physical_time = current_physical
            self.logical_time = 0
        else:
            self.logical_time += 1
        
        return (self.physical_time, self.logical_time)
    
    def update(self, remote_physical, remote_logical):
        """Update clock based on remote timestamp"""
        current_physical = int(time.time() * 1000)
        
        self.physical_time = max(
            current_physical,
            self.physical_time,
            remote_physical
        )
        
        if self.physical_time == remote_physical:
            self.logical_time = max(self.logical_time, remote_logical) + 1
        elif self.physical_time == current_physical:
            self.logical_time += 1
        else:
            self.logical_time = 0
        
        return (self.physical_time, self.logical_time)
```

---

## Distributed Transactions

### 15. Explain the Two-Phase Commit (2PC) protocol and its limitations.

**Answer:**

**Two-Phase Commit Implementation:**
```python
class TwoPhaseCommitCoordinator:
    def __init__(self, participants):
        self.participants = participants
        self.transaction_log = []
    
    def execute_transaction(self, transaction):
        transaction_id = self.generate_transaction_id()
        
        try:
            # Phase 1: Prepare
            if not self.prepare_phase(transaction_id, transaction):
                return self.abort_transaction(transaction_id)
            
            # Phase 2: Commit
            return self.commit_phase(transaction_id)
            
        except Exception as e:
            return self.abort_transaction(transaction_id)
    
    def prepare_phase(self, transaction_id, transaction):
        """Phase 1: Ask all participants to prepare"""
        self.log_event(f"PREPARE {transaction_id}")
        
        votes = []
        for participant in self.participants:
            try:
                vote = participant.prepare(transaction_id, transaction)
                votes.append(vote)
                
                if vote != "YES":
                    return False
                    
            except Exception:
                return False
        
        # All participants voted YES
        self.log_event(f"ALL_PREPARED {transaction_id}")
        return True
    
    def commit_phase(self, transaction_id):
        """Phase 2: Tell all participants to commit"""
        self.log_event(f"COMMIT {transaction_id}")
        
        for participant in self.participants:
            try:
                participant.commit(transaction_id)
            except Exception:
                # Participant must retry commit
                self.handle_commit_failure(participant, transaction_id)
        
        self.log_event(f"COMMITTED {transaction_id}")
        return True
    
    def abort_transaction(self, transaction_id):
        """Tell all participants to abort"""
        self.log_event(f"ABORT {transaction_id}")
        
        for participant in self.participants:
            try:
                participant.abort(transaction_id)
            except Exception:
                pass  # Abort is idempotent
        
        return False

class TwoPhaseCommitParticipant:
    def __init__(self, participant_id):
        self.participant_id = participant_id
        self.prepared_transactions = {}
        self.transaction_log = []
    
    def prepare(self, transaction_id, transaction):
        """Phase 1: Prepare to commit"""
        try:
            # Check if transaction can be committed
            if self.can_commit(transaction):
                # Lock resources and prepare
                self.lock_resources(transaction)
                self.prepared_transactions[transaction_id] = transaction
                self.log_event(f"PREPARED {transaction_id}")
                return "YES"
            else:
                return "NO"
                
        except Exception:
            return "NO"
    
    def commit(self, transaction_id):
        """Phase 2: Actually commit the transaction"""
        if transaction_id in self.prepared_transactions:
            transaction = self.prepared_transactions[transaction_id]
            self.execute_transaction(transaction)
            self.release_locks(transaction)
            del self.prepared_transactions[transaction_id]
            self.log_event(f"COMMITTED {transaction_id}")
    
    def abort(self, transaction_id):
        """Abort the transaction"""
        if transaction_id in self.prepared_transactions:
            transaction = self.prepared_transactions[transaction_id]
            self.release_locks(transaction)
            del self.prepared_transactions[transaction_id]
            self.log_event(f"ABORTED {transaction_id}")
```

**Limitations of 2PC:**

1. **Blocking Protocol:** Participants block if coordinator fails
2. **Single Point of Failure:** Coordinator failure stops progress
3. **Network Partitions:** Cannot distinguish slow from failed nodes
4. **Performance:** High latency due to multiple round trips

### 16. How do you implement distributed transactions without 2PC?

**Answer:**

**1. Saga Pattern:**
```python
class SagaOrchestrator:
    def __init__(self):
        self.saga_log = []
    
    def execute_saga(self, saga_definition):
        """Execute saga with compensation"""
        completed_steps = []
        
        try:
            for step in saga_definition.steps:
                result = self.execute_step(step)
                completed_steps.append((step, result))
                self.saga_log.append(f"COMPLETED: {step.name}")
            
            return True
            
        except Exception as e:
            # Compensate in reverse order
            self.compensate_saga(completed_steps)
            return False
    
    def compensate_saga(self, completed_steps):
        """Execute compensation actions in reverse order"""
        for step, result in reversed(completed_steps):
            try:
                step.compensate(result)
                self.saga_log.append(f"COMPENSATED: {step.name}")
            except Exception:
                # Log compensation failure
                self.saga_log.append(f"COMPENSATION_FAILED: {step.name}")

# Example: E-commerce order saga
class OrderSaga:
    def __init__(self):
        self.steps = [
            CreateOrderStep(),
            ProcessPaymentStep(),
            ReserveInventoryStep(),
            ShipOrderStep()
        ]

class ProcessPaymentStep:
    def execute(self, order):
        # Charge customer
        payment_result = payment_service.charge(
            order.customer_id, 
            order.total_amount
        )
        return payment_result
    
    def compensate(self, payment_result):
        # Refund customer
        payment_service.refund(payment_result.transaction_id)
```

**2. Event Sourcing with Eventual Consistency:**
```python
class EventSourcingTransaction:
    def __init__(self, event_store):
        self.event_store = event_store
    
    def transfer_money(self, from_account, to_account, amount):
        # Generate events instead of direct updates
        events = [
            AccountDebitedEvent(from_account, amount),
            AccountCreditedEvent(to_account, amount)
        ]
        
        # Store events atomically
        self.event_store.append_events(events)
        
        # Events will be processed asynchronously
        return True

class EventProcessor:
    def __init__(self):
        self.event_handlers = {
            'AccountDebited': self.handle_account_debited,
            'AccountCredited': self.handle_account_credited
        }
    
    def process_events(self):
        for event in self.event_store.get_unprocessed_events():
            handler = self.event_handlers.get(event.type)
            if handler:
                try:
                    handler(event)
                    self.mark_processed(event)
                except Exception:
                    self.schedule_retry(event)
```

**3. TCC (Try-Confirm-Cancel) Pattern:**
```python
class TCCTransaction:
    def __init__(self):
        self.participants = []
    
    def execute_tcc_transaction(self):
        # Phase 1: Try - Reserve resources
        try_results = []
        
        for participant in self.participants:
            try_result = participant.try_operation()
            if not try_result.success:
                # Cancel all previous tries
                self.cancel_all(try_results)
                return False
            try_results.append(try_result)
        
        # Phase 2: Confirm - Make changes permanent
        try:
            for participant, try_result in zip(self.participants, try_results):
                participant.confirm_operation(try_result.reservation_id)
            return True
            
        except Exception:
            # Phase 3: Cancel - Rollback changes
            self.cancel_all(try_results)
            return False
    
    def cancel_all(self, try_results):
        for participant, try_result in zip(self.participants, try_results):
            participant.cancel_operation(try_result.reservation_id)

class BankAccountTCC:
    def __init__(self, account_id):
        self.account_id = account_id
        self.reservations = {}
    
    def try_debit(self, amount):
        """Try to reserve amount for debit"""
        if self.get_available_balance() >= amount:
            reservation_id = self.generate_reservation_id()
            self.reservations[reservation_id] = amount
            return TryResult(True, reservation_id)
        return TryResult(False, None)
    
    def confirm_debit(self, reservation_id):
        """Confirm the debit operation"""
        if reservation_id in self.reservations:
            amount = self.reservations[reservation_id]
            self.debit_account(amount)
            del self.reservations[reservation_id]
    
    def cancel_debit(self, reservation_id):
        """Cancel the debit operation"""
        if reservation_id in self.reservations:
            del self.reservations[reservation_id]
```

---

This comprehensive interview questions file covers all major distributed systems concepts including detailed CAP theorem coverage, consensus algorithms, fault tolerance, replication strategies, and distributed transactions. Each answer includes practical code examples and real-world applications relevant to data engineering scenarios.