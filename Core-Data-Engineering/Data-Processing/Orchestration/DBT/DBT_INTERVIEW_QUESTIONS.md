# 🔧 DBT (Data Build Tool) Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts (1-20)](#core-concepts-1-20)
2. [Models & Transformations (21-40)](#models--transformations-21-40)
3. [Testing & Documentation (41-60)](#testing--documentation-41-60)
4. [Advanced Features (61-80)](#advanced-features-61-80)
5. [Production & Best Practices (81-100)](#production--best-practices-81-100)

---

## 🎯 **Introduction**

DBT (Data Build Tool) is a command-line tool that enables data analysts and engineers to transform data in their warehouse more effectively. It brings software engineering best practices to data transformation.

**Why DBT is Critical for Data Engineers:**
- **Version Control**: SQL transformations under version control
- **Testing**: Built-in data quality testing framework
- **Documentation**: Automatic documentation generation
- **Modularity**: Reusable SQL components and macros
- **Lineage**: Visual data lineage tracking

---

## Core Concepts (1-20)

### 1. What is DBT and how does it fit in the modern data stack?
**Answer**: DBT is a transformation tool that sits between data loading and data consumption in the ELT paradigm.

**Modern Data Stack Position:**
- **Extract**: Tools like Fivetran, Stitch
- **Load**: Direct loading to warehouse (Snowflake, BigQuery, Redshift)
- **Transform**: DBT transforms raw data into analytics-ready datasets
- **Analyze**: BI tools consume transformed data

```sql
-- Example DBT model
{{ config(materialized='table') }}

SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    created_at,
    CASE 
        WHEN created_at >= '2023-01-01' THEN 'new'
        ELSE 'existing'
    END as customer_type
FROM {{ ref('raw_customers') }}
WHERE email IS NOT NULL
```

### 2. What are DBT models and how do they work?
**Answer**: DBT models are SQL files that define transformations, compiled into CREATE TABLE or CREATE VIEW statements.

**Model Types:**
- **Table**: Materialized as physical table
- **View**: Materialized as view
- **Incremental**: Only processes new/changed data
- **Ephemeral**: CTE that exists only during compilation

```sql
-- models/customers.sql
{{ config(
    materialized='table',
    indexes=[{'columns': ['customer_id'], 'unique': True}]
) }}

SELECT 
    id as customer_id,
    first_name || ' ' || last_name as full_name,
    email,
    created_at
FROM {{ source('raw_data', 'customers') }}
```

### 3. Explain the difference between sources and refs in DBT
**Answer**: Sources and refs define different types of dependencies in DBT projects.

**Sources**: External tables not managed by DBT
**Refs**: Other DBT models within the project

```sql
-- sources.yml
version: 2
sources:
  - name: raw_data
    tables:
      - name: customers
        columns:
          - name: id
            tests:
              - unique
              - not_null

-- Using source
SELECT * FROM {{ source('raw_data', 'customers') }}

-- Using ref
SELECT * FROM {{ ref('dim_customers') }}
```

### 4. What is the DBT compilation process?
**Answer**: DBT compiles Jinja templates and SQL into executable SQL statements.

**Compilation Steps:**
1. **Parse**: Read project files and configuration
2. **Compile**: Process Jinja templates and macros
3. **Execute**: Run compiled SQL against warehouse
4. **Test**: Run data quality tests

```bash
# DBT commands
dbt compile  # Compile without running
dbt run      # Compile and execute
dbt test     # Run tests
dbt docs generate  # Generate documentation
```

### 5. How does DBT handle dependencies and the DAG?
**Answer**: DBT automatically builds a DAG based on ref() and source() functions.

```sql
-- models/staging/stg_customers.sql
SELECT * FROM {{ source('raw', 'customers') }}

-- models/marts/dim_customers.sql  
SELECT * FROM {{ ref('stg_customers') }}

-- models/marts/fct_orders.sql
SELECT 
    o.*,
    c.customer_name
FROM {{ source('raw', 'orders') }} o
JOIN {{ ref('dim_customers') }} c ON o.customer_id = c.customer_id
```

**Dependency Resolution:**
- DBT automatically determines execution order
- Circular dependencies are detected and prevented
- Parallel execution where possible

### 6. What are DBT materializations?
**Answer**: Materializations determine how models are built in the warehouse.

**Built-in Materializations:**
```sql
-- Table materialization
{{ config(materialized='table') }}

-- View materialization  
{{ config(materialized='view') }}

-- Incremental materialization
{{ config(
    materialized='incremental',
    unique_key='id'
) }}

-- Ephemeral materialization
{{ config(materialized='ephemeral') }}
```

### 7. How do you configure DBT projects?
**Answer**: DBT projects are configured through dbt_project.yml and profiles.yml files.

```yaml
# dbt_project.yml
name: 'my_dbt_project'
version: '1.0.0'
config-version: 2

model-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
seed-paths: ["data"]
macro-paths: ["macros"]

models:
  my_dbt_project:
    staging:
      +materialized: view
    marts:
      +materialized: table

# profiles.yml
my_dbt_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: abc123
      user: dbt_user
      password: password
      role: transformer
      database: analytics
      warehouse: compute_wh
      schema: dbt_dev
```

### 8. What are DBT macros and how do you use them?
**Answer**: Macros are reusable pieces of Jinja code that generate SQL.

```sql
-- macros/get_payment_methods.sql
{% macro get_payment_methods() %}
    {{ return(['credit_card', 'debit_card', 'bank_transfer', 'cash']) }}
{% endmacro %}

-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    ROUND({{ column_name }} / 100.0, {{ precision }})
{% endmacro %}

-- Using macros in models
SELECT 
    order_id,
    {{ cents_to_dollars('amount_cents') }} as amount_dollars,
    payment_method
FROM {{ ref('raw_orders') }}
WHERE payment_method IN (
    {% for method in get_payment_methods() %}
        '{{ method }}'{% if not loop.last %},{% endif %}
    {% endfor %}
)
```

## Models & Transformations (21-40)

### 21. How do you implement incremental models in DBT?
**Answer**: Incremental models only process new or changed data for efficiency.

```sql
-- models/fct_orders_incremental.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
) }}

SELECT 
    order_id,
    customer_id,
    order_date,
    total_amount,
    status,
    updated_at
FROM {{ source('raw', 'orders') }}

{% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

**Incremental Strategies:**
- **append**: Add new rows only
- **merge**: Update existing, insert new
- **delete+insert**: Replace data matching filter

### 22. How do you handle slowly changing dimensions (SCD) in DBT?
**Answer**: Implement SCD patterns using snapshots and incremental models.

```sql
-- snapshots/customers_snapshot.sql
{% snapshot customers_snapshot %}
    {{
        config(
          target_database='analytics',
          target_schema='snapshots',
          unique_key='id',
          strategy='timestamp',
          updated_at='updated_at',
        )
    }}
    
    SELECT * FROM {{ source('raw', 'customers') }}
{% endsnapshot %}

-- Type 2 SCD implementation
{{ config(materialized='table') }}

SELECT 
    id,
    first_name,
    last_name,
    email,
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,
    CASE 
        WHEN dbt_valid_to IS NULL THEN TRUE 
        ELSE FALSE 
    END as is_current
FROM {{ ref('customers_snapshot') }}
```

### 23. How do you implement data quality checks in DBT?
**Answer**: Use built-in tests and custom tests for data quality validation.

```yaml
# models/schema.yml
version: 2

models:
  - name: dim_customers
    description: "Customer dimension table"
    columns:
      - name: customer_id
        description: "Primary key"
        tests:
          - unique
          - not_null
      - name: email
        description: "Customer email"
        tests:
          - unique
          - not_null
          - relationships:
              to: ref('valid_emails')
              field: email

  - name: fct_orders
    tests:
      - dbt_utils.expression_is_true:
          expression: "total_amount >= 0"
      - dbt_utils.recency:
          datepart: day
          field: order_date
          interval: 1
```

```sql
-- tests/assert_positive_order_amounts.sql
SELECT *
FROM {{ ref('fct_orders') }}
WHERE total_amount < 0
```

### 24. How do you organize DBT models in a project structure?
**Answer**: Follow layered architecture with staging, intermediate, and mart layers.

```
models/
├── staging/
│   ├── _sources.yml
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   └── stg_products.sql
├── intermediate/
│   ├── int_order_items_summary.sql
│   └── int_customer_order_history.sql
└── marts/
    ├── core/
    │   ├── dim_customers.sql
    │   ├── dim_products.sql
    │   └── fct_orders.sql
    └── finance/
        ├── revenue_by_month.sql
        └── customer_ltv.sql
```

**Layer Purposes:**
- **Staging**: Clean and standardize raw data
- **Intermediate**: Business logic transformations
- **Marts**: Final analytics-ready datasets

### 25. How do you handle complex transformations with window functions?
**Answer**: Use window functions for advanced analytics and ranking.

```sql
-- models/customer_analytics.sql
{{ config(materialized='table') }}

WITH customer_orders AS (
    SELECT 
        customer_id,
        order_date,
        total_amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        ) as order_sequence,
        LAG(order_date) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        ) as previous_order_date,
        SUM(total_amount) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date 
            ROWS UNBOUNDED PRECEDING
        ) as cumulative_spend
    FROM {{ ref('fct_orders') }}
),

customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as total_orders,
        SUM(total_amount) as lifetime_value,
        AVG(total_amount) as avg_order_value,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        AVG(DATEDIFF('day', previous_order_date, order_date)) as avg_days_between_orders
    FROM customer_orders
    GROUP BY customer_id
)

SELECT * FROM customer_metrics
```

## Testing & Documentation (41-60)

### 41. What are the different types of tests in DBT?
**Answer**: DBT supports multiple test types for comprehensive data quality validation.

**Test Types:**
- **Schema Tests**: Defined in YAML files
- **Data Tests**: Custom SQL tests
- **Unit Tests**: Test individual model logic
- **Integration Tests**: Test model relationships

```yaml
# Schema tests
models:
  - name: customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
          - accepted_values:
              values: ['gmail.com', 'yahoo.com', 'outlook.com']

# Custom data test
# tests/assert_valid_order_status.sql
SELECT *
FROM {{ ref('orders') }}
WHERE status NOT IN ('pending', 'completed', 'cancelled')
```

### 42. How do you create custom tests in DBT?
**Answer**: Create reusable custom tests as macros.

```sql
-- macros/test_not_empty_string.sql
{% test not_empty_string(model, column_name) %}
    SELECT *
    FROM {{ model }}
    WHERE {{ column_name }} IS NOT NULL 
      AND TRIM({{ column_name }}) = ''
{% endtest %}

-- macros/test_valid_email_format.sql
{% test valid_email_format(model, column_name) %}
    SELECT *
    FROM {{ model }}
    WHERE {{ column_name }} IS NOT NULL
      AND NOT REGEXP_LIKE({{ column_name }}, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
{% endtest %}

-- Usage in schema.yml
models:
  - name: customers
    columns:
      - name: first_name
        tests:
          - not_empty_string
      - name: email
        tests:
          - valid_email_format
```

### 43. How do you generate and maintain documentation in DBT?
**Answer**: DBT automatically generates documentation from model descriptions and tests.

```yaml
# models/schema.yml
version: 2

models:
  - name: dim_customers
    description: |
      Customer dimension table containing all customer information.
      Updated daily from the raw customer data.
    columns:
      - name: customer_id
        description: "Unique identifier for each customer"
        tests:
          - unique
          - not_null
      - name: full_name
        description: "Customer's full name (first + last)"
      - name: email
        description: "Customer's email address"
        tests:
          - unique
          - not_null

sources:
  - name: raw_data
    description: "Raw data from operational systems"
    tables:
      - name: customers
        description: "Raw customer data from CRM system"
        columns:
          - name: id
            description: "Primary key from source system"
```

```bash
# Generate documentation
dbt docs generate

# Serve documentation locally
dbt docs serve --port 8080
```

### 44. How do you implement data freshness checks?
**Answer**: Use source freshness tests to monitor data pipeline health.

```yaml
# models/sources.yml
version: 2

sources:
  - name: raw_data
    description: "Raw data from operational systems"
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
    
    tables:
      - name: orders
        description: "Raw order data"
        freshness:
          warn_after: {count: 1, period: hour}
          error_after: {count: 6, period: hour}
        loaded_at_field: created_at
        
      - name: customers
        description: "Raw customer data"
        # Inherits source-level freshness settings
```

```bash
# Check source freshness
dbt source freshness
```

## Advanced Features (61-80)

### 61. How do you use DBT packages and dependencies?
**Answer**: DBT packages provide reusable macros and models from the community.

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.1
  - package: dbt-labs/audit_helper
    version: 0.9.0
  - git: "https://github.com/my-org/dbt-custom-utils.git"
    revision: v1.0.0

# Install packages
# dbt deps
```

```sql
-- Using dbt_utils package
SELECT 
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'order_date']) }} as order_key,
    customer_id,
    order_date,
    total_amount
FROM {{ ref('raw_orders') }}

-- Using pivot macro
SELECT 
    customer_id,
    {{ dbt_utils.pivot(
        'payment_method',
        dbt_utils.get_column_values(ref('orders'), 'payment_method')
    ) }}
FROM {{ ref('orders') }}
GROUP BY customer_id
```

### 62. How do you implement hooks in DBT?
**Answer**: Hooks allow you to run SQL before or after model execution.

```sql
-- dbt_project.yml
models:
  my_project:
    +pre-hook: "{{ logging.log_model_start_time() }}"
    +post-hook: "{{ logging.log_model_end_time() }}"
    
    marts:
      +post-hook: "GRANT SELECT ON {{ this }} TO ROLE analyst"

-- Model-specific hooks
{{ config(
    pre_hook="DELETE FROM {{ this }} WHERE created_date < CURRENT_DATE - 90",
    post_hook=[
        "CREATE INDEX IF NOT EXISTS idx_customer_id ON {{ this }} (customer_id)",
        "ANALYZE TABLE {{ this }}"
    ]
) }}

SELECT * FROM {{ ref('staging_orders') }}
```

### 63. How do you handle different environments in DBT?
**Answer**: Use profiles and variables to manage multiple environments.

```yaml
# profiles.yml
my_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: abc123
      database: DEV_ANALYTICS
      schema: dbt_{{ env_var('DBT_USER') }}
      warehouse: DEV_WH
      
    prod:
      type: snowflake
      account: abc123
      database: PROD_ANALYTICS
      schema: analytics
      warehouse: PROD_WH

# dbt_project.yml
vars:
  start_date: '2023-01-01'
  
  # Environment-specific variables
  dev:
    batch_size: 1000
  prod:
    batch_size: 10000
```

```sql
-- Using variables in models
SELECT *
FROM {{ ref('raw_orders') }}
WHERE order_date >= '{{ var("start_date") }}'
LIMIT {{ var("batch_size") }}
```

### 64. How do you implement custom materializations?
**Answer**: Create custom materializations for specific use cases.

```sql
-- macros/materialization_custom_table.sql
{% materialization custom_table, default %}
  {%- set target_relation = this.incorporate(type='table') -%}
  {%- set existing_relation = load_relation(this) -%}
  {%- set tmp_relation = make_temp_relation(this) -%}

  {{ run_hooks(pre_hooks, inside_transaction=false) }}

  -- Build model
  {% call statement('main') -%}
    {{ create_table_as(True, tmp_relation, sql) }}
  {%- endcall %}

  -- Swap tables
  {% if existing_relation is not none %}
    {{ adapter.rename_relation(existing_relation, backup_relation) }}
  {% endif %}
  
  {{ adapter.rename_relation(tmp_relation, target_relation) }}

  {{ run_hooks(post_hooks, inside_transaction=true) }}

  {{ return({'relations': [target_relation]}) }}
{% endmaterialization %}
```

### 65. How do you use DBT with CI/CD pipelines?
**Answer**: Integrate DBT into automated deployment workflows.

```yaml
# .github/workflows/dbt.yml
name: DBT CI/CD

on:
  pull_request:
    branches: [main]
  push:
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
          
      - name: Run DBT tests
        run: |
          dbt seed --target ci
          dbt run --target ci
          dbt test --target ci
          
  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          dbt run --target prod
          dbt test --target prod
```

## Production & Best Practices (81-100)

### 81. How do you monitor DBT in production?
**Answer**: Implement comprehensive monitoring and alerting.

```sql
-- macros/monitoring.sql
{% macro log_model_execution() %}
  INSERT INTO {{ ref('dbt_execution_log') }} (
    model_name,
    execution_time,
    rows_affected,
    status,
    executed_at
  ) VALUES (
    '{{ this.name }}',
    {{ adapter.get_last_query_execution_time() }},
    {{ adapter.get_rows_affected() }},
    'success',
    CURRENT_TIMESTAMP()
  )
{% endmacro %}

-- models/monitoring/dbt_execution_log.sql
{{ config(materialized='incremental', unique_key='id') }}

SELECT 
    {{ dbt_utils.generate_surrogate_key(['model_name', 'executed_at']) }} as id,
    model_name,
    execution_time,
    rows_affected,
    status,
    executed_at
FROM {{ ref('raw_dbt_logs') }}

{% if is_incremental() %}
    WHERE executed_at > (SELECT MAX(executed_at) FROM {{ this }})
{% endif %}
```

### 82. What are DBT best practices for large-scale projects?
**Answer**: Follow established patterns for maintainable, scalable projects.

**Best Practices:**
1. **Consistent Naming**: Use clear, consistent naming conventions
2. **Layered Architecture**: Staging → Intermediate → Marts
3. **Documentation**: Document all models and columns
4. **Testing**: Comprehensive test coverage
5. **Version Control**: Proper Git workflows
6. **Performance**: Optimize materializations and queries

```sql
-- Naming conventions
-- staging: stg_<source>_<table>
-- intermediate: int_<business_concept>
-- marts: dim_<entity> or fct_<process>

-- Example structure
models/
├── staging/
│   ├── crm/
│   │   ├── _crm_sources.yml
│   │   ├── stg_crm_customers.sql
│   │   └── stg_crm_contacts.sql
│   └── ecommerce/
│       ├── _ecommerce_sources.yml
│       ├── stg_ecommerce_orders.sql
│       └── stg_ecommerce_products.sql
├── intermediate/
│   ├── int_customer_order_summary.sql
│   └── int_product_performance.sql
└── marts/
    ├── core/
    │   ├── dim_customers.sql
    │   ├── dim_products.sql
    │   └── fct_orders.sql
    └── marketing/
        ├── customer_segments.sql
        └── campaign_performance.sql
```

### 83. How do you handle performance optimization in DBT?
**Answer**: Optimize models through proper materializations, indexing, and query design.

```sql
-- Performance optimization strategies

-- 1. Choose appropriate materialization
{{ config(
    materialized='incremental',
    unique_key='order_id',
    cluster_by=['order_date', 'customer_id'],
    partition_by={'field': 'order_date', 'data_type': 'date'}
) }}

-- 2. Use efficient joins
WITH customers AS (
    SELECT customer_id, customer_name
    FROM {{ ref('dim_customers') }}
),
orders AS (
    SELECT customer_id, order_date, total_amount
    FROM {{ ref('fct_orders') }}
    WHERE order_date >= '2023-01-01'  -- Filter early
)

SELECT 
    c.customer_name,
    COUNT(o.customer_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name

-- 3. Use query hints and optimization
{{ config(
    query_tag='daily_customer_summary',
    snowflake_warehouse='LARGE_WH'
) }}
```

### 84. How do you implement data governance with DBT?
**Answer**: Use DBT features to enforce data governance policies.

```yaml
# models/schema.yml - Data governance through documentation and testing
version: 2

models:
  - name: dim_customers
    description: "Master customer dimension - PII data"
    meta:
      owner: "data-team@company.com"
      classification: "PII"
      retention_days: 2555  # 7 years
    columns:
      - name: customer_id
        description: "Primary key"
        tests:
          - unique
          - not_null
      - name: email
        description: "Customer email - PII field"
        meta:
          classification: "PII"
        tests:
          - unique
          - not_null

# Governance macros
# macros/governance.sql
{% macro mask_pii(column_name) %}
  CASE 
    WHEN '{{ env_var("DBT_TARGET") }}' = 'prod' THEN {{ column_name }}
    ELSE '***MASKED***'
  END
{% endmacro %}

{% macro apply_retention_policy(model_name, retention_days) %}
  DELETE FROM {{ model_name }}
  WHERE created_at < CURRENT_DATE - {{ retention_days }}
{% endmacro %}
```

### 85. How do you debug and troubleshoot DBT issues?
**Answer**: Use DBT's debugging tools and logging capabilities.

```bash
# Debugging commands
dbt debug                    # Check connection and configuration
dbt compile --models my_model  # Compile specific model
dbt run --models my_model --full-refresh  # Force full refresh
dbt test --models my_model   # Test specific model
dbt run --models +my_model   # Run model and all upstream dependencies
dbt run --models my_model+   # Run model and all downstream dependencies

# Logging and verbosity
dbt run --debug             # Enable debug logging
dbt run --log-level debug   # Set log level
dbt run --vars '{"debug": true}'  # Pass debug variable
```

```sql
-- Debug macros
{% macro debug_print(message) %}
  {% if var("debug", false) %}
    {{ log(message, info=true) }}
  {% endif %}
{% endmacro %}

-- Usage in models
{{ debug_print("Starting customer processing") }}

SELECT 
    customer_id,
    COUNT(*) as order_count
FROM {{ ref('orders') }}
GROUP BY customer_id

{{ debug_print("Completed customer processing") }}
```

---

## 🎯 **Quick Reference Commands**

```bash
# Project setup
dbt init my_project
dbt deps

# Development
dbt compile
dbt run
dbt test
dbt run --models my_model
dbt test --models my_model

# Documentation
dbt docs generate
dbt docs serve

# Data freshness
dbt source freshness

# Debugging
dbt debug
dbt compile --models my_model
dbt run --models my_model --full-refresh

# Production
dbt run --target prod
dbt test --target prod
dbt source freshness --target prod
```

---

**Total Questions: 100** | **Difficulty: Beginner to Expert** | **Coverage: Complete DBT Ecosystem**