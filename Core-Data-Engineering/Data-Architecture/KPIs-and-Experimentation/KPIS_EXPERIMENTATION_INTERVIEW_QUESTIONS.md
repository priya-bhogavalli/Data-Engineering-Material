# KPIs and Experimentation Interview Questions

## 📋 Table of Contents

1. [KPI Fundamentals (1-10)](#kpi-fundamentals-1-10)
2. [A/B Testing & Experimentation (11-20)](#ab-testing--experimentation-11-20)
3. [Advanced Analytics (21-30)](#advanced-analytics-21-30)

---

## KPI Fundamentals (1-10)

### 1. What are KPIs and how do they differ from regular metrics?
**Answer**: 
- **KPIs**: Key Performance Indicators tied to business objectives
- **Metrics**: Any measurable data points
- **Differences**:
  - KPIs are strategic, metrics are operational
  - KPIs drive decisions, metrics provide context
  - KPIs are limited in number, metrics can be numerous

### 2. How do you design a KPI framework?
**Answer**: SMART KPI framework:
```sql
-- KPI definition table
CREATE TABLE kpi_definitions (
    kpi_id VARCHAR(50) PRIMARY KEY,
    kpi_name VARCHAR(200),
    description TEXT,
    calculation_logic TEXT,
    target_value DECIMAL(10,2),
    frequency VARCHAR(20), -- daily, weekly, monthly
    owner VARCHAR(100),
    business_objective VARCHAR(500)
);

-- KPI measurements
CREATE TABLE kpi_measurements (
    measurement_id UUID PRIMARY KEY,
    kpi_id VARCHAR(50),
    measurement_date DATE,
    actual_value DECIMAL(10,2),
    target_value DECIMAL(10,2),
    variance_percentage DECIMAL(5,2)
);
```

### 3. What are leading vs lagging indicators?
**Answer**:
- **Leading**: Predict future performance (pipeline value, website traffic)
- **Lagging**: Measure past performance (revenue, customer satisfaction)
```sql
-- Leading indicator example
SELECT 
    DATE_TRUNC('week', created_date) as week,
    COUNT(*) as leads_generated,
    AVG(lead_score) as avg_lead_quality
FROM leads
GROUP BY DATE_TRUNC('week', created_date);

-- Lagging indicator example  
SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(order_amount) as monthly_revenue,
    COUNT(DISTINCT customer_id) as customers_served
FROM orders
GROUP BY DATE_TRUNC('month', order_date);
```

### 4. How do you implement KPI alerting and monitoring?
**Answer**: Automated monitoring system:
```python
class KPIMonitor:
    def __init__(self, db_connection):
        self.db = db_connection
        
    def check_kpi_thresholds(self, kpi_id):
        query = """
        SELECT actual_value, target_value, 
               (actual_value - target_value) / target_value * 100 as variance
        FROM kpi_measurements 
        WHERE kpi_id = %s 
        ORDER BY measurement_date DESC LIMIT 1
        """
        
        result = self.db.execute(query, (kpi_id,))
        variance = result['variance']
        
        if abs(variance) > 10:  # 10% threshold
            self.send_alert(kpi_id, variance)
    
    def send_alert(self, kpi_id, variance):
        alert = {
            'kpi_id': kpi_id,
            'variance': variance,
            'timestamp': datetime.now(),
            'severity': 'HIGH' if abs(variance) > 20 else 'MEDIUM'
        }
        # Send to alerting system
```

### 5. What is a KPI dashboard and how do you design one?
**Answer**: Visual representation of key metrics:
- **Hierarchy**: Strategic → Tactical → Operational
- **Real-time Updates**: Automated data refresh
- **Drill-down Capability**: From summary to detail
- **Context**: Historical trends, benchmarks, targets

## A/B Testing & Experimentation (11-20)

### 6. What is A/B testing and how do you implement it?
**Answer**: Controlled experiment comparing two versions:
```sql
-- Experiment setup
CREATE TABLE experiments (
    experiment_id VARCHAR(50) PRIMARY KEY,
    experiment_name VARCHAR(200),
    hypothesis TEXT,
    start_date DATE,
    end_date DATE,
    traffic_allocation DECIMAL(3,2), -- 0.50 for 50/50 split
    status VARCHAR(20)
);

-- User assignments
CREATE TABLE experiment_assignments (
    user_id VARCHAR(50),
    experiment_id VARCHAR(50),
    variant VARCHAR(20), -- 'control', 'treatment'
    assignment_date TIMESTAMP,
    PRIMARY KEY (user_id, experiment_id)
);

-- Event tracking
CREATE TABLE experiment_events (
    event_id UUID PRIMARY KEY,
    user_id VARCHAR(50),
    experiment_id VARCHAR(50),
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP,
    event_value DECIMAL(10,2)
);
```

### 7. How do you calculate statistical significance in A/B tests?
**Answer**: Use statistical tests to validate results:
```python
import scipy.stats as stats

def calculate_significance(control_conversions, control_visitors, 
                         treatment_conversions, treatment_visitors):
    # Conversion rates
    control_rate = control_conversions / control_visitors
    treatment_rate = treatment_conversions / treatment_visitors
    
    # Z-test for proportions
    pooled_rate = (control_conversions + treatment_conversions) / \
                  (control_visitors + treatment_visitors)
    
    pooled_se = np.sqrt(pooled_rate * (1 - pooled_rate) * 
                       (1/control_visitors + 1/treatment_visitors))
    
    z_score = (treatment_rate - control_rate) / pooled_se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    return {
        'control_rate': control_rate,
        'treatment_rate': treatment_rate,
        'lift': (treatment_rate - control_rate) / control_rate,
        'p_value': p_value,
        'significant': p_value < 0.05
    }
```

### 8. What is statistical power and how do you calculate sample size?
**Answer**: Power is probability of detecting true effect:
```python
def calculate_sample_size(baseline_rate, minimum_detectable_effect, 
                         alpha=0.05, power=0.8):
    """
    Calculate required sample size for A/B test
    """
    from statsmodels.stats.power import ttest_power
    from statsmodels.stats.proportion import proportions_ztest
    
    # Effect size
    treatment_rate = baseline_rate * (1 + minimum_detectable_effect)
    
    # Calculate sample size using power analysis
    effect_size = (treatment_rate - baseline_rate) / \
                  np.sqrt(baseline_rate * (1 - baseline_rate))
    
    sample_size = ttest_power(effect_size, power, alpha, alternative='two-sided')
    
    return int(sample_size)
```

### 9. How do you handle multiple testing problems in experimentation?
**Answer**: Adjust for multiple comparisons:
```python
def bonferroni_correction(p_values, alpha=0.05):
    """Apply Bonferroni correction for multiple testing"""
    adjusted_alpha = alpha / len(p_values)
    significant_tests = [p < adjusted_alpha for p in p_values]
    return adjusted_alpha, significant_tests

def false_discovery_rate(p_values, alpha=0.05):
    """Apply Benjamini-Hochberg FDR correction"""
    from statsmodels.stats.multitest import multipletests
    
    rejected, p_adjusted, _, _ = multipletests(p_values, alpha, method='fdr_bh')
    return rejected, p_adjusted
```

### 10. What are guardrail metrics in experimentation?
**Answer**: Metrics that ensure experiments don't harm business:
```sql
-- Define guardrail metrics
CREATE TABLE guardrail_metrics (
    experiment_id VARCHAR(50),
    metric_name VARCHAR(100),
    threshold_type VARCHAR(20), -- 'min', 'max', 'range'
    threshold_value DECIMAL(10,4),
    current_value DECIMAL(10,4),
    status VARCHAR(20) -- 'PASS', 'FAIL', 'WARNING'
);

-- Monitor guardrails
SELECT 
    experiment_id,
    COUNT(*) as total_metrics,
    SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) as failed_metrics
FROM guardrail_metrics
GROUP BY experiment_id
HAVING failed_metrics > 0; -- Alert on any failures
```

## Advanced Analytics (21-30)

### 11. How do you implement cohort analysis?
**Answer**: Track user behavior over time:
```sql
-- Cohort analysis for retention
WITH user_cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', first_order_date) as cohort_month
    FROM (
        SELECT user_id, MIN(order_date) as first_order_date
        FROM orders
        GROUP BY user_id
    ) first_orders
),
cohort_data AS (
    SELECT 
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as order_month,
        COUNT(DISTINCT o.user_id) as active_users
    FROM user_cohorts c
    JOIN orders o ON c.user_id = o.user_id
    GROUP BY c.cohort_month, DATE_TRUNC('month', o.order_date)
)
SELECT 
    cohort_month,
    order_month,
    active_users,
    EXTRACT(MONTH FROM AGE(order_month, cohort_month)) as period_number
FROM cohort_data
ORDER BY cohort_month, period_number;
```

### 12. What is funnel analysis and how do you implement it?
**Answer**: Track user progression through steps:
```sql
-- Funnel analysis
WITH funnel_steps AS (
    SELECT 
        user_id,
        MAX(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) as viewed,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) as added_cart,
        MAX(CASE WHEN event_type = 'checkout' THEN 1 ELSE 0 END) as checkout,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) as purchased
    FROM events
    WHERE event_date BETWEEN '2024-01-01' AND '2024-01-31'
    GROUP BY user_id
)
SELECT 
    SUM(viewed) as step1_views,
    SUM(added_cart) as step2_cart,
    SUM(checkout) as step3_checkout,
    SUM(purchased) as step4_purchase,
    -- Conversion rates
    SUM(added_cart)::FLOAT / SUM(viewed) as view_to_cart_rate,
    SUM(checkout)::FLOAT / SUM(added_cart) as cart_to_checkout_rate,
    SUM(purchased)::FLOAT / SUM(checkout) as checkout_to_purchase_rate
FROM funnel_steps;
```

### 13. How do you implement attribution modeling?
**Answer**: Assign credit to marketing touchpoints:
```sql
-- First-touch attribution
WITH first_touch AS (
    SELECT 
        user_id,
        FIRST_VALUE(channel) OVER (
            PARTITION BY user_id 
            ORDER BY touchpoint_date
        ) as first_touch_channel
    FROM marketing_touchpoints
),
conversions AS (
    SELECT user_id, conversion_value
    FROM orders
    WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31'
)
SELECT 
    ft.first_touch_channel,
    COUNT(*) as conversions,
    SUM(c.conversion_value) as attributed_revenue
FROM first_touch ft
JOIN conversions c ON ft.user_id = c.user_id
GROUP BY ft.first_touch_channel;

-- Multi-touch attribution (linear)
SELECT 
    channel,
    SUM(conversion_value / touchpoint_count) as attributed_revenue
FROM (
    SELECT 
        mt.user_id,
        mt.channel,
        c.conversion_value,
        COUNT(*) OVER (PARTITION BY mt.user_id) as touchpoint_count
    FROM marketing_touchpoints mt
    JOIN conversions c ON mt.user_id = c.user_id
) attributed_touches
GROUP BY channel;
```

### 14. What is customer lifetime value (CLV) and how do you calculate it?
**Answer**: Predicted revenue from customer relationship:
```sql
-- Historical CLV calculation
WITH customer_metrics AS (
    SELECT 
        customer_id,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        COUNT(*) as total_orders,
        SUM(order_amount) as total_revenue,
        AVG(order_amount) as avg_order_value,
        EXTRACT(DAYS FROM MAX(order_date) - MIN(order_date)) as customer_lifespan_days
    FROM orders
    GROUP BY customer_id
)
SELECT 
    customer_id,
    total_revenue as historical_clv,
    -- Predictive CLV (simplified)
    avg_order_value * 
    (total_orders / NULLIF(customer_lifespan_days, 0) * 365) * 
    2 as predicted_annual_clv -- Assuming 2-year retention
FROM customer_metrics
WHERE customer_lifespan_days > 0;
```

### 15. How do you implement real-time experimentation?
**Answer**: Stream processing for live experiments:
```python
class RealTimeExperiment:
    def __init__(self, experiment_config):
        self.config = experiment_config
        self.redis_client = redis.Redis()
        
    def assign_user_to_variant(self, user_id):
        # Check if user already assigned
        assignment = self.redis_client.get(f"exp:{self.config['id']}:user:{user_id}")
        
        if assignment:
            return assignment.decode()
        
        # Hash-based assignment for consistency
        hash_value = hashlib.md5(f"{user_id}{self.config['id']}".encode()).hexdigest()
        hash_int = int(hash_value[:8], 16)
        
        if hash_int % 100 < self.config['traffic_allocation'] * 100:
            variant = 'treatment' if hash_int % 2 == 0 else 'control'
        else:
            variant = 'control'
        
        # Cache assignment
        self.redis_client.setex(
            f"exp:{self.config['id']}:user:{user_id}", 
            86400,  # 24 hours
            variant
        )
        
        return variant
    
    def track_event(self, user_id, event_type, value=None):
        variant = self.assign_user_to_variant(user_id)
        
        event = {
            'experiment_id': self.config['id'],
            'user_id': user_id,
            'variant': variant,
            'event_type': event_type,
            'value': value,
            'timestamp': time.time()
        }
        
        # Send to real-time analytics
        self.send_to_kafka('experiment_events', event)
```

---

## 📚 Study Guide

### KPI Best Practices
1. **SMART Criteria**: Specific, Measurable, Achievable, Relevant, Time-bound
2. **Balanced Scorecard**: Financial, Customer, Process, Learning perspectives
3. **Leading/Lagging Mix**: Balance predictive and outcome metrics
4. **Actionable**: KPIs should drive specific actions
5. **Regular Review**: Update KPIs as business evolves

### Experimentation Framework
1. **Hypothesis Formation**: Clear, testable predictions
2. **Sample Size Planning**: Adequate power for detection
3. **Randomization**: Proper user assignment
4. **Statistical Rigor**: Appropriate tests and corrections
5. **Business Impact**: Focus on meaningful metrics

### Common Pitfalls
- **Multiple Testing**: Not correcting for multiple comparisons
- **Peeking**: Stopping tests early based on interim results
- **Selection Bias**: Non-random user assignment
- **Novelty Effects**: Temporary behavior changes
- **Simpson's Paradox**: Segment-level reversals