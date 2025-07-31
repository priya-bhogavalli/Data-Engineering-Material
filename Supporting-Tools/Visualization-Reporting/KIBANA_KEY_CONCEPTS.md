# Kibana Key Concepts

## 1. Platform Overview
**What it is**: Data visualization and exploration tool for Elasticsearch, part of the Elastic Stack.

**Core Components**:
- **Discover**: Data exploration and search
- **Visualize**: Chart and graph creation
- **Dashboard**: Combine visualizations
- **Canvas**: Pixel-perfect presentations
- **Maps**: Geospatial data visualization

```bash
# Kibana configuration
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "password"
```

## 2. Index Patterns and Data Sources
**Index Patterns**: Define which Elasticsearch indices to analyze.

```json
// Create index pattern via API
PUT _kibana/api/saved_objects/index-pattern/sales-logs-*
{
  "attributes": {
    "title": "sales-logs-*",
    "timeFieldName": "@timestamp",
    "fields": "[{\"name\":\"@timestamp\",\"type\":\"date\",\"searchable\":true,\"aggregatable\":true}]"
  }
}
```

**Data View Configuration**:
```javascript
// Advanced index pattern with scripted fields
{
  "title": "ecommerce-*",
  "timeFieldName": "@timestamp",
  "fields": {
    "revenue_category": {
      "type": "string",
      "script": {
        "source": "if (doc['total_amount'].value > 1000) { return 'high' } else if (doc['total_amount'].value > 100) { return 'medium' } else { return 'low' }"
      }
    },
    "profit_margin": {
      "type": "number", 
      "script": {
        "source": "(doc['revenue'].value - doc['cost'].value) / doc['revenue'].value * 100"
      }
    }
  }
}
```

## 3. Discover - Data Exploration
**Search and Filter Data**:

```javascript
// KQL (Kibana Query Language) examples
// Basic field search
status: "error" AND response_time > 1000

// Wildcard search
message: "failed*" OR message: "*timeout*"

// Range queries
@timestamp >= "2024-01-01" AND @timestamp < "2024-02-01"
bytes: [1000 TO 5000]

// Boolean logic
(status: "error" OR status: "warning") AND NOT user_agent: "*bot*"

// Nested field queries
user.demographics.age >= 25 AND user.demographics.location: "US"

// Exists queries
_exists_: error_code AND NOT _exists_: resolved_at
```

**Saved Searches**:
```json
{
  "title": "High Value Transactions",
  "description": "Transactions over $1000 in the last 24 hours",
  "kibanaSavedObjectMeta": {
    "searchSourceJSON": {
      "query": {
        "bool": {
          "must": [
            {"range": {"amount": {"gte": 1000}}},
            {"range": {"@timestamp": {"gte": "now-24h"}}}
          ]
        }
      },
      "filter": [],
      "sort": [{"@timestamp": {"order": "desc"}}]
    }
  }
}
```

## 4. Visualizations
**Chart Types and Configuration**:

```json
// Line chart for time series
{
  "title": "Sales Over Time",
  "visState": {
    "type": "line",
    "params": {
      "grid": {"categoryLines": false, "style": {"color": "#eee"}},
      "categoryAxes": [{
        "id": "CategoryAxis-1",
        "type": "category",
        "position": "bottom",
        "show": true,
        "style": {},
        "scale": {"type": "linear"},
        "labels": {"show": true, "truncate": 100},
        "title": {}
      }],
      "valueAxes": [{
        "id": "ValueAxis-1",
        "name": "LeftAxis-1",
        "type": "value",
        "position": "left",
        "show": true,
        "style": {},
        "scale": {"type": "linear", "mode": "normal"},
        "labels": {"show": true, "rotate": 0, "filter": false, "truncate": 100},
        "title": {"text": "Sales Amount"}
      }]
    }
  },
  "aggs": [
    {
      "id": "1",
      "type": "sum",
      "schema": "metric",
      "params": {"field": "amount"}
    },
    {
      "id": "2", 
      "type": "date_histogram",
      "schema": "segment",
      "params": {
        "field": "@timestamp",
        "interval": "auto",
        "min_doc_count": 1
      }
    }
  ]
}
```

**Advanced Aggregations**:
```json
// Multi-metric visualization
{
  "aggs": [
    {
      "id": "1",
      "type": "avg",
      "schema": "metric", 
      "params": {"field": "response_time"}
    },
    {
      "id": "2",
      "type": "percentiles",
      "schema": "metric",
      "params": {
        "field": "response_time",
        "percents": [50, 95, 99]
      }
    },
    {
      "id": "3",
      "type": "cardinality",
      "schema": "metric",
      "params": {"field": "user_id"}
    },
    {
      "id": "4",
      "type": "terms",
      "schema": "segment",
      "params": {
        "field": "status_code",
        "size": 10,
        "order": "desc",
        "orderBy": "1"
      }
    }
  ]
}
```

## 5. Dashboards
**Dashboard Creation and Management**:

```json
// Dashboard configuration
{
  "title": "E-commerce Analytics Dashboard",
  "description": "Real-time analytics for e-commerce platform",
  "panelsJSON": [
    {
      "gridData": {"x": 0, "y": 0, "w": 24, "h": 15},
      "panelIndex": "1",
      "embeddableConfig": {},
      "panelRefName": "panel_1"
    },
    {
      "gridData": {"x": 24, "y": 0, "w": 24, "h": 15},
      "panelIndex": "2", 
      "embeddableConfig": {},
      "panelRefName": "panel_2"
    }
  ],
  "timeRestore": true,
  "timeTo": "now",
  "timeFrom": "now-24h",
  "refreshInterval": {
    "pause": false,
    "value": 30000
  }
}
```

**Dashboard Filters and Controls**:
```json
// Global filters
{
  "filters": [
    {
      "meta": {
        "alias": "Active Users Only",
        "disabled": false,
        "key": "status",
        "negate": false,
        "type": "phrase"
      },
      "query": {"match": {"status": "active"}}
    }
  ],
  "controls": [
    {
      "id": "region-filter",
      "type": "list",
      "source": {
        "indexPattern": "sales-*",
        "field": "region"
      },
      "options": {
        "multiselect": true,
        "size": 5
      }
    },
    {
      "id": "date-range",
      "type": "range",
      "source": {
        "indexPattern": "sales-*", 
        "field": "@timestamp"
      }
    }
  ]
}
```

## 6. Canvas - Pixel Perfect Reports
**Canvas Workpad Creation**:

```javascript
// Canvas expression language
// Data source
filters
| essql query="SELECT customer_type, AVG(order_value) as avg_value FROM sales GROUP BY customer_type"
| pointseries x="customer_type" y="avg_value"
| plot defaultStyle={seriesStyle bars=0.75}
| render

// Dynamic text with data
filters
| essql query="SELECT COUNT(*) as total_orders FROM sales WHERE @timestamp > now-24h"
| math "total_orders"
| formatnumber "0,0"
| markdown "## Total Orders Today: {{value}}"
| render

// Conditional formatting
filters  
| essql query="SELECT SUM(revenue) as daily_revenue FROM sales WHERE @timestamp > now-1d"
| math "daily_revenue > 10000 ? 'green' : 'red'"
| shape "square"
| render css=".canvasRenderEl {background-color: {{value}}}"
```

## 7. Maps - Geospatial Visualization
**Map Configuration**:

```json
{
  "title": "Sales by Region",
  "mapStateJSON": {
    "zoom": 4,
    "center": {"lat": 39.8283, "lon": -98.5795},
    "timeFilters": {
      "from": "now-7d",
      "to": "now"
    },
    "refreshConfig": {
      "isPaused": false,
      "interval": 60000
    },
    "query": {
      "query": "",
      "language": "kuery"
    }
  },
  "layerListJSON": [
    {
      "id": "sales-heatmap",
      "label": "Sales Heatmap",
      "sourceDescriptor": {
        "type": "ES_SEARCH",
        "indexPatternId": "sales-*",
        "geoField": "location",
        "requestType": "point",
        "filterByMapBounds": true
      },
      "style": {
        "type": "HEATMAP",
        "colorRampName": "Blues"
      }
    },
    {
      "id": "regional-boundaries",
      "label": "Regional Sales",
      "sourceDescriptor": {
        "type": "ES_GEO_GRID",
        "indexPatternId": "sales-*",
        "geoField": "location",
        "requestType": "grid",
        "resolution": "COARSE"
      },
      "style": {
        "type": "VECTOR",
        "properties": {
          "fillColor": {
            "type": "DYNAMIC",
            "options": {
              "field": {"name": "doc_count", "origin": "source"},
              "color": "Blues"
            }
          }
        }
      }
    }
  ]
}
```

## 8. Alerting and Monitoring
**Watcher Configuration** (X-Pack):

```json
{
  "trigger": {
    "schedule": {"interval": "5m"}
  },
  "input": {
    "search": {
      "request": {
        "search_type": "query_then_fetch",
        "indices": ["logs-*"],
        "body": {
          "query": {
            "bool": {
              "must": [
                {"range": {"@timestamp": {"gte": "now-5m"}}},
                {"term": {"level": "ERROR"}}
              ]
            }
          },
          "aggs": {
            "error_count": {
              "cardinality": {"field": "message.keyword"}
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {
      "ctx.payload.aggregations.error_count.value": {"gt": 10}
    }
  },
  "actions": {
    "send_email": {
      "email": {
        "to": ["ops-team@company.com"],
        "subject": "High Error Rate Alert",
        "body": "Error count: {{ctx.payload.aggregations.error_count.value}}"
      }
    },
    "slack_notification": {
      "webhook": {
        "scheme": "https",
        "host": "hooks.slack.com",
        "port": 443,
        "method": "post",
        "path": "/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
        "body": "{\"text\": \"🚨 High error rate detected: {{ctx.payload.aggregations.error_count.value}} errors in last 5 minutes\"}"
      }
    }
  }
}
```

## 9. Machine Learning Integration
**Anomaly Detection**:

```json
// ML job configuration
{
  "job_id": "sales-anomaly-detection",
  "description": "Detect anomalies in daily sales",
  "analysis_config": {
    "bucket_span": "1h",
    "detectors": [
      {
        "function": "sum",
        "field_name": "amount",
        "detector_description": "sum(amount)"
      },
      {
        "function": "distinct_count",
        "field_name": "customer_id",
        "detector_description": "distinct_count(customer_id)"
      }
    ],
    "influencers": ["region", "product_category"]
  },
  "data_description": {
    "time_field": "@timestamp",
    "time_format": "epoch_ms"
  },
  "datafeed_config": {
    "datafeed_id": "sales-anomaly-datafeed",
    "indices": ["sales-*"],
    "query": {
      "bool": {
        "must": [
          {"range": {"@timestamp": {"gte": "now-30d"}}}
        ]
      }
    }
  }
}
```

## 10. Advanced Features and Customization
**Custom Plugins and Extensions**:

```javascript
// Custom visualization plugin
import { PluginInitializerContext } from '../../../core/public';
import { CustomVisualizationPlugin } from './plugin';

export function plugin(initializerContext: PluginInitializerContext) {
  return new CustomVisualizationPlugin(initializerContext);
}

export {
  CustomVisualizationPluginSetup,
  CustomVisualizationPluginStart,
} from './plugin';

// Plugin implementation
export class CustomVisualizationPlugin implements Plugin<CustomVisualizationPluginSetup, CustomVisualizationPluginStart> {
  constructor(initializerContext: PluginInitializerContext) {}

  public setup(core: CoreSetup): CustomVisualizationPluginSetup {
    // Register custom visualization
    const visualizations = expressions.getService();
    
    visualizations.registerVisualization({
      name: 'custom_chart',
      title: 'Custom Chart',
      icon: 'visBarVertical',
      description: 'Custom visualization for specific use case',
      visConfig: {
        defaults: {
          // Default configuration
        }
      },
      editorConfig: {
        // Editor configuration
      },
      requestHandler: 'custom_request_handler',
      responseHandler: 'custom_response_handler'
    });

    return {};
  }

  public start(core: CoreStart): CustomVisualizationPluginStart {
    return {};
  }
}
```

**Scripted Fields and Runtime Fields**:
```javascript
// Runtime field in index pattern
{
  "runtime_mappings": {
    "customer_segment": {
      "type": "keyword",
      "script": {
        "source": """
          if (doc['total_purchases'].value > 10000) {
            emit('VIP');
          } else if (doc['total_purchases'].value > 1000) {
            emit('Premium');
          } else {
            emit('Standard');
          }
        """
      }
    },
    "days_since_last_order": {
      "type": "long",
      "script": {
        "source": """
          if (doc['last_order_date'].size() > 0) {
            emit(ChronoUnit.DAYS.between(
              Instant.ofEpochMilli(doc['last_order_date'].value.millis),
              Instant.now()
            ));
          }
        """
      }
    }
  }
}
```

**Advanced Dashboard Drilldowns**:
```json
{
  "drilldowns": [
    {
      "id": "dashboard-to-dashboard",
      "actionConfig": {
        "dashboardId": "detailed-sales-dashboard",
        "useCurrentFilters": true,
        "useCurrentDateRange": true
      },
      "triggers": ["VALUE_CLICK_TRIGGER"]
    },
    {
      "id": "dashboard-to-url",
      "actionConfig": {
        "url": "https://crm.company.com/customer/{{event.key}}",
        "openInNewTab": true
      },
      "triggers": ["VALUE_CLICK_TRIGGER"]
    }
  ]
}
```