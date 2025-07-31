# Linux Interview Questions for Data Engineers

## Basic Level Questions

### 1. What are the essential Linux commands for data engineers?
**Answer**: Core Linux commands for data engineering tasks:

**File Operations**:
```bash
# File and directory operations
ls -la                    # List files with details
find /path -name "*.csv"  # Find CSV files
du -sh /data/*           # Check directory sizes
df -h                    # Check disk usage
tree /data               # Show directory structure

# File content operations
head -n 100 data.csv     # First 100 lines
tail -f /var/log/app.log # Follow log file
wc -l data.txt           # Count lines
grep "ERROR" app.log     # Search for patterns
sort data.txt            # Sort file content
uniq -c sorted.txt       # Count unique lines
```

**Text Processing**:
```bash
# AWK for data processing
awk -F',' '{print $1,$3}' data.csv                    # Extract columns 1 and 3
awk -F',' '$3 > 100 {print $0}' sales.csv            # Filter rows where column 3 > 100
awk -F',' '{sum+=$3} END {print "Total:", sum}' data.csv  # Sum column 3

# SED for text manipulation
sed 's/old_text/new_text/g' file.txt                 # Replace text
sed -n '10,20p' file.txt                             # Print lines 10-20
sed '/pattern/d' file.txt                            # Delete lines matching pattern

# Cut for column extraction
cut -d',' -f1,3 data.csv                             # Extract columns 1 and 3
cut -c1-10 file.txt                                  # Extract characters 1-10
```

**Process Management**:
```bash
# Process monitoring
ps aux | grep python     # Find Python processes
top -p $(pgrep -d',' python)  # Monitor specific processes
htop                     # Interactive process viewer
nohup python script.py & # Run process in background
jobs                     # List background jobs
kill -9 PID             # Force kill process
```

### 2. How do you manage file permissions and ownership in Linux?
**Answer**: Linux permission system for data security:

**Permission Types**:
```bash
# Permission structure: rwxrwxrwx (owner, group, others)
# r=4, w=2, x=1

# View permissions
ls -l data.csv
# -rw-r--r-- 1 user group 1024 Jan 1 12:00 data.csv

# Change permissions
chmod 755 script.sh      # rwxr-xr-x (executable script)
chmod 644 data.csv       # rw-r--r-- (readable data file)
chmod 600 config.conf    # rw------- (private config)
chmod u+x script.py      # Add execute for owner
chmod g-w file.txt       # Remove write for group
chmod o-r sensitive.txt  # Remove read for others

# Change ownership
chown user:group file.txt        # Change owner and group
chown -R user:group /data/       # Recursive ownership change
chgrp dataeng /data/warehouse/   # Change group only

# Special permissions
chmod +t /tmp/shared/    # Sticky bit (only owner can delete)
chmod g+s /data/shared/  # Set group ID (files inherit group)
```

**Access Control Lists (ACL)**:
```bash
# Set ACL permissions
setfacl -m u:analyst:r-- data.csv           # Give user 'analyst' read access
setfacl -m g:dataeng:rw- /data/warehouse/   # Give group 'dataeng' read-write
setfacl -R -m d:g:dataeng:rwx /data/        # Default ACL for new files

# View ACL permissions
getfacl data.csv

# Remove ACL
setfacl -x u:analyst data.csv               # Remove user ACL
setfacl -b data.csv                         # Remove all ACLs
```

### 3. How do you monitor system resources and performance?
**Answer**: System monitoring for data engineering workloads:

**CPU and Memory Monitoring**:
```bash
# Real-time monitoring
top                      # System overview
htop                     # Enhanced system monitor
iotop                    # I/O monitoring
vmstat 5                 # Virtual memory stats every 5 seconds
iostat -x 5              # I/O statistics

# Memory analysis
free -h                  # Memory usage in human-readable format
cat /proc/meminfo        # Detailed memory information
ps aux --sort=-%mem      # Processes sorted by memory usage
pmap -x PID              # Memory map of specific process

# CPU analysis
lscpu                    # CPU information
cat /proc/cpuinfo        # Detailed CPU info
mpstat 5                 # CPU usage statistics
sar -u 5 10             # CPU utilization (5-second intervals, 10 times)
```

**Disk and Network Monitoring**:
```bash
# Disk monitoring
df -h                    # Disk space usage
du -sh /data/*          # Directory sizes
lsblk                   # Block devices
fdisk -l                # Disk partitions
iotop -o                # I/O usage by process

# Network monitoring
netstat -tuln           # Network connections
ss -tuln                # Socket statistics
iftop                   # Network bandwidth usage
nload                   # Network load monitor
tcpdump -i eth0         # Packet capture
```

**Log Analysis**:
```bash
# System logs
journalctl -f           # Follow systemd logs
journalctl -u service   # Logs for specific service
tail -f /var/log/syslog # Follow system log
dmesg | tail            # Kernel messages

# Application logs
tail -f /var/log/apache2/access.log
grep "ERROR" /var/log/app.log | tail -20
zcat /var/log/app.log.gz | grep "2024-01-01"
```

### 4. How do you work with environment variables and shell configuration?
**Answer**: Environment management for data engineering:

**Environment Variables**:
```bash
# View environment variables
env                      # All environment variables
echo $PATH              # Specific variable
printenv HOME           # Print specific variable

# Set environment variables
export SPARK_HOME=/opt/spark
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk
export PATH=$PATH:$SPARK_HOME/bin

# Persistent environment variables
# Add to ~/.bashrc or ~/.profile
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
source ~/.bashrc        # Reload configuration

# System-wide environment variables
sudo vim /etc/environment
# Add: SPARK_HOME=/opt/spark

# Temporary variables (current session only)
TEMP_VAR=value
echo $TEMP_VAR
```

**Shell Configuration**:
```bash
# Bash configuration files
~/.bashrc               # Interactive shell configuration
~/.bash_profile         # Login shell configuration
~/.profile              # POSIX shell configuration
/etc/bash.bashrc        # System-wide bash configuration

# Useful aliases for data engineers
alias ll='ls -la'
alias grep='grep --color=auto'
alias df='df -h'
alias du='du -h'
alias free='free -h'
alias psg='ps aux | grep'
alias logs='tail -f /var/log/syslog'

# Functions in .bashrc
function findlarge() {
    find ${1:-.} -type f -size +${2:-100M} -exec ls -lh {} \; | sort -k5 -hr
}

function csvhead() {
    head -n ${2:-10} $1 | column -t -s','
}
```

### 5. How do you manage services and processes in Linux?
**Answer**: Service and process management:

**Systemd Service Management**:
```bash
# Service operations
systemctl start apache2         # Start service
systemctl stop apache2          # Stop service
systemctl restart apache2       # Restart service
systemctl reload apache2        # Reload configuration
systemctl enable apache2        # Enable at boot
systemctl disable apache2       # Disable at boot
systemctl status apache2        # Check service status

# Service information
systemctl list-units --type=service    # List all services
systemctl list-unit-files --type=service --state=enabled  # Enabled services
systemctl show apache2                 # Detailed service info
journalctl -u apache2 -f               # Follow service logs
```

**Process Management**:
```bash
# Background processes
nohup python data_pipeline.py > pipeline.log 2>&1 &
disown                          # Detach from shell

# Process control
jobs                           # List background jobs
fg %1                          # Bring job 1 to foreground
bg %1                          # Send job 1 to background
kill %1                        # Kill job 1
killall python                # Kill all Python processes

# Process monitoring
pgrep -f "data_pipeline"       # Find process by name
pkill -f "data_pipeline"       # Kill process by name
pidof python                   # Get PID of process
```

## Intermediate Level Questions

### 6. How do you implement shell scripting for data engineering automation?
**Answer**: Advanced shell scripting for data pipelines:

**Data Processing Script**:
```bash
#!/bin/bash

# Data processing pipeline script
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
DATA_DIR="/data/raw"
PROCESSED_DIR="/data/processed"
LOG_FILE="/var/log/data_pipeline.log"
DATE=$(date +%Y%m%d)

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Cleanup function
cleanup() {
    log "Cleaning up temporary files..."
    rm -f /tmp/processing_*
}
trap cleanup EXIT

# Main processing function
process_data() {
    local input_file="$1"
    local output_file="$2"
    
    log "Processing $input_file..."
    
    # Validate input file
    [[ -f "$input_file" ]] || error_exit "Input file not found: $input_file"
    [[ -s "$input_file" ]] || error_exit "Input file is empty: $input_file"
    
    # Data validation
    local line_count=$(wc -l < "$input_file")
    log "Input file has $line_count lines"
    
    # Process data with error checking
    if ! awk -F',' '
        NR==1 { print; next }  # Header
        NF==5 && $3 ~ /^[0-9]+(\.[0-9]+)?$/ { print }  # Valid rows
    ' "$input_file" > "$output_file"; then
        error_exit "Data processing failed for $input_file"
    fi
    
    local processed_count=$(wc -l < "$output_file")
    log "Processed $processed_count valid records"
    
    # Validate output
    [[ -s "$output_file" ]] || error_exit "Output file is empty: $output_file"
}

# Archive function
archive_file() {
    local file="$1"
    local archive_dir="/data/archive/$DATE"
    
    mkdir -p "$archive_dir"
    
    if gzip -c "$file" > "$archive_dir/$(basename "$file").gz"; then
        log "Archived $file to $archive_dir"
        rm "$file"
    else
        error_exit "Failed to archive $file"
    fi
}

# Main execution
main() {
    log "Starting data processing pipeline"
    
    # Check dependencies
    command -v awk >/dev/null 2>&1 || error_exit "awk is required"
    command -v gzip >/dev/null 2>&1 || error_exit "gzip is required"
    
    # Create directories
    mkdir -p "$PROCESSED_DIR" "$DATA_DIR/archive"
    
    # Process all CSV files
    local processed_files=0
    
    for input_file in "$DATA_DIR"/*.csv; do
        [[ -f "$input_file" ]] || continue
        
        local filename=$(basename "$input_file" .csv)
        local output_file="$PROCESSED_DIR/${filename}_processed_$DATE.csv"
        
        process_data "$input_file" "$output_file"
        archive_file "$input_file"
        
        ((processed_files++))
    done
    
    log "Pipeline completed. Processed $processed_files files"
    
    # Send notification
    if command -v mail >/dev/null 2>&1; then
        echo "Data pipeline completed successfully. Processed $processed_files files." | \
        mail -s "Data Pipeline Status - $DATE" admin@company.com
    fi
}

# Execute main function
main "$@"
```

**Monitoring Script**:
```bash
#!/bin/bash

# System monitoring script for data engineering infrastructure
THRESHOLD_CPU=80
THRESHOLD_MEMORY=85
THRESHOLD_DISK=90
ALERT_EMAIL="admin@company.com"

check_cpu() {
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    cpu_usage=${cpu_usage%.*}  # Remove decimal
    
    if (( cpu_usage > THRESHOLD_CPU )); then
        echo "ALERT: CPU usage is ${cpu_usage}% (threshold: ${THRESHOLD_CPU}%)"
        return 1
    fi
    return 0
}

check_memory() {
    local mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    
    if (( mem_usage > THRESHOLD_MEMORY )); then
        echo "ALERT: Memory usage is ${mem_usage}% (threshold: ${THRESHOLD_MEMORY}%)"
        return 1
    fi
    return 0
}

check_disk() {
    local disk_usage=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    
    if (( disk_usage > THRESHOLD_DISK )); then
        echo "ALERT: Disk usage is ${disk_usage}% (threshold: ${THRESHOLD_DISK}%)"
        return 1
    fi
    return 0
}

check_services() {
    local services=("apache2" "mysql" "redis-server")
    local failed_services=()
    
    for service in "${services[@]}"; do
        if ! systemctl is-active --quiet "$service"; then
            failed_services+=("$service")
        fi
    done
    
    if (( ${#failed_services[@]} > 0 )); then
        echo "ALERT: Services not running: ${failed_services[*]}"
        return 1
    fi
    return 0
}

# Main monitoring function
main() {
    local alerts=()
    
    check_cpu || alerts+=("CPU")
    check_memory || alerts+=("Memory")
    check_disk || alerts+=("Disk")
    check_services || alerts+=("Services")
    
    if (( ${#alerts[@]} > 0 )); then
        local alert_message="System alerts detected: ${alerts[*]}"
        echo "$alert_message"
        
        # Send email alert
        if command -v mail >/dev/null 2>&1; then
            echo "$alert_message" | mail -s "System Alert - $(hostname)" "$ALERT_EMAIL"
        fi
        
        exit 1
    else
        echo "All systems normal"
        exit 0
    fi
}

main "$@"
```

### 7. How do you manage cron jobs for data engineering tasks?
**Answer**: Cron job management for automated data pipelines:

**Cron Configuration**:
```bash
# Edit crontab
crontab -e                    # Edit user crontab
sudo crontab -e               # Edit root crontab
crontab -l                    # List current cron jobs
crontab -r                    # Remove all cron jobs

# Cron syntax: minute hour day month day_of_week command
# * * * * * command
# | | | | |
# | | | | +-- Day of week (0-7, Sunday=0 or 7)
# | | | +---- Month (1-12)
# | | +------ Day of month (1-31)
# | +-------- Hour (0-23)
# +---------- Minute (0-59)

# Example cron jobs for data engineering
# Daily data backup at 2 AM
0 2 * * * /opt/scripts/backup_data.sh >> /var/log/backup.log 2>&1

# Hourly data processing
0 * * * * /opt/scripts/process_hourly_data.sh

# Weekly cleanup on Sunday at 3 AM
0 3 * * 0 /opt/scripts/cleanup_old_files.sh

# Monthly report generation on 1st day at 6 AM
0 6 1 * * /opt/scripts/generate_monthly_report.sh

# Every 15 minutes monitoring
*/15 * * * * /opt/scripts/system_monitor.sh

# Business hours only (9 AM to 5 PM, Monday to Friday)
0 9-17 * * 1-5 /opt/scripts/business_hours_task.sh
```

**Advanced Cron Management**:
```bash
# Cron with environment variables
# Add to crontab
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=admin@company.com
HOME=/home/dataeng

# Data pipeline with proper environment
0 2 * * * cd /opt/data-pipeline && ./run_pipeline.sh

# Cron job with logging and error handling
#!/bin/bash
# /opt/scripts/cron_wrapper.sh

SCRIPT_NAME="$1"
LOG_FILE="/var/log/cron_jobs.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$SCRIPT_NAME] $1" >> "$LOG_FILE"
}

log "Starting $SCRIPT_NAME"

if "$@"; then
    log "SUCCESS: $SCRIPT_NAME completed"
    exit 0
else
    log "ERROR: $SCRIPT_NAME failed with exit code $?"
    # Send alert email
    echo "$SCRIPT_NAME failed at $(date)" | mail -s "Cron Job Failure" admin@company.com
    exit 1
fi

# Use wrapper in crontab
0 2 * * * /opt/scripts/cron_wrapper.sh /opt/scripts/data_pipeline.sh
```

**Systemd Timers (Alternative to Cron)**:
```bash
# Create timer unit file
# /etc/systemd/system/data-pipeline.timer
[Unit]
Description=Run data pipeline daily
Requires=data-pipeline.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

# Create service unit file
# /etc/systemd/system/data-pipeline.service
[Unit]
Description=Data Pipeline Service
After=network.target

[Service]
Type=oneshot
User=dataeng
Group=dataeng
WorkingDirectory=/opt/data-pipeline
ExecStart=/opt/data-pipeline/run_pipeline.sh
StandardOutput=journal
StandardError=journal

# Enable and start timer
sudo systemctl daemon-reload
sudo systemctl enable data-pipeline.timer
sudo systemctl start data-pipeline.timer

# Check timer status
systemctl list-timers
systemctl status data-pipeline.timer
```

### 8. How do you implement log rotation and management?
**Answer**: Log management for data engineering applications:

**Logrotate Configuration**:
```bash
# System logrotate configuration
# /etc/logrotate.d/data-pipeline

/var/log/data-pipeline/*.log {
    daily                    # Rotate daily
    missingok               # Don't error if log file missing
    rotate 30               # Keep 30 days of logs
    compress                # Compress old logs
    delaycompress           # Don't compress most recent old log
    notifempty              # Don't rotate empty logs
    create 644 dataeng dataeng  # Create new log with permissions
    postrotate
        # Restart service to use new log file
        systemctl reload data-pipeline || true
    endscript
}

# Application-specific configuration
/opt/spark/logs/*.log {
    size 100M               # Rotate when log reaches 100MB
    rotate 10               # Keep 10 old logs
    compress
    missingok
    notifempty
    copytruncate           # Copy and truncate instead of moving
}

# Database logs
/var/log/mysql/*.log {
    weekly
    rotate 52              # Keep 1 year of weekly logs
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        /usr/bin/mysql -e 'FLUSH LOGS'
    endscript
}

# Test logrotate configuration
sudo logrotate -d /etc/logrotate.d/data-pipeline  # Debug mode
sudo logrotate -f /etc/logrotate.d/data-pipeline  # Force rotation
```

**Custom Log Management Script**:
```bash
#!/bin/bash
# Advanced log management script

LOG_DIRS=("/var/log/data-pipeline" "/opt/spark/logs" "/var/log/airflow")
RETENTION_DAYS=30
ARCHIVE_DIR="/data/log-archive"
COMPRESS_OLDER_THAN=7  # Days

manage_logs() {
    local log_dir="$1"
    
    echo "Managing logs in $log_dir"
    
    # Create archive directory
    mkdir -p "$ARCHIVE_DIR/$(basename "$log_dir")"
    
    # Find and compress logs older than specified days
    find "$log_dir" -name "*.log" -type f -mtime +$COMPRESS_OLDER_THAN ! -name "*.gz" -exec gzip {} \;
    
    # Archive old compressed logs
    find "$log_dir" -name "*.log.gz" -type f -mtime +$RETENTION_DAYS -exec mv {} "$ARCHIVE_DIR/$(basename "$log_dir")/" \;
    
    # Delete very old archived logs (1 year)
    find "$ARCHIVE_DIR/$(basename "$log_dir")" -name "*.log.gz" -type f -mtime +365 -delete
    
    # Report disk usage
    echo "Current log directory size: $(du -sh "$log_dir" | cut -f1)"
    echo "Archive directory size: $(du -sh "$ARCHIVE_DIR/$(basename "$log_dir")" | cut -f1)"
}

# Process all log directories
for dir in "${LOG_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        manage_logs "$dir"
    else
        echo "Warning: Log directory $dir does not exist"
    fi
done

# Clean up application-specific logs
# Spark event logs
find /opt/spark/work -name "app-*" -type d -mtime +7 -exec rm -rf {} \;

# Airflow task logs
find /var/log/airflow/dag_processor_manager -name "*.log" -mtime +30 -delete

echo "Log management completed at $(date)"
```

### 9. How do you secure Linux systems for data engineering environments?
**Answer**: Security hardening for data infrastructure:

**User and Access Management**:
```bash
# Create dedicated service accounts
sudo useradd -r -s /bin/false -d /opt/spark spark
sudo useradd -r -s /bin/false -d /opt/airflow airflow
sudo useradd -m -s /bin/bash dataeng

# Configure sudo access
# /etc/sudoers.d/dataeng
dataeng ALL=(ALL) NOPASSWD: /bin/systemctl restart data-pipeline
dataeng ALL=(ALL) NOPASSWD: /bin/systemctl status data-pipeline
dataeng ALL=(ALL) NOPASSWD: /usr/bin/tail -f /var/log/data-pipeline/*

# SSH key management
ssh-keygen -t rsa -b 4096 -C "dataeng@company.com"
ssh-copy-id -i ~/.ssh/id_rsa.pub user@remote-server

# Disable password authentication
# /etc/ssh/sshd_config
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
AllowUsers dataeng analyst
```

**Firewall Configuration**:
```bash
# UFW (Uncomplicated Firewall)
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow specific services
sudo ufw allow ssh
sudo ufw allow 8080/tcp  # Airflow web UI
sudo ufw allow 4040/tcp  # Spark UI
sudo ufw allow from 10.0.0.0/8 to any port 3306  # MySQL from internal network

# Check firewall status
sudo ufw status verbose

# iptables rules for advanced filtering
# Block suspicious IPs
sudo iptables -A INPUT -s 192.168.1.100 -j DROP

# Rate limiting for SSH
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
```

**File System Security**:
```bash
# Secure sensitive directories
sudo chmod 700 /opt/data-pipeline/config
sudo chmod 600 /opt/data-pipeline/config/*.conf
sudo chown -R dataeng:dataeng /opt/data-pipeline

# Set up encrypted storage for sensitive data
# Create encrypted partition
sudo cryptsetup luksFormat /dev/sdb1
sudo cryptsetup luksOpen /dev/sdb1 encrypted_data
sudo mkfs.ext4 /dev/mapper/encrypted_data

# Mount encrypted partition
sudo mkdir /data/encrypted
sudo mount /dev/mapper/encrypted_data /data/encrypted

# Add to /etc/fstab for automatic mounting
echo "/dev/mapper/encrypted_data /data/encrypted ext4 defaults 0 2" | sudo tee -a /etc/fstab

# File integrity monitoring with AIDE
sudo apt install aide
sudo aideinit
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Check for changes
sudo aide --check
```

### 10. How do you troubleshoot performance issues in Linux?
**Answer**: Performance troubleshooting methodology:

**System Performance Analysis**:
```bash
# CPU analysis
# Check CPU utilization
top -p $(pgrep -d',' python)
htop -p $(pgrep -d',' python)

# CPU per core
mpstat -P ALL 5

# Load average analysis
uptime
cat /proc/loadavg

# Process CPU usage
ps aux --sort=-%cpu | head -20

# Memory analysis
# Memory usage breakdown
free -h
cat /proc/meminfo

# Memory usage by process
ps aux --sort=-%mem | head -20
pmap -x PID  # Memory map of specific process

# Check for memory leaks
valgrind --tool=memcheck --leak-check=full python script.py

# I/O analysis
# Disk I/O statistics
iostat -x 5
iotop -o  # Show only processes doing I/O

# Check disk usage
df -h
du -sh /data/* | sort -hr

# Find large files
find /data -type f -size +1G -exec ls -lh {} \;

# Network analysis
# Network connections
netstat -tuln
ss -tuln

# Network traffic
iftop -i eth0
nload eth0

# Bandwidth usage
vnstat -i eth0
```

**Performance Monitoring Script**:
```bash
#!/bin/bash
# Comprehensive performance monitoring

REPORT_FILE="/tmp/performance_report_$(date +%Y%m%d_%H%M%S).txt"

{
    echo "=== SYSTEM PERFORMANCE REPORT ==="
    echo "Generated: $(date)"
    echo "Hostname: $(hostname)"
    echo ""
    
    echo "=== SYSTEM LOAD ==="
    uptime
    echo ""
    
    echo "=== CPU USAGE ==="
    mpstat 1 5
    echo ""
    
    echo "=== MEMORY USAGE ==="
    free -h
    echo ""
    echo "Top memory consumers:"
    ps aux --sort=-%mem | head -10
    echo ""
    
    echo "=== DISK USAGE ==="
    df -h
    echo ""
    echo "Largest directories in /data:"
    du -sh /data/* 2>/dev/null | sort -hr | head -10
    echo ""
    
    echo "=== I/O STATISTICS ==="
    iostat -x 1 5
    echo ""
    
    echo "=== NETWORK CONNECTIONS ==="
    ss -tuln | wc -l
    echo "Active connections count: $(ss -tuln | wc -l)"
    echo ""
    
    echo "=== TOP PROCESSES ==="
    ps aux --sort=-%cpu | head -15
    echo ""
    
    echo "=== SYSTEM ERRORS ==="
    dmesg | tail -20
    echo ""
    
} > "$REPORT_FILE"

echo "Performance report generated: $REPORT_FILE"

# Check for critical issues
check_critical_issues() {
    local issues=()
    
    # Check load average
    local load=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    if (( $(echo "$load > 5.0" | bc -l) )); then
        issues+=("High load average: $load")
    fi
    
    # Check memory usage
    local mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    if (( mem_usage > 90 )); then
        issues+=("High memory usage: ${mem_usage}%")
    fi
    
    # Check disk usage
    local disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if (( disk_usage > 90 )); then
        issues+=("High disk usage: ${disk_usage}%")
    fi
    
    if (( ${#issues[@]} > 0 )); then
        echo "CRITICAL ISSUES DETECTED:"
        printf '%s\n' "${issues[@]}"
        
        # Send alert
        if command -v mail >/dev/null 2>&1; then
            {
                echo "Critical performance issues detected on $(hostname):"
                printf '%s\n' "${issues[@]}"
                echo ""
                echo "Full report: $REPORT_FILE"
            } | mail -s "Performance Alert - $(hostname)" admin@company.com
        fi
    fi
}

check_critical_issues
```

This comprehensive Linux interview question set covers essential knowledge for data engineers, from basic command-line operations to advanced system administration, security, and performance troubleshooting in data engineering environments.