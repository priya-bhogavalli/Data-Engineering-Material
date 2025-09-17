# 🖥️ Systems & Infrastructure Practical Examples for Data Engineering

## 🐧 **Linux Administration for Data Engineers**

### **System Setup and Hardening**
```bash
#!/bin/bash
# data_server_setup.sh - Complete data server setup script

set -e

# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
    curl wget git vim htop iotop \
    build-essential software-properties-common \
    apt-transport-https ca-certificates gnupg lsb-release \
    python3 python3-pip python3-venv \
    postgresql-client redis-tools \
    jq unzip tree

# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Configure firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5432/tcp  # PostgreSQL
sudo ufw allow 6379/tcp  # Redis
sudo ufw allow 9090/tcp  # Prometheus
sudo ufw allow 3000/tcp  # Grafana

# System tuning for data workloads
cat << 'EOF' | sudo tee -a /etc/sysctl.conf
# Network optimizations
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 65536 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
net.core.netdev_max_backlog = 5000

# File system optimizations
fs.file-max = 2097152
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
EOF

# Apply sysctl changes
sudo sysctl -p

# Configure limits
cat << 'EOF' | sudo tee -a /etc/security/limits.conf
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768
EOF

# Create data directories
sudo mkdir -p /data/{raw,processed,logs,backups}
sudo chown -R $USER:$USER /data
sudo chmod -R 755 /data

# Setup log rotation for data applications
cat << 'EOF' | sudo tee /etc/logrotate.d/data-applications
/data/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
    postrotate
        systemctl reload rsyslog > /dev/null 2>&1 || true
    endscript
}
EOF

# Install monitoring tools
# Node Exporter for Prometheus
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
rm -rf node_exporter-1.6.1.linux-amd64*

# Create systemd service for node_exporter
cat << 'EOF' | sudo tee /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=nobody
Group=nobody
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

echo "Data server setup completed successfully!"
echo "Please reboot the system to apply all changes."
```

### **Automated Backup and Recovery**
```bash
#!/bin/bash
# backup_system.sh - Comprehensive backup solution

# Configuration
BACKUP_DIR="/data/backups"
S3_BUCKET="s3://my-data-backups"
RETENTION_DAYS=30
LOG_FILE="/data/logs/backup.log"
NOTIFICATION_EMAIL="admin@company.com"

# Database credentials
DB_HOST="localhost"
DB_NAME="datawarehouse"
DB_USER="backup_user"
DB_PASSWORD="secure_password"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Error handling
handle_error() {
    log "ERROR: $1"
    echo "Backup failed: $1" | mail -s "Backup Failure Alert" $NOTIFICATION_EMAIL
    exit 1
}

# Create backup directory
mkdir -p $BACKUP_DIR/$(date +%Y%m%d)
DAILY_BACKUP_DIR="$BACKUP_DIR/$(date +%Y%m%d)"

log "Starting backup process..."

# Database backup
log "Backing up PostgreSQL database..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME | gzip > $DAILY_BACKUP_DIR/database_$(date +%Y%m%d_%H%M%S).sql.gz
if [ $? -eq 0 ]; then
    log "Database backup completed successfully"
else
    handle_error "Database backup failed"
fi

# Application data backup
log "Backing up application data..."
tar -czf $DAILY_BACKUP_DIR/data_$(date +%Y%m%d_%H%M%S).tar.gz /data/processed /data/raw --exclude='*.tmp'
if [ $? -eq 0 ]; then
    log "Application data backup completed successfully"
else
    handle_error "Application data backup failed"
fi

# Configuration backup
log "Backing up system configurations..."
tar -czf $DAILY_BACKUP_DIR/config_$(date +%Y%m%d_%H%M%S).tar.gz \
    /etc/nginx \
    /etc/postgresql \
    /etc/redis \
    /etc/systemd/system \
    /home/$USER/.ssh \
    /home/$USER/.aws
if [ $? -eq 0 ]; then
    log "Configuration backup completed successfully"
else
    handle_error "Configuration backup failed"
fi

# Docker volumes backup
log "Backing up Docker volumes..."
docker run --rm -v /var/lib/docker/volumes:/volumes -v $DAILY_BACKUP_DIR:/backup alpine tar -czf /backup/docker_volumes_$(date +%Y%m%d_%H%M%S).tar.gz /volumes
if [ $? -eq 0 ]; then
    log "Docker volumes backup completed successfully"
else
    handle_error "Docker volumes backup failed"
fi

# Upload to S3
log "Uploading backups to S3..."
aws s3 sync $DAILY_BACKUP_DIR $S3_BUCKET/$(date +%Y%m%d)/ --storage-class STANDARD_IA
if [ $? -eq 0 ]; then
    log "S3 upload completed successfully"
else
    handle_error "S3 upload failed"
fi

# Cleanup old backups
log "Cleaning up old backups..."
find $BACKUP_DIR -type d -mtime +$RETENTION_DAYS -exec rm -rf {} +
aws s3 ls $S3_BUCKET/ | while read -r line; do
    backup_date=$(echo $line | awk '{print $2}' | tr -d '/')
    if [[ $backup_date =~ ^[0-9]{8}$ ]]; then
        days_old=$(( ($(date +%s) - $(date -d $backup_date +%s)) / 86400 ))
        if [ $days_old -gt $RETENTION_DAYS ]; then
            aws s3 rm $S3_BUCKET/$backup_date/ --recursive
            log "Removed old backup: $backup_date"
        fi
    fi
done

# Generate backup report
BACKUP_SIZE=$(du -sh $DAILY_BACKUP_DIR | cut -f1)
log "Backup process completed. Total size: $BACKUP_SIZE"

# Send success notification
echo "Backup completed successfully. Size: $BACKUP_SIZE" | mail -s "Backup Success" $NOTIFICATION_EMAIL

# Crontab entry (add to crontab -e):
# 0 2 * * * /path/to/backup_system.sh
```

## 🔒 **Security Implementation**

### **Comprehensive Security Setup**
```bash
#!/bin/bash
# security_hardening.sh - Security hardening for data servers

# Fail2ban installation and configuration
sudo apt install -y fail2ban

cat << 'EOF' | sudo tee /etc/fail2ban/jail.local
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
backend = systemd

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[postgresql]
enabled = true
port = 5432
filter = postgresql
logpath = /var/log/postgresql/postgresql-*.log
maxretry = 3
EOF

sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# SSH hardening
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

cat << 'EOF' | sudo tee /etc/ssh/sshd_config
# SSH Security Configuration
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Authentication
LoginGraceTime 60
PermitRootLogin no
StrictModes yes
MaxAuthTries 3
MaxSessions 4
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes

# Security options
X11Forwarding no
PrintMotd no
TCPKeepAlive yes
Compression delayed
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers dataeng
DenyUsers root

# Logging
SyslogFacility AUTH
LogLevel INFO
EOF

sudo systemctl restart sshd

# Install and configure OSSEC (Host-based Intrusion Detection)
wget -q -O - https://updates.atomicorp.com/installers/atomic | sudo bash
sudo yum install ossec-hids-server -y

# Configure OSSEC
cat << 'EOF' | sudo tee /var/ossec/etc/ossec.conf
<ossec_config>
  <global>
    <email_notification>yes</email_notification>
    <email_to>security@company.com</email_to>
    <smtp_server>localhost</smtp_server>
    <email_from>ossec@dataserver</email_from>
  </global>

  <rules>
    <include>rules_config.xml</include>
    <include>pam_rules.xml</include>
    <include>sshd_rules.xml</include>
    <include>telnetd_rules.xml</include>
    <include>syslog_rules.xml</include>
    <include>arpwatch_rules.xml</include>
    <include>symantec-av_rules.xml</include>
    <include>symantec-ws_rules.xml</include>
    <include>pix_rules.xml</include>
    <include>named_rules.xml</include>
    <include>smbd_rules.xml</include>
    <include>vsftpd_rules.xml</include>
    <include>pure-ftpd_rules.xml</include>
    <include>proftpd_rules.xml</include>
    <include>ms_ftpd_rules.xml</include>
    <include>ftpd_rules.xml</include>
    <include>hordeimp_rules.xml</include>
    <include>roundcube_rules.xml</include>
    <include>wordpress_rules.xml</include>
    <include>cimserver_rules.xml</include>
    <include>vpopmail_rules.xml</include>
    <include>vmpop3d_rules.xml</include>
    <include>courier_rules.xml</include>
    <include>web_rules.xml</include>
    <include>web_appsec_rules.xml</include>
    <include>apache_rules.xml</include>
    <include>nginx_rules.xml</include>
    <include>php_rules.xml</include>
    <include>mysql_rules.xml</include>
    <include>postgresql_rules.xml</include>
    <include>ids_rules.xml</include>
    <include>squid_rules.xml</include>
    <include>firewall_rules.xml</include>
    <include>cisco-ios_rules.xml</include>
    <include>netscreenfw_rules.xml</include>
    <include>sonicwall_rules.xml</include>
    <include>postfix_rules.xml</include>
    <include>sendmail_rules.xml</include>
    <include>imapd_rules.xml</include>
    <include>mailscanner_rules.xml</include>
    <include>dovecot_rules.xml</include>
    <include>ms-exchange_rules.xml</include>
    <include>racoon_rules.xml</include>
    <include>vpn_concentrator_rules.xml</include>
    <include>spamd_rules.xml</include>
    <include>msauth_rules.xml</include>
    <include>mcafee_av_rules.xml</include>
    <include>trend-osce_rules.xml</include>
    <include>ms-se_rules.xml</include>
    <include>zeus_rules.xml</include>
    <include>solaris_bsm_rules.xml</include>
    <include>vmware_rules.xml</include>
    <include>ms_dhcp_rules.xml</include>
    <include>asterisk_rules.xml</include>
    <include>ossec_rules.xml</include>
    <include>attack_rules.xml</include>
    <include>local_rules.xml</include>
  </rules>

  <syscheck>
    <frequency>79200</frequency>
    <directories check_all="yes">/etc,/usr/bin,/usr/sbin</directories>
    <directories check_all="yes">/bin,/sbin,/boot</directories>
    <directories check_all="yes">/data/processed</directories>
    <ignore>/etc/mtab</ignore>
    <ignore>/etc/hosts.deny</ignore>
    <ignore>/etc/mail/statistics</ignore>
    <ignore>/etc/random-seed</ignore>
    <ignore>/etc/adjtime</ignore>
    <ignore>/etc/httpd/logs</ignore>
    <ignore>/etc/utmpx</ignore>
    <ignore>/etc/wtmpx</ignore>
    <ignore>/etc/cups/certs</ignore>
    <ignore>/etc/dumpdates</ignore>
    <ignore>/etc/svc/volatile</ignore>
  </syscheck>

  <rootcheck>
    <rootkit_files>/var/ossec/etc/shared/rootkit_files.txt</rootkit_files>
    <rootkit_trojans>/var/ossec/etc/shared/rootkit_trojans.txt</rootkit_trojans>
  </rootcheck>

  <global>
    <white_list>127.0.0.1</white_list>
    <white_list>^localhost.localdomain$</white_list>
    <white_list>10.0.0.0/8</white_list>
  </global>

  <remote>
    <connection>secure</connection>
  </remote>

  <alerts>
    <log_alert_level>1</log_alert_level>
    <email_alert_level>7</email_alert_level>
  </alerts>

  <command>
    <name>host-deny</name>
    <executable>host-deny.sh</executable>
    <expect>srcip</expect>
    <timeout_allowed>yes</timeout_allowed>
  </command>

  <command>
    <name>firewall-drop</name>
    <executable>firewall-drop.sh</executable>
    <expect>srcip</expect>
    <timeout_allowed>yes</timeout_allowed>
  </command>

  <active-response>
    <command>host-deny</command>
    <location>local</location>
    <level>6</level>
    <timeout>600</timeout>
  </active-response>

  <active-response>
    <command>firewall-drop</command>
    <location>local</location>
    <level>6</level>
    <timeout>600</timeout>
  </active-response>

  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/messages</location>
  </localfile>

  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/secure</location>
  </localfile>

  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/maillog</location>
  </localfile>

  <localfile>
    <log_format>apache</log_format>
    <location>/var/log/nginx/access.log</location>
  </localfile>

  <localfile>
    <log_format>apache</log_format>
    <location>/var/log/nginx/error.log</location>
  </localfile>
</ossec_config>
EOF

sudo /var/ossec/bin/ossec-control start

# Install ClamAV antivirus
sudo apt install -y clamav clamav-daemon
sudo freshclam
sudo systemctl enable clamav-daemon
sudo systemctl start clamav-daemon

# Create antivirus scan script
cat << 'EOF' | sudo tee /usr/local/bin/daily_scan.sh
#!/bin/bash
SCAN_DIR="/data"
LOG_FILE="/var/log/clamav/daily_scan.log"
EMAIL="security@company.com"

echo "$(date): Starting daily antivirus scan" >> $LOG_FILE
clamscan -r $SCAN_DIR --log=$LOG_FILE --infected --remove

if [ $? -eq 1 ]; then
    echo "Malware detected and removed. Check log: $LOG_FILE" | mail -s "Malware Alert" $EMAIL
fi
EOF

sudo chmod +x /usr/local/bin/daily_scan.sh

# Add to crontab for daily execution
echo "0 3 * * * /usr/local/bin/daily_scan.sh" | sudo crontab -

echo "Security hardening completed!"
```

### **Network Security with pfSense**
```bash
# pfSense configuration script (to be run on pfSense firewall)

# Firewall rules for data engineering infrastructure
# WAN Rules (Block all by default, allow specific)
cat << 'EOF' > /tmp/wan_rules.txt
# Block all traffic from known bad IP ranges
block in quick on wan from <bogons> to any
block in quick on wan from <private_networks> to any

# Allow SSH from management network only
pass in on wan inet proto tcp from 203.0.113.0/24 to (wan) port 22 keep state

# Allow HTTPS for web interfaces
pass in on wan inet proto tcp from any to (wan) port 443 keep state

# Allow database connections from specific IPs
pass in on wan inet proto tcp from 198.51.100.0/24 to 10.0.1.100 port 5432 keep state

# Allow monitoring connections
pass in on wan inet proto tcp from 203.0.113.50 to 10.0.1.0/24 port 9090 keep state
pass in on wan inet proto tcp from 203.0.113.50 to 10.0.1.0/24 port 3000 keep state

# Block everything else
block in on wan all
EOF

# LAN Rules (Allow internal traffic with restrictions)
cat << 'EOF' > /tmp/lan_rules.txt
# Allow internal network communication
pass in on lan inet from 10.0.1.0/24 to 10.0.1.0/24 keep state

# Allow internet access for updates
pass in on lan inet from 10.0.1.0/24 to any port 80 keep state
pass in on lan inet from 10.0.1.0/24 to any port 443 keep state
pass in on lan inet from 10.0.1.0/24 to any port 53 keep state

# Allow NTP
pass in on lan inet proto udp from 10.0.1.0/24 to any port 123 keep state

# Block access to management interfaces from data servers
block in on lan inet from 10.0.1.100/32 to 10.0.1.1 port 80
block in on lan inet from 10.0.1.100/32 to 10.0.1.1 port 443

# Log denied traffic
block log all
EOF

# Traffic shaping for data workloads
cat << 'EOF' > /tmp/traffic_shaping.txt
# High priority for database traffic
altq on wan hfsc bandwidth 1Gb queue { db_queue, web_queue, default_queue }
queue db_queue hfsc(realtime 200Mb upperlimit 500Mb)
queue web_queue hfsc(realtime 100Mb upperlimit 300Mb)
queue default_queue hfsc(default)

# Assign traffic to queues
pass in on lan inet proto tcp from any to any port 5432 queue db_queue
pass in on lan inet proto tcp from any to any port 80 queue web_queue
pass in on lan inet proto tcp from any to any port 443 queue web_queue
EOF

# IDS/IPS Configuration (Suricata)
cat << 'EOF' > /tmp/suricata_rules.txt
# Custom rules for data engineering environment
alert tcp any any -> 10.0.1.0/24 5432 (msg:"PostgreSQL Brute Force Attempt"; flow:to_server,established; content:"authentication failed"; threshold:type both, track by_src, count 5, seconds 60; sid:1000001;)

alert tcp any any -> 10.0.1.0/24 6379 (msg:"Redis Unauthorized Access"; flow:to_server,established; content:"NOAUTH"; sid:1000002;)

alert tcp any any -> 10.0.1.0/24 any (msg:"Data Exfiltration Attempt"; flow:to_client,established; dsize:>1000000; threshold:type both, track by_src, count 10, seconds 60; sid:1000003;)

alert http any any -> 10.0.1.0/24 any (msg:"SQL Injection Attempt"; flow:to_server,established; content:"union select"; nocase; sid:1000004;)

alert tcp any any -> 10.0.1.0/24 22 (msg:"SSH Brute Force"; flow:to_server,established; threshold:type both, track by_src, count 10, seconds 60; sid:1000005;)
EOF

echo "pfSense configuration files created. Apply manually through web interface."
```

## 🔧 **Performance Monitoring and Optimization**

### **Comprehensive System Monitoring**
```python
# system_monitor.py - Advanced system monitoring for data infrastructure
import psutil
import time
import json
import requests
from datetime import datetime
import subprocess
import logging
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class SystemMonitor:
    def __init__(self, pushgateway_url="http://localhost:9091"):
        self.pushgateway_url = pushgateway_url
        self.registry = CollectorRegistry()
        
        # Define metrics
        self.cpu_usage = Gauge('system_cpu_usage_percent', 'CPU usage percentage', registry=self.registry)
        self.memory_usage = Gauge('system_memory_usage_percent', 'Memory usage percentage', registry=self.registry)
        self.disk_usage = Gauge('system_disk_usage_percent', 'Disk usage percentage', ['device'], registry=self.registry)
        self.network_io = Gauge('system_network_io_bytes', 'Network I/O bytes', ['direction'], registry=self.registry)
        self.disk_io = Gauge('system_disk_io_bytes', 'Disk I/O bytes', ['direction'], registry=self.registry)
        self.load_average = Gauge('system_load_average', 'System load average', ['period'], registry=self.registry)
        self.process_count = Gauge('system_process_count', 'Number of running processes', registry=self.registry)
        self.tcp_connections = Gauge('system_tcp_connections', 'Number of TCP connections', ['state'], registry=self.registry)
        
        # Database-specific metrics
        self.db_connections = Gauge('database_active_connections', 'Active database connections', ['database'], registry=self.registry)
        self.db_query_time = Gauge('database_avg_query_time_ms', 'Average query time in milliseconds', ['database'], registry=self.registry)
        
        # Application metrics
        self.app_response_time = Gauge('application_response_time_ms', 'Application response time', ['endpoint'], registry=self.registry)
        self.app_error_rate = Gauge('application_error_rate', 'Application error rate', ['service'], registry=self.registry)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def collect_system_metrics(self):
        """Collect basic system metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_usage.set(cpu_percent)
        
        # Memory usage
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.percent)
        
        # Disk usage
        for partition in psutil.disk_partitions():
            try:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = (disk_usage.used / disk_usage.total) * 100
                self.disk_usage.labels(device=partition.device).set(usage_percent)
            except PermissionError:
                continue
        
        # Network I/O
        network_io = psutil.net_io_counters()
        self.network_io.labels(direction='sent').set(network_io.bytes_sent)
        self.network_io.labels(direction='recv').set(network_io.bytes_recv)
        
        # Disk I/O
        disk_io = psutil.disk_io_counters()
        if disk_io:
            self.disk_io.labels(direction='read').set(disk_io.read_bytes)
            self.disk_io.labels(direction='write').set(disk_io.write_bytes)
        
        # Load average
        load_avg = psutil.getloadavg()
        self.load_average.labels(period='1min').set(load_avg[0])
        self.load_average.labels(period='5min').set(load_avg[1])
        self.load_average.labels(period='15min').set(load_avg[2])
        
        # Process count
        self.process_count.set(len(psutil.pids()))
        
        # TCP connections by state
        connections = psutil.net_connections()
        connection_states = {}
        for conn in connections:
            state = conn.status
            connection_states[state] = connection_states.get(state, 0) + 1
        
        for state, count in connection_states.items():
            self.tcp_connections.labels(state=state).set(count)
    
    def collect_database_metrics(self):
        """Collect database-specific metrics"""
        try:
            # PostgreSQL metrics
            import psycopg2
            
            conn = psycopg2.connect(
                host="localhost",
                database="datawarehouse",
                user="monitor_user",
                password="monitor_password"
            )
            cursor = conn.cursor()
            
            # Active connections
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
            active_connections = cursor.fetchone()[0]
            self.db_connections.labels(database='postgresql').set(active_connections)
            
            # Average query time
            cursor.execute("""
                SELECT COALESCE(AVG(mean_exec_time), 0) 
                FROM pg_stat_statements 
                WHERE calls > 0;
            """)
            avg_query_time = cursor.fetchone()[0]
            self.db_query_time.labels(database='postgresql').set(avg_query_time)
            
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error collecting database metrics: {e}")
    
    def collect_application_metrics(self):
        """Collect application-specific metrics"""
        endpoints = [
            'http://localhost:8080/health',
            'http://localhost:8080/api/data',
            'http://localhost:3000/api/health'
        ]
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(endpoint, timeout=5)
                response_time = (time.time() - start_time) * 1000
                
                self.app_response_time.labels(endpoint=endpoint).set(response_time)
                
                # Error rate (simplified)
                error_rate = 0 if response.status_code == 200 else 1
                self.app_error_rate.labels(service=endpoint.split('/')[2]).set(error_rate)
                
            except Exception as e:
                self.logger.error(f"Error checking endpoint {endpoint}: {e}")
                self.app_error_rate.labels(service=endpoint.split('/')[2]).set(1)
    
    def check_disk_space_alerts(self):
        """Check for disk space alerts"""
        alerts = []
        
        for partition in psutil.disk_partitions():
            try:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = (disk_usage.used / disk_usage.total) * 100
                
                if usage_percent > 90:
                    alerts.append({
                        'severity': 'critical',
                        'message': f"Disk usage critical on {partition.device}: {usage_percent:.1f}%"
                    })
                elif usage_percent > 80:
                    alerts.append({
                        'severity': 'warning',
                        'message': f"Disk usage high on {partition.device}: {usage_percent:.1f}%"
                    })
                    
            except PermissionError:
                continue
        
        return alerts
    
    def check_memory_alerts(self):
        """Check for memory alerts"""
        alerts = []
        memory = psutil.virtual_memory()
        
        if memory.percent > 90:
            alerts.append({
                'severity': 'critical',
                'message': f"Memory usage critical: {memory.percent:.1f}%"
            })
        elif memory.percent > 80:
            alerts.append({
                'severity': 'warning',
                'message': f"Memory usage high: {memory.percent:.1f}%"
            })
        
        return alerts
    
    def check_cpu_alerts(self):
        """Check for CPU alerts"""
        alerts = []
        cpu_percent = psutil.cpu_percent(interval=1)
        
        if cpu_percent > 90:
            alerts.append({
                'severity': 'critical',
                'message': f"CPU usage critical: {cpu_percent:.1f}%"
            })
        elif cpu_percent > 80:
            alerts.append({
                'severity': 'warning',
                'message': f"CPU usage high: {cpu_percent:.1f}%"
            })
        
        return alerts
    
    def send_alerts(self, alerts):
        """Send alerts to notification system"""
        if not alerts:
            return
        
        for alert in alerts:
            self.logger.warning(f"{alert['severity'].upper()}: {alert['message']}")
            
            # Send to Slack (example)
            try:
                webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
                payload = {
                    'text': f"🚨 {alert['severity'].upper()}: {alert['message']}",
                    'channel': '#alerts',
                    'username': 'System Monitor'
                }
                requests.post(webhook_url, json=payload, timeout=5)
            except Exception as e:
                self.logger.error(f"Failed to send Slack alert: {e}")
    
    def run_monitoring_cycle(self):
        """Run a complete monitoring cycle"""
        self.logger.info("Starting monitoring cycle...")
        
        # Collect all metrics
        self.collect_system_metrics()
        self.collect_database_metrics()
        self.collect_application_metrics()
        
        # Check for alerts
        all_alerts = []
        all_alerts.extend(self.check_disk_space_alerts())
        all_alerts.extend(self.check_memory_alerts())
        all_alerts.extend(self.check_cpu_alerts())
        
        # Send alerts if any
        self.send_alerts(all_alerts)
        
        # Push metrics to Prometheus
        try:
            push_to_gateway(self.pushgateway_url, job='system_monitor', registry=self.registry)
            self.logger.info("Metrics pushed to Prometheus successfully")
        except Exception as e:
            self.logger.error(f"Failed to push metrics to Prometheus: {e}")
        
        self.logger.info("Monitoring cycle completed")
    
    def run_continuous_monitoring(self, interval=60):
        """Run continuous monitoring"""
        self.logger.info(f"Starting continuous monitoring with {interval}s interval...")
        
        while True:
            try:
                self.run_monitoring_cycle()
                time.sleep(interval)
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring cycle: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    monitor = SystemMonitor()
    monitor.run_continuous_monitoring(interval=30)
```

### **Performance Optimization Script**
```bash
#!/bin/bash
# performance_optimization.sh - Optimize system for data workloads

# Database optimization (PostgreSQL)
optimize_postgresql() {
    echo "Optimizing PostgreSQL configuration..."
    
    # Calculate optimal settings based on system resources
    TOTAL_RAM=$(free -m | awk 'NR==2{printf "%.0f", $2}')
    SHARED_BUFFERS=$((TOTAL_RAM / 4))
    EFFECTIVE_CACHE_SIZE=$((TOTAL_RAM * 3 / 4))
    WORK_MEM=$((TOTAL_RAM / 64))
    
    cat << EOF | sudo tee -a /etc/postgresql/13/main/postgresql.conf
# Performance optimizations
shared_buffers = ${SHARED_BUFFERS}MB
effective_cache_size = ${EFFECTIVE_CACHE_SIZE}MB
work_mem = ${WORK_MEM}MB
maintenance_work_mem = 256MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
max_parallel_maintenance_workers = 4
EOF

    sudo systemctl restart postgresql
}

# Network optimization
optimize_network() {
    echo "Optimizing network settings..."
    
    cat << 'EOF' | sudo tee -a /etc/sysctl.conf
# Network performance tuning
net.core.rmem_default = 262144
net.core.rmem_max = 16777216
net.core.wmem_default = 262144
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 65536 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.core.netdev_max_backlog = 30000
net.ipv4.tcp_congestion_control = bbr
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_tw_reuse = 1
EOF

    sudo sysctl -p
}

# Disk I/O optimization
optimize_disk_io() {
    echo "Optimizing disk I/O..."
    
    # Set I/O scheduler for SSDs
    for disk in /sys/block/sd*; do
        if [ -f "$disk/queue/rotational" ] && [ "$(cat $disk/queue/rotational)" = "0" ]; then
            echo "noop" | sudo tee $disk/queue/scheduler
            echo "Setting noop scheduler for SSD: $(basename $disk)"
        fi
    done
    
    # Optimize mount options for data directories
    if ! grep -q "/data" /etc/fstab; then
        echo "# Data directory optimizations" | sudo tee -a /etc/fstab
        echo "/dev/sdb1 /data ext4 defaults,noatime,nodiratime,barrier=0 0 2" | sudo tee -a /etc/fstab
    fi
}

# Memory optimization
optimize_memory() {
    echo "Optimizing memory settings..."
    
    cat << 'EOF' | sudo tee -a /etc/sysctl.conf
# Memory optimization
vm.swappiness = 1
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
vm.dirty_expire_centisecs = 12000
vm.dirty_writeback_centisecs = 1500
vm.overcommit_memory = 1
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
EOF

    sudo sysctl -p
}

# CPU optimization
optimize_cpu() {
    echo "Optimizing CPU settings..."
    
    # Set CPU governor to performance
    echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
    
    # Disable CPU idle states for consistent performance
    sudo cpupower idle-set -D 2
    
    # Set CPU affinity for critical processes
    cat << 'EOF' | sudo tee /etc/systemd/system/postgresql-cpu-affinity.service
[Unit]
Description=Set PostgreSQL CPU Affinity
After=postgresql.service

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'taskset -cp 0-3 $(pgrep postgres | head -1)'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl enable postgresql-cpu-affinity.service
}

# Main execution
echo "Starting performance optimization..."

optimize_postgresql
optimize_network
optimize_disk_io
optimize_memory
optimize_cpu

echo "Performance optimization completed!"
echo "Please reboot the system to apply all changes."
```

## 🔧 **Quick Commands Reference**

### **System Administration**
```bash
# System information
hostnamectl                    # System info
lscpu                         # CPU info
free -h                       # Memory info
df -h                         # Disk usage
lsblk                         # Block devices
ip addr show                  # Network interfaces
ss -tuln                      # Listening ports

# Process management
ps aux | grep postgres        # Find PostgreSQL processes
htop                         # Interactive process viewer
iotop                        # I/O monitoring
nethogs                      # Network usage by process

# Log analysis
journalctl -u postgresql     # PostgreSQL logs
tail -f /var/log/syslog     # System logs
grep "ERROR" /data/logs/*.log # Application errors

# Performance monitoring
vmstat 1                     # Virtual memory stats
iostat -x 1                  # I/O statistics
sar -u 1 10                  # CPU usage over time
```

### **Security Commands**
```bash
# Firewall management
sudo ufw status              # UFW status
sudo ufw allow 5432/tcp      # Allow PostgreSQL
sudo ufw deny from 192.168.1.100  # Block specific IP

# Fail2ban management
sudo fail2ban-client status  # Check status
sudo fail2ban-client status sshd  # SSH jail status
sudo fail2ban-client unban 192.168.1.100  # Unban IP

# SSL/TLS certificates
openssl x509 -in cert.pem -text -noout  # View certificate
certbot renew --dry-run      # Test certificate renewal
```

---

*Updated: December 2024 | Focus: Production systems | Security: Enterprise-grade*