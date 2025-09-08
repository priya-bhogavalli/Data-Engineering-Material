# Fivetran - Comprehensive Interview Questions

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Connectors & Data Sources](#connectors--data-sources)
3. [Configuration & Setup](#configuration--setup)
4. [Data Transformation](#data-transformation)
5. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
6. [Security & Compliance](#security--compliance)
7. [Performance & Optimization](#performance--optimization)
8. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### 1. What is Fivetran and how does it differ from traditional ETL tools?

**Answer:**
Fivetran is a cloud-based ELT (Extract, Load, Transform) platform that automates data integration from various sources to data warehouses.

**Key Differences:**
- **Fully Managed**: No infrastructure management required
- **ELT Approach**: Loads raw data first, transforms in warehouse
- **Pre-built Connectors**: 300+ ready-to-use connectors
- **Automatic Schema Management**: Handles schema changes automatically
- **Zero Maintenance**: Automatic updates and monitoring

**Traditional ETL vs Fivetran:**
```
Traditional ETL:
Source → Custom Code → Transform → Load → Warehouse

Fivetran ELT:
Source → Fivetran Connector → Load → Warehouse → Transform (dbt)
```

### 2. Explain Fivetran's ELT approach and its advantages.

**Answer:**
**ELT (Extract, Load, Transform) Process:**
1. **Extract**: Pull data from source systems
2. **Load**: Store raw data in data warehouse
3. **Transform**: Use warehouse compute for transformations

**Advantages:**
- **Scalability**: Leverage warehouse compute power
- **Flexibility**: Transform data multiple ways without re-extraction
- **Speed**: Faster initial data loading
- **Cost-Effective**: Pay for warehouse compute only when needed

**Example Workflow:**
```sql
-- Raw data loaded by Fivetran
SELECT * FROM fivetran_schema.salesforce_opportunity;

-- Transformations in warehouse (using dbt)
{{ config(materialized='table') }}
SELECT 
    id,
    name,
    amount,
    stage_name,
    close_date,
    created_date
FROM {{ ref('salesforce_opportunity') }}
WHERE stage_name = 'Closed Won'
```

### 3. How do you set up a Salesforce connector in Fivetran?

**Answer:**
**Setup Steps:**
1. **Create Connector**: Select Salesforce from connector library
2. **Authentication**: Provide Salesforce credentials or OAuth
3. **Configuration**: Select objects and fields to sync
4. **Destination**: Choose target schema in warehouse
5. **Initial Sync**: Run full historical sync

**Configuration Example:**
```json
{
  "connector_type": "salesforce",
  "destination_schema": "salesforce_prod",
  "sync_frequency": "15min",
  "objects": [
    "Account",
    "Contact", 
    "Opportunity",
    "Lead",
    "Case"
  ],
  "custom_objects": [
    "Custom_Product__c"
  ]
}
```

### 4. How does Fivetran handle incremental data synchronization?

**Answer:**
**Incremental Sync Methods:**

1. **Cursor-based**: Uses timestamp or ID columns
```sql
-- Fivetran tracks last synced value
SELECT * FROM source_table 
WHERE updated_at > '2024-01-15 10:30:00'
```

2. **Log-based (CDC)**: Reads database transaction logs
```
Database → Transaction Log → Fivetran → Warehouse
```

3. **API-based**: Uses API pagination and timestamps
```python
# API incremental sync
def sync_incremental():
    last_sync = get_last_sync_timestamp()
    response = api.get_data(since=last_sync)
    return response.data
```

### 5. How does Fivetran integrate with dbt for transformations?

**Answer:**
**Integration Methods:**
1. **dbt Core**: Manual integration with orchestration
2. **dbt Cloud**: Native Fivetran integration
3. **Fivetran Transformations**: Built-in dbt functionality

**dbt Cloud Integration:**
```yaml
# dbt_project.yml
name: 'fivetran_analytics'
version: '1.0.0'

models:
  fivetran_analytics:
    staging:
      +materialized: view
    marts:
      +materialized: table

sources:
  - name: salesforce
    schema: fivetran_salesforce
    tables:
      - name: opportunity
      - name: account
```

**Example dbt Model:**
```sql
-- models/staging/stg_salesforce_opportunities.sql
{{ config(materialized='view') }}

SELECT 
    id as opportunity_id,
    name as opportunity_name,
    amount,
    stage_name,
    close_date,
    account_id,
    _fivetran_synced as last_updated
FROM {{ source('salesforce', 'opportunity') }}
WHERE _fivetran_deleted = FALSE
```

### 6. How do you monitor Fivetran connector health and performance?

**Answer:**
**Monitoring Methods:**

1. **Fivetran Dashboard**: Built-in monitoring interface
2. **Alerts**: Email/Slack notifications for issues
3. **API Monitoring**: Programmatic health checks
4. **Logs**: Detailed sync logs and error messages

**Key Metrics:**
```python
# Monitoring metrics to track
metrics = {
    'sync_frequency': 'How often syncs complete',
    'sync_duration': 'Time taken for each sync',
    'rows_synced': 'Number of records processed',
    'error_rate': 'Percentage of failed syncs',
    'data_freshness': 'Time since last successful sync',
    'api_usage': 'Source system API consumption'
}
```

**Alert Configuration:**
```json
{
  "alerts": [
    {
      "type": "sync_failure",
      "threshold": 2,
      "notification": "slack"
    },
    {
      "type": "sync_delay",
      "threshold": "30min",
      "notification": "email"
    }
  ]
}
```

### 7. What are common Fivetran sync issues and how do you troubleshoot them?

**Answer:**
**Common Issues:**

1. **Authentication Failures**
```
Error: Invalid credentials
Solution: Refresh OAuth tokens, check permissions
```

2. **API Rate Limits**
```
Error: Rate limit exceeded
Solution: Reduce sync frequency, contact source provider
```

3. **Schema Changes**
```
Error: Column not found
Solution: Review schema drift, update transformations
```

**Troubleshooting Process:**
```python
def troubleshoot_sync_issue(connector_id):
    # 1. Check connector status
    status = fivetran_api.get_connector_status(connector_id)
    
    # 2. Review recent logs
    logs = fivetran_api.get_logs(connector_id, limit=100)
    
    # 3. Analyze error patterns
    errors = [log for log in logs if log.level == 'ERROR']
    
    return {
        'status': status,
        'recent_errors': errors,
        'recommendations': generate_recommendations(errors)
    }
```

### 8. How does Fivetran handle data security and compliance?

**Answer:**
**Security Features:**

1. **Encryption**: Data encrypted in transit and at rest
2. **Network Security**: VPC peering, private connectivity
3. **Access Control**: Role-based permissions
4. **Audit Logging**: Complete activity tracking
5. **Compliance**: SOC 2, GDPR, HIPAA compliance

**Security Configuration:**
```json
{
  "security_settings": {
    "encryption": {
      "in_transit": "TLS 1.2+",
      "at_rest": "AES-256"
    },
    "network": {
      "ip_whitelist": ["10.0.0.0/8"],
      "vpc_peering": true,
      "private_link": true
    },
    "access_control": {
      "sso_enabled": true,
      "mfa_required": true,
      "rbac": true
    }
  }
}
```

### 9. How do you optimize Fivetran sync performance?

**Answer:**
**Optimization Strategies:**

1. **Incremental Sync**: Use proper cursor columns
2. **Column Selection**: Sync only needed columns
3. **Partitioning**: Use date-based partitioning
4. **Warehouse Optimization**: Right-size compute resources
5. **Sync Scheduling**: Avoid peak hours

**Performance Configuration:**
```json
{
  "optimization_settings": {
    "incremental_sync": {
      "enabled": true,
      "cursor_column": "updated_at",
      "lookback_window": "1 hour"
    },
    "column_selection": {
      "include_only": ["id", "name", "amount", "created_at"]
    },
    "sync_schedule": {
      "frequency": "1 hour",
      "avoid_peak_hours": true
    }
  }
}
```

### 10. Design a complete data pipeline using Fivetran for a SaaS company.

**Answer:**
**Architecture:**
```
Data Sources → Fivetran → Snowflake → dbt → BI Tools
     ↓             ↓          ↓        ↓       ↓
Salesforce → Connectors → Raw Data → Models → Dashboards
HubSpot                              
Google Analytics                     
Stripe                               
```

**Implementation:**
```yaml
# Data pipeline configuration
data_sources:
  - name: salesforce
    connector: salesforce
    sync_frequency: 15min
    objects: [Account, Contact, Opportunity, Lead]
    
  - name: hubspot
    connector: hubspot
    sync_frequency: 1hour
    objects: [Companies, Contacts, Deals]
    
  - name: stripe
    connector: stripe
    sync_frequency: 30min
    objects: [Customers, Charges, Subscriptions]

transformations:
  - name: customer_360
    depends_on: [salesforce, hubspot, stripe]
    models:
      - unified_customers
      - customer_metrics
      - churn_analysis
```

**dbt Models:**
```sql
-- Customer 360 view
{{ config(materialized='table') }}

WITH salesforce_accounts AS (
    SELECT id, name, industry, created_date
    FROM {{ ref('salesforce_account') }}
),
stripe_customers AS (
    SELECT id, email, created, subscription_status
    FROM {{ ref('stripe_customer') }}
)

SELECT 
    sf.id as account_id,
    sf.name as company_name,
    sf.industry,
    sc.subscription_status,
    sf.created_date as account_created,
    sc.created as customer_created
FROM salesforce_accounts sf
LEFT JOIN stripe_customers sc ON sf.email = sc.email
```

This comprehensive set of Fivetran interview questions covers essential concepts for modern ELT data integration, from basic setup to advanced optimization and real-world implementation scenarios.