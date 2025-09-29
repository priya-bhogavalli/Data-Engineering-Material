# 📊 Omni - Interview Questions & Answers

**Difficulty Levels**: 🟢 Beginner | 🟡 Intermediate | 🔴 Advanced | 🟣 Expert

---

## 🟢 Beginner Level Questions

### Q1: What is Omni and how does it position itself in the modern BI landscape?
**Answer**: Omni is a modern business intelligence platform that combines SQL-first data modeling with intuitive self-service analytics, designed to bridge the gap between technical data teams and business users.

**Key Positioning**:
- **SQL-First Approach**: Business logic defined in transparent SQL code
- **Modern Data Stack Native**: Built for cloud data warehouses and modern tools
- **Real-Time Collaboration**: Live editing and sharing capabilities
- **Semantic Layer**: Centralized metrics and governance
- **Developer + Business User Friendly**: Technical flexibility with user-friendly interfaces

**Comparison with Traditional BI**:
```sql
-- Traditional BI: Hidden business logic in proprietary formats
-- Omni: Transparent SQL-based modeling

-- Example: Customer segmentation in Omni
model customer_segments {
  sql_table_name: "analytics.customers"
  
  dimension customer_id {
    type: string
    primary_key: yes
    sql: ${TABLE}.customer_id
  }
  
  dimension customer_tier {
    type: string
    sql: CASE 
           WHEN ${total_revenue} >= 10000 THEN 'VIP'
           WHEN ${total_revenue} >= 5000 THEN 'Premium'
           WHEN ${total_revenue} >= 1000 THEN 'Standard'
           ELSE 'Basic'
         END
    description: "Customer value tier based on total revenue"
  }
  
  measure total_customers {
    type: count_distinct
    sql: ${customer_id}
    description: "Total number of unique customers"
  }
  
  measure average_revenue {
    type: average
    sql: ${TABLE}.total_revenue
    value_format: "$#,##0.00"
    description: "Average revenue per customer"
  }
}
```

**Benefits over Traditional BI**:
- **Transparency**: All business logic visible and auditable
- **Flexibility**: Easy to modify and extend models
- **Performance**: Leverages data warehouse compute power
- **Collaboration**: Real-time editing and sharing
- **Modern Integration**: Works seamlessly with cloud data stack

### Q2: Explain Omni's workbook concept and how it enables self-service analytics.
**Answer**: Omni's workbooks provide an interactive interface where business users can explore data, create visualizations, and build dashboards without writing SQL, while still leveraging the power of the underlying SQL models.

**Workbook Components**:
```yaml
# Example: Sales analysis workbook
workbook: "Sales Performance Analysis"
description: "Interactive sales metrics and trend analysis"

# Data exploration interface
explore: sales_metrics {
  # Available dimensions for grouping
  dimensions: [
    "order_date",
    "product_category", 
    "customer_segment",
    "sales_region",
    "sales_rep"
  ]
  
  # Available measures for analysis
  measures: [
    "total_revenue",
    "order_count",
    "average_order_value",
    "unique_customers",
    "conversion_rate"
  ]
  
  # Interactive filters
  filters: {
    date_range: {
      type: "date_filter"
      field: "order_date"
      default: "last_90_days"
      quick_options: ["today", "last_7_days", "last_30_days", "last_quarter"]
    }
    
    product_filter: {
      type: "multi_select"
      field: "product_category"
      default: "all"
      search_enabled: true
    }
    
    revenue_threshold: {
      type: "range_filter"
      field: "total_revenue"
      min: 0
      max: 1000000
    }
  }
}

# Dashboard configuration
dashboard: "Sales Executive Summary" {
  layout: "responsive_grid"
  auto_refresh: "5_minutes"
  
  tiles: [
    {
      name: "Total Revenue"
      type: "big_number"
      query: {
        measure: "total_revenue"
        filters: {
          order_date: "{{ date_range }}"
        }
      }
      comparison: {
        type: "previous_period"
        show_percentage: true
      }
    },
    
    {
      name: "Revenue Trend"
      type: "line_chart"
      query: {
        dimensions: ["order_date"]
        measures: ["total_revenue", "order_count"]
        filters: {
          order_date: "last_12_months"
        }
      }
      settings: {
        show_trend_line: true
        enable_zoom: true
      }
    },
    
    {
      name: "Top Products"
      type: "horizontal_bar"
      query: {
        dimensions: ["product_category"]
        measures: ["total_revenue"]
        sort: "total_revenue desc"
        limit: 10
      }
    }
  ]
}
```

**Self-Service Capabilities**:
- **Drag-and-Drop Interface**: Users can easily add dimensions and measures
- **Interactive Filtering**: Real-time filtering without technical knowledge
- **Visual Query Builder**: Point-and-click query construction
- **Automatic Visualizations**: Smart chart type suggestions
- **Export Options**: PDF, Excel, PNG exports available

### Q3: How does Omni handle data modeling and what are the key components of an Omni model?
**Answer**: Omni uses SQL-based data modeling where business logic is defined in structured model files that specify dimensions, measures, and relationships.

**Model Structure Components**:
```sql
-- Example: Comprehensive Omni model
-- File: models/ecommerce_analytics.sql

model ecommerce_orders {
  sql_table_name: "warehouse.fact_orders"
  description: "E-commerce order analytics with customer and product details"
  
  # ===== DIMENSIONS =====
  # Primary key dimension
  dimension order_id {
    type: string
    primary_key: yes
    sql: ${TABLE}.order_id
    description: "Unique order identifier"
  }
  
  # Date dimensions with hierarchy
  dimension_group order_date {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.order_date
    description: "When the order was placed"
  }
  
  # Categorical dimensions
  dimension customer_segment {
    type: string
    sql: ${TABLE}.customer_segment
    description: "Customer value segment"
    drill_fields: [customer_id, customer_name]
  }
  
  dimension product_category {
    type: string
    sql: ${TABLE}.product_category
    description: "Product category classification"
    suggest_explore: product_catalog
    suggest_dimension: category_name
  }
  
  dimension sales_channel {
    type: string
    sql: ${TABLE}.sales_channel
    description: "Channel through which order was placed"
    allowed_values: {
      list: ["online", "mobile_app", "retail_store", "phone"]
    }
  }
  
  # Geographic dimensions
  dimension shipping_region {
    type: string
    sql: ${TABLE}.shipping_region
    description: "Geographic region for shipping"
    map_layer_name: us_states
  }
  
  # Calculated dimensions
  dimension order_size_category {
    type: string
    sql: CASE 
           WHEN ${order_value} >= 500 THEN 'Large'
           WHEN ${order_value} >= 100 THEN 'Medium'
           ELSE 'Small'
         END
    description: "Order size classification"
  }
  
  # ===== MEASURES =====
  # Count measures
  measure total_orders {
    type: count
    description: "Total number of orders"
    drill_fields: [order_id, customer_name, order_date, order_value]
  }
  
  measure unique_customers {
    type: count_distinct
    sql: ${TABLE}.customer_id
    description: "Number of unique customers"
  }
  
  # Sum measures
  measure total_revenue {
    type: sum
    sql: ${TABLE}.order_value
    value_format: "$#,##0.00"
    description: "Total revenue from all orders"
  }
  
  measure total_quantity {
    type: sum
    sql: ${TABLE}.quantity
    description: "Total quantity of items ordered"
  }
  
  # Average measures
  measure average_order_value {
    type: average
    sql: ${TABLE}.order_value
    value_format: "$#,##0.00"
    description: "Average value per order"
  }
  
  # Calculated measures
  measure revenue_per_customer {
    type: number
    sql: ${total_revenue} / NULLIF(${unique_customers}, 0)
    value_format: "$#,##0.00"
    description: "Average revenue per unique customer"
  }
  
  measure conversion_rate {
    type: number
    sql: ${total_orders} / NULLIF(${website_sessions}, 0) * 100
    value_format: "#0.00%"
    description: "Order conversion rate from website sessions"
  }
  
  # ===== FILTERS =====
  filter order_status {
    type: string
    sql: ${TABLE}.order_status = {% parameter order_status %}
    default_value: "completed"
    allowed_values: {
      list: ["pending", "processing", "shipped", "completed", "cancelled"]
    }
  }
  
  # ===== SETS =====
  set order_details {
    fields: [
      order_id,
      order_date_date,
      customer_segment,
      product_category,
      order_value,
      order_status
    ]
  }
  
  set customer_analysis {
    fields: [
      customer_segment,
      unique_customers,
      total_revenue,
      revenue_per_customer,
      average_order_value
    ]
  }
}
```

**Key Model Components**:
1. **Dimensions**: Attributes for grouping and filtering (categorical, date, numeric)
2. **Measures**: Aggregated metrics (count, sum, average, calculated)
3. **Filters**: Parameterized filtering options
4. **Sets**: Predefined field collections for common analyses
5. **Relationships**: Joins between models (defined separately)

---

## 🟡 Intermediate Level Questions

### Q4: How does Omni implement its semantic layer and ensure metric consistency across the organization?
**Answer**: Omni's semantic layer provides a centralized definition of business metrics, dimensions, and business rules that ensures consistency across all reports and dashboards.

**Semantic Layer Architecture**:
```sql
-- Example: Centralized semantic layer definitions
-- File: semantic/business_metrics.sql

# ===== CORE BUSINESS METRICS =====
metric monthly_recurring_revenue {
  type: sum
  sql: subscription_amount
  filters: [
    subscription_status = 'active',
    billing_frequency = 'monthly'
  ]
  description: "Total monthly recurring revenue from active subscriptions"
  owner: "finance_team@company.com"
  certification_level: "certified"
  last_validated: "2024-01-15"
}

metric customer_acquisition_cost {
  type: number
  sql: ${marketing_spend} / NULLIF(${new_customers_acquired}, 0)
  description: "Average cost to acquire a new customer"
  formula_explanation: "Total Marketing Spend ÷ New Customers Acquired"
  owner: "marketing_team@company.com"
  certification_level: "certified"
  dependencies: ["marketing_spend", "new_customers_acquired"]
}

metric net_revenue_retention {
  type: number
  sql: (
    ${beginning_period_revenue} + 
    ${expansion_revenue} - 
    ${contraction_revenue} - 
    ${churn_revenue}
  ) / NULLIF(${beginning_period_revenue}, 0) * 100
  description: "Net revenue retention rate for existing customer cohort"
  business_definition: "Measures revenue growth from existing customers"
  owner: "customer_success@company.com"
  certification_level: "certified"
}

# ===== DIMENSION HIERARCHIES =====
dimension_hierarchy customer_hierarchy {
  levels: [
    customer_id,
    customer_name,
    customer_segment,
    customer_tier,
    region,
    country
  ]
  description: "Standard customer classification hierarchy"
  drill_path: "customer_id -> customer_segment -> region -> country"
}

dimension_hierarchy time_hierarchy {
  type: temporal
  levels: [
    date,
    week,
    month,
    quarter,
    year
  ]
  fiscal_year_start: "april"
  description: "Standard time hierarchy with fiscal year starting in April"
}

dimension_hierarchy product_hierarchy {
  levels: [
    sku,
    product_name,
    product_line,
    category,
    division
  ]
  description: "Product classification hierarchy"
}

# ===== BUSINESS RULES AND VALIDATIONS =====
business_rule revenue_consistency {
  validation_sql: |
    SELECT 
      SUM(CASE WHEN order_revenue != line_item_total THEN 1 ELSE 0 END) as inconsistencies
    FROM fact_orders o
    JOIN (
      SELECT order_id, SUM(price * quantity) as line_item_total
      FROM fact_order_lines
      GROUP BY order_id
    ) l ON o.order_id = l.order_id
  expected_result: 0
  description: "Ensure order revenue equals sum of line items"
  severity: "error"
  owner: "data_quality_team@company.com"
}

business_rule metric_freshness {
  validation_sql: |
    SELECT COUNT(*) as stale_metrics
    FROM metric_refresh_log
    WHERE last_refresh < CURRENT_TIMESTAMP - INTERVAL '24 hours'
      AND metric_name IN ('monthly_recurring_revenue', 'customer_acquisition_cost')
  expected_result: 0
  description: "Ensure critical metrics are refreshed within 24 hours"
  severity: "warning"
  notification_channels: ["slack://data-alerts", "email://data-team@company.com"]
}

# ===== METRIC GOVERNANCE =====
governance_policy metric_certification {
  certification_levels: {
    "certified": {
      description: "Fully validated and approved for executive reporting"
      requirements: [
        "business_owner_approval",
        "data_quality_validation", 
        "cross_functional_review",
        "documentation_complete"
      ]
      review_frequency: "quarterly"
    }
    
    "provisional": {
      description: "Under development or testing"
      requirements: [
        "basic_validation",
        "preliminary_documentation"
      ]
      usage_restrictions: ["no_executive_reporting", "development_only"]
    }
    
    "deprecated": {
      description: "No longer recommended for use"
      sunset_date: "required"
      replacement_metric: "required"
    }
  }
}

# ===== ACCESS CONTROLS =====
access_policy sensitive_metrics {
  metrics: [
    "customer_acquisition_cost",
    "net_revenue_retention", 
    "gross_margin"
  ]
  
  access_rules: {
    "finance_team": "full_access"
    "executive_team": "full_access"
    "sales_team": "read_only"
    "marketing_team": "read_only"
    "general_users": "no_access"
  }
  
  data_masking: {
    "customer_acquisition_cost": {
      "sales_team": "rounded_to_nearest_100"
      "marketing_team": "show_trends_only"
    }
  }
}
```

**Governance Implementation**:
```python
# Example: Semantic layer governance engine
# File: governance/semantic_governance.py

class SemanticLayerGovernance:
    def __init__(self):
        self.omni_client = OmniClient()
        self.governance_config = self.load_governance_config()
        
    def validate_metric_definitions(self):
        """Validate all metric definitions against business rules"""
        
        validation_results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        
        metrics = self.omni_client.get_all_metrics()
        
        for metric in metrics:
            # Check certification requirements
            cert_result = self.validate_certification(metric)
            if not cert_result['valid']:
                validation_results['failed'].append({
                    'metric': metric['name'],
                    'issue': 'certification_incomplete',
                    'details': cert_result['missing_requirements']
                })
            
            # Check business rule compliance
            rule_result = self.validate_business_rules(metric)
            if not rule_result['valid']:
                validation_results['failed'].append({
                    'metric': metric['name'],
                    'issue': 'business_rule_violation',
                    'details': rule_result['violations']
                })
            
            # Check data freshness
            freshness_result = self.check_metric_freshness(metric)
            if not freshness_result['fresh']:
                validation_results['warnings'].append({
                    'metric': metric['name'],
                    'issue': 'stale_data',
                    'last_refresh': freshness_result['last_refresh']
                })
        
        return validation_results
    
    def enforce_access_controls(self, user_id, requested_metrics):
        """Enforce access controls for metric requests"""
        
        user_roles = self.get_user_roles(user_id)
        accessible_metrics = []
        
        for metric in requested_metrics:
            access_policy = self.get_metric_access_policy(metric)
            
            # Check if user has access
            has_access = any(
                role in access_policy['allowed_roles'] 
                for role in user_roles
            )
            
            if has_access:
                # Apply data masking if required
                masking_rules = access_policy.get('masking_rules', {})
                user_masking = None
                
                for role in user_roles:
                    if role in masking_rules:
                        user_masking = masking_rules[role]
                        break
                
                accessible_metrics.append({
                    'metric': metric,
                    'access_level': 'full' if not user_masking else 'masked',
                    'masking_rule': user_masking
                })
        
        return accessible_metrics
    
    def track_metric_lineage(self, metric_name):
        """Track complete lineage for a metric"""
        
        lineage = {
            'metric': metric_name,
            'dependencies': [],
            'downstream_usage': [],
            'data_sources': []
        }
        
        # Get metric definition
        metric_def = self.omni_client.get_metric_definition(metric_name)
        
        # Parse SQL to find dependencies
        dependencies = self.parse_metric_dependencies(metric_def['sql'])
        lineage['dependencies'] = dependencies
        
        # Find downstream usage
        usage = self.omni_client.find_metric_usage(metric_name)
        lineage['downstream_usage'] = [
            {
                'type': item['type'],  # dashboard, report, alert
                'name': item['name'],
                'owner': item['owner'],
                'last_accessed': item['last_accessed']
            }
            for item in usage
        ]
        
        # Trace to data sources
        sources = self.trace_to_data_sources(dependencies)
        lineage['data_sources'] = sources
        
        return lineage
```

**Key Semantic Layer Benefits**:
1. **Consistency**: Same metric calculated the same way everywhere
2. **Governance**: Centralized control over business definitions
3. **Discoverability**: Searchable catalog of certified metrics
4. **Lineage**: Complete traceability from source to consumption
5. **Access Control**: Role-based access to sensitive metrics
6. **Quality Assurance**: Automated validation and monitoring

### Q5: Describe Omni's approach to performance optimization and how it handles large-scale data processing.
**Answer**: Omni implements multiple layers of performance optimization including intelligent caching, query optimization, and materialization strategies to handle enterprise-scale data processing.

**Performance Architecture**:
```sql
-- Example: Performance optimization strategies
-- File: performance/optimization_framework.sql

# ===== MATERIALIZATION STRATEGIES =====
# Large fact tables - materialize as tables
model fact_orders_materialized {
  sql_table_name: "warehouse.fact_orders"
  materialization: "table"
  
  # Partitioning for performance
  partition_keys: ["order_date"]
  cluster_keys: ["customer_id", "product_id"]
  
  # Incremental refresh strategy
  incremental_strategy: "merge"
  unique_key: "order_id"
  
  dimension order_date {
    type: date
    sql: ${TABLE}.order_date
    # Enable partition pruning
    partition_date_field: yes
  }
  
  measure total_orders {
    type: count
    # Pre-aggregated for performance
    sql: ${TABLE}.order_count
  }
}

# Aggregated metrics - use incremental materialization
model daily_sales_summary {
  sql_table_name: "analytics.daily_sales_summary"
  materialization: "incremental_table"
  
  # Only process new/updated data
  incremental_filter: "date >= (SELECT MAX(date) FROM ${TABLE})"
  
  dimension date {
    type: date
    sql: ${TABLE}.date
    primary_key: yes
  }
  
  measure daily_revenue {
    type: sum
    sql: ${TABLE}.revenue
    # Pre-calculated for fast access
  }
}

# Real-time metrics - use views with caching
model real_time_metrics {
  sql_table_name: "warehouse.real_time_events"
  materialization: "view"
  
  # Aggressive caching for frequently accessed data
  cache_policy: {
    ttl: "5_minutes"
    refresh_trigger: "data_change"
    warm_cache: true
  }
  
  measure current_active_users {
    type: count_distinct
    sql: ${TABLE}.user_id
    filters: [
      "last_activity >= CURRENT_TIMESTAMP - INTERVAL '15 minutes'"
    ]
  }
}
```

```python
# Example: Intelligent query optimization
# File: performance/query_optimizer.py

class OmniQueryOptimizer:
    def __init__(self):
        self.omni_client = OmniClient()
        self.performance_monitor = PerformanceMonitor()
        
    def optimize_query_execution(self, query_request):
        """Optimize query execution with multiple strategies"""
        
        optimization_plan = {
            'original_query': query_request,
            'optimizations_applied': [],
            'estimated_performance_gain': 0
        }
        
        # 1. Check cache first
        cache_result = self.check_query_cache(query_request)
        if cache_result['hit']:
            return {
                'result': cache_result['data'],
                'execution_time': cache_result['retrieval_time'],
                'cache_hit': True
            }
        
        # 2. Analyze query complexity
        complexity = self.analyze_query_complexity(query_request)
        
        # 3. Apply appropriate optimizations
        if complexity['large_result_set']:
            query_request = self.apply_result_limiting(query_request)
            optimization_plan['optimizations_applied'].append('result_limiting')
        
        if complexity['expensive_joins']:
            query_request = self.optimize_join_order(query_request)
            optimization_plan['optimizations_applied'].append('join_optimization')
        
        if complexity['complex_aggregations']:
            query_request = self.use_pre_aggregated_tables(query_request)
            optimization_plan['optimizations_applied'].append('pre_aggregation')
        
        # 4. Choose optimal execution strategy
        if complexity['score'] > 8:  # Very complex query
            execution_strategy = 'async_with_progress'
        elif complexity['score'] > 5:  # Moderately complex
            execution_strategy = 'optimized_sync'
        else:  # Simple query
            execution_strategy = 'direct_execution'
        
        # 5. Execute with monitoring
        start_time = time.time()
        result = self.execute_optimized_query(query_request, execution_strategy)
        execution_time = time.time() - start_time
        
        # 6. Cache result if appropriate
        if self.should_cache_result(query_request, execution_time):
            self.cache_query_result(query_request, result)
        
        # 7. Update performance statistics
        self.performance_monitor.record_query_performance({
            'query_hash': self.hash_query(query_request),
            'execution_time': execution_time,
            'result_size': len(result),
            'optimizations': optimization_plan['optimizations_applied']
        })
        
        return {
            'result': result,
            'execution_time': execution_time,
            'optimization_plan': optimization_plan
        }
    
    def implement_intelligent_caching(self):
        """Implement multi-layer intelligent caching"""
        
        caching_strategy = {
            # Layer 1: Query result cache
            'result_cache': {
                'storage': 'redis_cluster',
                'ttl_strategy': 'adaptive',  # Based on data freshness
                'size_limit': '10GB',
                'eviction_policy': 'lru_with_frequency'
            },
            
            # Layer 2: Materialized view cache
            'materialized_cache': {
                'storage': 'warehouse_tables',
                'refresh_strategy': 'incremental',
                'partition_strategy': 'date_based',
                'compression': 'columnar'
            },
            
            # Layer 3: Semantic layer cache
            'semantic_cache': {
                'storage': 'in_memory',
                'content': ['metric_definitions', 'dimension_hierarchies'],
                'refresh_trigger': 'model_change'
            }
        }
        
        # Adaptive TTL based on data characteristics
        def calculate_adaptive_ttl(query_metadata):
            base_ttl = 3600  # 1 hour
            
            # Real-time data: shorter TTL
            if query_metadata.get('real_time_data'):
                return 300  # 5 minutes
            
            # Historical data: longer TTL
            if query_metadata.get('historical_only'):
                return 86400  # 24 hours
            
            # Frequently accessed: medium TTL
            if query_metadata.get('access_frequency', 0) > 100:
                return 1800  # 30 minutes
            
            return base_ttl
        
        return caching_strategy
    
    def implement_auto_scaling(self):
        """Implement automatic resource scaling"""
        
        scaling_config = {
            'triggers': {
                'query_queue_length > 10': 'scale_up_compute',
                'avg_response_time > 30s': 'add_read_replicas',
                'cache_hit_rate < 60%': 'increase_cache_size',
                'concurrent_users > 500': 'scale_horizontally'
            },
            
            'scaling_actions': {
                'scale_up_compute': {
                    'action': 'increase_warehouse_size',
                    'increment': '1_size_level',
                    'max_size': 'X4LARGE'
                },
                
                'add_read_replicas': {
                    'action': 'create_read_replica',
                    'max_replicas': 5,
                    'distribution': 'round_robin'
                },
                
                'increase_cache_size': {
                    'action': 'expand_cache_cluster',
                    'increment': '25%',
                    'max_size': '50GB'
                }
            },
            
            'cost_optimization': {
                'scale_down_triggers': {
                    'low_usage_duration > 30_minutes': 'reduce_resources',
                    'off_peak_hours': 'minimal_resources'
                },
                
                'resource_scheduling': {
                    'business_hours': 'full_capacity',
                    'off_hours': '50%_capacity',
                    'weekends': '25%_capacity'
                }
            }
        }
        
        return scaling_config
```

**Performance Optimization Techniques**:

1. **Intelligent Materialization**:
   - Automatic identification of frequently accessed data
   - Incremental refresh strategies
   - Partition and cluster key optimization

2. **Multi-Layer Caching**:
   - Query result caching with adaptive TTL
   - Materialized view caching
   - Semantic layer metadata caching

3. **Query Optimization**:
   - Automatic query rewriting
   - Join order optimization
   - Predicate pushdown to data warehouse

4. **Resource Management**:
   - Auto-scaling based on workload
   - Resource scheduling for cost optimization
   - Connection pooling and load balancing

5. **Performance Monitoring**:
   - Real-time query performance tracking
   - Automatic bottleneck identification
   - Performance regression detection

---

## 🔴 Advanced Level Questions

### Q6: Design a comprehensive data governance framework for Omni that ensures data quality, security, and compliance in a multi-team environment.
**Answer**: A comprehensive data governance framework for Omni requires multiple layers of controls, policies, and automated processes to ensure data quality, security, and regulatory compliance.

**Governance Architecture**:
```yaml
# Example: Comprehensive governance framework
# File: governance/data_governance_framework.yml

data_governance:
  # ===== DATA CLASSIFICATION =====
  classification_framework:
    levels:
      public:
        description: "Data safe for public consumption"
        access_control: "all_authenticated_users"
        retention_policy: "indefinite"
        
      internal:
        description: "Internal business data"
        access_control: "company_employees"
        retention_policy: "7_years"
        
      confidential:
        description: "Sensitive business information"
        access_control: "need_to_know_basis"
        retention_policy: "5_years"
        audit_required: true
        
      restricted:
        description: "Highly sensitive data (PII, financial)"
        access_control: "explicit_authorization"
        retention_policy: "3_years"
        encryption_required: true
        audit_required: true
        masking_required: true
    
    # Automatic classification rules
    auto_classification:
      patterns:
        - regex: ".*_pii_.*|.*ssn.*|.*credit_card.*"
          classification: "restricted"
          
        - regex: ".*revenue.*|.*profit.*|.*salary.*"
          classification: "confidential"
          
        - regex: ".*customer.*|.*user.*|.*order.*"
          classification: "internal"
          
        - regex: ".*public.*|.*marketing.*"
          classification: "public"
  
  # ===== ACCESS CONTROL =====
  access_control:
    rbac_model:
      roles:
        data_analyst:
          permissions:
            - "read:public"
            - "read:internal"
            - "create:reports"
            - "share:internal_users"
          data_sources: ["analytics_warehouse", "staging_db"]
          row_level_filters: ["region = user_region"]
          
        business_user:
          permissions:
            - "read:public"
            - "read:internal:filtered"
            - "view:certified_dashboards"
          data_sources: ["analytics_warehouse"]
          column_restrictions: ["exclude_pii_columns"]
          
        data_scientist:
          permissions:
            - "read:public"
            - "read:internal" 
            - "read:confidential:masked"
            - "create:ml_models"
          data_sources: ["analytics_warehouse", "ml_feature_store"]
          
        compliance_officer:
          permissions:
            - "read:all_levels"
            - "audit:all_activities"
            - "export:compliance_reports"
          data_sources: ["all"]
    
    # Attribute-based access control
    abac_policies:
      - name: "geographic_data_access"
        condition: "user.region == data.region OR user.role == 'global_admin'"
        
      - name: "time_based_access"
        condition: "current_time BETWEEN '06:00' AND '22:00' OR user.role == 'on_call'"
        
      - name: "data_sensitivity_access"
        condition: "data.classification_level <= user.clearance_level"
  
  # ===== DATA QUALITY =====
  data_quality:
    quality_dimensions:
      completeness:
        description: "Percentage of non-null values"
        threshold: 95
        
      accuracy:
        description: "Correctness of data values"
        validation_rules: ["business_rule_compliance", "referential_integrity"]
        
      consistency:
        description: "Data consistency across sources"
        cross_reference_checks: true
        
      timeliness:
        description: "Data freshness and currency"
        max_age_hours: 24
        
      validity:
        description: "Data conforms to defined formats"
        format_validation: true
    
    # Automated quality checks
    quality_monitors:
      - name: "revenue_consistency_check"
        sql: |
          SELECT 
            COUNT(*) as inconsistencies
          FROM fact_orders o
          LEFT JOIN (
            SELECT order_id, SUM(line_total) as calculated_total
            FROM fact_order_lines
            GROUP BY order_id
          ) l ON o.order_id = l.order_id
          WHERE ABS(o.order_total - COALESCE(l.calculated_total, 0)) > 0.01
        expected_result: 0
        severity: "critical"
        
      - name: "customer_data_completeness"
        sql: |
          SELECT 
            (COUNT(*) - COUNT(email)) * 100.0 / COUNT(*) as missing_email_pct
          FROM dim_customers
          WHERE created_date >= CURRENT_DATE - INTERVAL '30 days'
        threshold: "< 5"
        severity: "warning"
```

```python
# Example: Governance enforcement engine
# File: governance/governance_engine.py

class OmniGovernanceEngine:
    def __init__(self):
        self.omni_client = OmniClient()
        self.governance_config = self.load_governance_config()
        self.audit_logger = AuditLogger()
        
    def enforce_data_classification(self):
        """Automatically classify and protect data based on content"""
        
        models = self.omni_client.get_all_models()
        
        for model in models:
            # Analyze model content for sensitive data
            classification = self.classify_model_content(model)
            
            # Apply appropriate protections
            if classification == 'restricted':
                self.apply_restricted_protections(model)
            elif classification == 'confidential':
                self.apply_confidential_protections(model)
            
            # Update model metadata
            self.omni_client.update_model_metadata(model['name'], {
                'data_classification': classification,
                'classification_date': datetime.now(),
                'classification_method': 'automated'
            })
    
    def implement_row_level_security(self, model_name, user_context):
        """Implement dynamic row-level security"""
        
        user_roles = self.get_user_roles(user_context['user_id'])
        security_filters = []
        
        # Apply role-based filters
        for role in user_roles:
            role_config = self.governance_config['access_control']['rbac_model']['roles'][role]
            
            if 'row_level_filters' in role_config:
                for filter_rule in role_config['row_level_filters']:
                    # Parse and apply filter
                    parsed_filter = self.parse_security_filter(filter_rule, user_context)
                    security_filters.append(parsed_filter)
        
        # Apply attribute-based policies
        abac_policies = self.governance_config['access_control']['abac_policies']
        for policy in abac_policies:
            if self.evaluate_abac_condition(policy['condition'], user_context):
                continue  # Policy allows access
            else:
                # Apply restrictive filter
                security_filters.append(policy.get('restrictive_filter', 'FALSE'))
        
        return security_filters
    
    def implement_column_level_security(self, model_name, user_context):
        """Implement column-level security and masking"""
        
        model_schema = self.omni_client.get_model_schema(model_name)
        secured_columns = {}
        
        user_clearance = self.get_user_clearance_level(user_context['user_id'])
        
        for column in model_schema['columns']:
            column_classification = self.get_column_classification(model_name, column['name'])
            
            # Determine access level
            if column_classification == 'restricted' and user_clearance < 4:
                secured_columns[column['name']] = 'BLOCKED'
            elif column_classification == 'confidential' and user_clearance < 3:
                secured_columns[column['name']] = 'MASKED'
            elif column_classification == 'internal' and user_clearance < 2:
                secured_columns[column['name']] = 'BLOCKED'
        
        return secured_columns
    
    def implement_audit_logging(self):
        """Comprehensive audit logging system"""
        
        audit_events = [
            'data_access',
            'model_creation',
            'model_modification',
            'dashboard_view',
            'data_export',
            'permission_change',
            'security_violation'
        ]
        
        for event_type in audit_events:
            self.setup_audit_trigger(event_type)
    
    def setup_audit_trigger(self, event_type):
        """Setup audit trigger for specific event type"""
        
        audit_config = {
            'event_type': event_type,
            'capture_fields': [
                'user_id',
                'timestamp',
                'resource_accessed',
                'action_performed',
                'ip_address',
                'user_agent',
                'session_id'
            ],
            'retention_period': '7_years',
            'encryption': True,
            'real_time_alerts': self.get_alert_rules(event_type)
        }
        
        # Create audit trigger
        self.audit_logger.create_trigger(audit_config)
    
    def monitor_compliance(self):
        """Continuous compliance monitoring"""
        
        compliance_checks = {
            'gdpr_compliance': self.check_gdpr_compliance(),
            'sox_compliance': self.check_sox_compliance(),
            'data_retention': self.check_retention_compliance(),
            'access_reviews': self.check_access_review_compliance()
        }
        
        # Generate compliance report
        report = self.generate_compliance_report(compliance_checks)
        
        # Alert on violations
        violations = [check for check, result in compliance_checks.items() 
                     if not result['compliant']]
        
        if violations:
            self.send_compliance_alerts(violations)
        
        return report
    
    def implement_data_lineage_tracking(self):
        """Implement comprehensive data lineage tracking"""
        
        lineage_tracker = {
            'source_tracking': {
                'database_tables': True,
                'api_endpoints': True,
                'file_sources': True,
                'external_systems': True
            },
            
            'transformation_tracking': {
                'sql_transformations': True,
                'model_dependencies': True,
                'calculated_fields': True,
                'aggregations': True
            },
            
            'consumption_tracking': {
                'dashboard_usage': True,
                'report_generation': True,
                'data_exports': True,
                'api_consumption': True
            },
            
            'impact_analysis': {
                'upstream_changes': True,
                'downstream_effects': True,
                'business_impact': True,
                'user_notifications': True
            }
        }
        
        return lineage_tracker
```

**Key Governance Components**:

1. **Data Classification**: Automatic identification and protection of sensitive data
2. **Access Controls**: Multi-layered security with RBAC and ABAC
3. **Data Quality**: Continuous monitoring and validation
4. **Audit Logging**: Comprehensive activity tracking
5. **Compliance Management**: Automated compliance checking and reporting
6. **Data Lineage**: Complete traceability from source to consumption
7. **Privacy Controls**: Data masking and anonymization capabilities

---

## 🟣 Expert Level Questions

### Q7: How would you architect a real-time analytics platform using Omni that can handle streaming data and provide sub-second query responses for operational dashboards?
**Answer**: Building a real-time analytics platform with Omni requires a sophisticated architecture that combines streaming data processing, in-memory computing, and intelligent caching strategies.

**Real-Time Analytics Architecture**:

```yaml
# Example: Real-time analytics architecture
# File: architecture/realtime_analytics.yml

realtime_architecture:
  # ===== STREAMING DATA LAYER =====
  streaming_ingestion:
    kafka_cluster:
      brokers: 9
      partitions_per_topic: 12
      replication_factor: 3
      retention: "7_days"
      
    topics:
      - name: "user_events"
        partitions: 24
        schema_registry: true
        
      - name: "transaction_events"
        partitions: 36
        schema_registry: true
        
      - name: "system_metrics"
        partitions: 12
        schema_registry: true
    
    stream_processors:
      - name: "event_enrichment"
        framework: "kafka_streams"
        parallelism: 24
        
      - name: "real_time_aggregation"
        framework: "apache_flink"
        parallelism: 36
        
      - name: "anomaly_detection"
        framework: "apache_flink"
        parallelism: 12
  
  # ===== REAL-TIME STORAGE LAYER =====
  storage_systems:
    olap_engine:
      type: "apache_druid"
      cluster_size: 12
      segment_granularity: "hour"
      query_granularity: "minute"
      
    in_memory_cache:
      type: "redis_cluster"
      nodes: 6
      memory_per_node: "64GB"
      persistence: "rdb_aof"
      
    time_series_db:
      type: "influxdb"
      cluster_size: 3
      retention_policy: "30_days"
      
    search_engine:
      type: "elasticsearch"
      cluster_size: 9
      indices_per_day: true
  
  # ===== OMNI INTEGRATION LAYER =====
  omni_integration:
    real_time_connectors:
      - type: "druid_connector"
        connection_pool: 20
        query_timeout: "5s"
        
      - type: "redis_connector"
        connection_pool: 50
        query_timeout: "100ms"
        
      - type: "influxdb_connector"
        connection_pool: 10
        query_timeout: "2s"
    
    caching_strategy:
      l1_cache:
        type: "in_memory"
        size: "8GB"
        ttl: "30s"
        
      l2_cache:
        type: "redis"
        size: "64GB"
        ttl: "5m"
        
      l3_cache:
        type: "materialized_views"
        refresh_interval: "1m"
```

```python
# Example: Real-time analytics implementation
# File: realtime/analytics_engine.py

class RealTimeAnalyticsEngine:
    def __init__(self):
        self.omni_client = OmniClient()
        self.stream_processor = StreamProcessor()
        self.cache_manager = CacheManager()
        self.druid_client = DruidClient()
        
    def setup_real_time_models(self):
        """Setup Omni models for real-time analytics"""
        
        # Real-time user activity model
        realtime_user_activity = """
        model realtime_user_activity {
          sql_table_name: "druid.user_events"
          
          # Time dimension with minute granularity
          dimension_group event_time {
            type: time
            timeframes: [raw, minute, hour, date]
            sql: ${TABLE}.__time
            datatype: timestamp
          }
          
          # User dimensions
          dimension user_id {
            type: string
            sql: ${TABLE}.user_id
          }
          
          dimension session_id {
            type: string
            sql: ${TABLE}.session_id
          }
          
          dimension event_type {
            type: string
            sql: ${TABLE}.event_type
          }
          
          # Real-time measures
          measure active_users_now {
            type: count_distinct
            sql: ${user_id}
            filters: [
              "${event_time_raw} >= CURRENT_TIMESTAMP - INTERVAL '5 minutes'"
            ]
            description: "Users active in last 5 minutes"
          }
          
          measure events_per_minute {
            type: count
            sql: ${TABLE}.event_id
            description: "Events processed per minute"
          }
          
          measure average_session_duration {
            type: average
            sql: ${TABLE}.session_duration_seconds
            filters: [
              "${event_type} = 'session_end'"
            ]
            description: "Average session duration in seconds"
          }
        }
        """
        
        # Real-time transaction model
        realtime_transactions = """
        model realtime_transactions {
          sql_table_name: "druid.transaction_events"
          
          dimension_group transaction_time {
            type: time
            timeframes: [raw, minute, hour, date]
            sql: ${TABLE}.__time
          }
          
          dimension transaction_type {
            type: string
            sql: ${TABLE}.transaction_type
          }
          
          dimension payment_method {
            type: string
            sql: ${TABLE}.payment_method
          }
          
          measure revenue_per_minute {
            type: sum
            sql: ${TABLE}.amount
            value_format: "$#,##0.00"
            description: "Revenue generated per minute"
          }
          
          measure transaction_count {
            type: count
            sql: ${TABLE}.transaction_id
            description: "Number of transactions"
          }
          
          measure average_transaction_value {
            type: average
            sql: ${TABLE}.amount
            value_format: "$#,##0.00"
            description: "Average transaction amount"
          }
          
          measure fraud_rate {
            type: number
            sql: SUM(CASE WHEN ${TABLE}.fraud_score > 0.8 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
            value_format: "#0.00%"
            description: "Percentage of potentially fraudulent transactions"
          }
        }
        """
        
        self.omni_client.create_model(realtime_user_activity)
        self.omni_client.create_model(realtime_transactions)
    
    def implement_streaming_pipeline(self):
        """Implement streaming data pipeline for real-time analytics"""
        
        pipeline_config = {
            'kafka_to_druid': {
                'source_topics': ['user_events', 'transaction_events'],
                'druid_datasources': ['user_events', 'transaction_events'],
                'ingestion_spec': {
                    'granularitySpec': {
                        'segmentGranularity': 'HOUR',
                        'queryGranularity': 'MINUTE'
                    },
                    'tuningConfig': {
                        'maxRowsInMemory': 100000,
                        'intermediatePersistPeriod': 'PT10M'
                    }
                }
            },
            
            'real_time_aggregations': {
                'window_functions': [
                    {
                        'name': 'active_users_5min',
                        'window_size': '5_minutes',
                        'slide_interval': '1_minute',
                        'aggregation': 'count_distinct(user_id)'
                    },
                    {
                        'name': 'revenue_per_minute',
                        'window_size': '1_minute',
                        'slide_interval': '10_seconds',
                        'aggregation': 'sum(transaction_amount)'
                    }
                ],
                'output_sink': 'redis_cache'
            }
        }
        
        return pipeline_config
    
    def optimize_for_sub_second_queries(self):
        """Implement optimizations for sub-second query response"""
        
        optimization_strategies = {
            # Pre-compute common aggregations
            'pre_aggregation': {
                'active_users_by_minute': {
                    'sql': """
                        SELECT 
                            DATE_TRUNC('minute', event_time) as minute,
                            COUNT(DISTINCT user_id) as active_users
                        FROM user_events
                        WHERE event_time >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
                        GROUP BY 1
                    """,
                    'refresh_interval': '10_seconds',
                    'storage': 'redis'
                },
                
                'revenue_by_minute': {
                    'sql': """
                        SELECT 
                            DATE_TRUNC('minute', transaction_time) as minute,
                            SUM(amount) as revenue,
                            COUNT(*) as transaction_count
                        FROM transaction_events
                        WHERE transaction_time >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
                        GROUP BY 1
                    """,
                    'refresh_interval': '5_seconds',
                    'storage': 'redis'
                }
            },
            
            # Intelligent query routing
            'query_routing': {
                'real_time_queries': {
                    'time_range': '< 1_hour',
                    'route_to': 'druid_cluster'
                },
                'recent_queries': {
                    'time_range': '1_hour_to_24_hours',
                    'route_to': 'cached_aggregations'
                },
                'historical_queries': {
                    'time_range': '> 24_hours',
                    'route_to': 'data_warehouse'
                }
            },
            
            # Result caching with smart invalidation
            'smart_caching': {
                'cache_layers': [
                    {
                        'name': 'query_result_cache',
                        'storage': 'redis',
                        'ttl': '30_seconds',
                        'invalidation': 'time_based'
                    },
                    {
                        'name': 'aggregation_cache',
                        'storage': 'in_memory',
                        'ttl': '10_seconds',
                        'invalidation': 'data_change'
                    }
                ]
            }
        }
        
        return optimization_strategies
    
    def create_operational_dashboard(self):
        """Create real-time operational dashboard"""
        
        dashboard_config = {
            'name': 'Real-Time Operations Dashboard',
            'refresh_interval': '5_seconds',
            'auto_refresh': True,
            
            'tiles': [
                {
                    'name': 'Active Users Now',
                    'type': 'big_number',
                    'query': {
                        'model': 'realtime_user_activity',
                        'measure': 'active_users_now'
                    },
                    'alert_thresholds': {
                        'critical_low': 100,
                        'warning_low': 500
                    }
                },
                
                {
                    'name': 'Revenue Per Minute',
                    'type': 'line_chart',
                    'query': {
                        'model': 'realtime_transactions',
                        'dimensions': ['transaction_time_minute'],
                        'measures': ['revenue_per_minute'],
                        'filters': {
                            'transaction_time': 'last_2_hours'
                        }
                    },
                    'real_time_updates': True
                },
                
                {
                    'name': 'System Health',
                    'type': 'gauge_chart',
                    'query': {
                        'model': 'system_metrics',
                        'measures': ['cpu_utilization', 'memory_usage', 'error_rate']
                    },
                    'thresholds': {
                        'cpu_utilization': {'warning': 70, 'critical': 90},
                        'memory_usage': {'warning': 80, 'critical': 95},
                        'error_rate': {'warning': 1, 'critical': 5}
                    }
                },
                
                {
                    'name': 'Transaction Fraud Detection',
                    'type': 'scatter_plot',
                    'query': {
                        'model': 'realtime_transactions',
                        'dimensions': ['transaction_time_minute'],
                        'measures': ['fraud_rate', 'transaction_count'],
                        'filters': {
                            'transaction_time': 'last_1_hour'
                        }
                    },
                    'anomaly_detection': True
                }
            ],
            
            'alerts': [
                {
                    'name': 'Low Active Users Alert',
                    'condition': 'active_users_now < 100',
                    'notification_channels': ['slack', 'pagerduty'],
                    'escalation_policy': 'immediate'
                },
                
                {
                    'name': 'High Fraud Rate Alert',
                    'condition': 'fraud_rate > 5',
                    'notification_channels': ['email', 'sms'],
                    'escalation_policy': 'within_5_minutes'
                }
            ]
        }
        
        return self.omni_client.create_dashboard(dashboard_config)
```

**Key Real-Time Architecture Components**:

1. **Streaming Ingestion**: Kafka-based event streaming with schema registry
2. **Stream Processing**: Real-time aggregation and enrichment using Flink/Kafka Streams
3. **OLAP Engine**: Apache Druid for sub-second analytical queries
4. **Multi-Layer Caching**: Redis + in-memory caching for ultra-fast access
5. **Intelligent Query Routing**: Route queries to optimal data store based on time range
6. **Pre-Aggregation**: Compute common metrics in advance
7. **Real-Time Dashboards**: Auto-refreshing operational dashboards with alerting

This architecture enables sub-second query responses for operational dashboards while maintaining data consistency and providing comprehensive real-time analytics capabilities.

---

**🎯 Key Interview Takeaways:**

1. **SQL-First Philosophy**: Understand transparent, code-based modeling approach
2. **Modern Data Stack**: Integration with cloud warehouses and streaming systems
3. **Semantic Layer**: Centralized metrics governance and consistency
4. **Real-Time Capabilities**: Streaming analytics and operational dashboards
5. **Performance Optimization**: Multi-layer caching and query optimization
6. **Collaboration Features**: Real-time editing and sharing capabilities
7. **Governance Framework**: Data security, quality, and compliance management

**🎯 Next Steps**: Explore Omni's integration with modern data stack tools, practice SQL modeling patterns, and understand real-time analytics architecture principles!