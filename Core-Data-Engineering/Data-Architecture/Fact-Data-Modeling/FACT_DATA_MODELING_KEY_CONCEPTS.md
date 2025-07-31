# Fact Data Modeling Key Concepts

## 🎯 What is Fact Data Modeling?
Design approach for creating fact tables that store quantitative business measurements and events in data warehouses.

## 🏗️ Types of Fact Tables

### 1. Transaction Facts
```sql
-- Individual business events
CREATE TABLE fact_sales_transaction (
    transaction_id INT PRIMARY KEY,
    date_key INT,
    time_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    salesperson_key INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);
```

### 2. Periodic Snapshot Facts
```sql
-- Regular interval measurements
CREATE TABLE fact_inventory_snapshot (
    product_key INT,
    warehouse_key INT,
    date_key INT,
    quantity_on_hand INT,
    quantity_allocated INT,
    quantity_available INT,
    unit_cost DECIMAL(10,2),
    total_value DECIMAL(15,2),
    PRIMARY KEY (product_key, warehouse_key, date_key)
);

-- Monthly account balance snapshot
CREATE TABLE fact_account_balance_monthly (
    account_key INT,
    date_key INT,
    opening_balance DECIMAL(15,2),
    closing_balance DECIMAL(15,2),
    average_balance DECIMAL(15,2),
    transaction_count INT,
    PRIMARY KEY (account_key, date_key)
);
```

### 3. Accumulating Snapshot Facts
```sql
-- Process lifecycle tracking
CREATE TABLE fact_order_fulfillment (
    order_key INT PRIMARY KEY,
    customer_key INT,
    product_key INT,
    order_date_key INT,
    payment_date_key INT,
    ship_date_key INT,
    delivery_date_key INT,
    order_amount DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    days_to_payment INT,
    days_to_ship INT,
    days_to_delivery INT,
    order_status VARCHAR(20)
);
```

### 4. Factless Facts
```sql
-- Events without measures
CREATE TABLE fact_student_class_attendance (
    student_key INT,
    class_key INT,
    date_key INT,
    attendance_type_key INT,
    PRIMARY KEY (student_key, class_key, date_key)
);

-- Promotion coverage
CREATE TABLE fact_promotion_coverage (
    product_key INT,
    store_key INT,
    promotion_key INT,
    date_key INT,
    PRIMARY KEY (product_key, store_key, promotion_key, date_key)
);
```

## 📊 Fact Table Design Patterns

### Additive, Semi-Additive, and Non-Additive Facts
```sql
CREATE TABLE fact_financial_metrics (
    account_key INT,
    date_key INT,
    -- Additive: Can sum across all dimensions
    transaction_amount DECIMAL(15,2),
    transaction_count INT,
    
    -- Semi-additive: Can sum across some dimensions (not time)
    account_balance DECIMAL(15,2),
    
    -- Non-additive: Cannot sum meaningfully
    interest_rate DECIMAL(5,4),
    exchange_rate DECIMAL(10,6),
    
    -- Derived additive measures
    interest_earned AS (account_balance * interest_rate / 365)
);
```

### Multi-Grain Facts
```sql
-- Different levels of detail in same fact table
CREATE TABLE fact_sales_multi_grain (
    grain_type VARCHAR(20), -- 'TRANSACTION', 'DAILY', 'MONTHLY'
    transaction_id INT,     -- NULL for aggregated grains
    date_key INT,
    customer_key INT,
    product_key INT,
    quantity INT,
    total_amount DECIMAL(10,2),
    record_count INT        -- 1 for transactions, >1 for aggregates
);
```

### Conformed Facts
```sql
-- Shared fact definitions across business processes
CREATE TABLE fact_revenue (
    revenue_id INT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    channel_key INT,
    revenue_amount DECIMAL(15,2),
    revenue_type VARCHAR(20) -- 'SALES', 'SUBSCRIPTION', 'SERVICE'
);

-- Used consistently across different fact tables
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    -- ... other dimensions
    revenue_amount DECIMAL(15,2), -- Same definition as fact_revenue
    cost_amount DECIMAL(15,2),
    profit_amount AS (revenue_amount - cost_amount)
);
```

## 🔧 Advanced Fact Modeling

### Heterogeneous Products
```sql
-- Generic fact structure for different product types
CREATE TABLE fact_product_sales (
    sale_id INT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    base_amount DECIMAL(15,2),
    
    -- Product-specific measures (nullable)
    -- For books
    pages INT,
    isbn VARCHAR(20),
    
    -- For electronics
    warranty_months INT,
    power_consumption DECIMAL(8,2),
    
    -- For clothing
    size_key INT,
    color_key INT
);
```

### Hot Swappable Dimensions
```sql
-- Flexible dimension assignment
CREATE TABLE fact_flexible_sales (
    sale_id INT PRIMARY KEY,
    date_key INT,
    dimension_1_key INT, -- Could be customer, product, etc.
    dimension_2_key INT,
    dimension_3_key INT,
    dimension_type_1 VARCHAR(20), -- 'CUSTOMER', 'PRODUCT', etc.
    dimension_type_2 VARCHAR(20),
    dimension_type_3 VARCHAR(20),
    amount DECIMAL(15,2)
);
```

## 🚀 Implementation Strategies

### Python Fact Loading
```python
import pandas as pd
from datetime import datetime, timedelta

class FactTableLoader:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def load_transaction_facts(self, source_df, fact_table):
        """Load transaction-level facts"""
        # Add surrogate keys
        fact_df = self.add_dimension_keys(source_df)
        
        # Add audit columns
        fact_df['load_timestamp'] = datetime.now()
        fact_df['source_system'] = 'OLTP'
        
        # Load to fact table
        fact_df.to_sql(fact_table, self.conn, if_exists='append', index=False)
        
        return len(fact_df)
    
    def create_periodic_snapshot(self, base_date, fact_table):
        """Create periodic snapshot from transaction data"""
        snapshot_sql = f"""
        INSERT INTO {fact_table} (
            product_key, warehouse_key, date_key,
            quantity_on_hand, quantity_allocated, total_value
        )
        SELECT 
            product_key,
            warehouse_key,
            {self.get_date_key(base_date)} as date_key,
            SUM(CASE WHEN transaction_type = 'RECEIPT' THEN quantity ELSE -quantity END) as quantity_on_hand,
            SUM(CASE WHEN status = 'ALLOCATED' THEN quantity ELSE 0 END) as quantity_allocated,
            SUM(quantity * unit_cost) as total_value
        FROM fact_inventory_transactions
        WHERE transaction_date <= %s
        GROUP BY product_key, warehouse_key
        """
        
        cursor = self.conn.cursor()
        cursor.execute(snapshot_sql, (base_date,))
        self.conn.commit()
    
    def update_accumulating_snapshot(self, order_id, milestone, milestone_date):
        """Update accumulating snapshot with new milestone"""
        update_sql = f"""
        UPDATE fact_order_fulfillment 
        SET {milestone}_date_key = %s,
            days_to_{milestone} = DATEDIFF(day, order_date, %s)
        WHERE order_key = (
            SELECT order_key FROM dim_order WHERE order_id = %s
        )
        """
        
        date_key = self.get_date_key(milestone_date)
        cursor = self.conn.cursor()
        cursor.execute(update_sql, (date_key, milestone_date, order_id))
        self.conn.commit()
    
    def add_dimension_keys(self, source_df):
        """Replace business keys with surrogate keys"""
        fact_df = source_df.copy()
        
        # Customer key lookup
        customer_lookup = pd.read_sql(
            "SELECT customer_id, customer_key FROM dim_customer WHERE is_current = TRUE",
            self.conn
        )
        fact_df = fact_df.merge(customer_lookup, on='customer_id', how='left')
        
        # Product key lookup
        product_lookup = pd.read_sql(
            "SELECT product_id, product_key FROM dim_product WHERE is_current = TRUE",
            self.conn
        )
        fact_df = fact_df.merge(product_lookup, on='product_id', how='left')
        
        # Date key lookup
        fact_df['date_key'] = fact_df['transaction_date'].apply(
            lambda x: int(x.strftime('%Y%m%d'))
        )
        
        return fact_df
```

### Fact Aggregation Strategies
```python
class FactAggregator:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def create_daily_aggregates(self, source_fact_table, target_fact_table):
        """Create daily aggregated facts from transaction facts"""
        agg_sql = f"""
        INSERT INTO {target_fact_table} (
            date_key, customer_key, product_key,
            transaction_count, total_quantity, total_amount
        )
        SELECT 
            date_key,
            customer_key,
            product_key,
            COUNT(*) as transaction_count,
            SUM(quantity) as total_quantity,
            SUM(total_amount) as total_amount
        FROM {source_fact_table}
        WHERE date_key = %s
        GROUP BY date_key, customer_key, product_key
        """
        
        cursor = self.conn.cursor()
        cursor.execute(agg_sql, (self.get_yesterday_key(),))
        self.conn.commit()
    
    def create_rolling_aggregates(self, fact_table, window_days=30):
        """Create rolling window aggregates"""
        rolling_sql = f"""
        SELECT 
            customer_key,
            date_key,
            SUM(total_amount) OVER (
                PARTITION BY customer_key 
                ORDER BY date_key 
                ROWS BETWEEN {window_days-1} PRECEDING AND CURRENT ROW
            ) as rolling_{window_days}day_amount,
            AVG(total_amount) OVER (
                PARTITION BY customer_key 
                ORDER BY date_key 
                ROWS BETWEEN {window_days-1} PRECEDING AND CURRENT ROW
            ) as avg_{window_days}day_amount
        FROM {fact_table}
        """
        
        return pd.read_sql(rolling_sql, self.conn)
```

## 🎯 Best Practices

### Fact Table Design
- Choose appropriate grain (level of detail)
- Use consistent measure definitions
- Implement proper indexing strategy
- Consider partitioning for large tables
- Design for common query patterns

### Performance Optimization
```sql
-- Partitioning by date
CREATE TABLE fact_sales_partitioned (
    sale_id INT,
    date_key INT,
    customer_key INT,
    total_amount DECIMAL(15,2)
) PARTITION BY RANGE (date_key) (
    PARTITION p2023 VALUES LESS THAN (20240101),
    PARTITION p2024 VALUES LESS THAN (20250101)
);

-- Covering indexes for common queries
CREATE INDEX idx_fact_sales_customer_date 
ON fact_sales (customer_key, date_key) 
INCLUDE (total_amount, quantity);
```

## 🎯 Use Cases
- Sales and revenue analysis
- Inventory management
- Financial reporting
- Customer behavior tracking
- Operational metrics
- Performance monitoring

## ⚠️ Considerations
- Storage requirements for detailed facts
- ETL complexity for different fact types
- Query performance optimization needs
- Data freshness requirements
- Aggregation strategy planning