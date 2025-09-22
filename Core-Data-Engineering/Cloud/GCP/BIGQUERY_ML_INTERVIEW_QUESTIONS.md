# Google BigQuery Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)

---

## Basic Level Questions (1-50)

### 22. How do you create and manage datasets in BigQuery?

**Answer:** Datasets are containers for tables, views, and other resources in BigQuery.

```sql
-- Create dataset
CREATE SCHEMA `project.sales_data`
OPTIONS(
  description="Sales data warehouse",
  location="US",
  default_table_expiration_days=90
);

-- Set dataset properties
ALTER SCHEMA `project.sales_data`
SET OPTIONS(
  description="Updated sales data warehouse",
  default_table_expiration_days=180
);

-- Grant access to dataset
GRANT `roles/bigquery.dataViewer`
ON SCHEMA `project.sales_data`
TO "user:analyst@company.com";
```

**Output:**
```
Dataset created: project.sales_data
Location: US
Default expiration: 90 days
Access granted to analyst@company.com
```

### 23. What are BigQuery's data types and how do you use them?

**Answer:** BigQuery supports various data types including complex nested structures.

```sql
-- Create table with different data types
CREATE TABLE `project.dataset.customer_data` (
  customer_id INT64 NOT NULL,
  name STRING(100),
  email STRING,
  birth_date DATE,
  registration_time TIMESTAMP,
  is_active BOOL,
  account_balance NUMERIC(10,2),
  preferences ARRAY<STRING>,
  address STRUCT<
    street STRING,
    city STRING,
    zipcode STRING,
    coordinates STRUCT<lat FLOAT64, lng FLOAT64>
  >,
  metadata JSON
);

-- Insert sample data
INSERT INTO `project.dataset.customer_data` VALUES
(
  1,
  'John Doe',
  'john@example.com',
  '1985-06-15',
  '2024-01-15 10:30:00',
  true,
  1250.75,
  ['email', 'sms', 'push'],
  STRUCT('123 Main St', 'New York', '10001', STRUCT(40.7128, -74.0060)),
  JSON '{"source": "web", "campaign": "summer2024"}'
);

-- Query complex data types
SELECT 
  customer_id,
  name,
  preferences,
  address.city,
  address.coordinates.lat,
  JSON_EXTRACT_SCALAR(metadata, '$.source') as source
FROM `project.dataset.customer_data`;
```

**Output:**
```
+-------------+----------+-------------------------+----------+--------+--------+
| customer_id | name     | preferences             | city     | lat    | source |
+-------------+----------+-------------------------+----------+--------+--------+
| 1           | John Doe | [email, sms, push]      | New York | 40.7128| web    |
+-------------+----------+-------------------------+----------+--------+--------+
```

### 24. How do you work with arrays and structs in BigQuery?

**Answer:** BigQuery provides powerful functions for working with nested and repeated data.

```sql
-- Working with arrays
WITH sample_data AS (
  SELECT 1 as id, ['apple', 'banana', 'cherry'] as fruits
  UNION ALL
  SELECT 2 as id, ['orange', 'grape'] as fruits
  UNION ALL
  SELECT 3 as id, ['kiwi', 'mango', 'pineapple', 'strawberry'] as fruits
)
SELECT 
  id,
  fruits,
  ARRAY_LENGTH(fruits) as fruit_count,
  fruits[OFFSET(0)] as first_fruit,
  fruits[SAFE_OFFSET(10)] as safe_access,  -- Returns NULL if index doesn't exist
  'apple' IN UNNEST(fruits) as has_apple
FROM sample_data;

-- Unnest arrays to rows
SELECT 
  id,
  fruit,
  ARRAY_LENGTH(fruits) as total_fruits
FROM sample_data,
UNNEST(fruits) as fruit;

-- Array aggregation
SELECT 
  ARRAY_AGG(fruit ORDER BY fruit) as all_fruits,
  ARRAY_AGG(DISTINCT fruit ORDER BY fruit) as unique_fruits,
  STRING_AGG(fruit, ', ' ORDER BY fruit) as fruits_string
FROM sample_data,
UNNEST(fruits) as fruit;
```

**Output:**
```
+----+-------------------------+-------------+-------------+
| id | fruits                  | fruit_count | first_fruit |
+----+-------------------------+-------------+-------------+
| 1  | [apple, banana, cherry] | 3           | apple       |
| 2  | [orange, grape]         | 2           | orange      |
| 3  | [kiwi, mango, ...]      | 4           | kiwi        |
+----+-------------------------+-------------+-------------+
```

### 25. How do you implement window functions in BigQuery?

**Answer:** Window functions perform calculations across related rows without grouping.

```sql
-- Sample sales data
WITH sales_data AS (
  SELECT DATE '2024-01-01' as sale_date, 'Electronics' as category, 'Alice' as salesperson, 1000 as amount
  UNION ALL SELECT DATE '2024-01-01', 'Electronics', 'Bob', 1500
  UNION ALL SELECT DATE '2024-01-01', 'Clothing', 'Charlie', 800
  UNION ALL SELECT DATE '2024-01-02', 'Electronics', 'Alice', 1200
  UNION ALL SELECT DATE '2024-01-02', 'Electronics', 'Bob', 900
  UNION ALL SELECT DATE '2024-01-02', 'Clothing', 'Charlie', 1100
)
SELECT 
  sale_date,
  category,
  salesperson,
  amount,
  
  -- Running totals
  SUM(amount) OVER (ORDER BY sale_date, salesperson) as running_total,
  
  -- Ranking functions
  ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) as row_num,
  RANK() OVER (PARTITION BY category ORDER BY amount DESC) as rank_val,
  DENSE_RANK() OVER (PARTITION BY category ORDER BY amount DESC) as dense_rank_val,
  
  -- Lead and lag
  LAG(amount, 1) OVER (PARTITION BY salesperson ORDER BY sale_date) as prev_amount,
  LEAD(amount, 1) OVER (PARTITION BY salesperson ORDER BY sale_date) as next_amount,
  
  -- Moving averages
  AVG(amount) OVER (PARTITION BY salesperson ORDER BY sale_date 
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as moving_avg_3
FROM sales_data
ORDER BY sale_date, category, salesperson;
```

### 26. How do you handle JSON data in BigQuery?

**Answer:** BigQuery provides comprehensive JSON functions for parsing and manipulating JSON data.

```sql
-- Sample JSON data
WITH json_data AS (
  SELECT 1 as id, '''
  {
    "customer": {
      "name": "John Doe",
      "email": "john@example.com",
      "age": 30,
      "preferences": ["email", "sms"]
    },
    "orders": [
      {"id": 101, "product": "Laptop", "price": 999.99, "date": "2024-01-15"},
      {"id": 102, "product": "Mouse", "price": 29.99, "date": "2024-01-16"}
    ],
    "metadata": {
      "source": "web",
      "campaign": "summer2024",
      "score": 85.5
    }
  }
  ''' as json_string
)
SELECT 
  id,
  
  -- Extract scalar values
  JSON_EXTRACT_SCALAR(json_string, '$.customer.name') as customer_name,
  JSON_EXTRACT_SCALAR(json_string, '$.customer.email') as customer_email,
  CAST(JSON_EXTRACT_SCALAR(json_string, '$.customer.age') AS INT64) as customer_age,
  
  -- Extract arrays
  JSON_EXTRACT_ARRAY(json_string, '$.customer.preferences') as preferences,
  JSON_EXTRACT_ARRAY(json_string, '$.orders') as orders,
  
  -- Extract objects
  JSON_EXTRACT(json_string, '$.metadata') as metadata,
  
  -- Extract nested values
  CAST(JSON_EXTRACT_SCALAR(json_string, '$.metadata.score') AS FLOAT64) as score
FROM json_data;
```

### 27. How do you implement BigQuery ML for machine learning?

**Answer:** BigQuery ML enables creating and executing machine learning models using SQL.

```sql
-- Create linear regression model
CREATE MODEL `project.dataset.sales_forecast_model`
OPTIONS(
  model_type='linear_reg',
  input_label_cols=['sales_amount']
) AS
SELECT
  advertising_spend,
  season,
  day_of_week,
  temperature,
  sales_amount
FROM `project.dataset.historical_sales`
WHERE date BETWEEN '2023-01-01' AND '2023-12-31';

-- Evaluate model performance
SELECT *
FROM ML.EVALUATE(MODEL `project.dataset.sales_forecast_model`,
  (SELECT advertising_spend, season, day_of_week, temperature, sales_amount
   FROM `project.dataset.test_sales_data`));

-- Make predictions
SELECT 
  *,
  predicted_sales_amount,
  predicted_sales_amount_interval_lower_bound,
  predicted_sales_amount_interval_upper_bound
FROM ML.PREDICT(MODEL `project.dataset.sales_forecast_model`,
  (SELECT advertising_spend, season, day_of_week, temperature
   FROM `project.dataset.future_scenarios`));

-- Feature importance
SELECT *
FROM ML.FEATURE_IMPORTANCE(MODEL `project.dataset.sales_forecast_model`);

-- Model information
SELECT *
FROM ML.TRAINING_INFO(MODEL `project.dataset.sales_forecast_model`);
```

### 28. How do you implement clustering with BigQuery ML?

**Answer:** K-means clustering for customer segmentation and pattern discovery.

```sql
-- Create K-means clustering model
CREATE MODEL `project.dataset.customer_segmentation_model`
OPTIONS(
  model_type='kmeans',
  num_clusters=4,
  standardize_features=true
) AS
SELECT
  total_spent,
  order_frequency,
  avg_order_value,
  days_since_last_order,
  product_categories_count
FROM `project.dataset.customer_features`
WHERE total_spent > 0;

-- Get cluster assignments
SELECT 
  customer_id,
  total_spent,
  order_frequency,
  CENTROID_ID as cluster_id
FROM ML.PREDICT(MODEL `project.dataset.customer_segmentation_model`,
  (SELECT customer_id, total_spent, order_frequency, avg_order_value,
          days_since_last_order, product_categories_count
   FROM `project.dataset.customer_features`));

-- Analyze cluster centroids
SELECT *
FROM ML.CENTROIDS(MODEL `project.dataset.customer_segmentation_model`);

-- Cluster evaluation metrics
SELECT *
FROM ML.EVALUATE(MODEL `project.dataset.customer_segmentation_model`);
```

### 29. How do you implement time series forecasting in BigQuery ML?

**Answer:** ARIMA models for time series prediction and trend analysis.

```sql
-- Create ARIMA time series model
CREATE MODEL `project.dataset.sales_timeseries_model`
OPTIONS(
  model_type='ARIMA_PLUS',
  time_series_timestamp_col='date',
  time_series_data_col='daily_sales',
  time_series_id_col='store_id',
  auto_arima=true,
  data_frequency='DAILY',
  holiday_region='US'
) AS
SELECT
  date,
  store_id,
  daily_sales
FROM `project.dataset.daily_store_sales`
WHERE date BETWEEN '2022-01-01' AND '2023-12-31';

-- Generate forecasts
SELECT *
FROM ML.FORECAST(MODEL `project.dataset.sales_timeseries_model`,
  STRUCT(30 AS horizon, 0.8 AS confidence_level));

-- Detect anomalies
SELECT *
FROM ML.DETECT_ANOMALIES(MODEL `project.dataset.sales_timeseries_model`,
  STRUCT(0.95 AS anomaly_prob_threshold));

-- Explain forecast
SELECT *
FROM ML.EXPLAIN_FORECAST(MODEL `project.dataset.sales_timeseries_model`,
  STRUCT(30 AS horizon, 0.8 AS confidence_level));
```

### 30. How do you implement classification models in BigQuery ML?

**Answer:** Logistic regression and other classification algorithms for prediction tasks.

```sql
-- Create logistic regression model for churn prediction
CREATE MODEL `project.dataset.customer_churn_model`
OPTIONS(
  model_type='logistic_reg',
  input_label_cols=['will_churn'],
  auto_class_weights=true
) AS
SELECT
  customer_age,
  total_spent,
  order_count,
  days_since_last_order,
  support_tickets,
  satisfaction_score,
  will_churn
FROM `project.dataset.customer_churn_training`
WHERE customer_age IS NOT NULL;

-- Evaluate classification model
SELECT *
FROM ML.EVALUATE(MODEL `project.dataset.customer_churn_model`,
  (SELECT customer_age, total_spent, order_count, days_since_last_order,
          support_tickets, satisfaction_score, will_churn
   FROM `project.dataset.customer_churn_test`));

-- Get predictions with probabilities
SELECT 
  customer_id,
  predicted_will_churn,
  predicted_will_churn_probs[OFFSET(1)].prob as churn_probability
FROM ML.PREDICT(MODEL `project.dataset.customer_churn_model`,
  (SELECT customer_id, customer_age, total_spent, order_count,
          days_since_last_order, support_tickets, satisfaction_score
   FROM `project.dataset.active_customers`));

-- Feature importance for interpretability
SELECT *
FROM ML.FEATURE_IMPORTANCE(MODEL `project.dataset.customer_churn_model`)
ORDER BY importance_weight DESC;
```

### 31. How do you implement deep neural networks in BigQuery ML?

**Answer:** DNN models for complex pattern recognition and prediction tasks.

```sql
-- Create deep neural network model
CREATE MODEL `project.dataset.product_recommendation_dnn`
OPTIONS(
  model_type='dnn_regressor',
  hidden_units=[128, 64, 32],
  dropout=0.2,
  batch_size=32,
  max_iterations=100,
  learn_rate=0.001,
  activation_fn='relu',
  optimizer='adam'
) AS
SELECT
  user_age,
  user_gender,
  user_location,
  product_category,
  price_range,
  season,
  day_of_week,
  rating as label
FROM `project.dataset.user_product_interactions`
WHERE rating IS NOT NULL;

-- Hyperparameter tuning
CREATE MODEL `project.dataset.tuned_dnn_model`
OPTIONS(
  model_type='dnn_regressor',
  num_trials=20,
  max_parallel_trials=5,
  hparam_tuning_objectives=['mean_squared_error'],
  hidden_units=hparam_range([64, 256]),
  dropout=hparam_range(0.1, 0.5),
  learn_rate=hparam_candidates([0.001, 0.01, 0.1])
) AS
SELECT * FROM `project.dataset.training_data`;

-- Model evaluation and comparison
SELECT 
  'DNN Model' as model_name,
  mean_squared_error,
  mean_absolute_error,
  r2_score
FROM ML.EVALUATE(MODEL `project.dataset.product_recommendation_dnn`,
  (SELECT * FROM `project.dataset.test_data`))
UNION ALL
SELECT 
  'Tuned DNN Model' as model_name,
  mean_squared_error,
  mean_absolute_error,
  r2_score
FROM ML.EVALUATE(MODEL `project.dataset.tuned_dnn_model`,
  (SELECT * FROM `project.dataset.test_data`));
```

### 32. How do you implement AutoML in BigQuery ML?

**Answer:** AutoML Tables for automated machine learning model development.

```sql
-- Create AutoML Tables model
CREATE MODEL `project.dataset.automl_sales_model`
OPTIONS(
  model_type='automl_regressor',
  budget_hours=2.0,
  optimization_objective='minimize_rmse'
) AS
SELECT
  * EXCEPT(sales_amount),
  sales_amount as label
FROM `project.dataset.sales_training_data`;

-- AutoML classification model
CREATE MODEL `project.dataset.automl_classification_model`
OPTIONS(
  model_type='automl_classifier',
  budget_hours=1.0,
  optimization_objective='maximize_au_prc'
) AS
SELECT
  * EXCEPT(category),
  category as label
FROM `project.dataset.classification_training_data`;

-- Get AutoML model information
SELECT *
FROM ML.TRAINING_INFO(MODEL `project.dataset.automl_sales_model`);

-- Feature importance from AutoML
SELECT *
FROM ML.FEATURE_IMPORTANCE(MODEL `project.dataset.automl_sales_model`)
ORDER BY importance_weight DESC;

-- Global explanations
SELECT *
FROM ML.GLOBAL_EXPLAIN(MODEL `project.dataset.automl_sales_model`);
```

### 33. How do you implement recommendation systems in BigQuery ML?

**Answer:** Matrix factorization for collaborative filtering and recommendations.

```sql
-- Create matrix factorization model for recommendations
CREATE MODEL `project.dataset.movie_recommendation_model`
OPTIONS(
  model_type='matrix_factorization',
  user_col='user_id',
  item_col='movie_id',
  rating_col='rating',
  l2_reg=0.1,
  num_factors=50,
  feedback_type='explicit'
) AS
SELECT
  user_id,
  movie_id,
  rating
FROM `project.dataset.movie_ratings`
WHERE rating IS NOT NULL;

-- Generate recommendations for users
SELECT *
FROM ML.RECOMMEND(MODEL `project.dataset.movie_recommendation_model`,
  STRUCT(5 AS max_recommendations))
WHERE user_id IN (123, 456, 789);

-- Get item-to-item recommendations
SELECT *
FROM ML.RECOMMEND(MODEL `project.dataset.movie_recommendation_model`,
  STRUCT(5 AS max_recommendations, 'item' AS recommendation_type))
WHERE movie_id IN (101, 102, 103);

-- Evaluate recommendation model
SELECT *
FROM ML.EVALUATE(MODEL `project.dataset.movie_recommendation_model`,
  (SELECT user_id, movie_id, rating
   FROM `project.dataset.movie_ratings_test`));
```

### 34. How do you implement anomaly detection in BigQuery ML?

**Answer:** Autoencoder and statistical methods for detecting outliers and anomalies.

```sql
-- Create autoencoder for anomaly detection
CREATE MODEL `project.dataset.network_anomaly_detector`
OPTIONS(
  model_type='autoencoder',
  activation_fn='relu',
  batch_size=32,
  dropout=0.2,
  hidden_units=[64, 32, 16, 32, 64],
  l2_reg=0.001,
  learn_rate=0.001,
  max_iterations=100
) AS
SELECT
  bytes_sent,
  bytes_received,
  packets_sent,
  packets_received,
  connection_duration,
  protocol_type,
  service_type
FROM `project.dataset.network_traffic`
WHERE is_normal = true;  -- Train only on normal data

-- Detect anomalies
SELECT 
  *,
  ML.RECONSTRUCT_ERROR(MODEL `project.dataset.network_anomaly_detector`, 
    STRUCT(bytes_sent, bytes_received, packets_sent, packets_received,
           connection_duration, protocol_type, service_type)) as reconstruction_error
FROM `project.dataset.network_traffic_new`
ORDER BY reconstruction_error DESC;

-- Statistical anomaly detection using Z-score
WITH stats AS (
  SELECT 
    AVG(response_time) as mean_response_time,
    STDDEV(response_time) as stddev_response_time
  FROM `project.dataset.api_logs`
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
)
SELECT 
  timestamp,
  endpoint,
  response_time,
  ABS(response_time - mean_response_time) / stddev_response_time as z_score,
  CASE 
    WHEN ABS(response_time - mean_response_time) / stddev_response_time > 3 
    THEN 'ANOMALY'
    ELSE 'NORMAL'
  END as status
FROM `project.dataset.api_logs`, stats
WHERE date = CURRENT_DATE()
ORDER BY z_score DESC;
```

### 35. How do you implement model explainability in BigQuery ML?

**Answer:** Various explainability techniques to understand model predictions.

```sql
-- Global feature importance
SELECT *
FROM ML.FEATURE_IMPORTANCE(MODEL `project.dataset.loan_approval_model`)
ORDER BY importance_weight DESC;

-- Local explanations for specific predictions
SELECT *
FROM ML.EXPLAIN_PREDICT(MODEL `project.dataset.loan_approval_model`,
  (SELECT * FROM `project.dataset.loan_applications` 
   WHERE application_id IN ('APP001', 'APP002', 'APP003')),
  STRUCT(3 AS top_k_features));

-- Global explanations
SELECT *
FROM ML.GLOBAL_EXPLAIN(MODEL `project.dataset.loan_approval_model`,
  STRUCT('predicted_approval_probability' AS class_level_explain));

-- Shapley values for feature attribution
SELECT 
  application_id,
  predicted_approval_probability,
  shapley_values
FROM ML.EXPLAIN_PREDICT(MODEL `project.dataset.loan_approval_model`,
  (SELECT * FROM `project.dataset.loan_applications_sample`),
  STRUCT(true AS use_shapley_values));

-- Feature statistics and distributions
SELECT 
  feature_name,
  min_value,
  max_value,
  mean_value,
  stddev_value,
  null_count,
  unique_count
FROM ML.FEATURE_INFO(MODEL `project.dataset.loan_approval_model`);
```

### 36. How do you implement model monitoring and drift detection?

**Answer:** Monitor model performance and detect data/concept drift over time.

```sql
-- Create model performance monitoring
WITH model_predictions AS (
  SELECT 
    prediction_date,
    actual_value,
    predicted_value,
    ABS(actual_value - predicted_value) as absolute_error,
    POWER(actual_value - predicted_value, 2) as squared_error
  FROM ML.PREDICT(MODEL `project.dataset.sales_model`,
    (SELECT * FROM `project.dataset.recent_sales_data`)) p
  JOIN `project.dataset.actual_sales` a
    ON p.date = a.date AND p.store_id = a.store_id
),
performance_metrics AS (
  SELECT 
    prediction_date,
    COUNT(*) as prediction_count,
    AVG(absolute_error) as mae,
    SQRT(AVG(squared_error)) as rmse,
    CORR(actual_value, predicted_value) as correlation
  FROM model_predictions
  GROUP BY prediction_date
)
SELECT 
  prediction_date,
  mae,
  rmse,
  correlation,
  -- Detect performance degradation
  CASE 
    WHEN mae > LAG(mae, 7) OVER (ORDER BY prediction_date) * 1.2 
    THEN 'PERFORMANCE_DEGRADED'
    WHEN correlation < 0.7 
    THEN 'LOW_CORRELATION'
    ELSE 'NORMAL'
  END as alert_status
FROM performance_metrics
ORDER BY prediction_date DESC;

-- Data drift detection using statistical tests
WITH feature_stats_baseline AS (
  SELECT 
    'baseline' as period,
    AVG(customer_age) as avg_age,
    STDDEV(customer_age) as stddev_age,
    AVG(income) as avg_income,
    STDDEV(income) as stddev_income
  FROM `project.dataset.training_data`
),
feature_stats_current AS (
  SELECT 
    'current' as period,
    AVG(customer_age) as avg_age,
    STDDEV(customer_age) as stddev_age,
    AVG(income) as avg_income,
    STDDEV(income) as stddev_income
  FROM `project.dataset.current_data`
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
)
SELECT 
  'customer_age' as feature,
  ABS(c.avg_age - b.avg_age) / b.stddev_age as drift_score,
  CASE 
    WHEN ABS(c.avg_age - b.avg_age) / b.stddev_age > 2 
    THEN 'SIGNIFICANT_DRIFT'
    ELSE 'NO_DRIFT'
  END as drift_status
FROM feature_stats_baseline b, feature_stats_current c
UNION ALL
SELECT 
  'income' as feature,
  ABS(c.avg_income - b.avg_income) / b.stddev_income as drift_score,
  CASE 
    WHEN ABS(c.avg_income - b.avg_income) / b.stddev_income > 2 
    THEN 'SIGNIFICANT_DRIFT'
    ELSE 'NO_DRIFT'
  END as drift_status
FROM feature_stats_baseline b, feature_stats_current c;
```

### 37. How do you implement A/B testing analysis in BigQuery?

**Answer:** Statistical analysis for A/B testing and experimentation.

```sql
-- A/B test analysis with statistical significance
WITH experiment_data AS (
  SELECT 
    user_id,
    variant,
    converted,
    revenue,
    session_duration
  FROM `project.dataset.ab_test_results`
  WHERE experiment_name = 'checkout_optimization'
    AND date BETWEEN '2024-01-01' AND '2024-01-31'
),
variant_stats AS (
  SELECT 
    variant,
    COUNT(*) as total_users,
    SUM(converted) as conversions,
    AVG(converted) as conversion_rate,
    STDDEV(converted) as conversion_stddev,
    AVG(revenue) as avg_revenue,
    STDDEV(revenue) as revenue_stddev,
    AVG(session_duration) as avg_session_duration
  FROM experiment_data
  GROUP BY variant
),
statistical_test AS (
  SELECT 
    a.variant as variant_a,
    b.variant as variant_b,
    a.conversion_rate as conversion_rate_a,
    b.conversion_rate as conversion_rate_b,
    (b.conversion_rate - a.conversion_rate) as lift,
    (b.conversion_rate - a.conversion_rate) / a.conversion_rate * 100 as lift_percent,
    
    -- Calculate standard error for difference
    SQRT(
      (a.conversion_rate * (1 - a.conversion_rate) / a.total_users) +
      (b.conversion_rate * (1 - b.conversion_rate) / b.total_users)
    ) as standard_error,
    
    -- Z-score for significance test
    (b.conversion_rate - a.conversion_rate) / SQRT(
      (a.conversion_rate * (1 - a.conversion_rate) / a.total_users) +
      (b.conversion_rate * (1 - b.conversion_rate) / b.total_users)
    ) as z_score
    
  FROM variant_stats a
  CROSS JOIN variant_stats b
  WHERE a.variant = 'control' AND b.variant = 'treatment'
)
SELECT 
  *,
  -- Two-tailed p-value approximation
  2 * (1 - APPROX_QUANTILES(ABS(z_score), 1000)[OFFSET(975)]) as p_value,
  CASE 
    WHEN ABS(z_score) > 1.96 THEN 'SIGNIFICANT'
    ELSE 'NOT_SIGNIFICANT'
  END as significance_95,
  CASE 
    WHEN ABS(z_score) > 2.58 THEN 'SIGNIFICANT'
    ELSE 'NOT_SIGNIFICANT'
  END as significance_99
FROM statistical_test;

-- Bayesian A/B test analysis
WITH bayesian_analysis AS (
  SELECT 
    variant,
    SUM(converted) as successes,
    COUNT(*) - SUM(converted) as failures,
    -- Beta distribution parameters (assuming uniform prior)
    SUM(converted) + 1 as alpha,
    COUNT(*) - SUM(converted) + 1 as beta
  FROM experiment_data
  GROUP BY variant
)
SELECT 
  variant,
  successes,
  failures,
  successes / (successes + failures) as observed_rate,
  alpha / (alpha + beta) as posterior_mean,
  SQRT(alpha * beta / (POWER(alpha + beta, 2) * (alpha + beta + 1))) as posterior_stddev
FROM bayesian_analysis;
```

### 38. How do you implement cohort analysis in BigQuery?

**Answer:** Analyze user behavior and retention over time using cohort analysis.

```sql
-- Customer cohort analysis
WITH user_cohorts AS (
  SELECT 
    user_id,
    DATE_TRUNC(MIN(order_date), MONTH) as cohort_month,
    MIN(order_date) as first_order_date
  FROM `project.dataset.orders`
  GROUP BY user_id
),
user_activities AS (
  SELECT 
    o.user_id,
    uc.cohort_month,
    DATE_TRUNC(o.order_date, MONTH) as activity_month,
    DATE_DIFF(DATE_TRUNC(o.order_date, MONTH), uc.cohort_month, MONTH) as period_number,
    SUM(o.order_value) as monthly_revenue
  FROM `project.dataset.orders` o
  JOIN user_cohorts uc ON o.user_id = uc.user_id
  GROUP BY 1, 2, 3, 4
),
cohort_table AS (
  SELECT 
    cohort_month,
    period_number,
    COUNT(DISTINCT user_id) as active_users,
    SUM(monthly_revenue) as cohort_revenue
  FROM user_activities
  GROUP BY cohort_month, period_number
),
cohort_sizes AS (
  SELECT 
    cohort_month,
    COUNT(DISTINCT user_id) as cohort_size
  FROM user_cohorts
  GROUP BY cohort_month
)
SELECT 
  ct.cohort_month,
  cs.cohort_size,
  ct.period_number,
  ct.active_users,
  ct.active_users / cs.cohort_size as retention_rate,
  ct.cohort_revenue,
  ct.cohort_revenue / ct.active_users as revenue_per_user
FROM cohort_table ct
JOIN cohort_sizes cs ON ct.cohort_month = cs.cohort_month
ORDER BY ct.cohort_month, ct.period_number;

-- Revenue cohort analysis
WITH revenue_cohorts AS (
  SELECT 
    cohort_month,
    period_number,
    SUM(cohort_revenue) as total_revenue,
    AVG(cohort_revenue / active_users) as avg_revenue_per_user,
    -- Cumulative revenue per cohort
    SUM(SUM(cohort_revenue)) OVER (
      PARTITION BY cohort_month 
      ORDER BY period_number 
      ROWS UNBOUNDED PRECEDING
    ) as cumulative_revenue
  FROM cohort_table
  WHERE active_users > 0
  GROUP BY cohort_month, period_number
)
SELECT 
  cohort_month,
  period_number,
  total_revenue,
  cumulative_revenue,
  avg_revenue_per_user,
  -- Calculate LTV (Customer Lifetime Value) projection
  cumulative_revenue / FIRST_VALUE(total_revenue) OVER (
    PARTITION BY cohort_month 
    ORDER BY period_number
  ) as ltv_multiplier
FROM revenue_cohorts
ORDER BY cohort_month, period_number;
```

### 39. How do you implement funnel analysis in BigQuery?

**Answer:** Analyze user conversion funnels and identify drop-off points.

```sql
-- E-commerce funnel analysis
WITH funnel_events AS (
  SELECT 
    user_id,
    session_id,
    event_timestamp,
    event_name,
    -- Define funnel steps
    CASE event_name
      WHEN 'page_view' THEN 1
      WHEN 'product_view' THEN 2
      WHEN 'add_to_cart' THEN 3
      WHEN 'begin_checkout' THEN 4
      WHEN 'purchase' THEN 5
      ELSE 0
    END as funnel_step
  FROM `project.dataset.user_events`
  WHERE event_name IN ('page_view', 'product_view', 'add_to_cart', 'begin_checkout', 'purchase')
    AND DATE(event_timestamp) BETWEEN '2024-01-01' AND '2024-01-31'
),
user_funnel_progress AS (
  SELECT 
    user_id,
    session_id,
    MAX(CASE WHEN funnel_step >= 1 THEN 1 ELSE 0 END) as reached_step_1,
    MAX(CASE WHEN funnel_step >= 2 THEN 1 ELSE 0 END) as reached_step_2,
    MAX(CASE WHEN funnel_step >= 3 THEN 1 ELSE 0 END) as reached_step_3,
    MAX(CASE WHEN funnel_step >= 4 THEN 1 ELSE 0 END) as reached_step_4,
    MAX(CASE WHEN funnel_step >= 5 THEN 1 ELSE 0 END) as reached_step_5,
    MAX(funnel_step) as max_step_reached
  FROM funnel_events
  WHERE funnel_step > 0
  GROUP BY user_id, session_id
),
funnel_summary AS (
  SELECT 
    'Step 1: Page View' as step_name,
    1 as step_number,
    SUM(reached_step_1) as users_reached,
    SUM(reached_step_1) / COUNT(*) as conversion_rate,
    NULL as drop_off_rate
  FROM user_funnel_progress
  
  UNION ALL
  
  SELECT 
    'Step 2: Product View' as step_name,
    2 as step_number,
    SUM(reached_step_2) as users_reached,
    SUM(reached_step_2) / SUM(reached_step_1) as conversion_rate,
    1 - (SUM(reached_step_2) / SUM(reached_step_1)) as drop_off_rate
  FROM user_funnel_progress
  WHERE reached_step_1 = 1
  
  UNION ALL
  
  SELECT 
    'Step 3: Add to Cart' as step_name,
    3 as step_number,
    SUM(reached_step_3) as users_reached,
    SUM(reached_step_3) / SUM(reached_step_2) as conversion_rate,
    1 - (SUM(reached_step_3) / SUM(reached_step_2)) as drop_off_rate
  FROM user_funnel_progress
  WHERE reached_step_2 = 1
  
  UNION ALL
  
  SELECT 
    'Step 4: Begin Checkout' as step_name,
    4 as step_number,
    SUM(reached_step_4) as users_reached,
    SUM(reached_step_4) / SUM(reached_step_3) as conversion_rate,
    1 - (SUM(reached_step_4) / SUM(reached_step_3)) as drop_off_rate
  FROM user_funnel_progress
  WHERE reached_step_3 = 1
  
  UNION ALL
  
  SELECT 
    'Step 5: Purchase' as step_name,
    5 as step_number,
    SUM(reached_step_5) as users_reached,
    SUM(reached_step_5) / SUM(reached_step_4) as conversion_rate,
    1 - (SUM(reached_step_5) / SUM(reached_step_4)) as drop_off_rate
  FROM user_funnel_progress
  WHERE reached_step_4 = 1
)
SELECT 
  step_name,
  step_number,
  users_reached,
  ROUND(conversion_rate * 100, 2) as conversion_rate_percent,
  ROUND(drop_off_rate * 100, 2) as drop_off_rate_percent,
  -- Overall conversion from step 1
  users_reached / FIRST_VALUE(users_reached) OVER (ORDER BY step_number) as overall_conversion_rate
FROM funnel_summary
ORDER BY step_number;

-- Time-based funnel analysis
WITH time_based_funnel AS (
  SELECT 
    user_id,
    session_id,
    MIN(CASE WHEN event_name = 'page_view' THEN event_timestamp END) as step_1_time,
    MIN(CASE WHEN event_name = 'product_view' THEN event_timestamp END) as step_2_time,
    MIN(CASE WHEN event_name = 'add_to_cart' THEN event_timestamp END) as step_3_time,
    MIN(CASE WHEN event_name = 'begin_checkout' THEN event_timestamp END) as step_4_time,
    MIN(CASE WHEN event_name = 'purchase' THEN event_timestamp END) as step_5_time
  FROM funnel_events
  GROUP BY user_id, session_id
),
funnel_timing AS (
  SELECT 
    user_id,
    session_id,
    TIMESTAMP_DIFF(step_2_time, step_1_time, SECOND) as time_to_product_view,
    TIMESTAMP_DIFF(step_3_time, step_2_time, SECOND) as time_to_add_cart,
    TIMESTAMP_DIFF(step_4_time, step_3_time, SECOND) as time_to_checkout,
    TIMESTAMP_DIFF(step_5_time, step_4_time, SECOND) as time_to_purchase,
    TIMESTAMP_DIFF(step_5_time, step_1_time, SECOND) as total_conversion_time
  FROM time_based_funnel
  WHERE step_1_time IS NOT NULL
)
SELECT 
  'Product View' as conversion_step,
  COUNT(*) as conversions,
  AVG(time_to_product_view) as avg_time_seconds,
  APPROX_QUANTILES(time_to_product_view, 100)[OFFSET(50)] as median_time_seconds,
  APPROX_QUANTILES(time_to_product_view, 100)[OFFSET(95)] as p95_time_seconds
FROM funnel_timing
WHERE time_to_product_view IS NOT NULL AND time_to_product_view > 0

UNION ALL

SELECT 
  'Add to Cart' as conversion_step,
  COUNT(*) as conversions,
  AVG(time_to_add_cart) as avg_time_seconds,
  APPROX_QUANTILES(time_to_add_cart, 100)[OFFSET(50)] as median_time_seconds,
  APPROX_QUANTILES(time_to_add_cart, 100)[OFFSET(95)] as p95_time_seconds
FROM funnel_timing
WHERE time_to_add_cart IS NOT NULL AND time_to_add_cart > 0

UNION ALL

SELECT 
  'Purchase' as conversion_step,
  COUNT(*) as conversions,
  AVG(total_conversion_time) as avg_time_seconds,
  APPROX_QUANTILES(total_conversion_time, 100)[OFFSET(50)] as median_time_seconds,
  APPROX_QUANTILES(total_conversion_time, 100)[OFFSET(95)] as p95_time_seconds
FROM funnel_timing
WHERE total_conversion_time IS NOT NULL AND total_conversion_time > 0;
```

### 40. How do you implement RFM analysis in BigQuery?

**Answer:** Recency, Frequency, Monetary analysis for customer segmentation.

```sql
-- RFM Analysis implementation
WITH customer_metrics AS (
  SELECT 
    customer_id,
    -- Recency: Days since last purchase
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) as recency_days,
    -- Frequency: Number of orders
    COUNT(DISTINCT order_id) as frequency,
    -- Monetary: Total spent
    SUM(order_value) as monetary_value,
    -- Additional metrics
    AVG(order_value) as avg_order_value,
    MIN(order_date) as first_order_date,
    MAX(order_date) as last_order_date
  FROM `project.dataset.orders`
  WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
  GROUP BY customer_id
),
rfm_scores AS (
  SELECT 
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    avg_order_value,
    
    -- RFM Scoring (1-5 scale, 5 being best)
    CASE 
      WHEN recency_days <= 30 THEN 5
      WHEN recency_days <= 60 THEN 4
      WHEN recency_days <= 90 THEN 3
      WHEN recency_days <= 180 THEN 2
      ELSE 1
    END as recency_score,
    
    CASE 
      WHEN frequency >= 10 THEN 5
      WHEN frequency >= 7 THEN 4
      WHEN frequency >= 4 THEN 3
      WHEN frequency >= 2 THEN 2
      ELSE 1
    END as frequency_score,
    
    CASE 
      WHEN monetary_value >= 1000 THEN 5
      WHEN monetary_value >= 500 THEN 4
      WHEN monetary_value >= 200 THEN 3
      WHEN monetary_value >= 50 THEN 2
      ELSE 1
    END as monetary_score
  FROM customer_metrics
),
rfm_segments AS (
  SELECT 
    *,
    CONCAT(
      CAST(recency_score AS STRING),
      CAST(frequency_score AS STRING), 
      CAST(monetary_score AS STRING)
    ) as rfm_score,
    
    -- Customer segmentation based on RFM scores
    CASE 
      WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
      WHEN recency_score >= 3 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Loyal Customers'
      WHEN recency_score >= 4 AND frequency_score <= 2 THEN 'New Customers'
      WHEN recency_score >= 3 AND frequency_score >= 3 AND monetary_score <= 2 THEN 'Potential Loyalists'
      WHEN recency_score >= 3 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'Promising'
      WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Need Attention'
      WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score <= 2 THEN 'About to Sleep'
      WHEN recency_score <= 2 AND frequency_score <= 2 AND monetary_score >= 3 THEN 'At Risk'
      WHEN recency_score <= 2 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'Lost'
      ELSE 'Others'
    END as customer_segment
  FROM rfm_scores
)
SELECT 
  customer_segment,
  COUNT(*) as customer_count,
  ROUND(COUNT(*) / SUM(COUNT(*)) OVER () * 100, 2) as segment_percentage,
  AVG(recency_days) as avg_recency_days,
  AVG(frequency) as avg_frequency,
  AVG(monetary_value) as avg_monetary_value,
  SUM(monetary_value) as total_segment_value,
  AVG(recency_score) as avg_recency_score,
  AVG(frequency_score) as avg_frequency_score,
  AVG(monetary_score) as avg_monetary_score
FROM rfm_segments
GROUP BY customer_segment
ORDER BY total_segment_value DESC;

-- RFM trend analysis over time
WITH monthly_rfm AS (
  SELECT 
    DATE_TRUNC(analysis_date, MONTH) as analysis_month,
    customer_segment,
    COUNT(*) as customer_count,
    AVG(monetary_value) as avg_clv
  FROM (
    SELECT 
      DATE_SUB(CURRENT_DATE(), INTERVAL month_offset MONTH) as analysis_date,
      customer_id,
      -- Recalculate RFM for each month
      DATE_DIFF(DATE_SUB(CURRENT_DATE(), INTERVAL month_offset MONTH), 
                MAX(order_date), DAY) as recency_days,
      COUNT(DISTINCT order_id) as frequency,
      SUM(order_value) as monetary_value
    FROM `project.dataset.orders` o
    CROSS JOIN UNNEST(GENERATE_ARRAY(0, 11)) as month_offset
    WHERE order_date <= DATE_SUB(CURRENT_DATE(), INTERVAL month_offset MONTH)
      AND order_date >= DATE_SUB(DATE_SUB(CURRENT_DATE(), INTERVAL month_offset MONTH), INTERVAL 365 DAY)
    GROUP BY analysis_date, customer_id
  ) monthly_data
  JOIN rfm_segments rs ON monthly_data.customer_id = rs.customer_id
  GROUP BY analysis_month, customer_segment
)
SELECT 
  analysis_month,
  customer_segment,
  customer_count,
  avg_clv,
  LAG(customer_count) OVER (PARTITION BY customer_segment ORDER BY analysis_month) as prev_count,
  customer_count - LAG(customer_count) OVER (PARTITION BY customer_segment ORDER BY analysis_month) as count_change
FROM monthly_rfm
ORDER BY analysis_month DESC, customer_count DESC;
```
