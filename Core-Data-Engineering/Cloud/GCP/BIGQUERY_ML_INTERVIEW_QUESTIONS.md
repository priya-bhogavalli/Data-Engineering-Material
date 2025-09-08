# BigQuery Machine Learning - Interview Questions

## 1. What is machine learning in BigQuery and how does it work?

**Answer:**
BigQuery ML enables data analysts to create and execute machine learning models using SQL queries directly in BigQuery.

**Key Features:**

**Built-in ML Models:**
- Linear regression
- Logistic regression
- K-means clustering
- Time series forecasting (ARIMA)
- Deep neural networks
- XGBoost
- AutoML integration

**SQL-Based Interface:**
```sql
-- Create a linear regression model
CREATE MODEL `project.dataset.sales_model`
OPTIONS(model_type='linear_reg') AS
SELECT
  advertising_spend,
  season,
  sales_amount as label
FROM `project.dataset.sales_data`;

-- Make predictions
SELECT
  predicted_sales_amount,
  advertising_spend
FROM ML.PREDICT(MODEL `project.dataset.sales_model`,
  (SELECT advertising_spend, season FROM `project.dataset.new_data`));
```

**Workflow:**
1. **CREATE MODEL**: Define and train model with SQL
2. **ML.EVALUATE**: Assess model performance
3. **ML.PREDICT**: Generate predictions
4. **ML.EXPLAIN**: Understand feature importance

**Advantages:**
- No data movement required
- Scales automatically
- Integrated with BigQuery ecosystem
- No separate ML infrastructure needed

## 2. What types of ML problems can BigQuery ML solve?

**Answer:**
BigQuery ML supports various machine learning use cases:

**Supervised Learning:**
- **Classification**: Customer churn, fraud detection
- **Regression**: Sales forecasting, price prediction

**Unsupervised Learning:**
- **Clustering**: Customer segmentation, anomaly detection

**Time Series:**
- **Forecasting**: Demand planning, resource allocation

**Deep Learning:**
- **Neural Networks**: Complex pattern recognition

**Example Use Cases:**
```sql
-- Customer Lifetime Value Prediction
CREATE MODEL `project.dataset.clv_model`
OPTIONS(model_type='linear_reg') AS
SELECT
  customer_age,
  purchase_frequency,
  avg_order_value,
  lifetime_value as label
FROM `project.dataset.customer_data`;

-- Customer Segmentation
CREATE MODEL `project.dataset.segment_model`
OPTIONS(model_type='kmeans', num_clusters=4) AS
SELECT
  annual_spend,
  purchase_frequency,
  days_since_last_purchase
FROM `project.dataset.customer_behavior`;
```