# Ansible Key Concepts

## 1. Ansible Fundamentals
**What is Ansible**: Agentless automation tool for configuration management, application deployment, and orchestration.

**Key Concepts**:
- **Playbooks**: YAML files defining automation tasks
- **Inventory**: List of managed hosts
- **Modules**: Reusable units of work
- **Tasks**: Individual actions to perform
- **Roles**: Organized collections of tasks, variables, and files

## 2. Inventory Management
```ini
# inventory/hosts.ini
[webservers]
web1.example.com ansible_host=192.168.1.10
web2.example.com ansible_host=192.168.1.11

[databases]
db1.example.com ansible_host=192.168.1.20
db2.example.com ansible_host=192.168.1.21

[dataprocessing]
spark-master ansible_host=10.0.1.10 ansible_user=ubuntu
spark-worker-[1:3] ansible_host=10.0.1.[11:13]

[all:vars]
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
```

```yaml
# inventory/group_vars/all.yml
common_packages:
  - git
  - curl
  - htop
  - python3-pip

# inventory/group_vars/dataprocessing.yml
spark_version: "3.4.0"
hadoop_version: "3.3.4"
java_home: "/usr/lib/jvm/java-11-openjdk-amd64"
```

## 3. Playbooks and Tasks
```yaml
# playbooks/setup-data-pipeline.yml
---
- name: Setup Data Processing Infrastructure
  hosts: dataprocessing
  become: yes
  
  vars:
    app_user: dataeng
    app_dir: /opt/data-pipeline
    
  tasks:
    - name: Create application user
      user:
        name: "{{ app_user }}"
        shell: /bin/bash
        create_home: yes
        
    - name: Install required packages
      apt:
        name: "{{ common_packages }}"
        state: present
        update_cache: yes
        
    - name: Create application directory
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        group: "{{ app_user }}"
        mode: '0755'
        
    - name: Download and extract Spark
      unarchive:
        src: "https://archive.apache.org/dist/spark/spark-{{ spark_version }}/spark-{{ spark_version }}-bin-hadoop3.tgz"
        dest: /opt
        remote_src: yes
        owner: "{{ app_user }}"
        creates: "/opt/spark-{{ spark_version }}-bin-hadoop3"
        
    - name: Create Spark symlink
      file:
        src: "/opt/spark-{{ spark_version }}-bin-hadoop3"
        dest: /opt/spark
        state: link
```

## 4. Roles and Organization
```yaml
# roles/postgresql/tasks/main.yml
---
- name: Install PostgreSQL
  apt:
    name:
      - postgresql
      - postgresql-contrib
      - python3-psycopg2
    state: present
    
- name: Start and enable PostgreSQL
  systemd:
    name: postgresql
    state: started
    enabled: yes
    
- name: Create database
  postgresql_db:
    name: "{{ db_name }}"
    state: present
  become_user: postgres
  
- name: Create database user
  postgresql_user:
    name: "{{ db_user }}"
    password: "{{ db_password }}"
    priv: "{{ db_name }}:ALL"
    state: present
  become_user: postgres
```

```yaml
# roles/postgresql/defaults/main.yml
---
db_name: analytics
db_user: dataeng
db_password: "{{ vault_db_password }}"
postgresql_version: "13"
```

```yaml
# playbooks/database-setup.yml
---
- name: Setup Database Servers
  hosts: databases
  become: yes
  roles:
    - postgresql
    - { role: backup, when: environment == "production" }
```

## 5. Templates and Variables
```yaml
# templates/spark-defaults.conf.j2
spark.master                     {{ spark_master_url }}
spark.eventLog.enabled           true
spark.eventLog.dir               {{ spark_event_log_dir }}
spark.sql.warehouse.dir          {{ spark_warehouse_dir }}
spark.executor.memory            {{ spark_executor_memory }}
spark.executor.cores             {{ spark_executor_cores }}
spark.driver.memory              {{ spark_driver_memory }}
spark.sql.adaptive.enabled       true
spark.sql.adaptive.coalescePartitions.enabled true

{% if environment == "production" %}
spark.dynamicAllocation.enabled  true
spark.dynamicAllocation.minExecutors 2
spark.dynamicAllocation.maxExecutors {{ spark_max_executors }}
{% endif %}
```

```yaml
# Using templates in tasks
- name: Configure Spark defaults
  template:
    src: spark-defaults.conf.j2
    dest: /opt/spark/conf/spark-defaults.conf
    owner: "{{ app_user }}"
    group: "{{ app_user }}"
    mode: '0644'
  notify: restart spark
```

## 6. Handlers and Notifications
```yaml
# roles/apache/handlers/main.yml
---
- name: restart apache
  systemd:
    name: apache2
    state: restarted
    
- name: reload apache
  systemd:
    name: apache2
    state: reloaded
    
- name: restart spark
  systemd:
    name: spark-master
    state: restarted
  when: inventory_hostname in groups['spark_masters']
```

```yaml
# Using handlers in tasks
- name: Update Apache configuration
  template:
    src: apache.conf.j2
    dest: /etc/apache2/sites-available/default.conf
  notify:
    - reload apache
    - restart spark
```

## 7. Conditionals and Loops
```yaml
# Conditional execution
- name: Install Docker on Ubuntu
  apt:
    name: docker.io
    state: present
  when: ansible_distribution == "Ubuntu"
  
- name: Install Docker on CentOS
  yum:
    name: docker
    state: present
  when: ansible_distribution == "CentOS"

# Loops
- name: Create multiple databases
  postgresql_db:
    name: "{{ item }}"
    state: present
  loop:
    - analytics
    - reporting
    - staging
  become_user: postgres
  
- name: Install Python packages
  pip:
    name: "{{ item.name }}"
    version: "{{ item.version | default(omit) }}"
  loop:
    - { name: pandas, version: "1.5.0" }
    - { name: numpy }
    - { name: boto3, version: "1.26.0" }
```

## 8. Vault and Security
```bash
# Create encrypted variables
ansible-vault create group_vars/all/vault.yml
ansible-vault edit group_vars/all/vault.yml

# Encrypt existing file
ansible-vault encrypt secrets.yml

# Run playbook with vault
ansible-playbook -i inventory/hosts.ini playbooks/deploy.yml --ask-vault-pass
ansible-playbook -i inventory/hosts.ini playbooks/deploy.yml --vault-password-file ~/.vault_pass
```

```yaml
# group_vars/all/vault.yml (encrypted)
vault_db_password: "super_secret_password"
vault_api_key: "secret_api_key_12345"
vault_ssl_cert: |
  -----BEGIN CERTIFICATE-----
  MIIDXTCCAkWgAwIBAgIJAKoK/heBjcOuMA0GCSqGSIb3DQEBBQUAMEUxCzAJBgNV
  ...
  -----END CERTIFICATE-----
```

```yaml
# Using vault variables
- name: Configure database connection
  template:
    src: database.conf.j2
    dest: /etc/app/database.conf
    mode: '0600'
  vars:
    db_password: "{{ vault_db_password }}"
```

## 9. Error Handling and Testing
```yaml
# Error handling
- name: Attempt to start service
  systemd:
    name: myservice
    state: started
  register: service_result
  failed_when: false
  
- name: Handle service failure
  debug:
    msg: "Service failed to start: {{ service_result.msg }}"
  when: service_result.failed
  
- name: Retry with backoff
  uri:
    url: "http://{{ inventory_hostname }}:8080/health"
    method: GET
  register: health_check
  until: health_check.status == 200
  retries: 5
  delay: 10
```

```yaml
# Testing with assert
- name: Verify Spark installation
  stat:
    path: /opt/spark/bin/spark-submit
  register: spark_binary
  
- name: Assert Spark is installed
  assert:
    that:
      - spark_binary.stat.exists
      - spark_binary.stat.executable
    fail_msg: "Spark binary not found or not executable"
    success_msg: "Spark installation verified"
```

## 10. Advanced Patterns
```yaml
# Dynamic inventory from cloud
# inventory/aws_ec2.yml
plugin: aws_ec2
regions:
  - us-west-2
keyed_groups:
  - key: tags.Environment
    prefix: env
  - key: instance_type
    prefix: type
hostnames:
  - tag:Name
  - dns-name
```

```yaml
# Rolling deployments
- name: Rolling update of web servers
  hosts: webservers
  serial: 1  # Update one server at a time
  
  pre_tasks:
    - name: Remove from load balancer
      uri:
        url: "http://lb.example.com/api/remove/{{ inventory_hostname }}"
        method: POST
        
  tasks:
    - name: Update application
      copy:
        src: app.jar
        dest: /opt/app/app.jar
      notify: restart app
      
  post_tasks:
    - name: Wait for service to be ready
      wait_for:
        port: 8080
        host: "{{ inventory_hostname }}"
        delay: 10
        
    - name: Add back to load balancer
      uri:
        url: "http://lb.example.com/api/add/{{ inventory_hostname }}"
        method: POST
```

```yaml
# Infrastructure as Code
- name: Provision AWS infrastructure
  hosts: localhost
  tasks:
    - name: Create VPC
      ec2_vpc_net:
        name: data-platform-vpc
        cidr_block: 10.0.0.0/16
        region: us-west-2
        tags:
          Environment: "{{ environment }}"
      register: vpc
      
    - name: Create subnets
      ec2_vpc_subnet:
        vpc_id: "{{ vpc.vpc.id }}"
        cidr: "{{ item.cidr }}"
        az: "{{ item.az }}"
        tags:
          Name: "{{ item.name }}"
      loop:
        - { cidr: "10.0.1.0/24", az: "us-west-2a", name: "public-1" }
        - { cidr: "10.0.2.0/24", az: "us-west-2b", name: "public-2" }
        - { cidr: "10.0.10.0/24", az: "us-west-2a", name: "private-1" }
```