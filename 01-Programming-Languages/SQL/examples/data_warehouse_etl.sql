-- Data Warehouse ETL Example
-- Complete ETL pipeline for e-commerce data warehouse

-- =====================================================
-- 1. CREATE STAGING TABLES
-- =====================================================

-- Staging table for customer data from source system
CREATE TABLE staging_customers (
    customer_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    registration_date DATE,
    last_login TIMESTAMP,
    status VARCHAR(20),
    source_system VARCHAR(20),
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staging table for product data
CREATE TABLE staging_products (
    product_id INTEGER,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    weight_kg DECIMAL(8,3),
    dimensions VARCHAR(50),
    supplier_id INTEGER,
    created_date DATE,
    status VARCHAR(20),
    source_system VARCHAR(20),
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staging table for order transactions
CREATE TABLE staging_orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date TIMESTAMP,
    ship_date TIMESTAMP,
    delivery_date TIMESTAMP,
    order_status VARCHAR(20),
    payment_method VARCHAR(50),
    shipping_cost DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    source_system VARCHAR(20),
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staging table for order line items
CREATE TABLE staging_order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    discount_percent DECIMAL(5,2),
    line_total DECIMAL(10,2),
    source_system VARCHAR(20),
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. CREATE DIMENSION TABLES
-- =====================================================

-- Customer Dimension (SCD Type 2)
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(101),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    customer_segment VARCHAR(20),
    registration_date DATE,
    effective_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product Dimension (SCD Type 1)
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INTEGER UNIQUE NOT NULL,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    current_price DECIMAL(10,2),
    current_cost DECIMAL(10,2),
    weight_kg DECIMAL(8,3),
    dimensions VARCHAR(50),
    supplier_id INTEGER,
    profit_margin DECIMAL(5,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Date Dimension
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    day_of_month INTEGER,
    day_of_year INTEGER,
    week_of_year INTEGER,
    month_number INTEGER,
    month_name VARCHAR(10),
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER
);

-- =====================================================
-- 3. CREATE FACT TABLES
-- =====================================================

-- Sales Fact Table
CREATE TABLE fact_sales (
    sales_key SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    product_key INTEGER REFERENCES dim_product(product_key),
    order_date_key INTEGER REFERENCES dim_date(date_key),
    ship_date_key INTEGER REFERENCES dim_date(date_key),
    delivery_date_key INTEGER REFERENCES dim_date(date_key),
    
    -- Measures
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    unit_cost DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    line_total DECIMAL(10,2),
    profit_amount DECIMAL(10,2),
    
    -- Degenerate dimensions
    order_status VARCHAR(20),
    payment_method VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 4. DATA QUALITY AND VALIDATION FUNCTIONS
-- =====================================================

-- Function to validate staging data
CREATE OR REPLACE FUNCTION validate_staging_data()
RETURNS TABLE(
    table_name TEXT,
    validation_rule TEXT,
    failed_records INTEGER,
    status TEXT
) AS $$
BEGIN
    -- Validate customers
    RETURN QUERY
    SELECT 
        'staging_customers'::TEXT,
        'Required fields not null'::TEXT,
        (SELECT COUNT(*) FROM staging_customers 
         WHERE customer_id IS NULL OR email IS NULL OR first_name IS NULL)::INTEGER,
        CASE WHEN (SELECT COUNT(*) FROM staging_customers 
                  WHERE customer_id IS NULL OR email IS NULL OR first_name IS NULL) = 0 
             THEN 'PASS' ELSE 'FAIL' END::TEXT;
    
    -- Validate email format
    RETURN QUERY
    SELECT 
        'staging_customers'::TEXT,
        'Valid email format'::TEXT,
        (SELECT COUNT(*) FROM staging_customers 
         WHERE email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')::INTEGER,
        CASE WHEN (SELECT COUNT(*) FROM staging_customers 
                  WHERE email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$') = 0 
             THEN 'PASS' ELSE 'FAIL' END::TEXT;
    
    -- Validate products
    RETURN QUERY
    SELECT 
        'staging_products'::TEXT,
        'Price greater than cost'::TEXT,
        (SELECT COUNT(*) FROM staging_products 
         WHERE price <= cost OR price <= 0 OR cost < 0)::INTEGER,
        CASE WHEN (SELECT COUNT(*) FROM staging_products 
                  WHERE price <= cost OR price <= 0 OR cost < 0) = 0 
             THEN 'PASS' ELSE 'FAIL' END::TEXT;
    
    -- Validate orders
    RETURN QUERY
    SELECT 
        'staging_orders'::TEXT,
        'Valid order amounts'::TEXT,
        (SELECT COUNT(*) FROM staging_orders 
         WHERE total_amount <= 0 OR shipping_cost < 0 OR tax_amount < 0)::INTEGER,
        CASE WHEN (SELECT COUNT(*) FROM staging_orders 
                  WHERE total_amount <= 0 OR shipping_cost < 0 OR tax_amount < 0) = 0 
             THEN 'PASS' ELSE 'FAIL' END::TEXT;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 5. DIMENSION LOADING PROCEDURES
-- =====================================================

-- Load Customer Dimension (SCD Type 2)
CREATE OR REPLACE FUNCTION load_customer_dimension()
RETURNS INTEGER AS $$
DECLARE
    records_processed INTEGER := 0;
BEGIN
    -- Close current records for changed customers
    UPDATE dim_customer 
    SET 
        end_date = CURRENT_DATE - 1,
        is_current = FALSE,
        updated_at = CURRENT_TIMESTAMP
    WHERE customer_id IN (
        SELECT s.customer_id
        FROM staging_customers s
        INNER JOIN dim_customer d ON s.customer_id = d.customer_id
        WHERE d.is_current = TRUE
          AND (
              s.first_name != d.first_name OR
              s.last_name != d.last_name OR
              s.email != d.email OR
              s.phone != d.phone OR
              s.address != d.address OR
              s.city != d.city OR
              s.state != d.state OR
              s.zip_code != d.zip_code
          )
    );
    
    -- Insert new versions for changed customers
    INSERT INTO dim_customer (
        customer_id, first_name, last_name, full_name, email, phone,
        address, city, state, zip_code, country, customer_segment,
        registration_date, effective_date
    )
    SELECT 
        s.customer_id,
        s.first_name,
        s.last_name,
        s.first_name || ' ' || s.last_name,
        s.email,
        s.phone,
        s.address,
        s.city,
        s.state,
        s.zip_code,
        s.country,
        -- Customer segmentation logic
        CASE 
            WHEN s.registration_date >= CURRENT_DATE - INTERVAL '30 days' THEN 'New'
            WHEN s.last_login >= CURRENT_DATE - INTERVAL '30 days' THEN 'Active'
            WHEN s.last_login >= CURRENT_DATE - INTERVAL '90 days' THEN 'At Risk'
            ELSE 'Inactive'
        END,
        s.registration_date,
        CURRENT_DATE
    FROM staging_customers s
    WHERE s.customer_id IN (
        SELECT customer_id 
        FROM dim_customer 
        WHERE end_date = CURRENT_DATE - 1
    );
    
    GET DIAGNOSTICS records_processed = ROW_COUNT;
    
    -- Insert completely new customers
    INSERT INTO dim_customer (
        customer_id, first_name, last_name, full_name, email, phone,
        address, city, state, zip_code, country, customer_segment,
        registration_date, effective_date
    )
    SELECT 
        s.customer_id,
        s.first_name,
        s.last_name,
        s.first_name || ' ' || s.last_name,
        s.email,
        s.phone,
        s.address,
        s.city,
        s.state,
        s.zip_code,
        s.country,
        CASE 
            WHEN s.registration_date >= CURRENT_DATE - INTERVAL '30 days' THEN 'New'
            WHEN s.last_login >= CURRENT_DATE - INTERVAL '30 days' THEN 'Active'
            WHEN s.last_login >= CURRENT_DATE - INTERVAL '90 days' THEN 'At Risk'
            ELSE 'Inactive'
        END,
        s.registration_date,
        CURRENT_DATE
    FROM staging_customers s
    WHERE s.customer_id NOT IN (
        SELECT DISTINCT customer_id FROM dim_customer
    );
    
    GET DIAGNOSTICS records_processed = records_processed + ROW_COUNT;
    
    RETURN records_processed;
END;
$$ LANGUAGE plpgsql;

-- Load Product Dimension (SCD Type 1)
CREATE OR REPLACE FUNCTION load_product_dimension()
RETURNS INTEGER AS $$
DECLARE
    records_processed INTEGER := 0;
BEGIN
    -- Update existing products
    UPDATE dim_product 
    SET 
        product_name = s.product_name,
        category = s.category,
        subcategory = s.subcategory,
        brand = s.brand,
        current_price = s.price,
        current_cost = s.cost,
        weight_kg = s.weight_kg,
        dimensions = s.dimensions,
        supplier_id = s.supplier_id,
        profit_margin = CASE 
            WHEN s.price > 0 THEN ((s.price - s.cost) / s.price) * 100 
            ELSE 0 
        END,
        status = s.status,
        updated_at = CURRENT_TIMESTAMP
    FROM staging_products s
    WHERE dim_product.product_id = s.product_id;
    
    GET DIAGNOSTICS records_processed = ROW_COUNT;
    
    -- Insert new products
    INSERT INTO dim_product (
        product_id, product_name, category, subcategory, brand,
        current_price, current_cost, weight_kg, dimensions, supplier_id,
        profit_margin, status
    )
    SELECT 
        s.product_id,
        s.product_name,
        s.category,
        s.subcategory,
        s.brand,
        s.price,
        s.cost,
        s.weight_kg,
        s.dimensions,
        s.supplier_id,
        CASE 
            WHEN s.price > 0 THEN ((s.price - s.cost) / s.price) * 100 
            ELSE 0 
        END,
        s.status
    FROM staging_products s
    WHERE s.product_id NOT IN (SELECT product_id FROM dim_product);
    
    GET DIAGNOSTICS records_processed = records_processed + ROW_COUNT;
    
    RETURN records_processed;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 6. FACT TABLE LOADING PROCEDURE
-- =====================================================

-- Load Sales Fact Table
CREATE OR REPLACE FUNCTION load_sales_fact()
RETURNS INTEGER AS $$
DECLARE
    records_processed INTEGER := 0;
BEGIN
    -- Insert sales facts
    INSERT INTO fact_sales (
        order_id, customer_key, product_key, order_date_key,
        ship_date_key, delivery_date_key, quantity, unit_price,
        unit_cost, discount_amount, line_total, profit_amount,
        order_status, payment_method
    )
    SELECT 
        so.order_id,
        dc.customer_key,
        dp.product_key,
        dd_order.date_key,
        dd_ship.date_key,
        dd_delivery.date_key,
        soi.quantity,
        soi.unit_price,
        dp.current_cost,
        soi.unit_price * soi.quantity * (soi.discount_percent / 100),
        soi.line_total,
        (soi.unit_price - dp.current_cost) * soi.quantity - 
        (soi.unit_price * soi.quantity * (soi.discount_percent / 100)),
        so.order_status,
        so.payment_method
    FROM staging_orders so
    INNER JOIN staging_order_items soi ON so.order_id = soi.order_id
    INNER JOIN dim_customer dc ON so.customer_id = dc.customer_id AND dc.is_current = TRUE
    INNER JOIN dim_product dp ON soi.product_id = dp.product_id
    INNER JOIN dim_date dd_order ON so.order_date::DATE = dd_order.full_date
    LEFT JOIN dim_date dd_ship ON so.ship_date::DATE = dd_ship.full_date
    LEFT JOIN dim_date dd_delivery ON so.delivery_date::DATE = dd_delivery.full_date
    WHERE NOT EXISTS (
        -- Avoid duplicates
        SELECT 1 FROM fact_sales fs 
        WHERE fs.order_id = so.order_id 
          AND fs.product_key = dp.product_key
    );
    
    GET DIAGNOSTICS records_processed = ROW_COUNT;
    
    RETURN records_processed;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 7. POPULATE DATE DIMENSION
-- =====================================================

-- Function to populate date dimension
CREATE OR REPLACE FUNCTION populate_date_dimension(
    start_date DATE,
    end_date DATE
) RETURNS INTEGER AS $$
DECLARE
    current_date DATE := start_date;
    records_inserted INTEGER := 0;
BEGIN
    WHILE current_date <= end_date LOOP
        INSERT INTO dim_date (
            date_key, full_date, day_of_week, day_name, day_of_month,
            day_of_year, week_of_year, month_number, month_name,
            quarter, year, is_weekend, is_holiday, fiscal_year, fiscal_quarter
        ) VALUES (
            TO_CHAR(current_date, 'YYYYMMDD')::INTEGER,
            current_date,
            EXTRACT(DOW FROM current_date),
            TO_CHAR(current_date, 'Day'),
            EXTRACT(DAY FROM current_date),
            EXTRACT(DOY FROM current_date),
            EXTRACT(WEEK FROM current_date),
            EXTRACT(MONTH FROM current_date),
            TO_CHAR(current_date, 'Month'),
            EXTRACT(QUARTER FROM current_date),
            EXTRACT(YEAR FROM current_date),
            EXTRACT(DOW FROM current_date) IN (0, 6),
            FALSE, -- Holiday logic would go here
            -- Fiscal year starts in July
            CASE 
                WHEN EXTRACT(MONTH FROM current_date) >= 7 
                THEN EXTRACT(YEAR FROM current_date) + 1
                ELSE EXTRACT(YEAR FROM current_date)
            END,
            -- Fiscal quarter
            CASE 
                WHEN EXTRACT(MONTH FROM current_date) IN (7, 8, 9) THEN 1
                WHEN EXTRACT(MONTH FROM current_date) IN (10, 11, 12) THEN 2
                WHEN EXTRACT(MONTH FROM current_date) IN (1, 2, 3) THEN 3
                ELSE 4
            END
        )
        ON CONFLICT (date_key) DO NOTHING;
        
        current_date := current_date + 1;
        records_inserted := records_inserted + 1;
    END LOOP;
    
    RETURN records_inserted;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 8. MAIN ETL ORCHESTRATION PROCEDURE
-- =====================================================

-- Main ETL procedure
CREATE OR REPLACE FUNCTION run_etl_pipeline()
RETURNS TABLE(
    step_name TEXT,
    status TEXT,
    records_processed INTEGER,
    execution_time INTERVAL,
    error_message TEXT
) AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    step_records INTEGER;
    validation_failed BOOLEAN := FALSE;
BEGIN
    -- Step 1: Validate staging data
    start_time := CURRENT_TIMESTAMP;
    
    -- Check if any validation failed
    SELECT COUNT(*) > 0 INTO validation_failed
    FROM validate_staging_data()
    WHERE status = 'FAIL';
    
    end_time := CURRENT_TIMESTAMP;
    
    RETURN QUERY
    SELECT 
        'Data Validation'::TEXT,
        CASE WHEN validation_failed THEN 'FAILED' ELSE 'SUCCESS' END::TEXT,
        0::INTEGER,
        end_time - start_time,
        CASE WHEN validation_failed THEN 'Data validation failed' ELSE NULL END::TEXT;
    
    -- Stop if validation failed
    IF validation_failed THEN
        RETURN;
    END IF;
    
    -- Step 2: Load Customer Dimension
    start_time := CURRENT_TIMESTAMP;
    BEGIN
        SELECT load_customer_dimension() INTO step_records;
        end_time := CURRENT_TIMESTAMP;
        
        RETURN QUERY
        SELECT 
            'Load Customer Dimension'::TEXT,
            'SUCCESS'::TEXT,
            step_records,
            end_time - start_time,
            NULL::TEXT;
    EXCEPTION WHEN OTHERS THEN
        end_time := CURRENT_TIMESTAMP;
        RETURN QUERY
        SELECT 
            'Load Customer Dimension'::TEXT,
            'FAILED'::TEXT,
            0::INTEGER,
            end_time - start_time,
            SQLERRM::TEXT;
    END;
    
    -- Step 3: Load Product Dimension
    start_time := CURRENT_TIMESTAMP;
    BEGIN
        SELECT load_product_dimension() INTO step_records;
        end_time := CURRENT_TIMESTAMP;
        
        RETURN QUERY
        SELECT 
            'Load Product Dimension'::TEXT,
            'SUCCESS'::TEXT,
            step_records,
            end_time - start_time,
            NULL::TEXT;
    EXCEPTION WHEN OTHERS THEN
        end_time := CURRENT_TIMESTAMP;
        RETURN QUERY
        SELECT 
            'Load Product Dimension'::TEXT,
            'FAILED'::TEXT,
            0::INTEGER,
            end_time - start_time,
            SQLERRM::TEXT;
    END;
    
    -- Step 4: Load Sales Fact
    start_time := CURRENT_TIMESTAMP;
    BEGIN
        SELECT load_sales_fact() INTO step_records;
        end_time := CURRENT_TIMESTAMP;
        
        RETURN QUERY
        SELECT 
            'Load Sales Fact'::TEXT,
            'SUCCESS'::TEXT,
            step_records,
            end_time - start_time,
            NULL::TEXT;
    EXCEPTION WHEN OTHERS THEN
        end_time := CURRENT_TIMESTAMP;
        RETURN QUERY
        SELECT 
            'Load Sales Fact'::TEXT,
            'FAILED'::TEXT,
            0::INTEGER,
            end_time - start_time,
            SQLERRM::TEXT;
    END;
    
    -- Step 5: Clean up staging tables
    start_time := CURRENT_TIMESTAMP;
    BEGIN
        TRUNCATE staging_customers, staging_products, staging_orders, staging_order_items;
        end_time := CURRENT_TIMESTAMP;
        
        RETURN QUERY
        SELECT 
            'Cleanup Staging Tables'::TEXT,
            'SUCCESS'::TEXT,
            0::INTEGER,
            end_time - start_time,
            NULL::TEXT;
    EXCEPTION WHEN OTHERS THEN
        end_time := CURRENT_TIMESTAMP;
        RETURN QUERY
        SELECT 
            'Cleanup Staging Tables'::TEXT,
            'FAILED'::TEXT,
            0::INTEGER,
            end_time - start_time,
            SQLERRM::TEXT;
    END;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 9. CREATE INDEXES FOR PERFORMANCE
-- =====================================================

-- Dimension table indexes
CREATE INDEX idx_dim_customer_id ON dim_customer(customer_id);
CREATE INDEX idx_dim_customer_current ON dim_customer(is_current) WHERE is_current = TRUE;
CREATE INDEX idx_dim_customer_effective_date ON dim_customer(effective_date);

CREATE INDEX idx_dim_product_id ON dim_product(product_id);
CREATE INDEX idx_dim_product_category ON dim_product(category, subcategory);
CREATE INDEX idx_dim_product_brand ON dim_product(brand);

CREATE INDEX idx_dim_date_full_date ON dim_date(full_date);
CREATE INDEX idx_dim_date_year_month ON dim_date(year, month_number);

-- Fact table indexes
CREATE INDEX idx_fact_sales_order_id ON fact_sales(order_id);
CREATE INDEX idx_fact_sales_customer_key ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product_key ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_order_date_key ON fact_sales(order_date_key);
CREATE INDEX idx_fact_sales_composite ON fact_sales(order_date_key, customer_key, product_key);

-- =====================================================
-- 10. SAMPLE USAGE AND TESTING
-- =====================================================

-- Populate date dimension for 5 years
-- SELECT populate_date_dimension('2020-01-01', '2024-12-31');

-- Sample data insertion (for testing)
/*
INSERT INTO staging_customers VALUES
(1, 'John', 'Doe', 'john.doe@email.com', '555-1234', '123 Main St', 'New York', 'NY', '10001', 'USA', '2024-01-15', '2024-01-20 10:30:00', 'active', 'CRM', CURRENT_TIMESTAMP),
(2, 'Jane', 'Smith', 'jane.smith@email.com', '555-5678', '456 Oak Ave', 'Los Angeles', 'CA', '90210', 'USA', '2024-01-10', '2024-01-19 14:15:00', 'active', 'CRM', CURRENT_TIMESTAMP);

INSERT INTO staging_products VALUES
(101, 'Laptop Pro 15"', 'Electronics', 'Computers', 'TechBrand', 1299.99, 800.00, 2.1, '35x24x2 cm', 501, '2024-01-01', 'active', 'ERP', CURRENT_TIMESTAMP),
(102, 'Wireless Mouse', 'Electronics', 'Accessories', 'TechBrand', 29.99, 15.00, 0.1, '12x6x4 cm', 502, '2024-01-01', 'active', 'ERP', CURRENT_TIMESTAMP);

INSERT INTO staging_orders VALUES
(1001, 1, '2024-01-20 15:30:00', '2024-01-21 09:00:00', '2024-01-23 14:30:00', 'delivered', 'credit_card', 15.99, 104.00, 0.00, 1345.98, 'ORDER_SYS', CURRENT_TIMESTAMP),
(1002, 2, '2024-01-21 11:15:00', '2024-01-22 10:00:00', NULL, 'shipped', 'paypal', 9.99, 2.40, 5.00, 37.38, 'ORDER_SYS', CURRENT_TIMESTAMP);

INSERT INTO staging_order_items VALUES
(1001, 101, 1, 1299.99, 0.00, 1299.99, 'ORDER_SYS', CURRENT_TIMESTAMP),
(1002, 102, 1, 29.99, 0.00, 29.99, 'ORDER_SYS', CURRENT_TIMESTAMP);
*/

-- Run the ETL pipeline
-- SELECT * FROM run_etl_pipeline();

-- Validate data quality
-- SELECT * FROM validate_staging_data();

-- =====================================================
-- 11. ANALYTICAL QUERIES FOR TESTING
-- =====================================================

-- Monthly sales summary
/*
SELECT 
    dd.year,
    dd.month_name,
    COUNT(DISTINCT fs.order_id) as total_orders,
    COUNT(DISTINCT fs.customer_key) as unique_customers,
    SUM(fs.quantity) as total_quantity,
    SUM(fs.line_total) as total_revenue,
    SUM(fs.profit_amount) as total_profit,
    ROUND(AVG(fs.line_total), 2) as avg_order_value
FROM fact_sales fs
JOIN dim_date dd ON fs.order_date_key = dd.date_key
GROUP BY dd.year, dd.month_number, dd.month_name
ORDER BY dd.year, dd.month_number;
*/

-- Top customers by revenue
/*
SELECT 
    dc.full_name,
    dc.customer_segment,
    dc.city,
    dc.state,
    COUNT(DISTINCT fs.order_id) as total_orders,
    SUM(fs.line_total) as total_revenue,
    SUM(fs.profit_amount) as total_profit,
    ROUND(AVG(fs.line_total), 2) as avg_order_value
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
WHERE dc.is_current = TRUE
GROUP BY dc.customer_key, dc.full_name, dc.customer_segment, dc.city, dc.state
ORDER BY total_revenue DESC
LIMIT 10;
*/

-- Product performance analysis
/*
SELECT 
    dp.category,
    dp.subcategory,
    dp.brand,
    dp.product_name,
    COUNT(DISTINCT fs.order_id) as orders_count,
    SUM(fs.quantity) as total_quantity_sold,
    SUM(fs.line_total) as total_revenue,
    SUM(fs.profit_amount) as total_profit,
    ROUND(AVG(fs.profit_amount / NULLIF(fs.line_total, 0)) * 100, 2) as avg_profit_margin_pct
FROM fact_sales fs
JOIN dim_product dp ON fs.product_key = dp.product_key
GROUP BY dp.product_key, dp.category, dp.subcategory, dp.brand, dp.product_name
ORDER BY total_revenue DESC
LIMIT 20;
*/