# Data Modeling Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [Conceptual Data Modeling](#conceptual-data-modeling)
   - [Logical Data Modeling](#logical-data-modeling)
   - [Physical Data Modeling](#physical-data-modeling)
3. [Data Modeling Architecture](#-data-modeling-architecture)
4. [Relational Data Modeling](#-relational-data-modeling)
5. [Dimensional Modeling](#-dimensional-modeling)
6. [NoSQL Data Modeling](#-nosql-data-modeling)
7. [Data Vault Modeling](#-data-vault-modeling)
8. [Performance Optimization](#-performance-optimization)
9. [Best Practices](#-best-practices)
10. [When to Use Different Approaches](#-when-to-use-different-approaches)
11. [Interview Focus Areas](#-interview-focus-areas)
12. [Quick References](#-quick-references)

---

## 🎯 Overview

Data modeling is the process of creating a conceptual representation of data structures and their relationships within a system. It serves as a blueprint for database design, data architecture, and system implementation, ensuring data consistency, integrity, and optimal performance.

**Key Benefits:**
- **Communication**: Provides common language between business and technical teams
- **Data Quality**: Ensures consistency and integrity through defined relationships
- **Performance**: Optimizes query performance through proper structure design
- **Maintenance**: Simplifies system maintenance and evolution
- **Compliance**: Supports regulatory requirements and data governance

## 📦 Core Components

### 1. Data Modeling Levels

#### Conceptual Data Modeling
**Definition**: High-level business view focusing on entities, relationships, and business rules without implementation details.

**Key Characteristics**:
- **Business-focused**: Uses business terminology and concepts
- **Technology-agnostic**: Independent of specific database or platform
- **High-level**: Shows major entities and relationships
- **Stakeholder communication**: Facilitates business-IT alignment

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CONCEPTUAL DATA MODEL                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐                    ┌─────────────┐                            │
│  │  CUSTOMER   │                    │   ORDER     │                            │
│  │             │                    │             │                            │
│  │ • Name      │◄──────────────────►│ • Date      │                            │
│  │ • Email     │    places          │ • Total     │                            │
│  │ • Phone     │                    │ • Status    │                            │
│  └─────────────┘                    └─────────────┘                            │
│         │                                   │                                  │
│         │ has                               │ contains                         │
│         ▼                                   ▼                                  │
│  ┌─────────────┐                    ┌─────────────┐                            │
│  │   ADDRESS   │                    │ ORDER_ITEM  │                            │
│  │             │                    │             │                            │
│  │ • Street    │                    │ • Quantity  │                            │
│  │ • City      │                    │ • Price     │                            │
│  │ • Country   │                    │             │                            │
│  └─────────────┘                    └─────────────┘                            │
│                                             │                                  │
│                                             │ references                       │
│                                             ▼                                  │
│                                      ┌─────────────┐                            │
│                                      │   PRODUCT   │                            │
│                                      │             │                            │
│                                      │ • Name      │                            │
│                                      │ • Price     │                            │
│                                      │ • Category  │                            │
│                                      └─────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Logical Data Modeling
**Definition**: Detailed structure with attributes, data types, and relationships, but still independent of specific technology.

**Key Features**:
- **Detailed attributes**: All entity attributes with data types
- **Relationships**: Primary and foreign key relationships
- **Constraints**: Business rules and data validation
- **Normalization**: Proper normalization levels applied

```sql
-- Logical model representation
ENTITY Customer {
    customer_id: INTEGER (Primary Key)
    first_name: VARCHAR(50) NOT NULL
    last_name: VARCHAR(50) NOT NULL
    email: VARCHAR(100) UNIQUE NOT NULL
    phone: VARCHAR(20)
    created_date: DATE NOT NULL
}

ENTITY Order {
    order_id: INTEGER (Primary Key)
    customer_id: INTEGER (Foreign Key -> Customer.customer_id)
    order_date: DATE NOT NULL
    total_amount: DECIMAL(10,2) NOT NULL
    status: VARCHAR(20) DEFAULT 'pending'
}

RELATIONSHIP Customer_Order {
    Customer (1) ──── (0..*) Order
    "A customer can place zero or many orders"
}
```

#### Physical Data Modeling
**Definition**: Implementation-specific design with indexes, partitions, storage details, and performance optimizations.

**Implementation Details**:
- **Storage structures**: Tables, indexes, partitions
- **Performance tuning**: Query optimization, caching strategies
- **Security**: Access controls, encryption
- **Platform-specific**: Database-specific features and constraints

```sql
-- Physical model implementation
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_created_date ON customers(created_date);

-- Partitioning for large tables
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE orders_2023 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### 2. Data Modeling Approaches

#### Entity-Relationship (ER) Modeling
**Definition**: Traditional approach focusing on entities, attributes, and relationships.

**Components**:
- **Entities**: Objects or concepts (Customer, Order, Product)
- **Attributes**: Properties of entities (name, price, date)
- **Relationships**: Associations between entities (Customer places Order)

#### Object-Oriented Modeling
**Definition**: Models data as objects with properties and methods.

**Features**:
- **Inheritance**: Objects can inherit from parent objects
- **Encapsulation**: Data and methods bundled together
- **Polymorphism**: Objects can take multiple forms

#### Graph Data Modeling
**Definition**: Represents data as nodes and edges in a graph structure.

**Use Cases**:
- **Social networks**: Users and connections
- **Recommendation engines**: Products and relationships
- **Fraud detection**: Transaction patterns and anomalies

## 🏗️ Data Modeling Architecture

### Architecture Patterns

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        DATA MODELING ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           BUSINESS LAYER                                    │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │ Business    │  │ Data        │  │ Process     │  │ Governance  │       │ │
│  │  │ Rules       │  │ Definitions │  │ Flows       │  │ Policies    │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                        │
│                                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         CONCEPTUAL LAYER                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │ Entity      │  │ Relationship│  │ Business    │  │ Data        │       │ │
│  │  │ Definitions │  │ Mapping     │  │ Context     │  │ Lineage     │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                        │
│                                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                          LOGICAL LAYER                                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │ Normalized  │  │ Data Types  │  │ Constraints │  │ Referential │       │ │
│  │  │ Structures  │  │ & Domains   │  │ & Rules     │  │ Integrity   │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                        │
│                                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         PHYSICAL LAYER                                     │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │ Storage     │  │ Indexes &   │  │ Partitioning│  │ Security &  │       │ │
│  │  │ Structures  │  │ Performance │  │ & Sharding  │  │ Access      │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🗄️ Relational Data Modeling

### Normalization Process

#### First Normal Form (1NF)
**Rules**:
- Each column contains atomic values
- No repeating groups
- Each row is unique

```sql
-- Violates 1NF (multiple values in one column)
CREATE TABLE customers_bad (
    id INTEGER,
    name VARCHAR(100),
    phones VARCHAR(200) -- "123-456-7890, 098-765-4321"
);

-- Follows 1NF
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE customer_phones (
    customer_id INTEGER,
    phone VARCHAR(20),
    phone_type VARCHAR(10), -- 'mobile', 'home', 'work'
    PRIMARY KEY (customer_id, phone),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

#### Second Normal Form (2NF)
**Rules**:
- Must be in 1NF
- No partial dependencies on composite primary keys

```sql
-- Violates 2NF (partial dependency)
CREATE TABLE order_items_bad (
    order_id INTEGER,
    product_id INTEGER,
    product_name VARCHAR(100), -- Depends only on product_id
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_id)
);

-- Follows 2NF
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    unit_price DECIMAL(10,2)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

#### Third Normal Form (3NF)
**Rules**:
- Must be in 2NF
- No transitive dependencies

```sql
-- Violates 3NF (transitive dependency)
CREATE TABLE employees_bad (
    employee_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    department_id INTEGER,
    department_name VARCHAR(100), -- Depends on department_id, not employee_id
    salary DECIMAL(10,2)
);

-- Follows 3NF
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    department_id INTEGER,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
```

### Denormalization Strategies

**When to Denormalize**:
- **Performance Requirements**: Frequent complex joins causing slow queries
- **Read-Heavy Workloads**: Analytics and reporting systems
- **Data Warehousing**: Dimensional modeling for OLAP
- **Caching Layers**: Materialized views for faster access

```sql
-- Denormalized table for reporting
CREATE TABLE sales_summary (
    sale_id INTEGER PRIMARY KEY,
    sale_date DATE,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    product_name VARCHAR(100),
    category_name VARCHAR(100),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    -- Calculated fields
    discount_amount DECIMAL(10,2),
    profit_margin DECIMAL(5,2)
);

-- Materialized view for performance
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    category_name,
    COUNT(*) as transaction_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_transaction_value
FROM sales_summary
GROUP BY DATE_TRUNC('month', sale_date), category_name;
```

## 📊 Dimensional Modeling

### Star Schema Design

**Definition**: Central fact table surrounded by dimension tables, resembling a star.

```sql
-- Fact table (center of star)
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INTEGER,
    product_key INTEGER,
    customer_key INTEGER,
    store_key INTEGER,
    -- Measures (additive)
    quantity_sold INTEGER,
    revenue DECIMAL(12,2),
    cost DECIMAL(12,2),
    profit DECIMAL(12,2),
    -- Foreign keys to dimensions
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);

-- Dimension tables (points of star)
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    day_of_week VARCHAR(10),
    day_of_month INTEGER,
    month_name VARCHAR(10),
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_price DECIMAL(10,2),
    -- SCD Type 2 fields
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(255),
    customer_type VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    age_group VARCHAR(20),
    income_bracket VARCHAR(20)
);
```

### Snowflake Schema Design

**Definition**: Normalized version of star schema where dimension tables are further normalized.

```sql
-- Normalized dimension tables
CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    subcategory_key INTEGER,
    brand_key INTEGER,
    FOREIGN KEY (subcategory_key) REFERENCES dim_subcategory(subcategory_key),
    FOREIGN KEY (brand_key) REFERENCES dim_brand(brand_key)
);

CREATE TABLE dim_subcategory (
    subcategory_key INTEGER PRIMARY KEY,
    subcategory_name VARCHAR(100),
    category_key INTEGER,
    FOREIGN KEY (category_key) REFERENCES dim_category(category_key)
);

CREATE TABLE dim_category (
    category_key INTEGER PRIMARY KEY,
    category_name VARCHAR(100)
);

CREATE TABLE dim_brand (
    brand_key INTEGER PRIMARY KEY,
    brand_name VARCHAR(100),
    brand_country VARCHAR(100)
);
```

### Slowly Changing Dimensions (SCD)

#### SCD Type 1 - Overwrite
```sql
-- Simply update the record
UPDATE dim_customer 
SET customer_name = 'John Smith Jr.',
    city = 'New York'
WHERE customer_id = 'CUST001';
```

#### SCD Type 2 - Historical Tracking
```sql
-- Add SCD Type 2 fields
CREATE TABLE dim_customer_scd2 (
    customer_key INTEGER PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    version_number INTEGER
);

-- Insert new version when data changes
INSERT INTO dim_customer_scd2 (
    customer_id, customer_name, city, state,
    effective_date, expiry_date, is_current, version_number
) VALUES (
    'CUST001', 'John Smith Jr.', 'New York', 'NY',
    CURRENT_DATE, '9999-12-31', TRUE, 2
);

-- Update previous version
UPDATE dim_customer_scd2 
SET expiry_date = CURRENT_DATE - 1,
    is_current = FALSE
WHERE customer_id = 'CUST001' AND is_current = TRUE;
```

#### SCD Type 3 - Previous Value Column
```sql
CREATE TABLE dim_customer_scd3 (
    customer_key INTEGER PRIMARY KEY,
    customer_id VARCHAR(50),
    customer_name VARCHAR(255),
    current_city VARCHAR(100),
    previous_city VARCHAR(100),
    city_change_date DATE
);
```

## 🔄 NoSQL Data Modeling

### Document Database Modeling

**MongoDB Example**:
```javascript
// Embedded document model
{
  "_id": ObjectId("..."),
  "customer_id": "CUST001",
  "name": "John Doe",
  "email": "john@email.com",
  "addresses": [
    {
      "type": "home",
      "street": "123 Main St",
      "city": "Boston",
      "state": "MA",
      "zip": "02101"
    },
    {
      "type": "work",
      "street": "456 Business Ave",
      "city": "Boston",
      "state": "MA",
      "zip": "02102"
    }
  ],
  "orders": [
    {
      "order_id": "ORD001",
      "date": ISODate("2023-01-15"),
      "total": 299.99,
      "items": [
        {
          "product_id": "PROD001",
          "name": "Laptop",
          "quantity": 1,
          "price": 299.99
        }
      ]
    }
  ]
}
```

### Key-Value Store Modeling

**Redis Example**:
```redis
# User profile
SET user:1001 '{"name":"John Doe","email":"john@email.com","last_login":"2023-01-15T10:30:00Z"}'

# User sessions
SET session:abc123 user:1001 EX 3600

# Shopping cart
HSET cart:user:1001 product:123 2
HSET cart:user:1001 product:456 1

# Product catalog
SET product:123 '{"name":"Laptop","price":999.99,"category":"Electronics"}'
```

### Column-Family Modeling

**Cassandra Example**:
```cql
-- Time-series data modeling
CREATE TABLE sensor_data (
    sensor_id UUID,
    timestamp TIMESTAMP,
    temperature DOUBLE,
    humidity DOUBLE,
    pressure DOUBLE,
    PRIMARY KEY (sensor_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- User activity tracking
CREATE TABLE user_activity (
    user_id UUID,
    activity_date DATE,
    activity_time TIMESTAMP,
    activity_type TEXT,
    details MAP<TEXT, TEXT>,
    PRIMARY KEY ((user_id, activity_date), activity_time)
) WITH CLUSTERING ORDER BY (activity_time DESC);
```

### Graph Database Modeling

**Neo4j Example**:
```cypher
// Create nodes
CREATE (u:User {id: 'user1', name: 'John Doe', email: 'john@email.com'})
CREATE (p:Product {id: 'prod1', name: 'Laptop', price: 999.99})
CREATE (c:Category {id: 'cat1', name: 'Electronics'})

// Create relationships
CREATE (u)-[:PURCHASED {date: '2023-01-15', quantity: 1}]->(p)
CREATE (p)-[:BELONGS_TO]->(c)
CREATE (u)-[:VIEWED {timestamp: '2023-01-14T10:30:00Z'}]->(p)

// Query patterns
MATCH (u:User)-[r:PURCHASED]->(p:Product)-[:BELONGS_TO]->(c:Category)
WHERE c.name = 'Electronics'
RETURN u.name, p.name, r.date, r.quantity
```

## 🏛️ Data Vault Modeling

### Core Components

#### Hubs
**Definition**: Unique business keys and metadata.

```sql
CREATE TABLE hub_customer (
    customer_hash_key CHAR(32) PRIMARY KEY,
    customer_business_key VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

CREATE TABLE hub_product (
    product_hash_key CHAR(32) PRIMARY KEY,
    product_business_key VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);
```

#### Links
**Definition**: Relationships between business keys.

```sql
CREATE TABLE link_customer_product (
    customer_product_hash_key CHAR(32) PRIMARY KEY,
    customer_hash_key CHAR(32) NOT NULL,
    product_hash_key CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_hash_key) REFERENCES hub_customer(customer_hash_key),
    FOREIGN KEY (product_hash_key) REFERENCES hub_product(product_hash_key)
);
```

#### Satellites
**Definition**: Descriptive attributes and historical changes.

```sql
CREATE TABLE sat_customer (
    customer_hash_key CHAR(32),
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    hash_diff CHAR(32),
    record_source VARCHAR(50),
    PRIMARY KEY (customer_hash_key, load_date),
    FOREIGN KEY (customer_hash_key) REFERENCES hub_customer(customer_hash_key)
);
```

## ⚡ Performance Optimization

### Indexing Strategies

```sql
-- B-tree indexes for equality and range queries
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_date_range ON orders(order_date);

-- Composite indexes for multi-column queries
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Partial indexes for filtered queries
CREATE INDEX idx_orders_pending ON orders(customer_id) 
WHERE status = 'pending';

-- Expression indexes for computed values
CREATE INDEX idx_customers_upper_email ON customers(UPPER(email));

-- Covering indexes to avoid table lookups
CREATE INDEX idx_orders_covering ON orders(customer_id) 
INCLUDE (order_date, total_amount, status);
```

### Partitioning Strategies

```sql
-- Range partitioning by date
CREATE TABLE sales_data (
    sale_id BIGINT,
    sale_date DATE,
    customer_id INTEGER,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2023_q1 PARTITION OF sales_data
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');
CREATE TABLE sales_2023_q2 PARTITION OF sales_data
    FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');

-- Hash partitioning for even distribution
CREATE TABLE user_data (
    user_id BIGINT,
    username VARCHAR(50),
    email VARCHAR(100)
) PARTITION BY HASH (user_id);

CREATE TABLE user_data_0 PARTITION OF user_data
    FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE user_data_1 PARTITION OF user_data
    FOR VALUES WITH (modulus 4, remainder 1);
```

### Query Optimization

```sql
-- Use appropriate WHERE clauses
SELECT customer_id, order_date, total_amount
FROM orders
WHERE order_date >= '2023-01-01'
  AND order_date < '2023-02-01'
  AND status = 'completed';

-- Optimize JOIN operations
SELECT c.customer_name, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_type = 'premium'
  AND o.order_date >= CURRENT_DATE - INTERVAL '30 days';

-- Use EXISTS instead of IN for better performance
SELECT customer_id, customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2023-01-01'
);
```

## 🎯 Best Practices

### Design Principles

1. **Start with Business Requirements**
   - Understand business processes and data flows
   - Identify key entities and relationships
   - Define data quality requirements

2. **Follow Naming Conventions**
   - Use consistent, descriptive names
   - Avoid abbreviations and acronyms
   - Use standard prefixes/suffixes

3. **Ensure Data Integrity**
   - Define primary and foreign keys
   - Implement appropriate constraints
   - Use check constraints for data validation

4. **Plan for Scalability**
   - Consider future growth and requirements
   - Design for horizontal and vertical scaling
   - Implement appropriate partitioning strategies

5. **Document Everything**
   - Maintain data dictionaries
   - Document business rules and assumptions
   - Keep models up-to-date with changes

### Common Anti-Patterns to Avoid

```sql
-- Anti-pattern: Generic columns
CREATE TABLE bad_design (
    id INTEGER,
    field1 VARCHAR(255),
    field2 VARCHAR(255),
    field3 VARCHAR(255)
);

-- Better: Specific, meaningful columns
CREATE TABLE good_design (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Anti-pattern: No constraints
CREATE TABLE orders_bad (
    order_id INTEGER,
    customer_id INTEGER,
    total_amount DECIMAL(10,2)
);

-- Better: Proper constraints
CREATE TABLE orders_good (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

## 📊 When to Use Different Approaches

### Relational Modeling
**Use When**:
- ACID compliance is critical
- Complex relationships between entities
- Strong consistency requirements
- Well-defined schema with stable structure

**Examples**: Financial systems, ERP, CRM

### Dimensional Modeling
**Use When**:
- Analytics and reporting requirements
- Historical data analysis
- OLAP operations
- Business intelligence applications

**Examples**: Data warehouses, business intelligence, reporting systems

### NoSQL Modeling
**Use When**:
- Flexible schema requirements
- High scalability needs
- Rapid development cycles
- Unstructured or semi-structured data

**Examples**: Content management, real-time analytics, IoT applications

### Data Vault Modeling
**Use When**:
- Enterprise data warehouse
- Regulatory compliance requirements
- Auditability and traceability needs
- Multiple source systems integration

**Examples**: Enterprise data hubs, regulatory reporting, data governance

## 🎯 Interview Focus Areas

1. **Normalization**: Understanding of 1NF, 2NF, 3NF, and BCNF
2. **Dimensional Modeling**: Star vs snowflake schema, SCD types
3. **NoSQL Patterns**: Document, key-value, column-family, graph modeling
4. **Performance**: Indexing strategies, partitioning, query optimization
5. **Data Vault**: Hub, link, satellite concepts and implementation
6. **Best Practices**: Naming conventions, constraints, documentation
7. **Trade-offs**: When to normalize vs denormalize
8. **Schema Evolution**: Handling changes over time
9. **Data Quality**: Constraints, validation, integrity
10. **Modern Patterns**: Event sourcing, CQRS, microservices data patterns

## 📚 Quick References

### Normalization Quick Check
- **1NF**: Atomic values, no repeating groups
- **2NF**: 1NF + no partial dependencies
- **3NF**: 2NF + no transitive dependencies
- **BCNF**: 3NF + every determinant is a candidate key

### SCD Types Summary
- **Type 0**: Retain original (no changes)
- **Type 1**: Overwrite (no history)
- **Type 2**: Add new record (full history)
- **Type 3**: Add new column (limited history)

### NoSQL Model Selection
- **Document**: Complex nested data, flexible schema
- **Key-Value**: Simple lookups, caching, sessions
- **Column-Family**: Time-series, wide tables, high write volume
- **Graph**: Relationships, social networks, recommendations

### Performance Optimization Checklist
- [ ] Appropriate indexes on frequently queried columns
- [ ] Partitioning for large tables
- [ ] Constraints for data integrity
- [ ] Proper data types and sizes
- [ ] Query optimization and execution plans
- [ ] Regular statistics updates
- [ ] Monitoring and alerting

---

**Remember**: The best data model balances business requirements, performance needs, and maintainability. Always start with understanding the business context and data usage patterns before choosing a modeling approach.