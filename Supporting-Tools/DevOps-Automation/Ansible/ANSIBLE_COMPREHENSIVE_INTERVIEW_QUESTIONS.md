# Ansible Interview Questions for Data Engineering & Infrastructure

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Playbook Development Questions (16-30)](#playbook-development-questions-16-30)
3. [Inventory & Variables Questions (31-45)](#inventory--variables-questions-31-45)
4. [Roles & Collections Questions (46-60)](#roles--collections-questions-46-60)
5. [Advanced Automation (61-75)](#advanced-automation-61-75)
6. [Security & Best Practices (76-90)](#security--best-practices-76-90)
7. [Integration & Scaling (91-100)](#integration--scaling-91-100)

---

## 🎯 **Introduction**

Ansible is an open-source automation platform for configuration management, application deployment, and infrastructure orchestration. For data engineers, Ansible provides essential capabilities for automating data infrastructure deployment, managing cluster configurations, and orchestrating complex data pipeline environments.

**Why Ansible is Critical for Data Engineers:**
- **Infrastructure as Code**: Declarative infrastructure management
- **Agentless Architecture**: No need to install agents on managed nodes
- **Idempotency**: Safe to run multiple times with consistent results
- **Integration**: Extensive modules for cloud providers and data tools
- **Scalability**: Manage thousands of nodes efficiently

---

## Core Concepts Questions (1-15)

### 1. What are the core components of Ansible and how do they work together?
**Answer**: 
Ansible's architecture consists of several key components that enable infrastructure automation.

**Core Components:**
- **Control Node**: Machine where Ansible is installed and runs
- **Managed Nodes**: Target machines managed by Ansible
- **Inventory**: List of managed nodes and their groupings
- **Playbooks**: YAML files defining automation tasks
- **Modules**: Units of code that perform specific tasks
- **Plugins**: Extend Ansible functionality
- **Facts**: System information gathered from managed nodes

```yaml
# Basic playbook structure
---
- name: Deploy Data Engineering Infrastructure
  hosts: data_cluster
  become: yes
  gather_facts: yes
  
  vars:
    spark_version: "3.4.0"
    hadoop_version: "3.3.4"
    java_version: "11"
    
  tasks:
    - name: Update system packages
      package:
        name: "*"
        state: latest
      when: ansible_os_family == "RedHat"
    
    - name: Install Java
      package:
        name: "java-{{ java_version }}-openjdk"
        state: present
    
    - name: Create spark user
      user:
        name: spark
        system: yes
        shell: /bin/bash
        home: /opt/spark
        create_home: yes
    
    - name: Download and install Spark
      unarchive:
        src: "https://archive.apache.org/dist/spark/spark-{{ spark_version }}/spark-{{ spark_version }}-bin-hadoop3.tgz"
        dest: /opt
        remote_src: yes
        owner: spark
        group: spark
        creates: "/opt/spark-{{ spark_version }}-bin-hadoop3"
    
    - name: Create Spark symlink
      file:
        src: "/opt/spark-{{ spark_version }}-bin-hadoop3"
        dest: /opt/spark
        state: link
        owner: spark
        group: spark
    
    - name: Configure Spark environment
      template:
        src: spark-env.sh.j2
        dest: /opt/spark/conf/spark-env.sh
        owner: spark
        group: spark
        mode: '0755'
      notify: restart spark
  
  handlers:
    - name: restart spark
      systemd:
        name: spark
        state: restarted
        enabled: yes
```

### 2. How do you manage inventory and host grouping for data infrastructure?
**Answer**: Inventory management is crucial for organizing and targeting different components of data infrastructure.

```ini
# Static inventory file (inventory/hosts)
[spark_masters]
spark-master-01 ansible_host=10.0.1.10
spark-master-02 ansible_host=10.0.1.11

[spark_workers]
spark-worker-01 ansible_host=10.0.1.20
spark-worker-02 ansible_host=10.0.1.21
spark-worker-03 ansible_host=10.0.1.22
spark-worker-04 ansible_host=10.0.1.23

[kafka_brokers]
kafka-broker-01 ansible_host=10.0.2.10 broker_id=1
kafka-broker-02 ansible_host=10.0.2.11 broker_id=2
kafka-broker-03 ansible_host=10.0.2.12 broker_id=3

[zookeeper]
zk-01 ansible_host=10.0.3.10 zk_id=1
zk-02 ansible_host=10.0.3.11 zk_id=2
zk-03 ansible_host=10.0.3.12 zk_id=3

[elasticsearch]
es-master-01 ansible_host=10.0.4.10 node_role=master
es-data-01 ansible_host=10.0.4.20 node_role=data
es-data-02 ansible_host=10.0.4.21 node_role=data

[databases]
postgres-primary ansible_host=10.0.5.10 db_role=primary
postgres-replica ansible_host=10.0.5.11 db_role=replica

# Group variables
[spark_cluster:children]
spark_masters
spark_workers

[kafka_cluster:children]
kafka_brokers
zookeeper

[data_infrastructure:children]
spark_cluster
kafka_cluster
elasticsearch
databases

# Host variables
[spark_masters:vars]
spark_master_port=7077
spark_master_webui_port=8080

[spark_workers:vars]
spark_worker_cores=4
spark_worker_memory=8g

[kafka_brokers:vars]
kafka_heap_size=4g
kafka_log_dirs=/data/kafka-logs

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/data-infrastructure.pem
```

```yaml
# Dynamic inventory using cloud providers
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
  - us-west-2

keyed_groups:
  # Group by instance type
  - key: instance_type
    prefix: type
  # Group by environment tag
  - key: tags.Environment
    prefix: env
  # Group by application tag
  - key: tags.Application
    prefix: app

filters:
  # Only include running instances
  instance-state-name: running
  # Only include instances with specific tags
  "tag:ManagedBy": ansible

compose:
  # Set ansible_host to private IP
  ansible_host: private_ip_address
  # Set custom variables from tags
  environment: tags.Environment
  application: tags.Application
  cluster_role: tags.ClusterRole
```

### 3. How do you implement idempotent operations in Ansible playbooks?
**Answer**: Idempotency ensures that playbooks can be run multiple times safely with consistent results.

```yaml
# Idempotent playbook examples
---
- name: Configure Kafka Cluster
  hosts: kafka_brokers
  become: yes
  
  tasks:
    # File operations - idempotent by default
    - name: Create Kafka directories
      file:
        path: "{{ item }}"
        state: directory
        owner: kafka
        group: kafka
        mode: '0755'
      loop:
        - /opt/kafka
        - /data/kafka-logs
        - /var/log/kafka
    
    # Package installation - idempotent
    - name: Install required packages
      package:
        name: "{{ item }}"
        state: present
      loop:
        - java-11-openjdk
        - wget
        - unzip
    
    # Service management - idempotent
    - name: Ensure Kafka service is running
      systemd:
        name: kafka
        state: started
        enabled: yes
    
    # Configuration with templates - idempotent
    - name: Configure Kafka server properties
      template:
        src: server.properties.j2
        dest: /opt/kafka/config/server.properties
        owner: kafka
        group: kafka
        mode: '0644'
        backup: yes
      notify: restart kafka
      register: kafka_config
    
    # Conditional tasks based on state
    - name: Check if Kafka topics exist
      shell: |
        /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
      register: existing_topics
      changed_when: false
    
    - name: Create Kafka topics
      shell: |
        /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
          --create --topic {{ item.name }} \
          --partitions {{ item.partitions }} \
          --replication-factor {{ item.replication_factor }}
      loop:
        - { name: "user-events", partitions: 12, replication_factor: 3 }
        - { name: "transaction-logs", partitions: 24, replication_factor: 3 }
        - { name: "system-metrics", partitions: 6, replication_factor: 2 }
      when: item.name not in existing_topics.stdout_lines
    
    # Database operations with proper checks
    - name: Check if database exists
      postgresql_query:
        login_host: "{{ db_host }}"
        login_user: "{{ db_admin_user }}"
        login_password: "{{ db_admin_password }}"
        query: "SELECT 1 FROM pg_database WHERE datname = '{{ db_name }}'"
      register: db_exists
      delegate_to: localhost
    
    - name: Create database
      postgresql_db:
        login_host: "{{ db_host }}"
        login_user: "{{ db_admin_user }}"
        login_password: "{{ db_admin_password }}"
        name: "{{ db_name }}"
        state: present
      when: db_exists.rowcount == 0
      delegate_to: localhost
    
    # Custom module for complex idempotent operations
    - name: Configure Spark cluster settings
      spark_config:
        config_file: /opt/spark/conf/spark-defaults.conf
        settings:
          spark.master: "spark://{{ groups['spark_masters'][0] }}:7077"
          spark.executor.memory: "{{ spark_executor_memory }}"
          spark.executor.cores: "{{ spark_executor_cores }}"
          spark.sql.adaptive.enabled: "true"
          spark.sql.adaptive.coalescePartitions.enabled: "true"
        backup: yes
      notify: restart spark workers

  handlers:
    - name: restart kafka
      systemd:
        name: kafka
        state: restarted
      when: kafka_config.changed
    
    - name: restart spark workers
      systemd:
        name: spark-worker
        state: restarted
      when: inventory_hostname in groups['spark_workers']
```

## Playbook Development Questions (16-30)

### 4. How do you structure complex data infrastructure playbooks with roles and includes?
**Answer**: Proper playbook organization using roles, includes, and modular design improves maintainability and reusability.

```yaml
# Main site.yml playbook
---
- import_playbook: playbooks/infrastructure.yml
- import_playbook: playbooks/data-services.yml
- import_playbook: playbooks/monitoring.yml
- import_playbook: playbooks/security.yml

# playbooks/infrastructure.yml
---
- name: Deploy Base Infrastructure
  hosts: all
  become: yes
  roles:
    - common
    - security-hardening
    - monitoring-agent

- name: Deploy Spark Cluster
  hosts: spark_cluster
  become: yes
  roles:
    - java
    - spark
  tags: [spark]

- name: Deploy Kafka Cluster
  hosts: kafka_cluster
  become: yes
  roles:
    - java
    - zookeeper
    - kafka
  tags: [kafka]

- name: Deploy Elasticsearch Cluster
  hosts: elasticsearch
  become: yes
  roles:
    - java
    - elasticsearch
  tags: [elasticsearch]
```

```yaml
# roles/spark/tasks/main.yml
---
- name: Include OS-specific variables
  include_vars: "{{ ansible_os_family }}.yml"

- name: Include installation tasks
  include_tasks: install.yml

- name: Include configuration tasks
  include_tasks: configure.yml

- name: Include service management tasks
  include_tasks: service.yml

- name: Include cluster setup tasks
  include_tasks: cluster.yml
  when: spark_cluster_mode | default(true)

# roles/spark/tasks/install.yml
---
- name: Create spark user
  user:
    name: "{{ spark_user }}"
    system: yes
    shell: /bin/bash
    home: "{{ spark_home }}"
    create_home: yes

- name: Download Spark
  get_url:
    url: "{{ spark_download_url }}"
    dest: "/tmp/spark-{{ spark_version }}.tgz"
    mode: '0644'
  register: spark_download

- name: Extract Spark
  unarchive:
    src: "/tmp/spark-{{ spark_version }}.tgz"
    dest: "{{ spark_install_dir }}"
    remote_src: yes
    owner: "{{ spark_user }}"
    group: "{{ spark_group }}"
    creates: "{{ spark_home }}/bin/spark-submit"
  when: spark_download.changed

- name: Create Spark directories
  file:
    path: "{{ item }}"
    state: directory
    owner: "{{ spark_user }}"
    group: "{{ spark_group }}"
    mode: '0755'
  loop:
    - "{{ spark_log_dir }}"
    - "{{ spark_work_dir }}"
    - "{{ spark_local_dir }}"

# roles/spark/tasks/configure.yml
---
- name: Configure Spark environment
  template:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    owner: "{{ spark_user }}"
    group: "{{ spark_group }}"
    mode: "{{ item.mode }}"
    backup: yes
  loop:
    - { src: "spark-env.sh.j2", dest: "{{ spark_home }}/conf/spark-env.sh", mode: "0755" }
    - { src: "spark-defaults.conf.j2", dest: "{{ spark_home }}/conf/spark-defaults.conf", mode: "0644" }
    - { src: "log4j.properties.j2", dest: "{{ spark_home }}/conf/log4j.properties", mode: "0644" }
  notify: restart spark services

- name: Configure Spark master
  template:
    src: spark-master.service.j2
    dest: /etc/systemd/system/spark-master.service
    mode: '0644'
  when: inventory_hostname in groups['spark_masters']
  notify:
    - reload systemd
    - restart spark master

- name: Configure Spark worker
  template:
    src: spark-worker.service.j2
    dest: /etc/systemd/system/spark-worker.service
    mode: '0644'
  when: inventory_hostname in groups['spark_workers']
  notify:
    - reload systemd
    - restart spark worker

# roles/spark/handlers/main.yml
---
- name: reload systemd
  systemd:
    daemon_reload: yes

- name: restart spark master
  systemd:
    name: spark-master
    state: restarted
    enabled: yes

- name: restart spark worker
  systemd:
    name: spark-worker
    state: restarted
    enabled: yes

- name: restart spark services
  systemd:
    name: "{{ item }}"
    state: restarted
  loop:
    - spark-master
    - spark-worker
  when: item in ansible_facts.services
```

### 5. How do you implement error handling and recovery in Ansible playbooks?
**Answer**: Robust error handling includes blocks, rescue, always sections, and proper failure management.

```yaml
# Error handling and recovery playbook
---
- name: Deploy Data Pipeline with Error Handling
  hosts: data_servers
  become: yes
  
  vars:
    max_retries: 3
    retry_delay: 30
    
  tasks:
    - name: Deploy application with error handling
      block:
        - name: Stop existing services
          systemd:
            name: "{{ item }}"
            state: stopped
          loop:
            - data-processor
            - data-collector
          ignore_errors: yes
        
        - name: Backup current configuration
          archive:
            path: /opt/data-app/config
            dest: "/tmp/config-backup-{{ ansible_date_time.epoch }}.tar.gz"
            format: gz
        
        - name: Download new application version
          get_url:
            url: "{{ app_download_url }}"
            dest: "/tmp/{{ app_package }}"
            timeout: 300
          register: download_result
          until: download_result is succeeded
          retries: "{{ max_retries }}"
          delay: "{{ retry_delay }}"
        
        - name: Deploy new version
          unarchive:
            src: "/tmp/{{ app_package }}"
            dest: /opt/data-app
            remote_src: yes
            owner: dataapp
            group: dataapp
          register: deployment_result
        
        - name: Update configuration
          template:
            src: "{{ item.src }}"
            dest: "{{ item.dest }}"
            owner: dataapp
            group: dataapp
            mode: '0644'
            backup: yes
          loop:
            - { src: "app.conf.j2", dest: "/opt/data-app/config/app.conf" }
            - { src: "database.conf.j2", dest: "/opt/data-app/config/database.conf" }
          register: config_result
        
        - name: Start services
          systemd:
            name: "{{ item }}"
            state: started
            enabled: yes
          loop:
            - data-collector
            - data-processor
          register: service_start
        
        - name: Verify service health
          uri:
            url: "http://localhost:{{ item.port }}/health"
            method: GET
            status_code: 200
          loop:
            - { service: "data-collector", port: 8080 }
            - { service: "data-processor", port: 8081 }
          register: health_check
          until: health_check is succeeded
          retries: 10
          delay: 30
        
        - name: Run smoke tests
          shell: |
            /opt/data-app/bin/smoke-test.sh
          register: smoke_test
          failed_when: smoke_test.rc != 0
        
      rescue:
        - name: Log deployment failure
          debug:
            msg: "Deployment failed. Starting rollback procedure."
        
        - name: Stop failed services
          systemd:
            name: "{{ item }}"
            state: stopped
          loop:
            - data-processor
            - data-collector
          ignore_errors: yes
        
        - name: Restore configuration backup
          unarchive:
            src: "/tmp/config-backup-{{ ansible_date_time.epoch }}.tar.gz"
            dest: /opt/data-app
            remote_src: yes
            owner: dataapp
            group: dataapp
          when: config_result is defined and config_result.changed
        
        - name: Rollback to previous version
          shell: |
            if [ -d /opt/data-app/previous ]; then
              rm -rf /opt/data-app/current
              mv /opt/data-app/previous /opt/data-app/current
            fi
          when: deployment_result is defined and deployment_result.changed
        
        - name: Restart services with previous version
          systemd:
            name: "{{ item }}"
            state: started
          loop:
            - data-collector
            - data-processor
        
        - name: Send failure notification
          mail:
            to: "{{ ops_email }}"
            subject: "Deployment Failed on {{ inventory_hostname }}"
            body: |
              Deployment failed on {{ inventory_hostname }}.
              Rollback completed successfully.
              
              Error details:
              {{ ansible_failed_result | default('Unknown error') }}
        
        - name: Fail the play after rollback
          fail:
            msg: "Deployment failed and rollback completed"
      
      always:
        - name: Cleanup temporary files
          file:
            path: "{{ item }}"
            state: absent
          loop:
            - "/tmp/{{ app_package }}"
            - "/tmp/config-backup-{{ ansible_date_time.epoch }}.tar.gz"
          ignore_errors: yes
        
        - name: Log deployment attempt
          lineinfile:
            path: /var/log/deployment.log
            line: "{{ ansible_date_time.iso8601 }} - Deployment attempt on {{ inventory_hostname }} - {{ 'SUCCESS' if ansible_failed_task is not defined else 'FAILED' }}"
            create: yes

    # Retry mechanism for critical operations
    - name: Database migration with retries
      block:
        - name: Run database migration
          shell: |
            /opt/data-app/bin/migrate-db.sh --env {{ environment }}
          register: migration_result
          until: migration_result.rc == 0
          retries: "{{ max_retries }}"
          delay: "{{ retry_delay }}"
      rescue:
        - name: Check database connectivity
          postgresql_ping:
            login_host: "{{ db_host }}"
            login_user: "{{ db_user }}"
            login_password: "{{ db_password }}"
          register: db_connectivity
        
        - name: Fail with detailed error
          fail:
            msg: |
              Database migration failed after {{ max_retries }} attempts.
              Database connectivity: {{ 'OK' if db_connectivity.is_available else 'FAILED' }}
              Last error: {{ migration_result.stderr | default('Unknown error') }}

    # Conditional error handling
    - name: Handle different types of failures
      shell: |
        /opt/data-app/bin/process-data.sh --batch {{ batch_id }}
      register: processing_result
      failed_when: false  # Don't fail immediately
      
    - name: Handle processing errors
      block:
        - name: Retry on temporary failure
          shell: |
            /opt/data-app/bin/process-data.sh --batch {{ batch_id }} --retry
          when: 
            - processing_result.rc == 2  # Temporary failure
            - processing_result.rc != 0
        
        - name: Skip on data not available
          debug:
            msg: "Skipping batch {{ batch_id }} - data not available"
          when: processing_result.rc == 3  # Data not available
        
        - name: Fail on critical error
          fail:
            msg: "Critical processing error: {{ processing_result.stderr }}"
          when: processing_result.rc == 1  # Critical error
```

This comprehensive Ansible interview questions file covers core concepts, playbook development, and error handling. Would you like me to continue with the remaining sections and then create comprehensive interview questions for other tools like Grafana, MLOps, etc.?