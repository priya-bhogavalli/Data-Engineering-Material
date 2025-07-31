# Elasticsearch Key Concepts

## 1. Elasticsearch Architecture
**Core Components**:
- **Cluster**: Collection of nodes
- **Node**: Single server instance
- **Index**: Collection of documents (like database)
- **Document**: JSON record (like table row)
- **Shard**: Horizontal partition of index
- **Replica**: Copy of shard for redundancy

```json
// Cluster health
GET /_cluster/health

// Node information
GET /_nodes

// Index information
GET /_cat/indices?v
```

## 2. Index Management
```json
// Create index with mapping
PUT /sales_data
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stop"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "customer_id": {"type": "keyword"},
      "product_name": {
        "type": "text",
        "analyzer": "custom_analyzer"
      },
      "amount": {"type": "double"},
      "order_date": {"type": "date"},
      "location": {"type": "geo_point"},
      "tags": {"type": "keyword"},
      "description": {
        "type": "text",
        "fields": {
          "keyword": {"type": "keyword"}
        }
      }
    }
  }
}

// Update mapping
PUT /sales_data/_mapping
{
  "properties": {
    "category": {"type": "keyword"}
  }
}

// Index templates
PUT /_index_template/logs_template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    },
    "mappings": {
      "properties": {
        "timestamp": {"type": "date"},
        "level": {"type": "keyword"},
        "message": {"type": "text"}
      }
    }
  }
}
```

## 3. Document Operations
```json
// Index document
POST /sales_data/_doc
{
  "customer_id": "CUST001",
  "product_name": "Laptop",
  "amount": 1299.99,
  "order_date": "2024-01-15T10:30:00",
  "location": {"lat": 40.7128, "lon": -74.0060},
  "tags": ["electronics", "computers"],
  "description": "High-performance laptop for data analysis"
}

// Index with specific ID
PUT /sales_data/_doc/12345
{
  "customer_id": "CUST002",
  "product_name": "Tablet",
  "amount": 599.99,
  "order_date": "2024-01-15T11:00:00"
}

// Bulk operations
POST /_bulk
{"index": {"_index": "sales_data"}}
{"customer_id": "CUST003", "product_name": "Phone", "amount": 899.99}
{"index": {"_index": "sales_data"}}
{"customer_id": "CUST004", "product_name": "Watch", "amount": 299.99}
{"update": {"_index": "sales_data", "_id": "12345"}}
{"doc": {"category": "electronics"}}
{"delete": {"_index": "sales_data", "_id": "old_doc"}}

// Update document
POST /sales_data/_update/12345
{
  "doc": {
    "amount": 649.99,
    "updated_at": "2024-01-15T12:00:00"
  }
}

// Upsert
POST /sales_data/_update/new_doc
{
  "doc": {
    "customer_id": "CUST005",
    "amount": 199.99
  },
  "upsert": {
    "customer_id": "CUST005",
    "product_name": "Accessory",
    "amount": 199.99,
    "order_date": "2024-01-15T13:00:00"
  }
}
```

## 4. Search Queries
```json
// Match all
GET /sales_data/_search
{
  "query": {
    "match_all": {}
  }
}

// Term query (exact match)
GET /sales_data/_search
{
  "query": {
    "term": {
      "customer_id": "CUST001"
    }
  }
}

// Match query (analyzed)
GET /sales_data/_search
{
  "query": {
    "match": {
      "product_name": "laptop computer"
    }
  }
}

// Multi-match query
GET /sales_data/_search
{
  "query": {
    "multi_match": {
      "query": "electronics",
      "fields": ["product_name", "description", "tags"]
    }
  }
}

// Range query
GET /sales_data/_search
{
  "query": {
    "range": {
      "amount": {
        "gte": 500,
        "lte": 2000
      }
    }
  }
}

// Bool query (compound)
GET /sales_data/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"product_name": "laptop"}},
        {"range": {"amount": {"gte": 1000}}}
      ],
      "filter": [
        {"term": {"tags": "electronics"}}
      ],
      "must_not": [
        {"term": {"customer_id": "CUST999"}}
      ],
      "should": [
        {"match": {"description": "high-performance"}}
      ]
    }
  }
}
```

## 5. Aggregations
```json
// Terms aggregation
GET /sales_data/_search
{
  "size": 0,
  "aggs": {
    "products": {
      "terms": {
        "field": "product_name.keyword",
        "size": 10
      }
    }
  }
}

// Date histogram
GET /sales_data/_search
{
  "size": 0,
  "aggs": {
    "sales_over_time": {
      "date_histogram": {
        "field": "order_date",
        "calendar_interval": "day"
      },
      "aggs": {
        "total_sales": {
          "sum": {"field": "amount"}
        }
      }
    }
  }
}

// Nested aggregations
GET /sales_data/_search
{
  "size": 0,
  "aggs": {
    "customers": {
      "terms": {"field": "customer_id"},
      "aggs": {
        "total_spent": {
          "sum": {"field": "amount"}
        },
        "avg_order": {
          "avg": {"field": "amount"}
        },
        "order_count": {
          "value_count": {"field": "amount"}
        }
      }
    }
  }
}

// Pipeline aggregations
GET /sales_data/_search
{
  "size": 0,
  "aggs": {
    "monthly_sales": {
      "date_histogram": {
        "field": "order_date",
        "calendar_interval": "month"
      },
      "aggs": {
        "total_sales": {"sum": {"field": "amount"}}
      }
    },
    "sales_growth": {
      "derivative": {
        "buckets_path": "monthly_sales>total_sales"
      }
    }
  }
}

// Geo aggregations
GET /sales_data/_search
{
  "size": 0,
  "aggs": {
    "sales_by_region": {
      "geo_distance": {
        "field": "location",
        "origin": {"lat": 40.7128, "lon": -74.0060},
        "ranges": [
          {"to": 100000},
          {"from": 100000, "to": 300000},
          {"from": 300000}
        ]
      }
    }
  }
}
```

## 6. Full-Text Search
```json
// Fuzzy search
GET /sales_data/_search
{
  "query": {
    "fuzzy": {
      "product_name": {
        "value": "labtop",
        "fuzziness": "AUTO"
      }
    }
  }
}

// Wildcard search
GET /sales_data/_search
{
  "query": {
    "wildcard": {
      "product_name.keyword": "*phone*"
    }
  }
}

// Phrase matching
GET /sales_data/_search
{
  "query": {
    "match_phrase": {
      "description": "high performance laptop"
    }
  }
}

// Highlighting
GET /sales_data/_search
{
  "query": {
    "match": {"description": "laptop"}
  },
  "highlight": {
    "fields": {
      "description": {}
    }
  }
}

// Search suggestions
GET /sales_data/_search
{
  "suggest": {
    "product_suggest": {
      "prefix": "lap",
      "completion": {
        "field": "product_name.suggest"
      }
    }
  }
}
```

## 7. Index Lifecycle Management
```json
// ILM Policy
PUT /_ilm/policy/logs_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "5GB",
            "max_age": "7d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
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
          "allocate": {
            "number_of_replicas": 0
          }
        }
      },
      "delete": {
        "min_age": "90d"
      }
    }
  }
}

// Apply ILM policy to index template
PUT /_index_template/logs_template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "index.lifecycle.name": "logs_policy",
      "index.lifecycle.rollover_alias": "logs"
    }
  }
}

// Reindex for schema changes
POST /_reindex
{
  "source": {
    "index": "old_sales_data"
  },
  "dest": {
    "index": "new_sales_data"
  },
  "script": {
    "source": "ctx._source.new_field = ctx._source.old_field * 2"
  }
}
```

## 8. Performance Optimization
```json
// Index settings for performance
PUT /high_performance_index
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "refresh_interval": "30s",
    "index.codec": "best_compression",
    "index.merge.policy.max_merged_segment": "2gb"
  }
}

// Bulk indexing optimization
PUT /bulk_index/_settings
{
  "refresh_interval": -1,
  "number_of_replicas": 0
}

// After bulk loading
PUT /bulk_index/_settings
{
  "refresh_interval": "1s",
  "number_of_replicas": 1
}

// Force merge after bulk loading
POST /bulk_index/_forcemerge?max_num_segments=1

// Search optimization
GET /sales_data/_search
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"customer_id": "CUST001"}},
        {"range": {"order_date": {"gte": "2024-01-01"}}}
      ]
    }
  },
  "_source": ["customer_id", "amount", "order_date"],
  "size": 100,
  "sort": [{"order_date": {"order": "desc"}}]
}
```

## 9. Monitoring and Maintenance
```json
// Cluster stats
GET /_cluster/stats

// Node stats
GET /_nodes/stats

// Index stats
GET /sales_data/_stats

// Shard allocation
GET /_cat/shards?v

// Hot threads
GET /_nodes/hot_threads

// Pending tasks
GET /_cluster/pending_tasks

// Health check
GET /_cluster/health?level=indices

// Explain allocation
GET /_cluster/allocation/explain
{
  "index": "sales_data",
  "shard": 0,
  "primary": true
}
```

## 10. Security and Access Control
```json
// Create role
POST /_security/role/sales_analyst
{
  "cluster": ["monitor"],
  "indices": [
    {
      "names": ["sales_*"],
      "privileges": ["read", "view_index_metadata"],
      "field_security": {
        "grant": ["customer_id", "product_name", "amount", "order_date"]
      },
      "query": {
        "term": {"department": "sales"}
      }
    }
  ]
}

// Create user
POST /_security/user/analyst_user
{
  "password": "secure_password",
  "roles": ["sales_analyst"],
  "full_name": "Sales Analyst",
  "email": "analyst@company.com"
}

// API key authentication
POST /_security/api_key
{
  "name": "data_pipeline_key",
  "role_descriptors": {
    "pipeline_role": {
      "cluster": ["monitor"],
      "indices": [
        {
          "names": ["logs-*", "metrics-*"],
          "privileges": ["create_index", "write", "read"]
        }
      ]
    }
  },
  "expiration": "1d"
}

// SSL/TLS configuration
# elasticsearch.yml
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
```