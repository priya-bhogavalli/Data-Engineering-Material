
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

### Q7: How do you create and use Ansible roles for data engineering infrastructure?
**Answer**: Roles provide reusable, modular automation for complex infrastructure components.

```yaml
# roles/kafka/tasks/main.yml
---
- name: Create kafka user
  user:
    name: kafka
    system: yes
    shell: /bin/bash
    home: /opt/kafka
    create_home: yes

- name: Install Java
  package:
    name: openjdk-11-jdk
    state: present

- name: Download Kafka
  get_url:
    url: "https://downloads.apache.org/kafka/{{ kafka_version }}/kafka_{{ kafka_scala_version }}-{{ kafka_version }}.tgz"
    dest: "/tmp/kafka_{{ kafka_scala_version }}-{{ kafka_version }}.tgz"
    timeout: 300

- name: Extract Kafka
  unarchive:
    src: "/tmp/kafka_{{ kafka_scala_version }}-{{ kafka_version }}.tgz"
    dest: /opt
    remote_src: yes
    owner: kafka
    group: kafka
    creates: "/opt/kafka_{{ kafka_scala_version }}-{{ kafka_version }}"

- name: Create Kafka symlink
  file:
    src: "/opt/kafka_{{ kafka_scala_version }}-{{ kafka_version }}"
    dest: /opt/kafka/current
    state: link
    owner: kafka
    group: kafka

- name: Create Kafka directories
  file:
    path: "{{ item }}"
    state: directory
    owner: kafka
    group: kafka
    mode: '0755'
  loop:
    - /opt/kafka/logs
    - /opt/kafka/config
    - "{{ kafka_log_dirs | join(' ') }}"

- name: Configure Kafka server properties
  template:
    src: server.properties.j2
    dest: /opt/kafka/config/server.properties
    owner: kafka
    group: kafka
    mode: '0644'
  notify: restart kafka

- name: Create Kafka systemd service
  template:
    src: kafka.service.j2
    dest: /etc/systemd/system/kafka.service
    mode: '0644'
  notify:
    - reload systemd
    - restart kafka

- name: Start and enable Kafka
  systemd:
    name: kafka
    state: started
    enabled: yes
    daemon_reload: yes
```

```yaml
# roles/spark/tasks/main.yml
---
- name: Create spark user
  user:
    name: spark
    system: yes
    shell: /bin/bash
    home: /opt/spark
    create_home: yes

- name: Download Spark
  get_url:
    url: "https://downloads.apache.org/spark/spark-{{ spark_version }}/spark-{{ spark_version }}-bin-hadoop{{ hadoop_version }}.tgz"
    dest: "/tmp/spark-{{ spark_version }}-bin-hadoop{{ hadoop_version }}.tgz"

- name: Extract Spark
  unarchive:
    src: "/tmp/spark-{{ spark_version }}-bin-hadoop{{ hadoop_version }}.tgz"
    dest: /opt
    remote_src: yes
    owner: spark
    group: spark

- name: Create Spark symlink
  file:
    src: "/opt/spark-{{ spark_version }}-bin-hadoop{{ hadoop_version }}"
    dest: /opt/spark/current
    state: link

- name: Configure Spark defaults
  template:
    src: spark-defaults.conf.j2
    dest: /opt/spark/current/conf/spark-defaults.conf
    owner: spark
    group: spark
  notify: restart spark

- name: Configure Spark environment
  template:
    src: spark-env.sh.j2
    dest: /opt/spark/current/conf/spark-env.sh
    owner: spark
    group: spark
    mode: '0755'
  notify: restart spark

- name: Create Spark master service
  template:
    src: spark-master.service.j2
    dest: /etc/systemd/system/spark-master.service
  when: spark_role == 'master'
  notify:
    - reload systemd
    - restart spark master

- name: Create Spark worker service
  template:
    src: spark-worker.service.j2
    dest: /etc/systemd/system/spark-worker.service
  when: spark_role == 'worker'
  notify:
    - reload systemd
    - restart spark worker
```

### Q8: How do you implement Ansible Galaxy and collections for data engineering?
**Answer**: Galaxy provides community roles and collections for reusable automation components.

```yaml
# requirements.yml
---
roles:
  - name: geerlingguy.docker
    version: 4.2.0
  - name: geerlingguy.postgresql
    version: 3.3.0
  - name: elastic.elasticsearch
    version: 7.17.0

collections:
  - name: community.general
    version: ">=4.0.0"
  - name: ansible.posix
    version: ">=1.3.0"
  - name: community.docker
    version: ">=2.0.0"
  - name: kubernetes.core
    version: ">=2.2.0"
  - name: amazon.aws
    version: ">=3.0.0"
  - name: community.postgresql
    version: ">=2.0.0"
```

```yaml
# data-platform-playbook.yml
---
- name: Deploy Data Engineering Platform
  hosts: data_platform
  become: yes
  
  pre_tasks:
    - name: Install required collections
      ansible.builtin.command:
        cmd: ansible-galaxy collection install -r requirements.yml
      delegate_to: localhost
      run_once: true
  
  roles:
    - role: geerlingguy.docker
      vars:
        docker_users:
          - "{{ ansible_user }}"
          - dataeng
    
    - role: geerlingguy.postgresql
      vars:
        postgresql_version: "13"
        postgresql_databases:
          - name: datawarehouse
            owner: dataeng
        postgresql_users:
          - name: dataeng
            password: "{{ vault_postgres_password }}"
            priv: "datawarehouse:ALL"
  
  tasks:
    - name: Deploy Kafka using community collection
      community.docker.docker_compose:
        project_src: /opt/kafka-cluster
        definition:
          version: '3.8'
          services:
            zookeeper:
              image: confluentinc/cp-zookeeper:7.0.0
              environment:
                ZOOKEEPER_CLIENT_PORT: 2181
                ZOOKEEPER_TICK_TIME: 2000
            
            kafka:
              image: confluentinc/cp-kafka:7.0.0
              depends_on:
                - zookeeper
              ports:
                - "9092:9092"
              environment:
                KAFKA_BROKER_ID: 1
                KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
                KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
                KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    
    - name: Create Kubernetes namespace for Spark
      kubernetes.core.k8s:
        name: spark-cluster
        api_version: v1
        kind: Namespace
        state: present
    
    - name: Deploy Spark on Kubernetes
      kubernetes.core.k8s:
        definition:
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: spark-master
            namespace: spark-cluster
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
                  image: bitnami/spark:3.2.0
                  env:
                  - name: SPARK_MODE
                    value: master
                  ports:
                  - containerPort: 7077
                  - containerPort: 8080
```

### Q9: How do you implement Ansible Vault for secure data engineering deployments?
**Answer**: Vault encrypts sensitive data like database passwords, API keys, and certificates.

```yaml
# Create encrypted variables file
# ansible-vault create group_vars/production/vault.yml

# vault.yml (encrypted content)
vault_database_passwords:
  postgres_admin: "P@ssw0rd123!"
  postgres_dataeng: "DataEng2023!"
  mysql_root: "MySQL_R00t!"

vault_api_keys:
  aws_access_key: "AKIAIOSFODNN7EXAMPLE"
  aws_secret_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  datadog_api_key: "1234567890abcdef1234567890abcdef"
  slack_webhook: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"

vault_ssl_certificates:
  private_key: |
    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
    -----END PRIVATE KEY-----
  certificate: |
    -----BEGIN CERTIFICATE-----
    MIIDXTCCAkWgAwIBAgIJAKoK/heBjcOuMA0GCSqGSIb3DQEBCwUA...
    -----END CERTIFICATE-----
```

```yaml
# group_vars/production/main.yml (unencrypted references)
---
# Database configuration
database_passwords:
  postgres_admin: "{{ vault_database_passwords.postgres_admin }}"
  postgres_dataeng: "{{ vault_database_passwords.postgres_dataeng }}"
  mysql_root: "{{ vault_database_passwords.mysql_root }}"

# API configuration
api_keys:
  aws_access_key: "{{ vault_api_keys.aws_access_key }}"
  aws_secret_key: "{{ vault_api_keys.aws_secret_key }}"
  datadog_api_key: "{{ vault_api_keys.datadog_api_key }}"
  slack_webhook: "{{ vault_api_keys.slack_webhook }}"

# SSL configuration
ssl_certificates:
  private_key: "{{ vault_ssl_certificates.private_key }}"
  certificate: "{{ vault_ssl_certificates.certificate }}"
```

```yaml
# secure-deployment.yml
---
- name: Secure Data Engineering Deployment
  hosts: production
  become: yes
  vars_files:
    - group_vars/production/vault.yml
  
  tasks:
    - name: Configure PostgreSQL with encrypted password
      postgresql_user:
        name: dataeng
        password: "{{ database_passwords.postgres_dataeng }}"
        priv: "datawarehouse:ALL"
        state: present
      no_log: true  # Prevent password logging
    
    - name: Create AWS credentials file
      template:
        src: aws_credentials.j2
        dest: /home/dataeng/.aws/credentials
        owner: dataeng
        group: dataeng
        mode: '0600'
      vars:
        aws_access_key_id: "{{ api_keys.aws_access_key }}"
        aws_secret_access_key: "{{ api_keys.aws_secret_key }}"
      no_log: true
    
    - name: Install SSL certificate
      copy:
        content: "{{ ssl_certificates.certificate }}"
        dest: /etc/ssl/certs/data-platform.crt
        mode: '0644'
    
    - name: Install SSL private key
      copy:
        content: "{{ ssl_certificates.private_key }}"
        dest: /etc/ssl/private/data-platform.key
        mode: '0600'
        owner: root
        group: root
      no_log: true
    
    - name: Configure monitoring with API key
      template:
        src: datadog.conf.j2
        dest: /etc/datadog-agent/datadog.yaml
        mode: '0640'
        owner: dd-agent
        group: dd-agent
      vars:
        datadog_api_key: "{{ api_keys.datadog_api_key }}"
      notify: restart datadog-agent
      no_log: true
```

### Q10: How do you implement Ansible for container orchestration and Kubernetes?
**Answer**: Ansible integrates with Docker and Kubernetes for container-based data engineering platforms.

```yaml
# docker-data-platform.yml
---
- name: Deploy Containerized Data Platform
  hosts: docker_hosts
  become: yes
  
  tasks:
    - name: Create data platform network
      community.docker.docker_network:
        name: data-platform
        driver: bridge
        ipam_config:
          - subnet: 172.20.0.0/16
    
    - name: Deploy PostgreSQL container
      community.docker.docker_container:
        name: postgres-db
        image: postgres:13
        state: started
        restart_policy: unless-stopped
        networks:
          - name: data-platform
        env:
          POSTGRES_DB: datawarehouse
          POSTGRES_USER: dataeng
          POSTGRES_PASSWORD: "{{ vault_postgres_password }}"
        volumes:
          - postgres_data:/var/lib/postgresql/data
          - /opt/postgres/init:/docker-entrypoint-initdb.d:ro
        ports:
          - "5432:5432"
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U dataeng"]
          interval: 30s
          timeout: 10s
          retries: 3
    
    - name: Deploy Redis container
      community.docker.docker_container:
        name: redis-cache
        image: redis:7-alpine
        state: started
        restart_policy: unless-stopped
        networks:
          - name: data-platform
        command: redis-server --appendonly yes
        volumes:
          - redis_data:/data
        ports:
          - "6379:6379"
    
    - name: Deploy Kafka cluster
      community.docker.docker_compose:
        project_name: kafka-cluster
        definition:
          version: '3.8'
          services:
            zookeeper:
              image: confluentinc/cp-zookeeper:7.0.0
              environment:
                ZOOKEEPER_CLIENT_PORT: 2181
                ZOOKEEPER_TICK_TIME: 2000
              volumes:
                - zk_data:/var/lib/zookeeper/data
                - zk_logs:/var/lib/zookeeper/log
            
            kafka-1:
              image: confluentinc/cp-kafka:7.0.0
              depends_on:
                - zookeeper
              environment:
                KAFKA_BROKER_ID: 1
                KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
                KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-1:9092
                KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
                KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
                KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 3
                KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 2
              volumes:
                - kafka1_data:/var/lib/kafka/data
            
            kafka-2:
              image: confluentinc/cp-kafka:7.0.0
              depends_on:
                - zookeeper
              environment:
                KAFKA_BROKER_ID: 2
                KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
                KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-2:9092
                KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
              volumes:
                - kafka2_data:/var/lib/kafka/data
          
          volumes:
            zk_data:
            zk_logs:
            kafka1_data:
            kafka2_data:
          
          networks:
            default:
              external:
                name: data-platform
```

```yaml
# kubernetes-spark-cluster.yml
---
- name: Deploy Spark Cluster on Kubernetes
  hosts: localhost
  connection: local
  
  tasks:
    - name: Create Spark namespace
      kubernetes.core.k8s:
        name: spark-cluster
        api_version: v1
        kind: Namespace
        state: present
    
    - name: Create Spark ConfigMap
      kubernetes.core.k8s:
        definition:
          apiVersion: v1
          kind: ConfigMap
          metadata:
            name: spark-config
            namespace: spark-cluster
          data:
            spark-defaults.conf: |
              spark.master                     spark://spark-master:7077
              spark.eventLog.enabled           true
              spark.eventLog.dir               /tmp/spark-events
              spark.history.fs.logDirectory    /tmp/spark-events
              spark.sql.adaptive.enabled       true
              spark.sql.adaptive.coalescePartitions.enabled true
    
    - name: Deploy Spark Master
      kubernetes.core.k8s:
        definition:
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: spark-master
            namespace: spark-cluster
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
                  image: bitnami/spark:3.3.0
                  env:
                  - name: SPARK_MODE
                    value: master
                  - name: SPARK_MASTER_HOST
                    value: "0.0.0.0"
                  - name: SPARK_MASTER_PORT
                    value: "7077"
                  - name: SPARK_MASTER_WEBUI_PORT
                    value: "8080"
                  ports:
                  - containerPort: 7077
                    name: spark
                  - containerPort: 8080
                    name: web-ui
                  volumeMounts:
                  - name: spark-config
                    mountPath: /opt/bitnami/spark/conf/spark-defaults.conf
                    subPath: spark-defaults.conf
                volumes:
                - name: spark-config
                  configMap:
                    name: spark-config
    
    - name: Create Spark Master Service
      kubernetes.core.k8s:
        definition:
          apiVersion: v1
          kind: Service
          metadata:
            name: spark-master
            namespace: spark-cluster
          spec:
            selector:
              app: spark-master
            ports:
            - name: spark
              port: 7077
              targetPort: 7077
            - name: web-ui
              port: 8080
              targetPort: 8080
            type: ClusterIP
    
    - name: Deploy Spark Workers
      kubernetes.core.k8s:
        definition:
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: spark-worker
            namespace: spark-cluster
          spec:
            replicas: 3
            selector:
              matchLabels:
                app: spark-worker
            template:
              metadata:
                labels:
                  app: spark-worker
              spec:
                containers:
                - name: spark-worker
                  image: bitnami/spark:3.3.0
                  env:
                  - name: SPARK_MODE
                    value: worker
                  - name: SPARK_MASTER_URL
                    value: spark://spark-master:7077
                  - name: SPARK_WORKER_MEMORY
                    value: "2g"
                  - name: SPARK_WORKER_CORES
                    value: "2"
                  resources:
                    requests:
                      memory: "2Gi"
                      cpu: "1"
                    limits:
                      memory: "4Gi"
                      cpu: "2"
```

### Q11: How do you implement Ansible for AWS data engineering infrastructure?
**Answer**: Ansible AWS modules automate cloud infrastructure provisioning and management.

```yaml
# aws-data-infrastructure.yml
---
- name: Provision AWS Data Engineering Infrastructure
  hosts: localhost
  connection: local
  gather_facts: no
  
  vars:
    aws_region: us-west-2
    environment: production
    project_name: data-platform
  
  tasks:
    - name: Create VPC for data platform
      amazon.aws.ec2_vpc_net:
        name: "{{ project_name }}-vpc"
        cidr_block: 10.0.0.0/16
        region: "{{ aws_region }}"
        tags:
          Environment: "{{ environment }}"
          Project: "{{ project_name }}"
        state: present
      register: vpc
    
    - name: Create public subnet
      amazon.aws.ec2_vpc_subnet:
        vpc_id: "{{ vpc.vpc.id }}"
        cidr: 10.0.1.0/24
        region: "{{ aws_region }}"
        az: "{{ aws_region }}a"
        tags:
          Name: "{{ project_name }}-public-subnet"
          Type: public
        state: present
      register: public_subnet
    
    - name: Create private subnets
      amazon.aws.ec2_vpc_subnet:
        vpc_id: "{{ vpc.vpc.id }}"
        cidr: "{{ item.cidr }}"
        region: "{{ aws_region }}"
        az: "{{ item.az }}"
        tags:
          Name: "{{ item.name }}"
          Type: private
        state: present
      loop:
        - { cidr: "10.0.2.0/24", az: "{{ aws_region }}a", name: "{{ project_name }}-private-subnet-a" }
        - { cidr: "10.0.3.0/24", az: "{{ aws_region }}b", name: "{{ project_name }}-private-subnet-b" }
      register: private_subnets
    
    - name: Create Internet Gateway
      amazon.aws.ec2_vpc_igw:
        vpc_id: "{{ vpc.vpc.id }}"
        region: "{{ aws_region }}"
        tags:
          Name: "{{ project_name }}-igw"
        state: present
      register: igw
    
    - name: Create security group for data services
      amazon.aws.ec2_security_group:
        name: "{{ project_name }}-data-services"
        description: Security group for data engineering services
        vpc_id: "{{ vpc.vpc.id }}"
        region: "{{ aws_region }}"
        rules:
          - proto: tcp
            ports:
              - 22
            cidr_ip: 10.0.0.0/16
            rule_desc: SSH access
          - proto: tcp
            ports:
              - 5432
            cidr_ip: 10.0.0.0/16
            rule_desc: PostgreSQL
          - proto: tcp
            ports:
              - 9092
            cidr_ip: 10.0.0.0/16
            rule_desc: Kafka
          - proto: tcp
            ports:
              - 7077
              - 8080
            cidr_ip: 10.0.0.0/16
            rule_desc: Spark
        tags:
          Environment: "{{ environment }}"
      register: security_group
    
    - name: Create RDS subnet group
      amazon.aws.rds_subnet_group:
        name: "{{ project_name }}-db-subnet-group"
        description: Subnet group for RDS instances
        subnets:
          - "{{ private_subnets.results[0].subnet.id }}"
          - "{{ private_subnets.results[1].subnet.id }}"
        region: "{{ aws_region }}"
        tags:
          Environment: "{{ environment }}"
      register: db_subnet_group
    
    - name: Create RDS PostgreSQL instance
      amazon.aws.rds_instance:
        db_instance_identifier: "{{ project_name }}-postgres"
        db_instance_class: db.t3.medium
        engine: postgres
        engine_version: "13.7"
        master_username: postgres
        master_user_password: "{{ vault_rds_password }}"
        allocated_storage: 100
        storage_type: gp2
        storage_encrypted: yes
        vpc_security_group_ids:
          - "{{ security_group.group_id }}"
        db_subnet_group_name: "{{ db_subnet_group.subnet_group.name }}"
        backup_retention_period: 7
        multi_az: yes
        region: "{{ aws_region }}"
        tags:
          Environment: "{{ environment }}"
          Service: database
      register: rds_instance
    
    - name: Create S3 bucket for data lake
      amazon.aws.s3_bucket:
        name: "{{ project_name }}-data-lake-{{ environment }}"
        region: "{{ aws_region }}"
        versioning: yes
        encryption: AES256
        tags:
          Environment: "{{ environment }}"
          Purpose: data-lake
      register: s3_bucket
    
    - name: Create EMR cluster
      amazon.aws.emr_cluster:
        name: "{{ project_name }}-emr-cluster"
        release_label: emr-6.4.0
        applications:
          - Name: Spark
          - Name: Hadoop
          - Name: Hive
          - Name: Zeppelin
        instance_groups:
          - Name: Master
            Market: ON_DEMAND
            InstanceRole: MASTER
            InstanceType: m5.xlarge
            InstanceCount: 1
          - Name: Core
            Market: ON_DEMAND
            InstanceRole: CORE
            InstanceType: m5.xlarge
            InstanceCount: 2
        ec2_attributes:
          KeyName: "{{ aws_key_name }}"
          InstanceProfile: EMR_EC2_DefaultRole
          SubnetId: "{{ private_subnets.results[0].subnet.id }}"
          EmrManagedMasterSecurityGroup: "{{ security_group.group_id }}"
          EmrManagedSlaveSecurityGroup: "{{ security_group.group_id }}"
        service_role: EMR_DefaultRole
        region: "{{ aws_region }}"
        tags:
          Environment: "{{ environment }}"
          Service: emr
      register: emr_cluster
    
    - name: Create Kinesis stream
      amazon.aws.kinesis_stream:
        name: "{{ project_name }}-data-stream"
        shards: 3
        retention_period: 168  # 7 days
        region: "{{ aws_region }}"
        tags:
          Environment: "{{ environment }}"
          Service: streaming
      register: kinesis_stream
```

### Q12: How do you implement Ansible testing and validation?
**Answer**: Ansible testing ensures playbook reliability through multiple testing approaches.

```yaml
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: ubuntu-20.04
    image: ubuntu:20.04
    pre_build_image: true
    privileged: true
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    command: "/lib/systemd/systemd"
  - name: centos-8
    image: centos:8
    pre_build_image: true
    privileged: true
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    command: "/usr/sbin/init"
provisioner:
  name: ansible
  config_options:
    defaults:
      interpreter_python: auto_silent
      callback_whitelist: profile_tasks, timer, yaml
    ssh_connection:
      pipelining: false
verifier:
  name: ansible
scenarios:
  - name: default
  - name: kafka-cluster
    platforms:
      - name: kafka-1
        groups:
          - kafka_cluster
      - name: kafka-2
        groups:
          - kafka_cluster
      - name: kafka-3
        groups:
          - kafka_cluster
```

```yaml
# molecule/default/converge.yml
---
- name: Converge
  hosts: all
  become: true
  
  pre_tasks:
    - name: Update package cache (Ubuntu)
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"
    
    - name: Update package cache (CentOS)
      yum:
        update_cache: yes
      when: ansible_os_family == "RedHat"
  
  roles:
    - role: kafka
      vars:
        kafka_version: "2.8.1"
        kafka_scala_version: "2.13"
        kafka_broker_id: "{{ groups['kafka_cluster'].index(inventory_hostname) + 1 }}"
```

```yaml
# molecule/default/verify.yml
---
- name: Verify
  hosts: all
  gather_facts: false
  
  tasks:
    - name: Check if Kafka service is running
      systemd:
        name: kafka
      register: kafka_service
    
    - name: Verify Kafka service is active
      assert:
        that:
          - kafka_service.status.ActiveState == "active"
        fail_msg: "Kafka service is not running"
    
    - name: Check Kafka port is listening
      wait_for:
        port: 9092
        host: "{{ ansible_default_ipv4.address }}"
        timeout: 30
    
    - name: Test Kafka broker connectivity
      uri:
        url: "http://{{ ansible_default_ipv4.address }}:9092"
        method: GET
      register: kafka_health
      failed_when: false
    
    - name: Verify Kafka configuration
      lineinfile:
        path: /opt/kafka/config/server.properties
        line: "broker.id={{ kafka_broker_id }}"
      check_mode: yes
      register: config_check
    
    - name: Assert configuration is correct
      assert:
        that:
          - not config_check.changed
        fail_msg: "Kafka configuration is incorrect"
```

```python
# tests/test_ansible_playbook.py
import pytest
import testinfra

@pytest.fixture(scope="module")
def host(request):
    return testinfra.get_host("ansible://kafka-1")

def test_kafka_user_exists(host):
    user = host.user("kafka")
    assert user.exists
    assert user.home == "/opt/kafka"

def test_kafka_service_running(host):
    service = host.service("kafka")
    assert service.is_running
    assert service.is_enabled

def test_kafka_port_listening(host):
    socket = host.socket("tcp://0.0.0.0:9092")
    assert socket.is_listening

def test_kafka_config_file(host):
    config = host.file("/opt/kafka/config/server.properties")
    assert config.exists
    assert config.user == "kafka"
    assert config.group == "kafka"
    assert config.mode == 0o644

def test_java_installed(host):
    java = host.run("java -version")
    assert java.rc == 0
    assert "openjdk" in java.stderr.lower()

def test_kafka_topics_command(host):
    cmd = host.run("/opt/kafka/current/bin/kafka-topics.sh --version")
    assert cmd.rc == 0
```

### Q13: How do you implement Ansible for monitoring and logging infrastructure?
**Answer**: Ansible automates deployment of monitoring stacks like ELK, Prometheus, and Grafana.

```yaml
# monitoring-stack.yml
---
- name: Deploy Monitoring and Logging Stack
  hosts: monitoring
  become: yes
  
  vars:
    elasticsearch_version: "7.17.0"
    kibana_version: "7.17.0"
    logstash_version: "7.17.0"
    prometheus_version: "2.35.0"
    grafana_version: "8.5.0"
  
  tasks:
    - name: Install Docker and Docker Compose
      include_role:
        name: geerlingguy.docker
      vars:
        docker_compose_version: "2.6.0"
    
    - name: Create monitoring directories
      file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
      loop:
        - /opt/monitoring
        - /opt/monitoring/elasticsearch/data
        - /opt/monitoring/prometheus/data
        - /opt/monitoring/grafana/data
        - /opt/monitoring/config
    
    - name: Create Elasticsearch configuration
      copy:
        content: |
          cluster.name: data-platform-logs
          node.name: elasticsearch-01
          path.data: /usr/share/elasticsearch/data
          network.host: 0.0.0.0
          discovery.type: single-node
          xpack.security.enabled: false
        dest: /opt/monitoring/config/elasticsearch.yml
    
    - name: Create Prometheus configuration
      template:
        src: prometheus.yml.j2
        dest: /opt/monitoring/config/prometheus.yml
      vars:
        scrape_configs:
          - job_name: 'prometheus'
            static_configs:
              - targets: ['localhost:9090']
          - job_name: 'node-exporter'
            static_configs:
              - targets: "{{ groups['data_servers'] | map('extract', hostvars, 'ansible_host') | map('regex_replace', '^(.*)$', '\\1:9100') | list }}"
          - job_name: 'kafka-exporter'
            static_configs:
              - targets: "{{ groups['kafka_cluster'] | map('extract', hostvars, 'ansible_host') | map('regex_replace', '^(.*)$', '\\1:9308') | list }}"
    
    - name: Create Grafana datasources configuration
      copy:
        content: |
          apiVersion: 1
          datasources:
            - name: Prometheus
              type: prometheus
              access: proxy
              url: http://prometheus:9090
              isDefault: true
            - name: Elasticsearch
              type: elasticsearch
              access: proxy
              url: http://elasticsearch:9200
              database: "logstash-*"
              timeField: "@timestamp"
        dest: /opt/monitoring/config/grafana-datasources.yml
    
    - name: Deploy monitoring stack with Docker Compose
      community.docker.docker_compose:
        project_name: monitoring
        project_src: /opt/monitoring
        definition:
          version: '3.8'
          
          services:
            elasticsearch:
              image: "docker.elastic.co/elasticsearch/elasticsearch:{{ elasticsearch_version }}"
              container_name: elasticsearch
              environment:
                - discovery.type=single-node
                - "ES_JAVA_OPTS=-Xms2g -Xmx2g"
              volumes:
                - ./config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml:ro
                - ./elasticsearch/data:/usr/share/elasticsearch/data
              ports:
                - "9200:9200"
              networks:
                - monitoring
            
            kibana:
              image: "docker.elastic.co/kibana/kibana:{{ kibana_version }}"
              container_name: kibana
              environment:
                - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
              ports:
                - "5601:5601"
              depends_on:
                - elasticsearch
              networks:
                - monitoring
            
            logstash:
              image: "docker.elastic.co/logstash/logstash:{{ logstash_version }}"
              container_name: logstash
              volumes:
                - ./config/logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
              ports:
                - "5044:5044"
                - "9600:9600"
              depends_on:
                - elasticsearch
              networks:
                - monitoring
            
            prometheus:
              image: "prom/prometheus:v{{ prometheus_version }}"
              container_name: prometheus
              command:
                - '--config.file=/etc/prometheus/prometheus.yml'
                - '--storage.tsdb.path=/prometheus'
                - '--web.console.libraries=/etc/prometheus/console_libraries'
                - '--web.console.templates=/etc/prometheus/consoles'
                - '--storage.tsdb.retention.time=200h'
                - '--web.enable-lifecycle'
              volumes:
                - ./config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
                - ./prometheus/data:/prometheus
              ports:
                - "9090:9090"
              networks:
                - monitoring
            
            grafana:
              image: "grafana/grafana:{{ grafana_version }}"
              container_name: grafana
              environment:
                - GF_SECURITY_ADMIN_PASSWORD={{ vault_grafana_password }}
                - GF_USERS_ALLOW_SIGN_UP=false
              volumes:
                - ./grafana/data:/var/lib/grafana
                - ./config/grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml:ro
              ports:
                - "3000:3000"
              depends_on:
                - prometheus
                - elasticsearch
              networks:
                - monitoring
          
          networks:
            monitoring:
              driver: bridge
          
          volumes:
            elasticsearch_data:
            prometheus_data:
            grafana_data:
```

### Q14: How do you implement Ansible for backup and disaster recovery?
**Answer**: Ansible automates backup procedures and disaster recovery workflows.

```yaml
# backup-strategy.yml
---
- name: Implement Backup and Disaster Recovery
  hosts: data_servers
  become: yes
  
  vars:
    backup_retention_days: 30
    backup_s3_bucket: "{{ project_name }}-backups-{{ environment }}"
    backup_schedule:
      databases: "0 2 * * *"  # Daily at 2 AM
      configs: "0 3 * * 0"   # Weekly on Sunday at 3 AM
      logs: "0 1 * * *"      # Daily at 1 AM
  
  tasks:
    - name: Install backup tools
      package:
        name:
          - postgresql-client
          - awscli
          - rsync
          - gzip
          - tar
        state: present
    
    - name: Create backup directories
      file:
        path: "{{ item }}"
        state: directory
        owner: backup
        group: backup
        mode: '0750'
      loop:
        - /opt/backups
        - /opt/backups/databases
        - /opt/backups/configs
        - /opt/backups/logs
        - /opt/backups/scripts
    
    - name: Create backup user
      user:
        name: backup
        system: yes
        shell: /bin/bash
        home: /opt/backups
        create_home: yes
    
    - name: Create database backup script
      template:
        src: backup_databases.sh.j2
        dest: /opt/backups/scripts/backup_databases.sh
        owner: backup
        group: backup
        mode: '0750'
      vars:
        databases:
          - name: datawarehouse
            host: "{{ rds_endpoint }}"
            port: 5432
            user: postgres
          - name: analytics
            host: localhost
            port: 5432
            user: postgres
    
    - name: Create configuration backup script
      copy:
        content: |
          #!/bin/bash
          set -euo pipefail
          
          BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
          BACKUP_DIR="/opt/backups/configs"
          S3_BUCKET="{{ backup_s3_bucket }}"
          
          # Create backup archive
          tar -czf "${BACKUP_DIR}/config_backup_${BACKUP_DATE}.tar.gz" \
              /etc/kafka \
              /etc/spark \
              /etc/postgresql \
              /opt/*/config \
              --exclude='*.log' \
              --exclude='*.pid'
          
          # Upload to S3
          aws s3 cp "${BACKUP_DIR}/config_backup_${BACKUP_DATE}.tar.gz" \
              "s3://${S3_BUCKET}/configs/config_backup_${BACKUP_DATE}.tar.gz"
          
          # Clean up old local backups
          find "${BACKUP_DIR}" -name "config_backup_*.tar.gz" -mtime +7 -delete
          
          echo "Configuration backup completed: config_backup_${BACKUP_DATE}.tar.gz"
        dest: /opt/backups/scripts/backup_configs.sh
        owner: backup
        group: backup
        mode: '0750'
    
    - name: Create disaster recovery script
      template:
        src: disaster_recovery.sh.j2
        dest: /opt/backups/scripts/disaster_recovery.sh
        owner: backup
        group: backup
        mode: '0750'
    
    - name: Schedule backup jobs
      cron:
        name: "{{ item.name }}"
        job: "{{ item.job }}"
        minute: "{{ item.minute }}"
        hour: "{{ item.hour }}"
        day: "{{ item.day | default('*') }}"
        weekday: "{{ item.weekday | default('*') }}"
        user: backup
      loop:
        - name: "Database backup"
          job: "/opt/backups/scripts/backup_databases.sh"
          minute: "0"
          hour: "2"
        - name: "Configuration backup"
          job: "/opt/backups/scripts/backup_configs.sh"
          minute: "0"
          hour: "3"
          weekday: "0"
        - name: "Log backup"
          job: "/opt/backups/scripts/backup_logs.sh"
          minute: "0"
          hour: "1"
    
    - name: Create backup monitoring script
      copy:
        content: |
          #!/bin/bash
          # Monitor backup job status and send alerts
          
          BACKUP_LOG="/var/log/backup.log"
          ALERT_EMAIL="ops-team@company.com"
          
          # Check if backups completed successfully
          if ! grep -q "backup completed" "$BACKUP_LOG"; then
              echo "Backup failure detected" | mail -s "ALERT: Backup Failed on $(hostname)" "$ALERT_EMAIL"
          fi
          
          # Check backup file sizes
          find /opt/backups -name "*.gz" -mtime -1 -size -1M -exec \
              echo "Small backup file detected: {}" \; | \
              mail -s "WARNING: Small backup files on $(hostname)" "$ALERT_EMAIL"
        dest: /opt/backups/scripts/monitor_backups.sh
        owner: backup
        group: backup
        mode: '0750'
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

