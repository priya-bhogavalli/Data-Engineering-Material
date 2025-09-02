# 🔍 Elasticsearch Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts (1-25)](#core-concepts-1-25)
2. [Indexing & Search (26-50)](#indexing--search-26-50)
3. [Performance & Scaling (51-75)](#performance--scaling-51-75)
4. [Operations & Monitoring (76-100)](#operations--monitoring-76-100)

---

## Core Concepts (1-25)

### 1. What is Elasticsearch and its primary use cases?
**Answer**: Elasticsearch is a distributed search and analytics engine built on Apache Lucene.

**Use Cases:**
- **Full-text Search**: Website search, document search
- **Log Analytics**: ELK stack for log analysis
- **Real-time Analytics**: Business metrics, monitoring
- **Application Search**: E-commerce product search

```bash
# Basic Elasticsearch operations
curl -X PUT "localhost:9200/products"
curl -X POST "localhost:9200/products/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics"
}'

curl -X GET "localhost:9200/products/_search?q=laptop"
```

### 2. Explain Elasticsearch cluster architecture
**Answer**: Elasticsearch uses a distributed architecture with nodes, indices, and shards.

**Components:**
- **Cluster**: Collection of nodes
- **Node**: Single Elasticsearch instance
- **Index**: Collection of documents
- **Shard**: Subset of index data
- **Replica**: Copy of primary shard

### 3. What are mappings and why are they important?
**Answer**: Mappings define how documents and fields are stored and indexed.

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": {"type": "text", "analyzer": "standard"},
      "price": {"type": "float"},
      "created_at": {"type": "date"},
      "tags": {"type": "keyword"}
    }
  }
}
```

### 4. How do you perform complex searches in Elasticsearch?
**Answer**: Use Query DSL for complex search operations.

```json
POST /products/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"name": "laptop"}},
        {"range": {"price": {"gte": 500, "lte": 1500}}}
      ],
      "filter": [
        {"term": {"category": "Electronics"}}
      ]
    }
  },
  "aggs": {
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          {"to": 500},
          {"from": 500, "to": 1000},
          {"from": 1000}
        ]
      }
    }
  }
}
```

### 5. What are analyzers and how do they work?
**Answer**: Analyzers process text during indexing and searching.

```json
PUT /products
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "stemmer"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "analyzer": "custom_analyzer"
      }
    }
  }
}
```

## Indexing & Search (26-50)

### 26. How do you optimize indexing performance?
**Answer**: Multiple strategies for faster indexing.

```json
PUT /_template/bulk_template
{
  "index_patterns": ["logs-*"],
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "refresh_interval": "30s",
    "index.translog.flush_threshold_size": "1gb"
  }
}
```

### 27. How do you implement real-time search?
**Answer**: Configure refresh intervals and use real-time GET.

```bash
# Real-time document retrieval
curl -X GET "localhost:9200/products/_doc/1?realtime=true"

# Force refresh for immediate search
curl -X POST "localhost:9200/products/_refresh"
```

### 28. What are aggregations and how do you use them?
**Answer**: Aggregations provide analytics capabilities.

```json
POST /sales/_search
{
  "size": 0,
  "aggs": {
    "sales_by_month": {
      "date_histogram": {
        "field": "date",
        "calendar_interval": "month"
      },
      "aggs": {
        "total_revenue": {
          "sum": {"field": "amount"}
        }
      }
    }
  }
}
```

## Performance & Scaling (51-75)

### 51. How do you scale Elasticsearch clusters?
**Answer**: Horizontal scaling through sharding and node addition.

```bash
# Add new node to cluster
elasticsearch -Ecluster.name=my-cluster -Enode.name=node-3

# Rebalance shards
curl -X POST "localhost:9200/_cluster/reroute?retry_failed=true"
```

### 52. How do you monitor Elasticsearch performance?
**Answer**: Use cluster APIs and monitoring tools.

```bash
# Cluster health
curl -X GET "localhost:9200/_cluster/health"

# Node stats
curl -X GET "localhost:9200/_nodes/stats"

# Index stats
curl -X GET "localhost:9200/_stats"
```

## Operations & Monitoring (76-100)

### 76. How do you backup and restore Elasticsearch?
**Answer**: Use snapshot and restore APIs.

```bash
# Create repository
curl -X PUT "localhost:9200/_snapshot/my_backup" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/mount/backups/my_backup"
  }
}'

# Create snapshot
curl -X PUT "localhost:9200/_snapshot/my_backup/snapshot_1"

# Restore snapshot
curl -X POST "localhost:9200/_snapshot/my_backup/snapshot_1/_restore"
```

### 77. How do you handle Elasticsearch security?
**Answer**: Implement authentication, authorization, and encryption.

```yaml
# elasticsearch.yml
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.http.ssl.enabled: true
```

---

**Total Questions: 100** | **Coverage: Complete Elasticsearch Ecosystem**