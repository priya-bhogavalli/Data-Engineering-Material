# Tableau Key Concepts

## 1. Tableau Fundamentals
**What is Tableau**: Business intelligence and data visualization platform for creating interactive dashboards and reports.

**Key Components**:
- **Tableau Desktop**: Authoring tool for creating visualizations
- **Tableau Server/Cloud**: Platform for sharing and collaboration
- **Tableau Prep**: Data preparation and cleaning tool
- **Tableau Public**: Free platform for public visualizations

## 2. Data Connections
```sql
-- Custom SQL in Tableau
SELECT 
    o.order_date,
    o.customer_id,
    c.customer_name,
    c.segment,
    o.sales,
    o.profit,
    p.category,
    p.sub_category
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= DATE('2023-01-01')
```

**Data Source Types**:
- **Live Connection**: Real-time queries to database
- **Extract**: Snapshot of data stored in .hyper format
- **Published Data Source**: Shared data source on server

**Connection Best Practices**:
```
Extract for:
- Large datasets (>1M rows)
- Complex calculations
- Performance optimization
- Offline analysis

Live for:
- Real-time data requirements
- Small datasets
- Frequently changing data
- Regulatory compliance
```

## 3. Calculated Fields
```tableau
// Basic calculations
Profit Ratio = [Profit] / [Sales]

Sales Growth = 
([Sales] - LOOKUP([Sales], -1)) / LOOKUP([Sales], -1)

// Date calculations
Days Since Order = DATEDIFF('day', [Order Date], TODAY())

Quarter Over Quarter Growth = 
(ZN(SUM([Sales])) - ZN(SUM([Sales]))) / ABS(ZN(SUM([Sales])))

// String manipulation
Customer Full Name = [First Name] + " " + [Last Name]

Email Domain = RIGHT([Email], LEN([Email]) - FIND("@", [Email]))

// Conditional logic
Customer Segment = 
IF [Sales] >= 10000 THEN "High Value"
ELSEIF [Sales] >= 5000 THEN "Medium Value"
ELSE "Low Value"
END

// Advanced calculations
Running Total = RUNNING_SUM(SUM([Sales]))

Rank by Sales = RANK(SUM([Sales]), 'desc')

Percentile = PERCENTILE([Sales], 0.75)
```

## 4. Parameters and Filters
```tableau
// Parameter examples
Date Range Parameter:
- Data Type: Date
- Allowable Values: Range
- Minimum: #2020-01-01#
- Maximum: TODAY()

Metric Selector Parameter:
- Data Type: String
- Allowable Values: List
- Values: Sales, Profit, Quantity, Discount

// Using parameters in calculations
Selected Metric = 
CASE [Metric Selector]
    WHEN "Sales" THEN SUM([Sales])
    WHEN "Profit" THEN SUM([Profit])
    WHEN "Quantity" THEN SUM([Quantity])
    WHEN "Discount" THEN AVG([Discount])
END

// Dynamic filtering
Dynamic Date Filter = [Order Date] >= [Start Date Parameter]

// Context filters for performance
// Right-click dimension → Add to Context
// Applies filter before other calculations
```

## 5. Table Calculations
```tableau
// Window functions
Percent of Total = SUM([Sales]) / TOTAL(SUM([Sales]))

Difference from Previous = SUM([Sales]) - LOOKUP(SUM([Sales]), -1)

Moving Average = WINDOW_AVG(SUM([Sales]), -2, 0)

// Ranking
Dense Rank = RANK_DENSE(SUM([Sales]), 'desc')

Percentile Rank = RANK_PERCENTILE(SUM([Sales]))

// Growth calculations
Year over Year Growth = 
(ZN(SUM([Sales])) - ZN(LOOKUP(SUM([Sales]), -12))) / 
ABS(ZN(LOOKUP(SUM([Sales]), -12)))

// Custom table calculations
Index = INDEX()  // Row number
Size = SIZE()    // Total rows in partition
First = FIRST()  // Distance from first row
Last = LAST()    // Distance from last row
```

## 6. Level of Detail (LOD) Expressions
```tableau
// FIXED LOD - ignores view filters
Customer Lifetime Value = 
{FIXED [Customer ID]: SUM([Sales])}

Average Order Value by Customer = 
{FIXED [Customer ID]: SUM([Sales])} / {FIXED [Customer ID]: COUNTD([Order ID])}

// INCLUDE LOD - adds dimensions
Sales per Customer per Region = 
{INCLUDE [Customer ID]: SUM([Sales])}

// EXCLUDE LOD - removes dimensions
Percent of Regional Sales = 
SUM([Sales]) / {EXCLUDE [State]: SUM([Sales])}

// Cohort analysis
Customer First Order Date = 
{FIXED [Customer ID]: MIN([Order Date])}

Months Since First Order = 
DATEDIFF('month', [Customer First Order Date], [Order Date])

// Advanced LOD examples
Top N Customers by Region = 
{FIXED [Region]: 
    IF RANK(SUM([Sales]), 'desc') <= [Top N Parameter] 
    THEN [Customer Name] 
    END}
```

## 7. Dashboard Design
```tableau
// Dashboard actions
Filter Action:
- Source: Sales by Region sheet
- Target: Product Details sheet
- Fields: Region → Region

Highlight Action:
- Source: Trend chart
- Target: All sheets
- Fields: Date → Date

URL Action:
- URL: https://company.com/customer/[Customer ID]
- Fields: Customer ID

// Dashboard parameters
Device Preview:
- Desktop: 1200x800
- Tablet: 1024x768
- Phone: 375x667

Layout containers:
- Horizontal: Side-by-side arrangement
- Vertical: Top-to-bottom stacking
- Floating: Absolute positioning
```

## 8. Performance Optimization
```tableau
// Data source optimization
1. Use extracts for large datasets
2. Aggregate data at source when possible
3. Remove unused fields
4. Use appropriate data types
5. Create efficient joins

// Calculation optimization
Efficient: SUM([Sales]) / SUM([Quantity])
Inefficient: SUM([Sales] / [Quantity])

// Use ATTR() for non-aggregated fields
Customer Type = ATTR([Customer Segment])

// Avoid complex nested calculations
// Break into multiple calculated fields

// Context filters for performance
// Apply most selective filters as context filters

// Dashboard optimization
1. Limit number of marks (< 10,000)
2. Use filters to reduce data
3. Avoid complex calculations in tooltips
4. Use dashboard actions instead of quick filters
5. Optimize sheet rendering order
```

## 9. Advanced Analytics
```tableau
// Statistical functions
Correlation = CORR([Sales], [Profit])
Standard Deviation = STDEV([Sales])
Variance = VAR([Sales])

// Forecasting (built-in)
// Analytics pane → Forecast
// Automatic trend detection and seasonality

// Clustering
// Analytics pane → Cluster
// K-means clustering on selected dimensions

// Reference lines and bands
// Analytics pane → Reference Line
Average Line = AVG([Sales])
Percentile Band = PERCENTILE([Sales], 0.25) to PERCENTILE([Sales], 0.75)

// Trend lines
// Analytics pane → Trend Line
// Linear, logarithmic, exponential, polynomial

// R/Python integration
SCRIPT_REAL("
library(forecast)
ts_data <- ts(.arg1, frequency=12)
forecast_result <- forecast(ts_data, h=12)
return(as.numeric(forecast_result$mean))
", SUM([Sales]))
```

## 10. Data Preparation with Tableau Prep
```tableau
// Prep flow steps
1. Input: Connect to data source
2. Clean: Remove nulls, fix data types
3. Join: Combine multiple tables
4. Union: Stack similar tables
5. Aggregate: Group and summarize
6. Pivot: Reshape data structure
7. Output: Save to file or publish

// Cleaning operations
- Remove empty rows/columns
- Split columns by delimiter
- Rename fields
- Change data types
- Filter rows
- Create calculated fields

// Join types in Prep
- Inner Join: Matching records only
- Left Join: All from left, matching from right
- Right Join: All from right, matching from left
- Full Outer Join: All records from both
- Union: Stack tables vertically

// Calculated fields in Prep
Clean Phone = REGEXP_REPLACE([Phone], '[^0-9]', '')
Full Name = [First Name] + ' ' + [Last Name]
Age Group = 
IF [Age] < 25 THEN 'Young'
ELSEIF [Age] < 55 THEN 'Middle'
ELSE 'Senior'
END

// Output options
- Tableau Data Extract (.hyper)
- CSV file
- Database table
- Published data source
```