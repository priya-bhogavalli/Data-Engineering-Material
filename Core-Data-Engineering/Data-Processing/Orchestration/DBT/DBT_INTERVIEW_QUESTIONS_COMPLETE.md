# DBT Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Modeling & Architecture (91-120)](#modeling--architecture-91-120)
5. [Testing & Documentation (121-150)](#testing--documentation-121-150)
6. [Production & Deployment (151-180)](#production--deployment-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is DBT and how does it work?

**DBT (Data Build Tool)** is a command-line tool that enables data analysts and engineers to transform data in their warehouse more effectively using SQL and software engineering best practices.

#### **Key Components:**

| Component | Description | Purpose |
|-----------|-------------|---------|
| **Models** | SQL files that define transformations | Data transformation logic |
| **Tests** | Assertions about data quality | Data validation |
| **Documentation** | Descriptions and metadata | Knowledge sharing |
| **Macros** | Reusable SQL code | Code reusability |
| **Seeds** | CSV files for reference data | Static data loading |
| **Snapshots** | SCD Type 2 implementation | Historical data tracking |

```sql
-- Example DBT model: models/staging/stg_customers.sql
{{ config(materialized='view') }}

WITH source_data AS (
    SELECT 
        customer_id,
        first_name,
        last_name,
        email,
        phone,
        created_at,
        updated_at
    FROM {{ source('raw_data', 'customers') }}
),

cleaned_data AS (
    SELECT 
        customer_id,
        TRIM(UPPER(first_name)) AS first_name,
        TRIM(UPPER(last_name)) AS last_name,
        LOWER(TRIM(email)) AS email,
        REGEXP_REPLACE(phone, '[^0-9]', '') AS phone_clean,
        created_at,
        updated_at,
        CONCAT(TRIM(UPPER(first_name)), ' ', TRIM(UPPER(last_name))) AS full_name
    FROM source_data
    WHERE customer_id IS NOT NULL
        AND email IS NOT NULL
        AND email LIKE '%@%'
)

SELECT * FROM cleaned_data
```

**Output (when compiled):**
```sql
CREATE VIEW analytics.staging.stg_customers AS (
    WITH source_data AS (
        SELECT 
            customer_id,
            first_name,
            last_name,
            email,
            phone,
            created_at,
            updated_at
        FROM raw_data.customers
    ),
    
    cleaned_data AS (
        SELECT 
            customer_id,
            TRIM(UPPER(first_name)) AS first_name,
            TRIM(UPPER(last_name)) AS last_name,
            LOWER(TRIM(email)) AS email,
            REGEXP_REPLACE(phone, '[^0-9]', '') AS phone_clean,
            created_at,
            updated_at,
            CONCAT(TRIM(UPPER(first_name)), ' ', TRIM(UPPER(last_name))) AS full_name
        FROM source_data
        WHERE customer_id IS NOT NULL
            AND email IS NOT NULL
            AND email LIKE '%@%'
    )
    
    SELECT * FROM cleaned_data
);
```

### 2. What are DBT models and materialization types?

**Answer:** DBT models are SQL files that define data transformations with different materialization strategies.

#### 🎯 **Materialization Types**
- **View**: Virtual table, computed on query
- **Table**: Physical table, pre-computed
- **Incremental**: Append/update only new data
- **Ephemeral**: CTE, not materialized

```sql
-- models/marts/dim_customers.sql
{{ config(
    materialized='table',
    indexes=[
        {'columns': ['customer_id'], 'unique': True},
        {'columns': ['email'], 'unique': True}
    ]
) }}

WITH customer_base AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) AS total_orders,
        SUM(order_amount) AS lifetime_value,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date,
        AVG(order_amount) AS avg_order_value
    FROM {{ ref('stg_orders') }}
    GROUP BY customer_id
),

final AS (
    SELECT 
        c.customer_id,
        c.full_name,
        c.email,
        c.phone_clean,
        c.created_at,
        COALESCE(m.total_orders, 0) AS total_orders,
        COALESCE(m.lifetime_value, 0) AS lifetime_value,
        COALESCE(m.avg_order_value, 0) AS avg_order_value,
        m.first_order_date,
        m.last_order_date,
        CASE 
            WHEN m.lifetime_value >= 1000 THEN 'High Value'
            WHEN m.lifetime_value >= 500 THEN 'Medium Value'
            WHEN m.lifetime_value > 0 THEN 'Low Value'
            ELSE 'No Orders'
        END AS customer_segment,
        CURRENT_TIMESTAMP() AS dbt_updated_at
    FROM customer_base c
    LEFT JOIN customer_metrics m ON c.customer_id = m.customer_id
)

SELECT * FROM final

-- Incremental model example: models/marts/fct_daily_sales.sql
{{ config(
    materialized='incremental',
    unique_key='date_day',
    on_schema_change='fail'
) }}

WITH daily_aggregates AS (
    SELECT 
        DATE(order_date) AS date_day,
        COUNT(*) AS total_orders,
        COUNT(DISTINCT customer_id) AS unique_customers,
        SUM(order_amount) AS total_revenue,
        AVG(order_amount) AS avg_order_value,
        MIN(order_amount) AS min_order_value,
        MAX(order_amount) AS max_order_value
    FROM {{ ref('stg_orders') }}
    
    {% if is_incremental() %}
        WHERE DATE(order_date) > (SELECT MAX(date_day) FROM {{ this }})
    {% endif %}
    
    GROUP BY DATE(order_date)
)

SELECT 
    *,
    CURRENT_TIMESTAMP() AS dbt_updated_at
FROM daily_aggregates
```

**DBT Run Output:**
```
Running with dbt=1.7.0
Found 3 models, 0 tests, 0 snapshots, 0 analyses, 0 macros, 0 operations, 0 seed files, 0 sources, 0 exposures, 0 metrics, 0 groups

Completed successfully

Done. PASS=3 WARN=0 ERROR=0 SKIP=0 TOTAL=3
```

### 3. How do you define sources and references in DBT?

**Answer:** Sources define external data, refs create dependencies between models.

#### 🎯 **Sources vs References**
- **Sources**: External tables (raw data)
- **References**: DBT models (transformed data)
- **Dependencies**: Automatic lineage tracking

```yaml
# models/staging/sources.yml
version: 2

sources:
  - name: raw_data
    description: Raw data from operational systems
    database: raw_db
    schema: public
    tables:
      - name: customers
        description: Customer master data
        columns:
          - name: customer_id
            description: Unique customer identifier
            tests:
              - unique
              - not_null
          - name: email
            description: Customer email address
            tests:
              - not_null
              - unique
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
          
      - name: orders
        description: Order transaction data
        columns:
          - name: order_id
            description: Unique order identifier
            tests:
              - unique
              - not_null
          - name: customer_id
            description: Foreign key to customers
            tests:
              - not_null
              - relationships:
                  to: source('raw_data', 'customers')
                  field: customer_id
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 6, period: hour}
          error_after: {count: 12, period: hour}

  - name: external_apis
    description: Data from external API sources
    database: api_db
    schema: staging
    tables:
      - name: product_catalog
        description: Product information from catalog API
```

```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

WITH source_orders AS (
    SELECT 
        order_id,
        customer_id,
        product_id,
        order_date,
        order_amount,
        status,
        created_at,
        updated_at
    FROM {{ source('raw_data', 'orders') }}
),

enriched_orders AS (
    SELECT 
        o.order_id,
        o.customer_id,
        o.product_id,
        o.order_date,
        o.order_amount,
        UPPER(TRIM(o.status)) AS status,
        o.created_at,
        o.updated_at,
        
        -- Add calculated fields
        EXTRACT(YEAR FROM o.order_date) AS order_year,
        EXTRACT(MONTH FROM o.order_date) AS order_month,
        EXTRACT(DOW FROM o.order_date) AS order_day_of_week,
        
        -- Business logic
        CASE 
            WHEN o.order_amount >= 500 THEN 'Large'
            WHEN o.order_amount >= 100 THEN 'Medium'
            ELSE 'Small'
        END AS order_size_category
        
    FROM source_orders o
    WHERE o.order_id IS NOT NULL
        AND o.customer_id IS NOT NULL
        AND o.order_amount > 0
)

SELECT * FROM enriched_orders

-- models/marts/customer_order_summary.sql
{{ config(materialized='table') }}

WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customer_summary AS (
    SELECT 
        c.customer_id,
        c.full_name,
        c.email,
        c.created_at AS customer_created_at,
        
        -- Order metrics
        COUNT(o.order_id) AS total_orders,
        SUM(o.order_amount) AS total_spent,
        AVG(o.order_amount) AS avg_order_value,
        MIN(o.order_date) AS first_order_date,
        MAX(o.order_date) AS last_order_date,
        
        -- Order categories
        SUM(CASE WHEN o.order_size_category = 'Large' THEN 1 ELSE 0 END) AS large_orders,
        SUM(CASE WHEN o.order_size_category = 'Medium' THEN 1 ELSE 0 END) AS medium_orders,
        SUM(CASE WHEN o.order_size_category = 'Small' THEN 1 ELSE 0 END) AS small_orders,
        
        -- Recency metrics
        DATEDIFF('day', MAX(o.order_date), CURRENT_DATE()) AS days_since_last_order
        
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.full_name, c.email, c.created_at
)

SELECT 
    *,
    CASE 
        WHEN days_since_last_order IS NULL THEN 'Never Ordered'
        WHEN days_since_last_order <= 30 THEN 'Active'
        WHEN days_since_last_order <= 90 THEN 'At Risk'
        ELSE 'Churned'
    END AS customer_status
FROM customer_summary
```

**DBT Lineage Output:**
```
Lineage for customer_order_summary:
  └── stg_customers
      └── source('raw_data', 'customers')
  └── stg_orders
      └── source('raw_data', 'orders')
```

### 4. What are DBT tests and how do you implement them?

**Answer:** DBT tests are assertions about data quality that run automatically during builds.

#### 🎯 **Test Types**
- **Generic Tests**: Built-in tests (unique, not_null, etc.)
- **Singular Tests**: Custom SQL assertions
- **Data Tests**: Column-level validations
- **Schema Tests**: Structure validations

```yaml
# models/staging/schema.yml
version: 2

models:
  - name: stg_customers
    description: Cleaned customer data from raw source
    columns:
      - name: customer_id
        description: Unique customer identifier
        tests:
          - unique
          - not_null
      - name: email
        description: Customer email address
        tests:
          - unique
          - not_null
          - dbt_utils.email_format
      - name: phone_clean
        description: Cleaned phone number (digits only)
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_match_regex:
              regex: '^[0-9]{10}$'
      - name: full_name
        description: Concatenated first and last name
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_not_be_null

  - name: stg_orders
    description: Cleaned order data from raw source
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - order_id
            - customer_id
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id
      - name: order_amount
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 10000
      - name: status
        tests:
          - accepted_values:
              values: ['PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED']
```

```sql
-- tests/assert_positive_order_amounts.sql
-- Singular test to ensure all order amounts are positive
SELECT 
    order_id,
    order_amount
FROM {{ ref('stg_orders') }}
WHERE order_amount <= 0

-- tests/assert_customer_email_domains.sql
-- Test to ensure email domains are from allowed list
WITH email_domains AS (
    SELECT 
        customer_id,
        email,
        SPLIT_PART(email, '@', 2) AS domain
    FROM {{ ref('stg_customers') }}
),

invalid_domains AS (
    SELECT *
    FROM email_domains
    WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'hotmail.com', 'company.com')
)

SELECT * FROM invalid_domains

-- tests/assert_order_date_consistency.sql
-- Test to ensure order dates are not in the future
SELECT 
    order_id,
    order_date,
    CURRENT_DATE() AS today
FROM {{ ref('stg_orders') }}
WHERE order_date > CURRENT_DATE()

-- Custom macro for reusable test logic
-- macros/test_data_freshness.sql
{% macro test_data_freshness(model, timestamp_column, max_age_hours=24) %}
    SELECT 
        COUNT(*) AS stale_records
    FROM {{ model }}
    WHERE {{ timestamp_column }} < DATEADD('hour', -{{ max_age_hours }}, CURRENT_TIMESTAMP())
    HAVING COUNT(*) > 0
{% endmacro %}

-- tests/assert_customer_data_freshness.sql
{{ test_data_freshness(ref('stg_customers'), 'updated_at', 48) }}
```

**DBT Test Output:**
```
Running with dbt=1.7.0
Found 3 models, 12 tests, 0 snapshots, 0 analyses, 1 macro, 0 operations, 0 seed files, 2 sources, 0 exposures, 0 metrics, 0 groups

Test results:
  PASS unique_stg_customers_customer_id
  PASS not_null_stg_customers_customer_id
  PASS unique_stg_customers_email
  PASS not_null_stg_customers_email
  PASS relationships_stg_orders_customer_id__customer_id__ref_stg_customers_
  PASS accepted_values_stg_orders_status__PENDING__CONFIRMED__SHIPPED__DELIVERED__CANCELLED
  PASS assert_positive_order_amounts
  PASS assert_customer_email_domains
  PASS assert_order_date_consistency
  FAIL assert_customer_data_freshness (1 row returned)

Completed with 1 error and 0 warnings:

Failure in test assert_customer_data_freshness (tests/assert_customer_data_freshness.sql)
  Got 1 result, expected 0.

Done. PASS=8 WARN=0 ERROR=1 SKIP=0 TOTAL=9
```

### 5. How do you use DBT macros for code reusability?

**Answer:** Macros are reusable SQL functions that generate code dynamically.

#### 🎯 **Macro Types**
- **Simple Macros**: Basic code generation
- **Parameterized Macros**: Accept arguments
- **Control Flow**: Loops and conditionals
- **Built-in Macros**: DBT utilities

```sql
-- macros/generate_schema_name.sql
-- Custom macro to control schema naming
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ default_schema }}_{{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}

-- macros/get_date_spine.sql
-- Macro to generate date spine for time series analysis
{% macro get_date_spine(start_date, end_date, datepart='day') %}
    WITH date_spine AS (
        {{ dbt_utils.date_spine(
            datepart=datepart,
            start_date="'" + start_date + "'",
            end_date="'" + end_date + "'"
        ) }}
    )
    SELECT 
        date_{{ datepart }} AS spine_date,
        EXTRACT(YEAR FROM date_{{ datepart }}) AS spine_year,
        EXTRACT(MONTH FROM date_{{ datepart }}) AS spine_month,
        EXTRACT(DAY FROM date_{{ datepart }}) AS spine_day,
        EXTRACT(DOW FROM date_{{ datepart }}) AS spine_day_of_week
    FROM date_spine
{% endmacro %}

-- macros/pivot_table.sql
-- Dynamic pivot macro
{% macro pivot_table(table_name, group_by_col, pivot_col, agg_col, agg_func='sum') %}
    {%- set pivot_values_query -%}
        SELECT DISTINCT {{ pivot_col }}
        FROM {{ table_name }}
        WHERE {{ pivot_col }} IS NOT NULL
        ORDER BY {{ pivot_col }}
    {%- endset -%}
    
    {%- set results = run_query(pivot_values_query) -%}
    {%- if execute -%}
        {%- set pivot_values = results.columns[0].values() -%}
    {%- else -%}
        {%- set pivot_values = [] -%}
    {%- endif -%}
    
    SELECT 
        {{ group_by_col }},
        {%- for value in pivot_values %}
        {{ agg_func }}(CASE WHEN {{ pivot_col }} = '{{ value }}' THEN {{ agg_col }} END) AS {{ value | replace(' ', '_') | replace('-', '_') | lower }}
        {%- if not loop.last -%},{%- endif -%}
        {%- endfor %}
    FROM {{ table_name }}
    GROUP BY {{ group_by_col }}
{% endmacro %}

-- macros/audit_helper.sql
-- Macro for data quality auditing
{% macro audit_helper(model_name, audit_columns=[]) %}
    {%- if audit_columns | length == 0 -%}
        {%- set audit_columns = adapter.get_columns_in_relation(ref(model_name)) -%}
    {%- endif -%}
    
    WITH audit_summary AS (
        SELECT 
            '{{ model_name }}' AS model_name,
            COUNT(*) AS total_rows,
            {%- for column in audit_columns %}
            COUNT({{ column.name }}) AS {{ column.name }}_non_null_count,
            COUNT(*) - COUNT({{ column.name }}) AS {{ column.name }}_null_count,
            {%- if column.dtype in ('varchar', 'text', 'string') %}
            COUNT(DISTINCT {{ column.name }}) AS {{ column.name }}_distinct_count,
            {%- endif %}
            {%- if not loop.last -%},{%- endif -%}
            {%- endfor %}
            CURRENT_TIMESTAMP() AS audit_timestamp
        FROM {{ ref(model_name) }}
    )
    SELECT * FROM audit_summary
{% endmacro %}

-- Using macros in models
-- models/marts/daily_sales_pivot.sql
{{ config(materialized='table') }}

WITH daily_sales AS (
    SELECT 
        DATE(order_date) AS sale_date,
        status,
        SUM(order_amount) AS total_amount
    FROM {{ ref('stg_orders') }}
    GROUP BY DATE(order_date), status
)

{{ pivot_table('daily_sales', 'sale_date', 'status', 'total_amount', 'sum') }}

-- models/utils/date_spine.sql
{{ config(materialized='table') }}

{{ get_date_spine('2023-01-01', '2024-12-31', 'day') }}

-- models/audit/customer_audit.sql
{{ config(materialized='view') }}

{{ audit_helper('stg_customers') }}

-- Advanced macro with control flow
-- macros/generate_surrogate_key.sql
{% macro generate_surrogate_key(columns) %}
    {%- if columns is string -%}
        {%- set columns = [columns] -%}
    {%- endif -%}
    
    {%- set concatenated_values -%}
        {%- for column in columns -%}
            COALESCE(CAST({{ column }} AS VARCHAR), 'NULL')
            {%- if not loop.last -%} || '|' || {%- endif -%}
        {%- endfor -%}
    {%- endset -%}
    
    {{ dbt_utils.hash(concatenated_values) }}
{% endmacro %}

-- models/marts/dim_customer_enhanced.sql
{{ config(materialized='table') }}

SELECT 
    {{ generate_surrogate_key(['customer_id', 'email']) }} AS customer_key,
    customer_id,
    full_name,
    email,
    phone_clean,
    created_at,
    CURRENT_TIMESTAMP() AS dbt_updated_at
FROM {{ ref('stg_customers') }}
```

**Macro Compilation Output:**
```sql
-- Compiled daily_sales_pivot.sql
WITH daily_sales AS (
    SELECT 
        DATE(order_date) AS sale_date,
        status,
        SUM(order_amount) AS total_amount
    FROM analytics.staging.stg_orders
    GROUP BY DATE(order_date), status
)

SELECT 
    sale_date,
    sum(CASE WHEN status = 'CANCELLED' THEN total_amount END) AS cancelled,
    sum(CASE WHEN status = 'CONFIRMED' THEN total_amount END) AS confirmed,
    sum(CASE WHEN status = 'DELIVERED' THEN total_amount END) AS delivered,
    sum(CASE WHEN status = 'PENDING' THEN total_amount END) AS pending,
    sum(CASE WHEN status = 'SHIPPED' THEN total_amount END) AS shipped
FROM daily_sales
GROUP BY sale_date

-- Compiled customer_audit.sql
WITH audit_summary AS (
    SELECT 
        'stg_customers' AS model_name,
        COUNT(*) AS total_rows,
        COUNT(customer_id) AS customer_id_non_null_count,
        COUNT(*) - COUNT(customer_id) AS customer_id_null_count,
        COUNT(full_name) AS full_name_non_null_count,
        COUNT(*) - COUNT(full_name) AS full_name_null_count,
        COUNT(DISTINCT full_name) AS full_name_distinct_count,
        COUNT(email) AS email_non_null_count,
        COUNT(*) - COUNT(email) AS email_null_count,
        COUNT(DISTINCT email) AS email_distinct_count,
        CURRENT_TIMESTAMP() AS audit_timestamp
    FROM analytics.staging.stg_customers
)
SELECT * FROM audit_summary
```

**DBT Macro Usage Output:**
```
MODEL_NAME    | TOTAL_ROWS | CUSTOMER_ID_NON_NULL_COUNT | EMAIL_DISTINCT_COUNT | AUDIT_TIMESTAMP
--------------|------------|----------------------------|---------------------|------------------
stg_customers | 1,000      | 1,000                      | 1,000               | 2024-01-15 10:30:00
```