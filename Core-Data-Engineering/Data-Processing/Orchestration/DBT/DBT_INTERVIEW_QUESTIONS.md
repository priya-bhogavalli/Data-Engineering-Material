# DBT (Data Build Tool) Interview Questions for Data Engineers

## Basic Level Questions

### 1. What is DBT and how does it fit into the modern data stack?
**Answer**: DBT (Data Build Tool) is a command-line tool that enables data analysts and engineers to transform data in their warehouse more effectively. It fits into the ELT paradigm:
- **Extract & Load**: Tools like Fivetran, Stitch load raw data
- **Transform**: DBT handles transformations using SQL
- **Analytics**: BI tools consume the transformed data
- **Version Control**: Git-based workflow for data transformations

```sql
-- Example DBT model (models/staging/stg_orders.sql)
{{ config(materialized='view') }}

SELECT 
    order_id,
    customer_id,
    order_date,
    status,
    CASE 
        WHEN status = 'completed' THEN 'fulfilled'
        WHEN status = 'cancelled' THEN 'cancelled'
        ELSE 'pending'
    END as order_status_clean,
    created_at,
    updated_at
FROM {{ source('raw_data', 'orders') }}
WHERE order_date >= '2020-01-01'
```

### 2. Explain the difference between models, sources, and seeds in DBT
**Answer**: 
- **Models**: SQL files that define transformations and create tables/views
- **Sources**: External data sources (raw tables) that DBT doesn't manage
- **Seeds**: CSV files that DBT can load into the warehouse

```yaml
# sources.yml
version: 2

sources:
  - name: raw_data
    description: Raw data from application database
    tables:
      - name: orders
        description: Raw orders table
        columns:
          - name: order_id
            description: Primary key
            tests:
              - unique
              - not_null

# seeds/country_codes.csv
country_code,country_name
US,United States
CA,Canada
UK,United Kingdom
```

```sql
-- models/marts/dim_customers.sql
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    cc.country_name
FROM {{ source('raw_data', 'customers') }} c
LEFT JOIN {{ ref('country_codes') }} cc
    ON c.country_code = cc.country_code
```

### 3. What are DBT materializations and when would you use each?
**Answer**: DBT materializations determine how models are built in the warehouse:
- **View**: Virtual table, good for simple transformations
- **Table**: Physical table, better performance for complex queries
- **Incremental**: Appends new data, efficient for large datasets
- **Ephemeral**: CTE, not materialized, used for intermediate logic

```sql
-- View materialization (default)
{{ config(materialized='view') }}
SELECT * FROM {{ source('raw_data', 'customers') }}

-- Table materialization
{{ config(materialized='table') }}
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(order_total) as lifetime_value
FROM {{ ref('stg_orders') }}
GROUP BY customer_id

-- Incremental materialization
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

SELECT * FROM {{ source('raw_data', 'orders') }}
{% if is_incremental() %}
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}

-- Ephemeral materialization
{{ config(materialized='ephemeral') }}
SELECT 
    order_id,
    CASE WHEN total > 100 THEN 'high_value' ELSE 'standard' END as order_tier
FROM {{ source('raw_data', 'orders') }}
```

### 4. How do you implement testing in DBT?
**Answer**: DBT provides built-in tests and supports custom tests:
- **Generic Tests**: unique, not_null, accepted_values, relationships
- **Singular Tests**: Custom SQL queries that return failing records
- **Data Tests**: Run on models and sources

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
      - name: status
        tests:
          - accepted_values:
              values: ['active', 'inactive', 'pending']

  - name: fact_orders
    tests:
      - relationships:
          to: ref('dim_customers')
          field: customer_id
```

```sql
-- tests/assert_positive_order_totals.sql (singular test)
SELECT 
    order_id,
    order_total
FROM {{ ref('fact_orders') }}
WHERE order_total <= 0
```

### 5. What is the DBT project structure and key configuration files?
**Answer**: Standard DBT project structure:
- **dbt_project.yml**: Main configuration file
- **models/**: SQL transformation files
- **tests/**: Custom test files
- **macros/**: Reusable SQL code
- **seeds/**: CSV files to load
- **snapshots/**: SCD Type 2 implementations

```yaml
# dbt_project.yml
name: 'analytics_dbt'
version: '1.0.0'
config-version: 2

profile: 'analytics'

model-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  analytics_dbt:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

## Intermediate Level Questions

### 6. How do you implement incremental models effectively?
**Answer**: Incremental models optimize performance by processing only new/changed data:
- **Unique Key**: Handles updates and deduplication
- **Incremental Strategy**: merge, append, delete+insert
- **Filters**: Use `is_incremental()` macro for conditional logic

```sql
-- models/fact_daily_sales.sql
{{ config(
    materialized='incremental',
    unique_key='date_customer_key',
    incremental_strategy='merge'
) }}

WITH daily_aggregates AS (
    SELECT 
        DATE(order_date) as order_date,
        customer_id,
        CONCAT(DATE(order_date), '_', customer_id) as date_customer_key,
        SUM(order_total) as daily_total,
        COUNT(*) as order_count,
        MAX(updated_at) as last_updated
    FROM {{ ref('stg_orders') }}
    
    {% if is_incremental() %}
        -- Only process recent data on incremental runs
        WHERE DATE(order_date) >= (
            SELECT COALESCE(MAX(order_date), '1900-01-01') 
            FROM {{ this }}
        ) - 7  -- 7-day lookback for late-arriving data
    {% endif %}
    
    GROUP BY DATE(order_date), customer_id
)

SELECT * FROM daily_aggregates

-- Post-hook to update metadata
{{ config(
    post_hook="INSERT INTO {{ target.schema }}.model_metadata 
               VALUES ('{{ this }}', '{{ run_started_at }}', {{ this.rows }})"
) }}
```

### 7. How do you use DBT macros for code reusability?
**Answer**: Macros enable reusable SQL code and dynamic query generation:
- **Jinja Templating**: Use variables and control structures
- **Built-in Macros**: `ref()`, `source()`, `var()`
- **Custom Macros**: Create reusable functions

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ default_schema }}_{{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}

-- macros/get_date_dimension.sql
{% macro get_date_dimension(start_date, end_date) %}
    WITH date_spine AS (
        {{ dbt_utils.date_spine(
            datepart="day",
            start_date="'" + start_date + "'",
            end_date="'" + end_date + "'"
        ) }}
    )
    SELECT 
        date_day,
        EXTRACT(year FROM date_day) as year,
        EXTRACT(month FROM date_day) as month,
        EXTRACT(day FROM date_day) as day,
        EXTRACT(dayofweek FROM date_day) as day_of_week,
        CASE WHEN EXTRACT(dayofweek FROM date_day) IN (1, 7) 
             THEN 'Weekend' ELSE 'Weekday' END as weekend_flag
    FROM date_spine
{% endmacro %}

-- Using the macro in a model
SELECT * FROM (
    {{ get_date_dimension('2020-01-01', '2024-12-31') }}
)
```

### 8. How do you implement slowly changing dimensions (SCD) with DBT snapshots?
**Answer**: DBT snapshots implement SCD Type 2 by tracking changes over time:
- **Timestamp Strategy**: Track changes based on updated_at column
- **Check Strategy**: Compare all columns for changes
- **Unique Key**: Identify records to track

```sql
-- snapshots/customers_snapshot.sql
{% snapshot customers_snapshot %}
    {{
        config(
          target_schema='snapshots',
          unique_key='customer_id',
          strategy='timestamp',
          updated_at='updated_at',
        )
    }}
    
    SELECT 
        customer_id,
        first_name,
        last_name,
        email,
        status,
        city,
        state,
        updated_at
    FROM {{ source('raw_data', 'customers') }}
    
{% endsnapshot %}

-- snapshots/products_snapshot.sql (check strategy)
{% snapshot products_snapshot %}
    {{
        config(
          target_schema='snapshots',
          unique_key='product_id',
          strategy='check',
          check_cols=['name', 'price', 'category', 'status'],
        )
    }}
    
    SELECT * FROM {{ source('raw_data', 'products') }}
    
{% endsnapshot %}

-- Using snapshot in a model
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    dbt_valid_from,
    dbt_valid_to,
    CASE WHEN dbt_valid_to IS NULL THEN TRUE ELSE FALSE END as is_current
FROM {{ ref('customers_snapshot') }}
```

### 9. How do you implement data quality checks and monitoring in DBT?
**Answer**: Comprehensive data quality framework using tests, macros, and hooks:
- **Schema Tests**: Built-in and custom tests
- **Data Tests**: Custom SQL assertions
- **Test Macros**: Reusable test logic
- **Monitoring**: Track test results over time

```sql
-- macros/test_data_quality.sql
{% macro test_row_count_change(model, threshold=0.1) %}
    WITH current_count AS (
        SELECT COUNT(*) as row_count
        FROM {{ model }}
    ),
    historical_avg AS (
        SELECT AVG(row_count) as avg_row_count
        FROM {{ target.schema }}.model_row_counts
        WHERE model_name = '{{ model }}'
        AND created_at >= CURRENT_DATE - 7
    )
    SELECT 
        current_count.row_count,
        historical_avg.avg_row_count,
        ABS(current_count.row_count - historical_avg.avg_row_count) / historical_avg.avg_row_count as change_ratio
    FROM current_count
    CROSS JOIN historical_avg
    WHERE ABS(current_count.row_count - historical_avg.avg_row_count) / historical_avg.avg_row_count > {{ threshold }}
{% endmacro %}

-- tests/data_quality/test_revenue_consistency.sql
WITH order_revenue AS (
    SELECT 
        DATE(order_date) as order_date,
        SUM(order_total) as total_revenue
    FROM {{ ref('fact_orders') }}
    GROUP BY DATE(order_date)
),
payment_revenue AS (
    SELECT 
        DATE(payment_date) as payment_date,
        SUM(amount) as total_payments
    FROM {{ ref('fact_payments') }}
    GROUP BY DATE(payment_date)
)
SELECT 
    o.order_date,
    o.total_revenue,
    p.total_payments,
    ABS(o.total_revenue - p.total_payments) as difference
FROM order_revenue o
FULL OUTER JOIN payment_revenue p
    ON o.order_date = p.payment_date
WHERE ABS(o.total_revenue - p.total_payments) > 100
```

### 10. How do you optimize DBT performance for large datasets?
**Answer**: Performance optimization strategies:
- **Incremental Models**: Process only new data
- **Partitioning**: Use warehouse-specific partitioning
- **Indexing**: Create appropriate indexes
- **Query Optimization**: Efficient SQL patterns

```sql
-- Optimized incremental model with partitioning
{{ config(
    materialized='incremental',
    unique_key='transaction_id',
    partition_by={
        "field": "transaction_date",
        "data_type": "date",
        "granularity": "day"
    },
    cluster_by=['customer_id', 'product_category']
) }}

WITH optimized_transactions AS (
    SELECT 
        transaction_id,
        customer_id,
        product_id,
        transaction_date,
        amount,
        -- Pre-calculate commonly used metrics
        EXTRACT(year FROM transaction_date) as transaction_year,
        EXTRACT(month FROM transaction_date) as transaction_month,
        CASE WHEN amount > 100 THEN 'high_value' ELSE 'standard' END as value_tier
    FROM {{ source('raw_data', 'transactions') }}
    
    {% if is_incremental() %}
        WHERE transaction_date > (
            SELECT COALESCE(MAX(transaction_date), '1900-01-01')
            FROM {{ this }}
        )
    {% endif %}
)

SELECT * FROM optimized_transactions

-- Use efficient joins and avoid SELECT *
-- models/customer_metrics.sql
{{ config(materialized='table') }}

SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.order_total) as lifetime_value,
    MAX(o.order_date) as last_order_date
FROM {{ ref('dim_customers') }} c
LEFT JOIN {{ ref('fact_orders') }} o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
```

## Advanced Level Questions

### 11. How do you implement advanced DBT workflows with hooks and operations?
**Answer**: Hooks and operations enable complex workflow orchestration:
- **Pre/Post Hooks**: Execute SQL before/after model runs
- **On-run-start/end**: Execute at beginning/end of dbt run
- **Operations**: Standalone SQL commands

```sql
-- dbt_project.yml
on-run-start:
  - "CREATE SCHEMA IF NOT EXISTS {{ target.schema }}_logs"
  - "INSERT INTO {{ target.schema }}_logs.run_log VALUES ('{{ run_started_at }}', 'started', '{{ invocation_id }}')"

on-run-end:
  - "INSERT INTO {{ target.schema }}_logs.run_log VALUES ('{{ run_started_at }}', 'completed', '{{ invocation_id }}')"
  - "{{ log_model_results() }}"

-- macros/log_model_results.sql
{% macro log_model_results() %}
    {% if execute %}
        {% for node in graph.nodes.values() %}
            {% if node.resource_type == 'model' %}
                INSERT INTO {{ target.schema }}_logs.model_run_log 
                VALUES (
                    '{{ run_started_at }}',
                    '{{ node.name }}',
                    '{{ node.config.materialized }}',
                    (SELECT COUNT(*) FROM {{ target.schema }}.{{ node.name }})
                );
            {% endif %}
        {% endfor %}
    {% endif %}
{% endmacro %}

-- models/fact_orders.sql with hooks
{{ config(
    materialized='incremental',
    unique_key='order_id',
    pre_hook="DELETE FROM {{ this }} WHERE order_status = 'cancelled'",
    post_hook=[
        "CREATE INDEX IF NOT EXISTS idx_orders_customer ON {{ this }} (customer_id)",
        "ANALYZE TABLE {{ this }} COMPUTE STATISTICS"
    ]
) }}

-- macros/operations/refresh_external_tables.sql
{% macro refresh_external_tables() %}
    {% set external_tables = ['raw_orders', 'raw_customers', 'raw_products'] %}
    {% for table in external_tables %}
        REFRESH TABLE {{ source('external_data', table) }};
    {% endfor %}
{% endmacro %}
```

### 12. How do you implement DBT with multiple environments and CI/CD?
**Answer**: Multi-environment setup with automated testing and deployment:
- **Profiles**: Different configurations per environment
- **Environment Variables**: Dynamic configuration
- **CI/CD Integration**: Automated testing and deployment

```yaml
# profiles.yml
analytics:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE') }}"
      database: analytics_dev
      warehouse: compute_wh
      schema: "{{ env_var('SNOWFLAKE_SCHEMA') }}"
      
    prod:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_PROD_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PROD_PASSWORD') }}"
      role: transformer
      database: analytics_prod
      warehouse: compute_wh
      schema: marts

# .github/workflows/dbt_ci.yml
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
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      
      - name: Install dependencies
        run: |
          pip install dbt-snowflake
          dbt deps
      
      - name: Run DBT tests
        run: |
          dbt seed --target dev
          dbt run --target dev --models +changed_models
          dbt test --target dev --models +changed_models
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          dbt seed --target prod
          dbt run --target prod
          dbt test --target prod
```

### 13. How do you implement data lineage and documentation in DBT?
**Answer**: DBT provides built-in lineage tracking and documentation generation:
- **Lineage Graphs**: Automatic dependency tracking
- **Documentation**: Generate and serve documentation
- **Column-level Lineage**: Track column transformations

```yaml
# models/schema.yml
version: 2

models:
  - name: fact_orders
    description: |
      Order fact table containing all order transactions.
      
      This table is updated incrementally every hour and contains
      both historical and current order data.
      
    columns:
      - name: order_id
        description: "Primary key for orders"
        tests:
          - unique
          - not_null
      
      - name: customer_id
        description: "Foreign key to dim_customers"
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      
      - name: order_total
        description: "Total order amount in USD"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 10000

# macros/generate_model_yaml.sql
{% macro generate_model_yaml(model_name) %}
    {% set relation = ref(model_name) %}
    {% set columns = adapter.get_columns_in_relation(relation) %}
    
    version: 2
    models:
      - name: {{ model_name }}
        columns:
        {% for column in columns %}
          - name: {{ column.name }}
            description: ""
        {% endfor %}
{% endmacro %}

# Generate documentation
# dbt docs generate
# dbt docs serve --port 8080
```

### 14. How do you implement advanced testing strategies in DBT?
**Answer**: Advanced testing includes custom tests, test macros, and data monitoring:

```sql
-- macros/tests/test_freshness.sql
{% test freshness(model, column_name, max_age_hours=24) %}
    SELECT *
    FROM {{ model }}
    WHERE {{ column_name }} < CURRENT_TIMESTAMP - INTERVAL {{ max_age_hours }} HOUR
{% endtest %}

-- macros/tests/test_distribution.sql
{% test distribution_similarity(model, column_name, ref_model, ref_column_name, threshold=0.1) %}
    WITH current_dist AS (
        SELECT 
            {{ column_name }} as value,
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as percentage
        FROM {{ model }}
        GROUP BY {{ column_name }}
    ),
    reference_dist AS (
        SELECT 
            {{ ref_column_name }} as value,
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as percentage
        FROM {{ ref_model }}
        GROUP BY {{ ref_column_name }}
    )
    SELECT 
        c.value,
        c.percentage as current_pct,
        r.percentage as reference_pct,
        ABS(c.percentage - COALESCE(r.percentage, 0)) as difference
    FROM current_dist c
    FULL OUTER JOIN reference_dist r ON c.value = r.value
    WHERE ABS(c.percentage - COALESCE(r.percentage, 0)) > {{ threshold }}
{% endtest %}

-- tests/business_logic/test_revenue_reconciliation.sql
WITH order_revenue AS (
    SELECT 
        DATE_TRUNC('day', order_date) as day,
        SUM(order_total) as order_revenue
    FROM {{ ref('fact_orders') }}
    WHERE order_status = 'completed'
    GROUP BY DATE_TRUNC('day', order_date)
),
payment_revenue AS (
    SELECT 
        DATE_TRUNC('day', payment_date) as day,
        SUM(amount) as payment_revenue
    FROM {{ ref('fact_payments') }}
    WHERE payment_status = 'successful'
    GROUP BY DATE_TRUNC('day', payment_date)
)
SELECT 
    COALESCE(o.day, p.day) as day,
    COALESCE(o.order_revenue, 0) as order_revenue,
    COALESCE(p.payment_revenue, 0) as payment_revenue,
    ABS(COALESCE(o.order_revenue, 0) - COALESCE(p.payment_revenue, 0)) as difference
FROM order_revenue o
FULL OUTER JOIN payment_revenue p ON o.day = p.day
WHERE ABS(COALESCE(o.order_revenue, 0) - COALESCE(p.payment_revenue, 0)) > 100
```

### 15. How do you implement DBT packages and custom materializations?
**Answer**: Extend DBT functionality with packages and custom materializations:

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 0.9.2
  - package: calogica/dbt_expectations
    version: 0.8.5
  - git: "https://github.com/your-org/custom-dbt-package.git"
    revision: v1.0.0

# Custom materialization
# macros/materializations/custom_incremental.sql
{% materialization custom_incremental, default %}
  {%- set unique_key = config.get('unique_key') -%}
  {%- set target_relation = this -%}
  {%- set existing_relation = load_relation(this) -%}
  {%- set tmp_relation = make_temp_relation(this) -%}

  {{ run_hooks(pre_hooks) }}

  {% if existing_relation is none %}
    -- First run: create table
    {% set build_sql = create_table_as(False, target_relation, sql) %}
  {% else %}
    -- Incremental run: merge data
    {% set build_sql %}
      CREATE OR REPLACE TEMPORARY TABLE {{ tmp_relation }} AS (
        {{ sql }}
      );
      
      MERGE INTO {{ target_relation }} as target
      USING {{ tmp_relation }} as source
      ON target.{{ unique_key }} = source.{{ unique_key }}
      WHEN MATCHED THEN UPDATE SET *
      WHEN NOT MATCHED THEN INSERT *;
      
      DROP TABLE {{ tmp_relation }};
    {% endset %}
  {% endif %}

  {% call statement('main') -%}
    {{ build_sql }}
  {%- endcall %}

  {{ run_hooks(post_hooks) }}

  {{ return({'relations': [target_relation]}) }}
{% endmaterialization %}
```

This comprehensive DBT interview question set covers essential knowledge for data engineers, from basic concepts to advanced implementation patterns and best practices.