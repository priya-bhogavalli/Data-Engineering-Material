# Applying Analytical Patterns Key Concepts

## 🎯 What are Analytical Patterns?
Reusable design templates that solve common data analysis and reporting problems in data warehousing and analytics.

## 🏗️ Core Analytical Patterns

### 1. Slowly Changing Dimensions (SCD)
```sql
-- Type 2 SCD: Track historical changes
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT,
    name VARCHAR(100),
    address VARCHAR(200),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
);

-- Insert new version when customer moves
INSERT INTO dim_customer (customer_id, name, address, effective_date, expiry_date, is_current)
VALUES (123, 'John Doe', 'New Address', CURRENT_DATE, '9999-12-31', TRUE);

-- Expire old version
UPDATE dim_customer 
SET expiry_date = CURRENT_DATE - 1, is_current = FALSE
WHERE customer_id = 123 AND is_current = TRUE;
```

### 2. Factless Fact Tables
```sql
-- Event tracking without measures
CREATE TABLE fact_student_attendance (
    student_key INT,
    date_key INT,
    class_key INT,
    attendance_type_key INT,
    PRIMARY KEY (student_key, date_key, class_key)
);
```

### 3. Accumulating Snapshot
```sql
-- Order lifecycle tracking
CREATE TABLE fact_order_snapshot (
    order_key INT PRIMARY KEY,
    customer_key INT,
    order_date_key INT,
    payment_date_key INT,
    ship_date_key INT,
    delivery_date_key INT,
    order_amount DECIMAL(10,2),
    days_to_ship INT,
    days_to_deliver INT
);
```

## 📊 Advanced Patterns

### Bridge Tables
```sql
-- Many-to-many relationships
CREATE TABLE bridge_account_customer (
    account_key INT,
    customer_key INT,
    allocation_percentage DECIMAL(5,2),
    effective_date DATE
);
```

### Hierarchy Flattening
```sql
-- Product hierarchy in dimension
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_code VARCHAR(20),
    product_name VARCHAR(100),
    subcategory VARCHAR(50),
    category VARCHAR(50),
    department VARCHAR(50),
    level_1_rollup VARCHAR(50),
    level_2_rollup VARCHAR(50)
);
```

### Conformed Dimensions
```sql
-- Shared dimension across fact tables
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_name VARCHAR(10),
    month_name VARCHAR(10),
    quarter INT,
    year INT,
    fiscal_year INT,
    is_holiday BOOLEAN
);

-- Used by multiple fact tables
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    -- other columns
);

CREATE TABLE fact_inventory (
    inventory_id INT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    -- other columns
);
```

## 🔧 Implementation Patterns

### Python Implementation
```python
import pandas as pd
from datetime import datetime, timedelta

class AnalyticalPatterns:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def implement_scd_type2(self, source_df, dim_table, business_key, compare_cols):
        """Implement SCD Type 2 pattern"""
        # Get current dimension data
        current_sql = f"SELECT * FROM {dim_table} WHERE is_current = TRUE"
        current_dim = pd.read_sql(current_sql, self.conn)
        
        # Identify changes
        changes = []
        for _, source_row in source_df.iterrows():
            current_row = current_dim[current_dim[business_key] == source_row[business_key]]
            
            if not current_row.empty:
                # Check if any tracked columns changed
                for col in compare_cols:
                    if current_row.iloc[0][col] != source_row[col]:
                        changes.append(source_row[business_key])
                        break
        
        if changes:
            # Expire changed records
            expire_sql = f"""
            UPDATE {dim_table} 
            SET expiry_date = %s, is_current = FALSE 
            WHERE {business_key} IN ({','.join(['%s'] * len(changes))}) 
            AND is_current = TRUE
            """
            
            cursor = self.conn.cursor()
            cursor.execute(expire_sql, [datetime.now().date()] + changes)
            
            # Insert new versions
            new_records = source_df[source_df[business_key].isin(changes)].copy()
            new_records['effective_date'] = datetime.now().date()
            new_records['expiry_date'] = datetime(9999, 12, 31).date()
            new_records['is_current'] = True
            
            new_records.to_sql(dim_table, self.conn, if_exists='append', index=False)
    
    def create_accumulating_snapshot(self, order_events_df):
        """Create accumulating snapshot fact table"""
        # Group events by order
        snapshot_data = []
        
        for order_id, events in order_events_df.groupby('order_id'):
            snapshot = {'order_id': order_id}
            
            # Extract milestone dates
            for _, event in events.iterrows():
                if event['event_type'] == 'ORDER_PLACED':
                    snapshot['order_date'] = event['event_date']
                elif event['event_type'] == 'PAYMENT_RECEIVED':
                    snapshot['payment_date'] = event['event_date']
                elif event['event_type'] == 'SHIPPED':
                    snapshot['ship_date'] = event['event_date']
                elif event['event_type'] == 'DELIVERED':
                    snapshot['delivery_date'] = event['event_date']
            
            # Calculate durations
            if 'order_date' in snapshot and 'ship_date' in snapshot:
                snapshot['days_to_ship'] = (snapshot['ship_date'] - snapshot['order_date']).days
            
            if 'ship_date' in snapshot and 'delivery_date' in snapshot:
                snapshot['days_to_deliver'] = (snapshot['delivery_date'] - snapshot['ship_date']).days
            
            snapshot_data.append(snapshot)
        
        return pd.DataFrame(snapshot_data)
    
    def implement_bridge_table(self, many_to_many_df, group_col, item_col):
        """Implement bridge table pattern for many-to-many relationships"""
        # Create bridge table with allocation percentages
        bridge_data = []
        
        for group_id, items in many_to_many_df.groupby(group_col):
            total_items = len(items)
            allocation = 1.0 / total_items  # Equal allocation
            
            for _, item in items.iterrows():
                bridge_data.append({
                    f'{group_col}_key': group_id,
                    f'{item_col}_key': item[item_col],
                    'allocation_percentage': allocation,
                    'effective_date': datetime.now().date()
                })
        
        return pd.DataFrame(bridge_data)
```

### Time-Based Patterns
```sql
-- Periodic snapshot pattern
CREATE TABLE fact_account_balance_monthly (
    account_key INT,
    date_key INT,
    balance_amount DECIMAL(15,2),
    transaction_count INT,
    PRIMARY KEY (account_key, date_key)
);

-- Transaction fact pattern
CREATE TABLE fact_transactions (
    transaction_key INT PRIMARY KEY,
    account_key INT,
    date_key INT,
    time_key INT,
    transaction_type_key INT,
    amount DECIMAL(15,2),
    running_balance DECIMAL(15,2)
);
```

## 🎯 Pattern Selection Guide

### When to Use Each Pattern

| Pattern | Use Case | Benefits | Considerations |
|---------|----------|----------|----------------|
| SCD Type 1 | Current state only | Simple, less storage | Loses history |
| SCD Type 2 | Historical tracking | Full audit trail | More complex, more storage |
| Factless Facts | Event tracking | Captures occurrences | No numeric measures |
| Accumulating Snapshot | Process milestones | Shows process flow | Complex updates |
| Bridge Tables | Many-to-many | Handles complex relationships | Query complexity |

### Implementation Decision Tree
```python
def choose_analytical_pattern(requirements):
    """Decision tree for pattern selection"""
    if requirements['track_history']:
        if requirements['storage_sensitive']:
            return "SCD_TYPE_1"
        else:
            return "SCD_TYPE_2"
    
    if requirements['many_to_many_relationships']:
        return "BRIDGE_TABLE"
    
    if requirements['process_tracking']:
        return "ACCUMULATING_SNAPSHOT"
    
    if requirements['event_tracking'] and not requirements['measures']:
        return "FACTLESS_FACT"
    
    return "STANDARD_DIMENSIONAL"
```

## 🎯 Use Cases
- Customer behavior analysis
- Sales performance tracking
- Inventory management
- Financial reporting
- Operational metrics
- Process optimization

## 🔧 Implementation Best Practices
- Choose appropriate SCD types based on business needs
- Design for query performance
- Maintain referential integrity
- Document business rules clearly
- Test data quality thoroughly
- Monitor pattern performance
- Consider storage implications