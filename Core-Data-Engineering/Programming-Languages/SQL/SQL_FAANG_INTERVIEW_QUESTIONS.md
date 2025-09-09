# FAANG SQL Interview Questions

## 🎯 **Quick Navigation & Study Guide**

### 📊 **FAANG Interview Success Metrics**
- **Technical Depth**: Advanced SQL concepts and optimization
- **Problem-Solving**: Complex analytical queries and business logic
- **Performance**: Query optimization and scalability considerations
- **Communication**: Clear explanation of approach and trade-offs
- **Real-World Application**: Understanding of production database challenges

### 🔥 **Most Critical Topics for FAANG**
1. **Window Functions & Advanced Analytics** - Essential for data analysis roles
2. **Complex Joins & Subqueries** - Multi-table relationship handling
3. **Performance Optimization** - Critical for large-scale systems
4. **Data Modeling & Schema Design** - System architecture understanding
5. **Business Logic Implementation** - Translating requirements to SQL

---

## 📋 Table of Contents

1. [Meta (Facebook) Questions](#meta-facebook-questions)
2. [Amazon Questions](#amazon-questions)
3. [Apple Questions](#apple-questions)
4. [Netflix Questions](#netflix-questions)
5. [Google Questions](#google-questions)
6. [Microsoft Questions](#microsoft-questions)
7. [Advanced FAANG Scenarios](#advanced-faang-scenarios)

---

## Meta (Facebook) Questions

### 1. **Active User Retention** (Meta)
**Problem**: Calculate the percentage of users who were active on both Day 1 and Day 7 after signing up.

```sql
-- Sample Data
CREATE TABLE user_activity (
    user_id INT,
    activity_date DATE,
    activity_type VARCHAR(50)
);

-- Solution
WITH day1_users AS (
    SELECT DISTINCT user_id
    FROM user_activity ua1
    JOIN users u ON ua1.user_id = u.user_id
    WHERE ua1.activity_date = u.signup_date + INTERVAL '1 day'
),
day7_users AS (
    SELECT DISTINCT user_id
    FROM user_activity ua2
    JOIN users u ON ua2.user_id = u.user_id
    WHERE ua2.activity_date = u.signup_date + INTERVAL '7 days'
)
SELECT 
    ROUND(
        COUNT(d7.user_id) * 100.0 / COUNT(d1.user_id), 2
    ) as retention_rate
FROM day1_users d1
LEFT JOIN day7_users d7 ON d1.user_id = d7.user_id;
```

### 2. **Page Recommendations** (Meta)
**Problem**: Find pages that should be recommended to users based on their friends' likes.

```sql
-- Sample Schema
CREATE TABLE friendships (
    user_id1 INT,
    user_id2 INT
);

CREATE TABLE page_likes (
    user_id INT,
    page_id INT,
    liked_date DATE
);

-- Solution
WITH user_friends AS (
    SELECT user_id1 as user_id, user_id2 as friend_id FROM friendships
    UNION
    SELECT user_id2 as user_id, user_id1 as friend_id FROM friendships
),
friend_likes AS (
    SELECT 
        uf.user_id,
        pl.page_id,
        COUNT(*) as friend_like_count
    FROM user_friends uf
    JOIN page_likes pl ON uf.friend_id = pl.user_id
    WHERE NOT EXISTS (
        SELECT 1 FROM page_likes pl2 
        WHERE pl2.user_id = uf.user_id 
        AND pl2.page_id = pl.page_id
    )
    GROUP BY uf.user_id, pl.page_id
)
SELECT 
    user_id,
    page_id,
    friend_like_count
FROM friend_likes
WHERE friend_like_count >= 2
ORDER BY user_id, friend_like_count DESC;
```

### 3. **Advertiser Status** (Meta)
**Problem**: Identify advertisers whose status changed from "NEW" or "EXISTING" to "CHURN" and back to "EXISTING" in consecutive periods.

```sql
-- Sample Data
CREATE TABLE advertiser_status (
    user_id INT,
    status VARCHAR(20), -- 'NEW', 'EXISTING', 'CHURN'
    period_start DATE,
    period_end DATE
);

-- Solution
WITH status_changes AS (
    SELECT 
        user_id,
        status,
        period_start,
        LAG(status) OVER (PARTITION BY user_id ORDER BY period_start) as prev_status,
        LEAD(status) OVER (PARTITION BY user_id ORDER BY period_start) as next_status
    FROM advertiser_status
)
SELECT DISTINCT user_id
FROM status_changes
WHERE prev_status IN ('NEW', 'EXISTING')
  AND status = 'CHURN'
  AND next_status = 'EXISTING';
```

---

## Amazon Questions

### 4. **Highest-Grossing Items** (Amazon)
**Problem**: Find the highest-grossing items for each category.

```sql
-- Sample Schema
CREATE TABLE product_spend (
    category VARCHAR(50),
    product VARCHAR(100),
    user_id INT,
    spend DECIMAL(10,2),
    transaction_date DATE
);

-- Solution
WITH category_totals AS (
    SELECT 
        category,
        product,
        SUM(spend) as total_spend,
        RANK() OVER (PARTITION BY category ORDER BY SUM(spend) DESC) as spend_rank
    FROM product_spend
    GROUP BY category, product
)
SELECT 
    category,
    product,
    total_spend
FROM category_totals
WHERE spend_rank = 1
ORDER BY total_spend DESC;
```

### 5. **Average Review Ratings** (Amazon)
**Problem**: Calculate the average rating for each product, excluding reviews from the same user on the same day.

```sql
-- Sample Schema
CREATE TABLE reviews (
    review_id INT,
    user_id INT,
    product_id INT,
    rating INT,
    review_date DATE
);

-- Solution
WITH deduplicated_reviews AS (
    SELECT 
        user_id,
        product_id,
        rating,
        review_date,
        ROW_NUMBER() OVER (
            PARTITION BY user_id, product_id, review_date 
            ORDER BY review_id
        ) as rn
    FROM reviews
)
SELECT 
    product_id,
    ROUND(AVG(rating::DECIMAL), 2) as avg_rating
FROM deduplicated_reviews
WHERE rn = 1
GROUP BY product_id
HAVING COUNT(*) >= 3  -- Minimum 3 reviews
ORDER BY avg_rating DESC;
```

### 6. **Prime Subscription Rate** (Amazon)
**Problem**: Calculate the percentage of Prime subscribers by country.

```sql
-- Sample Schema
CREATE TABLE users (
    user_id INT,
    country VARCHAR(50),
    subscription_type VARCHAR(20) -- 'Prime', 'Basic', 'Premium'
);

-- Solution
SELECT 
    country,
    ROUND(
        COUNT(CASE WHEN subscription_type = 'Prime' THEN 1 END) * 100.0 / 
        COUNT(*), 2
    ) as prime_percentage
FROM users
GROUP BY country
HAVING COUNT(*) >= 100  -- Minimum sample size
ORDER BY prime_percentage DESC;
```

---

## Apple Questions

### 7. **App Click-through Rate** (Apple)
**Problem**: Calculate the click-through rate (CTR) for each app.

```sql
-- Sample Schema
CREATE TABLE events (
    app_id INT,
    event_type VARCHAR(20), -- 'impression', 'click'
    timestamp TIMESTAMP
);

-- Solution
WITH app_metrics AS (
    SELECT 
        app_id,
        COUNT(CASE WHEN event_type = 'impression' THEN 1 END) as impressions,
        COUNT(CASE WHEN event_type = 'click' THEN 1 END) as clicks
    FROM events
    GROUP BY app_id
)
SELECT 
    app_id,
    impressions,
    clicks,
    CASE 
        WHEN impressions > 0 THEN 
            ROUND(clicks * 100.0 / impressions, 2)
        ELSE 0 
    END as ctr_percentage
FROM app_metrics
WHERE impressions > 0
ORDER BY ctr_percentage DESC;
```

### 8. **iPhone vs Android Users** (Apple)
**Problem**: Compare user engagement between iPhone and Android users.

```sql
-- Sample Schema
CREATE TABLE user_sessions (
    user_id INT,
    device_type VARCHAR(20), -- 'iPhone', 'Android'
    session_duration INT, -- in minutes
    session_date DATE
);

-- Solution
SELECT 
    device_type,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(*) as total_sessions,
    ROUND(AVG(session_duration), 2) as avg_session_duration,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT user_id), 2) as sessions_per_user
FROM user_sessions
WHERE session_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY device_type
ORDER BY avg_session_duration DESC;
```

---

## Netflix Questions

### 9. **Content Popularity** (Netflix)
**Problem**: Find the most popular content by genre based on viewing hours.

```sql
-- Sample Schema
CREATE TABLE content_views (
    content_id INT,
    user_id INT,
    genre VARCHAR(50),
    viewing_hours DECIMAL(5,2),
    view_date DATE
);

-- Solution
WITH genre_popularity AS (
    SELECT 
        genre,
        content_id,
        SUM(viewing_hours) as total_hours,
        COUNT(DISTINCT user_id) as unique_viewers,
        RANK() OVER (PARTITION BY genre ORDER BY SUM(viewing_hours) DESC) as popularity_rank
    FROM content_views
    WHERE view_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY genre, content_id
)
SELECT 
    genre,
    content_id,
    total_hours,
    unique_viewers,
    ROUND(total_hours / unique_viewers, 2) as hours_per_viewer
FROM genre_popularity
WHERE popularity_rank <= 3
ORDER BY genre, total_hours DESC;
```

### 10. **Subscription Churn Analysis** (Netflix)
**Problem**: Identify users likely to churn based on viewing patterns.

```sql
-- Sample Schema
CREATE TABLE user_activity (
    user_id INT,
    activity_date DATE,
    content_watched INT,
    total_watch_time INT -- in minutes
);

-- Solution
WITH user_metrics AS (
    SELECT 
        user_id,
        COUNT(DISTINCT activity_date) as active_days_last_30,
        AVG(total_watch_time) as avg_daily_watch_time,
        MAX(activity_date) as last_activity_date,
        CURRENT_DATE - MAX(activity_date) as days_since_last_activity
    FROM user_activity
    WHERE activity_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
),
churn_risk AS (
    SELECT 
        user_id,
        active_days_last_30,
        avg_daily_watch_time,
        days_since_last_activity,
        CASE 
            WHEN days_since_last_activity >= 14 THEN 'High Risk'
            WHEN days_since_last_activity >= 7 OR active_days_last_30 <= 5 THEN 'Medium Risk'
            WHEN avg_daily_watch_time < 30 THEN 'Low Risk'
            ELSE 'Engaged'
        END as churn_risk_category
    FROM user_metrics
)
SELECT 
    churn_risk_category,
    COUNT(*) as user_count,
    ROUND(AVG(active_days_last_30), 1) as avg_active_days,
    ROUND(AVG(avg_daily_watch_time), 1) as avg_watch_time
FROM churn_risk
GROUP BY churn_risk_category
ORDER BY 
    CASE churn_risk_category 
        WHEN 'High Risk' THEN 1 
        WHEN 'Medium Risk' THEN 2 
        WHEN 'Low Risk' THEN 3 
        ELSE 4 
    END;
```

---

## Google Questions

### 11. **Search Query Analysis** (Google)
**Problem**: Find the top search queries that have the highest click-through rate.

```sql
-- Sample Schema
CREATE TABLE search_events (
    query_id INT,
    query_text VARCHAR(255),
    event_type VARCHAR(20), -- 'search', 'click'
    user_id INT,
    timestamp TIMESTAMP
);

-- Solution
WITH query_metrics AS (
    SELECT 
        query_text,
        COUNT(CASE WHEN event_type = 'search' THEN 1 END) as searches,
        COUNT(CASE WHEN event_type = 'click' THEN 1 END) as clicks
    FROM search_events
    WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
    GROUP BY query_text
    HAVING COUNT(CASE WHEN event_type = 'search' THEN 1 END) >= 100
)
SELECT 
    query_text,
    searches,
    clicks,
    ROUND(clicks * 100.0 / searches, 2) as ctr_percentage
FROM query_metrics
ORDER BY ctr_percentage DESC, searches DESC
LIMIT 20;
```

### 12. **Ad Performance Optimization** (Google)
**Problem**: Calculate the return on ad spend (ROAS) for different campaigns.

```sql
-- Sample Schema
CREATE TABLE ad_campaigns (
    campaign_id INT,
    ad_spend DECIMAL(10,2),
    impressions INT,
    clicks INT,
    conversions INT,
    revenue DECIMAL(10,2),
    campaign_date DATE
);

-- Solution
SELECT 
    campaign_id,
    SUM(ad_spend) as total_spend,
    SUM(revenue) as total_revenue,
    SUM(impressions) as total_impressions,
    SUM(clicks) as total_clicks,
    SUM(conversions) as total_conversions,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) as roas,
    ROUND(SUM(clicks) * 100.0 / NULLIF(SUM(impressions), 0), 2) as ctr,
    ROUND(SUM(conversions) * 100.0 / NULLIF(SUM(clicks), 0), 2) as conversion_rate,
    ROUND(SUM(ad_spend) / NULLIF(SUM(conversions), 0), 2) as cost_per_conversion
FROM ad_campaigns
WHERE campaign_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY campaign_id
HAVING SUM(ad_spend) > 0
ORDER BY roas DESC;
```

---

## Microsoft Questions

### 13. **Teams Usage Analytics** (Microsoft)
**Problem**: Analyze Microsoft Teams usage patterns and identify power users.

```sql
-- Sample Schema
CREATE TABLE teams_activity (
    user_id INT,
    activity_type VARCHAR(50), -- 'meeting', 'chat', 'file_share', 'call'
    duration_minutes INT,
    activity_date DATE
);

-- Solution
WITH user_activity_summary AS (
    SELECT 
        user_id,
        COUNT(*) as total_activities,
        COUNT(CASE WHEN activity_type = 'meeting' THEN 1 END) as meetings,
        COUNT(CASE WHEN activity_type = 'chat' THEN 1 END) as chats,
        COUNT(CASE WHEN activity_type = 'call' THEN 1 END) as calls,
        SUM(duration_minutes) as total_duration,
        COUNT(DISTINCT activity_date) as active_days
    FROM teams_activity
    WHERE activity_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
),
user_segments AS (
    SELECT 
        user_id,
        total_activities,
        meetings,
        chats,
        calls,
        total_duration,
        active_days,
        CASE 
            WHEN total_activities >= 200 AND active_days >= 20 THEN 'Power User'
            WHEN total_activities >= 100 AND active_days >= 15 THEN 'Regular User'
            WHEN total_activities >= 50 AND active_days >= 10 THEN 'Moderate User'
            ELSE 'Light User'
        END as user_segment
    FROM user_activity_summary
)
SELECT 
    user_segment,
    COUNT(*) as user_count,
    ROUND(AVG(total_activities), 1) as avg_activities,
    ROUND(AVG(total_duration), 1) as avg_duration_minutes,
    ROUND(AVG(active_days), 1) as avg_active_days
FROM user_segments
GROUP BY user_segment
ORDER BY 
    CASE user_segment 
        WHEN 'Power User' THEN 1 
        WHEN 'Regular User' THEN 2 
        WHEN 'Moderate User' THEN 3 
        ELSE 4 
    END;
```

### 14. **Office 365 License Optimization** (Microsoft)
**Problem**: Identify underutilized Office 365 licenses for cost optimization.

```sql
-- Sample Schema
CREATE TABLE license_usage (
    user_id INT,
    license_type VARCHAR(50), -- 'E1', 'E3', 'E5'
    app_name VARCHAR(50), -- 'Word', 'Excel', 'PowerPoint', 'Teams'
    usage_hours DECIMAL(5,2),
    usage_date DATE
);

-- Solution
WITH user_license_usage AS (
    SELECT 
        user_id,
        license_type,
        SUM(usage_hours) as total_usage_hours,
        COUNT(DISTINCT app_name) as apps_used,
        COUNT(DISTINCT usage_date) as active_days,
        AVG(usage_hours) as avg_daily_usage
    FROM license_usage
    WHERE usage_date >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY user_id, license_type
),
license_recommendations AS (
    SELECT 
        user_id,
        license_type,
        total_usage_hours,
        apps_used,
        active_days,
        avg_daily_usage,
        CASE 
            WHEN total_usage_hours < 10 AND active_days < 30 THEN 'Consider Downgrade'
            WHEN total_usage_hours < 50 AND apps_used <= 2 THEN 'Review Usage'
            WHEN total_usage_hours >= 200 AND apps_used >= 4 THEN 'Optimal Usage'
            ELSE 'Standard Usage'
        END as recommendation
    FROM user_license_usage
)
SELECT 
    license_type,
    recommendation,
    COUNT(*) as user_count,
    ROUND(AVG(total_usage_hours), 1) as avg_usage_hours,
    ROUND(AVG(apps_used), 1) as avg_apps_used
FROM license_recommendations
GROUP BY license_type, recommendation
ORDER BY license_type, 
    CASE recommendation 
        WHEN 'Consider Downgrade' THEN 1 
        WHEN 'Review Usage' THEN 2 
        WHEN 'Standard Usage' THEN 3 
        ELSE 4 
    END;
```

---

## Advanced FAANG Scenarios

### 15. **Cross-Platform User Journey** (Multi-Company)
**Problem**: Track user journey across multiple platforms and identify conversion funnels.

```sql
-- Sample Schema
CREATE TABLE user_events (
    user_id INT,
    platform VARCHAR(20), -- 'web', 'mobile', 'tablet'
    event_type VARCHAR(50), -- 'page_view', 'add_to_cart', 'purchase'
    event_timestamp TIMESTAMP,
    session_id VARCHAR(100)
);

-- Solution
WITH user_sessions AS (
    SELECT 
        user_id,
        session_id,
        platform,
        MIN(event_timestamp) as session_start,
        MAX(event_timestamp) as session_end,
        COUNT(*) as total_events,
        COUNT(CASE WHEN event_type = 'page_view' THEN 1 END) as page_views,
        COUNT(CASE WHEN event_type = 'add_to_cart' THEN 1 END) as cart_adds,
        COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as purchases
    FROM user_events
    WHERE event_timestamp >= CURRENT_TIMESTAMP - INTERVAL '7 days'
    GROUP BY user_id, session_id, platform
),
conversion_funnel AS (
    SELECT 
        platform,
        COUNT(*) as total_sessions,
        COUNT(CASE WHEN page_views > 0 THEN 1 END) as sessions_with_views,
        COUNT(CASE WHEN cart_adds > 0 THEN 1 END) as sessions_with_cart,
        COUNT(CASE WHEN purchases > 0 THEN 1 END) as sessions_with_purchase
    FROM user_sessions
    GROUP BY platform
)
SELECT 
    platform,
    total_sessions,
    sessions_with_views,
    sessions_with_cart,
    sessions_with_purchase,
    ROUND(sessions_with_cart * 100.0 / NULLIF(sessions_with_views, 0), 2) as view_to_cart_rate,
    ROUND(sessions_with_purchase * 100.0 / NULLIF(sessions_with_cart, 0), 2) as cart_to_purchase_rate,
    ROUND(sessions_with_purchase * 100.0 / NULLIF(sessions_with_views, 0), 2) as overall_conversion_rate
FROM conversion_funnel
ORDER BY overall_conversion_rate DESC;
```

### 16. **Real-time Anomaly Detection** (Multi-Company)
**Problem**: Detect anomalies in user behavior patterns for fraud detection.

```sql
-- Sample Schema
CREATE TABLE user_transactions (
    transaction_id INT,
    user_id INT,
    amount DECIMAL(10,2),
    transaction_type VARCHAR(50),
    location VARCHAR(100),
    transaction_timestamp TIMESTAMP
);

-- Solution
WITH user_baselines AS (
    SELECT 
        user_id,
        AVG(amount) as avg_transaction_amount,
        STDDEV(amount) as stddev_amount,
        COUNT(*) as total_transactions,
        COUNT(DISTINCT DATE(transaction_timestamp)) as active_days,
        COUNT(DISTINCT location) as unique_locations
    FROM user_transactions
    WHERE transaction_timestamp >= CURRENT_TIMESTAMP - INTERVAL '30 days'
    GROUP BY user_id
    HAVING COUNT(*) >= 10  -- Minimum transaction history
),
recent_transactions AS (
    SELECT 
        ut.*,
        ub.avg_transaction_amount,
        ub.stddev_amount,
        ub.unique_locations
    FROM user_transactions ut
    JOIN user_baselines ub ON ut.user_id = ub.user_id
    WHERE ut.transaction_timestamp >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
),
anomaly_detection AS (
    SELECT 
        transaction_id,
        user_id,
        amount,
        location,
        transaction_timestamp,
        avg_transaction_amount,
        ABS(amount - avg_transaction_amount) / NULLIF(stddev_amount, 0) as z_score,
        CASE 
            WHEN ABS(amount - avg_transaction_amount) / NULLIF(stddev_amount, 0) > 3 THEN 'Amount Anomaly'
            WHEN amount > avg_transaction_amount * 5 THEN 'Large Transaction'
            ELSE 'Normal'
        END as anomaly_type
    FROM recent_transactions
    WHERE stddev_amount > 0
)
SELECT 
    user_id,
    transaction_id,
    amount,
    avg_transaction_amount,
    z_score,
    anomaly_type,
    transaction_timestamp
FROM anomaly_detection
WHERE anomaly_type != 'Normal'
ORDER BY z_score DESC, transaction_timestamp DESC;
```

### 17. **A/B Test Analysis** (Multi-Company)
**Problem**: Analyze A/B test results with statistical significance.

```sql
-- Sample Schema
CREATE TABLE ab_test_results (
    user_id INT,
    test_group VARCHAR(10), -- 'A', 'B'
    converted BOOLEAN,
    test_start_date DATE,
    conversion_date DATE
);

-- Solution
WITH test_metrics AS (
    SELECT 
        test_group,
        COUNT(*) as total_users,
        COUNT(CASE WHEN converted = TRUE THEN 1 END) as conversions,
        COUNT(CASE WHEN converted = TRUE THEN 1 END) * 1.0 / COUNT(*) as conversion_rate
    FROM ab_test_results
    GROUP BY test_group
),
statistical_test AS (
    SELECT 
        a.conversion_rate as rate_a,
        b.conversion_rate as rate_b,
        a.total_users as users_a,
        b.total_users as users_b,
        a.conversions as conv_a,
        b.conversions as conv_b,
        (b.conversion_rate - a.conversion_rate) as rate_difference,
        -- Simplified z-test calculation
        SQRT(
            (a.conversion_rate * (1 - a.conversion_rate) / a.total_users) +
            (b.conversion_rate * (1 - b.conversion_rate) / b.total_users)
        ) as standard_error
    FROM test_metrics a
    CROSS JOIN test_metrics b
    WHERE a.test_group = 'A' AND b.test_group = 'B'
)
SELECT 
    'Group A' as test_group,
    users_a as users,
    conv_a as conversions,
    ROUND(rate_a * 100, 2) as conversion_rate_percent
FROM statistical_test
UNION ALL
SELECT 
    'Group B' as test_group,
    users_b as users,
    conv_b as conversions,
    ROUND(rate_b * 100, 2) as conversion_rate_percent
FROM statistical_test
UNION ALL
SELECT 
    'Difference (B-A)' as test_group,
    NULL as users,
    NULL as conversions,
    ROUND(rate_difference * 100, 2) as conversion_rate_percent
FROM statistical_test;
```

---

## 🎯 **FAANG Interview Tips**

### **Technical Excellence**
- **Optimize for Scale**: Always consider performance implications
- **Handle Edge Cases**: NULL values, empty datasets, data quality issues
- **Explain Trade-offs**: Discuss different approaches and their pros/cons
- **Use Advanced Features**: Window functions, CTEs, analytical functions

### **Business Understanding**
- **Ask Clarifying Questions**: Understand the business context
- **Validate Assumptions**: Confirm data definitions and requirements
- **Consider Real-world Constraints**: Data freshness, system limitations
- **Think About Monitoring**: How would you track this in production?

### **Communication Skills**
- **Walk Through Your Approach**: Explain your thought process
- **Start Simple**: Begin with basic solution, then optimize
- **Test Your Logic**: Verify with sample data
- **Discuss Alternatives**: Show awareness of different solutions

---

## 📚 **Additional Resources**

### **Practice Platforms**
- [DataLemur](https://datalemur.com/) - FAANG-specific SQL questions
- [LeetCode Database](https://leetcode.com/problemset/database/) - Algorithm-style SQL problems
- [HackerRank SQL](https://www.hackerrank.com/domains/sql) - Comprehensive SQL challenges
- [Stratascratch](https://www.stratascratch.com/) - Real company interview questions

### **Key Concepts to Master**
- **Window Functions**: ROW_NUMBER(), RANK(), LAG(), LEAD()
- **Advanced Joins**: Self-joins, multiple table joins, complex conditions
- **Subqueries & CTEs**: Correlated subqueries, recursive CTEs
- **Performance Optimization**: Indexing strategies, query execution plans
- **Data Quality**: Handling duplicates, missing data, data validation

### **Company-Specific Focus Areas**
- **Meta**: Social network analysis, user engagement metrics
- **Amazon**: E-commerce analytics, recommendation systems
- **Google**: Search and advertising metrics, large-scale data processing
- **Netflix**: Content recommendation, user behavior analysis
- **Apple**: Product analytics, ecosystem integration
- **Microsoft**: Enterprise software metrics, productivity analysis

---

## Key Takeaways

1. **Master Advanced SQL**: Window functions and complex joins are essential
2. **Think at Scale**: Consider performance and optimization from the start
3. **Understand Business Context**: Connect technical solutions to business value
4. **Practice Real Scenarios**: Use actual company data patterns and problems
5. **Communicate Clearly**: Explain your approach and reasoning throughout
6. **Handle Edge Cases**: Always consider data quality and boundary conditions
7. **Optimize Iteratively**: Start with working solution, then improve performance
8. **Stay Current**: Keep up with latest SQL features and best practices