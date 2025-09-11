# Fact Data Modeling Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
3. [Architecture](#-architecture)
4. [Key Features](#-key-features)
5. [Use Cases](#-use-cases)
6. [Integration Patterns](#-integration-patterns)
7. [Best Practices](#-best-practices)
8. [Limitations](#-limitations)
9. [Version Highlights](#-version-highlights)

---

## 🎯 Overview

Fact Data Modeling is a dimensional modeling technique that focuses on designing fact tables - the central tables in a data warehouse that store quantitative data for analysis. Facts represent business events or measurements and are typically numeric, additive values that can be aggregated across different dimensions.

**Key Benefits:**
- **Performance**: Optimized for analytical queries and aggregations
- **Scalability**: Handles large volumes of transactional data efficiently  
- **Flexibility**: Supports various analytical perspectives through dimensions
- **Consistency**: Provides single source of truth for business metrics

## 📦 Core Components

### Fact Tables
**Definition**: Central tables containing measurable business events with foreign keys to dimension tables.

**Key Characteristics:**
- **Grain**: Level of detail (transaction, daily, monthly)
- **Measures**: Numeric values that can be aggregated
- **Foreign Keys**: References to dimension tables
- **Large Volume**: Typically contain millions/billions of rows

### Types of Facts

#### 1. Additive Facts
```sql
-- Sales amount - can be summed across all dimensions
CREATE TABLE sales_fact (
    date_key INT,
    product_key INT,
    store_key INT,
    sales_amount DECIMAL(10,2),  -- Additive
    quantity_sold INT            -- Additive
);
```

#### 2. Semi-Additive Facts
```sql
-- Account balance - can be summed across accounts but not time
CREATE TABLE account_balance_fact (
    date_key INT,
    account_key INT,
    balance_amount DECIMAL(15,2)  -- Semi-additive
);
```

#### 3. Non-Additive Facts
```sql
-- Ratios and percentages - cannot be summed
CREATE TABLE performance_fact (
    date_key INT,
    employee_key INT,
    performance_ratio DECIMAL(5,2),  -- Non-additive
    satisfaction_score DECIMAL(3,1)  -- Non-additive
);
```

#### 4. Factless Facts
```sql
-- Events with no measures - only foreign keys
CREATE TABLE student_enrollment_fact (
    student_key INT,
    course_key INT,
    semester_key INT,
    enrollment_date DATE
);
```

### Fact Table Types

#### Transaction Fact Tables
```sql
-- One row per business transaction
CREATE TABLE order_transaction_fact (
    transaction_id VARCHAR(50) PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    order_amount DECIMAL(10,2),
    quantity INT,
    discount_amount DECIMAL(8,2)
);
```

#### Periodic Snapshot Facts
```sql
-- Regular snapshots at specific intervals
CREATE TABLE monthly_inventory_fact (
    month_key INT,
    product_key INT,
    warehouse_key INT,
    beginning_inventory INT,
    ending_inventory INT,
    average_inventory DECIMAL(10,2)
);
```

#### Accumulating Snapshot Facts
```sql
-- Tracks process lifecycle with multiple dates
CREATE TABLE order_fulfillment_fact (
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

## 🏗️ Architecture

### Star Schema Architecture
```
                    ┌─────────────────┐
                    │   TIME_DIM      │
                    │                 │
                    │ date_key (PK)   │
                    │ date            │
                    │ month           │
                    │ quarter         │
                    │ year            │
                    └─────────┬───────┘
                              │
    ┌─────────────────┐      │      ┌─────────────────┐
    │  PRODUCT_DIM    │      │      │  CUSTOMER_DIM   │
    │                 │      │      │                 │
    │ product_key(PK) │      │      │ customer_key(PK)│
    │ product_name    │      │      │ customer_name   │
    │ category        │      │      │ city            │
    │ brand           │      │      │ state           │
    └─────────┬───────┘      │      └─────────┬───────┘
              │              │                │
              │    ┌─────────▼─────────┐      │
              └────┤   SALES_FACT      ├──────┘
                   │                   │
                   │ date_key (FK)     │
                   │ product_key (FK)  │
                   │ customer_key (FK) │
                   │ store_key (FK)    │
                   │ sales_amount      │
                   │ quantity_sold     │
                   │ discount_amount   │
                   └─────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │   STORE_DIM     │
                    │                 │
                    │ store_key (PK)  │
                    │ store_name      │
                    │ city            │
                    │ region          │
                    └─────────────────┘
```

### Snowflake Schema Architecture
```
    ┌─────────────────┐    ┌─────────────────┐
    │   CATEGORY_DIM  │    │   BRAND_DIM     │
    │                 │    │                 │
    │ category_key(PK)│    │ brand_key (PK)  │
    │ category_name   │    │ brand_name      │
    └─────────┬───────┘    └─────────┬───────┘
              │                      │
    ┌─────────▼─────────┐           │
    │  PRODUCT_DIM      │           │
    │                   │           │
    │ product_key (PK)  │           │
    │ product_name      │           │
    │ category_key (FK) ├───────────┘
    │ brand_key (FK)    ├───────────┘
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │   SALES_FACT      │
    │                   │
    │ product_key (FK)  │
    │ sales_amount      │
    │ quantity_sold     │
    └───────────────────┘
```

## 🔧 Key Features

### Grain Definition
**Definition**: The level of detail stored in the fact table.

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

### Slowly Changing Dimensions Integration
```sql
-- Fact table with SCD Type 2 dimension keys
CREATE TABLE sales_fact (
    transaction_date DATE,
    customer_key INT,  -- Points to specific version
    product_key INT,
    sales_amount DECIMAL(10,2),
    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer dimension with SCD Type 2
CREATE TABLE customer_dim (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    address VARCHAR(200),
    effective_date DATE,
    expiration_date DATE,
    current_flag BOOLEAN
);
```

### Conformed Facts
```sql
-- Revenue fact (conformed across business processes)
CREATE TABLE sales_revenue_fact (
    date_key INT,
    product_key INT,
    customer_key INT,
    revenue_amount DECIMAL(12,2)  -- Conformed measure
);

CREATE TABLE marketing_revenue_fact (
    date_key INT,
    campaign_key INT,
    product_key INT,
    revenue_amount DECIMAL(12,2)  -- Same definition as sales
);
```

## 🎯 Use Cases

### 1. Sales Analytics
```sql
-- Monthly sales performance by region
SELECT 
    d.year,
    d.month,
    s.region,
    SUM(f.sales_amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales_fact f
JOIN date_dim d ON f.date_key = d.date_key
JOIN store_dim s ON f.store_key = s.store_key
WHERE d.year = 2023
GROUP BY d.year, d.month, s.region
ORDER BY d.month, total_sales DESC;
```

### 2. Financial Reporting
```sql
-- Quarterly financial summary
SELECT 
    d.quarter,
    SUM(CASE WHEN f.transaction_type = 'SALE' THEN f.amount ELSE 0 END) as revenue,
    SUM(CASE WHEN f.transaction_type = 'REFUND' THEN f.amount ELSE 0 END) as refunds,
    COUNT(DISTINCT f.customer_key) as unique_customers
FROM financial_fact f
JOIN date_dim d ON f.date_key = d.date_key
WHERE d.year = 2023
GROUP BY d.quarter
ORDER BY d.quarter;
```

### 3. Inventory Management
```sql
-- Inventory turnover analysis
SELECT 
    p.category,
    AVG(f.beginning_inventory) as avg_beginning_inventory,
    AVG(f.ending_inventory) as avg_ending_inventory,
    SUM(f.units_sold) / AVG(f.average_inventory) as inventory_turnover
FROM inventory_fact f
JOIN product_dim p ON f.product_key = p.product_key
JOIN date_dim d ON f.date_key = d.date_key
WHERE d.year = 2023
GROUP BY p.category
ORDER BY inventory_turnover DESC;
```

## 🔗 Integration Patterns

### ETL Integration
```python
# Python ETL example for fact table loading
def load_sales_fact(spark, source_data):
    # Extract from source
    transactions = spark.read.jdbc(
        url="jdbc:postgresql://source-db:5432/sales",
        table="transactions",
        properties={"user": "etl_user", "password": "password"}
    )
    
    # Transform - join with dimensions to get keys
    fact_data = transactions.alias("t") \
        .join(date_dim.alias("d"), 
              col("t.transaction_date") == col("d.date")) \
        .join(customer_dim.alias("c"), 
              col("t.customer_id") == col("c.customer_id")) \
        .join(product_dim.alias("p"), 
              col("t.product_id") == col("p.product_id")) \
        .select(
            col("d.date_key"),
            col("c.customer_key"),
            col("p.product_key"),
            col("t.amount").alias("sales_amount"),
            col("t.quantity")
        )
    
    # Load to fact table
    fact_data.write.mode("append").saveAsTable("sales_fact")
```

### Real-time Integration
```python
# Streaming fact table updates
def stream_fact_updates(spark):
    # Read from Kafka
    stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "transactions") \
        .load()
    
    # Parse and enrich
    parsed_stream = stream.select(
        from_json(col("value").cast("string"), transaction_schema).alias("data")
    ).select("data.*")
    
    # Write to Delta table for ACID compliance
    query = parsed_stream.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "/checkpoints/sales_fact") \
        .start("/delta/sales_fact")
    
    return query
```

## 📋 Best Practices

### 1. Grain Consistency
```sql
-- Ensure consistent grain across related facts
-- All facts at daily grain
CREATE TABLE daily_sales_fact (
    date_key INT,
    product_key INT,
    daily_sales_amount DECIMAL(12,2)
);

CREATE TABLE daily_inventory_fact (
    date_key INT,
    product_key INT,
    ending_inventory INT
);
```

### 2. Surrogate Keys
```sql
-- Use surrogate keys for dimension references
CREATE TABLE sales_fact (
    sales_fact_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    date_key INT NOT NULL,
    customer_key INT NOT NULL,
    product_key INT NOT NULL,
    sales_amount DECIMAL(10,2),
    FOREIGN KEY (date_key) REFERENCES date_dim(date_key),
    FOREIGN KEY (customer_key) REFERENCES customer_dim(customer_key),
    FOREIGN KEY (product_key) REFERENCES product_dim(product_key)
);
```

### 3. Partitioning Strategy
```sql
-- Partition by date for query performance
CREATE TABLE sales_fact (
    date_key INT,
    customer_key INT,
    product_key INT,
    sales_amount DECIMAL(10,2)
) PARTITION BY RANGE (date_key);

-- Create monthly partitions
CREATE TABLE sales_fact_202301 PARTITION OF sales_fact
FOR VALUES FROM (20230101) TO (20230201);
```

### 4. Indexing Strategy
```sql
-- Create indexes on foreign keys and frequently filtered columns
CREATE INDEX idx_sales_fact_date ON sales_fact(date_key);
CREATE INDEX idx_sales_fact_customer ON sales_fact(customer_key);
CREATE INDEX idx_sales_fact_product ON sales_fact(product_key);
CREATE INDEX idx_sales_fact_composite ON sales_fact(date_key, customer_key);
```

## ⚠️ Limitations

### 1. Storage Requirements
- **Large Volume**: Fact tables can become extremely large
- **Storage Costs**: Detailed grain requires significant storage
- **Backup Complexity**: Large tables increase backup/restore time

### 2. Performance Challenges
- **Join Complexity**: Multiple dimension joins can impact performance
- **Aggregation Time**: Large fact tables slow down aggregation queries
- **Index Maintenance**: Multiple indexes require maintenance overhead

### 3. Data Quality Issues
- **Late Arriving Facts**: Handling delayed transaction data
- **Dimension Key Lookup**: Missing or invalid dimension references
- **Data Consistency**: Ensuring referential integrity across tables

### 4. Maintenance Overhead
- **ETL Complexity**: Complex transformation logic for fact loading
- **Historical Data**: Managing historical fact data and changes
- **Schema Evolution**: Modifying fact table structure in production

## 🔄 Version Highlights

### Traditional Fact Modeling
- **Kimball Methodology**: Star schema with conformed dimensions
- **Inmon Approach**: Normalized data warehouse with fact tables
- **OLAP Cubes**: Pre-aggregated fact data for fast queries

### Modern Fact Modeling
- **Delta Lake**: ACID transactions for fact table updates
- **Data Vault 2.0**: Hub-link-satellite model with fact satellites
- **Data Mesh**: Domain-oriented fact tables as data products
- **Real-time Facts**: Streaming fact table updates with Kafka/Kinesis

### Cloud-Native Approaches
- **Snowflake**: Automatic clustering and micro-partitions
- **BigQuery**: Columnar storage with automatic optimization
- **Redshift**: Distribution keys and sort keys for performance
- **Databricks**: Delta Lake with optimized Spark processing

### Advanced Patterns
- **Temporal Facts**: Bi-temporal fact tables with valid/transaction time
- **Multi-Grain Facts**: Facts at different levels of aggregation
- **Bridge Tables**: Handling many-to-many relationships
- **Factless Facts**: Event tracking without measures

---

## 📚 Quick References
- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/)
- [Data Vault 2.0 Methodology](https://datavaultalliance.com/)
- [Modern Data Stack Patterns](https://www.getdbt.com/analytics-engineering/)
- [Delta Lake Documentation](https://delta.io/)