# Elasticsearch Comprehensive Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Indexing & Mapping (16-30)](#indexing--mapping-16-30)
3. [Search & Query DSL (31-45)](#search--query-dsl-31-45)
4. [Performance & Optimization (46-60)](#performance--optimization-46-60)
5. [Clustering & Scaling (61-75)](#clustering--scaling-61-75)
6. [Monitoring & Operations (76-90)](#monitoring--operations-76-90)
7. [Integration & Architecture (91-100)](#integration--architecture-91-100)

---

## 🎯 **Introduction**

Elasticsearch is a distributed, RESTful search and analytics engine built on Apache Lucene. For data engineers, Elasticsearch provides powerful full-text search, real-time analytics, log analysis, and data visualization capabilities.

**Why Elasticsearch is Critical for Data Engineers:**
- **Full-Text Search**: Advanced search capabilities with relevance scoring
- **Real-Time Analytics**: Near real-time data ingestion and analysis
- **Scalability**: Horizontal scaling with automatic sharding
- **Schema-Free**: Dynamic mapping for flexible data structures
- **Ecosystem Integration**: Seamless integration with Logstash, Kibana, and Beats

---

## Core Concepts Questions (1-15)

### 1. Explain Elasticsearch architecture and core components.
**Answer**: 
Elasticsearch is built on a distributed architecture with several key components.

**Core Components:**
- **Cluster**: Collection of nodes that hold data and provide search capabilities
- **Node**: Single server that stores data and participates in clustering
- **Index**: Collection of documents with similar characteristics
- **Type**: Logical category within an index (deprecated in 7.x+)
- **Document**: Basic unit of information that can be indexed
- **Shard**: Subdivision of an index for horizontal scaling
- **Replica**: Copy of a shard for high availability

```python
from elasticsearch import Elasticsearch

# Connect to Elasticsearch cluster
es = Elasticsearch([
    {'host': 'localhost', 'port': 9200},
    {'host': 'es-node2', 'port': 9200},
    {'host': 'es-node3', 'port': 9200}
])

# Check cluster health
health = es.cluster.health()
print(f"Cluster status: {health['status']}")
print(f"Number of nodes: {health['number_of_nodes']}")
print(f"Active shards: {health['active_shards']}")

# Get cluster information
info = es.info()
print(f"Elasticsearch version: {info['version']['number']}")
```

### 2. What are the differences between Elasticsearch and traditional databases?
**Answer**: 
Elasticsearch differs from traditional RDBMS in several fundamental ways.

**Key Differences:**
- **Data Model**: Document-oriented vs. relational tables
- **Schema**: Dynamic mapping vs. fixed schema
- **Search**: Full-text search with relevance scoring vs. exact matches
- **Scaling**: Horizontal scaling with sharding vs. vertical scaling
- **ACID**: Eventually consistent vs. ACID compliant
- **Query Language**: Query DSL (JSON) vs. SQL

```python
# Document structure in Elasticsearch
document = {
    "user_id": "12345",
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "interests": ["data engineering", "elasticsearch", "python"],
    "profile": {
        "bio": "Data engineer with 5 years experience",
        "location": "San Francisco",
        "skills": ["Python", "Elasticsearch", "Kafka"]
    },
    "created_at": "2024-01-15T10:30:00Z"
}

# Index document
response = es.index(
    index="users",
    id="12345",
    body=document
)
print(f"Document indexed: {response['result']}")
```

### 3. How does Elasticsearch handle data distribution and sharding?
**Answer**: 
Elasticsearch automatically distributes data across multiple shards for scalability and performance.

**Sharding Concepts:**
- **Primary Shards**: Original shards that hold data
- **Replica Shards**: Copies of primary shards for redundancy
- **Routing**: Determines which shard stores a document
- **Rebalancing**: Automatic redistribution of shards

```python
# Create index with custom shard configuration
index_settings = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1,
        "index": {
            "routing": {
                "allocation": {
                    "include": {
                        "_tier_preference": "data_hot"
                    }
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "user_id": {"type": "keyword"},
            "timestamp": {"type": "date"},
            "message": {"type": "text"},
            "tags": {"type": "keyword"}
        }
    }
}

# Create index
es.indices.create(index="logs", body=index_settings)

# Check shard allocation
shards = es.cat.shards(index="logs", format="json")
for shard in shards:
    print(f"Shard {shard['shard']}: {shard['prirep']} on node {shard['node']}")
```

## Indexing & Mapping (16-30)

### 4. How do you design effective mappings for different data types?
**Answer**: 
Proper mapping design is crucial for search performance and functionality.

**Field Types and Mappings:**
```python
# Comprehensive mapping example
mapping = {
    "mappings": {
        "properties": {
            # Text fields for full-text search
            "title": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            
            # Keyword for exact matches and aggregations
            "status": {
                "type": "keyword"
            },
            
            # Numeric fields
            "price": {
                "type": "float"
            },
            "quantity": {
                "type": "integer"
            },
            
            # Date fields
            "created_at": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            },
            
            # Nested objects
            "user": {
                "type": "nested",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text"},
                    "email": {"type": "keyword"}
                }
            },
            
            # Geo-point for location data
            "location": {
                "type": "geo_point"
            },
            
            # Object field
            "metadata": {
                "type": "object",
                "properties": {
                    "source": {"type": "keyword"},
                    "version": {"type": "keyword"}
                }
            }
        }
    }
}

# Create index with mapping
es.indices.create(index="products", body=mapping)
```

### 5. How do you handle dynamic mapping and field explosion?
**Answer**: 
Dynamic mapping can lead to field explosion; proper configuration prevents this issue.

**Dynamic Mapping Control:**
```python
# Strict dynamic mapping
strict_mapping = {
    "mappings": {
        "dynamic": "strict",  # Only allow predefined fields
        "properties": {
            "title": {"type": "text"},
            "price": {"type": "float"},
            "category": {"type": "keyword"}
        }
    }
}

# Dynamic templates for pattern-based mapping
dynamic_template_mapping = {
    "mappings": {
        "dynamic_templates": [
            {
                "strings_as_keywords": {
                    "match_mapping_type": "string",
                    "match": "*_id",
                    "mapping": {
                        "type": "keyword"
                    }
                }
            },
            {
                "dates": {
                    "match": "*_date",
                    "mapping": {
                        "type": "date",
                        "format": "yyyy-MM-dd"
                    }
                }
            }
        ],
        "properties": {
            "timestamp": {"type": "date"}
        }
    }
}

# Index with field limit
limited_fields_mapping = {
    "settings": {
        "index.mapping.total_fields.limit": 1000,
        "index.mapping.depth.limit": 20,
        "index.mapping.nested_fields.limit": 50
    },
    "mappings": {
        "dynamic": "false",  # Ignore unmapped fields
        "properties": {
            "message": {"type": "text"}
        }
    }
}

es.indices.create(index="limited_index", body=limited_fields_mapping)
```

### 6. How do you implement custom analyzers for text processing?
**Answer**: 
Custom analyzers provide fine-grained control over text processing.

**Custom Analyzer Configuration:**
```python
# Custom analyzer with tokenizers and filters
custom_analyzer_settings = {
    "settings": {
        "analysis": {
            "tokenizer": {
                "custom_tokenizer": {
                    "type": "pattern",
                    "pattern": "[\\W&&[^-]]+"
                }
            },
            "filter": {
                "custom_stop": {
                    "type": "stop",
                    "stopwords": ["the", "and", "or", "but"]
                },
                "custom_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "custom_synonym": {
                    "type": "synonym",
                    "synonyms": [
                        "quick,fast,rapid",
                        "big,large,huge"
                    ]
                }
            },
            "analyzer": {
                "custom_text_analyzer": {
                    "type": "custom",
                    "tokenizer": "custom_tokenizer",
                    "filter": [
                        "lowercase",
                        "custom_stop",
                        "custom_synonym",
                        "custom_stemmer"
                    ]
                },
                "search_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "custom_stop"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "custom_text_analyzer",
                "search_analyzer": "search_analyzer"
            }
        }
    }
}

# Create index with custom analyzer
es.indices.create(index="custom_analyzed", body=custom_analyzer_settings)

# Test analyzer
analysis_result = es.indices.analyze(
    index="custom_analyzed",
    body={
        "analyzer": "custom_text_analyzer",
        "text": "The quick brown fox jumps"
    }
)

for token in analysis_result['tokens']:
    print(f"Token: {token['token']}, Position: {token['position']}")
```

## Search & Query DSL (31-45)

### 7. How do you construct complex search queries using Query DSL?
**Answer**: 
Elasticsearch Query DSL provides powerful query construction capabilities.

**Complex Query Examples:**
```python
# Multi-field search with boosting
complex_query = {
    "query": {
        "bool": {
            "must": [
                {
                    "multi_match": {
                        "query": "elasticsearch data engineering",
                        "fields": ["title^3", "content^2", "tags"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                }
            ],
            "filter": [
                {
                    "range": {
                        "created_at": {
                            "gte": "2024-01-01",
                            "lte": "2024-12-31"
                        }
                    }
                },
                {
                    "terms": {
                        "status": ["published", "featured"]
                    }
                }
            ],
            "should": [
                {
                    "match": {
                        "category": "tutorial"
                    }
                }
            ],
            "minimum_should_match": 0
        }
    },
    "sort": [
        {"_score": {"order": "desc"}},
        {"created_at": {"order": "desc"}}
    ],
    "highlight": {
        "fields": {
            "title": {},
            "content": {
                "fragment_size": 150,
                "number_of_fragments": 3
            }
        }
    },
    "aggs": {
        "categories": {
            "terms": {
                "field": "category.keyword",
                "size": 10
            }
        },
        "date_histogram": {
            "date_histogram": {
                "field": "created_at",
                "calendar_interval": "month"
            }
        }
    }
}

# Execute search
response = es.search(index="articles", body=complex_query)

# Process results
print(f"Total hits: {response['hits']['total']['value']}")
for hit in response['hits']['hits']:
    print(f"Score: {hit['_score']}, Title: {hit['_source']['title']}")
    
    # Process highlights
    if 'highlight' in hit:
        for field, highlights in hit['highlight'].items():
            print(f"Highlighted {field}: {highlights}")
```

### 8. How do you implement aggregations for analytics?
**Answer**: 
Elasticsearch aggregations provide powerful analytics capabilities.

**Advanced Aggregations:**
```python
# Complex aggregation query
analytics_query = {
    "size": 0,  # Don't return documents, only aggregations
    "aggs": {
        # Metric aggregations
        "total_revenue": {
            "sum": {"field": "amount"}
        },
        "avg_order_value": {
            "avg": {"field": "amount"}
        },
        "revenue_stats": {
            "stats": {"field": "amount"}
        },
        
        # Bucket aggregations
        "sales_by_category": {
            "terms": {
                "field": "category.keyword",
                "size": 10
            },
            "aggs": {
                "category_revenue": {
                    "sum": {"field": "amount"}
                },
                "avg_category_price": {
                    "avg": {"field": "amount"}
                }
            }
        },
        
        # Date histogram
        "sales_over_time": {
            "date_histogram": {
                "field": "order_date",
                "calendar_interval": "day"
            },
            "aggs": {
                "daily_revenue": {
                    "sum": {"field": "amount"}
                },
                "daily_orders": {
                    "value_count": {"field": "order_id"}
                }
            }
        },
        
        # Range aggregation
        "price_ranges": {
            "range": {
                "field": "amount",
                "ranges": [
                    {"to": 50},
                    {"from": 50, "to": 100},
                    {"from": 100, "to": 200},
                    {"from": 200}
                ]
            }
        },
        
        # Nested aggregation
        "customer_analysis": {
            "nested": {
                "path": "customer"
            },
            "aggs": {
                "customer_segments": {
                    "terms": {
                        "field": "customer.segment.keyword"
                    },
                    "aggs": {
                        "segment_revenue": {
                            "reverse_nested": {},
                            "aggs": {
                                "total": {
                                    "sum": {"field": "amount"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

# Execute aggregation query
response = es.search(index="orders", body=analytics_query)

# Process aggregation results
aggs = response['aggregations']
print(f"Total Revenue: ${aggs['total_revenue']['value']:.2f}")
print(f"Average Order Value: ${aggs['avg_order_value']['value']:.2f}")

# Process bucket aggregations
for bucket in aggs['sales_by_category']['buckets']:
    category = bucket['key']
    count = bucket['doc_count']
    revenue = bucket['category_revenue']['value']
    print(f"Category {category}: {count} orders, ${revenue:.2f} revenue")
```

### 9. How do you implement search suggestions and autocomplete?
**Answer**: 
Elasticsearch provides multiple approaches for search suggestions and autocomplete.

**Completion Suggester:**
```python
# Index mapping with completion suggester
suggestion_mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "suggest": {
                "type": "completion",
                "analyzer": "simple",
                "preserve_separators": True,
                "preserve_position_increments": True,
                "max_input_length": 50
            }
        }
    }
}

es.indices.create(index="suggestions", body=suggestion_mapping)

# Index documents with suggestions
documents = [
    {
        "title": "Elasticsearch Data Engineering",
        "suggest": {
            "input": ["elasticsearch", "data engineering", "search engine"],
            "weight": 10
        }
    },
    {
        "title": "Apache Kafka Streaming",
        "suggest": {
            "input": ["kafka", "streaming", "apache kafka"],
            "weight": 8
        }
    }
]

for i, doc in enumerate(documents):
    es.index(index="suggestions", id=i, body=doc)

# Search suggestions
suggestion_query = {
    "suggest": {
        "title_suggest": {
            "prefix": "data",
            "completion": {
                "field": "suggest",
                "size": 5,
                "skip_duplicates": True
            }
        }
    }
}

response = es.search(index="suggestions", body=suggestion_query)
suggestions = response['suggest']['title_suggest'][0]['options']

for suggestion in suggestions:
    print(f"Suggestion: {suggestion['text']}, Score: {suggestion['_score']}")
```

**Search-as-you-type:**
```python
# Search-as-you-type field mapping
search_as_type_mapping = {
    "mappings": {
        "properties": {
            "title": {
                "type": "search_as_you_type"
            },
            "content": {"type": "text"}
        }
    }
}

es.indices.create(index="search_as_type", body=search_as_type_mapping)

# Query for search-as-you-type
search_query = {
    "query": {
        "multi_match": {
            "query": "data eng",
            "type": "bool_prefix",
            "fields": [
                "title",
                "title._2gram",
                "title._3gram"
            ]
        }
    }
}

response = es.search(index="search_as_type", body=search_query)
```

## Performance & Optimization (46-60)

### 10. How do you optimize Elasticsearch performance for large datasets?
**Answer**: 
Multiple strategies for optimizing Elasticsearch performance at scale.

**Indexing Optimization:**
```python
# Bulk indexing for better performance
from elasticsearch.helpers import bulk

def bulk_index_documents(documents, index_name):
    """Bulk index documents efficiently"""
    
    # Prepare bulk actions
    actions = []
    for doc in documents:
        action = {
            "_index": index_name,
            "_source": doc
        }
        actions.append(action)
    
    # Bulk index with optimized settings
    success, failed = bulk(
        es,
        actions,
        chunk_size=1000,
        request_timeout=60,
        max_retries=3,
        initial_backoff=2,
        max_backoff=600
    )
    
    return success, failed

# Optimize index settings for bulk loading
bulk_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,  # Disable replicas during bulk loading
        "refresh_interval": "30s",  # Reduce refresh frequency
        "index": {
            "translog": {
                "flush_threshold_size": "1gb",
                "sync_interval": "30s"
            }
        }
    }
}

# Apply settings during bulk loading
es.indices.put_settings(index="bulk_index", body=bulk_settings["settings"])

# After bulk loading, restore normal settings
normal_settings = {
    "number_of_replicas": 1,
    "refresh_interval": "1s"
}

es.indices.put_settings(index="bulk_index", body=normal_settings)
```

**Query Optimization:**
```python
# Optimized query patterns
def optimized_search_patterns():
    """Examples of optimized search patterns"""
    
    # Use filters instead of queries when possible
    optimized_query = {
        "query": {
            "bool": {
                "filter": [  # Filters are cached and faster
                    {"term": {"status": "active"}},
                    {"range": {"created_at": {"gte": "2024-01-01"}}}
                ],
                "must": [  # Only use must for scoring
                    {"match": {"title": "elasticsearch"}}
                ]
            }
        }
    }
    
    # Use specific field queries
    field_specific_query = {
        "query": {
            "term": {"user_id.keyword": "12345"}  # Use .keyword for exact matches
        }
    }
    
    # Limit returned fields
    limited_fields_query = {
        "query": {"match_all": {}},
        "_source": ["title", "created_at", "author"],  # Only return needed fields
        "size": 10
    }
    
    return optimized_query, field_specific_query, limited_fields_query

# Index template for consistent optimization
index_template = {
    "index_patterns": ["logs-*"],
    "template": {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "index": {
                "codec": "best_compression",  # Better compression
                "sort": {
                    "field": ["timestamp"],
                    "order": ["desc"]
                }
            }
        },
        "mappings": {
            "properties": {
                "timestamp": {"type": "date"},
                "level": {"type": "keyword"},
                "message": {
                    "type": "text",
                    "norms": False  # Disable norms if scoring not needed
                }
            }
        }
    }
}

es.indices.put_index_template(name="logs_template", body=index_template)
```

### 11. How do you implement index lifecycle management (ILM)?
**Answer**: 
ILM automates index management based on performance, resiliency, and retention requirements.

**ILM Policy Configuration:**
```python
# Define ILM policy
ilm_policy = {
    "policy": {
        "phases": {
            "hot": {
                "actions": {
                    "rollover": {
                        "max_size": "10GB",
                        "max_age": "7d",
                        "max_docs": 10000000
                    },
                    "set_priority": {
                        "priority": 100
                    }
                }
            },
            "warm": {
                "min_age": "7d",
                "actions": {
                    "set_priority": {
                        "priority": 50
                    },
                    "allocate": {
                        "number_of_replicas": 0
                    },
                    "forcemerge": {
                        "max_num_segments": 1
                    }
                }
            },
            "cold": {
                "min_age": "30d",
                "actions": {
                    "set_priority": {
                        "priority": 0
                    },
                    "allocate": {
                        "number_of_replicas": 0,
                        "include": {
                            "box_type": "cold"
                        }
                    }
                }
            },
            "delete": {
                "min_age": "90d",
                "actions": {
                    "delete": {}
                }
            }
        }
    }
}

# Create ILM policy
es.ilm.put_lifecycle(policy="logs_policy", body=ilm_policy)

# Index template with ILM
ilm_template = {
    "index_patterns": ["logs-*"],
    "template": {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "index": {
                "lifecycle": {
                    "name": "logs_policy",
                    "rollover_alias": "logs"
                }
            }
        }
    }
}

es.indices.put_index_template(name="logs_ilm_template", body=ilm_template)

# Create initial index with alias
initial_index = {
    "aliases": {
        "logs": {
            "is_write_index": True
        }
    }
}

es.indices.create(index="logs-000001", body=initial_index)
```

## Clustering & Scaling (61-75)

### 12. How do you design and manage Elasticsearch clusters?
**Answer**: 
Proper cluster design is essential for performance, reliability, and scalability.

**Cluster Architecture:**
```python
# Cluster health monitoring
def monitor_cluster_health():
    """Monitor cluster health and performance"""
    
    # Basic cluster health
    health = es.cluster.health()
    print(f"Cluster Status: {health['status']}")
    print(f"Nodes: {health['number_of_nodes']}")
    print(f"Data Nodes: {health['number_of_data_nodes']}")
    print(f"Active Shards: {health['active_shards']}")
    print(f"Relocating Shards: {health['relocating_shards']}")
    print(f"Unassigned Shards: {health['unassigned_shards']}")
    
    # Node information
    nodes = es.nodes.info()
    for node_id, node_info in nodes['nodes'].items():
        print(f"Node: {node_info['name']}")
        print(f"  Roles: {node_info['roles']}")
        print(f"  Version: {node_info['version']}")
        print(f"  JVM Heap: {node_info['jvm']['mem']['heap_max_in_bytes']}")
    
    # Cluster stats
    stats = es.cluster.stats()
    print(f"Total Documents: {stats['indices']['count']}")
    print(f"Total Size: {stats['indices']['store']['size_in_bytes']}")
    
    return health['status'] == 'green'

# Shard allocation awareness
allocation_settings = {
    "persistent": {
        "cluster.routing.allocation.awareness.attributes": "rack_id",
        "cluster.routing.allocation.awareness.force.rack_id.values": "rack1,rack2,rack3"
    }
}

es.cluster.put_settings(body=allocation_settings)
```

**Node Roles and Configuration:**
```python
# Different node role configurations
node_configurations = {
    "master_node": {
        "node.roles": ["master"],
        "node.data": False,
        "discovery.seed_hosts": ["master1", "master2", "master3"],
        "cluster.initial_master_nodes": ["master1", "master2", "master3"]
    },
    
    "data_hot_node": {
        "node.roles": ["data_hot", "data_content"],
        "node.attr.box_type": "hot",
        "path.data": ["/fast_ssd/elasticsearch"]
    },
    
    "data_warm_node": {
        "node.roles": ["data_warm", "data_content"],
        "node.attr.box_type": "warm",
        "path.data": ["/slower_disk/elasticsearch"]
    },
    
    "data_cold_node": {
        "node.roles": ["data_cold", "data_content"],
        "node.attr.box_type": "cold",
        "path.data": ["/archive_storage/elasticsearch"]
    },
    
    "coordinating_node": {
        "node.roles": [],  # No specific roles = coordinating only
        "node.data": False,
        "node.master": False
    }
}

def configure_cluster_settings():
    """Configure cluster-wide settings"""
    cluster_settings = {
        "persistent": {
            # Shard allocation settings
            "cluster.routing.allocation.disk.threshold.enabled": True,
            "cluster.routing.allocation.disk.watermark.low": "85%",
            "cluster.routing.allocation.disk.watermark.high": "90%",
            "cluster.routing.allocation.disk.watermark.flood_stage": "95%",
            
            # Recovery settings
            "cluster.routing.allocation.node_concurrent_recoveries": 2,
            "indices.recovery.max_bytes_per_sec": "100mb",
            
            # Indexing settings
            "indices.memory.index_buffer_size": "10%",
            "thread_pool.write.queue_size": 1000
        }
    }
    
    es.cluster.put_settings(body=cluster_settings)
```

### 13. How do you handle cluster scaling and shard management?
**Answer**: 
Effective scaling requires proper shard sizing and distribution strategies.

**Shard Sizing Strategy:**
```python
def calculate_optimal_shards(data_size_gb, growth_rate, retention_days):
    """Calculate optimal shard configuration"""
    
    # Target shard size: 10-50GB per shard
    target_shard_size_gb = 30
    
    # Calculate total data size
    total_size_gb = data_size_gb * (1 + growth_rate) * (retention_days / 365)
    
    # Calculate number of shards
    num_shards = max(1, int(total_size_gb / target_shard_size_gb))
    
    # Ensure shards are distributed across nodes
    num_nodes = len(es.nodes.info()['nodes'])
    if num_shards < num_nodes:
        num_shards = num_nodes
    
    return {
        "recommended_shards": num_shards,
        "estimated_shard_size_gb": total_size_gb / num_shards,
        "total_estimated_size_gb": total_size_gb
    }

# Dynamic shard allocation
def rebalance_shards():
    """Rebalance shards across cluster"""
    
    # Enable shard allocation
    allocation_settings = {
        "transient": {
            "cluster.routing.allocation.enable": "all",
            "cluster.routing.rebalance.enable": "all"
        }
    }
    
    es.cluster.put_settings(body=allocation_settings)
    
    # Monitor rebalancing progress
    while True:
        health = es.cluster.health()
        if health['relocating_shards'] == 0:
            print("Rebalancing complete")
            break
        else:
            print(f"Relocating shards: {health['relocating_shards']}")
            time.sleep(30)

# Index shrinking for over-sharded indices
def shrink_index(source_index, target_index, target_shards=1):
    """Shrink an index to reduce shard count"""
    
    # Step 1: Move all shards to single node
    shrink_settings = {
        "settings": {
            "index.routing.allocation.require._name": "target_node_name",
            "index.blocks.write": True
        }
    }
    
    es.indices.put_settings(index=source_index, body=shrink_settings)
    
    # Step 2: Wait for relocation
    es.cluster.health(index=source_index, wait_for_no_relocating_shards=True)
    
    # Step 3: Shrink index
    shrink_body = {
        "settings": {
            "index.number_of_shards": target_shards,
            "index.number_of_replicas": 1,
            "index.codec": "best_compression"
        }
    }
    
    es.indices.shrink(
        index=source_index,
        target=target_index,
        body=shrink_body
    )
    
    # Step 4: Wait for shrink completion
    es.cluster.health(index=target_index, wait_for_status="green")
    
    print(f"Index {source_index} shrunk to {target_index}")
```

## Monitoring & Operations (76-90)

### 14. How do you monitor Elasticsearch performance and troubleshoot issues?
**Answer**: 
Comprehensive monitoring is essential for maintaining cluster health and performance.

**Performance Monitoring:**
```python
import time
from datetime import datetime

class ElasticsearchMonitor:
    def __init__(self, es_client):
        self.es = es_client
    
    def collect_metrics(self):
        """Collect comprehensive cluster metrics"""
        
        # Cluster health
        health = self.es.cluster.health()
        
        # Node stats
        node_stats = self.es.nodes.stats()
        
        # Index stats
        index_stats = self.es.indices.stats()
        
        # Cluster stats
        cluster_stats = self.es.cluster.stats()
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cluster': {
                'status': health['status'],
                'nodes': health['number_of_nodes'],
                'data_nodes': health['number_of_data_nodes'],
                'active_shards': health['active_shards'],
                'relocating_shards': health['relocating_shards'],
                'unassigned_shards': health['unassigned_shards']
            },
            'performance': {
                'search_query_total': cluster_stats['indices']['search']['query_total'],
                'search_query_time_in_millis': cluster_stats['indices']['search']['query_time_in_millis'],
                'indexing_index_total': cluster_stats['indices']['indexing']['index_total'],
                'indexing_index_time_in_millis': cluster_stats['indices']['indexing']['index_time_in_millis']
            },
            'storage': {
                'total_size_in_bytes': cluster_stats['indices']['store']['size_in_bytes'],
                'total_documents': cluster_stats['indices']['docs']['count']
            }
        }
        
        # Node-specific metrics
        metrics['nodes'] = {}
        for node_id, node_stat in node_stats['nodes'].items():
            node_name = node_stat['name']
            metrics['nodes'][node_name] = {
                'heap_used_percent': node_stat['jvm']['mem']['heap_used_percent'],
                'cpu_percent': node_stat['os']['cpu']['percent'],
                'load_average': node_stat['os']['cpu']['load_average'],
                'disk_usage': node_stat['fs']['total']['available_in_bytes'],
                'gc_time': node_stat['jvm']['gc']['collectors']['young']['collection_time_in_millis']
            }
        
        return metrics
    
    def check_alerts(self, metrics):
        """Check for alert conditions"""
        alerts = []
        
        # Cluster status alerts
        if metrics['cluster']['status'] != 'green':
            alerts.append(f"Cluster status is {metrics['cluster']['status']}")
        
        if metrics['cluster']['unassigned_shards'] > 0:
            alerts.append(f"Unassigned shards: {metrics['cluster']['unassigned_shards']}")
        
        # Node alerts
        for node_name, node_metrics in metrics['nodes'].items():
            if node_metrics['heap_used_percent'] > 85:
                alerts.append(f"High heap usage on {node_name}: {node_metrics['heap_used_percent']}%")
            
            if node_metrics['cpu_percent'] > 80:
                alerts.append(f"High CPU usage on {node_name}: {node_metrics['cpu_percent']}%")
        
        return alerts
    
    def analyze_slow_queries(self):
        """Analyze slow queries and performance bottlenecks"""
        
        # Get slow queries from logs (requires log parsing)
        # This is a simplified example
        slow_queries = []
        
        # Check for long-running searches
        tasks = self.es.tasks.list(actions="*search*", detailed=True)
        
        for task_id, task_info in tasks.get('nodes', {}).items():
            for task in task_info.get('tasks', {}).values():
                if task.get('running_time_in_nanos', 0) > 5000000000:  # 5 seconds
                    slow_queries.append({
                        'task_id': task['id'],
                        'action': task['action'],
                        'running_time_ms': task['running_time_in_nanos'] / 1000000,
                        'description': task.get('description', '')
                    })
        
        return slow_queries

# Usage
monitor = ElasticsearchMonitor(es)

def monitoring_loop():
    """Continuous monitoring loop"""
    while True:
        try:
            # Collect metrics
            metrics = monitor.collect_metrics()
            
            # Check for alerts
            alerts = monitor.check_alerts(metrics)
            
            # Log metrics and alerts
            print(f"Cluster Status: {metrics['cluster']['status']}")
            print(f"Active Shards: {metrics['cluster']['active_shards']}")
            
            if alerts:
                print("ALERTS:")
                for alert in alerts:
                    print(f"  - {alert}")
            
            # Check slow queries
            slow_queries = monitor.analyze_slow_queries()
            if slow_queries:
                print("SLOW QUERIES:")
                for query in slow_queries:
                    print(f"  - {query['action']}: {query['running_time_ms']:.2f}ms")
            
            time.sleep(60)  # Monitor every minute
            
        except Exception as e:
            print(f"Monitoring error: {e}")
            time.sleep(60)
```

## Integration & Architecture (91-100)

### 15. How do you integrate Elasticsearch with data pipelines and streaming systems?
**Answer**: 
Elasticsearch integrates well with various data pipeline architectures for real-time analytics.

**Logstash Integration:**
```python
# Logstash configuration for data pipeline
logstash_config = """
input {
  kafka {
    bootstrap_servers => "kafka1:9092,kafka2:9092"
    topics => ["user_events", "application_logs"]
    codec => "json"
  }
}

filter {
  if [type] == "user_event" {
    mutate {
      add_field => { "[@metadata][index]" => "user-events-%{+YYYY.MM.dd}" }
    }
    
    date {
      match => [ "timestamp", "ISO8601" ]
    }
    
    geoip {
      source => "ip_address"
      target => "geoip"
    }
  }
  
  if [type] == "application_log" {
    mutate {
      add_field => { "[@metadata][index]" => "app-logs-%{+YYYY.MM.dd}" }
    }
    
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:msg}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["es1:9200", "es2:9200", "es3:9200"]
    index => "%{[@metadata][index]}"
    template_name => "logstash"
    template_pattern => "logstash-*"
  }
}
"""

# Python equivalent using elasticsearch-py
from elasticsearch.helpers import streaming_bulk
import json

def kafka_to_elasticsearch_pipeline():
    """Stream data from Kafka to Elasticsearch"""
    
    from kafka import KafkaConsumer
    
    # Kafka consumer
    consumer = KafkaConsumer(
        'user_events', 'application_logs',
        bootstrap_servers=['kafka1:9092', 'kafka2:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    def generate_docs():
        """Generate documents for bulk indexing"""
        for message in consumer:
            event = message.value
            
            # Determine index based on event type
            if event.get('type') == 'user_event':
                index = f"user-events-{datetime.now().strftime('%Y.%m.%d')}"
            else:
                index = f"app-logs-{datetime.now().strftime('%Y.%m.%d')}"
            
            # Enrich event data
            if 'ip_address' in event:
                # Add geolocation (simplified)
                event['location'] = get_geolocation(event['ip_address'])
            
            yield {
                '_index': index,
                '_source': event
            }
    
    # Stream to Elasticsearch
    for success, info in streaming_bulk(es, generate_docs(), chunk_size=1000):
        if not success:
            print(f"Failed to index: {info}")

def get_geolocation(ip_address):
    """Get geolocation for IP address"""
    # Simplified geolocation lookup
    return {"country": "US", "city": "San Francisco"}
```

**Real-time Analytics Dashboard:**
```python
class RealTimeAnalytics:
    def __init__(self, es_client):
        self.es = es_client
    
    def create_real_time_dashboard(self):
        """Create real-time analytics queries"""
        
        # Real-time user activity
        user_activity_query = {
            "size": 0,
            "query": {
                "range": {
                    "timestamp": {
                        "gte": "now-5m"
                    }
                }
            },
            "aggs": {
                "activity_timeline": {
                    "date_histogram": {
                        "field": "timestamp",
                        "fixed_interval": "30s"
                    },
                    "aggs": {
                        "unique_users": {
                            "cardinality": {
                                "field": "user_id.keyword"
                            }
                        },
                        "event_types": {
                            "terms": {
                                "field": "event_type.keyword"
                            }
                        }
                    }
                },
                "top_pages": {
                    "terms": {
                        "field": "page_url.keyword",
                        "size": 10
                    }
                },
                "geographic_distribution": {
                    "terms": {
                        "field": "location.country.keyword"
                    }
                }
            }
        }
        
        response = self.es.search(index="user-events-*", body=user_activity_query)
        return self.format_dashboard_data(response)
    
    def format_dashboard_data(self, response):
        """Format Elasticsearch response for dashboard"""
        
        dashboard_data = {
            "timeline": [],
            "top_pages": [],
            "geographic_data": []
        }
        
        # Process timeline data
        for bucket in response['aggregations']['activity_timeline']['buckets']:
            dashboard_data['timeline'].append({
                'timestamp': bucket['key_as_string'],
                'unique_users': bucket['unique_users']['value'],
                'total_events': bucket['doc_count']
            })
        
        # Process top pages
        for bucket in response['aggregations']['top_pages']['buckets']:
            dashboard_data['top_pages'].append({
                'page': bucket['key'],
                'views': bucket['doc_count']
            })
        
        # Process geographic data
        for bucket in response['aggregations']['geographic_distribution']['buckets']:
            dashboard_data['geographic_data'].append({
                'country': bucket['key'],
                'users': bucket['doc_count']
            })
        
        return dashboard_data
    
    def setup_alerting(self):
        """Setup alerting for anomalies"""
        
        # Watcher query for anomaly detection
        watcher_query = {
            "trigger": {
                "schedule": {
                    "interval": "1m"
                }
            },
            "input": {
                "search": {
                    "request": {
                        "search_type": "query_then_fetch",
                        "indices": ["user-events-*"],
                        "body": {
                            "query": {
                                "range": {
                                    "timestamp": {
                                        "gte": "now-5m"
                                    }
                                }
                            },
                            "aggs": {
                                "error_rate": {
                                    "filter": {
                                        "term": {
                                            "event_type.keyword": "error"
                                        }
                                    }
                                },
                                "total_events": {
                                    "value_count": {
                                        "field": "event_type.keyword"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "condition": {
                "compare": {
                    "ctx.payload.aggregations.error_rate.doc_count": {
                        "gt": 100
                    }
                }
            },
            "actions": {
                "send_alert": {
                    "webhook": {
                        "scheme": "https",
                        "host": "hooks.slack.com",
                        "port": 443,
                        "method": "post",
                        "path": "/services/YOUR/SLACK/WEBHOOK",
                        "body": "High error rate detected: {{ctx.payload.aggregations.error_rate.doc_count}} errors in last 5 minutes"
                    }
                }
            }
        }
        
        # Note: This requires X-Pack/Elastic Stack license
        # es.watcher.put_watch(id="error_rate_alert", body=watcher_query)

# Usage
analytics = RealTimeAnalytics(es)
dashboard_data = analytics.create_real_time_dashboard()
```

---

## 🎯 **Summary**

This comprehensive guide covers Elasticsearch's essential concepts for data engineering interviews. Key areas include:

- **Distributed architecture** with sharding and replication
- **Advanced search capabilities** with Query DSL and aggregations
- **Performance optimization** through proper indexing and cluster management
- **Scalability patterns** with ILM and cluster scaling
- **Real-time analytics** and monitoring capabilities
- **Integration patterns** with data pipelines and streaming systems

**Interview Preparation Tips:**
1. **Master Query DSL** - Practice complex queries and aggregations
2. **Understand cluster architecture** - Know sharding, replication, and node roles
3. **Learn performance optimization** - Indexing strategies and query optimization
4. **Study operational aspects** - Monitoring, troubleshooting, and maintenance
5. **Know integration patterns** - How Elasticsearch fits in data architectures