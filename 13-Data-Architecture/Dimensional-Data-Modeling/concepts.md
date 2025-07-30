# Dimensional Data Modeling - Core Concepts

## Overview
Dimensional modeling is a data warehouse design technique that structures data to support analytical queries and business intelligence. It organizes data into facts and dimensions to optimize query performance and user understanding.

## Key Concepts

### 1. Fact Tables
**Definition**: Central tables containing quantitative, measurable business data (metrics/measures).

**Characteristics**:
- Contains foreign keys to dimension tables
- Stores numerical measures (sales amount, quantity, etc.)
- Represents business events or transactions
- Typically has many rows (millions to billions)
- Optimized for aggregation queries

**Types of Facts**:

#### Additive Facts
Can be summed across all dimensions
```sql
-- Sales amount can be summed across time, product, customer
SELECT 
    SUM(sales_amount) as total_sales
FROM fact_sales
WHERE date_key BETWEEN '20240101' AND '20240131';
```

#### Semi-Additive Facts
Can be summed across some dimensions but not others
```sql
-- Account balance can be summed across accounts but not time
SELECT 
    customer_key,
    AVG(account_balance) as avg_balance  -- Average over time
FROM fact_account_balance
GROUP BY customer_key;
```

#### Non-Additive Facts
Cannot be meaningfully summed
```sql
-- Ratios, percentages, temperatures
SELECT 
    AVG(profit_margin_percent) as avg_margin  -- Must use average
FROM fact_sales;
```

### 2. Dimension Tables
**Definition**: Descriptive tables containing attributes that provide context to facts.

**Characteristics**:
- Contains descriptive attributes (names, descriptions, categories)
- Relatively few rows compared to fact tables
- Wide tables with many columns
- Used for filtering, grouping, and labeling

**Example Dimension Structure**:
```sql
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,        -- Surrogate key
    product_id VARCHAR(50),             -- Natural key
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    color VARCHAR(50),
    size VARCHAR(20),
    unit_cost DECIMAL(10,2),
    created_date DATE,
    modified_date DATE,
    is_active BOOLEAN
);
```

### 3. Schema Types

#### Star Schema
**Structure**: Fact table at center, dimension tables directly connected
**Advantages**: Simple, fast queries, easy to understand
**Disadvantages**: Data redundancy in dimensions

```sql
-- Star Schema Example
-- Fact table connects directly to all dimensions
SELECT 
    d.date_name,
    p.product_name,
    c.customer_name,
    SUM(f.sales_amount) as total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY d.date_name, p.product_name, c.customer_name;
```

#### Snowflake Schema
**Structure**: Normalized dimensions with hierarchical relationships
**Advantages**: Reduced storage, no redundancy
**Disadvantages**: More complex queries, more joins

```sql
-- Snowflake Schema Example
-- Product dimension normalized into category hierarchy
SELECT 
    d.date_name,
    p.product_name,
    cat.category_name,
    subcat.subcategory_name,
    SUM(f.sales_amount) as total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_category cat ON p.category_key = cat.category_key
JOIN dim_subcategory subcat ON cat.subcategory_key = subcat.subcategory_key
GROUP BY d.date_name, p.product_name, cat.category_name, subcat.subcategory_name;
```

#### Galaxy Schema (Fact Constellation)
**Structure**: Multiple fact tables sharing dimension tables
**Use Case**: Complex business processes with multiple subject areas

### 4. Surrogate Keys
**Definition**: System-generated unique identifiers for dimension records.

**Benefits**:
- Performance optimization (integer keys)
- Handle changing natural keys
- Support slowly changing dimensions
- Isolate data warehouse from source system changes

```sql
-- Surrogate key implementation
CREATE TABLE dim_customer (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,  -- Surrogate key
    customer_id VARCHAR(50),                     -- Natural key
    customer_name VARCHAR(200),
    -- Other attributes
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
);
```

### 5. Slowly Changing Dimensions (SCD)

#### Type 0: Retain Original
Never change the attribute value
```sql
-- Original value preserved forever
UPDATE dim_customer 
SET customer_name = 'New Name'  -- This would never happen
WHERE customer_key = 123;
```

#### Type 1: Overwrite
Replace old value with new value
```sql
-- Simple overwrite - loses history
UPDATE dim_customer 
SET 
    customer_address = 'New Address',
    modified_date = CURRENT_DATE
WHERE customer_id = 'CUST001';
```

#### Type 2: Add New Record
Create new record for changed attributes
```sql
-- Close current record
UPDATE dim_customer 
SET 
    expiry_date = CURRENT_DATE - 1,
    is_current = FALSE
WHERE customer_id = 'CUST001' AND is_current = TRUE;

-- Insert new record
INSERT INTO dim_customer (
    customer_id, customer_name, customer_address,
    effective_date, expiry_date, is_current
) VALUES (
    'CUST001', 'John Smith', 'New Address',
    CURRENT_DATE, '9999-12-31', TRUE
);
```

#### Type 3: Add New Attribute
Add column to track previous value
```sql
ALTER TABLE dim_customer 
ADD COLUMN previous_address VARCHAR(500);

UPDATE dim_customer 
SET 
    previous_address = customer_address,
    customer_address = 'New Address'
WHERE customer_id = 'CUST001';
```

### 6. Grain Definition
**Definition**: The level of detail stored in a fact table.

**Importance**:
- Determines what questions can be answered
- Affects storage requirements
- Impacts query performance

**Examples**:
```sql
-- Daily grain
CREATE TABLE fact_sales_daily (
    date_key INT,
    product_key INT,
    store_key INT,
    daily_sales_amount DECIMAL(12,2),
    daily_quantity_sold INT
);

-- Transaction grain (more detailed)
CREATE TABLE fact_sales_transaction (
    transaction_id VARCHAR(50),
    date_key INT,
    time_key INT,
    product_key INT,
    store_key INT,
    customer_key INT,
    sales_amount DECIMAL(10,2),
    quantity INT,
    discount_amount DECIMAL(8,2)
);
```

### 7. Conformed Dimensions
**Definition**: Dimensions shared across multiple fact tables with identical structure and content.

**Benefits**:
- Consistent reporting across business processes
- Drill-across queries possible
- Reduced development and maintenance

```sql
-- Conformed date dimension used by multiple facts
-- fact_sales, fact_inventory, fact_budget all use same dim_date

SELECT 
    d.fiscal_year,
    d.fiscal_quarter,
    SUM(s.sales_amount) as total_sales,
    SUM(i.inventory_value) as total_inventory
FROM dim_date d
LEFT JOIN fact_sales s ON d.date_key = s.date_key
LEFT JOIN fact_inventory i ON d.date_key = i.date_key
GROUP BY d.fiscal_year, d.fiscal_quarter;
```

### 8. Junk Dimensions
**Definition**: Dimension containing miscellaneous low-cardinality flags and indicators.

**Purpose**: Avoid cluttering fact table with many flag columns

```sql
-- Instead of multiple flag columns in fact table
CREATE TABLE dim_transaction_flags (
    transaction_flag_key INT PRIMARY KEY,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    is_promotion BOOLEAN,
    payment_method VARCHAR(20),
    transaction_type VARCHAR(30)
);

-- Fact table references single junk dimension
CREATE TABLE fact_sales (
    transaction_id VARCHAR(50),
    date_key INT,
    product_key INT,
    customer_key INT,
    transaction_flag_key INT,  -- References junk dimension
    sales_amount DECIMAL(10,2)
);
```

### 9. Degenerate Dimensions
**Definition**: Dimension attributes stored directly in the fact table (no separate dimension table).

**Common Examples**: Transaction numbers, order numbers, invoice numbers

```sql
CREATE TABLE fact_order_line (
    order_number VARCHAR(50),      -- Degenerate dimension
    line_number INT,               -- Degenerate dimension
    date_key INT,
    product_key INT,
    customer_key INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    line_total DECIMAL(10,2)
);
```

## Design Process

### 1. Business Process Identification
- Identify key business processes to model
- Understand business questions to be answered
- Define success metrics

### 2. Grain Declaration
- Determine the atomic level of detail
- Ensure grain supports all required analyses
- Document grain clearly

### 3. Dimension Identification
- Identify all descriptive context
- Group related attributes into dimensions
- Plan for dimension changes over time

### 4. Fact Identification
- Identify measurable business events
- Determine additive vs. non-additive facts
- Plan for different levels of summarization

## Best Practices

### 1. Design Principles
- Start with business requirements
- Keep it simple (favor star schema)
- Use meaningful names
- Document everything thoroughly

### 2. Performance Optimization
- Use appropriate indexing strategies
- Consider partitioning large fact tables
- Implement proper aggregation strategies
- Monitor and tune query performance

### 3. Data Quality
- Implement data validation rules
- Handle missing and invalid data
- Maintain referential integrity
- Regular data quality monitoring

### 4. Maintenance
- Plan for dimension changes
- Implement proper ETL processes
- Monitor data lineage
- Regular performance reviews

## Common Patterns

### 1. Date Dimension
```sql
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_week VARCHAR(10),
    day_of_month INT,
    day_of_year INT,
    week_of_year INT,
    month_name VARCHAR(10),
    month_number INT,
    quarter VARCHAR(2),
    year INT,
    fiscal_year INT,
    fiscal_quarter VARCHAR(2),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    holiday_name VARCHAR(50)
);
```

### 2. Customer Dimension with SCD Type 2
```sql
CREATE TABLE dim_customer (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    customer_address VARCHAR(500),
    customer_city VARCHAR(100),
    customer_state VARCHAR(50),
    customer_zip VARCHAR(20),
    customer_segment VARCHAR(50),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN,
    created_date TIMESTAMP,
    modified_date TIMESTAMP
);
```

### 3. Sales Fact Table
```sql
CREATE TABLE fact_sales (
    sales_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    date_key INT,
    product_key INT,
    customer_key INT,
    store_key INT,
    promotion_key INT,
    order_number VARCHAR(50),        -- Degenerate dimension
    line_number INT,                 -- Degenerate dimension
    quantity_sold INT,
    unit_price DECIMAL(8,2),
    sales_amount DECIMAL(12,2),
    cost_amount DECIMAL(12,2),
    profit_amount DECIMAL(12,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    created_timestamp TIMESTAMP
);
```