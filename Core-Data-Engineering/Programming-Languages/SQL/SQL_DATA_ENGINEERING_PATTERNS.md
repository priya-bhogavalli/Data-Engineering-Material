# SQL Data Engineering Patterns

## 📋 Table of Contents

1. [ETL/ELT Patterns](#etlelt-patterns)
2. [Data Quality Patterns](#data-quality-patterns)
3. [Dimensional Modeling Patterns](#dimensional-modeling-patterns)
4. [Performance Optimization Patterns](#performance-optimization-patterns)
5. [Data Pipeline Patterns](#data-pipeline-patterns)
6. [Data Transformation Patterns](#data-transformation-patterns)
7. [Error Handling and Monitoring Patterns](#error-handling-and-monitoring-patterns)
8. [Advanced Analytics Patterns](#advanced-analytics-patterns)
9. [Data Security and Compliance Patterns](#data-security-and-compliance-patterns)

---

## Overview

This document provides comprehensive SQL patterns specifically designed for data engineering workflows. Each pattern includes detailed explanations, use cases, and practical implementations that can be adapted to various data engineering scenarios.

**Key Benefits:**
- **Reusable Solutions**: Proven patterns for common data engineering challenges
- **Performance Optimized**: Efficient SQL implementations for large-scale data processing
- **Best Practices**: Industry-standard approaches to data pipeline development
- **Scalable Designs**: Patterns that work from small datasets to enterprise-scale implementations

---

## ETL/ELT Patterns

### Incremental Data Loading
**Concept**: Load only new or changed data since the last extraction, reducing processing time and resource usage.

**Key Benefits:**
- Faster processing compared to full loads
- Reduced network and storage overhead
- Maintains data freshness with minimal impact
- Enables near real-time data pipelines

**Implementation Strategies:**
- **Timestamp-based**: Use last_modified or created_date columns
- **Change flags**: Use status columns to identify changed records
- **Log-based**: Capture changes from database transaction logs
- **Hash comparison**: Compare record checksums to detect changes

```sql
-- Delta load using timestamps
INSERT INTO target_table
SELECT * FROM source_table
WHERE last_modified > (SELECT COALESCE(MAX(last_modified), '1900-01-01') FROM target_table);

-- Upsert pattern (MERGE statement)
MERGE INTO dim_customer AS target
USING staging_customer AS source ON target.customer_id = source.customer_id
WHEN MATCHED THEN UPDATE SET name = source.name, email = source.email
WHEN NOT MATCHED THEN INSERT VALUES (source.customer_id, source.name, source.email);
```

### Change Data Capture (CDC) Pattern
**Concept**: Automatically capture and track all data changes (INSERT, UPDATE, DELETE) in real-time for downstream processing.

**CDC Approaches:**
- **Trigger-based**: Database triggers capture changes (high overhead)
- **Log-based**: Read database transaction logs (low overhead, near real-time)
- **Timestamp-based**: Poll for changes using modification timestamps
- **Snapshot comparison**: Compare current vs previous snapshots

**Use Cases:**
- Real-time data replication
- Event-driven architectures
- Data synchronization between systems
- Audit trails and compliance
- Stream processing pipelines

**Trade-offs:**
- **Trigger-based**: Easy to implement but impacts source system performance
- **Log-based**: Minimal impact but requires specialized tools (Debezium, AWS DMS)

```sql
-- Simple audit table structure
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    operation VARCHAR(10),
    record_id INT,
    old_values JSONB,
    new_values JSONB,
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Trigger function for CDC
CREATE FUNCTION audit_trigger() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, operation, record_id, old_values, new_values)
    VALUES (TG_TABLE_NAME, TG_OP, COALESCE(NEW.id, OLD.id), 
            CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) END,
            CASE WHEN TG_OP != 'DELETE' THEN row_to_json(NEW) END);
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

### Data Deduplication Patterns
**Concept**: Identify and remove duplicate records to maintain data quality and prevent analytical errors.

**Deduplication Strategies:**
- **Exact matching**: Remove records with identical key fields
- **Fuzzy matching**: Use similarity algorithms for near-duplicates
- **Rule-based**: Apply business rules to determine duplicates
- **Machine learning**: Use clustering algorithms for complex deduplication

**Common Scenarios:**
- Customer data from multiple sources
- Product catalogs with variations
- Address standardization
- Email list cleaning

**Performance Considerations:**
- Use appropriate indexes on deduplication keys
- Process in batches for large datasets
- Consider using staging tables for complex logic

```sql
-- Remove exact duplicates, keep latest
WITH ranked_data AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_date DESC) as rn
    FROM customers
)
DELETE FROM customers WHERE id IN (
    SELECT id FROM ranked_data WHERE rn > 1
);

-- Fuzzy matching for similar records
SELECT a.id, b.id, SIMILARITY(a.name, b.name) as similarity
FROM customers a JOIN customers b ON a.id < b.id
WHERE SIMILARITY(a.name, b.name) > 0.85;
```

## Data Quality Patterns

### Data Validation Framework
**Concept**: Systematic approach to ensure data meets quality standards through automated checks and monitoring.

**Data Quality Dimensions:**
- **Completeness**: No missing values in required fields
- **Accuracy**: Data reflects real-world values correctly
- **Consistency**: Data follows defined formats and rules
- **Validity**: Data conforms to defined domains and constraints
- **Uniqueness**: No unwanted duplicate records
- **Timeliness**: Data is current and up-to-date

**Implementation Approach:**
- Define quality rules in metadata tables
- Create reusable validation functions
- Implement automated monitoring and alerting
- Generate quality reports and dashboards
- Establish data quality SLAs

**Best Practices:**
- Validate data at ingestion points
- Use statistical methods for anomaly detection
- Implement data profiling for new sources
- Create feedback loops for continuous improvement

```sql
-- Data quality rules configuration
CREATE TABLE dq_rules (
    rule_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    rule_type VARCHAR(50), -- 'NOT_NULL', 'UNIQUE', 'RANGE', 'FORMAT'
    column_name VARCHAR(100),
    rule_config JSONB,
    threshold DECIMAL(5,2) DEFAULT 95.0
);

-- Simple quality check examples
SELECT 'Completeness' as check_type, 
       COUNT(*) - COUNT(email) as null_count,
       ROUND(COUNT(email) * 100.0 / COUNT(*), 2) as completeness_pct
FROM customers;

SELECT 'Uniqueness' as check_type,
       COUNT(*) - COUNT(DISTINCT email) as duplicate_count
FROM customers;
```

### Outlier Detection
**Concept**: Identify data points that deviate significantly from normal patterns, which may indicate errors or exceptional cases.

**Detection Methods:**
- **Statistical**: Z-score, IQR (Interquartile Range), standard deviation
- **Machine Learning**: Isolation Forest, One-Class SVM, clustering
- **Domain-specific**: Business rules and thresholds
- **Time-series**: Seasonal decomposition, moving averages

**Use Cases:**
- Fraud detection in financial transactions
- Quality control in manufacturing data
- Network security anomaly detection
- Customer behavior analysis
- Sensor data validation

**Considerations:**
- Define appropriate thresholds based on business context
- Consider seasonal patterns in time-series data
- Balance between false positives and missed outliers
- Document and review outlier handling decisions

```sql
-- IQR method for outlier detection
WITH stats AS (
    SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) as q1,
           PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) as q3
    FROM transactions
)
SELECT t.*, 
       CASE WHEN t.amount < (q1 - 1.5 * (q3 - q1)) OR 
                 t.amount > (q3 + 1.5 * (q3 - q1)) 
            THEN 'OUTLIER' ELSE 'NORMAL' END as flag
FROM transactions t CROSS JOIN stats;

-- Z-score method
WITH stats AS (
    SELECT AVG(amount) as mean, STDDEV(amount) as std FROM transactions
)
SELECT *, ABS(amount - mean) / std as z_score
FROM transactions CROSS JOIN stats
WHERE ABS(amount - mean) / std > 3;
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
-- Incremental refresh materialized view
CREATE MATERIALIZED VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_spent,
    AVG(o.amount) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Refresh strategy with concurrency
REFRESH MATERIALIZED VIEW CONCURRENTLY customer_summary;

-- Conditional refresh based on data changes
CREATE OR REPLACE FUNCTION refresh_customer_summary_if_needed()
RETURNS BOOLEAN AS $$
DECLARE
    last_refresh TIMESTAMP;
    last_data_change TIMESTAMP;
BEGIN
    -- Get last refresh time
    SELECT last_refresh_time INTO last_refresh
    FROM materialized_view_refresh_log
    WHERE view_name = 'customer_summary';
    
    -- Get last data change time
    SELECT MAX(GREATEST(last_modified, created_at)) INTO last_data_change
    FROM (SELECT last_modified, created_at FROM customers
          UNION ALL
          SELECT last_modified, created_at FROM orders) t;
    
    -- Refresh if data changed since last refresh
    IF last_data_change > COALESCE(last_refresh, '1900-01-01') THEN
        REFRESH MATERIALIZED VIEW CONCURRENTLY customer_summary;
        
        INSERT INTO materialized_view_refresh_log (view_name, last_refresh_time)
        VALUES ('customer_summary', CURRENT_TIMESTAMP)
        ON CONFLICT (view_name) DO UPDATE SET last_refresh_time = CURRENT_TIMESTAMP;
        
        RETURN TRUE;
    END IF;
    
    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;
```

## Data Pipeline Patterns

### Batch Processing Pattern
**Description:** Process data in chunks to handle large datasets efficiently while maintaining system performance.

```sql
-- Batch processing with cursor and commit points
CREATE OR REPLACE FUNCTION process_large_dataset(
    batch_size INTEGER DEFAULT 10000,
    max_batches INTEGER DEFAULT NULL
)
RETURNS TABLE(batch_number INTEGER, records_processed INTEGER, processing_time INTERVAL) AS $$
DECLARE
    batch_count INTEGER := 0;
    total_processed INTEGER := 0;
    batch_start_time TIMESTAMP;
    batch_end_time TIMESTAMP;
    cur CURSOR FOR 
        SELECT customer_id, email, registration_date
        FROM customers
        WHERE processed = FALSE
        ORDER BY customer_id;
    customer_record RECORD;
BEGIN
    OPEN cur;
    
    LOOP
        batch_count := batch_count + 1;
        batch_start_time := clock_timestamp();
        
        -- Process batch
        FOR i IN 1..batch_size LOOP
            FETCH cur INTO customer_record;
            EXIT WHEN NOT FOUND;
            
            -- Process individual record
            UPDATE customers 
            SET processed = TRUE,
                processed_date = CURRENT_TIMESTAMP
            WHERE customer_id = customer_record.customer_id;
            
            total_processed := total_processed + 1;
        END LOOP;
        
        batch_end_time := clock_timestamp();
        
        -- Return batch statistics
        RETURN QUERY SELECT 
            batch_count,
            LEAST(batch_size, total_processed - (batch_count - 1) * batch_size),
            batch_end_time - batch_start_time;
        
        -- Commit transaction
        COMMIT;
        
        -- Exit conditions
        EXIT WHEN NOT FOUND;
        EXIT WHEN max_batches IS NOT NULL AND batch_count >= max_batches;
    END LOOP;
    
    CLOSE cur;
END;
$$ LANGUAGE plpgsql;
```

### Stream Processing Simulation
**Description:** Simulate real-time data processing using SQL for continuous data ingestion and transformation.

```sql
-- Event-driven processing pattern
CREATE TABLE event_stream (
    event_id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    event_data JSONB,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- Stream processor function
CREATE OR REPLACE FUNCTION process_event_stream()
RETURNS TABLE(events_processed INTEGER, processing_errors INTEGER) AS $$
DECLARE
    event_record RECORD;
    processed_count INTEGER := 0;
    error_count INTEGER := 0;
BEGIN
    FOR event_record IN 
        SELECT * FROM event_stream 
        WHERE processed = FALSE 
        ORDER BY event_timestamp
        LIMIT 1000
    LOOP
        BEGIN
            -- Process based on event type
            CASE event_record.event_type
                WHEN 'user_registration' THEN
                    INSERT INTO users (email, name, registration_date)
                    SELECT 
                        event_record.event_data->>'email',
                        event_record.event_data->>'name',
                        event_record.event_timestamp;
                        
                WHEN 'order_placed' THEN
                    INSERT INTO orders (customer_id, amount, order_date)
                    SELECT 
                        (event_record.event_data->>'customer_id')::INTEGER,
                        (event_record.event_data->>'amount')::DECIMAL,
                        event_record.event_timestamp;
                        
                WHEN 'payment_processed' THEN
                    UPDATE orders 
                    SET status = 'PAID',
                        payment_date = event_record.event_timestamp
                    WHERE order_id = (event_record.event_data->>'order_id')::INTEGER;
            END CASE;
            
            -- Mark as processed
            UPDATE event_stream 
            SET processed = TRUE 
            WHERE event_id = event_record.event_id;
            
            processed_count := processed_count + 1;
            
        EXCEPTION WHEN OTHERS THEN
            -- Log error and continue
            INSERT INTO processing_errors (event_id, error_message, error_timestamp)
            VALUES (event_record.event_id, SQLERRM, CURRENT_TIMESTAMP);
            
            error_count := error_count + 1;
        END;
    END LOOP;
    
    RETURN QUERY SELECT processed_count, error_count;
END;
$$ LANGUAGE plpgsql;
```

## Data Transformation Patterns

### Pivot and Unpivot Operations
**Description:** Transform data between row and column representations for different analytical needs.

```sql
-- Dynamic pivot using conditional aggregation
WITH sales_data AS (
    SELECT 
        product_name,
        EXTRACT(MONTH FROM sale_date) as month,
        amount
    FROM sales
    WHERE EXTRACT(YEAR FROM sale_date) = 2023
)
SELECT 
    product_name,
    SUM(CASE WHEN month = 1 THEN amount ELSE 0 END) as jan_sales,
    SUM(CASE WHEN month = 2 THEN amount ELSE 0 END) as feb_sales,
    SUM(CASE WHEN month = 3 THEN amount ELSE 0 END) as mar_sales,
    SUM(CASE WHEN month = 4 THEN amount ELSE 0 END) as apr_sales,
    SUM(amount) as total_sales
FROM sales_data
GROUP BY product_name;

-- Unpivot operation using UNION ALL
WITH monthly_sales AS (
    SELECT product_name, jan_sales, feb_sales, mar_sales, apr_sales
    FROM product_monthly_summary
)
SELECT product_name, 'January' as month, jan_sales as amount FROM monthly_sales WHERE jan_sales > 0
UNION ALL
SELECT product_name, 'February' as month, feb_sales as amount FROM monthly_sales WHERE feb_sales > 0
UNION ALL
SELECT product_name, 'March' as month, mar_sales as amount FROM monthly_sales WHERE mar_sales > 0
UNION ALL
SELECT product_name, 'April' as month, apr_sales as amount FROM monthly_sales WHERE apr_sales > 0;
```

### Data Enrichment Patterns
**Description:** Enhance raw data with additional context, calculations, and derived attributes.

```sql
-- Geospatial enrichment
WITH enriched_customers AS (
    SELECT 
        c.*,
        -- Add geographic information
        CASE 
            WHEN c.state IN ('CA', 'OR', 'WA') THEN 'West Coast'
            WHEN c.state IN ('NY', 'NJ', 'CT', 'MA') THEN 'Northeast'
            WHEN c.state IN ('TX', 'FL', 'GA', 'NC') THEN 'South'
            ELSE 'Other'
        END as region,
        
        -- Add customer segmentation
        CASE 
            WHEN total_spent > 10000 THEN 'VIP'
            WHEN total_spent > 5000 THEN 'Premium'
            WHEN total_spent > 1000 THEN 'Regular'
            ELSE 'New'
        END as customer_segment,
        
        -- Add time-based attributes
        EXTRACT(DAYS FROM CURRENT_DATE - registration_date) as days_since_registration,
        DATE_TRUNC('quarter', registration_date) as registration_quarter
        
    FROM customers c
    LEFT JOIN (
        SELECT customer_id, SUM(amount) as total_spent
        FROM orders
        GROUP BY customer_id
    ) o ON c.customer_id = o.customer_id
)
SELECT * FROM enriched_customers;
```

## Error Handling and Monitoring Patterns

### Comprehensive Error Handling
**Description:** Implement robust error handling with logging, retry mechanisms, and graceful degradation.

```sql
-- Error handling with retry logic
CREATE OR REPLACE FUNCTION safe_data_processing(
    p_batch_id INTEGER,
    p_max_retries INTEGER DEFAULT 3
)
RETURNS TABLE(status TEXT, records_processed INTEGER, errors_encountered INTEGER) AS $$
DECLARE
    retry_count INTEGER := 0;
    processing_successful BOOLEAN := FALSE;
    current_error TEXT;
    processed_records INTEGER := 0;
    error_records INTEGER := 0;
BEGIN
    WHILE retry_count <= p_max_retries AND NOT processing_successful LOOP
        BEGIN
            -- Main processing logic
            WITH batch_data AS (
                SELECT * FROM staging_table 
                WHERE batch_id = p_batch_id
                AND processing_status = 'PENDING'
            )
            INSERT INTO target_table (customer_id, name, email, processed_date)
            SELECT 
                customer_id,
                TRIM(UPPER(name)),
                LOWER(email),
                CURRENT_TIMESTAMP
            FROM batch_data
            WHERE email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
            
            GET DIAGNOSTICS processed_records = ROW_COUNT;
            
            -- Update processing status
            UPDATE staging_table 
            SET processing_status = 'COMPLETED',
                processed_date = CURRENT_TIMESTAMP
            WHERE batch_id = p_batch_id;
            
            processing_successful := TRUE;
            
        EXCEPTION 
            WHEN OTHERS THEN
                current_error := SQLERRM;
                retry_count := retry_count + 1;
                
                -- Log error
                INSERT INTO processing_errors (
                    batch_id, retry_attempt, error_message, error_timestamp
                ) VALUES (
                    p_batch_id, retry_count, current_error, CURRENT_TIMESTAMP
                );
                
                -- Wait before retry (simulate with pg_sleep)
                PERFORM pg_sleep(retry_count * 2); -- Exponential backoff
        END;
    END LOOP;
    
    -- Handle failed records
    IF NOT processing_successful THEN
        UPDATE staging_table 
        SET processing_status = 'FAILED',
            error_message = current_error
        WHERE batch_id = p_batch_id;
        
        SELECT COUNT(*) INTO error_records
        FROM staging_table 
        WHERE batch_id = p_batch_id AND processing_status = 'FAILED';
    END IF;
    
    RETURN QUERY SELECT 
        CASE WHEN processing_successful THEN 'SUCCESS' ELSE 'FAILED' END,
        processed_records,
        error_records;
END;
$$ LANGUAGE plpgsql;
```

### Data Pipeline Monitoring
**Description:** Monitor data pipeline health, performance, and data quality metrics.

```sql
-- Pipeline monitoring framework
CREATE TABLE pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20), -- 'RUNNING', 'SUCCESS', 'FAILED', 'CANCELLED'
    records_processed INTEGER,
    records_failed INTEGER,
    execution_time_seconds INTEGER,
    error_message TEXT,
    metadata JSONB
);

-- Pipeline execution wrapper
CREATE OR REPLACE FUNCTION execute_pipeline(
    p_pipeline_name VARCHAR,
    p_pipeline_function VARCHAR,
    p_parameters JSONB DEFAULT '{}'
)
RETURNS INTEGER AS $$
DECLARE
    run_id INTEGER;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    execution_result RECORD;
    error_msg TEXT;
BEGIN
    start_time := CURRENT_TIMESTAMP;
    
    -- Create pipeline run record
    INSERT INTO pipeline_runs (pipeline_name, start_time, status, metadata)
    VALUES (p_pipeline_name, start_time, 'RUNNING', p_parameters)
    RETURNING pipeline_runs.run_id INTO run_id;
    
    BEGIN
        -- Execute pipeline function dynamically
        EXECUTE format('SELECT * FROM %I(%L)', p_pipeline_function, p_parameters::TEXT)
        INTO execution_result;
        
        end_time := CURRENT_TIMESTAMP;
        
        -- Update success status
        UPDATE pipeline_runs
        SET 
            end_time = end_time,
            status = 'SUCCESS',
            execution_time_seconds = EXTRACT(EPOCH FROM (end_time - start_time)),
            records_processed = COALESCE(execution_result.records_processed, 0),
            records_failed = COALESCE(execution_result.records_failed, 0)
        WHERE pipeline_runs.run_id = execute_pipeline.run_id;
        
    EXCEPTION WHEN OTHERS THEN
        error_msg := SQLERRM;
        end_time := CURRENT_TIMESTAMP;
        
        -- Update failure status
        UPDATE pipeline_runs
        SET 
            end_time = end_time,
            status = 'FAILED',
            execution_time_seconds = EXTRACT(EPOCH FROM (end_time - start_time)),
            error_message = error_msg
        WHERE pipeline_runs.run_id = execute_pipeline.run_id;
        
        -- Re-raise exception
        RAISE;
    END;
    
    RETURN run_id;
END;
$$ LANGUAGE plpgsql;

-- Pipeline health check
CREATE OR REPLACE FUNCTION check_pipeline_health()
RETURNS TABLE(
    pipeline_name VARCHAR,
    last_run_status VARCHAR,
    last_run_time TIMESTAMP,
    avg_execution_time_minutes DECIMAL,
    success_rate_24h DECIMAL,
    health_status VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    WITH pipeline_stats AS (
        SELECT 
            pr.pipeline_name,
            pr.status as last_run_status,
            pr.start_time as last_run_time,
            AVG(pr.execution_time_seconds) / 60.0 as avg_execution_time_minutes,
            COUNT(CASE WHEN pr.status = 'SUCCESS' THEN 1 END)::DECIMAL / COUNT(*) * 100 as success_rate_24h,
            ROW_NUMBER() OVER (PARTITION BY pr.pipeline_name ORDER BY pr.start_time DESC) as rn
        FROM pipeline_runs pr
        WHERE pr.start_time >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
        GROUP BY pr.pipeline_name, pr.status, pr.start_time
    )
    SELECT 
        ps.pipeline_name,
        ps.last_run_status,
        ps.last_run_time,
        ps.avg_execution_time_minutes,
        ps.success_rate_24h,
        CASE 
            WHEN ps.success_rate_24h >= 95 AND ps.last_run_status = 'SUCCESS' THEN 'HEALTHY'
            WHEN ps.success_rate_24h >= 80 THEN 'WARNING'
            ELSE 'CRITICAL'
        END as health_status
    FROM pipeline_stats ps
    WHERE ps.rn = 1;
END;
$$ LANGUAGE plpgsql;
```

## Advanced Analytics Patterns

### Time Series Analysis
**Description:** Analyze temporal data patterns, trends, and seasonality using SQL window functions.

```sql
-- Time series analysis with moving averages and trend detection
WITH daily_metrics AS (
    SELECT 
        DATE(order_date) as metric_date,
        COUNT(*) as daily_orders,
        SUM(amount) as daily_revenue,
        AVG(amount) as avg_order_value
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY DATE(order_date)
),
time_series_analysis AS (
    SELECT 
        metric_date,
        daily_orders,
        daily_revenue,
        avg_order_value,
        
        -- Moving averages
        AVG(daily_revenue) OVER (
            ORDER BY metric_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as revenue_7day_ma,
        
        AVG(daily_revenue) OVER (
            ORDER BY metric_date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) as revenue_30day_ma,
        
        -- Lag functions for trend analysis
        LAG(daily_revenue, 1) OVER (ORDER BY metric_date) as prev_day_revenue,
        LAG(daily_revenue, 7) OVER (ORDER BY metric_date) as prev_week_revenue,
        
        -- Percentile rankings
        PERCENT_RANK() OVER (ORDER BY daily_revenue) as revenue_percentile
        
    FROM daily_metrics
)
SELECT 
    *,
    -- Trend indicators
    CASE 
        WHEN daily_revenue > prev_day_revenue THEN 'UP'
        WHEN daily_revenue < prev_day_revenue THEN 'DOWN'
        ELSE 'FLAT'
    END as daily_trend,
    
    CASE 
        WHEN daily_revenue > prev_week_revenue * 1.1 THEN 'STRONG_GROWTH'
        WHEN daily_revenue > prev_week_revenue THEN 'GROWTH'
        WHEN daily_revenue < prev_week_revenue * 0.9 THEN 'DECLINE'
        ELSE 'STABLE'
    END as weekly_trend,
    
    -- Anomaly detection
    CASE 
        WHEN revenue_percentile > 0.95 THEN 'HIGH_ANOMALY'
        WHEN revenue_percentile < 0.05 THEN 'LOW_ANOMALY'
        ELSE 'NORMAL'
    END as anomaly_flag
    
FROM time_series_analysis
ORDER BY metric_date;
```

### Cohort Analysis
**Description:** Analyze user behavior and retention patterns over time using cohort-based segmentation.

```sql
-- Customer cohort analysis
WITH customer_cohorts AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month,
        MIN(order_date) as first_order_date
    FROM orders
    GROUP BY customer_id
),
cohort_data AS (
    SELECT 
        cc.cohort_month,
        DATE_TRUNC('month', o.order_date) as order_month,
        EXTRACT(EPOCH FROM (DATE_TRUNC('month', o.order_date) - cc.cohort_month)) / (30.44 * 24 * 3600) as period_number,
        COUNT(DISTINCT o.customer_id) as customers,
        SUM(o.amount) as revenue
    FROM customer_cohorts cc
    JOIN orders o ON cc.customer_id = o.customer_id
    GROUP BY cc.cohort_month, DATE_TRUNC('month', o.order_date)
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) as cohort_size
    FROM customer_cohorts
    GROUP BY cohort_month
)
SELECT 
    cd.cohort_month,
    cd.period_number,
    cd.customers,
    cs.cohort_size,
    ROUND(cd.customers::DECIMAL / cs.cohort_size * 100, 2) as retention_rate,
    cd.revenue,
    ROUND(cd.revenue / cd.customers, 2) as revenue_per_customer
FROM cohort_data cd
JOIN cohort_sizes cs ON cd.cohort_month = cs.cohort_month
WHERE cd.period_number <= 12 -- First 12 months
ORDER BY cd.cohort_month, cd.period_number;
```

## Data Security and Compliance Patterns

### Data Masking and Anonymization
**Description:** Protect sensitive data while maintaining analytical value through various masking techniques.

```sql
-- Comprehensive data masking functions
CREATE OR REPLACE FUNCTION mask_email(email TEXT)
RETURNS TEXT AS $$
BEGIN
    IF email IS NULL OR email = '' THEN
        RETURN email;
    END IF;
    
    RETURN CONCAT(
        LEFT(email, 2),
        REPEAT('*', GREATEST(0, POSITION('@' IN email) - 3)),
        RIGHT(SPLIT_PART(email, '@', 1), 1),
        '@',
        LEFT(SPLIT_PART(email, '@', 2), 1),
        REPEAT('*', GREATEST(0, LENGTH(SPLIT_PART(email, '@', 2)) - 5)),
        RIGHT(SPLIT_PART(email, '@', 2), 4)
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION mask_phone(phone TEXT)
RETURNS TEXT AS $$
BEGIN
    IF phone IS NULL OR LENGTH(phone) < 4 THEN
        RETURN phone;
    END IF;
    
    RETURN CONCAT(
        REPEAT('X', LENGTH(phone) - 4),
        RIGHT(phone, 4)
    );
END;
$$ LANGUAGE plpgsql;

-- Dynamic data masking view
CREATE OR REPLACE VIEW customers_masked AS
SELECT 
    customer_id,
    CASE 
        WHEN current_setting('app.user_role', true) = 'admin' THEN name
        ELSE 'Customer_' || customer_id
    END as name,
    CASE 
        WHEN current_setting('app.user_role', true) IN ('admin', 'analyst') THEN email
        ELSE mask_email(email)
    END as email,
    CASE 
        WHEN current_setting('app.user_role', true) = 'admin' THEN phone
        ELSE mask_phone(phone)
    END as phone,
    registration_date,
    city,
    state
FROM customers;
```

### Audit Trail Implementation
**Description:** Comprehensive audit logging for compliance and security monitoring.

```sql
-- Comprehensive audit trail system
CREATE TABLE audit_trail (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    record_id VARCHAR(100),
    operation_type VARCHAR(10), -- INSERT, UPDATE, DELETE, SELECT
    old_values JSONB,
    new_values JSONB,
    changed_fields TEXT[],
    user_id VARCHAR(100),
    session_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    application_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_id BIGINT DEFAULT txid_current()
);

-- Generic audit trigger function
CREATE OR REPLACE FUNCTION generic_audit_trigger()
RETURNS TRIGGER AS $$
DECLARE
    old_data JSONB;
    new_data JSONB;
    changed_fields TEXT[] := ARRAY[]::TEXT[];
    field_name TEXT;
BEGIN
    -- Prepare data based on operation
    IF TG_OP = 'DELETE' THEN
        old_data := row_to_json(OLD);
        new_data := NULL;
    ELSIF TG_OP = 'INSERT' THEN
        old_data := NULL;
        new_data := row_to_json(NEW);
    ELSIF TG_OP = 'UPDATE' THEN
        old_data := row_to_json(OLD);
        new_data := row_to_json(NEW);
        
        -- Identify changed fields
        FOR field_name IN SELECT jsonb_object_keys(new_data) LOOP
            IF old_data->field_name IS DISTINCT FROM new_data->field_name THEN
                changed_fields := array_append(changed_fields, field_name);
            END IF;
        END LOOP;
    END IF;
    
    -- Insert audit record
    INSERT INTO audit_trail (
        table_name,
        record_id,
        operation_type,
        old_values,
        new_values,
        changed_fields,
        user_id,
        session_id,
        ip_address,
        application_name
    ) VALUES (
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id)::TEXT,
        TG_OP,
        old_data,
        new_data,
        changed_fields,
        current_setting('app.user_id', true),
        current_setting('app.session_id', true),
        current_setting('app.client_ip', true)::INET,
        current_setting('application_name', true)
    );
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger to sensitive tables
CREATE TRIGGER customers_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION generic_audit_trigger();
```

These SQL patterns provide a comprehensive foundation for data engineering tasks, covering everything from basic ETL operations to advanced analytics and security implementations. Each pattern includes detailed descriptions and practical examples that can be adapted to specific use cases.
-- Aggregated materialized view
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT 
    DATE(order_date) as sale_date,
    COUNT(*) as order_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    COUNT(DISTINCT customer_id) as unique_customers
FROM orders
GROUP BY DATE(order_date);

-- Create index on materialized view
CREATE INDEX idx_mv_daily_sales_date ON mv_daily_sales (sale_date);

-- Refresh strategy
CREATE OR REPLACE FUNCTION refresh_daily_sales_mv()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;
END;
$$ LANGUAGE plpgsql;
```

### Query Optimization Patterns
```sql
-- Efficient pagination
SELECT *
FROM (
    SELECT *, ROW_NUMBER() OVER (ORDER BY created_at DESC) as rn
    FROM large_table
    WHERE status = 'active'
) ranked
WHERE rn BETWEEN 1001 AND 1100;

-- Batch processing pattern
DO $$
DECLARE
    batch_size INTEGER := 1000;
    processed INTEGER := 0;
    total_rows INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_rows FROM source_table WHERE processed = false;
    
    WHILE processed < total_rows LOOP
        WITH batch AS (
            SELECT id
            FROM source_table
            WHERE processed = false
            ORDER BY id
            LIMIT batch_size
        )
        UPDATE source_table
        SET processed = true,
            processed_at = CURRENT_TIMESTAMP
        WHERE id IN (SELECT id FROM batch);
        
        processed := processed + batch_size;
        COMMIT;
        
        -- Optional: Add delay to prevent overwhelming the system
        PERFORM pg_sleep(0.1);
    END LOOP;
END $$;
```

## Data Pipeline Patterns

### Idempotent Operations
```sql
-- Idempotent insert pattern
INSERT INTO target_table (id, name, value, created_at)
SELECT id, name, value, created_at
FROM source_table s
WHERE NOT EXISTS (
    SELECT 1 FROM target_table t
    WHERE t.id = s.id
);

-- Idempotent update pattern with checksum
UPDATE target_table t
SET 
    name = s.name,
    value = s.value,
    updated_at = CURRENT_TIMESTAMP,
    checksum = MD5(s.name || s.value)
FROM source_table s
WHERE t.id = s.id
AND t.checksum != MD5(s.name || s.value);
```

### Error Handling and Logging
```sql
-- Error logging table
CREATE TABLE etl_log (
    log_id SERIAL PRIMARY KEY,
    job_name VARCHAR(100),
    step_name VARCHAR(100),
    status VARCHAR(20), -- SUCCESS, ERROR, WARNING
    message TEXT,
    rows_processed INTEGER,
    execution_time INTERVAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ETL procedure with error handling
CREATE OR REPLACE FUNCTION process_customer_data()
RETURNS VOID AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    rows_affected INTEGER;
    error_message TEXT;
BEGIN
    start_time := CURRENT_TIMESTAMP;
    
    BEGIN
        -- Main processing logic
        INSERT INTO dim_customer (customer_id, name, email)
        SELECT customer_id, name, email
        FROM staging_customer
        WHERE customer_id NOT IN (SELECT customer_id FROM dim_customer);
        
        GET DIAGNOSTICS rows_affected = ROW_COUNT;
        end_time := CURRENT_TIMESTAMP;
        
        -- Log success
        INSERT INTO etl_log (job_name, step_name, status, rows_processed, execution_time)
        VALUES ('customer_etl', 'load_dimension', 'SUCCESS', rows_affected, end_time - start_time);
        
    EXCEPTION WHEN OTHERS THEN
        GET STACKED DIAGNOSTICS error_message = MESSAGE_TEXT;
        end_time := CURRENT_TIMESTAMP;
        
        -- Log error
        INSERT INTO etl_log (job_name, step_name, status, message, execution_time)
        VALUES ('customer_etl', 'load_dimension', 'ERROR', error_message, end_time - start_time);
        
        RAISE;
    END;
END;
$$ LANGUAGE plpgsql;
```

## Real-time Processing Patterns

### Event Sourcing Pattern
```sql
-- Event store table
CREATE TABLE event_store (
    event_id SERIAL PRIMARY KEY,
    aggregate_id UUID,
    event_type VARCHAR(100),
    event_data JSONB,
    event_version INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projection table
CREATE TABLE customer_projection (
    customer_id UUID PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    status VARCHAR(50),
    last_event_version INTEGER,
    updated_at TIMESTAMP
);

-- Event processing function
CREATE OR REPLACE FUNCTION process_customer_events()
RETURNS VOID AS $$
DECLARE
    event_record RECORD;
BEGIN
    FOR event_record IN
        SELECT * FROM event_store
        WHERE event_type LIKE 'customer_%'
        AND event_id > (
            SELECT COALESCE(MAX(last_processed_event_id), 0)
            FROM event_processing_checkpoint
            WHERE processor_name = 'customer_projection'
        )
        ORDER BY event_id
    LOOP
        CASE event_record.event_type
            WHEN 'customer_created' THEN
                INSERT INTO customer_projection (
                    customer_id, name, email, status, last_event_version, updated_at
                ) VALUES (
                    event_record.aggregate_id,
                    event_record.event_data->>'name',
                    event_record.event_data->>'email',
                    'active',
                    event_record.event_version,
                    event_record.created_at
                );
            
            WHEN 'customer_updated' THEN
                UPDATE customer_projection
                SET name = event_record.event_data->>'name',
                    email = event_record.event_data->>'email',
                    last_event_version = event_record.event_version,
                    updated_at = event_record.created_at
                WHERE customer_id = event_record.aggregate_id;
                
            WHEN 'customer_deleted' THEN
                UPDATE customer_projection
                SET status = 'deleted',
                    last_event_version = event_record.event_version,
                    updated_at = event_record.created_at
                WHERE customer_id = event_record.aggregate_id;
        END CASE;
    END LOOP;
    
    -- Update checkpoint
    UPDATE event_processing_checkpoint
    SET last_processed_event_id = (SELECT MAX(event_id) FROM event_store)
    WHERE processor_name = 'customer_projection';
END;
$$ LANGUAGE plpgsql;
```

### Streaming Aggregation Pattern
```sql
-- Time-windowed aggregations
WITH time_windows AS (
    SELECT 
        DATE_TRUNC('hour', event_timestamp) as window_start,
        DATE_TRUNC('hour', event_timestamp) + INTERVAL '1 hour' as window_end,
        user_id,
        COUNT(*) as event_count,
        SUM(CASE WHEN event_type = 'purchase' THEN amount ELSE 0 END) as total_purchases
    FROM user_events
    WHERE event_timestamp >= NOW() - INTERVAL '24 hours'
    GROUP BY DATE_TRUNC('hour', event_timestamp), user_id
)
SELECT 
    window_start,
    window_end,
    user_id,
    event_count,
    total_purchases,
    LAG(event_count) OVER (PARTITION BY user_id ORDER BY window_start) as prev_hour_events
FROM time_windows
ORDER BY user_id, window_start;
```

## Data Archival and Retention Patterns

### Automated Data Archival
```sql
-- Archive old data procedure
CREATE OR REPLACE FUNCTION archive_old_transactions()
RETURNS INTEGER AS $$
DECLARE
    archived_count INTEGER;
    cutoff_date DATE;
BEGIN
    cutoff_date := CURRENT_DATE - INTERVAL '7 years';
    
    -- Move to archive table
    WITH archived_data AS (
        DELETE FROM transactions
        WHERE transaction_date < cutoff_date
        RETURNING *
    )
    INSERT INTO transactions_archive
    SELECT * FROM archived_data;
    
    GET DIAGNOSTICS archived_count = ROW_COUNT;
    
    -- Log archival activity
    INSERT INTO data_maintenance_log (
        operation_type, table_name, records_affected, cutoff_date
    ) VALUES (
        'ARCHIVE', 'transactions', archived_count, cutoff_date
    );
    
    RETURN archived_count;
END;
$$ LANGUAGE plpgsql;
```

### Data Retention Policy
```sql
-- Retention policy configuration
CREATE TABLE data_retention_policies (
    table_name VARCHAR(100) PRIMARY KEY,
    retention_period INTERVAL,
    date_column VARCHAR(100),
    archive_before_delete BOOLEAN DEFAULT true,
    is_active BOOLEAN DEFAULT true
);

-- Generic retention enforcement
CREATE OR REPLACE FUNCTION enforce_retention_policies()
RETURNS VOID AS $$
DECLARE
    policy_record RECORD;
    sql_command TEXT;
    cutoff_date TIMESTAMP;
    affected_rows INTEGER;
BEGIN
    FOR policy_record IN
        SELECT * FROM data_retention_policies WHERE is_active = true
    LOOP
        cutoff_date := CURRENT_TIMESTAMP - policy_record.retention_period;
        
        IF policy_record.archive_before_delete THEN
            -- Archive first
            sql_command := format(
                'INSERT INTO %I_archive SELECT * FROM %I WHERE %I < %L',
                policy_record.table_name,
                policy_record.table_name,
                policy_record.date_column,
                cutoff_date
            );
            EXECUTE sql_command;
        END IF;
        
        -- Delete old records
        sql_command := format(
            'DELETE FROM %I WHERE %I < %L',
            policy_record.table_name,
            policy_record.date_column,
            cutoff_date
        );
        EXECUTE sql_command;
        GET DIAGNOSTICS affected_rows = ROW_COUNT;
        
        -- Log the operation
        INSERT INTO data_maintenance_log (
            operation_type, table_name, records_affected, cutoff_date
        ) VALUES (
            'RETENTION_DELETE', policy_record.table_name, affected_rows, cutoff_date
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## Best Practices for Data Engineering SQL

1. **Use transactions appropriately** - Wrap related operations in transactions
2. **Implement proper error handling** - Always include exception handling in procedures
3. **Log operations** - Maintain audit trails for data operations
4. **Make operations idempotent** - Ensure operations can be safely repeated
5. **Use appropriate data types** - Choose efficient data types for storage and processing
6. **Implement data validation** - Validate data quality at multiple stages
7. **Optimize for your workload** - Design indexes and partitions based on query patterns
8. **Monitor performance** - Regularly analyze query performance and optimize
9. **Document your patterns** - Maintain clear documentation for complex patterns
10. **Test with realistic data volumes** - Ensure patterns work at scale