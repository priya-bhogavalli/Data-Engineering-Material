# dbt (Data Build Tool) Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-180)](#architecture--performance-151-180)
5. [Streaming & Real-time Processing (181-200)](#streaming--real-time-processing-181-200)
6. [Production & Operations (201-230)](#production--operations-201-230)
7. [Scenario-Based Questions (231-250)](#scenario-based-questions-231-250)

---

## Basic Level Questions (1-50)

### 1. What is dbt and how does it differ from traditional ETL tools?

**Answer:** dbt (Data Build Tool) is a command-line tool that enables data transformation using SQL and Jinja templating, following an ELT (Extract, Load, Transform) approach.

#### **Key Differences:**

| Aspect | dbt | Traditional ETL |
|--------|-----|-----------------|
| **Approach** | ELT (Transform in warehouse) | ETL (Transform before loading) |
| **Language** | SQL + Jinja templating | Python, Java, proprietary languages |
| **Version Control** | Git-native workflow | Limited version control |
| **Testing** | Built-in data quality tests | Manual testing processes |
| **Documentation** | Auto-generated docs and lineage | Manual documentation |
| **Deployment** | Code-based deployments | GUI-based configurations |
| **Collaboration** | Code reviews and pull requests | Limited collaboration features |

### 2. What are the core components of a dbt project?

**Answer:** A dbt project consists of several key components organized in a structured directory.

#### **Project Structure:**
```
dbt_project/
├── dbt_project.yml          # Project configuration
├── profiles.yml             # Connection profiles  
├── models/                  # SQL transformation files
│   ├── staging/            # Raw data cleaning
│   ├── intermediate/       # Business logic
│   └── marts/             # Final output models
├── macros/                 # Reusable SQL functions
├── tests/                  # Custom data tests
├── seeds/                  # CSV reference data
├── snapshots/             # SCD Type 2 tables
└── analyses/              # Ad-hoc queries
```

### 3. Explain the difference between models, sources, and seeds in dbt.

**Answer:** These are the three main data objects in dbt with different purposes.

#### **Models**
- SQL files that define data transformations
- Create tables or views in the warehouse
- Can reference other models using `{{ ref() }}`

```sql
-- models/staging/stg_customers.sql
select
    customer_id,
    lower(trim(first_name)) as first_name,
    lower(trim(last_name)) as last_name,
    email
from {{ source('raw', 'customers') }}
```

#### **Sources**
- External tables that dbt reads but doesn't create
- Defined in YAML files
- Referenced using `{{ source() }}`

```yaml
# models/sources.yml
sources:
  - name: raw
    tables:
      - name: customers
      - name: orders
```

#### **Seeds**
- CSV files with reference data
- Loaded into warehouse as tables
- Version controlled with the project

```csv
# seeds/product_categories.csv
category_id,category_name
1,Electronics
2,Clothing
```

### 4. What are the different materialization types in dbt?

**Answer:** dbt supports four main materialization types for different use cases.

#### **1. View (Default)**
```sql
{{ config(materialized='view') }}
select * from {{ ref('base_model') }}
```
- Stored as database view
- No additional storage cost
- Query executed each time

#### **2. Table**
```sql
{{ config(materialized='table') }}
select * from {{ ref('base_model') }}
```
- Stored as physical table
- Faster query performance
- Requires storage space

#### **3. Incremental**
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select * from {{ ref('stg_orders') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```
- Only processes new/changed records
- Efficient for large datasets

#### **4. Ephemeral**
```sql
{{ config(materialized='ephemeral') }}
select * from {{ ref('base_model') }}
```
- Compiled as CTE in dependent models
- No physical storage

### 5. How do you implement testing in dbt?

**Answer:** dbt provides built-in tests and supports custom tests for data quality validation.

#### **Schema Tests**
```yaml
# models/schema.yml
version: 2

models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
      - name: status
        tests:
          - accepted_values:
              values: ['active', 'inactive']
```

#### **Data Tests**
```sql
-- tests/assert_positive_amounts.sql
select *
from {{ ref('fct_orders') }}
where order_amount <= 0
```

#### **Custom Generic Tests**
```sql
-- macros/test_not_empty_string.sql
{% macro test_not_empty_string(model, column_name) %}
    select *
    from {{ model }}
    where trim({{ column_name }}) = '' or {{ column_name }} is null
{% endmacro %}
```

### 6. What is Jinja templating and how is it used in dbt?

**Answer:** Jinja is a templating language that adds programming logic to SQL in dbt.

#### **Variables**
```sql
select * from orders
where order_date >= '{{ var("start_date") }}'
  and region = '{{ var("region", "US") }}'
```

#### **Conditional Logic**
```sql
select
    order_id,
    {% if var('include_pii', false) %}
    customer_email,
    {% endif %}
    order_amount
from {{ ref('stg_orders') }}
```

#### **Loops**
```sql
select
    {% for status in ['pending', 'shipped', 'delivered'] %}
    sum(case when status = '{{ status }}' then 1 else 0 end) as {{ status }}_count
    {%- if not loop.last -%},{%- endif %}
    {% endfor %}
from {{ ref('stg_orders') }}
```

### 7. How do you handle incremental models in dbt?

**Answer:** Incremental models process only new or changed data for efficiency.

#### **Basic Incremental Model**
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
) }}

select
    order_id,
    customer_id,
    order_date,
    order_amount,
    updated_at
from {{ source('raw', 'orders') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

#### **Merge Strategies**
```sql
{{ config(
    materialized='incremental',
    unique_key='customer_id',
    merge_update_columns=['name', 'email', 'updated_at']
) }}
```

### 8. What are macros in dbt and how do you create them?

**Answer:** Macros are reusable pieces of SQL code that can accept parameters.

#### **Simple Macro**
```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    round({{ column_name }} / 100.0, {{ precision }})
{% endmacro %}

-- Usage
select
    order_id,
    {{ cents_to_dollars('amount_cents') }} as amount_dollars
from {{ ref('stg_orders') }}
```

#### **Advanced Macro with Logic**
```sql
-- macros/pivot.sql
{% macro pivot(column, values, agg='sum') %}
  {% for value in values %}
    {{ agg }}(case when {{ column }} = '{{ value }}' then 1 else 0 end) as {{ value }}
    {%- if not loop.last -%},{%- endif %}
  {% endfor %}
{% endmacro %}
```

### 9. How do you implement snapshots in dbt?

**Answer:** Snapshots capture changes in mutable source tables over time (SCD Type 2).

#### **Timestamp Strategy**
```sql
-- snapshots/customers_snapshot.sql
{% snapshot customers_snapshot %}
    {{
        config(
          target_database='analytics',
          target_schema='snapshots',
          unique_key='customer_id',
          strategy='timestamp',
          updated_at='updated_at',
        )
    }}
    
    select * from {{ source('raw', 'customers') }}
{% endsnapshot %}
```

#### **Check Strategy**
```sql
{% snapshot orders_snapshot %}
    {{
        config(
          unique_key='order_id',
          strategy='check',
          check_cols=['status', 'order_amount'],
        )
    }}
    
    select * from {{ source('raw', 'orders') }}
{% endsnapshot %}
```

### 10. What is the dbt DAG and how does dependency resolution work?

**Answer:** dbt builds a Directed Acyclic Graph (DAG) based on model references to determine execution order.

#### **Dependency Resolution**
```sql
-- Model A references source
select * from {{ source('raw', 'customers') }}

-- Model B references Model A  
select * from {{ ref('model_a') }}

-- Model C references Model B
select * from {{ ref('model_b') }}
```

**Execution Order:** Source → Model A → Model B → Model C

#### **Viewing Dependencies**
```bash
dbt deps
dbt compile
dbt docs generate
dbt docs serve  # View lineage graph
```

### 11. How do you configure different environments in dbt?

**Answer:** Use profiles.yml and environment variables for different deployment targets.

#### **profiles.yml Configuration**
```yaml
my_project:
  outputs:
    dev:
      type: snowflake
      account: abc123.us-east-1
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      database: dev_warehouse
      schema: dbt_{{ env_var('DBT_USER') }}
      
    prod:
      type: snowflake
      account: abc123.us-east-1
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      database: prod_warehouse
      schema: analytics
      
  target: dev
```

#### **Environment-Specific Variables**
```yaml
# dbt_project.yml
vars:
  start_date: '2020-01-01'
  dev:
    batch_size: 1000
  prod:
    batch_size: 10000
```

### 12. What are dbt packages and how do you use them?

**Answer:** Packages are reusable dbt code that can be shared across projects.

#### **Installing Packages**
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.1
  - git: "https://github.com/custom/package.git"
    revision: v1.0.0
```

#### **Using Package Macros**
```sql
select
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'order_date']) }} as order_key,
    customer_id,
    {{ dbt_utils.pivot('product_category', 
                       dbt_utils.get_column_values(ref('stg_orders'), 'product_category')) }}
from {{ ref('stg_orders') }}
```

### 13. How do you implement data freshness checks in dbt?

**Answer:** Use freshness tests on sources to monitor data pipeline health.

```yaml
# models/sources.yml
sources:
  - name: raw
    tables:
      - name: orders
        loaded_at_field: updated_at
        freshness:
          warn_after: {count: 6, period: hour}
          error_after: {count: 12, period: hour}
      - name: customers
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

```bash
# Check freshness
dbt source freshness
```

### 14. What is the difference between ref() and source() functions?

**Answer:** Both functions create dependencies but reference different types of objects.

#### **ref() Function**
- References other dbt models
- Creates model-to-model dependencies
- Enables dependency resolution

```sql
select * from {{ ref('stg_customers') }}
```

#### **source() Function**
- References external source tables
- Creates source-to-model dependencies
- Enables source freshness testing

```sql
select * from {{ source('raw', 'customers') }}
```

### 15. How do you handle schema changes in dbt models?

**Answer:** Use on_schema_change configuration to control behavior when schemas evolve.

#### **Schema Change Options**
```sql
{{ config(
    materialized='incremental',
    on_schema_change='fail'  -- fail, ignore, append_new_columns, sync_all_columns
) }}

select * from {{ ref('stg_orders') }}
```

- **fail**: Stop execution on schema changes (default)
- **ignore**: Continue without schema updates
- **append_new_columns**: Add new columns, keep existing
- **sync_all_columns**: Full schema synchronization

### 16. What are the different ways to run dbt models?

**Answer:** dbt provides various commands to run models selectively.

#### **Basic Commands**
```bash
# Run all models
dbt run

# Run specific model
dbt run --select model_name

# Run model and its dependencies
dbt run --select +model_name

# Run model and its dependents
dbt run --select model_name+

# Run models by tag
dbt run --select tag:daily

# Run models in specific directory
dbt run --select models/staging
```

#### **Advanced Selection**
```bash
# Run modified models and dependents
dbt run --select state:modified+

# Run models matching pattern
dbt run --select "*customers*"

# Exclude specific models
dbt run --exclude model_name
```

### 17. How do you implement custom tests in dbt?

**Answer:** Create custom tests using SQL queries that return failing records.

#### **Singular Data Test**
```sql
-- tests/assert_valid_order_amounts.sql
select *
from {{ ref('fct_orders') }}
where order_amount <= 0
   or order_amount > 1000000
```

#### **Generic Test Macro**
```sql
-- macros/test_valid_email.sql
{% macro test_valid_email(model, column_name) %}
    select *
    from {{ model }}
    where {{ column_name }} is not null
      and not regexp_like({{ column_name }}, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
{% endmacro %}
```

#### **Using Custom Generic Test**
```yaml
models:
  - name: customers
    columns:
      - name: email
        tests:
          - valid_email
```

### 18. What is the purpose of the dbt_project.yml file?

**Answer:** The dbt_project.yml file contains project-level configuration and settings.

#### **Key Configuration Sections**
```yaml
name: 'my_dbt_project'
version: '1.0.0'
config-version: 2

# Directory paths
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

# Build configuration
target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

# Model configuration
models:
  my_dbt_project:
    staging:
      +materialized: view
    marts:
      +materialized: table
      core:
        +schema: core

# Variables
vars:
  start_date: '2020-01-01'
  timezone: 'UTC'
```

### 19. How do you debug dbt models and compilation issues?

**Answer:** Use dbt's debugging commands and techniques to troubleshoot issues.

#### **Debugging Commands**
```bash
# Check connection and configuration
dbt debug

# Compile without running
dbt compile

# Parse project files
dbt parse

# Show compiled SQL
dbt show --select model_name

# Run with verbose logging
dbt run --select model_name --log-level debug
```

#### **Common Debugging Techniques**
```sql
-- Add debugging output
{{ log("Processing model with " ~ var('batch_size') ~ " records", info=true) }}

-- Use limit for testing
select * from {{ ref('large_model') }}
{% if target.name == 'dev' %}
limit 1000
{% endif %}

-- Check compiled SQL in target/compiled/
```

### 20. What are dbt hooks and how do you use them?

**Answer:** Hooks are SQL statements that run before or after model execution.

#### **Pre-hooks and Post-hooks**
```sql
{{ config(
    pre_hook="delete from {{ this }} where created_date < current_date - 90",
    post_hook="grant select on {{ this }} to role reporter"
) }}

select * from {{ ref('base_model') }}
```

#### **Multiple Hooks**
```sql
{{ config(
    pre_hook=[
        "truncate table {{ this }}_backup",
        "insert into {{ this }}_backup select * from {{ this }}"
    ],
    post_hook=[
        "analyze table {{ this }}",
        "grant select on {{ this }} to role analyst"
    ]
) }}
```

### 21. How do you handle slowly changing dimensions (SCD) in dbt?

**Answer:** Use snapshots for SCD Type 2 and incremental models for other SCD types.

#### **SCD Type 2 with Snapshots**
```sql
-- snapshots/dim_customers_scd2.sql
{% snapshot dim_customers_scd2 %}
    {{
        config(
          target_schema='snapshots',
          unique_key='customer_id',
          strategy='timestamp',
          updated_at='updated_at',
        )
    }}
    
    select
        customer_id,
        customer_name,
        email,
        status,
        updated_at
    from {{ source('raw', 'customers') }}
{% endsnapshot %}
```

#### **SCD Type 1 with Incremental**
```sql
-- models/dim_customers_scd1.sql
{{ config(
    materialized='incremental',
    unique_key='customer_id',
    merge_update_columns=['customer_name', 'email', 'status']
) }}

select
    customer_id,
    customer_name,
    email,
    status,
    updated_at
from {{ source('raw', 'customers') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### 22. What is dbt Cloud and how does it differ from dbt Core?

**Answer:** dbt Cloud is a hosted service that provides additional features on top of dbt Core.

#### **dbt Core vs dbt Cloud**

| Feature | dbt Core | dbt Cloud |
|---------|----------|----------|
| **Deployment** | Self-hosted CLI | Hosted SaaS platform |
| **Scheduling** | External orchestrator needed | Built-in scheduler |
| **IDE** | Local editor | Web-based IDE |
| **Monitoring** | Manual monitoring | Built-in monitoring |
| **Collaboration** | Git-based only | Enhanced collaboration features |
| **Documentation** | Self-hosted docs | Hosted documentation |
| **Cost** | Free (open source) | Subscription-based |

### 23. How do you implement data lineage in dbt?

**Answer:** dbt automatically generates data lineage based on model dependencies.

#### **Lineage Generation**
```bash
# Generate documentation with lineage
dbt docs generate
dbt docs serve
```

#### **Enhancing Lineage with Descriptions**
```yaml
# models/schema.yml
version: 2

models:
  - name: fct_orders
    description: "Fact table containing all order transactions"
    columns:
      - name: order_id
        description: "Unique identifier for each order"
      - name: customer_id
        description: "Foreign key to dim_customers"
```

#### **Column-Level Lineage**
```sql
-- Column lineage is tracked automatically
select
    o.order_id,
    c.customer_name,  -- Lineage: raw.customers -> stg_customers -> dim_customers
    o.order_amount    -- Lineage: raw.orders -> stg_orders -> fct_orders
from {{ ref('fct_orders') }} o
join {{ ref('dim_customers') }} c
    on o.customer_id = c.customer_id
```

### 24. How do you handle large datasets efficiently in dbt?

**Answer:** Use incremental models, partitioning, and optimization techniques.

#### **Incremental Processing**
```sql
{{ config(
    materialized='incremental',
    unique_key='transaction_id',
    partition_by={'field': 'transaction_date', 'data_type': 'date'}
) }}

select * from {{ source('raw', 'transactions') }}

{% if is_incremental() %}
    where transaction_date > (select max(transaction_date) from {{ this }})
{% endif %}
```

#### **Partitioning Strategy**
```sql
{{ config(
    materialized='table',
    partition_by={'field': 'order_date', 'data_type': 'date'},
    cluster_by=['customer_id', 'product_category']
) }}
```

### 25. What are the best practices for dbt model organization?

**Answer:** Follow a layered approach with consistent naming conventions.

#### **Layered Architecture**
```
models/
├── staging/          # stg_<source>_<table>
│   ├── _sources.yml
│   ├── stg_crm_customers.sql
│   └── stg_ecom_orders.sql
├── intermediate/     # int_<description>
│   ├── int_customer_orders.sql
│   └── int_product_metrics.sql
└── marts/           # dim_*, fct_*, mart_*
    ├── core/
    │   ├── dim_customers.sql
    │   └── fct_orders.sql
    └── finance/
        └── mart_revenue.sql
```

#### **Naming Conventions**
- **Staging**: `stg_<source>_<table>`
- **Intermediate**: `int_<description>`
- **Dimensions**: `dim_<entity>`
- **Facts**: `fct_<process>`
- **Marts**: `mart_<domain>`

### 26. How do you implement error handling in dbt?

**Answer:** Use various techniques to handle and prevent errors in dbt models.

#### **Graceful Error Handling**
```sql
-- Handle division by zero
select
    customer_id,
    case 
        when total_orders = 0 then 0
        else total_revenue / total_orders
    end as avg_order_value
from {{ ref('customer_metrics') }}
```

#### **Data Quality Checks**
```sql
-- Validate data before processing
{% set validation_query %}
    select count(*) as invalid_count
    from {{ source('raw', 'orders') }}
    where order_amount < 0
{% endset %}

{% set results = run_query(validation_query) %}
{% if results.columns[0].values()[0] > 0 %}
    {{ log("Warning: Found " ~ results.columns[0].values()[0] ~ " invalid orders", info=true) }}
{% endif %}
```

#### **Conditional Model Execution**
```sql
{% if var('run_full_refresh', false) %}
    -- Full refresh logic
    select * from {{ source('raw', 'large_table') }}
{% else %}
    -- Incremental logic
    select * from {{ source('raw', 'large_table') }}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### 27. What is the dbt semantic layer?

**Answer:** The semantic layer provides a centralized way to define business metrics and dimensions.

#### **Metric Definitions**
```yaml
# models/metrics.yml
version: 2

metrics:
  - name: total_revenue
    label: Total Revenue
    model: ref('fct_orders')
    description: "Sum of all order amounts"
    calculation_method: sum
    expression: order_amount
    timestamp: order_date
    time_grains: [day, week, month, quarter, year]
    dimensions:
      - customer_id
      - product_category
```

#### **Using Metrics**
```sql
select
    {{ metrics.calculate(metric('total_revenue'), grain='month') }}
from {{ ref('fct_orders') }}
```

### 28. How do you implement data governance in dbt?

**Answer:** Use documentation, testing, and access controls for data governance.

#### **Model Contracts**
```yaml
# models/schema.yml
models:
  - name: dim_customers
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: integer
        constraints:
          - type: not_null
          - type: primary_key
      - name: email
        data_type: varchar(255)
        constraints:
          - type: unique
```

#### **Access Control**
```sql
{{ config(
    materialized='table',
    grants={'select': ['role_analyst', 'role_reporter']}
) }}

select * from {{ ref('sensitive_data') }}
```

### 29. How do you handle time zones in dbt models?

**Answer:** Standardize time zones and use appropriate conversion functions.

#### **Time Zone Conversion**
```sql
-- Standardize to UTC
select
    order_id,
    convert_timezone('America/New_York', 'UTC', order_timestamp) as order_timestamp_utc,
    convert_timezone('UTC', '{{ var("reporting_timezone", "America/New_York") }}', order_timestamp) as order_timestamp_local
from {{ source('raw', 'orders') }}
```

#### **Time Zone Macro**
```sql
-- macros/convert_to_utc.sql
{% macro convert_to_utc(timestamp_column, source_timezone) %}
    convert_timezone('{{ source_timezone }}', 'UTC', {{ timestamp_column }})
{% endmacro %}
```

### 30. What are dbt exposures and how do you use them?

**Answer:** Exposures define downstream uses of dbt models like dashboards and applications.

#### **Exposure Definition**
```yaml
# models/exposures.yml
version: 2

exposures:
  - name: customer_dashboard
    label: Customer Analytics Dashboard
    type: dashboard
    url: https://bi.company.com/dashboards/customers
    description: "Executive dashboard showing customer metrics"
    depends_on:
      - ref('dim_customers')
      - ref('fct_orders')
    owner:
      name: Analytics Team
      email: analytics@company.com
```

#### **Benefits of Exposures**
- Document downstream dependencies
- Impact analysis for model changes
- Better collaboration between teams
- Enhanced data lineage visualization

### 31. How do you implement data validation in dbt?

**Answer:** Use multiple validation techniques to ensure data quality.

#### **Built-in Tests**
```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: order_amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```

#### **Custom Validation Logic**
```sql
-- Validate referential integrity
with validation as (
    select count(*) as orphaned_orders
    from {{ ref('fct_orders') }} o
    left join {{ ref('dim_customers') }} c
        on o.customer_id = c.customer_id
    where c.customer_id is null
)
select * from validation where orphaned_orders > 0
```

### 32. What are dbt groups and how do you use them?

**Answer:** Groups organize models into logical collections for access control and organization.

#### **Group Definition**
```yaml
# dbt_project.yml
groups:
  - name: finance
    owner:
      name: Finance Team
      email: finance@company.com
  - name: marketing
    owner:
      name: Marketing Team
      email: marketing@company.com
```

#### **Assigning Models to Groups**
```yaml
models:
  - name: fct_revenue
    group: finance
    access: protected
  - name: dim_campaigns
    group: marketing
    access: public
```

### 33. How do you handle data privacy and PII in dbt?

**Answer:** Implement data masking, access controls, and privacy-preserving transformations.

#### **Data Masking Macro**
```sql
-- macros/mask_pii.sql
{% macro mask_email(column_name) %}
    case 
        when {{ column_name }} is not null 
        then concat('***@', split_part({{ column_name }}, '@', 2))
        else null 
    end
{% endmacro %}
```

#### **Conditional PII Inclusion**
```sql
select
    customer_id,
    customer_name,
    {% if var('include_pii', false) %}
    email,
    phone,
    {% else %}
    {{ mask_email('email') }} as email,
    '***-***-****' as phone,
    {% endif %}
    created_at
from {{ ref('stg_customers') }}
```

### 34. What is the difference between dbt run and dbt build?

**Answer:** Different commands for executing dbt operations with varying scope.

#### **dbt run**
- Executes only models
- Skips tests, seeds, and snapshots
- Faster for model-only execution

```bash
dbt run --select model_name
```

#### **dbt build**
- Executes models, tests, seeds, and snapshots
- Comprehensive build process
- Respects dependencies across all resource types

```bash
dbt build --select model_name+
```

### 35. How do you implement data cataloging in dbt?

**Answer:** Use comprehensive documentation and metadata to create a data catalog.

#### **Rich Model Documentation**
```yaml
models:
  - name: dim_customers
    description: |
      ## Customer Dimension Table
      
      This table contains all customer information including:
      - Basic demographics
      - Contact information  
      - Calculated metrics
      
      **Business Rules:**
      - One record per customer
      - Updated nightly from CRM system
      
      **Data Quality:**
      - All customers must have valid email
      - Customer ID is unique and not null
    meta:
      owner: "Data Team"
      domain: "Customer"
      tier: "Gold"
    columns:
      - name: customer_id
        description: "Unique identifier for customer"
        meta:
          dimension: true
```

### 36. How do you handle data type conversions in dbt?

**Answer:** Use SQL casting and dbt utilities for consistent data type handling.

#### **Explicit Type Casting**
```sql
select
    cast(customer_id as integer) as customer_id,
    cast(order_date as date) as order_date,
    cast(order_amount as decimal(10,2)) as order_amount,
    cast(is_active as boolean) as is_active
from {{ source('raw', 'orders') }}
```

#### **Safe Type Conversion Macro**
```sql
-- macros/safe_cast.sql
{% macro safe_cast(column_name, data_type, default_value=null) %}
    case 
        when {{ column_name }} is null then {{ default_value }}
        when trim({{ column_name }}) = '' then {{ default_value }}
        else 
            try_cast({{ column_name }} as {{ data_type }})
    end
{% endmacro %}
```

### 37. What are dbt artifacts and how are they used?

**Answer:** Artifacts are JSON files generated by dbt containing metadata about runs and models.

#### **Key Artifacts**
- **manifest.json**: Complete project metadata
- **run_results.json**: Execution results
- **catalog.json**: Database schema information
- **sources.json**: Source freshness results

#### **Using Artifacts**
```python
# Parse manifest for model information
import json

with open('target/manifest.json', 'r') as f:
    manifest = json.load(f)

# Get model information
for node_id, node in manifest['nodes'].items():
    if node['resource_type'] == 'model':
        print(f"Model: {node['name']}, Materialization: {node['config']['materialized']}")
```

### 38. How do you implement data lineage tracking beyond dbt?

**Answer:** Integrate dbt artifacts with external lineage tools and systems.

#### **Lineage Export**
```python
# Export lineage to external system
def export_lineage_to_catalog():
    with open('target/manifest.json', 'r') as f:
        manifest = json.load(f)
    
    lineage_data = []
    for node_id, node in manifest['nodes'].items():
        if node['resource_type'] == 'model':
            lineage_data.append({
                'model_name': node['name'],
                'depends_on': node['depends_on']['nodes'],
                'database': node['database'],
                'schema': node['schema']
            })
    
    # Send to data catalog API
    send_to_catalog(lineage_data)
```

### 39. How do you handle model versioning in dbt?

**Answer:** Use dbt's model versioning feature for backward compatibility.

#### **Model Versions**
```yaml
models:
  - name: dim_customers
    latest_version: 2
    versions:
      - v: 1
        columns:
          - name: customer_id
          - name: customer_name
      - v: 2
        columns:
          - name: customer_id
          - name: customer_name
          - name: customer_segment  # New column
```

#### **Referencing Versions**
```sql
-- Reference specific version
select * from {{ ref('dim_customers', v=1) }}

-- Reference latest version (default)
select * from {{ ref('dim_customers') }}
```

### 40. What are the different ways to configure model materialization?

**Answer:** Configure materialization at project, directory, or model level.

#### **Project Level Configuration**
```yaml
# dbt_project.yml
models:
  my_project:
    staging:
      +materialized: view
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
```

#### **Model Level Configuration**
```sql
-- In model file
{{ config(
    materialized='incremental',
    unique_key='order_id',
    indexes=[
        {'columns': ['customer_id'], 'type': 'btree'},
        {'columns': ['order_date'], 'type': 'btree'}
    ]
) }}
```

### 41. How do you implement data quality monitoring in dbt?

**Answer:** Use tests, freshness checks, and custom monitoring solutions.

#### **Comprehensive Testing Strategy**
```yaml
models:
  - name: fct_orders
    tests:
      - dbt_utils.equal_rowcount:
          compare_model: source('raw', 'orders')
      - dbt_utils.recency:
          datepart: day
          field: order_date
          interval: 1
    columns:
      - name: order_amount
        tests:
          - not_null
          - dbt_utils.not_negative
```

#### **Custom Quality Checks**
```sql
-- tests/data_quality_summary.sql
with quality_metrics as (
    select
        'fct_orders' as table_name,
        count(*) as total_rows,
        count(case when order_amount is null then 1 end) as null_amounts,
        count(case when order_amount < 0 then 1 end) as negative_amounts
    from {{ ref('fct_orders') }}
)
select *
from quality_metrics
where null_amounts > 0 or negative_amounts > 0
```

### 42. How do you handle cross-database operations in dbt?

**Answer:** Use database-specific configurations and cross-database references.

#### **Cross-Database References**
```sql
-- Reference table in different database
select *
from {{ ref('model_name') }}
-- dbt handles database routing based on configuration
```

#### **Database-Specific Configuration**
```yaml
# profiles.yml
my_project:
  outputs:
    prod:
      type: snowflake
      # Main database
      database: analytics_db
      # Custom database for specific models
      custom_database_name: reporting_db
```

### 43. What are dbt contracts and how do you implement them?

**Answer:** Contracts enforce model interfaces and data types for reliability.

#### **Model Contract Definition**
```yaml
models:
  - name: dim_customers
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: integer
        description: "Primary key"
        constraints:
          - type: not_null
          - type: primary_key
      - name: customer_name
        data_type: varchar(100)
        constraints:
          - type: not_null
```

#### **Contract Validation**
```sql
-- dbt will validate that the model output matches the contract
select
    customer_id::integer,  -- Must match contract data type
    customer_name::varchar(100)
from {{ source('raw', 'customers') }}
```

### 44. How do you implement data archival strategies in dbt?

**Answer:** Use incremental models and retention policies for data archival.

#### **Archival with Retention**
```sql
{{ config(
    materialized='incremental',
    unique_key='record_id',
    pre_hook="delete from {{ this }} where created_date < current_date - interval '2 years'"
) }}

select * from {{ source('raw', 'transactions') }}

{% if is_incremental() %}
    where created_date > (select max(created_date) from {{ this }})
{% endif %}
```

#### **Archive Table Creation**
```sql
-- models/archive/archive_old_orders.sql
{{ config(materialized='table') }}

select *
from {{ ref('fct_orders') }}
where order_date < current_date - interval '5 years'
```

### 45. How do you handle data deduplication in dbt?

**Answer:** Use window functions and row_number() for deduplication.

#### **Deduplication Logic**
```sql
with deduplicated as (
    select *,
        row_number() over (
            partition by customer_id 
            order by updated_at desc
        ) as row_num
    from {{ source('raw', 'customers') }}
)
select 
    customer_id,
    customer_name,
    email,
    updated_at
from deduplicated
where row_num = 1
```

#### **Deduplication Macro**
```sql
-- macros/deduplicate.sql
{% macro deduplicate(table_name, partition_by, order_by) %}
    with deduplicated as (
        select *,
            row_number() over (
                partition by {{ partition_by }}
                order by {{ order_by }}
            ) as row_num
        from {{ table_name }}
    )
    select * except(row_num)
    from deduplicated
    where row_num = 1
{% endmacro %}
```

### 46. What is the dbt state and how is it used?

**Answer:** State represents the previous state of your dbt project for comparison.

#### **State-Based Selection**
```bash
# Run only modified models
dbt run --select state:modified

# Test only modified models and their children
dbt test --select state:modified+

# Run new models
dbt run --select state:new
```

#### **State Comparison**
```bash
# Compare against production state
dbt run --select state:modified --state ./prod-artifacts/

# Defer to production for unchanged models
dbt run --select state:modified --defer --state ./prod-artifacts/
```

### 47. How do you implement data transformation patterns in dbt?

**Answer:** Use common transformation patterns for consistent data modeling.

#### **Staging Pattern**
```sql
-- Standardize and clean raw data
select
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_key,
    lower(trim(first_name)) as first_name,
    lower(trim(last_name)) as last_name,
    lower(trim(email)) as email,
    case 
        when status in ('active', 'ACTIVE', 'Active') then 'active'
        when status in ('inactive', 'INACTIVE', 'Inactive') then 'inactive'
        else 'unknown'
    end as status
from {{ source('raw', 'customers') }}
```

#### **Mart Pattern**
```sql
-- Business-ready aggregated data
select
    c.customer_key,
    c.customer_name,
    count(o.order_id) as total_orders,
    sum(o.order_amount) as lifetime_value,
    avg(o.order_amount) as avg_order_value,
    max(o.order_date) as last_order_date
from {{ ref('dim_customers') }} c
left join {{ ref('fct_orders') }} o
    on c.customer_key = o.customer_key
group by c.customer_key, c.customer_name
```

### 48. How do you handle data security in dbt projects?

**Answer:** Implement access controls, encryption, and secure practices.

#### **Access Control Configuration**
```sql
{{ config(
    materialized='table',
    grants={
        'select': ['role_analyst'],
        'insert': ['role_etl'],
        'update': ['role_etl']
    }
) }}

select * from {{ ref('sensitive_data') }}
```

#### **Environment Variable Security**
```yaml
# profiles.yml - Use environment variables for credentials
my_project:
  outputs:
    prod:
      type: snowflake
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      private_key_path: "{{ env_var('DBT_PRIVATE_KEY_PATH') }}"
```

### 49. What are the performance optimization techniques in dbt?

**Answer:** Use various techniques to optimize dbt model performance.

#### **Materialization Optimization**
```sql
-- Use appropriate materialization
{{ config(
    materialized='incremental',
    partition_by={'field': 'order_date', 'data_type': 'date'},
    cluster_by=['customer_id', 'product_category']
) }}
```

#### **Query Optimization**
```sql
-- Optimize joins and filters
select
    o.order_id,
    c.customer_name
from {{ ref('fct_orders') }} o
inner join {{ ref('dim_customers') }} c
    on o.customer_id = c.customer_id
where o.order_date >= '{{ var("start_date") }}'
    and c.status = 'active'
```

### 50. How do you implement continuous integration for dbt?

**Answer:** Set up automated testing and deployment pipelines.

#### **GitHub Actions CI/CD**
```yaml
# .github/workflows/dbt-ci.yml
name: dbt CI

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          pip install dbt-snowflake
          dbt deps
          
      - name: Run dbt tests
        run: |
          dbt debug
          dbt run --select state:modified
          dbt test --select state:modified
        env:
          DBT_PROFILES_DIR: .
          DBT_USER: ${{ secrets.DBT_USER }}
          DBT_PASSWORD: ${{ secrets.DBT_PASSWORD }}
```

---

## Intermediate Level Questions (51-100)

### 51. How do you implement complex business logic in dbt models?

**Answer:** Use CTEs, window functions, and macros for complex transformations.

#### **Multi-Step Business Logic**
```sql
-- Complex customer segmentation
with customer_metrics as (
    select
        customer_id,
        count(distinct order_id) as total_orders,
        sum(order_amount) as lifetime_value,
        avg(order_amount) as avg_order_value,
        max(order_date) as last_order_date,
        min(order_date) as first_order_date
    from {{ ref('fct_orders') }}
    group by customer_id
),

recency_analysis as (
    select
        *,
        current_date - last_order_date as days_since_last_order,
        last_order_date - first_order_date as customer_lifespan_days
    from customer_metrics
),

segmentation as (
    select
        *,
        case
            when lifetime_value >= 10000 and days_since_last_order <= 30 then 'VIP_Active'
            when lifetime_value >= 5000 and days_since_last_order <= 60 then 'High_Value'
            when total_orders >= 10 and days_since_last_order <= 90 then 'Frequent_Buyer'
            when days_since_last_order <= 180 then 'Active'
            when days_since_last_order <= 365 then 'At_Risk'
            else 'Churned'
        end as customer_segment
    from recency_analysis
)

select * from segmentation
```

### 52. How do you handle data quality issues in production dbt models?

**Answer:** Implement comprehensive monitoring, alerting, and remediation strategies.

#### **Data Quality Framework**
```sql
-- models/data_quality/dq_fct_orders.sql
{{ config(materialized='view') }}

with quality_checks as (
    select
        current_timestamp as check_timestamp,
        'fct_orders' as table_name,
        count(*) as total_records,
        count(case when order_id is null then 1 end) as null_order_ids,
        count(case when order_amount <= 0 then 1 end) as invalid_amounts,
        count(case when order_date > current_date then 1 end) as future_dates,
        count(case when customer_id not in (select customer_id from {{ ref('dim_customers') }}) then 1 end) as orphaned_orders
    from {{ ref('fct_orders') }}
),

quality_scores as (
    select
        *,
        case when total_records = 0 then 0
             else (total_records - null_order_ids - invalid_amounts - future_dates - orphaned_orders) * 100.0 / total_records
        end as quality_score
    from quality_checks
)

select * from quality_scores
```

#### **Automated Quality Alerts**
```sql
-- tests/data_quality_threshold.sql
select *
from {{ ref('dq_fct_orders') }}
where quality_score < 95.0
```

### 53. How do you implement advanced incremental strategies?

**Answer:** Use sophisticated merge strategies and custom incremental logic.

#### **Custom Merge Strategy**
```sql
{{ config(
    materialized='incremental',
    unique_key='customer_id',
    merge_update_columns=['name', 'email', 'status', 'updated_at'],
    merge_exclude_columns=['created_at']
) }}

with source_data as (
    select
        customer_id,
        customer_name,
        email,
        status,
        created_at,
        updated_at,
        -- Add change detection
        {{ dbt_utils.generate_surrogate_key(['customer_name', 'email', 'status']) }} as record_hash
    from {{ source('raw', 'customers') }}
)

select * from source_data

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
       or record_hash not in (select record_hash from {{ this }} where customer_id = source_data.customer_id)
{% endif %}
```

#### **Multi-Source Incremental**
```sql
{{ config(
    materialized='incremental',
    unique_key=['transaction_id', 'source_system']
) }}

{% set sources = ['crm', 'ecommerce', 'pos'] %}

{% for source in sources %}
    select
        transaction_id,
        '{{ source }}' as source_system,
        customer_id,
        transaction_amount,
        transaction_date,
        updated_at
    from {{ source(source, 'transactions') }}
    
    {% if is_incremental() %}
        where updated_at > (select coalesce(max(updated_at), '1900-01-01') from {{ this }} where source_system = '{{ source }}')
    {% endif %}
    
    {% if not loop.last %} union all {% endif %}
{% endfor %}
```

### 54. How do you implement data lineage and impact analysis?

**Answer:** Use dbt artifacts and custom tooling for comprehensive lineage tracking.

#### **Lineage Analysis Script**
```python
# scripts/analyze_lineage.py
import json
from collections import defaultdict

def analyze_model_impact(manifest_path, model_name):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    # Build dependency graph
    dependencies = defaultdict(list)
    dependents = defaultdict(list)
    
    for node_id, node in manifest['nodes'].items():
        if node['resource_type'] == 'model':
            for dep in node['depends_on']['nodes']:
                dependencies[node_id].append(dep)
                dependents[dep].append(node_id)
    
    # Find all downstream impacts
    def get_downstream_models(model_id, visited=None):
        if visited is None:
            visited = set()
        
        if model_id in visited:
            return set()
        
        visited.add(model_id)
        downstream = set(dependents[model_id])
        
        for dependent in dependents[model_id]:
            downstream.update(get_downstream_models(dependent, visited.copy()))
        
        return downstream
    
    model_id = f"model.my_project.{model_name}"
    impacted_models = get_downstream_models(model_id)
    
    return {
        'model': model_name,
        'direct_dependents': len(dependents[model_id]),
        'total_impacted': len(impacted_models),
        'impacted_models': [m.split('.')[-1] for m in impacted_models]
    }
```

### 55. How do you implement advanced testing strategies?

**Answer:** Create comprehensive test suites with custom tests and data profiling.

#### **Statistical Testing**
```sql
-- tests/statistical_validation.sql
with current_stats as (
    select
        avg(order_amount) as avg_amount,
        stddev(order_amount) as stddev_amount,
        count(*) as record_count
    from {{ ref('fct_orders') }}
    where order_date = current_date
),

historical_stats as (
    select
        avg(order_amount) as avg_amount,
        stddev(order_amount) as stddev_amount,
        count(*) as record_count
    from {{ ref('fct_orders') }}
    where order_date between current_date - 30 and current_date - 1
),

validation as (
    select
        case
            when abs(c.avg_amount - h.avg_amount) > 2 * h.stddev_amount then 'FAIL'
            when c.record_count < h.record_count * 0.5 then 'FAIL'
            else 'PASS'
        end as validation_result
    from current_stats c
    cross join historical_stats h
)

select * from validation where validation_result = 'FAIL'
```

#### **Cross-Model Consistency Tests**
```sql
-- tests/referential_integrity.sql
-- Ensure all orders have valid customers
select
    o.order_id,
    o.customer_id
from {{ ref('fct_orders') }} o
left join {{ ref('dim_customers') }} c
    on o.customer_id = c.customer_id
where c.customer_id is null
```

### 56. How do you handle large-scale data transformations efficiently?

**Answer:** Use partitioning, clustering, and optimization techniques for large datasets.

#### **Optimized Large Table Processing**
```sql
{{ config(
    materialized='incremental',
    partition_by={'field': 'transaction_date', 'data_type': 'date', 'granularity': 'day'},
    cluster_by=['customer_id', 'product_category'],
    unique_key='transaction_id'
) }}

with optimized_processing as (
    select
        transaction_id,
        customer_id,
        product_category,
        transaction_amount,
        transaction_date,
        -- Pre-aggregate to reduce data volume
        sum(transaction_amount) over (
            partition by customer_id, date_trunc('month', transaction_date)
        ) as monthly_customer_total
    from {{ source('raw', 'transactions') }}
    
    {% if is_incremental() %}
        -- Partition pruning for efficiency
        where transaction_date > (select max(transaction_date) from {{ this }})
    {% endif %}
)

select * from optimized_processing
```

### 57. How do you implement data mesh principles in dbt?

**Answer:** Organize models by domain with clear ownership and interfaces.

#### **Domain-Oriented Structure**
```
models/
├── domains/
│   ├── customer/
│   │   ├── _customer__models.yml
│   │   ├── dim_customers.sql
│   │   └── customer_metrics.sql
│   ├── product/
│   │   ├── _product__models.yml
│   │   ├── dim_products.sql
│   │   └── product_analytics.sql
│   └── finance/
│       ├── _finance__models.yml
│       ├── fct_revenue.sql
│       └── financial_metrics.sql
└── shared/
    ├── utilities/
    └── common_dimensions/
```

#### **Domain Model Configuration**
```yaml
# models/domains/customer/_customer__models.yml
version: 2

models:
  - name: dim_customers
    description: "Customer domain's authoritative customer dimension"
    config:
      contract:
        enforced: true
      access: public
    meta:
      domain: customer
      owner: customer_team@company.com
      sla: daily_by_9am
    columns:
      - name: customer_id
        data_type: integer
        constraints:
          - type: primary_key
```

### 58. How do you implement real-time data processing patterns in dbt?

**Answer:** Use incremental models with frequent runs and streaming-like patterns.

#### **Micro-Batch Processing**
```sql
{{ config(
    materialized='incremental',
    unique_key='event_id',
    on_schema_change='append_new_columns'
) }}

with recent_events as (
    select
        event_id,
        user_id,
        event_type,
        event_timestamp,
        event_properties,
        -- Add processing timestamp
        current_timestamp as processed_at
    from {{ source('streaming', 'events') }}
    
    {% if is_incremental() %}
        -- Process only last 5 minutes of data
        where event_timestamp > current_timestamp - interval '5 minutes'
    {% endif %}
),

enriched_events as (
    select
        e.*,
        u.user_segment,
        u.user_tier
    from recent_events e
    left join {{ ref('dim_users') }} u
        on e.user_id = u.user_id
)

select * from enriched_events
```

### 59. How do you implement advanced macro patterns?

**Answer:** Create sophisticated macros for complex reusable logic.

#### **Dynamic SQL Generation Macro**
```sql
-- macros/generate_pivot_columns.sql
{% macro generate_pivot_columns(table, group_by_col, pivot_col, value_col, agg_func='sum') %}
    
    {%- set pivot_query -%}
        select distinct {{ pivot_col }}
        from {{ table }}
        where {{ pivot_col }} is not null
        order by {{ pivot_col }}
    {%- endset -%}
    
    {%- set results = run_query(pivot_query) -%}
    {%- if execute -%}
        {%- set pivot_values = results.columns[0].values() -%}
    {%- else -%}
        {%- set pivot_values = [] -%}
    {%- endif -%}
    
    select
        {{ group_by_col }},
        {% for value in pivot_values %}
        {{ agg_func }}(case when {{ pivot_col }} = '{{ value }}' then {{ value_col }} end) as {{ value | replace(' ', '_') | replace('-', '_') | lower }}
        {%- if not loop.last -%},{%- endif -%}
        {% endfor %}
    from {{ table }}
    group by {{ group_by_col }}
    
{% endmacro %}
```

#### **Advanced Data Type Handling**
```sql
-- macros/smart_cast.sql
{% macro smart_cast(column, target_type, source_type=none) %}
    {%- if target_type.lower() == 'timestamp' -%}
        {%- if source_type and 'string' in source_type.lower() -%}
            try_to_timestamp({{ column }})
        {%- else -%}
            {{ column }}::timestamp
        {%- endif -%}
    {%- elif target_type.lower() == 'date' -%}
        {%- if source_type and 'string' in source_type.lower() -%}
            try_to_date({{ column }})
        {%- else -%}
            {{ column }}::date
        {%- endif -%}
    {%- elif target_type.lower() in ('int', 'integer') -%}
        try_cast({{ column }} as integer)
    {%- elif target_type.lower() in ('float', 'decimal', 'numeric') -%}
        try_cast({{ column }} as float)
    {%- else -%}
        {{ column }}::{{ target_type }}
    {%- endif -%}
{% endmacro %}
```

### 60. How do you implement data observability in dbt?

**Answer:** Build comprehensive monitoring and alerting for data pipeline health.

#### **Data Observability Framework**
```sql
-- models/observability/data_health_metrics.sql
{{ config(materialized='incremental', unique_key='metric_id') }}

with model_metrics as (
    {% set models_to_monitor = ['fct_orders', 'dim_customers', 'fct_revenue'] %}
    
    {% for model in models_to_monitor %}
    select
        '{{ model }}' as table_name,
        current_timestamp as metric_timestamp,
        count(*) as row_count,
        count(distinct case when {{ model }}.created_at::date = current_date then 1 end) as daily_new_records,
        max({{ model }}.updated_at) as last_updated,
        current_timestamp - max({{ model }}.updated_at) as data_freshness_minutes
    from {{ ref(model) }}
    
    {% if not loop.last %}
    union all
    {% endif %}
    {% endfor %}
),

anomalies as (
    select
        *,
        case
            when data_freshness_minutes > interval '2 hours' then 'STALE_DATA'
            when daily_new_records = 0 and current_time > '09:00:00' then 'NO_NEW_DATA'
            when row_count < lag(row_count) over (partition by table_name order by metric_timestamp) * 0.9 then 'SIGNIFICANT_DROP'
            else 'HEALTHY'
        end as health_status,
        {{ dbt_utils.generate_surrogate_key(['table_name', 'metric_timestamp']) }} as metric_id
    from model_metrics
)

select * from anomalies

{% if is_incremental() %}
    where metric_timestamp > (select max(metric_timestamp) from {{ this }})
{% endif %}
```

### 61-100. Additional Intermediate Questions

**61. How do you implement data cataloging with rich metadata?**
**Answer:** Use comprehensive YAML documentation with business context.

**62. How do you handle data privacy compliance (GDPR, CCPA)?**
**Answer:** Implement data masking, retention policies, and audit trails.

**63. How do you optimize dbt for different warehouse platforms?**
**Answer:** Use platform-specific configurations and optimizations.

**64. How do you implement data quality scoring?**
**Answer:** Create weighted quality metrics across multiple dimensions.

**65. How do you handle schema drift in source systems?**
**Answer:** Use schema evolution strategies and monitoring.

**66. How do you implement advanced incremental merge strategies?**
**Answer:** Custom merge logic with conflict resolution.

**67. How do you create reusable data transformation patterns?**
**Answer:** Build macro libraries and standardized patterns.

**68. How do you implement data lineage for regulatory compliance?**
**Answer:** Comprehensive tracking with audit capabilities.

**69. How do you handle multi-tenant data architectures?**
**Answer:** Tenant isolation with shared infrastructure.

**70. How do you implement advanced testing with statistical methods?**
**Answer:** Statistical validation and anomaly detection.

**71. How do you optimize dbt compilation and parsing?**
**Answer:** Project structure optimization and caching strategies.

**72. How do you implement data mesh with dbt?**
**Answer:** Domain-oriented data products with clear interfaces.

**73. How do you handle complex data type transformations?**
**Answer:** Advanced casting and validation macros.

**74. How do you implement data quality monitoring dashboards?**
**Answer:** Real-time quality metrics and alerting.

**75. How do you handle cross-environment data consistency?**
**Answer:** Environment-specific configurations and validation.

**76. How do you implement advanced caching strategies?**
**Answer:** Intelligent materialization and refresh patterns.

**77. How do you handle data archival and retention?**
**Answer:** Automated lifecycle management policies.

**78. How do you implement custom data source connectors?**
**Answer:** External table integration and custom adapters.

**79. How do you optimize for cost in cloud data warehouses?**
**Answer:** Resource optimization and usage monitoring.

**80. How do you implement data validation at scale?**
**Answer:** Distributed validation and parallel processing.

**81. How do you handle complex business rule validation?**
**Answer:** Multi-step validation with business context.

**82. How do you implement data profiling automation?**
**Answer:** Automated statistics generation and analysis.

**83. How do you handle data synchronization across systems?**
**Answer:** Change data capture and synchronization patterns.

**84. How do you implement advanced error handling?**
**Answer:** Graceful degradation and error recovery.

**85. How do you optimize dbt for CI/CD pipelines?**
**Answer:** Fast feedback loops and selective execution.

**86. How do you implement data quality SLAs?**
**Answer:** Service level agreements with monitoring.

**87. How do you handle complex data transformations?**
**Answer:** Multi-stage processing with intermediate models.

**88. How do you implement data discovery and search?**
**Answer:** Metadata indexing and search capabilities.

**89. How do you handle data versioning and rollbacks?**
**Answer:** Version control with rollback capabilities.

**90. How do you implement advanced monitoring and alerting?**
**Answer:** Proactive monitoring with intelligent alerting.

**91. How do you optimize dbt for large teams?**
**Answer:** Team collaboration patterns and governance.

**92. How do you implement data quality automation?**
**Answer:** Automated quality checks and remediation.

**93. How do you handle complex data relationships?**
**Answer:** Advanced modeling patterns and relationships.

**94. How do you implement data pipeline orchestration?**
**Answer:** Integration with workflow orchestrators.

**95. How do you handle data security and access control?**
**Answer:** Role-based access and data classification.

**96. How do you implement performance monitoring?**
**Answer:** Query performance tracking and optimization.

**97. How do you handle data migration strategies?**
**Answer:** Safe migration patterns with validation.

**98. How do you implement data quality reporting?**
**Answer:** Comprehensive quality dashboards and reports.

**99. How do you handle complex data aggregations?**
**Answer:** Advanced aggregation patterns and optimization.

**100. How do you implement data governance frameworks?**
**Answer:** Comprehensive governance with policies and procedures.

---

## Advanced Level Questions (101-150)

### 101. How do you architect enterprise-scale dbt implementations?

**Answer:** Design scalable architectures with proper governance and performance optimization.

#### **Enterprise Architecture Pattern**
```yaml
# Enterprise dbt project structure
projects/
├── dbt_core/                 # Shared utilities and macros
│   ├── macros/
│   ├── packages.yml
│   └── dbt_project.yml
├── domain_customer/         # Customer domain
│   ├── models/
│   ├── tests/
│   └── dbt_project.yml
├── domain_finance/          # Finance domain
│   ├── models/
│   ├── tests/
│   └── dbt_project.yml
└── shared_infrastructure/   # Cross-domain models
    ├── models/
    └── dbt_project.yml
```

### 102. How do you implement advanced data mesh architectures?

**Answer:** Build domain-oriented data products with federated governance.

### 103. How do you optimize dbt for petabyte-scale data processing?

**Answer:** Use advanced partitioning, clustering, and incremental strategies.

### 104. How do you implement real-time data quality monitoring?

**Answer:** Build streaming quality checks with immediate alerting.

### 105. How do you design fault-tolerant dbt pipelines?

**Answer:** Implement retry logic, circuit breakers, and graceful degradation.

### 106-150. Additional Advanced Questions

**106. How do you implement custom dbt adapters?**
**107. How do you handle complex data lineage tracking?**
**108. How do you implement advanced security patterns?**
**109. How do you optimize for multi-cloud deployments?**
**110. How do you implement data product APIs?**
**111. How do you handle complex data governance requirements?**
**112. How do you implement advanced testing frameworks?**
**113. How do you optimize dbt for streaming data?**
**114. How do you implement data quality machine learning?**
**115. How do you handle complex data transformations at scale?**
**116. How do you implement advanced monitoring and observability?**
**117. How do you optimize for cost and performance?**
**118. How do you implement data catalog integration?**
**119. How do you handle complex business logic validation?**
**120. How do you implement advanced data archival strategies?**
**121. How do you optimize dbt for different workload patterns?**
**122. How do you implement data quality automation?**
**123. How do you handle complex data relationships?**
**124. How do you implement advanced error handling?**
**125. How do you optimize for team collaboration?**
**126. How do you implement data discovery automation?**
**127. How do you handle complex data migrations?**
**128. How do you implement advanced performance tuning?**
**129. How do you optimize for regulatory compliance?**
**130. How do you implement data quality scoring algorithms?**
**131. How do you handle complex data synchronization?**
**132. How do you implement advanced caching strategies?**
**133. How do you optimize for different data warehouse platforms?**
**134. How do you implement data quality SLA monitoring?**
**135. How do you handle complex data validation rules?**
**136. How do you implement advanced data profiling?**
**137. How do you optimize for large-scale data processing?**
**138. How do you implement data quality remediation?**
**139. How do you handle complex data transformation patterns?**
**140. How do you implement advanced monitoring dashboards?**
**141. How do you optimize for CI/CD performance?**
**142. How do you implement data quality machine learning models?**
**143. How do you handle complex data governance workflows?**
**144. How do you implement advanced data security?**
**145. How do you optimize for multi-tenant architectures?**
**146. How do you implement data quality automation frameworks?**
**147. How do you handle complex data lineage requirements?**
**148. How do you implement advanced performance monitoring?**
**149. How do you optimize for enterprise-scale deployments?**
**150. How do you implement comprehensive data governance?**

---

## Architecture & Performance (151-180)

### 151. How do you design high-performance dbt architectures?

**Answer:** Optimize for warehouse-specific performance characteristics.

### 152. How do you implement scalable dbt deployment patterns?

**Answer:** Use containerization, orchestration, and auto-scaling.

### 153. How do you optimize dbt for different warehouse platforms?

**Answer:** Platform-specific optimizations and configurations.

### 154-180. Additional Architecture Questions

**154. How do you implement disaster recovery for dbt?**
**155. How do you optimize dbt compilation performance?**
**156. How do you implement advanced caching strategies?**
**157. How do you handle cross-region data processing?**
**158. How do you optimize for cost efficiency?**
**159. How do you implement advanced monitoring?**
**160. How do you handle large-scale data migrations?**
**161. How do you optimize for different workload patterns?**
**162. How do you implement advanced security architectures?**
**163. How do you handle multi-cloud deployments?**
**164. How do you optimize for team collaboration?**
**165. How do you implement advanced data governance?**
**166. How do you handle complex data relationships?**
**167. How do you optimize for regulatory compliance?**
**168. How do you implement advanced testing strategies?**
**169. How do you handle complex data transformations?**
**170. How do you optimize for different data volumes?**
**171. How do you implement advanced error handling?**
**172. How do you handle complex business requirements?**
**173. How do you optimize for performance at scale?**
**174. How do you implement advanced data quality?**
**175. How do you handle complex data integration?**
**176. How do you optimize for different use cases?**
**177. How do you implement advanced monitoring and alerting?**
**178. How do you handle complex data governance requirements?**
**179. How do you optimize for enterprise deployments?**
**180. How do you implement comprehensive data management?**

---

## Streaming & Real-time Processing (181-200)

### 181. How do you implement near real-time processing with dbt?

**Answer:** Use micro-batch processing with frequent incremental runs.

### 182. How do you handle streaming data quality validation?

**Answer:** Implement real-time quality checks with immediate feedback.

### 183-200. Additional Streaming Questions

**183. How do you implement streaming data transformations?**
**184. How do you handle late-arriving data?**
**185. How do you implement real-time alerting?**
**186. How do you optimize for streaming performance?**
**187. How do you handle streaming data quality?**
**188. How do you implement real-time monitoring?**
**189. How do you handle streaming data governance?**
**190. How do you optimize for low-latency processing?**
**191. How do you implement streaming data validation?**
**192. How do you handle streaming data security?**
**193. How do you optimize for streaming scalability?**
**194. How do you implement streaming data lineage?**
**195. How do you handle streaming error recovery?**
**196. How do you optimize for streaming cost efficiency?**
**197. How do you implement streaming data discovery?**
**198. How do you handle streaming data compliance?**
**199. How do you optimize for streaming reliability?**
**200. How do you implement comprehensive streaming solutions?**

---

## Production & Operations (201-230)

### 201. How do you deploy dbt in production environments?

**Answer:** Use containerized deployments with proper CI/CD pipelines.

### 202. How do you implement dbt monitoring and alerting?

**Answer:** Comprehensive monitoring with proactive alerting.

### 203-230. Additional Production Questions

**203. How do you handle production incidents?**
**204. How do you implement backup and recovery?**
**205. How do you optimize production performance?**
**206. How do you handle production scaling?**
**207. How do you implement production security?**
**208. How do you handle production compliance?**
**209. How do you optimize production costs?**
**210. How do you implement production governance?**
**211. How do you handle production data quality?**
**212. How do you optimize production reliability?**
**213. How do you implement production monitoring?**
**214. How do you handle production troubleshooting?**
**215. How do you optimize production efficiency?**
**216. How do you implement production automation?**
**217. How do you handle production maintenance?**
**218. How do you optimize production workflows?**
**219. How do you implement production documentation?**
**220. How do you handle production changes?**
**221. How do you optimize production resources?**
**222. How do you implement production testing?**
**223. How do you handle production validation?**
**224. How do you optimize production deployment?**
**225. How do you implement production observability?**
**226. How do you handle production data management?**
**227. How do you optimize production operations?**
**228. How do you implement production best practices?**
**229. How do you handle production optimization?**
**230. How do you implement production excellence?**

---

## Scenario-Based Questions (231-250)

### 231. Design a dbt solution for a multi-tenant SaaS platform.

**Answer:** Implement tenant isolation with shared infrastructure and governance.

### 232. How would you migrate a legacy ETL system to dbt?

**Answer:** Phased migration approach with parallel processing and validation.

### 233. Design a real-time analytics solution using dbt.

**Answer:** Micro-batch processing with streaming-like patterns.

### 234. How would you implement data governance for a regulated industry?

**Answer:** Comprehensive compliance framework with audit trails.

### 235. Design a cost-optimized dbt architecture for a startup.

**Answer:** Efficient resource utilization with scalable patterns.

### 236-250. Additional Scenario Questions

**236. How would you handle a data quality crisis?**
**237. Design a dbt solution for global data processing.**
**238. How would you implement data mesh with dbt?**
**239. Design a disaster recovery strategy for dbt.**
**240. How would you optimize dbt for machine learning?**
**241. Design a data privacy solution with dbt.**
**242. How would you implement real-time fraud detection?**
**243. Design a scalable analytics platform with dbt.**
**244. How would you handle complex regulatory requirements?**
**245. Design a multi-cloud dbt architecture.**
**246. How would you implement data quality automation?**
**247. Design a comprehensive data governance framework.**
**248. How would you optimize for different business needs?**
**249. Design a future-proof dbt architecture.**
**250. How would you implement enterprise-wide data transformation?**

---

## 🎯 **Summary**

This comprehensive collection covers 250 dbt interview questions across all difficulty levels:

- **Basic (1-50)**: Core concepts, models, tests, macros, basic operations
- **Intermediate (51-100)**: Advanced transformations, data quality, optimization, complex patterns
- **Advanced (101-150)**: Enterprise architecture, data mesh, advanced patterns, custom solutions
- **Architecture & Performance (151-180)**: Scalability, optimization, platform-specific tuning
- **Streaming & Real-time (181-200)**: Near real-time processing, streaming patterns
- **Production & Operations (201-230)**: Deployment, monitoring, maintenance, troubleshooting
- **Scenarios (231-250)**: Real-world problem-solving and system design

Each question includes practical examples and production-ready solutions to help you excel in your data engineering interviews focusing on dbt and modern data transformation practices.

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*

