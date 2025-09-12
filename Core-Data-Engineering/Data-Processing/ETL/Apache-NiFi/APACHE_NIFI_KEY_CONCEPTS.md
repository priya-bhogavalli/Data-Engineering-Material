# Apache NiFi Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [FlowFiles](#flowfiles)
   - [Processors](#processors)
   - [Connections](#connections)
   - [Process Groups](#process-groups)
3. [NiFi Architecture](#-nifi-architecture)
4. [Data Flow Design](#-data-flow-design)
5. [Security & Access Control](#-security--access-control)
6. [Performance Optimization](#-performance-optimization)
7. [Configuration](#️-configuration)
8. [Clustering](#-clustering)
9. [When to Use NiFi](#-when-to-use-nifi)
10. [Interview Focus Areas](#-interview-focus-areas)
11. [Quick References](#-quick-references)

---

## 🎯 Overview

Apache NiFi is a powerful, easy-to-use data integration platform that automates the flow of data between systems with a web-based user interface for designing, controlling, and monitoring data flows.

**Key Benefits:**
- **Visual Interface**: Drag-and-drop web UI for flow design
- **Data Provenance**: Complete lineage tracking from source to destination
- **Real-time Processing**: Stream processing with back-pressure handling
- **Security**: Fine-grained access control and data encryption
- **Extensible**: Custom processors and integrations

## 📦 Core Components

### FlowFiles
**Definition**: Fundamental data object in NiFi representing a piece of data moving through the system.

**Structure**:
- **Attributes**: Key-value metadata pairs
- **Content**: Actual data payload (can be empty)

```python
# FlowFile conceptual structure
flowfile_example = {
    'attributes': {
        # Standard attributes
        'filename': 'customer_data.json',
        'path': '/input/customers/',
        'uuid': '12345678-1234-1234-1234-123456789abc',
        'entryDate': '2024-01-15T10:30:00.000Z',
        'fileSize': '1024',
        
        # Custom attributes
        'source.system': 'CRM',
        'data.type': 'customer',
        'processing.priority': 'high'
    },
    'content': {
        'data': '{"id": 1, "name": "John Doe", "email": "john@example.com"}'
    }
}
```

### Processors
**Definition**: Components that perform work on FlowFiles - the building blocks of data flows.

**Categories**:
- **Data Ingestion**: GetFile, GetHTTP, GetKafka, GetSFTP
- **Data Transformation**: JoltTransformJSON, ReplaceText, SplitText
- **Data Routing**: RouteOnAttribute, RouteOnContent, DistributeLoad
- **Data Egress**: PutFile, PutHTTP, PutKafka, PutS3Object

```python
# Common processor configurations
processors = {
    'GetFile': {
        'properties': {
            'Input Directory': '/data/input',
            'File Filter': '.*\\.json$',
            'Keep Source File': 'false',
            'Minimum File Age': '5 sec',
            'Polling Interval': '10 sec'
        }
    },
    
    'JoltTransformJSON': {
        'properties': {
            'Jolt Specification': '''{
                "operation": "shift",
                "spec": {
                    "customer_id": "id",
                    "customer_name": "name",
                    "email_address": "email"
                }
            }'''
        }
    },
    
    'RouteOnAttribute': {
        'properties': {
            'high_priority': "${processing.priority:equals('high')}",
            'medium_priority': "${processing.priority:equals('medium')}",
            'low_priority': "${processing.priority:equals('low')}"
        }
    }
}
```

### Connections
**Definition**: Queues that link processors and control data flow between them.

**Key Features**:
- **Back Pressure**: Prevents overwhelming downstream processors
- **FlowFile Prioritization**: Control processing order
- **Load Balancing**: Distribute FlowFiles across connections

```python
# Connection configuration example
connection_config = {
    'settings': {
        'FlowFile Expiration': '1 hour',
        'Back Pressure Object Threshold': '10000',
        'Back Pressure Data Size Threshold': '1 GB',
        'Prioritizers': ['FirstInFirstOutPrioritizer'],
        'Load Balance Strategy': 'ROUND_ROBIN'
    }
}
```

### Process Groups
**Definition**: Containers that organize processors, connections, and other components into logical units.

**Benefits**:
- **Organization**: Group related components
- **Reusability**: Create templates for common patterns
- **Security**: Apply access controls at group level
- **Monitoring**: Aggregate statistics and alerts

## 🏧 NiFi Architecture

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                NIFI CLUSTER                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           NIFI WEB UI                                      │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │   Canvas    │  │  Processor  │  │   Data      │  │   System    │       │ │
│  │  │   Design    │  │   Config    │  │ Provenance  │  │ Diagnostics │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           NIFI NODES                                       │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │     NODE 1      │  │     NODE 2      │  │     NODE N      │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │Flow Engine  │ │  │ │Flow Engine  │ │  │ │Flow Engine  │ │             │ │
│  │ │ │             │ │  │ │             │ │  │ │             │ │             │ │
│  │ │ │┌───────────┐│ │  │ │┌───────────┐│ │  │ │┌───────────┐│ │             │ │
│  │ │ ││Processors ││ │  │ ││Processors ││ │  │ ││Processors ││ │             │ │
│  │ │ ││           ││ │  │ ││           ││ │  │ ││           ││ │             │ │
│  │ │ │└───────────┘│ │  │ │└───────────┘│ │  │ │└───────────┘│ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │FlowFile     │ │  │ │FlowFile     │ │  │ │FlowFile     │ │             │ │
│  │ │ │Repository   │ │  │ │Repository   │ │  │ │Repository   │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │Content      │ │  │ │Content      │ │  │ │Content      │ │             │ │
│  │ │ │Repository   │ │  │ │Repository   │ │  │ │Repository   │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │             │ │
│  │ │ │Provenance   │ │  │ │Provenance   │ │  │ │Provenance   │ │             │ │
│  │ │ │Repository   │ │  │ │Repository   │ │  │ │Repository   │ │             │ │
│  │ │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                         │
│                                       ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         ZOOKEEPER CLUSTER                                  │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                        │ │
│  │  │ZooKeeper 1  │  │ZooKeeper 2  │  │ZooKeeper 3  │                        │ │
│  │  │             │  │             │  │             │                        │ │
│  │  │• Cluster    │  │• Leader     │  │• Flow       │                        │ │
│  │  │  State      │  │  Election   │  │  Versioning │                        │ │
│  │  │• Node       │  │• Config     │  │• User       │                        │ │
│  │  │  Discovery  │  │  Management │  │  Management │                        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Core Components**:
- **Web Server**: Hosts the user interface and REST API
- **Flow Controller**: Manages threads and coordinates processor execution
- **FlowFile Repository**: Tracks FlowFile state and attributes
- **Content Repository**: Stores FlowFile content data
- **Provenance Repository**: Records data lineage and processing history

## 🔄 Data Flow Design

### Expression Language
**Definition**: Powerful query language for accessing FlowFile attributes, system properties, and performing calculations.

```python
# Common expression language examples
expressions = {
    # Attribute access
    'filename': '${filename}',
    'file_size': '${fileSize}',
    'custom_attr': '${my.custom.attribute}',
    
    # String manipulation
    'uppercase': '${filename:toUpper()}',
    'substring': '${filename:substring(0, 5)}',
    'replace': '${filename:replace(\".txt\", \".processed\")}',
    
    # Conditional logic
    'conditional': '${fileSize:toNumber():gt(1000):ifElse(\"large\", \"small\")}',
    'equals_check': '${data.type:equals(\"customer\")}',
    
    # Date/time functions
    'current_time': '${now():format(\"yyyy-MM-dd HH:mm:ss\")}',
    'date_math': '${now():plus(1, \"days\"):format(\"yyyy-MM-dd\")}',
    
    # System properties
    'hostname': '${hostname()}',
    'java_version': '${java.version}',
    
    # Mathematical operations
    'calculation': '${fileSize:toNumber():multiply(2):plus(100)}'
}
```

### Flow Design Patterns

```python
# Common NiFi flow patterns
flow_patterns = {
    # Fan-out pattern: One input, multiple outputs
    'fan_out': {
        'source': 'GetFile',
        'router': 'RouteOnAttribute',
        'destinations': ['PutS3Object', 'PutKafka', 'PutDatabase']
    },
    
    # Fan-in pattern: Multiple inputs, one output
    'fan_in': {
        'sources': ['GetFile', 'GetHTTP', 'GetKafka'],
        'merger': 'MergeContent',
        'destination': 'PutFile'
    },
    
    # ETL pattern: Extract, Transform, Load
    'etl': {
        'extract': 'GetDatabase',
        'transform': ['ConvertAvroToJSON', 'JoltTransformJSON', 'UpdateAttribute'],
        'load': 'PutElasticsearch'
    },
    
    # Error handling pattern
    'error_handling': {
        'main_flow': 'ProcessorChain',
        'error_handling': 'LogAttribute',
        'retry_logic': 'RetryFlowFile',
        'dead_letter': 'PutFile'
    }
}
```

## 🔒 Security & Access Control

### Authentication Methods
```python
# Authentication configuration options
auth_methods = {
    'ldap': {
        'provider': 'ldap-provider',
        'url': 'ldap://localhost:389',
        'user_search_base': 'ou=users,dc=example,dc=com',
        'user_search_filter': 'cn={0}'
    },
    
    'kerberos': {
        'provider': 'kerberos-provider',
        'realm': 'EXAMPLE.COM',
        'kdc': 'kdc.example.com'
    },
    
    'certificate': {
        'keystore': '/path/to/keystore.jks',
        'truststore': '/path/to/truststore.jks',
        'client_auth': 'REQUIRED'
    }
}
```

### Authorization Policies
```python
# Role-based access control
authorization_roles = {
    'admin': [
        'view the user interface',
        'access the controller',
        'query provenance',
        'access restricted components',
        'access all policies',
        'access users/user groups'
    ],
    
    'data_engineer': [
        'view the user interface',
        'access the controller',
        'query provenance',
        'access restricted components'
    ],
    
    'read_only': [
        'view the user interface',
        'view system diagnostics'
    ]
}
```

## ⚡ Performance Optimization

### Threading Configuration
```python
# Processor threading settings
threading_config = {
    'concurrent_tasks': {
        'description': 'Number of tasks to run concurrently',
        'default': 1,
        'recommendations': {
            'cpu_intensive': 'Set to number of CPU cores',
            'io_intensive': 'Set higher than CPU cores',
            'memory_intensive': 'Keep low to avoid OOM'
        }
    },
    
    'scheduling': {
        'strategy': ['TIMER_DRIVEN', 'CRON_DRIVEN', 'EVENT_DRIVEN'],
        'run_schedule': {
            'timer_driven': '0 sec',  # Run continuously
            'cron_driven': '0 0 * * * ?'  # Hourly
        }
    }
}
```

### Memory Management
```python
# Memory optimization settings
memory_config = {
    'jvm_settings': {
        'heap_size': '-Xmx4g -Xms4g',
        'gc_settings': '-XX:+UseG1GC -XX:MaxGCPauseMillis=200'
    },
    
    'flowfile_repository': {
        'implementation': 'org.apache.nifi.controller.repository.WriteAheadFlowFileRepository',
        'partitions': 256,
        'checkpoint_interval': '2 mins'
    },
    
    'content_repository': {
        'implementation': 'org.apache.nifi.controller.repository.FileSystemRepository',
        'claim_max_appendable_size': '10 MB',
        'claim_max_flow_files': 100
    }
}
```

## 🛠️ Configuration

### Core Properties
```python
# nifi.properties key configurations
nifi_properties = {
    # Core settings
    'nifi.flow.configuration.file': './conf/flow.xml.gz',
    'nifi.flow.configuration.archive.enabled': 'true',
    'nifi.flow.configuration.archive.max.time': '30 days',
    'nifi.flow.configuration.archive.max.storage': '500 MB',
    
    # Web properties
    'nifi.web.http.host': '0.0.0.0',
    'nifi.web.http.port': '8080',
    'nifi.web.https.port': '8443',
    
    # Cluster properties
    'nifi.cluster.is.node': 'true',
    'nifi.cluster.node.address': 'localhost',
    'nifi.cluster.node.protocol.port': '11443',
    'nifi.zookeeper.connect.string': 'localhost:2181',
    
    # Repository settings
    'nifi.flowfile.repository.implementation': 'org.apache.nifi.controller.repository.WriteAheadFlowFileRepository',
    'nifi.content.repository.implementation': 'org.apache.nifi.controller.repository.FileSystemRepository',
    'nifi.provenance.repository.implementation': 'org.apache.nifi.provenance.WriteAheadProvenanceRepository'
}
```

## 🔗 Clustering

### Cluster Setup
```python
# Cluster configuration example
cluster_config = {
    'node_1': {
        'nifi.cluster.is.node': 'true',
        'nifi.cluster.node.address': '192.168.1.10',
        'nifi.cluster.node.protocol.port': '11443',
        'nifi.zookeeper.connect.string': '192.168.1.20:2181,192.168.1.21:2181,192.168.1.22:2181'
    },
    
    'node_2': {
        'nifi.cluster.is.node': 'true',
        'nifi.cluster.node.address': '192.168.1.11',
        'nifi.cluster.node.protocol.port': '11443',
        'nifi.zookeeper.connect.string': '192.168.1.20:2181,192.168.1.21:2181,192.168.1.22:2181'
    },
    
    'load_balancing': {
        'strategies': ['ROUND_ROBIN', 'SINGLE_NODE', 'PARTITION_BY_ATTRIBUTE'],
        'compression': 'GZIP',
        'timeout': '30 sec'
    }
}
```

## 📊 When to Use NiFi

**Ideal Use Cases:**
- **Data Integration**: Connecting heterogeneous systems
- **Real-time ETL**: Stream processing with visual design
- **Data Routing**: Content-based routing and transformation
- **IoT Data Processing**: Handling sensor data streams
- **Log Processing**: Collecting and processing log files
- **API Integration**: REST/SOAP service integration

**Not Ideal For:**
- **Complex Analytics**: Use Spark or Hadoop for heavy computation
- **High-Volume Batch**: Traditional batch processing tools may be better
- **Simple File Transfers**: Basic tools like rsync might suffice

## 🎯 Interview Focus Areas

1. **Core Concepts**: FlowFiles, Processors, Connections, Process Groups
2. **Architecture**: Web server, flow controller, repositories
3. **Expression Language**: Syntax and common functions
4. **Security**: Authentication, authorization, encryption
5. **Performance**: Threading, memory management, clustering
6. **Data Provenance**: Lineage tracking and auditing
7. **Flow Design**: Common patterns and best practices
8. **Integration**: Connecting with various systems and protocols
9. **Monitoring**: Metrics, alerts, and troubleshooting
10. **Clustering**: Multi-node setup and load balancing

## 📚 Quick References

- [NiFi Documentation](https://nifi.apache.org/docs.html)
- [Expression Language Guide](https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html)
- [Processor Documentation](https://nifi.apache.org/docs/nifi-docs/components/)
- [Admin Guide](https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html)
- [Developer Guide](https://nifi.apache.org/docs/nifi-docs/html/developer-guide.html)