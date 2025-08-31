# DBT (Data Build Tool) Interview Questions

## Table of Contents

1. [Basic DBT Concepts](#basic-dbt-concepts)
2. [Models and Transformations](#models-and-transformations)
3. [Testing and Documentation](#testing-and-documentation)
4. [Macros and Packages](#macros-and-packages)
5. [Deployment and Operations](#deployment-and-operations)
6. [Advanced Features](#advanced-features)

---

## Basic DBT Concepts

### Q1: What is DBT and how does it fit into the modern data stack?

**Answer:**
DBT (Data Build Tool) is a transformation tool that enables data analysts and engineers to transform data in their warehouse using SQL and software engineering best practices. It sits between data ingestion and data consumption layers.

**Key Features:**
- **SQL-based transformations**: Write transformations in SQL
- **Version control**: Git-based workflow for data transformations
- **Testing**: Built-in data quality testing framework
- **Documentation**: Automatic documentation generation
- **Lineage**: Data lineage tracking and visualization

**Code Example:**
```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

select
    order_id,
    customer_id,
    order_date,
    status,
    -- Clean and standardize data
    upper(trim(status)) as order_status,
    cast(order_date as date) as order_date_clean,
    -- Add metadata
    current_timestamp() as dbt_updated_at
from {{ source('raw_data', 'orders') }}
where order_date >= '2020-01-01'
```

```sql
-- models/marts/dim_customers.sql
{{ config(
    materialized='table',
    indexes=[
      {'columns': ['customer_id'], 'unique': True}
    ]
) }}

with customer_orders as (
    select
        customer_id,
        count(*) as total_orders,
        sum(order_amount) as total_spent,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date
    from {{ ref('stg_orders') }}
    group by customer_id
),

customer_info as (
    select
        customer_id,
        first_name,
        last_name,
        email,
        registration_date
    from {{ ref('stg_customers') }}
)

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.registration_date,
    coalesce(o.total_orders, 0) as total_orders,
    coalesce(o.total_spent, 0) as total_spent,
    o.first_order_date,
    o.last_order_date,
    -- Customer segmentation
    case
        when o.total_spent >= 1000 then 'High Value'
        when o.total_spent >= 500 then 'Medium Value'
        when o.total_spent > 0 then 'Low Value'
        else 'No Purchases'
    end as customer_segment
from customer_info c
left join customer_orders o using (customer_id)
```

```yaml
# dbt_project.yml
name: 'ecommerce_analytics'
version: '1.0.0'
config-version: 2

profile: 'ecommerce'

model-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
seed-paths: ["data"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  ecommerce_analytics:
    staging:
      +materialized: view
      +docs:
        node_color: "lightblue"
    marts:
      +materialized: table
      +docs:
        node_color: "green"
    
vars:
  start_date: '2020-01-01'
  timezone: 'UTC'
```

### Q2: Explain DBT's compilation and execution process.

**Answer:**
DBT compiles Jinja templates and SQL into executable SQL, then executes them in the target data warehouse. The process involves parsing, compilation, and execution phases.

**Compilation Process:**
1. **Parse**: Read project files and build dependency graph
2. **Compile**: Render Jinja templates and resolve references
3. **Execute**: Run compiled SQL in target warehouse

**Code Example:**
```sql
-- Original DBT model with Jinja
-- models/monthly_revenue.sql
{{ config(materialized='table') }}

{% set months = ['2023-01', '2023-02', '2023-03'] %}

select
    order_date,
    {% for month in months %}
    sum(case when date_trunc('month', order_date) = '{{ month }}-01' 
        then order_amount else 0 end) as revenue_{{ month | replace('-', '_') }}
    {%- if not loop.last -%},{%- endif %}
    {% endfor %}
from {{ ref('stg_orders') }}
where order_date >= '{{ var("start_date") }}'
group by order_date
```

```sql
-- Compiled SQL (target/compiled/...)
-- This is what DBT generates and executes

select
    order_date,
    sum(case when date_trunc('month', order_date) = '2023-01-01' 
        then order_amount else 0 end) as revenue_2023_01,
    sum(case when date_trunc('month', order_date) = '2023-02-01' 
        then order_amount else 0 end) as revenue_2023_02,
    sum(case when date_trunc('month', order_date) = '2023-03-01' 
        then order_amount else 0 end) as revenue_2023_03
from "analytics"."staging"."stg_orders"
where order_date >= '2020-01-01'
group by order_date
```

```bash
# DBT commands and their purposes

# Compile models without running them
dbt compile
# Output: Compiled SQL files in target/compiled/

# Run models (compile + execute)
dbt run
# Output: 
# 14:32:15  Running with dbt=1.0.0
# 14:32:15  Found 5 models, 3 tests, 0 snapshots, 0 analyses, 165 macros, 0 operations, 0 seed files, 2 sources
# 14:32:15  
# 14:32:16  Concurrency: 4 threads (target='dev')
# 14:32:16  
# 14:32:16  1 of 5 START view model staging.stg_customers ........................... [RUN]
# 14:32:16  1 of 5 OK created view model staging.stg_customers ...................... [CREATE VIEW in 0.12s]
# 14:32:16  2 of 5 START view model staging.stg_orders ............................. [RUN]
# 14:32:16  2 of 5 OK created view model staging.stg_orders ........................ [CREATE VIEW in 0.08s]
# 14:32:16  3 of 5 START table model marts.dim_customers ........................... [RUN]
# 14:32:17  3 of 5 OK created table model marts.dim_customers ...................... [CREATE TABLE in 0.45s]

# Run specific models
dbt run --models dim_customers

# Run models and downstream dependencies
dbt run --models +dim_customers+

# Test data quality
dbt test
# Output:
# 14:33:01  1 of 3 START test not_null_dim_customers_customer_id ................... [RUN]
# 14:33:01  1 of 3 PASS not_null_dim_customers_customer_id ......................... [PASS in 0.03s]
```

### Q3: How do you manage different environments (dev, staging, prod) in DBT?

**Answer:**
DBT uses profiles and targets to manage different environments, allowing the same code to run against different databases with environment-specific configurations.

**Code Example:**
```yaml
# ~/.dbt/profiles.yml
ecommerce:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xy12345.us-east-1
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: developer
      database: analytics_dev
      warehouse: compute_wh
      schema: "{{ env_var('DBT_USER') }}_dev"
      threads: 4
      keepalives_idle: 240
      
    staging:
      type: snowflake
      account: xy12345.us-east-1
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: analyst
      database: analytics_staging
      warehouse: compute_wh
      schema: staging
      threads: 8
      
    prod:
      type: snowflake
      account: xy12345.us-east-1
      user: "{{ env_var('DBT_PROD_USER') }}"
      password: "{{ env_var('DBT_PROD_PASSWORD') }}"
      role: transformer
      database: analytics_prod
      warehouse: compute_wh
      schema: prod
      threads: 16
```

```yaml
# dbt_project.yml - Environment-specific configurations
name: 'ecommerce_analytics'
version: '1.0.0'

models:
  ecommerce_analytics:
    staging:
      +materialized: view
    marts:
      +materialized: "{{ 'table' if target.name == 'prod' else 'view' }}"
      +post-hook: "{{ 'grant select on {{ this }} to role reporter' if target.name == 'prod' }}"

vars:
  # Environment-specific variables
  start_date: "{{ '2020-01-01' if target.name == 'prod' else '2023-01-01' }}"
  batch_size: "{{ 10000 if target.name == 'prod' else 1000 }}"
  
  # Feature flags
  enable_advanced_analytics: "{{ target.name in ['staging', 'prod'] }}"
  enable_pii_masking: "{{ target.name != 'dev' }}"
```

```sql
-- models/marts/fact_orders.sql - Environment-aware model
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
    
    -- Conditional PII masking based on environment
    {% if var('enable_pii_masking') %}
    'MASKED' as customer_email,
    'MASKED' as customer_phone
    {% else %}
    customer_email,
    customer_phone
    {% endif %},
    
    -- Environment-specific transformations
    {% if var('enable_advanced_analytics') %}
    {{ calculate_customer_ltv('customer_id', 'order_amount') }} as customer_ltv,
    {{ predict_churn_score('customer_id') }} as churn_score
    {% else %}
    null as customer_ltv,
    null as churn_score
    {% endif %}

from {{ ref('stg_orders') }}

{% if is_incremental() %}
    -- Only process new/updated records in incremental runs
    where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

```bash
# Environment-specific deployment commands

# Development
export DBT_USER=john_doe
export DBT_PASSWORD=dev_password
dbt run --target dev

# Staging deployment
export DBT_USER=staging_user
export DBT_PASSWORD=staging_password
dbt run --target staging --full-refresh

# Production deployment
export DBT_PROD_USER=prod_service_account
export DBT_PROD_PASSWORD=prod_password
dbt run --target prod --exclude tag:experimental

# Environment-specific testing
dbt test --target staging --store-failures
dbt test --target prod --store-failures --fail-fast
```

## Models and Transformations

### Q4: How do you implement incremental models and handle late-arriving data?

**Answer:**
Incremental models process only new or changed data to improve performance. Handling late-arriving data requires strategies like lookback windows and merge strategies.

**Code Example:**
```sql
-- models/marts/fact_daily_sales.sql
{{ config(
    materialized='incremental',
    unique_key=['date', 'product_id', 'store_id'],
    merge_update_columns=['sales_amount', 'quantity_sold', 'updated_at'],
    on_schema_change='sync_all_columns'
) }}

{% set lookback_days = 7 %}

with daily_sales as (
    select
        date(order_date) as date,
        product_id,
        store_id,
        sum(order_amount) as sales_amount,
        sum(quantity) as quantity_sold,
        count(distinct order_id) as order_count,
        current_timestamp() as updated_at
    from {{ ref('stg_orders') }}
    
    {% if is_incremental() %}
        -- Handle late-arriving data with lookback window
        where date(order_date) >= (
            select dateadd('day', -{{ lookback_days }}, max(date))
            from {{ this }}
        )
    {% else %}
        where date(order_date) >= '{{ var("start_date") }}'
    {% endif %}
    
    group by 1, 2, 3
),

-- Add business logic and enrichment
enriched_sales as (
    select
        ds.*,
        p.product_name,
        p.category,
        s.store_name,
        s.region,
        -- Calculate metrics
        case
            when ds.sales_amount > 1000 then 'High'
            when ds.sales_amount > 500 then 'Medium'
            else 'Low'
        end as sales_tier,
        
        -- Running totals (for incremental context)
        sum(ds.sales_amount) over (
            partition by ds.product_id, ds.store_id
            order by ds.date
            rows unbounded preceding
        ) as cumulative_sales
        
    from daily_sales ds
    left join {{ ref('dim_products') }} p using (product_id)
    left join {{ ref('dim_stores') }} s using (store_id)
)

select * from enriched_sales
```

```sql
-- models/staging/stg_orders_incremental.sql
-- Advanced incremental pattern with change data capture
{{ config(
    materialized='incremental',
    unique_key='order_id',
    merge_update_columns=['status', 'updated_at'],
    on_schema_change='sync_all_columns'
) }}

select
    order_id,
    customer_id,
    order_date,
    order_amount,
    status,
    created_at,
    updated_at,
    -- Add hash for change detection
    {{ dbt_utils.generate_surrogate_key([
        'order_id', 'customer_id', 'order_amount', 'status'
    ]) }} as row_hash

from {{ source('raw_data', 'orders') }}

{% if is_incremental() %}
    where 
        -- Capture new records
        created_at > (select max(created_at) from {{ this }})
        or 
        -- Capture updated records
        updated_at > (select max(updated_at) from {{ this }})
        or
        -- Handle deleted records (if using soft deletes)
        (deleted_at is not null and deleted_at > (select max(coalesce(updated_at, created_at)) from {{ this }}))
{% endif %}
```

```sql
-- macros/handle_late_data.sql
-- Custom macro for late data handling
{% macro handle_late_data(model_name, date_column, lookback_days=3) %}
    
    {% if is_incremental() %}
        -- Delete potentially stale data before inserting fresh data
        delete from {{ this }}
        where {{ date_column }} >= (
            select dateadd('day', -{{ lookback_days }}, max({{ date_column }}))
            from {{ this }}
        );
    {% endif %}
    
{% endmacro %}
```

```yaml
# models/schema.yml - Incremental model configuration
version: 2

models:
  - name: fact_daily_sales
    description: "Daily aggregated sales data with incremental processing"
    config:
      materialized: incremental
      unique_key: ['date', 'product_id', 'store_id']
      merge_update_columns: ['sales_amount', 'quantity_sold', 'updated_at']
      
    columns:
      - name: date
        description: "Sales date"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: "'2020-01-01'"
              max_value: "current_date()"
              
      - name: sales_amount
        description: "Total sales amount for the day"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              inclusive: true

    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - date
            - product_id
            - store_id
```

### Q5: How do you implement complex business logic using DBT macros?

**Answer:**
DBT macros enable reusable SQL logic, complex calculations, and dynamic SQL generation. They use Jinja templating for parameterization and conditional logic.

**Code Example:**
```sql
-- macros/business_logic.sql
-- Customer Lifetime Value calculation macro
{% macro calculate_customer_ltv(customer_id_col, order_amount_col, prediction_months=12) %}
    
    (
        select
            avg(monthly_revenue) * {{ prediction_months }}
        from (
            select
                date_trunc('month', order_date) as month,
                sum({{ order_amount_col }}) as monthly_revenue
            from {{ ref('stg_orders') }}
            where {{ customer_id_col }} = main.{{ customer_id_col }}
                and order_date >= dateadd('month', -12, current_date())
            group by 1
        ) monthly_stats
    )
    
{% endmacro %}

-- Revenue recognition macro with different methods
{% macro recognize_revenue(amount_col, start_date_col, end_date_col, method='straight_line') %}
    
    {% if method == 'straight_line' %}
        -- Straight-line revenue recognition
        {{ amount_col }} / greatest(1, datediff('day', {{ start_date_col }}, {{ end_date_col }}))
        
    {% elif method == 'milestone' %}
        -- Milestone-based recognition
        case
            when current_date() >= {{ end_date_col }} then {{ amount_col }}
            when current_date() >= {{ start_date_col }} then {{ amount_col }} * 0.5
            else 0
        end
        
    {% elif method == 'usage_based' %}
        -- Usage-based recognition (requires usage_percentage parameter)
        {{ amount_col }} * coalesce(usage_percentage, 0)
        
    {% else %}
        -- Default to immediate recognition
        {{ amount_col }}
    {% endif %}
    
{% endmacro %}

-- Dynamic pivot macro
{% macro pivot(column_name, values, agg_func='sum', then_value=1) %}
    
    {% for value in values %}
        {{ agg_func }}(
            case when {{ column_name }} = '{{ value }}'
            then {{ then_value }}
            else 0 end
        ) as {{ value | replace(' ', '_') | replace('-', '_') | lower }}
        {%- if not loop.last -%},{%- endif %}
    {% endfor %}
    
{% endmacro %}

-- Data quality check macro
{% macro data_quality_check(table_name, checks) %}
    
    select
        '{{ table_name }}' as table_name,
        current_timestamp() as check_timestamp,
        
        {% for check in checks %}
        
        {% if check.type == 'row_count' %}
        (select count(*) from {{ ref(table_name) }}) as row_count,
        case when (select count(*) from {{ ref(table_name) }}) {{ check.operator }} {{ check.threshold }}
             then 'PASS' else 'FAIL' end as row_count_status,
             
        {% elif check.type == 'null_percentage' %}
        (select 
            round(100.0 * sum(case when {{ check.column }} is null then 1 else 0 end) / count(*), 2)
         from {{ ref(table_name) }}) as {{ check.column }}_null_pct,
        case when (select 
                    100.0 * sum(case when {{ check.column }} is null then 1 else 0 end) / count(*)
                   from {{ ref(table_name) }}) {{ check.operator }} {{ check.threshold }}
             then 'PASS' else 'FAIL' end as {{ check.column }}_null_status,
             
        {% elif check.type == 'freshness' %}
        (select max({{ check.column }}) from {{ ref(table_name) }}) as latest_{{ check.column }},
        case when (select max({{ check.column }}) from {{ ref(table_name) }}) >= 
                  dateadd('{{ check.interval }}', -{{ check.count }}, current_timestamp())
             then 'PASS' else 'FAIL' end as {{ check.column }}_freshness_status
        {% endif %}
        
        {%- if not loop.last -%},{%- endif %}
        {% endfor %}
    
{% endmacro %}
```

```sql
-- models/marts/customer_analytics.sql - Using business logic macros
select
    customer_id,
    first_name,
    last_name,
    registration_date,
    
    -- Use LTV calculation macro
    {{ calculate_customer_ltv('customer_id', 'order_amount', 24) }} as predicted_24m_ltv,
    
    -- Use pivot macro for order status distribution
    {{ pivot('order_status', ['completed', 'pending', 'cancelled'], 'count') }},
    
    -- Revenue recognition for subscription customers
    {{ recognize_revenue('subscription_amount', 'subscription_start', 'subscription_end', 'straight_line') }} as daily_recognized_revenue,
    
    -- Customer segmentation using custom logic
    case
        when {{ calculate_customer_ltv('customer_id', 'order_amount', 12) }} > 1000 then 'High Value'
        when total_orders >= 5 then 'Loyal'
        when days_since_last_order <= 30 then 'Active'
        else 'At Risk'
    end as customer_segment

from {{ ref('dim_customers') }}
```

```sql
-- models/quality/data_quality_report.sql - Using quality check macro
{{ config(materialized='table') }}

{{ data_quality_check('dim_customers', [
    {'type': 'row_count', 'operator': '>', 'threshold': 1000},
    {'type': 'null_percentage', 'column': 'email', 'operator': '<', 'threshold': 5},
    {'type': 'freshness', 'column': 'updated_at', 'interval': 'hour', 'count': 24}
]) }}

union all

{{ data_quality_check('fact_orders', [
    {'type': 'row_count', 'operator': '>', 'threshold': 10000},
    {'type': 'null_percentage', 'column': 'order_amount', 'operator': '=', 'threshold': 0},
    {'type': 'freshness', 'column': 'order_date', 'interval': 'day', 'count': 1}
]) }}
```

```sql
-- macros/generate_schema_name.sql - Custom schema naming
{% macro generate_schema_name(custom_schema_name, node) -%}
    
    {%- set default_schema = target.schema -%}
    
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
        
    {%- elif target.name == 'prod' -%}
        {{ custom_schema_name | trim }}
        
    {%- else -%}
        {{ default_schema }}_{{ custom_schema_name | trim }}
        
    {%- endif -%}
    
{%- endmacro %}

-- macros/post_hook_grants.sql - Automatic permission management
{% macro grant_select_on_schemas(schemas, role) %}
    
    {% for schema in schemas %}
        {% set grant_sql %}
            grant usage on schema {{ schema }} to role {{ role }};
            grant select on all tables in schema {{ schema }} to role {{ role }};
            grant select on all views in schema {{ schema }} to role {{ role }};
        {% endset %}
        
        {% if execute %}
            {% do run_query(grant_sql) %}
        {% endif %}
    {% endfor %}
    
{% endmacro %}
```

## Testing and Documentation

### Q6: How do you implement comprehensive data testing in DBT?

**Answer:**
DBT provides built-in tests, custom tests, and integration with external testing frameworks. Comprehensive testing includes schema tests, data tests, and business logic validation.

**Code Example:**
```yaml
# models/schema.yml - Comprehensive testing configuration
version: 2

sources:
  - name: raw_data
    description: "Raw data from operational systems"
    tables:
      - name: orders
        description: "Raw order data"
        columns:
          - name: order_id
            tests:
              - not_null
              - unique
          - name: order_date
            tests:
              - not_null
        tests:
          - dbt_utils.expression_is_true:
              expression: "order_amount >= 0"
          - dbt_utils.recency:
              datepart: day
              field: order_date
              interval: 1

models:
  - name: dim_customers
    description: "Customer dimension table"
    columns:
      - name: customer_id
        description: "Unique customer identifier"
        tests:
          - not_null
          - unique
          
      - name: email
        description: "Customer email address"
        tests:
          - not_null
          - dbt_utils.not_empty_string
          - dbt_expectations.expect_column_values_to_match_regex:
              regex: '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
              
      - name: registration_date
        description: "Date customer registered"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: "'2020-01-01'"
              max_value: "current_date()"
              
      - name: customer_segment
        description: "Customer value segment"
        tests:
          - accepted_values:
              values: ['High Value', 'Medium Value', 'Low Value', 'No Purchases']
              
    tests:
      # Custom business logic tests
      - assert_customer_email_unique
      - assert_high_value_customers_have_orders
      - dbt_utils.equal_rowcount:
          compare_model: ref('stg_customers')

  - name: fact_orders
    description: "Order fact table"
    tests:
      # Referential integrity tests
      - dbt_utils.relationships_where:
          to: ref('dim_customers')
          field: customer_id
          from_condition: customer_id is not null
      
      # Data freshness test
      - dbt_utils.recency:
          datepart: hour
          field: created_at
          interval: 24
      
      # Business rule tests
      - assert_order_amount_positive
      - assert_completed_orders_have_payment
```

```sql
-- tests/assert_customer_email_unique.sql - Custom singular test
select
    email,
    count(*) as email_count
from {{ ref('dim_customers') }}
where email is not null
group by email
having count(*) > 1
```

```sql
-- tests/assert_high_value_customers_have_orders.sql
-- Business logic test
with high_value_customers as (
    select customer_id
    from {{ ref('dim_customers') }}
    where customer_segment = 'High Value'
),

customer_orders as (
    select distinct customer_id
    from {{ ref('fact_orders') }}
)

select
    hvc.customer_id
from high_value_customers hvc
left join customer_orders co using (customer_id)
where co.customer_id is null
```

```sql
-- tests/generic/assert_order_amount_positive.sql - Generic test
select *
from {{ ref('fact_orders') }}
where order_amount <= 0
```

```sql
-- macros/test_utils.sql - Custom test macros
{% test assert_recent_data(model, column_name, days_threshold=1) %}
    
    select *
    from {{ model }}
    where {{ column_name }} < dateadd('day', -{{ days_threshold }}, current_date())
    
{% endtest %}

{% test assert_no_gaps_in_sequence(model, column_name) %}
    
    with sequence_check as (
        select
            {{ column_name }},
            lag({{ column_name }}) over (order by {{ column_name }}) as prev_value,
            {{ column_name }} - lag({{ column_name }}) over (order by {{ column_name }}) as gap
        from {{ model }}
    )
    
    select *
    from sequence_check
    where gap > 1
    
{% endtest %}

{% test assert_percentage_range(model, column_name, min_pct=0, max_pct=100) %}
    
    select *
    from {{ model }}
    where {{ column_name }} < {{ min_pct }} or {{ column_name }} > {{ max_pct }}
    
{% endtest %}
```

```yaml
# Custom test usage in schema.yml
models:
  - name: daily_metrics
    tests:
      - assert_recent_data:
          column_name: metric_date
          days_threshold: 2
      - assert_no_gaps_in_sequence:
          column_name: day_number
          
    columns:
      - name: conversion_rate
        tests:
          - assert_percentage_range:
              min_pct: 0
              max_pct: 100
```

```python
# tests/python/test_business_logic.py - Python tests for complex logic
import pytest
from dbt.cli.main import dbtRunner

class TestBusinessLogic:
    
    def test_customer_ltv_calculation(self):
        """Test customer LTV calculation logic"""
        dbt = dbtRunner()
        
        # Run specific model
        res = dbt.invoke(['run', '--models', 'customer_ltv_test'])
        assert res.success
        
        # Run tests
        res = dbt.invoke(['test', '--models', 'customer_ltv_test'])
        assert res.success
    
    def test_revenue_recognition(self):
        """Test revenue recognition logic"""
        dbt = dbtRunner()
        
        # Test different recognition methods
        for method in ['straight_line', 'milestone', 'usage_based']:
            res = dbt.invoke([
                'run', 
                '--models', 'revenue_recognition_test',
                '--vars', f'{{"recognition_method": "{method}"}}'
            ])
            assert res.success
    
    def test_data_quality_thresholds(self):
        """Test data quality meets business thresholds"""
        dbt = dbtRunner()
        
        # Run data quality tests
        res = dbt.invoke(['test', '--models', 'tag:data_quality'])
        
        # Check specific quality metrics
        if not res.success:
            # Log detailed failure information
            pytest.fail("Data quality tests failed")
```

```bash
# Testing commands and workflows

# Run all tests
dbt test
# Output:
# 14:45:23  Running with dbt=1.0.0
# 14:45:23  Found 12 models, 25 tests, 0 snapshots, 0 analyses, 165 macros
# 14:45:23  
# 14:45:24  Concurrency: 4 threads (target='dev')
# 14:45:24  
# 14:45:24  1 of 25 START test not_null_dim_customers_customer_id .................. [RUN]
# 14:45:24  1 of 25 PASS not_null_dim_customers_customer_id ...................... [PASS in 0.03s]

# Run tests for specific models
dbt test --models dim_customers

# Run tests and store failures for investigation
dbt test --store-failures

# Run only custom tests
dbt test --models test_type:singular

# Run tests with specific tags
dbt test --models tag:data_quality

# Fail fast on first test failure
dbt test --fail-fast

# Generate and serve documentation with test results
dbt docs generate
dbt docs serve
```

---

## Key Takeaways

1. **SQL-First Approach**: DBT enables analytics engineering using familiar SQL syntax
2. **Version Control**: Git-based workflow brings software engineering practices to data
3. **Testing Framework**: Comprehensive testing ensures data quality and business logic
4. **Documentation**: Automatic documentation generation improves data discovery
5. **Incremental Processing**: Efficient handling of large datasets with incremental models
6. **Environment Management**: Consistent deployment across dev, staging, and production
7. **Macro System**: Reusable SQL logic through Jinja templating
8. **Lineage Tracking**: Visual representation of data dependencies and transformations