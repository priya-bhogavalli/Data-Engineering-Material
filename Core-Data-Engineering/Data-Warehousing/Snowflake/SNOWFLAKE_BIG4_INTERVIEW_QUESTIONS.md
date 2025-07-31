# Snowflake Interview Questions - Big4 Companies

## Google Interview Questions

### 1. Design a multi-tenant data warehouse architecture for Google Workspace using Snowflake
**Answer:**
```sql
-- Multi-tenant architecture with row-level security
CREATE DATABASE google_workspace_dw;
CREATE SCHEMA google_workspace_dw.tenant_data;

-- Tenant isolation using row access policies
CREATE ROW ACCESS POLICY tenant_isolation AS (tenant_id STRING) RETURNS BOOLEAN ->
    CURRENT_ROLE() = 'SUPER_ADMIN' OR 
    CURRENT_USER() IN (
        SELECT user_name FROM tenant_users 
        WHERE tenant_id = tenant_isolation.tenant_id
    );

-- Core tables with tenant isolation
CREATE TABLE organizations (
    org_id STRING PRIMARY KEY,
    tenant_id STRING NOT NULL,
    org_name STRING,
    domain STRING,
    subscription_type STRING,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

ALTER TABLE organizations ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);

CREATE TABLE users (
    user_id STRING PRIMARY KEY,
    tenant_id STRING NOT NULL,
    org_id STRING,
    email STRING,
    display_name STRING,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

ALTER TABLE users ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);

-- Gmail analytics table
CREATE TABLE gmail_usage (
    user_id STRING,
    tenant_id STRING,
    date DATE,
    emails_sent INTEGER,
    emails_received INTEGER,
    storage_used_mb INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) CLUSTER BY (tenant_id, date);

ALTER TABLE gmail_usage ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);

-- Drive analytics table
CREATE TABLE drive_usage (
    user_id STRING,
    tenant_id STRING,
    date DATE,
    files_created INTEGER,
    files_shared INTEGER,
    storage_used_gb DECIMAL(10,2),
    collaboration_events INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) CLUSTER BY (tenant_id, date);

ALTER TABLE drive_usage ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);

-- Meet analytics table
CREATE TABLE meet_usage (
    meeting_id STRING PRIMARY KEY,
    tenant_id STRING,
    organizer_id STRING,
    meeting_date DATE,
    duration_minutes INTEGER,
    participant_count INTEGER,
    recording_enabled BOOLEAN,
    FOREIGN KEY (organizer_id) REFERENCES users(user_id)
) CLUSTER BY (tenant_id, meeting_date);

ALTER TABLE meet_usage ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);

-- Tenant-specific data marts
CREATE VIEW tenant_usage_summary AS
SELECT 
    o.tenant_id,
    o.org_name,
    COUNT(DISTINCT u.user_id) as active_users,
    SUM(g.emails_sent) as total_emails_sent,
    SUM(d.storage_used_gb) as total_drive_storage_gb,
    COUNT(DISTINCT m.meeting_id) as total_meetings,
    AVG(m.duration_minutes) as avg_meeting_duration
FROM organizations o
LEFT JOIN users u ON o.org_id = u.org_id
LEFT JOIN gmail_usage g ON u.user_id = g.user_id
LEFT JOIN drive_usage d ON u.user_id = d.user_id
LEFT JOIN meet_usage m ON u.user_id = m.organizer_id
WHERE u.is_active = TRUE
  AND g.date >= DATEADD(MONTH, -1, CURRENT_DATE())
  AND d.date >= DATEADD(MONTH, -1, CURRENT_DATE())
  AND m.meeting_date >= DATEADD(MONTH, -1, CURRENT_DATE())
GROUP BY o.tenant_id, o.org_name;

-- Tenant resource monitoring
CREATE PROCEDURE monitor_tenant_resources()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    tenant_cursor CURSOR FOR 
        SELECT DISTINCT tenant_id FROM organizations;
    current_tenant STRING;
    storage_usage DECIMAL(15,2);
    compute_credits DECIMAL(10,2);
BEGIN
    FOR tenant_record IN tenant_cursor DO
        current_tenant := tenant_record.tenant_id;
        
        -- Calculate storage usage per tenant
        SELECT SUM(
            (SELECT SUM(bytes) FROM TABLE(INFORMATION_SCHEMA.TABLE_STORAGE_METRICS(table_name))
             WHERE table_schema = 'TENANT_DATA')
        ) / (1024*1024*1024) INTO storage_usage
        FROM INFORMATION_SCHEMA.TABLES
        WHERE table_schema = 'TENANT_DATA';
        
        -- Log tenant resource usage
        INSERT INTO tenant_resource_usage (
            tenant_id, 
            date, 
            storage_gb, 
            compute_credits,
            created_at
        ) VALUES (
            current_tenant,
            CURRENT_DATE(),
            storage_usage,
            compute_credits,
            CURRENT_TIMESTAMP()
        );
    END FOR;
    
    RETURN 'Tenant resource monitoring completed';
END;
$$;
```

### 2. Implement real-time analytics for Google Search query patterns
**Answer:**
```sql
-- Real-time search analytics pipeline
CREATE STAGE search_logs_stage
    URL = 'gcs://google-search-logs/'
    CREDENTIALS = (GCS_SERVICE_ACCOUNT = 'search-analytics@project.iam.gserviceaccount.com');

-- External table for streaming search logs
CREATE EXTERNAL TABLE raw_search_logs (
    query_id STRING AS (value:query_id::STRING),
    search_query STRING AS (value:query::STRING),
    user_id STRING AS (value:user_id::STRING),
    timestamp TIMESTAMP AS (value:timestamp::TIMESTAMP),
    results_count INTEGER AS (value:results_count::INTEGER),
    click_through_rate DECIMAL(5,4) AS (value:ctr::DECIMAL(5,4)),
    location VARIANT AS (value:location::VARIANT),
    device_type STRING AS (value:device_type::STRING)
)
WITH LOCATION = @search_logs_stage
FILE_FORMAT = (TYPE = 'JSON')
AUTO_REFRESH = TRUE;

-- Stream for change detection
CREATE STREAM search_logs_stream ON EXTERNAL TABLE raw_search_logs;

-- Real-time aggregation tables
CREATE TABLE search_metrics_realtime (
    time_window TIMESTAMP,
    search_volume INTEGER,
    unique_users INTEGER,
    avg_ctr DECIMAL(5,4),
    top_queries ARRAY,
    geographic_distribution VARIANT,
    device_breakdown VARIANT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) CLUSTER BY (time_window);

-- Real-time processing task
CREATE TASK process_search_analytics
    WAREHOUSE = 'REALTIME_WH'
    SCHEDULE = '1 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('search_logs_stream')
AS
    MERGE INTO search_metrics_realtime smr
    USING (
        SELECT 
            DATE_TRUNC('MINUTE', timestamp) as time_window,
            COUNT(*) as search_volume,
            COUNT(DISTINCT user_id) as unique_users,
            AVG(click_through_rate) as avg_ctr,
            ARRAY_AGG(DISTINCT search_query) WITHIN GROUP (ORDER BY COUNT(*) DESC) as top_queries,
            OBJECT_CONSTRUCT(
                'countries', 
                OBJECT_AGG(location:country::STRING, COUNT(*))
            ) as geographic_distribution,
            OBJECT_CONSTRUCT(
                'mobile', SUM(CASE WHEN device_type = 'mobile' THEN 1 ELSE 0 END),
                'desktop', SUM(CASE WHEN device_type = 'desktop' THEN 1 ELSE 0 END),
                'tablet', SUM(CASE WHEN device_type = 'tablet' THEN 1 ELSE 0 END)
            ) as device_breakdown
        FROM search_logs_stream
        WHERE METADATA$ACTION = 'INSERT'
        GROUP BY DATE_TRUNC('MINUTE', timestamp)
    ) sls ON smr.time_window = sls.time_window
    WHEN MATCHED THEN
        UPDATE SET 
            search_volume = smr.search_volume + sls.search_volume,
            unique_users = smr.unique_users + sls.unique_users,
            avg_ctr = (smr.avg_ctr + sls.avg_ctr) / 2,
            updated_at = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
        INSERT (time_window, search_volume, unique_users, avg_ctr, top_queries, geographic_distribution, device_breakdown)
        VALUES (sls.time_window, sls.search_volume, sls.unique_users, sls.avg_ctr, sls.top_queries, sls.geographic_distribution, sls.device_breakdown);

-- Trending queries detection
CREATE TASK detect_trending_queries
    WAREHOUSE = 'ANALYTICS_WH'
    SCHEDULE = '5 MINUTE'
AS
    INSERT INTO trending_queries (query, trend_score, time_detected, metadata)
    WITH query_velocity AS (
        SELECT 
            search_query,
            COUNT(*) as current_volume,
            LAG(COUNT(*)) OVER (PARTITION BY search_query ORDER BY DATE_TRUNC('HOUR', timestamp)) as previous_volume
        FROM raw_search_logs
        WHERE timestamp >= DATEADD(HOUR, -2, CURRENT_TIMESTAMP())
        GROUP BY search_query, DATE_TRUNC('HOUR', timestamp)
    )
    SELECT 
        search_query,
        (current_volume - COALESCE(previous_volume, 0)) / GREATEST(COALESCE(previous_volume, 1), 1) as trend_score,
        CURRENT_TIMESTAMP(),
        OBJECT_CONSTRUCT(
            'current_volume', current_volume,
            'previous_volume', previous_volume,
            'growth_rate', (current_volume - COALESCE(previous_volume, 0)) / GREATEST(COALESCE(previous_volume, 1), 1)
        )
    FROM query_velocity
    WHERE (current_volume - COALESCE(previous_volume, 0)) / GREATEST(COALESCE(previous_volume, 1), 1) > 2.0  -- 200% increase
    ORDER BY trend_score DESC
    LIMIT 100;

-- Enable real-time processing
ALTER TASK process_search_analytics RESUME;
ALTER TASK detect_trending_queries RESUME;
```

## Amazon Interview Questions

### 3. Design a data warehouse for Amazon's recommendation engine using Snowflake
**Answer:**
```sql
-- Recommendation engine data warehouse
CREATE DATABASE amazon_recommendations;
CREATE SCHEMA amazon_recommendations.core;
CREATE SCHEMA amazon_recommendations.ml_features;
CREATE SCHEMA amazon_recommendations.serving;

-- Customer dimension with behavioral segmentation
CREATE TABLE dim_customer (
    customer_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    customer_id STRING UNIQUE NOT NULL,
    customer_segment STRING,
    lifetime_value DECIMAL(12,2),
    acquisition_channel STRING,
    registration_date DATE,
    last_purchase_date DATE,
    preferred_categories ARRAY,
    price_sensitivity_score DECIMAL(3,2),
    effective_date DATE NOT NULL,
    expiry_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE
) CLUSTER BY (customer_segment, is_current);

-- Product dimension with rich metadata
CREATE TABLE dim_product (
    product_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    product_id STRING UNIQUE NOT NULL,
    title STRING,
    category_hierarchy ARRAY,
    brand STRING,
    price DECIMAL(10,2),
    avg_rating DECIMAL(3,2),
    review_count INTEGER,
    features VARIANT,
    tags ARRAY,
    availability_status STRING,
    created_date DATE,
    updated_date DATE DEFAULT CURRENT_DATE()
) CLUSTER BY (category_hierarchy[0], brand);

-- Interaction fact table
CREATE TABLE fact_interactions (
    interaction_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    customer_sk NUMBER,
    product_sk NUMBER,
    interaction_type STRING, -- view, cart_add, purchase, rating, review
    interaction_timestamp TIMESTAMP,
    session_id STRING,
    interaction_value DECIMAL(10,2), -- rating value, purchase amount, etc.
    context VARIANT, -- page context, search query, etc.
    FOREIGN KEY (customer_sk) REFERENCES dim_customer(customer_sk),
    FOREIGN KEY (product_sk) REFERENCES dim_product(product_sk)
) CLUSTER BY (interaction_timestamp, interaction_type);

-- Feature engineering for ML
CREATE VIEW ml_customer_features AS
SELECT 
    c.customer_id,
    c.customer_segment,
    c.lifetime_value,
    c.price_sensitivity_score,
    
    -- Behavioral features
    COUNT(DISTINCT CASE WHEN i.interaction_type = 'view' THEN i.product_sk END) as products_viewed_30d,
    COUNT(DISTINCT CASE WHEN i.interaction_type = 'purchase' THEN i.product_sk END) as products_purchased_30d,
    AVG(CASE WHEN i.interaction_type = 'rating' THEN i.interaction_value END) as avg_rating_given,
    
    -- Category preferences
    MODE(p.category_hierarchy[0]) as preferred_category,
    COUNT(DISTINCT p.category_hierarchy[0]) as category_diversity,
    
    -- Temporal patterns
    EXTRACT(HOUR FROM i.interaction_timestamp) as preferred_hour,
    EXTRACT(DOW FROM i.interaction_timestamp) as preferred_day_of_week,
    
    -- Recency features
    DATEDIFF(DAY, MAX(CASE WHEN i.interaction_type = 'purchase' THEN i.interaction_timestamp END), CURRENT_DATE()) as days_since_last_purchase,
    DATEDIFF(DAY, MAX(i.interaction_timestamp), CURRENT_DATE()) as days_since_last_interaction

FROM dim_customer c
LEFT JOIN fact_interactions i ON c.customer_sk = i.customer_sk
LEFT JOIN dim_product p ON i.product_sk = p.product_sk
WHERE c.is_current = TRUE
  AND i.interaction_timestamp >= DATEADD(DAY, -30, CURRENT_DATE())
GROUP BY c.customer_id, c.customer_segment, c.lifetime_value, c.price_sensitivity_score;

-- Product similarity matrix
CREATE TABLE product_similarity (
    product_id_1 STRING,
    product_id_2 STRING,
    similarity_score DECIMAL(5,4),
    similarity_type STRING, -- content_based, collaborative, hybrid
    computed_date DATE DEFAULT CURRENT_DATE(),
    PRIMARY KEY (product_id_1, product_id_2, similarity_type)
) CLUSTER BY (product_id_1, similarity_type);

-- Real-time recommendation serving table
CREATE TABLE recommendations_serving (
    customer_id STRING,
    recommended_products ARRAY,
    recommendation_scores ARRAY,
    recommendation_reasons ARRAY,
    model_version STRING,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    expires_at TIMESTAMP,
    PRIMARY KEY (customer_id)
) CLUSTER BY (customer_id);

-- Batch recommendation generation
CREATE PROCEDURE generate_recommendations()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    batch_size INTEGER := 10000;
    processed_customers INTEGER := 0;
BEGIN
    -- Collaborative filtering recommendations
    CREATE OR REPLACE TEMPORARY TABLE temp_recommendations AS
    WITH customer_similarity AS (
        SELECT 
            c1.customer_id as customer_id_1,
            c2.customer_id as customer_id_2,
            COSINE_SIMILARITY(
                ARRAY_CONSTRUCT_COMPACT(c1.products_viewed_30d, c1.products_purchased_30d),
                ARRAY_CONSTRUCT_COMPACT(c2.products_viewed_30d, c2.products_purchased_30d)
            ) as similarity_score
        FROM ml_customer_features c1
        CROSS JOIN ml_customer_features c2
        WHERE c1.customer_id != c2.customer_id
          AND c1.customer_segment = c2.customer_segment
    ),
    recommendations AS (
        SELECT 
            cs.customer_id_1 as customer_id,
            p.product_id,
            AVG(cs.similarity_score * i.interaction_value) as recommendation_score,
            'collaborative_filtering' as reason
        FROM customer_similarity cs
        JOIN fact_interactions i ON cs.customer_id_2 = (
            SELECT customer_id FROM dim_customer WHERE customer_sk = i.customer_sk
        )
        JOIN dim_product p ON i.product_sk = p.product_sk
        WHERE cs.similarity_score > 0.3
          AND i.interaction_type IN ('purchase', 'rating')
          AND i.interaction_value >= 4.0
          AND p.product_id NOT IN (
              SELECT DISTINCT p2.product_id
              FROM fact_interactions i2
              JOIN dim_product p2 ON i2.product_sk = p2.product_sk
              WHERE i2.customer_sk = (
                  SELECT customer_sk FROM dim_customer WHERE customer_id = cs.customer_id_1
              )
          )
        GROUP BY cs.customer_id_1, p.product_id
    )
    SELECT 
        customer_id,
        ARRAY_AGG(product_id) WITHIN GROUP (ORDER BY recommendation_score DESC) as recommended_products,
        ARRAY_AGG(recommendation_score) WITHIN GROUP (ORDER BY recommendation_score DESC) as recommendation_scores,
        ARRAY_AGG(reason) WITHIN GROUP (ORDER BY recommendation_score DESC) as recommendation_reasons
    FROM recommendations
    GROUP BY customer_id;
    
    -- Update serving table
    MERGE INTO recommendations_serving rs
    USING temp_recommendations tr ON rs.customer_id = tr.customer_id
    WHEN MATCHED THEN
        UPDATE SET 
            recommended_products = tr.recommended_products,
            recommendation_scores = tr.recommendation_scores,
            recommendation_reasons = tr.recommendation_reasons,
            generated_at = CURRENT_TIMESTAMP(),
            expires_at = DATEADD(HOUR, 24, CURRENT_TIMESTAMP())
    WHEN NOT MATCHED THEN
        INSERT (customer_id, recommended_products, recommendation_scores, recommendation_reasons, expires_at)
        VALUES (tr.customer_id, tr.recommended_products, tr.recommendation_scores, tr.recommendation_reasons, DATEADD(HOUR, 24, CURRENT_TIMESTAMP()));
    
    SELECT COUNT(*) INTO processed_customers FROM temp_recommendations;
    
    RETURN 'Generated recommendations for ' || processed_customers || ' customers';
END;
$$;

-- A/B testing framework for recommendations
CREATE TABLE recommendation_experiments (
    experiment_id STRING PRIMARY KEY,
    experiment_name STRING,
    start_date DATE,
    end_date DATE,
    control_algorithm STRING,
    treatment_algorithm STRING,
    traffic_split DECIMAL(3,2), -- 0.5 = 50/50 split
    success_metrics ARRAY,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE recommendation_performance (
    customer_id STRING,
    experiment_id STRING,
    variant STRING, -- control or treatment
    recommended_products ARRAY,
    clicks INTEGER DEFAULT 0,
    purchases INTEGER DEFAULT 0,
    revenue DECIMAL(12,2) DEFAULT 0,
    date DATE DEFAULT CURRENT_DATE(),
    PRIMARY KEY (customer_id, experiment_id, date)
);
```

### 4. Implement real-time inventory management with Snowflake Streams
**Answer:**
```sql
-- Real-time inventory management system
CREATE DATABASE inventory_management;
CREATE SCHEMA inventory_management.realtime;
CREATE SCHEMA inventory_management.analytics;

-- Core inventory table
CREATE TABLE inventory (
    product_id STRING PRIMARY KEY,
    warehouse_id STRING,
    current_stock INTEGER NOT NULL,
    reserved_stock INTEGER DEFAULT 0,
    available_stock INTEGER GENERATED ALWAYS AS (current_stock - reserved_stock),
    reorder_point INTEGER,
    max_stock_level INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    version INTEGER DEFAULT 1
) CLUSTER BY (warehouse_id, product_id);

-- Stream to capture inventory changes
CREATE STREAM inventory_changes_stream ON TABLE inventory;

-- Inventory transactions log
CREATE TABLE inventory_transactions (
    transaction_id STRING PRIMARY KEY,
    product_id STRING,
    warehouse_id STRING,
    transaction_type STRING, -- inbound, outbound, adjustment, reservation
    quantity_change INTEGER,
    reference_id STRING, -- order_id, shipment_id, etc.
    transaction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    processed BOOLEAN DEFAULT FALSE
);

-- Stream for transaction processing
CREATE STREAM inventory_transactions_stream ON TABLE inventory_transactions;

-- Real-time inventory update task
CREATE TASK process_inventory_transactions
    WAREHOUSE = 'INVENTORY_WH'
    SCHEDULE = '1 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('inventory_transactions_stream')
AS
    MERGE INTO inventory i
    USING (
        SELECT 
            product_id,
            warehouse_id,
            SUM(CASE WHEN transaction_type = 'inbound' THEN quantity_change
                     WHEN transaction_type = 'outbound' THEN -quantity_change
                     WHEN transaction_type = 'adjustment' THEN quantity_change
                     ELSE 0 END) as stock_change,
            SUM(CASE WHEN transaction_type = 'reservation' THEN quantity_change
                     WHEN transaction_type = 'release_reservation' THEN -quantity_change
                     ELSE 0 END) as reservation_change
        FROM inventory_transactions_stream
        WHERE METADATA$ACTION = 'INSERT'
          AND processed = FALSE
        GROUP BY product_id, warehouse_id
    ) its ON i.product_id = its.product_id AND i.warehouse_id = its.warehouse_id
    WHEN MATCHED THEN
        UPDATE SET 
            current_stock = i.current_stock + its.stock_change,
            reserved_stock = i.reserved_stock + its.reservation_change,
            last_updated = CURRENT_TIMESTAMP(),
            version = i.version + 1
    WHEN NOT MATCHED THEN
        INSERT (product_id, warehouse_id, current_stock, reserved_stock, reorder_point, max_stock_level)
        VALUES (its.product_id, its.warehouse_id, its.stock_change, its.reservation_change, 10, 1000);

-- Mark transactions as processed
CREATE TASK mark_transactions_processed
    WAREHOUSE = 'INVENTORY_WH'
    AFTER process_inventory_transactions
AS
    UPDATE inventory_transactions
    SET processed = TRUE
    WHERE transaction_id IN (
        SELECT transaction_id 
        FROM inventory_transactions_stream
        WHERE METADATA$ACTION = 'INSERT'
    );

-- Real-time alerts for low stock
CREATE TABLE inventory_alerts (
    alert_id STRING PRIMARY KEY DEFAULT UUID_STRING(),
    product_id STRING,
    warehouse_id STRING,
    alert_type STRING,
    current_stock INTEGER,
    threshold INTEGER,
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    resolved BOOLEAN DEFAULT FALSE
);

CREATE TASK generate_inventory_alerts
    WAREHOUSE = 'INVENTORY_WH'
    SCHEDULE = '5 MINUTE'
AS
    INSERT INTO inventory_alerts (product_id, warehouse_id, alert_type, current_stock, threshold)
    SELECT 
        product_id,
        warehouse_id,
        CASE 
            WHEN available_stock <= 0 THEN 'OUT_OF_STOCK'
            WHEN available_stock <= reorder_point THEN 'LOW_STOCK'
            WHEN current_stock >= max_stock_level THEN 'OVERSTOCK'
        END as alert_type,
        available_stock,
        reorder_point
    FROM inventory
    WHERE (available_stock <= reorder_point OR current_stock >= max_stock_level)
      AND NOT EXISTS (
          SELECT 1 FROM inventory_alerts ia
          WHERE ia.product_id = inventory.product_id
            AND ia.warehouse_id = inventory.warehouse_id
            AND ia.resolved = FALSE
            AND ia.alert_type = CASE 
                WHEN inventory.available_stock <= 0 THEN 'OUT_OF_STOCK'
                WHEN inventory.available_stock <= inventory.reorder_point THEN 'LOW_STOCK'
                WHEN inventory.current_stock >= inventory.max_stock_level THEN 'OVERSTOCK'
            END
      );

-- Inventory forecasting
CREATE VIEW inventory_forecast AS
WITH daily_consumption AS (
    SELECT 
        product_id,
        warehouse_id,
        DATE(transaction_timestamp) as date,
        SUM(CASE WHEN transaction_type = 'outbound' THEN quantity_change ELSE 0 END) as daily_outbound
    FROM inventory_transactions
    WHERE transaction_timestamp >= DATEADD(DAY, -30, CURRENT_DATE())
    GROUP BY product_id, warehouse_id, DATE(transaction_timestamp)
),
consumption_stats AS (
    SELECT 
        product_id,
        warehouse_id,
        AVG(daily_outbound) as avg_daily_consumption,
        STDDEV(daily_outbound) as stddev_daily_consumption
    FROM daily_consumption
    GROUP BY product_id, warehouse_id
)
SELECT 
    i.product_id,
    i.warehouse_id,
    i.available_stock,
    cs.avg_daily_consumption,
    CASE 
        WHEN cs.avg_daily_consumption > 0 
        THEN i.available_stock / cs.avg_daily_consumption
        ELSE 999
    END as days_of_stock,
    CASE 
        WHEN cs.avg_daily_consumption > 0 
        THEN DATEADD(DAY, i.available_stock / cs.avg_daily_consumption, CURRENT_DATE())
        ELSE '9999-12-31'
    END as estimated_stockout_date
FROM inventory i
LEFT JOIN consumption_stats cs ON i.product_id = cs.product_id AND i.warehouse_id = cs.warehouse_id;

-- Enable real-time processing
ALTER TASK process_inventory_transactions RESUME;
ALTER TASK mark_transactions_processed RESUME;
ALTER TASK generate_inventory_alerts RESUME;
```

## Microsoft Interview Questions

### 5. Design a data warehouse for Microsoft Teams collaboration analytics
**Answer:**
```sql
-- Teams collaboration analytics data warehouse
CREATE DATABASE teams_analytics;
CREATE SCHEMA teams_analytics.core;
CREATE SCHEMA teams_analytics.metrics;

-- Organization hierarchy
CREATE TABLE dim_organization (
    org_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    tenant_id STRING UNIQUE NOT NULL,
    org_name STRING,
    industry STRING,
    employee_count INTEGER,
    subscription_tier STRING,
    region STRING,
    created_date DATE
) CLUSTER BY (region, subscription_tier);

-- User dimension with role hierarchy
CREATE TABLE dim_user (
    user_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    user_id STRING UNIQUE NOT NULL,
    tenant_id STRING,
    display_name STRING,
    email STRING,
    department STRING,
    job_title STRING,
    manager_id STRING,
    user_type STRING, -- internal, external, guest
    is_active BOOLEAN DEFAULT TRUE,
    hire_date DATE,
    effective_date DATE NOT NULL,
    expiry_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (tenant_id) REFERENCES dim_organization(tenant_id)
) CLUSTER BY (tenant_id, department);

-- Teams and channels dimension
CREATE TABLE dim_team (
    team_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    team_id STRING UNIQUE NOT NULL,
    tenant_id STRING,
    team_name STRING,
    team_type STRING, -- public, private, shared
    owner_id STRING,
    member_count INTEGER,
    channel_count INTEGER,
    created_date DATE,
    is_archived BOOLEAN DEFAULT FALSE
) CLUSTER BY (tenant_id, team_type);

CREATE TABLE dim_channel (
    channel_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    channel_id STRING UNIQUE NOT NULL,
    team_sk NUMBER,
    channel_name STRING,
    channel_type STRING, -- standard, private, shared
    created_date DATE,
    is_archived BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (team_sk) REFERENCES dim_team(team_sk)
) CLUSTER BY (team_sk, channel_type);

-- Meeting fact table
CREATE TABLE fact_meetings (
    meeting_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    meeting_id STRING UNIQUE NOT NULL,
    organizer_sk NUMBER,
    team_sk NUMBER,
    meeting_date DATE,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    scheduled_duration_minutes INTEGER,
    participant_count INTEGER,
    external_participant_count INTEGER,
    recording_enabled BOOLEAN,
    screen_sharing_used BOOLEAN,
    chat_message_count INTEGER,
    meeting_type STRING, -- scheduled, instant, recurring
    FOREIGN KEY (organizer_sk) REFERENCES dim_user(user_sk),
    FOREIGN KEY (team_sk) REFERENCES dim_team(team_sk)
) CLUSTER BY (meeting_date, organizer_sk);

-- Message activity fact table
CREATE TABLE fact_messages (
    message_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    message_id STRING UNIQUE NOT NULL,
    sender_sk NUMBER,
    channel_sk NUMBER,
    message_date DATE,
    message_timestamp TIMESTAMP,
    message_type STRING, -- text, file, image, mention, reaction
    character_count INTEGER,
    has_attachments BOOLEAN,
    mention_count INTEGER,
    reaction_count INTEGER,
    reply_count INTEGER,
    FOREIGN KEY (sender_sk) REFERENCES dim_user(user_sk),
    FOREIGN KEY (channel_sk) REFERENCES dim_channel(channel_sk)
) CLUSTER BY (message_date, channel_sk);

-- File sharing fact table
CREATE TABLE fact_file_activities (
    file_activity_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    file_id STRING,
    user_sk NUMBER,
    team_sk NUMBER,
    activity_date DATE,
    activity_timestamp TIMESTAMP,
    activity_type STRING, -- upload, download, share, edit, delete
    file_size_mb DECIMAL(10,2),
    file_type STRING,
    is_external_share BOOLEAN,
    FOREIGN KEY (user_sk) REFERENCES dim_user(user_sk),
    FOREIGN KEY (team_sk) REFERENCES dim_team(team_sk)
) CLUSTER BY (activity_date, team_sk);

-- Collaboration metrics aggregation
CREATE VIEW collaboration_metrics_daily AS
SELECT 
    d.tenant_id,
    d.org_name,
    fm.meeting_date as metric_date,
    
    -- Meeting metrics
    COUNT(DISTINCT fm.meeting_id) as total_meetings,
    SUM(fm.duration_minutes) as total_meeting_minutes,
    AVG(fm.duration_minutes) as avg_meeting_duration,
    SUM(fm.participant_count) as total_participants,
    AVG(fm.participant_count) as avg_participants_per_meeting,
    
    -- Message metrics
    COUNT(DISTINCT fmsg.message_id) as total_messages,
    COUNT(DISTINCT fmsg.sender_sk) as active_message_senders,
    SUM(fmsg.character_count) as total_characters,
    
    -- File sharing metrics
    COUNT(DISTINCT ffa.file_id) as files_shared,
    SUM(ffa.file_size_mb) as total_file_size_mb,
    COUNT(DISTINCT CASE WHEN ffa.is_external_share THEN ffa.file_id END) as external_shares,
    
    -- User engagement
    COUNT(DISTINCT COALESCE(fm.organizer_sk, fmsg.sender_sk, ffa.user_sk)) as active_users

FROM dim_organization d
LEFT JOIN dim_team dt ON d.tenant_id = dt.tenant_id
LEFT JOIN fact_meetings fm ON dt.team_sk = fm.team_sk
LEFT JOIN dim_channel dc ON dt.team_sk = dc.team_sk
LEFT JOIN fact_messages fmsg ON dc.channel_sk = fmsg.channel_sk AND DATE(fmsg.message_timestamp) = fm.meeting_date
LEFT JOIN fact_file_activities ffa ON dt.team_sk = ffa.team_sk AND ffa.activity_date = fm.meeting_date
WHERE fm.meeting_date >= DATEADD(DAY, -30, CURRENT_DATE())
GROUP BY d.tenant_id, d.org_name, fm.meeting_date;

-- Advanced analytics: Collaboration patterns
CREATE VIEW collaboration_patterns AS
WITH user_collaboration_scores AS (
    SELECT 
        u.user_sk,
        u.display_name,
        u.department,
        
        -- Meeting participation score
        COUNT(DISTINCT fm.meeting_id) * 1.0 as meeting_score,
        
        -- Message activity score
        COUNT(DISTINCT fmsg.message_id) * 0.5 as message_score,
        
        -- File sharing score
        COUNT(DISTINCT ffa.file_id) * 2.0 as file_score,
        
        -- Cross-team collaboration
        COUNT(DISTINCT dt.team_sk) * 3.0 as cross_team_score,
        
        -- External collaboration
        SUM(CASE WHEN fm.external_participant_count > 0 THEN 1 ELSE 0 END) * 2.0 as external_collab_score
        
    FROM dim_user u
    LEFT JOIN fact_meetings fm ON u.user_sk = fm.organizer_sk
    LEFT JOIN fact_messages fmsg ON u.user_sk = fmsg.sender_sk
    LEFT JOIN fact_file_activities ffa ON u.user_sk = ffa.user_sk
    LEFT JOIN dim_team dt ON fm.team_sk = dt.team_sk OR ffa.team_sk = dt.team_sk
    WHERE u.is_current = TRUE
      AND u.is_active = TRUE
      AND (fm.meeting_date >= DATEADD(DAY, -30, CURRENT_DATE()) OR
           fmsg.message_date >= DATEADD(DAY, -30, CURRENT_DATE()) OR
           ffa.activity_date >= DATEADD(DAY, -30, CURRENT_DATE()))
    GROUP BY u.user_sk, u.display_name, u.department
)
SELECT 
    user_sk,
    display_name,
    department,
    meeting_score + message_score + file_score + cross_team_score + external_collab_score as total_collaboration_score,
    CASE 
        WHEN meeting_score + message_score + file_score + cross_team_score + external_collab_score > 100 THEN 'High Collaborator'
        WHEN meeting_score + message_score + file_score + cross_team_score + external_collab_score > 50 THEN 'Medium Collaborator'
        WHEN meeting_score + message_score + file_score + cross_team_score + external_collab_score > 10 THEN 'Low Collaborator'
        ELSE 'Inactive'
    END as collaboration_level,
    meeting_score,
    message_score,
    file_score,
    cross_team_score,
    external_collab_score
FROM user_collaboration_scores
ORDER BY total_collaboration_score DESC;

-- Productivity insights
CREATE PROCEDURE generate_productivity_insights()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    insight_count INTEGER := 0;
BEGIN
    -- Meeting efficiency analysis
    INSERT INTO productivity_insights (insight_type, insight_text, metric_value, generated_date)
    SELECT 
        'MEETING_EFFICIENCY',
        'Average meeting duration is ' || ROUND(AVG(duration_minutes), 1) || ' minutes with ' || 
        ROUND(AVG(participant_count), 1) || ' participants on average',
        AVG(duration_minutes),
        CURRENT_DATE()
    FROM fact_meetings
    WHERE meeting_date >= DATEADD(DAY, -7, CURRENT_DATE());
    
    -- Collaboration hotspots
    INSERT INTO productivity_insights (insight_type, insight_text, metric_value, generated_date)
    SELECT 
        'COLLABORATION_HOTSPOT',
        'Department ' || department || ' has the highest collaboration score of ' || 
        ROUND(AVG(total_collaboration_score), 1),
        AVG(total_collaboration_score),
        CURRENT_DATE()
    FROM collaboration_patterns
    GROUP BY department
    ORDER BY AVG(total_collaboration_score) DESC
    LIMIT 1;
    
    -- External collaboration trends
    INSERT INTO productivity_insights (insight_type, insight_text, metric_value, generated_date)
    SELECT 
        'EXTERNAL_COLLABORATION',
        'External collaboration increased by ' || 
        ROUND(((current_week.external_meetings - previous_week.external_meetings) * 100.0 / 
               GREATEST(previous_week.external_meetings, 1)), 1) || '% this week',
        current_week.external_meetings,
        CURRENT_DATE()
    FROM (
        SELECT COUNT(*) as external_meetings
        FROM fact_meetings
        WHERE meeting_date >= DATEADD(DAY, -7, CURRENT_DATE())
          AND external_participant_count > 0
    ) current_week
    CROSS JOIN (
        SELECT COUNT(*) as external_meetings
        FROM fact_meetings
        WHERE meeting_date >= DATEADD(DAY, -14, CURRENT_DATE())
          AND meeting_date < DATEADD(DAY, -7, CURRENT_DATE())
          AND external_participant_count > 0
    ) previous_week;
    
    SELECT COUNT(*) INTO insight_count FROM productivity_insights WHERE generated_date = CURRENT_DATE();
    
    RETURN 'Generated ' || insight_count || ' productivity insights';
END;
$$;
```

## Meta Interview Questions

### 6. Design a social media analytics platform using Snowflake for Facebook/Instagram data
**Answer:**
```sql
-- Social media analytics platform
CREATE DATABASE social_analytics;
CREATE SCHEMA social_analytics.core;
CREATE SCHEMA social_analytics.engagement;
CREATE SCHEMA social_analytics.content;

-- User dimension with social graph metrics
CREATE TABLE dim_user (
    user_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    user_id STRING UNIQUE NOT NULL,
    username STRING,
    display_name STRING,
    account_type STRING, -- personal, business, creator
    follower_count INTEGER,
    following_count INTEGER,
    post_count INTEGER,
    verification_status BOOLEAN,
    account_creation_date DATE,
    location VARIANT,
    bio_text STRING,
    profile_category STRING,
    is_active BOOLEAN DEFAULT TRUE,
    last_activity_date DATE,
    effective_date DATE NOT NULL,
    expiry_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE
) CLUSTER BY (account_type, verification_status);

-- Content dimension
CREATE TABLE dim_content (
    content_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    content_id STRING UNIQUE NOT NULL,
    creator_sk NUMBER,
    content_type STRING, -- post, story, reel, video, live
    platform STRING, -- facebook, instagram
    caption TEXT,
    hashtags ARRAY,
    mentions ARRAY,
    media_type STRING, -- image, video, carousel, text
    media_urls ARRAY,
    duration_seconds INTEGER,
    content_category STRING,
    is_sponsored BOOLEAN DEFAULT FALSE,
    created_timestamp TIMESTAMP,
    FOREIGN KEY (creator_sk) REFERENCES dim_user(user_sk)
) CLUSTER BY (platform, content_type, created_timestamp::DATE);

-- Engagement fact table
CREATE TABLE fact_engagement (
    engagement_sk NUMBER AUTOINCREMENT PRIMARY KEY,
    content_sk NUMBER,
    user_sk NUMBER,
    engagement_type STRING, -- like, comment, share, save, view
    engagement_timestamp TIMESTAMP,
    engagement_date DATE GENERATED ALWAYS AS (DATE(engagement_timestamp)),
    session_id STRING,
    device_type STRING,
    location VARIANT,
    FOREIGN KEY (content_sk) REFERENCES dim_content(content_sk),
    FOREIGN KEY (user_sk) REFERENCES dim_user(user_sk)
) CLUSTER BY (engagement_date, content_sk);

-- Real-time engagement aggregation
CREATE TABLE engagement_metrics_realtime (
    content_id STRING,
    time_window TIMESTAMP,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    save_count INTEGER DEFAULT 0,
    unique_engagers INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4),
    viral_coefficient DECIMAL(8,4),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (content_id, time_window)
) CLUSTER BY (time_window, viral_coefficient DESC);

-- Stream for real-time processing
CREATE STREAM engagement_stream ON TABLE fact_engagement;

-- Real-time aggregation task
CREATE TASK aggregate_engagement_realtime
    WAREHOUSE = 'SOCIAL_ANALYTICS_WH'
    SCHEDULE = '1 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('engagement_stream')
AS
    MERGE INTO engagement_metrics_realtime emr
    USING (
        SELECT 
            dc.content_id,
            DATE_TRUNC('MINUTE', fe.engagement_timestamp) as time_window,
            COUNT(CASE WHEN fe.engagement_type = 'like' THEN 1 END) as like_count,
            COUNT(CASE WHEN fe.engagement_type = 'comment' THEN 1 END) as comment_count,
            COUNT(CASE WHEN fe.engagement_type = 'share' THEN 1 END) as share_count,
            COUNT(CASE WHEN fe.engagement_type = 'view' THEN 1 END) as view_count,
            COUNT(CASE WHEN fe.engagement_type = 'save' THEN 1 END) as save_count,
            COUNT(DISTINCT fe.user_sk) as unique_engagers
        FROM engagement_stream fe
        JOIN dim_content dc ON fe.content_sk = dc.content_sk
        WHERE METADATA$ACTION = 'INSERT'
        GROUP BY dc.content_id, DATE_TRUNC('MINUTE', fe.engagement_timestamp)
    ) es ON emr.content_id = es.content_id AND emr.time_window = es.time_window
    WHEN MATCHED THEN
        UPDATE SET 
            like_count = emr.like_count + es.like_count,
            comment_count = emr.comment_count + es.comment_count,
            share_count = emr.share_count + es.share_count,
            view_count = emr.view_count + es.view_count,
            save_count = emr.save_count + es.save_count,
            unique_engagers = emr.unique_engagers + es.unique_engagers,
            engagement_rate = (emr.like_count + emr.comment_count + emr.share_count + emr.save_count) * 1.0 / GREATEST(emr.view_count, 1),
            viral_coefficient = (emr.share_count * 1.0) / GREATEST(emr.view_count, 1),
            updated_at = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
        INSERT (content_id, time_window, like_count, comment_count, share_count, view_count, save_count, unique_engagers, engagement_rate, viral_coefficient)
        VALUES (es.content_id, es.time_window, es.like_count, es.comment_count, es.share_count, es.view_count, es.save_count, es.unique_engagers,
                (es.like_count + es.comment_count + es.share_count + es.save_count) * 1.0 / GREATEST(es.view_count, 1),
                (es.share_count * 1.0) / GREATEST(es.view_count, 1));

-- Viral content detection
CREATE TASK detect_viral_content
    WAREHOUSE = 'SOCIAL_ANALYTICS_WH'
    SCHEDULE = '5 MINUTE'
AS
    INSERT INTO viral_content_alerts (content_id, viral_score, detection_timestamp, metrics)
    WITH content_velocity AS (
        SELECT 
            content_id,
            SUM(like_count + comment_count + share_count) as total_engagement,
            MAX(time_window) as latest_window,
            DATEDIFF(MINUTE, MIN(time_window), MAX(time_window)) as time_span_minutes,
            SUM(like_count + comment_count + share_count) / GREATEST(DATEDIFF(MINUTE, MIN(time_window), MAX(time_window)), 1) as engagement_velocity
        FROM engagement_metrics_realtime
        WHERE time_window >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
        GROUP BY content_id
        HAVING SUM(like_count + comment_count + share_count) > 1000  -- Minimum engagement threshold
    ),
    viral_candidates AS (
        SELECT 
            cv.*,
            dc.creator_sk,
            du.follower_count,
            -- Viral score calculation
            (cv.engagement_velocity * 0.4 +
             (cv.total_engagement / GREATEST(du.follower_count, 1)) * 0.3 +
             emr.viral_coefficient * 0.3) as viral_score
        FROM content_velocity cv
        JOIN dim_content dc ON cv.content_id = dc.content_id
        JOIN dim_user du ON dc.creator_sk = du.user_sk
        JOIN engagement_metrics_realtime emr ON cv.content_id = emr.content_id
        WHERE du.is_current = TRUE
    )
    SELECT 
        content_id,
        viral_score,
        CURRENT_TIMESTAMP(),
        OBJECT_CONSTRUCT(
            'total_engagement', total_engagement,
            'engagement_velocity', engagement_velocity,
            'creator_followers', follower_count,
            'time_span_minutes', time_span_minutes
        )
    FROM viral_candidates
    WHERE viral_score > 10.0  -- Viral threshold
      AND NOT EXISTS (
          SELECT 1 FROM viral_content_alerts vca
          WHERE vca.content_id = viral_candidates.content_id
            AND vca.detection_timestamp >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
      )
    ORDER BY viral_score DESC
    LIMIT 100;

-- Content performance analytics
CREATE VIEW content_performance_analytics AS
WITH content_metrics AS (
    SELECT 
        dc.content_id,
        dc.creator_sk,
        du.username,
        dc.content_type,
        dc.platform,
        dc.created_timestamp,
        ARRAY_SIZE(dc.hashtags) as hashtag_count,
        ARRAY_SIZE(dc.mentions) as mention_count,
        dc.is_sponsored,
        
        -- Engagement metrics
        SUM(CASE WHEN fe.engagement_type = 'like' THEN 1 ELSE 0 END) as total_likes,
        SUM(CASE WHEN fe.engagement_type = 'comment' THEN 1 ELSE 0 END) as total_comments,
        SUM(CASE WHEN fe.engagement_type = 'share' THEN 1 ELSE 0 END) as total_shares,
        SUM(CASE WHEN fe.engagement_type = 'view' THEN 1 ELSE 0 END) as total_views,
        COUNT(DISTINCT fe.user_sk) as unique_engagers,
        
        -- Time-based metrics
        MIN(fe.engagement_timestamp) as first_engagement,
        MAX(fe.engagement_timestamp) as last_engagement,
        DATEDIFF(HOUR, dc.created_timestamp, MAX(fe.engagement_timestamp)) as engagement_lifespan_hours
        
    FROM dim_content dc
    LEFT JOIN fact_engagement fe ON dc.content_sk = fe.content_sk
    LEFT JOIN dim_user du ON dc.creator_sk = du.user_sk
    WHERE dc.created_timestamp >= DATEADD(DAY, -30, CURRENT_TIMESTAMP())
      AND du.is_current = TRUE
    GROUP BY dc.content_id, dc.creator_sk, du.username, dc.content_type, dc.platform, 
             dc.created_timestamp, dc.hashtags, dc.mentions, dc.is_sponsored
)
SELECT 
    *,
    -- Calculated metrics
    (total_likes + total_comments + total_shares) as total_engagement,
    CASE WHEN total_views > 0 THEN (total_likes + total_comments + total_shares) * 100.0 / total_views ELSE 0 END as engagement_rate,
    CASE WHEN total_views > 0 THEN total_shares * 100.0 / total_views ELSE 0 END as share_rate,
    CASE WHEN engagement_lifespan_hours > 0 THEN (total_likes + total_comments + total_shares) / engagement_lifespan_hours ELSE 0 END as engagement_velocity,
    
    -- Performance categories
    CASE 
        WHEN (total_likes + total_comments + total_shares) > 10000 THEN 'Viral'
        WHEN (total_likes + total_comments + total_shares) > 1000 THEN 'High Performing'
        WHEN (total_likes + total_comments + total_shares) > 100 THEN 'Medium Performing'
        ELSE 'Low Performing'
    END as performance_category
    
FROM content_metrics
ORDER BY total_engagement DESC;

-- Enable real-time processing
ALTER TASK aggregate_engagement_realtime RESUME;
ALTER TASK detect_viral_content RESUME;
```

These Big4 interview questions demonstrate advanced Snowflake capabilities including:
- Multi-tenant architectures with row-level security
- Real-time analytics with Streams and Tasks
- Complex data modeling patterns
- Machine learning feature engineering
- Advanced security and governance
- Performance optimization at scale
- Cross-platform data integration

Each solution showcases production-ready implementations that would be expected at enterprise scale in these major technology companies.