# 📊 Visualization & BI Practical Examples for Data Engineering

## 🎯 **Real-time Data Dashboard with Grafana**

### **Prometheus Metrics Collection**
```python
# src/metrics_collector.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import random
import psycopg2
import redis
from datetime import datetime

class DataPipelineMetrics:
    def __init__(self):
        # Define metrics
        self.pipeline_runs = Counter(
            'data_pipeline_runs_total',
            'Total number of pipeline runs',
            ['pipeline_name', 'status']
        )
        
        self.pipeline_duration = Histogram(
            'data_pipeline_duration_seconds',
            'Time spent processing pipeline',
            ['pipeline_name']
        )
        
        self.records_processed = Counter(
            'data_records_processed_total',
            'Total number of records processed',
            ['pipeline_name', 'table_name']
        )
        
        self.data_quality_score = Gauge(
            'data_quality_score',
            'Current data quality score',
            ['table_name']
        )
        
        self.database_connections = Gauge(
            'database_connections_active',
            'Number of active database connections',
            ['database_name']
        )
        
        self.cache_hit_rate = Gauge(
            'cache_hit_rate',
            'Cache hit rate percentage',
            ['cache_type']
        )
    
    def record_pipeline_run(self, pipeline_name, status, duration, records_count, table_name):
        """Record pipeline execution metrics"""
        self.pipeline_runs.labels(pipeline_name=pipeline_name, status=status).inc()
        self.pipeline_duration.labels(pipeline_name=pipeline_name).observe(duration)
        self.records_processed.labels(pipeline_name=pipeline_name, table_name=table_name).inc(records_count)
    
    def update_data_quality(self, table_name, score):
        """Update data quality score"""
        self.data_quality_score.labels(table_name=table_name).set(score)
    
    def update_database_metrics(self):
        """Update database connection metrics"""
        try:
            # PostgreSQL connections
            conn = psycopg2.connect(
                host="localhost",
                database="datawarehouse",
                user="dataeng",
                password="password"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
            active_connections = cursor.fetchone()[0]
            self.database_connections.labels(database_name="postgresql").set(active_connections)
            conn.close()
            
        except Exception as e:
            print(f"Error collecting database metrics: {e}")
    
    def update_cache_metrics(self):
        """Update cache hit rate metrics"""
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            info = r.info()
            
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total = hits + misses
            
            hit_rate = (hits / total * 100) if total > 0 else 0
            self.cache_hit_rate.labels(cache_type="redis").set(hit_rate)
            
        except Exception as e:
            print(f"Error collecting cache metrics: {e}")

# Simulate data pipeline with metrics
def simulate_data_pipeline():
    metrics = DataPipelineMetrics()
    
    # Start Prometheus metrics server
    start_http_server(8000)
    print("Metrics server started on port 8000")
    
    pipelines = ['customer_etl', 'order_processing', 'analytics_aggregation']
    tables = ['customers', 'orders', 'products', 'analytics']
    
    while True:
        for pipeline in pipelines:
            # Simulate pipeline execution
            start_time = time.time()
            
            # Random execution parameters
            status = random.choice(['success', 'success', 'success', 'failed'])  # 75% success rate
            records_count = random.randint(1000, 10000)
            table_name = random.choice(tables)
            
            # Simulate processing time
            processing_time = random.uniform(10, 120)  # 10-120 seconds
            time.sleep(2)  # Actual sleep for demo
            
            # Record metrics
            metrics.record_pipeline_run(pipeline, status, processing_time, records_count, table_name)
            
            # Update data quality scores
            quality_score = random.uniform(0.7, 1.0) if status == 'success' else random.uniform(0.3, 0.7)
            metrics.update_data_quality(table_name, quality_score)
        
        # Update system metrics
        metrics.update_database_metrics()
        metrics.update_cache_metrics()
        
        time.sleep(30)  # Update every 30 seconds

if __name__ == "__main__":
    simulate_data_pipeline()
```

### **Grafana Dashboard Configuration**
```json
{
  "dashboard": {
    "id": null,
    "title": "Data Engineering Pipeline Dashboard",
    "tags": ["data-engineering", "pipelines"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Pipeline Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(data_pipeline_runs_total{status=\"success\"}[5m]) / rate(data_pipeline_runs_total[5m]) * 100",
            "legendFormat": "Success Rate %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 80},
                {"color": "green", "value": 95}
              ]
            },
            "unit": "percent"
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Pipeline Execution Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(data_pipeline_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(data_pipeline_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ],
        "yAxes": [
          {
            "label": "Duration (seconds)",
            "min": 0
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 6, "y": 0}
      },
      {
        "id": 3,
        "title": "Records Processed per Hour",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(data_records_processed_total[1h]) * 3600",
            "legendFormat": "{{pipeline_name}} - {{table_name}}"
          }
        ],
        "gridPos": {"h": 8, "w": 6, "x": 18, "y": 0}
      },
      {
        "id": 4,
        "title": "Data Quality Scores",
        "type": "graph",
        "targets": [
          {
            "expr": "data_quality_score",
            "legendFormat": "{{table_name}}"
          }
        ],
        "yAxes": [
          {
            "label": "Quality Score",
            "min": 0,
            "max": 1
          }
        ],
        "alert": {
          "conditions": [
            {
              "query": {"params": ["A", "5m", "now"]},
              "reducer": {"params": [], "type": "last"},
              "evaluator": {"params": [0.8], "type": "lt"}
            }
          ],
          "executionErrorState": "alerting",
          "for": "5m",
          "frequency": "10s",
          "handler": 1,
          "name": "Data Quality Alert",
          "noDataState": "no_data",
          "notifications": []
        },
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
      },
      {
        "id": 5,
        "title": "System Metrics",
        "type": "graph",
        "targets": [
          {
            "expr": "database_connections_active",
            "legendFormat": "DB Connections - {{database_name}}"
          },
          {
            "expr": "cache_hit_rate",
            "legendFormat": "Cache Hit Rate - {{cache_type}}"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
```

## 📈 **Interactive Analytics Dashboard with Streamlit**

### **Data Engineering KPI Dashboard**
```python
# src/streamlit_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Data Engineering Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DataEngineeringDashboard:
    def __init__(self):
        self.conn = None
        self.connect_to_database()
    
    def connect_to_database(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                host=st.secrets["database"]["host"],
                database=st.secrets["database"]["name"],
                user=st.secrets["database"]["user"],
                password=st.secrets["database"]["password"]
            )
        except Exception as e:
            st.error(f"Database connection failed: {e}")
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def load_pipeline_metrics(_self, days=7):
        """Load pipeline execution metrics"""
        query = """
        SELECT 
            pipeline_name,
            execution_date,
            status,
            duration_seconds,
            records_processed,
            data_quality_score
        FROM pipeline_executions 
        WHERE execution_date >= CURRENT_DATE - INTERVAL '%s days'
        ORDER BY execution_date DESC
        """
        
        return pd.read_sql(query, _self.conn, params=[days])
    
    @st.cache_data(ttl=300)
    def load_data_quality_trends(_self, days=30):
        """Load data quality trends"""
        query = """
        SELECT 
            table_name,
            check_date,
            completeness_score,
            accuracy_score,
            consistency_score,
            timeliness_score,
            overall_score
        FROM data_quality_checks 
        WHERE check_date >= CURRENT_DATE - INTERVAL '%s days'
        ORDER BY check_date DESC
        """
        
        return pd.read_sql(query, _self.conn, params=[days])
    
    @st.cache_data(ttl=300)
    def load_system_performance(_self, hours=24):
        """Load system performance metrics"""
        query = """
        SELECT 
            timestamp,
            cpu_usage,
            memory_usage,
            disk_usage,
            network_io,
            active_connections
        FROM system_metrics 
        WHERE timestamp >= NOW() - INTERVAL '%s hours'
        ORDER BY timestamp DESC
        """
        
        return pd.read_sql(query, _self.conn, params=[hours])
    
    def create_kpi_cards(self, df_pipelines):
        """Create KPI cards"""
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate KPIs
        total_runs = len(df_pipelines)
        success_rate = (df_pipelines['status'] == 'success').mean() * 100
        avg_duration = df_pipelines['duration_seconds'].mean()
        total_records = df_pipelines['records_processed'].sum()
        
        with col1:
            st.metric(
                label="Total Pipeline Runs",
                value=f"{total_runs:,}",
                delta=f"+{total_runs - len(df_pipelines[df_pipelines['execution_date'] < datetime.now().date() - timedelta(days=1)]):,}"
            )
        
        with col2:
            st.metric(
                label="Success Rate",
                value=f"{success_rate:.1f}%",
                delta=f"{success_rate - 95:.1f}%" if success_rate < 95 else f"+{success_rate - 95:.1f}%"
            )
        
        with col3:
            st.metric(
                label="Avg Duration",
                value=f"{avg_duration:.0f}s",
                delta=f"{avg_duration - 60:.0f}s"
            )
        
        with col4:
            st.metric(
                label="Records Processed",
                value=f"{total_records:,.0f}",
                delta=f"+{total_records * 0.1:,.0f}"
            )
    
    def create_pipeline_performance_chart(self, df_pipelines):
        """Create pipeline performance visualization"""
        st.subheader("📈 Pipeline Performance Trends")
        
        # Group by date and pipeline
        daily_stats = df_pipelines.groupby(['execution_date', 'pipeline_name']).agg({
            'duration_seconds': 'mean',
            'records_processed': 'sum',
            'status': lambda x: (x == 'success').mean() * 100
        }).reset_index()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Execution Duration', 'Records Processed', 'Success Rate', 'Data Quality Score'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Duration chart
        for pipeline in daily_stats['pipeline_name'].unique():
            pipeline_data = daily_stats[daily_stats['pipeline_name'] == pipeline]
            fig.add_trace(
                go.Scatter(
                    x=pipeline_data['execution_date'],
                    y=pipeline_data['duration_seconds'],
                    mode='lines+markers',
                    name=f'{pipeline} Duration',
                    showlegend=True
                ),
                row=1, col=1
            )
        
        # Records processed
        for pipeline in daily_stats['pipeline_name'].unique():
            pipeline_data = daily_stats[daily_stats['pipeline_name'] == pipeline]
            fig.add_trace(
                go.Bar(
                    x=pipeline_data['execution_date'],
                    y=pipeline_data['records_processed'],
                    name=f'{pipeline} Records',
                    showlegend=False
                ),
                row=1, col=2
            )
        
        # Success rate
        for pipeline in daily_stats['pipeline_name'].unique():
            pipeline_data = daily_stats[daily_stats['pipeline_name'] == pipeline]
            fig.add_trace(
                go.Scatter(
                    x=pipeline_data['execution_date'],
                    y=pipeline_data['status'],
                    mode='lines+markers',
                    name=f'{pipeline} Success Rate',
                    showlegend=False
                ),
                row=2, col=1
            )
        
        # Data quality score
        quality_by_date = df_pipelines.groupby('execution_date')['data_quality_score'].mean().reset_index()
        fig.add_trace(
            go.Scatter(
                x=quality_by_date['execution_date'],
                y=quality_by_date['data_quality_score'],
                mode='lines+markers',
                name='Avg Quality Score',
                line=dict(color='green'),
                showlegend=False
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    def create_data_quality_dashboard(self, df_quality):
        """Create data quality dashboard"""
        st.subheader("🔍 Data Quality Monitoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Quality score heatmap
            pivot_data = df_quality.pivot_table(
                values='overall_score',
                index='table_name',
                columns='check_date',
                aggfunc='mean'
            )
            
            fig_heatmap = px.imshow(
                pivot_data,
                title="Data Quality Heatmap",
                color_continuous_scale="RdYlGn",
                aspect="auto"
            )
            fig_heatmap.update_layout(height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with col2:
            # Quality dimensions radar chart
            latest_quality = df_quality.groupby('table_name').last().reset_index()
            
            fig_radar = go.Figure()
            
            for table in latest_quality['table_name'].unique()[:3]:  # Show top 3 tables
                table_data = latest_quality[latest_quality['table_name'] == table].iloc[0]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=[
                        table_data['completeness_score'],
                        table_data['accuracy_score'],
                        table_data['consistency_score'],
                        table_data['timeliness_score']
                    ],
                    theta=['Completeness', 'Accuracy', 'Consistency', 'Timeliness'],
                    fill='toself',
                    name=table
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=True,
                title="Data Quality Dimensions",
                height=400
            )
            st.plotly_chart(fig_radar, use_container_width=True)
    
    def create_system_monitoring(self, df_system):
        """Create system monitoring dashboard"""
        st.subheader("🖥️ System Performance")
        
        # System metrics over time
        fig_system = make_subplots(
            rows=2, cols=2,
            subplot_titles=('CPU Usage', 'Memory Usage', 'Disk Usage', 'Active Connections')
        )
        
        fig_system.add_trace(
            go.Scatter(x=df_system['timestamp'], y=df_system['cpu_usage'], name='CPU %'),
            row=1, col=1
        )
        
        fig_system.add_trace(
            go.Scatter(x=df_system['timestamp'], y=df_system['memory_usage'], name='Memory %'),
            row=1, col=2
        )
        
        fig_system.add_trace(
            go.Scatter(x=df_system['timestamp'], y=df_system['disk_usage'], name='Disk %'),
            row=2, col=1
        )
        
        fig_system.add_trace(
            go.Scatter(x=df_system['timestamp'], y=df_system['active_connections'], name='Connections'),
            row=2, col=2
        )
        
        fig_system.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_system, use_container_width=True)
        
        # System alerts
        st.subheader("🚨 System Alerts")
        
        # Check for alerts
        latest_metrics = df_system.iloc[0]
        
        alerts = []
        if latest_metrics['cpu_usage'] > 80:
            alerts.append(f"⚠️ High CPU usage: {latest_metrics['cpu_usage']:.1f}%")
        
        if latest_metrics['memory_usage'] > 85:
            alerts.append(f"⚠️ High memory usage: {latest_metrics['memory_usage']:.1f}%")
        
        if latest_metrics['disk_usage'] > 90:
            alerts.append(f"⚠️ High disk usage: {latest_metrics['disk_usage']:.1f}%")
        
        if alerts:
            for alert in alerts:
                st.error(alert)
        else:
            st.success("✅ All system metrics are within normal ranges")
    
    def run_dashboard(self):
        """Main dashboard function"""
        st.title("📊 Data Engineering Dashboard")
        st.markdown("Real-time monitoring of data pipelines, quality, and system performance")
        
        # Sidebar filters
        st.sidebar.header("Filters")
        days_filter = st.sidebar.selectbox("Time Range", [1, 7, 14, 30], index=1)
        pipeline_filter = st.sidebar.multiselect(
            "Select Pipelines",
            ["customer_etl", "order_processing", "analytics_aggregation"],
            default=["customer_etl", "order_processing", "analytics_aggregation"]
        )
        
        # Auto-refresh
        auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)")
        if auto_refresh:
            st.rerun()
        
        # Load data
        with st.spinner("Loading data..."):
            df_pipelines = self.load_pipeline_metrics(days_filter)
            df_quality = self.load_data_quality_trends(days_filter)
            df_system = self.load_system_performance(24)
        
        # Filter data
        if pipeline_filter:
            df_pipelines = df_pipelines[df_pipelines['pipeline_name'].isin(pipeline_filter)]
        
        # Create dashboard sections
        self.create_kpi_cards(df_pipelines)
        
        st.divider()
        
        self.create_pipeline_performance_chart(df_pipelines)
        
        st.divider()
        
        self.create_data_quality_dashboard(df_quality)
        
        st.divider()
        
        self.create_system_monitoring(df_system)
        
        # Data export
        st.sidebar.header("Data Export")
        if st.sidebar.button("Export Pipeline Data"):
            csv = df_pipelines.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"pipeline_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Run the dashboard
if __name__ == "__main__":
    dashboard = DataEngineeringDashboard()
    dashboard.run_dashboard()
```

## 📊 **Power BI Integration for Data Engineering**

### **Power BI Data Model Setup**
```python
# src/powerbi_integration.py
import pandas as pd
from sqlalchemy import create_engine
import requests
import json
from datetime import datetime, timedelta

class PowerBIDataPrep:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
    
    def create_pipeline_fact_table(self):
        """Create fact table for pipeline executions"""
        query = """
        SELECT 
            pe.execution_id,
            pe.pipeline_name,
            pe.execution_date,
            pe.start_time,
            pe.end_time,
            pe.status,
            pe.duration_seconds,
            pe.records_processed,
            pe.error_message,
            dq.overall_score as data_quality_score,
            CASE 
                WHEN pe.status = 'success' THEN 1 
                ELSE 0 
            END as success_flag,
            CASE 
                WHEN pe.duration_seconds <= 60 THEN 'Fast'
                WHEN pe.duration_seconds <= 300 THEN 'Medium'
                ELSE 'Slow'
            END as performance_category
        FROM pipeline_executions pe
        LEFT JOIN data_quality_checks dq 
            ON pe.pipeline_name = dq.table_name 
            AND pe.execution_date = dq.check_date
        WHERE pe.execution_date >= CURRENT_DATE - INTERVAL '90 days'
        """
        
        df = pd.read_sql(query, self.engine)
        
        # Add calculated columns
        df['execution_hour'] = pd.to_datetime(df['start_time']).dt.hour
        df['execution_day_of_week'] = pd.to_datetime(df['execution_date']).dt.day_name()
        df['records_per_second'] = df['records_processed'] / df['duration_seconds']
        
        return df
    
    def create_data_quality_dimension(self):
        """Create dimension table for data quality metrics"""
        query = """
        SELECT DISTINCT
            table_name,
            schema_name,
            table_type,
            source_system,
            business_owner,
            technical_owner,
            criticality_level,
            sla_hours
        FROM table_metadata
        """
        
        return pd.read_sql(query, self.engine)
    
    def create_time_dimension(self):
        """Create time dimension table"""
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now() + timedelta(days=30)
        
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        time_dim = pd.DataFrame({
            'date': date_range,
            'year': date_range.year,
            'quarter': date_range.quarter,
            'month': date_range.month,
            'month_name': date_range.month_name(),
            'day': date_range.day,
            'day_of_week': date_range.dayofweek + 1,
            'day_name': date_range.day_name(),
            'week_of_year': date_range.isocalendar().week,
            'is_weekend': date_range.dayofweek >= 5,
            'is_month_end': date_range == date_range + pd.offsets.MonthEnd(0),
            'is_quarter_end': date_range == date_range + pd.offsets.QuarterEnd(0)
        })
        
        return time_dim
    
    def export_to_powerbi_format(self, output_path="powerbi_data/"):
        """Export all tables in Power BI friendly format"""
        import os
        os.makedirs(output_path, exist_ok=True)
        
        # Export fact table
        fact_table = self.create_pipeline_fact_table()
        fact_table.to_csv(f"{output_path}pipeline_executions_fact.csv", index=False)
        
        # Export dimensions
        quality_dim = self.create_data_quality_dimension()
        quality_dim.to_csv(f"{output_path}table_metadata_dim.csv", index=False)
        
        time_dim = self.create_time_dimension()
        time_dim.to_csv(f"{output_path}time_dimension.csv", index=False)
        
        print(f"Data exported to {output_path}")
        return {
            'fact_table_rows': len(fact_table),
            'quality_dim_rows': len(quality_dim),
            'time_dim_rows': len(time_dim)
        }

# Power BI REST API integration
class PowerBIAPI:
    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Power BI API"""
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
        else:
            raise Exception(f"Authentication failed: {response.text}")
    
    def refresh_dataset(self, workspace_id, dataset_id):
        """Trigger dataset refresh"""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "notifyOption": "MailOnCompletion"
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 202:
            return response.json()
        else:
            raise Exception(f"Dataset refresh failed: {response.text}")
    
    def get_refresh_status(self, workspace_id, dataset_id, refresh_id):
        """Check refresh status"""
        url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes/{refresh_id}"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get refresh status: {response.text}")

# Usage example
if __name__ == "__main__":
    # Prepare data for Power BI
    connection_string = "postgresql://user:password@localhost:5432/datawarehouse"
    data_prep = PowerBIDataPrep(connection_string)
    
    # Export data
    export_stats = data_prep.export_to_powerbi_format()
    print(f"Exported {export_stats}")
    
    # Refresh Power BI dataset (optional)
    # powerbi_api = PowerBIAPI(tenant_id, client_id, client_secret)
    # refresh_result = powerbi_api.refresh_dataset(workspace_id, dataset_id)
    # print(f"Dataset refresh initiated: {refresh_result}")
```

### **Power BI DAX Measures**
```dax
-- Key Performance Indicators

-- Pipeline Success Rate
Pipeline Success Rate = 
DIVIDE(
    CALCULATE(COUNT(PipelineExecutions[execution_id]), PipelineExecutions[status] = "success"),
    COUNT(PipelineExecutions[execution_id])
)

-- Average Pipeline Duration
Avg Pipeline Duration = 
AVERAGE(PipelineExecutions[duration_seconds])

-- Data Quality Score Trend
Data Quality Trend = 
VAR CurrentScore = AVERAGE(PipelineExecutions[data_quality_score])
VAR PreviousScore = 
    CALCULATE(
        AVERAGE(PipelineExecutions[data_quality_score]),
        DATEADD(TimeDimension[date], -7, DAY)
    )
RETURN
    CurrentScore - PreviousScore

-- Records Processed per Hour
Records per Hour = 
SUMX(
    PipelineExecutions,
    PipelineExecutions[records_processed] / (PipelineExecutions[duration_seconds] / 3600)
)

-- Pipeline Efficiency Score
Pipeline Efficiency = 
VAR AvgRecordsPerSecond = AVERAGE(PipelineExecutions[records_per_second])
VAR MaxRecordsPerSecond = MAX(PipelineExecutions[records_per_second])
RETURN
    DIVIDE(AvgRecordsPerSecond, MaxRecordsPerSecond) * 100

-- Data Freshness Score
Data Freshness = 
VAR HoursSinceLastRun = 
    DATEDIFF(
        MAX(PipelineExecutions[end_time]),
        NOW(),
        HOUR
    )
RETURN
    SWITCH(
        TRUE(),
        HoursSinceLastRun <= 1, 100,
        HoursSinceLastRun <= 6, 80,
        HoursSinceLastRun <= 24, 60,
        40
    )

-- SLA Compliance
SLA Compliance = 
VAR OnTimeExecutions = 
    CALCULATE(
        COUNT(PipelineExecutions[execution_id]),
        PipelineExecutions[duration_seconds] <= TableMetadata[sla_hours] * 3600
    )
VAR TotalExecutions = COUNT(PipelineExecutions[execution_id])
RETURN
    DIVIDE(OnTimeExecutions, TotalExecutions)

-- Error Rate by Pipeline
Error Rate = 
DIVIDE(
    CALCULATE(COUNT(PipelineExecutions[execution_id]), PipelineExecutions[status] = "failed"),
    COUNT(PipelineExecutions[execution_id])
)

-- Peak Hour Performance
Peak Hour Indicator = 
IF(
    HOUR(PipelineExecutions[start_time]) >= 8 && HOUR(PipelineExecutions[start_time]) <= 18,
    "Business Hours",
    "Off Hours"
)

-- Monthly Growth Rate
Monthly Growth Rate = 
VAR CurrentMonth = SUM(PipelineExecutions[records_processed])
VAR PreviousMonth = 
    CALCULATE(
        SUM(PipelineExecutions[records_processed]),
        DATEADD(TimeDimension[date], -1, MONTH)
    )
RETURN
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth)
```

## 🔧 **Quick Setup Commands**

### **Grafana Setup with Docker**
```bash
# Create Grafana configuration
mkdir -p grafana/provisioning/{dashboards,datasources}

# Start Grafana
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -v grafana-storage:/var/lib/grafana \
  -v $(pwd)/grafana/provisioning:/etc/grafana/provisioning \
  grafana/grafana

# Access: http://localhost:3000 (admin/admin)
```

### **Streamlit Dashboard Deployment**
```bash
# Install dependencies
pip install streamlit plotly pandas psycopg2-binary

# Run dashboard
streamlit run src/streamlit_dashboard.py --server.port 8501

# Deploy to Streamlit Cloud
# 1. Push to GitHub
# 2. Connect at share.streamlit.io
# 3. Deploy from repository
```

### **Power BI Data Gateway Setup**
```powershell
# Download and install Power BI Gateway
# Configure data source connections
# Set up scheduled refresh

# PowerShell script for automated refresh
$headers = @{
    'Authorization' = "Bearer $accessToken"
    'Content-Type' = 'application/json'
}

$body = @{
    'notifyOption' = 'MailOnCompletion'
} | ConvertTo-Json

Invoke-RestMethod -Uri $refreshUrl -Method Post -Headers $headers -Body $body
```

---

*Updated: December 2024 | Focus: Production dashboards | Integration: Real-time monitoring*