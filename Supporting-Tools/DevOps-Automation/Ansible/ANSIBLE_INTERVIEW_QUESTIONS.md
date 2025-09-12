
### Q1: What is Ansible and how does it differ from other configuration management tools?

**Answer:**
Ansible is an agentless configuration management, deployment, and orchestration tool that uses SSH for communication. It differs from other tools by being push-based, agentless, and using YAML for configuration.

**Key Differences:**
- **Agentless**: No need to install agents on target machines
- **Push-based**: Control node pushes configurations to targets
- **YAML syntax**: Human-readable configuration files
- **Idempotent**: Safe to run multiple times
- **SSH-based**: Uses existing SSH infrastructure

**Code Example:**
```yaml
# Simple Ansible playbook example
---
- name: Configure Data Engineering Environment
  hosts: data_servers
  become: yes
  
  tasks:
    - name: Install Python 3.9
      package:
        name: python3.9
        state: present
      
    - name: Install pip packages
      pip:
        name:
          - pandas
          - numpy
          - apache-airflow
          - psycopg2-binary
        executable: pip3.9
      
    - name: Create data directory
      file:
        path: /opt/data
        state: directory
        owner: dataeng
        group: dataeng
        mode: '0755'
      
    - name: Copy configuration file
      template:
        src: config.j2
        dest: /opt/data/config.yml
        owner: dataeng
        group: dataeng
        mode: '0644'
      notify: restart data service
  
  handlers:
    - name: restart data service
      systemd:
        name: data-pipeline
        state: restarted
```

```bash
# Running the playbook
ansible-playbook -i inventory.yml configure-data-env.yml

# Output:
PLAY [Configure Data Engineering Environment] **********************************

TASK [Gathering Facts] *********************************************************
ok: [data-server-01]
ok: [data-server-02]

TASK [Install Python 3.9] *****************************************************
changed: [data-server-01]
changed: [data-server-02]

TASK [Install pip packages] ***************************************************
changed: [data-server-01]
changed: [data-server-02]

TASK [Create data directory] ***************************************************
changed: [data-server-01]
changed: [data-server-02]

TASK [Copy configuration file] *************************************************
changed: [data-server-01]
changed: [data-server-02]

RUNNING HANDLER [restart data service] *****************************************
changed: [data-server-01]
changed: [data-server-02]

PLAY RECAP *********************************************************************
data-server-01             : ok=5    changed=5    unreachable=0    failed=0
data-server-02             : ok=5    changed=5    unreachable=0    failed=0
```

### Q2: Explain Ansible architecture and its core components.

**Answer:**
Ansible follows a simple architecture with a control node managing multiple managed nodes through modules and plugins.

**Core Components:**
- **Control Node**: Machine running Ansible commands
- **Managed Nodes**: Target machines being configured
- **Inventory**: List of managed nodes and their properties
- **Modules**: Units of work executed on managed nodes
- **Playbooks**: YAML files containing automation instructions
- **Plugins**: Extend Ansible functionality

**Code Example:**
```yaml
# ansible.cfg - Configuration file
[defaults]
inventory = ./inventory.yml
host_key_checking = False
remote_user = ansible
private_key_file = ~/.ssh/ansible_key
timeout = 30
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts_cache

[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False
```

```yaml
# inventory.yml - Inventory file
all:
  children:
    data_engineering:
      children:
        kafka_cluster:
          hosts:
            kafka-01:
              ansible_host: 10.0.1.10
              kafka_broker_id: 1
            kafka-02:
              ansible_host: 10.0.1.11
              kafka_broker_id: 2
            kafka-03:
              ansible_host: 10.0.1.12
              kafka_broker_id: 3
          vars:
            kafka_version: "2.8.1"
            kafka_port: 9092
        
        spark_cluster:
          hosts:
            spark-master:
              ansible_host: 10.0.2.10
              spark_role: master
            spark-worker-01:
              ansible_host: 10.0.2.11
              spark_role: worker
            spark-worker-02:
              ansible_host: 10.0.2.12
              spark_role: worker
          vars:
            spark_version: "3.2.0"
            spark_master_port: 7077
        
        databases:
          hosts:
            postgres-primary:
              ansible_host: 10.0.3.10
              postgres_role: primary
            postgres-replica:
              ansible_host: 10.0.3.11
              postgres_role: replica
          vars:
            postgres_version: "13"
            postgres_port: 5432

  vars:
    ansible_user: ubuntu
    ansible_ssh_private_key_file: ~/.ssh/data_eng_key
```

### Q3: How do you handle secrets and sensitive data in Ansible?

**Answer:**
Ansible provides multiple methods for handling sensitive data: Ansible Vault for encryption, external secret management integration, and environment variables.

**Code Example:**
```yaml
# Using Ansible Vault
# Create encrypted file
# ansible-vault create secrets.yml

# secrets.yml (encrypted content)
$ANSIBLE_VAULT;1.1;AES256
66386439653765386161653464336464643435396464643266373064366534...

# Decrypted content would be:
database_password: "super_secret_password"
api_key: "sk-1234567890abcdef"
ssl_private_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
  -----END PRIVATE KEY-----
```

```yaml
# playbook-with-secrets.yml
---
- name: Deploy Data Pipeline with Secrets
  hosts: data_servers
  vars_files:
    - secrets.yml  # Encrypted file
  
  tasks:
    - name: Create database connection config
      template:
        src: db_config.j2
        dest: /opt/app/config/database.yml
        mode: '0600'
        owner: app
        group: app
      vars:
        db_password: "{{ database_password }}"
    
    - name: Set environment variables
      lineinfile:
        path: /opt/app/.env
        line: "API_KEY={{ api_key }}"
        create: yes
        mode: '0600'
      no_log: true  # Prevent logging sensitive data
    
    - name: Install SSL certificate
      copy:
        content: "{{ ssl_private_key }}"
        dest: /etc/ssl/private/app.key
        mode: '0600'
        owner: root
        group: root
      no_log: true
```

```yaml
# Using external secret management (HashiCorp Vault)
---
- name: Retrieve secrets from Vault
  hosts: localhost
  tasks:
    - name: Get database credentials from Vault
      hashivault_read:
        secret: secret/data/database
        key: password
      register: vault_db_password
    
    - name: Get API key from Vault
      hashivault_read:
        secret: secret/data/api
        key: token
      register: vault_api_key

- name: Deploy with Vault secrets
  hosts: data_servers
  vars:
    db_password: "{{ hostvars['localhost']['vault_db_password']['value'] }}"
    api_token: "{{ hostvars['localhost']['vault_api_key']['value'] }}"
  
  tasks:
    - name: Configure application
      template:
        src: app_config.j2
        dest: /opt/app/config.yml
```

```bash
# Running playbook with vault
ansible-playbook -i inventory.yml --ask-vault-pass playbook-with-secrets.yml

# Or using vault password file
ansible-playbook -i inventory.yml --vault-password-file ~/.vault_pass playbook-with-secrets.yml

# Using environment variable for vault password
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass
ansible-playbook -i inventory.yml playbook-with-secrets.yml
```

## Playbooks and Tasks

### Q4: How do you write efficient and maintainable Ansible playbooks?

**Answer:**
Efficient playbooks use proper structure, error handling, conditionals, loops, and follow best practices for readability and reusability.

**Code Example:**
```yaml
# efficient-data-pipeline-deployment.yml
---
- name: Deploy Data Engineering Pipeline
  hosts: "{{ target_environment | default('staging') }}"
  gather_facts: yes
  become: yes
  
  vars:
    app_name: data-pipeline
    app_version: "{{ pipeline_version | default('latest') }}"
    deployment_timestamp: "{{ ansible_date_time.epoch }}"
    
  pre_tasks:
    - name: Validate deployment parameters
      assert:
        that:
          - app_version is defined
          - app_version != ""
          - target_environment in ['dev', 'staging', 'prod']
        fail_msg: "Invalid deployment parameters"
    
    - name: Check system requirements
      assert:
        that:
          - ansible_memtotal_mb >= 4096
          - ansible_processor_vcpus >= 2
        fail_msg: "System does not meet minimum requirements"
  
  tasks:
    - name: Create application user
      user:
        name: "{{ app_name }}"
        system: yes
        shell: /bin/bash
        home: "/opt/{{ app_name }}"
        create_home: yes
      tags: [setup, users]
    
    - name: Install system dependencies
      package:
        name: "{{ item }}"
        state: present
      loop:
        - python3.9
        - python3.9-pip
        - python3.9-venv
        - postgresql-client
        - redis-tools
      tags: [setup, packages]
    
    - name: Create directory structure
      file:
        path: "{{ item.path }}"
        state: directory
        owner: "{{ item.owner | default(app_name) }}"
        group: "{{ item.group | default(app_name) }}"
        mode: "{{ item.mode | default('0755') }}"
      loop:
        - { path: "/opt/{{ app_name }}/app" }
        - { path: "/opt/{{ app_name }}/config" }
        - { path: "/opt/{{ app_name }}/logs", mode: "0775" }
        - { path: "/opt/{{ app_name }}/data" }
        - { path: "/var/log/{{ app_name }}", owner: "root", group: "{{ app_name }}", mode: "0775" }
      tags: [setup, directories]
    
    - name: Download and extract application
      unarchive:
        src: "https://releases.company.com/{{ app_name }}/{{ app_version }}/{{ app_name }}-{{ app_version }}.tar.gz"
        dest: "/opt/{{ app_name }}/app"
        remote_src: yes
        owner: "{{ app_name }}"
        group: "{{ app_name }}"
        creates: "/opt/{{ app_name }}/app/{{ app_name }}-{{ app_version }}"
      notify: restart application
      tags: [deployment, download]
    
    - name: Create Python virtual environment
      pip:
        requirements: "/opt/{{ app_name }}/app/requirements.txt"
        virtualenv: "/opt/{{ app_name }}/venv"
        virtualenv_python: python3.9
      become_user: "{{ app_name }}"
      notify: restart application
      tags: [deployment, python]
    
    - name: Generate configuration from template
      template:
        src: "{{ item.src }}"
        dest: "{{ item.dest }}"
        owner: "{{ app_name }}"
        group: "{{ app_name }}"
        mode: "{{ item.mode | default('0644') }}"
        backup: yes
      loop:
        - { src: "config.yml.j2", dest: "/opt/{{ app_name }}/config/config.yml" }
        - { src: "logging.conf.j2", dest: "/opt/{{ app_name }}/config/logging.conf" }
        - { src: "systemd.service.j2", dest: "/etc/systemd/system/{{ app_name }}.service", mode: "0644" }
      notify:
        - reload systemd
        - restart application
      tags: [configuration]
    
    - name: Run database migrations
      command: >
        /opt/{{ app_name }}/venv/bin/python
        /opt/{{ app_name }}/app/manage.py migrate
      become_user: "{{ app_name }}"
      environment:
        CONFIG_FILE: "/opt/{{ app_name }}/config/config.yml"
      when: run_migrations | default(true)
      register: migration_result
      changed_when: "'No migrations to apply' not in migration_result.stdout"
      tags: [deployment, database]
    
    - name: Start and enable application service
      systemd:
        name: "{{ app_name }}"
        state: started
        enabled: yes
        daemon_reload: yes
      tags: [service]
    
    - name: Wait for application to be ready
      uri:
        url: "http://localhost:{{ app_port | default(8080) }}/health"
        method: GET
        status_code: 200
      retries: 30
      delay: 10
      register: health_check
      until: health_check.status == 200
      tags: [verification]
    
    - name: Create deployment marker
      copy:
        content: |
          Deployment Information:
          Version: {{ app_version }}
          Timestamp: {{ deployment_timestamp }}
          Deployed by: {{ ansible_user }}
          Host: {{ inventory_hostname }}
        dest: "/opt/{{ app_name }}/DEPLOYMENT_INFO"
        owner: "{{ app_name }}"
        group: "{{ app_name }}"
      tags: [deployment]
  
  handlers:
    - name: reload systemd
      systemd:
        daemon_reload: yes
    
    - name: restart application
      systemd:
        name: "{{ app_name }}"
        state: restarted
      listen: "restart application"
  
  post_tasks:
    - name: Verify deployment
      uri:
        url: "http://localhost:{{ app_port | default(8080) }}/version"
        method: GET
      register: version_check
      failed_when: app_version not in version_check.json.version
    
    - name: Send deployment notification
      mail:
        to: "devops-team@company.com"
        subject: "Deployment Complete: {{ app_name }} {{ app_version }}"
        body: |
          Deployment completed successfully:
          
          Application: {{ app_name }}
          Version: {{ app_version }}
          Environment: {{ target_environment }}
          Host: {{ inventory_hostname }}
          Deployed by: {{ ansible_user }}
          Timestamp: {{ ansible_date_time.iso8601 }}
      when: send_notifications | default(false)
      tags: [notification]
```

### Q5: How do you implement error handling and rollback strategies in Ansible?

**Answer:**
Ansible provides multiple mechanisms for error handling: failed_when, ignore_errors, rescue blocks, and custom rollback procedures.

**Code Example:**
```yaml
# error-handling-rollback.yml
---
- name: Deploy with Error Handling and Rollback
  hosts: web_servers
  vars:
    app_name: data-api
    backup_dir: "/opt/backups"
    rollback_enabled: true
  
  tasks:
    - name: Create backup directory
      file:
        path: "{{ backup_dir }}"
        state: directory
        mode: '0755'
      tags: [backup]
    
    - name: Backup current application
      block:
        - name: Check if application exists
          stat:
            path: "/opt/{{ app_name }}"
          register: app_exists
        
        - name: Create backup of current version
          archive:
            path: "/opt/{{ app_name }}"
            dest: "{{ backup_dir }}/{{ app_name }}-backup-{{ ansible_date_time.epoch }}.tar.gz"
            format: gz
          when: app_exists.stat.exists
          register: backup_created
        
        - name: Store backup path for rollback
          set_fact:
            backup_path: "{{ backup_created.dest }}"
          when: backup_created is succeeded
      
      rescue:
        - name: Backup failed
          debug:
            msg: "Backup creation failed, proceeding without backup"
          when: not rollback_enabled
        
        - name: Fail deployment if backup required
          fail:
            msg: "Backup creation failed and rollback is enabled"
          when: rollback_enabled
      
      tags: [backup]
    
    - name: Deploy new version
      block:
        - name: Download new application version
          get_url:
            url: "https://releases.company.com/{{ app_name }}/{{ app_version }}.tar.gz"
            dest: "/tmp/{{ app_name }}-{{ app_version }}.tar.gz"
            timeout: 300
          register: download_result
        
        - name: Stop application service
          systemd:
            name: "{{ app_name }}"
            state: stopped
          register: service_stopped
          failed_when: false  # Don't fail if service doesn't exist
        
        - name: Extract new version
          unarchive:
            src: "/tmp/{{ app_name }}-{{ app_version }}.tar.gz"
            dest: "/opt/"
            remote_src: yes
            owner: "{{ app_name }}"
            group: "{{ app_name }}"
          register: extraction_result
        
        - name: Update configuration
          template:
            src: config.yml.j2
            dest: "/opt/{{ app_name }}/config.yml"
            backup: yes
          register: config_updated
        
        - name: Install dependencies
          pip:
            requirements: "/opt/{{ app_name }}/requirements.txt"
            virtualenv: "/opt/{{ app_name }}/venv"
          register: deps_installed
        
        - name: Start application service
          systemd:
            name: "{{ app_name }}"
            state: started
            enabled: yes
          register: service_started
        
        - name: Verify application health
          uri:
            url: "http://localhost:8080/health"
            method: GET
            status_code: 200
          retries: 10
          delay: 5
          register: health_check
      
      rescue:
        - name: Deployment failed, initiating rollback
          debug:
            msg: "Deployment failed at task: {{ ansible_failed_task.name }}"
        
        - name: Rollback deployment
          include_tasks: rollback.yml
          when: rollback_enabled and backup_path is defined
        
        - name: Fail after rollback attempt
          fail:
            msg: "Deployment failed and rollback completed"
      
      tags: [deployment]
    
    - name: Post-deployment verification
      block:
        - name: Run application tests
          uri:
            url: "http://localhost:8080/api/test"
            method: GET
            status_code: 200
          register: api_test
        
        - name: Check application logs for errors
          shell: |
            tail -n 100 /var/log/{{ app_name }}/app.log | grep -i error | wc -l
          register: error_count
          changed_when: false
        
        - name: Fail if too many errors
          fail:
            msg: "Application has {{ error_count.stdout }} errors in logs"
          when: error_count.stdout | int > 5
        
        - name: Clean up old backups
          find:
            paths: "{{ backup_dir }}"
            patterns: "{{ app_name }}-backup-*.tar.gz"
            age: "7d"
          register: old_backups
        
        - name: Remove old backup files
          file:
            path: "{{ item.path }}"
            state: absent
          loop: "{{ old_backups.files }}"
          when: old_backups.files | length > 3
      
      rescue:
        - name: Post-deployment verification failed
          debug:
            msg: "Post-deployment checks failed, consider manual intervention"
        
        - name: Send alert notification
          mail:
            to: "ops-team@company.com"
            subject: "ALERT: Deployment verification failed for {{ app_name }}"
            body: |
              Deployment verification failed for {{ app_name }} on {{ inventory_hostname }}
              
              Failed task: {{ ansible_failed_task.name }}
              Error: {{ ansible_failed_result.msg }}
              
              Please investigate immediately.
      
      tags: [verification]

# rollback.yml - Separate rollback tasks
---
- name: Stop failed application
  systemd:
    name: "{{ app_name }}"
    state: stopped
  failed_when: false

- name: Remove failed deployment
  file:
    path: "/opt/{{ app_name }}"
    state: absent

- name: Restore from backup
  unarchive:
    src: "{{ backup_path }}"
    dest: "/opt/"
    remote_src: yes
  when: backup_path is defined

- name: Start restored application
  systemd:
    name: "{{ app_name }}"
    state: started

- name: Verify rollback success
  uri:
    url: "http://localhost:8080/health"
    method: GET
    status_code: 200
  retries: 5
  delay: 10
  register: rollback_health

- name: Rollback notification
  debug:
    msg: "Rollback completed successfully"
  when: rollback_health is succeeded
```

## Inventory and Variables

### Q6: How do you manage complex inventories and variable precedence in Ansible?

**Answer:**
Ansible provides flexible inventory management with dynamic inventories, group variables, host variables, and a well-defined variable precedence order.

**Code Example:**
```yaml
# inventory/production.yml - Static inventory
all:
  children:
    data_engineering:
      children:
        kafka_cluster:
          hosts:
            kafka-prod-01:
              ansible_host: 10.1.1.10
              kafka_broker_id: 1
              kafka_heap_size: "4g"
            kafka-prod-02:
              ansible_host: 10.1.1.11
              kafka_broker_id: 2
              kafka_heap_size: "4g"
            kafka-prod-03:
              ansible_host: 10.1.1.12
              kafka_broker_id: 3
              kafka_heap_size: "4g"
          vars:
            kafka_version: "2.8.1"
            kafka_port: 9092
            kafka_log_retention_hours: 168
            kafka_num_partitions: 12
        
        spark_cluster:
          hosts:
            spark-master-prod:
              ansible_host: 10.1.2.10
              spark_role: master
              spark_master_memory: "8g"
            spark-worker-prod-01:
              ansible_host: 10.1.2.11
              spark_role: worker
              spark_worker_memory: "16g"
              spark_worker_cores: 8
            spark-worker-prod-02:
              ansible_host: 10.1.2.12
              spark_role: worker
              spark_worker_memory: "16g"
              spark_worker_cores: 8
          vars:
            spark_version: "3.2.0"
            spark_master_port: 7077
            spark_history_server_port: 18080
        
        databases:
          children:
            postgres_primary:
              hosts:
                postgres-prod-primary:
                  ansible_host: 10.1.3.10
                  postgres_role: primary
                  postgres_max_connections: 200
            postgres_replicas:
              hosts:
                postgres-prod-replica-01:
                  ansible_host: 10.1.3.11
                  postgres_role: replica
                  postgres_max_connections: 100
                postgres-prod-replica-02:
                  ansible_host: 10.1.3.12
                  postgres_role: replica
                  postgres_max_connections: 100
          vars:
            postgres_version: "13"
            postgres_port: 5432
            postgres_shared_buffers: "2GB"
            postgres_effective_cache_size: "6GB"

  vars:
    environment: production
    ansible_user: ansible
    ansible_ssh_private_key_file: ~/.ssh/prod_key
    monitoring_enabled: true
    backup_enabled: true
    log_level: "INFO"
```

```python
# inventory/dynamic_aws.py - Dynamic inventory script
#!/usr/bin/env python3

import json
import boto3
import sys
from collections import defaultdict

def get_aws_inventory():
    """Generate dynamic inventory from AWS EC2 instances"""
    
    inventory = {
        '_meta': {
            'hostvars': {}
        },
        'all': {
            'children': ['ungrouped']
        }
    }
    
    # Initialize EC2 client
    ec2 = boto3.client('ec2', region_name='us-west-2')
    
    # Get all running instances
    response = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']},
            {'Name': 'tag:Environment', 'Values': ['production', 'staging']}
        ]
    )
    
    groups = defaultdict(lambda: {'hosts': [], 'vars': {}})
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Extract instance information
            instance_id = instance['InstanceId']
            private_ip = instance.get('PrivateIpAddress', '')
            public_ip = instance.get('PublicIpAddress', '')
            
            # Extract tags
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            
            # Determine hostname
            hostname = tags.get('Name', instance_id)
            
            # Group by various criteria
            environment = tags.get('Environment', 'unknown')
            service = tags.get('Service', 'unknown')
            role = tags.get('Role', 'unknown')
            
            # Add to groups
            groups[environment]['hosts'].append(hostname)
            groups[f"{service}_{environment}"]['hosts'].append(hostname)
            groups[f"{role}_{environment}"]['hosts'].append(hostname)
            
            # Set host variables
            inventory['_meta']['hostvars'][hostname] = {
                'ansible_host': private_ip or public_ip,
                'instance_id': instance_id,
                'instance_type': instance['InstanceType'],
                'availability_zone': instance['Placement']['AvailabilityZone'],
                'environment': environment,
                'service': service,
                'role': role,
                'tags': tags
            }
    
    # Add groups to inventory
    for group_name, group_data in groups.items():
        if group_data['hosts']:
            inventory[group_name] = group_data
    
    return inventory

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        print(json.dumps(get_aws_inventory(), indent=2))
    elif len(sys.argv) == 3 and sys.argv[1] == '--host':
        # Return empty dict for host-specific vars (handled in --list)
        print(json.dumps({}))
    else:
        print("Usage: %s --list or %s --host <hostname>" % (sys.argv[0], sys.argv[0]))
        sys.exit(1)
```

```yaml
# group_vars/all.yml - Global variables
---
# Common configuration for all hosts
ansible_python_interpreter: /usr/bin/python3
gather_timeout: 30

# Monitoring configuration
monitoring:
  enabled: "{{ monitoring_enabled | default(true) }}"
  agent: "datadog"
  tags:
    - "environment:{{ environment }}"
    - "managed_by:ansible"

# Backup configuration
backup:
  enabled: "{{ backup_enabled | default(true) }}"
  retention_days: 30
  s3_bucket: "company-backups-{{ environment }}"

# Security settings
security:
  ssh_port: 22
  fail2ban_enabled: true
  ufw_enabled: true
  
# Common packages
common_packages:
  - htop
  - vim
  - curl
  - wget
  - unzip
  - jq

# Logging configuration
logging:
  level: "{{ log_level | default('INFO') }}"
  max_file_size: "100MB"
  max_files: 10
```

```yaml
# group_vars/kafka_cluster.yml - Kafka-specific variables
---
kafka:
  version: "{{ kafka_version | default('2.8.1') }}"
  scala_version: "2.13"
  port: "{{ kafka_port | default(9092) }}"
  
  # JVM settings
  heap_size: "{{ kafka_heap_size | default('2g') }}"
  jvm_opts: >
    -XX:+UseG1GC
    -XX:MaxGCPauseMillis=20
    -XX:InitiatingHeapOccupancyPercent=35
    -XX:+ExplicitGCInvokesConcurrent
    -Djava.awt.headless=true
  
  # Kafka configuration
  config:
    num_network_threads: 8
    num_io_threads: 8
    socket_send_buffer_bytes: 102400
    socket_receive_buffer_bytes: 102400
    socket_request_max_bytes: 104857600
    
    log_retention_hours: "{{ kafka_log_retention_hours | default(168) }}"
    log_segment_bytes: 1073741824
    log_retention_check_interval_ms: 300000
    
    num_partitions: "{{ kafka_num_partitions | default(3) }}"
    default_replication_factor: 3
    min_insync_replicas: 2
    
    zookeeper_connect: "{{ groups['zookeeper'] | map('extract', hostvars, 'ansible_host') | map('regex_replace', '^(.*)$', '\\1:2181') | join(',') }}"

# Monitoring specific to Kafka
kafka_monitoring:
  jmx_port: 9999
  metrics_reporters: "io.confluent.metrics.reporter.ConfluentMetricsReporter"
  
# Security settings for Kafka
kafka_security:
  ssl_enabled: "{{ environment == 'production' }}"
  sasl_enabled: "{{ environment == 'production' }}"
  acl_enabled: "{{ environment == 'production' }}"
```

```yaml
# host_vars/kafka-prod-01.yml - Host-specific variables
---
# Host-specific overrides
kafka_broker_id: 1
kafka_heap_size: "6g"  # Override group default

# Network configuration
network_interfaces:
  - name: eth0
    ip: "{{ ansible_host }}"
    netmask: "255.255.255.0"
    gateway: "10.1.1.1"

# Disk configuration
kafka_log_dirs:
  - /data/kafka-logs-1
  - /data/kafka-logs-2
  - /data/kafka-logs-3

# Mount points
mount_points:
  - device: /dev/nvme1n1
    path: /data
    fstype: xfs
    opts: "noatime,nodiratime"

# Host-specific monitoring
host_monitoring:
  disk_usage_threshold: 85
  memory_usage_threshold: 90
  load_average_threshold: 8.0
```

```yaml
# Variable precedence demonstration playbook
---
- name: Demonstrate Variable Precedence
  hosts: kafka_cluster
  vars:
    # Playbook variables (precedence 16)
    kafka_heap_size: "playbook_override"
    demo_var: "from_playbook"
  
  tasks:
    - name: Show variable sources and precedence
      debug:
        msg: |
          Variable Precedence Demonstration:
          
          1. kafka_heap_size (should be host_vars override): {{ kafka_heap_size }}
          2. kafka_version (from group_vars): {{ kafka_version }}
          3. environment (from inventory): {{ environment }}
          4. demo_var (from playbook vars): {{ demo_var }}
          5. ansible_host (from inventory host): {{ ansible_host }}
          
          Full variable precedence order (lowest to highest):
          1. command line values (for example, -u my_user, these are not variables)
          2. role defaults [1]
          3. inventory file or script group vars [2]
          4. inventory group_vars/all [3]
          5. playbook group_vars/all [3]
          6. inventory group_vars/* [3]
          7. playbook group_vars/* [3]
          8. inventory file or script host vars [2]
          9. inventory host_vars/* [3]
          10. playbook host_vars/* [3]
          11. host facts / cached set_facts [4]
          12. play vars
          13. play vars_prompt
          14. play vars_files
          15. role vars (defined in role/vars/main.yml)
          16. block vars (only for tasks in block)
          17. task vars (only for the task)
          18. include_vars
          19. set_facts / registered vars
          20. role (and include_role) params
          21. include params
          22. extra vars (always win precedence)
    
    - name: Set runtime facts
      set_fact:
        runtime_var: "set at runtime"
        kafka_heap_size: "runtime_override"  # This will override previous values
    
    - name: Show updated variables
      debug:
        msg: |
          After set_fact:
          kafka_heap_size: {{ kafka_heap_size }}
          runtime_var: {{ runtime_var }}
```

---

## Key Takeaways

1. **Agentless Architecture**: Ansible uses SSH for communication without requiring agents
2. **Idempotency**: Safe to run playbooks multiple times with consistent results
3. **YAML Configuration**: Human-readable playbook and inventory definitions
4. **Variable Precedence**: Understanding the order helps manage complex configurations
5. **Error Handling**: Proper use of blocks, rescue, and rollback strategies
6. **Secret Management**: Ansible Vault and external secret integration for security
7. **Dynamic Inventories**: Automatically discover and manage infrastructure
8. **Modular Design**: Roles and collections promote reusability and maintainability

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*

