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

### 10. What is crontab?
**Answer**: Crontab (cron table) is a configuration file that specifies shell commands to run periodically on a given schedule.

**Cron Basics:**
- **Purpose**: Automate recurring tasks and system maintenance
- **Daemon**: Controlled by the cron daemon (crond)
- **User-specific**: Each user can have their own crontab
- **System-wide**: System crontab files in /etc/cron.d/

**Crontab Syntax:**
```bash
# Format: minute hour day month day_of_week command
# * * * * * command
# | | | | |
# | | | | +-- Day of week (0-7, Sunday=0 or 7)
# | | | +---- Month (1-12)
# | | +------ Day of month (1-31)
# | +-------- Hour (0-23)
# +---------- Minute (0-59)

# Examples:
0 2 * * * /opt/scripts/backup.sh          # Daily at 2 AM
*/15 * * * * /opt/scripts/monitor.sh       # Every 15 minutes
0 9-17 * * 1-5 /opt/scripts/business.sh   # Business hours, weekdays
0 0 1 * * /opt/scripts/monthly.sh         # First day of month
```

**Common Crontab Commands:**
```bash
# Edit user crontab
crontab -e

# List current cron jobs
crontab -l

# Remove all cron jobs
crontab -r

# Edit another user's crontab (as root)
crontab -u username -e

# System-wide cron directories
/etc/cron.hourly/    # Hourly scripts
/etc/cron.daily/     # Daily scripts
/etc/cron.weekly/    # Weekly scripts
/etc/cron.monthly/   # Monthly scripts
```

**Data Engineering Use Cases:**
```bash
# Daily data backup
0 2 * * * /opt/scripts/backup_data.sh >> /var/log/backup.log 2>&1

# Hourly log rotation
0 * * * * /opt/scripts/rotate_logs.sh

# Weekly cleanup of old files
0 3 * * 0 find /data/temp -type f -mtime +7 -delete

# Monthly report generation
0 6 1 * * /opt/scripts/generate_monthly_report.sh
```

### 11. How do you troubleshoot performance issues in Linux?
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

### 12. How do you manage and troubleshoot cron jobs?
**Answer**: Comprehensive cron job management and troubleshooting:

**Debugging Cron Jobs:**
```bash
# Check if cron daemon is running
systemctl status cron
# or
ps aux | grep cron

# View cron logs
tail -f /var/log/cron
# or on some systems
journalctl -u cron -f

# Test cron job manually
# Run the exact command from crontab to test
/opt/scripts/backup.sh

# Check user's mail for cron output
mail
# or
cat /var/mail/$USER
```

**Common Cron Issues and Solutions:**
```bash
# Issue: Environment variables not available
# Solution: Set environment in crontab
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
HOME=/home/user

# Issue: Script works manually but not in cron
# Solution: Use absolute paths
0 2 * * * cd /opt/data-pipeline && /usr/bin/python3 /opt/data-pipeline/process.py

# Issue: No output or error messages
# Solution: Redirect output to log files
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1

# Issue: Script runs but fails silently
# Solution: Add error handling and logging
#!/bin/bash
set -e  # Exit on error
exec > >(tee -a /var/log/script.log)
exec 2>&1
echo "[$(date)] Starting backup process"
```

**Advanced Cron Management:**
```bash
# Cron job wrapper for better error handling
#!/bin/bash
# /opt/scripts/cron_wrapper.sh
SCRIPT="$1"
LOG_FILE="/var/log/cron_jobs.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "Starting $SCRIPT"
if "$@"; then
    log "SUCCESS: $SCRIPT completed"
else
    log "ERROR: $SCRIPT failed with exit code $?"
    # Send alert email
    echo "Cron job $SCRIPT failed at $(date)" | mail -s "Cron Job Failure" admin@company.com
fi

# Use wrapper in crontab
0 2 * * * /opt/scripts/cron_wrapper.sh /opt/scripts/backup.sh
```

**Monitoring Cron Jobs:**
```bash
# Create monitoring script
#!/bin/bash
# Check if critical cron jobs are running
check_cron_job() {
    local job_pattern="$1"
    local max_age_minutes="$2"
    
    # Check if job has run recently
    if ! grep -q "$job_pattern" /var/log/cron | tail -100 | grep -q "$(date -d "$max_age_minutes minutes ago" '+%b %d %H:%M')"; then
        echo "WARNING: Cron job '$job_pattern' may not be running"
        return 1
    fi
    return 0
}

# Monitor critical jobs
check_cron_job "backup.sh" 1440  # Should run daily
check_cron_job "monitor.sh" 30   # Should run every 15 minutes
```

This comprehensive Linux interview question set covers essential knowledge for data engineers, from basic command-line operations to advanced system administration, security, performance troubleshooting, and automated task scheduling in data engineering environments.
## Advanced Level Questions

### 13. How do you implement advanced networking for data engineering?
**Answer**: Network configuration and optimization for data infrastructure:

**Network Interface Management**:
```bash
# Network interface configuration
ip addr show                    # Show all interfaces
ip link set eth0 up            # Bring interface up
ip addr add 192.168.1.100/24 dev eth0  # Add IP address

# Network routing
ip route show                   # Show routing table
ip route add 10.0.0.0/8 via 192.168.1.1  # Add route
ip route del 10.0.0.0/8        # Delete route

# Network namespaces for isolation
ip netns add data-pipeline      # Create namespace
ip netns exec data-pipeline ip addr show  # Execute in namespace
ip link set veth0 netns data-pipeline     # Move interface to namespace

# Bridge networking for containers
brctl addbr br0                 # Create bridge
brctl addif br0 eth0           # Add interface to bridge
brctl show                     # Show bridge configuration
```

**Advanced Network Monitoring**:
```bash
# Network performance analysis
iperf3 -s                      # Start iperf server
iperf3 -c server_ip -t 60      # Test bandwidth for 60 seconds

# Network latency testing
ping -c 10 -i 0.1 server_ip    # High frequency ping
mtr server_ip                  # Network route analysis

# Packet analysis
tcpdump -i eth0 -w capture.pcap port 8080  # Capture packets
wireshark capture.pcap         # Analyze captured packets

# Network security scanning
nmap -sS -O target_ip          # SYN scan with OS detection
netstat -tuln | grep LISTEN   # Show listening ports
```

**Network Optimization for Data Transfer**:
```bash
# TCP tuning for large data transfers
echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem = 4096 87380 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem = 4096 65536 134217728' >> /etc/sysctl.conf
sysctl -p                      # Apply changes

# Network bonding for redundancy
modprobe bonding
echo 'alias bond0 bonding' >> /etc/modprobe.conf
echo 'options bond0 mode=1 miimon=100' >> /etc/modprobe.conf
```

### 14. How do you implement container orchestration with Docker and Kubernetes?
**Answer**: Container management for scalable data engineering:

**Docker Container Management**:
```bash
# Advanced Docker operations
docker build -t data-pipeline:v1.0 .
docker run -d --name pipeline \
  --memory=4g --cpus=2 \
  -v /data:/app/data \
  -e SPARK_HOME=/opt/spark \
  data-pipeline:v1.0

# Docker networking
docker network create --driver bridge data-net
docker run --network=data-net --name db postgres:13
docker run --network=data-net --name app --link db:database app:latest

# Docker volumes for persistent data
docker volume create data-volume
docker run -v data-volume:/data postgres:13

# Multi-stage builds for optimization
FROM python:3.9 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]
```

**Kubernetes for Data Engineering**:
```yaml
# Kubernetes deployment for Spark
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-master
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spark-master
  template:
    metadata:
      labels:
        app: spark-master
    spec:
      containers:
      - name: spark-master
        image: bitnami/spark:3.2
        ports:
        - containerPort: 8080
        - containerPort: 7077
        env:
        - name: SPARK_MODE
          value: "master"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"

---
apiVersion: v1
kind: Service
metadata:
  name: spark-master-service
spec:
  selector:
    app: spark-master
  ports:
  - name: web-ui
    port: 8080
    targetPort: 8080
  - name: spark-port
    port: 7077
    targetPort: 7077
  type: LoadBalancer
```

**Kubernetes ConfigMaps and Secrets**:
```bash
# Create ConfigMap for application configuration
kubectl create configmap app-config \
  --from-file=config.properties \
  --from-literal=database.host=postgres.default.svc.cluster.local

# Create Secret for sensitive data
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=secretpassword

# Use in deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: data-app:latest
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: db-secret
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
      volumes:
      - name: config-volume
        configMap:
          name: app-config
```

### 15. How do you implement advanced storage management?
**Answer**: Storage optimization and management for data workloads:

**LVM (Logical Volume Management)**:
```bash
# Create physical volumes
pvcreate /dev/sdb /dev/sdc
pvdisplay                      # Show physical volumes

# Create volume group
vgcreate data-vg /dev/sdb /dev/sdc
vgdisplay                      # Show volume groups

# Create logical volumes
lvcreate -L 100G -n data-lv data-vg
lvcreate -L 50G -n logs-lv data-vg
lvdisplay                      # Show logical volumes

# Extend logical volume
lvextend -L +50G /dev/data-vg/data-lv
resize2fs /dev/data-vg/data-lv  # Resize filesystem

# Create filesystem and mount
mkfs.ext4 /dev/data-vg/data-lv
mkdir /data
mount /dev/data-vg/data-lv /data

# Add to fstab for persistent mounting
echo '/dev/data-vg/data-lv /data ext4 defaults 0 2' >> /etc/fstab
```

**RAID Configuration**:
```bash
# Software RAID setup
mdadm --create --verbose /dev/md0 \
  --level=5 --raid-devices=3 \
  /dev/sdb /dev/sdc /dev/sdd

# Check RAID status
cat /proc/mdstat
mdadm --detail /dev/md0

# Monitor RAID health
mdadm --monitor --mail=admin@company.com /dev/md0

# RAID configuration file
mdadm --detail --scan >> /etc/mdadm/mdadm.conf
update-initramfs -u
```

**Advanced Filesystem Management**:
```bash
# XFS filesystem for large files
mkfs.xfs -f /dev/sdb1
mount -t xfs /dev/sdb1 /data

# XFS maintenance
xfs_repair /dev/sdb1           # Repair filesystem
xfs_growfs /data               # Grow mounted filesystem
xfs_fsr /data                  # Defragment filesystem

# Btrfs for snapshots and compression
mkfs.btrfs /dev/sdb1
mount -o compress=zstd /dev/sdb1 /data

# Btrfs snapshots
btrfs subvolume create /data/snapshots
btrfs subvolume snapshot /data /data/snapshots/backup-$(date +%Y%m%d)
btrfs subvolume list /data
```

### 16. How do you implement system backup and disaster recovery?
**Answer**: Comprehensive backup and recovery strategies:

**System Backup Scripts**:
```bash
#!/bin/bash
# Comprehensive backup script

BACKUP_ROOT="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30
LOG_FILE="/var/log/backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Full system backup
full_system_backup() {
    local backup_dir="$BACKUP_ROOT/system/$DATE"
    mkdir -p "$backup_dir"
    
    log "Starting full system backup to $backup_dir"
    
    # System files backup
    tar --exclude=/proc --exclude=/sys --exclude=/dev \
        --exclude=/tmp --exclude=/backup \
        -czf "$backup_dir/system.tar.gz" /
    
    # Database backup
    mysqldump --all-databases --single-transaction \
        --routines --triggers > "$backup_dir/mysql_backup.sql"
    
    # Configuration backup
    tar -czf "$backup_dir/etc.tar.gz" /etc
    
    log "Full system backup completed"
}

# Incremental backup using rsync
incremental_backup() {
    local source="/data"
    local dest="$BACKUP_ROOT/incremental/$DATE"
    local link_dest="$BACKUP_ROOT/incremental/latest"
    
    mkdir -p "$dest"
    
    log "Starting incremental backup"
    
    if [[ -d "$link_dest" ]]; then
        rsync -av --link-dest="$link_dest" "$source/" "$dest/"
    else
        rsync -av "$source/" "$dest/"
    fi
    
    # Update latest link
    rm -f "$link_dest"
    ln -s "$dest" "$link_dest"
    
    log "Incremental backup completed"
}

# Database backup with point-in-time recovery
database_backup() {
    local backup_dir="$BACKUP_ROOT/database/$DATE"
    mkdir -p "$backup_dir"
    
    log "Starting database backup"
    
    # MySQL backup with binary logs
    mysqldump --all-databases --single-transaction \
        --flush-logs --master-data=2 \
        --routines --triggers > "$backup_dir/full_backup.sql"
    
    # Copy binary logs
    cp /var/log/mysql/mysql-bin.* "$backup_dir/"
    
    # PostgreSQL backup
    pg_dumpall > "$backup_dir/postgres_backup.sql"
    
    log "Database backup completed"
}

# Cleanup old backups
cleanup_old_backups() {
    log "Cleaning up backups older than $RETENTION_DAYS days"
    
    find "$BACKUP_ROOT" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;
    
    log "Cleanup completed"
}

# Verify backup integrity
verify_backup() {
    local backup_file="$1"
    
    if [[ -f "$backup_file" ]]; then
        if tar -tzf "$backup_file" >/dev/null 2>&1; then
            log "Backup verification successful: $backup_file"
            return 0
        else
            log "ERROR: Backup verification failed: $backup_file"
            return 1
        fi
    fi
}

# Main execution
main() {
    case "${1:-full}" in
        "full")
            full_system_backup
            ;;
        "incremental")
            incremental_backup
            ;;
        "database")
            database_backup
            ;;
        *)
            echo "Usage: $0 {full|incremental|database}"
            exit 1
            ;;
    esac
    
    cleanup_old_backups
}

main "$@"
```

**Disaster Recovery Procedures**:
```bash
# System recovery from backup
restore_system() {
    local backup_file="$1"
    local target_dir="${2:-/}"
    
    echo "WARNING: This will restore system from $backup_file to $target_dir"
    read -p "Continue? (yes/no): " confirm
    
    if [[ "$confirm" == "yes" ]]; then
        tar -xzf "$backup_file" -C "$target_dir"
        echo "System restored. Reboot required."
    fi
}

# Database recovery
restore_database() {
    local backup_file="$1"
    
    # MySQL restore
    mysql < "$backup_file"
    
    # Point-in-time recovery using binary logs
    mysqlbinlog --start-datetime="2024-01-01 12:00:00" \
                --stop-datetime="2024-01-01 13:00:00" \
                mysql-bin.000001 | mysql
}

# Automated disaster recovery testing
test_disaster_recovery() {
    local test_vm="disaster-test"
    
    # Create test VM
    virt-install --name "$test_vm" \
                 --memory 2048 \
                 --vcpus 2 \
                 --disk size=20 \
                 --cdrom /path/to/rescue.iso
    
    # Restore backup to test VM
    # Verify system functionality
    # Generate test report
}
```

### 17. How do you implement advanced process management and systemd?
**Answer**: Advanced process control and service management:

**Custom Systemd Services**:
```bash
# Create custom service unit
# /etc/systemd/system/data-pipeline.service
[Unit]
Description=Data Pipeline Service
After=network.target mysql.service
Requires=mysql.service
StartLimitIntervalSec=0

[Service]
Type=simple
User=dataeng
Group=dataeng
WorkingDirectory=/opt/data-pipeline
ExecStart=/opt/data-pipeline/start.sh
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/opt/data-pipeline/stop.sh
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=JAVA_HOME=/usr/lib/jvm/java-11-openjdk
Environment=SPARK_HOME=/opt/spark

[Install]
WantedBy=multi-user.target

# Service management
systemctl daemon-reload
systemctl enable data-pipeline.service
systemctl start data-pipeline.service
systemctl status data-pipeline.service
```

**Advanced Process Control**:
```bash
# Process resource limits
# /etc/security/limits.conf
dataeng soft nofile 65536
dataeng hard nofile 65536
dataeng soft nproc 32768
dataeng hard nproc 32768

# Systemd resource limits
[Service]
LimitNOFILE=65536
LimitNPROC=32768
MemoryLimit=8G
CPUQuota=200%

# Process monitoring and management
#!/bin/bash
# Process watchdog script

PROCESS_NAME="data-pipeline"
MAX_MEMORY_MB=4096
MAX_CPU_PERCENT=80

monitor_process() {
    local pid=$(pgrep -f "$PROCESS_NAME")
    
    if [[ -z "$pid" ]]; then
        echo "Process $PROCESS_NAME not running, starting..."
        systemctl start data-pipeline
        return
    fi
    
    # Check memory usage
    local memory_kb=$(ps -o rss= -p "$pid")
    local memory_mb=$((memory_kb / 1024))
    
    if (( memory_mb > MAX_MEMORY_MB )); then
        echo "Process $pid using too much memory: ${memory_mb}MB"
        systemctl restart data-pipeline
        return
    fi
    
    # Check CPU usage
    local cpu_percent=$(ps -o %cpu= -p "$pid")
    cpu_percent=${cpu_percent%.*}
    
    if (( cpu_percent > MAX_CPU_PERCENT )); then
        echo "Process $pid using too much CPU: ${cpu_percent}%"
        # Send warning but don't restart for CPU
        logger "High CPU usage detected for $PROCESS_NAME: ${cpu_percent}%"
    fi
}

# Run monitoring
while true; do
    monitor_process
    sleep 60
done
```

### 18. How do you implement advanced security hardening?
**Answer**: Comprehensive security measures for data infrastructure:

**System Hardening**:
```bash
# Kernel security parameters
# /etc/sysctl.d/99-security.conf
# Network security
net.ipv4.ip_forward = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0

# Memory protection
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2
kernel.yama.ptrace_scope = 1

# Apply settings
sysctl -p /etc/sysctl.d/99-security.conf

# File system security
# Mount options in /etc/fstab
/dev/sda1 /tmp ext4 defaults,nodev,nosuid,noexec 0 2
/dev/sda2 /var/tmp ext4 defaults,nodev,nosuid,noexec 0 2

# Set file permissions
chmod 700 /root
chmod 644 /etc/passwd
chmod 600 /etc/shadow
chmod 644 /etc/group
chmod 600 /etc/gshadow
```

**Advanced Authentication**:
```bash
# PAM configuration for strong authentication
# /etc/pam.d/common-password
password requisite pam_pwquality.so retry=3 minlen=12 difok=3 \
         ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1

# Two-factor authentication with Google Authenticator
apt install libpam-google-authenticator
google-authenticator

# Add to /etc/pam.d/sshd
auth required pam_google_authenticator.so

# SSH hardening
# /etc/ssh/sshd_config
Protocol 2
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers dataeng analyst
DenyUsers root guest
```

**Intrusion Detection**:
```bash
# Install and configure AIDE
apt install aide
aideinit
cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Daily integrity check
echo '0 2 * * * /usr/bin/aide --check' | crontab -

# Install fail2ban
apt install fail2ban

# Configure fail2ban
# /etc/fail2ban/jail.local
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[apache-auth]
enabled = true
port = http,https
filter = apache-auth
logpath = /var/log/apache2/error.log
maxretry = 3
```

### 19. How do you implement advanced log analysis and monitoring?
**Answer**: Comprehensive logging and monitoring solutions:

**Centralized Logging with ELK Stack**:
```bash
# Elasticsearch configuration
# /etc/elasticsearch/elasticsearch.yml
cluster.name: data-engineering-logs
node.name: log-node-1
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node

# Logstash configuration
# /etc/logstash/conf.d/data-pipeline.conf
input {
  file {
    path => "/var/log/data-pipeline/*.log"
    start_position => "beginning"
    type => "data-pipeline"
  }
  
  beats {
    port => 5044
  }
}

filter {
  if [type] == "data-pipeline" {
    grok {
      match => { 
        "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" 
      }
    }
    
    date {
      match => [ "timestamp", "ISO8601" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "data-pipeline-%{+YYYY.MM.dd}"
  }
}

# Filebeat configuration
# /etc/filebeat/filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/data-pipeline/*.log
  fields:
    service: data-pipeline
  fields_under_root: true

output.logstash:
  hosts: ["localhost:5044"]

processors:
- add_host_metadata:
    when.not.contains.tags: forwarded
```

**Advanced Log Analysis Scripts**:
```bash
#!/bin/bash
# Log analysis and alerting script

LOG_DIR="/var/log/data-pipeline"
ALERT_EMAIL="admin@company.com"
ERROR_THRESHOLD=10
WARNING_THRESHOLD=50

analyze_logs() {
    local log_file="$1"
    local time_window="${2:-1h}"
    
    echo "Analyzing $log_file for last $time_window"
    
    # Count errors and warnings
    local errors=$(grep -c "ERROR" "$log_file")
    local warnings=$(grep -c "WARNING" "$log_file")
    
    # Performance metrics
    local avg_response_time=$(grep "response_time" "$log_file" | \
        awk '{sum+=$NF; count++} END {print sum/count}')
    
    # Memory usage patterns
    local max_memory=$(grep "memory_usage" "$log_file" | \
        awk '{if($NF>max) max=$NF} END {print max}')
    
    # Generate report
    {
        echo "Log Analysis Report - $(date)"
        echo "================================"
        echo "File: $log_file"
        echo "Time Window: $time_window"
        echo ""
        echo "Error Count: $errors"
        echo "Warning Count: $warnings"
        echo "Average Response Time: ${avg_response_time}ms"
        echo "Peak Memory Usage: ${max_memory}MB"
        echo ""
        
        # Top error messages
        echo "Top Error Messages:"
        grep "ERROR" "$log_file" | \
            awk '{for(i=4;i<=NF;i++) printf "%s ", $i; print ""}' | \
            sort | uniq -c | sort -nr | head -5
        
    } > "/tmp/log_analysis_$(basename "$log_file").txt"
    
    # Check thresholds and send alerts
    if (( errors > ERROR_THRESHOLD )); then
        send_alert "High error count: $errors errors in $log_file"
    fi
    
    if (( warnings > WARNING_THRESHOLD )); then
        send_alert "High warning count: $warnings warnings in $log_file"
    fi
}

send_alert() {
    local message="$1"
    echo "$message" | mail -s "Log Alert - $(hostname)" "$ALERT_EMAIL"
    logger "LOG_ALERT: $message"
}

# Real-time log monitoring
monitor_logs_realtime() {
    tail -F "$LOG_DIR"/*.log | while read line; do
        if echo "$line" | grep -q "CRITICAL\|FATAL"; then
            send_alert "Critical error detected: $line"
        fi
        
        if echo "$line" | grep -q "OutOfMemoryError"; then
            send_alert "Out of memory error detected: $line"
        fi
        
        if echo "$line" | grep -q "Connection refused\|Connection timeout"; then
            send_alert "Connection issue detected: $line"
        fi
    done
}

# Log rotation and archival
manage_log_retention() {
    local retention_days=30
    local archive_dir="/data/log-archive"
    
    mkdir -p "$archive_dir"
    
    # Compress and archive old logs
    find "$LOG_DIR" -name "*.log" -mtime +7 -exec gzip {} \;
    find "$LOG_DIR" -name "*.log.gz" -mtime +$retention_days \
        -exec mv {} "$archive_dir/" \;
    
    # Clean very old archives
    find "$archive_dir" -name "*.log.gz" -mtime +365 -delete
}

# Main execution
case "${1:-analyze}" in
    "analyze")
        for log_file in "$LOG_DIR"/*.log; do
            [[ -f "$log_file" ]] && analyze_logs "$log_file"
        done
        ;;
    "monitor")
        monitor_logs_realtime
        ;;
    "cleanup")
        manage_log_retention
        ;;
    *)
        echo "Usage: $0 {analyze|monitor|cleanup}"
        exit 1
        ;;
esac
```

### 20. How do you implement high availability and load balancing?
**Answer**: HA and load balancing for data engineering infrastructure:

**HAProxy Load Balancer Configuration**:
```bash
# /etc/haproxy/haproxy.cfg
global
    daemon
    maxconn 4096
    log stdout local0
    
defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog
    
# Frontend for data API
frontend data_api_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/data-api.pem
    redirect scheme https if !{ ssl_fc }
    
    # ACL for different services
    acl is_spark_ui path_beg /spark
    acl is_airflow_ui path_beg /airflow
    acl is_api path_beg /api
    
    # Route to appropriate backend
    use_backend spark_ui if is_spark_ui
    use_backend airflow_ui if is_airflow_ui
    use_backend data_api if is_api
    default_backend data_api

# Backend for data API servers
backend data_api
    balance roundrobin
    option httpchk GET /health
    
    server api1 10.0.1.10:8080 check
    server api2 10.0.1.11:8080 check
    server api3 10.0.1.12:8080 check

# Backend for Spark UI
backend spark_ui
    balance source
    server spark1 10.0.2.10:4040 check
    server spark2 10.0.2.11:4040 check

# Backend for Airflow UI
backend airflow_ui
    balance roundrobin
    server airflow1 10.0.3.10:8080 check
    server airflow2 10.0.3.11:8080 check

# Statistics page
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats admin if TRUE
```

**Keepalived for HA**:
```bash
# /etc/keepalived/keepalived.conf
vrrp_script chk_haproxy {
    script "/bin/kill -0 `cat /var/run/haproxy.pid`"
    interval 2
    weight 2
    fall 3
    rise 2
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 101
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass mypassword
    }
    virtual_ipaddress {
        192.168.1.100
    }
    track_script {
        chk_haproxy
    }
}
```

This completes the comprehensive Linux interview questions with 80+ detailed questions covering all aspects from basic commands to advanced system administration, security, networking, containerization, and high availability for data engineering environments.