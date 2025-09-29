# Apache NiFi - Best Practices & Production Guidelines

## 📋 Table of Contents

1. [Flow Design Best Practices](#-flow-design-best-practices)
2. [Performance Optimization](#-performance-optimization)
3. [Security Hardening](#-security-hardening)
4. [Monitoring & Alerting](#-monitoring--alerting)
5. [Error Handling](#-error-handling)
6. [Configuration Management](#-configuration-management)
7. [Clustering Best Practices](#-clustering-best-practices)
8. [Development Workflow](#-development-workflow)
9. [Production Deployment](#-production-deployment)
10. [Troubleshooting Guide](#-troubleshooting-guide)

---

## 🎨 Flow Design Best Practices

### 1. Processor Configuration
```python
# Optimal processor settings
processor_best_practices = {
    'concurrent_tasks': {
        'cpu_bound': 'Set to CPU cores (4-8)',
        'io_bound': 'Set higher than CPU cores (8-16)',
        'memory_intensive': 'Keep low (1-2)',
        'network_bound': 'Moderate (4-8)'
    },
    
    'scheduling': {
        'run_schedule': {
            'continuous': '0 sec',
            'batch_processing': '5 min',
            'low_priority': '1 hour'
        },
        'yield_duration': '1 sec'  # Prevent CPU spinning
    }
}
```

### 2. Connection Queue Management
```python
# Connection configuration best practices
connection_settings = {
    'back_pressure': {
        'object_threshold': 10000,
        'size_threshold': '1 GB',
        'rationale': 'Prevents memory overflow'
    },
    
    'flowfile_expiration': {
        'real_time': '1 hour',
        'batch': '24 hours',
        'archive': '7 days'
    },
    
    'prioritizers': [
        'FirstInFirstOutPrioritizer',  # Default
        'NewestFlowFileFirstPrioritizer',  # For real-time
        'PriorityAttributePrioritizer'  # Custom priority
    ]
}
```

### 3. Process Group Organization
```
Recommended Structure:
├── Data Ingestion
│   ├── File Sources
│   ├── Database Sources
│   └── API Sources
├── Data Transformation
│   ├── Validation
│   ├── Enrichment
│   └── Format Conversion
├── Data Routing
│   ├── Content-based Routing
│   └── Load Balancing
└── Data Egress
    ├── Database Targets
    ├── File Targets
    └── Message Queue Targets
```

---

## ⚡ Performance Optimization

### 1. JVM Tuning
```bash
# Optimal JVM settings for production
export JAVA_OPTS="-Xmx8g -Xms8g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -XX:G1HeapRegionSize=16m \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+UseCGroupMemoryLimitForHeap \
  -Djava.net.preferIPv4Stack=true"
```

### 2. Repository Optimization
```python
# Repository performance settings
repository_config = {
    'flowfile_repository': {
        'partitions': 256,  # Increase for high throughput
        'checkpoint_interval': '2 mins',
        'always_sync': 'false'  # Better performance
    },
    
    'content_repository': {
        'claim_max_appendable_size': '10 MB',
        'claim_max_flow_files': 100,
        'archive_max_retention_period': '12 hours',
        'archive_max_usage_percentage': '50%'
    },
    
    'provenance_repository': {
        'max_storage_time': '24 hours',
        'max_storage_size': '1 GB',
        'rollover_time': '30 secs',
        'rollover_size': '100 MB'
    }
}
```

### 3. Processor-Specific Optimizations
```python
# High-performance processor configurations
processor_optimizations = {
    'GetFile': {
        'batch_size': '100',
        'polling_interval': '10 sec',
        'minimum_file_age': '5 sec'
    },
    
    'PutDatabaseRecord': {
        'batch_size': '1000',
        'obtain_generated_keys': 'false',
        'rollback_on_failure': 'false'
    },
    
    'ConsumeKafka': {
        'max_poll_records': '10000',
        'session_timeout': '60 seconds',
        'auto_offset_reset': 'latest'
    }
}
```

---

## 🔒 Security Hardening

### 1. Authentication Configuration
```xml
<!-- login-identity-providers.xml -->
<loginIdentityProviders>
    <provider>
        <identifier>ldap-provider</identifier>
        <class>org.apache.nifi.ldap.LdapProvider</class>
        <property name="Authentication Strategy">SIMPLE</property>
        <property name="Manager DN">cn=admin,dc=example,dc=com</property>
        <property name="Manager Password">password</property>
        <property name="TLS - Keystore">/path/to/keystore.jks</property>
        <property name="TLS - Keystore Password">keystorePassword</property>
        <property name="TLS - Keystore Type">JKS</property>
        <property name="Url">ldaps://localhost:636</property>
        <property name="User Search Base">ou=users,dc=example,dc=com</property>
        <property name="User Search Filter">cn={0}</property>
    </provider>
</loginIdentityProviders>
```

### 2. Authorization Policies
```python
# Role-based access control setup
security_policies = {
    'global_policies': [
        'view the user interface',
        'access the controller',
        'query provenance',
        'access restricted components'
    ],
    
    'component_policies': {
        'sensitive_processors': ['admin', 'data_engineer'],
        'public_processors': ['admin', 'data_engineer', 'analyst'],
        'system_diagnostics': ['admin']
    },
    
    'data_policies': {
        'pii_data': ['admin', 'compliance_officer'],
        'financial_data': ['admin', 'finance_team'],
        'public_data': ['admin', 'data_engineer', 'analyst']
    }
}
```

### 3. Encryption Best Practices
```python
# Encryption configuration
encryption_config = {
    'data_in_transit': {
        'https_enabled': True,
        'tls_version': 'TLSv1.2',
        'cipher_suites': [
            'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384',
            'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256'
        ]
    },
    
    'data_at_rest': {
        'sensitive_properties_key': 'nifi.sensitive.props.key',
        'encrypt_config_repos': True,
        'flowfile_encryption': 'AES/GCM/NoPadding'
    },
    
    'certificate_management': {
        'keystore_type': 'PKCS12',
        'key_algorithm': 'RSA',
        'key_size': 2048,
        'cert_validity': '365 days'
    }
}
```

---

## 📊 Monitoring & Alerting

### 1. Key Metrics to Monitor
```python
# Critical metrics for production monitoring
monitoring_metrics = {
    'system_metrics': {
        'cpu_utilization': {'threshold': 80, 'alert': 'warning'},
        'memory_usage': {'threshold': 85, 'alert': 'critical'},
        'disk_usage': {'threshold': 90, 'alert': 'critical'},
        'network_io': {'threshold': '1 GB/s', 'alert': 'info'}
    },
    
    'nifi_metrics': {
        'active_threads': {'threshold': 100, 'alert': 'warning'},
        'flowfiles_queued': {'threshold': 50000, 'alert': 'warning'},
        'bytes_queued': {'threshold': '5 GB', 'alert': 'critical'},
        'processor_errors': {'threshold': 10, 'alert': 'critical'}
    },
    
    'flow_metrics': {
        'throughput': {'min_threshold': '1000 records/min'},
        'latency': {'max_threshold': '30 seconds'},
        'error_rate': {'max_threshold': '1%'},
        'back_pressure_events': {'max_threshold': 5}
    }
}
```

### 2. Prometheus Integration
```yaml
# prometheus.yml configuration
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'nifi'
    static_configs:
      - targets: ['nifi-node1:9092', 'nifi-node2:9092', 'nifi-node3:9092']
    metrics_path: /nifi-api/system-diagnostics
    scrape_interval: 30s
```

### 3. Alerting Rules
```yaml
# alerting_rules.yml
groups:
  - name: nifi_alerts
    rules:
      - alert: NiFiHighCPU
        expr: nifi_jvm_cpu_usage > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "NiFi CPU usage is high"
          
      - alert: NiFiHighMemory
        expr: nifi_jvm_heap_usage_percent > 85
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "NiFi memory usage is critical"
          
      - alert: NiFiProcessorErrors
        expr: increase(nifi_processor_errors_total[5m]) > 10
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "High error rate in NiFi processors"
```

---

## 🚨 Error Handling

### 1. Error Handling Patterns
```python
# Comprehensive error handling strategy
error_handling_patterns = {
    'retry_pattern': {
        'processors': ['RetryFlowFile', 'PenalizeFlowFile'],
        'configuration': {
            'retry_attempts': 3,
            'penalty_duration': '30 sec',
            'exponential_backoff': True
        }
    },
    
    'dead_letter_queue': {
        'processors': ['RouteOnAttribute', 'PutFile'],
        'routing_criteria': 'retry.count >= 3',
        'storage_location': '/data/nifi/failed-records'
    },
    
    'circuit_breaker': {
        'failure_threshold': 10,
        'timeout_duration': '5 min',
        'recovery_strategy': 'gradual'
    }
}
```

### 2. Validation and Data Quality
```python
# Data validation best practices
validation_strategies = {
    'schema_validation': {
        'processors': ['ValidateRecord', 'ValidateJson'],
        'actions': {
            'valid': 'continue_processing',
            'invalid': 'route_to_error_queue'
        }
    },
    
    'business_rules': {
        'processors': ['RouteOnAttribute', 'ExecuteScript'],
        'rules': [
            'required_fields_present',
            'data_format_correct',
            'business_logic_valid'
        ]
    },
    
    'data_profiling': {
        'processors': ['UpdateAttribute', 'LogAttribute'],
        'metrics': ['record_count', 'null_values', 'data_types']
    }
}
```

---

## 🔧 Configuration Management

### 1. Environment-Specific Configurations
```python
# Environment configuration strategy
environment_configs = {
    'development': {
        'nifi.web.http.port': '8080',
        'nifi.cluster.is.node': 'false',
        'nifi.provenance.repository.max.storage.time': '1 hour',
        'logging.level': 'DEBUG'
    },
    
    'staging': {
        'nifi.web.https.port': '8443',
        'nifi.cluster.is.node': 'true',
        'nifi.provenance.repository.max.storage.time': '12 hours',
        'logging.level': 'INFO'
    },
    
    'production': {
        'nifi.web.https.port': '8443',
        'nifi.cluster.is.node': 'true',
        'nifi.provenance.repository.max.storage.time': '24 hours',
        'logging.level': 'WARN'
    }
}
```

### 2. Parameter Contexts
```json
{
  "parameter-contexts": [
    {
      "name": "Database-Config",
      "parameters": [
        {
          "name": "db.host",
          "value": "${DB_HOST}",
          "sensitive": false
        },
        {
          "name": "db.password",
          "value": "${DB_PASSWORD}",
          "sensitive": true
        }
      ]
    },
    {
      "name": "Kafka-Config",
      "parameters": [
        {
          "name": "kafka.brokers",
          "value": "${KAFKA_BROKERS}",
          "sensitive": false
        }
      ]
    }
  ]
}
```

---

## 🔗 Clustering Best Practices

### 1. Cluster Architecture
```
Recommended Cluster Setup:
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   NiFi Node 1   │  │   NiFi Node 2   │  │   NiFi Node 3   │
│   (Primary)     │  │   (Secondary)   │  │   (Secondary)   │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
┌─────────────────────────────────────────────────────────────┐
│              ZooKeeper Ensemble                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   ZK Node 1 │  │   ZK Node 2 │  │   ZK Node 3 │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### 2. Load Balancing Strategies
```python
# Load balancing configuration
load_balancing = {
    'round_robin': {
        'use_case': 'Even distribution of data',
        'configuration': {
            'strategy': 'ROUND_ROBIN',
            'compression': 'GZIP',
            'timeout': '30 sec'
        }
    },
    
    'partition_by_attribute': {
        'use_case': 'Data locality requirements',
        'configuration': {
            'strategy': 'PARTITION_BY_ATTRIBUTE',
            'attribute_name': 'customer_id',
            'partitioner': 'hash'
        }
    },
    
    'single_node': {
        'use_case': 'Stateful processing',
        'configuration': {
            'strategy': 'SINGLE_NODE',
            'preferred_node': 'node-1'
        }
    }
}
```

---

## 🔄 Development Workflow

### 1. Version Control Strategy
```bash
# Git workflow for NiFi flows
git_workflow = {
    'branches': {
        'main': 'Production-ready flows',
        'develop': 'Integration branch',
        'feature/*': 'New flow development',
        'hotfix/*': 'Production fixes'
    },
    
    'flow_versioning': {
        'registry_url': 'http://nifi-registry:18080',
        'bucket_name': 'production-flows',
        'version_strategy': 'semantic_versioning'
    }
}

# Example commands
git checkout -b feature/customer-data-pipeline
# Develop flow in NiFi UI
# Commit flow to registry
git add flow-definition.json
git commit -m "Add customer data pipeline"
git push origin feature/customer-data-pipeline
```

### 2. Testing Strategy
```python
# Testing approach for NiFi flows
testing_strategy = {
    'unit_testing': {
        'tools': ['NiFi Test Framework', 'MockProcessors'],
        'scope': 'Individual processor logic'
    },
    
    'integration_testing': {
        'tools': ['Docker Compose', 'Test Containers'],
        'scope': 'End-to-end flow validation'
    },
    
    'performance_testing': {
        'tools': ['JMeter', 'Custom Load Generators'],
        'metrics': ['throughput', 'latency', 'resource_usage']
    }
}
```

---

## 🚀 Production Deployment

### 1. Deployment Checklist
```python
deployment_checklist = {
    'pre_deployment': [
        'Backup current flow configuration',
        'Validate flow in staging environment',
        'Check resource requirements',
        'Verify security configurations',
        'Test rollback procedures'
    ],
    
    'deployment': [
        'Stop affected process groups',
        'Deploy new flow version',
        'Update parameter contexts',
        'Restart process groups',
        'Verify flow execution'
    ],
    
    'post_deployment': [
        'Monitor system metrics',
        'Validate data quality',
        'Check error logs',
        'Verify downstream systems',
        'Update documentation'
    ]
}
```

### 2. Blue-Green Deployment
```python
# Blue-green deployment strategy
blue_green_deployment = {
    'blue_environment': {
        'cluster': 'nifi-blue-cluster',
        'status': 'active',
        'traffic_percentage': 100
    },
    
    'green_environment': {
        'cluster': 'nifi-green-cluster',
        'status': 'standby',
        'traffic_percentage': 0
    },
    
    'deployment_process': [
        'Deploy to green environment',
        'Run validation tests',
        'Gradually shift traffic (10%, 50%, 100%)',
        'Monitor metrics and errors',
        'Complete cutover or rollback'
    ]
}
```

---

## 🔍 Troubleshooting Guide

### 1. Common Issues and Solutions
```python
troubleshooting_guide = {
    'performance_issues': {
        'symptoms': ['High CPU usage', 'Memory leaks', 'Slow processing'],
        'solutions': [
            'Optimize processor concurrency',
            'Tune JVM garbage collection',
            'Implement back pressure handling',
            'Review connection queue sizes'
        ]
    },
    
    'connectivity_issues': {
        'symptoms': ['Connection timeouts', 'Authentication failures'],
        'solutions': [
            'Check network connectivity',
            'Verify credentials and certificates',
            'Review firewall rules',
            'Test connection pooling settings'
        ]
    },
    
    'data_quality_issues': {
        'symptoms': ['Data corruption', 'Missing records', 'Format errors'],
        'solutions': [
            'Implement data validation',
            'Add error handling flows',
            'Monitor data lineage',
            'Set up data quality alerts'
        ]
    }
}
```

### 2. Diagnostic Commands
```bash
# Useful diagnostic commands
diagnostic_commands = {
    'system_health': [
        'curl -k https://nifi-host:8443/nifi-api/system-diagnostics',
        'curl -k https://nifi-host:8443/nifi-api/controller/cluster',
        'jstack <nifi-pid> > thread-dump.txt'
    ],
    
    'log_analysis': [
        'tail -f logs/nifi-app.log | grep ERROR',
        'grep -i "outofmemory" logs/nifi-bootstrap.log',
        'find logs/ -name "*.log" -mtime -1 -exec grep -l "WARN" {} \;'
    ],
    
    'performance_monitoring': [
        'top -p <nifi-pid>',
        'iostat -x 1',
        'netstat -an | grep :8080'
    ]
}
```

---

## 📚 Additional Resources

- [NiFi System Administrator's Guide](https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html)
- [NiFi Expression Language Guide](https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html)
- [NiFi Registry User Guide](https://nifi.apache.org/docs/nifi-registry-docs/html/user-guide.html)
- [NiFi Toolkit Guide](https://nifi.apache.org/docs/nifi-docs/html/toolkit-guide.html)