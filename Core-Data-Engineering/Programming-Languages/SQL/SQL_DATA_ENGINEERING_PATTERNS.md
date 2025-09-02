# SQL Data Engineering Patterns

## 📋 Overview

This comprehensive guide covers essential SQL patterns specifically designed for data engineering workflows. These patterns are battle-tested solutions for common data engineering challenges including ETL/ELT processes, data quality management, dimensional modeling, and performance optimization.

## 🎯 Purpose

Data engineers work with complex data pipelines, large datasets, and demanding performance requirements. This document provides:

- **Production-Ready Patterns**: Proven SQL patterns used in enterprise data engineering
- **Performance Optimization**: Techniques for handling large-scale data operations
- **Data Quality**: Comprehensive approaches to ensure data integrity and consistency
- **Dimensional Modeling**: Star schema and data warehouse design patterns
- **Real-World Examples**: Practical implementations with detailed explanations

## 🏗️ Pattern Categories

### 1. ETL/ELT Patterns
- Incremental data loading strategies
- Change Data Capture (CDC) implementations
- Data deduplication techniques
- Bulk data processing patterns

### 2. Data Quality Patterns
- Automated data validation frameworks
- Outlier detection algorithms
- Data profiling and monitoring
- Constraint-based quality checks

### 3. Dimensional Modeling Patterns
- Slowly Changing Dimensions (SCD) Types 1, 2, and 3
- Bridge table implementations
- Fact table design patterns
- Time-based partitioning strategies

### 4. Performance Optimization Patterns
- Partitioning strategies for large tables
- Materialized view patterns
- Index optimization techniques
- Query performance tuning

## 💡 Key Benefits

- **Scalability**: Patterns designed to handle enterprise-scale data volumes
- **Maintainability**: Clean, documented code that's easy to understand and modify
- **Performance**: Optimized for speed and resource efficiency
- **Reliability**: Error handling and data integrity built-in
- **Flexibility**: Adaptable patterns that work across different database systems

## 🔧 Prerequisites

- Intermediate to advanced SQL knowledge
- Understanding of data warehousing concepts
- Familiarity with database performance tuning
- Experience with ETL/ELT processes

---

## ETL/ELT Patterns

### Incremental Data Loading
```sql
-- Delta load pattern using timestamps
INSERT INTO target_table
SELECT *
FROM source_table
WHERE last_modified > (
    SELECT COALESCE(MAX(last_modified), '1900-01-01')
    FROM target_table
);

-- Upsert pattern for incremental loads
MERGE INTO dim_customer AS target
USING (
    SELECT customer_id, name, email, city, last_modified
    FROM staging_customer
    WHERE last_modified > ?
) AS source ON target.customer_id = source.customer_id
WHEN MATCHED THEN
    UPDATE SET 
        name = source.name,
        email = source.email,
        city = source.city,
        last_modified = source.last_modified
WHEN NOT MATCHED THEN
    INSERT (customer_id, name, email, city, last_modified)
    VALUES (source.customer_id, source.name, source.email, source.city, source.last_modified);
```

### Change Data Capture (CDC) Pattern
```sql
-- Create audit table for tracking changes
CREATE TABLE customer_audit (
    audit_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    operation_type VARCHAR(10), -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger function for CDC
CREATE OR REPLACE FUNCTION customer_audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO customer_audit (customer_id, operation_type, old_values)
        VALUES (OLD.customer_id, 'DELETE', row_to_json(OLD));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO customer_audit (customer_id, operation_type, old_values, new_values)
        VALUES (NEW.customer_id, 'UPDATE', row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO customer_audit (customer_id, operation_type, new_values)
        VALUES (NEW.customer_id, 'INSERT', row_to_json(NEW));
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### Data Deduplication Patterns
```sql
-- Remove duplicates keeping latest record
WITH ranked_data AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id 
               ORDER BY last_modified DESC
           ) as rn
    FROM customer_staging
)
DELETE FROM customer_staging
WHERE (customer_id, last_modified) IN (
    SELECT customer_id, last_modified
    FROM ranked_data
    WHERE rn > 1
);

-- Fuzzy deduplication using similarity
WITH potential_duplicates AS (
    SELECT 
        a.id as id1,
        b.id as id2,
        SIMILARITY(a.name, b.name) as name_similarity,
        SIMILARITY(a.email, b.email) as email_similarity
    FROM customers a
    JOIN customers b ON a.id < b.id
    WHERE SIMILARITY(a.name, b.name) > 0.8
       OR SIMILARITY(a.email, b.email) > 0.9
)
SELECT * FROM potential_duplicates
WHERE name_similarity > 0.8 OR email_similarity > 0.9;
```

## Data Quality Patterns

### Data Validation Framework
```sql
-- Create data quality rules table
CREATE TABLE data_quality_rules (
    rule_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    rule_type VARCHAR(50),
    rule_definition TEXT,
    threshold_value DECIMAL,
    is_active BOOLEAN DEFAULT true
);

-- Data quality check function
CREATE OR REPLACE FUNCTION check_data_quality(
    p_table_name VARCHAR,
    p_column_name VARCHAR DEFAULT NULL
)
RETURNS TABLE(
    rule_id INTEGER,
    table_name VARCHAR,
    column_name VARCHAR,
    rule_type VARCHAR,
    failed_records INTEGER,
    total_records INTEGER,
    failure_rate DECIMAL
) AS $$
DECLARE
    rule_record RECORD;
    sql_query TEXT;
BEGIN
    FOR rule_record IN 
        SELECT * FROM data_quality_rules 
        WHERE table_name = p_table_name 
        AND (p_column_name IS NULL OR column_name = p_column_name)
        AND is_active = true
    LOOP
        -- Build dynamic SQL based on rule type
        CASE rule_record.rule_type
            WHEN 'NOT_NULL' THEN
                sql_query := format('SELECT COUNT(*) FROM %I WHERE %I IS NULL', 
                                  rule_record.table_name, rule_record.column_name);
            WHEN 'UNIQUE' THEN
                sql_query := format('SELECT COUNT(*) - COUNT(DISTINCT %I) FROM %I', 
                                  rule_record.column_name, rule_record.table_name);
            WHEN 'RANGE' THEN
                sql_query := format('SELECT COUNT(*) FROM %I WHERE %I NOT BETWEEN %s AND %s', 
                                  rule_record.table_name, rule_record.column_name,
                                  split_part(rule_record.rule_definition, ',', 1),
                                  split_part(rule_record.rule_definition, ',', 2));
        END CASE;
        
        -- Execute and return results
        -- Implementation would continue here...
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### Outlier Detection
```sql
-- Statistical outlier detection using IQR
WITH stats AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) as q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) as q3,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) as median
    FROM transactions
),
outlier_bounds AS (
    SELECT 
        q1,
        q3,
        median,
        q1 - 1.5 * (q3 - q1) as lower_bound,
        q3 + 1.5 * (q3 - q1) as upper_bound
    FROM stats
)
SELECT 
    t.*,
    CASE 
        WHEN t.amount < ob.lower_bound THEN 'LOW_OUTLIER'
        WHEN t.amount > ob.upper_bound THEN 'HIGH_OUTLIER'
        ELSE 'NORMAL'
    END as outlier_flag
FROM transactions t
CROSS JOIN outlier_bounds ob;
```

## Dimensional Modeling Patterns

### Type 2 SCD Implementation
```sql
-- Complete Type 2 SCD procedure
CREATE OR REPLACE FUNCTION update_customer_dimension(
    p_customer_id INTEGER,
    p_name VARCHAR,
    p_email VARCHAR,
    p_city VARCHAR
)
RETURNS VOID AS $$
DECLARE
    current_record RECORD;
    changes_detected BOOLEAN := false;
BEGIN
    -- Get current active record
    SELECT * INTO current_record
    FROM dim_customer
    WHERE customer_id = p_customer_id
    AND is_current = true;
    
    -- Check if record exists
    IF current_record IS NULL THEN
        -- Insert new record
        INSERT INTO dim_customer (
            customer_id, name, email, city,
            effective_date, expiry_date, is_current, version
        ) VALUES (
            p_customer_id, p_name, p_email, p_city,
            CURRENT_DATE, '9999-12-31', true, 1
        );
    ELSE
        -- Check for changes
        IF current_record.name != p_name OR 
           current_record.email != p_email OR 
           current_record.city != p_city THEN
            changes_detected := true;
        END IF;
        
        -- If changes detected, create new version
        IF changes_detected THEN
            -- Close current record
            UPDATE dim_customer
            SET expiry_date = CURRENT_DATE - 1,
                is_current = false
            WHERE customer_id = p_customer_id
            AND is_current = true;
            
            -- Insert new version
            INSERT INTO dim_customer (
                customer_id, name, email, city,
                effective_date, expiry_date, is_current, version
            ) VALUES (
                p_customer_id, p_name, p_email, p_city,
                CURRENT_DATE, '9999-12-31', true, current_record.version + 1
            );
        END IF;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### Bridge Table Pattern
```sql
-- Many-to-many relationship handling
CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    date_key INTEGER,
    customer_key INTEGER,
    product_group_key INTEGER, -- Points to bridge table
    amount DECIMAL(10,2)
);

CREATE TABLE bridge_product_group (
    product_group_key SERIAL PRIMARY KEY,
    product_key INTEGER,
    weight_factor DECIMAL(5,4) DEFAULT 1.0
);

-- Query with bridge table
SELECT 
    fs.sale_id,
    fs.amount,
    fs.amount * bpg.weight_factor as allocated_amount,
    dp.product_name
FROM fact_sales fs
JOIN bridge_product_group bpg ON fs.product_group_key = bpg.product_group_key
JOIN dim_product dp ON bpg.product_key = dp.product_key;
```

## Performance Optimization Patterns

### Partitioning Strategies
```sql
-- Range partitioning by date
CREATE TABLE sales_data (
    id SERIAL,
    sale_date DATE,
    amount DECIMAL(10,2),
    customer_id INTEGER
) PARTITION BY RANGE (sale_date);

-- Create monthly partitions
CREATE TABLE sales_data_2023_01 PARTITION OF sales_data
FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');

CREATE TABLE sales_data_2023_02 PARTITION OF sales_data
FOR VALUES FROM ('2023-02-01') TO ('2023-03-01');

-- Hash partitioning for even distribution
CREATE TABLE user_activity (
    user_id INTEGER,
    activity_date DATE,
    activity_type VARCHAR(50)
) PARTITION BY HASH (user_id);

CREATE TABLE user_activity_0 PARTITION OF user_activity
FOR VALUES WITH (MODULUS 4, REMAINDER 0);
```

### Materialized View Patterns
```sql
-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    product_category,
    COUNT(*) as order_count,
    SUM(order_amount) as total_sales,
    AVG(order_amount) as avg_order_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY DATE_TRUNC('month', order_date), product_category;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_sales_summary;

-- Incremental refresh pattern
CREATE OR REPLACE FUNCTION refresh_monthly_sales()
RETURNS VOID AS $$
BEGIN
    -- Delete current month data
    DELETE FROM monthly_sales_summary 
    WHERE month = DATE_TRUNC('month', CURRENT_DATE);
    
    -- Insert updated current month data
    INSERT INTO monthly_sales_summary
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        product_category,
        COUNT(*) as order_count,
        SUM(order_amount) as total_sales,
        AVG(order_amount) as avg_order_value
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    WHERE DATE_TRUNC('month', order_date) = DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY DATE_TRUNC('month', order_date), product_category;
END;
$$ LANGUAGE plpgsql;
```

## 🚀 Advanced Patterns

### Bulk Data Processing
```sql
-- Batch processing with cursor
CREATE OR REPLACE FUNCTION process_large_dataset()
RETURNS VOID AS $$
DECLARE
    batch_size INTEGER := 10000;
    processed_count INTEGER := 0;
    batch_cursor CURSOR FOR 
        SELECT customer_id, order_amount 
        FROM orders 
        WHERE status = 'PENDING'
        ORDER BY order_id;
    batch_record RECORD;
BEGIN
    OPEN batch_cursor;
    
    LOOP
        FETCH batch_cursor INTO batch_record;
        EXIT WHEN NOT FOUND;
        
        -- Process individual record
        UPDATE customers 
        SET total_spent = total_spent + batch_record.order_amount
        WHERE customer_id = batch_record.customer_id;
        
        processed_count := processed_count + 1;
        
        -- Commit in batches
        IF processed_count % batch_size = 0 THEN
            COMMIT;
            RAISE NOTICE 'Processed % records', processed_count;
        END IF;
    END LOOP;
    
    CLOSE batch_cursor;
    COMMIT;
    RAISE NOTICE 'Total processed: % records', processed_count;
END;
$$ LANGUAGE plpgsql;
```

### Data Pipeline Orchestration
```sql
-- Pipeline status tracking
CREATE TABLE pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20), -- 'RUNNING', 'SUCCESS', 'FAILED'
    records_processed INTEGER,
    error_message TEXT
);

-- Pipeline execution function
CREATE OR REPLACE FUNCTION execute_data_pipeline(p_pipeline_name VARCHAR)
RETURNS INTEGER AS $$
DECLARE
    run_id INTEGER;
    records_count INTEGER := 0;
BEGIN
    -- Start pipeline run
    INSERT INTO pipeline_runs (pipeline_name, status)
    VALUES (p_pipeline_name, 'RUNNING')
    RETURNING pipeline_runs.run_id INTO run_id;
    
    BEGIN
        -- Execute pipeline steps
        CASE p_pipeline_name
            WHEN 'customer_etl' THEN
                PERFORM extract_customer_data();
                PERFORM transform_customer_data();
                PERFORM load_customer_data();
                SELECT COUNT(*) INTO records_count FROM staging_customers;
            WHEN 'order_etl' THEN
                PERFORM extract_order_data();
                PERFORM transform_order_data();
                PERFORM load_order_data();
                SELECT COUNT(*) INTO records_count FROM staging_orders;
        END CASE;
        
        -- Mark as successful
        UPDATE pipeline_runs 
        SET status = 'SUCCESS',
            end_time = CURRENT_TIMESTAMP,
            records_processed = records_count
        WHERE pipeline_runs.run_id = execute_data_pipeline.run_id;
        
    EXCEPTION WHEN OTHERS THEN
        -- Mark as failed
        UPDATE pipeline_runs 
        SET status = 'FAILED',
            end_time = CURRENT_TIMESTAMP,
            error_message = SQLERRM
        WHERE pipeline_runs.run_id = execute_data_pipeline.run_id;
        
        RAISE;
    END;
    
    RETURN run_id;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Monitoring and Observability

### Performance Metrics Collection
```sql
-- Query performance tracking
CREATE TABLE query_performance_log (
    log_id SERIAL PRIMARY KEY,
    query_hash VARCHAR(64),
    query_text TEXT,
    execution_time_ms INTEGER,
    rows_affected INTEGER,
    execution_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(50),
    database_name VARCHAR(50)
);

-- Automatic performance logging
CREATE OR REPLACE FUNCTION log_query_performance()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO query_performance_log (
        query_hash,
        query_text,
        execution_time_ms,
        rows_affected,
        user_name,
        database_name
    ) VALUES (
        MD5(current_query()),
        current_query(),
        EXTRACT(MILLISECONDS FROM (clock_timestamp() - statement_timestamp())),
        TG_ROWCOUNT,
        current_user,
        current_database()
    );
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

## 🔧 Best Practices

### Error Handling
```sql
-- Comprehensive error handling pattern
CREATE OR REPLACE FUNCTION safe_data_operation()
RETURNS BOOLEAN AS $$
DECLARE
    operation_successful BOOLEAN := FALSE;
    error_context TEXT;
BEGIN
    BEGIN
        -- Perform data operation
        INSERT INTO target_table SELECT * FROM source_table;
        operation_successful := TRUE;
        
    EXCEPTION 
        WHEN unique_violation THEN
            GET STACKED DIAGNOSTICS error_context = PG_EXCEPTION_CONTEXT;
            RAISE WARNING 'Duplicate key violation: %', error_context;
            -- Handle duplicate key scenario
            
        WHEN foreign_key_violation THEN
            GET STACKED DIAGNOSTICS error_context = PG_EXCEPTION_CONTEXT;
            RAISE WARNING 'Foreign key violation: %', error_context;
            -- Handle referential integrity issue
            
        WHEN OTHERS THEN
            GET STACKED DIAGNOSTICS error_context = PG_EXCEPTION_CONTEXT;
            RAISE EXCEPTION 'Unexpected error: % Context: %', SQLERRM, error_context;
    END;
    
    RETURN operation_successful;
END;
$$ LANGUAGE plpgsql;
```

### Configuration Management
```sql
-- Configuration table for pipeline parameters
CREATE TABLE pipeline_config (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value TEXT,
    config_type VARCHAR(20), -- 'STRING', 'INTEGER', 'BOOLEAN', 'JSON'
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Configuration getter function
CREATE OR REPLACE FUNCTION get_config(p_key VARCHAR, p_default TEXT DEFAULT NULL)
RETURNS TEXT AS $$
DECLARE
    config_value TEXT;
BEGIN
    SELECT pipeline_config.config_value INTO config_value
    FROM pipeline_config
    WHERE config_key = p_key;
    
    RETURN COALESCE(config_value, p_default);
END;
$$ LANGUAGE plpgsql;
```

## 📚 Additional Resources

- **Performance Tuning**: Focus on indexing strategies and query optimization
- **Data Modeling**: Study dimensional modeling and normalization techniques
- **Monitoring**: Implement comprehensive logging and alerting
- **Testing**: Create data quality tests and validation procedures
- **Documentation**: Maintain clear documentation for all patterns and procedures

## 🎯 Next Steps

1. **Implement Gradually**: Start with basic patterns and build complexity
2. **Monitor Performance**: Track execution times and resource usage
3. **Test Thoroughly**: Validate data quality and pattern effectiveness
4. **Document Everything**: Maintain clear documentation for team knowledge sharing
5. **Iterate and Improve**: Continuously refine patterns based on real-world usage