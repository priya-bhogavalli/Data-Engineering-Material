# Yellowfin BI Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
3. [Architecture](#-architecture)
4. [Data Connectivity](#-data-connectivity)
5. [Analytics & Visualization](#-analytics--visualization)
6. [Collaboration Features](#-collaboration-features)
7. [Embedded Analytics](#-embedded-analytics)
8. [Performance Optimization](#-performance-optimization)
9. [When to Use Yellowfin BI](#-when-to-use-yellowfin-bi)
10. [Interview Focus Areas](#-interview-focus-areas)

---

## 🎯 Overview

Yellowfin BI is a comprehensive business intelligence and analytics platform that combines traditional BI capabilities with modern collaborative features and embedded analytics.

**Key Benefits:**
- **Collaborative BI**: Social collaboration features built into analytics
- **Embedded Analytics**: Easy integration into existing applications
- **Automated Insights**: AI-powered automated analysis and alerts
- **Mobile-First**: Native mobile applications with offline capabilities
- **Self-Service**: User-friendly interface for business users

## 📦 Core Components

### 1. Yellowfin Reports
**Definition**: Traditional reporting engine for creating formatted reports and dashboards.

**Key Features:**
- **Pixel-Perfect Reports**: Precise formatting for regulatory and operational reports
- **Parameterized Reports**: Dynamic reports with user-defined parameters
- **Scheduled Distribution**: Automated report delivery via email, FTP, or web services
- **Multi-Format Export**: PDF, Excel, CSV, Word, and other formats

```python
# Example: Report configuration
report_config = {
    "report_name": "Monthly Sales Report",
    "report_type": "tabular",
    "data_source": "sales_database",
    "parameters": [
        {
            "name": "month",
            "type": "date_picker",
            "default": "current_month",
            "required": True
        },
        {
            "name": "region",
            "type": "dropdown",
            "source": "SELECT DISTINCT region FROM sales_data",
            "default": "All Regions"
        }
    ],
    "formatting": {
        "page_size": "A4",
        "orientation": "landscape",
        "header": "Company Logo and Report Title",
        "footer": "Page numbers and generation timestamp"
    },
    "distribution": {
        "schedule": "monthly_first_business_day",
        "recipients": ["sales_managers@company.com", "executives@company.com"],
        "format": "PDF"
    }
}
```

### 2. Yellowfin Dashboards
**Definition**: Interactive dashboard platform for real-time business monitoring and analysis.

**Key Features:**
- **Drag-and-Drop Designer**: Visual dashboard creation interface
- **Real-Time Updates**: Live data refresh capabilities
- **Interactive Filters**: Dynamic filtering and drill-down actions
- **Responsive Design**: Automatic adaptation to different screen sizes

### 3. Yellowfin Stories
**Definition**: Collaborative analytics platform that combines data analysis with social collaboration.

**Key Features:**
- **Data Storytelling**: Narrative-driven data presentation
- **Social Collaboration**: Comments, discussions, and sharing
- **Timeline View**: Chronological view of analysis and discussions
- **Automated Insights**: AI-generated insights and anomaly detection

### 4. Yellowfin Signals
**Definition**: Automated monitoring and alerting system for business metrics.

**Key Features:**
- **Automated Monitoring**: Continuous monitoring of key metrics
- **Smart Alerts**: AI-powered anomaly detection and alerting
- **Root Cause Analysis**: Automated analysis of metric changes
- **Proactive Notifications**: Push notifications and email alerts

```python
# Example: Signal configuration
signal_config = {
    "signal_name": "Sales Performance Monitor",
    "metric": "daily_sales_revenue",
    "monitoring_frequency": "hourly",
    "alert_conditions": [
        {
            "condition": "value_drops_below",
            "threshold": "10000",
            "severity": "high"
        },
        {
            "condition": "percentage_change",
            "threshold": "-15%",
            "comparison": "same_day_last_week",
            "severity": "medium"
        }
    ],
    "recipients": ["sales_director@company.com", "ceo@company.com"],
    "delivery_methods": ["email", "mobile_push", "dashboard_notification"]
}
```

## 🏗️ Architecture

### Yellowfin BI Platform Architecture
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           YELLOWFIN BI PLATFORM                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                        PRESENTATION LAYER                                   │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │   Web Client    │  │  Mobile Apps    │  │ Embedded Apps   │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ • Dashboards    │  │ • iOS App       │  │ • JavaScript SDK│             │ │
│  │ │ • Reports       │  │ • Android App   │  │ • REST APIs     │             │ │
│  │ │ • Stories       │  │ • Offline Mode  │  │ • White Label   │             │ │
│  │ │ • Signals       │  │ • Push Alerts   │  │ • Custom Themes │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         APPLICATION LAYER                                   │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │ Analytics Engine│  │Collaboration    │  │  AI/ML Engine   │             │ │
│  │ │                 │  │    Engine       │  │                 │             │ │
│  │ │ • Query Engine  │  │ • Social Feed   │  │ • Auto Insights │             │ │
│  │ │ • Calculations  │  │ • Comments      │  │ • Anomaly Detect│             │ │
│  │ │ • Aggregations  │  │ • Notifications │  │ • Forecasting   │             │ │
│  │ │ • Caching       │  │ • Workflows     │  │ • NLP Processing│             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          SERVICES LAYER                                     │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │Security Service │  │ Metadata Service│  │ Scheduler Service│             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ • Authentication│  │ • Data Models   │  │ • Report Jobs   │             │ │
│  │ │ • Authorization │  │ • Relationships │  │ • Data Refresh  │             │ │
│  │ │ • Audit Logging │  │ • Calculations  │  │ • Alerts        │             │ │
│  │ │ • Encryption    │  │ • Lineage       │  │ • Maintenance   │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           DATA LAYER                                        │ │
│  │                                                                             │ │
│  │ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │ │  Data Sources   │  │   Data Cache    │  │   Metadata DB   │             │ │
│  │ │                 │  │                 │  │                 │             │ │
│  │ │ • RDBMS         │  │ • Query Cache   │  │ • System Config │             │ │
│  │ │ • Cloud DBs     │  │ • Result Cache  │  │ • User Profiles │             │ │
│  │ │ • Files/APIs    │  │ • Temp Storage  │  │ • Content Store │             │ │
│  │ │ • Big Data      │  │ • Session Data  │  │ • Audit Logs    │             │ │
│  │ └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘

                              DEPLOYMENT OPTIONS
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐               │
│  │   On-Premise    │  │     Cloud       │  │   Embedded      │               │
│  │                 │  │                 │  │                 │               │
│  │ • Full Control  │  │ • SaaS Model    │  │ • White Label   │               │
│  │ • Custom Config │  │ • Quick Deploy  │  │ • API Integration│               │
│  │ • High Security │  │ • Auto Updates  │  │ • Custom Branding│               │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔗 Data Connectivity

### Supported Data Sources
```python
data_connectivity = {
    "relational_databases": {
        "enterprise_databases": {
            "oracle": {
                "versions": ["11g", "12c", "18c", "19c", "21c"],
                "features": ["PL/SQL support", "Materialized views", "Partitioned tables"],
                "connection_types": ["Native", "JDBC", "ODBC"]
            },
            "sql_server": {
                "versions": ["2012", "2014", "2016", "2017", "2019", "2022"],
                "features": ["Stored procedures", "Views", "Functions", "CTEs"],
                "authentication": ["Windows", "SQL Server", "Azure AD"]
            },
            "db2": {
                "platforms": ["z/OS", "Linux", "Unix", "Windows"],
                "features": ["Stored procedures", "User-defined functions"],
                "connection_pooling": True
            }
        },
        "open_source_databases": {
            "mysql": {
                "versions": ["5.7", "8.0"],
                "features": ["Views", "Stored procedures", "Functions"],
                "ssl_support": True
            },
            "postgresql": {
                "versions": ["10", "11", "12", "13", "14", "15"],
                "features": ["Advanced SQL", "JSON support", "Arrays"],
                "connection_pooling": True
            }
        }
    },
    
    "cloud_platforms": {
        "amazon_aws": {
            "services": {
                "rds": "Managed relational databases",
                "redshift": "Data warehouse service",
                "athena": "Serverless query service",
                "s3": "Object storage with SQL queries"
            },
            "authentication": ["IAM roles", "Access keys", "Database credentials"]
        },
        "microsoft_azure": {
            "services": {
                "sql_database": "Managed SQL database",
                "synapse_analytics": "Analytics service",
                "cosmos_db": "Multi-model database",
                "data_lake": "Big data storage"
            },
            "authentication": ["Azure AD", "Service principals", "Connection strings"]
        },
        "google_cloud": {
            "services": {
                "cloud_sql": "Managed relational databases",
                "bigquery": "Serverless data warehouse",
                "firestore": "NoSQL document database",
                "cloud_storage": "Object storage"
            },
            "authentication": ["Service accounts", "OAuth 2.0", "API keys"]
        }
    },
    
    "big_data_platforms": {
        "hadoop_ecosystem": {
            "hive": "Data warehouse software",
            "impala": "Real-time SQL queries",
            "spark_sql": "Spark SQL engine",
            "presto": "Distributed SQL query engine"
        },
        "nosql_databases": {
            "mongodb": "Document database",
            "cassandra": "Wide-column database",
            "elasticsearch": "Search and analytics engine"
        }
    }
}
```

### Data Integration Patterns
```python
integration_patterns = {
    "real_time_connectivity": {
        "description": "Direct connection to live data sources",
        "use_cases": ["Operational dashboards", "Real-time monitoring", "Live reporting"],
        "benefits": ["Always current data", "No data duplication", "Immediate updates"],
        "considerations": ["Source system performance", "Network latency", "Concurrent user limits"]
    },
    
    "cached_data": {
        "description": "Data cached in Yellowfin for performance",
        "use_cases": ["High-performance dashboards", "Complex calculations", "Large user base"],
        "benefits": ["Fast query response", "Reduced source load", "Offline capabilities"],
        "refresh_options": ["Scheduled", "On-demand", "Incremental", "Real-time"]
    },
    
    "data_warehouse": {
        "description": "Connection to centralized data warehouse",
        "use_cases": ["Historical analysis", "Cross-functional reporting", "Enterprise BI"],
        "benefits": ["Consistent data model", "Optimized for analytics", "Data governance"],
        "requirements": ["ETL processes", "Data modeling", "Maintenance overhead"]
    }
}
```

## 📊 Analytics & Visualization

### Visualization Types
```python
visualization_capabilities = {
    "standard_charts": {
        "bar_charts": {
            "types": ["Vertical", "Horizontal", "Stacked", "Grouped", "100% Stacked"],
            "use_cases": ["Category comparison", "Ranking analysis", "Part-to-whole"],
            "customization": ["Colors", "Labels", "Tooltips", "Animations"]
        },
        "line_charts": {
            "types": ["Simple", "Multi-series", "Area", "Stepped", "Spline"],
            "use_cases": ["Time series", "Trend analysis", "Forecasting"],
            "features": ["Multiple Y-axes", "Trend lines", "Annotations", "Zoom/pan"]
        },
        "pie_charts": {
            "types": ["Standard", "Donut", "Semi-circle", "Exploded"],
            "use_cases": ["Market share", "Budget allocation", "Simple proportions"],
            "enhancements": ["3D effects", "Custom colors", "Data labels"]
        }
    },
    
    "advanced_visualizations": {
        "geographic_maps": {
            "types": ["Choropleth", "Symbol maps", "Heat maps", "Flow maps"],
            "data_requirements": ["Geographic identifiers", "Numeric measures"],
            "features": ["Zoom controls", "Layer management", "Custom boundaries"]
        },
        "statistical_charts": {
            "types": ["Box plots", "Scatter plots", "Histograms", "Regression lines"],
            "use_cases": ["Statistical analysis", "Correlation studies", "Distribution analysis"],
            "features": ["Confidence intervals", "Outlier detection", "Clustering"]
        },
        "specialized_charts": {
            "types": ["Gantt charts", "Waterfall charts", "Bullet charts", "Gauge charts"],
            "use_cases": ["Project management", "Financial analysis", "Performance monitoring"],
            "customization": ["Thresholds", "Color coding", "Interactive elements"]
        }
    },
    
    "interactive_features": {
        "drill_actions": {
            "types": ["Drill down", "Drill up", "Drill through", "Drill across"],
            "configuration": ["Hierarchy-based", "Custom navigation", "Parameter passing"],
            "user_experience": ["Breadcrumb navigation", "Context preservation"]
        },
        "filtering": {
            "types": ["Global filters", "Chart-specific filters", "Cross-filtering"],
            "controls": ["Dropdown", "Multi-select", "Date picker", "Slider", "Search"],
            "advanced_features": ["Cascading filters", "Filter dependencies", "Saved filter sets"]
        }
    }
}
```

### Analytics Features
```python
analytics_capabilities = {
    "calculated_fields": {
        "arithmetic_calculations": {
            "operations": ["Addition", "Subtraction", "Multiplication", "Division"],
            "functions": ["SUM", "AVG", "COUNT", "MIN", "MAX", "MEDIAN"],
            "examples": ["Profit = Revenue - Cost", "Growth Rate = (Current - Previous) / Previous"]
        },
        "date_calculations": {
            "functions": ["YEAR", "MONTH", "DAY", "QUARTER", "WEEK"],
            "relative_dates": ["Yesterday", "Last Week", "Last Month", "YTD", "QTD"],
            "date_arithmetic": ["Date differences", "Date additions", "Business days"]
        },
        "conditional_logic": {
            "functions": ["IF", "CASE", "COALESCE", "NULLIF"],
            "examples": ["Status = IF(Sales > Target, 'Above', 'Below')", "Category = CASE WHEN Amount > 1000 THEN 'High' ELSE 'Low' END"]
        }
    },
    
    "statistical_analysis": {
        "descriptive_statistics": {
            "measures": ["Mean", "Median", "Mode", "Standard deviation", "Variance"],
            "percentiles": ["25th", "50th", "75th", "90th", "95th", "99th"],
            "distribution": ["Skewness", "Kurtosis", "Range", "Interquartile range"]
        },
        "time_series_analysis": {
            "trend_analysis": ["Linear trends", "Polynomial trends", "Moving averages"],
            "seasonality": ["Seasonal decomposition", "Seasonal adjustment"],
            "forecasting": ["Linear regression", "Exponential smoothing", "ARIMA models"]
        }
    },
    
    "advanced_analytics": {
        "cohort_analysis": {
            "description": "Analyze user behavior over time",
            "metrics": ["Retention rates", "Churn analysis", "Lifetime value"],
            "visualizations": ["Cohort tables", "Retention curves", "Heat maps"]
        },
        "funnel_analysis": {
            "description": "Analyze conversion rates through process steps",
            "metrics": ["Conversion rates", "Drop-off rates", "Step completion"],
            "visualizations": ["Funnel charts", "Sankey diagrams", "Step analysis"]
        }
    }
}
```

## 🤝 Collaboration Features

### Social BI Capabilities
```python
collaboration_features = {
    "yellowfin_stories": {
        "data_storytelling": {
            "narrative_structure": "Combine data visualizations with narrative text",
            "timeline_view": "Chronological view of analysis and discussions",
            "collaborative_editing": "Multiple users can contribute to stories",
            "version_control": "Track changes and maintain story versions"
        },
        "social_features": {
            "comments_and_discussions": {
                "threaded_comments": "Nested comment threads on specific data points",
                "mentions": "@mention users to notify and involve them",
                "reactions": "Like, dislike, and emoji reactions",
                "notifications": "Real-time notifications for new comments"
            },
            "sharing_and_permissions": {
                "sharing_options": ["Public", "Private", "Team-specific", "Role-based"],
                "permission_levels": ["View", "Comment", "Edit", "Admin"],
                "external_sharing": "Share with external stakeholders via secure links"
            }
        }
    },
    
    "workflow_integration": {
        "approval_workflows": {
            "report_approval": "Multi-stage approval process for reports",
            "data_validation": "Collaborative data quality validation",
            "change_management": "Approval workflows for dashboard changes"
        },
        "task_management": {
            "action_items": "Create and assign action items from insights",
            "follow_up_tracking": "Track completion of assigned tasks",
            "integration": "Integration with project management tools"
        }
    },
    
    "knowledge_sharing": {
        "best_practices": {
            "template_library": "Shared library of dashboard and report templates",
            "calculation_library": "Reusable calculation formulas",
            "style_guides": "Consistent branding and styling guidelines"
        },
        "training_and_onboarding": {
            "guided_tours": "Interactive tours for new users",
            "help_documentation": "Context-sensitive help and documentation",
            "video_tutorials": "Embedded video tutorials and training materials"
        }
    }
}
```

## 🔧 Embedded Analytics

### Integration Capabilities
```python
embedded_analytics = {
    "integration_methods": {
        "javascript_sdk": {
            "description": "Client-side JavaScript SDK for web applications",
            "features": ["Dashboard embedding", "Single sign-on", "Custom styling"],
            "use_cases": ["Web applications", "Customer portals", "SaaS platforms"],
            "example_code": """
            // Embed Yellowfin dashboard
            yellowfin.embed({
                url: 'https://your-yellowfin-server.com',
                dashboardId: '12345',
                containerId: 'dashboard-container',
                theme: 'custom-theme',
                filters: {
                    'customer_id': getCurrentCustomerId(),
                    'date_range': 'last_30_days'
                }
            });
            """
        },
        "rest_api": {
            "description": "RESTful API for server-side integration",
            "endpoints": ["Authentication", "Content management", "User management", "Data access"],
            "use_cases": ["Backend integration", "Automated workflows", "Data synchronization"],
            "authentication": ["OAuth 2.0", "API keys", "JWT tokens"]
        },
        "iframe_embedding": {
            "description": "Simple iframe-based embedding",
            "features": ["Easy implementation", "Responsive design", "Security controls"],
            "limitations": ["Limited customization", "Cross-origin restrictions"],
            "use_cases": ["Quick integration", "Proof of concepts", "Internal applications"]
        }
    },
    
    "customization_options": {
        "white_labeling": {
            "branding": ["Custom logos", "Color schemes", "Fonts", "Styling"],
            "ui_customization": ["Menu structure", "Navigation", "Layout", "Controls"],
            "localization": ["Multi-language support", "Regional formatting", "Time zones"]
        },
        "functional_customization": {
            "feature_control": ["Enable/disable features", "Custom permissions", "Workflow modifications"],
            "data_security": ["Row-level security", "Column-level security", "Dynamic filtering"],
            "integration_hooks": ["Custom authentication", "Event handlers", "Callback functions"]
        }
    },
    
    "deployment_patterns": {
        "multi_tenant_saas": {
            "description": "Serve multiple customers from single instance",
            "features": ["Tenant isolation", "Custom branding per tenant", "Scalable architecture"],
            "considerations": ["Data security", "Performance isolation", "Customization limits"]
        },
        "customer_portal": {
            "description": "Provide analytics to external customers",
            "features": ["Customer-specific data", "Self-service analytics", "Branded experience"],
            "use_cases": ["B2B platforms", "Financial services", "Healthcare portals"]
        },
        "internal_applications": {
            "description": "Embed analytics in internal business applications",
            "features": ["Seamless integration", "Single sign-on", "Consistent user experience"],
            "benefits": ["Increased adoption", "Reduced training", "Better decision making"]
        }
    }
}
```

## ⚡ Performance Optimization

### Optimization Strategies
```python
performance_optimization = {
    "query_optimization": {
        "sql_optimization": {
            "techniques": ["Query rewriting", "Index utilization", "Join optimization"],
            "features": ["Automatic query optimization", "Execution plan analysis"],
            "monitoring": ["Query performance tracking", "Slow query identification"]
        },
        "caching_strategies": {
            "result_caching": {
                "levels": ["Query level", "User level", "Global level"],
                "invalidation": ["Time-based", "Data change triggers", "Manual refresh"],
                "storage": ["Memory", "Disk", "Distributed cache"]
            },
            "metadata_caching": {
                "components": ["Schema information", "User permissions", "Calculation definitions"],
                "benefits": ["Faster dashboard loading", "Reduced database queries"],
                "refresh_strategies": ["Automatic", "Scheduled", "On-demand"]
            }
        }
    },
    
    "data_optimization": {
        "data_modeling": {
            "best_practices": ["Star schema design", "Proper indexing", "Partitioning strategies"],
            "aggregation_tables": ["Pre-calculated summaries", "Materialized views", "OLAP cubes"],
            "data_types": ["Appropriate data type selection", "Compression techniques"]
        },
        "incremental_loading": {
            "strategies": ["Timestamp-based", "Change data capture", "Delta detection"],
            "benefits": ["Faster refresh times", "Reduced system load", "Near real-time data"],
            "implementation": ["ETL optimization", "Trigger-based updates", "Log mining"]
        }
    },
    
    "system_optimization": {
        "hardware_scaling": {
            "vertical_scaling": ["CPU upgrades", "Memory expansion", "Storage optimization"],
            "horizontal_scaling": ["Load balancing", "Clustering", "Distributed processing"],
            "cloud_scaling": ["Auto-scaling", "Elastic resources", "Performance monitoring"]
        },
        "application_tuning": {
            "jvm_optimization": ["Heap size tuning", "Garbage collection optimization"],
            "connection_pooling": ["Database connection optimization", "Resource management"],
            "thread_management": ["Concurrent processing", "Resource allocation"]
        }
    }
}
```

## 📈 When to Use Yellowfin BI

**Use Yellowfin BI When:**
- Need collaborative analytics with social features
- Require embedded analytics in existing applications
- Want automated insights and anomaly detection
- Need strong mobile BI capabilities
- Require pixel-perfect reporting alongside self-service analytics
- Want comprehensive BI platform with minimal integration complexity

**Consider Alternatives When:**
- Need advanced data science capabilities
- Require extensive data preparation features
- Have very large-scale enterprise requirements (10,000+ users)
- Need open-source or highly customizable solutions
- Require specialized industry-specific features

## 🎯 Interview Focus Areas

1. **Platform Components**: Reports, Dashboards, Stories, Signals
2. **Collaboration Features**: Social BI, data storytelling, workflow integration
3. **Embedded Analytics**: JavaScript SDK, REST API, white-labeling
4. **Data Connectivity**: Supported sources, integration patterns
5. **Automated Insights**: AI-powered analytics, anomaly detection
6. **Mobile BI**: Native apps, offline capabilities
7. **Performance**: Caching strategies, query optimization
8. **Security**: Authentication, authorization, data security
9. **Architecture**: Deployment options, scalability
10. **Comparison**: vs other BI tools (Tableau, Power BI, Qlik)

## 📚 Quick References

- [Yellowfin Documentation](https://wiki.yellowfinbi.com/)
- [Yellowfin Community](https://community.yellowfinbi.com/)
- [Developer Resources](https://wiki.yellowfinbi.com/display/yfcurrent/Developer+Resources)
- [Best Practices Guide](https://wiki.yellowfinbi.com/display/yfcurrent/Best+Practices)