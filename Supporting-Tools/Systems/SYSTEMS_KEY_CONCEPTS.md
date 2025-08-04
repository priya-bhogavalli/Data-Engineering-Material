# Systems Key Concepts for Data Engineering

## 1. Linux Fundamentals
**What it is**: Open-source operating system widely used in data engineering for servers, containers, and cloud environments.

**Why important**: Most data engineering infrastructure runs on Linux. Understanding Linux is essential for managing servers, troubleshooting issues, and optimizing performance.

**Key Commands**:
```bash
# File operations
ls -la                    # List files with details
cd /path/to/directory     # Change directory
mkdir -p /path/to/dir     # Create directory
cp source destination     # Copy files
mv old_name new_name      # Move/rename
rm -rf directory          # Remove directory
find /path -name "*.log"  # Find files

# Process management
ps aux                    # List all processes
top                       # Real-time process monitor
htop                      # Enhanced process monitor
kill -9 PID              # Kill process
nohup command &          # Run command in background

# System monitoring
df -h                     # Disk usage
free -h                   # Memory usage
iostat                    # I/O statistics
netstat -tulpn           # Network connections
```

## 2. Shell Scripting for Automation
**What it is**: Writing scripts to automate system tasks and data processing workflows.

**Why important**: Automates repetitive tasks, orchestrates data pipelines, and enables consistent deployments.

**Example Scripts**:
```bash
#!/bin/bash
# data_pipeline_monitor.sh

# Configuration
LOG_FILE="/var/log/data_pipeline.log"
ERROR_THRESHOLD=10
EMAIL="admin@company.com"

# Function to check pipeline status
check_pipeline_status() {
    local pipeline_name=$1
    local status=$(systemctl is-active $pipeline_name)
    
    if [ "$status" != "active" ]; then
        echo "$(date): Pipeline $pipeline_name is not running" >> $LOG_FILE
        return 1
    fi
    return 0
}

# Function to check error count
check_error_count() {
    local error_count=$(grep -c "ERROR" $LOG_FILE)
    
    if [ $error_count -gt $ERROR_THRESHOLD ]; then
        echo "High error count detected: $error_count errors"
        send_alert "High error count: $error_count"
        return 1
    fi
    return 0
}

# Function to send alerts
send_alert() {
    local message=$1
    echo "$message" | mail -s "Data Pipeline Alert" $EMAIL
}

# Main monitoring loop
main() {
    echo "$(date): Starting pipeline monitoring"
    
    # Check critical pipelines
    pipelines=("customer-etl" "product-sync" "analytics-processor")
    
    for pipeline in "${pipelines[@]}"; do
        if ! check_pipeline_status $pipeline; then
            send_alert "Pipeline $pipeline is down"
        fi
    done
    
    # Check error rates
    check_error_count
    
    echo "$(date): Monitoring check completed"
}

# Run main function
main
```

## 3. Networking Fundamentals
**What it is**: Understanding network protocols, configurations, and troubleshooting for distributed data systems.

**Why important**: Data engineering involves distributed systems that communicate over networks. Network issues can cause pipeline failures and performance problems.

**Key Concepts**:
```bash
# Network diagnostics
ping google.com           # Test connectivity
traceroute google.com     # Trace network path
nslookup domain.com       # DNS lookup
dig domain.com           # DNS information
netstat -i               # Network interfaces

# Port and service checking
telnet host port         # Test port connectivity
nc -zv host port         # Check if port is open
ss -tulpn               # Show listening ports
lsof -i :8080           # Show what's using port 8080

# Network configuration
ifconfig                 # Network interface config
ip addr show            # Show IP addresses
route -n                # Show routing table
iptables -L             # Show firewall rules
```

## 4. Security Fundamentals
**What it is**: Protecting data systems, managing access controls, and ensuring compliance with security standards.

**Why important**: Data engineering handles sensitive information and must implement proper security measures to protect data and systems.

**Security Practices**:
```bash
# User and permission management
sudo useradd -m dataeng          # Create user
sudo usermod -aG sudo dataeng    # Add to sudo group
chmod 755 script.sh             # Set file permissions
chown user:group file.txt        # Change ownership

# SSH security
ssh-keygen -t rsa -b 4096       # Generate SSH key
ssh-copy-id user@server         # Copy public key
ssh -i ~/.ssh/key user@server   # Connect with key

# File encryption
gpg --symmetric file.txt        # Encrypt file
gpg --decrypt file.txt.gpg      # Decrypt file
openssl enc -aes-256-cbc -in file.txt -out file.enc  # OpenSSL encryption
```

## 5. System Design Principles
**What it is**: Designing scalable, reliable, and maintainable distributed systems for data processing.

**Why important**: Data engineering systems must handle large volumes of data reliably. Good system design ensures scalability and fault tolerance.

**Design Patterns**:
```python
# Circuit Breaker Pattern
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise e

# Retry Pattern with Exponential Backoff
import random

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def unreliable_api_call():
    # Simulated API call that might fail
    pass
```

## 6. Performance Monitoring and Optimization
**What it is**: Monitoring system performance and optimizing resource usage for data processing workloads.

**Why important**: Data processing can be resource-intensive. Monitoring and optimization ensure efficient resource usage and identify bottlenecks.

**Monitoring Tools**:
```bash
# CPU monitoring
top                      # Real-time CPU usage
htop                     # Enhanced process viewer
sar -u 1 10             # CPU utilization over time
mpstat 1 5              # Multi-processor statistics

# Memory monitoring
free -h                  # Memory usage
vmstat 1 5              # Virtual memory statistics
pmap PID                # Process memory map

# Disk I/O monitoring
iostat -x 1 5           # Extended I/O statistics
iotop                   # I/O usage by process
df -h                   # Disk space usage
du -sh /path            # Directory size

# Network monitoring
iftop                   # Network usage by connection
nethogs                 # Network usage by process
ss -i                   # Socket statistics
```

**Performance Optimization Script**:
```python
#!/usr/bin/env python3
import psutil
import time
import logging
from typing import Dict, List

class SystemMonitor:
    def __init__(self, thresholds: Dict[str, float]):
        self.thresholds = thresholds
        self.logger = logging.getLogger(__name__)
    
    def check_cpu_usage(self) -> Dict[str, float]:
        """Monitor CPU usage and identify high-usage processes."""
        cpu_percent = psutil.cpu_percent(interval=1)
        
        if cpu_percent > self.thresholds.get('cpu', 80):
            self.logger.warning(f"High CPU usage: {cpu_percent}%")
            
            # Get top CPU processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 5:  # Only processes using >5% CPU
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            return {
                'cpu_percent': cpu_percent,
                'top_processes': processes[:5]
            }
        
        return {'cpu_percent': cpu_percent}
    
    def check_memory_usage(self) -> Dict[str, float]:
        """Monitor memory usage."""
        memory = psutil.virtual_memory()
        
        if memory.percent > self.thresholds.get('memory', 85):
            self.logger.warning(f"High memory usage: {memory.percent}%")
            
            # Get memory-intensive processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['memory_percent'] > 2:  # Only processes using >2% memory
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
            
            return {
                'memory_percent': memory.percent,
                'available_gb': memory.available / (1024**3),
                'top_processes': processes[:5]
            }
        
        return {'memory_percent': memory.percent}
    
    def check_disk_usage(self) -> Dict[str, float]:
        """Monitor disk usage."""
        disk_usage = {}
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = (usage.used / usage.total) * 100
                
                disk_usage[partition.mountpoint] = {
                    'percent': usage_percent,
                    'free_gb': usage.free / (1024**3),
                    'total_gb': usage.total / (1024**3)
                }
                
                if usage_percent > self.thresholds.get('disk', 90):
                    self.logger.warning(f"High disk usage on {partition.mountpoint}: {usage_percent:.1f}%")
                    
            except PermissionError:
                continue
        
        return disk_usage
    
    def generate_report(self) -> Dict:
        """Generate comprehensive system report."""
        return {
            'timestamp': time.time(),
            'cpu': self.check_cpu_usage(),
            'memory': self.check_memory_usage(),
            'disk': self.check_disk_usage(),
            'load_average': psutil.getloadavg(),
            'boot_time': psutil.boot_time()
        }

# Usage
if __name__ == "__main__":
    thresholds = {
        'cpu': 80,      # 80% CPU usage
        'memory': 85,   # 85% memory usage
        'disk': 90      # 90% disk usage
    }
    
    monitor = SystemMonitor(thresholds)
    
    while True:
        report = monitor.generate_report()
        print(f"System Report: {report}")
        time.sleep(60)  # Check every minute
```

These system concepts provide the foundation for managing and optimizing the infrastructure that supports data engineering workloads, ensuring reliable and efficient data processing operations.