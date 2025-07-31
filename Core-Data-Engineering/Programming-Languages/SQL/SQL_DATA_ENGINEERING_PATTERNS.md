# SQL Data Engineering Patterns

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