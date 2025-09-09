
### Q1: What is Looker and how does it differ from traditional BI tools?
**Answer:**
Looker is a modern business intelligence platform that uses a unique modeling layer approach.

**Key Differentiators:**
- **Single Source of Truth**: Centralized data definitions
- **LookML**: Code-based modeling language
- **In-Database Architecture**: Queries run directly in your database
- **Git Integration**: Version control for data models
- **API-First**: Programmatic access to all features
- **Embedded Analytics**: Native embedding capabilities

**vs Traditional BI:**
- No data extraction/transformation required
- Real-time data access
- Consistent metrics across organization
- Developer-friendly approach

### Q2: Explain Looker's architecture and key components.
**Answer:**
**Core Components:**
- **Looker Application**: Web-based interface
- **LookML**: Modeling layer and language
- **Database**: Your existing data warehouse
- **Git Repository**: Version control for models
- **API**: Programmatic access

**Architecture Flow:**
1. **LookML Models** define data relationships
2. **Explores** create user-friendly interfaces
3. **Looks** are saved queries and visualizations
4. **Dashboards** combine multiple Looks
5. **Queries** execute directly in database

### Q3: What is LookML and why is it important?
**Answer:**
LookML (Looker Modeling Language) is Looker's proprietary language for describing data relationships and business logic.

**Key Features:**
- **Declarative**: Describes what data means, not how to get it
- **Reusable**: Define once, use everywhere
- **Version Controlled**: Git-based development workflow
- **Maintainable**: Centralized business logic
- **Scalable**: Handles complex data relationships

**Benefits:**
- Consistent metrics across organization
- Reduced development time
- Easy maintenance and updates
- Collaborative development

---

## LookML Fundamentals

### Q4: What are the basic LookML objects and their purposes?
**Answer:**
**Core LookML Objects:**

1. **Connection**: Database connection configuration
```lookml
connection: "my_database" {
  url: "jdbc:postgresql://localhost:5432/mydb"
  username: "looker_user"
  password: "password"
}
```

2. **View**: Represents a table or query
```lookml
view: orders {
  sql_table_name: public.orders ;;
  
  dimension: order_id {
    type: number
    sql: ${TABLE}.order_id ;;
  }
}
```

3. **Explore**: Defines how users can explore data
```lookml
explore: orders {
  join: customers {
    sql_on: ${orders.customer_id} = ${customers.customer_id} ;;
  }
}
```

4. **Model**: Contains explores and connections
```lookml
connection: "my_db"
include: "*.view"

explore: orders {}
```

### Q5: How do you define dimensions in LookML?
**Answer:**
**Dimension Types:**
```lookml
view: orders {
  # String dimension
  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
  }
  
  # Number dimension
  dimension: amount {
    type: number
    sql: ${TABLE}.amount ;;
    value_format_name: usd
  }
  
  # Date dimension
  dimension_group: created {
    type: time
    timeframes: [date, week, month, year]
    sql: ${TABLE}.created_at ;;
  }
  
  # Yesno dimension
  dimension: is_returned {
    type: yesno
    sql: ${TABLE}.returned_at IS NOT NULL ;;
  }
  
  # Tier dimension
  dimension: amount_tier {
    type: tier
    tiers: [0, 100, 500, 1000]
    sql: ${amount} ;;
  }
}
```

### Q6: How do you create measures in LookML?
**Answer:**
**Common Measure Types:**
```lookml
view: orders {
  # Count measure
  measure: count {
    type: count
    drill_fields: [order_id, customer_name, created_date]
  }
  
  # Sum measure
  measure: total_revenue {
    type: sum
    sql: ${amount} ;;
    value_format_name: usd
  }
  
  # Average measure
  measure: average_order_value {
    type: average
    sql: ${amount} ;;
    value_format_name: usd
  }
  
  # Count distinct
  measure: customer_count {
    type: count_distinct
    sql: ${customer_id} ;;
  }
  
  # Custom measure
  measure: conversion_rate {
    type: number
    sql: ${orders_count} / ${visitors_count} ;;
    value_format_name: percent_2
  }
}
```

---

## Data Modeling

### Q7: How do you create joins in LookML?
**Answer:**
**Join Types and Syntax:**
```lookml
explore: orders {
  # Inner join (default)
  join: customers {
    sql_on: ${orders.customer_id} = ${customers.customer_id} ;;
  }
  
  # Left join
  join: order_items {
    type: left_outer
    sql_on: ${orders.order_id} = ${order_items.order_id} ;;
    relationship: one_to_many
  }
  
  # Many-to-one join
  join: products {
    sql_on: ${order_items.product_id} = ${products.product_id} ;;
    relationship: many_to_one
  }
  
  # Join with conditions
  join: promotions {
    sql_on: ${orders.promotion_id} = ${promotions.promotion_id} 
            AND ${orders.created_date} >= ${promotions.start_date}
            AND ${orders.created_date} <= ${promotions.end_date} ;;
  }
}
```

### Q8: What are the different relationship types in Looker?
**Answer:**
**Relationship Types:**
- **one_to_one**: Each record matches exactly one record
- **one_to_many**: One record can match multiple records
- **many_to_one**: Multiple records match one record
- **many_to_many**: Multiple records match multiple records

**Impact on Queries:**
- Affects how measures are calculated
- Determines fanout behavior
- Influences performance optimization

### Q9: How do you handle slowly changing dimensions in Looker?
**Answer:**
**Approaches:**
1. **Type 1 SCD**: Overwrite historical data
2. **Type 2 SCD**: Keep historical records with effective dates

**LookML Implementation:**
```lookml
view: customers_scd {
  dimension: customer_id {
    type: number
    sql: ${TABLE}.customer_id ;;
  }
  
  dimension_group: effective {
    type: time
    timeframes: [date]
    sql: ${TABLE}.effective_date ;;
  }
  
  dimension_group: expiration {
    type: time
    timeframes: [date]
    sql: ${TABLE}.expiration_date ;;
  }
  
  dimension: is_current {
    type: yesno
    sql: ${TABLE}.is_current = 'Y' ;;
  }
}

explore: orders {
  join: customers_scd {
    sql_on: ${orders.customer_id} = ${customers_scd.customer_id}
            AND ${orders.created_date} >= ${customers_scd.effective_date}
            AND ${orders.created_date} < ${customers_scd.expiration_date} ;;
  }
}
```

---

## Explores & Dimensions

### Q10: How do you create conditional logic in LookML?
**Answer:**
**Using CASE Statements:**
```lookml
dimension: customer_segment {
  type: string
  sql: CASE 
        WHEN ${lifetime_value} >= 1000 THEN 'Premium'
        WHEN ${lifetime_value} >= 500 THEN 'Standard'
        ELSE 'Basic'
       END ;;
}

# Using liquid templating
dimension: dynamic_timeframe {
  type: string
  sql: {% if orders.created_date._in_query %}
         ${orders.created_date}
       {% else %}
         'All Time'
       {% endif %} ;;
}
```

### Q11: How do you implement filters and parameters in LookML?
**Answer:**
**Filter Implementation:**
```lookml
# Basic filter
filter: date_filter {
  type: date
  default_value: "7 days"
}

# Parameter for dynamic grouping
parameter: grouping_selector {
  type: unquoted
  allowed_value: {
    label: "By Month"
    value: "month"
  }
  allowed_value: {
    label: "By Quarter"
    value: "quarter"
  }
}

# Dynamic dimension using parameter
dimension: dynamic_date_group {
  type: string
  sql: {% parameter grouping_selector %} ;;
}
```

### Q12: How do you create derived tables in LookML?
**Answer:**
**SQL-based Derived Table:**
```lookml
view: customer_summary {
  derived_table: {
    sql: SELECT 
           customer_id,
           COUNT(*) as order_count,
           SUM(amount) as total_spent,
           MAX(created_at) as last_order_date
         FROM orders 
         GROUP BY customer_id ;;
  }
  
  dimension: customer_id {
    type: number
    sql: ${TABLE}.customer_id ;;
  }
  
  measure: total_customers {
    type: count
  }
}
```

**Native Derived Table (NDT):**
```lookml
view: customer_facts {
  derived_table: {
    explore_source: orders {
      column: customer_id {}
      column: order_count { field: orders.count }
      column: total_revenue { field: orders.total_amount }
    }
  }
}
```

---

## Measures & Calculations

### Q13: How do you create complex calculations and window functions?
**Answer:**
**Window Functions:**
```lookml
measure: running_total {
  type: running_total
  sql: ${total_revenue} ;;
}

dimension: rank_by_revenue {
  type: number
  sql: RANK() OVER (ORDER BY ${total_revenue} DESC) ;;
}

measure: percent_of_total {
  type: percent_of_total
  sql: ${total_revenue} ;;
}
```

**Custom Calculations:**
```lookml
measure: growth_rate {
  type: number
  sql: (${current_period_revenue} - ${previous_period_revenue}) 
       / ${previous_period_revenue} ;;
  value_format_name: percent_2
}
```

### Q14: How do you handle date calculations and periods?
**Answer:**
**Date Comparisons:**
```lookml
measure: revenue_last_month {
  type: sum
  sql: ${amount} ;;
  filters: [created_date: "1 month ago for 1 month"]
}

measure: revenue_growth {
  type: number
  sql: ${revenue_this_month} - ${revenue_last_month} ;;
}

# Using liquid for dynamic periods
measure: revenue_period_over_period {
  type: sum
  sql: ${amount} ;;
  filters: [
    created_date: "{% parameter date_range %}"
  ]
}
```

### Q15: How do you implement cohort analysis in Looker?
**Answer:**
**Cohort Analysis Setup:**
```lookml
view: customer_cohorts {
  derived_table: {
    sql: SELECT 
           customer_id,
           DATE_TRUNC('month', MIN(created_at)) as cohort_month,
           created_at as order_date
         FROM orders 
         GROUP BY customer_id, created_at ;;
  }
  
  dimension: cohort_month {
    type: date
    sql: ${TABLE}.cohort_month ;;
  }
  
  dimension: periods_since_cohort {
    type: number
    sql: DATEDIFF('month', ${cohort_month}, ${order_date}) ;;
  }
  
  measure: retention_rate {
    type: number
    sql: COUNT(DISTINCT ${customer_id}) / 
         COUNT(DISTINCT CASE WHEN ${periods_since_cohort} = 0 
                            THEN ${customer_id} END) ;;
    value_format_name: percent_2
  }
}
```

---

## Dashboards & Visualizations

### Q16: How do you create and customize dashboards in Looker?
**Answer:**
**Dashboard Creation:**
1. **Create Dashboard**: New → Dashboard
2. **Add Elements**: Looks, text, filters
3. **Configure Layout**: Arrange and resize
4. **Add Filters**: Dashboard-level filtering
5. **Set Refresh**: Auto-refresh settings

**LookML Dashboard:**
```lookml
dashboard: sales_overview {
  title: "Sales Overview Dashboard"
  
  filters: [
    {
      name: "Date Range"
      type: field_filter
      explore: orders
      field: orders.created_date
      default_value: "30 days"
    }
  ]
  
  elements: [
    {
      name: "Total Revenue"
      type: single_value
      query: {
        model: sales
        explore: orders
        measures: [orders.total_revenue]
        filters: {
          orders.created_date: "30 days"
        }
      }
    }
  ]
}
```

### Q17: What visualization types are available in Looker?
**Answer:**
**Chart Types:**
- **Table**: Detailed data view
- **Column/Bar**: Categorical comparisons
- **Line**: Trends over time
- **Pie/Donut**: Part-to-whole relationships
- **Scatter**: Correlation analysis
- **Map**: Geographic data
- **Single Value**: KPI display
- **Funnel**: Conversion analysis
- **Waterfall**: Sequential changes

**Custom Visualizations:**
- Marketplace visualizations
- Custom D3.js visualizations
- Third-party integrations

---

## Administration & Security

### Q18: How do you manage user access and permissions in Looker?
**Answer:**
**Permission Levels:**
- **Admin**: Full system access
- **Developer**: Can create and edit LookML
- **User**: Can create Looks and dashboards
- **Viewer**: Read-only access

**Model-level Permissions:**
```lookml
# In model file
access_grant: sales_team {
  allowed_values: ["sales", "manager"]
  user_attribute: department
}

explore: orders {
  required_access_grants: [sales_team]
}
```

**Row-level Security:**
```lookml
dimension: customer_id {
  type: number
  sql: ${TABLE}.customer_id ;;
  # Only show data for user's customers
  sql: {% if _user_attributes['customer_ids'] %}
         CASE WHEN ${TABLE}.customer_id IN ({{ _user_attributes['customer_ids'] }})
              THEN ${TABLE}.customer_id
              ELSE NULL
         END
       {% else %}
         ${TABLE}.customer_id
       {% endif %} ;;
}
```

### Q19: How do you implement data governance in Looker?
**Answer:**
**Governance Features:**
- **Content Validation**: Automated testing
- **Usage Analytics**: Track dashboard and Look usage
- **Data Dictionary**: Document fields and measures
- **Approval Workflows**: Review process for changes
- **Audit Logs**: Track user activities

**Implementation:**
```lookml
# Data tests
test: orders_have_positive_amounts {
  explore_source: orders {
    column: count {}
    filters: [orders.amount: "<0"]
  }
  assert: count = 0
}
```

---

## Performance & Optimization

### Q20: How do you optimize Looker performance?
**Answer:**
**Database Optimization:**
- Create appropriate indexes
- Use aggregate tables
- Optimize SQL queries
- Implement partitioning

**LookML Optimization:**
```lookml
# Use aggregate awareness
view: orders_summary {
  sql_table_name: orders_daily_summary ;;
  
  dimension: date {
    type: date
    sql: ${TABLE}.date ;;
  }
  
  measure: total_revenue {
    type: sum
    sql: ${TABLE}.daily_revenue ;;
  }
}

# Persistent derived tables
view: customer_facts {
  derived_table: {
    sql: SELECT customer_id, SUM(amount) as lifetime_value
         FROM orders GROUP BY customer_id ;;
    
    # Performance optimizations
    persist_for: "1 hour"
    indexes: ["customer_id"]
    sortkeys: ["customer_id"]
  }
}
```

### Q21: What is caching in Looker and how does it work?
**Answer:**
**Caching Layers:**
1. **Query Cache**: Stores query results
2. **Connection Cache**: Database connection pooling
3. **Metadata Cache**: Schema information

**Cache Configuration:**
- **Datagroup**: Define cache invalidation rules
- **Persist_for**: Set cache duration
- **Max_cache_age**: Override default caching

```lookml
datagroup: orders_datagroup {
  sql_trigger: SELECT MAX(updated_at) FROM orders ;;
  max_cache_age: "1 hour"
}

explore: orders {
  persist_with: orders_datagroup
}
```

---

## Advanced Features

### Q22: How do you implement embedded analytics with Looker?
**Answer:**
**Embedding Options:**
1. **Public Embedding**: No authentication
2. **Private Embedding**: SSO integration
3. **Signed Embedding**: JWT-based security

**Implementation:**
```javascript
// Signed embedding
const embed_url = `https://company.looker.com/embed/dashboards/123?embed_domain=${domain}&external_user_id=${user_id}`;

// Using Looker SDK
const sdk = new LookerSDK({
  base_url: 'https://company.looker.com:19999',
  client_id: 'your_client_id',
  client_secret: 'your_client_secret'
});

const dashboard = await sdk.create_sso_embed_url({
  target_url: '/dashboards/123',
  session_length: 3600,
  external_user_id: 'user123'
});
```

### Q23: How do you use Looker's API for automation?
**Answer:**
**Common API Use Cases:**
- Automated report delivery
- User management
- Content deployment
- Data extraction

**API Examples:**
```python
import looker_sdk

# Initialize SDK
sdk = looker_sdk.init40()

# Run a query
query = {
    'model': 'sales',
    'explore': 'orders',
    'fields': ['orders.created_date', 'orders.total_revenue'],
    'filters': {'orders.created_date': '30 days'}
}

result = sdk.run_inline_query('json', query)

# Schedule dashboard delivery
schedule = {
    'name': 'Weekly Sales Report',
    'dashboard_id': 123,
    'scheduled_plan_destination': [{
        'type': 'email',
        'address': 'team@company.com'
    }],
    'crontab': '0 9 * * 1'  # Every Monday at 9 AM
}

sdk.create_scheduled_plan(schedule)
```

---

## Troubleshooting

### Q24: How do you debug LookML errors?
**Answer:**
**Common Error Types:**
1. **Syntax Errors**: Missing semicolons, brackets
2. **Reference Errors**: Invalid field references
3. **SQL Errors**: Database-specific issues
4. **Join Errors**: Incorrect relationships

**Debugging Tools:**
- **LookML Validator**: Built-in syntax checking
- **SQL Runner**: Test queries directly
- **Content Validator**: Automated testing
- **Query Inspector**: Examine generated SQL

**Best Practices:**
- Use version control for rollback capability
- Test changes in development environment
- Validate SQL in database before implementing
- Use descriptive error messages

### Q25: How do you handle performance issues in Looker?
**Answer:**
**Diagnosis Steps:**
1. **Query Inspector**: Examine SQL and execution time
2. **System Activity**: Monitor concurrent users
3. **Database Performance**: Check database metrics
4. **Cache Hit Rates**: Analyze caching effectiveness

**Solutions:**
- Optimize database queries and indexes
- Implement aggregate tables
- Use persistent derived tables
- Configure appropriate caching
- Limit result sets with filters

---

## Best Practices

### Q26: What are LookML development best practices?
**Answer:**
**Code Organization:**
- Use consistent naming conventions
- Organize files logically
- Document complex logic
- Use version control effectively

**Performance:**
- Minimize joins in explores
- Use appropriate data types
- Implement caching strategies
- Create efficient derived tables

**Maintainability:**
- Use refinements for customization
- Create reusable view templates
- Implement proper testing
- Document business logic

### Q27: How do you ensure data quality in Looker?
**Answer:**
**Data Quality Measures:**
- **Content Validation**: Automated testing
- **Data Tests**: Assert expected values
- **Documentation**: Clear field descriptions
- **Monitoring**: Track data freshness
- **Governance**: Review processes

**Implementation:**
```lookml
# Data quality tests
test: revenue_is_positive {
  explore_source: orders {
    column: count {}
    filters: [orders.total_revenue: "<0"]
  }
  assert: count = 0
}

test: no_future_dates {
  explore_source: orders {
    column: count {}
    filters: [orders.created_date: "after today"]
  }
  assert: count = 0
}
```

---

## Scenario-Based Questions

### Q28: How would you migrate from another BI tool to Looker?
**Answer:**
**Migration Strategy:**
1. **Assessment**: Inventory existing reports and data models
2. **Data Modeling**: Recreate business logic in LookML
3. **User Training**: Educate team on Looker concepts
4. **Gradual Rollout**: Phase migration by department
5. **Validation**: Ensure data accuracy and completeness

**Technical Steps:**
- Map existing metrics to LookML
- Recreate dashboards and reports
- Set up user access and permissions
- Implement data governance
- Establish development workflows

### Q29: How would you design a multi-tenant Looker implementation?
**Answer:**
**Architecture Approaches:**
1. **Separate Instances**: Dedicated Looker per tenant
2. **Shared Instance**: Single Looker with row-level security
3. **Hybrid**: Combination based on requirements

**Implementation:**
```lookml
# Row-level security for multi-tenancy
dimension: tenant_id {
  type: string
  sql: ${TABLE}.tenant_id ;;
  # Hide from users
  hidden: yes
}

# Apply tenant filter automatically
explore: orders {
  sql_always_where: ${tenant_id} = '{{ _user_attributes['tenant_id'] }}' ;;
}
```

### Q30: How would you implement real-time analytics in Looker?
**Answer:**
**Real-time Strategies:**
1. **Streaming Data**: Use real-time data pipelines
2. **Frequent Refresh**: Short cache durations
3. **Push Notifications**: Alerts for critical changes
4. **Live Dashboards**: Auto-refresh capabilities

**Implementation:**
```lookml
# Real-time datagroup
datagroup: realtime_orders {
  sql_trigger: SELECT CURRENT_TIMESTAMP ;;
  max_cache_age: "5 minutes"
}

# Live dashboard with alerts
dashboard: operations_center {
  refresh: 30  # seconds
  
  elements: [
    {
      name: "Live Orders"
      type: single_value
      query: {
        model: sales
        explore: orders
        measures: [orders.count]
        filters: {
          orders.created_date: "today"
        }
      }
    }
  ]
}
```

---

## 🎯 Key Takeaways

- **LookML Mastery**: Understanding LookML is crucial for Looker success
- **Data Modeling**: Proper modeling ensures scalable and maintainable analytics
- **Performance**: Database optimization and caching are critical
- **Security**: Implement proper access controls and row-level security
- **Best Practices**: Follow development standards and testing procedures
- **API Integration**: Leverage APIs for automation and embedding
- **Governance**: Establish processes for data quality and content management

Remember: Looker's strength lies in its modeling layer approach, which creates a single source of truth for business metrics while enabling self-service analytics.