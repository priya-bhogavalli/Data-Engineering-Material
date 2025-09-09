
### Q1: What is Prometheus and what problems does it solve?
**Answer:**
Prometheus is an open-source monitoring and alerting toolkit designed for reliability and scalability.

**Key Problems Solved:**
- **System Monitoring**: Track application and infrastructure metrics
- **Alerting**: Proactive issue detection and notification
- **Performance Monitoring**: Application performance insights
- **Capacity Planning**: Resource utilization tracking
- **Troubleshooting**: Historical data for root cause analysis

**Core Features:**
- Multi-dimensional data model
- Powerful query language (PromQL)
- Pull-based metric collection
- Service discovery integration
- Built-in alerting
- Visualization support

### Q2: What is Prometheus's data model?
**Answer:**
**Data Model Components:**
- **Metric Name**: Identifies the measurement
- **Labels**: Key-value pairs for dimensions
- **Timestamp**: When the measurement was taken
- **Value**: The actual measurement (float64)

**Example:**
```
http_requests_total{method="GET", handler="/api/users", status="200"} 1027 @1609459200
```

**Metric Types:**
- **Counter**: Monotonically increasing values
- **Gauge**: Values that can go up and down
- **Histogram**: Distribution of observations
- **Summary**: Similar to histogram with quantiles

---

## Architecture & Components

### Q3: Explain Prometheus architecture and its components.
**Answer:**
**Core Components:**
- **Prometheus Server**: Main server that scrapes and stores metrics
- **Client Libraries**: Instrument applications
- **Push Gateway**: For short-lived jobs
- **Exporters**: Expose metrics from third-party systems
- **Alertmanager**: Handle alerts and notifications
- **Web UI**: Built-in expression browser

**Architecture Flow:**
```
Applications → Prometheus Server → Alertmanager
     ↓              ↓                    ↓
Exporters      Time Series DB      Notifications
     ↓              ↓
Push Gateway   Grafana/UI
```

### Q4: What are Prometheus exporters and how do they work?
**Answer:**
**Exporter Types:**
- **Official Exporters**: Node, Blackbox, MySQL, etc.
- **Third-party Exporters**: Community-maintained
- **Custom Exporters**: Application-specific metrics

**Popular Exporters:**
```yaml
# Node Exporter - System metrics
node_cpu_seconds_total
node_memory_MemAvailable_bytes
node_filesystem_size_bytes

# MySQL Exporter - Database metrics
mysql_up
mysql_global_status_connections
mysql_global_status_slow_queries
```

**Custom Exporter Example:**
```python
from prometheus_client import start_http_server, Counter, Gauge
import time

# Define metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
ACTIVE_USERS = Gauge('app_active_users', 'Currently active users')

# Start metrics server
start_http_server(8000)

# Update metrics
REQUEST_COUNT.labels(method='GET', endpoint='/api/users').inc()
ACTIVE_USERS.set(150)
```

---

## Metrics & Data Model

### Q5: What are the different metric types in Prometheus?
**Answer:**
**Counter:**
- Always increasing values
- Use for: requests, errors, tasks completed
```python
from prometheus_client import Counter
requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method'])
requests_total.labels(method='GET').inc()
```

**Gauge:**
- Values that can increase or decrease
- Use for: temperature, memory usage, queue size
```python
from prometheus_client import Gauge
memory_usage = Gauge('memory_usage_bytes', 'Memory usage in bytes')
memory_usage.set(1024 * 1024 * 512)  # 512MB
```

**Histogram:**
- Distribution of observations
- Use for: request durations, response sizes
```python
from prometheus_client import Histogram
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
with request_duration.time():
    # Process request
    pass
```

### Q6: How do labels work in Prometheus?
**Answer:**
**Label Characteristics:**
- Key-value pairs for metric dimensions
- Enable multi-dimensional queries
- Create unique time series

**Best Practices:**
```python
# Good - Low cardinality labels
http_requests_total{method="GET", status="200", handler="/api/users"}

# Bad - High cardinality labels (avoid)
http_requests_total{user_id="12345", session_id="abcdef"}  # Too many unique values

# Good - Bounded cardinality
http_requests_total{method="GET", status_class="2xx", endpoint="/api/users"}
```

---

## PromQL

### Q7: What is PromQL and how do you use it?
**Answer:**
PromQL (Prometheus Query Language) is used to query and aggregate time series data.

**Basic Queries:**
```promql
# Instant vector - current values
http_requests_total

# Range vector - values over time
http_requests_total[5m]

# Rate calculation
rate(http_requests_total[5m])

# Aggregation
sum(rate(http_requests_total[5m])) by (method)
```

**Common Functions:**
```promql
# Rate and increase
rate(counter[5m])          # Per-second rate
increase(counter[5m])      # Total increase

# Aggregation
sum(metric) by (label)     # Sum by label
avg(metric)                # Average
max(metric)                # Maximum
count(metric)              # Count of series
```

### Q8: How do you write complex PromQL queries?
**Answer:**
**Advanced Queries:**
```promql
# Error rate calculation
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m])) * 100

# 95th percentile latency
histogram_quantile(0.95, 
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)

# Memory usage percentage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) /
node_memory_MemTotal_bytes * 100

# Top 5 endpoints by request rate
topk(5, sum(rate(http_requests_total[5m])) by (endpoint))
```

---

## Configuration

### Q9: How do you configure Prometheus?
**Answer:**
**Configuration File (prometheus.yml):**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
  
  - job_name: 'application'
    metrics_path: '/metrics'
    scrape_interval: 30s
    static_configs:
      - targets: ['app1:8080', 'app2:8080']
```

### Q10: How do you configure scrape intervals and timeouts?
**Answer:**
**Scrape Configuration:**
```yaml
scrape_configs:
  - job_name: 'high-frequency-app'
    scrape_interval: 5s      # Override global interval
    scrape_timeout: 3s       # Timeout for scrape
    metrics_path: '/metrics'
    static_configs:
      - targets: ['app:8080']
  
  - job_name: 'batch-jobs'
    scrape_interval: 60s     # Less frequent scraping
    scrape_timeout: 10s
    static_configs:
      - targets: ['batch-server:9090']
```

**Best Practices:**
- Default: 15s scrape interval
- High-frequency: 5-10s for critical services
- Low-frequency: 60s+ for batch jobs
- Timeout: Should be less than scrape interval

---

## Service Discovery

### Q11: What service discovery mechanisms does Prometheus support?
**Answer:**
**Service Discovery Types:**
- **Static**: Manual target configuration
- **DNS**: DNS-based discovery
- **Kubernetes**: Native Kubernetes integration
- **Consul**: HashiCorp Consul integration
- **EC2**: AWS EC2 instance discovery
- **File**: File-based configuration

**Kubernetes Service Discovery:**
```yaml
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

### Q12: How do you use relabeling in Prometheus?
**Answer:**
**Relabeling Actions:**
- **keep**: Keep targets matching regex
- **drop**: Drop targets matching regex
- **replace**: Replace label values
- **labelmap**: Map label names

**Example:**
```yaml
relabel_configs:
  # Keep only targets with scrape annotation
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    action: keep
    regex: true
  
  # Set custom metrics path
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
    action: replace
    target_label: __metrics_path__
    regex: (.+)
  
  # Add environment label
  - source_labels: [__meta_kubernetes_namespace]
    action: replace
    target_label: environment
    regex: (.+)
```

---

## Alerting

### Q13: How do you configure alerting in Prometheus?
**Answer:**
**Alert Rules (alert_rules.yml):**
```yaml
groups:
  - name: example
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) /
          sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"
      
      - alert: HighMemoryUsage
        expr: |
          (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) /
          node_memory_MemTotal_bytes > 0.9
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
```

### Q14: How does Alertmanager work with Prometheus?
**Answer:**
**Alertmanager Configuration:**
```yaml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@company.com'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
  - name: 'web.hook'
    email_configs:
      - to: 'admin@company.com'
        subject: 'Alert: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}
    
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#alerts'
        title: 'Alert: {{ .GroupLabels.alertname }}'
```

---

## Storage & Performance

### Q15: How does Prometheus store data?
**Answer:**
**Storage Architecture:**
- **Local Storage**: Time series database on disk
- **Retention**: Configurable data retention period
- **Compaction**: Automatic data compaction
- **WAL**: Write-ahead log for durability

**Storage Configuration:**
```yaml
# Command line flags
--storage.tsdb.path=/prometheus/data
--storage.tsdb.retention.time=15d
--storage.tsdb.retention.size=10GB
--storage.tsdb.wal-compression
```

**Storage Structure:**
```
/prometheus/data/
├── 01ABCDEF/          # Block directory
│   ├── chunks/        # Compressed chunks
│   ├── index          # Series index
│   └── meta.json      # Block metadata
├── wal/               # Write-ahead log
└── queries.active     # Active queries
```

### Q16: How do you optimize Prometheus performance?
**Answer:**
**Performance Optimization:**

1. **Reduce Cardinality**: Limit label combinations
```python
# Bad - High cardinality
requests_total{user_id="12345", session_id="abcdef"}

# Good - Low cardinality
requests_total{endpoint="/api/users", method="GET", status="200"}
```

2. **Efficient Queries**: Use recording rules
```yaml
groups:
  - name: recording_rules
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
```

3. **Resource Allocation**:
```yaml
# Docker resource limits
resources:
  limits:
    memory: "4Gi"
    cpu: "2"
  requests:
    memory: "2Gi"
    cpu: "1"
```

---

## Integration

### Q17: How do you integrate Prometheus with Grafana?
**Answer:**
**Grafana Data Source Configuration:**
```json
{
  "name": "Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy",
  "isDefault": true
}
```

**Dashboard Query Examples:**
```promql
# CPU Usage Panel
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Usage Panel
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / 
node_memory_MemTotal_bytes * 100

# Request Rate Panel
sum(rate(http_requests_total[5m])) by (method)
```

### Q18: How do you integrate Prometheus with Kubernetes?
**Answer:**
**Kubernetes Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
        - name: storage
          mountPath: /prometheus
      volumes:
      - name: config
        configMap:
          name: prometheus-config
      - name: storage
        persistentVolumeClaim:
          claimName: prometheus-storage
```

**ServiceMonitor for Operator:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-monitor
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

---

## Best Practices

### Q19: What are Prometheus best practices?
**Answer:**
**Metric Design:**
- Use descriptive metric names
- Keep label cardinality low
- Use appropriate metric types
- Include units in metric names

**Naming Conventions:**
```python
# Good metric names
http_requests_total          # Counter with _total suffix
http_request_duration_seconds # Histogram with unit
memory_usage_bytes          # Gauge with unit
process_cpu_seconds_total   # Counter with unit

# Bad metric names
requests                    # No unit, unclear type
http_req_dur               # Abbreviated, no unit
```

**Query Optimization:**
- Use recording rules for complex queries
- Avoid high-cardinality aggregations
- Use appropriate time ranges
- Leverage caching where possible

---

## Scenario-Based Questions

### Q20: How would you monitor a microservices architecture with Prometheus?
**Answer:**
**Monitoring Strategy:**
1. **Service-level Metrics**: RED method (Rate, Errors, Duration)
2. **Infrastructure Metrics**: USE method (Utilization, Saturation, Errors)
3. **Business Metrics**: Custom application metrics
4. **Distributed Tracing**: Integration with Jaeger/Zipkin

**Implementation:**
```yaml
# Service discovery for microservices
scrape_configs:
  - job_name: 'microservices'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: microservice-.*
      - source_labels: [__meta_kubernetes_pod_label_version]
        target_label: version
```

**Key Metrics:**
```promql
# Request rate
sum(rate(http_requests_total[5m])) by (service)

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service) /
sum(rate(http_requests_total[5m])) by (service)

# Response time
histogram_quantile(0.95, 
  sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
)
```

---

## 🎯 Key Takeaways

- **Pull-based Model**: Prometheus scrapes metrics from targets
- **Multi-dimensional**: Rich data model with labels
- **PromQL**: Powerful query language for analysis
- **Service Discovery**: Automatic target discovery
- **Alerting**: Built-in alerting with Alertmanager
- **Scalable**: Handles high-cardinality metrics efficiently
- **Ecosystem**: Rich ecosystem of exporters and integrations

Remember: Prometheus excels at monitoring dynamic, cloud-native environments with its pull-based model and powerful query capabilities.