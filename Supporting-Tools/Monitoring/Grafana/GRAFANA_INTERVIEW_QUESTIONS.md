# Grafana Interview Questions

## Table of Contents

1. [Basic Grafana Questions](#basic-grafana-questions)
2. [Data Sources & Queries](#data-sources--queries)
3. [Dashboard Development](#dashboard-development)
4. [Visualization & Panels](#visualization--panels)
5. [Alerting & Notifications](#alerting--notifications)
6. [Administration & Security](#administration--security)
7. [Performance & Scaling](#performance--scaling)
8. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Grafana Questions

### 1. What is Grafana and what are its primary use cases?
**Answer:**
Grafana is an open-source analytics and monitoring platform for visualizing time-series data.

**Primary Use Cases:**
- **Infrastructure Monitoring**: Server, network, and application metrics
- **Application Performance Monitoring**: APM and observability
- **Business Analytics**: KPIs and business metrics dashboards
- **IoT Monitoring**: Sensor data visualization
- **Log Analysis**: Log aggregation and analysis
- **DevOps Dashboards**: CI/CD pipeline monitoring

### 2. What are the key features of Grafana?
**Answer:**
- **Multi-Data Source Support**: Connect to various databases and services
- **Rich Visualizations**: Multiple chart types and panel options
- **Dashboard Sharing**: Share dashboards across teams and organizations
- **Alerting**: Built-in alerting with multiple notification channels
- **Templating**: Dynamic dashboards with variables
- **Annotations**: Add context to graphs with events and deployments
- **Plugin Ecosystem**: Extensive plugin library for data sources and panels

### 3. How does Grafana differ from other monitoring tools?
**Answer:**
**vs. Kibana:**
- Grafana: Multi-data source, time-series focused
- Kibana: Elasticsearch-specific, log analysis focused

**vs. Tableau:**
- Grafana: Real-time monitoring, open-source
- Tableau: Business intelligence, commercial

**vs. Prometheus:**
- Grafana: Visualization layer
- Prometheus: Data collection and storage

### 4. What are the main components of Grafana architecture?
**Answer:**
- **Grafana Server**: Core application server
- **Database**: Stores dashboards, users, and configuration (SQLite, MySQL, PostgreSQL)
- **Data Sources**: External systems providing data
- **Plugins**: Extend functionality (data sources, panels, apps)
- **Authentication**: User management and access control
- **Alerting Engine**: Monitors metrics and sends notifications

### 5. What data sources does Grafana support?
**Answer:**
**Time-Series Databases:**
- Prometheus, InfluxDB, TimescaleDB, OpenTSDB

**Relational Databases:**
- MySQL, PostgreSQL, Microsoft SQL Server

**Cloud Services:**
- AWS CloudWatch, Azure Monitor, Google Cloud Monitoring

**Application Monitoring:**
- Jaeger, Zipkin, Elastic APM

**Log Aggregation:**
- Elasticsearch, Loki, Splunk

**Others:**
- Graphite, Zabbix, TestData, CSV, JSON API

## Data Sources & Queries

### 6. How do you configure a data source in Grafana?
**Answer:**
1. **Navigate to Configuration**: Go to Configuration → Data Sources
2. **Add Data Source**: Click "Add data source"
3. **Select Type**: Choose appropriate data source type
4. **Configure Connection**: Enter URL, credentials, and settings
5. **Test Connection**: Verify connectivity
6. **Save & Test**: Save configuration and test queries

**Example Prometheus Configuration:**
```yaml
Name: Prometheus
Type: Prometheus
URL: http://prometheus:9090
Access: Server (default)
Scrape interval: 15s
Query timeout: 60s
HTTP Method: GET
```

### 7. What is the difference between Server and Browser access modes?
**Answer:**
**Server Access (Proxy):**
- Grafana server makes requests to data source
- Data source not directly accessible from browser
- Better security for internal data sources
- Grafana handles authentication and CORS

**Browser Access (Direct):**
- Browser makes direct requests to data source
- Data source must be accessible from client
- Requires CORS configuration on data source
- Useful for public APIs and services

### 8. How do you write queries for different data sources?
**Answer:**
**Prometheus (PromQL):**
```promql
# CPU usage rate
rate(cpu_usage_seconds_total[5m])

# Memory usage percentage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# HTTP request rate by status code
sum(rate(http_requests_total[5m])) by (status_code)
```

**InfluxDB (InfluxQL):**
```sql
SELECT mean("usage_percent") 
FROM "cpu" 
WHERE $timeFilter 
GROUP BY time($__interval), "host" 
fill(null)
```

**MySQL:**
```sql
SELECT 
  created_at as time,
  count(*) as value
FROM orders 
WHERE $__timeFilter(created_at)
GROUP BY $__timeGroup(created_at, $__interval)
ORDER BY time
```

### 9. What are Grafana variables and how do you use them?
**Answer:**
Variables make dashboards dynamic and reusable:

**Variable Types:**
- **Query**: Values from data source query
- **Custom**: Manually defined values
- **Constant**: Single constant value
- **Datasource**: Select data source
- **Interval**: Time interval selection
- **Ad hoc filters**: Dynamic filters

**Example Query Variable:**
```sql
-- Variable name: server
-- Query: SELECT DISTINCT hostname FROM metrics
-- Usage in query: WHERE hostname = '$server'
```

**Multi-value Variable:**
```promql
# Variable allows multiple selections
up{instance=~"$instance"}
```

### 10. How do you use template functions in Grafana?
**Answer:**
Template functions process variable values:

**Common Functions:**
- `$__timeFilter()`: Time range filter for SQL
- `$__timeGroup()`: Time grouping for SQL
- `$__interval`: Auto-calculated interval
- `$__rate_interval`: Rate calculation interval

**Variable Functions:**
- `${var:regex}`: Apply regex to variable
- `${var:csv}`: Comma-separated values
- `${var:pipe}`: Pipe-separated values
- `${var:singlequote}`: Single-quoted values

```sql
SELECT 
  $__timeGroup(timestamp, $__interval) as time,
  avg(value) as avg_value
FROM metrics 
WHERE $__timeFilter(timestamp) 
  AND server IN (${server:singlequote})
GROUP BY time
ORDER BY time
```

## Dashboard Development

### 11. What are the best practices for dashboard design?
**Answer:**
- **Clear Purpose**: Each dashboard should have a specific purpose
- **Logical Layout**: Organize panels in logical groups
- **Consistent Styling**: Use consistent colors and formatting
- **Appropriate Visualizations**: Choose right chart types for data
- **Performance**: Optimize queries and reduce panel count
- **Documentation**: Add descriptions and annotations
- **Responsive Design**: Consider different screen sizes

### 12. How do you organize panels in a Grafana dashboard?
**Answer:**
**Layout Strategies:**
- **Grid System**: 24-unit wide grid for positioning
- **Rows**: Group related panels in collapsible rows
- **Panel Sizing**: Consistent panel sizes for visual harmony
- **Hierarchy**: Most important metrics at the top
- **Flow**: Logical reading flow (left to right, top to bottom)

**Panel Organization:**
```json
{
  "panels": [
    {
      "title": "System Overview",
      "type": "row",
      "gridPos": {"h": 1, "w": 24, "x": 0, "y": 0}
    },
    {
      "title": "CPU Usage",
      "type": "graph",
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 1}
    },
    {
      "title": "Memory Usage",
      "type": "graph", 
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 1}
    }
  ]
}
```

### 13. How do you implement dashboard templating?
**Answer:**
```json
{
  "templating": {
    "list": [
      {
        "name": "datasource",
        "type": "datasource",
        "query": "prometheus"
      },
      {
        "name": "job",
        "type": "query",
        "datasource": "$datasource",
        "query": "label_values(up, job)",
        "multi": true,
        "includeAll": true
      },
      {
        "name": "instance",
        "type": "query",
        "datasource": "$datasource", 
        "query": "label_values(up{job=~\"$job\"}, instance)",
        "multi": true,
        "includeAll": true
      }
    ]
  }
}
```

### 14. What are dashboard annotations and how to use them?
**Answer:**
Annotations add contextual information to graphs:

**Types:**
- **Built-in**: Grafana annotations stored in database
- **Query-based**: Annotations from data source queries
- **API-based**: External annotations via API

**Configuration:**
```json
{
  "annotations": {
    "list": [
      {
        "name": "Deployments",
        "datasource": "prometheus",
        "expr": "increase(deployment_timestamp[1m])",
        "titleFormat": "Deployment",
        "textFormat": "Version {{version}} deployed",
        "iconColor": "green"
      }
    ]
  }
}
```

### 15. How do you share and export Grafana dashboards?
**Answer:**
**Sharing Methods:**
- **Dashboard Links**: Share URL with view permissions
- **Snapshots**: Static snapshots with data
- **Export JSON**: Download dashboard definition
- **PDF Reports**: Generate PDF reports (Enterprise)
- **Embed Panels**: Embed panels in external applications

**Export/Import:**
```bash
# Export dashboard
curl -H "Authorization: Bearer $API_KEY" \
  http://grafana:3000/api/dashboards/uid/dashboard-uid

# Import dashboard
curl -X POST -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d @dashboard.json \
  http://grafana:3000/api/dashboards/db
```

## Visualization & Panels

### 16. What are the different panel types in Grafana?
**Answer:**
**Graph Panels:**
- **Time Series**: Line, bar, and area charts
- **State Timeline**: State changes over time
- **Status History**: Status values over time

**Single Value Panels:**
- **Stat**: Single value with optional sparkline
- **Gauge**: Circular or linear gauge
- **Bar Gauge**: Horizontal/vertical bar gauge

**Table & Text:**
- **Table**: Tabular data display
- **Text**: Markdown and HTML content
- **News**: RSS feed display

**Specialized:**
- **Heatmap**: 2D histogram
- **Pie Chart**: Proportional data
- **Worldmap**: Geographic data visualization
- **Node Graph**: Network topology

### 17. How do you configure time series visualizations?
**Answer:**
```json
{
  "type": "timeseries",
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "linear",
        "lineWidth": 1,
        "fillOpacity": 10,
        "gradientMode": "none",
        "spanNulls": false,
        "pointSize": 5,
        "stacking": {
          "mode": "none",
          "group": "A"
        }
      },
      "color": {
        "mode": "palette-classic"
      },
      "unit": "bytes",
      "min": 0,
      "thresholds": {
        "steps": [
          {"color": "green", "value": null},
          {"color": "red", "value": 80}
        ]
      }
    }
  }
}
```

### 18. How do you implement thresholds and conditional formatting?
**Answer:**
**Thresholds Configuration:**
```json
{
  "thresholds": {
    "mode": "absolute",
    "steps": [
      {"color": "green", "value": null},
      {"color": "yellow", "value": 70},
      {"color": "red", "value": 90}
    ]
  }
}
```

**Value Mappings:**
```json
{
  "mappings": [
    {
      "type": "value",
      "value": "0",
      "text": "Down"
    },
    {
      "type": "value", 
      "value": "1",
      "text": "Up"
    },
    {
      "type": "range",
      "from": 2,
      "to": 10,
      "text": "Warning"
    }
  ]
}
```

### 19. How do you create custom panels and plugins?
**Answer:**
**Panel Plugin Structure:**
```typescript
// src/SimplePanel.tsx
import React from 'react';
import { PanelProps } from '@grafana/data';
import { SimpleOptions } from 'types';

interface Props extends PanelProps<SimpleOptions> {}

export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {
  return (
    <div style={{ width, height }}>
      <h2>{options.text}</h2>
      <p>Data points: {data.series[0]?.length || 0}</p>
    </div>
  );
};
```

**Plugin Configuration:**
```json
{
  "type": "panel",
  "name": "Custom Panel",
  "id": "custom-panel",
  "info": {
    "description": "Custom panel plugin",
    "author": {
      "name": "Your Name"
    },
    "version": "1.0.0"
  }
}
```

### 20. How do you optimize panel performance?
**Answer:**
- **Query Optimization**: Efficient queries with appropriate time ranges
- **Data Reduction**: Use aggregation and sampling
- **Caching**: Enable query result caching
- **Panel Limits**: Limit number of panels per dashboard
- **Refresh Intervals**: Appropriate refresh rates
- **Data Source Selection**: Choose efficient data sources

```json
{
  "targets": [
    {
      "expr": "avg_over_time(cpu_usage[5m])",
      "interval": "30s",
      "maxDataPoints": 1000,
      "refId": "A"
    }
  ],
  "refresh": "30s",
  "cacheTimeout": "300s"
}
```

## Alerting & Notifications

### 21. How does Grafana alerting work?
**Answer:**
**Alerting Components:**
- **Alert Rules**: Define conditions for triggering alerts
- **Notification Channels**: Define where to send alerts
- **Alert Manager**: Manages alert routing and grouping
- **Silences**: Temporarily disable alerts

**Alert Rule Configuration:**
```json
{
  "alert": {
    "name": "High CPU Usage",
    "message": "CPU usage is above 80%",
    "frequency": "10s",
    "conditions": [
      {
        "query": {
          "queryType": "",
          "refId": "A"
        },
        "reducer": {
          "type": "avg",
          "params": []
        },
        "evaluator": {
          "params": [80],
          "type": "gt"
        }
      }
    ]
  }
}
```

### 22. What notification channels does Grafana support?
**Answer:**
**Built-in Channels:**
- **Email**: SMTP-based email notifications
- **Slack**: Slack channel integration
- **PagerDuty**: Incident management integration
- **Webhook**: Custom HTTP webhooks
- **Microsoft Teams**: Teams channel notifications
- **Discord**: Discord channel integration

**Configuration Example:**
```json
{
  "name": "slack-alerts",
  "type": "slack",
  "settings": {
    "url": "https://hooks.slack.com/services/...",
    "channel": "#alerts",
    "username": "Grafana",
    "title": "Alert: {{range .Alerts}}{{.AlertName}}{{end}}",
    "text": "{{range .Alerts}}{{.Message}}{{end}}"
  }
}
```

### 23. How do you create effective alert rules?
**Answer:**
**Best Practices:**
- **Clear Conditions**: Define precise alert conditions
- **Appropriate Thresholds**: Set meaningful threshold values
- **Time Windows**: Use appropriate evaluation periods
- **Alert Fatigue**: Avoid too many false positives
- **Escalation**: Implement alert escalation policies
- **Documentation**: Include helpful alert messages

**Example Alert Rule:**
```json
{
  "alert": {
    "name": "Database Connection Pool Exhausted",
    "message": "Database connection pool usage is above 90% for more than 5 minutes",
    "frequency": "1m",
    "conditions": [
      {
        "query": {
          "queryType": "",
          "refId": "A",
          "model": {
            "expr": "avg(db_connection_pool_usage_percent) by (instance)"
          }
        },
        "reducer": {
          "type": "avg"
        },
        "evaluator": {
          "params": [90],
          "type": "gt"
        }
      }
    ],
    "executionErrorState": "alerting",
    "noDataState": "no_data",
    "for": "5m"
  }
}
```

### 24. How do you implement alert routing and grouping?
**Answer:**
**Alertmanager Configuration:**
```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@company.com'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
  routes:
  - match:
      severity: critical
    receiver: 'pager'
  - match:
      team: database
    receiver: 'database-team'

receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://127.0.0.1:5001/'

- name: 'pager'
  pagerduty_configs:
  - service_key: 'your-service-key'

- name: 'database-team'
  email_configs:
  - to: 'db-team@company.com'
    subject: 'Database Alert: {{ .GroupLabels.alertname }}'
```

## Administration & Security

### 25. How do you manage users and permissions in Grafana?
**Answer:**
**User Management:**
- **Local Users**: Created in Grafana database
- **LDAP/AD Integration**: Enterprise directory integration
- **OAuth**: Google, GitHub, Azure AD authentication
- **SAML**: Enterprise SSO integration

**Permission Levels:**
- **Viewer**: Read-only access to dashboards
- **Editor**: Create and edit dashboards
- **Admin**: Full administrative access

**Organization Roles:**
```json
{
  "users": [
    {
      "email": "user@company.com",
      "role": "Editor",
      "orgId": 1
    }
  ],
  "teams": [
    {
      "name": "DevOps Team",
      "members": ["user1@company.com", "user2@company.com"],
      "permissions": [
        {
          "datasource": "prometheus",
          "permission": "Query"
        }
      ]
    }
  ]
}
```

### 26. How do you configure LDAP authentication in Grafana?
**Answer:**
```ini
# grafana.ini
[auth.ldap]
enabled = true
config_file = /etc/grafana/ldap.toml
allow_sign_up = true
```

```toml
# ldap.toml
[[servers]]
host = "ldap.company.com"
port = 389
use_ssl = false
start_tls = false
ssl_skip_verify = false
bind_dn = "cn=admin,dc=company,dc=com"
bind_password = "password"
search_filter = "(cn=%s)"
search_base_dns = ["dc=company,dc=com"]

[servers.attributes]
name = "givenName"
surname = "sn"
username = "cn"
member_of = "memberOf"
email = "email"

[[servers.group_mappings]]
group_dn = "cn=admins,ou=groups,dc=company,dc=com"
org_role = "Admin"

[[servers.group_mappings]]
group_dn = "cn=developers,ou=groups,dc=company,dc=com"
org_role = "Editor"
```

### 27. How do you backup and restore Grafana?
**Answer:**
**Database Backup:**
```bash
# SQLite backup
cp /var/lib/grafana/grafana.db /backup/grafana-$(date +%Y%m%d).db

# MySQL backup
mysqldump -u grafana -p grafana > grafana-backup-$(date +%Y%m%d).sql

# PostgreSQL backup
pg_dump -U grafana grafana > grafana-backup-$(date +%Y%m%d).sql
```

**Configuration Backup:**
```bash
# Backup configuration
tar -czf grafana-config-$(date +%Y%m%d).tar.gz /etc/grafana/

# Backup dashboards via API
curl -H "Authorization: Bearer $API_KEY" \
  http://grafana:3000/api/search?type=dash-db | \
  jq -r '.[] | .uid' | \
  xargs -I {} curl -H "Authorization: Bearer $API_KEY" \
  http://grafana:3000/api/dashboards/uid/{} > dashboards-backup.json
```

### 28. How do you monitor Grafana itself?
**Answer:**
**Metrics Collection:**
```ini
# grafana.ini
[metrics]
enabled = true
interval_seconds = 10

[metrics.prometheus]
enabled = true
```

**Key Metrics to Monitor:**
- **Response Time**: Dashboard load times
- **Error Rates**: HTTP error responses
- **Resource Usage**: CPU, memory, disk usage
- **Database Performance**: Query execution times
- **User Activity**: Login attempts, dashboard views

**Monitoring Dashboard:**
```promql
# Grafana HTTP requests
grafana_http_request_duration_seconds_bucket

# Database query duration
grafana_database_query_duration_seconds

# Active users
grafana_stat_active_users

# Dashboard views
grafana_page_response_time_milliseconds
```

## Performance & Scaling

### 29. How do you optimize Grafana performance?
**Answer:**
**Query Optimization:**
- **Time Range Limits**: Reasonable default time ranges
- **Query Caching**: Enable query result caching
- **Data Source Optimization**: Efficient data source queries
- **Panel Limits**: Limit panels per dashboard

**Infrastructure Optimization:**
- **Database Performance**: Optimize Grafana database
- **Memory Allocation**: Sufficient memory for caching
- **Load Balancing**: Multiple Grafana instances
- **CDN**: Content delivery for static assets

**Configuration:**
```ini
# grafana.ini
[database]
max_idle_conn = 2
max_open_conn = 0
conn_max_lifetime = 14400

[caching]
enabled = true

[dataproxy]
timeout = 30
keep_alive_seconds = 30
```

### 30. How do you scale Grafana for large organizations?
**Answer:**
**Horizontal Scaling:**
- **Load Balancer**: Distribute traffic across instances
- **Shared Database**: Common database for all instances
- **Session Storage**: Redis for session management
- **File Storage**: Shared storage for plugins and images

**Architecture:**
```yaml
# docker-compose.yml
version: '3'
services:
  grafana-1:
    image: grafana/grafana
    environment:
      - GF_DATABASE_TYPE=mysql
      - GF_DATABASE_HOST=mysql:3306
      - GF_SESSION_PROVIDER=redis
      - GF_SESSION_PROVIDER_CONFIG=redis:6379
  
  grafana-2:
    image: grafana/grafana
    environment:
      - GF_DATABASE_TYPE=mysql
      - GF_DATABASE_HOST=mysql:3306
      - GF_SESSION_PROVIDER=redis
      - GF_SESSION_PROVIDER_CONFIG=redis:6379
  
  nginx:
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - grafana-1
      - grafana-2
```

## Scenario-Based Questions

### 31. Design a monitoring dashboard for a microservices architecture.
**Answer:**
**Dashboard Structure:**
```json
{
  "dashboard": {
    "title": "Microservices Overview",
    "tags": ["microservices", "monitoring"],
    "templating": {
      "list": [
        {
          "name": "service",
          "type": "query",
          "query": "label_values(up{job=~\".*service.*\"}, job)",
          "multi": true,
          "includeAll": true
        },
        {
          "name": "environment", 
          "type": "custom",
          "options": ["dev", "staging", "prod"]
        }
      ]
    },
    "panels": [
      {
        "title": "Service Health Overview",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=~\"$service\", environment=\"$environment\"}"
          }
        ]
      },
      {
        "title": "Request Rate",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=~\"$service\"}[5m])) by (job)"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "timeseries", 
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{job=~\"$service\", status=~\"5..\"}[5m])) by (job)"
          }
        ]
      },
      {
        "title": "Response Time P99",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{job=~\"$service\"}[5m])) by (job, le))"
          }
        ]
      }
    ]
  }
}
```

### 32. How would you implement alerting for a data pipeline monitoring system?
**Answer:**
**Alert Rules:**
```json
{
  "alerts": [
    {
      "name": "Data Pipeline Failure",
      "message": "Data pipeline {{$labels.pipeline}} has failed",
      "frequency": "1m",
      "conditions": [
        {
          "query": {
            "expr": "pipeline_status{status=\"failed\"} == 1"
          },
          "reducer": {"type": "last"},
          "evaluator": {"params": [1], "type": "gt"}
        }
      ],
      "notifications": ["data-team-slack", "pagerduty"]
    },
    {
      "name": "Data Freshness Alert",
      "message": "Data in {{$labels.table}} is stale (last update: {{$value}} hours ago)",
      "frequency": "5m", 
      "conditions": [
        {
          "query": {
            "expr": "(time() - data_last_updated_timestamp) / 3600"
          },
          "reducer": {"type": "last"},
          "evaluator": {"params": [2], "type": "gt"}
        }
      ],
      "for": "10m"
    },
    {
      "name": "Data Quality Issues",
      "message": "Data quality check failed for {{$labels.check_name}}",
      "conditions": [
        {
          "query": {
            "expr": "data_quality_check_success == 0"
          },
          "reducer": {"type": "last"},
          "evaluator": {"params": [0], "type": "eq"}
        }
      ]
    }
  ]
}
```

### 33. Your Grafana dashboards are loading slowly. How do you troubleshoot and optimize?
**Answer:**
1. **Identify Bottlenecks**: Check query execution times
2. **Optimize Queries**: Reduce time ranges and add filters
3. **Database Performance**: Monitor Grafana database performance
4. **Panel Optimization**: Reduce number of panels and queries
5. **Caching**: Enable query result caching
6. **Infrastructure**: Scale Grafana infrastructure

**Optimization Steps:**
```bash
# Check query performance
curl -H "Authorization: Bearer $API_KEY" \
  "http://grafana:3000/api/datasources/proxy/1/api/v1/query_range?query=up&start=1609459200&end=1609545600&step=60" \
  -w "@curl-format.txt"

# Enable query caching
# In grafana.ini:
[caching]
enabled = true

# Optimize panel queries
# Use appropriate time ranges and intervals
# Add proper WHERE clauses and filters
# Use aggregation functions when possible
```

---

## Key Takeaways for Interviews

1. **Core Concepts**: Understand data sources, dashboards, and visualization principles
2. **Query Languages**: Know how to write queries for different data sources
3. **Dashboard Design**: Master best practices for effective dashboard creation
4. **Alerting**: Understand alert configuration and notification channels
5. **Administration**: Know user management, security, and scaling concepts
6. **Performance**: Focus on optimization techniques for queries and infrastructure
7. **Integration**: Be familiar with common integrations and plugin ecosystem
8. **Real-world Scenarios**: Practice designing monitoring solutions for different use cases