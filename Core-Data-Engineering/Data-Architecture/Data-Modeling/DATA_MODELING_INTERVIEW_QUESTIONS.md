# Data Modeling Interview Questions

## 📋 Table of Contents
1. [Fundamentals](#fundamentals)
2. [Relational Data Modeling](#relational-data-modeling)
3. [Dimensional Modeling](#dimensional-modeling)
4. [Data Vault 2.0](#data-vault-20)
5. [Activity Schema](#activity-schema)
6. [NoSQL Data Modeling](#nosql-data-modeling)
7. [Modern Approaches](#modern-approaches)
8. [Performance & Optimization](#performance--optimization)
9. [Real-World Scenarios](#real-world-scenarios)

---

## Fundamentals

### Q1: What is data modeling and why is it important?
**Answer:**
Data modeling is the process of creating a conceptual representation of data structures and their relationships within a system. It serves as a blueprint for database design and data architecture.

**Importance:**
- **Communication**: Provides common language between business and technical teams
- **Data Quality**: Ensures consistency and integrity through defined relationships
- **Performance**: Optimizes query performance through proper structure design
- **Maintenance**: Simplifies system maintenance and evolution
- **Compliance**: Supports regulatory requirements and data governance

**Three Levels of Data Modeling:**
1. **Conceptual**: High-level business view (entities and relationships)
2. **Logical**: Detailed structure without implementation specifics
3. **Physical**: Implementation-specific design with indexes, partitions, etc.

### Q2: Compare different data modeling approaches and when to use each
**Answer:**

| Approach | Best For | Strengths | Weaknesses |
|----------|----------|-----------|------------|
| **Relational** | OLTP, transactional systems | ACID compliance, data integrity | Complex joins, rigid schema |
| **Dimensional** | OLAP, analytics, reporting | Query performance, business-friendly | Data redundancy, ETL complexity |
| **Data Vault** | Enterprise data warehouses | Auditability, flexibility | Learning curve, complexity |
| **Activity Schema** | Event-driven systems | Temporal analysis, immutability | Storage overhead, query complexity |
| **NoSQL** | Big data, flexible schemas | Scalability, schema flexibility | Eventual consistency, limited ACID |

### Q3: What are the key principles of good data modeling?
**Answer:**
1. **Simplicity**: Keep models as simple as possible while meeting requirements
2. **Consistency**: Use consistent naming conventions and patterns
3. **Completeness**: Capture all necessary business rules and relationships
4. **Flexibility**: Design for future changes and requirements
5. **Performance**: Consider query patterns and optimization needs
6. **Integrity**: Implement proper constraints and validation rules
7. **Documentation**: Maintain clear documentation and metadata

---

## Relational Data Modeling

### Q4: Explain database normalization and its forms
**Answer:**

**Normalization**: Process of organizing data to reduce redundancy and improve data integrity.

**Normal Forms:**

**1NF (First Normal Form):**
- Each column contains atomic values
- No repeating groups
- Each row is unique

```sql
-- Violates 1NF (multiple values in one column)
CREATE TABLE customers_bad (
    id INT,
    name VARCHAR(100),
    phones VARCHAR(200) -- "123-456-7890, 098-765-4321"
);

-- Follows 1NF
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE customer_phones (
    customer_id INT,
    phone VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**2NF (Second Normal Form):**
- Must be in 1NF
- No partial dependencies on composite primary keys

**3NF (Third Normal Form):**
- Must be in 2NF
- No transitive dependencies

**BCNF (Boyce-Codd Normal Form):**
- Stricter version of 3NF
- Every determinant is a candidate key

### Q5: When would you denormalize a database and what are the trade-offs?
**Answer:**

**When to Denormalize:**
- **Performance Requirements**: Frequent complex joins causing slow queries
- **Read-Heavy Workloads**: Analytics and reporting systems
- **Data Warehousing**: Dimensional modeling for OLAP
- **Caching Layers**: Materialized views for faster access

**Denormalization Techniques:**
1. **Calculated Fields**: Store computed values
2. **Redundant Data**: Duplicate frequently accessed data
3. **Flattened Tables**: Combine related tables
4. **Summary Tables**: Pre-aggregated data

**Trade-offs:**
```
Advantages:
✓ Improved query performance
✓ Reduced join complexity
✓ Better read performance
✓ Simplified queries

Disadvantages:
✗ Data redundancy
✗ Update anomalies
✗ Increased storage
✗ Complex maintenance
✗ Data consistency challenges
```

### Q6: Design a relational model for an e-commerce system
**Answer:**

```sql
-- Core entities
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    category_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_category_id INT,
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
);

-- Order management
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Inventory management
CREATE TABLE inventory (
    product_id INT PRIMARY KEY,
    quantity_available INT DEFAULT 0,
    reserved_quantity INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

---

## Dimensional Modeling

### Q7: Explain the star schema and its components
**Answer:**

**Star Schema**: Dimensional modeling approach with a central fact table surrounded by dimension tables.

**Components:**

**1. Fact Table (Center):**
- Contains measurable business metrics
- Foreign keys to dimension tables
- Additive, semi-additive, or non-additive measures

**2. Dimension Tables (Points of Star):**
- Descriptive attributes for analysis
- Denormalized for query performance
- Slowly Changing Dimensions (SCD) handling

```sql
-- Fact table example
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT,
    product_key INT,
    customer_key INT,
    store_key INT,
    quantity_sold INT,
    revenue DECIMAL(10,2),
    cost DECIMAL(10,2),
    profit DECIMAL(10,2),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);

-- Dimension table example
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_price DECIMAL(10,2),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);
```

### Q8: What is the difference between star schema and snowflake schema?
**Answer:**

| Aspect | Star Schema | Snowflake Schema |
|--------|-------------|------------------|
| **Structure** | Denormalized dimensions | Normalized dimensions |
| **Complexity** | Simple, flat structure | Complex, hierarchical |
| **Query Performance** | Faster (fewer joins) | Slower (more joins) |
| **Storage** | Higher (redundancy) | Lower (normalization) |
| **Maintenance** | Easier updates | Complex updates |
| **Use Case** | OLAP, reporting | Complex hierarchies |

**Star Schema Example:**
```sql
-- Single dimension table (denormalized)
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100)
);
```

**Snowflake Schema Example:**
```sql
-- Normalized dimension tables
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(255),
    subcategory_key INT,
    brand_key INT
);

CREATE TABLE dim_subcategory (
    subcategory_key INT PRIMARY KEY,
    subcategory_name VARCHAR(100),
    category_key INT
);

CREATE TABLE dim_category (
    category_key INT PRIMARY KEY,
    category_name VARCHAR(100)
);
```

### Q9: Explain Slowly Changing Dimensions (SCD) and their types
**Answer:**

**SCD**: Techniques to handle changes in dimension attributes over time.

**Type 0 - Retain Original:**
- Never change the attribute
- Used for fixed attributes like birth date

**Type 1 - Overwrite:**
- Replace old value with new value
- No history maintained
- Simple but loses historical context

```sql
-- Type 1 example
UPDATE dim_customer 
SET city = 'New York', last_updated = CURRENT_TIMESTAMP
WHERE customer_key = 123;
```

**Type 2 - Add New Record:**
- Create new record for each change
- Maintains full history
- Most common approach

```sql
-- Type 2 example
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    name VARCHAR(255),
    city VARCHAR(100),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
);

-- Insert new record for address change
INSERT INTO dim_customer VALUES 
(124, 'CUST001', 'John Doe', 'New York', '2024-01-01', '9999-12-31', TRUE);

-- Update old record
UPDATE dim_customer 
SET expiry_date = '2023-12-31', is_current = FALSE
WHERE customer_key = 123;
```

**Type 3 - Add New Attribute:**
- Add column to track previous value
- Limited history (usually one previous value)

**Type 4 - History Table:**
- Separate table for historical records
- Current table for active records

### Q10: Design a dimensional model for retail sales analytics
**Answer:**

```sql
-- Date dimension (conformed dimension)
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_week VARCHAR(10),
    day_of_month INT,
    month_name VARCHAR(10),
    month_number INT,
    quarter VARCHAR(2),
    year INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

-- Product dimension
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    brand VARCHAR(100),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
);

-- Store dimension
CREATE TABLE dim_store (
    store_key INT PRIMARY KEY,
    store_id VARCHAR(50),
    store_name VARCHAR(255),
    address VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50),
    region VARCHAR(100),
    store_type VARCHAR(50),
    opening_date DATE
);

-- Customer dimension
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    age_group VARCHAR(20),
    gender VARCHAR(10),
    city VARCHAR(100),
    state VARCHAR(50),
    customer_segment VARCHAR(50),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN
);

-- Sales fact table
CREATE TABLE fact_sales (
    sales_key BIGINT PRIMARY KEY,
    date_key INT,
    product_key INT,
    store_key INT,
    customer_key INT,
    transaction_id VARCHAR(50),
    quantity_sold INT,
    unit_price DECIMAL(10,2),
    unit_cost DECIMAL(10,2),
    gross_sales DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    net_sales DECIMAL(10,2),
    cost_of_goods DECIMAL(10,2),
    gross_profit DECIMAL(10,2),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);

-- Inventory snapshot fact table
CREATE TABLE fact_inventory (
    inventory_key BIGINT PRIMARY KEY,
    date_key INT,
    product_key INT,
    store_key INT,
    beginning_inventory INT,
    units_received INT,
    units_sold INT,
    units_adjusted INT,
    ending_inventory INT,
    inventory_value DECIMAL(10,2),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);
```

---

## Data Vault 2.0

### Q11: Explain Data Vault methodology and its core components
**Answer:**

**Data Vault 2.0**: Modeling methodology designed for enterprise data warehouses, emphasizing auditability, flexibility, and scalability.

**Core Components:**

**1. Hubs:**
- Unique business keys
- Immutable once created
- Represent core business entities

```sql
CREATE TABLE hub_customer (
    customer_hash_key CHAR(32) PRIMARY KEY,
    customer_business_key VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);
```

**2. Links:**
- Relationships between hubs
- Many-to-many associations
- Transaction records

```sql
CREATE TABLE link_customer_order (
    customer_order_hash_key CHAR(32) PRIMARY KEY,
    customer_hash_key CHAR(32) NOT NULL,
    order_hash_key CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_hash_key) REFERENCES hub_customer(customer_hash_key),
    FOREIGN KEY (order_hash_key) REFERENCES hub_order(order_hash_key)
);
```

**3. Satellites:**
- Descriptive attributes
- Historical changes
- Context and metadata

```sql
CREATE TABLE sat_customer_details (
    customer_hash_key CHAR(32),
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(500),
    hash_diff CHAR(32),
    record_source VARCHAR(50),
    PRIMARY KEY (customer_hash_key, load_date),
    FOREIGN KEY (customer_hash_key) REFERENCES hub_customer(customer_hash_key)
);
```

### Q12: What are the advantages and challenges of Data Vault modeling?
**Answer:**

**Advantages:**
- **Auditability**: Complete data lineage and history
- **Flexibility**: Easy to add new data sources
- **Parallel Loading**: Independent loading of hubs, links, satellites
- **Scalability**: Handles large volumes efficiently
- **Agility**: Supports agile development practices
- **Compliance**: Built-in audit trail for regulations

**Challenges:**
- **Complexity**: Steep learning curve
- **Performance**: More joins required for queries
- **Storage Overhead**: Redundant hash keys and metadata
- **Tooling**: Limited native tool support
- **Query Complexity**: Business users need abstraction layers

**Best Practices:**
1. Use consistent hash key generation
2. Implement proper indexing strategies
3. Create business vault views for end users
4. Automate code generation where possible
5. Establish clear naming conventions

### Q13: Design a Data Vault model for an order management system
**Answer:**

```sql
-- Hubs
CREATE TABLE hub_customer (
    customer_hash_key CHAR(32) PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

CREATE TABLE hub_product (
    product_hash_key CHAR(32) PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

CREATE TABLE hub_order (
    order_hash_key CHAR(32) PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Links
CREATE TABLE link_customer_order (
    customer_order_hash_key CHAR(32) PRIMARY KEY,
    customer_hash_key CHAR(32) NOT NULL,
    order_hash_key CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_hash_key) REFERENCES hub_customer(customer_hash_key),
    FOREIGN KEY (order_hash_key) REFERENCES hub_order(order_hash_key)
);

CREATE TABLE link_order_product (
    order_product_hash_key CHAR(32) PRIMARY KEY,
    order_hash_key CHAR(32) NOT NULL,
    product_hash_key CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    FOREIGN KEY (order_hash_key) REFERENCES hub_order(order_hash_key),
    FOREIGN KEY (product_hash_key) REFERENCES hub_product(product_hash_key)
);

-- Satellites
CREATE TABLE sat_customer_profile (
    customer_hash_key CHAR(32),
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    date_of_birth DATE,
    hash_diff CHAR(32),
    record_source VARCHAR(50),
    PRIMARY KEY (customer_hash_key, load_date),
    FOREIGN KEY (customer_hash_key) REFERENCES hub_customer(customer_hash_key)
);

CREATE TABLE sat_order_details (
    order_hash_key CHAR(32),
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    order_date DATE,
    order_status VARCHAR(50),
    total_amount DECIMAL(10,2),
    currency VARCHAR(3),
    payment_method VARCHAR(50),
    hash_diff CHAR(32),
    record_source VARCHAR(50),
    PRIMARY KEY (order_hash_key, load_date),
    FOREIGN KEY (order_hash_key) REFERENCES hub_order(order_hash_key)
);

CREATE TABLE sat_order_product_quantity (
    order_product_hash_key CHAR(32),
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    quantity INT,
    unit_price DECIMAL(10,2),
    line_total DECIMAL(10,2),
    hash_diff CHAR(32),
    record_source VARCHAR(50),
    PRIMARY KEY (order_product_hash_key, load_date),
    FOREIGN KEY (order_product_hash_key) REFERENCES link_order_product(order_product_hash_key)
);
```

---

## Activity Schema

### Q14: What is Activity Schema and when should it be used?
**Answer:**

**Activity Schema**: Event-centric data modeling approach that captures business activities as immutable events with temporal context.

**Core Principles:**
- **Immutability**: Events never change once recorded
- **Temporal Focus**: Time is a first-class citizen
- **Activity-Centric**: Models business processes as activities
- **Auditability**: Complete audit trail by design

**Key Components:**

**1. Activities Table:**
```sql
CREATE TABLE activities (
    activity_id UUID PRIMARY KEY,
    activity_ts TIMESTAMP NOT NULL,
    activity VARCHAR(100) NOT NULL,
    feature_json JSONB,
    entity VARCHAR(100),
    entity_id VARCHAR(100),
    link VARCHAR(100),
    link_id VARCHAR(100)
);
```

**2. Entities Table:**
```sql
CREATE TABLE entities (
    entity VARCHAR(100),
    entity_id VARCHAR(100),
    ts TIMESTAMP,
    feature_json JSONB,
    PRIMARY KEY (entity, entity_id, ts)
);
```

**When to Use Activity Schema:**
- **Event-Driven Systems**: Natural fit for event sourcing
- **Audit Requirements**: Complete traceability needed
- **Temporal Analysis**: Time-based analytics are critical
- **Regulatory Compliance**: Immutable audit trails required
- **Real-time Analytics**: Stream processing scenarios

### Q15: Compare Activity Schema with traditional dimensional modeling
**Answer:**

| Aspect | Activity Schema | Dimensional Modeling |
|--------|-----------------|---------------------|
| **Data Structure** | Event-centric, temporal | Entity-centric, snapshot |
| **Immutability** | Immutable events | Mutable dimensions |
| **Time Handling** | Native temporal support | SCD patterns |
| **Schema Evolution** | Flexible JSON attributes | Schema changes required |
| **Query Patterns** | Temporal aggregations | Cross-dimensional analysis |
| **Storage** | Higher (all events stored) | Lower (current state focus) |
| **Complexity** | Simple structure, complex queries | Complex structure, simple queries |
| **Use Case** | Event analysis, audit trails | Business intelligence, reporting |

**Activity Schema Example:**
```sql
-- Customer registration activity
INSERT INTO activities VALUES (
    gen_random_uuid(),
    '2024-01-15 10:30:00',
    'customer_registered',
    '{"email": "john@example.com", "source": "website"}',
    'customer',
    'CUST001',
    NULL,
    NULL
);

-- Order placement activity
INSERT INTO activities VALUES (
    gen_random_uuid(),
    '2024-01-15 14:20:00',
    'order_placed',
    '{"amount": 150.00, "items": 3, "payment_method": "credit_card"}',
    'order',
    'ORD001',
    'customer',
    'CUST001'
);
```

### Q16: Design an Activity Schema for an e-commerce platform
**Answer:**

```sql
-- Core activities table
CREATE TABLE activities (
    activity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_ts TIMESTAMP NOT NULL,
    activity VARCHAR(100) NOT NULL,
    feature_json JSONB,
    entity VARCHAR(100),
    entity_id VARCHAR(100),
    link VARCHAR(100),
    link_id VARCHAR(100),
    session_id VARCHAR(100),
    user_agent TEXT,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Entities snapshot table
CREATE TABLE entities (
    entity VARCHAR(100),
    entity_id VARCHAR(100),
    ts TIMESTAMP,
    feature_json JSONB,
    PRIMARY KEY (entity, entity_id, ts)
);

-- Activity types and their schemas
CREATE TABLE activity_schemas (
    activity VARCHAR(100) PRIMARY KEY,
    schema_version VARCHAR(10),
    json_schema JSONB,
    description TEXT
);

-- Sample activity types
INSERT INTO activity_schemas VALUES
('customer_registered', '1.0', 
 '{"type": "object", "properties": {"email": {"type": "string"}, "source": {"type": "string"}}}',
 'Customer registration event'),
('product_viewed', '1.0',
 '{"type": "object", "properties": {"product_id": {"type": "string"}, "category": {"type": "string"}, "price": {"type": "number"}}}',
 'Product page view event'),
('cart_item_added', '1.0',
 '{"type": "object", "properties": {"product_id": {"type": "string"}, "quantity": {"type": "integer"}, "price": {"type": "number"}}}',
 'Item added to cart event'),
('order_placed', '1.0',
 '{"type": "object", "properties": {"total_amount": {"type": "number"}, "item_count": {"type": "integer"}, "payment_method": {"type": "string"}}}',
 'Order placement event');

-- Indexes for performance
CREATE INDEX idx_activities_ts ON activities(activity_ts);
CREATE INDEX idx_activities_entity ON activities(entity, entity_id);
CREATE INDEX idx_activities_activity ON activities(activity);
CREATE INDEX idx_activities_link ON activities(link, link_id);

-- Sample data insertion
INSERT INTO activities (activity_ts, activity, feature_json, entity, entity_id, session_id) VALUES
('2024-01-15 10:30:00', 'customer_registered', 
 '{"email": "john@example.com", "source": "website", "marketing_consent": true}',
 'customer', 'CUST001', 'sess_123'),
 
('2024-01-15 10:35:00', 'product_viewed',
 '{"product_id": "PROD001", "category": "electronics", "price": 299.99, "brand": "TechCorp"}',
 'product', 'PROD001', 'sess_123'),
 
('2024-01-15 10:37:00', 'cart_item_added',
 '{"product_id": "PROD001", "quantity": 1, "price": 299.99}',
 'cart', 'CART001', 'sess_123');

-- Analytical queries
-- Customer journey analysis
SELECT 
    entity_id as customer_id,
    activity,
    activity_ts,
    feature_json,
    LAG(activity_ts) OVER (PARTITION BY entity_id ORDER BY activity_ts) as prev_activity_ts
FROM activities 
WHERE entity = 'customer' 
    AND entity_id = 'CUST001'
ORDER BY activity_ts;

-- Conversion funnel analysis
WITH funnel_steps AS (
    SELECT 
        session_id,
        COUNT(CASE WHEN activity = 'product_viewed' THEN 1 END) as views,
        COUNT(CASE WHEN activity = 'cart_item_added' THEN 1 END) as cart_adds,
        COUNT(CASE WHEN activity = 'order_placed' THEN 1 END) as orders
    FROM activities
    WHERE activity_ts >= '2024-01-01'
    GROUP BY session_id
)
SELECT 
    COUNT(*) as total_sessions,
    COUNT(CASE WHEN views > 0 THEN 1 END) as sessions_with_views,
    COUNT(CASE WHEN cart_adds > 0 THEN 1 END) as sessions_with_cart_adds,
    COUNT(CASE WHEN orders > 0 THEN 1 END) as sessions_with_orders,
    ROUND(COUNT(CASE WHEN cart_adds > 0 THEN 1 END)::DECIMAL / COUNT(CASE WHEN views > 0 THEN 1 END) * 100, 2) as view_to_cart_rate,
    ROUND(COUNT(CASE WHEN orders > 0 THEN 1 END)::DECIMAL / COUNT(CASE WHEN cart_adds > 0 THEN 1 END) * 100, 2) as cart_to_order_rate
FROM funnel_steps;
```

---

## NoSQL Data Modeling

### Q17: How does data modeling differ in NoSQL databases?
**Answer:**

**Key Differences:**

| Aspect | Relational | NoSQL |
|--------|------------|-------|
| **Schema** | Fixed, predefined | Flexible, dynamic |
| **Normalization** | Highly normalized | Denormalized |
| **Relationships** | Foreign keys, joins | Embedded documents, references |
| **Query Patterns** | Query-agnostic design | Query-driven design |
| **Consistency** | ACID transactions | Eventual consistency |
| **Scalability** | Vertical scaling | Horizontal scaling |

**NoSQL Modeling Principles:**
1. **Denormalization**: Embed related data together
2. **Query-Driven Design**: Model based on access patterns
3. **Atomic Operations**: Design for single-document transactions
4. **Indexing Strategy**: Plan indexes for query performance

**Document Database Example (MongoDB):**
```javascript
// Embedded approach - order with items
{
  "_id": ObjectId("..."),
  "order_id": "ORD001",
  "customer": {
    "customer_id": "CUST001",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "items": [
    {
      "product_id": "PROD001",
      "name": "Laptop",
      "quantity": 1,
      "price": 999.99
    },
    {
      "product_id": "PROD002", 
      "name": "Mouse",
      "quantity": 2,
      "price": 29.99
    }
  ],
  "total_amount": 1059.97,
  "order_date": ISODate("2024-01-15"),
  "status": "shipped"
}
```

### Q18: Design a data model for a social media platform using MongoDB
**Answer:**

```javascript
// Users collection
{
  "_id": ObjectId("..."),
  "username": "johndoe",
  "email": "john@example.com",
  "profile": {
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Software engineer passionate about technology",
    "avatar_url": "https://example.com/avatars/johndoe.jpg",
    "location": "San Francisco, CA",
    "website": "https://johndoe.dev"
  },
  "stats": {
    "followers_count": 1250,
    "following_count": 890,
    "posts_count": 156
  },
  "settings": {
    "privacy": "public",
    "notifications": {
      "email": true,
      "push": false
    }
  },
  "created_at": ISODate("2023-01-15"),
  "last_active": ISODate("2024-01-15")
}

// Posts collection
{
  "_id": ObjectId("..."),
  "user_id": ObjectId("..."),
  "username": "johndoe", // Denormalized for query performance
  "content": {
    "text": "Just deployed my new app! 🚀 #coding #javascript",
    "media": [
      {
        "type": "image",
        "url": "https://example.com/media/post123.jpg",
        "alt_text": "Screenshot of application dashboard"
      }
    ],
    "hashtags": ["coding", "javascript"],
    "mentions": ["@janedoe"]
  },
  "engagement": {
    "likes_count": 45,
    "comments_count": 12,
    "shares_count": 8
  },
  "visibility": "public",
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}

// Comments collection (separate for scalability)
{
  "_id": ObjectId("..."),
  "post_id": ObjectId("..."),
  "user_id": ObjectId("..."),
  "username": "janedoe",
  "content": "Great work! The UI looks amazing 👏",
  "parent_comment_id": null, // For nested comments
  "likes_count": 5,
  "created_at": ISODate("2024-01-15T11:00:00Z")
}

// Followers collection (for relationships)
{
  "_id": ObjectId("..."),
  "follower_id": ObjectId("..."),
  "following_id": ObjectId("..."),
  "created_at": ISODate("2024-01-10")
}

// User timeline/feed (materialized view approach)
{
  "_id": ObjectId("..."),
  "user_id": ObjectId("..."),
  "posts": [
    {
      "post_id": ObjectId("..."),
      "user_id": ObjectId("..."),
      "username": "janedoe",
      "content_preview": "Just finished reading an amazing book...",
      "created_at": ISODate("2024-01-15T09:00:00Z"),
      "engagement": {
        "likes_count": 23,
        "comments_count": 5
      }
    }
  ],
  "last_updated": ISODate("2024-01-15T12:00:00Z")
}

// Indexes for performance
db.users.createIndex({"username": 1}, {"unique": true})
db.users.createIndex({"email": 1}, {"unique": true})
db.posts.createIndex({"user_id": 1, "created_at": -1})
db.posts.createIndex({"content.hashtags": 1})
db.comments.createIndex({"post_id": 1, "created_at": 1})
db.followers.createIndex({"follower_id": 1})
db.followers.createIndex({"following_id": 1})
```

---

## Modern Approaches

### Q19: What is Data Mesh and how does it impact data modeling?
**Answer:**

**Data Mesh**: Decentralized data architecture that treats data as a product, with domain-oriented ownership and federated governance.

**Core Principles:**
1. **Domain-oriented decentralized data ownership**
2. **Data as a product**
3. **Self-serve data infrastructure as a platform**
4. **Federated computational governance**

**Impact on Data Modeling:**

**Domain-Driven Models:**
```sql
-- Sales domain model
CREATE SCHEMA sales_domain;

CREATE TABLE sales_domain.customer_product (
    domain_id VARCHAR(100) PRIMARY KEY,
    customer_global_id VARCHAR(100),
    product_global_id VARCHAR(100),
    purchase_date DATE,
    quantity INT,
    revenue DECIMAL(10,2),
    -- Domain-specific attributes
    sales_channel VARCHAR(50),
    discount_applied DECIMAL(5,2),
    sales_rep_id VARCHAR(50)
);

-- Marketing domain model  
CREATE SCHEMA marketing_domain;

CREATE TABLE marketing_domain.customer_engagement (
    domain_id VARCHAR(100) PRIMARY KEY,
    customer_global_id VARCHAR(100),
    campaign_id VARCHAR(100),
    engagement_date DATE,
    engagement_type VARCHAR(50),
    -- Domain-specific attributes
    channel VARCHAR(50),
    content_id VARCHAR(100),
    conversion_value DECIMAL(10,2)
);
```

**Data Product Specifications:**
```yaml
# Data product contract
apiVersion: v1
kind: DataProduct
metadata:
  name: customer-purchase-behavior
  domain: sales
spec:
  owner: sales-team@company.com
  description: Customer purchase patterns and behavior analytics
  schema:
    format: parquet
    location: s3://data-mesh/sales/customer-purchase-behavior/
    fields:
      - name: customer_id
        type: string
        description: Global customer identifier
      - name: purchase_date
        type: date
        description: Date of purchase
      - name: product_category
        type: string
        description: Product category
  sla:
    freshness: 24h
    availability: 99.9%
    quality_score: 95%
```

### Q20: How do you handle schema evolution in modern data systems?
**Answer:**

**Schema Evolution Strategies:**

**1. Backward Compatibility:**
- Add optional fields only
- Never remove or rename fields
- Use default values for new fields

```json
// Version 1
{
  "customer_id": "CUST001",
  "name": "John Doe",
  "email": "john@example.com"
}

// Version 2 (backward compatible)
{
  "customer_id": "CUST001", 
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",  // New optional field
  "preferences": {          // New nested object
    "newsletter": true
  }
}
```

**2. Forward Compatibility:**
- Ignore unknown fields
- Use schema registries
- Version-aware consumers

**3. Schema Registry Approach:**
```python
# Avro schema evolution example
from confluent_kafka import avro

# Schema v1
schema_v1 = """
{
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"}
  ]
}
"""

# Schema v2 (with default values)
schema_v2 = """
{
  "type": "record", 
  "name": "Customer",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "phone", "type": ["null", "string"], "default": null},
    {"name": "created_at", "type": "long", "default": 0}
  ]
}
"""
```

**4. Data Lake Schema Evolution:**
```sql
-- Partition-based evolution
CREATE TABLE customer_data (
    customer_id STRING,
    name STRING,
    email STRING,
    phone STRING,
    created_at TIMESTAMP
)
PARTITIONED BY (
    schema_version STRING,
    year INT,
    month INT
);

-- Query across schema versions
SELECT 
    customer_id,
    name,
    email,
    CASE 
        WHEN schema_version >= '2.0' THEN phone 
        ELSE NULL 
    END as phone
FROM customer_data
WHERE year = 2024;
```

---

## Performance & Optimization

### Q21: How do you optimize data models for query performance?
**Answer:**

**Optimization Strategies:**

**1. Indexing Strategy:**
```sql
-- Composite indexes for common query patterns
CREATE INDEX idx_sales_date_customer ON sales(sale_date, customer_id);
CREATE INDEX idx_product_category_price ON products(category, price DESC);

-- Partial indexes for filtered queries
CREATE INDEX idx_active_customers ON customers(customer_id) 
WHERE status = 'active';

-- Covering indexes to avoid table lookups
CREATE INDEX idx_order_summary ON orders(customer_id, order_date) 
INCLUDE (total_amount, status);
```

**2. Partitioning:**
```sql
-- Range partitioning by date
CREATE TABLE sales_2024 (
    sale_id BIGINT,
    sale_date DATE,
    customer_id INT,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2024_q1 PARTITION OF sales_2024
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

-- Hash partitioning for even distribution
CREATE TABLE customer_data (
    customer_id INT,
    name VARCHAR(255),
    email VARCHAR(255)
) PARTITION BY HASH (customer_id);
```

**3. Denormalization for Read Performance:**
```sql
-- Materialized view for complex aggregations
CREATE MATERIALIZED VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    MAX(o.order_date) as last_order_date,
    AVG(o.total_amount) as avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email;

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY customer_summary;
```

**4. Column Store Optimization:**
```sql
-- Columnar storage for analytics
CREATE TABLE sales_analytics (
    sale_date DATE,
    product_id INT,
    category VARCHAR(50),
    quantity INT,
    revenue DECIMAL(10,2)
) WITH (orientation = column);

-- Compression for better performance
ALTER TABLE sales_analytics SET (compression = 'lz4');
```

### Q22: Design a data model that handles both OLTP and OLAP workloads
**Answer:**

**Hybrid HTAP (Hybrid Transactional/Analytical Processing) Design:**

**1. Operational Layer (OLTP):**
```sql
-- Normalized tables for transactional integrity
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Indexes optimized for OLTP
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
```

**2. Analytical Layer (OLAP):**
```sql
-- Denormalized tables for analytical queries
CREATE TABLE fact_sales_summary (
    date_key DATE,
    customer_id INT,
    product_id INT,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    quantity_sold INT,
    revenue DECIMAL(10,2),
    cost DECIMAL(10,2),
    profit DECIMAL(10,2)
) PARTITION BY RANGE (date_key);

-- Columnar indexes for analytics
CREATE INDEX idx_sales_summary_date_category ON fact_sales_summary 
USING BRIN (date_key, category);

-- Aggregated tables for fast reporting
CREATE TABLE daily_sales_summary (
    summary_date DATE PRIMARY KEY,
    total_orders INT,
    total_revenue DECIMAL(12,2),
    total_customers INT,
    avg_order_value DECIMAL(10,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**3. Real-time Synchronization:**
```sql
-- CDC (Change Data Capture) triggers
CREATE OR REPLACE FUNCTION sync_to_analytics()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert into analytical layer
    INSERT INTO fact_sales_summary (
        date_key, customer_id, product_id, 
        quantity_sold, revenue
    )
    SELECT 
        DATE(o.order_date),
        o.customer_id,
        oi.product_id,
        oi.quantity,
        oi.quantity * oi.unit_price
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_id = NEW.order_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_sync_analytics
    AFTER INSERT ON orders
    FOR EACH ROW
    EXECUTE FUNCTION sync_to_analytics();
```

**4. Query Routing Strategy:**
```python
class QueryRouter:
    def route_query(self, query_type, query_pattern):
        if query_type == 'transactional':
            # Route to OLTP optimized tables
            return self.oltp_connection
        elif query_type == 'analytical':
            # Route to OLAP optimized tables/views
            return self.olap_connection
        elif 'real_time' in query_pattern:
            # Route to hybrid views
            return self.hybrid_connection
        else:
            return self.default_connection

# Usage example
router = QueryRouter()

# Transactional query
conn = router.route_query('transactional', 'INSERT INTO orders...')

# Analytical query  
conn = router.route_query('analytical', 'SELECT SUM(revenue) FROM fact_sales...')
```

---

## Real-World Scenarios

### Q23: You need to migrate from a monolithic database to microservices. How do you approach data modeling?
**Answer:**

**Migration Strategy:**

**1. Domain Decomposition:**
```sql
-- Original monolithic schema
CREATE TABLE customers (customer_id, name, email, address, phone);
CREATE TABLE orders (order_id, customer_id, product_id, quantity, price);
CREATE TABLE products (product_id, name, category, price, inventory);
CREATE TABLE payments (payment_id, order_id, amount, method, status);

-- Decomposed microservice schemas

-- Customer Service
CREATE SCHEMA customer_service;
CREATE TABLE customer_service.customers (
    customer_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    profile JSONB,
    created_at TIMESTAMP,
    version INT
);

-- Order Service  
CREATE SCHEMA order_service;
CREATE TABLE order_service.orders (
    order_id UUID PRIMARY KEY,
    customer_id UUID, -- Reference to customer service
    order_data JSONB,
    status VARCHAR(50),
    created_at TIMESTAMP,
    version INT
);

-- Product Service
CREATE SCHEMA product_service;
CREATE TABLE product_service.products (
    product_id UUID PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10,2),
    inventory_count INT,
    version INT
);

-- Payment Service
CREATE SCHEMA payment_service;
CREATE TABLE payment_service.payments (
    payment_id UUID PRIMARY KEY,
    order_id UUID, -- Reference to order service
    amount DECIMAL(10,2),
    method VARCHAR(50),
    status VARCHAR(50),
    processed_at TIMESTAMP
);
```

**2. Data Consistency Patterns:**
```python
# Saga pattern for distributed transactions
class OrderSaga:
    def __init__(self):
        self.steps = []
        
    def create_order(self, order_data):
        # Step 1: Reserve inventory
        inventory_result = self.product_service.reserve_inventory(
            order_data['product_id'], 
            order_data['quantity']
        )
        
        if not inventory_result.success:
            return self.handle_failure("inventory_reservation_failed")
            
        # Step 2: Create order
        order_result = self.order_service.create_order(order_data)
        
        if not order_result.success:
            # Compensate: Release inventory
            self.product_service.release_inventory(
                order_data['product_id'], 
                order_data['quantity']
            )
            return self.handle_failure("order_creation_failed")
            
        # Step 3: Process payment
        payment_result = self.payment_service.process_payment(
            order_result.order_id,
            order_data['amount']
        )
        
        if not payment_result.success:
            # Compensate: Cancel order and release inventory
            self.order_service.cancel_order(order_result.order_id)
            self.product_service.release_inventory(
                order_data['product_id'], 
                order_data['quantity']
            )
            return self.handle_failure("payment_failed")
            
        return {"success": True, "order_id": order_result.order_id}
```

**3. Event-Driven Data Synchronization:**
```python
# Event sourcing for cross-service data consistency
class OrderEventHandler:
    def handle_order_created(self, event):
        # Update customer service with order count
        self.customer_service.update_order_count(
            event.customer_id, 
            increment=1
        )
        
        # Update product service with sales data
        self.product_service.record_sale(
            event.product_id,
            event.quantity
        )
        
    def handle_payment_completed(self, event):
        # Update order status
        self.order_service.update_status(
            event.order_id,
            "paid"
        )
        
        # Update customer lifetime value
        self.customer_service.update_lifetime_value(
            event.customer_id,
            event.amount
        )
```

### Q24: Design a data model for a real-time recommendation system
**Answer:**

**Multi-Layer Architecture:**

**1. User Profile Store:**
```sql
-- User preferences and behavior
CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY,
    demographics JSONB,
    preferences JSONB,
    behavior_summary JSONB,
    last_updated TIMESTAMP
);

-- Example user profile
INSERT INTO user_profiles VALUES (
    'user123',
    '{"age_group": "25-34", "location": "SF", "gender": "M"}',
    '{"categories": ["electronics", "books"], "brands": ["apple", "nike"]}',
    '{"avg_session_duration": 1200, "purchase_frequency": "weekly", "price_sensitivity": "medium"}',
    CURRENT_TIMESTAMP
);
```

**2. Item Features Store:**
```sql
-- Product/content features
CREATE TABLE item_features (
    item_id UUID PRIMARY KEY,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    features JSONB,
    popularity_score DECIMAL(5,2),
    last_updated TIMESTAMP
);

-- Example item features
INSERT INTO item_features VALUES (
    'item456',
    'electronics',
    'smartphones',
    '{"brand": "apple", "price_range": "high", "features": ["5G", "camera", "wireless_charging"]}',
    8.5,
    CURRENT_TIMESTAMP
);
```

**3. Interaction Events (Stream Processing):**
```python
# Kafka event schema
interaction_event_schema = {
    "user_id": "string",
    "item_id": "string", 
    "interaction_type": "string",  # view, click, purchase, rating
    "timestamp": "long",
    "context": {
        "session_id": "string",
        "device": "string",
        "location": "string"
    },
    "metadata": "object"  # flexible additional data
}

# Real-time feature extraction
class FeatureExtractor:
    def extract_user_features(self, user_id, time_window='1h'):
        # Recent interactions
        recent_interactions = self.get_recent_interactions(user_id, time_window)
        
        # Calculate features
        features = {
            'categories_viewed': self.extract_categories(recent_interactions),
            'avg_price_range': self.calculate_avg_price(recent_interactions),
            'session_duration': self.calculate_session_duration(recent_interactions),
            'interaction_velocity': len(recent_interactions) / 3600  # per hour
        }
        
        return features
```

**4. Real-time Scoring Store:**
```python
# Redis for real-time recommendations
import redis
import json

class RecommendationCache:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    def store_recommendations(self, user_id, recommendations, ttl=3600):
        """Store pre-computed recommendations with TTL"""
        key = f"rec:{user_id}"
        value = json.dumps({
            'recommendations': recommendations,
            'generated_at': time.time(),
            'model_version': '1.2.3'
        })
        self.redis_client.setex(key, ttl, value)
        
    def get_recommendations(self, user_id):
        """Get cached recommendations"""
        key = f"rec:{user_id}"
        cached = self.redis_client.get(key)
        if cached:
            return json.loads(cached)
        return None
        
    def store_user_embedding(self, user_id, embedding):
        """Store user embedding vector"""
        key = f"emb:user:{user_id}"
        # Store as binary for efficiency
        self.redis_client.set(key, embedding.tobytes())
```

**5. Feature Store Integration:**
```python
# Feature store for ML model features
class FeatureStore:
    def __init__(self):
        self.online_store = redis.Redis()  # Low latency
        self.offline_store = self.connect_to_warehouse()  # Historical data
        
    def get_user_features(self, user_id, feature_names):
        """Get real-time user features"""
        features = {}
        for feature_name in feature_names:
            key = f"feature:user:{user_id}:{feature_name}"
            value = self.online_store.get(key)
            if value:
                features[feature_name] = json.loads(value)
        return features
        
    def get_item_features(self, item_id, feature_names):
        """Get item features"""
        features = {}
        for feature_name in feature_names:
            key = f"feature:item:{item_id}:{feature_name}"
            value = self.online_store.get(key)
            if value:
                features[feature_name] = json.loads(value)
        return features
        
    def update_features_batch(self, feature_updates):
        """Batch update features from streaming pipeline"""
        pipe = self.online_store.pipeline()
        for update in feature_updates:
            key = f"feature:{update['entity_type']}:{update['entity_id']}:{update['feature_name']}"
            pipe.setex(key, 3600, json.dumps(update['value']))
        pipe.execute()
```

**6. A/B Testing Data Model:**
```sql
-- Experiment tracking
CREATE TABLE recommendation_experiments (
    experiment_id UUID PRIMARY KEY,
    user_id UUID,
    variant VARCHAR(50),
    recommendations JSONB,
    timestamp TIMESTAMP,
    context JSONB
);

-- Performance metrics
CREATE TABLE recommendation_metrics (
    metric_id UUID PRIMARY KEY,
    experiment_id UUID,
    user_id UUID,
    item_id UUID,
    interaction_type VARCHAR(50),
    timestamp TIMESTAMP,
    value DECIMAL(10,4),
    FOREIGN KEY (experiment_id) REFERENCES recommendation_experiments(experiment_id)
);
```

This comprehensive data modeling approach supports:
- **Real-time inference** with cached recommendations
- **Feature engineering** with online/offline feature stores  
- **Model training** with historical interaction data
- **A/B testing** with experiment tracking
- **Scalability** through distributed caching and streaming
- **Flexibility** with JSON storage for evolving features

---

## 🎯 Key Takeaways

### Data Modeling Best Practices:
1. **Understand Requirements**: Query patterns drive design decisions
2. **Choose Right Approach**: Match modeling technique to use case
3. **Plan for Evolution**: Design for change and growth
4. **Optimize Performance**: Balance normalization with query needs
5. **Ensure Data Quality**: Implement proper constraints and validation
6. **Document Everything**: Maintain clear documentation and metadata
7. **Test Thoroughly**: Validate design with realistic data volumes

### Modern Considerations:
- **Cloud-Native**: Design for distributed, scalable architectures
- **Real-Time**: Support streaming and low-latency requirements  
- **Multi-Model**: Combine different approaches as needed
- **Data Governance**: Implement proper lineage and compliance
- **Cost Optimization**: Consider storage and compute costs
- **Developer Experience**: Make models intuitive and maintainable