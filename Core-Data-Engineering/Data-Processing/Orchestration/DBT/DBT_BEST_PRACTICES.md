# dbt Best Practices for Data Engineering

## Project Structure

### Directory Organization
```
dbt_project/
├── dbt_project.yml
├── models/
│   ├── staging/
│   │   ├── _sources.yml
│   │   └── stg_customers.sql
│   ├── intermediate/
│   │   └── int_customer_orders.sql
│   ├── marts/
│   │   ├── core/
│   │   └── finance/
│   └── schema.yml
├── macros/
├── tests/
├── snapshots/
└── analyses/
```

### Model Layering
```sql
-- models/staging/stg_customers.sql
{{ config(materialized='view') }}

select
    customer_id,
    lower(trim(first_name)) as first_name,
    lower(trim(last_name)) as last_name,
    lower(trim(email)) as email,
    created_at,
    updated_at
from {{ source('raw', 'customers') }}

-- models/intermediate/int_customer_orders.sql
{{ config(materialized='ephemeral') }}

select
    c.customer_id,
    c.first_name,
    c.last_name,
    count(o.order_id) as total_orders,
    sum(o.amount) as total_amount
from {{ ref('stg_customers') }} c
left join {{ ref('stg_orders') }} o
    on c.customer_id = o.customer_id
group by 1, 2, 3

-- models/marts/core/dim_customers.sql
{{ config(
    materialized='table',
    indexes=[
        {'columns': ['customer_id'], 'unique': True}
    ]
) }}

select
    customer_id,
    first_name,
    last_name,
    email,
    total_orders,
    total_amount,
    case
        when total_amount > 1000 then 'high_value'
        when total_amount > 100 then 'medium_value'
        else 'low_value'
    end as customer_segment
from {{ ref('int_customer_orders') }}
```

## Configuration Management

### dbt_project.yml
```yaml
name: 'data_warehouse'
version: '1.0.0'
config-version: 2

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  data_warehouse:
    staging:
      +materialized: view
      +docs:
        node_color: "lightblue"
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      core:
        +schema: core
      finance:
        +schema: finance

vars:
  start_date: '2020-01-01'
  timezone: 'UTC'
```

### Environment-Specific Profiles
```yaml
# profiles.yml
data_warehouse:
  outputs:
    dev:
      type: snowflake
      account: abc123.us-east-1
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: transformer
      database: dev_warehouse
      warehouse: dev_wh
      schema: dbt_{{ env_var('DBT_USER') }}
      
    prod:
      type: snowflake
      account: abc123.us-east-1
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: transformer
      database: prod_warehouse
      warehouse: prod_wh
      schema: analytics
      
  target: dev
```

## Testing and Documentation

### Schema Tests
```yaml
# models/schema.yml
version: 2

models:
  - name: dim_customers
    description: "Customer dimension table"
    columns:
      - name: customer_id
        description: "Unique customer identifier"
        tests:
          - unique
          - not_null
      - name: email
        description: "Customer email address"
        tests:
          - unique
          - not_null
      - name: customer_segment
        description: "Customer value segment"
        tests:
          - accepted_values:
              values: ['high_value', 'medium_value', 'low_value']

sources:
  - name: raw
    description: "Raw data from source systems"
    tables:
      - name: customers
        description: "Raw customer data"
        columns:
          - name: customer_id
            tests:
              - unique
              - not_null
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

### Custom Tests
```sql
-- tests/assert_positive_order_amounts.sql
select *
from {{ ref('fct_orders') }}
where amount <= 0

-- macros/test_not_empty_string.sql
{% macro test_not_empty_string(model, column_name) %}
    select *
    from {{ model }}
    where trim({{ column_name }}) = '' or {{ column_name }} is null
{% endmacro %}
```

## Macros and Reusability

### Utility Macros
```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}

-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    round({{ column_name }} / 100.0, {{ precision }})
{% endmacro %}

-- Usage in model
select
    order_id,
    {{ cents_to_dollars('amount_cents') }} as amount_dollars
from {{ ref('stg_orders') }}
```

### Advanced Macros
```sql
-- macros/pivot.sql
{% macro pivot(column, values, agg='sum', then_value=1) %}
  {% for value in values %}
    {{ agg }}(
      case when {{ column }} = '{{ value }}' 
           then {{ then_value }} 
           else 0 
      end
    ) as {{ value }}
    {%- if not loop.last -%},{%- endif %}
  {% endfor %}
{% endmacro %}

-- Usage
select
    customer_id,
    {{ pivot('product_category', ['electronics', 'clothing', 'books']) }}
from {{ ref('stg_orders') }}
group by customer_id
```

## Incremental Models

### Incremental Processing
```sql
-- models/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='fail'
) }}

select
    order_id,
    customer_id,
    order_date,
    amount,
    status,
    created_at,
    updated_at
from {{ source('raw', 'orders') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

### Merge Strategies
```sql
-- models/dim_customers_scd2.sql
{{ config(
    materialized='incremental',
    unique_key='customer_id',
    merge_update_columns=['first_name', 'last_name', 'email'],
    on_schema_change='append_new_columns'
) }}

select
    customer_id,
    first_name,
    last_name,
    email,
    created_at,
    updated_at,
    case 
        when {{ is_incremental() }} then current_timestamp()
        else created_at
    end as dbt_valid_from,
    null as dbt_valid_to
from {{ ref('stg_customers') }}

{% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

## Performance Optimization

### Materialization Strategies
```sql
-- Large fact table - table materialization
{{ config(
    materialized='table',
    post_hook="create index if not exists idx_order_date on {{ this }} (order_date)"
) }}

-- Aggregated metrics - incremental
{{ config(
    materialized='incremental',
    unique_key=['date', 'customer_id']
) }}

-- Intermediate transformations - ephemeral
{{ config(materialized='ephemeral') }}
```

### Query Optimization
```sql
-- Use CTEs for readability and performance
with customer_orders as (
    select
        customer_id,
        count(*) as order_count,
        sum(amount) as total_amount
    from {{ ref('fct_orders') }}
    group by customer_id
),

customer_segments as (
    select
        customer_id,
        case
            when total_amount > 1000 then 'high_value'
            when total_amount > 100 then 'medium_value'
            else 'low_value'
        end as segment
    from customer_orders
)

select * from customer_segments
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/dbt.yml
name: dbt CI/CD

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
          
      - name: Install dbt
        run: pip install dbt-snowflake
        
      - name: Run dbt debug
        run: dbt debug
        env:
          DBT_PROFILES_DIR: .
          
      - name: Run dbt tests
        run: dbt test
        
      - name: Run dbt docs generate
        run: dbt docs generate
        
  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Run dbt in production
        run: dbt run --target prod
```