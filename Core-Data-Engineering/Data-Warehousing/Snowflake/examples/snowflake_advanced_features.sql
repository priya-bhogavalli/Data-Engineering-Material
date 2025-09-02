-- Snowflake Advanced Features Examples
-- Comprehensive examples of advanced Snowflake capabilities

-- =====================================================
-- 1. TIME TRAVEL AND CLONING
-- =====================================================

-- Time Travel Examples
-- Query data as it existed at a specific timestamp
SELECT * FROM customers AT (TIMESTAMP => '2024-01-15 10:30:00'::TIMESTAMP);

-- Query data from 1 hour ago
SELECT * FROM orders AT (OFFSET => -3600);

-- Query data before a specific statement
SELECT * FROM products BEFORE (STATEMENT => '01a2b3c4-5678-90ab-cdef-1234567890ab');

-- Show changes between two points in time
SELECT * FROM customers CHANGES(INFORMATION => DEFAULT)
AT (TIMESTAMP => '2024-01-15 09:00:00'::TIMESTAMP)
END (TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP);

-- Zero-Copy Cloning Examples
-- Clone a table instantly
CREATE TABLE customers_backup CLONE customers;

-- Clone a table at a specific point in time
CREATE TABLE customers_jan1 CLONE customers AT (TIMESTAMP => '2024-01-01 00:00:00'::TIMESTAMP);

-- Clone entire database
CREATE DATABASE dev_environment CLONE production;

-- Clone schema
CREATE SCHEMA analytics_backup CLONE production.analytics;

-- Undrop operations
UNDROP TABLE accidentally_dropped_table;
UNDROP DATABASE accidentally_dropped_db;

-- Show history of dropped objects
SHOW TABLES HISTORY;
SHOW DATABASES HISTORY;

-- =====================================================
-- 2. STREAMS AND CHANGE DATA CAPTURE
-- =====================================================

-- Create streams on different object types
CREATE STREAM customer_changes_stream ON TABLE customers;
CREATE STREAM order_view_stream ON VIEW order_summary;

-- Advanced stream with specific columns
CREATE STREAM product_price_stream ON TABLE products
SHOW_INITIAL_ROWS = TRUE;

-- Query stream to see changes
SELECT 
    product_id,
    product_name,
    price,
    METADATA$ACTION as change_type,
    METADATA$ISUPDATE as is_update,
    METADATA$ROW_ID as row_id
FROM product_price_stream
WHERE METADATA$ACTION IN ('INSERT', 'UPDATE', 'DELETE');

-- Process stream data with MERGE
MERGE INTO product_audit_log pal
USING (
    SELECT 
        product_id,
        product_name,
        price,
        METADATA$ACTION as action_type,
        CURRENT_TIMESTAMP() as audit_timestamp
    FROM product_price_stream
) ps ON FALSE  -- Always insert, never match
WHEN NOT MATCHED THEN
    INSERT (product_id, product_name, price, action_type, audit_timestamp)
    VALUES (ps.product_id, ps.product_name, ps.price, ps.action_type, ps.audit_timestamp);

-- Check if stream has data
SELECT SYSTEM$STREAM_HAS_DATA('customer_changes_stream');

-- =====================================================
-- 3. TASKS AND SCHEDULING
-- =====================================================

-- Simple scheduled task
CREATE TASK daily_summary_task
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = 'USING CRON 0 2 * * * UTC'  -- Daily at 2 AM UTC
AS
    INSERT INTO daily_sales_summary
    SELECT 
        CURRENT_DATE() - 1 as summary_date,
        COUNT(*) as order_count,
        SUM(total_amount) as total_revenue,
        AVG(total_amount) as avg_order_value
    FROM orders
    WHERE DATE(order_timestamp) = CURRENT_DATE() - 1;

-- Task with stream dependency
CREATE TASK process_customer_updates
    WAREHOUSE = 'SMALL_WH'
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('customer_changes_stream')
AS
    CALL process_customer_changes();

-- Task tree with dependencies
CREATE TASK parent_task
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = '1 HOUR'
AS
    CALL extract_data_from_source();

CREATE TASK child_task_1
    WAREHOUSE = 'ETL_WH'
    AFTER parent_task
AS
    CALL transform_customer_data();

CREATE TASK child_task_2
    WAREHOUSE = 'ETL_WH'
    AFTER parent_task
AS
    CALL transform_product_data();

CREATE TASK final_task
    WAREHOUSE = 'ETL_WH'
    AFTER child_task_1, child_task_2
AS
    CALL load_to_data_mart();

-- Task with error handling
CREATE TASK robust_etl_task
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = '30 MINUTE'
    ERROR_INTEGRATION = 'email_notification'
AS
    CALL etl_with_error_handling();

-- Resume/Suspend tasks
ALTER TASK daily_summary_task RESUME;
ALTER TASK process_customer_updates SUSPEND;

-- Monitor task execution
SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
WHERE NAME = 'DAILY_SUMMARY_TASK'
ORDER BY SCHEDULED_TIME DESC
LIMIT 10;

-- =====================================================
-- 4. STORED PROCEDURES AND UDFS
-- =====================================================

-- JavaScript Stored Procedure
CREATE OR REPLACE PROCEDURE complex_data_processing(table_name STRING, date_filter DATE)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    try {
        // Dynamic SQL construction
        var sql_command = `
            SELECT COUNT(*) as record_count 
            FROM ${TABLE_NAME} 
            WHERE DATE(created_at) = '${DATE_FILTER}'
        `;
        
        var statement = snowflake.createStatement({sqlText: sql_command});
        var result_set = statement.execute();
        
        result_set.next();
        var count = result_set.getColumnValue(1);
        
        // Log processing
        var log_sql = `
            INSERT INTO processing_log (table_name, process_date, record_count, status)
            VALUES ('${TABLE_NAME}', '${DATE_FILTER}', ${count}, 'SUCCESS')
        `;
        
        var log_statement = snowflake.createStatement({sqlText: log_sql});
        log_statement.execute();
        
        return `Processed ${count} records from ${TABLE_NAME}`;
        
    } catch (err) {
        return `Error: ${err.message}`;
    }
$$;

-- SQL Stored Procedure with loops and conditionals
CREATE OR REPLACE PROCEDURE calculate_customer_segments()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    customer_cursor CURSOR FOR 
        SELECT customer_id, SUM(total_amount) as lifetime_value
        FROM orders 
        GROUP BY customer_id;
    current_customer_id NUMBER;
    current_ltv DECIMAL(12,2);
    segment VARCHAR(20);
    processed_count INTEGER := 0;
BEGIN
    FOR customer_record IN customer_cursor DO
        current_customer_id := customer_record.customer_id;
        current_ltv := customer_record.lifetime_value;
        
        -- Determine segment
        IF (current_ltv >= 10000) THEN
            segment := 'VIP';
        ELSEIF (current_ltv >= 5000) THEN
            segment := 'Premium';
        ELSEIF (current_ltv >= 1000) THEN
            segment := 'Regular';
        ELSE
            segment := 'Basic';
        END IF;
        
        -- Update customer segment
        UPDATE customers 
        SET customer_segment = segment,
            updated_at = CURRENT_TIMESTAMP()
        WHERE customer_id = current_customer_id;
        
        processed_count := processed_count + 1;
    END FOR;
    
    RETURN 'Updated segments for ' || processed_count || ' customers';
END;
$$;

-- User-Defined Functions (UDFs)
-- SQL UDF
CREATE OR REPLACE FUNCTION calculate_shipping_cost(weight_kg DECIMAL(8,3), distance_km INTEGER)
RETURNS DECIMAL(8,2)
AS
$$
    CASE 
        WHEN weight_kg <= 1 AND distance_km <= 100 THEN 5.00
        WHEN weight_kg <= 1 AND distance_km <= 500 THEN 8.00
        WHEN weight_kg <= 5 AND distance_km <= 100 THEN 10.00
        WHEN weight_kg <= 5 AND distance_km <= 500 THEN 15.00
        ELSE 20.00 + (weight_kg * 2) + (distance_km * 0.1)
    END
$$;

-- JavaScript UDF for complex string processing
CREATE OR REPLACE FUNCTION extract_domain_from_email(email STRING)
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    if (!EMAIL || typeof EMAIL !== 'string') {
        return null;
    }
    
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(EMAIL)) {
        return null;
    }
    
    var parts = EMAIL.split('@');
    return parts.length > 1 ? parts[1].toLowerCase() : null;
$$;

-- Table UDF (UDTF)
CREATE OR REPLACE FUNCTION split_address(address STRING)
RETURNS TABLE (street STRING, city STRING, state STRING, zip STRING)
LANGUAGE JAVASCRIPT
AS
$$
{
    processRow: function(row, rowWriter, context) {
        var address = row.ADDRESS;
        if (!address) {
            rowWriter.writeRow({STREET: null, CITY: null, STATE: null, ZIP: null});
            return;
        }
        
        // Simple address parsing logic
        var parts = address.split(',');
        var street = parts[0] ? parts[0].trim() : null;
        var city = parts[1] ? parts[1].trim() : null;
        var stateZip = parts[2] ? parts[2].trim() : null;
        
        var state = null;
        var zip = null;
        
        if (stateZip) {
            var stateZipParts = stateZip.split(' ');
            state = stateZipParts[0];
            zip = stateZipParts[1];
        }
        
        rowWriter.writeRow({
            STREET: street,
            CITY: city,
            STATE: state,
            ZIP: zip
        });
    }
}
$$;

-- =====================================================
-- 5. SEMI-STRUCTURED DATA PROCESSING
-- =====================================================

-- Working with JSON data
-- Parse JSON strings
SELECT 
    event_id,
    PARSE_JSON(event_data) as parsed_data
FROM events
WHERE event_type = 'purchase';

-- Extract values from VARIANT columns
SELECT 
    event_id,
    event_data:user_id::NUMBER as user_id,
    event_data:product_id::NUMBER as product_id,
    event_data:quantity::INTEGER as quantity,
    event_data:price::DECIMAL(10,2) as price,
    event_data:metadata.source::STRING as traffic_source
FROM events
WHERE event_type = 'purchase';

-- Flatten nested arrays
SELECT 
    event_id,
    f.value:product_id::NUMBER as product_id,
    f.value:product_name::STRING as product_name,
    f.value:price::DECIMAL(10,2) as price
FROM events,
LATERAL FLATTEN(input => event_data:items) f
WHERE event_type = 'cart_view';

-- Complex JSON processing with multiple levels
SELECT 
    customer_id,
    order_data:order_id::NUMBER as order_id,
    item.value:product_id::NUMBER as product_id,
    item.value:quantity::INTEGER as quantity,
    addr.value:type::STRING as address_type,
    addr.value:street::STRING as street,
    addr.value:city::STRING as city
FROM customer_orders,
LATERAL FLATTEN(input => order_data:items) item,
LATERAL FLATTEN(input => order_data:addresses) addr;

-- JSON path expressions
SELECT 
    event_id,
    GET_PATH(event_data, 'user.profile.preferences.notifications') as notification_prefs,
    GET_PATH(event_data, 'transaction.payment.method') as payment_method
FROM events;

-- =====================================================
-- 6. ADVANCED SECURITY FEATURES
-- =====================================================

-- Row Access Policies
CREATE ROW ACCESS POLICY customer_region_policy AS (customer_region STRING) RETURNS BOOLEAN ->
    CASE 
        WHEN CURRENT_ROLE() = 'GLOBAL_ADMIN' THEN TRUE
        WHEN CURRENT_ROLE() = 'US_ANALYST' AND customer_region = 'US' THEN TRUE
        WHEN CURRENT_ROLE() = 'EU_ANALYST' AND customer_region = 'EU' THEN TRUE
        WHEN CURRENT_ROLE() = 'APAC_ANALYST' AND customer_region = 'APAC' THEN TRUE
        ELSE FALSE
    END;

-- Apply row access policy
ALTER TABLE customers ADD ROW ACCESS POLICY customer_region_policy ON (region);

-- Dynamic Data Masking
CREATE MASKING POLICY pii_masking_policy AS (val STRING) RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('ADMIN', 'DATA_ENGINEER', 'COMPLIANCE_OFFICER') THEN val
        WHEN CURRENT_ROLE() IN ('ANALYST', 'MANAGER') THEN 
            CASE 
                WHEN val RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' 
                THEN REGEXP_REPLACE(val, '^(.{2}).*(@.*)$', '\\1****\\2')
                ELSE '****'
            END
        ELSE '****'
    END;

-- Apply masking policy to sensitive columns
ALTER TABLE customers MODIFY COLUMN email SET MASKING POLICY pii_masking_policy;
ALTER TABLE customers MODIFY COLUMN phone SET MASKING POLICY pii_masking_policy;

-- Tag-based governance
CREATE TAG sensitive_data;
CREATE TAG pii_data;

-- Apply tags to objects
ALTER TABLE customers SET TAG (sensitive_data = 'high', pii_data = 'yes');
ALTER TABLE customers MODIFY COLUMN email SET TAG (pii_data = 'email');
ALTER TABLE customers MODIFY COLUMN phone SET TAG (pii_data = 'phone');

-- Query objects by tags
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
WHERE TAG_NAME = 'PII_DATA';

-- =====================================================
-- 7. PERFORMANCE OPTIMIZATION
-- =====================================================

-- Clustering Keys
-- Add clustering key to large table
ALTER TABLE large_fact_table CLUSTER BY (date_column, region_id);

-- Multi-column clustering
ALTER TABLE sales_fact CLUSTER BY (sale_date, customer_id, product_category);

-- Monitor clustering effectiveness
SELECT 
    table_name,
    clustering_key,
    total_partition_count,
    total_constant_partition_count,
    average_overlaps,
    average_depth,
    partition_depth_histogram
FROM SNOWFLAKE.INFORMATION_SCHEMA.AUTOMATIC_CLUSTERING_HISTORY
WHERE table_name = 'LARGE_FACT_TABLE'
ORDER BY start_time DESC;

-- Check clustering depth
SELECT SYSTEM$CLUSTERING_DEPTH('large_fact_table', '(date_column, region_id)');

-- Materialized Views
CREATE MATERIALIZED VIEW customer_summary_mv AS
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(total_amount) as total_spent,
    AVG(total_amount) as avg_order_value,
    MAX(order_date) as last_order_date,
    MIN(order_date) as first_order_date
FROM orders
GROUP BY customer_id;

-- Search Optimization Service
ALTER TABLE products ADD SEARCH OPTIMIZATION;
ALTER TABLE customers ADD SEARCH OPTIMIZATION ON (first_name, last_name, email);

-- Query acceleration service
ALTER WAREHOUSE analytics_wh SET ENABLE_QUERY_ACCELERATION = TRUE;

-- =====================================================
-- 8. DATA SHARING AND COLLABORATION
-- =====================================================

-- Create secure share
CREATE SHARE customer_analytics_share;

-- Grant database and schema access
GRANT USAGE ON DATABASE analytics_db TO SHARE customer_analytics_share;
GRANT USAGE ON SCHEMA analytics_db.public TO SHARE customer_analytics_share;

-- Grant table access with secure views
CREATE SECURE VIEW shared_customer_summary AS
SELECT 
    customer_id,
    CASE WHEN CURRENT_ACCOUNT() = 'PARTNER_ACCOUNT' 
         THEN customer_segment 
         ELSE 'RESTRICTED' END as segment,
    order_count,
    total_spent,
    CASE WHEN CURRENT_ACCOUNT() = 'PARTNER_ACCOUNT' 
         THEN last_order_date 
         ELSE NULL END as last_order_date
FROM customer_summary_mv;

GRANT SELECT ON VIEW shared_customer_summary TO SHARE customer_analytics_share;

-- Add consumer accounts
ALTER SHARE customer_analytics_share ADD ACCOUNTS = ('PARTNER_ACCOUNT_1', 'PARTNER_ACCOUNT_2');

-- Create reader account
CREATE MANAGED ACCOUNT customer_reader_account
    ADMIN_NAME = 'reader_admin'
    ADMIN_PASSWORD = 'SecurePassword123!'
    TYPE = READER;

-- =====================================================
-- 9. MONITORING AND OBSERVABILITY
-- =====================================================

-- Query performance monitoring
SELECT 
    query_id,
    query_text,
    user_name,
    warehouse_name,
    start_time,
    end_time,
    total_elapsed_time / 1000 as execution_seconds,
    compilation_time / 1000 as compilation_seconds,
    bytes_scanned,
    bytes_written,
    credits_used_cloud_services
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(DAY, -1, CURRENT_TIMESTAMP())
  AND total_elapsed_time > 60000  -- Queries taking more than 1 minute
ORDER BY total_elapsed_time DESC
LIMIT 20;

-- Storage usage monitoring
SELECT 
    database_name,
    schema_name,
    table_name,
    active_bytes / (1024*1024*1024) as active_gb,
    time_travel_bytes / (1024*1024*1024) as time_travel_gb,
    failsafe_bytes / (1024*1024*1024) as failsafe_gb,
    retained_for_clone_bytes / (1024*1024*1024) as clone_gb
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE schema_name != 'INFORMATION_SCHEMA'
ORDER BY active_bytes DESC
LIMIT 50;

-- Credit usage analysis
SELECT 
    warehouse_name,
    DATE(start_time) as usage_date,
    SUM(credits_used) as daily_credits,
    SUM(credits_used_compute) as compute_credits,
    SUM(credits_used_cloud_services) as cloud_services_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD(DAY, -30, CURRENT_TIMESTAMP())
GROUP BY warehouse_name, DATE(start_time)
ORDER BY daily_credits DESC;

-- Data loading monitoring
SELECT 
    table_name,
    last_load_time,
    status,
    row_count,
    row_parsed,
    file_size,
    first_error_message
FROM SNOWFLAKE.ACCOUNT_USAGE.LOAD_HISTORY
WHERE last_load_time >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
ORDER BY last_load_time DESC;

-- =====================================================
-- 10. EXTERNAL FUNCTIONS AND INTEGRATIONS
-- =====================================================

-- Create external function (AWS Lambda example)
CREATE OR REPLACE EXTERNAL FUNCTION sentiment_analysis(text STRING)
RETURNS VARIANT
LANGUAGE PYTHON
HANDLER = 'sentiment_handler'
API_INTEGRATION = aws_lambda_integration;

-- Use external function
SELECT 
    review_id,
    review_text,
    sentiment_analysis(review_text):sentiment::STRING as sentiment,
    sentiment_analysis(review_text):confidence::FLOAT as confidence
FROM product_reviews;

-- External table with automatic refresh
CREATE EXTERNAL TABLE external_sales_data (
    order_id NUMBER AS (value:c1::NUMBER),
    customer_id NUMBER AS (value:c2::NUMBER),
    order_date DATE AS (value:c3::DATE),
    amount DECIMAL(10,2) AS (value:c4::DECIMAL(10,2))
)
WITH LOCATION = @s3_external_stage
FILE_FORMAT = (TYPE = 'CSV')
AUTO_REFRESH = TRUE
REFRESH_ON_CREATE = TRUE;

-- =====================================================
-- 11. ADVANCED ANALYTICS FUNCTIONS
-- =====================================================

-- Window functions with advanced features
SELECT 
    customer_id,
    order_date,
    total_amount,
    -- Running totals
    SUM(total_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total,
    -- Moving averages
    AVG(total_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as moving_avg_3_orders,
    -- Percentile functions
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_amount) OVER (
        PARTITION BY customer_id
    ) as median_order_value,
    -- Lead/Lag functions
    LAG(total_amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as previous_order_amount,
    LEAD(order_date, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) as next_order_date
FROM orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) <= 10;

-- MATCH_RECOGNIZE for pattern detection
SELECT *
FROM stock_prices
MATCH_RECOGNIZE (
    PARTITION BY symbol
    ORDER BY trade_date
    MEASURES
        FIRST(A.trade_date) as start_date,
        LAST(C.trade_date) as end_date,
        FIRST(A.price) as start_price,
        LAST(C.price) as end_price
    PATTERN (A B+ C)
    DEFINE
        A AS price > LAG(price),
        B AS price > LAG(price),
        C AS price < LAG(price)
);

-- Pivot and Unpivot operations
-- Pivot example
SELECT *
FROM (
    SELECT customer_id, product_category, total_spent
    FROM customer_purchases
) PIVOT (
    SUM(total_spent) FOR product_category IN (
        'Electronics' as electronics,
        'Clothing' as clothing,
        'Books' as books,
        'Home' as home
    )
);

-- Unpivot example
SELECT *
FROM quarterly_sales UNPIVOT (
    sales_amount FOR quarter IN (q1, q2, q3, q4)
);

-- =====================================================
-- 12. SAMPLE USAGE AND TESTING
-- =====================================================

-- Test the advanced features
-- CALL complex_data_processing('customers', '2024-01-15');
-- CALL calculate_customer_segments();

-- SELECT calculate_shipping_cost(2.5, 150) as shipping_cost;
-- SELECT extract_domain_from_email('user@example.com') as domain;

-- SELECT * FROM TABLE(split_address('123 Main St, New York, NY 10001'));

-- Test time travel
-- SELECT COUNT(*) FROM customers AT (OFFSET => -86400);  -- 24 hours ago

-- Test stream processing
-- SELECT COUNT(*) FROM customer_changes_stream;

-- Monitor task execution
-- SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY()) 
-- WHERE NAME = 'DAILY_SUMMARY_TASK' 
-- ORDER BY SCHEDULED_TIME DESC LIMIT 5;