# Fact Data Modeling Interview Questions

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-180)](#architecture--performance-151-180)
5. [Streaming & Real-time Processing (181-200)](#streaming--real-time-processing-181-200)
6. [Production & Operations (201-220)](#production--operations-201-220)
7. [Scenario-Based Questions (221-250)](#scenario-based-questions-221-250)

---

## Basic Level Questions (1-50)

### 1. What is a fact table and how does it differ from a dimension table?
**Answer**: 
- **Fact Table**: Contains measurable business events/metrics with foreign keys to dimensions
- **Dimension Table**: Contains descriptive attributes for analysis context
- **Key Differences**:
  - Facts: Numeric, additive, large volume, narrow tables
  - Dimensions: Textual, descriptive, smaller volume, wide tables

### 2. What are the different types of facts?
**Answer**:
- **Additive**: Can be summed across all dimensions (sales amount, quantity)
- **Semi-Additive**: Can be summed across some dimensions (account balance - not across time)
- **Non-Additive**: Cannot be summed (ratios, percentages, temperatures)
- **Factless**: No measures, only foreign keys (events, coverage)

### 3. Explain the grain of a fact table.
**Answer**: The grain defines the level of detail stored in the fact table.
```sql
-- Transaction grain (most detailed)
CREATE TABLE transaction_fact (
    transaction_id VARCHAR(50),
    timestamp TIMESTAMP,
    customer_key INT,
    product_key INT,
    amount DECIMAL(10,2)
);

-- Daily grain (aggregated)
CREATE TABLE daily_sales_fact (
    date_key INT,
    customer_key INT,
    product_key INT,
    daily_sales_amount DECIMAL(12,2),
    transaction_count INT
);
```

### 4. What is a factless fact table and when would you use it?
**Answer**: Contains only foreign keys, no measures. Used for:
- **Event Tracking**: Student enrollment, employee attendance
- **Coverage Analysis**: What products were promoted in which stores
```sql
-- Student enrollment factless fact
CREATE TABLE enrollment_fact (
    student_key INT,
    course_key INT,
    semester_key INT,
    enrollment_date DATE
);
```

### 5. How do you handle late-arriving facts?
**Answer**: Strategies for delayed data:
- **Grace Period**: Wait before processing final aggregations
- **Reprocessing**: Update historical data when late facts arrive
- **Separate Pipeline**: Handle late data in dedicated process
```sql
-- Track data arrival
ALTER TABLE sales_fact ADD COLUMN 
    data_arrival_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```

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
    order_amount DECIMAL(10,2),
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
    original_amount DECIMAL(10,2),
    original_currency_code VARCHAR(3),
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
```

### 10. How do you implement slowly changing dimensions in fact tables?
**Answer**: Use appropriate dimension keys:
```sql
CREATE TABLE sales_fact (
    transaction_date DATE,
    customer_key INT, -- Points to correct SCD version
    product_key INT,
    sales_amount DECIMAL(10,2)
);
```

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
```

### 15. What is a mini-dimension and when do you use it?
**Answer**: Subset of rapidly changing dimension attributes:
```sql
-- Customer mini-dimension
CREATE TABLE customer_mini_dim (
    customer_mini_key INT PRIMARY KEY,
    income_band VARCHAR(50),
    credit_score_range VARCHAR(50),
    age_band VARCHAR(50)
);

-- Fact table references both dimensions
CREATE TABLE sales_fact (
    customer_key INT,
    customer_mini_key INT,
    product_key INT,
    sales_amount DECIMAL(10,2)
);
```

### 16. How do you implement fact table compression?
**Answer**: Techniques to reduce storage:
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
-- Base facts with derived column
CREATE TABLE order_line_fact (
    order_key INT,
    product_key INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    line_total AS (quantity * unit_price) -- Derived
);
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
```

### 19. What is a heterogeneous fact table?
**Answer**: Contains facts from different business processes:
```sql
CREATE TABLE financial_fact (
    date_key INT,
    account_key INT,
    transaction_type VARCHAR(20), -- 'SALE', 'REFUND', 'PAYMENT'
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
        'date_key': get_date_key(message['timestamp']),
        'customer_key': lookup_customer_key(message['customer_id']),
        'amount': message['amount']
    }
    insert_fact_record(fact_record)
```

### 21. How do you handle fact table indexing?
**Answer**: Create indexes on foreign keys and frequently filtered columns:
```sql
-- Primary indexes
CREATE INDEX idx_sales_fact_date ON sales_fact(date_key);
CREATE INDEX idx_sales_fact_customer ON sales_fact(customer_key);
CREATE INDEX idx_sales_fact_product ON sales_fact(product_key);

-- Composite index for common queries
CREATE INDEX idx_sales_fact_date_customer ON sales_fact(date_key, customer_key);
```

### 22. What is fact table normalization and when do you use it?
**Answer**: Breaking down facts into multiple related tables:
```sql
-- Normalized approach
CREATE TABLE order_header_fact (
    order_key INT PRIMARY KEY,
    customer_key INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_line_fact (
    order_line_key INT PRIMARY KEY,
    order_key INT,
    product_key INT,
    quantity INT,
    line_amount DECIMAL(10,2)
);
```

### 23. How do you implement fact table versioning?
**Answer**: Track changes over time:
```sql
CREATE TABLE sales_fact_versioned (
    fact_key BIGINT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    sales_amount DECIMAL(10,2),
    version_number INT,
    effective_date TIMESTAMP,
    expiration_date TIMESTAMP,
    current_flag BOOLEAN
);
```

### 24. What are transaction fact tables?
**Answer**: Store individual business transactions:
```sql
CREATE TABLE transaction_fact (
    transaction_key BIGINT PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE,
    timestamp TIMESTAMP,
    customer_key INT,
    product_key INT,
    transaction_amount DECIMAL(10,2),
    payment_method VARCHAR(20)
);
```

### 25. How do you handle fact table deduplication?
**Answer**: Prevent duplicate fact records:
```sql
-- Unique constraint on business key
ALTER TABLE sales_fact ADD CONSTRAINT uk_sales_fact 
UNIQUE (transaction_id, date_key, customer_key);

-- Deduplication query
WITH deduplicated AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY transaction_id 
        ORDER BY created_timestamp DESC
    ) as rn
    FROM sales_fact
)
SELECT * FROM deduplicated WHERE rn = 1;
```

### 26. What is a periodic snapshot fact table?
**Answer**: Regular snapshots at specific intervals:
```sql
CREATE TABLE monthly_account_snapshot (
    snapshot_date DATE,
    account_key INT,
    beginning_balance DECIMAL(15,2),
    ending_balance DECIMAL(15,2),
    average_balance DECIMAL(15,2),
    transaction_count INT,
    PRIMARY KEY (snapshot_date, account_key)
);
```

### 27. How do you implement fact table archiving?
**Answer**: Move old data to archive tables:
```sql
-- Archive old data
CREATE TABLE sales_fact_archive AS
SELECT * FROM sales_fact 
WHERE date_key < 20230101;

-- Delete archived data from main table
DELETE FROM sales_fact 
WHERE date_key < 20230101;
```

### 28. What are consolidated fact tables?
**Answer**: Pre-aggregated facts for performance:
```sql
-- Consolidated monthly facts
CREATE TABLE monthly_sales_consolidated AS
SELECT 
    DATE_TRUNC('month', transaction_date) as month,
    customer_key,
    product_key,
    SUM(sales_amount) as total_sales,
    COUNT(*) as transaction_count,
    AVG(sales_amount) as avg_transaction
FROM daily_sales_fact
GROUP BY month, customer_key, product_key;
```

### 29. How do you handle fact table data quality?
**Answer**: Implement validation rules:
```sql
-- Data quality constraints
ALTER TABLE sales_fact ADD CONSTRAINT chk_sales_amount 
CHECK (sales_amount >= 0);

ALTER TABLE sales_fact ADD CONSTRAINT chk_quantity 
CHECK (quantity > 0);

-- Referential integrity
ALTER TABLE sales_fact ADD CONSTRAINT fk_customer 
FOREIGN KEY (customer_key) REFERENCES customer_dim(customer_key);
```

### 30. What is fact table lineage and how do you track it?
**Answer**: Track data flow and transformations:
```sql
-- Lineage tracking table
CREATE TABLE fact_lineage (
    lineage_id BIGINT PRIMARY KEY,
    source_system VARCHAR(100),
    target_table VARCHAR(100),
    transformation_logic TEXT,
    load_timestamp TIMESTAMP,
    record_count BIGINT
);
```

### 31. How do you implement fact table surrogate keys?
**Answer**: Use system-generated keys for fact records:
```sql
CREATE TABLE sales_fact (
    sales_fact_key BIGINT IDENTITY(1,1) PRIMARY KEY, -- Surrogate key
    transaction_id VARCHAR(50), -- Business key
    date_key INT,
    customer_key INT,
    sales_amount DECIMAL(10,2)
);
```

### 32. What is fact table granularity and how do you determine it?
**Answer**: Level of detail based on business requirements:
- **Transaction Level**: Most detailed, largest volume
- **Daily Level**: Aggregated by day, moderate volume
- **Monthly Level**: Highly aggregated, smallest volume

### 33. How do you handle fact table null values?
**Answer**: Strategies for missing measures:
```sql
-- Use default values
CREATE TABLE sales_fact (
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    sales_amount DECIMAL(10,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0
);

-- Separate null indicator
ALTER TABLE sales_fact ADD COLUMN 
    sales_amount_null_flag BOOLEAN DEFAULT FALSE;
```

### 34. What are additive, semi-additive, and non-additive measures?
**Answer**: Different aggregation behaviors:
```sql
-- Additive: Can sum across all dimensions
SUM(sales_amount) -- Valid across time, customer, product

-- Semi-additive: Can sum across some dimensions
SUM(account_balance) -- Valid across accounts, NOT across time

-- Non-additive: Cannot sum
AVG(temperature) -- Must recalculate, not sum averages
```

### 35. How do you implement fact table change data capture?
**Answer**: Track changes to fact records:
```sql
CREATE TABLE sales_fact_cdc (
    cdc_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    operation_type CHAR(1), -- I, U, D
    transaction_id VARCHAR(50),
    old_sales_amount DECIMAL(10,2),
    new_sales_amount DECIMAL(10,2),
    change_timestamp TIMESTAMP
);
```

### 36. What is a junk dimension and how does it relate to facts?
**Answer**: Combines low-cardinality attributes:
```sql
-- Junk dimension
CREATE TABLE transaction_junk_dim (
    junk_key INT PRIMARY KEY,
    payment_method VARCHAR(20),
    shipping_method VARCHAR(20),
    promotion_flag BOOLEAN,
    gift_wrap_flag BOOLEAN
);

-- Fact table reference
CREATE TABLE sales_fact (
    date_key INT,
    customer_key INT,
    product_key INT,
    transaction_junk_key INT, -- Reference to junk dimension
    sales_amount DECIMAL(10,2)
);
```

### 37. How do you handle fact table performance optimization?
**Answer**: Multiple optimization techniques:
```sql
-- Partitioning
CREATE TABLE sales_fact (
    date_key INT,
    sales_amount DECIMAL(10,2)
) PARTITION BY RANGE (date_key);

-- Columnstore index (SQL Server)
CREATE COLUMNSTORE INDEX cci_sales_fact ON sales_fact;

-- Distribution key (Redshift)
CREATE TABLE sales_fact (
    customer_key INT DISTKEY,
    sales_amount DECIMAL(10,2)
) SORTKEY (date_key);
```

### 38. What is fact table drill-across and how do you implement it?
**Answer**: Query multiple fact tables with conformed dimensions:
```sql
-- Sales and inventory facts with conformed dimensions
SELECT 
    d.month,
    p.category,
    s.total_sales,
    i.avg_inventory
FROM (
    SELECT date_key, product_key, SUM(sales_amount) as total_sales
    FROM sales_fact GROUP BY date_key, product_key
) s
FULL OUTER JOIN (
    SELECT date_key, product_key, AVG(inventory_level) as avg_inventory
    FROM inventory_fact GROUP BY date_key, product_key
) i ON s.date_key = i.date_key AND s.product_key = i.product_key
JOIN date_dim d ON COALESCE(s.date_key, i.date_key) = d.date_key
JOIN product_dim p ON COALESCE(s.product_key, i.product_key) = p.product_key;
```

### 39. How do you implement fact table error handling?
**Answer**: Comprehensive error management:
```sql
-- Error logging table
CREATE TABLE fact_load_errors (
    error_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    source_record TEXT,
    error_message VARCHAR(500),
    error_timestamp TIMESTAMP,
    table_name VARCHAR(100)
);

-- Reject table for invalid records
CREATE TABLE sales_fact_rejects (
    reject_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    transaction_id VARCHAR(50),
    reject_reason VARCHAR(200),
    reject_timestamp TIMESTAMP,
    raw_data TEXT
);
```

### 40. What are fact table design patterns?
**Answer**: Common design approaches:
- **Star Schema**: Fact table surrounded by dimension tables
- **Snowflake Schema**: Normalized dimension tables
- **Galaxy Schema**: Multiple fact tables sharing dimensions
- **Fact Constellation**: Complex multi-fact environment

### 41. How do you handle fact table temporal data?
**Answer**: Manage time-based fact data:
```sql
CREATE TABLE temporal_sales_fact (
    transaction_id VARCHAR(50),
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    transaction_time TIMESTAMP,
    customer_key INT,
    sales_amount DECIMAL(10,2)
);
```

### 42. What is fact table denormalization?
**Answer**: Include dimension attributes in fact table:
```sql
-- Denormalized fact table
CREATE TABLE denormalized_sales_fact (
    date_key INT,
    customer_key INT,
    customer_name VARCHAR(100), -- Denormalized
    customer_city VARCHAR(50),  -- Denormalized
    product_key INT,
    product_name VARCHAR(100),  -- Denormalized
    sales_amount DECIMAL(10,2)
);
```

### 43. How do you implement fact table data validation?
**Answer**: Ensure data integrity:
```sql
-- Validation rules
CREATE OR REPLACE FUNCTION validate_sales_fact()
RETURNS TRIGGER AS $$
BEGIN
    -- Check amount is positive
    IF NEW.sales_amount < 0 THEN
        RAISE EXCEPTION 'Sales amount cannot be negative';
    END IF;
    
    -- Check foreign key exists
    IF NOT EXISTS (SELECT 1 FROM customer_dim WHERE customer_key = NEW.customer_key) THEN
        RAISE EXCEPTION 'Invalid customer key';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 44. What are fact table loading strategies?
**Answer**: Different approaches to load data:
- **Full Load**: Complete refresh of fact table
- **Incremental Load**: Only new/changed records
- **Delta Load**: Based on change timestamps
- **Merge Load**: Upsert operations

### 45. How do you handle fact table referential integrity?
**Answer**: Maintain relationships with dimensions:
```sql
-- Foreign key constraints
ALTER TABLE sales_fact 
ADD CONSTRAINT fk_sales_date 
FOREIGN KEY (date_key) REFERENCES date_dim(date_key);

ALTER TABLE sales_fact 
ADD CONSTRAINT fk_sales_customer 
FOREIGN KEY (customer_key) REFERENCES customer_dim(customer_key);
```

### 46. What is fact table metadata management?
**Answer**: Track fact table information:
```sql
CREATE TABLE fact_metadata (
    table_name VARCHAR(100) PRIMARY KEY,
    grain_description TEXT,
    load_frequency VARCHAR(50),
    retention_period INT,
    business_owner VARCHAR(100),
    last_updated TIMESTAMP
);
```

### 47. How do you implement fact table monitoring?
**Answer**: Track fact table health:
```sql
-- Monitoring metrics
CREATE TABLE fact_monitoring (
    monitor_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    table_name VARCHAR(100),
    record_count BIGINT,
    load_duration_seconds INT,
    data_quality_score DECIMAL(5,2),
    monitor_timestamp TIMESTAMP
);
```

### 48. What are fact table business rules?
**Answer**: Implement domain-specific logic:
```sql
-- Business rule: Sales amount must match line items
CREATE VIEW validated_sales_fact AS
SELECT s.*
FROM sales_fact s
WHERE s.total_amount = (
    SELECT SUM(line_amount)
    FROM order_line_fact ol
    WHERE ol.order_key = s.order_key
);
```

### 49. How do you handle fact table scalability?
**Answer**: Design for growth:
```sql
-- Horizontal partitioning
CREATE TABLE sales_fact_2024_q1 (
    LIKE sales_fact INCLUDING ALL,
    CHECK (date_key >= 20240101 AND date_key < 20240401)
) INHERITS (sales_fact);

-- Vertical partitioning
CREATE TABLE sales_fact_measures (
    fact_key BIGINT PRIMARY KEY,
    sales_amount DECIMAL(10,2),
    cost_amount DECIMAL(10,2)
);
```

### 50. What is fact table documentation?
**Answer**: Comprehensive documentation strategy:
```sql
-- Table comments
COMMENT ON TABLE sales_fact IS 'Daily sales transactions at line item level';
COMMENT ON COLUMN sales_fact.sales_amount IS 'Net sales amount in USD';
COMMENT ON COLUMN sales_fact.date_key IS 'Foreign key to date dimension';

-- Data dictionary
CREATE TABLE fact_data_dictionary (
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    data_type VARCHAR(50),
    business_definition TEXT,
    calculation_logic TEXT
);
```

---

## Intermediate Level Questions (51-100)
