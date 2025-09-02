-- Snowflake Data Pipeline Example
-- Complete ETL pipeline with real-time processing, error handling, and monitoring

-- =====================================================
-- 1. SETUP: Database, Schema, and Warehouse
-- =====================================================

-- Create database and schemas
CREATE DATABASE IF NOT EXISTS ecommerce_dw;
USE DATABASE ecommerce_dw;

CREATE SCHEMA IF NOT EXISTS raw_data;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;
CREATE SCHEMA IF NOT EXISTS monitoring;

-- Create warehouses for different workloads
CREATE WAREHOUSE IF NOT EXISTS etl_warehouse WITH
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'ETL processing warehouse';

CREATE WAREHOUSE IF NOT EXISTS analytics_warehouse WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 3
    SCALING_POLICY = 'STANDARD'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    COMMENT = 'Analytics and reporting warehouse';

-- =====================================================
-- 2. FILE FORMATS AND STAGES
-- =====================================================

-- Create file formats
CREATE FILE FORMAT IF NOT EXISTS csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    TRIM_SPACE = TRUE
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    REPLACE_INVALID_CHARACTERS = TRUE
    DATE_FORMAT = 'YYYY-MM-DD'
    TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS';

CREATE FILE FORMAT IF NOT EXISTS json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE
    COMMENT = 'JSON format for event data';

-- Create external stage (S3)
CREATE STAGE IF NOT EXISTS s3_data_stage
    URL = 's3://ecommerce-data-bucket/raw-data/'
    CREDENTIALS = (AWS_KEY_ID = 'your_access_key' AWS_SECRET_KEY = 'your_secret_key')
    FILE_FORMAT = csv_format
    COMMENT = 'S3 stage for raw data files';

-- =====================================================
-- 3. RAW DATA TABLES
-- =====================================================

USE SCHEMA raw_data;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id NUMBER(10,0) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    registration_date DATE,
    last_login TIMESTAMP_NTZ,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id NUMBER(10,0) PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    description TEXT,
    weight_kg DECIMAL(8,3),
    dimensions VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id NUMBER(12,0) PRIMARY KEY,
    customer_id NUMBER(10,0),
    order_date DATE,
    order_timestamp TIMESTAMP_NTZ,
    status VARCHAR(20),
    total_amount DECIMAL(12,2),
    tax_amount DECIMAL(10,2),
    shipping_amount DECIMAL(8,2),
    discount_amount DECIMAL(8,2),
    payment_method VARCHAR(50),
    shipping_address VARCHAR(500),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) CLUSTER BY (order_date, customer_id);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id NUMBER(15,0) PRIMARY KEY,
    order_id NUMBER(12,0),
    product_id NUMBER(10,0),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(12,2),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
) CLUSTER BY (order_id);

-- Event tracking table (JSON data)
CREATE TABLE IF NOT EXISTS events (
    event_id STRING PRIMARY KEY,
    user_id NUMBER(10,0),
    session_id STRING,
    event_type STRING,
    event_timestamp TIMESTAMP_NTZ,
    event_data VARIANT,
    page_url STRING,
    user_agent STRING,
    ip_address STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
) CLUSTER BY (event_timestamp::DATE, event_type);

-- =====================================================
-- 4. DATA LOADING WITH ERROR HANDLING
-- =====================================================

-- Load customers data
COPY INTO customers (
    customer_id, first_name, last_name, email, phone, 
    address, city, state, zip_code, country, registration_date
)
FROM (
    SELECT 
        $1::NUMBER,
        $2::VARCHAR,
        $3::VARCHAR,
        LOWER($4::VARCHAR),
        $5::VARCHAR,
        $6::VARCHAR,
        $7::VARCHAR,
        $8::VARCHAR,
        $9::VARCHAR,
        $10::VARCHAR,
        $11::DATE
    FROM @s3_data_stage/customers/
)
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE'
PURGE = TRUE;

-- Load products data with validation
COPY INTO products (
    product_id, product_name, category, subcategory, brand, 
    price, cost, description, weight_kg, dimensions
)
FROM (
    SELECT 
        $1::NUMBER,
        $2::VARCHAR,
        $3::VARCHAR,
        $4::VARCHAR,
        $5::VARCHAR,
        TRY_CAST($6 AS DECIMAL(10,2)),
        TRY_CAST($7 AS DECIMAL(10,2)),
        $8::VARCHAR,
        TRY_CAST($9 AS DECIMAL(8,3)),
        $10::VARCHAR
    FROM @s3_data_stage/products/
)
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE'
VALIDATION_MODE = 'RETURN_ERRORS';

-- =====================================================
-- 5. STREAMING DATA WITH SNOWPIPE
-- =====================================================

-- Create pipe for real-time order processing
CREATE PIPE IF NOT EXISTS orders_pipe
    AUTO_INGEST = TRUE
    AS COPY INTO orders (
        order_id, customer_id, order_date, order_timestamp, status,
        total_amount, tax_amount, shipping_amount, discount_amount,
        payment_method, shipping_address
    )
    FROM (
        SELECT 
            $1::NUMBER,
            $2::NUMBER,
            $3::DATE,
            $4::TIMESTAMP_NTZ,
            $5::VARCHAR,
            $6::DECIMAL(12,2),
            $7::DECIMAL(10,2),
            $8::DECIMAL(8,2),
            $9::DECIMAL(8,2),
            $10::VARCHAR,
            $11::VARCHAR
        FROM @s3_data_stage/orders/
    )
    FILE_FORMAT = csv_format
    ON_ERROR = 'CONTINUE';

-- Create pipe for event data (JSON)
CREATE PIPE IF NOT EXISTS events_pipe
    AUTO_INGEST = TRUE
    AS COPY INTO events (
        event_id, user_id, session_id, event_type, event_timestamp,
        event_data, page_url, user_agent, ip_address
    )
    FROM (
        SELECT 
            $1:event_id::STRING,
            $1:user_id::NUMBER,
            $1:session_id::STRING,
            $1:event_type::STRING,
            $1:timestamp::TIMESTAMP_NTZ,
            $1:data::VARIANT,
            $1:page_url::STRING,
            $1:user_agent::STRING,
            $1:ip_address::STRING
        FROM @s3_data_stage/events/
    )
    FILE_FORMAT = json_format
    ON_ERROR = 'CONTINUE';

-- =====================================================
-- 6. STAGING LAYER WITH TRANSFORMATIONS
-- =====================================================

USE SCHEMA staging;

-- Customer dimension with SCD Type 2
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    customer_id NUMBER(10,0) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(101) GENERATED ALWAYS AS (first_name || ' ' || last_name),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    registration_date DATE,
    customer_segment VARCHAR(20),
    lifetime_value DECIMAL(12,2),
    is_active BOOLEAN,
    effective_date DATE NOT NULL,
    expiry_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
) CLUSTER BY (customer_id, is_current);

-- Product dimension
CREATE TABLE IF NOT EXISTS dim_product (
    product_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    product_id NUMBER(10,0) NOT NULL,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    margin DECIMAL(10,2) GENERATED ALWAYS AS (price - cost),
    margin_percent DECIMAL(5,2) GENERATED ALWAYS AS ((price - cost) / NULLIF(price, 0) * 100),
    description TEXT,
    weight_kg DECIMAL(8,3),
    dimensions VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
) CLUSTER BY (category, brand);

-- Date dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    date_value DATE UNIQUE NOT NULL,
    year NUMBER(4,0),
    quarter NUMBER(1,0),
    month NUMBER(2,0),
    month_name VARCHAR(20),
    day_of_month NUMBER(2,0),
    day_of_week NUMBER(1,0),
    day_name VARCHAR(20),
    week_of_year NUMBER(2,0),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN DEFAULT FALSE,
    fiscal_year NUMBER(4,0),
    fiscal_quarter NUMBER(1,0)
) CLUSTER BY (date_value);

-- Sales fact table
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    order_id NUMBER(12,0),
    customer_sk NUMBER,
    product_sk NUMBER,
    date_sk NUMBER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(12,2),
    cost DECIMAL(10,2),
    profit DECIMAL(10,2) GENERATED ALWAYS AS (total_price - cost),
    discount_amount DECIMAL(8,2),
    tax_amount DECIMAL(8,2),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (customer_sk) REFERENCES dim_customer(customer_sk),
    FOREIGN KEY (product_sk) REFERENCES dim_product(product_sk),
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk)
) CLUSTER BY (date_sk, customer_sk);

-- =====================================================
-- 7. STREAMS FOR CHANGE DATA CAPTURE
-- =====================================================

-- Create streams to capture changes
CREATE STREAM IF NOT EXISTS customers_stream ON TABLE raw_data.customers;
CREATE STREAM IF NOT EXISTS products_stream ON TABLE raw_data.products;
CREATE STREAM IF NOT EXISTS orders_stream ON TABLE raw_data.orders;
CREATE STREAM IF NOT EXISTS order_items_stream ON TABLE raw_data.order_items;

-- =====================================================
-- 8. STORED PROCEDURES FOR ETL PROCESSING
-- =====================================================

-- Procedure to populate date dimension
CREATE OR REPLACE PROCEDURE populate_date_dimension(start_date DATE, end_date DATE)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    current_date DATE;
    row_count INTEGER := 0;
BEGIN
    current_date := start_date;
    
    WHILE (current_date <= end_date) DO
        INSERT INTO dim_date (
            date_value, year, quarter, month, month_name, day_of_month,
            day_of_week, day_name, week_of_year, is_weekend,
            fiscal_year, fiscal_quarter
        )
        SELECT 
            current_date,
            EXTRACT(YEAR FROM current_date),
            EXTRACT(QUARTER FROM current_date),
            EXTRACT(MONTH FROM current_date),
            MONTHNAME(current_date),
            EXTRACT(DAY FROM current_date),
            EXTRACT(DOW FROM current_date),
            DAYNAME(current_date),
            EXTRACT(WEEK FROM current_date),
            CASE WHEN EXTRACT(DOW FROM current_date) IN (0, 6) THEN TRUE ELSE FALSE END,
            CASE WHEN EXTRACT(MONTH FROM current_date) >= 4 
                 THEN EXTRACT(YEAR FROM current_date) + 1 
                 ELSE EXTRACT(YEAR FROM current_date) END,
            CASE WHEN EXTRACT(MONTH FROM current_date) >= 4 
                 THEN EXTRACT(QUARTER FROM DATEADD(MONTH, -3, current_date))
                 ELSE EXTRACT(QUARTER FROM DATEADD(MONTH, 9, current_date)) END
        WHERE NOT EXISTS (SELECT 1 FROM dim_date WHERE date_value = current_date);
        
        current_date := DATEADD(DAY, 1, current_date);
        row_count := row_count + 1;
    END WHILE;
    
    RETURN 'Populated ' || row_count || ' date records';
END;
$$;

-- Procedure to process customer dimension (SCD Type 2)
CREATE OR REPLACE PROCEDURE process_customer_dimension()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    processed_count INTEGER := 0;
BEGIN
    -- Handle new and changed customers
    MERGE INTO dim_customer dc
    USING (
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,
            c.address,
            c.city,
            c.state,
            c.zip_code,
            c.country,
            c.registration_date,
            CASE 
                WHEN SUM(o.total_amount) >= 10000 THEN 'VIP'
                WHEN SUM(o.total_amount) >= 5000 THEN 'Premium'
                WHEN SUM(o.total_amount) >= 1000 THEN 'Regular'
                ELSE 'Basic'
            END as customer_segment,
            COALESCE(SUM(o.total_amount), 0) as lifetime_value,
            c.is_active,
            CURRENT_DATE() as effective_date
        FROM customers_stream c
        LEFT JOIN raw_data.orders o ON c.customer_id = o.customer_id
        WHERE METADATA$ACTION IN ('INSERT', 'UPDATE')
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone,
                 c.address, c.city, c.state, c.zip_code, c.country, 
                 c.registration_date, c.is_active
    ) cs ON dc.customer_id = cs.customer_id AND dc.is_current = TRUE
    WHEN MATCHED AND (
        dc.first_name != cs.first_name OR
        dc.last_name != cs.last_name OR
        dc.email != cs.email OR
        dc.phone != cs.phone OR
        dc.address != cs.address OR
        dc.city != cs.city OR
        dc.state != cs.state OR
        dc.zip_code != cs.zip_code OR
        dc.country != cs.country OR
        dc.customer_segment != cs.customer_segment OR
        dc.is_active != cs.is_active
    ) THEN UPDATE SET
        is_current = FALSE,
        expiry_date = CURRENT_DATE() - 1,
        updated_at = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN INSERT (
        customer_id, first_name, last_name, email, phone, address,
        city, state, zip_code, country, registration_date,
        customer_segment, lifetime_value, is_active, effective_date
    ) VALUES (
        cs.customer_id, cs.first_name, cs.last_name, cs.email, cs.phone, cs.address,
        cs.city, cs.state, cs.zip_code, cs.country, cs.registration_date,
        cs.customer_segment, cs.lifetime_value, cs.is_active, cs.effective_date
    );
    
    -- Insert new versions for changed records
    INSERT INTO dim_customer (
        customer_id, first_name, last_name, email, phone, address,
        city, state, zip_code, country, registration_date,
        customer_segment, lifetime_value, is_active, effective_date
    )
    SELECT 
        cs.customer_id, cs.first_name, cs.last_name, cs.email, cs.phone, cs.address,
        cs.city, cs.state, cs.zip_code, cs.country, cs.registration_date,
        cs.customer_segment, cs.lifetime_value, cs.is_active, cs.effective_date
    FROM (
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,
            c.address,
            c.city,
            c.state,
            c.zip_code,
            c.country,
            c.registration_date,
            CASE 
                WHEN SUM(o.total_amount) >= 10000 THEN 'VIP'
                WHEN SUM(o.total_amount) >= 5000 THEN 'Premium'
                WHEN SUM(o.total_amount) >= 1000 THEN 'Regular'
                ELSE 'Basic'
            END as customer_segment,
            COALESCE(SUM(o.total_amount), 0) as lifetime_value,
            c.is_active,
            CURRENT_DATE() as effective_date
        FROM customers_stream c
        LEFT JOIN raw_data.orders o ON c.customer_id = o.customer_id
        WHERE METADATA$ACTION IN ('INSERT', 'UPDATE')
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone,
                 c.address, c.city, c.state, c.zip_code, c.country, 
                 c.registration_date, c.is_active
    ) cs
    WHERE EXISTS (
        SELECT 1 FROM dim_customer dc 
        WHERE dc.customer_id = cs.customer_id 
          AND dc.is_current = FALSE 
          AND dc.expiry_date = CURRENT_DATE() - 1
    );
    
    GET DIAGNOSTICS processed_count = ROW_COUNT;
    RETURN 'Processed ' || processed_count || ' customer records';
END;
$$;

-- =====================================================
-- 9. TASKS FOR AUTOMATED PROCESSING
-- =====================================================

USE WAREHOUSE etl_warehouse;

-- Task to process customer dimension
CREATE TASK IF NOT EXISTS process_customers_task
    WAREHOUSE = etl_warehouse
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('customers_stream')
AS
    CALL process_customer_dimension();

-- Task to process sales facts
CREATE TASK IF NOT EXISTS process_sales_task
    WAREHOUSE = etl_warehouse
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('order_items_stream')
AS
    INSERT INTO fact_sales (
        order_id, customer_sk, product_sk, date_sk, quantity,
        unit_price, total_price, cost, discount_amount, tax_amount
    )
    SELECT 
        oi.order_id,
        dc.customer_sk,
        dp.product_sk,
        dd.date_sk,
        oi.quantity,
        oi.unit_price,
        oi.total_price,
        dp.cost * oi.quantity,
        COALESCE(o.discount_amount * (oi.total_price / o.total_amount), 0),
        COALESCE(o.tax_amount * (oi.total_price / o.total_amount), 0)
    FROM order_items_stream oi
    JOIN raw_data.orders o ON oi.order_id = o.order_id
    JOIN dim_customer dc ON o.customer_id = dc.customer_id AND dc.is_current = TRUE
    JOIN dim_product dp ON oi.product_id = dp.product_id
    JOIN dim_date dd ON o.order_date = dd.date_value
    WHERE METADATA$ACTION = 'INSERT';

-- =====================================================
-- 10. MONITORING AND ALERTING
-- =====================================================

USE SCHEMA monitoring;

-- Error tracking table
CREATE TABLE IF NOT EXISTS etl_errors (
    error_id NUMBER AUTOINCREMENT PRIMARY KEY,
    error_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    error_type VARCHAR(50),
    error_message TEXT,
    table_name VARCHAR(100),
    query_id STRING,
    resolved BOOLEAN DEFAULT FALSE
);

-- Data quality checks table
CREATE TABLE IF NOT EXISTS data_quality_checks (
    check_id NUMBER AUTOINCREMENT PRIMARY KEY,
    check_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    check_name VARCHAR(100),
    table_name VARCHAR(100),
    check_result VARCHAR(20),
    record_count INTEGER,
    error_count INTEGER,
    check_details VARIANT
);

-- Procedure for data quality checks
CREATE OR REPLACE PROCEDURE run_data_quality_checks()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    check_count INTEGER := 0;
BEGIN
    -- Check for duplicate customers
    INSERT INTO data_quality_checks (check_name, table_name, check_result, record_count, error_count)
    SELECT 
        'Duplicate Customer Check',
        'dim_customer',
        CASE WHEN duplicate_count > 0 THEN 'FAILED' ELSE 'PASSED' END,
        total_count,
        duplicate_count
    FROM (
        SELECT 
            COUNT(*) as total_count,
            COUNT(*) - COUNT(DISTINCT customer_id) as duplicate_count
        FROM staging.dim_customer
        WHERE is_current = TRUE
    );
    
    -- Check for orphaned sales records
    INSERT INTO data_quality_checks (check_name, table_name, check_result, record_count, error_count)
    SELECT 
        'Orphaned Sales Check',
        'fact_sales',
        CASE WHEN orphaned_count > 0 THEN 'FAILED' ELSE 'PASSED' END,
        total_count,
        orphaned_count
    FROM (
        SELECT 
            COUNT(*) as total_count,
            COUNT(CASE WHEN dc.customer_sk IS NULL THEN 1 END) as orphaned_count
        FROM staging.fact_sales fs
        LEFT JOIN staging.dim_customer dc ON fs.customer_sk = dc.customer_sk
    );
    
    check_count := 2;
    RETURN 'Completed ' || check_count || ' data quality checks';
END;
$$;

-- =====================================================
-- 11. ENABLE TASKS AND RESUME PROCESSING
-- =====================================================

-- Enable tasks (run these commands to start the pipeline)
-- ALTER TASK process_customers_task RESUME;
-- ALTER TASK process_sales_task RESUME;

-- =====================================================
-- 12. SAMPLE QUERIES FOR TESTING
-- =====================================================

-- Populate date dimension for current year
-- CALL populate_date_dimension('2024-01-01', '2024-12-31');

-- Check pipeline status
-- SELECT SYSTEM$PIPE_STATUS('orders_pipe');
-- SELECT SYSTEM$PIPE_STATUS('events_pipe');

-- Monitor task execution
-- SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY()) 
-- WHERE NAME IN ('PROCESS_CUSTOMERS_TASK', 'PROCESS_SALES_TASK')
-- ORDER BY SCHEDULED_TIME DESC;

-- Sample analytics query
-- SELECT 
--     dc.customer_segment,
--     dd.month_name,
--     COUNT(DISTINCT fs.order_id) as order_count,
--     SUM(fs.total_price) as total_revenue,
--     AVG(fs.total_price) as avg_order_value
-- FROM staging.fact_sales fs
-- JOIN staging.dim_customer dc ON fs.customer_sk = dc.customer_sk
-- JOIN staging.dim_date dd ON fs.date_sk = dd.date_sk
-- WHERE dd.year = 2024
-- GROUP BY dc.customer_segment, dd.month_name, dd.month
-- ORDER BY dd.month, total_revenue DESC;