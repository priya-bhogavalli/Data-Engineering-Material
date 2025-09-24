# ☁️ Cloud Cost Optimization for Data Engineering

> **Practical strategies to reduce cloud costs by 30-70% without sacrificing performance**

## 💰 **Cost Optimization Fundamentals**

### **The 4 Pillars of Cloud Cost Management**
1. **Right-sizing**: Match resources to actual needs
2. **Scheduling**: Turn off unused resources
3. **Reserved Capacity**: Commit for discounts
4. **Monitoring**: Track and alert on spending

## 🎯 **AWS Cost Optimization**

### **Compute Optimization**
```python
# EC2 Spot Instances (up to 90% savings)
spot_config = {
    'InstanceType': 'm5.large',
    'SpotPrice': '0.05',  # vs $0.096 on-demand
    'InstanceInterruptionBehavior': 'terminate'
}

# Auto Scaling for variable workloads
auto_scaling = {
    'MinSize': 1,
    'MaxSize': 10,
    'DesiredCapacity': 2,
    'TargetCPUUtilization': 70
}
```

### **Storage Optimization**
```python
# S3 Intelligent Tiering (automatic cost optimization)
s3_lifecycle = {
    'Rules': [{
        'Status': 'Enabled',
        'Transitions': [
            {'Days': 30, 'StorageClass': 'STANDARD_IA'},
            {'Days': 90, 'StorageClass': 'GLACIER'},
            {'Days': 365, 'StorageClass': 'DEEP_ARCHIVE'}
        ]
    }]
}

# Data compression (50-80% storage savings)
df.write.option("compression", "gzip").parquet("s3://bucket/data/")
```

### **Data Processing Optimization**
```python
# EMR Spot Instances
emr_config = {
    'InstanceGroups': [
        {
            'InstanceRole': 'MASTER',
            'InstanceType': 'm5.xlarge',
            'InstanceCount': 1,
            'Market': 'ON_DEMAND'
        },
        {
            'InstanceRole': 'CORE',
            'InstanceType': 'm5.xlarge', 
            'InstanceCount': 2,
            'Market': 'SPOT',
            'BidPrice': '0.20'
        }
    ]
}

# Glue job optimization
glue_job = {
    'MaxCapacity': 2,  # Start small, scale as needed
    'Timeout': 60,     # Prevent runaway jobs
    'MaxRetries': 1    # Limit retry costs
}
```

## 🔷 **Azure Cost Optimization**

### **Compute Savings**
```python
# Azure Spot VMs (up to 90% savings)
spot_vm_config = {
    'vm_size': 'Standard_D2s_v3',
    'priority': 'Spot',
    'eviction_policy': 'Deallocate',
    'max_price': 0.05
}

# Reserved Instances (up to 72% savings)
reserved_instance = {
    'term': '3_years',
    'payment_option': 'all_upfront',
    'instance_type': 'Standard_D2s_v3',
    'savings': '72%'
}
```

### **Data Factory Optimization**
```json
{
    "pipeline": {
        "activities": [
            {
                "type": "Copy",
                "typeProperties": {
                    "parallelCopies": 4,
                    "dataIntegrationUnits": 2,
                    "enableSkipIncompatibleRow": true
                }
            }
        ]
    }
}
```

## 🟢 **GCP Cost Optimization**

### **Compute Engine Savings**
```python
# Preemptible VMs (up to 80% savings)
preemptible_config = {
    'machine_type': 'n1-standard-4',
    'preemptible': True,
    'automatic_restart': False,
    'on_host_maintenance': 'TERMINATE'
}

# Sustained Use Discounts (automatic up to 30% savings)
# No configuration needed - automatic for running >25% of month
```

### **BigQuery Optimization**
```sql
-- Partition tables for cost efficiency
CREATE TABLE dataset.partitioned_table
PARTITION BY DATE(timestamp_column)
CLUSTER BY user_id, category
AS SELECT * FROM dataset.source_table;

-- Use approximate aggregation functions
SELECT 
    APPROX_COUNT_DISTINCT(user_id) as unique_users,
    APPROX_QUANTILES(amount, 100)[OFFSET(50)] as median_amount
FROM dataset.transactions;
```

## 📊 **Cost Monitoring & Alerting**

### **AWS Cost Monitoring**
```python
import boto3

def create_cost_budget():
    budgets = boto3.client('budgets')
    
    budget = {
        'BudgetName': 'DataEngineering-Monthly',
        'BudgetLimit': {
            'Amount': '1000',
            'Unit': 'USD'
        },
        'TimeUnit': 'MONTHLY',
        'BudgetType': 'COST'
    }
    
    subscribers = [{
        'SubscriptionType': 'EMAIL',
        'Address': 'admin@company.com'
    }]
    
    budgets.create_budget(
        AccountId='123456789012',
        Budget=budget,
        NotificationsWithSubscribers=[{
            'Notification': {
                'NotificationType': 'ACTUAL',
                'ComparisonOperator': 'GREATER_THAN',
                'Threshold': 80
            },
            'Subscribers': subscribers
        }]
    )
```

### **Multi-Cloud Cost Dashboard**
```python
# Terraform for cost monitoring infrastructure
resource "aws_cloudwatch_dashboard" "cost_dashboard" {
  dashboard_name = "DataEngineering-Costs"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        properties = {
          metrics = [
            ["AWS/Billing", "EstimatedCharges", "Currency", "USD"]
          ]
          period = 86400
          stat   = "Maximum"
          region = "us-east-1"
          title  = "Daily Costs"
        }
      }
    ]
  })
}
```

## 🎯 **Data Pipeline Cost Optimization**

### **Spark Optimization**
```python
# Optimize Spark configuration for cost
spark_config = {
    'spark.sql.adaptive.enabled': 'true',
    'spark.sql.adaptive.coalescePartitions.enabled': 'true',
    'spark.sql.adaptive.skewJoin.enabled': 'true',
    'spark.serializer': 'org.apache.spark.serializer.KryoSerializer',
    'spark.sql.execution.arrow.pyspark.enabled': 'true'
}

# Use broadcast joins for small tables
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")

# Cache frequently accessed data
df.cache()
df.count()  # Trigger caching
```

### **Storage Format Optimization**
```python
# Parquet with compression (70% storage savings)
df.write \
  .option("compression", "snappy") \
  .mode("overwrite") \
  .parquet("s3://bucket/optimized-data/")

# Delta Lake for ACID transactions and time travel
df.write \
  .format("delta") \
  .option("mergeSchema", "true") \
  .save("s3://bucket/delta-table/")
```

## 📈 **ROI Measurement**

### **Cost Tracking Template**
```python
cost_metrics = {
    'baseline_monthly_cost': 10000,
    'optimized_monthly_cost': 4000,
    'savings_percentage': 60,
    'optimization_effort_hours': 40,
    'hourly_rate': 100,
    'roi_calculation': {
        'monthly_savings': 6000,
        'annual_savings': 72000,
        'optimization_cost': 4000,
        'roi_percentage': 1700  # (72000-4000)/4000 * 100
    }
}
```

## 🛠️ **Cost Optimization Tools**

### **AWS Tools**
- **Cost Explorer**: Analyze spending patterns
- **Trusted Advisor**: Automated recommendations
- **AWS Budgets**: Set spending alerts
- **Cost Anomaly Detection**: ML-powered alerts

### **Azure Tools**
- **Cost Management**: Spending analysis
- **Azure Advisor**: Optimization recommendations
- **Budgets**: Cost control and alerts
- **Cost Alerts**: Proactive notifications

### **GCP Tools**
- **Cloud Billing**: Cost analysis and reporting
- **Recommender**: AI-powered suggestions
- **Budgets & Alerts**: Spending controls
- **Cloud Asset Inventory**: Resource tracking

### **Third-Party Tools**
- **CloudHealth**: Multi-cloud cost management
- **Cloudability**: Cost optimization platform
- **ParkMyCloud**: Automated resource scheduling
- **Spot.io**: Automated spot instance management

## 🎯 **Best Practices Checklist**

### **Daily**
- [ ] Monitor cost dashboards
- [ ] Check for cost anomalies
- [ ] Review resource utilization

### **Weekly**
- [ ] Analyze top spending services
- [ ] Review and clean up unused resources
- [ ] Optimize underutilized instances

### **Monthly**
- [ ] Review and adjust budgets
- [ ] Analyze cost trends and patterns
- [ ] Update reserved instance strategy
- [ ] Generate cost optimization reports

### **Quarterly**
- [ ] Comprehensive cost review
- [ ] Update cost optimization strategy
- [ ] Evaluate new cost-saving services
- [ ] Team training on cost awareness

## 💡 **Quick Wins (Immediate 20-40% Savings)**

1. **Turn off dev/test environments** after hours
2. **Right-size over-provisioned instances**
3. **Use spot/preemptible instances** for batch jobs
4. **Enable auto-scaling** for variable workloads
5. **Implement data lifecycle policies**
6. **Compress and optimize data formats**
7. **Clean up unused storage and snapshots**
8. **Use reserved instances** for predictable workloads