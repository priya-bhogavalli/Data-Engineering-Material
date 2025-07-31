# Tableau Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Tableau and why is it important for data engineering?
**Answer**: Tableau is a powerful data visualization and business intelligence tool that helps transform raw data into interactive dashboards and reports.

**Importance for Data Engineering**:
- **Data Visualization**: Transform complex data into understandable visuals
- **Self-Service Analytics**: Enable business users to explore data independently
- **Real-time Dashboards**: Connect to live data sources for up-to-date insights
- **Data Quality Validation**: Quickly identify data issues through visualization
- **Stakeholder Communication**: Present data insights to non-technical audiences

```sql
-- Example: Data preparation for Tableau
-- Sales performance dashboard data
SELECT 
    s.sale_date,
    s.sale_id,
    p.product_name,
    p.category,
    c.customer_name,
    c.region,
    s.quantity,
    s.unit_price,
    s.total_amount,
    s.discount_amount,
    (s.total_amount - s.discount_amount) AS net_revenue,
    CASE 
        WHEN s.total_amount > 1000 THEN 'High Value'
        WHEN s.total_amount > 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS sale_category
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN customers c ON s.customer_id = c.customer_id
WHERE s.sale_date >= DATEADD(year, -2, GETDATE());

-- Time series data for trend analysis
SELECT 
    DATE_TRUNC('month', sale_date) AS month,
    region,
    category,
    COUNT(*) AS transaction_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_transaction_value
FROM sales_fact sf
JOIN dim_date dd ON sf.date_key = dd.date_key
JOIN dim_product dp ON sf.product_key = dp.product_key
JOIN dim_customer dc ON sf.customer_key = dc.customer_key
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;
```

### 2. Explain Tableau's data connection types and when to use each
**Answer**: Tableau offers different connection types optimized for various use cases and performance requirements.

**Connection Types**:

**Live Connection**:
- Real-time data access
- Always shows current data
- Queries sent to source database
- Best for: Real-time dashboards, small datasets

**Extract Connection**:
- Snapshot of data stored in Tableau
- Faster performance
- Can work offline
- Best for: Large datasets, complex calculations

**Published Data Source**:
- Centralized, reusable data connection
- Consistent definitions across organization
- Version control and governance
- Best for: Enterprise deployments

```python
# Python script to create Tableau extract
import pandas as pd
import tableauserverclient as TSC

def create_tableau_extract():
    """Create Tableau extract from data source."""
    
    # Connect to data source
    df = pd.read_sql("""
        SELECT 
            date_column,
            category,
            sales_amount,
            profit_margin,
            customer_segment
        FROM sales_data
        WHERE date_column >= '2023-01-01'
    """, connection)
    
    # Data preprocessing for Tableau
    df['date_column'] = pd.to_datetime(df['date_column'])
    df['year'] = df['date_column'].dt.year
    df['month'] = df['date_column'].dt.month
    df['quarter'] = df['date_column'].dt.quarter
    
    # Create calculated fields
    df['profit_amount'] = df['sales_amount'] * df['profit_margin']
    df['sales_category'] = pd.cut(
        df['sales_amount'], 
        bins=[0, 1000, 5000, float('inf')], 
        labels=['Low', 'Medium', 'High']
    )
    
    # Save as Tableau extract format
    df.to_csv('sales_extract.csv', index=False)
    
    return df

# Publish data source to Tableau Server
def publish_data_source():
    """Publish data source to Tableau Server."""
    
    # Server connection
    server = TSC.Server('https://tableau-server.company.com')
    
    # Authentication
    tableau_auth = TSC.TableauAuth('username', 'password', 'site_id')
    
    with server.auth.sign_in(tableau_auth):
        # Create data source item
        datasource = TSC.DatasourceItem('project_id')
        datasource.name = 'Sales Data Source'
        datasource.description = 'Centralized sales data for reporting'
        
        # Publish data source
        datasource = server.datasources.publish(
            datasource, 
            'sales_extract.csv', 
            'Overwrite'
        )
        
        print(f"Data source published: {datasource.id}")
```

### 3. What are Dimensions and Measures in Tableau?
**Answer**: Dimensions and Measures are fundamental concepts that determine how data is aggregated and displayed.

**Dimensions**:
- Categorical fields (qualitative data)
- Used to slice and dice data
- Examples: Product Category, Region, Date
- Create headers and labels

**Measures**:
- Numerical fields (quantitative data)
- Aggregated by default (SUM, AVG, COUNT, etc.)
- Examples: Sales Amount, Quantity, Profit
- Create axes and values

```sql
-- Data structure example for Tableau
CREATE VIEW tableau_sales_view AS
SELECT 
    -- Dimensions (categorical data)
    p.product_name,
    p.category,
    p.sub_category,
    c.customer_segment,
    c.region,
    c.country,
    d.year,
    d.quarter,
    d.month_name,
    d.day_of_week,
    
    -- Measures (numerical data)
    s.quantity,
    s.unit_price,
    s.sales_amount,
    s.discount_amount,
    s.profit_amount,
    s.shipping_cost,
    
    -- Calculated measures
    (s.sales_amount - s.discount_amount) AS net_sales,
    (s.profit_amount / s.sales_amount) * 100 AS profit_margin_pct,
    
    -- Date field (can be dimension or measure)
    s.order_date,
    s.ship_date,
    DATEDIFF(day, s.order_date, s.ship_date) AS days_to_ship
    
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN customers c ON s.customer_id = c.customer_id
JOIN date_dim d ON s.order_date = d.date_key;
```

**Tableau Calculated Fields**:
```
// Calculated Field Examples

// Profit Ratio
[Profit] / [Sales]

// Sales Growth
(ZN(SUM([Sales])) - LOOKUP(ZN(SUM([Sales])), -1)) / ABS(LOOKUP(ZN(SUM([Sales])), -1))

// Customer Segmentation
IF [Sales] > 10000 THEN "High Value"
ELSEIF [Sales] > 5000 THEN "Medium Value"
ELSE "Low Value"
END

// Date Calculations
DATETRUNC('month', [Order Date])
DATEDIFF('day', [Order Date], [Ship Date])

// String Manipulation
UPPER([Customer Name])
LEFT([Product Name], 10)
CONTAINS([Product Name], "Pro")

// Conditional Logic
CASE [Region]
    WHEN "North" THEN [Sales] * 1.1
    WHEN "South" THEN [Sales] * 1.05
    ELSE [Sales]
END
```

### 4. How do you create different chart types in Tableau?
**Answer**: Tableau offers various chart types, each suited for different data analysis needs.

**Common Chart Types and Use Cases**:

```
// Bar Chart - Compare categories
Columns: SUM([Sales])
Rows: [Category]

// Line Chart - Show trends over time
Columns: [Order Date]
Rows: SUM([Sales])

// Scatter Plot - Show correlation
Columns: SUM([Sales])
Rows: SUM([Profit])
Detail: [Customer Name]

// Heat Map - Show patterns in matrix
Columns: [Category]
Rows: [Region]
Color: SUM([Sales])

// Tree Map - Show hierarchical data
Size: SUM([Sales])
Color: SUM([Profit])
Detail: [Product Name]

// Pie Chart - Show parts of whole
Angle: SUM([Sales])
Color: [Category]

// Histogram - Show distribution
Columns: [Sales] (bin)
Rows: CNT([Customer ID])

// Box Plot - Show statistical distribution
Columns: [Category]
Rows: [Sales]
```

**Advanced Chart Examples**:
```python
# Python script to generate data for advanced Tableau charts
import pandas as pd
import numpy as np

def generate_dashboard_data():
    """Generate sample data for various chart types."""
    
    # Time series data for trend analysis
    dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
    time_series = pd.DataFrame({
        'date': dates,
        'sales': np.random.normal(1000, 200, len(dates)) + 
                np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 100,
        'profit': np.random.normal(150, 50, len(dates)),
        'orders': np.random.poisson(50, len(dates))
    })
    
    # Geographic data for map visualization
    regions = ['North', 'South', 'East', 'West', 'Central']
    states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
    
    geographic_data = pd.DataFrame({
        'state': np.random.choice(states, 1000),
        'region': np.random.choice(regions, 1000),
        'sales': np.random.exponential(1000, 1000),
        'customers': np.random.poisson(10, 1000)
    })
    
    # Product hierarchy for tree map
    categories = ['Technology', 'Furniture', 'Office Supplies']
    products = {
        'Technology': ['Phones', 'Computers', 'Accessories'],
        'Furniture': ['Chairs', 'Tables', 'Storage'],
        'Office Supplies': ['Paper', 'Binders', 'Pens']
    }
    
    product_data = []
    for category in categories:
        for product in products[category]:
            for i in range(50):
                product_data.append({
                    'category': category,
                    'product': product,
                    'sales': np.random.exponential(500),
                    'profit': np.random.normal(100, 30),
                    'quantity': np.random.poisson(5)
                })
    
    product_df = pd.DataFrame(product_data)
    
    return time_series, geographic_data, product_df
```

### 5. How do you create calculated fields and parameters?
**Answer**: Calculated fields and parameters add flexibility and interactivity to Tableau dashboards.

**Calculated Fields**:
```
// Basic Calculations
Profit Margin: [Profit] / [Sales]
Sales Growth: ([Sales] - LOOKUP([Sales], -1)) / LOOKUP([Sales], -1)

// Date Calculations
Days Since Order: DATEDIFF('day', [Order Date], TODAY())
Month Over Month Growth: 
(ZN(SUM([Sales])) - LOOKUP(ZN(SUM([Sales])), -1)) / ABS(LOOKUP(ZN(SUM([Sales])), -1))

// String Calculations
Full Name: [First Name] + " " + [Last Name]
Product Code: LEFT([Product Name], 3) + "-" + STR([Product ID])

// Conditional Logic
Customer Tier: 
IF [Total Sales] > 50000 THEN "Platinum"
ELSEIF [Total Sales] > 25000 THEN "Gold"
ELSEIF [Total Sales] > 10000 THEN "Silver"
ELSE "Bronze"
END

// Advanced Calculations
Running Total: RUNNING_SUM(SUM([Sales]))
Rank: RANK(SUM([Sales]), 'desc')
Percentile: PERCENTILE([Sales], 0.75)

// Window Functions
Moving Average: WINDOW_AVG(SUM([Sales]), -2, 0)
Year over Year: 
(ZN(SUM([Sales])) - ZN(SUM([Sales Previous Year]))) / ABS(ZN(SUM([Sales Previous Year])))
```

**Parameters for Interactivity**:
```
// Parameter Examples

// Metric Selection Parameter
Name: Metric Selector
Data Type: String
Allowable Values: List
Values: Sales, Profit, Quantity, Orders

// Calculated Field using Parameter
Selected Metric:
CASE [Metric Selector]
    WHEN "Sales" THEN SUM([Sales])
    WHEN "Profit" THEN SUM([Profit])
    WHEN "Quantity" THEN SUM([Quantity])
    WHEN "Orders" THEN COUNTD([Order ID])
END

// Date Range Parameter
Name: Analysis Period
Data Type: Integer
Current Value: 12
Range: 1 to 36

// Dynamic Date Filter
Date Filter: [Order Date] >= DATEADD('month', -[Analysis Period], TODAY())

// Top N Parameter
Name: Top N
Data Type: Integer
Current Value: 10
Range: 5 to 50

// Top N Calculation
Top N Products: INDEX() <= [Top N]
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you optimize Tableau dashboard performance?
**Answer**: Performance optimization involves data source optimization, efficient calculations, and dashboard design best practices.

**Data Source Optimization**:
```sql
-- Create optimized views for Tableau
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    product_category,
    customer_segment,
    region,
    COUNT(*) AS order_count,
    SUM(sales_amount) AS total_sales,
    SUM(profit_amount) AS total_profit,
    AVG(sales_amount) AS avg_order_value
FROM sales_fact sf
JOIN dim_product dp ON sf.product_key = dp.product_key
JOIN dim_customer dc ON sf.customer_key = dc.customer_key
JOIN dim_date dd ON sf.date_key = dd.date_key
GROUP BY 1, 2, 3, 4;

-- Create indexes for better performance
CREATE INDEX idx_sales_date_category ON sales_fact (date_key, product_key);
CREATE INDEX idx_customer_segment ON dim_customer (customer_segment);
```

**Tableau Performance Best Practices**:
```
// Efficient Calculated Fields

// Avoid complex nested calculations
// Bad:
IF [Region] = "North" THEN
    IF [Category] = "Technology" THEN [Sales] * 1.1
    ELSE [Sales] * 1.05
    END
ELSE [Sales]
END

// Good: Use CASE for multiple conditions
CASE 
    WHEN [Region] = "North" AND [Category] = "Technology" THEN [Sales] * 1.1
    WHEN [Region] = "North" THEN [Sales] * 1.05
    ELSE [Sales]
END

// Use aggregated calculations when possible
// Instead of: SUM([Sales]) / SUM([Quantity])
// Use: AVG([Unit Price]) when appropriate

// Optimize date calculations
// Use built-in date functions instead of string manipulation
DATETRUNC('month', [Order Date])  // Good
DATE(LEFT(STR([Order Date]), 7) + "-01")  // Avoid

// Context filters for performance
// Use context filters to reduce data before other filters are applied
```

**Dashboard Design Optimization**:
```python
# Python script for Tableau performance monitoring
import tableauserverclient as TSC
import pandas as pd

def monitor_dashboard_performance():
    """Monitor Tableau dashboard performance metrics."""
    
    server = TSC.Server('https://tableau-server.company.com')
    tableau_auth = TSC.TableauAuth('username', 'password', 'site_id')
    
    with server.auth.sign_in(tableau_auth):
        # Get workbook performance data
        workbooks = server.workbooks.get()
        
        performance_data = []
        for workbook in workbooks:
            # Get workbook details
            workbook_detail = server.workbooks.get_by_id(workbook.id)
            
            performance_data.append({
                'workbook_name': workbook.name,
                'size': workbook.size,
                'views': len(workbook.views),
                'last_updated': workbook.updated_at,
                'project': workbook.project_name
            })
        
        df = pd.DataFrame(performance_data)
        
        # Identify large workbooks that may need optimization
        large_workbooks = df[df['size'] > 50000000]  # > 50MB
        
        return large_workbooks

def optimize_extract_refresh():
    """Optimize extract refresh schedules."""
    
    # Schedule incremental refreshes for large datasets
    refresh_schedule = {
        'sales_data': {
            'type': 'incremental',
            'frequency': 'hourly',
            'filter': "order_date >= DATEADD('day', -7, TODAY())"
        },
        'customer_data': {
            'type': 'full',
            'frequency': 'daily',
            'time': '02:00'
        }
    }
    
    return refresh_schedule
```

### 7. How do you implement advanced analytics in Tableau?
**Answer**: Use Tableau's built-in analytics features and integrate with external tools for advanced statistical analysis.

**Built-in Analytics Features**:
```
// Trend Lines
// Add trend line to scatter plot or line chart
// Analytics Pane > Trend Line > Linear/Logarithmic/Exponential/Polynomial

// Forecasting
// Analytics Pane > Forecast
// Automatic forecasting based on historical data
// Customizable confidence intervals and seasonality

// Reference Lines and Bands
// Analytics Pane > Reference Line
// Add average, median, constant lines
// Confidence intervals and percentiles

// Clustering
// Analytics Pane > Cluster
// K-means clustering for scatter plots
// Automatic optimal cluster determination

// Statistical Summary
// Analytics Pane > Summarize
// Box plots with quartiles, median, outliers
```

**Advanced Calculated Fields**:
```
// Statistical Calculations

// Standard Deviation
STDEV([Sales])

// Correlation Coefficient
CORR([Sales], [Profit])

// Percentiles
PERCENTILE([Sales], 0.95)

// Z-Score
([Sales] - WINDOW_AVG(SUM([Sales]))) / WINDOW_STDEV(SUM([Sales]))

// Moving Statistics
Moving Average: WINDOW_AVG(SUM([Sales]), -6, 0)
Moving Standard Deviation: WINDOW_STDEV(SUM([Sales]), -6, 0)

// Cohort Analysis
Customer Cohort Month: 
DATEDIFF('month', 
    {FIXED [Customer ID]: MIN([Order Date])}, 
    [Order Date]
)

// RFM Analysis (Recency, Frequency, Monetary)
Recency: DATEDIFF('day', {FIXED [Customer ID]: MAX([Order Date])}, TODAY())
Frequency: {FIXED [Customer ID]: COUNTD([Order ID])}
Monetary: {FIXED [Customer ID]: SUM([Sales])}

// Customer Lifetime Value
CLV: [Average Order Value] * [Purchase Frequency] * [Customer Lifespan]
```

**Integration with R and Python**:
```python
# TabPy integration for advanced analytics
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def tableau_clustering(_arg1, _arg2, _arg3):
    """Custom clustering function for Tableau."""
    
    # Prepare data
    data = pd.DataFrame({
        'sales': _arg1,
        'profit': _arg2,
        'quantity': _arg3
    })
    
    # Standardize features
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(data_scaled)
    
    return clusters.tolist()

def tableau_forecasting(_arg1, _arg2):
    """Custom forecasting function for Tableau."""
    
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    
    # Prepare time series data
    dates = pd.to_datetime(_arg1)
    values = _arg2
    
    ts_data = pd.Series(values, index=dates).sort_index()
    
    # Fit exponential smoothing model
    model = ExponentialSmoothing(
        ts_data, 
        trend='add', 
        seasonal='add', 
        seasonal_periods=12
    )
    fitted_model = model.fit()
    
    # Generate forecast
    forecast = fitted_model.forecast(steps=12)
    
    return forecast.tolist()

# Tableau calculated field using TabPy
# SCRIPT_REAL("
# return tableau_clustering(_arg1, _arg2, _arg3)
# ", SUM([Sales]), SUM([Profit]), SUM([Quantity]))
```

### 8. How do you create interactive dashboards with actions?
**Answer**: Use Tableau actions to create dynamic, interactive dashboards that respond to user interactions.

**Types of Actions**:
```
// Filter Actions
// Source Sheet: Sales by Region (map)
// Target Sheet: Product Details (bar chart)
// Action: When user clicks on region, filter product details

// Highlight Actions
// Source Sheet: Category Performance
// Target Sheet: Monthly Trends
// Action: Highlight corresponding data points across sheets

// URL Actions
// Source Sheet: Customer List
// Target Sheet: External CRM system
// URL: https://crm.company.com/customer/<Customer ID>

// Parameter Actions
// Source Sheet: Metric Selection buttons
// Target Parameter: Selected Metric
// Action: Change parameter value based on selection

// Set Actions
// Source Sheet: Product comparison
// Target Set: Selected Products
// Action: Add/remove products from comparison set
```

**Dashboard Interactivity Examples**:
```python
# Python script to generate interactive dashboard data
def create_interactive_dashboard_data():
    """Create data structure for interactive dashboards."""
    
    # Drill-down hierarchy data
    hierarchy_data = {
        'level_1': ['Technology', 'Furniture', 'Office Supplies'],
        'level_2': {
            'Technology': ['Phones', 'Computers', 'Accessories'],
            'Furniture': ['Chairs', 'Tables', 'Storage'],
            'Office Supplies': ['Paper', 'Binders', 'Pens']
        },
        'level_3': {
            'Phones': ['iPhone', 'Samsung', 'Google'],
            'Computers': ['Laptops', 'Desktops', 'Tablets'],
            # ... more detailed breakdown
        }
    }
    
    # Time-based filtering data
    time_periods = {
        'daily': pd.date_range('2024-01-01', '2024-12-31', freq='D'),
        'weekly': pd.date_range('2024-01-01', '2024-12-31', freq='W'),
        'monthly': pd.date_range('2024-01-01', '2024-12-31', freq='M'),
        'quarterly': pd.date_range('2024-01-01', '2024-12-31', freq='Q')
    }
    
    # Geographic drill-down data
    geographic_hierarchy = {
        'country': ['USA', 'Canada', 'Mexico'],
        'state': {
            'USA': ['CA', 'TX', 'NY', 'FL'],
            'Canada': ['ON', 'BC', 'AB', 'QC'],
            'Mexico': ['DF', 'JAL', 'NL', 'BC']
        },
        'city': {
            'CA': ['Los Angeles', 'San Francisco', 'San Diego'],
            'TX': ['Houston', 'Dallas', 'Austin'],
            # ... more cities
        }
    }
    
    return hierarchy_data, time_periods, geographic_hierarchy
```

**Advanced Dashboard Features**:
```
// Dynamic Titles
// Title: Top [Top N] [Selected Metric] by [Selected Dimension]

// Conditional Formatting
// Color: IF SUM([Sales]) > WINDOW_AVG(SUM([Sales])) THEN "Above Average" ELSE "Below Average" END

// Dynamic Axis
// Axis Range: Based on parameter selection
// Synchronized axes across multiple charts

// Tooltip Customization
// Custom HTML tooltip with additional context
// Embedded visualizations in tooltips

// Mobile Optimization
// Device-specific layouts
// Touch-friendly interactions
// Responsive design elements
```

### 9. How do you implement data governance in Tableau?
**Answer**: Establish data governance through certified data sources, user permissions, and standardized practices.

**Data Source Certification**:
```python
# Python script for data source governance
import tableauserverclient as TSC

def implement_data_governance():
    """Implement data governance practices."""
    
    server = TSC.Server('https://tableau-server.company.com')
    tableau_auth = TSC.TableauAuth('admin', 'password', 'site_id')
    
    with server.auth.sign_in(tableau_auth):
        
        # Certify trusted data sources
        trusted_sources = [
            'Sales_Data_Warehouse',
            'Customer_Master_Data',
            'Financial_Reporting_DB'
        ]
        
        for source_name in trusted_sources:
            datasources = server.datasources.get()
            for ds in datasources:
                if ds.name == source_name:
                    # Certify data source
                    ds.certified = True
                    ds.certification_note = "Certified by Data Governance Team"
                    server.datasources.update(ds)
        
        # Set up user permissions
        governance_permissions = {
            'data_stewards': ['View', 'Connect', 'Save', 'Download'],
            'business_analysts': ['View', 'Connect'],
            'executives': ['View'],
            'data_engineers': ['View', 'Connect', 'Save', 'Download', 'Delete']
        }
        
        return governance_permissions

def create_data_dictionary():
    """Create standardized data dictionary."""
    
    data_dictionary = {
        'sales_amount': {
            'definition': 'Total revenue from product sales excluding taxes',
            'data_type': 'Currency',
            'source': 'Sales Transaction System',
            'calculation': 'quantity * unit_price',
            'business_rules': 'Excludes returns and refunds'
        },
        'customer_segment': {
            'definition': 'Customer classification based on purchase behavior',
            'data_type': 'String',
            'values': ['Consumer', 'Corporate', 'Home Office'],
            'source': 'Customer Master Data',
            'update_frequency': 'Monthly'
        },
        'profit_margin': {
            'definition': 'Percentage of profit relative to sales',
            'data_type': 'Percentage',
            'calculation': '(sales_amount - cost_amount) / sales_amount * 100',
            'business_rules': 'Calculated at product level'
        }
    }
    
    return data_dictionary
```

**Standardization and Best Practices**:
```
// Naming Conventions
// Dimensions: [Category], [Region], [Customer Segment]
// Measures: [Sales Amount], [Profit Amount], [Order Count]
// Calculated Fields: [Profit Margin %], [Sales Growth %]

// Color Standards
// Positive values: Green (#2E8B57)
// Negative values: Red (#DC143C)
// Neutral values: Blue (#4682B4)
// Categories: Consistent color palette across dashboards

// Dashboard Standards
// Logo placement: Top left corner
// Filter placement: Top or left side
// Title format: [Dashboard Name] - [Time Period]
// Font: Tableau Book for titles, Tableau Regular for content

// Documentation Requirements
// Data source documentation
// Calculation explanations
// Business context and assumptions
// Refresh schedules and dependencies
```

### 10. How do you troubleshoot common Tableau issues?
**Answer**: Use systematic approaches to diagnose and resolve performance, data, and visualization issues.

**Performance Troubleshooting**:
```python
# Performance monitoring and troubleshooting
def diagnose_performance_issues():
    """Systematic approach to performance troubleshooting."""
    
    performance_checklist = {
        'data_source': [
            'Check extract vs live connection performance',
            'Analyze query execution time in database',
            'Review data source filters and context filters',
            'Optimize database indexes and views'
        ],
        'calculations': [
            'Identify complex calculated fields',
            'Review table calculations and window functions',
            'Check for nested IF statements',
            'Optimize LOD expressions'
        ],
        'dashboard_design': [
            'Count number of marks in visualizations',
            'Review filter interactions and dependencies',
            'Check for unnecessary detail in views',
            'Analyze sheet loading order'
        ],
        'server_resources': [
            'Monitor CPU and memory usage',
            'Check concurrent user load',
            'Review extract refresh schedules',
            'Analyze network latency'
        ]
    }
    
    return performance_checklist

def common_error_solutions():
    """Common Tableau errors and solutions."""
    
    error_solutions = {
        'cannot_mix_aggregate_non_aggregate': {
            'error': 'Cannot mix aggregate and non-aggregate comparisons',
            'cause': 'Comparing aggregated and non-aggregated fields',
            'solution': 'Use LOD expressions or ensure consistent aggregation'
        },
        'data_source_error': {
            'error': 'Unable to connect to data source',
            'cause': 'Connection timeout or credential issues',
            'solution': 'Check network connectivity and refresh credentials'
        },
        'invalid_date': {
            'error': 'Invalid date value',
            'cause': 'Date format mismatch or null values',
            'solution': 'Use DATEPARSE() or handle null dates with IFNULL()'
        },
        'memory_error': {
            'error': 'Out of memory error',
            'cause': 'Too many marks or complex calculations',
            'solution': 'Reduce data granularity or use data extracts'
        }
    }
    
    return error_solutions

# Tableau log analysis
def analyze_tableau_logs():
    """Analyze Tableau logs for troubleshooting."""
    
    import re
    
    log_patterns = {
        'slow_query': r'Query took (\d+) seconds',
        'memory_usage': r'Memory usage: (\d+)MB',
        'connection_error': r'Connection failed: (.+)',
        'extract_refresh': r'Extract refresh (completed|failed)'
    }
    
    # Parse log files for patterns
    with open('tableau_server.log', 'r') as log_file:
        log_content = log_file.read()
        
        issues = {}
        for pattern_name, pattern in log_patterns.items():
            matches = re.findall(pattern, log_content)
            if matches:
                issues[pattern_name] = matches
    
    return issues
```

**Data Quality Issues**:
```
// Common Data Quality Checks

// Null Value Detection
Null Count: SUM(IF ISNULL([Field]) THEN 1 ELSE 0 END)
Null Percentage: [Null Count] / COUNT([Field]) * 100

// Duplicate Detection
Duplicate Records: 
IF COUNTD([Record ID]) < COUNT([Record ID]) THEN "Duplicates Found" ELSE "No Duplicates" END

// Data Freshness Check
Data Age: DATEDIFF('day', MAX([Last Updated]), TODAY())
Freshness Status: IF [Data Age] > 1 THEN "Stale" ELSE "Fresh" END

// Value Range Validation
Out of Range: 
IF [Sales Amount] < 0 OR [Sales Amount] > 1000000 THEN "Invalid" ELSE "Valid" END

// Referential Integrity
Orphaned Records: 
IF ISNULL([Foreign Key]) THEN "Orphaned" ELSE "Valid" END
```

This comprehensive set covers Tableau fundamentals through advanced dashboard development and troubleshooting with practical data engineering examples.