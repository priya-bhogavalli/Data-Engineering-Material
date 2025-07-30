# Datadog Key Concepts

## 1. Datadog Architecture
**Core Components**:
- **Agent**: Collects metrics, logs, and traces
- **Integrations**: Pre-built connectors for services
- **Dashboards**: Visualization and monitoring
- **Alerts**: Notification system
- **APM**: Application Performance Monitoring
- **Logs**: Centralized log management

```yaml
# datadog.yaml configuration
api_key: YOUR_API_KEY
site: datadoghq.com
hostname: data-pipeline-server

# Enable integrations
integrations:
  postgres:
    host: localhost
    port: 5432
    username: datadog
    password: password
    
  kafka:
    kafka_connect_str: localhost:9092
    
  spark:
    spark_url: http://localhost:4040
```

## 2. Metrics Collection
```python
from datadog import initialize, statsd
import time

# Initialize Datadog
options = {
    'api_key': 'your_api_key',
    'app_key': 'your_app_key'
}
initialize(**options)

# Custom metrics
def track_pipeline_metrics():
    # Counter - tracks events
    statsd.increment('pipeline.records.processed', 
                    value=1000, 
                    tags=['pipeline:sales_etl', 'env:prod'])
    
    # Gauge - tracks current value
    statsd.gauge('pipeline.queue.size', 
                value=150, 
                tags=['queue:processing'])
    
    # Histogram - tracks distribution
    statsd.histogram('pipeline.processing.duration', 
                    value=45.2, 
                    tags=['stage:transform'])
    
    # Timer - measures execution time
    with statsd.timed('pipeline.database.query_time'):
        # Database operation
        time.sleep(0.5)

# Business metrics
def track_business_metrics():
    statsd.gauge('business.daily_revenue', 
                value=125000.50, 
                tags=['currency:USD', 'region:us-east'])
    
    statsd.increment('business.orders.completed', 
                    tags=['product_category:electronics'])
    
    statsd.histogram('business.order_value', 
                    value=299.99, 
                    tags=['customer_tier:premium'])

# Data quality metrics
def track_data_quality():
    statsd.gauge('data_quality.completeness_score', 
                value=0.95, 
                tags=['dataset:customer_data'])
    
    statsd.increment('data_quality.validation_failures', 
                    tags=['rule:email_format', 'severity:high'])
    
    statsd.histogram('data_quality.freshness_hours', 
                    value=2.5, 
                    tags=['source:sales_db'])
```

## 3. Log Management
```python
import logging
from datadog import DogStatsdClient

# Configure logging for Datadog
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
)

logger = logging.getLogger('data_pipeline')

# Structured logging
def process_data_with_logging():
    logger.info("Starting data processing", extra={
        'pipeline_id': 'sales_etl_001',
        'batch_size': 10000,
        'source': 'postgresql'
    })
    
    try:
        # Processing logic
        records_processed = 9850
        
        logger.info("Data processing completed", extra={
            'records_processed': records_processed,
            'success_rate': 0.985,
            'duration_seconds': 120
        })
        
    except Exception as e:
        logger.error("Data processing failed", extra={
            'error_type': type(e).__name__,
            'error_message': str(e),
            'pipeline_stage': 'transformation'
        })

# Log aggregation patterns
def setup_log_patterns():
    # Error tracking
    logger.error("Database connection failed", extra={
        'error.kind': 'connection_error',
        'error.stack': 'traceback_here',
        'db.host': 'prod-db-01',
        'db.port': 5432
    })
    
    # Performance tracking
    logger.info("Query executed", extra={
        'query.duration_ms': 1250,
        'query.rows_returned': 50000,
        'query.type': 'SELECT',
        'db.table': 'sales_transactions'
    })
    
    # Business events
    logger.info("Order processed", extra={
        'order.id': 'ORD-12345',
        'order.value': 299.99,
        'customer.tier': 'premium',
        'payment.method': 'credit_card'
    })
```

## 4. APM and Distributed Tracing
```python
from ddtrace import tracer, patch_all
import requests
import psycopg2

# Auto-instrument common libraries
patch_all()

# Custom tracing
@tracer.wrap('data_pipeline.extract')
def extract_data(source_config):
    with tracer.trace('database.query', service='data-pipeline') as span:
        span.set_tag('db.type', 'postgresql')
        span.set_tag('db.table', 'sales')
        
        # Database operation
        conn = psycopg2.connect(**source_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales WHERE date >= %s", ('2024-01-01',))
        results = cursor.fetchall()
        
        span.set_tag('db.rows_returned', len(results))
        return results

@tracer.wrap('data_pipeline.transform')
def transform_data(raw_data):
    with tracer.trace('data.validation') as span:
        # Validation logic
        valid_records = [r for r in raw_data if r[2] > 0]  # Amount > 0
        span.set_tag('validation.input_count', len(raw_data))
        span.set_tag('validation.output_count', len(valid_records))
    
    with tracer.trace('data.enrichment') as span:
        # Enrichment logic
        enriched_data = []
        for record in valid_records:
            # Add calculated fields
            enriched_record = record + (record[2] * 0.1,)  # Add tax
            enriched_data.append(enriched_record)
        
        span.set_tag('enrichment.records_processed', len(enriched_data))
        return enriched_data

@tracer.wrap('data_pipeline.load')
def load_data(processed_data, target_config):
    with tracer.trace('api.call', service='data-warehouse') as span:
        span.set_tag('api.endpoint', '/bulk_insert')
        span.set_tag('api.method', 'POST')
        
        response = requests.post(
            f"{target_config['url']}/bulk_insert",
            json={'data': processed_data},
            headers={'Authorization': f"Bearer {target_config['token']}"}
        )
        
        span.set_tag('http.status_code', response.status_code)
        span.set_tag('api.records_inserted', len(processed_data))
        
        if response.status_code != 200:
            span.set_error(Exception(f"API call failed: {response.text}"))
        
        return response.status_code == 200

# Pipeline orchestration with tracing
def run_etl_pipeline():
    with tracer.trace('etl_pipeline.full_run', service='data-pipeline') as span:
        span.set_tag('pipeline.name', 'sales_etl')
        span.set_tag('pipeline.version', '1.2.0')
        
        try:
            # Extract
            raw_data = extract_data({'host': 'db.example.com', 'database': 'sales'})
            
            # Transform
            processed_data = transform_data(raw_data)
            
            # Load
            success = load_data(processed_data, {'url': 'https://api.warehouse.com'})
            
            span.set_tag('pipeline.status', 'success' if success else 'failed')
            span.set_tag('pipeline.records_processed', len(processed_data))
            
        except Exception as e:
            span.set_error(e)
            span.set_tag('pipeline.status', 'error')
            raise
```

## 5. Infrastructure Monitoring
```yaml
# Kubernetes monitoring
apiVersion: v1
kind: ConfigMap
metadata:
  name: datadog-config
data:
  datadog.yaml: |
    api_key: YOUR_API_KEY
    site: datadoghq.com
    
    # Kubernetes integration
    kubernetes_kubelet_host: ${DD_KUBERNETES_KUBELET_HOST}
    kubernetes_http_kubelet_port: 10255
    kubernetes_https_kubelet_port: 10250
    
    # Container monitoring
    container_collect_all: true
    
    # Log collection
    logs_enabled: true
    logs_config:
      container_collect_all: true
      
    # Process monitoring
    process_config:
      enabled: "true"

---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: datadog-agent
spec:
  selector:
    matchLabels:
      app: datadog-agent
  template:
    metadata:
      labels:
        app: datadog-agent
    spec:
      containers:
      - name: datadog-agent
        image: datadog/agent:latest
        env:
        - name: DD_API_KEY
          valueFrom:
            secretKeyRef:
              name: datadog-secret
              key: api-key
        - name: DD_KUBERNETES_KUBELET_HOST
          valueFrom:
            fieldRef:
              fieldPath: status.hostIP
        volumeMounts:
        - name: config
          mountPath: /etc/datadog-agent/datadog.yaml
          subPath: datadog.yaml
      volumes:
      - name: config
        configMap:
          name: datadog-config
```

## 6. Dashboards and Visualization
```json
{
  "title": "Data Pipeline Monitoring",
  "description": "Monitor ETL pipeline performance and data quality",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "requests": [
          {
            "q": "avg:pipeline.records.processed{pipeline:sales_etl}.as_rate()",
            "display_type": "line",
            "style": {
              "palette": "dog_classic",
              "line_type": "solid",
              "line_width": "normal"
            }
          }
        ],
        "title": "Records Processed Rate",
        "yaxis": {
          "scale": "linear",
          "min": "auto",
          "max": "auto"
        }
      }
    },
    {
      "definition": {
        "type": "query_value",
        "requests": [
          {
            "q": "avg:data_quality.completeness_score{dataset:customer_data}",
            "aggregator": "avg"
          }
        ],
        "title": "Data Completeness Score",
        "precision": 2,
        "custom_links": [
          {
            "label": "View Data Quality Dashboard",
            "link": "/dashboard/data-quality"
          }
        ]
      }
    },
    {
      "definition": {
        "type": "heatmap",
        "requests": [
          {
            "q": "avg:pipeline.processing.duration{*} by {pipeline,stage}"
          }
        ],
        "title": "Processing Duration Heatmap"
      }
    }
  ],
  "layout_type": "ordered"
}
```

## 7. Alerting and Notifications
```python
from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor

# Configure API client
configuration = Configuration()
configuration.api_key['apiKeyAuth'] = 'your_api_key'
configuration.api_key['appKeyAuth'] = 'your_app_key'

# Create monitor
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    
    # Pipeline failure alert
    pipeline_monitor = Monitor(
        name="Data Pipeline Failure Alert",
        type="metric alert",
        query="avg(last_5m):avg:pipeline.records.processed{pipeline:sales_etl}.as_rate() < 100",
        message="""
        @slack-data-engineering
        
        **Pipeline Alert**: Sales ETL pipeline processing rate has dropped below 100 records/minute.
        
        **Runbook**: https://wiki.company.com/data-pipeline-troubleshooting
        **Dashboard**: https://app.datadoghq.com/dashboard/pipeline-monitoring
        
        {{#is_alert}}
        **Action Required**: Check pipeline logs and restart if necessary.
        {{/is_alert}}
        
        {{#is_recovery}}
        **Resolved**: Pipeline processing rate has returned to normal.
        {{/is_recovery}}
        """,
        tags=["team:data-engineering", "service:etl-pipeline"],
        options={
            "thresholds": {
                "critical": 100,
                "warning": 500
            },
            "notify_no_data": True,
            "no_data_timeframe": 10,
            "evaluation_delay": 60,
            "include_tags": True
        }
    )
    
    created_monitor = api_instance.create_monitor(body=pipeline_monitor)
    print(f"Created monitor: {created_monitor.id}")

# Data quality alert
data_quality_monitor = Monitor(
    name="Data Quality Degradation",
    type="metric alert",
    query="avg(last_15m):avg:data_quality.completeness_score{dataset:customer_data} < 0.9",
    message="""
    @pagerduty-data-team
    
    **Data Quality Alert**: Customer data completeness score has dropped below 90%.
    
    **Current Score**: {{value}}%
    **Threshold**: 90%
    
    **Immediate Actions**:
    1. Check data source connectivity
    2. Validate recent data loads
    3. Review transformation logic
    
    **Escalation**: If not resolved in 30 minutes, page on-call engineer.
    """,
    priority=1  # High priority
)

# Composite monitor for complex conditions
composite_monitor = Monitor(
    name="Pipeline Health Composite",
    type="composite",
    query="(a && b) || c",
    message="Multiple pipeline issues detected",
    options={
        "composite_monitors": [
            {"id": pipeline_monitor.id, "name": "a"},
            {"id": data_quality_monitor.id, "name": "b"},
            {"id": 12345, "name": "c"}  # Existing monitor ID
        ]
    }
)
```

## 8. Custom Integrations
```python
# Custom check for data pipeline monitoring
from datadog_checks.base import AgentCheck

class DataPipelineCheck(AgentCheck):
    def check(self, instance):
        # Get pipeline status from API
        pipeline_api_url = instance.get('pipeline_api_url')
        pipeline_name = instance.get('pipeline_name')
        
        try:
            response = self.http.get(f"{pipeline_api_url}/status/{pipeline_name}")
            pipeline_data = response.json()
            
            # Submit metrics
            self.gauge('pipeline.last_run_duration', 
                      pipeline_data['last_run_duration'],
                      tags=[f'pipeline:{pipeline_name}'])
            
            self.gauge('pipeline.records_processed', 
                      pipeline_data['records_processed'],
                      tags=[f'pipeline:{pipeline_name}'])
            
            # Submit service check
            if pipeline_data['status'] == 'healthy':
                self.service_check('pipeline.status', 
                                 AgentCheck.OK,
                                 tags=[f'pipeline:{pipeline_name}'])
            else:
                self.service_check('pipeline.status', 
                                 AgentCheck.CRITICAL,
                                 message=pipeline_data.get('error_message'),
                                 tags=[f'pipeline:{pipeline_name}'])
                
        except Exception as e:
            self.service_check('pipeline.status', 
                             AgentCheck.CRITICAL,
                             message=str(e),
                             tags=[f'pipeline:{pipeline_name}'])

# Configuration for custom check
# conf.d/data_pipeline.yaml
instances:
  - pipeline_api_url: "https://api.datapipeline.com"
    pipeline_name: "sales_etl"
    min_collection_interval: 60
    
  - pipeline_api_url: "https://api.datapipeline.com"
    pipeline_name: "customer_sync"
    min_collection_interval: 300
```

## 9. Log Analysis and Patterns
```python
# Log parsing and analysis
import json
import re
from datetime import datetime

def parse_pipeline_logs():
    # Define log patterns
    patterns = {
        'error': re.compile(r'ERROR.*?(\w+Exception): (.+)'),
        'performance': re.compile(r'Query executed in (\d+)ms, returned (\d+) rows'),
        'business_event': re.compile(r'Order (\w+) processed: \$(\d+\.\d+)')
    }
    
    # Process log entries
    with open('/var/log/pipeline.log', 'r') as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                
                # Extract structured data
                if 'error' in log_entry.get('level', '').lower():
                    statsd.increment('logs.errors',
                                   tags=[f"error_type:{log_entry.get('error_type', 'unknown')}"])
                
                # Performance metrics from logs
                if 'query.duration_ms' in log_entry:
                    statsd.histogram('database.query_duration',
                                   log_entry['query.duration_ms'],
                                   tags=[f"table:{log_entry.get('db.table', 'unknown')}"])
                
                # Business metrics from logs
                if 'order.value' in log_entry:
                    statsd.histogram('business.order_value',
                                   log_entry['order.value'],
                                   tags=[f"tier:{log_entry.get('customer.tier', 'standard')}"])
                    
            except json.JSONDecodeError:
                # Handle non-JSON logs
                for pattern_name, pattern in patterns.items():
                    match = pattern.search(line)
                    if match:
                        if pattern_name == 'error':
                            statsd.increment('logs.errors.unstructured',
                                           tags=[f'exception:{match.group(1)}'])
                        elif pattern_name == 'performance':
                            statsd.histogram('database.query_duration.parsed',
                                           int(match.group(1)),
                                           tags=['source:log_parsing'])

# Log-based alerting
def setup_log_monitors():
    log_monitor = Monitor(
        name="High Error Rate in Pipeline Logs",
        type="log alert",
        query='logs("service:data-pipeline ERROR").index("*").rollup("count").last("5m") > 10',
        message="""
        @slack-data-engineering
        
        **Log Alert**: High error rate detected in data pipeline logs.
        
        **Error Count**: {{value}} errors in the last 5 minutes
        **Threshold**: 10 errors
        
        **Investigation Steps**:
        1. Check recent deployments
        2. Review error patterns in logs
        3. Validate data source connectivity
        
        **Logs**: https://app.datadoghq.com/logs?query=service:data-pipeline ERROR
        """,
        options={
            "thresholds": {"critical": 10, "warning": 5},
            "evaluation_delay": 60
        }
    )
```

## 10. Cost Optimization and Best Practices
```python
# Efficient metric collection
class OptimizedMetricsCollector:
    def __init__(self):
        self.batch_metrics = []
        self.batch_size = 100
        
    def add_metric(self, metric_name, value, tags=None):
        self.batch_metrics.append({
            'metric': metric_name,
            'value': value,
            'tags': tags or [],
            'timestamp': time.time()
        })
        
        if len(self.batch_metrics) >= self.batch_size:
            self.flush_metrics()
    
    def flush_metrics(self):
        if self.batch_metrics:
            # Send batch to Datadog
            for metric in self.batch_metrics:
                statsd.gauge(metric['metric'], 
                           metric['value'], 
                           tags=metric['tags'])
            
            self.batch_metrics.clear()

# Sampling for high-volume metrics
def sample_high_volume_metrics():
    import random
    
    # Sample 10% of high-frequency events
    if random.random() < 0.1:
        statsd.increment('high_volume.api_calls',
                        tags=['endpoint:/api/data'])

# Tag optimization
def optimize_tags():
    # Good: Limited, meaningful tags
    statsd.gauge('pipeline.duration', 
                value=120,
                tags=['pipeline:sales_etl', 'env:prod', 'region:us-east'])
    
    # Avoid: Too many high-cardinality tags
    # statsd.gauge('pipeline.duration', 
    #             value=120,
    #             tags=[f'user_id:{user_id}', f'request_id:{request_id}'])

# Monitor usage and costs
def track_datadog_usage():
    # Custom metrics count
    statsd.gauge('datadog.custom_metrics.count', 
                get_custom_metrics_count(),
                tags=['account:production'])
    
    # Log volume
    statsd.gauge('datadog.logs.volume_gb', 
                get_daily_log_volume(),
                tags=['source:application'])
    
    # APM trace volume
    statsd.gauge('datadog.apm.traces.count', 
                get_trace_count(),
                tags=['service:data-pipeline'])
```