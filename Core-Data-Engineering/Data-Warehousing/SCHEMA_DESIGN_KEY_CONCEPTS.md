# Schema Design - Key Concepts

## 1. Schema Design Fundamentals

### Schema Types Overview
- **Star Schema**: Central fact table with denormalized dimensions
- **Snowflake Schema**: Normalized dimension tables with hierarchies
- **Galaxy Schema**: Multiple fact tables sharing common dimensions
- **Data Vault**: Hub-Link-Satellite model for enterprise warehouses

### Design Considerations
- **Query Performance**: Optimize for analytical workloads
- **Storage Efficiency**: Balance performance with storage costs
- **Maintainability**: Design for easy updates and modifications
- **Scalability**: Support growing data volumes and users

## 2. Dimensional Modeling

### Fact Tables
```sql
-- Example Fact Table Structure
CREATE TABLE fact_sales (
    date_key INT,
    product_key INT,
    customer_key INT,
    store_key INT,
    sales_amount DECIMAL(10,2),
    quantity_sold INT,
    discount_amount DECIMAL(10,2),
    cost_amount DECIMAL(10,2)
);
```

#### Fact Table Types
- **Transaction Facts**: Individual business events
- **Periodic Snapshot Facts**: Regular interval summaries
- **Accumulating Snapshot Facts**: Process lifecycle tracking
- **Factless Facts**: Events without measurements

#### Fact Grain Definition
- **Atomic Level**: Lowest level of detail
- **Aggregated Level**: Pre-summarized data
- **Mixed Grain**: Multiple detail levels in same table
- **Grain Declaration**: Explicit definition of fact level

### Dimension Tables
```sql
-- Example Dimension Table Structure
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    supplier VARCHAR(100),
    unit_cost DECIMAL(8,2),
    effective_date DATE,
    expiry_date DATE,
    current_flag CHAR(1)
);
```

#### Dimension Characteristics
- **Descriptive Attributes**: Text fields for filtering and grouping
- **Hierarchies**: Natural drill-down paths
- **Surrogate Keys**: System-generated unique identifiers
- **Natural Keys**: Business-meaningful identifiers

## 3. Star Schema Design

### Star Schema Structure
```
        dim_date
            |
dim_product -- fact_sales -- dim_customer
            |
        dim_store
```

### Advantages
- **Simple Queries**: Easy to understand and write
- **Fast Performance**: Minimal joins required
- **User-Friendly**: Intuitive for business users
- **Tool Compatibility**: Works well with BI tools

### Design Guidelines
- **Denormalized Dimensions**: Include all attributes in dimension tables
- **Consistent Grain**: All facts at same detail level
- **Conformed Dimensions**: Shared dimensions across fact tables
- **Surrogate Keys**: Use artificial keys for relationships

### Example Implementation
```sql
-- Star Schema Example
SELECT 
    d.year,
    d.quarter,
    p.category,
    c.region,
    SUM(f.sales_amount) as total_sales
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY d.year, d.quarter, p.category, c.region;
```

## 4. Snowflake Schema Design

### Snowflake Schema Structure
```
    dim_date
        |
dim_product_category
        |
    dim_product -- fact_sales -- dim_customer -- dim_customer_segment
        |                           |
    dim_supplier               dim_geography
```

### Normalization Benefits
- **Storage Efficiency**: Reduced redundancy
- **Data Integrity**: Consistent reference data
- **Maintenance**: Easier to update hierarchies
- **Flexibility**: Support complex hierarchies

### Design Considerations
- **Join Complexity**: More joins required for queries
- **Performance Impact**: Potential slower query performance
- **ETL Complexity**: More complex loading processes
- **User Experience**: Less intuitive for end users

## 5. Slowly Changing Dimensions (SCD)

### SCD Type 1 - Overwrite
```sql
-- Update existing record
UPDATE dim_customer 
SET customer_status = 'Inactive',
    last_modified = CURRENT_DATE
WHERE customer_key = 12345;
```

### SCD Type 2 - Add New Record
```sql
-- Insert new record with version
INSERT INTO dim_customer (
    customer_id, customer_name, customer_status,
    effective_date, expiry_date, current_flag
) VALUES (
    'CUST001', 'John Smith', 'Premium',
    '2024-01-01', '9999-12-31', 'Y'
);

-- Update previous record
UPDATE dim_customer 
SET expiry_date = '2023-12-31',
    current_flag = 'N'
WHERE customer_id = 'CUST001' 
AND current_flag = 'Y';
```

### SCD Type 3 - Add New Attribute
```sql
-- Add previous value column
ALTER TABLE dim_customer 
ADD COLUMN previous_status VARCHAR(50);

-- Update with new and previous values
UPDATE dim_customer 
SET previous_status = customer_status,
    customer_status = 'Premium'
WHERE customer_key = 12345;
```

### SCD Type 4 - History Table
```sql
-- Current dimension table
CREATE TABLE dim_customer_current (
    customer_key INT,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    customer_status VARCHAR(50)
);

-- History dimension table
CREATE TABLE dim_customer_history (
    customer_key INT,
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    customer_status VARCHAR(50),
    effective_date DATE,
    expiry_date DATE
);
```

## 6. Data Vault Modeling

### Hub Tables
```sql
-- Hub stores unique business keys
CREATE TABLE hub_customer (
    customer_hash_key CHAR(32) PRIMARY KEY,
    customer_id VARCHAR(50),
    load_date TIMESTAMP,
    record_source VARCHAR(50)
);
```

### Link Tables
```sql
-- Link stores relationships
CREATE TABLE link_customer_order (
    customer_order_hash_key CHAR(32) PRIMARY KEY,
    customer_hash_key CHAR(32),
    order_hash_key CHAR(32),
    load_date TIMESTAMP,
    record_source VARCHAR(50)
);
```

### Satellite Tables
```sql
-- Satellite stores descriptive data
CREATE TABLE sat_customer_details (
    customer_hash_key CHAR(32),
    load_date TIMESTAMP,
    customer_name VARCHAR(200),
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    hash_diff CHAR(32),
    record_source VARCHAR(50),
    PRIMARY KEY (customer_hash_key, load_date)
);
```

## 7. Advanced Schema Patterns

### Bridge Tables
```sql
-- Handle many-to-many relationships
CREATE TABLE bridge_account_customer (
    account_key INT,
    customer_key INT,
    allocation_percentage DECIMAL(5,2),
    effective_date DATE,
    expiry_date DATE
);
```

### Junk Dimensions
```sql
-- Combine low-cardinality flags
CREATE TABLE dim_transaction_flags (
    transaction_flag_key INT PRIMARY KEY,
    is_weekend CHAR(1),
    is_holiday CHAR(1),
    is_promotion CHAR(1),
    payment_method VARCHAR(20)
);
```

### Degenerate Dimensions
```sql
-- Store dimension attributes in fact table
CREATE TABLE fact_order_line (
    date_key INT,
    product_key INT,
    customer_key INT,
    order_number VARCHAR(20), -- Degenerate dimension
    line_number INT,          -- Degenerate dimension
    quantity INT,
    unit_price DECIMAL(8,2)
);
```

## 8. Performance Optimization

### Indexing Strategies
```sql
-- Clustered index on date for partitioning
CREATE CLUSTERED INDEX IX_fact_sales_date 
ON fact_sales (date_key);

-- Non-clustered indexes on foreign keys
CREATE INDEX IX_fact_sales_product 
ON fact_sales (product_key);

-- Composite indexes for common queries
CREATE INDEX IX_fact_sales_date_product 
ON fact_sales (date_key, product_key);
```

### Partitioning
```sql
-- Range partitioning by date
CREATE TABLE fact_sales (
    date_key INT,
    product_key INT,
    sales_amount DECIMAL(10,2)
)
PARTITION BY RANGE (date_key) (
    PARTITION p2023 VALUES LESS THAN (20240101),
    PARTITION p2024 VALUES LESS THAN (20250101)
);
```

### Aggregation Tables
```sql
-- Pre-aggregated monthly summary
CREATE TABLE fact_sales_monthly (
    year_month INT,
    product_key INT,
    customer_key INT,
    total_sales DECIMAL(12,2),
    total_quantity INT,
    transaction_count INT
);
```

## 9. Modern Schema Approaches

### Wide Tables
```sql
-- Denormalized wide table for analytics
CREATE TABLE customer_360 (
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    total_orders INT,
    total_revenue DECIMAL(12,2),
    last_order_date DATE,
    preferred_category VARCHAR(100),
    lifetime_value DECIMAL(12,2),
    churn_probability DECIMAL(3,2)
);
```

### Columnar Storage Optimization
```sql
-- Optimize for columnar databases
CREATE TABLE fact_sales_columnar (
    date_key INT ENCODING DELTA,
    product_key INT ENCODING LZO,
    customer_key INT ENCODING LZO,
    sales_amount DECIMAL(10,2) ENCODING ZSTD
)
SORTKEY (date_key, product_key);
```

### JSON and Semi-Structured Data
```sql
-- Handle semi-structured data
CREATE TABLE customer_events (
    event_id VARCHAR(50),
    customer_id VARCHAR(50),
    event_timestamp TIMESTAMP,
    event_data JSON,
    event_type VARCHAR(50)
);

-- Query JSON data
SELECT 
    customer_id,
    JSON_EXTRACT(event_data, '$.product_id') as product_id,
    JSON_EXTRACT(event_data, '$.amount') as amount
FROM customer_events
WHERE event_type = 'purchase';
```

## 10. Schema Evolution and Maintenance

### Version Control
```sql
-- Schema versioning
CREATE TABLE schema_version (
    version_number VARCHAR(10),
    deployment_date TIMESTAMP,
    description TEXT,
    rollback_script TEXT
);
```

### Backward Compatibility
```sql
-- Add columns with defaults
ALTER TABLE dim_product 
ADD COLUMN sustainability_rating INT DEFAULT 0;

-- Create views for compatibility
CREATE VIEW dim_product_v1 AS
SELECT 
    product_key,
    product_id,
    product_name,
    category
FROM dim_product;
```

### Impact Analysis
- **Dependency Mapping**: Track table relationships
- **Query Analysis**: Identify affected queries and reports
- **Performance Testing**: Validate changes don't degrade performance
- **Rollback Planning**: Prepare rollback procedures

### Best Practices
- **Documentation**: Maintain comprehensive schema documentation
- **Testing**: Validate changes in development environment
- **Communication**: Notify stakeholders of schema changes
- **Monitoring**: Track performance after schema modifications