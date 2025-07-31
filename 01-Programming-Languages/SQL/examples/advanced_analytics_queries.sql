-- Advanced Analytics SQL Queries for Data Engineering
-- This file contains practical examples of complex analytical queries

-- =====================================================
-- 1. COHORT ANALYSIS
-- =====================================================

-- Customer cohort analysis to track retention
WITH first_purchase AS (
    SELECT 
        customer_id,
        MIN(DATE_TRUNC('month', order_date)) as cohort_month
    FROM orders
    GROUP BY customer_id
),
customer_activities AS (
    SELECT 
        fp.customer_id,
        fp.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month
    FROM first_purchase fp
    JOIN orders o ON fp.customer_id = o.customer_id
),
cohort_data AS (
    SELECT 
        cohort_month,
        activity_month,
        EXTRACT(YEAR FROM AGE(activity_month, cohort_month)) * 12 + 
        EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) as period_number,
        COUNT(DISTINCT customer_id) as customers
    FROM customer_activities
    GROUP BY cohort_month, activity_month
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) as cohort_size
    FROM first_purchase
    GROUP BY cohort_month
)
SELECT 
    cd.cohort_month,
    cs.cohort_size,
    cd.period_number,
    cd.customers,
    ROUND(100.0 * cd.customers / cs.cohort_size, 2) as retention_rate
FROM cohort_data cd
JOIN cohort_sizes cs ON cd.cohort_month = cs.cohort_month
ORDER BY cd.cohort_month, cd.period_number;

-- =====================================================
-- 2. RFM ANALYSIS (Recency, Frequency, Monetary)
-- =====================================================

WITH customer_metrics AS (
    SELECT 
        customer_id,
        MAX(order_date) as last_order_date,
        COUNT(*) as frequency,
        SUM(amount) as monetary_value,
        CURRENT_DATE - MAX(order_date) as recency_days
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency,
        monetary_value,
        NTILE(5) OVER (ORDER BY recency_days DESC) as recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) as frequency_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) as monetary_score
    FROM customer_metrics
),
rfm_segments AS (
    SELECT 
        customer_id,
        recency_score,
        frequency_score,
        monetary_score,
        CASE 
            WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
            WHEN recency_score >= 3 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Loyal Customers'
            WHEN recency_score >= 3 AND frequency_score <= 2 AND monetary_score >= 3 THEN 'Potential Loyalists'
            WHEN recency_score >= 4 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'New Customers'
            WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'At Risk'
            WHEN recency_score <= 2 AND frequency_score <= 2 AND monetary_score >= 3 THEN 'Cannot Lose Them'
            WHEN recency_score <= 2 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'Lost'
            ELSE 'Others'
        END as rfm_segment
    FROM rfm_scores
)
SELECT 
    rfm_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(recency_score), 2) as avg_recency,
    ROUND(AVG(frequency_score), 2) as avg_frequency,
    ROUND(AVG(monetary_score), 2) as avg_monetary
FROM rfm_segments
GROUP BY rfm_segment
ORDER BY customer_count DESC;

-- =====================================================
-- 3. FUNNEL ANALYSIS
-- =====================================================

WITH funnel_events AS (
    SELECT 
        user_id,
        event_type,
        event_timestamp,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_timestamp) as event_sequence
    FROM user_events
    WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
    AND event_type IN ('page_view', 'add_to_cart', 'checkout', 'purchase')
),
funnel_steps AS (
    SELECT 
        user_id,
        MAX(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) as step_1_page_view,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) as step_2_add_to_cart,
        MAX(CASE WHEN event_type = 'checkout' THEN 1 ELSE 0 END) as step_3_checkout,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) as step_4_purchase
    FROM funnel_events
    GROUP BY user_id
)
SELECT 
    'Page View' as step,
    1 as step_number,
    SUM(step_1_page_view) as users,
    100.0 as conversion_rate
FROM funnel_steps
WHERE step_1_page_view = 1

UNION ALL

SELECT 
    'Add to Cart' as step,
    2 as step_number,
    SUM(step_2_add_to_cart) as users,
    ROUND(100.0 * SUM(step_2_add_to_cart) / SUM(step_1_page_view), 2) as conversion_rate
FROM funnel_steps
WHERE step_1_page_view = 1

UNION ALL

SELECT 
    'Checkout' as step,
    3 as step_number,
    SUM(step_3_checkout) as users,
    ROUND(100.0 * SUM(step_3_checkout) / SUM(step_2_add_to_cart), 2) as conversion_rate
FROM funnel_steps
WHERE step_2_add_to_cart = 1

UNION ALL

SELECT 
    'Purchase' as step,
    4 as step_number,
    SUM(step_4_purchase) as users,
    ROUND(100.0 * SUM(step_4_purchase) / SUM(step_3_checkout), 2) as conversion_rate
FROM funnel_steps
WHERE step_3_checkout = 1

ORDER BY step_number;

-- =====================================================
-- 4. CUSTOMER LIFETIME VALUE (CLV) CALCULATION
-- =====================================================

WITH customer_summary AS (
    SELECT 
        customer_id,
        MIN(order_date) as first_order_date,
        MAX(order_date) as last_order_date,
        COUNT(*) as total_orders,
        SUM(amount) as total_spent,
        AVG(amount) as avg_order_value,
        EXTRACT(DAYS FROM (MAX(order_date) - MIN(order_date))) + 1 as customer_lifespan_days
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(*) > 1  -- Only customers with multiple orders
),
clv_metrics AS (
    SELECT 
        customer_id,
        total_orders,
        total_spent,
        avg_order_value,
        customer_lifespan_days,
        CASE 
            WHEN customer_lifespan_days > 0 
            THEN total_orders::DECIMAL / (customer_lifespan_days / 365.25)
            ELSE 0 
        END as purchase_frequency_per_year,
        CASE 
            WHEN total_orders > 1 
            THEN customer_lifespan_days::DECIMAL / (total_orders - 1)
            ELSE NULL 
        END as avg_days_between_orders
    FROM customer_summary
),
clv_calculation AS (
    SELECT 
        customer_id,
        avg_order_value,
        purchase_frequency_per_year,
        avg_days_between_orders,
        -- Simple CLV calculation: AOV * Purchase Frequency * Estimated Lifespan
        avg_order_value * purchase_frequency_per_year * 3 as estimated_clv_3_years,
        CASE 
            WHEN avg_days_between_orders IS NOT NULL 
            THEN avg_order_value * (365.25 / avg_days_between_orders) * 2
            ELSE avg_order_value * purchase_frequency_per_year * 2
        END as estimated_clv_2_years
    FROM clv_metrics
)
SELECT 
    CASE 
        WHEN estimated_clv_3_years >= 1000 THEN 'High Value (>$1000)'
        WHEN estimated_clv_3_years >= 500 THEN 'Medium Value ($500-$1000)'
        WHEN estimated_clv_3_years >= 100 THEN 'Low Value ($100-$500)'
        ELSE 'Very Low Value (<$100)'
    END as clv_segment,
    COUNT(*) as customer_count,
    ROUND(AVG(estimated_clv_3_years), 2) as avg_clv_3_years,
    ROUND(AVG(avg_order_value), 2) as avg_order_value,
    ROUND(AVG(purchase_frequency_per_year), 2) as avg_purchase_frequency
FROM clv_calculation
GROUP BY 
    CASE 
        WHEN estimated_clv_3_years >= 1000 THEN 'High Value (>$1000)'
        WHEN estimated_clv_3_years >= 500 THEN 'Medium Value ($500-$1000)'
        WHEN estimated_clv_3_years >= 100 THEN 'Low Value ($100-$500)'
        ELSE 'Very Low Value (<$100)'
    END
ORDER BY avg_clv_3_years DESC;

-- =====================================================
-- 5. SEASONAL TREND ANALYSIS
-- =====================================================

WITH monthly_sales AS (
    SELECT 
        EXTRACT(YEAR FROM order_date) as year,
        EXTRACT(MONTH FROM order_date) as month,
        SUM(amount) as monthly_revenue,
        COUNT(*) as monthly_orders,
        COUNT(DISTINCT customer_id) as unique_customers
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '3 years'
    GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date)
),
seasonal_analysis AS (
    SELECT 
        year,
        month,
        monthly_revenue,
        monthly_orders,
        unique_customers,
        LAG(monthly_revenue, 12) OVER (ORDER BY year, month) as same_month_last_year,
        AVG(monthly_revenue) OVER (
            ORDER BY year, month 
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        ) as rolling_12_month_avg,
        CASE 
            WHEN month IN (12, 1, 2) THEN 'Winter'
            WHEN month IN (3, 4, 5) THEN 'Spring'
            WHEN month IN (6, 7, 8) THEN 'Summer'
            WHEN month IN (9, 10, 11) THEN 'Fall'
        END as season
    FROM monthly_sales
)
SELECT 
    year,
    month,
    season,
    monthly_revenue,
    same_month_last_year,
    CASE 
        WHEN same_month_last_year IS NOT NULL 
        THEN ROUND(100.0 * (monthly_revenue - same_month_last_year) / same_month_last_year, 2)
        ELSE NULL 
    END as yoy_growth_percent,
    ROUND(rolling_12_month_avg, 2) as rolling_12_month_avg,
    ROUND(100.0 * monthly_revenue / rolling_12_month_avg, 2) as seasonal_index
FROM seasonal_analysis
ORDER BY year, month;

-- =====================================================
-- 6. PRODUCT AFFINITY ANALYSIS (Market Basket)
-- =====================================================

WITH order_products AS (
    SELECT 
        o.order_id,
        o.customer_id,
        oi.product_id,
        p.product_name,
        p.category
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '6 months'
),
product_pairs AS (
    SELECT 
        op1.product_id as product_a,
        op1.product_name as product_a_name,
        op2.product_id as product_b,
        op2.product_name as product_b_name,
        COUNT(DISTINCT op1.order_id) as co_occurrence_count
    FROM order_products op1
    JOIN order_products op2 ON op1.order_id = op2.order_id
    WHERE op1.product_id < op2.product_id  -- Avoid duplicates and self-pairs
    GROUP BY op1.product_id, op1.product_name, op2.product_id, op2.product_name
    HAVING COUNT(DISTINCT op1.order_id) >= 10  -- Minimum co-occurrence threshold
),
product_totals AS (
    SELECT 
        product_id,
        COUNT(DISTINCT order_id) as total_orders
    FROM order_products
    GROUP BY product_id
),
affinity_metrics AS (
    SELECT 
        pp.product_a,
        pp.product_a_name,
        pp.product_b,
        pp.product_b_name,
        pp.co_occurrence_count,
        pt1.total_orders as product_a_orders,
        pt2.total_orders as product_b_orders,
        ROUND(100.0 * pp.co_occurrence_count / pt1.total_orders, 2) as lift_a_to_b,
        ROUND(100.0 * pp.co_occurrence_count / pt2.total_orders, 2) as lift_b_to_a,
        ROUND(
            pp.co_occurrence_count::DECIMAL / 
            SQRT(pt1.total_orders * pt2.total_orders), 4
        ) as cosine_similarity
    FROM product_pairs pp
    JOIN product_totals pt1 ON pp.product_a = pt1.product_id
    JOIN product_totals pt2 ON pp.product_b = pt2.product_id
)
SELECT 
    product_a_name,
    product_b_name,
    co_occurrence_count,
    lift_a_to_b,
    lift_b_to_a,
    cosine_similarity,
    CASE 
        WHEN cosine_similarity >= 0.1 THEN 'Strong Affinity'
        WHEN cosine_similarity >= 0.05 THEN 'Moderate Affinity'
        ELSE 'Weak Affinity'
    END as affinity_strength
FROM affinity_metrics
ORDER BY cosine_similarity DESC
LIMIT 20;

-- =====================================================
-- 7. CHURN PREDICTION FEATURES
-- =====================================================

WITH customer_features AS (
    SELECT 
        customer_id,
        MAX(order_date) as last_order_date,
        MIN(order_date) as first_order_date,
        COUNT(*) as total_orders,
        SUM(amount) as total_spent,
        AVG(amount) as avg_order_value,
        STDDEV(amount) as order_value_stddev,
        EXTRACT(DAYS FROM (MAX(order_date) - MIN(order_date))) as customer_lifespan_days,
        CURRENT_DATE - MAX(order_date) as days_since_last_order,
        COUNT(DISTINCT EXTRACT(MONTH FROM order_date)) as active_months,
        COUNT(DISTINCT DATE_TRUNC('week', order_date)) as active_weeks
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
    GROUP BY customer_id
),
behavioral_features AS (
    SELECT 
        cf.*,
        CASE 
            WHEN cf.customer_lifespan_days > 0 
            THEN cf.total_orders::DECIMAL / (cf.customer_lifespan_days / 30.0)
            ELSE 0 
        END as orders_per_month,
        CASE 
            WHEN cf.total_orders > 1 
            THEN cf.customer_lifespan_days::DECIMAL / (cf.total_orders - 1)
            ELSE NULL 
        END as avg_days_between_orders,
        CASE 
            WHEN cf.customer_lifespan_days > 0 
            THEN cf.active_months::DECIMAL / (cf.customer_lifespan_days / 30.0)
            ELSE 0 
        END as engagement_ratio
    FROM customer_features cf
),
churn_indicators AS (
    SELECT 
        customer_id,
        days_since_last_order,
        total_orders,
        avg_order_value,
        orders_per_month,
        engagement_ratio,
        CASE 
            WHEN days_since_last_order > 180 THEN 'High Risk'
            WHEN days_since_last_order > 90 THEN 'Medium Risk'
            WHEN days_since_last_order > 30 THEN 'Low Risk'
            ELSE 'Active'
        END as churn_risk_category,
        CASE 
            WHEN days_since_last_order > 365 THEN 1 
            ELSE 0 
        END as is_churned,
        -- Churn score calculation (0-100)
        LEAST(100, 
            (days_since_last_order / 10.0) + 
            (CASE WHEN orders_per_month < 0.5 THEN 20 ELSE 0 END) +
            (CASE WHEN engagement_ratio < 0.3 THEN 15 ELSE 0 END) +
            (CASE WHEN avg_order_value < 50 THEN 10 ELSE 0 END)
        ) as churn_score
    FROM behavioral_features
)
SELECT 
    churn_risk_category,
    COUNT(*) as customer_count,
    ROUND(AVG(churn_score), 2) as avg_churn_score,
    ROUND(AVG(days_since_last_order), 1) as avg_days_since_last_order,
    ROUND(AVG(total_orders), 1) as avg_total_orders,
    ROUND(AVG(avg_order_value), 2) as avg_order_value,
    SUM(is_churned) as churned_customers,
    ROUND(100.0 * SUM(is_churned) / COUNT(*), 2) as actual_churn_rate
FROM churn_indicators
GROUP BY churn_risk_category
ORDER BY avg_churn_score DESC;

-- =====================================================
-- 8. TIME SERIES ANOMALY DETECTION
-- =====================================================

WITH daily_metrics AS (
    SELECT 
        DATE(order_date) as date,
        COUNT(*) as daily_orders,
        SUM(amount) as daily_revenue,
        COUNT(DISTINCT customer_id) as daily_customers
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '1 year'
    GROUP BY DATE(order_date)
),
statistical_bounds AS (
    SELECT 
        date,
        daily_orders,
        daily_revenue,
        daily_customers,
        AVG(daily_orders) OVER (
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as rolling_avg_orders,
        STDDEV(daily_orders) OVER (
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as rolling_stddev_orders,
        AVG(daily_revenue) OVER (
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as rolling_avg_revenue,
        STDDEV(daily_revenue) OVER (
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as rolling_stddev_revenue
    FROM daily_metrics
),
anomaly_detection AS (
    SELECT 
        date,
        daily_orders,
        daily_revenue,
        rolling_avg_orders,
        rolling_stddev_orders,
        rolling_avg_revenue,
        rolling_stddev_revenue,
        ABS(daily_orders - rolling_avg_orders) / NULLIF(rolling_stddev_orders, 0) as orders_z_score,
        ABS(daily_revenue - rolling_avg_revenue) / NULLIF(rolling_stddev_revenue, 0) as revenue_z_score,
        CASE 
            WHEN ABS(daily_orders - rolling_avg_orders) / NULLIF(rolling_stddev_orders, 0) > 2 THEN 'Order Anomaly'
            WHEN ABS(daily_revenue - rolling_avg_revenue) / NULLIF(rolling_stddev_revenue, 0) > 2 THEN 'Revenue Anomaly'
            ELSE 'Normal'
        END as anomaly_type
    FROM statistical_bounds
    WHERE rolling_stddev_orders IS NOT NULL
)
SELECT 
    date,
    daily_orders,
    ROUND(rolling_avg_orders, 1) as expected_orders,
    daily_revenue,
    ROUND(rolling_avg_revenue, 2) as expected_revenue,
    ROUND(orders_z_score, 2) as orders_z_score,
    ROUND(revenue_z_score, 2) as revenue_z_score,
    anomaly_type
FROM anomaly_detection
WHERE anomaly_type != 'Normal'
ORDER BY date DESC;

-- =====================================================
-- 9. ADVANCED SEGMENTATION WITH CLUSTERING FEATURES
-- =====================================================

WITH customer_behavior_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as total_orders,
        SUM(amount) as total_spent,
        AVG(amount) as avg_order_value,
        MAX(order_date) as last_order_date,
        MIN(order_date) as first_order_date,
        CURRENT_DATE - MAX(order_date) as recency_days,
        EXTRACT(DAYS FROM (MAX(order_date) - MIN(order_date))) as customer_lifespan_days,
        COUNT(DISTINCT DATE_TRUNC('month', order_date)) as active_months,
        STDDEV(amount) as order_value_variance
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
    GROUP BY customer_id
),
normalized_features AS (
    SELECT 
        customer_id,
        total_orders,
        total_spent,
        avg_order_value,
        recency_days,
        active_months,
        -- Normalize features using min-max scaling
        (total_orders - MIN(total_orders) OVER()) / 
        NULLIF(MAX(total_orders) OVER() - MIN(total_orders) OVER(), 0) as norm_frequency,
        
        (total_spent - MIN(total_spent) OVER()) / 
        NULLIF(MAX(total_spent) OVER() - MIN(total_spent) OVER(), 0) as norm_monetary,
        
        1 - (recency_days - MIN(recency_days) OVER()) / 
        NULLIF(MAX(recency_days) OVER() - MIN(recency_days) OVER(), 0) as norm_recency,
        
        (active_months - MIN(active_months) OVER()) / 
        NULLIF(MAX(active_months) OVER() - MIN(active_months) OVER(), 0) as norm_engagement
    FROM customer_behavior_metrics
),
customer_segments AS (
    SELECT 
        customer_id,
        norm_frequency,
        norm_monetary,
        norm_recency,
        norm_engagement,
        -- Simple rule-based segmentation
        CASE 
            WHEN norm_frequency >= 0.8 AND norm_monetary >= 0.8 AND norm_recency >= 0.8 THEN 'VIP Champions'
            WHEN norm_frequency >= 0.6 AND norm_monetary >= 0.6 AND norm_recency >= 0.6 THEN 'Loyal Customers'
            WHEN norm_recency >= 0.7 AND norm_frequency <= 0.3 THEN 'New Customers'
            WHEN norm_recency <= 0.3 AND norm_frequency >= 0.5 THEN 'At Risk'
            WHEN norm_recency <= 0.2 THEN 'Lost Customers'
            WHEN norm_monetary >= 0.7 AND norm_frequency <= 0.4 THEN 'Big Spenders'
            ELSE 'Regular Customers'
        END as segment
    FROM normalized_features
)
SELECT 
    segment,
    COUNT(*) as customer_count,
    ROUND(AVG(norm_frequency), 3) as avg_frequency_score,
    ROUND(AVG(norm_monetary), 3) as avg_monetary_score,
    ROUND(AVG(norm_recency), 3) as avg_recency_score,
    ROUND(AVG(norm_engagement), 3) as avg_engagement_score,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as segment_percentage
FROM customer_segments
GROUP BY segment
ORDER BY customer_count DESC;

-- =====================================================
-- 10. REVENUE ATTRIBUTION ANALYSIS
-- =====================================================

WITH customer_touchpoints AS (
    SELECT 
        customer_id,
        order_id,
        order_date,
        amount,
        marketing_channel,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_sequence,
        LAG(marketing_channel) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_channel,
        LEAD(marketing_channel) OVER (PARTITION BY customer_id ORDER BY order_date) as next_channel
    FROM orders o
    LEFT JOIN marketing_attribution ma ON o.customer_id = ma.customer_id 
        AND ma.attribution_date <= o.order_date
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '1 year'
),
attribution_models AS (
    SELECT 
        customer_id,
        order_id,
        amount,
        marketing_channel,
        order_sequence,
        -- First-touch attribution
        FIRST_VALUE(marketing_channel) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date 
            ROWS UNBOUNDED PRECEDING
        ) as first_touch_channel,
        -- Last-touch attribution
        LAST_VALUE(marketing_channel) OVER (
            PARTITION BY customer_id 
            ORDER BY order_date 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as last_touch_channel,
        -- Linear attribution weight
        1.0 / COUNT(*) OVER (PARTITION BY customer_id) as linear_weight
    FROM customer_touchpoints
)
SELECT 
    'First Touch' as attribution_model,
    first_touch_channel as channel,
    COUNT(DISTINCT customer_id) as customers,
    COUNT(*) as orders,
    SUM(amount) as total_revenue,
    ROUND(AVG(amount), 2) as avg_order_value
FROM attribution_models
WHERE first_touch_channel IS NOT NULL
GROUP BY first_touch_channel

UNION ALL

SELECT 
    'Last Touch' as attribution_model,
    last_touch_channel as channel,
    COUNT(DISTINCT customer_id) as customers,
    COUNT(*) as orders,
    SUM(amount) as total_revenue,
    ROUND(AVG(amount), 2) as avg_order_value
FROM attribution_models
WHERE last_touch_channel IS NOT NULL
GROUP BY last_touch_channel

UNION ALL

SELECT 
    'Linear' as attribution_model,
    marketing_channel as channel,
    COUNT(DISTINCT customer_id) as customers,
    COUNT(*) as orders,
    ROUND(SUM(amount * linear_weight), 2) as total_revenue,
    ROUND(AVG(amount), 2) as avg_order_value
FROM attribution_models
WHERE marketing_channel IS NOT NULL
GROUP BY marketing_channel

ORDER BY attribution_model, total_revenue DESC;