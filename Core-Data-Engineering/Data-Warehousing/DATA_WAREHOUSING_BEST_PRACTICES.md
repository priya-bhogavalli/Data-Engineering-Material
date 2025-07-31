# Data Warehousing Best Practices

## 1. Schema Design

### Dimensional Modeling
```sql
-- Star Schema Design
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2)
);

-- Dimension with SCD Type 2
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    name VARCHAR(100),
    email VARCHAR(100),
    effective_date DATE,
    expiration_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);
```

### Naming Conventions
- Use consistent prefixes (fact_, dim_, bridge_)
- Descriptive column names
- Standardized data types
- Clear primary/foreign key relationships

## 2. Performance Optimization

### Indexing Strategy
```sql
-- Clustered index on date for time-series data
CREATE CLUSTERED INDEX idx_sales_date ON fact_sales(sale_date);

-- Non-clustered indexes on frequently queried columns
CREATE INDEX idx_customer_key ON fact_sales(customer_key);
CREATE INDEX idx_product_key ON fact_sales(product_key);

-- Composite indexes for multi-column queries
CREATE INDEX idx_customer_date ON fact_sales(customer_key, sale_date);
```

### Partitioning
```sql
-- Range partitioning by date
CREATE TABLE fact_sales (
    sale_id BIGINT,
    sale_date DATE,
    amount DECIMAL(12,2)
) PARTITION BY RANGE (sale_date);

-- Create monthly partitions
CREATE TABLE fact_sales_2024_01 PARTITION OF fact_sales
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## 3. Data Loading Strategies

### Incremental Loading
```python
def incremental_load(source_table, target_table, watermark_column):
    # Get last loaded timestamp
    last_watermark = get_max_watermark(target_table, watermark_column)
    
    # Extract incremental data
    incremental_data = extract_data(
        source_table, 
        where_clause=f"{watermark_column} > '{last_watermark}'"
    )
    
    # Transform and load
    transformed_data = transform_data(incremental_data)
    load_data(transformed_data, target_table, mode="append")
```

### Bulk Loading
```sql
-- Use COPY for bulk inserts (PostgreSQL)
COPY fact_sales FROM '/path/to/data.csv' 
WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- Use MERGE for upserts
MERGE target_table t
USING source_data s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET amount = s.amount
WHEN NOT MATCHED THEN INSERT VALUES (s.id, s.amount);
```

## 4. Data Quality Management

### Data Validation
```python
def validate_data_quality(df):
    quality_checks = {
        'completeness': check_completeness(df),
        'uniqueness': check_uniqueness(df),
        'consistency': check_consistency(df),
        'accuracy': check_accuracy(df)
    }
    
    for check, result in quality_checks.items():
        if not result['passed']:
            raise DataQualityError(f"{check} check failed: {result['message']}")
    
    return quality_checks
```

### Data Lineage Tracking
```python
class DataLineageTracker:
    def track_transformation(self, source_table, target_table, transformation_logic):
        lineage_record = {
            'source_table': source_table,
            'target_table': target_table,
            'transformation_logic': transformation_logic,
            'execution_time': datetime.now(),
            'job_id': self.current_job_id
        }
        self.store_lineage(lineage_record)
```

## 5. Security and Governance

### Access Control
```sql
-- Role-based access control
CREATE ROLE data_analyst;
GRANT SELECT ON fact_sales TO data_analyst;
GRANT SELECT ON dim_customer TO data_analyst;

-- Row-level security
CREATE POLICY customer_policy ON fact_sales
    FOR SELECT TO data_analyst
    USING (customer_region = current_user_region());
```

### Data Masking
```python
def mask_sensitive_data(df):
    return df.withColumn(
        "email_masked",
        regexp_replace(col("email"), r"(.{2}).*(@.*)", r"$1***$2")
    ).withColumn(
        "phone_masked",
        regexp_replace(col("phone"), r"(\d{3})\d{3}(\d{4})", r"$1***$2")
    )
```

## 6. Monitoring and Maintenance

### Performance Monitoring
```python
def monitor_query_performance():
    slow_queries = execute_query("""
        SELECT query, avg_execution_time, call_count
        FROM query_stats
        WHERE avg_execution_time > 30000  -- 30 seconds
        ORDER BY avg_execution_time DESC
    """)
    
    for query in slow_queries:
        alert_slow_query(query)
```

### Automated Maintenance
```sql
-- Automated statistics updates
CREATE EVENT update_statistics
ON SCHEDULE EVERY 1 DAY
DO UPDATE STATISTICS fact_sales, dim_customer, dim_product;

-- Automated partition management
CREATE PROCEDURE manage_partitions()
BEGIN
    -- Drop old partitions
    DROP TABLE IF EXISTS fact_sales_old_partition;
    
    -- Create new partitions
    CREATE TABLE fact_sales_new_partition PARTITION OF fact_sales
        FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');
END;
```