# 🔄 DBT (Data Build Tool) - Comprehensive Interview Questions & Answers

## 📋 Table of Contents
1. [Fundamentals (Questions 1-15)](#fundamentals)
2. [Models & Transformations (Questions 16-30)](#models--transformations)
3. [Testing & Documentation (Questions 31-45)](#testing--documentation)
4. [Advanced Features (Questions 46-60)](#advanced-features)
5. [Operations & Best Practices (Questions 61-75)](#operations--best-practices)

---

## 🔰 Fundamentals

### 1. What is DBT and what problems does it solve?
**Answer:** DBT (Data Build Tool) is a transformation tool that enables data analysts and engineers to transform data in their warehouse by writing SQL SELECT statements. It solves:
- **Version control**: SQL transformations under version control
- **Testing**: Built-in data quality testing
- **Documentation**: Automatic documentation generation
- **Dependency management**: Handles complex transformation dependencies
- **Modularity**: Reusable SQL components

### 2. Explain DBT's core philosophy and approach
**Answer:**
- **Transform after Load (ELT)**: Transform data in the warehouse
- **SQL-first**: Use familiar SQL for transformations
- **Version control**: Treat analytics code like software
- **Testing**: Built-in data quality checks
- **Documentation**: Self-documenting data models

### 3. What are the main components of a DBT project?
**Answer:**
```
dbt_project/
├── dbt_project.yml          # Project configuration
├── models/                  # SQL transformation files
│   ├── staging/            # Raw data cleaning
│   ├── intermediate/       # Business logic
│   └── marts/             # Final business entities
├── tests/                  # Custom data tests
├── macros/                 # Reusable SQL functions
├── seeds/                  # CSV reference data
├── snapshots/              # SCD Type 2 tables
├── analyses/               # Ad-hoc analyses
└── docs/                   # Additional documentation
```

### 4. What is the difference between DBT Core and DBT Cloud?
**Answer:**
| Feature | DBT Core | DBT Cloud |
|---------|----------|-----------|
| **Cost** | Free, open-source | Paid service |
| **Deployment** | Self-hosted | Managed service |
| **IDE** | Local editor | Web-based IDE |
| **Scheduling** | External scheduler needed | Built-in scheduler |
| **Collaboration** | Git-based | Built-in collaboration |
| **Monitoring** | Manual setup | Built-in monitoring |

### 5. How does DBT handle dependencies?
**Answer:**
```sql
-- models/staging/stg_orders.sql
SELECT * FROM {{ source('raw', 'orders') }}

-- models/marts/fct_orders.sql
SELECT * FROM {{ ref('stg_orders') }}
```
- **ref()**: References other models, creates dependencies
- **source()**: References raw data tables
- **Dependency graph**: DBT builds execution order automatically
- **Incremental builds**: Only rebuild changed models

### 6. What are DBT materializations?
**Answer:**
```sql
-- Table materialization
{{ config(materialized='table') }}
SELECT * FROM source_data

-- View materialization (default)
{{ config(materialized='view') }}
SELECT * FROM source_data

-- Incremental materialization
{{ config(materialized='incremental') }}
SELECT * FROM source_data
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}

-- Ephemeral materialization
{{ config(materialized='ephemeral') }}
SELECT * FROM source_data
```

### 7. Explain DBT's compilation process
**Answer:**
1. **Parse**: Read project files and build dependency graph
2. **Compile**: Convert Jinja templates to raw SQL
3. **Execute**: Run compiled SQL in target warehouse
4. **Artifacts**: Generate manifest, catalog, and run results

### 8. What is the dbt_project.yml file?
**Answer:**
```yaml
name: 'my_dbt_project'
version: '1.0.0'
config-version: 2

profile: 'my_profile'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets: ["target", "dbt_packages"]

models:
  my_dbt_project:
    staging:
      +materialized: view
    marts:
      +materialized: table
      +schema: analytics
```

### 9. How do you configure database connections in DBT?
**Answer:**
```yaml
# profiles.yml
my_profile:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: dbt_user
      password: password
      port: 5432
      dbname: analytics
      schema: dbt_dev
      threads: 4
      keepalives_idle: 0
    
    prod:
      type: snowflake
      account: my_account
      user: prod_user
      password: "{{ env_var('DBT_PASSWORD') }}"
      role: transformer
      database: ANALYTICS
      warehouse: COMPUTE_WH
      schema: PROD
      threads: 8
```

### 10. What are DBT sources?
**Answer:**
```yaml
# models/staging/sources.yml
version: 2

sources:
  - name: raw_data
    description: Raw data from application database
    tables:
      - name: users
        description: User information
        columns:
          - name: user_id
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

### 11. How do you use variables in DBT?
**Answer:**
```yaml
# dbt_project.yml
vars:
  start_date: '2023-01-01'
  end_date: '2023-12-31'
```

```sql
-- In model
SELECT *
FROM orders
WHERE order_date BETWEEN '{{ var("start_date") }}' AND '{{ var("end_date") }}'

-- Command line override
dbt run --vars '{"start_date": "2023-06-01"}'
```

### 12. What are DBT macros?
**Answer:**
```sql
-- macros/get_payment_methods.sql
{% macro get_payment_methods() %}
    {{ return(['credit_card', 'debit_card', 'bank_transfer', 'cash']) }}
{% endmacro %}

-- Usage in model
SELECT
    order_id,
    CASE payment_method
        {% for method in get_payment_methods() %}
        WHEN '{{ method }}' THEN '{{ method | title }}'
        {% endfor %}
        ELSE 'Other'
    END as payment_method_clean
FROM orders
```

### 13. How does DBT handle environments?
**Answer:**
```bash
# Development
dbt run --target dev

# Production
dbt run --target prod

# Staging
dbt run --target staging
```
- **Profiles**: Different targets for different environments
- **Schema separation**: Separate schemas per environment
- **Variable overrides**: Environment-specific configurations

### 14. What is the DBT manifest file?
**Answer:**
The manifest.json contains:
- **Nodes**: All models, tests, sources, snapshots
- **Dependencies**: Relationships between nodes
- **Metadata**: Compilation information, timing
- **Usage**: Powers DBT docs, lineage, and external tools

### 15. How do you run DBT commands?
**Answer:**
```bash
# Run all models
dbt run

# Run specific model
dbt run --select my_model

# Run models and downstream
dbt run --select my_model+

# Run models and upstream
dbt run --select +my_model

# Test all models
dbt test

# Generate documentation
dbt docs generate
dbt docs serve

# Compile without running
dbt compile
```

---

## 🏗️ Models & Transformations

### 16. What are the different types of DBT models?
**Answer:**
- **Staging models**: Clean and standardize raw data
- **Intermediate models**: Business logic transformations
- **Mart models**: Final business entities for consumption
- **Utility models**: Helper models for complex logic

```sql
-- Staging model (stg_orders.sql)
SELECT
    order_id,
    customer_id,
    order_date::date as order_date,
    UPPER(status) as status
FROM {{ source('raw', 'orders') }}

-- Mart model (fct_orders.sql)
SELECT
    o.order_id,
    c.customer_name,
    o.order_date,
    o.total_amount
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('dim_customers') }} c ON o.customer_id = c.customer_id
```

### 17. How do you implement incremental models?
**Answer:**
```sql
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
    updated_at
FROM {{ source('raw', 'orders') }}

{% if is_incremental() %}
    -- Only process new/updated records
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

### 18. What are incremental strategies in DBT?
**Answer:**
- **append**: Add new rows only
- **delete+insert**: Delete matching records, insert new ones
- **merge**: Upsert based on unique key
- **insert_overwrite**: Overwrite partitions (BigQuery)

```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id'
) }}
```

### 19. How do you handle slowly changing dimensions (SCD)?
**Answer:**
```sql
-- snapshots/orders_snapshot.sql
{% snapshot orders_snapshot %}
    {{
        config(
          target_schema='snapshots',
          unique_key='order_id',
          strategy='timestamp',
          updated_at='updated_at',
        )
    }}
    
    SELECT * FROM {{ source('raw', 'orders') }}
{% endsnapshot %}
```

### 20. What are DBT seeds and when to use them?
**Answer:**
```csv
-- seeds/country_codes.csv
country_code,country_name
US,United States
CA,Canada
UK,United Kingdom
```

```sql
-- Use in model
SELECT
    o.*,
    cc.country_name
FROM {{ ref('orders') }} o
JOIN {{ ref('country_codes') }} cc ON o.country_code = cc.country_code
```

Use seeds for:
- Reference data (country codes, categories)
- Small lookup tables
- Configuration data

### 21. How do you implement data quality checks?
**Answer:**
```yaml
# models/schema.yml
version: 2

models:
  - name: fct_orders
    description: Order fact table
    columns:
      - name: order_id
        description: Primary key
        tests:
          - unique
          - not_null
      
      - name: customer_id
        description: Foreign key to customers
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      
      - name: order_total
        description: Order total amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```

### 22. How do you create custom tests?
**Answer:**
```sql
-- tests/assert_positive_order_amounts.sql
SELECT *
FROM {{ ref('fct_orders') }}
WHERE order_total <= 0
```

```sql
-- macros/test_no_gaps_in_sequence.sql
{% test no_gaps_in_sequence(model, column_name) %}
    WITH sequence_check AS (
        SELECT
            {{ column_name }},
            LAG({{ column_name }}) OVER (ORDER BY {{ column_name }}) as prev_value
        FROM {{ model }}
    )
    SELECT *
    FROM sequence_check
    WHERE {{ column_name }} - prev_value > 1
{% endtest %}
```

### 23. How do you handle complex transformations with CTEs?
**Answer:**
```sql
-- models/marts/customer_metrics.sql
WITH order_summary AS (
    SELECT
        customer_id,
        COUNT(*) as total_orders,
        SUM(order_total) as total_spent,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date
    FROM {{ ref('fct_orders') }}
    GROUP BY customer_id
),

customer_segments AS (
    SELECT
        *,
        CASE
            WHEN total_spent > 10000 THEN 'VIP'
            WHEN total_spent > 1000 THEN 'Premium'
            ELSE 'Standard'
        END as customer_segment
    FROM order_summary
)

SELECT
    c.customer_id,
    c.customer_name,
    cs.total_orders,
    cs.total_spent,
    cs.customer_segment,
    DATEDIFF('day', cs.first_order_date, cs.last_order_date) as customer_lifetime_days
FROM {{ ref('dim_customers') }} c
JOIN customer_segments cs ON c.customer_id = cs.customer_id
```

### 24. How do you implement window functions in DBT?
**Answer:**
```sql
-- models/marts/order_analytics.sql
SELECT
    order_id,
    customer_id,
    order_date,
    order_total,
    
    -- Running totals
    SUM(order_total) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS UNBOUNDED PRECEDING
    ) as running_total,
    
    -- Ranking
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as order_sequence,
    
    -- Moving averages
    AVG(order_total) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3_orders,
    
    -- Lead/Lag
    LAG(order_date) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as previous_order_date

FROM {{ ref('fct_orders') }}
```

### 25. How do you handle date and time transformations?
**Answer:**
```sql
-- macros/date_helpers.sql
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
        CASE EXTRACT(dayofweek FROM date_day)
            WHEN 1 THEN 'Sunday'
            WHEN 2 THEN 'Monday'
            -- ... etc
        END as day_name,
        CASE
            WHEN EXTRACT(dayofweek FROM date_day) IN (1, 7) THEN 'Weekend'
            ELSE 'Weekday'
        END as weekend_flag
    FROM date_spine
{% endmacro %}
```

### 26. How do you implement data pivoting in DBT?
**Answer:**
```sql
-- Using dbt_utils.pivot
SELECT
    customer_id,
    {{ dbt_utils.pivot(
        'payment_method',
        dbt_utils.get_column_values(ref('orders'), 'payment_method'),
        agg='sum',
        then_value='order_total'
    ) }}
FROM {{ ref('orders') }}
GROUP BY customer_id

-- Manual pivot
SELECT
    customer_id,
    SUM(CASE WHEN payment_method = 'credit_card' THEN order_total ELSE 0 END) as credit_card_total,
    SUM(CASE WHEN payment_method = 'debit_card' THEN order_total ELSE 0 END) as debit_card_total,
    SUM(CASE WHEN payment_method = 'cash' THEN order_total ELSE 0 END) as cash_total
FROM {{ ref('orders') }}
GROUP BY customer_id
```

### 27. How do you handle JSON data in DBT?
**Answer:**
```sql
-- Snowflake JSON parsing
SELECT
    order_id,
    metadata:customer:name::string as customer_name,
    metadata:customer:email::string as customer_email,
    metadata:items[0]:product_id::string as first_product_id,
    ARRAY_SIZE(metadata:items) as item_count
FROM {{ source('raw', 'orders') }}

-- BigQuery JSON parsing
SELECT
    order_id,
    JSON_EXTRACT_SCALAR(metadata, '$.customer.name') as customer_name,
    JSON_EXTRACT_SCALAR(metadata, '$.customer.email') as customer_email,
    JSON_EXTRACT_ARRAY(metadata, '$.items') as items
FROM {{ source('raw', 'orders') }}
```

### 28. How do you implement data deduplication?
**Answer:**
```sql
-- Remove duplicates using ROW_NUMBER()
WITH deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id, order_date 
            ORDER BY updated_at DESC
        ) as row_num
    FROM {{ source('raw', 'orders') }}
)

SELECT *
FROM deduplicated
WHERE row_num = 1

-- Using QUALIFY (Snowflake)
SELECT *
FROM {{ source('raw', 'orders') }}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer_id, order_date 
    ORDER BY updated_at DESC
) = 1
```

### 29. How do you implement cross-database joins?
**Answer:**
```sql
-- Using DBT's cross-database functionality
WITH orders AS (
    SELECT * FROM {{ source('postgres_db', 'orders') }}
),

customers AS (
    SELECT * FROM {{ source('snowflake_db', 'customers') }}
)

-- DBT handles the cross-database complexity
SELECT
    o.order_id,
    c.customer_name,
    o.order_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
```

### 30. How do you handle model performance optimization?
**Answer:**
```sql
-- Clustering for better performance
{{ config(
    materialized='table',
    cluster_by=['order_date', 'customer_id']
) }}

-- Partitioning
{{ config(
    materialized='table',
    partition_by={
        "field": "order_date",
        "data_type": "date",
        "granularity": "day"
    }
) }}

-- Indexes (where supported)
{{ config(
    materialized='table',
    indexes=[
        {'columns': ['customer_id'], 'type': 'btree'},
        {'columns': ['order_date', 'status'], 'type': 'btree'}
    ]
) }}
```

---

## 🧪 Testing & Documentation

### 31. What are the built-in tests in DBT?
**Answer:**
- **unique**: Column values must be unique
- **not_null**: Column cannot contain null values
- **accepted_values**: Column values must be in specified list
- **relationships**: Foreign key constraint validation

```yaml
models:
  - name: orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
      - name: customer_id
        tests:
          - relationships:
              to: ref('customers')
              field: customer_id
```

### 32. How do you create custom generic tests?
**Answer:**
```sql
-- macros/test_valid_email.sql
{% test valid_email(model, column_name) %}
    SELECT *
    FROM {{ model }}
    WHERE {{ column_name }} IS NOT NULL
    AND NOT REGEXP_LIKE({{ column_name }}, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
{% endtest %}

-- Usage
models:
  - name: customers
    columns:
      - name: email
        tests:
          - valid_email
```

### 33. How do you implement data freshness tests?
**Answer:**
```yaml
sources:
  - name: raw_data
    tables:
      - name: orders
        freshness:
          warn_after: {count: 6, period: hour}
          error_after: {count: 12, period: hour}
        loaded_at_field: updated_at
```

```bash
# Run freshness tests
dbt source freshness
```

### 34. What are DBT test configurations?
**Answer:**
```yaml
tests:
  - name: assert_valid_order_totals
    config:
      severity: error  # or warn
      error_if: ">= 1"  # Fail if any rows returned
      warn_if: ">= 1"   # Warn if any rows returned
      limit: 100        # Limit rows in test output
      store_failures: true  # Store failed rows
```

### 35. How do you document DBT models?
**Answer:**
```yaml
# models/schema.yml
version: 2

models:
  - name: fct_orders
    description: |
      Order fact table containing all order transactions.
      
      This table is updated daily and includes:
      - Order details and amounts
      - Customer information
      - Product information
      - Payment details
      
      **Business Rules:**
      - One row per order
      - Orders are immutable once created
      - Cancelled orders remain in the table with status = 'cancelled'
    
    columns:
      - name: order_id
        description: "Unique identifier for each order (Primary Key)"
        tests:
          - unique
          - not_null
      
      - name: customer_id
        description: "Foreign key to dim_customers table"
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

### 36. How do you add model and column descriptions?
**Answer:**
```sql
-- In the model file
{{ config(
    description="Customer dimension table with SCD Type 2 implementation"
) }}

-- Column descriptions in schema.yml
models:
  - name: dim_customers
    description: "Customer dimension with historical tracking"
    columns:
      - name: customer_key
        description: "Surrogate key for customer dimension"
      - name: customer_id
        description: "Natural key from source system"
      - name: valid_from
        description: "Start date for this version of the customer record"
      - name: valid_to
        description: "End date for this version (NULL for current)"
```

### 37. How do you generate and serve DBT documentation?
**Answer:**
```bash
# Generate documentation
dbt docs generate

# Serve documentation locally
dbt docs serve --port 8080

# Generate with custom target
dbt docs generate --target prod

# Include sources in documentation
dbt docs generate --include-sources
```

### 38. What are DBT exposures?
**Answer:**
```yaml
# models/exposures.yml
version: 2

exposures:
  - name: weekly_sales_report
    type: dashboard
    maturity: high
    url: https://bi.company.com/dashboards/weekly-sales
    description: |
      Weekly sales performance dashboard used by the sales team
      to track KPIs and identify trends.
    
    depends_on:
      - ref('fct_sales')
      - ref('dim_products')
      - ref('dim_customers')
    
    owner:
      name: Sales Analytics Team
      email: sales-analytics@company.com
```

### 39. How do you implement data lineage tracking?
**Answer:**
DBT automatically tracks lineage through:
- **ref()** functions create model dependencies
- **source()** functions link to raw data
- **Manifest file** contains complete lineage graph
- **Documentation site** visualizes lineage

```sql
-- This model's lineage is automatically tracked
SELECT
    o.order_id,
    c.customer_name,
    p.product_name
FROM {{ ref('stg_orders') }} o  -- Dependency tracked
JOIN {{ ref('dim_customers') }} c ON o.customer_id = c.customer_id
JOIN {{ ref('dim_products') }} p ON o.product_id = p.product_id
```

### 40. How do you test data relationships across models?
**Answer:**
```yaml
# Test referential integrity
models:
  - name: fct_orders
    tests:
      - dbt_utils.equal_rowcount:
          compare_model: ref('stg_orders')
      
      - dbt_utils.fewer_rows_than:
          compare_model: ref('raw_orders')

# Custom relationship test
tests:
  - name: test_order_customer_relationship
    description: "Ensure all orders have valid customers"
```

```sql
-- tests/test_order_customer_relationship.sql
WITH order_customers AS (
    SELECT DISTINCT customer_id FROM {{ ref('fct_orders') }}
),
valid_customers AS (
    SELECT customer_id FROM {{ ref('dim_customers') }}
)

SELECT oc.customer_id
FROM order_customers oc
LEFT JOIN valid_customers vc ON oc.customer_id = vc.customer_id
WHERE vc.customer_id IS NULL
```

### 41. How do you implement test coverage metrics?
**Answer:**
```sql
-- Macro to check test coverage
{% macro get_test_coverage() %}
    {% set models_query %}
        SELECT COUNT(*) as total_models
        FROM {{ ref('dbt_models') }}
    {% endset %}
    
    {% set tested_models_query %}
        SELECT COUNT(DISTINCT model_name) as tested_models
        FROM {{ ref('dbt_tests') }}
        WHERE test_type IN ('unique', 'not_null', 'relationships', 'accepted_values')
    {% endset %}
    
    {% set results = run_query(models_query) %}
    {% set tested_results = run_query(tested_models_query) %}
    
    {{ log("Test Coverage: " ~ (tested_results[0][0] / results[0][0] * 100) ~ "%", info=True) }}
{% endmacro %}
```

### 42. How do you implement automated testing in CI/CD?
**Answer:**
```yaml
# .github/workflows/dbt_ci.yml
name: DBT CI
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
          python-version: '3.8'
      
      - name: Install DBT
        run: pip install dbt-snowflake
      
      - name: Run DBT tests
        run: |
          dbt deps
          dbt seed --target ci
          dbt run --target ci
          dbt test --target ci
        env:
          DBT_PROFILES_DIR: .
```

### 43. What are DBT test selection methods?
**Answer:**
```bash
# Run all tests
dbt test

# Test specific model
dbt test --select my_model

# Test model and downstream
dbt test --select my_model+

# Test by tag
dbt test --select tag:critical

# Test by test type
dbt test --select test_type:unique

# Test sources only
dbt test --select source:*

# Exclude certain tests
dbt test --exclude tag:slow
```

### 44. How do you handle test failures in production?
**Answer:**
```yaml
# Configure test behavior
tests:
  my_dbt_project:
    +severity: warn  # Don't fail pipeline on test failures
    
    critical_tests:
      +severity: error  # Fail pipeline for critical tests

# Store test failures for analysis
models:
  my_dbt_project:
    +store_failures: true
```

```sql
-- Query failed test results
SELECT *
FROM {{ ref('my_model_test_failures') }}
WHERE test_run_date = CURRENT_DATE
```

### 45. How do you implement data quality monitoring?
**Answer:**
```sql
-- macros/data_quality_checks.sql
{% macro data_quality_summary(model_name) %}
    SELECT
        '{{ model_name }}' as model_name,
        COUNT(*) as total_rows,
        COUNT(DISTINCT customer_id) as unique_customers,
        SUM(CASE WHEN order_total IS NULL THEN 1 ELSE 0 END) as null_order_totals,
        MIN(order_date) as min_order_date,
        MAX(order_date) as max_order_date,
        CURRENT_TIMESTAMP as check_timestamp
    FROM {{ ref(model_name) }}
{% endmacro %}

-- models/data_quality/dq_fct_orders.sql
{{ data_quality_summary('fct_orders') }}
```

---

## 🚀 Advanced Features

### 46. How do you implement DBT packages?
**Answer:**
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.0.0
  
  - package: calogica/dbt_expectations
    version: 0.8.5
  
  - git: "https://github.com/my-org/custom-dbt-package.git"
    revision: v1.2.0
  
  - local: ../local-package
```

```bash
# Install packages
dbt deps
```

### 47. What are DBT hooks and how do you use them?
**Answer:**
```yaml
# dbt_project.yml
on-run-start:
  - "CREATE SCHEMA IF NOT EXISTS {{ target.schema }}_audit"
  - "{{ log_run_start() }}"

on-run-end:
  - "{{ log_run_end() }}"
  - "{{ cleanup_temp_tables() }}"

models:
  my_project:
    +pre-hook: "{{ log_model_start() }}"
    +post-hook: 
      - "ANALYZE TABLE {{ this }}"
      - "{{ log_model_end() }}"
```

```sql
-- macros/logging_hooks.sql
{% macro log_run_start() %}
    INSERT INTO {{ target.schema }}_audit.run_log
    VALUES ('{{ run_started_at }}', 'RUN_START', '{{ invocation_id }}')
{% endmacro %}
```

### 48. How do you implement custom materializations?
**Answer:**
```sql
-- macros/materializations/my_custom_materialization.sql
{% materialization my_custom, default %}
  {%- set target_relation = this.incorporate(type='table') -%}
  {%- set existing_relation = load_relation(this) -%}
  {%- set tmp_relation = make_temp_relation(this) -%}

  {{ run_hooks(pre_hooks) }}

  -- Build model in temp table
  {% call statement('main') -%}
    {{ create_table_as(False, tmp_relation, sql) }}
  {%- endcall %}

  -- Swap tables atomically
  {% if existing_relation is not none %}
    {{ adapter.rename_relation(existing_relation, backup_relation) }}
  {% endif %}
  
  {{ adapter.rename_relation(tmp_relation, target_relation) }}

  {{ run_hooks(post_hooks) }}

  {{ return({'relations': [target_relation]}) }}
{% endmaterialization %}
```

### 49. How do you use DBT with different adapters?
**Answer:**
```yaml
# Snowflake adapter
profiles:
  snowflake_profile:
    target: dev
    outputs:
      dev:
        type: snowflake
        account: my_account
        warehouse: COMPUTE_WH
        database: DEV_DB
        schema: DBT_SCHEMA

# BigQuery adapter
profiles:
  bigquery_profile:
    target: dev
    outputs:
      dev:
        type: bigquery
        method: service-account
        project: my-project
        dataset: dbt_dataset
        keyfile: /path/to/keyfile.json

# Postgres adapter
profiles:
  postgres_profile:
    target: dev
    outputs:
      dev:
        type: postgres
        host: localhost
        user: postgres
        password: password
        port: 5432
        dbname: analytics
```

### 50. How do you implement cross-project dependencies?
**Answer:**
```yaml
# dependencies.yml in downstream project
projects:
  - name: upstream_project
    git: "https://github.com/company/upstream-dbt-project.git"
    revision: main

# Reference models from upstream project
SELECT * FROM {{ ref('upstream_project', 'shared_model') }}
```

### 51. How do you use DBT with orchestration tools?
**Answer:**
```python
# Airflow DAG
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG('dbt_pipeline', schedule_interval='@daily')

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='cd /dbt && dbt run --target prod',
    dag=dag
)

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='cd /dbt && dbt test --target prod',
    dag=dag
)

dbt_run >> dbt_test
```

### 52. How do you implement DBT state comparison?
**Answer:**
```bash
# Run only changed models
dbt run --state ./previous_state --defer

# Test only changed models
dbt test --state ./previous_state --defer

# Generate docs with state comparison
dbt docs generate --state ./previous_state
```

### 53. How do you use DBT selectors?
**Answer:**
```yaml
# selectors.yml
selectors:
  - name: critical_models
    definition:
      union:
        - tag:critical
        - config.materialized:table
  
  - name: daily_models
    definition:
      intersection:
        - tag:daily
        - config.materialized:incremental

# Usage
dbt run --selector critical_models
```

### 54. How do you implement DBT artifacts analysis?
**Answer:**
```python
# Analyze DBT artifacts
import json

# Load manifest
with open('target/manifest.json') as f:
    manifest = json.load(f)

# Analyze model performance
with open('target/run_results.json') as f:
    run_results = json.load(f)

for result in run_results['results']:
    model_name = result['unique_id']
    execution_time = result['execution_time']
    print(f"{model_name}: {execution_time}s")

# Find models without tests
models_with_tests = set()
for test in manifest['nodes'].values():
    if test['resource_type'] == 'test':
        for ref in test['refs']:
            models_with_tests.add(ref[0])

all_models = {node['name'] for node in manifest['nodes'].values() 
              if node['resource_type'] == 'model'}

untested_models = all_models - models_with_tests
print(f"Untested models: {untested_models}")
```

### 55. How do you implement DBT performance monitoring?
**Answer:**
```sql
-- models/monitoring/model_performance.sql
WITH model_runs AS (
    SELECT
        model_name,
        run_date,
        execution_time_seconds,
        rows_affected,
        status
    FROM {{ ref('dbt_run_results') }}
),

performance_metrics AS (
    SELECT
        model_name,
        AVG(execution_time_seconds) as avg_execution_time,
        MAX(execution_time_seconds) as max_execution_time,
        COUNT(*) as total_runs,
        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) / COUNT(*) as success_rate
    FROM model_runs
    WHERE run_date >= CURRENT_DATE - 30
    GROUP BY model_name
)

SELECT
    model_name,
    avg_execution_time,
    max_execution_time,
    total_runs,
    success_rate,
    CASE
        WHEN avg_execution_time > 300 THEN 'Slow'
        WHEN success_rate < 0.95 THEN 'Unreliable'
        ELSE 'Good'
    END as performance_status
FROM performance_metrics
ORDER BY avg_execution_time DESC
```

### 56. How do you implement DBT with version control strategies?
**Answer:**
```bash
# Feature branch workflow
git checkout -b feature/new-model
# Make changes
dbt run --target dev
dbt test --target dev
git commit -m "Add new customer segmentation model"
git push origin feature/new-model

# Production deployment
git checkout main
git merge feature/new-model
dbt run --target prod
dbt test --target prod

# Rollback strategy
git revert <commit-hash>
dbt run --target prod --full-refresh
```

### 57. How do you handle DBT secrets and credentials?
**Answer:**
```yaml
# Use environment variables
profiles:
  my_profile:
    target: "{{ env_var('DBT_TARGET', 'dev') }}"
    outputs:
      prod:
        type: snowflake
        account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
        user: "{{ env_var('SNOWFLAKE_USER') }}"
        password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
        warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"

# Use DBT Cloud environment variables
# Or external secret management
```

### 58. How do you implement DBT model contracts?
**Answer:**
```yaml
# models/schema.yml
version: 2

models:
  - name: dim_customers
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: varchar(50)
        constraints:
          - type: not_null
          - type: primary_key
      
      - name: customer_name
        data_type: varchar(255)
        constraints:
          - type: not_null
      
      - name: email
        data_type: varchar(255)
        constraints:
          - type: unique
```

### 59. How do you implement DBT unit testing?
**Answer:**
```yaml
# Unit tests (DBT 1.8+)
unit_tests:
  - name: test_customer_segmentation
    model: customer_segments
    given:
      - input: ref('customers')
        rows:
          - {customer_id: 1, total_spent: 15000}
          - {customer_id: 2, total_spent: 500}
    expect:
      rows:
        - {customer_id: 1, segment: 'VIP'}
        - {customer_id: 2, segment: 'Standard'}
```

### 60. How do you implement DBT governance and compliance?
**Answer:**
```yaml
# Governance configuration
models:
  my_project:
    +meta:
      owner: "data-team@company.com"
      classification: "internal"
      retention_days: 2555  # 7 years
      contains_pii: false
    
    sensitive_data:
      +meta:
        classification: "confidential"
        contains_pii: true
        access_level: "restricted"

# Compliance checks
tests:
  - name: check_pii_masking
    description: "Ensure PII fields are properly masked"
```

---

## 🔧 Operations & Best Practices

### 61. What are DBT deployment strategies?
**Answer:**
**Blue-Green Deployment:**
```bash
# Deploy to green environment
dbt run --target green
dbt test --target green

# Switch traffic to green
# Update load balancer/DNS

# Keep blue as rollback option
```

**Rolling Deployment:**
```bash
# Deploy models incrementally
dbt run --select tag:tier1
dbt test --select tag:tier1

dbt run --select tag:tier2
dbt test --select tag:tier2
```

### 62. How do you implement DBT monitoring and alerting?
**Answer:**
```python
# Monitoring script
import json
import requests

def check_dbt_run_status():
    with open('target/run_results.json') as f:
        results = json.load(f)
    
    failed_models = [
        r['unique_id'] for r in results['results'] 
        if r['status'] == 'error'
    ]
    
    if failed_models:
        send_alert(f"DBT run failed for models: {failed_models}")
    
    # Check execution times
    slow_models = [
        r['unique_id'] for r in results['results']
        if r['execution_time'] > 300  # 5 minutes
    ]
    
    if slow_models:
        send_warning(f"Slow DBT models detected: {slow_models}")

def send_alert(message):
    # Send to Slack, email, PagerDuty, etc.
    requests.post(webhook_url, json={'text': message})
```

### 63. How do you optimize DBT performance?
**Answer:**
```yaml
# dbt_project.yml optimizations
models:
  my_project:
    # Use appropriate materializations
    staging:
      +materialized: view
    marts:
      +materialized: table
    
    # Optimize incremental models
    incremental_models:
      +materialized: incremental
      +incremental_strategy: merge
      +on_schema_change: sync_all_columns

# Use threading
dbt run --threads 8

# Partial parsing
dbt run --partial-parse

# Use selectors for targeted runs
dbt run --select state:modified+
```

### 64. What are DBT naming conventions?
**Answer:**
```
# Folder structure
models/
├── staging/           # stg_<source>_<table>
│   ├── stg_salesforce_accounts.sql
│   └── stg_stripe_payments.sql
├── intermediate/      # int_<business_concept>
│   ├── int_customer_orders.sql
│   └── int_payment_aggregates.sql
└── marts/            # fct_<business_process> / dim_<entity>
    ├── core/
    │   ├── fct_orders.sql
    │   └── dim_customers.sql
    └── finance/
        └── fct_revenue.sql

# Naming patterns
- Sources: raw table names
- Staging: stg_<source>_<table>
- Intermediate: int_<business_concept>
- Facts: fct_<business_process>
- Dimensions: dim_<entity>
```

### 65. How do you implement DBT code reviews?
**Answer:**
```yaml
# .github/pull_request_template.md
## DBT Changes Checklist

### Model Changes
- [ ] New models follow naming conventions
- [ ] Models have appropriate materialization
- [ ] Models include description and column documentation
- [ ] Tests are added for new models

### Performance
- [ ] Query performance has been considered
- [ ] Appropriate indexes/clustering added
- [ ] Incremental strategy is optimal

### Testing
- [ ] All tests pass locally
- [ ] Data quality tests are comprehensive
- [ ] Edge cases are handled

### Documentation
- [ ] Schema.yml updated with descriptions
- [ ] Business logic is documented
- [ ] Breaking changes are noted
```

### 66. How do you handle DBT environment management?
**Answer:**
```yaml
# profiles.yml
my_project:
  target: "{{ env_var('DBT_TARGET', 'dev') }}"
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      database: DEV_DB
      schema: "dbt_{{ env_var('USER', 'unknown') }}"
      warehouse: DEV_WH
    
    staging:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      database: STAGING_DB
      schema: DBT_STAGING
      warehouse: STAGING_WH
    
    prod:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      database: PROD_DB
      schema: DBT_PROD
      warehouse: PROD_WH
```

### 67. How do you implement DBT data lineage governance?
**Answer:**
```python
# Lineage analysis script
import json
import networkx as nx

def analyze_dbt_lineage():
    with open('target/manifest.json') as f:
        manifest = json.load(f)
    
    # Build dependency graph
    G = nx.DiGraph()
    
    for node_id, node in manifest['nodes'].items():
        if node['resource_type'] == 'model':
            G.add_node(node_id, **node)
            
            # Add dependencies
            for dep in node['depends_on']['nodes']:
                G.add_edge(dep, node_id)
    
    # Find critical path models
    critical_models = []
    for node in G.nodes():
        if G.out_degree(node) > 5:  # Models with many dependents
            critical_models.append(node)
    
    # Find orphaned models
    orphaned_models = [node for node in G.nodes() if G.out_degree(node) == 0]
    
    return {
        'critical_models': critical_models,
        'orphaned_models': orphaned_models,
        'total_models': len(G.nodes())
    }
```

### 68. How do you implement DBT cost optimization?
**Answer:**
```sql
-- Cost monitoring model
WITH model_costs AS (
    SELECT
        model_name,
        execution_date,
        warehouse_size,
        execution_time_seconds,
        -- Estimate cost based on warehouse size and time
        CASE warehouse_size
            WHEN 'X-SMALL' THEN execution_time_seconds * 0.0003
            WHEN 'SMALL' THEN execution_time_seconds * 0.0006
            WHEN 'MEDIUM' THEN execution_time_seconds * 0.0012
            WHEN 'LARGE' THEN execution_time_seconds * 0.0024
        END as estimated_cost_usd
    FROM {{ ref('dbt_run_metadata') }}
),

daily_costs AS (
    SELECT
        execution_date,
        SUM(estimated_cost_usd) as daily_cost,
        COUNT(*) as models_run
    FROM model_costs
    GROUP BY execution_date
)

SELECT
    execution_date,
    daily_cost,
    models_run,
    daily_cost / models_run as avg_cost_per_model
FROM daily_costs
ORDER BY execution_date DESC
```

### 69. How do you implement DBT disaster recovery?
**Answer:**
```bash
#!/bin/bash
# DBT disaster recovery script

# Backup DBT artifacts
backup_artifacts() {
    aws s3 cp target/ s3://dbt-backups/$(date +%Y%m%d)/ --recursive
    aws s3 cp logs/ s3://dbt-backups/$(date +%Y%m%d)/logs/ --recursive
}

# Restore from backup
restore_artifacts() {
    local backup_date=$1
    aws s3 cp s3://dbt-backups/$backup_date/ target/ --recursive
    aws s3 cp s3://dbt-backups/$backup_date/logs/ logs/ --recursive
}

# Emergency rollback
emergency_rollback() {
    # Restore previous state
    restore_artifacts $(date -d "yesterday" +%Y%m%d)
    
    # Run with previous state
    dbt run --state target/
    dbt test --state target/
}
```

### 70. How do you implement DBT security best practices?
**Answer:**
```yaml
# Security configuration
models:
  my_project:
    # Sensitive data models
    sensitive:
      +meta:
        contains_pii: true
        access_level: "restricted"
      +materialized: table
      +post-hook: "GRANT SELECT ON {{ this }} TO ROLE sensitive_data_readers"
    
    # Public models
    public:
      +materialized: view
      +post-hook: "GRANT SELECT ON {{ this }} TO ROLE all_users"

# Row-level security
{{ config(
    post_hook="CREATE ROW ACCESS POLICY customer_policy ON {{ this }} 
               GRANT TO ('CUSTOMER_ROLE') 
               FILTER USING (customer_id = CURRENT_USER())"
) }}
```

### 71. How do you implement DBT change management?
**Answer:**
```yaml
# Change management workflow
name: DBT Change Management
on:
  pull_request:
    branches: [main]

jobs:
  validate_changes:
    runs-on: ubuntu-latest
    steps:
      - name: Check breaking changes
        run: |
          # Compare schemas
          dbt run --state ./prod_state --defer --target ci
          
          # Check for column removals
          python scripts/check_breaking_changes.py
      
      - name: Impact analysis
        run: |
          # Generate impact report
          dbt ls --state ./prod_state --select state:modified+ --output json > impact.json
          
          # Notify stakeholders
          python scripts/notify_stakeholders.py impact.json
```

### 72. How do you implement DBT metadata management?
**Answer:**
```sql
-- Metadata collection model
WITH model_metadata AS (
    SELECT
        model_name,
        model_type,
        materialization,
        owner,
        description,
        tags,
        created_date,
        last_modified_date,
        row_count,
        column_count,
        file_size_mb
    FROM {{ ref('dbt_model_registry') }}
),

usage_stats AS (
    SELECT
        model_name,
        COUNT(*) as query_count,
        COUNT(DISTINCT user_name) as unique_users,
        MAX(last_accessed) as last_accessed_date
    FROM {{ ref('query_history') }}
    WHERE query_date >= CURRENT_DATE - 30
    GROUP BY model_name
)

SELECT
    m.*,
    COALESCE(u.query_count, 0) as monthly_queries,
    COALESCE(u.unique_users, 0) as monthly_users,
    u.last_accessed_date,
    CASE
        WHEN u.query_count IS NULL THEN 'Unused'
        WHEN u.query_count < 10 THEN 'Low Usage'
        WHEN u.query_count < 100 THEN 'Medium Usage'
        ELSE 'High Usage'
    END as usage_category
FROM model_metadata m
LEFT JOIN usage_stats u ON m.model_name = u.model_name
```

### 73. How do you implement DBT quality gates?
**Answer:**
```python
# Quality gates script
import json
import sys

def check_quality_gates():
    # Load test results
    with open('target/run_results.json') as f:
        results = json.load(f)
    
    # Quality gate 1: No test failures
    test_failures = [r for r in results['results'] if r['status'] == 'error']
    if test_failures:
        print(f"❌ Quality Gate Failed: {len(test_failures)} test failures")
        return False
    
    # Quality gate 2: Performance threshold
    slow_models = [r for r in results['results'] if r['execution_time'] > 600]
    if slow_models:
        print(f"⚠️  Warning: {len(slow_models)} models exceed 10min execution time")
    
    # Quality gate 3: Coverage threshold
    coverage = calculate_test_coverage()
    if coverage < 0.8:
        print(f"❌ Quality Gate Failed: Test coverage {coverage:.1%} below 80%")
        return False
    
    print("✅ All quality gates passed")
    return True

if __name__ == "__main__":
    if not check_quality_gates():
        sys.exit(1)
```

### 74. How do you implement DBT multi-tenant architecture?
**Answer:**
```yaml
# Multi-tenant configuration
models:
  my_project:
    tenant_a:
      +schema: tenant_a
      +database: "{{ 'TENANT_A_' + target.name | upper }}"
    
    tenant_b:
      +schema: tenant_b
      +database: "{{ 'TENANT_B_' + target.name | upper }}"

# Tenant-specific variables
vars:
  tenant_configs:
    tenant_a:
      source_schema: raw_tenant_a
      retention_days: 2555
    tenant_b:
      source_schema: raw_tenant_b
      retention_days: 1825
```

```sql
-- Tenant-aware model
{% set tenant_config = var('tenant_configs')[var('current_tenant')] %}

SELECT *
FROM {{ source(tenant_config.source_schema, 'orders') }}
WHERE created_at >= CURRENT_DATE - {{ tenant_config.retention_days }}
```

### 75. How do you implement DBT enterprise governance?
**Answer:**
```yaml
# Enterprise governance framework
governance:
  data_classification:
    public:
      - models/marts/public/
    internal:
      - models/marts/internal/
    confidential:
      - models/marts/sensitive/
  
  approval_workflows:
    production_changes:
      required_approvers: 2
      required_roles: ["data_engineer", "data_architect"]
    
    schema_changes:
      required_approvers: 1
      required_roles: ["data_architect"]
  
  compliance_checks:
    - name: pii_detection
      pattern: "(?i)(ssn|social.security|credit.card)"
      action: block
    
    - name: retention_policy
      check: models must have retention metadata
      action: warn

# Automated governance checks
tests:
  - name: governance_compliance
    description: "Ensure all models meet governance requirements"
```

---

## 🎯 **Quick Reference Commands**

```bash
# Basic commands
dbt run                    # Run all models
dbt test                   # Run all tests
dbt docs generate          # Generate documentation
dbt docs serve            # Serve documentation

# Selection syntax
dbt run --select my_model              # Run specific model
dbt run --select my_model+             # Run model and downstream
dbt run --select +my_model             # Run model and upstream
dbt run --select tag:daily             # Run models with tag
dbt run --select @my_model             # Run model and neighbors

# Environment management
dbt run --target prod                  # Run against production
dbt run --vars '{"key": "value"}'      # Pass variables

# State comparison
dbt run --state ./prod_state --defer   # Run only changed models
dbt test --state ./prod_state          # Test only changed models

# Debugging
dbt compile                           # Compile without running
dbt show --select my_model            # Preview model results
dbt debug                            # Check configuration
```

---

**Total Questions: 75** | **Difficulty: Beginner to Expert** | **Coverage: Complete DBT Ecosystem**