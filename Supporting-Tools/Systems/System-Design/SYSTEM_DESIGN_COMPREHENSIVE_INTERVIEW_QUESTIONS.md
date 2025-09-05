# System Design - Comprehensive Interview Questions for Data Engineers

## 📋 Table of Contents
1. [Fundamentals](#fundamentals)
2. [Scalability & Performance](#scalability--performance)
3. [Data Storage Systems](#data-storage-systems)
4. [Distributed Systems](#distributed-systems)
5. [Data Pipeline Architecture](#data-pipeline-architecture)
6. [Real-time Systems](#real-time-systems)
7. [Microservices Architecture](#microservices-architecture)
8. [Cloud Architecture](#cloud-architecture)
9. [Monitoring & Observability](#monitoring--observability)
10. [Case Studies](#case-studies)

---

## Fundamentals

### 1. What are the key principles of system design for data engineering?

**Answer:**
System design for data engineering focuses on building scalable, reliable, and maintainable data systems.

**Core Principles:**

**1. Scalability:**
- **Horizontal scaling**: Add more machines
- **Vertical scaling**: Add more power to existing machines
- **Data partitioning**: Distribute data across multiple nodes

**2. Reliability:**
- **Fault tolerance**: System continues operating despite failures
- **Data durability**: Data is not lost
- **Disaster recovery**: Ability to recover from catastrophic failures

**3. Consistency:**
- **ACID properties**: Atomicity, Consistency, Isolation, Durability
- **CAP theorem**: Consistency, Availability, Partition tolerance
- **Eventual consistency**: System will become consistent over time

**4. Performance:**
- **Latency**: Time to process a single request
- **Throughput**: Number of requests processed per unit time
- **Bandwidth**: Amount of data transferred per unit time

```python
# Example: Design principles in action
class DataPipelineDesign:
    def __init__(self):
        self.principles = {
            'scalability': {
                'horizontal': 'Add more processing nodes',
                'partitioning': 'Distribute data by key/time',
                'load_balancing': 'Distribute workload evenly'
            },
            'reliability': {
                'replication': 'Multiple copies of data',
                'checkpointing': 'Save intermediate states',
                'retry_logic': 'Handle transient failures'
            },
            'performance': {
                'caching': 'Store frequently accessed data',
                'indexing': 'Fast data retrieval',
                'compression': 'Reduce storage and transfer costs'
            }
        }
```

### 2. Explain the CAP theorem and its implications for data systems.

**Answer:**
The CAP theorem states that in a distributed system, you can only guarantee two out of three properties:

**CAP Properties:**
- **Consistency (C)**: All nodes see the same data simultaneously
- **Availability (A)**: System remains operational
- **Partition Tolerance (P)**: System continues despite network failures

**Trade-offs:**

**CP Systems (Consistency + Partition Tolerance):**
- Examples: MongoDB, HBase, Redis Cluster
- Sacrifice availability during network partitions
- Use case: Financial systems, inventory management

**AP Systems (Availability + Partition Tolerance):**
- Examples: Cassandra, DynamoDB, CouchDB
- Sacrifice consistency for availability
- Use case: Social media, content delivery

**CA Systems (Consistency + Availability):**
- Examples: Traditional RDBMS (PostgreSQL, MySQL)
- Cannot handle network partitions
- Use case: Single-node or tightly coupled systems

```python
# Example: CAP theorem in practice
class DistributedDataStore:
    def __init__(self, consistency_level='eventual'):
        self.consistency_level = consistency_level
    
    def write_data(self, key, value):
        if self.consistency_level == 'strong':
            # CP system: Wait for all replicas to acknowledge
            return self.write_to_all_replicas(key, value)
        else:
            # AP system: Write to available replicas
            return self.write_to_available_replicas(key, value)
    
    def read_data(self, key):
        if self.consistency_level == 'strong':
            # Read from majority of replicas
            return self.read_from_majority(key)
        else:
            # Read from any available replica
            return self.read_from_any_replica(key)
```

### 3. How do you approach system design interviews?

**Answer:**
System design interviews require a structured approach to solve complex problems.

**Step-by-Step Approach:**

**1. Clarify Requirements (5-10 minutes):**
```
Functional Requirements:
- What features does the system need?
- What are the core use cases?
- Who are the users?

Non-Functional Requirements:
- How many users?
- What's the expected load?
- What's the acceptable latency?
- What's the availability requirement?
```

**2. Estimate Scale (5 minutes):**
```
Users: 100M daily active users
Reads: 1B reads/day = 12K reads/second
Writes: 100M writes/day = 1.2K writes/second
Storage: 1TB new data/day = 365TB/year
Bandwidth: 1GB/second peak
```

**3. High-Level Design (10-15 minutes):**
```
Client → Load Balancer → API Gateway → Services → Database
                                    ↓
                              Message Queue → Workers
```

**4. Detailed Design (15-20 minutes):**
- Database schema
- API design
- Caching strategy
- Data flow

**5. Scale the Design (10-15 minutes):**
- Identify bottlenecks
- Add caching layers
- Database sharding
- CDN for static content

**6. Address Edge Cases (5-10 minutes):**
- Failure scenarios
- Data consistency
- Security considerations

---

## Scalability & Performance

### 4. How do you design a system to handle 1 million requests per second?

**Answer:**
Handling 1M RPS requires careful architecture design across multiple layers.

**Architecture Overview:**
```
Internet → CDN → Load Balancer → API Gateway → Microservices → Cache → Database
```

**1. Load Balancing:**
```python
# Multiple layers of load balancing
class LoadBalancingStrategy:
    def __init__(self):
        self.strategies = {
            'dns_load_balancing': 'Route traffic to different data centers',
            'l4_load_balancing': 'TCP/UDP level routing',
            'l7_load_balancing': 'HTTP level routing with content awareness',
            'service_mesh': 'Microservice-level load balancing'
        }
    
    def calculate_capacity(self):
        # Each server handles 1K RPS
        servers_needed = 1_000_000 / 1_000  # 1000 servers
        
        # With load balancer overhead (20%)
        total_servers = servers_needed * 1.2  # 1200 servers
        
        return {
            'application_servers': 1200,
            'load_balancers': 10,  # Each handles 100K RPS
            'data_centers': 3      # Geographic distribution
        }
```

**2. Caching Strategy:**
```python
class CachingArchitecture:
    def __init__(self):
        self.layers = {
            'cdn': 'Static content, 90% cache hit rate',
            'reverse_proxy': 'API responses, 70% cache hit rate',
            'application_cache': 'Database queries, 80% cache hit rate',
            'database_cache': 'Query results, 60% cache hit rate'
        }
    
    def calculate_cache_reduction(self):
        original_rps = 1_000_000
        
        # CDN reduces load by 90%
        after_cdn = original_rps * 0.1  # 100K RPS
        
        # Reverse proxy reduces by 70%
        after_proxy = after_cdn * 0.3   # 30K RPS
        
        # Application cache reduces by 80%
        after_app_cache = after_proxy * 0.2  # 6K RPS
        
        return {
            'database_load': after_app_cache,
            'cache_effectiveness': '99.4% reduction'
        }
```

**3. Database Scaling:**
```python
class DatabaseScaling:
    def __init__(self):
        self.strategies = {
            'read_replicas': 'Scale read operations',
            'sharding': 'Distribute data across multiple databases',
            'partitioning': 'Split large tables',
            'caching': 'Reduce database load'
        }
    
    def design_sharding_strategy(self):
        return {
            'user_based_sharding': 'Shard by user_id % num_shards',
            'geographic_sharding': 'Shard by user location',
            'time_based_sharding': 'Shard by timestamp',
            'feature_based_sharding': 'Shard by feature/service'
        }
```

**4. Microservices Architecture:**
```python
class MicroservicesDesign:
    def __init__(self):
        self.services = {
            'user_service': {'rps': 200_000, 'instances': 200},
            'content_service': {'rps': 300_000, 'instances': 300},
            'recommendation_service': {'rps': 150_000, 'instances': 150},
            'analytics_service': {'rps': 100_000, 'instances': 100},
            'notification_service': {'rps': 250_000, 'instances': 250}
        }
    
    def calculate_resources(self):
        total_instances = sum(s['instances'] for s in self.services.values())
        return {
            'total_instances': total_instances,
            'cpu_cores': total_instances * 4,
            'memory_gb': total_instances * 8,
            'estimated_cost': f'${total_instances * 100}/month'
        }
```

### 5. How do you design for high availability (99.99% uptime)?

**Answer:**
Achieving 99.99% uptime (52.56 minutes downtime/year) requires eliminating single points of failure.

**High Availability Architecture:**

**1. Redundancy at Every Layer:**
```python
class HighAvailabilityDesign:
    def __init__(self):
        self.availability_targets = {
            '99.9%': '8.77 hours downtime/year',
            '99.99%': '52.56 minutes downtime/year',
            '99.999%': '5.26 minutes downtime/year'
        }
    
    def design_redundancy(self):
        return {
            'load_balancers': {
                'primary': 'Active load balancer',
                'secondary': 'Standby with health checks',
                'failover_time': '< 30 seconds'
            },
            'application_servers': {
                'min_instances': 3,
                'auto_scaling': 'Scale based on CPU/memory',
                'health_checks': 'Every 30 seconds'
            },
            'databases': {
                'master_slave': 'Read replicas for scaling',
                'master_master': 'Active-active for writes',
                'backup_strategy': 'Point-in-time recovery'
            }
        }
```

**2. Multi-Region Deployment:**
```python
class MultiRegionArchitecture:
    def __init__(self):
        self.regions = {
            'primary': {
                'region': 'us-east-1',
                'traffic_percentage': 60,
                'services': ['all']
            },
            'secondary': {
                'region': 'us-west-2',
                'traffic_percentage': 30,
                'services': ['all']
            },
            'disaster_recovery': {
                'region': 'eu-west-1',
                'traffic_percentage': 10,
                'services': ['critical_only']
            }
        }
    
    def calculate_availability(self):
        # Single region: 99.9%
        # Two regions: 1 - (0.001 * 0.001) = 99.9999%
        single_region_downtime = 0.001
        multi_region_downtime = single_region_downtime ** 2
        availability = (1 - multi_region_downtime) * 100
        
        return f'{availability}% availability'
```

**3. Circuit Breaker Pattern:**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call_service(self, service_function):
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = service_function()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
```

---

## Data Storage Systems

### 6. How do you choose between SQL and NoSQL databases?

**Answer:**
The choice between SQL and NoSQL depends on specific requirements and trade-offs.

**Decision Matrix:**

| Factor | SQL | NoSQL |
|--------|-----|-------|
| **ACID Compliance** | ✅ Strong | ⚠️ Eventual |
| **Schema Flexibility** | ❌ Rigid | ✅ Flexible |
| **Horizontal Scaling** | ⚠️ Limited | ✅ Excellent |
| **Complex Queries** | ✅ SQL | ❌ Limited |
| **Consistency** | ✅ Strong | ⚠️ Eventual |
| **Performance** | ⚠️ Good | ✅ Excellent |

**Use Cases:**

**Choose SQL When:**
```python
class SQLUseCases:
    def __init__(self):
        self.scenarios = {
            'financial_systems': {
                'reason': 'ACID compliance required',
                'example': 'Banking transactions, accounting'
            },
            'complex_analytics': {
                'reason': 'Complex joins and aggregations',
                'example': 'Business intelligence, reporting'
            },
            'structured_data': {
                'reason': 'Well-defined schema',
                'example': 'User profiles, product catalogs'
            },
            'small_to_medium_scale': {
                'reason': 'Vertical scaling sufficient',
                'example': 'Internal tools, small applications'
            }
        }
```

**Choose NoSQL When:**
```python
class NoSQLUseCases:
    def __init__(self):
        self.scenarios = {
            'high_scale': {
                'reason': 'Horizontal scaling required',
                'example': 'Social media, IoT data'
            },
            'flexible_schema': {
                'reason': 'Schema evolution needed',
                'example': 'Content management, user-generated content'
            },
            'high_performance': {
                'reason': 'Low latency requirements',
                'example': 'Real-time recommendations, gaming'
            },
            'unstructured_data': {
                'reason': 'Varied data formats',
                'example': 'Logs, documents, multimedia'
            }
        }
```

**Hybrid Approach:**
```python
class HybridDataArchitecture:
    def __init__(self):
        self.data_stores = {
            'postgresql': {
                'use_case': 'User profiles, transactions',
                'characteristics': 'ACID, complex queries'
            },
            'redis': {
                'use_case': 'Session data, caching',
                'characteristics': 'In-memory, fast access'
            },
            'elasticsearch': {
                'use_case': 'Search, analytics',
                'characteristics': 'Full-text search, aggregations'
            },
            'cassandra': {
                'use_case': 'Time-series data, logs',
                'characteristics': 'High write throughput, scalable'
            },
            's3': {
                'use_case': 'File storage, data lake',
                'characteristics': 'Object storage, unlimited scale'
            }
        }
```

### 7. Design a data storage system for a time-series database.

**Answer:**
Time-series databases are optimized for storing and querying time-stamped data.

**Requirements Analysis:**
```python
class TimeSeriesRequirements:
    def __init__(self):
        self.characteristics = {
            'high_write_throughput': '1M+ writes/second',
            'time_based_queries': 'Range queries, aggregations',
            'data_retention': 'Hot/warm/cold storage tiers',
            'compression': 'Efficient storage of similar data',
            'downsampling': 'Reduce resolution over time'
        }
```

**Architecture Design:**

**1. Data Model:**
```python
class TimeSeriesDataModel:
    def __init__(self):
        self.schema = {
            'timestamp': 'Primary key component',
            'metric_name': 'What is being measured',
            'tags': 'Dimensions for filtering/grouping',
            'value': 'The actual measurement'
        }
    
    def design_partitioning(self):
        return {
            'time_partitioning': {
                'strategy': 'Partition by day/hour',
                'benefit': 'Efficient range queries',
                'retention': 'Drop old partitions'
            },
            'metric_partitioning': {
                'strategy': 'Partition by metric type',
                'benefit': 'Isolate different workloads',
                'scaling': 'Independent scaling per metric'
            }
        }
```

**2. Storage Engine:**
```python
class TimeSeriesStorageEngine:
    def __init__(self):
        self.components = {
            'write_ahead_log': 'Durability for recent writes',
            'memtable': 'In-memory buffer for recent data',
            'sstables': 'Immutable sorted files on disk',
            'compaction': 'Merge and compress old data'
        }
    
    def write_path(self, timestamp, metric, tags, value):
        # 1. Write to WAL for durability
        self.wal.append(timestamp, metric, tags, value)
        
        # 2. Write to memtable
        self.memtable.insert(timestamp, metric, tags, value)
        
        # 3. Flush to SSTable when memtable is full
        if self.memtable.is_full():
            self.flush_to_sstable()
    
    def read_path(self, metric, start_time, end_time):
        # 1. Check memtable first
        recent_data = self.memtable.query(metric, start_time, end_time)
        
        # 2. Query relevant SSTables
        historical_data = self.query_sstables(metric, start_time, end_time)
        
        # 3. Merge and return results
        return self.merge_results(recent_data, historical_data)
```

**3. Compression Strategy:**
```python
class TimeSeriesCompression:
    def __init__(self):
        self.techniques = {
            'delta_encoding': 'Store differences between consecutive values',
            'run_length_encoding': 'Compress repeated values',
            'dictionary_encoding': 'Compress repeated strings/tags',
            'gorilla_compression': 'Facebook\'s algorithm for floating-point values'
        }
    
    def compress_data_points(self, data_points):
        compressed = []
        
        # Delta encoding for timestamps
        prev_timestamp = 0
        for point in data_points:
            delta = point.timestamp - prev_timestamp
            compressed.append({
                'timestamp_delta': delta,
                'value': point.value,
                'tags': point.tags
            })
            prev_timestamp = point.timestamp
        
        return compressed
```

**4. Query Optimization:**
```python
class TimeSeriesQueryEngine:
    def __init__(self):
        self.optimizations = {
            'time_range_pruning': 'Skip irrelevant time partitions',
            'tag_indexing': 'Fast filtering by tags',
            'pre_aggregation': 'Store common aggregations',
            'downsampling': 'Reduce data resolution for old data'
        }
    
    def execute_query(self, query):
        # 1. Parse query and identify time range
        time_range = self.parse_time_range(query)
        
        # 2. Identify relevant partitions
        partitions = self.get_relevant_partitions(time_range)
        
        # 3. Apply tag filters
        filtered_data = self.apply_tag_filters(partitions, query.tags)
        
        # 4. Execute aggregation
        return self.aggregate_data(filtered_data, query.aggregation)
```

---

## Distributed Systems

### 8. How do you design a distributed data processing system?

**Answer:**
Distributed data processing systems handle large-scale data across multiple machines.

**Architecture Components:**

**1. Master-Worker Architecture:**
```python
class DistributedProcessingSystem:
    def __init__(self):
        self.components = {
            'master_node': {
                'responsibilities': [
                    'Job scheduling',
                    'Resource allocation',
                    'Failure detection',
                    'Metadata management'
                ]
            },
            'worker_nodes': {
                'responsibilities': [
                    'Task execution',
                    'Data processing',
                    'Status reporting',
                    'Local storage'
                ]
            },
            'coordination_service': {
                'technology': 'ZooKeeper/etcd',
                'purpose': 'Distributed coordination'
            }
        }
```

**2. Data Partitioning Strategy:**
```python
class DataPartitioning:
    def __init__(self):
        self.strategies = {
            'hash_partitioning': {
                'method': 'hash(key) % num_partitions',
                'pros': 'Even distribution',
                'cons': 'No range queries'
            },
            'range_partitioning': {
                'method': 'Partition by key ranges',
                'pros': 'Range queries efficient',
                'cons': 'Potential hotspots'
            },
            'round_robin': {
                'method': 'Distribute records sequentially',
                'pros': 'Simple, even distribution',
                'cons': 'No data locality'
            }
        }
    
    def calculate_partitions(self, data_size_gb, partition_size_gb=1):
        num_partitions = math.ceil(data_size_gb / partition_size_gb)
        return {
            'total_partitions': num_partitions,
            'partition_size': f'{partition_size_gb}GB',
            'parallelism': num_partitions
        }
```

**3. Fault Tolerance:**
```python
class FaultToleranceStrategy:
    def __init__(self):
        self.mechanisms = {
            'replication': {
                'data_replication': 'Multiple copies of data',
                'computation_replication': 'Redundant task execution'
            },
            'checkpointing': {
                'periodic_snapshots': 'Save intermediate state',
                'recovery_points': 'Restart from last checkpoint'
            },
            'lineage_tracking': {
                'dependency_graph': 'Track data dependencies',
                'recomputation': 'Recreate lost data'
            }
        }
    
    def handle_node_failure(self, failed_node):
        # 1. Detect failure
        if not self.heartbeat_received(failed_node):
            # 2. Reassign tasks
            tasks = self.get_tasks_on_node(failed_node)
            for task in tasks:
                available_node = self.find_available_node()
                self.reassign_task(task, available_node)
            
            # 3. Recover data
            self.recover_data_from_replicas(failed_node)
```

**4. Load Balancing:**
```python
class LoadBalancer:
    def __init__(self):
        self.strategies = {
            'round_robin': 'Distribute tasks evenly',
            'least_connections': 'Send to least busy node',
            'weighted_round_robin': 'Consider node capacity',
            'consistent_hashing': 'Minimize data movement'
        }
    
    def distribute_tasks(self, tasks, workers):
        # Consider worker capacity and current load
        task_assignments = {}
        
        for task in tasks:
            # Find best worker based on:
            # 1. Current load
            # 2. Data locality
            # 3. Resource requirements
            best_worker = self.find_optimal_worker(task, workers)
            task_assignments[task.id] = best_worker
        
        return task_assignments
```

### 9. Explain consensus algorithms and their use in distributed systems.

**Answer:**
Consensus algorithms ensure distributed nodes agree on a single value or state.

**Common Consensus Algorithms:**

**1. Raft Algorithm:**
```python
class RaftConsensus:
    def __init__(self, node_id, cluster_nodes):
        self.node_id = node_id
        self.cluster_nodes = cluster_nodes
        self.state = 'FOLLOWER'  # FOLLOWER, CANDIDATE, LEADER
        self.current_term = 0
        self.voted_for = None
        self.log = []
    
    def start_election(self):
        """Start leader election process"""
        self.state = 'CANDIDATE'
        self.current_term += 1
        self.voted_for = self.node_id
        
        votes_received = 1  # Vote for self
        
        # Request votes from other nodes
        for node in self.cluster_nodes:
            if node != self.node_id:
                vote = self.request_vote(node)
                if vote:
                    votes_received += 1
        
        # Become leader if majority votes received
        if votes_received > len(self.cluster_nodes) // 2:
            self.state = 'LEADER'
            self.send_heartbeats()
    
    def append_entry(self, entry):
        """Append entry to log (leader only)"""
        if self.state != 'LEADER':
            return False
        
        # Add to local log
        self.log.append({
            'term': self.current_term,
            'entry': entry,
            'index': len(self.log)
        })
        
        # Replicate to followers
        success_count = 1  # Leader counts as success
        for node in self.cluster_nodes:
            if node != self.node_id:
                if self.replicate_to_follower(node, entry):
                    success_count += 1
        
        # Commit if majority acknowledges
        if success_count > len(self.cluster_nodes) // 2:
            self.commit_entry(entry)
            return True
        
        return False
```

**2. PBFT (Practical Byzantine Fault Tolerance):**
```python
class PBFTConsensus:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.f = (total_nodes - 1) // 3  # Max Byzantine nodes
        self.view = 0
        self.sequence_number = 0
        self.state = 'NORMAL'
    
    def three_phase_protocol(self, request):
        """PBFT three-phase protocol"""
        
        # Phase 1: Pre-prepare (Primary only)
        if self.is_primary():
            pre_prepare_msg = {
                'view': self.view,
                'sequence': self.sequence_number,
                'request': request,
                'digest': self.hash(request)
            }
            self.broadcast_pre_prepare(pre_prepare_msg)
        
        # Phase 2: Prepare (All nodes)
        prepare_msg = {
            'view': self.view,
            'sequence': self.sequence_number,
            'digest': self.hash(request),
            'node_id': self.node_id
        }
        self.broadcast_prepare(prepare_msg)
        
        # Phase 3: Commit (All nodes)
        if self.received_2f_prepares():
            commit_msg = {
                'view': self.view,
                'sequence': self.sequence_number,
                'digest': self.hash(request),
                'node_id': self.node_id
            }
            self.broadcast_commit(commit_msg)
        
        # Execute request if 2f+1 commits received
        if self.received_2f_commits():
            self.execute_request(request)
```

**Use Cases in Data Systems:**

**1. Distributed Databases:**
```python
class DistributedDatabase:
    def __init__(self):
        self.consensus_use_cases = {
            'leader_election': 'Choose primary replica',
            'configuration_changes': 'Add/remove nodes safely',
            'transaction_commit': 'Ensure ACID properties',
            'schema_changes': 'Coordinate schema updates'
        }
```

**2. Distributed File Systems:**
```python
class DistributedFileSystem:
    def __init__(self):
        self.consensus_applications = {
            'metadata_management': 'Consistent file metadata',
            'block_allocation': 'Coordinate block placement',
            'namespace_operations': 'File/directory operations',
            'failure_recovery': 'Coordinate recovery processes'
        }
```

---

## Data Pipeline Architecture

### 10. Design a real-time data pipeline for processing 1TB of data per day.

**Answer:**
A real-time data pipeline for 1TB/day requires careful architecture for ingestion, processing, and storage.

**Scale Analysis:**
```python
class PipelineScaleAnalysis:
    def __init__(self):
        self.daily_volume = 1024  # GB per day
        self.calculations = self.calculate_requirements()
    
    def calculate_requirements(self):
        return {
            'throughput': {
                'per_second': f'{self.daily_volume * 1024 / 86400:.2f} MB/s',
                'per_minute': f'{self.daily_volume * 1024 / 1440:.2f} MB/min',
                'per_hour': f'{self.daily_volume / 24:.2f} GB/hour'
            },
            'storage': {
                'daily': f'{self.daily_volume} GB',
                'monthly': f'{self.daily_volume * 30} GB',
                'yearly': f'{self.daily_volume * 365} GB'
            },
            'processing_power': {
                'cpu_cores': 100,  # Estimated
                'memory_gb': 500,  # Estimated
                'network_gbps': 10  # Estimated
            }
        }
```

**Architecture Design:**

**1. Data Ingestion Layer:**
```python
class DataIngestionLayer:
    def __init__(self):
        self.components = {
            'kafka_cluster': {
                'brokers': 9,  # 3 per AZ
                'partitions_per_topic': 50,
                'replication_factor': 3,
                'retention': '7 days'
            },
            'schema_registry': {
                'purpose': 'Schema evolution management',
                'technology': 'Confluent Schema Registry'
            },
            'producers': {
                'applications': 'Web apps, mobile apps, IoT devices',
                'batch_size': '16KB',
                'compression': 'snappy'
            }
        }
    
    def design_kafka_topics(self):
        return {
            'user_events': {
                'partitions': 50,
                'throughput': '500 MB/s',
                'use_case': 'User interactions'
            },
            'system_logs': {
                'partitions': 30,
                'throughput': '300 MB/s',
                'use_case': 'Application logs'
            },
            'iot_data': {
                'partitions': 20,
                'throughput': '200 MB/s',
                'use_case': 'Sensor data'
            }
        }
```

**2. Stream Processing Layer:**
```python
class StreamProcessingLayer:
    def __init__(self):
        self.technologies = {
            'apache_flink': {
                'use_case': 'Complex event processing',
                'features': ['Exactly-once processing', 'Low latency'],
                'cluster_size': '20 task managers'
            },
            'apache_kafka_streams': {
                'use_case': 'Simple transformations',
                'features': ['Lightweight', 'Easy deployment'],
                'instances': '50 application instances'
            },
            'apache_spark_streaming': {
                'use_case': 'Micro-batch processing',
                'features': ['Rich APIs', 'ML integration'],
                'cluster_size': '30 executors'
            }
        }
    
    def design_processing_topology(self):
        return {
            'data_validation': {
                'function': 'Validate schema and data quality',
                'parallelism': 20,
                'resources': '2 CPU, 4GB RAM per task'
            },
            'data_enrichment': {
                'function': 'Join with reference data',
                'parallelism': 15,
                'resources': '4 CPU, 8GB RAM per task'
            },
            'aggregation': {
                'function': 'Real-time metrics calculation',
                'parallelism': 10,
                'resources': '2 CPU, 4GB RAM per task'
            },
            'alerting': {
                'function': 'Anomaly detection and alerts',
                'parallelism': 5,
                'resources': '4 CPU, 8GB RAM per task'
            }
        }
```

**3. Storage Layer:**
```python
class StorageLayer:
    def __init__(self):
        self.storage_tiers = {
            'hot_storage': {
                'technology': 'Apache Cassandra',
                'retention': '7 days',
                'use_case': 'Real-time queries',
                'size': '7TB'
            },
            'warm_storage': {
                'technology': 'Apache HBase',
                'retention': '90 days',
                'use_case': 'Analytics queries',
                'size': '90TB'
            },
            'cold_storage': {
                'technology': 'Amazon S3',
                'retention': '7 years',
                'use_case': 'Archival and compliance',
                'size': '2.5PB'
            }
        }
    
    def design_data_lake(self):
        return {
            'raw_zone': {
                'format': 'Avro/JSON',
                'partitioning': 'year/month/day/hour',
                'compression': 'snappy'
            },
            'processed_zone': {
                'format': 'Parquet',
                'partitioning': 'year/month/day',
                'compression': 'gzip'
            },
            'curated_zone': {
                'format': 'Delta Lake',
                'partitioning': 'business_date',
                'features': ['ACID', 'Time travel', 'Schema evolution']
            }
        }
```

**4. Monitoring and Observability:**
```python
class MonitoringLayer:
    def __init__(self):
        self.metrics = {
            'throughput_metrics': [
                'Messages per second',
                'Bytes per second',
                'Processing latency'
            ],
            'quality_metrics': [
                'Data completeness',
                'Schema validation errors',
                'Duplicate records'
            ],
            'system_metrics': [
                'CPU utilization',
                'Memory usage',
                'Disk I/O',
                'Network bandwidth'
            ]
        }
    
    def design_alerting(self):
        return {
            'critical_alerts': {
                'pipeline_down': 'Pipeline stopped processing',
                'data_loss': 'Messages dropped or lost',
                'high_latency': 'Processing latency > 5 minutes'
            },
            'warning_alerts': {
                'high_cpu': 'CPU usage > 80%',
                'queue_backlog': 'Message backlog > 1 hour',
                'schema_errors': 'Schema validation errors > 1%'
            }
        }
```

### 11. How do you handle backpressure in streaming systems?

**Answer:**
Backpressure occurs when downstream systems cannot keep up with upstream data flow.

**Backpressure Strategies:**

**1. Flow Control:**
```python
class FlowControlStrategy:
    def __init__(self):
        self.strategies = {
            'buffering': 'Temporary storage of excess data',
            'dropping': 'Discard oldest or newest data',
            'blocking': 'Slow down upstream producers',
            'load_shedding': 'Selectively drop non-critical data'
        }
    
    def implement_buffering(self, buffer_size=1000):
        class BufferedProcessor:
            def __init__(self, buffer_size):
                self.buffer = queue.Queue(maxsize=buffer_size)
                self.processing_rate = 100  # messages/second
            
            def process_message(self, message):
                try:
                    # Non-blocking put with timeout
                    self.buffer.put(message, timeout=1)
                except queue.Full:
                    # Handle backpressure
                    self.handle_buffer_full(message)
            
            def handle_buffer_full(self, message):
                # Strategy 1: Drop oldest message
                try:
                    self.buffer.get_nowait()
                    self.buffer.put(message)
                except queue.Empty:
                    pass
                
                # Strategy 2: Apply load shedding
                if message.priority < 5:
                    return  # Drop low priority messages
```

**2. Dynamic Scaling:**
```python
class DynamicScaling:
    def __init__(self):
        self.scaling_metrics = {
            'queue_depth': 'Number of pending messages',
            'processing_latency': 'Time to process messages',
            'cpu_utilization': 'Resource usage',
            'throughput': 'Messages processed per second'
        }
    
    def auto_scale_processors(self, current_load):
        if current_load > 0.8:  # 80% capacity
            # Scale up
            new_instances = self.calculate_scale_up(current_load)
            self.add_processing_instances(new_instances)
        elif current_load < 0.3:  # 30% capacity
            # Scale down
            instances_to_remove = self.calculate_scale_down(current_load)
            self.remove_processing_instances(instances_to_remove)
    
    def calculate_scale_up(self, load):
        # Scale up by 50% when load > 80%
        current_instances = self.get_current_instances()
        return max(1, int(current_instances * 0.5))
```

**3. Circuit Breaker Pattern:**
```python
class StreamingCircuitBreaker:
    def __init__(self, failure_threshold=10, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
    
    def process_stream(self, message_stream):
        for message in message_stream:
            if self.state == 'OPEN':
                if self._should_attempt_reset():
                    self.state = 'HALF_OPEN'
                else:
                    # Drop messages when circuit is open
                    self.send_to_dead_letter_queue(message)
                    continue
            
            try:
                self.process_message(message)
                self._on_success()
            except Exception as e:
                self._on_failure()
                self.send_to_dead_letter_queue(message)
```

**4. Kafka-Specific Backpressure:**
```python
class KafkaBackpressureHandler:
    def __init__(self):
        self.consumer_config = {
            'max.poll.records': 100,  # Limit batch size
            'fetch.max.wait.ms': 500,  # Max wait time
            'session.timeout.ms': 30000,  # Session timeout
            'heartbeat.interval.ms': 3000  # Heartbeat interval
        }
    
    def handle_slow_consumer(self):
        strategies = {
            'pause_partitions': self.pause_slow_partitions,
            'increase_parallelism': self.add_consumer_instances,
            'optimize_processing': self.optimize_message_processing,
            'use_async_processing': self.implement_async_processing
        }
        return strategies
    
    def pause_slow_partitions(self, consumer, slow_partitions):
        # Temporarily pause consuming from slow partitions
        consumer.pause(slow_partitions)
        
        # Resume after processing catches up
        time.sleep(10)
        consumer.resume(slow_partitions)
```

---

## Real-time Systems

### 12. Design a real-time recommendation system.

**Answer:**
A real-time recommendation system requires low-latency data processing and serving.

**System Requirements:**
```python
class RecommendationSystemRequirements:
    def __init__(self):
        self.requirements = {
            'latency': '< 100ms response time',
            'throughput': '100K requests/second',
            'users': '10M active users',
            'items': '1M items in catalog',
            'updates': 'Real-time model updates',
            'personalization': 'User-specific recommendations'
        }
```

**Architecture Design:**

**1. Data Collection Layer:**
```python
class DataCollectionLayer:
    def __init__(self):
        self.data_sources = {
            'user_interactions': {
                'events': ['view', 'click', 'purchase', 'rating'],
                'volume': '1M events/hour',
                'latency': 'Real-time'
            },
            'item_catalog': {
                'updates': ['new_items', 'price_changes', 'inventory'],
                'volume': '10K updates/hour',
                'latency': 'Near real-time'
            },
            'user_profiles': {
                'updates': ['preferences', 'demographics'],
                'volume': '100K updates/hour',
                'latency': 'Batch updates'
            }
        }
    
    def design_event_streaming(self):
        return {
            'kafka_topics': {
                'user_events': {
                    'partitions': 100,
                    'key': 'user_id',
                    'schema': {
                        'user_id': 'string',
                        'item_id': 'string',
                        'event_type': 'string',
                        'timestamp': 'long',
                        'context': 'map<string,string>'
                    }
                }
            }
        }
```

**2. Feature Engineering:**
```python
class FeatureEngineering:
    def __init__(self):
        self.feature_types = {
            'user_features': [
                'age_group', 'location', 'purchase_history',
                'browsing_patterns', 'time_preferences'
            ],
            'item_features': [
                'category', 'price_range', 'popularity',
                'ratings', 'seasonal_trends'
            ],
            'interaction_features': [
                'click_through_rate', 'conversion_rate',
                'time_spent', 'sequence_patterns'
            ]
        }
    
    def real_time_feature_computation(self):
        return {
            'streaming_aggregations': {
                'user_session_features': 'Current session behavior',
                'item_popularity': 'Real-time popularity scores',
                'trending_categories': 'Trending item categories'
            },
            'feature_store': {
                'technology': 'Redis/DynamoDB',
                'purpose': 'Low-latency feature serving',
                'ttl': '1 hour for real-time features'
            }
        }
```

**3. Model Serving Architecture:**
```python
class ModelServingArchitecture:
    def __init__(self):
        self.serving_patterns = {
            'online_serving': {
                'technology': 'TensorFlow Serving/MLflow',
                'latency': '< 50ms',
                'use_case': 'Real-time inference'
            },
            'precomputed_recommendations': {
                'technology': 'Redis/Cassandra',
                'latency': '< 10ms',
                'use_case': 'Popular/trending items'
            },
            'hybrid_approach': {
                'strategy': 'Combine precomputed + real-time',
                'fallback': 'Use precomputed if real-time fails'
            }
        }
    
    def design_serving_pipeline(self):
        return {
            'request_flow': [
                '1. Receive user request',
                '2. Fetch user features from feature store',
                '3. Get candidate items (precomputed)',
                '4. Score candidates with ML model',
                '5. Apply business rules and filters',
                '6. Return top-N recommendations'
            ],
            'caching_strategy': {
                'user_cache': 'Cache user features (5 min TTL)',
                'model_cache': 'Cache model predictions (1 min TTL)',
                'result_cache': 'Cache final recommendations (30 sec TTL)'
            }
        }
```

**4. A/B Testing Framework:**
```python
class ABTestingFramework:
    def __init__(self):
        self.experiment_types = {
            'model_comparison': 'Compare different ML models',
            'feature_testing': 'Test new features',
            'algorithm_variants': 'Test recommendation algorithms',
            'ui_changes': 'Test presentation changes'
        }
    
    def implement_experimentation(self):
        return {
            'traffic_splitting': {
                'method': 'Consistent hashing on user_id',
                'variants': {
                    'control': '50% traffic',
                    'treatment_a': '25% traffic',
                    'treatment_b': '25% traffic'
                }
            },
            'metrics_tracking': {
                'primary_metrics': ['click_through_rate', 'conversion_rate'],
                'secondary_metrics': ['engagement_time', 'diversity_score'],
                'guardrail_metrics': ['latency', 'error_rate']
            }
        }
```

**5. Real-time Model Updates:**
```python
class RealTimeModelUpdates:
    def __init__(self):
        self.update_strategies = {
            'online_learning': {
                'method': 'Incremental model updates',
                'frequency': 'Every batch of events',
                'algorithms': ['SGD', 'Online Matrix Factorization']
            },
            'periodic_retraining': {
                'method': 'Full model retraining',
                'frequency': 'Every 4 hours',
                'data_window': 'Last 7 days'
            },
            'ensemble_updates': {
                'method': 'Update ensemble weights',
                'frequency': 'Every hour',
                'based_on': 'Recent performance metrics'
            }
        }
    
    def implement_model_pipeline(self):
        return {
            'training_pipeline': {
                'data_preparation': 'Feature engineering on recent data',
                'model_training': 'Train on distributed cluster',
                'validation': 'A/B test new model',
                'deployment': 'Gradual rollout'
            },
            'monitoring': {
                'model_drift': 'Monitor prediction quality',
                'data_drift': 'Monitor input feature distribution',
                'performance': 'Track business metrics'
            }
        }
```

This comprehensive system design guide covers the essential concepts and practical implementations needed for data engineering system design interviews, with real-world examples and scalable architectures.