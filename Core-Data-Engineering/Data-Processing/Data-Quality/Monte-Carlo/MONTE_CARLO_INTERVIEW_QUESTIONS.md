# 🎯 Monte Carlo Interview Questions

**Difficulty Levels**: 🟢 Beginner | 🟡 Intermediate | 🔴 Advanced  
**Total Questions**: 50+  
**Interview Frequency**: 30% of senior data engineering roles

---

## 🟢 Beginner Level Questions

### **Q1: What is Monte Carlo and what problem does it solve?**

**Answer:**
Monte Carlo is a data observability platform that prevents data downtime by monitoring data pipelines, detecting anomalies, and providing root cause analysis.

**Problems It Solves**:
- **Data Downtime**: Prevents business disruption from bad data
- **Manual Monitoring**: Automates data quality checks
- **Late Detection**: Identifies issues before they impact business
- **Root Cause Analysis**: Quickly identifies source of data problems
- **Impact Assessment**: Shows downstream effects of data issues

**Key Benefits**:
```
Traditional Approach: Manual checks → Late detection → Business impact
Monte Carlo Approach: Automated monitoring → Early detection → Proactive resolution
```

**Core Capabilities**:
- Automated anomaly detection using ML
- Data lineage and impact analysis
- Incident management and alerting
- Data quality metrics and SLA monitoring
- Integration with existing data stack

---

### **Q2: What are the five pillars of data observability?**

**Answer:**
Monte Carlo focuses on five key pillars of data observability:

**1. Freshness**: Is data arriving on time?
```python
# Example freshness check
def check_data_freshness(table_name, expected_interval_hours=24):
    last_update = get_last_update_time(table_name)
    current_time = datetime.now()
    
    hours_since_update = (current_time - last_update).total_seconds() / 3600
    
    return {
        "is_fresh": hours_since_update <= expected_interval_hours,
        "hours_since_update": hours_since_update,
        "status": "fresh" if hours_since_update <= expected_interval_hours else "stale"
    }
```

**2. Volume**: Is data volume within expected ranges?
```python
def check_data_volume(table_name, expected_range):
    current_count = get_table_row_count(table_name)
    min_expected, max_expected = expected_range
    
    return {
        "is_normal": min_expected <= current_count <= max_expected,
        "current_count": current_count,
        "expected_range": expected_range,
        "deviation": calculate_deviation(current_count, expected_range)
    }
```

**3. Schema**: Are schema changes breaking downstream systems?
```python
def detect_schema_changes(table_name):
    current_schema = get_current_schema(table_name)
    previous_schema = get_previous_schema(table_name)
    
    changes = {
        "added_columns": set(current_schema.keys()) - set(previous_schema.keys()),
        "removed_columns": set(previous_schema.keys()) - set(current_schema.keys()),
        "type_changes": find_type_changes(current_schema, previous_schema)
    }
    
    return changes
```

**4. Distribution**: Are data distributions normal?
```python
def check_data_distribution(table_name, column_name):
    current_stats = get_column_statistics(table_name, column_name)
    historical_stats = get_historical_statistics(table_name, column_name)
    
    return {
        "mean_deviation": abs(current_stats["mean"] - historical_stats["mean"]),
        "std_deviation": abs(current_stats["std"] - historical_stats["std"]),
        "is_anomalous": detect_statistical_anomaly(current_stats, historical_stats)
    }
```

**5. Lineage**: How does data flow through systems?
```python
def trace_data_lineage(table_name):
    return {
        "upstream_dependencies": get_upstream_tables(table_name),
        "downstream_dependencies": get_downstream_tables(table_name),
        "transformation_logic": get_transformation_queries(table_name),
        "impact_radius": calculate_impact_radius(table_name)
    }
```

---

### **Q3: How does Monte Carlo detect anomalies in data?**

**Answer:**
Monte Carlo uses machine learning algorithms to automatically detect anomalies across multiple dimensions:

**1. Statistical Anomaly Detection**:
```python
# Monte Carlo's approach to anomaly detection
class AnomalyDetector:
    def __init__(self):
        self.models = {
            "volume": "time_series_forecasting",
            "distribution": "statistical_process_control", 
            "freshness": "threshold_based",
            "null_rates": "moving_average_deviation"
        }
    
    def detect_volume_anomaly(self, table_metrics):
        # Uses time series forecasting
        historical_volumes = table_metrics["historical_row_counts"]
        current_volume = table_metrics["current_row_count"]
        
        # Predict expected volume based on historical patterns
        expected_volume = self.forecast_expected_volume(historical_volumes)
        confidence_interval = self.calculate_confidence_interval(historical_volumes)
        
        is_anomaly = not (
            confidence_interval["lower"] <= current_volume <= confidence_interval["upper"]
        )
        
        return {
            "is_anomaly": is_anomaly,
            "current_volume": current_volume,
            "expected_volume": expected_volume,
            "confidence_interval": confidence_interval,
            "severity": self.calculate_severity(current_volume, expected_volume)
        }
```

**2. Machine Learning Models Used**:
- **Time Series Forecasting**: For volume and freshness patterns
- **Statistical Process Control**: For distribution changes
- **Isolation Forest**: For multivariate anomaly detection
- **Seasonal Decomposition**: For handling periodic patterns

**3. Anomaly Types Detected**:
```python
anomaly_types = {
    "volume_spike": "Sudden increase in row count",
    "volume_drop": "Sudden decrease in row count", 
    "freshness_delay": "Data arriving later than expected",
    "schema_break": "Breaking schema changes",
    "null_rate_spike": "Increase in null values",
    "distribution_shift": "Statistical distribution changes",
    "duplicate_increase": "Higher than normal duplicate rates"
}
```

---

### **Q4: What is data lineage and why is it important?**

**Answer:**
Data lineage is the tracking of data flow from source to destination, showing how data moves and transforms through systems.

**Components of Data Lineage**:
```python
class DataLineage:
    def __init__(self, table_name):
        self.table_name = table_name
        self.lineage_map = self.build_lineage_map()
    
    def build_lineage_map(self):
        return {
            "upstream_sources": self.get_upstream_sources(),
            "transformations": self.get_transformations(),
            "downstream_consumers": self.get_downstream_consumers(),
            "dependencies": self.get_dependencies()
        }
    
    def get_upstream_sources(self):
        # Tables that feed into this table
        return [
            {"table": "raw_orders", "type": "source"},
            {"table": "customer_dim", "type": "dimension"},
            {"table": "product_catalog", "type": "reference"}
        ]
    
    def get_downstream_consumers(self):
        # Tables/systems that consume this table
        return [
            {"table": "daily_sales_report", "type": "report"},
            {"dashboard": "executive_dashboard", "type": "visualization"},
            {"api": "customer_api", "type": "service"}
        ]
```

**Why Lineage is Important**:

**1. Impact Analysis**:
```python
def assess_incident_impact(failed_table):
    lineage = DataLineage(failed_table)
    downstream_tables = lineage.get_downstream_consumers()
    
    impact_assessment = {
        "directly_affected": len(downstream_tables),
        "business_critical_affected": len([
            t for t in downstream_tables 
            if t.get("criticality") == "high"
        ]),
        "estimated_users_affected": sum(
            t.get("user_count", 0) for t in downstream_tables
        )
    }
    
    return impact_assessment
```

**2. Root Cause Analysis**:
```python
def find_root_cause(problematic_table):
    lineage = DataLineage(problematic_table)
    upstream_tables = lineage.get_upstream_sources()
    
    # Check each upstream table for issues
    for upstream_table in upstream_tables:
        health_status = check_table_health(upstream_table["table"])
        if not health_status["healthy"]:
            return {
                "root_cause_table": upstream_table["table"],
                "issue_type": health_status["issues"],
                "propagation_path": trace_propagation_path(
                    upstream_table["table"], 
                    problematic_table
                )
            }
```

**3. Change Impact Planning**:
```python
def plan_schema_change_impact(table_name, proposed_changes):
    lineage = DataLineage(table_name)
    
    impact_plan = {
        "breaking_changes": [],
        "affected_downstream": [],
        "required_updates": []
    }
    
    for change in proposed_changes:
        if change["type"] == "column_removal":
            # Find downstream queries using this column
            affected_queries = find_queries_using_column(
                table_name, 
                change["column_name"]
            )
            impact_plan["breaking_changes"].extend(affected_queries)
    
    return impact_plan
```

---

### **Q5: How do you set up monitoring for a new data table?**

**Answer:**
Setting up monitoring involves configuring monitors for each observability pillar:

**1. Basic Table Monitoring Setup**:
```python
def setup_table_monitoring(table_config):
    """Set up comprehensive monitoring for a new table"""
    
    monitors = []
    
    # Freshness monitor
    if table_config.get("has_timestamp_column"):
        freshness_monitor = {
            "type": "freshness",
            "table": table_config["table_name"],
            "timestamp_column": table_config["timestamp_column"],
            "expected_interval": table_config.get("update_frequency", "24h"),
            "alert_threshold": table_config.get("freshness_threshold", "2h")
        }
        monitors.append(freshness_monitor)
    
    # Volume monitor
    volume_monitor = {
        "type": "volume",
        "table": table_config["table_name"],
        "training_period": "30d",  # Use 30 days to learn patterns
        "sensitivity": table_config.get("volume_sensitivity", "medium"),
        "min_threshold": table_config.get("min_rows", 0)
    }
    monitors.append(volume_monitor)
    
    # Schema monitor (always enabled)
    schema_monitor = {
        "type": "schema",
        "table": table_config["table_name"],
        "alert_on": ["column_addition", "column_removal", "type_change"],
        "ignore_columns": table_config.get("ignore_schema_changes", [])
    }
    monitors.append(schema_monitor)
    
    return monitors

# Example usage
table_config = {
    "table_name": "sales_transactions",
    "timestamp_column": "created_at",
    "update_frequency": "1h",
    "freshness_threshold": "30m",
    "volume_sensitivity": "high",
    "min_rows": 100,
    "business_criticality": "high"
}

monitors = setup_table_monitoring(table_config)
```

**2. Custom Business Logic Monitors**:
```python
def create_custom_business_monitor():
    """Create monitor for business-specific logic"""
    
    custom_monitor = {
        "name": "Daily Revenue Check",
        "type": "custom_sql",
        "query": """
            SELECT 
                DATE(created_at) as date,
                SUM(amount) as daily_revenue
            FROM sales_transactions 
            WHERE created_at >= CURRENT_DATE - 7
            GROUP BY DATE(created_at)
            ORDER BY date DESC
            LIMIT 1
        """,
        "validation_rules": [
            {
                "rule": "daily_revenue > 10000",
                "severity": "high",
                "message": "Daily revenue below $10K threshold"
            },
            {
                "rule": "daily_revenue < 1000000", 
                "severity": "medium",
                "message": "Daily revenue unusually high"
            }
        ],
        "schedule": "0 9 * * *"  # Run daily at 9 AM
    }
    
    return custom_monitor
```

**3. Alert Configuration**:
```python
def configure_alerting(table_name, business_criticality):
    """Configure alerting based on table criticality"""
    
    if business_criticality == "critical":
        alert_config = {
            "channels": ["pagerduty", "slack", "email"],
            "escalation_policy": "immediate",
            "sla_minutes": 15
        }
    elif business_criticality == "high":
        alert_config = {
            "channels": ["slack", "email"],
            "escalation_policy": "business_hours",
            "sla_minutes": 60
        }
    else:
        alert_config = {
            "channels": ["email"],
            "escalation_policy": "next_business_day",
            "sla_minutes": 480
        }
    
    return alert_config
```

---

## 🟡 Intermediate Level Questions

### **Q6: How do you implement custom anomaly detection rules?**

**Answer:**
Custom anomaly detection allows you to implement business-specific logic beyond Monte Carlo's built-in ML models:

**1. SQL-Based Custom Rules**:
```python
class CustomAnomalyDetector:
    def __init__(self, monte_carlo_client):
        self.mc_client = monte_carlo_client
    
    def create_revenue_anomaly_detector(self):
        """Detect anomalies in daily revenue patterns"""
        
        custom_rule = {
            "name": "Daily Revenue Anomaly Detection",
            "description": "Detect unusual patterns in daily revenue",
            "query": """
                WITH daily_revenue AS (
                    SELECT 
                        DATE(created_at) as date,
                        SUM(amount) as revenue,
                        COUNT(*) as transaction_count
                    FROM sales_transactions 
                    WHERE created_at >= CURRENT_DATE - 90
                    GROUP BY DATE(created_at)
                ),
                revenue_stats AS (
                    SELECT 
                        AVG(revenue) as avg_revenue,
                        STDDEV(revenue) as stddev_revenue,
                        AVG(transaction_count) as avg_transactions
                    FROM daily_revenue
                    WHERE date < CURRENT_DATE  -- Exclude today
                )
                SELECT 
                    dr.date,
                    dr.revenue,
                    dr.transaction_count,
                    rs.avg_revenue,
                    rs.stddev_revenue,
                    ABS(dr.revenue - rs.avg_revenue) / rs.stddev_revenue as z_score,
                    CASE 
                        WHEN ABS(dr.revenue - rs.avg_revenue) / rs.stddev_revenue > 3 
                        THEN 'ANOMALY'
                        WHEN ABS(dr.revenue - rs.avg_revenue) / rs.stddev_revenue > 2 
                        THEN 'WARNING'
                        ELSE 'NORMAL'
                    END as status
                FROM daily_revenue dr
                CROSS JOIN revenue_stats rs
                WHERE dr.date = CURRENT_DATE
            """,
            "anomaly_conditions": [
                {
                    "condition": "status = 'ANOMALY'",
                    "severity": "high",
                    "message": "Daily revenue is more than 3 standard deviations from normal"
                },
                {
                    "condition": "status = 'WARNING'",
                    "severity": "medium", 
                    "message": "Daily revenue is 2-3 standard deviations from normal"
                }
            ],
            "schedule": "0 10 * * *"  # Run daily at 10 AM
        }
        
        return self.mc_client.create_custom_monitor(custom_rule)
```

**2. Multi-Table Correlation Rules**:
```python
def create_correlation_anomaly_detector():
    """Detect anomalies across related tables"""
    
    correlation_rule = {
        "name": "Orders-Inventory Correlation Check",
        "description": "Ensure orders and inventory updates are correlated",
        "query": """
            WITH daily_metrics AS (
                SELECT 
                    DATE(o.created_at) as date,
                    COUNT(o.id) as order_count,
                    COUNT(i.id) as inventory_updates
                FROM orders o
                FULL OUTER JOIN inventory_updates i 
                    ON DATE(o.created_at) = DATE(i.updated_at)
                WHERE DATE(o.created_at) >= CURRENT_DATE - 7
                GROUP BY DATE(o.created_at)
            )
            SELECT 
                date,
                order_count,
                inventory_updates,
                CASE 
                    WHEN order_count > 0 AND inventory_updates = 0 
                    THEN 'MISSING_INVENTORY_UPDATES'
                    WHEN inventory_updates > order_count * 1.5 
                    THEN 'EXCESSIVE_INVENTORY_UPDATES'
                    ELSE 'NORMAL'
                END as correlation_status
            FROM daily_metrics
            WHERE date = CURRENT_DATE
        """,
        "anomaly_conditions": [
            {
                "condition": "correlation_status != 'NORMAL'",
                "severity": "medium",
                "message": "Orders and inventory updates are not properly correlated"
            }
        ]
    }
    
    return correlation_rule
```

**3. Time-Series Pattern Detection**:
```python
def create_seasonal_pattern_detector():
    """Detect deviations from seasonal patterns"""
    
    seasonal_rule = {
        "name": "Seasonal Pattern Anomaly Detection",
        "description": "Detect deviations from expected seasonal patterns",
        "query": """
            WITH historical_patterns AS (
                SELECT 
                    EXTRACT(DOW FROM created_at) as day_of_week,
                    EXTRACT(HOUR FROM created_at) as hour_of_day,
                    AVG(COUNT(*)) OVER (
                        PARTITION BY EXTRACT(DOW FROM created_at), 
                                   EXTRACT(HOUR FROM created_at)
                    ) as expected_count,
                    STDDEV(COUNT(*)) OVER (
                        PARTITION BY EXTRACT(DOW FROM created_at), 
                                   EXTRACT(HOUR FROM created_at)
                    ) as stddev_count
                FROM user_events 
                WHERE created_at >= CURRENT_DATE - 30
                  AND created_at < CURRENT_DATE
                GROUP BY 
                    DATE(created_at),
                    EXTRACT(DOW FROM created_at),
                    EXTRACT(HOUR FROM created_at)
            ),
            current_hour_data AS (
                SELECT 
                    EXTRACT(DOW FROM CURRENT_TIMESTAMP) as current_dow,
                    EXTRACT(HOUR FROM CURRENT_TIMESTAMP) as current_hour,
                    COUNT(*) as current_count
                FROM user_events 
                WHERE created_at >= DATE_TRUNC('hour', CURRENT_TIMESTAMP)
                  AND created_at < DATE_TRUNC('hour', CURRENT_TIMESTAMP) + INTERVAL '1 hour'
            )
            SELECT 
                chd.current_count,
                hp.expected_count,
                hp.stddev_count,
                ABS(chd.current_count - hp.expected_count) / hp.stddev_count as deviation_score,
                CASE 
                    WHEN ABS(chd.current_count - hp.expected_count) / hp.stddev_count > 2.5
                    THEN 'SEASONAL_ANOMALY'
                    ELSE 'NORMAL'
                END as pattern_status
            FROM current_hour_data chd
            JOIN historical_patterns hp 
                ON chd.current_dow = hp.day_of_week 
                AND chd.current_hour = hp.hour_of_day
        """,
        "schedule": "0 * * * *"  # Run hourly
    }
    
    return seasonal_rule
```

---

### **Q7: How do you handle false positives in anomaly detection?**

**Answer:**
False positives are common in anomaly detection. Here's how to minimize and handle them:

**1. Threshold Tuning**:
```python
class FalsePositiveReducer:
    def __init__(self):
        self.sensitivity_levels = {
            "low": {"z_score_threshold": 3.5, "confidence": 0.99},
            "medium": {"z_score_threshold": 2.5, "confidence": 0.95},
            "high": {"z_score_threshold": 1.5, "confidence": 0.85}
        }
    
    def tune_anomaly_thresholds(self, table_name, historical_alerts):
        """Tune thresholds based on historical false positive rate"""
        
        false_positive_rate = self.calculate_false_positive_rate(historical_alerts)
        
        if false_positive_rate > 0.3:  # More than 30% false positives
            # Reduce sensitivity
            new_sensitivity = "low"
            recommendation = "Increase thresholds to reduce false positives"
        elif false_positive_rate < 0.05:  # Less than 5% false positives
            # Can increase sensitivity
            new_sensitivity = "high" 
            recommendation = "Can increase sensitivity to catch more issues"
        else:
            new_sensitivity = "medium"
            recommendation = "Current thresholds are well-tuned"
        
        return {
            "recommended_sensitivity": new_sensitivity,
            "current_false_positive_rate": false_positive_rate,
            "recommendation": recommendation,
            "new_thresholds": self.sensitivity_levels[new_sensitivity]
        }
```

**2. Context-Aware Filtering**:
```python
def apply_contextual_filters(anomaly_alert, context_data):
    """Filter anomalies based on business context"""
    
    filters = []
    
    # Holiday filter
    if context_data.get("is_holiday"):
        if anomaly_alert["type"] == "volume_drop":
            filters.append({
                "filter": "holiday_volume_drop",
                "action": "suppress",
                "reason": "Expected volume drop during holidays"
            })
    
    # Maintenance window filter
    if context_data.get("maintenance_window"):
        if anomaly_alert["severity"] in ["low", "medium"]:
            filters.append({
                "filter": "maintenance_window",
                "action": "suppress",
                "reason": "System maintenance in progress"
            })
    
    # Business hours filter
    current_hour = datetime.now().hour
    if not (9 <= current_hour <= 17):  # Outside business hours
        if anomaly_alert["type"] == "freshness_delay":
            filters.append({
                "filter": "after_hours_processing",
                "action": "reduce_severity",
                "reason": "ETL processes run after business hours"
            })
    
    return filters

def smart_alert_processor(anomaly_alert):
    """Process alerts with contextual intelligence"""
    
    context_data = get_business_context()
    filters = apply_contextual_filters(anomaly_alert, context_data)
    
    for filter_rule in filters:
        if filter_rule["action"] == "suppress":
            return {
                "action": "suppress",
                "reason": filter_rule["reason"],
                "original_alert": anomaly_alert
            }
        elif filter_rule["action"] == "reduce_severity":
            anomaly_alert["severity"] = reduce_severity(anomaly_alert["severity"])
    
    return {
        "action": "send",
        "modified_alert": anomaly_alert,
        "applied_filters": filters
    }
```

**3. Machine Learning for False Positive Reduction**:
```python
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class FalsePositiveMLFilter:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
    
    def train_false_positive_model(self, historical_alerts):
        """Train ML model to predict false positives"""
        
        # Feature engineering
        features = []
        labels = []
        
        for alert in historical_alerts:
            feature_vector = self.extract_features(alert)
            features.append(feature_vector)
            labels.append(1 if alert["was_false_positive"] else 0)
        
        X = pd.DataFrame(features)
        y = pd.Series(labels)
        
        self.model.fit(X, y)
        self.is_trained = True
        
        return {
            "training_accuracy": self.model.score(X, y),
            "feature_importance": dict(zip(X.columns, self.model.feature_importances_))
        }
    
    def extract_features(self, alert):
        """Extract features for false positive prediction"""
        
        return {
            "anomaly_severity": self.encode_severity(alert["severity"]),
            "time_of_day": datetime.fromisoformat(alert["timestamp"]).hour,
            "day_of_week": datetime.fromisoformat(alert["timestamp"]).weekday(),
            "table_criticality": self.encode_criticality(alert["table_criticality"]),
            "anomaly_type": self.encode_anomaly_type(alert["anomaly_type"]),
            "deviation_magnitude": alert.get("deviation_magnitude", 0),
            "historical_alert_frequency": alert.get("historical_frequency", 0)
        }
    
    def predict_false_positive_probability(self, new_alert):
        """Predict probability that alert is false positive"""
        
        if not self.is_trained:
            return 0.5  # Default uncertainty
        
        features = self.extract_features(new_alert)
        feature_df = pd.DataFrame([features])
        
        false_positive_probability = self.model.predict_proba(feature_df)[0][1]
        
        return {
            "false_positive_probability": false_positive_probability,
            "confidence": "high" if abs(false_positive_probability - 0.5) > 0.3 else "low",
            "recommendation": self.get_recommendation(false_positive_probability)
        }
    
    def get_recommendation(self, fp_probability):
        if fp_probability > 0.8:
            return "suppress_alert"
        elif fp_probability > 0.6:
            return "reduce_priority"
        elif fp_probability < 0.2:
            return "high_confidence_alert"
        else:
            return "normal_processing"
```

---

### **Q8: How do you implement data quality SLAs with Monte Carlo?**

**Answer:**
Data quality SLAs define measurable commitments for data reliability and availability:

**1. SLA Definition Framework**:
```python
class DataQualitySLA:
    def __init__(self):
        self.sla_tiers = {
            "tier_1_critical": {
                "availability": 99.9,  # 99.9% uptime
                "freshness_sla": 30,   # 30 minutes max delay
                "quality_score": 95,   # 95% quality score
                "mttr_minutes": 15     # 15 minutes mean time to resolution
            },
            "tier_2_important": {
                "availability": 99.5,
                "freshness_sla": 120,  # 2 hours max delay
                "quality_score": 90,
                "mttr_minutes": 60
            },
            "tier_3_standard": {
                "availability": 99.0,
                "freshness_sla": 480,  # 8 hours max delay
                "quality_score": 85,
                "mttr_minutes": 240
            }
        }
    
    def define_table_sla(self, table_name, business_criticality, custom_requirements=None):
        """Define SLA for a specific table"""
        
        base_sla = self.sla_tiers[f"tier_{business_criticality}"]
        
        if custom_requirements:
            base_sla.update(custom_requirements)
        
        table_sla = {
            "table_name": table_name,
            "tier": business_criticality,
            "sla_requirements": base_sla,
            "measurement_period": "monthly",
            "penalty_clauses": self.define_penalty_clauses(base_sla),
            "monitoring_config": self.create_monitoring_config(base_sla)
        }
        
        return table_sla
```

**2. SLA Monitoring Implementation**:
```python
class SLAMonitor:
    def __init__(self, monte_carlo_client):
        self.mc_client = monte_carlo_client
        self.sla_tracker = {}
    
    def track_sla_compliance(self, table_name, sla_config):
        """Track SLA compliance metrics"""
        
        current_period = self.get_current_measurement_period()
        
        compliance_metrics = {
            "availability_compliance": self.calculate_availability_compliance(
                table_name, current_period
            ),
            "freshness_compliance": self.calculate_freshness_compliance(
                table_name, sla_config["sla_requirements"]["freshness_sla"]
            ),
            "quality_compliance": self.calculate_quality_compliance(
                table_name, sla_config["sla_requirements"]["quality_score"]
            ),
            "mttr_compliance": self.calculate_mttr_compliance(
                table_name, sla_config["sla_requirements"]["mttr_minutes"]
            )
        }
        
        overall_compliance = self.calculate_overall_compliance(compliance_metrics)
        
        return {
            "table_name": table_name,
            "measurement_period": current_period,
            "compliance_metrics": compliance_metrics,
            "overall_compliance": overall_compliance,
            "sla_status": "met" if overall_compliance >= 95 else "breached"
        }
    
    def calculate_availability_compliance(self, table_name, period):
        """Calculate data availability percentage"""
        
        incidents = self.get_incidents_for_period(table_name, period)
        total_minutes = period["total_minutes"]
        downtime_minutes = sum(incident["duration_minutes"] for incident in incidents)
        
        availability_percentage = ((total_minutes - downtime_minutes) / total_minutes) * 100
        
        return {
            "availability_percentage": availability_percentage,
            "total_incidents": len(incidents),
            "total_downtime_minutes": downtime_minutes,
            "target_availability": 99.9
        }
    
    def calculate_freshness_compliance(self, table_name, freshness_sla_minutes):
        """Calculate freshness SLA compliance"""
        
        freshness_violations = self.get_freshness_violations(table_name)
        total_updates = self.get_total_updates(table_name)
        
        compliance_rate = ((total_updates - len(freshness_violations)) / total_updates) * 100
        
        return {
            "compliance_rate": compliance_rate,
            "violations": len(freshness_violations),
            "total_updates": total_updates,
            "target_freshness_minutes": freshness_sla_minutes
        }
```

**3. SLA Reporting and Alerting**:
```python
def generate_sla_report(table_slas, reporting_period):
    """Generate comprehensive SLA compliance report"""
    
    report = {
        "reporting_period": reporting_period,
        "summary": {
            "total_tables": len(table_slas),
            "sla_met": 0,
            "sla_breached": 0,
            "at_risk": 0
        },
        "table_details": [],
        "recommendations": []
    }
    
    for table_sla in table_slas:
        compliance = track_sla_compliance(
            table_sla["table_name"], 
            table_sla
        )
        
        report["table_details"].append(compliance)
        
        # Update summary
        if compliance["sla_status"] == "met":
            report["summary"]["sla_met"] += 1
        else:
            report["summary"]["sla_breached"] += 1
        
        # Generate recommendations
        if compliance["overall_compliance"] < 90:
            report["recommendations"].append({
                "table": table_sla["table_name"],
                "issue": "Low SLA compliance",
                "recommendation": generate_improvement_recommendation(compliance)
            })
    
    return report

def setup_sla_alerting(table_sla):
    """Set up proactive SLA alerting"""
    
    alert_rules = []
    
    # Availability alert
    alert_rules.append({
        "name": f"{table_sla['table_name']}_availability_alert",
        "condition": "availability_percentage < target_availability",
        "severity": "high",
        "notification_channels": ["pagerduty", "slack"],
        "message": f"Table {table_sla['table_name']} availability below SLA threshold"
    })
    
    # Freshness alert
    alert_rules.append({
        "name": f"{table_sla['table_name']}_freshness_alert", 
        "condition": f"data_delay_minutes > {table_sla['sla_requirements']['freshness_sla']}",
        "severity": "medium",
        "notification_channels": ["slack", "email"],
        "message": f"Table {table_sla['table_name']} freshness SLA breached"
    })
    
    return alert_rules
```

This comprehensive SLA framework ensures data quality commitments are measurable, monitored, and maintained.

---

## 🔴 Advanced Level Questions

### **Q9: How would you design a multi-tenant data observability architecture?**

**Answer:**
Multi-tenant data observability requires isolation, scalability, and customization per tenant:

**1. Tenant Isolation Architecture**:
```python
class MultiTenantObservabilityPlatform:
    def __init__(self):
        self.tenant_configs = {}
        self.isolation_strategy = "schema_based"  # or "database_based"
        
    def setup_tenant_observability(self, tenant_id, tenant_config):
        """Set up observability for a new tenant"""
        
        tenant_setup = {
            "tenant_id": tenant_id,
            "isolation_config": self.create_isolation_config(tenant_id),
            "monitoring_config": self.create_tenant_monitoring_config(tenant_config),
            "alerting_config": self.create_tenant_alerting_config(tenant_config),
            "sla_config": self.create_tenant_sla_config(tenant_config),
            "access_controls": self.create_tenant_access_controls(tenant_id)
        }
        
        self.tenant_configs[tenant_id] = tenant_setup
        return tenant_setup
    
    def create_isolation_config(self, tenant_id):
        """Create data isolation configuration"""
        
        if self.isolation_strategy == "schema_based":
            return {
                "type": "schema_isolation",
                "metadata_schema": f"observability_tenant_{tenant_id}",
                "metrics_schema": f"metrics_tenant_{tenant_id}",
                "alerts_schema": f"alerts_tenant_{tenant_id}"
            }
        elif self.isolation_strategy == "database_based":
            return {
                "type": "database_isolation", 
                "metadata_database": f"obs_metadata_{tenant_id}",
                "metrics_database": f"obs_metrics_{tenant_id}",
                "alerts_database": f"obs_alerts_{tenant_id}"
            }
    
    def create_tenant_monitoring_config(self, tenant_config):
        """Create tenant-specific monitoring configuration"""
        
        monitoring_config = {
            "data_sources": tenant_config["data_sources"],
            "custom_monitors": [],
            "anomaly_detection_settings": {
                "sensitivity": tenant_config.get("anomaly_sensitivity", "medium"),
                "training_period_days": tenant_config.get("training_period", 30),
                "custom_algorithms": tenant_config.get("custom_algorithms", [])
            },
            "lineage_tracking": {
                "enabled": tenant_config.get("lineage_enabled", True),
                "depth_limit": tenant_config.get("lineage_depth", 5),
                "cross_system_tracking": tenant_config.get("cross_system_lineage", False)
            }
        }
        
        # Add tenant-specific custom monitors
        for monitor_config in tenant_config.get("custom_monitors", []):
            custom_monitor = self.create_custom_monitor(monitor_config, tenant_config["tenant_id"])
            monitoring_config["custom_monitors"].append(custom_monitor)
        
        return monitoring_config
```

**2. Tenant-Specific Customization**:
```python
class TenantCustomizationEngine:
    def __init__(self):
        self.customization_templates = {
            "financial_services": self.get_finserv_template(),
            "healthcare": self.get_healthcare_template(),
            "ecommerce": self.get_ecommerce_template(),
            "saas": self.get_saas_template()
        }
    
    def get_finserv_template(self):
        """Financial services specific observability template"""
        return {
            "required_monitors": [
                "regulatory_reporting_freshness",
                "transaction_volume_anomalies", 
                "data_lineage_compliance",
                "pii_detection"
            ],
            "sla_requirements": {
                "availability": 99.95,
                "freshness_minutes": 15,
                "quality_score": 98
            },
            "compliance_checks": [
                "sox_compliance",
                "gdpr_compliance", 
                "pci_compliance"
            ],
            "alert_escalation": {
                "critical_incidents": "immediate_pagerduty",
                "compliance_violations": "regulatory_team_notification"
            }
        }
    
    def customize_for_tenant(self, tenant_id, industry, custom_requirements):
        """Apply industry template and custom requirements"""
        
        base_template = self.customization_templates.get(industry, {})
        
        # Merge custom requirements with industry template
        tenant_config = self.deep_merge(base_template, custom_requirements)
        
        # Add tenant-specific customizations
        tenant_config["tenant_id"] = tenant_id
        tenant_config["custom_dashboards"] = self.create_custom_dashboards(
            tenant_id, tenant_config
        )
        tenant_config["custom_metrics"] = self.create_custom_metrics(
            tenant_id, tenant_config
        )
        
        return tenant_config
```

**3. Resource Allocation and Scaling**:
```python
class TenantResourceManager:
    def __init__(self):
        self.resource_pools = {
            "compute": {"total": 1000, "allocated": 0},
            "storage": {"total": 10000, "allocated": 0},  # GB
            "api_calls": {"total": 1000000, "allocated": 0}  # per month
        }
        self.tenant_allocations = {}
    
    def allocate_resources(self, tenant_id, tier, custom_limits=None):
        """Allocate resources based on tenant tier"""
        
        tier_allocations = {
            "enterprise": {
                "compute_units": 200,
                "storage_gb": 2000,
                "api_calls_monthly": 200000,
                "concurrent_monitors": 500
            },
            "professional": {
                "compute_units": 50,
                "storage_gb": 500,
                "api_calls_monthly": 50000,
                "concurrent_monitors": 100
            },
            "starter": {
                "compute_units": 10,
                "storage_gb": 100,
                "api_calls_monthly": 10000,
                "concurrent_monitors": 20
            }
        }
        
        allocation = tier_allocations[tier].copy()
        
        if custom_limits:
            allocation.update(custom_limits)
        
        # Check if resources are available
        if self.can_allocate_resources(allocation):
            self.tenant_allocations[tenant_id] = allocation
            self.update_resource_pools(allocation, "allocate")
            return allocation
        else:
            raise ResourceAllocationError("Insufficient resources available")
    
    def monitor_tenant_usage(self, tenant_id):
        """Monitor tenant resource usage and enforce limits"""
        
        current_usage = self.get_tenant_usage(tenant_id)
        allocated_limits = self.tenant_allocations[tenant_id]
        
        usage_report = {}
        for resource, limit in allocated_limits.items():
            usage_percentage = (current_usage[resource] / limit) * 100
            usage_report[resource] = {
                "current_usage": current_usage[resource],
                "limit": limit,
                "usage_percentage": usage_percentage,
                "status": self.get_usage_status(usage_percentage)
            }
        
        # Trigger alerts for high usage
        for resource, usage_info in usage_report.items():
            if usage_info["usage_percentage"] > 90:
                self.trigger_resource_alert(tenant_id, resource, usage_info)
        
        return usage_report
```

**4. Cross-Tenant Analytics and Insights**:
```python
class CrossTenantAnalytics:
    def __init__(self):
        self.analytics_engine = TenantAnalyticsEngine()
    
    def generate_platform_insights(self):
        """Generate insights across all tenants while maintaining privacy"""
        
        aggregated_metrics = {
            "total_tables_monitored": 0,
            "total_incidents_detected": 0,
            "average_resolution_time": 0,
            "common_anomaly_patterns": [],
            "industry_benchmarks": {}
        }
        
        # Aggregate metrics across tenants (anonymized)
        for tenant_id in self.get_active_tenants():
            tenant_metrics = self.get_anonymized_tenant_metrics(tenant_id)
            
            aggregated_metrics["total_tables_monitored"] += tenant_metrics["table_count"]
            aggregated_metrics["total_incidents_detected"] += tenant_metrics["incident_count"]
            
            # Industry benchmarking (anonymized)
            industry = self.get_tenant_industry(tenant_id)
            if industry not in aggregated_metrics["industry_benchmarks"]:
                aggregated_metrics["industry_benchmarks"][industry] = {
                    "avg_health_score": [],
                    "common_issues": [],
                    "resolution_times": []
                }
            
            aggregated_metrics["industry_benchmarks"][industry]["avg_health_score"].append(
                tenant_metrics["avg_health_score"]
            )
        
        # Generate insights and recommendations
        platform_insights = {
            "platform_health": self.calculate_platform_health(aggregated_metrics),
            "improvement_opportunities": self.identify_improvement_opportunities(aggregated_metrics),
            "industry_benchmarks": self.calculate_industry_benchmarks(aggregated_metrics["industry_benchmarks"]),
            "feature_usage_patterns": self.analyze_feature_usage_patterns()
        }
        
        return platform_insights
```

This multi-tenant architecture provides scalable, secure, and customizable data observability while maintaining tenant isolation and enabling platform-wide insights.

---

### **Q10: How do you implement real-time data quality scoring at scale?**

**Answer:**
Real-time data quality scoring requires streaming architecture and efficient computation:

**1. Streaming Quality Score Architecture**:
```python
import asyncio
from kafka import KafkaConsumer, KafkaProducer
import json
import time
from collections import defaultdict, deque

class RealTimeQualityScorer:
    def __init__(self):
        self.kafka_consumer = KafkaConsumer(
            'data_events',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        # In-memory state for real-time calculations
        self.table_metrics = defaultdict(lambda: {
            'recent_records': deque(maxlen=10000),  # Last 10K records
            'quality_scores': deque(maxlen=1000),   # Last 1K scores
            'anomaly_detectors': {},
            'schema_tracker': {},
            'last_update': time.time()
        })
        
        self.quality_dimensions = [
            'completeness', 'uniqueness', 'validity', 
            'consistency', 'timeliness', 'accuracy'
        ]
    
    async def process_data_stream(self):
        """Process streaming data events for real-time quality scoring"""
        
        async for message in self.kafka_consumer:
            try:
                data_event = message.value
                await self.process_single_event(data_event)
            except Exception as e:
                print(f"Error processing event: {e}")
    
    async def process_single_event(self, data_event):
        """Process a single data event and update quality scores"""
        
        table_name = data_event['table_name']
        record_data = data_event['record_data']
        event_timestamp = data_event['timestamp']
        
        # Update table metrics
        table_state = self.table_metrics[table_name]
        table_state['recent_records'].append({
            'data': record_data,
            'timestamp': event_timestamp
        })
        table_state['last_update'] = time.time()
        
        # Calculate real-time quality scores
        quality_scores = await self.calculate_realtime_quality_scores(
            table_name, record_data, table_state
        )
        
        # Update rolling quality score
        table_state['quality_scores'].append({
            'timestamp': event_timestamp,
            'scores': quality_scores,
            'overall_score': sum(quality_scores.values()) / len(quality_scores)
        })
        
        # Detect anomalies in quality scores
        anomalies = await self.detect_quality_anomalies(table_name, quality_scores)
        
        # Publish quality score update
        await self.publish_quality_update(table_name, quality_scores, anomalies)
    
    async def calculate_realtime_quality_scores(self, table_name, record_data, table_state):
        """Calculate quality scores for current record"""
        
        scores = {}
        recent_records = list(table_state['recent_records'])
        
        # Completeness: Percentage of non-null values
        scores['completeness'] = self.calculate_completeness_score(record_data)
        
        # Uniqueness: Check for duplicates in recent records
        scores['uniqueness'] = self.calculate_uniqueness_score(
            record_data, recent_records
        )
        
        # Validity: Check data format and constraints
        scores['validity'] = await self.calculate_validity_score(
            table_name, record_data
        )
        
        # Consistency: Check against business rules
        scores['consistency'] = await self.calculate_consistency_score(
            table_name, record_data, recent_records
        )
        
        # Timeliness: Check data freshness
        scores['timeliness'] = self.calculate_timeliness_score(
            record_data.get('created_at', time.time())
        )
        
        # Accuracy: Check against reference data (if available)
        scores['accuracy'] = await self.calculate_accuracy_score(
            table_name, record_data
        )
        
        return scores
```

**2. Scalable Quality Computation Engine**:
```python
class ScalableQualityEngine:
    def __init__(self):
        self.computation_workers = []
        self.result_aggregator = QualityScoreAggregator()
        self.cache_manager = QualityScoreCache()
    
    async def setup_distributed_processing(self, num_workers=10):
        """Set up distributed quality score computation"""
        
        for i in range(num_workers):
            worker = QualityComputationWorker(worker_id=i)
            self.computation_workers.append(worker)
            asyncio.create_task(worker.start_processing())
    
    async def compute_quality_scores_distributed(self, data_batch):
        """Distribute quality score computation across workers"""
        
        # Partition data across workers
        batch_size = len(data_batch) // len(self.computation_workers)
        worker_tasks = []
        
        for i, worker in enumerate(self.computation_workers):
            start_idx = i * batch_size
            end_idx = start_idx + batch_size if i < len(self.computation_workers) - 1 else len(data_batch)
            
            worker_batch = data_batch[start_idx:end_idx]
            task = asyncio.create_task(
                worker.compute_batch_quality_scores(worker_batch)
            )
            worker_tasks.append(task)
        
        # Wait for all workers to complete
        worker_results = await asyncio.gather(*worker_tasks)
        
        # Aggregate results
        aggregated_scores = await self.result_aggregator.aggregate_worker_results(
            worker_results
        )
        
        return aggregated_scores

class QualityComputationWorker:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.quality_calculators = {
            'completeness': CompletenessCalculator(),
            'uniqueness': UniquenessCalculator(),
            'validity': ValidityCalculator(),
            'consistency': ConsistencyCalculator(),
            'timeliness': TimelinessCalculator(),
            'accuracy': AccuracyCalculator()
        }
    
    async def compute_batch_quality_scores(self, data_batch):
        """Compute quality scores for a batch of records"""
        
        batch_results = []
        
        for record in data_batch:
            record_scores = {}
            
            # Compute each quality dimension in parallel
            score_tasks = []
            for dimension, calculator in self.quality_calculators.items():
                task = asyncio.create_task(
                    calculator.calculate_score(record)
                )
                score_tasks.append((dimension, task))
            
            # Wait for all dimension scores
            for dimension, task in score_tasks:
                record_scores[dimension] = await task
            
            # Calculate overall score
            record_scores['overall'] = sum(record_scores.values()) / len(record_scores)
            
            batch_results.append({
                'record_id': record.get('id'),
                'table_name': record.get('table_name'),
                'scores': record_scores,
                'timestamp': time.time(),
                'worker_id': self.worker_id
            })
        
        return batch_results
```

**3. Real-time Quality Score Aggregation**:
```python
class RealTimeQualityAggregator:
    def __init__(self):
        self.time_windows = {
            '1min': 60,
            '5min': 300,
            '15min': 900,
            '1hour': 3600
        }
        self.aggregated_scores = defaultdict(lambda: defaultdict(dict))
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    async def aggregate_quality_scores(self, table_name, quality_scores):
        """Aggregate quality scores across different time windows"""
        
        current_timestamp = time.time()
        
        for window_name, window_seconds in self.time_windows.items():
            window_start = int(current_timestamp // window_seconds) * window_seconds
            
            # Get or create window aggregation
            window_key = f"{table_name}:{window_name}:{window_start}"
            
            if window_key not in self.aggregated_scores[table_name][window_name]:
                self.aggregated_scores[table_name][window_name][window_key] = {
                    'count': 0,
                    'sum_scores': defaultdict(float),
                    'min_scores': defaultdict(lambda: float('inf')),
                    'max_scores': defaultdict(lambda: float('-inf')),
                    'window_start': window_start,
                    'window_end': window_start + window_seconds
                }
            
            window_agg = self.aggregated_scores[table_name][window_name][window_key]
            
            # Update aggregations
            window_agg['count'] += 1
            
            for dimension, score in quality_scores.items():
                window_agg['sum_scores'][dimension] += score
                window_agg['min_scores'][dimension] = min(
                    window_agg['min_scores'][dimension], score
                )
                window_agg['max_scores'][dimension] = max(
                    window_agg['max_scores'][dimension], score
                )
            
            # Calculate averages
            avg_scores = {
                dimension: window_agg['sum_scores'][dimension] / window_agg['count']
                for dimension in quality_scores.keys()
            }
            
            window_agg['avg_scores'] = avg_scores
            
            # Cache in Redis for fast access
            await self.cache_aggregated_scores(window_key, window_agg)
            
            # Publish aggregated scores
            await self.publish_aggregated_scores(table_name, window_name, window_agg)
    
    async def get_realtime_quality_dashboard_data(self, table_name):
        """Get real-time quality dashboard data"""
        
        dashboard_data = {
            'table_name': table_name,
            'current_scores': {},
            'trends': {},
            'alerts': []
        }
        
        # Get current scores (1-minute window)
        current_window = await self.get_latest_window_scores(table_name, '1min')
        if current_window:
            dashboard_data['current_scores'] = current_window['avg_scores']
        
        # Get trends (compare current hour vs previous hour)
        current_hour_scores = await self.get_latest_window_scores(table_name, '1hour')
        previous_hour_scores = await self.get_previous_window_scores(table_name, '1hour')
        
        if current_hour_scores and previous_hour_scores:
            dashboard_data['trends'] = self.calculate_score_trends(
                current_hour_scores['avg_scores'],
                previous_hour_scores['avg_scores']
            )
        
        # Get active quality alerts
        dashboard_data['alerts'] = await self.get_active_quality_alerts(table_name)
        
        return dashboard_data
```

This real-time quality scoring system provides immediate feedback on data quality issues while maintaining scalability through distributed processing and efficient aggregation.

---

## 🎯 Interview Tips

### **Preparation Strategy**
1. **Understand Data Observability Concepts**: Know the five pillars and their importance
2. **Hands-on Experience**: Try Monte Carlo or similar tools (Great Expectations, Datafold)
3. **Business Impact Focus**: Understand how data quality affects business outcomes
4. **Integration Knowledge**: Know how observability fits in modern data stacks
5. **Incident Response**: Practice troubleshooting data quality issues

### **Key Points to Emphasize**
- Proactive vs reactive data quality management
- Business impact of data downtime
- Automated anomaly detection capabilities
- Data lineage for root cause analysis
- SLA-driven data quality management
- Integration with existing data infrastructure

---

**🎯 Ready for your interview?** Focus on real-world scenarios and business impact of data observability solutions.