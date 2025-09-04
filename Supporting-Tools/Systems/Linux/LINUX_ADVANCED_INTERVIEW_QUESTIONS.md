# Linux Advanced Interview Questions & Answers

## 📋 Table of Contents
1. [System Administration](#system-administration)
2. [Performance Monitoring](#performance-monitoring)
3. [Process Management](#process-management)
4. [File Systems](#file-systems)
5. [Networking](#networking)

---

## System Administration

### 1. How do you manage system resources for data engineering workloads?

**Answer:**
Resource management involves CPU, memory, disk, and network optimization:

**CPU Management:**
```bash
# Check CPU usage and load
top -p $(pgrep -d',' python)
htop
iostat -c 1 5

# Set CPU affinity for data processing
taskset -c 0,1,2,3 python data_pipeline.py
numactl --cpunodebind=0 --membind=0 spark-submit job.py

# Control CPU limits with cgroups
echo "50000" > /sys/fs/cgroup/cpu/data-processing/cpu.cfs_quota_us
echo $$ > /sys/fs/cgroup/cpu/data-processing/cgroup.procs
```

**Memory Management:**
```bash
# Monitor memory usage
free -h
vmstat 1 5
cat /proc/meminfo

# Configure swap for large datasets
swapon -s
fallocate -l 32G /swapfile
mkswap /swapfile
swapon /swapfile

# Memory limits with systemd
systemctl edit data-pipeline.service
# Add:
[Service]
MemoryLimit=16G
MemoryAccounting=yes
```

### 2. How do you configure Linux for optimal data processing performance?

**Answer:**
System tuning for data-intensive workloads:

**Kernel Parameters:**
```bash
# /etc/sysctl.conf optimizations
vm.swappiness=10                    # Reduce swap usage
vm.dirty_ratio=15                   # Dirty page cache ratio
vm.dirty_background_ratio=5         # Background writeback threshold
net.core.rmem_max=134217728        # Increase network buffer
net.core.wmem_max=134217728
fs.file-max=2097152                # Increase file descriptor limit

# Apply changes
sysctl -p
```

**I/O Scheduler:**
```bash
# Check current scheduler
cat /sys/block/sda/queue/scheduler

# Set deadline scheduler for SSDs
echo deadline > /sys/block/sda/queue/scheduler

# Optimize for data processing
echo 4096 > /sys/block/sda/queue/read_ahead_kb
echo mq-deadline > /sys/block/sda/queue/scheduler
```

**File System Tuning:**
```bash
# Mount options for data processing
mount -o noatime,nodiratime,nobarrier /dev/sdb1 /data

# XFS tuning for large files
mkfs.xfs -f -d agcount=32 /dev/sdc1
mount -o noatime,largeio,inode64,swalloc /dev/sdc1 /data
```

---

## Performance Monitoring

### 3. How do you diagnose performance bottlenecks in data processing systems?

**Answer:**
Systematic approach to identify and resolve bottlenecks:

**CPU Bottlenecks:**
```bash
# Identify CPU-bound processes
top -o %CPU
ps aux --sort=-%cpu | head -10

# Profile CPU usage
perf top -p $(pgrep python)
perf record -g python data_pipeline.py
perf report

# Check CPU frequency scaling
cpupower frequency-info
cat /proc/cpuinfo | grep MHz
```

**Memory Bottlenecks:**
```bash
# Memory usage analysis
ps aux --sort=-%mem | head -10
pmap -x $(pgrep python)
valgrind --tool=massif python script.py

# Check for memory leaks
cat /proc/$(pgrep python)/status | grep Vm
watch -n 1 'cat /proc/meminfo | grep -E "MemFree|Cached|Buffers"'
```

**I/O Bottlenecks:**
```bash
# Disk I/O monitoring
iostat -x 1 5
iotop -o
lsof +D /data

# Network I/O monitoring
iftop -i eth0
netstat -i
ss -tuln
```

### 4. How do you use system monitoring tools for data pipeline observability?

**Answer:**
Comprehensive monitoring setup for data pipelines:

**System Metrics Collection:**
```bash
# Install and configure collectd
apt-get install collectd
# /etc/collectd/collectd.conf
LoadPlugin cpu
LoadPlugin memory
LoadPlugin disk
LoadPlugin network
LoadPlugin processes

<Plugin processes>
    ProcessMatch "spark" ".*spark.*"
    ProcessMatch "kafka" ".*kafka.*"
    ProcessMatch "python" ".*python.*"
</Plugin>
```

**Custom Monitoring Scripts:**
```bash
#!/bin/bash
# data_pipeline_monitor.sh

# Check pipeline health
check_pipeline_health() {
    local pipeline_name=$1
    local pid=$(pgrep -f $pipeline_name)
    
    if [ -z "$pid" ]; then
        echo "CRITICAL: $pipeline_name not running"
        return 2
    fi
    
    # Check CPU usage
    local cpu_usage=$(ps -p $pid -o %cpu --no-headers)
    if (( $(echo "$cpu_usage > 80" | bc -l) )); then
        echo "WARNING: $pipeline_name high CPU usage: $cpu_usage%"
        return 1
    fi
    
    # Check memory usage
    local mem_usage=$(ps -p $pid -o %mem --no-headers)
    if (( $(echo "$mem_usage > 70" | bc -l) )); then
        echo "WARNING: $pipeline_name high memory usage: $mem_usage%"
        return 1
    fi
    
    echo "OK: $pipeline_name running normally"
    return 0
}

# Monitor data directories
check_disk_space() {
    local threshold=85
    local usage=$(df /data | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [ $usage -gt $threshold ]; then
        echo "CRITICAL: Disk usage ${usage}% exceeds threshold ${threshold}%"
        return 2
    fi
    
    echo "OK: Disk usage ${usage}%"
    return 0
}
```

---

## Process Management

### 5. How do you manage long-running data processing jobs?

**Answer:**
Process management strategies for data engineering workloads:

**Process Control:**
```bash
# Start process in background with nohup
nohup python long_running_etl.py > etl.log 2>&1 &

# Use screen for interactive management
screen -S data-pipeline
python data_pipeline.py
# Ctrl+A, D to detach
screen -r data-pipeline  # Reattach

# Systemd service for production
# /etc/systemd/system/data-pipeline.service
[Unit]
Description=Data Processing Pipeline
After=network.target

[Service]
Type=simple
User=dataeng
WorkingDirectory=/opt/data-pipeline
ExecStart=/usr/bin/python3 pipeline.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Process Monitoring:**
```bash
# Monitor process tree
pstree -p $(pgrep python)

# Check process limits
cat /proc/$(pgrep python)/limits

# Monitor process I/O
cat /proc/$(pgrep python)/io
pidstat -d 1 $(pgrep python)

# Kill processes gracefully
pkill -TERM -f "data_pipeline"
sleep 10
pkill -KILL -f "data_pipeline"
```

### 6. How do you implement process isolation for data engineering workloads?

**Answer:**
Isolation techniques to prevent resource conflicts:

**Cgroups (Control Groups):**
```bash
# Create cgroup for data processing
mkdir /sys/fs/cgroup/memory/data-processing
mkdir /sys/fs/cgroup/cpu/data-processing

# Set memory limit (8GB)
echo 8589934592 > /sys/fs/cgroup/memory/data-processing/memory.limit_in_bytes

# Set CPU limit (50% of 4 cores)
echo 200000 > /sys/fs/cgroup/cpu/data-processing/cpu.cfs_quota_us
echo 100000 > /sys/fs/cgroup/cpu/data-processing/cpu.cfs_period_us

# Add process to cgroup
echo $$ > /sys/fs/cgroup/memory/data-processing/cgroup.procs
echo $$ > /sys/fs/cgroup/cpu/data-processing/cgroup.procs
```

**Namespaces:**
```bash
# Network namespace isolation
ip netns add data-processing
ip netns exec data-processing ip link set lo up

# Mount namespace for file isolation
unshare --mount --pid --fork chroot /data-processing-root /bin/bash

# User namespace for security
unshare --user --map-root-user python data_pipeline.py
```

**Docker Containers:**
```dockerfile
# Dockerfile for data processing
FROM python:3.9-slim

RUN useradd -m -u 1000 dataeng
USER dataeng
WORKDIR /app

COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY pipeline.py .
CMD ["python", "pipeline.py"]
```

```bash
# Run with resource limits
docker run -d \
  --name data-pipeline \
  --memory=8g \
  --cpus=2.0 \
  --ulimit nofile=65536:65536 \
  data-pipeline:latest
```

---

## File Systems

### 7. How do you optimize file system performance for big data workloads?

**Answer:**
File system selection and tuning for data processing:

**File System Comparison:**
```bash
# XFS - Best for large files and parallel I/O
mkfs.xfs -f -d agcount=32 -l size=128m /dev/sdb1
mount -o noatime,largeio,inode64,swalloc /dev/sdb1 /data

# EXT4 - Good general purpose with extent support
mkfs.ext4 -F -E stride=32,stripe-width=128 /dev/sdc1
mount -o noatime,data=writeback,barrier=0 /dev/sdc1 /data

# ZFS - Advanced features but higher overhead
zpool create -o ashift=12 datapool /dev/sdd1
zfs set compression=lz4 datapool
zfs set recordsize=1M datapool  # For large sequential I/O
```

**Performance Tuning:**
```bash
# Increase readahead for sequential access
echo 4096 > /sys/block/sdb/queue/read_ahead_kb

# Optimize for SSDs
echo noop > /sys/block/sdb/queue/scheduler
echo 1 > /sys/block/sdb/queue/nomerges

# Tune dirty page writeback
echo 15 > /proc/sys/vm/dirty_ratio
echo 5 > /proc/sys/vm/dirty_background_ratio
echo 500 > /proc/sys/vm/dirty_expire_centisecs
```

### 8. How do you manage large datasets and file operations efficiently?

**Answer:**
Efficient file operations for big data:

**Parallel File Operations:**
```bash
# Parallel copy with rsync
rsync -av --progress --partial \
  --bwlimit=100000 \
  /source/data/ /destination/data/

# Parallel compression
find /data -name "*.csv" -print0 | \
  xargs -0 -P 8 -I {} gzip {}

# Parallel file processing
find /data -name "*.log" -print0 | \
  xargs -0 -P 4 -I {} python process_log.py {}
```

**Efficient File Handling:**
```python
# Memory-mapped files for large datasets
import mmap

def process_large_file(filename):
    with open(filename, 'r+b') as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            # Process file without loading into memory
            for line in iter(mm.readline, b""):
                process_line(line)

# Streaming file processing
def process_streaming(filename):
    with open(filename, 'r') as f:
        for line in f:  # Reads one line at a time
            yield process_line(line.strip())
```

**File System Monitoring:**
```bash
# Monitor file system usage
df -h
du -sh /data/*
lsof +D /data | wc -l  # Open file count

# Find large files
find /data -type f -size +1G -exec ls -lh {} \;

# Monitor file system performance
iostat -x 1 5
sar -d 1 5
```

---

## Networking

### 9. How do you optimize network performance for distributed data processing?

**Answer:**
Network optimization for data-intensive applications:

**Network Tuning:**
```bash
# TCP buffer tuning
echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem = 4096 87380 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem = 4096 65536 134217728' >> /etc/sysctl.conf

# Increase connection limits
echo 'net.core.somaxconn = 65535' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_max_syn_backlog = 65535' >> /etc/sysctl.conf

# Apply settings
sysctl -p
```

**Network Monitoring:**
```bash
# Monitor network throughput
iftop -i eth0
nload eth0
bmon -p eth0

# Check network connections
ss -tuln | grep :9092  # Kafka
ss -tuln | grep :8080  # HTTP services
netstat -an | grep ESTABLISHED | wc -l

# Network performance testing
iperf3 -s  # Server
iperf3 -c server-ip -t 60 -P 4  # Client with 4 parallel streams
```

### 10. How do you troubleshoot network issues in distributed data systems?

**Answer:**
Systematic network troubleshooting approach:

**Connectivity Testing:**
```bash
# Basic connectivity
ping -c 4 kafka-broker-1
telnet kafka-broker-1 9092
nc -zv kafka-broker-1 9092

# DNS resolution
nslookup kafka-broker-1
dig kafka-broker-1

# Route tracing
traceroute kafka-broker-1
mtr kafka-broker-1
```

**Performance Analysis:**
```bash
# Packet capture and analysis
tcpdump -i eth0 -w capture.pcap host kafka-broker-1
wireshark capture.pcap

# Network latency testing
ping -c 100 kafka-broker-1 | tail -1
hping3 -S -p 9092 -c 100 kafka-broker-1

# Bandwidth testing between nodes
iperf3 -c kafka-broker-1 -p 5001 -t 30
```

**Application-Level Debugging:**
```bash
# Check service bindings
netstat -tlnp | grep :9092
ss -tlnp | grep :9092

# Monitor connection states
watch -n 1 'ss -s'
watch -n 1 'netstat -an | grep :9092 | wc -l'

# Application logs correlation
tail -f /var/log/kafka/server.log | grep -E "(ERROR|WARN|Connection)"
journalctl -u kafka -f | grep network
```

---

## Summary

Advanced Linux skills for data engineering include:

1. **System Administration**: Resource management and performance tuning
2. **Performance Monitoring**: Bottleneck identification and system observability
3. **Process Management**: Long-running job control and isolation
4. **File Systems**: Optimization for big data workloads
5. **Networking**: Distributed system connectivity and troubleshooting