# Elasticsearch Key Concepts

## 🎯 What is Elasticsearch?
Distributed search and analytics engine built on Apache Lucene for full-text search, structured search, and analytics.

## 🏗️ Core Architecture

### Key Components
- **Cluster** - Collection of nodes
- **Node** - Single server instance
- **Index** - Collection of documents (like database)
- **Document** - JSON object (like row)
- **Field** - Key-value pair (like column)
- **Shard** - Subset of index data
- **Replica** - Copy of shard for redundancy

### Document Structure
```json
{
  "_index": "products",
  "_id": "1",
  "_source": {
    "name": "Laptop",
    "category": "Electronics",
    "price": 999.99,
    "description": "High-performance laptop",
    "tags": ["computer", "portable"],
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

## 🔧 Basic Operations

### Index Management
```bash
# Create index
PUT /products
{
  "mappings": {
    "properties": {
      "name": {"type": "text"},
      "price": {"type": "float"},
      "created_at": {"type": "date"}
    }
  }
}

# Delete index
DELETE /products
```

### Document Operations
```bash
# Index document
POST /products/_doc/1
{
  "name": "Laptop",
  "price": 999.99,
  "category": "Electronics"
}

# Get document
GET /products/_doc/1

# Update document
POST /products/_update/1
{
  "doc": {
    "price": 899.99
  }
}

# Delete document
DELETE /products/_doc/1
```

## 🔍 Search Capabilities

### Basic Search
```bash
# Match all
GET /products/_search
{
  "query": {
    "match_all": {}
  }
}

# Term search
GET /products/_search
{
  "query": {
    "term": {
      "category": "Electronics"
    }
  }
}

# Full-text search
GET /products/_search
{
  "query": {
    "match": {
      "description": "high performance"
    }
  }
}
```

### Complex Queries
```bash
# Bool query
GET /products/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"category": "Electronics"}}
      ],
      "filter": [
        {"range": {"price": {"gte": 100, "lte": 1000}}}
      ],
      "must_not": [
        {"term": {"discontinued": true}}
      ]
    }
  }
}
```

## 📊 Aggregations

### Metric Aggregations
```bash
# Average price
GET /products/_search
{
  "aggs": {
    "avg_price": {
      "avg": {
        "field": "price"
      }
    }
  }
}

# Statistics
GET /products/_search
{
  "aggs": {
    "price_stats": {
      "stats": {
        "field": "price"
      }
    }
  }
}
```

### Bucket Aggregations
```bash
# Group by category
GET /products/_search
{
  "aggs": {
    "categories": {
      "terms": {
        "field": "category.keyword"
      }
    }
  }
}

# Date histogram
GET /logs/_search
{
  "aggs": {
    "sales_over_time": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "day"
      }
    }
  }
}
```

## 🚀 Advanced Features

### Mapping & Analysis
```bash
# Custom analyzer
PUT /products
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "tokenizer": "standard",
          "filter": ["lowercase", "stop"]
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

### Index Templates
```bash
# Create template
PUT /_index_template/logs_template
{
  "index_patterns": ["logs-*"],
  "template": {
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

## 🔧 Python Integration

### Basic Operations
```python
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Index document
doc = {
    'name': 'Laptop',
    'price': 999.99,
    'category': 'Electronics'
}
es.index(index='products', id=1, body=doc)

# Search
response = es.search(
    index='products',
    body={
        'query': {
            'match': {
                'name': 'laptop'
            }
        }
    }
)
```

### Bulk Operations
```python
from elasticsearch.helpers import bulk

def generate_docs():
    for i in range(1000):
        yield {
            '_index': 'products',
            '_id': i,
            '_source': {
                'name': f'Product {i}',
                'price': i * 10,
                'category': 'Electronics'
            }
        }

# Bulk index
bulk(es, generate_docs())
```

## 🎯 Use Cases & Patterns

### Log Analysis
```python
# Log ingestion
def ingest_logs(logs):
    actions = []
    for log in logs:
        actions.append({
            '_index': f'logs-{log["date"]}',
            '_source': {
                'timestamp': log['timestamp'],
                'level': log['level'],
                'message': log['message'],
                'service': log['service']
            }
        })
    bulk(es, actions)
```

### E-commerce Search
```python
# Product search with filters
def search_products(query, category=None, price_range=None):
    body = {
        'query': {
            'bool': {
                'must': [
                    {'multi_match': {
                        'query': query,
                        'fields': ['name^2', 'description']
                    }}
                ]
            }
        }
    }
    
    if category:
        body['query']['bool']['filter'] = [
            {'term': {'category': category}}
        ]
    
    if price_range:
        body['query']['bool']['filter'].append({
            'range': {'price': price_range}
        })
    
    return es.search(index='products', body=body)
```

## 🔒 Best Practices

### Performance
- Use appropriate shard sizes (20-40GB)
- Implement proper mapping strategies
- Use bulk operations for indexing
- Monitor cluster health regularly

### Security
- Enable authentication and authorization
- Use TLS for data in transit
- Implement field-level security
- Regular security updates

### Operations
- Regular backups and snapshots
- Monitor disk usage and performance
- Implement proper logging
- Use index lifecycle management

## 🎯 Common Use Cases
- Full-text search applications
- Log and event data analysis
- Real-time application monitoring
- E-commerce product search
- Business intelligence and analytics
- Security information and event management (SIEM)

## ⚠️ Considerations
- Memory-intensive operations
- Complex cluster management
- Query performance tuning required
- Storage requirements for replicas