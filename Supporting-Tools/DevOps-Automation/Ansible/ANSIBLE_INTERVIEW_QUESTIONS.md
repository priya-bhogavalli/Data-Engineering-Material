# Ansible Interview Questions

## Table of Contents

1. [Basic Ansible Questions](#basic-ansible-questions)
2. [Architecture & Components](#architecture--components)
3. [Playbooks & Tasks](#playbooks--tasks)
4. [Inventory Management](#inventory-management)
5. [Variables & Templates](#variables--templates)
6. [Roles & Collections](#roles--collections)
7. [Security & Best Practices](#security--best-practices)
8. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Ansible Questions

### 1. What is Ansible and what are its key characteristics?
**Answer:**
Ansible is an open-source automation tool for configuration management, application deployment, and task automation.

**Key Characteristics:**
- **Agentless**: No need to install agents on target machines
- **Idempotent**: Safe to run multiple times with same result
- **Simple**: YAML-based configuration language
- **Push-based**: Control node pushes configurations to targets
- **SSH-based**: Uses SSH for communication (Linux) and WinRM (Windows)

### 2. How does Ansible differ from other configuration management tools?
**Answer:**
**vs. Puppet/Chef:**
- Ansible: Agentless, push-based, YAML syntax
- Puppet/Chef: Agent-based, pull-based, Ruby DSL

**vs. Terraform:**
- Ansible: Configuration management, mutable infrastructure
- Terraform: Infrastructure provisioning, immutable infrastructure

**vs. SaltStack:**
- Ansible: SSH-based, simpler learning curve
- SaltStack: Agent-based, more complex but faster

### 3. What are the main components of Ansible?
**Answer:**
- **Control Node**: Machine where Ansible is installed and run
- **Managed Nodes**: Target machines managed by Ansible
- **Inventory**: List of managed nodes and their details
- **Modules**: Units of code that perform specific tasks
- **Playbooks**: YAML files containing automation instructions
- **Roles**: Reusable collections of tasks, variables, and files

### 4. What is idempotency in Ansible?
**Answer:**
Idempotency means running the same operation multiple times produces the same result:
- **Safe Execution**: No unintended side effects from re-runs
- **State Management**: Ansible checks current state before making changes
- **Efficiency**: Only makes necessary changes
- **Reliability**: Consistent results across multiple executions

### 5. Explain Ansible's push vs. pull model.
**Answer:**
**Push Model (Ansible):**
- Control node initiates connections to managed nodes
- Immediate execution of tasks
- Real-time feedback and control
- Requires network connectivity from control to managed nodes

**Pull Model (Puppet/Chef):**
- Managed nodes pull configurations from central server
- Periodic synchronization
- Works well with intermittent connectivity
- Agents run independently on managed nodes

## Architecture & Components

### 6. What are Ansible modules and how do they work?
**Answer:**
Modules are discrete units of code that perform specific tasks:
- **Core Modules**: Shipped with Ansible (file, service, yum, etc.)
- **Community Modules**: Contributed by community
- **Custom Modules**: User-developed modules
- **Execution**: Modules are copied to target nodes and executed
- **Return Values**: Modules return JSON with results and status

```yaml
- name: Install nginx
  yum:
    name: nginx
    state: present

- name: Start nginx service
  service:
    name: nginx
    state: started
    enabled: yes
```

### 7. What is Ansible Galaxy and its purpose?
**Answer:**
Ansible Galaxy is a hub for sharing Ansible content:
- **Role Repository**: Community-contributed roles
- **Collections**: Packaged content including roles, modules, plugins
- **Installation**: `ansible-galaxy install` command
- **Publishing**: Share your own roles and collections
- **Dependencies**: Manage role dependencies

```bash
# Install role from Galaxy
ansible-galaxy install geerlingguy.nginx

# Install collection
ansible-galaxy collection install community.general
```

### 8. Explain Ansible's execution model.
**Answer:**
1. **Inventory Parsing**: Read and parse inventory file
2. **Playbook Loading**: Load and validate playbook syntax
3. **Task Execution**: Execute tasks on target hosts
4. **Module Transfer**: Copy modules to target hosts
5. **Module Execution**: Run modules on target hosts
6. **Result Collection**: Gather results and return to control node
7. **Cleanup**: Remove temporary files from target hosts

### 9. What are Ansible plugins and their types?
**Answer:**
Plugins extend Ansible's functionality:
- **Action Plugins**: Control task execution
- **Cache Plugins**: Store gathered facts
- **Callback Plugins**: Respond to events during execution
- **Connection Plugins**: Connect to target hosts
- **Filter Plugins**: Transform data in templates
- **Inventory Plugins**: Parse inventory sources
- **Lookup Plugins**: Retrieve data from external sources

### 10. How does Ansible handle parallel execution?
**Answer:**
- **Forks**: Control number of parallel processes (default: 5)
- **Serial**: Control how many hosts to process at once
- **Strategy**: Linear (default) or free strategy
- **Throttle**: Limit concurrent tasks per play

```yaml
- hosts: webservers
  serial: 2  # Process 2 hosts at a time
  tasks:
    - name: Update packages
      yum:
        name: "*"
        state: latest
      throttle: 1  # Only 1 host at a time for this task
```

## Playbooks & Tasks

### 11. What is an Ansible playbook and its structure?
**Answer:**
A playbook is a YAML file containing automation instructions:
```yaml
---
- name: Web server setup
  hosts: webservers
  become: yes
  vars:
    http_port: 80
  tasks:
    - name: Install Apache
      yum:
        name: httpd
        state: present
    
    - name: Start Apache
      service:
        name: httpd
        state: started
        enabled: yes
  
  handlers:
    - name: restart apache
      service:
        name: httpd
        state: restarted
```

### 12. What are handlers in Ansible and when to use them?
**Answer:**
Handlers are special tasks that run only when notified:
- **Triggered by Changes**: Only run when tasks report changes
- **Run Once**: Execute only once even if notified multiple times
- **End of Play**: Run at the end of the play by default
- **Common Use**: Service restarts, configuration reloads

```yaml
tasks:
  - name: Update Apache config
    template:
      src: httpd.conf.j2
      dest: /etc/httpd/conf/httpd.conf
    notify: restart apache

handlers:
  - name: restart apache
    service:
      name: httpd
      state: restarted
```

### 13. How do you handle conditional execution in Ansible?
**Answer:**
```yaml
tasks:
  - name: Install package on RedHat
    yum:
      name: httpd
      state: present
    when: ansible_os_family == "RedHat"
  
  - name: Install package on Debian
    apt:
      name: apache2
      state: present
    when: ansible_os_family == "Debian"
  
  - name: Check if file exists
    stat:
      path: /etc/myapp.conf
    register: config_file
  
  - name: Create config if not exists
    template:
      src: myapp.conf.j2
      dest: /etc/myapp.conf
    when: not config_file.stat.exists
```

### 14. What are loops in Ansible and how to use them?
**Answer:**
```yaml
tasks:
  - name: Install multiple packages
    yum:
      name: "{{ item }}"
      state: present
    loop:
      - httpd
      - mysql-server
      - php
  
  - name: Create users
    user:
      name: "{{ item.name }}"
      group: "{{ item.group }}"
      state: present
    loop:
      - { name: 'alice', group: 'developers' }
      - { name: 'bob', group: 'admins' }
  
  - name: Install packages with conditions
    yum:
      name: "{{ item }}"
      state: present
    loop: "{{ packages }}"
    when: item != "excluded_package"
```

### 15. How do you handle errors and failures in Ansible?
**Answer:**
```yaml
tasks:
  - name: Task that might fail
    command: /bin/false
    ignore_errors: yes
  
  - name: Task with custom failure condition
    shell: echo "Hello World"
    register: result
    failed_when: "'World' not in result.stdout"
  
  - name: Task with changed condition
    command: echo "No changes"
    changed_when: false
  
  - name: Rescue block example
    block:
      - name: Risky task
        command: /might/fail
    rescue:
      - name: Handle failure
        debug:
          msg: "Task failed, handling gracefully"
    always:
      - name: Cleanup
        file:
          path: /tmp/cleanup
          state: absent
```

## Inventory Management

### 16. What is Ansible inventory and its formats?
**Answer:**
Inventory defines the hosts and groups that Ansible manages:

**INI Format:**
```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com ansible_host=192.168.1.10
db2.example.com ansible_host=192.168.1.11

[production:children]
webservers
databases
```

**YAML Format:**
```yaml
all:
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
    databases:
      hosts:
        db1.example.com:
          ansible_host: 192.168.1.10
        db2.example.com:
          ansible_host: 192.168.1.11
```

### 17. How do you use dynamic inventory in Ansible?
**Answer:**
Dynamic inventory sources hosts from external systems:
```bash
# AWS EC2 dynamic inventory
ansible-inventory -i aws_ec2.yml --list

# Custom dynamic inventory script
#!/usr/bin/env python3
import json

inventory = {
    'webservers': {
        'hosts': ['web1.example.com', 'web2.example.com']
    },
    '_meta': {
        'hostvars': {
            'web1.example.com': {'ansible_host': '192.168.1.10'}
        }
    }
}

print(json.dumps(inventory))
```

### 18. What are inventory variables and their precedence?
**Answer:**
**Variable Precedence (highest to lowest):**
1. Extra vars (`-e` command line)
2. Task vars
3. Block vars
4. Role and include vars
5. Play vars
6. Host facts
7. Inventory host vars
8. Inventory group vars
9. Role defaults

```yaml
# Group variables
[webservers:vars]
http_port=80
max_clients=200

# Host variables
web1.example.com http_port=8080
```

## Variables & Templates

### 19. How do you define and use variables in Ansible?
**Answer:**
```yaml
# Playbook variables
- hosts: webservers
  vars:
    http_port: 80
    server_name: "{{ ansible_hostname }}"
  vars_files:
    - vars/main.yml
  tasks:
    - name: Use variables
      template:
        src: httpd.conf.j2
        dest: /etc/httpd/conf/httpd.conf
      vars:
        task_var: "task level variable"
```

**Variable Files:**
```yaml
# vars/main.yml
database_host: db.example.com
database_port: 3306
app_users:
  - alice
  - bob
  - charlie
```

### 20. What are Jinja2 templates and how to use them?
**Answer:**
Jinja2 templates allow dynamic content generation:
```jinja2
# templates/httpd.conf.j2
ServerRoot /etc/httpd
Listen {{ http_port }}
ServerName {{ server_name }}

{% for user in app_users %}
User {{ user }}
{% endfor %}

{% if ssl_enabled %}
LoadModule ssl_module modules/mod_ssl.so
{% endif %}

# Conditional content
{% if ansible_os_family == "RedHat" %}
LoadModule rewrite_module modules/mod_rewrite.so
{% elif ansible_os_family == "Debian" %}
LoadModule rewrite_module /usr/lib/apache2/modules/mod_rewrite.so
{% endif %}
```

### 21. How do you use Ansible facts?
**Answer:**
Facts are system information automatically gathered by Ansible:
```yaml
tasks:
  - name: Display facts
    debug:
      msg: "OS: {{ ansible_os_family }}, IP: {{ ansible_default_ipv4.address }}"
  
  - name: Custom fact gathering
    setup:
      filter: ansible_memory_mb
  
  - name: Disable fact gathering
    gather_facts: no
  
  - name: Use facts in conditions
    yum:
      name: httpd
      state: present
    when: ansible_os_family == "RedHat"
```

**Custom Facts:**
```bash
# /etc/ansible/facts.d/custom.fact
#!/bin/bash
echo '{"app_version": "1.2.3", "environment": "production"}'
```

## Roles & Collections

### 22. What are Ansible roles and their structure?
**Answer:**
Roles organize playbook content into reusable components:
```
roles/
  webserver/
    tasks/main.yml          # Main task list
    handlers/main.yml       # Handlers
    templates/              # Jinja2 templates
    files/                  # Static files
    vars/main.yml          # Role variables
    defaults/main.yml      # Default variables
    meta/main.yml          # Role metadata
    README.md              # Documentation
```

**Using Roles:**
```yaml
- hosts: webservers
  roles:
    - webserver
    - { role: database, db_port: 3306 }
    - role: monitoring
      when: monitoring_enabled
```

### 23. How do you create and use Ansible collections?
**Answer:**
Collections package and distribute Ansible content:
```bash
# Create collection structure
ansible-galaxy collection init my_namespace.my_collection

# Collection structure
collections/
  ansible_collections/
    my_namespace/
      my_collection/
        plugins/
        roles/
        playbooks/
        galaxy.yml
```

**Using Collections:**
```yaml
- hosts: all
  collections:
    - my_namespace.my_collection
  tasks:
    - name: Use collection module
      my_namespace.my_collection.custom_module:
        param: value
```

### 24. What are role dependencies and how to manage them?
**Answer:**
```yaml
# meta/main.yml
dependencies:
  - role: common
    vars:
      common_var: value
  - role: apache
    when: webserver_type == "apache"
  - src: https://github.com/user/role
    version: "1.0"
    name: external_role
```

**Galaxy Requirements:**
```yaml
# requirements.yml
- src: geerlingguy.nginx
  version: "2.8.0"
- src: https://github.com/user/custom-role
  name: custom_role
```

## Security & Best Practices

### 25. How do you handle sensitive data in Ansible?
**Answer:**
**Ansible Vault:**
```bash
# Create encrypted file
ansible-vault create secrets.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# Encrypt existing file
ansible-vault encrypt vars.yml

# Run playbook with vault
ansible-playbook -i inventory playbook.yml --ask-vault-pass
```

**Vault in Playbooks:**
```yaml
- hosts: all
  vars_files:
    - secrets.yml  # Encrypted file
  tasks:
    - name: Use encrypted variable
      debug:
        msg: "Database password is {{ db_password }}"
```

### 26. What are Ansible security best practices?
**Answer:**
- **Vault Usage**: Encrypt sensitive data with Ansible Vault
- **SSH Keys**: Use SSH key authentication instead of passwords
- **Privilege Escalation**: Use `become` instead of running as root
- **Network Security**: Secure SSH configuration and firewall rules
- **Code Review**: Review playbooks and roles before deployment
- **Least Privilege**: Grant minimum necessary permissions
- **Logging**: Enable and monitor Ansible logs

### 27. How do you implement privilege escalation in Ansible?
**Answer:**
```yaml
- hosts: all
  become: yes          # Enable privilege escalation
  become_method: sudo  # Method (sudo, su, pbrun, etc.)
  become_user: root    # Target user
  tasks:
    - name: Install package (requires root)
      yum:
        name: httpd
        state: present
    
    - name: Task without privilege escalation
      debug:
        msg: "This runs as regular user"
      become: no
    
    - name: Run as specific user
      command: whoami
      become_user: apache
```

### 28. How do you test Ansible playbooks?
**Answer:**
**Syntax Check:**
```bash
ansible-playbook --syntax-check playbook.yml
```

**Dry Run:**
```bash
ansible-playbook --check playbook.yml
```

**Molecule Testing:**
```yaml
# molecule/default/molecule.yml
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: centos:7
provisioner:
  name: ansible
verifier:
  name: ansible
```

**Test Playbook:**
```yaml
# molecule/default/verify.yml
- name: Verify
  hosts: all
  tasks:
    - name: Check if service is running
      service:
        name: httpd
        state: started
      check_mode: yes
      register: service_status
      failed_when: service_status.changed
```

## Scenario-Based Questions

### 29. Design an Ansible playbook for deploying a web application across multiple environments.
**Answer:**
```yaml
# deploy-webapp.yml
- name: Deploy Web Application
  hosts: "{{ target_env }}"
  become: yes
  vars:
    app_name: mywebapp
    app_version: "{{ version | default('latest') }}"
  
  pre_tasks:
    - name: Validate environment
      fail:
        msg: "Invalid environment: {{ target_env }}"
      when: target_env not in ['dev', 'staging', 'prod']
  
  roles:
    - common
    - webserver
    - { role: database, when: inventory_hostname in groups['db_servers'] }
  
  tasks:
    - name: Download application
      get_url:
        url: "https://releases.example.com/{{ app_name }}-{{ app_version }}.tar.gz"
        dest: "/tmp/{{ app_name }}-{{ app_version }}.tar.gz"
    
    - name: Extract application
      unarchive:
        src: "/tmp/{{ app_name }}-{{ app_version }}.tar.gz"
        dest: /opt/
        remote_src: yes
        creates: "/opt/{{ app_name }}-{{ app_version }}"
    
    - name: Create symlink
      file:
        src: "/opt/{{ app_name }}-{{ app_version }}"
        dest: "/opt/{{ app_name }}"
        state: link
      notify: restart webserver
    
    - name: Deploy configuration
      template:
        src: "app.conf.j2"
        dest: "/etc/{{ app_name }}/app.conf"
        backup: yes
      notify: restart webserver
  
  handlers:
    - name: restart webserver
      service:
        name: "{{ webserver_service }}"
        state: restarted

# Usage:
# ansible-playbook -i inventory deploy-webapp.yml -e target_env=staging -e version=1.2.3
```

### 30. How would you use Ansible for infrastructure provisioning and configuration?
**Answer:**
```yaml
# provision-infrastructure.yml
- name: Provision AWS Infrastructure
  hosts: localhost
  gather_facts: no
  vars:
    region: us-west-2
    instance_type: t3.medium
  
  tasks:
    - name: Create VPC
      ec2_vpc_net:
        name: "{{ project_name }}-vpc"
        cidr_block: 10.0.0.0/16
        region: "{{ region }}"
        state: present
      register: vpc
    
    - name: Create subnet
      ec2_vpc_subnet:
        vpc_id: "{{ vpc.vpc.id }}"
        cidr: 10.0.1.0/24
        region: "{{ region }}"
        state: present
      register: subnet
    
    - name: Launch EC2 instances
      ec2_instance:
        name: "{{ project_name }}-{{ item }}"
        image_id: ami-0c02fb55956c7d316
        instance_type: "{{ instance_type }}"
        subnet_id: "{{ subnet.subnet.id }}"
        security_groups: ["{{ security_group.group_id }}"]
        key_name: "{{ key_pair }}"
        state: present
        wait: yes
      loop:
        - web1
        - web2
        - db1
      register: instances
    
    - name: Add instances to inventory
      add_host:
        name: "{{ item.instances[0].public_ip_address }}"
        groups: "{{ item.item.startswith('web') | ternary('webservers', 'databases') }}"
        ansible_ssh_private_key_file: "{{ private_key_path }}"
      loop: "{{ instances.results }}"

- name: Configure instances
  hosts: all
  become: yes
  roles:
    - common
    - { role: webserver, when: inventory_hostname in groups['webservers'] }
    - { role: database, when: inventory_hostname in groups['databases'] }
```

### 31. Your Ansible playbook is running slowly. How do you optimize it?
**Answer:**
1. **Increase Parallelism**: Adjust forks and serial settings
2. **Fact Caching**: Enable fact caching to avoid repeated gathering
3. **Pipelining**: Enable SSH pipelining
4. **Strategy**: Use 'free' strategy for independent tasks
5. **Conditional Execution**: Use proper when conditions
6. **Module Optimization**: Use appropriate modules (package vs yum/apt)

```yaml
# ansible.cfg optimizations
[defaults]
forks = 20
host_key_checking = False
fact_caching = memory
fact_caching_timeout = 86400

[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=60s

# Playbook optimizations
- hosts: all
  strategy: free  # Don't wait for all hosts
  gather_facts: no  # Skip if not needed
  tasks:
    - name: Gather minimal facts
      setup:
        filter: ansible_os_family
      when: ansible_os_family is not defined
```

### 32. How would you implement rolling deployments with Ansible?
**Answer:**
```yaml
- name: Rolling Deployment
  hosts: webservers
  serial: "25%"  # Deploy to 25% of hosts at a time
  max_fail_percentage: 10  # Fail if more than 10% fail
  
  pre_tasks:
    - name: Remove from load balancer
      uri:
        url: "http://{{ load_balancer }}/api/remove/{{ inventory_hostname }}"
        method: POST
      delegate_to: localhost
    
    - name: Wait for connections to drain
      wait_for:
        timeout: 30
  
  tasks:
    - name: Stop application
      service:
        name: myapp
        state: stopped
    
    - name: Deploy new version
      unarchive:
        src: "{{ app_package }}"
        dest: /opt/myapp/
        backup: yes
    
    - name: Start application
      service:
        name: myapp
        state: started
    
    - name: Health check
      uri:
        url: "http://{{ inventory_hostname }}:8080/health"
        status_code: 200
      retries: 5
      delay: 10
  
  post_tasks:
    - name: Add back to load balancer
      uri:
        url: "http://{{ load_balancer }}/api/add/{{ inventory_hostname }}"
        method: POST
      delegate_to: localhost
```

---

## Key Takeaways for Interviews

1. **Core Concepts**: Understand idempotency, agentless architecture, and YAML syntax
2. **Playbook Design**: Master tasks, handlers, variables, and conditional logic
3. **Inventory Management**: Know static and dynamic inventory concepts
4. **Security**: Understand Ansible Vault and privilege escalation
5. **Roles & Collections**: Know how to organize and reuse Ansible content
6. **Best Practices**: Follow security, testing, and performance optimization practices
7. **Troubleshooting**: Practice debugging playbooks and performance issues
8. **Real-world Scenarios**: Prepare for infrastructure automation and deployment questions