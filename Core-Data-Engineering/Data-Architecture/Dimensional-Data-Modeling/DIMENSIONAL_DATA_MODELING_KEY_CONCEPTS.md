# Dimensional Data Modeling Key Concepts

## 🎯 What is Dimensional Modeling?
Data modeling technique optimized for data warehousing and analytics, organizing data into facts and dimensions.

## 🏗️ Core Components

### 1. Fact Tables
```sql
-- Sales fact table
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);
```

### 2. Dimension Tables
```sql
-- Customer dimension
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(20),
    zip_code VARCHAR(10),
    customer_segment VARCHAR(20),
    registration_date DATE,
    is_active BOOLEAN
);

-- Product dimension with hierarchy
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    brand VARCHAR(50),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    department VARCHAR(50),
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    product_status VARCHAR(20)
);
```

### 3. Date Dimension
```sql
-- Comprehensive date dimension
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_week INT,
    day_name VARCHAR(10),
    day_of_month INT,
    day_of_year INT,
    week_of_year INT,
    month_number INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    holiday_name VARCHAR(50),
    fiscal_year INT,
    fiscal_quarter INT,
    fiscal_month INT
);

-- Populate date dimension
INSERT INTO dim_date (date_key, full_date, day_of_week, day_name, ...)
SELECT 
    CAST(FORMAT(date_val, 'yyyyMMdd') AS INT) as date_key,
    date_val as full_date,
    DATEPART(weekday, date_val) as day_of_week,
    DATENAME(weekday, date_val) as day_name,
    -- ... other date attributes
FROM generate_series('2020-01-01'::date, '2030-12-31'::date, '1 day') as date_val;
```

## 📊 Schema Patterns

### Star Schema
```sql
-- Central fact table surrounded by dimension tables
SELECT 
    d.year,
    d.quarter,
    p.category,
    c.customer_segment,
    SUM(f.total_amount) as total_sales,
    COUNT(*) as transaction_count
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE d.year = 2024
GROUP BY d.year, d.quarter, p.category, c.customer_segment;
```

### Snowflake Schema
```sql
-- Normalized dimension tables
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    subcategory_key INT,
    FOREIGN KEY (subcategory_key) REFERENCES dim_subcategory(subcategory_key)
);

CREATE TABLE dim_subcategory (
    subcategory_key INT PRIMARY KEY,
    subcategory_name VARCHAR(50),
    category_key INT,
    FOREIGN KEY (category_key) REFERENCES dim_category(category_key)
);

CREATE TABLE dim_category (
    category_key INT PRIMARY KEY,
    category_name VARCHAR(50),
    department_key INT,
    FOREIGN KEY (department_key) REFERENCES dim_department(department_key)
);
```

## 🔧 Advanced Concepts

### Slowly Changing Dimensions (SCD)
```sql
-- Type 2 SCD: Historical tracking
CREATE TABLE dim_customer_scd2 (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(200),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN,
    version_number INT
);

-- SCD Type 2 update process
-- 1. Expire current record
UPDATE dim_customer_scd2 
SET expiry_date = CURRENT_DATE - 1, is_current = FALSE
WHERE customer_id = '12345' AND is_current = TRUE;

-- 2. Insert new record
INSERT INTO dim_customer_scd2 (customer_id, first_name, last_name, address, 
                               effective_date, expiry_date, is_current, version_number)
VALUES ('12345', 'John', 'Doe', 'New Address', 
        CURRENT_DATE, '9999-12-31', TRUE, 2);
```

### Factless Fact Tables
```sql
-- Event tracking without measures
CREATE TABLE fact_student_attendance (
    attendance_key INT PRIMARY KEY,
    student_key INT,
    date_key INT,
    class_key INT,
    attendance_type_key INT,
    FOREIGN KEY (student_key) REFERENCES dim_student(student_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (class_key) REFERENCES dim_class(class_key)
);

-- Query: Students who attended specific classes
SELECT 
    s.student_name,
    c.class_name,
    d.full_date
FROM fact_student_attendance f
JOIN dim_student s ON f.student_key = s.student_key
JOIN dim_class c ON f.class_key = c.class_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.month_name = 'January' AND d.year = 2024;
```

### Aggregate Tables
```sql
-- Monthly sales summary
CREATE TABLE fact_sales_monthly (
    date_key INT,
    product_key INT,
    customer_segment_key INT,
    total_quantity INT,
    total_amount DECIMAL(12,2),
    transaction_count INT,
    PRIMARY KEY (date_key, product_key, customer_segment_key)
);

-- Populate from detailed fact table
INSERT INTO fact_sales_monthly
SELECT 
    d.month_key as date_key,
    f.product_key,
    c.segment_key as customer_segment_key,
    SUM(f.quantity) as total_quantity,
    SUM(f.total_amount) as total_amount,
    COUNT(*) as transaction_count
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY d.month_key, f.product_key, c.segment_key;
```

## 🚀 ETL Implementation

### Python ETL for Dimensional Model
```python
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

class DimensionalETL:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
    
    def load_dimension(self, source_df, dim_table, business_key, scd_type=1):
        """Load dimension table with SCD handling"""
        if scd_type == 1:
            # Type 1: Overwrite
            self.load_scd_type1(source_df, dim_table, business_key)
        elif scd_type == 2:
            # Type 2: Historical tracking
            self.load_scd_type2(source_df, dim_table, business_key)
    
    def load_scd_type2(self, source_df, dim_table, business_key):
        """Load SCD Type 2 dimension"""
        # Get current dimension data
        current_dim = pd.read_sql(f"SELECT * FROM {dim_table} WHERE is_current = TRUE", self.engine)
        
        # Identify changes
        changes = self.identify_changes(source_df, current_dim, business_key)
        
        if not changes.empty:
            # Expire changed records
            expire_sql = f"""
            UPDATE {dim_table} 
            SET expiry_date = %s, is_current = FALSE 
            WHERE {business_key} IN ({','.join(['%s'] * len(changes))}) 
            AND is_current = TRUE
            """
            
            with self.engine.connect() as conn:
                conn.execute(expire_sql, [datetime.now().date()] + changes[business_key].tolist())
            
            # Insert new versions
            new_records = source_df[source_df[business_key].isin(changes[business_key])]
            new_records['effective_date'] = datetime.now().date()
            new_records['expiry_date'] = '9999-12-31'
            new_records['is_current'] = True
            
            new_records.to_sql(dim_table, self.engine, if_exists='append', index=False)
    
    def load_fact_table(self, source_df, fact_table, dimension_mappings):
        """Load fact table with dimension key lookups"""
        fact_df = source_df.copy()
        
        # Replace business keys with surrogate keys
        for dim_table, mapping in dimension_mappings.items():
            business_key = mapping['business_key']
            surrogate_key = mapping['surrogate_key']
            
            dim_lookup = pd.read_sql(
                f"SELECT {business_key}, {surrogate_key} FROM {dim_table} WHERE is_current = TRUE",
                self.engine
            )
            
            fact_df = fact_df.merge(dim_lookup, on=business_key, how='left')
            fact_df.drop(columns=[business_key], inplace=True)
        
        # Load to fact table
        fact_df.to_sql(fact_table, self.engine, if_exists='append', index=False)
```

## 🎯 Benefits
- Optimized for analytical queries
- Intuitive business-friendly structure
- Excellent query performance
- Supports historical analysis
- Scalable design patterns

## 🔧 Best Practices
- Use meaningful surrogate keys
- Implement proper indexing strategy
- Design for common query patterns
- Maintain referential integrity
- Document business rules and definitions
- Consider aggregate tables for performance

## ⚠️ Considerations
- Storage overhead from denormalization
- ETL complexity for SCD handling
- Maintenance of dimension hierarchies
- Data freshness requirements
- Performance tuning needs