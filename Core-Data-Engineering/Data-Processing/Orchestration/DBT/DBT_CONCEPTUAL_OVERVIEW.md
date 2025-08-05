# DBT (Data Build Tool) - Conceptual Overview

## 🎯 What is DBT?

DBT (Data Build Tool) is a **transformation workflow tool** that enables data analysts and engineers to transform raw data in their warehouse by simply writing select statements. Think of DBT as the "T" in ELT (Extract, Load, Transform) - it handles the transformation layer with software engineering best practices like version control, testing, and documentation.

### Key Characteristics:
- **SQL-First**: Write transformations using familiar SQL
- **Version Control**: Git-based workflow for collaboration
- **Testing**: Built-in data quality testing framework
- **Documentation**: Auto-generated documentation
- **Modularity**: Reusable models and macros

## 🏗️ Core Architecture Concepts

### 1. DBT Workflow Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    DBT Transformation Workflow             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Raw Data  │───▶│ DBT Models  │───▶│ Transformed │     │
│  │             │    │             │    │    Data     │     │
│  │ • CSV Files │    │ • Staging   │    │ • Marts     │     │
│  │ • APIs      │    │ • Intermediate │ │ • Reports   │     │
│  │ • Databases │    │ • Marts     │    │ • Analytics │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                             │                              │
│                             ▼                              │
│  ┌─────────────────────────────────────────────────────────┤
│  │                DBT Core Components                     │
│  │                                                        │
│  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │ │   Models    │ │    Tests    │ │    Macros   │       │
│  │ │ SQL files   │ │ Data quality│ │ Reusable    │       │
│  │ │ .sql        │ │ validations │ │ SQL code    │       │
│  │ └─────────────┘ └─────────────┘ └─────────────┘       │
│  │                                                        │
│  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │ │ Snapshots   │ │    Seeds    │ │    Docs     │       │
│  │ │ Historical  │ │ Reference   │ │ Auto-gen    │       │
│  │ │ data        │ │ data        │ │ documentation│       │
│  │ └─────────────┘ └─────────────┘ └─────────────┘       │
│  └─────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

### Component Explanations:

**Models**: 
- SQL files that define data transformations
- Each model creates a table or view in your warehouse
- Organized in layers: staging, intermediate, marts

**Tests**: 
- Data quality checks written in SQL
- Built-in tests: unique, not_null, accepted_values, relationships
- Custom tests for business logic validation

**Macros**: 
- Reusable SQL code snippets
- Similar to functions in programming languages
- Enable DRY (Don't Repeat Yourself) principles

**Snapshots**: 
- Capture historical changes in slowly changing dimensions
- Track how data changes over time
- Useful for auditing and historical analysis

**Seeds**: 
- CSV files with reference data
- Version-controlled lookup tables
- Small datasets that rarely change

## 📊 DBT Project Structure

### 1. Typical DBT Project Layout
```
my_dbt_project/
├── dbt_project.yml          # Project configuration
├── profiles.yml             # Database connection settings
├── models/                  # SQL transformation files
│   ├── staging/            # Raw data cleaning
│   │   ├── _sources.yml    # Source definitions
│   │   ├── stg_customers.sql
│   │   └── stg_orders.sql
│   ├── intermediate/       # Business logic
│   │   ├── int_customer_orders.sql
│   │   └── int_order_metrics.sql
│   └── marts/             # Final business-ready tables
│       ├── dim_customers.sql
│       ├── fact_orders.sql
│       └── _schema.yml    # Model documentation and tests
├── macros/                 # Reusable SQL functions
│   ├── get_payment_methods.sql
│   └── cents_to_dollars.sql
├── tests/                  # Custom data tests
│   └── assert_positive_order_amounts.sql
├── snapshots/             # Historical data capture
│   └── customers_snapshot.sql
└── seeds/                 # Reference data CSV files
    └── payment_methods.csv
```

### 2. Model Layering Strategy

**Staging Layer** (Raw data cleaning):
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
from {{ source('raw_data', 'customers') }}
where customer_id is not null
```

**Intermediate Layer** (Business logic):
```sql
-- models/intermediate/int_customer_orders.sql
{{ config(materialized='table') }}

select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    count(o.order_id) as total_orders,
    sum(o.order_amount) as total_spent,
    avg(o.order_amount) as avg_order_value,
    min(o.order_date) as first_order_date,
    max(o.order_date) as last_order_date
from {{ ref('stg_customers') }} c
left join {{ ref('stg_orders') }} o
    on c.customer_id = o.customer_id
group by 1, 2, 3, 4
```

**Marts Layer** (Business-ready tables):
```sql
-- models/marts/dim_customers.sql
{{ config(materialized='table') }}

select
    customer_id,
    first_name,
    last_name,
    email,
    total_orders,
    total_spent,
    avg_order_value,
    case
        when total_spent >= 1000 then 'High Value'
        when total_spent >= 500 then 'Medium Value'
        else 'Low Value'
    end as customer_segment,
    first_order_date,
    last_order_date,
    current_timestamp as updated_at
from {{ ref('int_customer_orders') }}
```

## 🔧 DBT Core Features

### 1. Jinja Templating

**Dynamic SQL Generation**:
```sql
-- Using variables
select *
from orders
where order_date >= '{{ var("start_date") }}'

-- Using loops
select
    order_id,
    {% for payment_method in ['credit_card', 'paypal', 'bank_transfer'] %}
    sum(case when payment_method = '{{ payment_method }}' then amount else 0 end) as {{ payment_method }}_amount
    {%- if not loop.last -%},{%- endif -%}
    {% endfor %}
from payments
group by order_id
```

**Macros for Reusability**:
```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    round({{ column_name }} / 100.0, {{ precision }})
{% endmacro %}

-- Usage in models
select
    order_id,
    {{ cents_to_dollars('amount_cents') }} as amount_dollars
from orders
```

### 2. Testing Framework

**Built-in Tests**:
```yaml
# models/_schema.yml
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
              values: ['High Value', 'Medium Value', 'Low Value']
```

**Custom Tests**:
```sql
-- tests/assert_positive_order_amounts.sql
select *
from {{ ref('fact_orders') }}
where order_amount <= 0
```

### 3. Documentation Generation

**Model Documentation**:
```yaml
# models/_schema.yml
version: 2

models:
  - name: fact_orders
    description: "Order fact table with customer and product details"
    columns:
      - name: order_id
        description: "Unique order identifier"
      - name: customer_id
        description: "Foreign key to customer dimension"
      - name: order_amount
        description: "Total order amount in dollars"
        meta:
          business_definition: "Includes tax and shipping, excludes discounts"
```

## 🚀 DBT Execution and Deployment

### 1. Development Workflow

**Local Development**:
```bash
# Install DBT
pip install dbt-core dbt-postgres  # or dbt-snowflake, dbt-bigquery, etc.

# Initialize new project
dbt init my_project

# Test database connection
dbt debug

# Run models
dbt run

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

**Model Selection**:
```bash
# Run specific model
dbt run --select dim_customers

# Run model and downstream dependencies
dbt run --select dim_customers+

# Run model and upstream dependencies
dbt run --select +dim_customers

# Run models by tag
dbt run --select tag:daily

# Run modified models only
dbt run --select state:modified
```

### 2. Production Deployment

**CI/CD Pipeline Example**:
```yaml
# .github/workflows/dbt.yml
name: DBT CI/CD
on:
  push:
    branches: [main]
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
      
      - name: Install DBT
        run: |
          pip install dbt-core dbt-snowflake
      
      - name: Run DBT tests
        run: |
          dbt deps
          dbt seed
          dbt run
          dbt test
        env:
          DBT_PROFILES_DIR: .
          DBT_SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          DBT_SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          DBT_SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Production
        run: |
          dbt run --target prod
          dbt test --target prod
```

## 🎯 When to Use DBT

### ✅ Ideal Use Cases:

**1. Analytics Engineering**:
- Transform raw data into analytics-ready datasets
- Build dimensional models for BI tools
- Create metrics and KPIs for business users

**2. Data Quality Management**:
- Implement data quality tests
- Monitor data freshness and completeness
- Validate business rules and constraints

**3. Collaborative Data Development**:
- Version control for data transformations
- Code review process for data changes
- Documentation for data lineage

**4. ELT Workflows**:
- Modern data stack with cloud warehouses
- Transform data after loading (ELT vs ETL)
- Leverage warehouse compute power

### ❌ Not Ideal For:

**1. Real-time Processing**: Use streaming tools instead
**2. Complex ETL Logic**: Consider dedicated ETL tools
**3. Non-SQL Transformations**: Limited to SQL-based transformations
**4. Small Data Sets**: May be overkill for simple transformations

## 🎯 Real-World Analogy

Think of DBT like a **modern software development environment for data**:

**DBT Project** = **Software Application**:
- Models are like functions/classes
- Tests are like unit tests
- Documentation is like code comments
- Macros are like libraries/modules

**Development Workflow** = **Software Engineering Practices**:
- **Git**: Version control for data transformations
- **Code Review**: Peer review of data logic
- **CI/CD**: Automated testing and deployment
- **Documentation**: Auto-generated data lineage

**Data Lineage** = **Dependency Graph**:
- Models depend on other models (like function calls)
- Changes propagate through dependencies
- Clear understanding of data flow
- Impact analysis for changes

## 📊 Performance and Best Practices

### Materialization Strategies:
- **View**: Fast to build, slow to query
- **Table**: Slow to build, fast to query
- **Incremental**: Only process new/changed data
- **Ephemeral**: Compile as CTE, no persistence

### Optimization Techniques:
- Use incremental models for large datasets
- Implement proper indexing strategies
- Leverage warehouse-specific optimizations
- Monitor query performance and costs

### Development Best Practices:
- Follow consistent naming conventions
- Implement comprehensive testing
- Document business logic clearly
- Use version control effectively
- Monitor data quality continuously

This conceptual understanding helps you implement modern analytics engineering practices using DBT, enabling scalable and maintainable data transformation workflows.