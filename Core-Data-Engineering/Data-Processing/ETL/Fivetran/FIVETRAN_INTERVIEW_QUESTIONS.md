# Fivetran - Comprehensive Interview Questions

## 📋 Table of Contents

1. [Basic Level Questions](#-basic-level-questions)
2. [Intermediate Level Questions](#-intermediate-level-questions)
3. [Advanced Level Questions](#-advanced-level-questions)
4. [Architecture & Performance](#-architecture--performance)
5. [Streaming & Real-time Processing](#-streaming--real-time-processing)
6. [Production & Operations](#-production--operations)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🟢 Basic Level Questions

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
- **Data Preservation**: Keep raw data for future analysis

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

### 5. What are the main components of Fivetran's architecture?

**Answer:**
**Core Components:**

1. **Connectors**: Pre-built integrations for data sources
2. **Sync Engine**: Manages data extraction and loading
3. **Transformation Layer**: Built-in dbt for data modeling
4. **Monitoring Dashboard**: Real-time sync status and alerts
5. **Security Layer**: Encryption, access control, compliance

**Architecture Flow:**
```
Data Sources → Connectors → Sync Engine → Destination → Transformations
     ↓             ↓           ↓            ↓            ↓
  Salesforce → API Polling → Raw Tables → Snowflake → dbt Models
```

### 6. How does Fivetran integrate with dbt for transformations?

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

### 7. What types of data sources can Fivetran connect to?

**Answer:**
**Connector Categories:**

1. **SaaS Applications**: Salesforce, HubSpot, Zendesk, Shopify, Stripe
2. **Databases**: PostgreSQL, MySQL, SQL Server, Oracle, MongoDB
3. **Cloud Storage**: Amazon S3, Google Cloud Storage, Azure Blob
4. **Advertising Platforms**: Google Ads, Facebook Ads, LinkedIn Ads
5. **Analytics Tools**: Google Analytics, Adobe Analytics, Mixpanel
6. **File Systems**: FTP, SFTP, local files
7. **Event Streaming**: Kafka, Kinesis

**Popular Connectors:**
```python
popular_connectors = {
    "crm": ["Salesforce", "HubSpot", "Pipedrive"],
    "support": ["Zendesk", "Intercom", "Freshdesk"],
    "ecommerce": ["Shopify", "WooCommerce", "Magento"],
    "payments": ["Stripe", "PayPal", "Square"],
    "databases": ["PostgreSQL", "MySQL", "SQL Server"]
}
```

### 8. How do you monitor Fivetran connector health and performance?

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

### 9. What are Fivetran's metadata columns and why are they important?

**Answer:**
**Standard Metadata Columns:**

1. **_fivetran_synced**: Timestamp when record was last synced
2. **_fivetran_deleted**: Boolean flag for soft deletes
3. **_fivetran_id**: Unique identifier for deduplication

**Importance:**
- **Data Quality**: Track data freshness and validity
- **Debugging**: Identify sync issues and timing
- **Auditing**: Maintain data lineage and history
- **Deduplication**: Handle duplicate records

**Usage Example:**
```sql
-- Query with metadata filtering
SELECT 
    id,
    name,
    amount,
    _fivetran_synced as last_updated
FROM salesforce_opportunity
WHERE _fivetran_deleted = FALSE  -- Exclude soft-deleted records
    AND _fivetran_synced >= CURRENT_DATE - 1  -- Recent data only
ORDER BY _fivetran_synced DESC;
```

### 10. How does Fivetran handle schema changes in source systems?

**Answer:**
**Automatic Schema Management:**

1. **Detection**: Monitors source schema changes
2. **Notification**: Alerts when changes detected
3. **Adaptation**: Automatically adds new columns
4. **Preservation**: Maintains historical data integrity

**Schema Change Types:**
```sql
-- New column added
ALTER TABLE salesforce_opportunity 
ADD COLUMN new_field VARCHAR(255);
-- Fivetran automatically detects and adds

-- Data type change
-- Fivetran creates new column with suffix
-- old_column (original type)
-- old_column__st (new string type)

-- Column renamed
-- Fivetran treats as new column + deprecated old column
```

**Best Practices:**
- Monitor schema change notifications
- Update downstream transformations accordingly
- Test impact on existing queries and reports
- Document schema evolution for team awareness

---

*Continue reading for Intermediate Level Questions...*
# Fivetran - Comprehensive Interview Questions

## 📋 Table of Contents

1. [Basic Level Questions](#-basic-level-questions)
2. [Intermediate Level Questions](#-intermediate-level-questions)
3. [Advanced Level Questions](#-advanced-level-questions)
4. [Architecture & Performance](#-architecture--performance)
5. [Streaming & Real-time Processing](#-streaming--real-time-processing)
6. [Production & Operations](#-production--operations)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🟢 Basic Level Questions

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
- **Data Preservation**: Keep raw data for future analysis

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

### 5. What are the main components of Fivetran's architecture?

**Answer:**
**Core Components:**

1. **Connectors**: Pre-built integrations for data sources
2. **Sync Engine**: Manages data extraction and loading
3. **Transformation Layer**: Built-in dbt for data modeling
4. **Monitoring Dashboard**: Real-time sync status and alerts
5. **Security Layer**: Encryption, access control, compliance

**Architecture Flow:**
```
Data Sources → Connectors → Sync Engine → Destination → Transformations
     ↓             ↓           ↓            ↓            ↓
  Salesforce → API Polling → Raw Tables → Snowflake → dbt Models
```

### 6. How does Fivetran integrate with dbt for transformations?

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

### 7. What types of data sources can Fivetran connect to?

**Answer:**
**Connector Categories:**

1. **SaaS Applications**: Salesforce, HubSpot, Zendesk, Shopify, Stripe
2. **Databases**: PostgreSQL, MySQL, SQL Server, Oracle, MongoDB
3. **Cloud Storage**: Amazon S3, Google Cloud Storage, Azure Blob
4. **Advertising Platforms**: Google Ads, Facebook Ads, LinkedIn Ads
5. **Analytics Tools**: Google Analytics, Adobe Analytics, Mixpanel
6. **File Systems**: FTP, SFTP, local files
7. **Event Streaming**: Kafka, Kinesis

**Popular Connectors:**
```python
popular_connectors = {
    "crm": ["Salesforce", "HubSpot", "Pipedrive"],
    "support": ["Zendesk", "Intercom", "Freshdesk"],
    "ecommerce": ["Shopify", "WooCommerce", "Magento"],
    "payments": ["Stripe", "PayPal", "Square"],
    "databases": ["PostgreSQL", "MySQL", "SQL Server"]
}
```

### 8. How do you monitor Fivetran connector health and performance?

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

### 9. What are Fivetran's metadata columns and why are they important?

**Answer:**
**Standard Metadata Columns:**

1. **_fivetran_synced**: Timestamp when record was last synced
2. **_fivetran_deleted**: Boolean flag for soft deletes
3. **_fivetran_id**: Unique identifier for deduplication

**Importance:**
- **Data Quality**: Track data freshness and validity
- **Debugging**: Identify sync issues and timing
- **Auditing**: Maintain data lineage and history
- **Deduplication**: Handle duplicate records

**Usage Example:**
```sql
-- Query with metadata filtering
SELECT 
    id,
    name,
    amount,
    _fivetran_synced as last_updated
FROM salesforce_opportunity
WHERE _fivetran_deleted = FALSE  -- Exclude soft-deleted records
    AND _fivetran_synced >= CURRENT_DATE - 1  -- Recent data only
ORDER BY _fivetran_synced DESC;
```

### 10. How does Fivetran handle schema changes in source systems?

**Answer:**
**Automatic Schema Management:**

1. **Detection**: Monitors source schema changes
2. **Notification**: Alerts when changes detected
3. **Adaptation**: Automatically adds new columns
4. **Preservation**: Maintains historical data integrity

**Schema Change Types:**
```sql
-- New column added
ALTER TABLE salesforce_opportunity 
ADD COLUMN new_field VARCHAR(255);
-- Fivetran automatically detects and adds

-- Data type change
-- Fivetran creates new column with suffix
-- old_column (original type)
-- old_column__st (new string type)

-- Column renamed
-- Fivetran treats as new column + deprecated old column
```

**Best Practices:**
- Monitor schema change notifications
- Update downstream transformations accordingly
- Test impact on existing queries and reports
- Document schema evolution for team awareness

---

## 🟡 Intermediate Level Questions

### 11. Compare Fivetran's pricing model and how to optimize costs.

**Answer:**
**Pricing Model - Monthly Active Rows (MAR):**

**MAR Calculation:**
- Count of unique rows that changed during the month
- Includes new, updated, and deleted records
- Excludes unchanged rows from cost calculation

**Cost Optimization Strategies:**

1. **Data Filtering**:
```sql
-- Sync only necessary data
WHERE created_date >= '2020-01-01'  -- Historical cutoff
AND status != 'archived'           -- Exclude archived records
AND record_type = 'active'         -- Only active records
```

2. **Column Selection**:
```json
{
  "sync_mode": "incremental",
  "selected_fields": [
    "id", "name", "amount", "stage_name", "close_date"
  ],
  "excluded_fields": [
    "system_modstamp", "created_by_id", "last_modified_by_id"
  ]
}
```

3. **Sync Frequency Optimization**:
```python
# Optimize based on data criticality
sync_frequencies = {
    "critical_data": "15 minutes",      # Real-time needs
    "operational_data": "1 hour",       # Regular updates
    "reference_data": "24 hours",       # Static/slow-changing
    "historical_data": "weekly"         # Archive data
}
```

### 12. How do you troubleshoot common Fivetran sync issues?

**Answer:**
**Common Issues and Solutions:**

1. **Authentication Failures**:
```python
# Troubleshooting steps
def troubleshoot_auth_failure():
    steps = [
        "Check credential expiration",
        "Verify API permissions",
        "Refresh OAuth tokens",
        "Test connection manually",
        "Review IP whitelist settings"
    ]
    return steps
```

2. **API Rate Limits**:
```json
{
  "error": "Rate limit exceeded",
  "solutions": [
    "Reduce sync frequency",
    "Contact source provider for limit increase",
    "Implement data filtering",
    "Use off-peak sync scheduling"
  ]
}
```

3. **Schema Drift Issues**:
```sql
-- Check for schema changes
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'fivetran_salesforce'
ORDER BY table_name, ordinal_position;
```

4. **Data Quality Problems**:
```python
# Data quality checks
def data_quality_checks():
    return {
        "null_checks": "Unexpected null values",
        "duplicate_checks": "Duplicate primary keys",
        "type_validation": "Data type mismatches",
        "referential_integrity": "Broken foreign key relationships"
    }
```

### 13. Explain Fivetran's approach to handling deletes and data changes.

**Answer:**
**Delete Handling Methods:**

1. **Soft Deletes** (Default):
```sql
-- Fivetran marks records as deleted
SELECT 
    id,
    name,
    amount,
    _fivetran_deleted,  -- TRUE for deleted records
    _fivetran_synced
FROM salesforce_opportunity
WHERE _fivetran_deleted = FALSE;  -- Active records only
```

2. **Hard Deletes** (Optional):
```sql
-- Records physically removed from destination
-- Configured per connector based on requirements
-- Less common due to audit trail needs
```

**Change Data Capture (CDC):**
```python
# CDC implementation for databases
cdc_methods = {
    "log_based": {
        "databases": ["PostgreSQL", "MySQL", "SQL Server"],
        "mechanism": "Transaction log reading",
        "latency": "< 1 minute",
        "captures": ["INSERT", "UPDATE", "DELETE"]
    },
    "trigger_based": {
        "databases": ["Oracle", "older versions"],
        "mechanism": "Database triggers",
        "latency": "1-5 minutes",
        "overhead": "Higher on source system"
    }
}
```

**Handling Updates:**
```sql
-- Fivetran tracks all changes
SELECT 
    id,
    name,
    amount,
    stage_name,
    _fivetran_synced,  -- Last update timestamp
    LAG(_fivetran_synced) OVER (
        PARTITION BY id 
        ORDER BY _fivetran_synced
    ) as previous_sync
FROM salesforce_opportunity_history  -- Historical tracking
ORDER BY id, _fivetran_synced;
```

### 14. How do you implement data validation and quality checks with Fivetran?

**Answer:**
**Data Validation Strategies:**

1. **dbt Tests Integration**:
```sql
-- models/staging/stg_salesforce_opportunity.sql
{{ config(materialized='view') }}

SELECT 
    id,
    name,
    amount,
    stage_name,
    close_date,
    created_date,
    -- Data quality flags
    CASE 
        WHEN amount IS NULL OR amount < 0 THEN 'Invalid Amount'
        WHEN close_date < created_date THEN 'Invalid Dates'
        WHEN stage_name IS NULL THEN 'Missing Stage'
        ELSE 'Valid'
    END as data_quality_flag
FROM {{ source('salesforce', 'opportunity') }}
WHERE _fivetran_deleted = FALSE
```

2. **dbt Schema Tests**:
```yaml
# models/staging/schema.yml
version: 2

models:
  - name: stg_salesforce_opportunity
    columns:
      - name: id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 10000000
      - name: stage_name
        tests:
          - accepted_values:
              values: ['Prospecting', 'Qualification', 'Proposal', 'Closed Won', 'Closed Lost']
```

3. **Custom Data Quality Checks**:
```sql
-- Custom validation queries
WITH data_quality_summary AS (
    SELECT 
        COUNT(*) as total_records,
        COUNT(CASE WHEN amount IS NULL THEN 1 END) as null_amounts,
        COUNT(CASE WHEN close_date < created_date THEN 1 END) as invalid_dates,
        COUNT(CASE WHEN _fivetran_synced < CURRENT_DATE - 1 THEN 1 END) as stale_records
    FROM fivetran_salesforce.opportunity
    WHERE _fivetran_deleted = FALSE
)
SELECT 
    total_records,
    null_amounts,
    ROUND(null_amounts * 100.0 / total_records, 2) as null_amount_pct,
    invalid_dates,
    stale_records
FROM data_quality_summary;
```

### 15. How do you handle large datasets and optimize sync performance?

**Answer:**
**Performance Optimization Techniques:**

1. **Incremental Sync Configuration**:
```json
{
  "sync_mode": "incremental",
  "cursor_column": "updated_at",
  "lookback_window": "2 hours",
  "batch_size": 10000,
  "parallel_streams": 4
}
```

2. **Data Partitioning**:
```sql
-- Partition large tables by date
CREATE TABLE salesforce_opportunity_partitioned (
    id VARCHAR(18),
    name VARCHAR(255),
    amount DECIMAL(18,2),
    close_date DATE,
    _fivetran_synced TIMESTAMP
)
PARTITION BY RANGE (close_date) (
    PARTITION p2023 VALUES LESS THAN ('2024-01-01'),
    PARTITION p2024 VALUES LESS THAN ('2025-01-01')
);
```

3. **Column Selection Optimization**:
```python
# Optimize by selecting only necessary columns
column_optimization = {
    "include_only_needed": [
        "id", "name", "amount", "stage_name", 
        "close_date", "account_id"
    ],
    "exclude_system_fields": [
        "system_modstamp", "last_modified_by_id",
        "created_by_id", "last_activity_date"
    ],
    "exclude_large_text": [
        "description", "notes", "comments"
    ]
}
```

4. **Sync Scheduling**:
```python
# Optimize sync timing
sync_schedule = {
    "high_priority": {
        "frequency": "15 minutes",
        "time_window": "Business hours"
    },
    "medium_priority": {
        "frequency": "1 hour", 
        "time_window": "Extended hours"
    },
    "low_priority": {
        "frequency": "Daily",
        "time_window": "Off-peak (2-4 AM)"
    }
}
```

### 16. Describe Fivetran's security features and compliance capabilities.

**Answer:**
**Security Features:**

1. **Data Encryption**:
```python
encryption_features = {
    "in_transit": {
        "protocol": "TLS 1.2+",
        "certificates": "SSL certificates",
        "validation": "Certificate pinning"
    },
    "at_rest": {
        "algorithm": "AES-256",
        "key_management": "AWS KMS, Azure Key Vault",
        "rotation": "Automatic key rotation"
    }
}
```

2. **Network Security**:
```json
{
  "network_security": {
    "vpc_peering": "Private network connections",
    "ip_whitelisting": "Restrict source IPs",
    "private_link": "AWS PrivateLink, Azure Private Link",
    "firewall_rules": "Configurable access rules"
  }
}
```

3. **Access Control**:
```python
access_control = {
    "authentication": ["SSO", "SAML", "OAuth"],
    "authorization": "Role-based access control (RBAC)",
    "mfa": "Multi-factor authentication",
    "session_management": "Automatic session timeout"
}
```

**Compliance Certifications:**
```python
compliance_standards = {
    "soc2_type2": "Security and availability controls",
    "gdpr": "European data protection regulation",
    "hipaa": "Healthcare data protection (BAA available)",
    "iso27001": "Information security management",
    "pci_dss": "Payment card industry standards"
}
```

### 17. How do you implement disaster recovery and backup strategies with Fivetran?

**Answer:**
**Disaster Recovery Strategies:**

1. **Data Backup**:
```sql
-- Automated warehouse backups
-- Snowflake example
CREATE OR REPLACE TABLE opportunity_backup 
CLONE salesforce_opportunity;

-- Point-in-time recovery
CREATE OR REPLACE TABLE opportunity_restore 
CLONE salesforce_opportunity AT (TIMESTAMP => '2024-01-15 10:00:00');
```

2. **Multi-Region Setup**:
```python
# Multi-region configuration
disaster_recovery = {
    "primary_region": {
        "location": "us-east-1",
        "warehouse": "snowflake-primary",
        "sync_frequency": "15 minutes"
    },
    "backup_region": {
        "location": "us-west-2", 
        "warehouse": "snowflake-backup",
        "sync_frequency": "1 hour",
        "replication": "Cross-region replication"
    }
}
```

3. **Recovery Procedures**:
```python
def disaster_recovery_plan():
    return {
        "rto": "Recovery Time Objective: 4 hours",
        "rpo": "Recovery Point Objective: 1 hour",
        "steps": [
            "Assess impact and scope",
            "Switch to backup region",
            "Verify data integrity",
            "Update DNS/connection strings",
            "Resume normal operations"
        ]
    }
```

### 18. Explain how to integrate Fivetran with different data warehouse platforms.

**Answer:**
**Supported Warehouses:**

1. **Snowflake Integration**:
```sql
-- Snowflake-specific optimizations
CREATE WAREHOUSE FIVETRAN_WH 
WITH WAREHOUSE_SIZE = 'MEDIUM'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE;

-- Clustering for performance
ALTER TABLE salesforce_opportunity 
CLUSTER BY (close_date, stage_name);
```

2. **BigQuery Integration**:
```sql
-- BigQuery partitioning
CREATE TABLE `project.dataset.salesforce_opportunity`
PARTITION BY DATE(close_date)
CLUSTER BY stage_name, account_id
AS SELECT * FROM source_table;
```

3. **Redshift Integration**:
```sql
-- Redshift distribution and sort keys
CREATE TABLE salesforce_opportunity (
    id VARCHAR(18),
    name VARCHAR(255),
    amount DECIMAL(18,2),
    close_date DATE
)
DISTKEY(account_id)
SORTKEY(close_date, stage_name);
```

**Configuration Examples:**
```python
warehouse_configs = {
    "snowflake": {
        "account": "your_account.snowflakecomputing.com",
        "warehouse": "FIVETRAN_WH",
        "database": "ANALYTICS",
        "schema": "RAW_DATA"
    },
    "bigquery": {
        "project_id": "your-project",
        "dataset": "fivetran_data",
        "location": "US"
    },
    "redshift": {
        "host": "cluster.region.redshift.amazonaws.com",
        "database": "analytics",
        "schema": "fivetran"
    }
}
```

### 19. How do you handle API rate limits and source system constraints?

**Answer:**
**Rate Limit Management:**

1. **API Limit Monitoring**:
```python
# Monitor API usage
def monitor_api_limits():
    return {
        "salesforce": {
            "daily_limit": 100000,
            "current_usage": 45000,
            "remaining": 55000,
            "reset_time": "24 hours"
        },
        "hubspot": {
            "rate_limit": "100 requests/10 seconds",
            "burst_limit": 1000,
            "current_usage": 75
        }
    }
```

2. **Adaptive Sync Strategies**:
```json
{
  "rate_limit_handling": {
    "backoff_strategy": "Exponential backoff",
    "retry_attempts": 3,
    "queue_management": "Priority-based queuing",
    "load_balancing": "Distribute across time windows"
  }
}
```

3. **Source System Optimization**:
```python
# Optimize source queries
optimization_strategies = {
    "field_selection": "Sync only necessary fields",
    "date_filtering": "Use date ranges to limit data",
    "batch_sizing": "Optimize batch sizes for API",
    "parallel_processing": "Use multiple API connections",
    "caching": "Cache frequently accessed data"
}
```

### 20. Describe best practices for organizing and structuring Fivetran data in the warehouse.

**Answer:**
**Data Organization Best Practices:**

1. **Schema Structure**:
```sql
-- Recommended schema organization
CREATE SCHEMA raw_salesforce;      -- Raw Fivetran data
CREATE SCHEMA staging_salesforce;  -- Cleaned/standardized data  
CREATE SCHEMA marts_sales;         -- Business logic applied
CREATE SCHEMA metrics_sales;       -- Aggregated metrics
```

2. **Naming Conventions**:
```python
naming_conventions = {
    "raw_tables": "source_system_object (e.g., salesforce_opportunity)",
    "staging_tables": "stg_source_object (e.g., stg_salesforce_opportunity)", 
    "mart_tables": "business_domain (e.g., customer_360, sales_pipeline)",
    "metric_tables": "metric_domain (e.g., daily_sales_metrics)"
}
```

3. **dbt Project Structure**:
```
models/
├── staging/
│   ├── salesforce/
│   │   ├── stg_salesforce_opportunity.sql
│   │   ├── stg_salesforce_account.sql
│   │   └── schema.yml
│   └── hubspot/
├── intermediate/
│   ├── int_customer_touchpoints.sql
│   └── int_sales_pipeline.sql
├── marts/
│   ├── sales/
│   │   ├── customer_360.sql
│   │   └── sales_performance.sql
│   └── marketing/
└── metrics/
    ├── daily_sales_metrics.sql
    └── monthly_revenue_metrics.sql
```

4. **Data Lineage Documentation**:
```yaml
# models/marts/sales/customer_360.yml
version: 2

models:
  - name: customer_360
    description: "Complete customer view combining CRM, support, and billing data"
    columns:
      - name: customer_id
        description: "Unique customer identifier from Salesforce"
        tests:
          - unique
          - not_null
    meta:
      data_sources:
        - salesforce_account
        - salesforce_opportunity  
        - zendesk_tickets
        - stripe_customers
```

---

*Continue reading for Advanced Level Questions...*
## 🔴 Advanced Level Questions

### 21. Design a complete data architecture using Fivetran for a multi-tenant SaaS company.

**Answer:**
**Architecture Components:**
```
Data Sources → Fivetran → Data Lake → Warehouse → Analytics
     ↓             ↓          ↓         ↓          ↓
Multi-tenant → Connectors → S3/Delta → Snowflake → BI Tools
```

**Implementation:**
```python
# Multi-tenant data architecture
architecture = {
    "sources": ["Salesforce", "Stripe", "Zendesk", "Mixpanel"],
    "destinations": ["Snowflake", "S3 Data Lake"],
    "transformations": "dbt with tenant isolation",
    "security": "Row-level security by tenant_id"
}
```

### 22. How do you implement real-time analytics with Fivetran?

**Answer:**
**Real-time Setup:**
- Log-based CDC for databases
- 1-minute sync frequency for critical data
- Stream processing with Kafka integration

```sql
-- Real-time view
CREATE VIEW real_time_sales AS
SELECT 
    tenant_id,
    SUM(amount) as revenue,
    COUNT(*) as deals,
    MAX(_fivetran_synced) as last_update
FROM opportunity
WHERE _fivetran_synced >= CURRENT_TIMESTAMP - INTERVAL '5 minutes'
GROUP BY tenant_id;
```

### 23. Explain Fivetran's approach to handling complex data transformations.

**Answer:**
**Transformation Layers:**
1. **Raw Layer**: Fivetran loads unchanged data
2. **Staging Layer**: dbt models for cleaning
3. **Mart Layer**: Business logic and aggregations

```sql
-- Complex transformation example
{{ config(materialized='incremental', unique_key='customer_id') }}

WITH customer_metrics AS (
    SELECT 
        c.id as customer_id,
        SUM(o.amount) as lifetime_value,
        COUNT(DISTINCT o.id) as total_orders,
        DATEDIFF('day', c.created_date, CURRENT_DATE) as customer_age_days
    FROM {{ ref('stg_customers') }} c
    LEFT JOIN {{ ref('stg_orders') }} o ON c.id = o.customer_id
    GROUP BY c.id, c.created_date
)
SELECT * FROM customer_metrics
{% if is_incremental() %}
WHERE customer_id IN (
    SELECT DISTINCT customer_id 
    FROM {{ ref('stg_orders') }}
    WHERE _fivetran_synced >= (SELECT MAX(_fivetran_synced) FROM {{ this }})
)
{% endif %}
```

### 24. How do you handle data governance and compliance in Fivetran?

**Answer:**
**Governance Framework:**
- Data lineage tracking through dbt
- Automated PII detection and masking
- Audit logs for all data access

```python
# Compliance configuration
compliance_config = {
    "pii_detection": "Automatic field classification",
    "data_masking": "Hash sensitive fields",
    "retention_policies": "Configurable by data type",
    "audit_logging": "Complete access tracking"
}
```

### 25. Describe strategies for cost optimization at scale.

**Answer:**
**Cost Optimization Techniques:**

1. **Smart Filtering:**
```sql
-- Reduce MAR with intelligent filtering
WHERE status = 'active' 
AND last_modified_date >= '2023-01-01'
AND record_type != 'test'
```

2. **Tiered Sync Strategy:**
```python
sync_tiers = {
    "tier_1": {"frequency": "15min", "data": "critical_operational"},
    "tier_2": {"frequency": "1hour", "data": "standard_business"},
    "tier_3": {"frequency": "daily", "data": "reference_historical"}
}
```

### 26. How do you implement data quality monitoring at enterprise scale?

**Answer:**
**Quality Monitoring Framework:**

```sql
-- Automated data quality checks
WITH quality_metrics AS (
    SELECT 
        table_name,
        COUNT(*) as total_rows,
        COUNT(CASE WHEN primary_key IS NULL THEN 1 END) as null_keys,
        COUNT(DISTINCT primary_key) as unique_keys,
        MAX(_fivetran_synced) as last_sync
    FROM information_schema.tables
    WHERE schema_name LIKE 'fivetran_%'
    GROUP BY table_name
)
SELECT 
    table_name,
    CASE WHEN null_keys > 0 THEN 'FAIL' ELSE 'PASS' END as key_quality,
    CASE WHEN unique_keys != total_rows THEN 'FAIL' ELSE 'PASS' END as uniqueness,
    CASE WHEN last_sync < CURRENT_TIMESTAMP - INTERVAL '2 hours' THEN 'STALE' ELSE 'FRESH' END as freshness
FROM quality_metrics;
```

### 27. Explain Fivetran's handling of schema evolution in complex scenarios.

**Answer:**
**Schema Evolution Strategies:**
- Automatic column addition with notifications
- Backward compatibility preservation
- Version control integration for schema changes

```python
# Schema change handling
def handle_schema_change(change_type, table, column):
    if change_type == "new_column":
        return "auto_add_with_notification"
    elif change_type == "type_change":
        return "create_new_column_with_suffix"
    elif change_type == "column_dropped":
        return "mark_deprecated_keep_data"
```

### 28. How do you design disaster recovery for mission-critical data pipelines?

**Answer:**
**DR Strategy:**
- Multi-region Fivetran setup
- Cross-region warehouse replication
- Automated failover procedures

```python
# Disaster recovery configuration
dr_config = {
    "primary": {"region": "us-east-1", "rto": "15min", "rpo": "5min"},
    "secondary": {"region": "us-west-2", "rto": "1hour", "rpo": "15min"},
    "failover": "automated_with_manual_approval"
}
```

### 29. Describe advanced monitoring and alerting strategies.

**Answer:**
**Advanced Monitoring:**

```python
# Comprehensive monitoring setup
monitoring_stack = {
    "metrics": ["sync_latency", "data_volume", "error_rates"],
    "alerts": ["threshold_based", "anomaly_detection", "trend_analysis"],
    "dashboards": ["operational", "business", "executive"],
    "integrations": ["PagerDuty", "Slack", "DataDog"]
}
```

### 30. How do you optimize Fivetran for high-volume, high-velocity data scenarios?

**Answer:**
**High-Volume Optimization:**

1. **Parallel Processing:**
```json
{
  "connector_config": {
    "parallel_streams": 8,
    "batch_size": 50000,
    "compression": "gzip",
    "connection_pooling": true
  }
}
```

2. **Warehouse Optimization:**
```sql
-- Optimize for high-volume ingestion
CREATE TABLE high_volume_table (
    id BIGINT,
    data JSON,
    timestamp TIMESTAMP
)
CLUSTER BY (timestamp)
PARTITION BY DATE(timestamp);
```

---

## 🏗️ Architecture & Performance

### 31. Compare Fivetran with other ELT/ETL solutions (Stitch, Airbyte, custom solutions).

**Answer:**
**Comparison Matrix:**

| Feature | Fivetran | Stitch | Airbyte | Custom ETL |
|---------|----------|--------|---------|------------|
| **Maintenance** | Zero | Low | Medium | High |
| **Connectors** | 300+ | 100+ | 200+ | Custom |
| **Cost** | High | Medium | Low | Variable |
| **Reliability** | High | Medium | Medium | Depends |
| **Customization** | Limited | Limited | High | Full |

**When to Choose Fivetran:**
- Enterprise requirements
- Zero maintenance needed
- Budget allows premium pricing
- Need for reliable, proven connectors

### 32. Explain Fivetran's internal architecture and data flow.

**Answer:**
**Internal Architecture:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Connector     │    │  Sync Engine    │    │  Destination    │
│   Managers      │───▶│                 │───▶│   Writers       │
│                 │    │  • Scheduling   │    │                 │
│  • API Clients  │    │  • Queuing      │    │  • Batching     │
│  • CDC Readers  │    │  • Monitoring   │    │  • Compression  │
│  • File Parsers │    │  • Error Handle │    │  • Optimization │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 33. How does Fivetran handle backpressure and flow control?

**Answer:**
**Flow Control Mechanisms:**
- Adaptive batch sizing based on destination performance
- Queue management with priority levels
- Circuit breaker patterns for failing destinations

```python
# Flow control example
flow_control = {
    "batch_size": "adaptive_based_on_latency",
    "queue_depth": "max_10000_records",
    "backpressure": "exponential_backoff",
    "circuit_breaker": "fail_fast_after_3_attempts"
}
```

### 34. Describe Fivetran's approach to handling data skew and hotspots.

**Answer:**
**Skew Handling:**
- Automatic partition key detection
- Dynamic load balancing across workers
- Intelligent batching strategies

```sql
-- Detect data skew
SELECT 
    partition_key,
    COUNT(*) as record_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() as percentage
FROM large_table
GROUP BY partition_key
ORDER BY record_count DESC;
```

### 35. How do you implement custom transformations beyond dbt capabilities?

**Answer:**
**Extended Transformation Options:**

1. **External Processing:**
```python
# Post-Fivetran processing
def custom_transformation():
    # Read from warehouse
    data = warehouse.query("SELECT * FROM fivetran_table")
    
    # Apply complex logic
    processed = apply_ml_model(data)
    
    # Write back to warehouse
    warehouse.write(processed, "transformed_table")
```

2. **Webhook Integration:**
```json
{
  "webhook_config": {
    "trigger": "sync_complete",
    "endpoint": "https://api.company.com/process-data",
    "payload": {"table": "salesforce_opportunity"}
  }
}
```

---

## 🌊 Streaming & Real-time Processing

### 36. How does Fivetran support real-time data streaming?

**Answer:**
**Real-time Capabilities:**
- Log-based CDC with <1 minute latency
- Kafka integration for event streaming
- Change stream processing

```python
# Real-time configuration
realtime_config = {
    "cdc_method": "log_based",
    "latency": "< 60 seconds",
    "supported_dbs": ["PostgreSQL", "MySQL", "SQL Server"],
    "change_types": ["INSERT", "UPDATE", "DELETE"]
}
```

### 37. Explain how to integrate Fivetran with Apache Kafka.

**Answer:**
**Kafka Integration:**

```json
{
  "kafka_connector": {
    "bootstrap_servers": "kafka-cluster:9092",
    "topics": ["user_events", "transaction_events"],
    "consumer_group": "fivetran_consumer",
    "offset_management": "automatic"
  }
}
```

**Processing Pipeline:**
```
Kafka Topics → Fivetran Kafka Connector → Warehouse → Stream Processing
```

### 38. How do you handle late-arriving data in streaming scenarios?

**Answer:**
**Late Data Handling:**
- Configurable lookback windows
- Watermarking for event-time processing
- Reprocessing capabilities

```sql
-- Handle late arrivals
SELECT 
    event_time,
    user_id,
    event_type,
    _fivetran_synced
FROM events
WHERE event_time BETWEEN 
    CURRENT_TIMESTAMP - INTERVAL '1 hour' AND 
    CURRENT_TIMESTAMP + INTERVAL '5 minutes'  -- Allow 5min late arrivals
```

### 39. Describe event-driven architectures with Fivetran.

**Answer:**
**Event-Driven Pattern:**

```python
# Event-driven workflow
event_architecture = {
    "triggers": ["data_sync_complete", "schema_change", "sync_failure"],
    "actions": ["run_transformations", "send_notifications", "trigger_ml_pipeline"],
    "integration": ["AWS Lambda", "Azure Functions", "Webhooks"]
}
```

### 40. How do you implement Change Data Capture (CDC) with Fivetran?

**Answer:**
**CDC Implementation:**

1. **Database Setup:**
```sql
-- Enable CDC on PostgreSQL
SELECT pg_create_logical_replication_slot('fivetran_slot', 'pgoutput');
ALTER TABLE customers REPLICA IDENTITY FULL;
```

2. **Fivetran Configuration:**
```json
{
  "cdc_config": {
    "method": "logical_replication",
    "slot_name": "fivetran_slot",
    "publication": "fivetran_publication",
    "initial_sync": "full_table"
  }
}
```

---

## 🔧 Production & Operations

### 41. How do you implement CI/CD pipelines for Fivetran configurations?

**Answer:**
**CI/CD Implementation:**

```yaml
# .github/workflows/fivetran-deploy.yml
name: Deploy Fivetran Configuration
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy Connectors
        run: |
          curl -X POST "https://api.fivetran.com/v1/connectors" \
            -H "Authorization: Bearer ${{ secrets.FIVETRAN_API_KEY }}" \
            -d @connector-config.json
```

### 42. Describe monitoring strategies for production Fivetran deployments.

**Answer:**
**Production Monitoring:**

```python
# Comprehensive monitoring
monitoring_strategy = {
    "infrastructure": ["sync_health", "api_limits", "error_rates"],
    "data_quality": ["freshness", "completeness", "accuracy"],
    "business_impact": ["sla_compliance", "downstream_dependencies"],
    "cost_tracking": ["mar_usage", "compute_costs", "optimization_opportunities"]
}
```

### 43. How do you handle Fivetran upgrades and maintenance windows?

**Answer:**
**Maintenance Strategy:**
- Automated connector updates
- Staged rollout procedures
- Rollback capabilities

```python
# Maintenance planning
maintenance_plan = {
    "connector_updates": "automatic_with_notification",
    "schema_changes": "staged_rollout",
    "major_upgrades": "scheduled_maintenance_window",
    "rollback": "automated_within_24_hours"
}
```

### 44. Explain capacity planning for Fivetran at scale.

**Answer:**
**Capacity Planning:**

```python
# Capacity metrics
capacity_planning = {
    "data_volume": "TB per month growth rate",
    "connector_count": "New sources quarterly",
    "sync_frequency": "Real-time requirements",
    "warehouse_compute": "Peak processing needs",
    "cost_projection": "MAR growth modeling"
}
```

### 45. How do you implement data lineage tracking with Fivetran?

**Answer:**
**Lineage Implementation:**

```sql
-- Data lineage query
WITH lineage_tracking AS (
    SELECT 
        'fivetran_salesforce.opportunity' as source_table,
        'marts.customer_360' as target_table,
        'dbt_transformation' as transformation_type,
        CURRENT_TIMESTAMP as lineage_timestamp
)
SELECT * FROM lineage_tracking;
```

---

## 🎭 Scenario-Based Questions

### 46. A critical Salesforce sync has been failing for 2 hours. Walk through your troubleshooting process.

**Answer:**
**Troubleshooting Steps:**

1. **Immediate Assessment:**
```python
def troubleshoot_sync_failure():
    steps = [
        "Check Fivetran dashboard for error details",
        "Verify Salesforce API limits and permissions", 
        "Review recent schema changes",
        "Check network connectivity",
        "Examine sync logs for specific errors"
    ]
    return steps
```

2. **Resolution Actions:**
- Reset connector if authentication issue
- Adjust sync frequency if rate limited
- Contact Salesforce admin for permission issues
- Implement temporary workaround if needed

### 47. Your company is migrating from on-premise databases to cloud. How do you plan the Fivetran migration?

**Answer:**
**Migration Strategy:**

```python
migration_plan = {
    "phase_1": "Assess current data sources and volumes",
    "phase_2": "Set up parallel Fivetran connectors",
    "phase_3": "Validate data consistency",
    "phase_4": "Cutover with minimal downtime",
    "phase_5": "Decommission legacy systems"
}
```

### 48. Design a data pipeline for a real-time fraud detection system using Fivetran.

**Answer:**
**Fraud Detection Pipeline:**

```
Transaction Data → Fivetran CDC → Warehouse → ML Model → Alert System
```

**Implementation:**
```sql
-- Real-time fraud scoring
CREATE VIEW fraud_detection AS
SELECT 
    transaction_id,
    user_id,
    amount,
    merchant,
    CASE 
        WHEN amount > user_avg_amount * 5 THEN 'HIGH_RISK'
        WHEN merchant IN (SELECT merchant FROM blacklist) THEN 'HIGH_RISK'
        ELSE 'LOW_RISK'
    END as risk_score,
    _fivetran_synced
FROM transactions
WHERE _fivetran_synced >= CURRENT_TIMESTAMP - INTERVAL '5 minutes';
```

### 49. How would you handle a scenario where Fivetran costs are exceeding budget due to high MAR?

**Answer:**
**Cost Reduction Strategy:**

1. **Immediate Actions:**
```python
cost_reduction = {
    "data_filtering": "Exclude unnecessary historical data",
    "column_selection": "Sync only required fields", 
    "sync_frequency": "Reduce frequency for non-critical data",
    "archive_old_data": "Move historical data to cheaper storage"
}
```

2. **Long-term Optimization:**
- Implement data lifecycle policies
- Negotiate volume discounts
- Consider hybrid approach with custom connectors

### 50. Your team needs to ensure GDPR compliance for EU customer data. How do you configure Fivetran?

**Answer:**
**GDPR Compliance Setup:**

```python
gdpr_compliance = {
    "data_residency": "EU region deployment",
    "pii_identification": "Automatic field classification",
    "data_masking": "Hash/encrypt sensitive fields",
    "right_to_erasure": "Implement deletion workflows",
    "audit_logging": "Complete access tracking"
}
```

**Implementation:**
```sql
-- PII masking example
SELECT 
    customer_id,
    SHA2(email, 256) as email_hash,  -- Mask email
    LEFT(phone, 3) || 'XXXXX' as phone_masked,  -- Mask phone
    country,
    _fivetran_synced
FROM customers
WHERE gdpr_consent = TRUE;
```

---

**Total Questions: 50**

This comprehensive set covers all aspects of Fivetran from basic concepts to advanced production scenarios, providing thorough preparation for data engineering interviews.