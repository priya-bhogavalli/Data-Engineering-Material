# DBT (Data Build Tool) Key Concepts

## 1. DBT Fundamentals
**What is DBT**: A command-line tool that enables data analysts and engineers to transform data in their warehouse by writing simple SQL SELECT statements.

**Core Philosophy**:
- **Transform data in the warehouse**: No data movement, leverage warehouse compute
- **Version control for analytics**: Git-based workflow for data transformations
- **Testing and documentation**: Built-in data quality and documentation features
- **Modularity**: Reusable SQL components and macros

**DBT Project Structure**:
```
my_dbt_project/
├── dbt_project.yml          # Project configuration
├── models/                  # SQL transformation files
│   ├── staging/            # Raw data cleaning
│   ├── intermediate/       # Business logic
│   └── marts/             # Final business tables
├── macros/                 # Reusable SQL functions
├── tests/                  # Data quality tests
├── snapshots/             # Slowly changing dimensions
├── seeds/                 # CSV reference data
└── analyses/              # Ad-hoc analysis queries
```

## 2. Models
**What they are**: SQL files that define data transformations, each model creates one table/view.

**Model Types**:

### Table Models
```sql
-- models/marts/dim_customers.sql
{{ config(materialized='table') }}

SELECT 
    customer_id,
    customer_name,
    email,
    registration_date,
    customer_tier
FROM {{ ref('stg_customers') }}
WHERE is_active = true
```

### View Models
```sql
-- models/intermediate/int_order_metrics.sql
{{ config(materialized='view') }}

SELECT 
    order_id,
    customer_id,
    order_total,
    order_date,
    EXTRACT(YEAR FROM order_date) as order_year
FROM {{ ref('stg_orders') }}
```

### Incremental Models
```sql
-- models/marts/fact_daily_sales.sql
{{ config(
    materialized='incremental',
    unique_key='date_day',
    on_schema_change='fail'
) }}

SELECT 
    DATE(order_date) as date_day,
    SUM(order_total) as total_sales,
    COUNT(*) as order_count
FROM {{ ref('stg_orders') }}

{% if is_incremental() %}
    WHERE order_date > (SELECT MAX(date_day) FROM {{ this }})
{% endif %}

GROUP BY DATE(order_date)
```

**Model Configurations**:
```yaml
# dbt_project.yml
models:
  my_project:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      +schema: marts
```

## 3. Sources and Seeds
**Sources**: External data tables that DBT doesn't manage but references.

```yaml
# models/sources.yml
version: 2

sources:
  - name: raw_data
    description: Raw application database
    tables:
      - name: customers
        description: Customer master data
        columns:
          - name: customer_id
            description: Primary key
            tests:
              - unique
              - not_null
      - name: orders
        description: Order transactions
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

**Using Sources**:
```sql
-- models/staging/stg_customers.sql
SELECT 
    customer_id,
    TRIM(customer_name) as customer_name,
    LOWER(email) as email,
    registration_date
FROM {{ source('raw_data', 'customers') }}
```

**Seeds**: CSV files for reference data.
```csv
-- seeds/customer_tiers.csv
tier_id,tier_name,min_spend
1,Bronze,0
2,Silver,1000
3,Gold,5000
4,Platinum,10000
```

```sql
-- Using seeds in models
SELECT 
    c.*,
    t.tier_name
FROM {{ ref('stg_customers') }} c
LEFT JOIN {{ ref('customer_tiers') }} t
    ON c.annual_spend >= t.min_spend
```

## 4. Tests
**Built-in Tests**:
```yaml
# models/schema.yml
version: 2

models:
  - name: dim_customers
    description: Customer dimension table
    columns:
      - name: customer_id
        description: Primary key
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
          - not_null
      - name: customer_tier
        tests:
          - accepted_values:
              values: ['Bronze', 'Silver', 'Gold', 'Platinum']
```

**Custom Tests**:
```sql
-- tests/assert_positive_order_totals.sql
SELECT *
FROM {{ ref('fact_orders') }}
WHERE order_total <= 0
```

**Singular Tests**:
```sql
-- tests/assert_valid_customer_emails.sql
SELECT *
FROM {{ ref('dim_customers') }}
WHERE email NOT LIKE '%@%.%'
```

**Running Tests**:
```bash
dbt test                           # Run all tests
dbt test --models dim_customers    # Test specific model
dbt test --select test_type:generic # Run only generic tests
```

## 5. Macros
**What they are**: Reusable SQL functions using Jinja templating.

**Simple Macro**:
```sql
-- macros/get_current_timestamp.sql
{% macro get_current_timestamp() %}
    {{ return(adapter.dispatch('get_current_timestamp')()) }}
{% endmacro %}

{% macro default__get_current_timestamp() %}
    CURRENT_TIMESTAMP
{% endmacro %}

{% macro snowflake__get_current_timestamp() %}
    CURRENT_TIMESTAMP()
{% endmacro %}
```

**Parameterized Macro**:
```sql
-- macros/generate_schema_name.sql
{% macro generate_alias_name(custom_alias_name=none, node=none) -%}
    {%- if custom_alias_name is none -%}
        {{ node.name }}
    {%- else -%}
        {{ custom_alias_name | trim }}
    {%- endif -%}
{%- endmacro %}
```

**Using Macros**:
```sql
-- models/marts/fact_orders.sql
SELECT 
    order_id,
    customer_id,
    order_total,
    {{ get_current_timestamp() }} as processed_at
FROM {{ ref('stg_orders') }}
```

## 6. Jinja and Templating
**Variables**:
```yaml
# dbt_project.yml
vars:
  start_date: '2023-01-01'
  end_date: '2023-12-31'
  exclude_test_users: true
```

```sql
-- Using variables in models
SELECT *
FROM {{ ref('stg_orders') }}
WHERE order_date BETWEEN '{{ var("start_date") }}' AND '{{ var("end_date") }}'
{% if var("exclude_test_users") %}
    AND customer_email NOT LIKE '%test%'
{% endif %}
```

**Loops and Conditionals**:
```sql
-- Dynamic column selection
SELECT 
    order_id,
    customer_id,
    {% for column in ['product_a', 'product_b', 'product_c'] %}
    SUM(CASE WHEN product_name = '{{ column }}' THEN quantity ELSE 0 END) as {{ column }}_qty
    {%- if not loop.last -%},{%- endif %}
    {% endfor %}
FROM {{ ref('stg_order_items') }}
GROUP BY order_id, customer_id
```

**Environment-based Logic**:
```sql
SELECT *
FROM {{ ref('stg_orders') }}
{% if target.name == 'dev' %}
    LIMIT 1000  -- Limit data in development
{% endif %}
```

## 7. Snapshots (SCD Type 2)
**What they are**: Capture changes in mutable source tables over time.

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
    
    SELECT * FROM {{ source('raw_data', 'customers') }}
{% endsnapshot %}
```

**Check Strategy Snapshot**:
```sql
{% snapshot orders_snapshot %}
    {{
        config(
          target_schema='snapshots',
          unique_key='order_id',
          strategy='check',
          check_cols=['status', 'total_amount'],
        )
    }}
    
    SELECT * FROM {{ source('raw_data', 'orders') }}
{% endsnapshot %}
```

**Using Snapshots**:
```sql
-- models/marts/dim_customers_scd.sql
SELECT 
    customer_id,
    customer_name,
    email,
    dbt_valid_from,
    dbt_valid_to,
    CASE 
        WHEN dbt_valid_to IS NULL THEN true 
        ELSE false 
    END as is_current
FROM {{ ref('customers_snapshot') }}
```

## 8. Documentation
**Model Documentation**:
```yaml
# models/schema.yml
version: 2

models:
  - name: dim_customers
    description: |
      Customer dimension table containing current customer information.
      Updated daily from the source system.
    columns:
      - name: customer_id
        description: Unique identifier for each customer
      - name: customer_name
        description: Full name of the customer
      - name: lifetime_value
        description: |
          Total revenue generated by this customer.
          Calculated as sum of all order totals.
```

**Generating Documentation**:
```bash
dbt docs generate    # Generate documentation
dbt docs serve       # Serve documentation locally
```

**Adding Descriptions in Models**:
```sql
-- models/marts/dim_customers.sql
{{ config(
    description="Customer dimension with enriched attributes"
) }}

SELECT 
    customer_id,
    customer_name,
    -- Customer tier based on annual spend
    CASE 
        WHEN annual_spend >= 10000 THEN 'Platinum'
        WHEN annual_spend >= 5000 THEN 'Gold'
        WHEN annual_spend >= 1000 THEN 'Silver'
        ELSE 'Bronze'
    END as customer_tier
FROM {{ ref('stg_customers') }}
```

## 9. Packages
**Installing Packages**:
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.1
  - git: "https://github.com/dbt-labs/dbt-audit-helper.git"
    revision: 0.9.0
```

**Using Package Macros**:
```sql
-- Using dbt_utils
SELECT 
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'order_date']) }} as order_key,
    customer_id,
    order_date,
    order_total
FROM {{ ref('stg_orders') }}
```

**Popular Packages**:
- **dbt_utils**: General utility macros
- **dbt_expectations**: Advanced testing framework
- **dbt_audit_helper**: Data validation helpers
- **dbt_external_tables**: External table management

## 10. Deployment and Environments
**Environment Configuration**:
```yaml
# profiles.yml
my_project:
  outputs:
    dev:
      type: snowflake
      account: abc123.us-east-1
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: developer
      database: dev_analytics
      warehouse: dev_warehouse
      schema: "dbt_{{ env_var('DBT_USER') }}"
    prod:
      type: snowflake
      account: abc123.us-east-1
      user: "{{ env_var('DBT_PROD_USER') }}"
      password: "{{ env_var('DBT_PROD_PASSWORD') }}"
      role: transformer
      database: analytics
      warehouse: prod_warehouse
      schema: analytics
  target: dev
```

**Deployment Commands**:
```bash
# Development workflow
dbt debug                    # Test connection
dbt deps                     # Install packages
dbt seed                     # Load seed files
dbt run                      # Run all models
dbt test                     # Run all tests

# Production deployment
dbt run --target prod        # Run in production
dbt run --models +dim_customers  # Run model and upstream
dbt run --exclude staging   # Exclude staging models
```

**CI/CD Integration**:
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
      - name: Install DBT
        run: pip install dbt-snowflake
      - name: Run DBT
        run: |
          dbt deps
          dbt run --target ci
          dbt test --target ci
```