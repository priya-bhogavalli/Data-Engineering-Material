# KPIs and Experimentation Key Concepts

## 🎯 What are KPIs and Experimentation?
Key Performance Indicators (KPIs) measure business success, while experimentation (A/B testing) validates hypotheses through controlled tests.

## 📊 KPI Framework

### 1. KPI Categories
```python
# Business KPI definitions
class KPIDefinitions:
    def __init__(self):
        self.kpis = {
            # Revenue KPIs
            'monthly_recurring_revenue': {
                'formula': 'SUM(subscription_amount) WHERE status = "active"',
                'frequency': 'monthly',
                'target': 1000000,
                'threshold': {'red': 0.9, 'yellow': 0.95, 'green': 1.0}
            },
            
            # Customer KPIs
            'customer_acquisition_cost': {
                'formula': 'marketing_spend / new_customers',
                'frequency': 'monthly',
                'target': 100,
                'threshold': {'green': 100, 'yellow': 150, 'red': 200}
            },
            
            # Operational KPIs
            'system_uptime': {
                'formula': 'uptime_minutes / total_minutes * 100',
                'frequency': 'daily',
                'target': 99.9,
                'threshold': {'red': 99.0, 'yellow': 99.5, 'green': 99.9}
            }
        }
```

### 2. KPI Data Model
```sql
-- KPI fact table
CREATE TABLE fact_kpi_metrics (
    kpi_key INT PRIMARY KEY,
    date_key INT,
    business_unit_key INT,
    kpi_name VARCHAR(100),
    actual_value DECIMAL(15,4),
    target_value DECIMAL(15,4),
    variance_percentage DECIMAL(8,4),
    status VARCHAR(10), -- 'GREEN', 'YELLOW', 'RED'
    calculation_timestamp TIMESTAMP,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- KPI dimension
CREATE TABLE dim_kpi (
    kpi_key INT PRIMARY KEY,
    kpi_name VARCHAR(100),
    kpi_category VARCHAR(50),
    calculation_formula TEXT,
    frequency VARCHAR(20),
    owner VARCHAR(100),
    description TEXT
);
```

### 3. KPI Calculation Engine
```python
import pandas as pd
from datetime import datetime, timedelta

class KPICalculator:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.calculation_date = datetime.now().date()
    
    def calculate_revenue_kpis(self):
        """Calculate revenue-related KPIs"""
        # Monthly Recurring Revenue
        mrr_sql = """
        SELECT 
            DATE_TRUNC('month', subscription_date) as month,
            SUM(monthly_amount) as mrr
        FROM subscriptions 
        WHERE status = 'active'
        AND subscription_date <= %s
        GROUP BY DATE_TRUNC('month', subscription_date)
        """
        
        mrr_df = pd.read_sql(mrr_sql, self.conn, params=[self.calculation_date])
        
        # Average Revenue Per User
        arpu_sql = """
        SELECT 
            DATE_TRUNC('month', transaction_date) as month,
            SUM(amount) / COUNT(DISTINCT customer_id) as arpu
        FROM transactions
        WHERE transaction_date >= %s
        GROUP BY DATE_TRUNC('month', transaction_date)
        """
        
        start_date = self.calculation_date - timedelta(days=365)
        arpu_df = pd.read_sql(arpu_sql, self.conn, params=[start_date])
        
        return {'mrr': mrr_df, 'arpu': arpu_df}
    
    def calculate_customer_kpis(self):
        """Calculate customer-related KPIs"""
        # Customer Acquisition Cost
        cac_sql = """
        SELECT 
            DATE_TRUNC('month', acquisition_date) as month,
            SUM(marketing_spend) / COUNT(customer_id) as cac
        FROM customer_acquisition ca
        JOIN marketing_campaigns mc ON ca.campaign_id = mc.campaign_id
        WHERE acquisition_date >= %s
        GROUP BY DATE_TRUNC('month', acquisition_date)
        """
        
        start_date = self.calculation_date - timedelta(days=365)
        cac_df = pd.read_sql(cac_sql, self.conn, params=[start_date])
        
        # Customer Lifetime Value
        clv_sql = """
        WITH customer_revenue AS (
            SELECT 
                customer_id,
                SUM(amount) as total_revenue,
                COUNT(*) as transaction_count,
                MAX(transaction_date) - MIN(transaction_date) as lifetime_days
            FROM transactions
            GROUP BY customer_id
        )
        SELECT 
            AVG(total_revenue) as avg_clv,
            AVG(lifetime_days) as avg_lifetime_days
        FROM customer_revenue
        WHERE lifetime_days > 0
        """
        
        clv_df = pd.read_sql(clv_sql, self.conn)
        
        return {'cac': cac_df, 'clv': clv_df}
    
    def store_kpi_results(self, kpi_results):
        """Store calculated KPIs in fact table"""
        for kpi_name, df in kpi_results.items():
            for _, row in df.iterrows():
                kpi_record = {
                    'date_key': int(row['month'].strftime('%Y%m%d')),
                    'kpi_name': kpi_name,
                    'actual_value': row[kpi_name],
                    'calculation_timestamp': datetime.now()
                }
                
                # Insert into fact table
                insert_sql = """
                INSERT INTO fact_kpi_metrics 
                (date_key, kpi_name, actual_value, calculation_timestamp)
                VALUES (%(date_key)s, %(kpi_name)s, %(actual_value)s, %(calculation_timestamp)s)
                """
                
                cursor = self.conn.cursor()
                cursor.execute(insert_sql, kpi_record)
        
        self.conn.commit()
```

## 🧪 A/B Testing Framework

### 1. Experiment Design
```python
import random
import numpy as np
from scipy import stats

class ExperimentDesigner:
    def __init__(self):
        self.experiments = {}
    
    def design_experiment(self, experiment_name, hypothesis, metric, 
                         effect_size, alpha=0.05, power=0.8):
        """Design A/B test with proper sample size calculation"""
        
        # Calculate required sample size
        sample_size = self.calculate_sample_size(effect_size, alpha, power)
        
        experiment = {
            'name': experiment_name,
            'hypothesis': hypothesis,
            'primary_metric': metric,
            'effect_size': effect_size,
            'alpha': alpha,
            'power': power,
            'sample_size_per_group': sample_size,
            'status': 'designed'
        }
        
        self.experiments[experiment_name] = experiment
        return experiment
    
    def calculate_sample_size(self, effect_size, alpha, power):
        """Calculate required sample size for experiment"""
        # Using Cohen's d for effect size
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        sample_size = 2 * ((z_alpha + z_beta) / effect_size) ** 2
        return int(np.ceil(sample_size))
    
    def assign_treatment(self, user_id, experiment_name):
        """Assign user to treatment or control group"""
        # Use hash for consistent assignment
        hash_value = hash(f"{user_id}_{experiment_name}")
        return 'treatment' if hash_value % 2 == 0 else 'control'
```

### 2. Experiment Data Model
```sql
-- Experiment definition
CREATE TABLE dim_experiment (
    experiment_key INT PRIMARY KEY,
    experiment_name VARCHAR(100),
    hypothesis TEXT,
    primary_metric VARCHAR(100),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    sample_size_per_group INT,
    effect_size DECIMAL(8,4),
    significance_level DECIMAL(4,3)
);

-- User assignments
CREATE TABLE fact_experiment_assignment (
    assignment_key INT PRIMARY KEY,
    experiment_key INT,
    user_key INT,
    assignment_date DATE,
    treatment_group VARCHAR(20), -- 'control', 'treatment'
    FOREIGN KEY (experiment_key) REFERENCES dim_experiment(experiment_key)
);

-- Experiment results
CREATE TABLE fact_experiment_metrics (
    metric_key INT PRIMARY KEY,
    experiment_key INT,
    user_key INT,
    date_key INT,
    treatment_group VARCHAR(20),
    metric_name VARCHAR(100),
    metric_value DECIMAL(15,4),
    conversion_flag BOOLEAN
);
```

### 3. Statistical Analysis
```python
class ExperimentAnalyzer:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def analyze_experiment(self, experiment_name):
        """Perform statistical analysis of A/B test results"""
        
        # Get experiment data
        results_sql = """
        SELECT 
            treatment_group,
            metric_value,
            conversion_flag
        FROM fact_experiment_metrics fem
        JOIN dim_experiment de ON fem.experiment_key = de.experiment_key
        WHERE de.experiment_name = %s
        """
        
        results_df = pd.read_sql(results_sql, self.conn, params=[experiment_name])
        
        # Separate control and treatment groups
        control = results_df[results_df['treatment_group'] == 'control']
        treatment = results_df[results_df['treatment_group'] == 'treatment']
        
        # Perform t-test for continuous metrics
        if 'metric_value' in results_df.columns:
            t_stat, p_value = stats.ttest_ind(
                treatment['metric_value'].dropna(),
                control['metric_value'].dropna()
            )
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt(
                ((len(treatment) - 1) * treatment['metric_value'].var() + 
                 (len(control) - 1) * control['metric_value'].var()) /
                (len(treatment) + len(control) - 2)
            )
            
            cohens_d = (treatment['metric_value'].mean() - control['metric_value'].mean()) / pooled_std
        
        # Perform chi-square test for conversion rates
        if 'conversion_flag' in results_df.columns:
            contingency_table = pd.crosstab(
                results_df['treatment_group'], 
                results_df['conversion_flag']
            )
            
            chi2, p_value_chi2, dof, expected = stats.chi2_contingency(contingency_table)
            
            # Calculate conversion rates
            control_conversion = control['conversion_flag'].mean()
            treatment_conversion = treatment['conversion_flag'].mean()
            lift = (treatment_conversion - control_conversion) / control_conversion
        
        return {
            'experiment_name': experiment_name,
            'sample_sizes': {
                'control': len(control),
                'treatment': len(treatment)
            },
            'continuous_metrics': {
                't_statistic': t_stat,
                'p_value': p_value,
                'effect_size': cohens_d,
                'control_mean': control['metric_value'].mean(),
                'treatment_mean': treatment['metric_value'].mean()
            },
            'conversion_metrics': {
                'chi2_statistic': chi2,
                'p_value': p_value_chi2,
                'control_rate': control_conversion,
                'treatment_rate': treatment_conversion,
                'lift': lift
            }
        }
    
    def calculate_confidence_interval(self, data, confidence=0.95):
        """Calculate confidence interval for metric"""
        n = len(data)
        mean = np.mean(data)
        std_err = stats.sem(data)
        
        h = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
        
        return {
            'mean': mean,
            'lower_bound': mean - h,
            'upper_bound': mean + h,
            'margin_of_error': h
        }
```

## 📈 Advanced Analytics

### Sequential Testing
```python
class SequentialTesting:
    def __init__(self, alpha=0.05, beta=0.2):
        self.alpha = alpha
        self.beta = beta
    
    def calculate_boundaries(self, n_max):
        """Calculate sequential testing boundaries"""
        # Simplified O'Brien-Fleming boundaries
        boundaries = []
        
        for i in range(1, n_max + 1):
            # Upper boundary for early stopping
            z_upper = stats.norm.ppf(1 - self.alpha / (2 * np.sqrt(i)))
            # Lower boundary for futility
            z_lower = stats.norm.ppf(self.beta / np.sqrt(i))
            
            boundaries.append({
                'analysis': i,
                'upper_boundary': z_upper,
                'lower_boundary': z_lower
            })
        
        return boundaries
    
    def should_stop_experiment(self, current_z_score, analysis_number, boundaries):
        """Determine if experiment should be stopped early"""
        current_boundary = boundaries[analysis_number - 1]
        
        if abs(current_z_score) >= current_boundary['upper_boundary']:
            return True, 'significant'
        elif abs(current_z_score) <= current_boundary['lower_boundary']:
            return True, 'futile'
        else:
            return False, 'continue'
```

## 🎯 Best Practices

### KPI Management
- Define clear, measurable objectives
- Establish realistic targets and thresholds
- Automate calculation and reporting
- Monitor trends and seasonality
- Regular review and adjustment

### Experimentation
- Formulate clear hypotheses
- Calculate proper sample sizes
- Ensure random assignment
- Monitor for external factors
- Document learnings and decisions

## 🛠️ Tools & Technologies
- **Analytics**: Python, R, SQL
- **Visualization**: Tableau, Power BI, Grafana
- **Experimentation**: Optimizely, VWO, custom platforms
- **Statistical**: SciPy, statsmodels, R
- **Monitoring**: Datadog, New Relic, custom dashboards

## ⚠️ Common Pitfalls
- Multiple testing without correction
- Peeking at results too early
- Insufficient sample sizes
- Selection bias in assignment
- Ignoring external factors
- Misinterpreting statistical significance