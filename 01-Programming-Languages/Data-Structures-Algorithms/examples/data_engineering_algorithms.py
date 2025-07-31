"""
Data Engineering Algorithms Implementation

This module demonstrates practical implementations of algorithms
commonly used in data engineering scenarios.
"""

import heapq
import bisect
from collections import defaultdict, deque
from typing import List, Dict, Any, Optional, Iterator
import hashlib
import time


# ============================================================================
# STREAMING ALGORITHMS
# ============================================================================

class CountMinSketch:
    """Space-efficient frequency estimation for streaming data."""
    
    def __init__(self, width: int = 1000, depth: int = 5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
        self.hash_functions = [
            lambda x, i=i: hash(f"{x}_{i}") % width 
            for i in range(depth)
        ]
    
    def add(self, item: str, count: int = 1):
        """Add item to sketch."""
        for i in range(self.depth):
            j = self.hash_functions[i](item)
            self.table[i][j] += count
    
    def estimate(self, item: str) -> int:
        """Estimate frequency of item."""
        return min(
            self.table[i][self.hash_functions[i](item)] 
            for i in range(self.depth)
        )


class HyperLogLog:
    """Cardinality estimation for large datasets."""
    
    def __init__(self, precision: int = 10):
        self.precision = precision
        self.m = 1 << precision  # 2^precision
        self.buckets = [0] * self.m
        self.alpha = self._get_alpha()
    
    def _get_alpha(self) -> float:
        """Get alpha constant for bias correction."""
        if self.m >= 128:
            return 0.7213 / (1 + 1.079 / self.m)
        elif self.m >= 64:
            return 0.709
        elif self.m >= 32:
            return 0.697
        else:
            return 0.673
    
    def add(self, item: str):
        """Add item to HyperLogLog."""
        # Hash the item
        hash_value = int(hashlib.md5(item.encode()).hexdigest(), 16)
        
        # Get bucket index (first p bits)
        bucket = hash_value & (self.m - 1)
        
        # Count leading zeros in remaining bits
        w = hash_value >> self.precision
        leading_zeros = self._count_leading_zeros(w) + 1
        
        # Update bucket with maximum leading zeros seen
        self.buckets[bucket] = max(self.buckets[bucket], leading_zeros)
    
    def _count_leading_zeros(self, w: int) -> int:
        """Count leading zeros in binary representation."""
        if w == 0:
            return 32
        
        count = 0
        for i in range(31, -1, -1):
            if w & (1 << i):
                break
            count += 1
        return count
    
    def cardinality(self) -> int:
        """Estimate cardinality."""
        raw_estimate = self.alpha * (self.m ** 2) / sum(2 ** (-x) for x in self.buckets)
        
        # Apply small range correction
        if raw_estimate <= 2.5 * self.m:
            zeros = self.buckets.count(0)
            if zeros != 0:
                return int(self.m * math.log(self.m / zeros))
        
        return int(raw_estimate)


class ReservoirSampling:
    """Uniform random sampling from data streams."""
    
    def __init__(self, sample_size: int):
        self.sample_size = sample_size
        self.reservoir = []
        self.count = 0
    
    def add(self, item: Any):
        """Add item to reservoir sample."""
        self.count += 1
        
        if len(self.reservoir) < self.sample_size:
            self.reservoir.append(item)
        else:
            # Replace random item with probability k/n
            import random
            j = random.randint(0, self.count - 1)
            if j < self.sample_size:
                self.reservoir[j] = item
    
    def get_sample(self) -> List[Any]:
        """Get current sample."""
        return self.reservoir.copy()


# ============================================================================
# DISTRIBUTED ALGORITHMS
# ============================================================================

class ConsistentHashing:
    """Consistent hashing for distributed systems."""
    
    def __init__(self, replicas: int = 150):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []
    
    def _hash(self, key: str) -> int:
        """Hash function for ring positions."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node: str):
        """Add node to hash ring."""
        for i in range(self.replicas):
            virtual_key = self._hash(f"{node}:{i}")
            self.ring[virtual_key] = node
            bisect.insort(self.sorted_keys, virtual_key)
    
    def remove_node(self, node: str):
        """Remove node from hash ring."""
        for i in range(self.replicas):
            virtual_key = self._hash(f"{node}:{i}")
            if virtual_key in self.ring:
                del self.ring[virtual_key]
                self.sorted_keys.remove(virtual_key)
    
    def get_node(self, key: str) -> Optional[str]:
        """Get node responsible for key."""
        if not self.ring:
            return None
        
        hash_key = self._hash(key)
        idx = bisect.bisect_right(self.sorted_keys, hash_key)
        
        if idx == len(self.sorted_keys):
            idx = 0
        
        return self.ring[self.sorted_keys[idx]]


class DistributedLock:
    """Simple distributed lock implementation."""
    
    def __init__(self, lock_timeout: int = 30):
        self.locks = {}
        self.lock_timeout = lock_timeout
    
    def acquire_lock(self, resource: str, client_id: str) -> bool:
        """Acquire lock for resource."""
        current_time = time.time()
        
        # Check if lock exists and is not expired
        if resource in self.locks:
            lock_time, lock_client = self.locks[resource]
            if current_time - lock_time < self.lock_timeout:
                return lock_client == client_id
        
        # Acquire new lock
        self.locks[resource] = (current_time, client_id)
        return True
    
    def release_lock(self, resource: str, client_id: str) -> bool:
        """Release lock for resource."""
        if resource in self.locks:
            _, lock_client = self.locks[resource]
            if lock_client == client_id:
                del self.locks[resource]
                return True
        return False


# ============================================================================
# GRAPH ALGORITHMS FOR DATA LINEAGE
# ============================================================================

class DataLineageGraph:
    """Graph for tracking data lineage and dependencies."""
    
    def __init__(self):
        self.graph = defaultdict(list)  # adjacency list
        self.reverse_graph = defaultdict(list)  # for upstream dependencies
        self.node_metadata = {}
    
    def add_dependency(self, source: str, target: str, metadata: Dict = None):
        """Add dependency: target depends on source."""
        self.graph[source].append(target)
        self.reverse_graph[target].append(source)
        
        if metadata:
            self.node_metadata[f"{source}->{target}"] = metadata
    
    def get_downstream_dependencies(self, node: str) -> List[str]:
        """Get all nodes that depend on this node."""
        visited = set()
        result = []
        
        def dfs(current):
            if current in visited:
                return
            visited.add(current)
            
            for neighbor in self.graph[current]:
                result.append(neighbor)
                dfs(neighbor)
        
        dfs(node)
        return result
    
    def get_upstream_dependencies(self, node: str) -> List[str]:
        """Get all nodes this node depends on."""
        visited = set()
        result = []
        
        def dfs(current):
            if current in visited:
                return
            visited.add(current)
            
            for neighbor in self.reverse_graph[current]:
                result.append(neighbor)
                dfs(neighbor)
        
        dfs(node)
        return result
    
    def topological_sort(self) -> List[str]:
        """Get topological ordering for execution."""
        in_degree = defaultdict(int)
        
        # Calculate in-degrees
        for node in self.graph:
            for neighbor in self.graph[node]:
                in_degree[neighbor] += 1
        
        # Find nodes with no incoming edges
        queue = deque([node for node in self.graph if in_degree[node] == 0])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            
            for neighbor in self.graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result
    
    def detect_cycles(self) -> List[List[str]]:
        """Detect cycles in dependency graph."""
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node, path):
            if node in rec_stack:
                # Found cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.graph[node]:
                dfs(neighbor, path)
            
            path.pop()
            rec_stack.remove(node)
        
        for node in self.graph:
            if node not in visited:
                dfs(node, [])
        
        return cycles


# ============================================================================
# TIME SERIES ALGORITHMS
# ============================================================================

class TimeSeriesIndex:
    """Efficient time series data indexing."""
    
    def __init__(self):
        self.data = []  # (timestamp, value) pairs
        self.timestamps = []  # sorted timestamps for binary search
    
    def insert(self, timestamp: int, value: Any):
        """Insert time series data point."""
        idx = bisect.bisect_left(self.timestamps, timestamp)
        
        if idx < len(self.timestamps) and self.timestamps[idx] == timestamp:
            # Update existing point
            self.data[idx] = (timestamp, value)
        else:
            # Insert new point
            self.timestamps.insert(idx, timestamp)
            self.data.insert(idx, (timestamp, value))
    
    def range_query(self, start_time: int, end_time: int) -> List[tuple]:
        """Get data points in time range."""
        start_idx = bisect.bisect_left(self.timestamps, start_time)
        end_idx = bisect.bisect_right(self.timestamps, end_time)
        
        return self.data[start_idx:end_idx]
    
    def nearest_point(self, timestamp: int) -> Optional[tuple]:
        """Find nearest data point to timestamp."""
        if not self.timestamps:
            return None
        
        idx = bisect.bisect_left(self.timestamps, timestamp)
        
        if idx == 0:
            return self.data[0]
        elif idx == len(self.timestamps):
            return self.data[-1]
        else:
            # Choose closer point
            left_diff = timestamp - self.timestamps[idx - 1]
            right_diff = self.timestamps[idx] - timestamp
            
            if left_diff <= right_diff:
                return self.data[idx - 1]
            else:
                return self.data[idx]


class SlidingWindowAggregator:
    """Efficient sliding window aggregations."""
    
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.window = deque()
        self.sum_value = 0
        self.min_deque = deque()  # For min queries
        self.max_deque = deque()  # For max queries
    
    def add(self, value: float, timestamp: int = None):
        """Add value to sliding window."""
        if timestamp is None:
            timestamp = time.time()
        
        # Remove old values outside window
        current_time = timestamp
        while (self.window and 
               current_time - self.window[0][1] >= self.window_size):
            old_value, _ = self.window.popleft()
            self.sum_value -= old_value
            
            # Update min/max deques
            if self.min_deque and self.min_deque[0][1] == _:
                self.min_deque.popleft()
            if self.max_deque and self.max_deque[0][1] == _:
                self.max_deque.popleft()
        
        # Add new value
        self.window.append((value, timestamp))
        self.sum_value += value
        
        # Update min deque
        while self.min_deque and self.min_deque[-1][0] >= value:
            self.min_deque.pop()
        self.min_deque.append((value, timestamp))
        
        # Update max deque
        while self.max_deque and self.max_deque[-1][0] <= value:
            self.max_deque.pop()
        self.max_deque.append((value, timestamp))
    
    def get_sum(self) -> float:
        """Get sum of values in current window."""
        return self.sum_value
    
    def get_average(self) -> float:
        """Get average of values in current window."""
        return self.sum_value / len(self.window) if self.window else 0
    
    def get_min(self) -> Optional[float]:
        """Get minimum value in current window."""
        return self.min_deque[0][0] if self.min_deque else None
    
    def get_max(self) -> Optional[float]:
        """Get maximum value in current window."""
        return self.max_deque[0][0] if self.max_deque else None


# ============================================================================
# EXTERNAL SORTING FOR BIG DATA
# ============================================================================

class ExternalSorter:
    """External sorting for datasets larger than memory."""
    
    def __init__(self, chunk_size: int = 1000000):
        self.chunk_size = chunk_size
        self.temp_files = []
    
    def sort_file(self, input_file: str, output_file: str):
        """Sort large file using external sorting."""
        # Phase 1: Create sorted chunks
        self._create_sorted_chunks(input_file)
        
        # Phase 2: Merge sorted chunks
        self._merge_chunks(output_file)
        
        # Cleanup
        self._cleanup_temp_files()
    
    def _create_sorted_chunks(self, input_file: str):
        """Create sorted chunks from input file."""
        chunk_num = 0
        
        with open(input_file, 'r') as f:
            while True:
                chunk = []
                
                # Read chunk
                for _ in range(self.chunk_size):
                    line = f.readline()
                    if not line:
                        break
                    chunk.append(line.strip())
                
                if not chunk:
                    break
                
                # Sort chunk
                chunk.sort()
                
                # Write to temp file
                temp_file = f"temp_chunk_{chunk_num}.txt"
                self.temp_files.append(temp_file)
                
                with open(temp_file, 'w') as tf:
                    for item in chunk:
                        tf.write(f"{item}\n")
                
                chunk_num += 1
    
    def _merge_chunks(self, output_file: str):
        """Merge sorted chunks using k-way merge."""
        file_handles = []
        heap = []
        
        try:
            # Open all temp files
            for i, temp_file in enumerate(self.temp_files):
                f = open(temp_file, 'r')
                file_handles.append(f)
                
                # Read first line from each file
                line = f.readline().strip()
                if line:
                    heapq.heappush(heap, (line, i))
            
            # Merge using heap
            with open(output_file, 'w') as out_f:
                while heap:
                    value, file_idx = heapq.heappop(heap)
                    out_f.write(f"{value}\n")
                    
                    # Read next line from same file
                    next_line = file_handles[file_idx].readline().strip()
                    if next_line:
                        heapq.heappush(heap, (next_line, file_idx))
        
        finally:
            # Close all file handles
            for f in file_handles:
                f.close()
    
    def _cleanup_temp_files(self):
        """Remove temporary files."""
        import os
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass
        self.temp_files.clear()


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def demonstrate_streaming_algorithms():
    """Demonstrate streaming algorithms."""
    print("=== Streaming Algorithms Demo ===")
    
    # Count-Min Sketch
    cms = CountMinSketch(width=100, depth=5)
    
    # Simulate stream of events
    events = ["user1", "user2", "user1", "user3", "user1", "user2"]
    for event in events:
        cms.add(event)
    
    print(f"Estimated frequency of 'user1': {cms.estimate('user1')}")
    print(f"Estimated frequency of 'user2': {cms.estimate('user2')}")
    
    # HyperLogLog
    hll = HyperLogLog(precision=8)
    
    # Add many unique items
    for i in range(10000):
        hll.add(f"item_{i}")
    
    print(f"Estimated cardinality: {hll.cardinality()}")
    
    # Reservoir Sampling
    reservoir = ReservoirSampling(sample_size=10)
    
    # Stream 1000 items, keep sample of 10
    for i in range(1000):
        reservoir.add(f"item_{i}")
    
    print(f"Sample: {reservoir.get_sample()}")


def demonstrate_distributed_algorithms():
    """Demonstrate distributed algorithms."""
    print("\n=== Distributed Algorithms Demo ===")
    
    # Consistent Hashing
    ch = ConsistentHashing(replicas=3)
    
    # Add nodes
    nodes = ["server1", "server2", "server3"]
    for node in nodes:
        ch.add_node(node)
    
    # Distribute keys
    keys = ["key1", "key2", "key3", "key4", "key5"]
    for key in keys:
        node = ch.get_node(key)
        print(f"Key '{key}' -> Node '{node}'")


def demonstrate_graph_algorithms():
    """Demonstrate graph algorithms for data lineage."""
    print("\n=== Graph Algorithms Demo ===")
    
    # Data Lineage Graph
    lineage = DataLineageGraph()
    
    # Build lineage: raw_data -> processed_data -> aggregated_data -> report
    lineage.add_dependency("raw_data", "processed_data")
    lineage.add_dependency("processed_data", "aggregated_data")
    lineage.add_dependency("aggregated_data", "report")
    lineage.add_dependency("external_data", "report")
    
    print(f"Downstream of 'raw_data': {lineage.get_downstream_dependencies('raw_data')}")
    print(f"Upstream of 'report': {lineage.get_upstream_dependencies('report')}")
    print(f"Execution order: {lineage.topological_sort()}")


if __name__ == "__main__":
    demonstrate_streaming_algorithms()
    demonstrate_distributed_algorithms()
    demonstrate_graph_algorithms()