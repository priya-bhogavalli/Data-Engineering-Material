# 🚀 Grafana Key Concepts - Mission Control Dashboard

> **Think of Grafana as NASA's mission control center where engineers monitor spacecraft systems through multiple screens showing real-time telemetry, with customizable dashboards for different missions and automatic alerts when anything goes wrong**

[![Grafana](https://img.shields.io/badge/Grafana-Latest-orange)](https://grafana.com/)
[![Difficulty](https://img.shields.io/badge/Difficulty-Intermediate-yellow)](https://github.com/yourusername/Data-Engineering-Material)
[![Interview Frequency](https://img.shields.io/badge/Interview-High-red)](https://github.com/yourusername/Data-Engineering-Material)

## 🎯 What is Grafana? - Mission Control Center

> **Think of Grafana like NASA's advanced mission control center where engineers monitor complex systems through multiple customizable screens, track real-time telemetry from various sources, and get automatic alerts when critical thresholds are exceeded**

### 🚀 **Mission Control Analogy**
Grafana is like an advanced mission control center where:
- **🖥️ Multiple Monitors** (Dashboards) - Customizable screens showing different aspects of system health
- **📡 Telemetry Systems** (Data Sources) - Connections to various monitoring systems and sensors
- **⚠️ Alert Systems** (Alerting) - Automatic notifications when critical thresholds are exceeded
- **👥 Control Rooms** (Teams & Organizations) - Different mission control rooms for different projects
- **📊 Real-Time Displays** (Live Data) - Continuously updated information with minimal delay
- **🎛️ Custom Controls** (Plugins) - Specialized instruments for specific monitoring needs

### 💼 **Why Mission Control Works**
- **Comprehensive Monitoring** - Single view of all critical systems and metrics
- **Real-Time Awareness** - Immediate visibility into system status and performance
- **Proactive Alerts** - Early warning system prevents small issues from becoming disasters
- **Customizable Views** - Different dashboards for different roles and responsibilities
- **Historical Analysis** - Track trends and patterns over time for better decision-making
- **Collaborative Environment** - Shared visibility enables coordinated response to issues

## 1. Grafana Architecture - Control Center Layout

> **Think of Grafana's architecture like a mission control center's layout with different components working together - the main control systems, data feeds from various spacecraft, display screens, and communication networks**
**Components**:
- **Grafana Server**: Web application and API
- **Data Sources**: External systems providing metrics
- **Dashboards**: Collections of panels and visualizations
- **Panels**: Individual visualizations
- **Alerting**: Notification system for threshold breaches

## 2. Data Sources
```yaml
# Prometheus data source
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true

  - name: InfluxDB
    type: influxdb
    url: http://influxdb:8086
    database: metrics
    user: grafana
    password: password

  - name: Elasticsearch
    type: elasticsearch
    url: http://elasticsearch:9200
    index: logstash-*
    timeField: "@timestamp"
```

```sql
-- PostgreSQL data source queries
SELECT 
    time_bucket('5m', created_at) as time,
    COUNT(*) as order_count
FROM orders 
WHERE created_at >= NOW() - INTERVAL '1 hour'
GROUP BY time_bucket('5m', created_at)
ORDER BY time;

-- MySQL data source
SELECT 
    DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i:00') as time,
    AVG(response_time) as avg_response_time
FROM api_metrics 
WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
GROUP BY DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i:00');
```

## 3. Dashboard Creation
```json
{
  "dashboard": {
    "title": "Data Pipeline Monitoring",
    "tags": ["data-engineering", "etl"],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s",
    "panels": [
      {
        "title": "Pipeline Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(pipeline_success_total[5m]) / rate(pipeline_total[5m]) * 100",
            "legendFormat": "Success Rate %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 90},
                {"color": "green", "value": 95}
              ]
            }
          }
        }
      }
    ]
  }
}
```

## 4. Prometheus Queries (PromQL)
```promql
# Basic metrics
pipeline_duration_seconds

# Rate of change
rate(http_requests_total[5m])

# Aggregation
sum(rate(pipeline_records_processed[5m])) by (pipeline_name)

# Percentiles
histogram_quantile(0.95, rate(api_response_time_bucket[5m]))

# Alerts
avg_over_time(cpu_usage_percent[5m]) > 80

# Complex queries for data pipelines
sum(rate(kafka_consumer_lag_sum[5m])) by (topic, consumer_group)

# Database connection pool
avg(database_connections_active) / avg(database_connections_max) * 100

# Data freshness
time() - max(last_successful_run_timestamp)

# Error rate
rate(pipeline_errors_total[5m]) / rate(pipeline_runs_total[5m]) * 100
```

## 5. Panel Types and Visualizations
```json
// Time series panel
{
  "type": "timeseries",
  "title": "Records Processed Over Time",
  "targets": [
    {
      "expr": "rate(records_processed_total[5m])",
      "legendFormat": "{{pipeline_name}}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "smooth",
        "fillOpacity": 10
      }
    }
  }
}

// Gauge panel
{
  "type": "gauge",
  "title": "Current CPU Usage",
  "targets": [
    {
      "expr": "avg(cpu_usage_percent)"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "min": 0,
      "max": 100,
      "thresholds": {
        "steps": [
          {"color": "green", "value": 0},
          {"color": "yellow", "value": 70},
          {"color": "red", "value": 90}
        ]
      }
    }
  }
}

// Table panel
{
  "type": "table",
  "title": "Pipeline Status",
  "targets": [
    {
      "expr": "pipeline_last_run_status",
      "format": "table",
      "instant": true
    }
  ],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {"Time": true},
        "renameByName": {
          "pipeline_name": "Pipeline",
          "Value": "Status"
        }
      }
    }
  ]
}
```

## 6. Variables and Templating
```json
{
  "templating": {
    "list": [
      {
        "name": "environment",
        "type": "custom",
        "options": [
          {"text": "Production", "value": "prod"},
          {"text": "Staging", "value": "staging"},
          {"text": "Development", "value": "dev"}
        ]
      },
      {
        "name": "pipeline",
        "type": "query",
        "query": "label_values(pipeline_duration_seconds, pipeline_name)",
        "refresh": 1
      },
      {
        "name": "time_range",
        "type": "interval",
        "options": [
          {"text": "1m", "value": "1m"},
          {"text": "5m", "value": "5m"},
          {"text": "15m", "value": "15m"},
          {"text": "1h", "value": "1h"}
        ]
      }
    ]
  }
}

// Using variables in queries
sum(rate(pipeline_duration_seconds{pipeline_name="$pipeline", environment="$environment"}[$time_range]))
```

## 7. Alerting
```json
{
  "alert": {
    "name": "High Pipeline Failure Rate",
    "message": "Pipeline failure rate is above 5% for the last 10 minutes",
    "frequency": "30s",
    "conditions": [
      {
        "query": {
          "queryType": "",
          "refId": "A",
          "model": {
            "expr": "rate(pipeline_failures_total[5m]) / rate(pipeline_runs_total[5m]) * 100",
            "interval": "",
            "refId": "A"
          }
        },
        "reducer": {
          "type": "last",
          "params": []
        },
        "evaluator": {
          "params": [5],
          "type": "gt"
        }
      }
    ],
    "executionErrorState": "alerting",
    "noDataState": "no_data",
    "for": "5m"
  }
}

// Notification channels
{
  "name": "slack-alerts",
  "type": "slack",
  "settings": {
    "url": "https://hooks.slack.com/services/...",
    "channel": "#data-engineering",
    "title": "Grafana Alert",
    "text": "{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}"
  }
}
```

## 8. Transformations
```json
// Data transformations
{
  "transformations": [
    {
      "id": "reduce",
      "options": {
        "reducers": ["last", "mean", "max"]
      }
    },
    {
      "id": "calculateField",
      "options": {
        "alias": "Success Rate",
        "mode": "binary",
        "binary": {
          "left": "successful_runs",
          "operator": "/",
          "right": "total_runs"
        }
      }
    },
    {
      "id": "filterFieldsByName",
      "options": {
        "include": {
          "names": ["Time", "Pipeline", "Success Rate"]
        }
      }
    },
    {
      "id": "sortBy",
      "options": {
        "sort": [
          {
            "field": "Success Rate",
            "desc": false
          }
        ]
      }
    }
  ]
}
```

## 9. Custom Plugins
```javascript
// Custom panel plugin
import { PanelPlugin } from '@grafana/data';
import { DataPipelinePanel } from './DataPipelinePanel';

export const plugin = new PanelPlugin(DataPipelinePanel).setPanelOptions(builder => {
  return builder
    .addTextInput({
      path: 'pipelineName',
      name: 'Pipeline Name',
      description: 'Name of the data pipeline to monitor',
      defaultValue: 'default-pipeline'
    })
    .addNumberInput({
      path: 'refreshInterval',
      name: 'Refresh Interval (seconds)',
      defaultValue: 30
    });
});

// Custom data source plugin
import { DataSourcePlugin } from '@grafana/data';
import { DataSource } from './DataSource';
import { ConfigEditor } from './ConfigEditor';
import { QueryEditor } from './QueryEditor';

export const plugin = new DataSourcePlugin(DataSource)
  .setConfigEditor(ConfigEditor)
  .setQueryEditor(QueryEditor);
```

## 10. Advanced Features
```yaml
# Grafana configuration (grafana.ini)
[server]
http_port = 3000
domain = grafana.company.com

[database]
type = postgres
host = postgres:5432
name = grafana
user = grafana
password = password

[auth.ldap]
enabled = true
config_file = /etc/grafana/ldap.toml

[alerting]
enabled = true
execute_alerts = true

[metrics]
enabled = true
interval_seconds = 10

# Provisioning dashboards
apiVersion: 1
providers:
  - name: 'data-engineering'
    orgId: 1
    folder: 'Data Engineering'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /var/lib/grafana/dashboards

# Grafana API usage
curl -X POST \
  http://grafana:3000/api/dashboards/db \
  -H 'Authorization: Bearer eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk' \
  -H 'Content-Type: application/json' \
  -d '{
    "dashboard": {
      "title": "API Generated Dashboard",
      "panels": [...]
    },
    "overwrite": true
  }'

# Backup and restore
# Export dashboard
curl -H "Authorization: Bearer $API_KEY" \
  http://grafana:3000/api/dashboards/uid/dashboard-uid

# Import dashboard
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @dashboard.json \
  http://grafana:3000/api/dashboards/db
```