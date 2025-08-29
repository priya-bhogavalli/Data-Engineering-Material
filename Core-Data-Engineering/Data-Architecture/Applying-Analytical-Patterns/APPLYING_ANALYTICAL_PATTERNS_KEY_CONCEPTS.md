# Applying Analytical Patterns Key Concepts

## 📋 Table of Contents

1. [What are Analytical Patterns?](#-what-are-analytical-patterns)
2. [Core Analytical Patterns](#️-core-analytical-patterns)
   - [Slowly Changing Dimensions (SCD)](#1-slowly-changing-dimensions-scd)
   - [Key Difference: Type 2 vs Type 3](#-key-difference-type-2-vs-type-3)
   - [When to Use Each Type](#-when-to-use-each-type)
   - [Factless Fact Tables](#2-factless-fact-tables)
   - [Accumulating Snapshot](#3-accumulating-snapshot)
3. [Advanced Patterns](#-advanced-patterns)
   - [Bridge Tables](#bridge-tables)

---

## 📋 Table of Contents

### 🎯 [What are Analytical Patterns?](#-what-are-analytical-patterns)

### 📊 [Dimensions vs Facts - Fundamental Concepts](#-dimensions-vs-facts---fundamental-concepts)

### 🏗️ [Core Analytical Patterns](#️-core-analytical-patterns)
1. **[Slowly Changing Dimensions (SCD)](#1-slowly-changing-dimensions-scd)**
   - [Key Difference: Type 2 vs Type 3](#-key-difference-type-2-vs-type-3)
   - [When to Use Each Type](#-when-to-use-each-type)
2. **[Factless Fact Tables](#2-factless-fact-tables)**
3. **[Accumulating Snapshot](#3-accumulating-snapshot)**

### 📊 [Advanced Patterns](#-advanced-patterns)
4. **[Bridge Tables](#bridge-tables)**
5. **[Hierarchy Flattening](#hierarchy-flattening)**
6. **[Conformed Dimensions](#conformed-dimensions)**
7. **[Periodic Snapshot](#periodic-snapshot)**
8. **[Transaction Fact](#transaction-fact)**
9. **[Mini-Dimensions](#mini-dimensions)**
10. **[Junk Dimensions](#junk-dimensions)**
11. **[Role-Playing Dimensions](#role-playing-dimensions)**
12. **[Degenerate Dimensions](#degenerate-dimensions)**

### 🔧 [Implementation Patterns](#-implementation-patterns)
- **[Python Implementation](#python-implementation)**
- **[Time-Based Patterns](#time-based-patterns)**

### 🎯 [Pattern Selection Guide](#-pattern-selection-guide)
- **[When to Use Each Pattern](#when-to-use-each-pattern)**
- **[Implementation Decision Tree](#implementation-decision-tree)**

### 🎯 [Use Cases](#-use-cases)

### 🔧 [Implementation Best Practices](#-implementation-best-practices)

---

## 🎯 What are Analytical Patterns?
Reusable design templates that solve common data analysis and reporting problems in data warehousing and analytics. These patterns provide proven solutions for handling complex data relationships, tracking changes over time, and optimizing query performance in analytical systems.

## 📊 Dimensions vs Facts - Fundamental Concepts

### 🔍 **Key Differences**

| Aspect | Dimensions | Facts |
|--------|------------|-------|
| **Purpose** | Describe the "WHO, WHAT, WHERE, WHEN" | Record the "HOW MUCH, HOW MANY" |
| **Data Type** | Descriptive, textual attributes | Numeric measures, quantities |
| **Size** | Smaller, relatively static | Larger, grows continuously |
| **Updates** | Occasional changes (SCD patterns) | Frequent inserts |
| **Queries** | Used for filtering, grouping | Used for aggregation, calculation |

### 📋 **Dimensions - The Context**
**Description**: Provide context and descriptive information for analysis. They answer "Who did what, where, and when?"

**Characteristics**:
- **Descriptive attributes**: Names, descriptions, categories
- **Hierarchical**: Can have multiple levels (Country → State → City)
- **Relatively stable**: Don't change frequently
- **Used for**: Filtering, grouping, drill-down analysis

**Real Example**: Customer Dimension
```sql
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,     -- Surrogate key
    customer_id INT,                  -- Business key
    customer_name VARCHAR(100),       -- Descriptive
    email VARCHAR(100),              -- Descriptive
    phone VARCHAR(20),               -- Descriptive
    address VARCHAR(200),            -- Descriptive
    city VARCHAR(50),                -- Hierarchical
    state VARCHAR(50),               -- Hierarchical
    country VARCHAR(50),             -- Hierarchical
    customer_segment VARCHAR(20),     -- Categorical
    registration_date DATE           -- Descriptive
);

-- Sample dimension data
INSERT INTO dim_customer VALUES 
(1, 101, 'John Smith', 'john@email.com', '555-1234', 
 '123 Main St', 'New York', 'NY', 'USA', 'Premium', '2024-01-15');
```

### 📈 **Facts - The Measurements**
**Description**: Store quantitative data and measurements. They answer "How much?" and "How many?"

**Characteristics**:
- **Numeric measures**: Sales amounts, quantities, counts
- **Foreign keys**: References to dimensions
- **Additive**: Can be summed across dimensions
- **High volume**: Grows rapidly with business activity
- **Used for**: Calculations, aggregations, KPIs

**Real Example**: Sales Fact
```sql
CREATE TABLE fact_sales (
    sale_key INT PRIMARY KEY,         -- Surrogate key
    customer_key INT,                 -- FK to dim_customer
    product_key INT,                  -- FK to dim_product
    date_key INT,                     -- FK to dim_date
    store_key INT,                    -- FK to dim_store
    -- MEASURES (the "facts")
    quantity_sold INT,                -- How many?
    unit_price DECIMAL(10,2),         -- How much each?
    sales_amount DECIMAL(10,2),       -- Total revenue
    cost_amount DECIMAL(10,2),        -- Total cost
    profit_amount DECIMAL(10,2)       -- Calculated measure
);

-- Sample fact data
INSERT INTO fact_sales VALUES 
(1, 1, 201, 20240115, 301, 2, 25.00, 50.00, 30.00, 20.00);
```

### 🔗 **How They Work Together**
**Star Schema Example**: Facts in center, dimensions around the edges

```sql
-- Analysis: Sales by customer segment and product category
SELECT 
    c.customer_segment,              -- Dimension attribute
    p.category,                      -- Dimension attribute
    d.month_name,                    -- Dimension attribute
    COUNT(*) as transaction_count,    -- Fact aggregation
    SUM(f.quantity_sold) as total_qty, -- Fact aggregation
    SUM(f.sales_amount) as total_sales, -- Fact aggregation
    AVG(f.unit_price) as avg_price   -- Fact aggregation
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY c.customer_segment, p.category, d.month_name
ORDER BY total_sales DESC;
```

### 🎯 **Types of Measures in Facts**

**1. Additive Measures**: Can be summed across all dimensions
```sql
-- Examples: Sales amount, quantity, cost
SELECT SUM(sales_amount) FROM fact_sales; -- Valid across all dimensions
```

**2. Semi-Additive Measures**: Can be summed across some dimensions, not others
```sql
-- Examples: Account balance, inventory levels
-- Can sum across accounts, but NOT across time
SELECT account_key, balance_amount FROM fact_account_balance 
WHERE date_key = 20241231; -- Point-in-time only
```

**3. Non-Additive Measures**: Cannot be summed meaningfully
```sql
-- Examples: Ratios, percentages, temperatures
-- Use AVG, MIN, MAX instead of SUM
SELECT AVG(profit_margin_percent) FROM fact_sales;
```

### 🔄 **Dimension vs Fact Design Decisions**

**When to use Dimension**:
- Descriptive, categorical data
- Used for filtering and grouping
- Changes infrequently
- Examples: Customer, Product, Date, Geography

**When to use Fact**:
- Numeric, measurable data
- Used for calculations and aggregations
- High volume, frequent updates
- Examples: Sales, Transactions, Inventory, Performance metrics

**Gray Areas - Could be Either**:
- **Price**: Could be dimension attribute (product price) or fact measure (transaction price)
- **Status**: Could be dimension (current status) or fact (status changes)
- **Decision factors**: Update frequency, analysis needs, data volume

## 🏗️ Core Analytical Patterns

### 1. Slowly Changing Dimensions (SCD)
**Description**: Handles how dimension data changes over time. Type 1 overwrites old values (current state only), Type 2 creates new records to preserve history, and Type 3 adds columns for previous values. Essential for tracking customer information, product details, or any reference data that evolves.

**Real Example**: Employee department tracking - Same scenario, different approaches
- **Type 1**: Only current department (no history)
- **Type 2**: Complete history of all department changes (multiple rows)
- **Type 3**: Current + one previous department only (single row)

## 🔍 **Key Difference: Type 2 vs Type 3**
**Scenario**: Employee John Doe changes departments: Sales → Marketing → Finance

**Type 2**: Creates NEW ROW for each change (unlimited history)
**Type 3**: Updates SAME ROW with limited history (current + previous only)

```sql
-- Type 1 SCD: Product pricing (overwrite - no history needed)
-- Before: iPhone 14 costs $999
-- After: iPhone 14 costs $899 (price drop)
CREATE TABLE dim_product_type1 (
    product_key SERIAL PRIMARY KEY,
    product_id INT UNIQUE,
    product_name VARCHAR(100),
    current_price DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Price change: $999 → $899 (old price lost)
UPDATE dim_product_type1 
SET current_price = 899.00, last_updated = CURRENT_TIMESTAMP
WHERE product_id = 'IPHONE14';

-- Type 2 SCD: Complete department history (multiple rows per employee)
CREATE TABLE dim_employee_type2 (
    employee_key SERIAL PRIMARY KEY,
    employee_id INT,
    name VARCHAR(100),
    department VARCHAR(50),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
);

-- John's department changes: Sales → Marketing → Finance
-- RESULT: 3 separate rows for John (complete history)

-- Initial: John in Sales (Jan 1 - Mar 31)
INSERT INTO dim_employee_type2 VALUES 
(1, 123, 'John Doe', 'Sales', '2024-01-01', '2024-03-31', FALSE);

-- Change 1: John moves to Marketing (Apr 1 - Aug 31)
INSERT INTO dim_employee_type2 VALUES 
(2, 123, 'John Doe', 'Marketing', '2024-04-01', '2024-08-31', FALSE);

-- Change 2: John moves to Finance (Sep 1 - current)
INSERT INTO dim_employee_type2 VALUES 
(3, 123, 'John Doe', 'Finance', '2024-09-01', '9999-12-31', TRUE);

-- Query: John's complete department history
SELECT employee_id, name, department, effective_date, expiry_date
FROM dim_employee_type2 
WHERE employee_id = 123
ORDER BY effective_date;
-- Returns: 3 rows showing Sales → Marketing → Finance

-- Type 3 SCD: Limited history (current + previous only in same row)
CREATE TABLE dim_employee_type3 (
    employee_key SERIAL PRIMARY KEY,
    employee_id INT UNIQUE,
    name VARCHAR(100),
    current_department VARCHAR(50),
    previous_department VARCHAR(50),
    department_change_date DATE
);

-- Same scenario: John's changes Sales → Marketing → Finance
-- RESULT: 1 row for John (loses Sales history when he moves to Finance)

-- Initial state: John in Sales
INSERT INTO dim_employee_type3 VALUES 
(123, 123, 'John Doe', 'Sales', NULL, '2024-01-01');

-- Change 1: Sales → Marketing (Sales becomes previous)
UPDATE dim_employee_type3 
SET previous_department = current_department,
    current_department = 'Marketing',
    department_change_date = '2024-04-01'
WHERE employee_id = 123;
-- Row now shows: Current=Marketing, Previous=Sales

-- Change 2: Marketing → Finance (Marketing becomes previous, Sales is LOST)
UPDATE dim_employee_type3 
SET previous_department = current_department,
    current_department = 'Finance',
    department_change_date = '2024-09-01'
WHERE employee_id = 123;
-- Row now shows: Current=Finance, Previous=Marketing (Sales history LOST)

-- 📊 COMPARISON SUMMARY:
-- Type 2: 3 rows = Complete history (Sales, Marketing, Finance)
-- Type 3: 1 row = Limited history (Finance + Marketing only, Sales lost)
```

## 🎯 **When to Use Each Type**

| Aspect | Type 2 | Type 3 |
|--------|--------|--------|
| **History** | Complete unlimited history | Current + 1 previous only |
| **Storage** | More storage (multiple rows) | Less storage (single row) |
| **Complexity** | More complex queries | Simpler queries |
| **Use Case** | Audit trails, compliance | Simple before/after analysis |
| **Example** | Customer address changes | Employee department transfers |

**Choose Type 2 when**: You need complete audit trail (banking, healthcare, compliance)
**Choose Type 3 when**: You only need to compare current vs previous state (reporting, simple analysis)

### 2. Factless Fact Tables
**Description**: Fact tables that capture events or relationships without numeric measures. Used to track occurrences like student attendance, product promotions, or coverage scenarios. They answer "what happened" rather than "how much" questions.

**Real Example**: University attendance tracking
- Track which students attended which classes on which days
- No measures like grades or hours - just the fact that attendance occurred
- Enables analysis: "Which students have perfect attendance?" or "What's the attendance rate by class?"

```sql
-- Student attendance tracking (no numeric measures)
CREATE TABLE fact_student_attendance (
    student_key INT,        -- References dim_student
    date_key INT,          -- References dim_date  
    class_key INT,         -- References dim_class
    attendance_type_key INT, -- References dim_attendance_type (Present, Absent, Late)
    PRIMARY KEY (student_key, date_key, class_key)
);

-- Sample data: Student 101 attended Math class on Jan 15, 2024
INSERT INTO fact_student_attendance VALUES 
(101, 20240115, 201, 1), -- Present
(102, 20240115, 201, 2), -- Absent  
(103, 20240115, 201, 3); -- Late

-- Query: Find attendance rate for Math class
SELECT 
    c.class_name,
    COUNT(CASE WHEN at.type_name = 'Present' THEN 1 END) * 100.0 / COUNT(*) as attendance_rate
FROM fact_student_attendance f
JOIN dim_class c ON f.class_key = c.class_key
JOIN dim_attendance_type at ON f.attendance_type_key = at.type_key
WHERE c.class_name = 'Mathematics'
GROUP BY c.class_name;
```

### 3. Accumulating Snapshot
**Description**: Tracks the progress of processes through multiple milestones by updating a single record as events occur. Perfect for order fulfillment, loan processing, or any workflow with defined stages. Shows the complete lifecycle in one row.

**Real Example**: E-commerce order fulfillment
- Single row per order that gets updated as order progresses
- Track: Order → Payment → Shipping → Delivery milestones
- Calculate performance metrics: time to ship, time to deliver

```sql
-- Order lifecycle tracking with milestones
CREATE TABLE fact_order_snapshot (
    order_key INT PRIMARY KEY,
    customer_key INT,
    order_date_key INT,
    payment_date_key INT,
    ship_date_key INT,
    delivery_date_key INT,
    order_amount DECIMAL(10,2),
    days_to_ship INT,
    days_to_deliver INT,
    order_status VARCHAR(20)
);

-- Order lifecycle example: Order #12345
-- Day 1: Order placed
INSERT INTO fact_order_snapshot (order_key, customer_key, order_date_key, order_amount, order_status)
VALUES (12345, 101, 20240115, 299.99, 'ORDERED');

-- Day 1: Payment received (same day)
UPDATE fact_order_snapshot 
SET payment_date_key = 20240115, order_status = 'PAID'
WHERE order_key = 12345;

-- Day 3: Order shipped
UPDATE fact_order_snapshot 
SET ship_date_key = 20240117, 
    days_to_ship = 2,
    order_status = 'SHIPPED'
WHERE order_key = 12345;

-- Day 5: Order delivered
UPDATE fact_order_snapshot 
SET delivery_date_key = 20240119,
    days_to_deliver = 2,
    order_status = 'DELIVERED'
WHERE order_key = 12345;

-- Analysis: Average shipping performance
SELECT 
    AVG(days_to_ship) as avg_ship_time,
    AVG(days_to_deliver) as avg_delivery_time
FROM fact_order_snapshot 
WHERE order_status = 'DELIVERED';
```

## 📊 Advanced Patterns

### Bridge Tables
**Description**: Solves many-to-many relationships between dimensions and facts. For example, when multiple customers share an account or a product belongs to multiple categories. Includes allocation percentages to distribute measures appropriately across related entities.

**Real Example**: Joint bank account management
- Account shared by husband and wife (50/50 split)
- Business account with 3 partners (33.33% each)
- Enables proper allocation of account balances and transactions

```sql
-- Joint account ownership tracking
CREATE TABLE bridge_account_customer (
    account_key INT,
    customer_key INT,
    allocation_percentage DECIMAL(5,2),
    relationship_type VARCHAR(20),
    effective_date DATE
);

-- Example: Joint checking account
-- Account 1001 shared by John (customer 101) and Jane (customer 102)
INSERT INTO bridge_account_customer VALUES 
(1001, 101, 50.00, 'PRIMARY', '2024-01-01'),    -- John 50%
(1001, 102, 50.00, 'JOINT', '2024-01-01');      -- Jane 50%

-- Business account with 3 partners
INSERT INTO bridge_account_customer VALUES 
(2001, 201, 33.33, 'PARTNER', '2024-01-01'),    -- Partner A
(2001, 202, 33.33, 'PARTNER', '2024-01-01'),    -- Partner B  
(2001, 203, 33.34, 'PARTNER', '2024-01-01');    -- Partner C

-- Query: Customer's share of account balance
SELECT 
    c.customer_name,
    a.account_number,
    f.balance_amount,
    b.allocation_percentage,
    (f.balance_amount * b.allocation_percentage / 100) as customer_share
FROM fact_account_balance f
JOIN bridge_account_customer b ON f.account_key = b.account_key
JOIN dim_customer c ON b.customer_key = c.customer_key
JOIN dim_account a ON f.account_key = a.account_key
WHERE c.customer_id = 101;
```

### Hierarchy Flattening
**Description**: Stores hierarchical data (like organizational charts or product categories) in a flat structure within dimensions. Enables easy drill-down and roll-up operations without complex joins. Each level of the hierarchy becomes a separate column.

**Real Example**: Retail product hierarchy
- Electronics → Computers → Laptops → Gaming Laptops → "ASUS ROG Strix"
- Enables easy reporting at any level: Department, Category, Subcategory, Product
- Fast aggregation without recursive queries

```sql
-- Flattened product hierarchy for easy reporting
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_code VARCHAR(20),
    product_name VARCHAR(100),
    brand VARCHAR(50),
    subcategory VARCHAR(50),     -- Gaming Laptops
    category VARCHAR(50),        -- Laptops  
    department VARCHAR(50),      -- Computers
    division VARCHAR(50),        -- Electronics
    level_1_rollup VARCHAR(50),  -- Technology
    level_2_rollup VARCHAR(50)   -- All Products
);

-- Sample data: Gaming laptop hierarchy
INSERT INTO dim_product VALUES (
    1001, 
    'ASUS-ROG-001', 
    'ASUS ROG Strix G15', 
    'ASUS',
    'Gaming Laptops',     -- Level 4
    'Laptops',           -- Level 3  
    'Computers',         -- Level 2
    'Electronics',       -- Level 1
    'Technology',        -- Rollup 1
    'All Products'       -- Rollup 2
);

-- Easy drill-down reporting without joins
-- Department level sales
SELECT department, SUM(sales_amount) 
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY department;

-- Category level sales  
SELECT category, SUM(sales_amount)
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
WHERE department = 'Computers'
GROUP BY category;
```

### Conformed Dimensions
**Description**: Shared dimensions used consistently across multiple fact tables to enable integrated reporting. Examples include date, geography, or customer dimensions. Ensures data consistency and enables cross-process analysis.

**Real Example**: Retail analytics with shared date dimension
- Same date dimension used by Sales, Inventory, and Marketing fact tables
- Enables integrated analysis: "Compare sales vs inventory levels by quarter"
- Consistent calendar definitions across all business processes

```sql
-- Shared date dimension across all business processes
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,        -- 20240115
    full_date DATE,                  -- 2024-01-15
    day_name VARCHAR(10),           -- Monday
    month_name VARCHAR(10),         -- January
    quarter INT,                    -- 1
    year INT,                       -- 2024
    fiscal_year INT,               -- 2024 (or 2025 if fiscal year starts July)
    is_holiday BOOLEAN,            -- FALSE
    is_weekend BOOLEAN,            -- FALSE
    week_of_year INT               -- 3
);

-- Sales fact table uses conformed date
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    customer_key INT,
    product_key INT,
    sales_amount DECIMAL(10,2),
    quantity_sold INT
);

-- Inventory fact table uses same conformed date
CREATE TABLE fact_inventory (
    inventory_id INT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT,
    warehouse_key INT,
    stock_quantity INT,
    reorder_point INT
);

-- Marketing campaigns use same conformed date
CREATE TABLE fact_marketing_spend (
    campaign_id INT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    channel_key INT,
    spend_amount DECIMAL(10,2),
    impressions INT
);

-- Integrated analysis: Sales vs Marketing spend by quarter
SELECT 
    d.quarter,
    d.year,
    SUM(s.sales_amount) as total_sales,
    SUM(m.spend_amount) as total_marketing_spend,
    SUM(s.sales_amount) / SUM(m.spend_amount) as roi_ratio
FROM dim_date d
LEFT JOIN fact_sales s ON d.date_key = s.date_key
LEFT JOIN fact_marketing_spend m ON d.date_key = m.date_key
WHERE d.year = 2024
GROUP BY d.quarter, d.year
ORDER BY d.quarter;
```

### Periodic Snapshot
**Description**: Captures the state of measures at regular intervals (daily, weekly, monthly). Unlike accumulating snapshots that track process milestones, periodic snapshots show point-in-time balances or quantities.

**Real Example**: Monthly account balances
- Capture account balance at month-end for trend analysis
- Track inventory levels at regular intervals
- Monitor KPI performance over time

```sql
-- Monthly account balance snapshots
CREATE TABLE fact_account_balance_monthly (
    account_key INT,
    month_end_date_key INT,
    balance_amount DECIMAL(15,2),
    transaction_count INT,
    average_daily_balance DECIMAL(15,2),
    PRIMARY KEY (account_key, month_end_date_key)
);

-- Sample data: Account balances at month-end
INSERT INTO fact_account_balance_monthly VALUES 
(1001, 20240131, 15000.00, 25, 14500.00),  -- Jan 2024
(1001, 20240229, 16200.00, 30, 15800.00),  -- Feb 2024
(1001, 20240331, 14800.00, 22, 15100.00);  -- Mar 2024

-- Analysis: Account balance trends
SELECT 
    a.account_number,
    d.month_name,
    f.balance_amount,
    LAG(f.balance_amount) OVER (PARTITION BY f.account_key ORDER BY f.month_end_date_key) as prev_balance,
    f.balance_amount - LAG(f.balance_amount) OVER (PARTITION BY f.account_key ORDER BY f.month_end_date_key) as balance_change
FROM fact_account_balance_monthly f
JOIN dim_account a ON f.account_key = a.account_key
JOIN dim_date d ON f.month_end_date_key = d.date_key;
```

### Transaction Fact
**Description**: Records individual business events as they occur with full detail. Most granular level of fact data, typically used for detailed analysis and as source for other fact types.

**Real Example**: Banking transactions
- Every deposit, withdrawal, transfer recorded individually
- Enables detailed transaction analysis and audit trails
- Source data for periodic snapshots and accumulating snapshots

```sql
-- Individual transaction recording
CREATE TABLE fact_transactions (
    transaction_key INT PRIMARY KEY,
    account_key INT,
    date_key INT,
    time_key INT,
    transaction_type_key INT,
    amount DECIMAL(15,2),
    running_balance DECIMAL(15,2),
    description VARCHAR(200)
);

-- Sample transactions for account 1001
INSERT INTO fact_transactions VALUES 
(1, 1001, 20240115, 0900, 1, 1000.00, 15000.00, 'Salary deposit'),
(2, 1001, 20240116, 1430, 2, -250.00, 14750.00, 'ATM withdrawal'),
(3, 1001, 20240117, 1015, 3, -75.50, 14674.50, 'Online purchase');

-- Analysis: Daily transaction summary
SELECT 
    d.full_date,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN f.amount > 0 THEN f.amount END) as total_deposits,
    SUM(CASE WHEN f.amount < 0 THEN ABS(f.amount) END) as total_withdrawals,
    SUM(f.amount) as net_change
FROM fact_transactions f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.account_key = 1001
GROUP BY d.full_date
ORDER BY d.full_date;
```

### Mini-Dimensions
**Description**: Handles rapidly changing dimension attributes by splitting them into separate smaller dimensions. Reduces the number of SCD Type 2 records in main dimension.

**Real Example**: Customer demographics
- Customer age, income bracket change frequently
- Split into mini-dimension to avoid excessive SCD Type 2 records
- Main customer dimension remains stable

```sql
-- Main customer dimension (stable attributes)
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id INT,
    name VARCHAR(100),
    gender VARCHAR(10),
    registration_date DATE
);

-- Mini-dimension for changing demographics
CREATE TABLE dim_customer_demographics (
    demographics_key INT PRIMARY KEY,
    age_range VARCHAR(20),      -- 25-34, 35-44, etc.
    income_bracket VARCHAR(20), -- 50K-75K, 75K-100K, etc.
    credit_score_range VARCHAR(20), -- 700-750, 750-800, etc.
    effective_date DATE,
    expiry_date DATE
);

-- Fact table references both dimensions
CREATE TABLE fact_customer_transactions (
    transaction_key INT PRIMARY KEY,
    customer_key INT REFERENCES dim_customer(customer_key),
    demographics_key INT REFERENCES dim_customer_demographics(demographics_key),
    date_key INT,
    amount DECIMAL(10,2)
);

-- Sample data: Customer ages from 25-34 to 35-44 bracket
INSERT INTO dim_customer_demographics VALUES 
(1, '25-34', '50K-75K', '700-750', '2024-01-01', '2024-12-31'),
(2, '35-44', '75K-100K', '750-800', '2025-01-01', '9999-12-31');
```

### Junk Dimensions
**Description**: Combines low-cardinality flags and indicators into a single dimension to avoid creating many small dimensions. Reduces fact table width and improves performance.

**Real Example**: Transaction flags
- Online/offline, weekend/weekday, promotional/regular flags
- Instead of 3 separate dimensions, create one junk dimension
- Pre-populate all possible combinations

```sql
-- Junk dimension for transaction flags
CREATE TABLE dim_transaction_flags (
    flags_key INT PRIMARY KEY,
    is_online BOOLEAN,
    is_weekend BOOLEAN,
    is_promotional BOOLEAN,
    is_international BOOLEAN,
    flag_combination VARCHAR(50)
);

-- Pre-populate all combinations (2^4 = 16 rows)
INSERT INTO dim_transaction_flags VALUES 
(1, FALSE, FALSE, FALSE, FALSE, 'Offline-Weekday-Regular-Domestic'),
(2, TRUE, FALSE, FALSE, FALSE, 'Online-Weekday-Regular-Domestic'),
(3, FALSE, TRUE, FALSE, FALSE, 'Offline-Weekend-Regular-Domestic'),
(4, TRUE, TRUE, TRUE, TRUE, 'Online-Weekend-Promotional-International');
-- ... continue for all 16 combinations

-- Fact table uses single junk dimension key
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    customer_key INT,
    product_key INT,
    date_key INT,
    flags_key INT REFERENCES dim_transaction_flags(flags_key),
    sales_amount DECIMAL(10,2)
);

-- Query: Sales by transaction type
SELECT 
    f.flag_combination,
    COUNT(*) as transaction_count,
    SUM(s.sales_amount) as total_sales
FROM fact_sales s
JOIN dim_transaction_flags f ON s.flags_key = f.flags_key
GROUP BY f.flag_combination;
```

### Role-Playing Dimensions
**Description**: Single physical dimension used multiple times in the same fact table with different logical meanings. Saves storage and maintenance while providing different analytical perspectives.

**Real Example**: Date dimension roles
- Order date, ship date, delivery date all use same date dimension
- Different foreign keys point to same dimension table
- Enables analysis by different date perspectives

```sql
-- Single date dimension
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_name VARCHAR(10),
    month_name VARCHAR(10),
    quarter INT,
    year INT
);

-- Fact table with multiple date roles
CREATE TABLE fact_orders (
    order_key INT PRIMARY KEY,
    customer_key INT,
    order_date_key INT REFERENCES dim_date(date_key),
    ship_date_key INT REFERENCES dim_date(date_key),
    delivery_date_key INT REFERENCES dim_date(date_key),
    order_amount DECIMAL(10,2)
);

-- Analysis using different date roles
SELECT 
    od.month_name as order_month,
    sd.month_name as ship_month,
    COUNT(*) as order_count,
    AVG(f.order_amount) as avg_order_value
FROM fact_orders f
JOIN dim_date od ON f.order_date_key = od.date_key    -- Order date role
JOIN dim_date sd ON f.ship_date_key = sd.date_key     -- Ship date role
WHERE od.year = 2024
GROUP BY od.month_name, sd.month_name;
```

### Degenerate Dimensions
**Description**: Dimension attributes stored directly in the fact table without a separate dimension table. Typically used for transaction numbers or other high-cardinality identifiers.

**Real Example**: Invoice numbers
- Invoice number stored in sales fact table
- No separate invoice dimension needed
- Provides grouping capability without additional joins

```sql
-- Fact table with degenerate dimension
CREATE TABLE fact_sales (
    sale_key INT PRIMARY KEY,
    invoice_number VARCHAR(20),  -- Degenerate dimension
    customer_key INT,
    product_key INT,
    date_key INT,
    line_number INT,            -- Another degenerate dimension
    quantity INT,
    unit_price DECIMAL(10,2),
    line_total DECIMAL(10,2)
);

-- Sample data: Multiple lines per invoice
INSERT INTO fact_sales VALUES 
(1, 'INV-2024-001', 101, 201, 20240115, 1, 2, 25.00, 50.00),
(2, 'INV-2024-001', 101, 202, 20240115, 2, 1, 15.00, 15.00),
(3, 'INV-2024-002', 102, 201, 20240115, 1, 3, 25.00, 75.00);

-- Analysis: Invoice-level summary using degenerate dimension
SELECT 
    invoice_number,
    COUNT(*) as line_count,
    SUM(quantity) as total_quantity,
    SUM(line_total) as invoice_total
FROM fact_sales
GROUP BY invoice_number
ORDER BY invoice_number;
```

## 🔧 Implementation Patterns
**Description**: Practical code implementations of analytical patterns using Python and SQL. These examples show how to automate pattern implementation, handle data quality, and maintain performance in production systems.

### Python Implementation
```python
import pandas as pd
from datetime import datetime, timedelta

class AnalyticalPatterns:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def implement_scd_type2(self, source_df, dim_table, business_key, compare_cols):
        """Implement SCD Type 2 pattern"""
        # Get current dimension data
        current_sql = f"SELECT * FROM {dim_table} WHERE is_current = TRUE"
        current_dim = pd.read_sql(current_sql, self.conn)
        
        # Identify changes
        changes = []
        for _, source_row in source_df.iterrows():
            current_row = current_dim[current_dim[business_key] == source_row[business_key]]
            
            if not current_row.empty:
                # Check if any tracked columns changed
                for col in compare_cols:
                    if current_row.iloc[0][col] != source_row[col]:
                        changes.append(source_row[business_key])
                        break
        
        if changes:
            # Expire changed records
            expire_sql = f"""
            UPDATE {dim_table} 
            SET expiry_date = %s, is_current = FALSE 
            WHERE {business_key} IN ({','.join(['%s'] * len(changes))}) 
            AND is_current = TRUE
            """
            
            cursor = self.conn.cursor()
            cursor.execute(expire_sql, [datetime.now().date()] + changes)
            
            # Insert new versions
            new_records = source_df[source_df[business_key].isin(changes)].copy()
            new_records['effective_date'] = datetime.now().date()
            new_records['expiry_date'] = datetime(9999, 12, 31).date()
            new_records['is_current'] = True
            
            new_records.to_sql(dim_table, self.conn, if_exists='append', index=False)
    
    def create_accumulating_snapshot(self, order_events_df):
        """Create accumulating snapshot fact table"""
        # Group events by order
        snapshot_data = []
        
        for order_id, events in order_events_df.groupby('order_id'):
            snapshot = {'order_id': order_id}
            
            # Extract milestone dates
            for _, event in events.iterrows():
                if event['event_type'] == 'ORDER_PLACED':
                    snapshot['order_date'] = event['event_date']
                elif event['event_type'] == 'PAYMENT_RECEIVED':
                    snapshot['payment_date'] = event['event_date']
                elif event['event_type'] == 'SHIPPED':
                    snapshot['ship_date'] = event['event_date']
                elif event['event_type'] == 'DELIVERED':
                    snapshot['delivery_date'] = event['event_date']
            
            # Calculate durations
            if 'order_date' in snapshot and 'ship_date' in snapshot:
                snapshot['days_to_ship'] = (snapshot['ship_date'] - snapshot['order_date']).days
            
            if 'ship_date' in snapshot and 'delivery_date' in snapshot:
                snapshot['days_to_deliver'] = (snapshot['delivery_date'] - snapshot['ship_date']).days
            
            snapshot_data.append(snapshot)
        
        return pd.DataFrame(snapshot_data)
    
    def implement_bridge_table(self, many_to_many_df, group_col, item_col):
        """Implement bridge table pattern for many-to-many relationships"""
        # Create bridge table with allocation percentages
        bridge_data = []
        
        for group_id, items in many_to_many_df.groupby(group_col):
            total_items = len(items)
            allocation = 1.0 / total_items  # Equal allocation
            
            for _, item in items.iterrows():
                bridge_data.append({
                    f'{group_col}_key': group_id,
                    f'{item_col}_key': item[item_col],
                    'allocation_percentage': allocation,
                    'effective_date': datetime.now().date()
                })
        
        return pd.DataFrame(bridge_data)
```

### Time-Based Patterns
**Description**: Specialized patterns for handling temporal data. Periodic snapshots capture state at regular intervals (daily, monthly), while transaction facts record individual events with timestamps. Critical for financial reporting and trend analysis.
```sql
-- Periodic snapshot pattern
CREATE TABLE fact_account_balance_monthly (
    account_key INT,
    date_key INT,
    balance_amount DECIMAL(15,2),
    transaction_count INT,
    PRIMARY KEY (account_key, date_key)
);

-- Transaction fact pattern
CREATE TABLE fact_transactions (
    transaction_key INT PRIMARY KEY,
    account_key INT,
    date_key INT,
    time_key INT,
    transaction_type_key INT,
    amount DECIMAL(15,2),
    running_balance DECIMAL(15,2)
);
```

## 🎯 Pattern Selection Guide
**Description**: Decision framework for choosing the right analytical pattern based on business requirements, technical constraints, and performance needs. Consider data volume, query patterns, and historical requirements when selecting patterns.

### When to Use Each Pattern

| Pattern | Use Case | Benefits | Considerations |
|---------|----------|----------|----------------|
| SCD Type 1 | Current state only | Simple, less storage | Loses history |
| SCD Type 2 | Historical tracking | Full audit trail | More complex, more storage |
| Factless Facts | Event tracking | Captures occurrences | No numeric measures |
| Accumulating Snapshot | Process milestones | Shows process flow | Complex updates |
| Bridge Tables | Many-to-many | Handles complex relationships | Query complexity |

### Implementation Decision Tree
**Description**: Automated decision logic to help select appropriate patterns based on specific requirements. This code-based approach ensures consistent pattern selection across different projects and teams.
```python
def choose_analytical_pattern(requirements):
    """Decision tree for pattern selection"""
    if requirements['track_history']:
        if requirements['storage_sensitive']:
            return "SCD_TYPE_1"
        else:
            return "SCD_TYPE_2"
    
    if requirements['many_to_many_relationships']:
        return "BRIDGE_TABLE"
    
    if requirements['process_tracking']:
        return "ACCUMULATING_SNAPSHOT"
    
    if requirements['event_tracking'] and not requirements['measures']:
        return "FACTLESS_FACT"
    
    return "STANDARD_DIMENSIONAL"
```

## 🎯 Use Cases
**Description**: Real-world applications where analytical patterns solve specific business problems:
- **Customer behavior analysis**: Track customer journey and preferences over time
- **Sales performance tracking**: Monitor sales trends and rep performance across regions
- **Inventory management**: Track stock levels, movements, and supplier relationships
- **Financial reporting**: Ensure accurate period-end reporting and audit trails
- **Operational metrics**: Monitor KPIs and process efficiency across departments
- **Process optimization**: Identify bottlenecks and improvement opportunities in workflows

## 🔧 Implementation Best Practices
**Description**: Essential guidelines for successful analytical pattern implementation in production environments:
- **Choose appropriate SCD types**: Match pattern complexity to business requirements and technical capabilities
- **Design for query performance**: Optimize indexes, partitioning, and data distribution for analytical workloads
- **Maintain referential integrity**: Ensure data consistency across dimensions and facts through proper constraints
- **Document business rules clearly**: Create comprehensive documentation for pattern logic and business definitions
- **Test data quality thoroughly**: Implement validation rules and monitoring for pattern-specific data issues
- **Monitor pattern performance**: Track query response times and resource usage for pattern-based queries
- **Consider storage implications**: Balance historical data retention with storage costs and performance requirements