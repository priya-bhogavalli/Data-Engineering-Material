-- PostgreSQL Data Pipeline Example
-- Complete ETL pipeline with data quality checks and monitoring

-- =====================================================
-- 1. SETUP: Schemas and Extensions
-- =====================================================

-- Create schemas for data organization
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS monitoring;

-- Enable useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- =====================================================
-- 2. STAGING TABLES (Bronze Layer)
-- =====================================================

-- Raw customer data
CREATE TABLE staging.raw_customers (
    id SERIAL PRIMARY KEY,
    raw_data JSONB NOT NULL,
    source_file VARCHAR(255),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- Raw orders data
CREATE TABLE staging.raw_orders (
    id SERIAL PRIMARY KEY,
    raw_data JSONB NOT NULL,
    source_file VARCHAR(255),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- =====================================================
-- 3. WAREHOUSE TABLES (Silver/Gold Layer)
-- =====================================================

-- Customer dimension table
CREATE TABLE warehouse.dim_customers (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER UNIQUE NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    address JSONB,
    registration_date DATE,
    customer_segment VARCHAR(50),
    lifetime_value DECIMAL(12,2) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product dimension table
CREATE TABLE warehouse.dim_products (
    product_key SERIAL PRIMARY KEY,
    product_id INTEGER UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Date dimension table
CREATE TABLE warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    date_value DATE UNIQUE NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    day_of_month INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(20),
    week_of_year INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN DEFAULT FALSE
);

-- Sales fact table (partitioned by date)
CREATE TABLE warehouse.fact_sales (
    sale_key BIGSERIAL,
    customer_key INTEGER REFERENCES warehouse.dim_customers(customer_key),
    product_key INTEGER REFERENCES warehouse.dim_products(product_key),
    date_key INTEGER REFERENCES warehouse.dim_date(date_key),
    order_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    profit_amount DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (sale_key, date_key)
) PARTITION BY RANGE (date_key);

-- Create partitions for fact_sales
CREATE TABLE warehouse.fact_sales_2024_q1 PARTITION OF warehouse.fact_sales
FOR VALUES FROM (20240101) TO (20240401);

CREATE TABLE warehouse.fact_sales_2024_q2 PARTITION OF warehouse.fact_sales
FOR VALUES FROM (20240401) TO (20240701);

-- =====================================================
-- 4. INDEXES FOR PERFORMANCE
-- =====================================================

-- Staging table indexes
CREATE INDEX idx_raw_customers_processed ON staging.raw_customers(processed, loaded_at);
CREATE INDEX idx_raw_orders_processed ON staging.raw_orders(processed, loaded_at);
CREATE INDEX idx_raw_customers_gin ON staging.raw_customers USING GIN(raw_data);

-- Dimension table indexes
CREATE INDEX idx_dim_customers_segment ON warehouse.dim_customers(customer_segment);
CREATE INDEX idx_dim_customers_active ON warehouse.dim_customers(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_dim_products_category ON warehouse.dim_products(category, subcategory);
CREATE INDEX idx_dim_date_year_month ON warehouse.dim_date(year, month);

-- Fact table indexes
CREATE INDEX idx_fact_sales_customer ON warehouse.fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON warehouse.fact_sales(product_key);
CREATE INDEX idx_fact_sales_order ON warehouse.fact_sales(order_id);

-- =====================================================
-- 5. DATA QUALITY FRAMEWORK
-- =====================================================

-- Data quality rules table
CREATE TABLE monitoring.data_quality_rules (
    rule_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    column_name VARCHAR(100),
    rule_type VARCHAR(50) NOT NULL,
    rule_description TEXT,
    rule_sql TEXT,
    threshold_value DECIMAL,
    severity VARCHAR(20) DEFAULT 'ERROR',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data quality results table
CREATE TABLE monitoring.data_quality_results (
    result_id SERIAL PRIMARY KEY,
    rule_id INTEGER REFERENCES monitoring.data_quality_rules(rule_id),
    check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    passed BOOLEAN NOT NULL,
    actual_value DECIMAL,
    expected_value DECIMAL,
    error_count INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    details JSONB
);

-- Insert sample data quality rules
INSERT INTO monitoring.data_quality_rules (table_name, column_name, rule_type, rule_description, threshold_value) VALUES
('warehouse.dim_customers', 'email', 'null_check', 'Email should not be null', 5.0),
('warehouse.dim_customers', 'customer_id', 'duplicate_check', 'Customer ID should be unique', 0.0),
('warehouse.fact_sales', 'total_amount', 'range_check', 'Total amount should be positive', 0.0),
('warehouse.fact_sales', 'quantity', 'range_check', 'Quantity should be positive', 0.0);

-- =====================================================
-- 6. ETL FUNCTIONS
-- =====================================================

-- Function to populate date dimension
CREATE OR REPLACE FUNCTION warehouse.populate_date_dimension(
    start_date DATE,
    end_date DATE
) RETURNS INTEGER AS $$
DECLARE
    current_date DATE;
    inserted_count INTEGER := 0;
BEGIN
    current_date := start_date;
    
    WHILE current_date <= end_date LOOP
        INSERT INTO warehouse.dim_date (
            date_key, date_value, year, quarter, month, month_name,
            day_of_month, day_of_week, day_name, week_of_year, is_weekend
        )
        SELECT 
            TO_CHAR(current_date, 'YYYYMMDD')::INTEGER,
            current_date,
            EXTRACT(YEAR FROM current_date)::INTEGER,
            EXTRACT(QUARTER FROM current_date)::INTEGER,
            EXTRACT(MONTH FROM current_date)::INTEGER,
            TO_CHAR(current_date, 'Month'),
            EXTRACT(DAY FROM current_date)::INTEGER,
            EXTRACT(DOW FROM current_date)::INTEGER,
            TO_CHAR(current_date, 'Day'),
            EXTRACT(WEEK FROM current_date)::INTEGER,
            EXTRACT(DOW FROM current_date) IN (0, 6)
        WHERE NOT EXISTS (
            SELECT 1 FROM warehouse.dim_date WHERE date_value = current_date
        );
        
        IF FOUND THEN
            inserted_count := inserted_count + 1;
        END IF;
        
        current_date := current_date + INTERVAL '1 day';
    END LOOP;
    
    RETURN inserted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to process customer data
CREATE OR REPLACE FUNCTION warehouse.process_customers()
RETURNS TABLE(processed_count INTEGER, error_count INTEGER) AS $$
DECLARE
    v_processed INTEGER := 0;
    v_errors INTEGER := 0;
    v_record RECORD;
BEGIN
    -- Process unprocessed customer records
    FOR v_record IN 
        SELECT id, raw_data 
        FROM staging.raw_customers 
        WHERE processed = FALSE
        ORDER BY loaded_at
    LOOP
        BEGIN
            -- Insert or update customer dimension
            INSERT INTO warehouse.dim_customers (
                customer_id, customer_name, email, phone, address, registration_date
            )
            SELECT 
                (raw_data->>'customer_id')::INTEGER,
                raw_data->>'customer_name',
                raw_data->>'email',
                raw_data->>'phone',
                raw_data->'address',
                (raw_data->>'registration_date')::DATE
            FROM staging.raw_customers
            WHERE id = v_record.id
            ON CONFLICT (customer_id) DO UPDATE SET
                customer_name = EXCLUDED.customer_name,
                email = EXCLUDED.email,
                phone = EXCLUDED.phone,
                address = EXCLUDED.address,
                updated_at = CURRENT_TIMESTAMP;
            
            -- Mark as processed
            UPDATE staging.raw_customers 
            SET processed = TRUE 
            WHERE id = v_record.id;
            
            v_processed := v_processed + 1;
            
        EXCEPTION
            WHEN OTHERS THEN
                -- Log error
                INSERT INTO monitoring.etl_errors (
                    table_name, record_id, error_message, error_timestamp
                ) VALUES (
                    'staging.raw_customers', 
                    v_record.id, 
                    SQLERRM, 
                    CURRENT_TIMESTAMP
                );
                
                v_errors := v_errors + 1;
        END;
    END LOOP;
    
    RETURN QUERY SELECT v_processed, v_errors;
END;
$$ LANGUAGE plpgsql;

-- Function to process sales data
CREATE OR REPLACE FUNCTION warehouse.process_sales()
RETURNS TABLE(processed_count INTEGER, error_count INTEGER) AS $$
DECLARE
    v_processed INTEGER := 0;
    v_errors INTEGER := 0;
    v_record RECORD;
BEGIN
    FOR v_record IN 
        SELECT id, raw_data 
        FROM staging.raw_orders 
        WHERE processed = FALSE
        ORDER BY loaded_at
    LOOP
        BEGIN
            -- Insert into fact_sales with proper keys
            INSERT INTO warehouse.fact_sales (
                customer_key, product_key, date_key, order_id,
                quantity, unit_price, total_amount, discount_amount, tax_amount
            )
            SELECT 
                dc.customer_key,
                dp.product_key,
                TO_CHAR((v_record.raw_data->>'order_date')::DATE, 'YYYYMMDD')::INTEGER,
                (v_record.raw_data->>'order_id')::INTEGER,
                (v_record.raw_data->>'quantity')::INTEGER,
                (v_record.raw_data->>'unit_price')::DECIMAL(10,2),
                (v_record.raw_data->>'total_amount')::DECIMAL(12,2),
                COALESCE((v_record.raw_data->>'discount_amount')::DECIMAL(10,2), 0),
                COALESCE((v_record.raw_data->>'tax_amount')::DECIMAL(10,2), 0)
            FROM warehouse.dim_customers dc
            JOIN warehouse.dim_products dp ON dp.product_id = (v_record.raw_data->>'product_id')::INTEGER
            WHERE dc.customer_id = (v_record.raw_data->>'customer_id')::INTEGER;
            
            -- Mark as processed
            UPDATE staging.raw_orders 
            SET processed = TRUE 
            WHERE id = v_record.id;
            
            v_processed := v_processed + 1;
            
        EXCEPTION
            WHEN OTHERS THEN
                INSERT INTO monitoring.etl_errors (
                    table_name, record_id, error_message, error_timestamp
                ) VALUES (
                    'staging.raw_orders', 
                    v_record.id, 
                    SQLERRM, 
                    CURRENT_TIMESTAMP
                );
                
                v_errors := v_errors + 1;
        END;
    END LOOP;
    
    RETURN QUERY SELECT v_processed, v_errors;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 7. DATA QUALITY FUNCTIONS
-- =====================================================

-- Function to run data quality checks
CREATE OR REPLACE FUNCTION monitoring.run_data_quality_checks(p_table_name VARCHAR DEFAULT NULL)
RETURNS TABLE(
    rule_id INTEGER,
    table_name VARCHAR,
    rule_type VARCHAR,
    passed BOOLEAN,
    message TEXT
) AS $$
DECLARE
    v_rule RECORD;
    v_sql TEXT;
    v_result RECORD;
    v_passed BOOLEAN;
    v_actual_value DECIMAL;
    v_total_count INTEGER;
    v_error_count INTEGER;
BEGIN
    FOR v_rule IN 
        SELECT * FROM monitoring.data_quality_rules 
        WHERE is_active = TRUE 
        AND (p_table_name IS NULL OR monitoring.data_quality_rules.table_name = p_table_name)
    LOOP
        BEGIN
            CASE v_rule.rule_type
                WHEN 'null_check' THEN
                    v_sql := format('SELECT COUNT(*) as total, COUNT(%I) as non_null FROM %s',
                                   v_rule.column_name, v_rule.table_name);
                    EXECUTE v_sql INTO v_result;
                    v_total_count := v_result.total;
                    v_error_count := v_result.total - v_result.non_null;
                    v_actual_value := CASE WHEN v_total_count > 0 THEN (v_error_count * 100.0 / v_total_count) ELSE 0 END;
                    v_passed := v_actual_value <= v_rule.threshold_value;
                    
                WHEN 'duplicate_check' THEN
                    v_sql := format('SELECT COUNT(*) as total, COUNT(DISTINCT %I) as unique_count FROM %s',
                                   v_rule.column_name, v_rule.table_name);
                    EXECUTE v_sql INTO v_result;
                    v_total_count := v_result.total;
                    v_error_count := v_result.total - v_result.unique_count;
                    v_actual_value := v_error_count;
                    v_passed := v_actual_value <= v_rule.threshold_value;
                    
                WHEN 'range_check' THEN
                    v_sql := format('SELECT COUNT(*) as total, COUNT(*) FILTER (WHERE %I <= 0) as violations FROM %s',
                                   v_rule.column_name, v_rule.table_name);
                    EXECUTE v_sql INTO v_result;
                    v_total_count := v_result.total;
                    v_error_count := v_result.violations;
                    v_actual_value := v_error_count;
                    v_passed := v_actual_value <= v_rule.threshold_value;
            END CASE;
            
            -- Log result
            INSERT INTO monitoring.data_quality_results (
                rule_id, passed, actual_value, total_count, error_count
            ) VALUES (
                v_rule.rule_id, v_passed, v_actual_value, v_total_count, v_error_count
            );
            
            RETURN QUERY SELECT 
                v_rule.rule_id,
                v_rule.table_name,
                v_rule.rule_type,
                v_passed,
                format('%s: %s (errors: %s/%s, threshold: %s)', 
                       v_rule.rule_description,
                       CASE WHEN v_passed THEN 'PASSED' ELSE 'FAILED' END,
                       v_error_count,
                       v_total_count,
                       v_rule.threshold_value);
                       
        EXCEPTION
            WHEN OTHERS THEN
                RETURN QUERY SELECT 
                    v_rule.rule_id,
                    v_rule.table_name,
                    v_rule.rule_type,
                    FALSE,
                    format('ERROR: %s', SQLERRM);
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 8. MONITORING TABLES
-- =====================================================

-- ETL execution log
CREATE TABLE monitoring.etl_log (
    log_id SERIAL PRIMARY KEY,
    process_name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status VARCHAR(20) NOT NULL,
    records_processed INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    error_message TEXT,
    details JSONB
);

-- ETL errors table
CREATE TABLE monitoring.etl_errors (
    error_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    record_id INTEGER,
    error_message TEXT,
    error_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE
);

-- =====================================================
-- 9. MAIN ETL ORCHESTRATION FUNCTION
-- =====================================================

CREATE OR REPLACE FUNCTION warehouse.run_etl_pipeline()
RETURNS JSONB AS $$
DECLARE
    v_start_time TIMESTAMP := CURRENT_TIMESTAMP;
    v_customer_result RECORD;
    v_sales_result RECORD;
    v_quality_results JSONB;
    v_log_id INTEGER;
    v_final_result JSONB;
BEGIN
    -- Log ETL start
    INSERT INTO monitoring.etl_log (process_name, start_time, status)
    VALUES ('full_etl_pipeline', v_start_time, 'RUNNING')
    RETURNING log_id INTO v_log_id;
    
    BEGIN
        -- Step 1: Process customers
        SELECT * INTO v_customer_result FROM warehouse.process_customers();
        
        -- Step 2: Process sales
        SELECT * INTO v_sales_result FROM warehouse.process_sales();
        
        -- Step 3: Run data quality checks
        SELECT jsonb_agg(
            jsonb_build_object(
                'rule_id', rule_id,
                'table_name', table_name,
                'rule_type', rule_type,
                'passed', passed,
                'message', message
            )
        ) INTO v_quality_results
        FROM monitoring.run_data_quality_checks();
        
        -- Update ETL log with success
        UPDATE monitoring.etl_log 
        SET 
            end_time = CURRENT_TIMESTAMP,
            status = 'SUCCESS',
            records_processed = v_customer_result.processed_count + v_sales_result.processed_count,
            records_failed = v_customer_result.error_count + v_sales_result.error_count,
            details = jsonb_build_object(
                'customers_processed', v_customer_result.processed_count,
                'customers_failed', v_customer_result.error_count,
                'sales_processed', v_sales_result.processed_count,
                'sales_failed', v_sales_result.error_count,
                'quality_checks', v_quality_results
            )
        WHERE log_id = v_log_id;
        
        -- Build final result
        v_final_result := jsonb_build_object(
            'status', 'SUCCESS',
            'execution_time_seconds', EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - v_start_time)),
            'customers_processed', v_customer_result.processed_count,
            'sales_processed', v_sales_result.processed_count,
            'total_errors', v_customer_result.error_count + v_sales_result.error_count,
            'quality_checks', v_quality_results
        );
        
    EXCEPTION
        WHEN OTHERS THEN
            -- Update ETL log with failure
            UPDATE monitoring.etl_log 
            SET 
                end_time = CURRENT_TIMESTAMP,
                status = 'FAILED',
                error_message = SQLERRM
            WHERE log_id = v_log_id;
            
            v_final_result := jsonb_build_object(
                'status', 'FAILED',
                'error_message', SQLERRM,
                'execution_time_seconds', EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - v_start_time))
            );
    END;
    
    RETURN v_final_result;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 10. SAMPLE DATA AND USAGE
-- =====================================================

-- Populate date dimension for 2024
-- SELECT warehouse.populate_date_dimension('2024-01-01', '2024-12-31');

-- Sample raw customer data
-- INSERT INTO staging.raw_customers (raw_data, source_file) VALUES
-- ('{"customer_id": 1, "customer_name": "John Doe", "email": "john@example.com", "phone": "555-0123", "registration_date": "2024-01-15"}', 'customers_batch_1.json'),
-- ('{"customer_id": 2, "customer_name": "Jane Smith", "email": "jane@example.com", "phone": "555-0124", "registration_date": "2024-01-16"}', 'customers_batch_1.json');

-- Sample raw order data
-- INSERT INTO staging.raw_orders (raw_data, source_file) VALUES
-- ('{"order_id": 1001, "customer_id": 1, "product_id": 101, "order_date": "2024-01-20", "quantity": 2, "unit_price": 29.99, "total_amount": 59.98}', 'orders_batch_1.json'),
-- ('{"order_id": 1002, "customer_id": 2, "product_id": 102, "order_date": "2024-01-21", "quantity": 1, "unit_price": 49.99, "total_amount": 49.99}', 'orders_batch_1.json');

-- Run the complete ETL pipeline
-- SELECT warehouse.run_etl_pipeline();

-- Check ETL execution history
-- SELECT * FROM monitoring.etl_log ORDER BY start_time DESC LIMIT 10;

-- Check data quality results
-- SELECT * FROM monitoring.data_quality_results ORDER BY check_timestamp DESC LIMIT 20;

-- Performance monitoring queries
-- SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del, n_live_tup, n_dead_tup
-- FROM pg_stat_user_tables 
-- WHERE schemaname IN ('staging', 'warehouse')
-- ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC;