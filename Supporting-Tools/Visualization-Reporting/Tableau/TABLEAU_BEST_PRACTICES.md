# Tableau Best Practices for Data Engineering

## Data Source Optimization

### Connection Strategy
```sql
-- Create optimized views for Tableau
CREATE VIEW tableau_sales_summary AS
SELECT 
    DATE_TRUNC('day', order_date) as order_date,
    customer_segment,
    product_category,
    region,
    SUM(sales_amount) as total_sales,
    COUNT(DISTINCT order_id) as order_count,
    COUNT(DISTINCT customer_id) as customer_count
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
JOIN dim_product p ON f.product_id = p.product_id
WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
GROUP BY 1, 2, 3, 4;
```

### Extract Optimization
```python
import tableauserverclient as TSC
import pandas as pd

def create_optimized_extract():
    df = pd.read_sql("""
        SELECT * FROM tableau_sales_summary
        WHERE order_date >= CURRENT_DATE - INTERVAL '1 year'
    """, connection)
    
    # Optimize data types
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['customer_segment'] = df['customer_segment'].astype('category')
    df['product_category'] = df['product_category'].astype('category')
    
    return df
```

## Dashboard Performance

### Calculation Optimization
```tableau
// Efficient calculated fields
{ FIXED [Customer ID] : SUM([Sales]) }

// Use parameters for thresholds
IF [Sales] > [Sales Threshold Parameter] THEN "High" ELSE "Low" END

// Table calculations for running totals
RUNNING_SUM(SUM([Sales]))

// Optimize date calculations
DATETRUNC('month', [Order Date])
```

## Security and Governance

### Row-Level Security
```sql
CREATE TABLE user_region_access (
    username VARCHAR(100),
    region VARCHAR(50)
);

CREATE VIEW secure_sales_data AS
SELECT s.*
FROM sales_data s
JOIN user_region_access u ON s.region = u.region
WHERE u.username = USER();
```

## Automation

### Extract Refresh
```python
import tableauserverclient as TSC

def refresh_extracts():
    server = TSC.Server('https://tableau-server')
    auth_req = TSC.TableauAuth('username', 'password', 'site_id')
    
    with server.auth.sign_in(auth_req):
        datasources, pagination = server.datasources.get()
        
        for ds in datasources:
            if ds.has_extracts:
                job = server.datasources.refresh(ds)
                print(f"Refresh job {job.id} started for {ds.name}")
```