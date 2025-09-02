# Elasticsearch Complete Guide for Data Engineering

## 🎯 What is Elasticsearch?

Elasticsearch is a **distributed search and analytics engine** built on Apache Lucene. It's essential for data engineering applications requiring full-text search, log analytics, real-time data analysis, and complex aggregations.

### Key Characteristics
- **Distributed**: Scales horizontally across multiple nodes
- **Real-time**: Near real-time search and analytics
- **Schema-free**: Dynamic mapping with JSON documents
- **RESTful API**: HTTP-based API for all operations
- **Analytics**: Powerful aggregation framework

## 💾 Core Concepts

### 1. Basic Architecture
```bash
# Cluster structure
Cluster
├── Node 1
│   ├── Index: logs-2024
│   │   ├── Shard 0 (Primary)
│   │   └── Shard 1 (Replica)
│   └── Index: users
│       └── Shard 0 (Primary)
└── Node 2
    ├── Index: logs-2024
    │   ├── Shard 1 (Primary)
    │   └── Shard 0 (Replica)
    └── Index: users
        └── Shard 0 (Replica)
```

### 2. Index Management
```bash
# Create index with mapping
PUT /users
{
  "mappings": {
    "properties": {
      "user_id": {"type": "keyword"},
      "name": {"type": "text"},
      "email": {"type": "keyword"},
      "age": {"type": "integer"},
      "created_at": {"type": "date"},
      "preferences": {"type": "object"},
      "tags": {"type": "keyword"}
    }
  },
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1,
    "refresh_interval": "1s"
  }
}

# Index documents
POST /users/_doc/1
{
  "user_id": "user_001",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "created_at": "2024-01-15T10:30:00Z",
  "preferences": {
    "theme": "dark",
    "notifications": true
  },
  "tags": ["premium", "active"]
}

# Bulk indexing
POST /_bulk
{"index": {"_index": "users", "_id": "2"}}
{"user_id": "user_002", "name": "Jane Smith", "email": "jane@example.com", "age": 25}
{"index": {"_index": "users", "_id": "3"}}
{"user_id": "user_003", "name": "Bob Johnson", "email": "bob@example.com", "age": 35}
```

### 3. Search Operations
```bash
# Basic search
GET /users/_search
{
  "query": {
    "match": {
      "name": "John"
    }
  }
}

# Complex search with filters
GET /users/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"name": "John"}}
      ],
      "filter": [
        {"range": {"age": {"gte": 25, "lte": 40}}},
        {"terms": {"tags": ["premium", "active"]}}
      ]
    }
  },
  "sort": [
    {"created_at": {"order": "desc"}}
  ],
  "size": 10,
  "from": 0
}

# Aggregations
GET /users/_search
{
  "size": 0,
  "aggs": {
    "age_groups": {
      "histogram": {
        "field": "age",
        "interval": 10
      }
    },
    "popular_tags": {
      "terms": {
        "field": "tags",
        "size": 10
      }
    },
    "avg_age": {
      "avg": {
        "field": "age"
      }
    }
  }
}
```

## 🔧 Data Engineering Use Cases

### 1. Log Analytics Pipeline
```python
from elasticsearch import Elasticsearch, helpers
import json
from datetime import datetime
import logging

class LogAnalytics:
    def __init__(self, es_hosts=['localhost:9200']):
        self.es = Elasticsearch(
            es_hosts,
            retry_on_timeout=True,
            max_retries=3,
            timeout=30
        )
    
    def create_log_index_template(self):
        """Create index template for log data"""
        template = {
            "index_patterns": ["logs-*"],
            "template": {
                "settings": {
                    "number_of_shards": 2,
                    "number_of_replicas": 1,
                    "refresh_interval": "5s",
                    "index.lifecycle.name": "logs-policy",
                    "index.lifecycle.rollover_alias": "logs"
                },
                "mappings": {
                    "properties": {
                        "@timestamp": {"type": "date"},
                        "level": {"type": "keyword"},
                        "message": {"type": "text"},
                        "service": {"type": "keyword"},
                        "host": {"type": "keyword"},
                        "user_id": {"type": "keyword"},
                        "request_id": {"type": "keyword"},
                        "duration_ms": {"type": "integer"},
                        "status_code": {"type": "integer"},
                        "ip_address": {"type": "ip"},
                        "user_agent": {"type": "text"},
                        "tags": {"type": "keyword"}
                    }
                }
            }
        }
        
        return self.es.indices.put_index_template(
            name="logs-template",
            body=template
        )
    
    def bulk_index_logs(self, log_entries):
        """Bulk index log entries"""
        actions = []
        
        for log_entry in log_entries:
            # Generate index name based on date
            index_date = datetime.now().strftime('%Y.%m.%d')
            index_name = f"logs-{index_date}"
            
            action = {
                "_index": index_name,
                "_source": {
                    "@timestamp": log_entry.get('timestamp', datetime.now().isoformat()),
                    "level": log_entry.get('level', 'INFO'),
                    "message": log_entry.get('message', ''),
                    "service": log_entry.get('service', 'unknown'),
                    "host": log_entry.get('host', 'unknown'),
                    "user_id": log_entry.get('user_id'),
                    "request_id": log_entry.get('request_id'),
                    "duration_ms": log_entry.get('duration_ms'),
                    "status_code": log_entry.get('status_code'),
                    "ip_address": log_entry.get('ip_address'),
                    "user_agent": log_entry.get('user_agent'),
                    "tags": log_entry.get('tags', [])
                }
            }
            actions.append(action)
        
        # Bulk index
        success, failed = helpers.bulk(
            self.es,
            actions,
            chunk_size=1000,
            request_timeout=60
        )
        
        return success, failed
    
    def search_logs(self, query_params):
        """Search logs with various filters"""
        query = {
            "bool": {
                "must": [],
                "filter": []
            }
        }
        
        # Text search
        if query_params.get('message'):
            query["bool"]["must"].append({
                "match": {
                    "message": query_params['message']
                }
            })
        
        # Time range filter
        if query_params.get('start_time') or query_params.get('end_time'):
            time_range = {}
            if query_params.get('start_time'):
                time_range['gte'] = query_params['start_time']
            if query_params.get('end_time'):
                time_range['lte'] = query_params['end_time']
            
            query["bool"]["filter"].append({
                "range": {
                    "@timestamp": time_range
                }
            })
        
        # Service filter
        if query_params.get('service'):
            query["bool"]["filter"].append({
                "term": {
                    "service": query_params['service']
                }
            })
        
        # Log level filter
        if query_params.get('level'):
            query["bool"]["filter"].append({
                "term": {
                    "level": query_params['level']
                }
            })
        
        search_body = {
            "query": query,
            "sort": [
                {"@timestamp": {"order": "desc"}}
            ],
            "size": query_params.get('size', 100)
        }
        
        return self.es.search(
            index="logs-*",
            body=search_body
        )
    
    def get_log_analytics(self, time_range='1h'):
        """Get log analytics and metrics"""
        analytics_query = {
            "size": 0,
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": f"now-{time_range}"
                    }
                }
            },
            "aggs": {
                "log_levels": {
                    "terms": {
                        "field": "level",
                        "size": 10
                    }
                },
                "services": {
                    "terms": {
                        "field": "service",
                        "size": 20
                    }
                },
                "error_rate": {
                    "filter": {
                        "term": {"level": "ERROR"}
                    }
                },
                "avg_response_time": {
                    "avg": {
                        "field": "duration_ms"
                    }
                },
                "timeline": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "fixed_interval": "5m"
                    },
                    "aggs": {
                        "error_count": {
                            "filter": {
                                "term": {"level": "ERROR"}
                            }
                        }
                    }
                }
            }
        }
        
        return self.es.search(
            index="logs-*",
            body=analytics_query
        )

# Usage example
log_analytics = LogAnalytics()

# Create index template
log_analytics.create_log_index_template()

# Sample log entries
sample_logs = [
    {
        'timestamp': '2024-01-15T10:30:00Z',
        'level': 'INFO',
        'message': 'User login successful',
        'service': 'auth-service',
        'host': 'web-01',
        'user_id': 'user_123',
        'request_id': 'req_456',
        'duration_ms': 150,
        'status_code': 200,
        'ip_address': '192.168.1.100'
    },
    {
        'timestamp': '2024-01-15T10:31:00Z',
        'level': 'ERROR',
        'message': 'Database connection failed',
        'service': 'user-service',
        'host': 'web-02',
        'duration_ms': 5000,
        'status_code': 500,
        'tags': ['database', 'error']
    }
]

# Index logs
success, failed = log_analytics.bulk_index_logs(sample_logs)
print(f"Indexed {success} logs successfully")

# Search logs
search_results = log_analytics.search_logs({
    'level': 'ERROR',
    'start_time': 'now-1h',
    'size': 50
})

print(f"Found {search_results['hits']['total']['value']} error logs")
```

### 2. Real-time Data Analytics
```python
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import json

class RealTimeAnalytics:
    def __init__(self, es_hosts=['localhost:9200']):
        self.es = Elasticsearch(es_hosts)
    
    def create_events_index(self):
        """Create index for real-time events"""
        mapping = {
            "mappings": {
                "properties": {
                    "event_id": {"type": "keyword"},
                    "user_id": {"type": "keyword"},
                    "event_type": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "properties": {"type": "object"},
                    "session_id": {"type": "keyword"},
                    "page_url": {"type": "keyword"},
                    "referrer": {"type": "keyword"},
                    "user_agent": {"type": "text"},
                    "ip_address": {"type": "ip"},
                    "location": {"type": "geo_point"}
                }
            },
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 1,
                "refresh_interval": "1s"
            }
        }
        
        return self.es.indices.create(
            index="events",
            body=mapping,
            ignore=400  # Ignore if index already exists
        )
    
    def track_event(self, event_data):
        """Track a single event"""
        return self.es.index(
            index="events",
            body=event_data
        )
    
    def get_real_time_dashboard(self):
        """Get real-time dashboard metrics"""
        dashboard_query = {
            "size": 0,
            "query": {
                "range": {
                    "timestamp": {
                        "gte": "now-1h"
                    }
                }
            },
            "aggs": {
                "total_events": {
                    "value_count": {
                        "field": "event_id"
                    }
                },
                "unique_users": {
                    "cardinality": {
                        "field": "user_id"
                    }
                },
                "event_types": {
                    "terms": {
                        "field": "event_type",
                        "size": 10
                    }
                },
                "events_over_time": {
                    "date_histogram": {
                        "field": "timestamp",
                        "fixed_interval": "1m"
                    }
                },
                "top_pages": {
                    "terms": {
                        "field": "page_url",
                        "size": 10
                    }
                },
                "geographic_distribution": {
                    "geo_hash_grid": {
                        "field": "location",
                        "precision": 3
                    }
                }
            }
        }
        
        return self.es.search(
            index="events",
            body=dashboard_query
        )
    
    def get_user_journey(self, user_id, hours=24):
        """Get user journey for specific user"""
        journey_query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"user_id": user_id}},
                        {"range": {
                            "timestamp": {
                                "gte": f"now-{hours}h"
                            }
                        }}
                    ]
                }
            },
            "sort": [
                {"timestamp": {"order": "asc"}}
            ],
            "size": 1000
        }
        
        return self.es.search(
            index="events",
            body=journey_query
        )
    
    def detect_anomalies(self):
        """Detect anomalies in event patterns"""
        anomaly_query = {
            "size": 0,
            "query": {
                "range": {
                    "timestamp": {
                        "gte": "now-24h"
                    }
                }
            },
            "aggs": {
                "events_per_hour": {
                    "date_histogram": {
                        "field": "timestamp",
                        "fixed_interval": "1h"
                    },
                    "aggs": {
                        "event_count": {
                            "value_count": {
                                "field": "event_id"
                            }
                        },
                        "anomaly_detection": {
                            "moving_avg": {
                                "buckets_path": "event_count",
                                "window": 6,
                                "model": "linear"
                            }
                        }
                    }
                }
            }
        }
        
        return self.es.search(
            index="events",
            body=anomaly_query
        )

# Usage
analytics = RealTimeAnalytics()
analytics.create_events_index()

# Track events
event = {
    "event_id": "evt_123",
    "user_id": "user_456",
    "event_type": "page_view",
    "timestamp": datetime.now().isoformat(),
    "properties": {
        "page_title": "Dashboard",
        "load_time": 1.2
    },
    "page_url": "/dashboard",
    "session_id": "sess_789"
}

analytics.track_event(event)

# Get dashboard metrics
dashboard = analytics.get_real_time_dashboard()
print(f"Total events in last hour: {dashboard['aggregations']['total_events']['value']}")
```

## ⚡ Performance Optimization

### 1. Index Optimization
```bash
# Index settings for performance
PUT /high_performance_index
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "30s",
    "index.translog.flush_threshold_size": "1gb",
    "index.merge.policy.max_merged_segment": "5gb",
    "index.compound_format": false
  },
  "mappings": {
    "properties": {
      "id": {"type": "keyword", "store": true},
      "title": {"type": "text", "analyzer": "standard"},
      "content": {"type": "text", "analyzer": "standard", "store": false},
      "tags": {"type": "keyword"},
      "created_at": {"type": "date", "format": "strict_date_optional_time"}
    }
  }
}

# Force merge for read-heavy indices
POST /logs-2024.01.01/_forcemerge?max_num_segments=1

# Update index settings
PUT /my_index/_settings
{
  "refresh_interval": "1s",
  "number_of_replicas": 2
}
```

### 2. Query Optimization
```bash
# Use filters instead of queries when possible
GET /users/_search
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"status": "active"}},
        {"range": {"age": {"gte": 18}}}
      ]
    }
  }
}

# Use source filtering
GET /users/_search
{
  "_source": ["name", "email", "created_at"],
  "query": {"match_all": {}}
}

# Use scroll for large result sets
POST /users/_search?scroll=1m
{
  "size": 1000,
  "query": {"match_all": {}}
}
```

## 🔒 Security and Monitoring

### 1. Security Configuration
```bash
# Enable security in elasticsearch.yml
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.http.ssl.enabled: true

# Create users and roles
POST /_security/role/data_engineer
{
  "cluster": ["monitor"],
  "indices": [
    {
      "names": ["logs-*", "events-*"],
      "privileges": ["read", "write", "create_index"]
    }
  ]
}

POST /_security/user/john_doe
{
  "password": "secure_password",
  "roles": ["data_engineer"],
  "full_name": "John Doe",
  "email": "john@company.com"
}
```

### 2. Monitoring and Alerting
```python
def monitor_cluster_health():
    """Monitor Elasticsearch cluster health"""
    health = es.cluster.health()
    
    metrics = {
        'cluster_name': health['cluster_name'],
        'status': health['status'],
        'number_of_nodes': health['number_of_nodes'],
        'active_primary_shards': health['active_primary_shards'],
        'active_shards': health['active_shards'],
        'relocating_shards': health['relocating_shards'],
        'initializing_shards': health['initializing_shards'],
        'unassigned_shards': health['unassigned_shards']
    }
    
    # Alert on yellow or red status
    if health['status'] in ['yellow', 'red']:
        send_alert(f"Cluster status is {health['status']}")
    
    return metrics

def monitor_index_performance():
    """Monitor index performance metrics"""
    stats = es.indices.stats(index='_all')
    
    for index_name, index_stats in stats['indices'].items():
        metrics = {
            'index': index_name,
            'docs_count': index_stats['total']['docs']['count'],
            'store_size': index_stats['total']['store']['size_in_bytes'],
            'indexing_rate': index_stats['total']['indexing']['index_total'],
            'search_rate': index_stats['total']['search']['query_total']
        }
        
        # Check for performance issues
        if metrics['store_size'] > 50 * 1024 * 1024 * 1024:  # 50GB
            print(f"Large index detected: {index_name}")
```

## 🎯 Best Practices Summary

### 1. Index Design Best Practices
- **Proper Mapping**: Define explicit mappings for better performance
- **Shard Sizing**: Aim for 10-50GB per shard
- **Time-based Indices**: Use date-based indices for time-series data
- **Index Templates**: Use templates for consistent index creation

### 2. Query Optimization Best Practices
- **Use Filters**: Prefer filters over queries for exact matches
- **Limit Source**: Only return necessary fields
- **Pagination**: Use scroll API for large result sets
- **Caching**: Leverage query and filter caching

### 3. Performance Best Practices
- **Bulk Operations**: Use bulk API for indexing multiple documents
- **Refresh Interval**: Adjust refresh interval based on use case
- **Force Merge**: Regularly force merge read-heavy indices
- **Monitor Resources**: Keep track of CPU, memory, and disk usage

### 4. Security Best Practices
- **Enable Security**: Use X-Pack security features
- **Role-based Access**: Implement proper role-based access control
- **SSL/TLS**: Enable encryption for data in transit
- **Audit Logging**: Enable audit logging for compliance

This guide provides essential Elasticsearch knowledge for data engineering. Focus on understanding indexing strategies, search optimization, and aggregations for building powerful search and analytics applications.