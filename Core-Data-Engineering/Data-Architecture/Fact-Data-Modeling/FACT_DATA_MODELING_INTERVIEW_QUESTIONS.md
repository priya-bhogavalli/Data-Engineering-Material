# Fact Data Modeling Interview Questions

## 📋 Table of Contents

1. [Core Concepts (1-10)](#core-concepts-1-10)
2. [Fact Table Design (11-20)](#fact-table-design-11-20)
3. [Advanced Techniques (21-30)](#advanced-techniques-21-30)

---

## Core Concepts (1-10)

### 1. What is a fact table and how does it differ from a dimension table?
**Answer**: 
- **Fact Table**: Contains measurable business events/metrics
- **Dimension Table**: Contains descriptive attributes
- **Key Differences**:
  - Facts: Numeric, additive, large volume
  - Dimensions: Textual, descriptive, smaller volume

### 2. What are the different types of facts?
**Answer**:
- **Additive**: Can be summed across all dimensions (sales amount)
- **Semi-Additive**: Can be summed across some dimensions (account balance)
- **Non-Additive**: Cannot be summed (ratios, percentages)
- **Factless**: No measures, only foreign keys (events)

### 3. Explain the grain of a fact table.
**Answer**: The grain defines the level of detail:
```sql
-- Daily sales grain
CREATE TABLE daily_sales_fact (
    date_key INT,
    product_key INT,
    store_key INT,
    sales_amount DECIMAL(10,2),
    quantity_sold INT
);

-- Transaction-level grain (more detailed)
CREATE TABLE transaction_fact (
    transaction_id VARCHAR(50),
    timestamp TIMESTAMP,
    product_key INT,
    customer_key INT,
    amount DECIMAL(10,2)
);
```

### 4. What is a factless fact table and when would you use it?
**Answer**: Contains only foreign keys, no measures:
```sql
-- Student enrollment (event tracking)
CREATE TABLE enrollment_fact (
    student_key INT,
    course_key INT,
    semester_key INT,
    enrollment_date DATE
);

-- Coverage fact (what didn't happen)
CREATE TABLE promotion_coverage_fact (
    product_key INT,
    store_key INT,
    promotion_key INT,
    date_key INT
);
```

### 5. How do you handle late-arriving facts?
**Answer**: Strategies for delayed data:
- **Grace Period**: Wait before processing
- **Reprocessing**: Update historical data
- **Separate Pipeline**: Handle late data separately
```sql
-- Track data arrival
ALTER TABLE sales_fact ADD COLUMN 
    data_arrival_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```

## Fact Table Design (11-20)

### 6. What are the different fact table types?
**Answer**:
- **Transaction**: One row per business event
- **Periodic Snapshot**: Regular intervals (daily, monthly)
- **Accumulating Snapshot**: Tracks process lifecycle
- **Consolidated**: Aggregated from detailed facts

### 7. How do you design an accumulating snapshot fact table?
**Answer**: Tracks milestones in a process:
```sql
CREATE TABLE order_lifecycle_fact (
    order_key INT PRIMARY KEY,
    customer_key INT,
    order_date DATE,
    payment_date DATE,
    ship_date DATE,
    delivery_date DATE,
    -- Measures at each stage
    order_amount DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    -- Days between milestones
    days_to_ship INT,
    days_to_deliver INT
);
```

### 8. How do you handle multiple currencies in fact tables?
**Answer**: Store both original and standardized amounts:
```sql
CREATE TABLE sales_fact (
    transaction_id VARCHAR(50),
    date_key INT,
    product_key INT,
    -- Original currency
    original_amount DECIMAL(10,2),
    original_currency_code VARCHAR(3),
    -- Standardized currency
    usd_amount DECIMAL(10,2),
    exchange_rate DECIMAL(10,6),
    rate_date DATE
);
```

### 9. What is a bridge table and when do you use it?
**Answer**: Handles many-to-many relationships:
```sql
-- Account can have multiple customers
CREATE TABLE account_customer_bridge (
    account_key INT,
    customer_key INT,
    allocation_percentage DECIMAL(5,2),
    effective_date DATE,
    expiration_date DATE
);

-- Fact table references bridge
CREATE TABLE account_balance_fact (
    account_key INT,
    date_key INT,
    balance_amount DECIMAL(15,2)
);
```

### 10. How do you implement slowly changing dimensions in fact tables?
**Answer**: Use appropriate dimension keys:
```sql
-- Type 2 SCD with fact table
CREATE TABLE customer_dim (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    effective_date DATE,
    expiration_date DATE,
    current_flag BOOLEAN
);

CREATE TABLE sales_fact (
    transaction_date DATE,
    customer_key INT, -- Points to correct version
    product_key INT,
    sales_amount DECIMAL(10,2)
);
```

## Advanced Techniques (21-30)

### 11. How do you handle fact table partitioning?
**Answer**: Partition by date for performance:
```sql
-- Range partitioning by date
CREATE TABLE sales_fact (
    transaction_date DATE,
    product_key INT,
    sales_amount DECIMAL(10,2)
) PARTITION BY RANGE (transaction_date);

-- Create monthly partitions
CREATE TABLE sales_fact_2024_01 PARTITION OF sales_fact
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### 12. What are conformed facts and why are they important?
**Answer**: Facts with identical meaning across fact tables:
- **Consistent Definitions**: Same calculation logic
- **Same Grain**: Identical level of detail
- **Cross-Process Analysis**: Enable drill-across queries

### 13. How do you implement fact table aggregations?
**Answer**: Pre-calculate common summaries:
```sql
-- Detailed fact
CREATE TABLE daily_sales_fact (
    date_key INT,
    product_key INT,
    store_key INT,
    sales_amount DECIMAL(10,2)
);

-- Monthly aggregate
CREATE TABLE monthly_sales_fact (
    month_key INT,
    product_key INT,
    store_key INT,
    total_sales DECIMAL(12,2),
    avg_daily_sales DECIMAL(10,2)
);
```

### 14. How do you handle fact table updates and corrections?
**Answer**: Strategies for data corrections:
```sql
-- Audit columns
ALTER TABLE sales_fact ADD COLUMN 
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_timestamp TIMESTAMP,
    version_number INT DEFAULT 1;

-- Correction tracking
CREATE TABLE fact_corrections (
    correction_id INT PRIMARY KEY,
    table_name VARCHAR(100),
    record_key VARCHAR(500),
    correction_date TIMESTAMP,
    reason VARCHAR(500)
);
```

### 15. What is a mini-dimension and when do you use it?
**Answer**: Subset of rapidly changing dimension attributes:
```sql
-- Customer mini-dimension for frequently changing attributes
CREATE TABLE customer_mini_dim (
    customer_mini_key INT PRIMARY KEY,
    income_band VARCHAR(50),
    credit_score_range VARCHAR(50),
    age_band VARCHAR(50)
);

-- Fact table references both full and mini dimensions
CREATE TABLE sales_fact (
    customer_key INT,
    customer_mini_key INT,
    product_key INT,
    sales_amount DECIMAL(10,2)
);
```

### 16. How do you implement fact table compression?
**Answer**: Techniques to reduce storage:
- **Columnar Storage**: Store by column
- **Data Types**: Use appropriate sizes
- **Compression**: Enable table compression
```sql
-- Optimize data types
CREATE TABLE sales_fact (
    date_key INT, -- Instead of DATE
    product_key SMALLINT, -- If < 32K products
    sales_amount DECIMAL(8,2) -- Appropriate precision
) WITH (compression = 'lz4');
```

### 17. What are derived facts and how do you implement them?
**Answer**: Calculated from base facts:
```sql
-- Base facts
CREATE TABLE order_line_fact (
    order_key INT,
    product_key INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    line_total AS (quantity * unit_price) -- Derived
);

-- Aggregated derived facts
CREATE VIEW monthly_metrics AS
SELECT 
    month_key,
    SUM(sales_amount) as total_sales,
    COUNT(*) as transaction_count,
    AVG(sales_amount) as avg_transaction -- Derived
FROM daily_sales_fact
GROUP BY month_key;
```

### 18. How do you handle fact table security and privacy?
**Answer**: Implement row-level security:
```sql
-- Row-level security policy
CREATE POLICY sales_policy ON sales_fact
FOR SELECT TO sales_role
USING (region_key IN (
    SELECT region_key FROM user_regions 
    WHERE user_id = current_user
));

-- Column-level security
GRANT SELECT (date_key, product_key, quantity) 
ON sales_fact TO analyst_role;
```

### 19. What is a heterogeneous fact table?
**Answer**: Contains facts from different business processes:
```sql
CREATE TABLE financial_fact (
    date_key INT,
    account_key INT,
    transaction_type VARCHAR(20), -- 'SALE', 'REFUND', 'PAYMENT'
    -- Different measures for different types
    sales_amount DECIMAL(10,2),
    refund_amount DECIMAL(10,2),
    payment_amount DECIMAL(10,2)
);
```

### 20. How do you implement real-time fact loading?
**Answer**: Stream processing for real-time updates:
```python
# Kafka consumer for real-time facts
def process_transaction(message):
    fact_record = {
        'transaction_id': message['id'],
        'timestamp': message['timestamp'],
        'customer_key': lookup_customer_key(message['customer_id']),
        'product_key': lookup_product_key(message['product_id']),
        'amount': message['amount']
    }
    
    # Insert into fact table
    insert_fact(fact_record)
    
    # Update real-time aggregates
    update_realtime_metrics(fact_record)
```

---

## 📚 Study Guide

### Key Design Principles
1. **Grain Definition**: Clearly define the level of detail
2. **Additive Measures**: Prefer additive facts when possible
3. **Consistent Keys**: Use surrogate keys for dimensions
4. **Audit Trail**: Track data lineage and changes
5. **Performance**: Consider partitioning and indexing

### Common Patterns
- **Transaction Facts**: Detailed business events
- **Snapshot Facts**: Point-in-time measurements
- **Accumulating Facts**: Process lifecycle tracking
- **Consolidated Facts**: Pre-aggregated summaries

### Best Practices
- Keep fact tables narrow (fewer columns)
- Use appropriate data types
- Implement proper indexing strategy
- Consider compression for large tables
- Plan for data retention and archiving