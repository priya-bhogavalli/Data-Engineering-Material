# SQL Interview Questions - Big4 Companies (Google, Amazon, Microsoft, Meta)

## Google Interview Questions

### 1. Design a database schema for YouTube (Google)
**Answer:**
```sql
-- Users table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    profile_image_url VARCHAR(500),
    subscriber_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE
);

-- Channels table
CREATE TABLE channels (
    channel_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    channel_name VARCHAR(100) NOT NULL,
    description TEXT,
    banner_image_url VARCHAR(500),
    subscriber_count BIGINT DEFAULT 0,
    total_views BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Videos table
CREATE TABLE videos (
    video_id BIGSERIAL PRIMARY KEY,
    channel_id BIGINT REFERENCES channels(channel_id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    video_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    duration_seconds INT,
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    dislike_count BIGINT DEFAULT 0,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT TRUE,
    category_id INT
);

-- Comments table
CREATE TABLE comments (
    comment_id BIGSERIAL PRIMARY KEY,
    video_id BIGINT REFERENCES videos(video_id),
    user_id BIGINT REFERENCES users(user_id),
    parent_comment_id BIGINT REFERENCES comments(comment_id),
    comment_text TEXT NOT NULL,
    like_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subscriptions table
CREATE TABLE subscriptions (
    subscription_id BIGSERIAL PRIMARY KEY,
    subscriber_id BIGINT REFERENCES users(user_id),
    channel_id BIGINT REFERENCES channels(channel_id),
    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(subscriber_id, channel_id)
);

-- Video views tracking
CREATE TABLE video_views (
    view_id BIGSERIAL PRIMARY KEY,
    video_id BIGINT REFERENCES videos(video_id),
    user_id BIGINT REFERENCES users(user_id),
    view_duration_seconds INT,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_videos_channel_upload ON videos(channel_id, upload_date DESC);
CREATE INDEX idx_comments_video ON comments(video_id, created_at DESC);
CREATE INDEX idx_subscriptions_subscriber ON subscriptions(subscriber_id);
CREATE INDEX idx_video_views_video_date ON video_views(video_id, viewed_at);
```

### 2. Find the top 3 most viewed videos for each category (Google)
**Answer:**
```sql
WITH video_rankings AS (
    SELECT 
        v.video_id,
        v.title,
        v.category_id,
        c.category_name,
        v.view_count,
        ROW_NUMBER() OVER (
            PARTITION BY v.category_id 
            ORDER BY v.view_count DESC
        ) as rank_in_category
    FROM videos v
    JOIN categories c ON v.category_id = c.category_id
    WHERE v.is_public = TRUE
)
SELECT 
    category_name,
    title,
    view_count,
    rank_in_category
FROM video_rankings
WHERE rank_in_category <= 3
ORDER BY category_name, rank_in_category;

-- Alternative using DENSE_RANK for ties
WITH video_rankings AS (
    SELECT 
        v.video_id,
        v.title,
        v.category_id,
        c.category_name,
        v.view_count,
        DENSE_RANK() OVER (
            PARTITION BY v.category_id 
            ORDER BY v.view_count DESC
        ) as dense_rank
    FROM videos v
    JOIN categories c ON v.category_id = c.category_id
    WHERE v.is_public = TRUE
)
SELECT 
    category_name,
    title,
    view_count,
    dense_rank
FROM video_rankings
WHERE dense_rank <= 3
ORDER BY category_name, dense_rank, view_count DESC;
```

### 3. Calculate user engagement metrics (Google)
**Answer:**
```sql
WITH user_engagement AS (
    SELECT 
        u.user_id,
        u.username,
        -- Video metrics
        COUNT(DISTINCT vv.video_id) as videos_watched,
        SUM(vv.view_duration_seconds) as total_watch_time,
        AVG(vv.view_duration_seconds) as avg_watch_duration,
        
        -- Interaction metrics
        COUNT(DISTINCT c.comment_id) as comments_made,
        COUNT(DISTINCT s.channel_id) as channels_subscribed,
        
        -- Engagement score calculation
        (COUNT(DISTINCT vv.video_id) * 1.0 +
         COUNT(DISTINCT c.comment_id) * 2.0 +
         COUNT(DISTINCT s.channel_id) * 3.0) as engagement_score
    FROM users u
    LEFT JOIN video_views vv ON u.user_id = vv.user_id
    LEFT JOIN comments c ON u.user_id = c.user_id
    LEFT JOIN subscriptions s ON u.user_id = s.subscriber_id
    WHERE u.created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY u.user_id, u.username
),
engagement_percentiles AS (
    SELECT 
        *,
        PERCENT_RANK() OVER (ORDER BY engagement_score) as engagement_percentile,
        CASE 
            WHEN engagement_score >= (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY engagement_score) FROM user_engagement) THEN 'High'
            WHEN engagement_score >= (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY engagement_score) FROM user_engagement) THEN 'Medium'
            ELSE 'Low'
        END as engagement_tier
    FROM user_engagement
)
SELECT 
    username,
    videos_watched,
    total_watch_time,
    ROUND(avg_watch_duration, 2) as avg_watch_duration,
    comments_made,
    channels_subscribed,
    ROUND(engagement_score, 2) as engagement_score,
    ROUND(engagement_percentile * 100, 1) as engagement_percentile,
    engagement_tier
FROM engagement_percentiles
ORDER BY engagement_score DESC;
```

## Amazon Interview Questions

### 4. Design a database for Amazon's order system (Amazon)
**Answer:**
```sql
-- Customers table
CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    registration_date DATE DEFAULT CURRENT_DATE,
    customer_tier VARCHAR(20) DEFAULT 'Regular' -- Regular, Prime, Business
);

-- Addresses table
CREATE TABLE addresses (
    address_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(customer_id),
    address_type VARCHAR(20) NOT NULL, -- shipping, billing
    street_address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE
);

-- Products table
CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,
    seller_id BIGINT,
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INT,
    brand VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    inventory_count INT DEFAULT 0,
    weight_kg DECIMAL(8,3),
    dimensions_cm VARCHAR(50), -- "L x W x H"
    is_prime_eligible BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, shipped, delivered, cancelled
    shipping_address_id BIGINT REFERENCES addresses(address_id),
    billing_address_id BIGINT REFERENCES addresses(address_id),
    subtotal DECIMAL(10,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    shipping_cost DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    estimated_delivery_date DATE
);

-- Order items table
CREATE TABLE order_items (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(order_id),
    product_id BIGINT REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    seller_id BIGINT
);

-- Shipments table
CREATE TABLE shipments (
    shipment_id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(order_id),
    tracking_number VARCHAR(100) UNIQUE,
    carrier VARCHAR(50), -- UPS, FedEx, USPS
    shipped_date TIMESTAMP,
    delivered_date TIMESTAMP,
    shipment_status VARCHAR(20) DEFAULT 'preparing' -- preparing, shipped, in_transit, delivered
);

-- Reviews table
CREATE TABLE reviews (
    review_id BIGSERIAL PRIMARY KEY,
    product_id BIGINT REFERENCES products(product_id),
    customer_id BIGINT REFERENCES customers(customer_id),
    order_id BIGINT REFERENCES orders(order_id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_title VARCHAR(200),
    review_text TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_votes INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date DESC);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_products_category ON products(category_id, price);
CREATE INDEX idx_reviews_product_rating ON reviews(product_id, rating DESC);
```

### 5. Find customers who haven't ordered in the last 90 days but were active before (Amazon)
**Answer:**
```sql
WITH customer_order_activity AS (
    SELECT 
        c.customer_id,
        c.email,
        c.first_name,
        c.last_name,
        c.customer_tier,
        MAX(o.order_date) as last_order_date,
        COUNT(o.order_id) as total_orders,
        SUM(o.total_amount) as total_spent,
        MIN(o.order_date) as first_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.email, c.first_name, c.last_name, c.customer_tier
),
inactive_customers AS (
    SELECT 
        customer_id,
        email,
        first_name,
        last_name,
        customer_tier,
        last_order_date,
        total_orders,
        total_spent,
        first_order_date,
        CURRENT_DATE - last_order_date::DATE as days_since_last_order,
        -- Calculate customer lifetime in days
        last_order_date::DATE - first_order_date::DATE as customer_lifetime_days
    FROM customer_order_activity
    WHERE last_order_date IS NOT NULL  -- Had at least one order
      AND last_order_date < CURRENT_DATE - INTERVAL '90 days'  -- Inactive for 90+ days
      AND total_orders >= 2  -- Was an active customer (multiple orders)
)
SELECT 
    email,
    first_name,
    last_name,
    customer_tier,
    last_order_date,
    days_since_last_order,
    total_orders,
    ROUND(total_spent, 2) as total_spent,
    ROUND(total_spent / total_orders, 2) as avg_order_value,
    customer_lifetime_days,
    -- Prioritize high-value customers for re-engagement
    CASE 
        WHEN total_spent > 1000 AND customer_tier = 'Prime' THEN 'High Priority'
        WHEN total_spent > 500 THEN 'Medium Priority'
        ELSE 'Low Priority'
    END as reengagement_priority
FROM inactive_customers
ORDER BY 
    CASE 
        WHEN customer_tier = 'Prime' THEN 1
        WHEN customer_tier = 'Business' THEN 2
        ELSE 3
    END,
    total_spent DESC,
    days_since_last_order DESC;
```

### 6. Calculate product recommendation scores based on purchase history (Amazon)
**Answer:**
```sql
WITH customer_purchase_history AS (
    SELECT 
        o.customer_id,
        oi.product_id,
        p.category_id,
        p.brand,
        COUNT(*) as purchase_count,
        SUM(oi.total_price) as total_spent_on_product,
        MAX(o.order_date) as last_purchase_date
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.order_status IN ('delivered', 'shipped')
    GROUP BY o.customer_id, oi.product_id, p.category_id, p.brand
),
customer_preferences AS (
    SELECT 
        customer_id,
        category_id,
        brand,
        COUNT(DISTINCT product_id) as products_bought_in_category,
        SUM(purchase_count) as total_purchases_in_category,
        SUM(total_spent_on_product) as total_spent_in_category
    FROM customer_purchase_history
    GROUP BY customer_id, category_id, brand
),
similar_customers AS (
    SELECT 
        cp1.customer_id as customer_a,
        cp2.customer_id as customer_b,
        COUNT(*) as common_categories,
        SUM(LEAST(cp1.total_purchases_in_category, cp2.total_purchases_in_category)) as similarity_score
    FROM customer_preferences cp1
    JOIN customer_preferences cp2 ON cp1.category_id = cp2.category_id 
                                  AND cp1.brand = cp2.brand
                                  AND cp1.customer_id != cp2.customer_id
    GROUP BY cp1.customer_id, cp2.customer_id
    HAVING COUNT(*) >= 2  -- At least 2 common categories
),
product_recommendations AS (
    SELECT 
        sc.customer_a as target_customer_id,
        oi.product_id,
        p.product_name,
        p.price,
        p.category_id,
        -- Recommendation score based on similar customers' purchases
        SUM(sc.similarity_score * oi.quantity) as recommendation_score,
        COUNT(DISTINCT sc.customer_b) as recommended_by_count,
        AVG(r.rating) as avg_rating
    FROM similar_customers sc
    JOIN orders o ON sc.customer_b = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN reviews r ON p.product_id = r.product_id
    WHERE o.order_status IN ('delivered', 'shipped')
      AND o.order_date >= CURRENT_DATE - INTERVAL '180 days'  -- Recent purchases
      -- Exclude products already bought by target customer
      AND NOT EXISTS (
          SELECT 1 FROM customer_purchase_history cph
          WHERE cph.customer_id = sc.customer_a 
            AND cph.product_id = oi.product_id
      )
    GROUP BY sc.customer_a, oi.product_id, p.product_name, p.price, p.category_id
)
SELECT 
    target_customer_id,
    product_id,
    product_name,
    price,
    ROUND(recommendation_score, 2) as recommendation_score,
    recommended_by_count,
    ROUND(COALESCE(avg_rating, 0), 1) as avg_rating,
    -- Final recommendation rank
    ROW_NUMBER() OVER (
        PARTITION BY target_customer_id 
        ORDER BY recommendation_score DESC, avg_rating DESC
    ) as recommendation_rank
FROM product_recommendations
WHERE recommendation_score > 0
  AND recommended_by_count >= 2  -- Recommended by at least 2 similar customers
ORDER BY target_customer_id, recommendation_rank
LIMIT 1000;
```

## Microsoft Interview Questions

### 7. Design a database schema for Microsoft Teams (Microsoft)
**Answer:**
```sql
-- Organizations table
CREATE TABLE organizations (
    org_id BIGSERIAL PRIMARY KEY,
    org_name VARCHAR(200) NOT NULL,
    domain VARCHAR(100) UNIQUE NOT NULL,
    subscription_type VARCHAR(50), -- Free, Business, Enterprise
    max_users INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    org_id BIGINT REFERENCES organizations(org_id),
    email VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    job_title VARCHAR(100),
    department VARCHAR(100),
    manager_id BIGINT REFERENCES users(user_id),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teams table
CREATE TABLE teams (
    team_id BIGSERIAL PRIMARY KEY,
    org_id BIGINT REFERENCES organizations(org_id),
    team_name VARCHAR(200) NOT NULL,
    description TEXT,
    team_type VARCHAR(20) DEFAULT 'private', -- public, private
    owner_id BIGINT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_archived BOOLEAN DEFAULT FALSE
);

-- Team members table
CREATE TABLE team_members (
    membership_id BIGSERIAL PRIMARY KEY,
    team_id BIGINT REFERENCES teams(team_id),
    user_id BIGINT REFERENCES users(user_id),
    role VARCHAR(20) DEFAULT 'member', -- owner, member, guest
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, user_id)
);

-- Channels table
CREATE TABLE channels (
    channel_id BIGSERIAL PRIMARY KEY,
    team_id BIGINT REFERENCES teams(team_id),
    channel_name VARCHAR(200) NOT NULL,
    description TEXT,
    channel_type VARCHAR(20) DEFAULT 'standard', -- standard, private, shared
    created_by BIGINT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_archived BOOLEAN DEFAULT FALSE
);

-- Messages table
CREATE TABLE messages (
    message_id BIGSERIAL PRIMARY KEY,
    channel_id BIGINT REFERENCES channels(channel_id),
    user_id BIGINT REFERENCES users(user_id),
    parent_message_id BIGINT REFERENCES messages(message_id), -- For replies
    message_text TEXT,
    message_type VARCHAR(20) DEFAULT 'text', -- text, file, image, meeting_invite
    edited_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Message reactions table
CREATE TABLE message_reactions (
    reaction_id BIGSERIAL PRIMARY KEY,
    message_id BIGINT REFERENCES messages(message_id),
    user_id BIGINT REFERENCES users(user_id),
    reaction_type VARCHAR(50), -- like, love, laugh, wow, sad, angry
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(message_id, user_id, reaction_type)
);

-- Meetings table
CREATE TABLE meetings (
    meeting_id BIGSERIAL PRIMARY KEY,
    team_id BIGINT REFERENCES teams(team_id),
    channel_id BIGINT REFERENCES channels(channel_id),
    organizer_id BIGINT REFERENCES users(user_id),
    meeting_title VARCHAR(200) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    meeting_url VARCHAR(500),
    is_recurring BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Meeting participants table
CREATE TABLE meeting_participants (
    participant_id BIGSERIAL PRIMARY KEY,
    meeting_id BIGINT REFERENCES meetings(meeting_id),
    user_id BIGINT REFERENCES users(user_id),
    join_time TIMESTAMP,
    leave_time TIMESTAMP,
    attendance_duration_minutes INT,
    UNIQUE(meeting_id, user_id)
);

-- Files table
CREATE TABLE files (
    file_id BIGSERIAL PRIMARY KEY,
    channel_id BIGINT REFERENCES channels(channel_id),
    message_id BIGINT REFERENCES messages(message_id),
    uploaded_by BIGINT REFERENCES users(user_id),
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT,
    file_type VARCHAR(50),
    file_url VARCHAR(500),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_messages_channel_time ON messages(channel_id, created_at DESC);
CREATE INDEX idx_team_members_user ON team_members(user_id);
CREATE INDEX idx_meetings_team_time ON meetings(team_id, start_time);
CREATE INDEX idx_users_org_active ON users(org_id, is_active);
```

### 8. Find the most active users across all teams in the last 30 days (Microsoft)
**Answer:**
```sql
WITH user_activity_metrics AS (
    SELECT 
        u.user_id,
        u.display_name,
        u.email,
        u.department,
        
        -- Message activity
        COUNT(DISTINCT m.message_id) as messages_sent,
        COUNT(DISTINCT m.channel_id) as channels_participated,
        COUNT(DISTINCT c.team_id) as teams_active_in,
        
        -- Meeting activity
        COUNT(DISTINCT mp.meeting_id) as meetings_attended,
        COALESCE(SUM(mp.attendance_duration_minutes), 0) as total_meeting_minutes,
        
        -- Reaction activity
        COUNT(DISTINCT mr.reaction_id) as reactions_given,
        
        -- File sharing activity
        COUNT(DISTINCT f.file_id) as files_shared
        
    FROM users u
    LEFT JOIN messages m ON u.user_id = m.user_id 
        AND m.created_at >= CURRENT_DATE - INTERVAL '30 days'
        AND m.is_deleted = FALSE
    LEFT JOIN channels c ON m.channel_id = c.channel_id
    LEFT JOIN meeting_participants mp ON u.user_id = mp.user_id
    LEFT JOIN meetings mt ON mp.meeting_id = mt.meeting_id
        AND mt.start_time >= CURRENT_DATE - INTERVAL '30 days'
    LEFT JOIN message_reactions mr ON u.user_id = mr.user_id
        AND mr.created_at >= CURRENT_DATE - INTERVAL '30 days'
    LEFT JOIN files f ON u.user_id = f.uploaded_by
        AND f.uploaded_at >= CURRENT_DATE - INTERVAL '30 days'
    WHERE u.is_active = TRUE
    GROUP BY u.user_id, u.display_name, u.email, u.department
),
activity_scores AS (
    SELECT 
        *,
        -- Calculate weighted activity score
        (messages_sent * 1.0 +
         channels_participated * 2.0 +
         teams_active_in * 3.0 +
         meetings_attended * 2.5 +
         (total_meeting_minutes / 60.0) * 1.5 +
         reactions_given * 0.5 +
         files_shared * 2.0) as activity_score,
         
        -- Calculate engagement metrics
        CASE 
            WHEN messages_sent > 0 THEN ROUND(reactions_given::DECIMAL / messages_sent, 2)
            ELSE 0
        END as avg_reactions_per_message,
        
        CASE 
            WHEN meetings_attended > 0 THEN ROUND(total_meeting_minutes::DECIMAL / meetings_attended, 1)
            ELSE 0
        END as avg_meeting_duration_minutes
        
    FROM user_activity_metrics
),
activity_rankings AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY activity_score DESC) as overall_rank,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY activity_score DESC) as dept_rank,
        PERCENT_RANK() OVER (ORDER BY activity_score) as activity_percentile
    FROM activity_scores
    WHERE activity_score > 0  -- Only include users with some activity
)
SELECT 
    display_name,
    email,
    department,
    messages_sent,
    channels_participated,
    teams_active_in,
    meetings_attended,
    total_meeting_minutes,
    reactions_given,
    files_shared,
    ROUND(activity_score, 2) as activity_score,
    overall_rank,
    dept_rank,
    ROUND(activity_percentile * 100, 1) as activity_percentile,
    avg_reactions_per_message,
    avg_meeting_duration_minutes,
    -- Activity level classification
    CASE 
        WHEN activity_percentile >= 0.9 THEN 'Highly Active'
        WHEN activity_percentile >= 0.7 THEN 'Very Active'
        WHEN activity_percentile >= 0.5 THEN 'Moderately Active'
        WHEN activity_percentile >= 0.3 THEN 'Somewhat Active'
        ELSE 'Low Activity'
    END as activity_level
FROM activity_rankings
ORDER BY activity_score DESC
LIMIT 50;
```

### 9. Analyze meeting patterns and productivity metrics (Microsoft)
**Answer:**
```sql
WITH meeting_analysis AS (
    SELECT 
        m.meeting_id,
        m.meeting_title,
        m.start_time,
        m.end_time,
        EXTRACT(HOUR FROM m.start_time) as meeting_hour,
        EXTRACT(DOW FROM m.start_time) as day_of_week, -- 0=Sunday, 6=Saturday
        EXTRACT(EPOCH FROM (m.end_time - m.start_time)) / 60 as scheduled_duration_minutes,
        
        -- Participant metrics
        COUNT(mp.user_id) as invited_participants,
        COUNT(CASE WHEN mp.join_time IS NOT NULL THEN 1 END) as actual_attendees,
        
        -- Attendance rate
        ROUND(
            COUNT(CASE WHEN mp.join_time IS NOT NULL THEN 1 END)::DECIMAL / 
            NULLIF(COUNT(mp.user_id), 0) * 100, 1
        ) as attendance_rate_percent,
        
        -- Average actual attendance duration
        ROUND(AVG(mp.attendance_duration_minutes), 1) as avg_attendance_duration,
        
        -- Meeting efficiency metrics
        CASE 
            WHEN AVG(mp.attendance_duration_minutes) >= EXTRACT(EPOCH FROM (m.end_time - m.start_time)) / 60 * 0.8 
            THEN 'High Engagement'
            WHEN AVG(mp.attendance_duration_minutes) >= EXTRACT(EPOCH FROM (m.end_time - m.start_time)) / 60 * 0.5 
            THEN 'Medium Engagement'
            ELSE 'Low Engagement'
        END as engagement_level
        
    FROM meetings m
    LEFT JOIN meeting_participants mp ON m.meeting_id = mp.meeting_id
    WHERE m.start_time >= CURRENT_DATE - INTERVAL '30 days'
      AND m.start_time < CURRENT_DATE
    GROUP BY m.meeting_id, m.meeting_title, m.start_time, m.end_time
),
time_pattern_analysis AS (
    SELECT 
        -- Time-based patterns
        meeting_hour,
        day_of_week,
        CASE 
            WHEN day_of_week IN (1,2,3,4,5) THEN 'Weekday'
            ELSE 'Weekend'
        END as day_type,
        CASE 
            WHEN meeting_hour BETWEEN 9 AND 11 THEN 'Morning (9-11 AM)'
            WHEN meeting_hour BETWEEN 12 AND 14 THEN 'Lunch (12-2 PM)'
            WHEN meeting_hour BETWEEN 15 AND 17 THEN 'Afternoon (3-5 PM)'
            ELSE 'Other Hours'
        END as time_slot,
        
        COUNT(*) as meeting_count,
        ROUND(AVG(attendance_rate_percent), 1) as avg_attendance_rate,
        ROUND(AVG(scheduled_duration_minutes), 1) as avg_scheduled_duration,
        ROUND(AVG(avg_attendance_duration), 1) as avg_actual_duration,
        
        -- Productivity score (attendance rate * engagement)
        ROUND(AVG(attendance_rate_percent * 
            CASE engagement_level 
                WHEN 'High Engagement' THEN 1.0
                WHEN 'Medium Engagement' THEN 0.7
                ELSE 0.4
            END), 1) as productivity_score
        
    FROM meeting_analysis
    GROUP BY meeting_hour, day_of_week, day_type, time_slot
),
meeting_size_analysis AS (
    SELECT 
        CASE 
            WHEN invited_participants <= 3 THEN 'Small (1-3)'
            WHEN invited_participants <= 8 THEN 'Medium (4-8)'
            WHEN invited_participants <= 15 THEN 'Large (9-15)'
            ELSE 'Very Large (16+)'
        END as meeting_size_category,
        
        COUNT(*) as meeting_count,
        ROUND(AVG(attendance_rate_percent), 1) as avg_attendance_rate,
        ROUND(AVG(scheduled_duration_minutes), 1) as avg_duration,
        
        -- Efficiency metrics by size
        COUNT(CASE WHEN engagement_level = 'High Engagement' THEN 1 END) as high_engagement_count,
        ROUND(
            COUNT(CASE WHEN engagement_level = 'High Engagement' THEN 1 END)::DECIMAL / 
            COUNT(*) * 100, 1
        ) as high_engagement_percent
        
    FROM meeting_analysis
    GROUP BY meeting_size_category
)
-- Final comprehensive report
SELECT 
    'Time Pattern Analysis' as analysis_type,
    CONCAT(day_type, ' - ', time_slot) as category,
    meeting_count::TEXT as metric1,
    avg_attendance_rate::TEXT as metric2,
    productivity_score::TEXT as metric3
FROM time_pattern_analysis
WHERE meeting_count >= 5  -- Only include patterns with sufficient data

UNION ALL

SELECT 
    'Meeting Size Analysis' as analysis_type,
    meeting_size_category as category,
    meeting_count::TEXT as metric1,
    avg_attendance_rate::TEXT as metric2,
    high_engagement_percent::TEXT as metric3
FROM meeting_size_analysis

ORDER BY analysis_type, 
    CASE 
        WHEN category LIKE '%Weekday%' THEN 1
        ELSE 2
    END,
    metric3::DECIMAL DESC;
```

## Meta Interview Questions

### 10. Design a database schema for Facebook's news feed (Meta)
**Answer:**
```sql
-- Users table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    profile_picture_url VARCHAR(500),
    cover_photo_url VARCHAR(500),
    bio TEXT,
    location VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    privacy_setting VARCHAR(20) DEFAULT 'friends', -- public, friends, private
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Friendships table (bidirectional relationships)
CREATE TABLE friendships (
    friendship_id BIGSERIAL PRIMARY KEY,
    user_id_1 BIGINT REFERENCES users(user_id),
    user_id_2 BIGINT REFERENCES users(user_id),
    status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, blocked
    requested_by BIGINT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP,
    UNIQUE(user_id_1, user_id_2),
    CHECK(user_id_1 != user_id_2)
);

-- Posts table
CREATE TABLE posts (
    post_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    content TEXT,
    post_type VARCHAR(20) DEFAULT 'text', -- text, photo, video, link, event
    media_urls TEXT[], -- Array of media URLs
    privacy_setting VARCHAR(20) DEFAULT 'friends',
    location VARCHAR(100),
    tagged_users BIGINT[], -- Array of tagged user IDs
    like_count BIGINT DEFAULT 0,
    comment_count BIGINT DEFAULT 0,
    share_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comments table
CREATE TABLE comments (
    comment_id BIGSERIAL PRIMARY KEY,
    post_id BIGINT REFERENCES posts(post_id),
    user_id BIGINT REFERENCES users(user_id),
    parent_comment_id BIGINT REFERENCES comments(comment_id),
    comment_text TEXT NOT NULL,
    like_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Likes table (for posts and comments)
CREATE TABLE likes (
    like_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    post_id BIGINT REFERENCES posts(post_id),
    comment_id BIGINT REFERENCES comments(comment_id),
    reaction_type VARCHAR(20) DEFAULT 'like', -- like, love, haha, wow, sad, angry
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, post_id, comment_id),
    CHECK((post_id IS NOT NULL AND comment_id IS NULL) OR (post_id IS NULL AND comment_id IS NOT NULL))
);

-- Shares table
CREATE TABLE shares (
    share_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    original_post_id BIGINT REFERENCES posts(post_id),
    shared_post_id BIGINT REFERENCES posts(post_id), -- The new post created when sharing
    share_text TEXT, -- Optional text when sharing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- News feed algorithm factors
CREATE TABLE user_interactions (
    interaction_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    target_user_id BIGINT REFERENCES users(user_id),
    interaction_type VARCHAR(20) NOT NULL, -- view, like, comment, share, click
    post_id BIGINT REFERENCES posts(post_id),
    interaction_weight DECIMAL(3,2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User preferences for feed algorithm
CREATE TABLE user_feed_preferences (
    preference_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    preferred_content_types TEXT[], -- Array of preferred content types
    close_friends BIGINT[], -- Array of close friend user IDs
    muted_users BIGINT[], -- Array of muted user IDs
    interest_keywords TEXT[], -- Array of interest keywords
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for news feed performance
CREATE INDEX idx_posts_user_time ON posts(user_id, created_at DESC);
CREATE INDEX idx_friendships_users ON friendships(user_id_1, user_id_2, status);
CREATE INDEX idx_user_interactions_user_time ON user_interactions(user_id, created_at DESC);
CREATE INDEX idx_likes_post ON likes(post_id, reaction_type);
CREATE INDEX idx_comments_post_time ON comments(post_id, created_at DESC);

-- Partitioning for large tables
CREATE TABLE posts_2024 PARTITION OF posts
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE user_interactions_2024 PARTITION OF user_interactions
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### 11. Generate personalized news feed with ranking algorithm (Meta)
**Answer:**
```sql
WITH user_social_graph AS (
    -- Get user's friends and their relationship strength
    SELECT 
        f.user_id_1 as user_id,
        f.user_id_2 as friend_id,
        CASE 
            WHEN f.accepted_at >= CURRENT_DATE - INTERVAL '30 days' THEN 1.2
            WHEN f.accepted_at >= CURRENT_DATE - INTERVAL '90 days' THEN 1.1
            ELSE 1.0
        END as recency_boost,
        
        -- Calculate interaction strength
        COALESCE(interaction_strength.strength, 0.1) as interaction_strength
    FROM friendships f
    LEFT JOIN (
        SELECT 
            user_id,
            target_user_id,
            SUM(interaction_weight) / COUNT(*) as strength
        FROM user_interactions
        WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY user_id, target_user_id
    ) interaction_strength ON f.user_id_1 = interaction_strength.user_id 
                           AND f.user_id_2 = interaction_strength.target_user_id
    WHERE f.status = 'accepted'
),
post_engagement_metrics AS (
    -- Calculate post engagement metrics
    SELECT 
        p.post_id,
        p.user_id as author_id,
        p.content,
        p.post_type,
        p.created_at,
        p.like_count,
        p.comment_count,
        p.share_count,
        
        -- Engagement rate calculation
        (p.like_count * 1.0 + p.comment_count * 2.0 + p.share_count * 3.0) as engagement_score,
        
        -- Time decay factor (newer posts get higher scores)
        CASE 
            WHEN p.created_at >= CURRENT_DATE - INTERVAL '2 hours' THEN 1.0
            WHEN p.created_at >= CURRENT_DATE - INTERVAL '6 hours' THEN 0.9
            WHEN p.created_at >= CURRENT_DATE - INTERVAL '12 hours' THEN 0.8
            WHEN p.created_at >= CURRENT_DATE - INTERVAL '24 hours' THEN 0.6
            WHEN p.created_at >= CURRENT_DATE - INTERVAL '48 hours' THEN 0.4
            ELSE 0.2
        END as time_decay_factor,
        
        -- Content type preference (based on user's historical interactions)
        CASE p.post_type
            WHEN 'photo' THEN 1.2
            WHEN 'video' THEN 1.3
            WHEN 'link' THEN 0.9
            ELSE 1.0
        END as content_type_multiplier
        
    FROM posts p
    WHERE p.created_at >= CURRENT_DATE - INTERVAL '7 days'
      AND p.privacy_setting IN ('public', 'friends')
),
user_feed_candidates AS (
    -- Generate feed candidates for a specific user (user_id = 12345)
    SELECT 
        12345 as target_user_id,  -- Replace with actual user ID
        pem.post_id,
        pem.author_id,
        pem.content,
        pem.post_type,
        pem.created_at,
        pem.engagement_score,
        pem.time_decay_factor,
        pem.content_type_multiplier,
        
        -- Social connection strength
        COALESCE(usg.interaction_strength * usg.recency_boost, 0.1) as social_strength,
        
        -- Check if user has already interacted with this post
        CASE 
            WHEN EXISTS (
                SELECT 1 FROM user_interactions ui 
                WHERE ui.user_id = 12345 
                  AND ui.post_id = pem.post_id
            ) THEN 0.5  -- Reduce score for already seen posts
            ELSE 1.0
        END as novelty_factor,
        
        -- Personal relevance based on user's interests
        CASE 
            WHEN pem.content ILIKE ANY(
                SELECT '%' || keyword || '%' 
                FROM user_feed_preferences ufp, 
                     UNNEST(ufp.interest_keywords) as keyword
                WHERE ufp.user_id = 12345
            ) THEN 1.3
            ELSE 1.0
        END as relevance_multiplier
        
    FROM post_engagement_metrics pem
    LEFT JOIN user_social_graph usg ON usg.user_id = 12345 
                                    AND usg.friend_id = pem.author_id
    WHERE pem.author_id != 12345  -- Exclude user's own posts from feed
      AND pem.author_id NOT IN (
          -- Exclude muted users
          SELECT UNNEST(muted_users) 
          FROM user_feed_preferences 
          WHERE user_id = 12345
      )
),
ranked_feed AS (
    SELECT 
        *,
        -- Calculate final ranking score
        (engagement_score * 0.3 +
         social_strength * 0.25 +
         time_decay_factor * 0.2 +
         content_type_multiplier * 0.1 +
         novelty_factor * 0.1 +
         relevance_multiplier * 0.05) as final_score,
         
        ROW_NUMBER() OVER (ORDER BY 
            (engagement_score * 0.3 +
             social_strength * 0.25 +
             time_decay_factor * 0.2 +
             content_type_multiplier * 0.1 +
             novelty_factor * 0.1 +
             relevance_multiplier * 0.05) DESC
        ) as feed_rank
    FROM user_feed_candidates
)
SELECT 
    post_id,
    author_id,
    LEFT(content, 100) || '...' as content_preview,
    post_type,
    created_at,
    ROUND(final_score, 3) as ranking_score,
    feed_rank,
    ROUND(engagement_score, 1) as engagement_score,
    ROUND(social_strength, 2) as social_strength,
    ROUND(time_decay_factor, 2) as time_decay,
    novelty_factor,
    relevance_multiplier
FROM ranked_feed
WHERE feed_rank <= 50  -- Top 50 posts for the feed
ORDER BY feed_rank;
```

### 12. Analyze viral content patterns and predict trending posts (Meta)
**Answer:**
```sql
WITH post_growth_metrics AS (
    -- Calculate growth metrics for posts in different time windows
    SELECT 
        p.post_id,
        p.user_id as author_id,
        p.content,
        p.post_type,
        p.created_at,
        
        -- Current engagement metrics
        p.like_count,
        p.comment_count,
        p.share_count,
        (p.like_count + p.comment_count * 2 + p.share_count * 3) as total_engagement,
        
        -- Time-based engagement analysis
        COUNT(CASE WHEN l.created_at <= p.created_at + INTERVAL '1 hour' THEN 1 END) as likes_1h,
        COUNT(CASE WHEN l.created_at <= p.created_at + INTERVAL '6 hours' THEN 1 END) as likes_6h,
        COUNT(CASE WHEN l.created_at <= p.created_at + INTERVAL '24 hours' THEN 1 END) as likes_24h,
        
        -- Engagement velocity (likes per hour in different periods)
        COUNT(CASE WHEN l.created_at <= p.created_at + INTERVAL '1 hour' THEN 1 END)::DECIMAL as velocity_1h,
        COUNT(CASE WHEN l.created_at BETWEEN p.created_at + INTERVAL '1 hour' 
                                        AND p.created_at + INTERVAL '6 hours' THEN 1 END)::DECIMAL / 5 as velocity_1_6h,
        COUNT(CASE WHEN l.created_at BETWEEN p.created_at + INTERVAL '6 hours' 
                                        AND p.created_at + INTERVAL '24 hours' THEN 1 END)::DECIMAL / 18 as velocity_6_24h,
        
        -- Share velocity (strong indicator of viral potential)
        COUNT(CASE WHEN s.created_at <= p.created_at + INTERVAL '1 hour' THEN 1 END) as shares_1h,
        COUNT(CASE WHEN s.created_at <= p.created_at + INTERVAL '6 hours' THEN 1 END) as shares_6h,
        
        -- Author influence metrics
        (SELECT COUNT(*) FROM friendships f WHERE f.user_id_2 = p.user_id AND f.status = 'accepted') as author_followers,
        
        -- Content characteristics
        LENGTH(p.content) as content_length,
        CASE WHEN p.media_urls IS NOT NULL AND array_length(p.media_urls, 1) > 0 THEN TRUE ELSE FALSE END as has_media
        
    FROM posts p
    LEFT JOIN likes l ON p.post_id = l.post_id
    LEFT JOIN shares s ON p.post_id = s.original_post_id
    WHERE p.created_at >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY p.post_id, p.user_id, p.content, p.post_type, p.created_at, 
             p.like_count, p.comment_count, p.share_count
),
viral_indicators AS (
    SELECT 
        *,
        -- Acceleration metrics (increasing engagement velocity)
        CASE 
            WHEN velocity_1_6h > velocity_1h * 1.5 THEN 'Accelerating'
            WHEN velocity_6_24h > velocity_1_6h * 1.2 THEN 'Sustained Growth'
            WHEN velocity_6_24h < velocity_1_6h * 0.5 THEN 'Declining'
            ELSE 'Stable'
        END as growth_pattern,
        
        -- Viral potential score
        (velocity_1h * 0.4 +
         CASE WHEN velocity_1_6h > velocity_1h THEN velocity_1_6h * 0.3 ELSE 0 END +
         shares_1h * 2.0 +
         shares_6h * 1.5 +
         CASE WHEN has_media THEN 1.2 ELSE 1.0 END +
         LOG(GREATEST(author_followers, 1)) * 0.1) as viral_score,
        
        -- Engagement rate relative to author's follower count
        CASE 
            WHEN author_followers > 0 THEN total_engagement::DECIMAL / author_followers
            ELSE total_engagement
        END as engagement_rate,
        
        -- Time since creation
        EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - created_at)) / 3600 as hours_since_creation
        
    FROM post_growth_metrics
),
trending_predictions AS (
    SELECT 
        *,
        -- Predict trending potential
        CASE 
            WHEN viral_score > 50 AND growth_pattern IN ('Accelerating', 'Sustained Growth') THEN 'High Viral Potential'
            WHEN viral_score > 20 AND shares_6h > 10 THEN 'Medium Viral Potential'
            WHEN viral_score > 10 AND velocity_1h > 5 THEN 'Low Viral Potential'
            ELSE 'Unlikely to Trend'
        END as trending_prediction,
        
        -- Rank posts by viral potential
        ROW_NUMBER() OVER (ORDER BY viral_score DESC) as viral_rank,
        
        -- Category-based ranking
        ROW_NUMBER() OVER (PARTITION BY post_type ORDER BY viral_score DESC) as category_rank
        
    FROM viral_indicators
    WHERE hours_since_creation <= 48  -- Focus on recent posts
)
SELECT 
    post_id,
    author_id,
    post_type,
    LEFT(content, 80) || '...' as content_preview,
    created_at,
    hours_since_creation,
    
    -- Engagement metrics
    total_engagement,
    like_count,
    comment_count,
    share_count,
    
    -- Growth metrics
    likes_1h,
    likes_6h,
    shares_1h,
    shares_6h,
    ROUND(velocity_1h, 2) as velocity_1h,
    ROUND(velocity_1_6h, 2) as velocity_1_6h,
    growth_pattern,
    
    -- Viral indicators
    ROUND(viral_score, 2) as viral_score,
    ROUND(engagement_rate, 4) as engagement_rate,
    trending_prediction,
    viral_rank,
    
    -- Author metrics
    author_followers,
    has_media
    
FROM trending_predictions
WHERE trending_prediction != 'Unlikely to Trend'
   OR viral_rank <= 20  -- Include top 20 regardless of prediction
ORDER BY viral_score DESC
LIMIT 50;
```

## System Design & Architecture Questions

### 13. Design a distributed database architecture for handling billions of social media posts
**Answer:**
```sql
-- Horizontal partitioning strategy for posts table
-- Partition by user_id hash for even distribution

-- Partition 1: user_id % 4 = 0
CREATE TABLE posts_partition_0 (
    LIKE posts INCLUDING ALL,
    CHECK (user_id % 4 = 0)
);

-- Partition 2: user_id % 4 = 1
CREATE TABLE posts_partition_1 (
    LIKE posts INCLUDING ALL,
    CHECK (user_id % 4 = 1)
);

-- Partition 3: user_id % 4 = 2
CREATE TABLE posts_partition_2 (
    LIKE posts INCLUDING ALL,
    CHECK (user_id % 4 = 2)
);

-- Partition 4: user_id % 4 = 3
CREATE TABLE posts_partition_3 (
    LIKE posts INCLUDING ALL,
    CHECK (user_id % 4 = 3)
);

-- Time-based partitioning for analytics
CREATE TABLE posts_analytics_2024_q1 PARTITION OF posts_analytics
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE posts_analytics_2024_q2 PARTITION OF posts_analytics
FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Read replica configuration for scaling reads
-- Master-slave setup with read routing
CREATE TABLE user_feed_cache (
    user_id BIGINT,
    feed_data JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

-- Materialized views for common queries
CREATE MATERIALIZED VIEW trending_posts_hourly AS
SELECT 
    post_id,
    author_id,
    engagement_score,
    created_at,
    ROW_NUMBER() OVER (ORDER BY engagement_score DESC) as trend_rank
FROM posts 
WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
  AND engagement_score > 100;

-- Refresh strategy
CREATE OR REPLACE FUNCTION refresh_trending_posts()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY trending_posts_hourly;
END;
$$ LANGUAGE plpgsql;

-- Automated refresh every 15 minutes
SELECT cron.schedule('refresh-trending', '*/15 * * * *', 'SELECT refresh_trending_posts();');
```

### 14. Implement a data archiving strategy for old social media data
**Answer:**
```sql
-- Create archive tables with same structure but different storage
CREATE TABLE posts_archive (
    LIKE posts INCLUDING ALL
) WITH (
    fillfactor = 100,  -- Optimize for read-only access
    autovacuum_enabled = false
);

-- Create archive function
CREATE OR REPLACE FUNCTION archive_old_posts()
RETURNS INTEGER AS $$
DECLARE
    archived_count INTEGER := 0;
    batch_size INTEGER := 10000;
    cutoff_date DATE := CURRENT_DATE - INTERVAL '2 years';
BEGIN
    -- Archive posts older than 2 years in batches
    LOOP
        WITH posts_to_archive AS (
            SELECT post_id
            FROM posts
            WHERE created_at < cutoff_date
            ORDER BY created_at
            LIMIT batch_size
        ),
        moved_posts AS (
            INSERT INTO posts_archive
            SELECT p.*
            FROM posts p
            INNER JOIN posts_to_archive pta ON p.post_id = pta.post_id
            RETURNING post_id
        ),
        deleted_posts AS (
            DELETE FROM posts
            WHERE post_id IN (SELECT post_id FROM moved_posts)
            RETURNING post_id
        )
        SELECT COUNT(*) INTO archived_count
        FROM deleted_posts;
        
        -- Exit if no more posts to archive
        EXIT WHEN archived_count = 0;
        
        -- Log progress
        RAISE NOTICE 'Archived % posts', archived_count;
        
        -- Small delay to avoid overwhelming the system
        PERFORM pg_sleep(1);
    END LOOP;
    
    RETURN archived_count;
END;
$$ LANGUAGE plpgsql;

-- Archive related data (comments, likes, etc.)
CREATE OR REPLACE FUNCTION archive_related_data()
RETURNS void AS $$
BEGIN
    -- Archive comments for archived posts
    INSERT INTO comments_archive
    SELECT c.*
    FROM comments c
    WHERE c.post_id IN (SELECT post_id FROM posts_archive)
      AND c.post_id NOT IN (SELECT post_id FROM posts);
    
    DELETE FROM comments
    WHERE post_id IN (SELECT post_id FROM posts_archive)
      AND post_id NOT IN (SELECT post_id FROM posts);
    
    -- Archive likes for archived posts
    INSERT INTO likes_archive
    SELECT l.*
    FROM likes l
    WHERE l.post_id IN (SELECT post_id FROM posts_archive)
      AND l.post_id NOT IN (SELECT post_id FROM posts);
    
    DELETE FROM likes
    WHERE post_id IN (SELECT post_id FROM posts_archive)
      AND post_id NOT IN (SELECT post_id FROM posts);
END;
$$ LANGUAGE plpgsql;

-- Schedule archiving process
SELECT cron.schedule(
    'archive-old-posts',
    '0 2 * * 0',  -- Run every Sunday at 2 AM
    'SELECT archive_old_posts(); SELECT archive_related_data();'
);

-- Create indexes on archive tables for occasional queries
CREATE INDEX idx_posts_archive_author_date ON posts_archive(author_id, created_at);
CREATE INDEX idx_posts_archive_created_at ON posts_archive(created_at);

-- Compressed storage for very old data
CREATE TABLE posts_cold_storage (
    year INTEGER,
    month INTEGER,
    compressed_data BYTEA,  -- Compressed JSON data
    record_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Function to compress data older than 5 years
CREATE OR REPLACE FUNCTION compress_ancient_posts()
RETURNS void AS $$
DECLARE
    target_year INTEGER;
    target_month INTEGER;
    compressed_data BYTEA;
    record_count INTEGER;
BEGIN
    FOR target_year IN 
        SELECT DISTINCT EXTRACT(YEAR FROM created_at)::INTEGER
        FROM posts_archive
        WHERE created_at < CURRENT_DATE - INTERVAL '5 years'
    LOOP
        FOR target_month IN 1..12 LOOP
            -- Compress monthly data
            SELECT 
                pg_compress(jsonb_agg(row_to_json(p))::text::bytea),
                COUNT(*)
            INTO compressed_data, record_count
            FROM posts_archive p
            WHERE EXTRACT(YEAR FROM created_at) = target_year
              AND EXTRACT(MONTH FROM created_at) = target_month;
            
            IF record_count > 0 THEN
                -- Store compressed data
                INSERT INTO posts_cold_storage (year, month, compressed_data, record_count)
                VALUES (target_year, target_month, compressed_data, record_count);
                
                -- Remove from archive
                DELETE FROM posts_archive
                WHERE EXTRACT(YEAR FROM created_at) = target_year
                  AND EXTRACT(MONTH FROM created_at) = target_month;
                
                RAISE NOTICE 'Compressed % posts from %-%', record_count, target_year, target_month;
            END IF;
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```