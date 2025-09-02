# Dimensional Data Modeling Interview Questions & Answers

## Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Star Schema vs Snowflake Schema](#star-schema-vs-snowflake-schema)
3. [Fact Tables](#fact-tables)
4. [Dimension Tables](#dimension-tables)
5. [Slowly Changing Dimensions (SCD)](#slowly-changing-dimensions-scd)
6. [Advanced Modeling Techniques](#advanced-modeling-techniques)
7. [Performance & Optimization](#performance--optimization)

---

## Basic Concepts

### 1. What is dimensional data modeling and why is it important?

**Answer:**
Dimensional data modeling is a design technique for structuring data warehouses that organizes data into facts and dimensions to support analytical queries and business intelligence.

**Key Benefits:**
- **Query Performance**: Optimized for analytical queries
- **User-Friendly**: Intuitive structure for business users
- **Flexibility**: Easy to add new dimensions and facts
- **Aggregation**: Supports efficient summarization
- **Historical Tracking**: Maintains historical data effectively

**Core Components:**
- **Fact Tables**: Store measurable business events
- **Dimension Tables**: Store descriptive attributes
- **Star Schema**: Central fact table surrounded by dimensions
- **Snowflake Schema**: Normalized dimension tables

### 2. What are the key differences between OLTP and OLAP systems?

**Answer:**

| Aspect | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
|--------|-------------------------------------|-------------------------------------|
| **Purpose** | Day-to-day operations | Analysis and reporting |
| **Data Model** | Normalized (3NF) | Dimensional (Star/Snowflake) |
| **Query Type** | Simple, frequent transactions | Complex analytical queries |
| **Data Volume** | Current data | Historical data |
| **Users** | Many concurrent users | Fewer analytical users |
| **Response Time** | Sub-second | Seconds to minutes |
| **Data Updates** | Frequent inserts/updates | Batch loads |

**Example:**
```sql
-- OLTP Query (Order Processing)
INSERT INTO orders (customer_id, product_id, quantity, order_date)
VALUES (12345, 67890, 2, '2024-01-15');

-- OLAP Query (Sales Analysis)
SELECT 
    d.year,
    d.quarter,
    p.category,
    SUM(f.sales_amount) as total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY d.year, d.quarter, p.category;
```

### 3. What is a business process and how does it relate to fact tables?

**Answer:**
A business process is a collection of related business activities that create value for the organization. Each business process typically corresponds to one fact table.

**Examples of Business Processes:**
- **Sales Process** → Sales Fact Table
- **Inventory Process** → Inventory Fact Table
- **Customer Service Process** → Service Fact Table
- **Marketing Process** → Campaign Fact Table

**Fact Table Design:**
```sql
-- Sales Fact Table
CREATE TABLE fact_sales (
    sales_key BIGINT PRIMARY KEY,
    date_key INT FOREIGN KEY,
    customer_key INT FOREIGN KEY,
    product_key INT FOREIGN KEY,
    store_key INT FOREIGN KEY,
    -- Measures
    quantity_sold INT,
    unit_price DECIMAL(10,2),
    sales_amount DECIMAL(12,2),
    cost_amount DECIMAL(12,2),
    profit_amount DECIMAL(12,2)
);
```

---

## Star Schema vs Snowflake Schema

### 4. Compare Star Schema and Snowflake Schema designs.

**Answer:**

**Star Schema:**
- Denormalized dimension tables
- Single table per dimension
- Faster query performance
- More storage space
- Simpler to understand

**Snowflake Schema:**
- Normalized dimension tables
- Multiple related tables per dimension
- Slower query performance
- Less storage space
- More complex structure

**Example:**

**Star Schema:**
```sql
-- Single Product Dimension Table
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category_name VARCHAR(100),
    subcategory_name VARCHAR(100),
    brand_name VARCHAR(100),
    supplier_name VARCHAR(100)
);
```

**Snowflake Schema:**
```sql
-- Normalized Product Dimension
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category_key INT FOREIGN KEY,
    brand_key INT FOREIGN KEY,
    supplier_key INT FOREIGN KEY
);

CREATE TABLE dim_category (
    category_key INT PRIMARY KEY,
    category_name VARCHAR(100),
    subcategory_name VARCHAR(100)
);

CREATE TABLE dim_brand (
    brand_key INT PRIMARY KEY,
    brand_name VARCHAR(100)
);
```

### 5. When would you choose Star Schema over Snowflake Schema?

**Answer:**

**Choose Star Schema When:**
- Query performance is critical
- Storage cost is not a major concern
- Business users need simple, intuitive structure
- Frequent ad-hoc queries are expected
- Data warehouse is primarily for reporting

**Choose Snowflake Schema When:**
- Storage optimization is important
- Data integrity and normalization are priorities
- Complex hierarchical relationships exist
- Maintenance overhead needs to be minimized
- Source systems are highly normalized

**Hybrid Approach:**
```sql
-- Partially normalized (Galaxy Schema)
-- Keep frequently queried dimensions denormalized
-- Normalize less frequently used dimensions
```

---

## Fact Tables

### 6. What are the different types of fact tables?

**Answer:**

**1. Transaction Fact Tables:**
- Store individual business transactions
- Highest level of detail
- Large volume of records

```sql
CREATE TABLE fact_sales_transaction (
    transaction_key BIGINT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    transaction_number VARCHAR(50),
    line_item_number INT,
    quantity_sold INT,
    unit_price DECIMAL(10,2),
    sales_amount DECIMAL(12,2)
);
```

**2. Periodic Snapshot Fact Tables:**
- Store regular snapshots of business state
- Fixed time intervals (daily, weekly, monthly)
- Consistent grain across time

```sql
CREATE TABLE fact_inventory_snapshot (
    snapshot_key BIGINT PRIMARY KEY,
    date_key INT,
    product_key INT,
    warehouse_key INT,
    quantity_on_hand INT,
    quantity_allocated INT,
    quantity_available INT,
    unit_cost DECIMAL(10,2),
    inventory_value DECIMAL(12,2)
);
```

**3. Accumulating Snapshot Fact Tables:**
- Track business processes with defined lifecycle
- Multiple date columns for process milestones
- Updated as process progresses

```sql
CREATE TABLE fact_order_fulfillment (
    order_key BIGINT PRIMARY KEY,
    customer_key INT,
    product_key INT,
    order_date_key INT,
    ship_date_key INT,
    delivery_date_key INT,
    order_amount DECIMAL(12,2),
    days_to_ship INT,
    days_to_deliver INT
);
```

### 7. What is grain in dimensional modeling?

**Answer:**
Grain defines the level of detail stored in a fact table - what each row represents.

**Importance:**
- Determines fact table size and performance
- Affects what questions can be answered
- Must be consistent across all measures
- Drives dimension table design

**Examples:**

**Fine Grain (Transaction Level):**
```sql
-- Each row = one line item on one order
SELECT 
    order_number,
    line_item_number,
    product_id,
    quantity,
    unit_price
FROM fact_sales_detail;
```

**Coarse Grain (Daily Summary):**
```sql
-- Each row = daily sales summary by product
SELECT 
    date_key,
    product_key,
    total_quantity,
    total_sales_amount
FROM fact_sales_daily;
```

**Grain Declaration:**
"The grain of the sales fact table is one row per product sold to a customer on a specific date at a specific store."

### 8. How do you handle different levels of granularity in fact tables?

**Answer:**

**Approach 1: Multiple Fact Tables**
```sql
-- Detailed transaction level
CREATE TABLE fact_sales_detail (
    transaction_key BIGINT,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    quantity_sold INT,
    sales_amount DECIMAL(12,2)
);

-- Daily summary level
CREATE TABLE fact_sales_daily (
    daily_key BIGINT,
    date_key INT,
    product_key INT,
    store_key INT,
    total_quantity INT,
    total_sales_amount DECIMAL(12,2),
    transaction_count INT
);
```

**Approach 2: Aggregate Tables**
```sql
-- Create materialized views for different grains
CREATE MATERIALIZED VIEW fact_sales_monthly AS
SELECT 
    DATE_TRUNC('month', d.full_date) as month_date,
    p.category_name,
    s.region_name,
    SUM(f.quantity_sold) as total_quantity,
    SUM(f.sales_amount) as total_sales
FROM fact_sales_detail f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_store s ON f.store_key = s.store_key
GROUP BY 1, 2, 3;
```

---

## Dimension Tables

### 9. What are the characteristics of a well-designed dimension table?

**Answer:**

**Key Characteristics:**
1. **Descriptive Attributes**: Rich, business-friendly descriptions
2. **Surrogate Keys**: System-generated primary keys
3. **Natural Keys**: Business keys from source systems
4. **Denormalized Structure**: Optimized for query performance
5. **Slowly Changing Dimension Support**: Historical tracking

**Example:**
```sql
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,           -- Surrogate key
    customer_id VARCHAR(50) NOT NULL,       -- Natural key
    customer_name VARCHAR(200),
    customer_type VARCHAR(50),
    birth_date DATE,
    age_range VARCHAR(20),
    gender VARCHAR(10),
    marital_status VARCHAR(20),
    education_level VARCHAR(50),
    income_range VARCHAR(30),
    address_line1 VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    phone_number VARCHAR(30),
    email_address VARCHAR(200),
    registration_date DATE,
    customer_status VARCHAR(20),
    credit_rating VARCHAR(20),
    -- SCD tracking columns
    effective_date DATE,
    expiration_date DATE,
    current_flag CHAR(1),
    row_version INT
);
```

### 10. What are surrogate keys and why are they important?

**Answer:**

**Definition:**
Surrogate keys are system-generated, meaningless identifiers used as primary keys in dimension tables.

**Benefits:**
- **Performance**: Integer keys are faster for joins
- **Stability**: Immune to business key changes
- **SCD Support**: Enable historical tracking
- **Data Integration**: Handle multiple source systems
- **Buffer Changes**: Protect from source system modifications

**Example:**
```sql
-- Without Surrogate Key (Problems)
CREATE TABLE dim_product_bad (
    product_code VARCHAR(20) PRIMARY KEY,  -- Natural key as PK
    product_name VARCHAR(200),
    category VARCHAR(100)
);

-- With Surrogate Key (Better)
CREATE TABLE dim_product_good (
    product_key INT IDENTITY(1,1) PRIMARY KEY,  -- Surrogate key
    product_code VARCHAR(20) NOT NULL,          -- Natural key
    product_name VARCHAR(200),
    category VARCHAR(100),
    UNIQUE(product_code)
);
```

**Surrogate Key Generation:**
```sql
-- Auto-increment in SQL Server
product_key INT IDENTITY(1,1)

-- Sequence in PostgreSQL
product_key INT DEFAULT nextval('product_key_seq')

-- UUID approach
product_key UUID DEFAULT gen_random_uuid()
```

---

## Slowly Changing Dimensions (SCD)

### 11. Explain the different types of Slowly Changing Dimensions.

**Answer:**

**Type 0: Retain Original**
- Never change the attribute value
- Used for fixed attributes

```sql
-- Birth date never changes
birth_date DATE  -- Always keep original value
```

**Type 1: Overwrite**
- Replace old value with new value
- No history maintained
- Used for corrections or non-critical changes

```sql
-- Update customer phone number
UPDATE dim_customer 
SET phone_number = '555-123-4567'
WHERE customer_key = 12345;
```

**Type 2: Add New Record**
- Create new record for each change
- Maintain complete history
- Most common approach

```sql
CREATE TABLE dim_customer_scd2 (
    customer_key INT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    customer_status VARCHAR(20),
    effective_date DATE,
    expiration_date DATE,
    current_flag CHAR(1)
);

-- Insert new record for status change
INSERT INTO dim_customer_scd2 (
    customer_id, customer_name, customer_status,
    effective_date, expiration_date, current_flag
) VALUES (
    'CUST001', 'John Smith', 'Premium',
    '2024-01-15', '9999-12-31', 'Y'
);

-- Update previous record
UPDATE dim_customer_scd2 
SET expiration_date = '2024-01-14', current_flag = 'N'
WHERE customer_id = 'CUST001' AND current_flag = 'Y';
```

**Type 3: Add New Attribute**
- Keep both current and previous values
- Limited history (usually just previous value)

```sql
CREATE TABLE dim_customer_scd3 (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    current_status VARCHAR(20),
    previous_status VARCHAR(20),
    status_change_date DATE
);
```

**Type 4: History Table**
- Separate table for historical records
- Current table has only active records

```sql
-- Current records
CREATE TABLE dim_customer_current (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    customer_status VARCHAR(20)
);

-- Historical records
CREATE TABLE dim_customer_history (
    customer_key INT,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    customer_status VARCHAR(20),
    effective_date DATE,
    expiration_date DATE
);
```

### 12. How do you implement SCD Type 2 processing?

**Answer:**

**ETL Process for SCD Type 2:**

```sql
-- Step 1: Identify changed records
WITH changed_records AS (
    SELECT 
        s.customer_id,
        s.customer_name,
        s.customer_status,
        d.customer_key,
        d.current_flag
    FROM staging_customer s
    LEFT JOIN dim_customer d ON s.customer_id = d.customer_id 
                              AND d.current_flag = 'Y'
    WHERE d.customer_key IS NULL  -- New records
       OR (d.customer_status != s.customer_status)  -- Changed records
)

-- Step 2: Expire old records
UPDATE dim_customer 
SET expiration_date = CURRENT_DATE - 1,
    current_flag = 'N'
WHERE customer_id IN (
    SELECT customer_id FROM changed_records 
    WHERE customer_key IS NOT NULL
);

-- Step 3: Insert new records
INSERT INTO dim_customer (
    customer_id, customer_name, customer_status,
    effective_date, expiration_date, current_flag
)
SELECT 
    customer_id,
    customer_name,
    customer_status,
    CURRENT_DATE,
    '9999-12-31',
    'Y'
FROM changed_records;
```

**Python Implementation:**
```python
def process_scd_type2(staging_df, dimension_df):
    # Identify changes
    merged = staging_df.merge(
        dimension_df[dimension_df['current_flag'] == 'Y'],
        on='customer_id',
        how='left',
        suffixes=('_new', '_old')
    )
    
    # Find changed records
    changed_mask = (
        merged['customer_status_new'] != merged['customer_status_old']
    ) | merged['customer_key'].isna()
    
    changed_records = merged[changed_mask]
    
    # Expire old records
    expire_keys = changed_records['customer_key'].dropna()
    dimension_df.loc[
        dimension_df['customer_key'].isin(expire_keys),
        ['expiration_date', 'current_flag']
    ] = [datetime.now().date(), 'N']
    
    # Insert new records
    new_records = changed_records[[
        'customer_id', 'customer_name_new', 'customer_status_new'
    ]].copy()
    new_records['effective_date'] = datetime.now().date()
    new_records['expiration_date'] = datetime(9999, 12, 31).date()
    new_records['current_flag'] = 'Y'
    
    return pd.concat([dimension_df, new_records])
```

---

## Advanced Modeling Techniques

### 13. What are conformed dimensions and why are they important?

**Answer:**

**Definition:**
Conformed dimensions are dimensions that have the same meaning and content when used across multiple fact tables or data marts.

**Benefits:**
- **Consistent Reporting**: Same dimension attributes across all reports
- **Drill-Across Queries**: Combine data from multiple fact tables
- **Data Integration**: Single version of truth for dimensions
- **Reduced Maintenance**: One dimension serves multiple fact tables

**Example:**
```sql
-- Conformed Date Dimension used by multiple fact tables
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_week VARCHAR(10),
    day_of_month INT,
    day_of_year INT,
    week_of_year INT,
    month_name VARCHAR(10),
    month_number INT,
    quarter_number INT,
    year_number INT,
    is_weekend CHAR(1),
    is_holiday CHAR(1)
);

-- Used by Sales Fact
CREATE TABLE fact_sales (
    sales_key BIGINT,
    date_key INT FOREIGN KEY REFERENCES dim_date(date_key),
    -- other dimensions and measures
);

-- Used by Inventory Fact
CREATE TABLE fact_inventory (
    inventory_key BIGINT,
    date_key INT FOREIGN KEY REFERENCES dim_date(date_key),
    -- other dimensions and measures
);
```

**Drill-Across Query:**
```sql
-- Compare sales and inventory by month
SELECT 
    d.month_name,
    d.year_number,
    SUM(s.sales_amount) as total_sales,
    AVG(i.quantity_on_hand) as avg_inventory
FROM dim_date d
LEFT JOIN fact_sales s ON d.date_key = s.date_key
LEFT JOIN fact_inventory i ON d.date_key = i.date_key
GROUP BY d.month_name, d.year_number
ORDER BY d.year_number, d.month_number;
```

### 14. What are degenerate dimensions?

**Answer:**

**Definition:**
Degenerate dimensions are dimension attributes that are stored directly in the fact table rather than in a separate dimension table.

**Characteristics:**
- Usually transaction identifiers or control numbers
- No descriptive attributes
- High cardinality
- Used for drill-down to transaction detail

**Examples:**
```sql
CREATE TABLE fact_sales (
    sales_key BIGINT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    -- Degenerate dimensions
    invoice_number VARCHAR(20),      -- Degenerate dimension
    line_item_number INT,            -- Degenerate dimension
    promotion_code VARCHAR(10),      -- Degenerate dimension
    -- Measures
    quantity_sold INT,
    sales_amount DECIMAL(12,2)
);
```

**Usage:**
```sql
-- Drill down to specific invoice details
SELECT 
    invoice_number,
    line_item_number,
    p.product_name,
    quantity_sold,
    sales_amount
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
WHERE invoice_number = 'INV-2024-001234'
ORDER BY line_item_number;
```

### 15. How do you handle many-to-many relationships in dimensional modeling?

**Answer:**

**Problem:**
Traditional star schema assumes many-to-one relationships between facts and dimensions.

**Solutions:**

**1. Bridge Tables (Factless Fact Tables):**
```sql
-- Many-to-many: Students to Courses
CREATE TABLE bridge_student_course (
    student_key INT,
    course_key INT,
    enrollment_date DATE,
    grade VARCHAR(2),
    credit_hours INT,
    PRIMARY KEY (student_key, course_key)
);

-- Query with bridge table
SELECT 
    s.student_name,
    c.course_name,
    b.grade
FROM dim_student s
JOIN bridge_student_course b ON s.student_key = b.student_key
JOIN dim_course c ON b.course_key = c.course_key
WHERE s.major = 'Computer Science';
```

**2. Weighting Factors:**
```sql
-- Account to Customer relationship with ownership percentages
CREATE TABLE bridge_account_customer (
    account_key INT,
    customer_key INT,
    ownership_percentage DECIMAL(5,2),
    relationship_type VARCHAR(20),
    effective_date DATE,
    PRIMARY KEY (account_key, customer_key)
);

-- Allocate account balance based on ownership
SELECT 
    c.customer_name,
    SUM(f.account_balance * b.ownership_percentage / 100) as allocated_balance
FROM fact_account f
JOIN bridge_account_customer b ON f.account_key = b.account_key
JOIN dim_customer c ON b.customer_key = c.customer_key
GROUP BY c.customer_name;
```

**3. Flattened Approach:**
```sql
-- Store multiple values in fact table
CREATE TABLE fact_sales_multi_promotion (
    sales_key BIGINT,
    date_key INT,
    customer_key INT,
    product_key INT,
    promotion1_key INT,
    promotion2_key INT,
    promotion3_key INT,
    sales_amount DECIMAL(12,2)
);
```

---

## Performance & Optimization

### 16. What are the key performance optimization techniques for dimensional models?

**Answer:**

**1. Indexing Strategy:**
```sql
-- Fact table indexes
CREATE CLUSTERED INDEX IX_fact_sales_date 
ON fact_sales (date_key);

CREATE NONCLUSTERED INDEX IX_fact_sales_customer 
ON fact_sales (customer_key) INCLUDE (sales_amount);

CREATE NONCLUSTERED INDEX IX_fact_sales_product_date 
ON fact_sales (product_key, date_key);

-- Dimension table indexes
CREATE UNIQUE INDEX IX_dim_customer_natural_key 
ON dim_customer (customer_id);

CREATE INDEX IX_dim_customer_name 
ON dim_customer (customer_name);
```

**2. Partitioning:**
```sql
-- Partition fact table by date
CREATE PARTITION FUNCTION pf_sales_date (DATE)
AS RANGE RIGHT FOR VALUES 
('2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01');

CREATE PARTITION SCHEME ps_sales_date
AS PARTITION pf_sales_date
TO (fg_2023_q1, fg_2023_q1, fg_2023_q1, fg_2023_q2);

CREATE TABLE fact_sales (
    sales_key BIGINT,
    date_key INT,
    sales_date DATE,
    -- other columns
) ON ps_sales_date (sales_date);
```

**3. Aggregate Tables:**
```sql
-- Pre-calculated monthly aggregates
CREATE TABLE fact_sales_monthly (
    month_key INT,
    product_key INT,
    customer_segment_key INT,
    total_quantity INT,
    total_sales_amount DECIMAL(15,2),
    total_cost_amount DECIMAL(15,2),
    transaction_count INT
);
```

**4. Columnstore Indexes:**
```sql
-- SQL Server columnstore for analytics
CREATE CLUSTERED COLUMNSTORE INDEX CCI_fact_sales
ON fact_sales;

-- Filtered columnstore for historical data
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCI_fact_sales_history
ON fact_sales (date_key, customer_key, product_key, sales_amount)
WHERE date_key < 20240101;
```

### 17. How do you handle large dimension tables?

**Answer:**

**Challenges:**
- Memory consumption during joins
- Slow dimension loading
- Storage requirements
- Query performance impact

**Solutions:**

**1. Mini-Dimensions:**
```sql
-- Split large customer dimension
CREATE TABLE dim_customer_core (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    customer_type VARCHAR(50)
);

CREATE TABLE dim_customer_demographics (
    demographics_key INT PRIMARY KEY,
    age_range VARCHAR(20),
    income_range VARCHAR(30),
    education_level VARCHAR(50),
    marital_status VARCHAR(20)
);

-- Fact table references both
CREATE TABLE fact_sales (
    sales_key BIGINT,
    customer_key INT,
    demographics_key INT,
    -- other dimensions and measures
);
```

**2. Dimension Hierarchies:**
```sql
-- Create hierarchy levels
CREATE TABLE dim_geography_country (
    country_key INT PRIMARY KEY,
    country_name VARCHAR(100),
    country_code VARCHAR(3)
);

CREATE TABLE dim_geography_state (
    state_key INT PRIMARY KEY,
    country_key INT,
    state_name VARCHAR(100),
    state_code VARCHAR(5)
);

CREATE TABLE dim_geography_city (
    city_key INT PRIMARY KEY,
    state_key INT,
    city_name VARCHAR(100),
    postal_code VARCHAR(20)
);
```

**3. Dimension Compression:**
```sql
-- Use appropriate data types
CREATE TABLE dim_product_optimized (
    product_key INT PRIMARY KEY,           -- 4 bytes vs BIGINT 8 bytes
    product_code VARCHAR(20),              -- Variable length
    category_id TINYINT,                   -- 1 byte for small ranges
    is_active BIT,                         -- 1 bit vs CHAR(1)
    unit_price DECIMAL(8,2),               -- Appropriate precision
    created_date DATE                      -- 3 bytes vs DATETIME 8 bytes
);
```

---

## Summary

Dimensional data modeling is fundamental to successful data warehouse design. Key principles include:

1. **Business Process Focus**: Design around business processes
2. **Grain Declaration**: Clearly define fact table grain
3. **Conformed Dimensions**: Ensure consistency across data marts
4. **SCD Implementation**: Handle changing dimension data appropriately
5. **Performance Optimization**: Index, partition, and aggregate strategically
6. **User-Centric Design**: Prioritize query performance and usability

Success requires balancing query performance, storage efficiency, and maintenance complexity while keeping the business requirements at the center of all design decisions.