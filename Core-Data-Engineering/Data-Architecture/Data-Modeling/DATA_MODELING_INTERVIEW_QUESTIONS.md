# Data Modeling Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-200)](#architecture--performance-151-200)
5. [NoSQL & Modern Patterns (201-250)](#nosql--modern-patterns-201-250)
6. [Production & Operations (251-300)](#production--operations-251-300)
7. [Scenario-Based Questions (301-350)](#scenario-based-questions-301-350)

---

## Basic Level Questions (1-50)

### 1. What is data modeling and why is it important?
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

### 2. Compare different data modeling approaches and when to use each
**Answer:**

| Approach | Best For | Strengths | Weaknesses |
|----------|----------|-----------|------------|
| **Relational** | OLTP, transactional systems | ACID compliance, data integrity | Complex joins, rigid schema |
| **Dimensional** | OLAP, analytics, reporting | Query performance, business-friendly | Data redundancy, ETL complexity |
| **Data Vault** | Enterprise data warehouses | Auditability, flexibility | Learning curve, complexity |
| **NoSQL** | Big data, flexible schemas | Scalability, schema flexibility | Eventual consistency, limited ACID |

### 3. What are the key principles of good data modeling?
**Answer:**
1. **Simplicity**: Keep models as simple as possible while meeting requirements
2. **Consistency**: Use consistent naming conventions and patterns
3. **Completeness**: Capture all necessary business rules and relationships
4. **Flexibility**: Design for future changes and requirements
5. **Performance**: Consider query patterns and optimization needs
6. **Integrity**: Implement proper constraints and validation rules
7. **Documentation**: Maintain clear documentation and metadata

### 4. Explain database normalization and its forms
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

### 5. When would you denormalize a database and what are the trade-offs?
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

### 6. Design a relational model for an e-commerce system
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

### 7. Explain the star schema and its components
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

### 8. What is the difference between star schema and snowflake schema?
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

### 9. Explain Slowly Changing Dimensions (SCD) and their types
**Answer:**

**SCD**: Techniques to handle changes in dimension attributes over time.

**Type 0 - Retain Original:**
- Never change the attribute
- Used for fixed attributes like birth date

**Type 1 - Overwrite:**
- Replace old value with new value
- No history maintained
- Simple but loses historical data

```sql
UPDATE dim_customer 
SET city = 'New York', state = 'NY'
WHERE customer_id = 'CUST001';
```

**Type 2 - Add New Record:**
- Create new record for each change
- Maintains full history
- Most common approach

```sql
-- Insert new record
INSERT INTO dim_customer (
    customer_id, name, city, state,
    effective_date, expiry_date, is_current
) VALUES (
    'CUST001', 'John Doe', 'New York', 'NY',
    CURRENT_DATE, '9999-12-31', TRUE
);

-- Update previous record
UPDATE dim_customer 
SET expiry_date = CURRENT_DATE - 1, is_current = FALSE
WHERE customer_id = 'CUST001' AND is_current = TRUE;
```

**Type 3 - Add New Column:**
- Add column for previous value
- Limited history (only one previous value)

```sql
ALTER TABLE dim_customer 
ADD COLUMN previous_city VARCHAR(100),
ADD COLUMN city_change_date DATE;
```

### 10. What are primary keys, foreign keys, and their importance?
**Answer:**

**Primary Key:**
- Uniquely identifies each record in a table
- Cannot be NULL
- Ensures entity integrity
- Used for indexing and relationships

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100)
);
```

**Foreign Key:**
- References primary key of another table
- Ensures referential integrity
- Maintains relationships between tables
- Can be NULL (optional relationship)

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**Importance:**
- **Data Integrity**: Prevents orphaned records
- **Relationships**: Maintains logical connections
- **Performance**: Enables efficient joins
- **Constraints**: Enforces business rules

---

## Basic Level Questions (11-20)

### 11. What is an Entity-Relationship (ER) diagram?
**Answer:**

**ER Diagram**: Visual representation of entities, attributes, and relationships in a database.

**Components:**
- **Entities**: Rectangles (Customer, Order, Product)
- **Attributes**: Ovals (name, price, date)
- **Relationships**: Diamonds (places, contains, belongs to)
- **Cardinality**: Numbers indicating relationship ratios

**Example:**
```
Customer (1) ──places──► (M) Order (1) ──contains──► (M) OrderItem (M) ◄──references── (1) Product
```

**Cardinality Types:**
- **One-to-One (1:1)**: Each entity instance relates to one instance
- **One-to-Many (1:M)**: One instance relates to many instances
- **Many-to-Many (M:M)**: Many instances relate to many instances

### 12. How do you handle many-to-many relationships?
**Answer:**

**Problem**: Direct many-to-many relationships cannot be implemented in relational databases.

**Solution**: Create a junction/bridge table with foreign keys to both entities.

```sql
-- Many-to-many: Students and Courses
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100),
    credits INT
);

-- Junction table
CREATE TABLE student_enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE(student_id, course_id)
);
```

### 13. What are database constraints and their types?
**Answer:**

**Database Constraints**: Rules that enforce data integrity and business logic.

**Types:**

**1. NOT NULL Constraint:**
```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL
);
```

**2. UNIQUE Constraint:**
```sql
ALTER TABLE customers 
ADD CONSTRAINT unique_email UNIQUE (email);
```

**3. CHECK Constraint:**
```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL(10,2) CHECK (price > 0),
    status VARCHAR(20) CHECK (status IN ('active', 'inactive', 'discontinued'))
);
```

**4. FOREIGN KEY Constraint:**
```sql
ALTER TABLE orders 
ADD CONSTRAINT fk_customer 
FOREIGN KEY (customer_id) REFERENCES customers(customer_id);
```

**5. DEFAULT Constraint:**
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'pending'
);
```

### 14. What is data integrity and how do you ensure it?
**Answer:**

**Data Integrity**: Accuracy, consistency, and reliability of data throughout its lifecycle.

**Types of Data Integrity:**

**1. Entity Integrity:**
- Each table has a primary key
- Primary key values are unique and not null

**2. Referential Integrity:**
- Foreign key values match existing primary key values
- Prevents orphaned records

**3. Domain Integrity:**
- Data values conform to defined data types and constraints
- Valid ranges and formats

**4. User-Defined Integrity:**
- Business rules and custom constraints
- Triggers and stored procedures

**Implementation:**
```sql
-- Entity integrity
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Referential integrity
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Domain integrity
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL(10,2) CHECK (price >= 0),
    category VARCHAR(50) CHECK (category IN ('electronics', 'clothing', 'books'))
);

-- User-defined integrity (trigger example)
CREATE OR REPLACE FUNCTION check_order_total()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.total_amount < 0 THEN
        RAISE EXCEPTION 'Order total cannot be negative';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_order_total
    BEFORE INSERT OR UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION check_order_total();
```

### 15. What are indexes and how do they improve performance?
**Answer:**

**Index**: Data structure that improves query performance by creating shortcuts to data.

**Types of Indexes:**

**1. B-Tree Index (Default):**
```sql
-- Single column index
CREATE INDEX idx_customers_email ON customers(email);

-- Composite index
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
```

**2. Unique Index:**
```sql
CREATE UNIQUE INDEX idx_customers_email_unique ON customers(email);
```

**3. Partial Index:**
```sql
-- Index only active customers
CREATE INDEX idx_customers_active ON customers(customer_id) 
WHERE status = 'active';
```

**4. Expression Index:**
```sql
-- Index on computed value
CREATE INDEX idx_customers_upper_name ON customers(UPPER(last_name));
```

**Performance Benefits:**
- **Faster SELECT queries**: Direct data access
- **Efficient ORDER BY**: Pre-sorted data
- **Quick JOIN operations**: Faster key lookups
- **Unique constraint enforcement**: Prevents duplicates

**Trade-offs:**
```
Advantages:
✓ Faster query performance
✓ Efficient sorting and grouping
✓ Quick data retrieval

Disadvantages:
✗ Additional storage space
✗ Slower INSERT/UPDATE/DELETE
✗ Index maintenance overhead
```

### 16. What is the difference between clustered and non-clustered indexes?
**Answer:**

**Clustered Index:**
- Physical ordering of data matches index order
- One per table (usually primary key)
- Data pages stored in order of clustered index key
- Faster range queries

**Non-Clustered Index:**
- Logical ordering separate from physical storage
- Multiple per table allowed
- Points to data location
- Additional lookup required

```sql
-- SQL Server example
-- Clustered index (primary key)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY CLUSTERED,
    name VARCHAR(100),
    email VARCHAR(255)
);

-- Non-clustered index
CREATE NONCLUSTERED INDEX idx_customers_email 
ON customers(email);
```

**Performance Comparison:**
| Aspect | Clustered | Non-Clustered |
|--------|-----------|---------------|
| **Data Access** | Direct | Indirect (bookmark lookup) |
| **Range Queries** | Very fast | Moderate |
| **Insert Performance** | Slower (reordering) | Faster |
| **Storage** | No additional space | Additional space required |
| **Quantity per Table** | One | Multiple |

### 17. What are views and when should you use them?
**Answer:**

**View**: Virtual table based on a SQL query that doesn't store data physically.

**Types of Views:**

**1. Simple View:**
```sql
CREATE VIEW active_customers AS
SELECT customer_id, name, email
FROM customers
WHERE status = 'active';
```

**2. Complex View (with joins):**
```sql
CREATE VIEW customer_order_summary AS
SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

**3. Materialized View:**
```sql
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_sales_summary;
```

**When to Use Views:**
- **Security**: Hide sensitive columns
- **Simplification**: Complex queries made simple
- **Abstraction**: Hide underlying table structure
- **Reusability**: Common queries used multiple times
- **Data Consistency**: Standardized business logic

**Benefits:**
- Simplified queries for end users
- Enhanced security through column/row filtering
- Logical data independence
- Centralized business logic

### 18. What is database partitioning and its types?
**Answer:**

**Partitioning**: Dividing large tables into smaller, manageable pieces while maintaining logical unity.

**Types of Partitioning:**

**1. Range Partitioning:**
```sql
-- Partition by date range
CREATE TABLE sales_data (
    sale_id BIGINT,
    sale_date DATE,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2023_q1 PARTITION OF sales_data
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');
CREATE TABLE sales_2023_q2 PARTITION OF sales_data
    FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');
```

**2. Hash Partitioning:**
```sql
-- Even distribution across partitions
CREATE TABLE user_data (
    user_id BIGINT,
    username VARCHAR(50)
) PARTITION BY HASH (user_id);

CREATE TABLE user_data_0 PARTITION OF user_data
    FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE user_data_1 PARTITION OF user_data
    FOR VALUES WITH (modulus 4, remainder 1);
```

**3. List Partitioning:**
```sql
-- Partition by specific values
CREATE TABLE regional_sales (
    sale_id BIGINT,
    region VARCHAR(20),
    amount DECIMAL(10,2)
) PARTITION BY LIST (region);

CREATE TABLE sales_north PARTITION OF regional_sales
    FOR VALUES IN ('north', 'northeast', 'northwest');
CREATE TABLE sales_south PARTITION OF regional_sales
    FOR VALUES IN ('south', 'southeast', 'southwest');
```

**Benefits:**
- **Performance**: Partition pruning reduces scan time
- **Maintenance**: Easier backup, archiving, and maintenance
- **Scalability**: Better handling of large datasets
- **Parallel Processing**: Operations can run in parallel

### 19. What are stored procedures and functions?
**Answer:**

**Stored Procedures**: Pre-compiled SQL code stored in database for reuse.

**Stored Procedure Example:**
```sql
CREATE OR REPLACE PROCEDURE create_customer_order(
    p_customer_id INT,
    p_product_ids INT[],
    p_quantities INT[],
    OUT p_order_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total_amount DECIMAL(10,2) := 0;
    v_product_id INT;
    v_quantity INT;
    v_price DECIMAL(10,2);
    i INT;
BEGIN
    -- Create order
    INSERT INTO orders (customer_id, order_date, status)
    VALUES (p_customer_id, CURRENT_DATE, 'pending')
    RETURNING order_id INTO p_order_id;
    
    -- Add order items
    FOR i IN 1..array_length(p_product_ids, 1) LOOP
        v_product_id := p_product_ids[i];
        v_quantity := p_quantities[i];
        
        -- Get product price
        SELECT price INTO v_price FROM products WHERE product_id = v_product_id;
        
        -- Insert order item
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (p_order_id, v_product_id, v_quantity, v_price);
        
        v_total_amount := v_total_amount + (v_price * v_quantity);
    END LOOP;
    
    -- Update order total
    UPDATE orders SET total_amount = v_total_amount WHERE order_id = p_order_id;
END;
$$;
```

**Function Example:**
```sql
CREATE OR REPLACE FUNCTION calculate_customer_lifetime_value(p_customer_id INT)
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total_value DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(total_amount), 0)
    INTO v_total_value
    FROM orders
    WHERE customer_id = p_customer_id
    AND status = 'completed';
    
    RETURN v_total_value;
END;
$$;

-- Usage
SELECT customer_id, name, calculate_customer_lifetime_value(customer_id) as ltv
FROM customers;
```

**Benefits:**
- **Performance**: Pre-compiled and cached
- **Security**: Controlled data access
- **Reusability**: Code reuse across applications
- **Maintainability**: Centralized business logic
- **Network Traffic**: Reduced data transfer

### 20. What are triggers and when should you use them?
**Answer:**

**Triggers**: Special stored procedures that automatically execute in response to database events.

**Types of Triggers:**

**1. BEFORE Triggers:**
```sql
-- Audit trigger - track changes before they happen
CREATE OR REPLACE FUNCTION audit_customer_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- Log the change
    INSERT INTO customer_audit (
        customer_id, 
        old_email, 
        new_email, 
        changed_by, 
        changed_at
    ) VALUES (
        NEW.customer_id,
        OLD.email,
        NEW.email,
        current_user,
        current_timestamp
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_audit_customer_changes
    BEFORE UPDATE ON customers
    FOR EACH ROW
    WHEN (OLD.email IS DISTINCT FROM NEW.email)
    EXECUTE FUNCTION audit_customer_changes();
```

**2. AFTER Triggers:**
```sql
-- Update inventory after order item insertion
CREATE OR REPLACE FUNCTION update_inventory_after_order()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE inventory 
    SET reserved_quantity = reserved_quantity + NEW.quantity
    WHERE product_id = NEW.product_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_inventory
    AFTER INSERT ON order_items
    FOR EACH ROW
    EXECUTE FUNCTION update_inventory_after_order();
```

**3. INSTEAD OF Triggers (for views):**
```sql
-- Make a view updatable
CREATE OR REPLACE FUNCTION update_customer_view()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE customers 
    SET name = NEW.name, email = NEW.email
    WHERE customer_id = NEW.customer_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_customer_view
    INSTEAD OF UPDATE ON customer_summary_view
    FOR EACH ROW
    EXECUTE FUNCTION update_customer_view();
```

**When to Use Triggers:**
- **Auditing**: Track data changes
- **Business Rules**: Enforce complex constraints
- **Automatic Updates**: Maintain derived data
- **Logging**: Record database activities
- **Data Validation**: Complex validation logic

**Best Practices:**
- Keep triggers simple and fast
- Avoid recursive triggers
- Document trigger logic thoroughly
- Consider alternatives (application logic, constraints)
- Test thoroughly for performance impact

---

## Basic Level Questions (21-30)

### 21. What is referential integrity and how do you maintain it?
**Answer:**

**Referential Integrity**: Ensures relationships between tables remain consistent by preventing actions that would destroy links between tables.

**Key Concepts:**
- Foreign key values must match existing primary key values
- Prevents orphaned records
- Maintains data consistency across related tables

**Implementation:**
```sql
-- Basic foreign key constraint
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Foreign key with referential actions
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE    -- Delete items when order is deleted
        ON UPDATE CASCADE,   -- Update item's order_id when order's id changes
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE RESTRICT   -- Prevent product deletion if referenced
        ON UPDATE CASCADE
);
```

**Referential Actions:**
- **CASCADE**: Automatically update/delete related records
- **RESTRICT**: Prevent action if related records exist
- **SET NULL**: Set foreign key to NULL
- **SET DEFAULT**: Set foreign key to default value
- **NO ACTION**: Check constraint at end of transaction

### 22. What are database transactions and ACID properties?
**Answer:**

**Transaction**: Unit of work that must be completed entirely or not at all.

**ACID Properties:**

**1. Atomicity:**
- All operations succeed or all fail
- No partial transactions

```sql
BEGIN TRANSACTION;
    INSERT INTO orders (customer_id, total_amount) VALUES (1, 100.00);
    INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 101, 2);
    UPDATE inventory SET quantity = quantity - 2 WHERE product_id = 101;
COMMIT; -- All succeed or all rollback
```

**2. Consistency:**
- Database remains in valid state
- All constraints maintained

```sql
-- Constraint ensures consistency
ALTER TABLE accounts ADD CONSTRAINT check_balance CHECK (balance >= 0);

BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
    -- If first account would go negative, transaction fails
COMMIT;
```

**3. Isolation:**
- Concurrent transactions don't interfere
- Different isolation levels available

```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRANSACTION;
    SELECT balance FROM accounts WHERE account_id = 1;
    -- Other transactions can't modify this account until commit
    UPDATE accounts SET balance = balance - 50 WHERE account_id = 1;
COMMIT;
```

**4. Durability:**
- Committed changes persist even after system failure
- Write-ahead logging ensures durability

**Isolation Levels:**
- **READ UNCOMMITTED**: Lowest isolation, allows dirty reads
- **READ COMMITTED**: Prevents dirty reads
- **REPEATABLE READ**: Prevents dirty and non-repeatable reads
- **SERIALIZABLE**: Highest isolation, prevents all phenomena

### 23. What is the difference between DELETE, TRUNCATE, and DROP?
**Answer:**

**DELETE:**
- Removes specific rows based on WHERE clause
- Can be rolled back
- Triggers fire
- Slower for large datasets

```sql
-- Delete specific records
DELETE FROM customers WHERE status = 'inactive';

-- Delete all records (can be rolled back)
DELETE FROM temp_data;
```

**TRUNCATE:**
- Removes all rows from table
- Faster than DELETE for large tables
- Cannot be rolled back in some databases
- Resets identity columns
- Triggers don't fire

```sql
-- Remove all data quickly
TRUNCATE TABLE temp_data;

-- Cannot use WHERE clause
-- TRUNCATE TABLE customers WHERE status = 'inactive'; -- ERROR
```

**DROP:**
- Removes entire table structure and data
- Cannot be rolled back
- Frees up storage space completely

```sql
-- Remove table completely
DROP TABLE temp_data;

-- Remove with dependencies
DROP TABLE customers CASCADE;
```

**Comparison:**
| Operation | Speed | Rollback | Triggers | WHERE Clause | Structure |
|-----------|-------|----------|----------|--------------|-----------|
| DELETE | Slow | Yes | Yes | Yes | Preserved |
| TRUNCATE | Fast | Limited | No | No | Preserved |
| DROP | Fast | No | No | No | Removed |

### 24. What are common database design patterns?
**Answer:**

**1. Repository Pattern:**
- Encapsulates data access logic
- Provides consistent interface for data operations

```sql
-- Repository interface implementation
CREATE VIEW customer_repository AS
SELECT 
    customer_id,
    CONCAT(first_name, ' ', last_name) as full_name,
    email,
    status,
    created_at
FROM customers
WHERE deleted_at IS NULL;

-- Stored procedures for CRUD operations
CREATE OR REPLACE PROCEDURE create_customer(
    p_first_name VARCHAR(50),
    p_last_name VARCHAR(50),
    p_email VARCHAR(255)
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO customers (first_name, last_name, email, created_at)
    VALUES (p_first_name, p_last_name, p_email, CURRENT_TIMESTAMP);
END;
$$;
```

**2. Active Record Pattern:**
- Each table row represented as object
- Object contains both data and behavior

```sql
-- Table with built-in methods via functions
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'active'
);

-- Method-like functions
CREATE OR REPLACE FUNCTION product_is_available(p_product_id INT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM products 
        WHERE product_id = p_product_id AND status = 'active'
    );
END;
$$ LANGUAGE plpgsql;
```

**3. Data Mapper Pattern:**
- Separates domain objects from database schema
- Flexible mapping between objects and tables

```sql
-- Flexible mapping table
CREATE TABLE entity_attributes (
    entity_id INT,
    entity_type VARCHAR(50),
    attribute_name VARCHAR(100),
    attribute_value TEXT,
    data_type VARCHAR(20),
    PRIMARY KEY (entity_id, entity_type, attribute_name)
);

-- Dynamic entity storage
INSERT INTO entity_attributes VALUES
(1, 'customer', 'name', 'John Doe', 'string'),
(1, 'customer', 'age', '30', 'integer'),
(1, 'customer', 'email', 'john@email.com', 'string');
```

**4. Unit of Work Pattern:**
- Maintains list of objects affected by transaction
- Coordinates writing out changes

```sql
-- Transaction coordination table
CREATE TABLE unit_of_work (
    transaction_id UUID PRIMARY KEY,
    entity_type VARCHAR(50),
    entity_id INT,
    operation VARCHAR(10), -- INSERT, UPDATE, DELETE
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 25. How do you handle hierarchical data in relational databases?
**Answer:**

**1. Adjacency List Model:**
- Each record stores reference to its parent
- Simple but inefficient for deep hierarchies

```sql
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_id INT,
    FOREIGN KEY (parent_id) REFERENCES categories(category_id)
);

-- Sample data
INSERT INTO categories (name, parent_id) VALUES
('Electronics', NULL),
('Computers', 1),
('Laptops', 2),
('Gaming Laptops', 3);

-- Recursive query to get hierarchy
WITH RECURSIVE category_tree AS (
    -- Base case: root categories
    SELECT category_id, name, parent_id, 0 as level, name as path
    FROM categories
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive case: child categories
    SELECT c.category_id, c.name, c.parent_id, ct.level + 1,
           ct.path || ' > ' || c.name
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.category_id
)
SELECT * FROM category_tree ORDER BY path;
```

**2. Nested Set Model:**
- Each node has left and right values
- Efficient for read-heavy operations

```sql
CREATE TABLE categories_nested (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    lft INT NOT NULL,
    rgt INT NOT NULL
);

-- Sample data (Electronics: 1-8, Computers: 2-7, Laptops: 3-6, Gaming: 4-5)
INSERT INTO categories_nested (name, lft, rgt) VALUES
('Electronics', 1, 8),
('Computers', 2, 7),
('Laptops', 3, 6),
('Gaming Laptops', 4, 5);

-- Get all descendants of a node
SELECT child.name
FROM categories_nested parent, categories_nested child
WHERE child.lft BETWEEN parent.lft AND parent.rgt
AND parent.name = 'Computers';
```

**3. Path Enumeration:**
- Store full path to each node
- Good for read performance

```sql
CREATE TABLE categories_path (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    path VARCHAR(500) -- e.g., '/1/2/3/'
);

-- Query descendants
SELECT * FROM categories_path
WHERE path LIKE '/1/2/%';
```

**4. Closure Table:**
- Separate table stores all ancestor-descendant relationships
- Most flexible but requires more storage

```sql
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE category_closure (
    ancestor_id INT,
    descendant_id INT,
    depth INT,
    PRIMARY KEY (ancestor_id, descendant_id),
    FOREIGN KEY (ancestor_id) REFERENCES categories(category_id),
    FOREIGN KEY (descendant_id) REFERENCES categories(category_id)
);

-- Get all descendants
SELECT c.name
FROM categories c
JOIN category_closure cc ON c.category_id = cc.descendant_id
WHERE cc.ancestor_id = 1; -- Electronics
```

### 26. What is data modeling for time-series data?
**Answer:**

**Time-Series Data**: Data points indexed by time, typically collected at regular intervals.

**Design Considerations:**
- High write volume
- Time-based queries
- Data retention policies
- Aggregation requirements

**1. Basic Time-Series Table:**
```sql
CREATE TABLE sensor_readings (
    reading_id BIGSERIAL PRIMARY KEY,
    sensor_id INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    pressure DECIMAL(7,2),
    INDEX idx_sensor_time (sensor_id, timestamp)
);

-- Partition by time for better performance
CREATE TABLE sensor_readings_2024_01 PARTITION OF sensor_readings
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

**2. Wide Table Approach:**
```sql
-- Store multiple metrics in single row
CREATE TABLE iot_metrics (
    device_id INT,
    timestamp TIMESTAMP,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    disk_usage DECIMAL(5,2),
    network_in BIGINT,
    network_out BIGINT,
    PRIMARY KEY (device_id, timestamp)
);
```

**3. Narrow Table Approach:**
```sql
-- Flexible schema for different metric types
CREATE TABLE metric_values (
    device_id INT,
    timestamp TIMESTAMP,
    metric_name VARCHAR(50),
    metric_value DECIMAL(15,4),
    PRIMARY KEY (device_id, timestamp, metric_name)
);
```

**4. Pre-aggregated Tables:**
```sql
-- Store different aggregation levels
CREATE TABLE sensor_readings_hourly (
    sensor_id INT,
    hour_timestamp TIMESTAMP,
    avg_temperature DECIMAL(5,2),
    min_temperature DECIMAL(5,2),
    max_temperature DECIMAL(5,2),
    reading_count INT,
    PRIMARY KEY (sensor_id, hour_timestamp)
);

CREATE TABLE sensor_readings_daily (
    sensor_id INT,
    date DATE,
    avg_temperature DECIMAL(5,2),
    min_temperature DECIMAL(5,2),
    max_temperature DECIMAL(5,2),
    reading_count INT,
    PRIMARY KEY (sensor_id, date)
);
```

**5. Time-Series Specific Features:**
```sql
-- PostgreSQL TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Convert regular table to hypertable
SELECT create_hypertable('sensor_readings', 'timestamp');

-- Continuous aggregates
CREATE MATERIALIZED VIEW sensor_readings_hourly
WITH (timescaledb.continuous) AS
SELECT 
    sensor_id,
    time_bucket('1 hour', timestamp) AS hour,
    AVG(temperature) as avg_temp,
    MIN(temperature) as min_temp,
    MAX(temperature) as max_temp
FROM sensor_readings
GROUP BY sensor_id, hour;
```

### 27. How do you model audit trails and change tracking?
**Answer:**

**Audit Trail**: Record of all changes made to data for compliance and debugging.

**1. Shadow Table Approach:**
```sql
-- Main table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    status VARCHAR(20),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit table (shadow table)
CREATE TABLE customers_audit (
    audit_id SERIAL PRIMARY KEY,
    customer_id INT,
    name VARCHAR(100),
    email VARCHAR(255),
    status VARCHAR(20),
    operation VARCHAR(10), -- INSERT, UPDATE, DELETE
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_values JSONB,
    new_values JSONB
);

-- Trigger to populate audit table
CREATE OR REPLACE FUNCTION audit_customers()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO customers_audit (
            customer_id, operation, changed_by, changed_at, old_values
        ) VALUES (
            OLD.customer_id, 'DELETE', current_user, current_timestamp,
            row_to_json(OLD)
        );
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO customers_audit (
            customer_id, operation, changed_by, changed_at, old_values, new_values
        ) VALUES (
            NEW.customer_id, 'UPDATE', current_user, current_timestamp,
            row_to_json(OLD), row_to_json(NEW)
        );
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO customers_audit (
            customer_id, operation, changed_by, changed_at, new_values
        ) VALUES (
            NEW.customer_id, 'INSERT', current_user, current_timestamp,
            row_to_json(NEW)
        );
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_audit_customers
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION audit_customers();
```

**2. Generic Audit Log:**
```sql
CREATE TABLE audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    record_id VARCHAR(100),
    operation VARCHAR(10),
    field_name VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100),
    ip_address INET
);

-- Index for efficient queries
CREATE INDEX idx_audit_log_table_record ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_changed_at ON audit_log(changed_at);
```

**3. Temporal Tables (SQL Server/PostgreSQL):**
```sql
-- PostgreSQL temporal table
CREATE TABLE customers_temporal (
    customer_id SERIAL,
    name VARCHAR(100),
    email VARCHAR(255),
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_to TIMESTAMP DEFAULT 'infinity',
    PRIMARY KEY (customer_id, valid_from)
);

-- Update function that maintains history
CREATE OR REPLACE FUNCTION update_customer_temporal(
    p_customer_id INT,
    p_name VARCHAR(100),
    p_email VARCHAR(255)
)
RETURNS VOID AS $$
BEGIN
    -- End current version
    UPDATE customers_temporal 
    SET valid_to = CURRENT_TIMESTAMP
    WHERE customer_id = p_customer_id AND valid_to = 'infinity';
    
    -- Insert new version
    INSERT INTO customers_temporal (customer_id, name, email, valid_from)
    VALUES (p_customer_id, p_name, p_email, CURRENT_TIMESTAMP);
END;
$$ LANGUAGE plpgsql;
```

**4. Event Sourcing Pattern:**
```sql
CREATE TABLE customer_events (
    event_id BIGSERIAL PRIMARY KEY,
    customer_id INT,
    event_type VARCHAR(50), -- customer_created, email_changed, etc.
    event_data JSONB,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_version INT,
    created_by VARCHAR(100)
);

-- Rebuild current state from events
CREATE OR REPLACE FUNCTION rebuild_customer_state(p_customer_id INT)
RETURNS TABLE(customer_id INT, name VARCHAR(100), email VARCHAR(255)) AS $$
DECLARE
    event_record RECORD;
    result_record RECORD;
BEGIN
    -- Initialize result
    result_record.customer_id := p_customer_id;
    
    -- Apply events in order
    FOR event_record IN 
        SELECT * FROM customer_events 
        WHERE customer_id = p_customer_id 
        ORDER BY event_timestamp
    LOOP
        CASE event_record.event_type
            WHEN 'customer_created' THEN
                result_record.name := event_record.event_data->>'name';
                result_record.email := event_record.event_data->>'email';
            WHEN 'name_changed' THEN
                result_record.name := event_record.event_data->>'new_name';
            WHEN 'email_changed' THEN
                result_record.email := event_record.event_data->>'new_email';
        END CASE;
    END LOOP;
    
    RETURN QUERY SELECT result_record.customer_id, result_record.name, result_record.email;
END;
$$ LANGUAGE plpgsql;
```

### 28. What are database design anti-patterns to avoid?
**Answer:**

**1. Generic Columns Anti-Pattern:**
```sql
-- BAD: Generic, meaningless column names
CREATE TABLE bad_design (
    id INT,
    field1 VARCHAR(255),
    field2 VARCHAR(255),
    field3 VARCHAR(255),
    data TEXT
);

-- GOOD: Specific, meaningful columns
CREATE TABLE good_design (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    registration_date DATE NOT NULL
);
```

**2. Entity-Attribute-Value (EAV) Anti-Pattern:**
```sql
-- BAD: EAV pattern (hard to query and maintain)
CREATE TABLE eav_bad (
    entity_id INT,
    attribute_name VARCHAR(100),
    attribute_value VARCHAR(255)
);

-- Sample data
INSERT INTO eav_bad VALUES
(1, 'first_name', 'John'),
(1, 'last_name', 'Doe'),
(1, 'email', 'john@email.com'),
(2, 'first_name', 'Jane'),
(2, 'email', 'jane@email.com');

-- GOOD: Proper table structure
CREATE TABLE customers_good (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);
```

**3. Polymorphic Associations Anti-Pattern:**
```sql
-- BAD: Generic foreign key without referential integrity
CREATE TABLE comments_bad (
    comment_id INT PRIMARY KEY,
    commentable_id INT,
    commentable_type VARCHAR(50), -- 'post', 'photo', 'video'
    comment_text TEXT
);

-- GOOD: Separate tables or proper foreign keys
CREATE TABLE post_comments (
    comment_id INT PRIMARY KEY,
    post_id INT NOT NULL,
    comment_text TEXT,
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
);

CREATE TABLE photo_comments (
    comment_id INT PRIMARY KEY,
    photo_id INT NOT NULL,
    comment_text TEXT,
    FOREIGN KEY (photo_id) REFERENCES photos(photo_id)
);
```

**4. Multicolumn Attributes Anti-Pattern:**
```sql
-- BAD: Multiple columns for similar data
CREATE TABLE contacts_bad (
    contact_id INT PRIMARY KEY,
    phone1 VARCHAR(20),
    phone2 VARCHAR(20),
    phone3 VARCHAR(20),
    email1 VARCHAR(100),
    email2 VARCHAR(100),
    email3 VARCHAR(100)
);

-- GOOD: Separate table for multiple values
CREATE TABLE contacts_good (
    contact_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE contact_phones (
    contact_id INT,
    phone VARCHAR(20),
    phone_type VARCHAR(20), -- 'mobile', 'home', 'work'
    PRIMARY KEY (contact_id, phone),
    FOREIGN KEY (contact_id) REFERENCES contacts_good(contact_id)
);
```

**5. Metadata Tribbles Anti-Pattern:**
```sql
-- BAD: Creating tables for each time period
CREATE TABLE sales_2023_01 (sale_id INT, amount DECIMAL(10,2), sale_date DATE);
CREATE TABLE sales_2023_02 (sale_id INT, amount DECIMAL(10,2), sale_date DATE);
CREATE TABLE sales_2023_03 (sale_id INT, amount DECIMAL(10,2), sale_date DATE);
-- ... continues for each month

-- GOOD: Single table with partitioning
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    amount DECIMAL(10,2),
    sale_date DATE
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2023_q1 PARTITION OF sales
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');
```

**6. Fear of the Unknown Anti-Pattern:**
```sql
-- BAD: Using VARCHAR(255) for everything
CREATE TABLE products_bad (
    product_id INT,
    name VARCHAR(255),
    price VARCHAR(255), -- Should be DECIMAL
    category VARCHAR(255),
    is_active VARCHAR(255) -- Should be BOOLEAN
);

-- GOOD: Appropriate data types
CREATE TABLE products_good (
    product_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);
```

### 29. How do you handle data versioning and temporal data?
**Answer:**

**Temporal Data**: Data that changes over time and requires historical tracking.

**1. Effective Dating:**
```sql
CREATE TABLE employee_positions (
    employee_id INT,
    position_title VARCHAR(100),
    salary DECIMAL(10,2),
    effective_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (employee_id, effective_date)
);

-- Insert new position
INSERT INTO employee_positions (employee_id, position_title, salary, effective_date)
VALUES (1, 'Senior Developer', 75000, '2024-01-01');

-- Promote employee (end current, start new)
UPDATE employee_positions 
SET end_date = '2024-06-30', is_current = FALSE
WHERE employee_id = 1 AND is_current = TRUE;

INSERT INTO employee_positions (employee_id, position_title, salary, effective_date)
VALUES (1, 'Lead Developer', 85000, '2024-07-01');

-- Query current position
SELECT * FROM employee_positions 
WHERE employee_id = 1 AND is_current = TRUE;

-- Query position at specific date
SELECT * FROM employee_positions 
WHERE employee_id = 1 
AND effective_date <= '2024-05-01' 
AND (end_date IS NULL OR end_date > '2024-05-01');
```

**2. Bitemporal Data (Valid Time + Transaction Time):**
```sql
CREATE TABLE customer_addresses_bitemporal (
    customer_id INT,
    address TEXT,
    -- Valid time (when fact was true in reality)
    valid_from DATE,
    valid_to DATE,
    -- Transaction time (when fact was recorded in database)
    transaction_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_to TIMESTAMP DEFAULT 'infinity',
    PRIMARY KEY (customer_id, valid_from, transaction_from)
);

-- Customer moves on 2024-01-15, but we record it on 2024-01-20
INSERT INTO customer_addresses_bitemporal (
    customer_id, address, valid_from, valid_to, transaction_from
) VALUES (
    1, '123 New Street', '2024-01-15', 'infinity', '2024-01-20 10:00:00'
);

-- Later we discover the move actually happened on 2024-01-10
-- Close the current record
UPDATE customer_addresses_bitemporal 
SET transaction_to = CURRENT_TIMESTAMP
WHERE customer_id = 1 AND transaction_to = 'infinity';

-- Insert corrected record
INSERT INTO customer_addresses_bitemporal (
    customer_id, address, valid_from, valid_to
) VALUES (
    1, '123 New Street', '2024-01-10', 'infinity'
);
```

**3. Data Versioning with Version Numbers:**
```sql
CREATE TABLE document_versions (
    document_id INT,
    version_number INT,
    title VARCHAR(255),
    content TEXT,
    author_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (document_id, version_number)
);

-- Create new version
INSERT INTO document_versions (document_id, version_number, title, content, author_id)
SELECT document_id, MAX(version_number) + 1, 'Updated Title', 'New content', 123
FROM document_versions 
WHERE document_id = 1
GROUP BY document_id;

-- Get latest version
SELECT * FROM document_versions 
WHERE document_id = 1 
ORDER BY version_number DESC 
LIMIT 1;

-- Get published version
SELECT * FROM document_versions 
WHERE document_id = 1 AND is_published = TRUE
ORDER BY version_number DESC 
LIMIT 1;
```

**4. Snapshot Tables:**
```sql
-- Daily snapshots of account balances
CREATE TABLE account_balance_snapshots (
    snapshot_date DATE,
    account_id INT,
    balance DECIMAL(15,2),
    currency VARCHAR(3),
    PRIMARY KEY (snapshot_date, account_id)
);

-- Procedure to create daily snapshot
CREATE OR REPLACE PROCEDURE create_daily_snapshot(p_snapshot_date DATE)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO account_balance_snapshots (snapshot_date, account_id, balance, currency)
    SELECT 
        p_snapshot_date,
        account_id,
        current_balance,
        currency
    FROM accounts
    WHERE status = 'active';
END;
$$;

-- Query balance at specific date
SELECT account_id, balance 
FROM account_balance_snapshots 
WHERE snapshot_date = '2024-01-15';

-- Query balance changes over time
SELECT 
    account_id,
    snapshot_date,
    balance,
    LAG(balance) OVER (PARTITION BY account_id ORDER BY snapshot_date) as previous_balance,
    balance - LAG(balance) OVER (PARTITION BY account_id ORDER BY snapshot_date) as change
FROM account_balance_snapshots
WHERE account_id = 1
ORDER BY snapshot_date;
```

### 30. What are the considerations for designing multi-tenant databases?
**Answer:**

**Multi-Tenancy**: Single application instance serves multiple tenants (customers/organizations).

**1. Shared Database, Shared Schema:**
```sql
-- All tenants share same tables with tenant_id column
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    name VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Row Level Security (RLS) for tenant isolation
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Policy to restrict access to tenant's own data
CREATE POLICY tenant_isolation_customers ON customers
    FOR ALL TO application_role
    USING (tenant_id = current_setting('app.current_tenant_id')::INT);

CREATE POLICY tenant_isolation_orders ON orders
    FOR ALL TO application_role
    USING (tenant_id = current_setting('app.current_tenant_id')::INT);

-- Set tenant context in application
-- SET app.current_tenant_id = 123;
```

**2. Shared Database, Separate Schemas:**
```sql
-- Create schema per tenant
CREATE SCHEMA tenant_123;
CREATE SCHEMA tenant_456;

-- Create tables in each tenant schema
CREATE TABLE tenant_123.customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255)
);

CREATE TABLE tenant_123.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES tenant_123.customers(customer_id)
);

-- Replicate structure for other tenants
CREATE TABLE tenant_456.customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255)
);

-- Function to create tenant schema
CREATE OR REPLACE FUNCTION create_tenant_schema(tenant_id INT)
RETURNS VOID AS $$
DECLARE
    schema_name VARCHAR(50) := 'tenant_' || tenant_id;
BEGIN
    EXECUTE 'CREATE SCHEMA ' || schema_name;
    
    EXECUTE 'CREATE TABLE ' || schema_name || '.customers (
        customer_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(255)
    )';
    
    EXECUTE 'CREATE TABLE ' || schema_name || '.orders (
        order_id SERIAL PRIMARY KEY,
        customer_id INT,
        order_date DATE,
        FOREIGN KEY (customer_id) REFERENCES ' || schema_name || '.customers(customer_id)
    )';
END;
$$ LANGUAGE plpgsql;
```

**3. Separate Databases:**
```sql
-- Database per tenant approach
-- tenant_123_db, tenant_456_db, etc.

-- Connection routing in application layer
-- Based on tenant_id, connect to appropriate database

-- Master tenant registry
CREATE TABLE tenant_registry (
    tenant_id INT PRIMARY KEY,
    tenant_name VARCHAR(100),
    database_name VARCHAR(100),
    connection_string TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tenant_registry (tenant_id, tenant_name, database_name, connection_string)
VALUES 
(123, 'Acme Corp', 'tenant_123_db', 'postgresql://user:pass@host:5432/tenant_123_db'),
(456, 'Beta Inc', 'tenant_456_db', 'postgresql://user:pass@host:5432/tenant_456_db');
```

**4. Hybrid Approach:**
```sql
-- Core shared tables
CREATE TABLE tenants (
    tenant_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    plan VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    username VARCHAR(100),
    email VARCHAR(255),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);

-- Tenant-specific tables with partitioning
CREATE TABLE tenant_data (
    tenant_id INT,
    data_id SERIAL,
    data_type VARCHAR(50),
    data_value JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tenant_id, data_id)
) PARTITION BY HASH (tenant_id);

-- Create partitions for different tenants
CREATE TABLE tenant_data_0 PARTITION OF tenant_data
    FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE tenant_data_1 PARTITION OF tenant_data
    FOR VALUES WITH (modulus 4, remainder 1);
```

**Design Considerations:**

**Security:**
- Data isolation between tenants
- Access control and authentication
- Audit trails per tenant

**Performance:**
- Query performance with large datasets
- Index strategies for multi-tenant queries
- Resource allocation per tenant

**Scalability:**
- Horizontal vs vertical scaling
- Tenant onboarding process
- Database maintenance operations

**Compliance:**
- Data residency requirements
- Tenant-specific compliance needs
- Data retention policies

**Maintenance:**
- Schema migrations across tenants
- Backup and recovery strategies
- Monitoring and alerting per tenant

---

I'll continue with the remaining questions in the next batch. This covers the first 30 basic level questions with comprehensive answers and practical examples.

## Basic Level Questions (31-40)

### 31. What are materialized views and when should you use them?
**Answer:**

**Materialized View**: Physical storage of query results that can be refreshed periodically.

**Regular View vs Materialized View:**
```sql
-- Regular view (virtual table)
CREATE VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Materialized view (physical storage)
CREATE MATERIALIZED VIEW customer_summary_mv AS
SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW customer_summary_mv;

-- Concurrent refresh (PostgreSQL)
REFRESH MATERIALIZED VIEW CONCURRENTLY customer_summary_mv;
```

**When to Use Materialized Views:**
- **Complex aggregations**: Expensive calculations
- **Reporting**: Dashboard queries with historical data
- **Data warehousing**: Pre-computed metrics
- **Performance**: Frequently accessed complex queries

**Refresh Strategies:**
```sql
-- Manual refresh
REFRESH MATERIALIZED VIEW sales_summary;

-- Scheduled refresh (using cron or scheduler)
-- 0 2 * * * psql -d mydb -c "REFRESH MATERIALIZED VIEW sales_summary;"

-- Incremental refresh (custom implementation)
CREATE OR REPLACE FUNCTION refresh_sales_summary_incremental()
RETURNS VOID AS $$
BEGIN
    -- Delete changed records
    DELETE FROM sales_summary_mv 
    WHERE sale_date >= CURRENT_DATE - INTERVAL '1 day';
    
    -- Insert updated records
    INSERT INTO sales_summary_mv
    SELECT 
        sale_date,
        product_category,
        SUM(amount) as total_sales,
        COUNT(*) as transaction_count
    FROM sales
    WHERE sale_date >= CURRENT_DATE - INTERVAL '1 day'
    GROUP BY sale_date, product_category;
END;
$$ LANGUAGE plpgsql;
```

### 32. How do you design databases for high availability?
**Answer:**

**High Availability**: System remains operational with minimal downtime.

**1. Replication Strategies:**
```sql
-- Master-Slave Replication Setup
-- Master database configuration
-- postgresql.conf
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64

-- Create replication user
CREATE USER replicator REPLICATION LOGIN CONNECTION LIMIT 3 ENCRYPTED PASSWORD 'password';

-- Slave database setup
-- recovery.conf
standby_mode = 'on'
primary_conninfo = 'host=master_ip port=5432 user=replicator password=password'
```

**2. Failover Mechanisms:**
```sql
-- Automatic failover with connection pooling
-- pgpool.conf configuration
backend_hostname0 = 'master_db'
backend_port0 = 5432
backend_weight0 = 1
backend_flag0 = 'ALLOW_TO_FAILOVER'

backend_hostname1 = 'slave_db'
backend_port1 = 5432
backend_weight1 = 1
backend_flag1 = 'ALLOW_TO_FAILOVER'

-- Health check configuration
health_check_period = 10
health_check_timeout = 20
health_check_user = 'health_check'
```

**3. Clustering Solutions:**
```sql
-- PostgreSQL Cluster with Patroni
-- patroni.yml configuration
scope: postgres-cluster
name: node1

restapi:
  listen: 0.0.0.0:8008
  connect_address: node1_ip:8008

etcd:
  host: etcd_ip:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 30
    maximum_lag_on_failover: 1048576
```

**4. Backup and Recovery:**
```sql
-- Continuous archiving setup
-- postgresql.conf
archive_mode = on
archive_command = 'cp %p /backup/archive/%f'

-- Point-in-time recovery
-- Create base backup
pg_basebackup -D /backup/base -Ft -z -P -U backup_user

-- Recovery configuration
-- recovery.conf
restore_command = 'cp /backup/archive/%f %p'
recovery_target_time = '2024-01-15 14:30:00'
```

### 33. What is database sharding and how do you implement it?
**Answer:**

**Sharding**: Horizontal partitioning across multiple database instances.

**1. Horizontal Sharding by Key:**
```sql
-- Shard by customer_id hash
-- Shard 1: customer_id % 3 = 0
-- Shard 2: customer_id % 3 = 1  
-- Shard 3: customer_id % 3 = 2

-- Application logic for shard selection
def get_shard_connection(customer_id):
    shard_id = customer_id % 3
    return connections[shard_id]

-- Each shard has same schema
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP
);
```

**2. Range-based Sharding:**
```sql
-- Shard by date ranges
-- Shard 1: 2023 data
-- Shard 2: 2024 data
-- Shard 3: 2025 data

-- Shard routing logic
def get_shard_by_date(order_date):
    year = order_date.year
    if year == 2023:
        return shard_2023
    elif year == 2024:
        return shard_2024
    else:
        return shard_current

-- Each shard contains year-specific data
CREATE TABLE orders_2023 (
    order_id BIGINT PRIMARY KEY,
    customer_id INT,
    order_date DATE CHECK (EXTRACT(YEAR FROM order_date) = 2023),
    total_amount DECIMAL(10,2)
);
```

**3. Directory-based Sharding:**
```sql
-- Shard lookup table
CREATE TABLE shard_directory (
    entity_type VARCHAR(50),
    entity_id BIGINT,
    shard_id INT,
    shard_connection_string TEXT,
    PRIMARY KEY (entity_type, entity_id)
);

-- Lookup shard for specific entity
SELECT shard_connection_string 
FROM shard_directory 
WHERE entity_type = 'customer' AND entity_id = 12345;
```

**4. Cross-shard Queries:**
```sql
-- Federated query across shards
-- Application-level aggregation
def get_customer_total_orders(customer_id):
    results = []
    for shard in all_shards:
        result = shard.execute("""
            SELECT COUNT(*) as order_count
            FROM orders 
            WHERE customer_id = %s
        """, [customer_id])
        results.append(result)
    
    return sum(results)

-- Distributed join using application logic
def get_customer_orders_with_products():
    # Get customers from customer shards
    customers = get_customers_from_shards()
    
    # Get orders for each customer
    for customer in customers:
        shard = get_order_shard(customer.id)
        orders = shard.get_orders(customer.id)
        
        # Get product details from product shards
        for order in orders:
            product_shard = get_product_shard(order.product_id)
            order.product = product_shard.get_product(order.product_id)
```

**Sharding Challenges:**
- **Cross-shard joins**: Complex application logic
- **Rebalancing**: Moving data between shards
- **Hotspots**: Uneven data distribution
- **Transactions**: ACID across multiple shards

### 34. How do you handle database migrations and schema changes?
**Answer:**

**Database Migration**: Systematic way to evolve database schema over time.

**1. Migration Scripts:**
```sql
-- Migration 001: Create initial tables
-- migrations/001_create_customers.sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Migration 002: Add phone column
-- migrations/002_add_customer_phone.sql
ALTER TABLE customers 
ADD COLUMN phone VARCHAR(20);

-- Migration 003: Create orders table
-- migrations/003_create_orders.sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**2. Migration Tracking:**
```sql
-- Schema migrations table
CREATE TABLE schema_migrations (
    version VARCHAR(50) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms INT,
    checksum VARCHAR(64)
);

-- Track applied migrations
INSERT INTO schema_migrations (version, execution_time_ms, checksum)
VALUES ('002_add_customer_phone', 150, 'abc123def456');
```

**3. Rollback Strategies:**
```sql
-- Forward migration
-- migrations/004_add_customer_status_up.sql
ALTER TABLE customers 
ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- Rollback migration  
-- migrations/004_add_customer_status_down.sql
ALTER TABLE customers 
DROP COLUMN status;

-- Safe column addition with default
ALTER TABLE customers 
ADD COLUMN status VARCHAR(20) DEFAULT 'active' NOT NULL;

-- Update existing records if needed
UPDATE customers SET status = 'active' WHERE status IS NULL;
```

**4. Zero-downtime Migrations:**
```sql
-- Step 1: Add new column (nullable)
ALTER TABLE customers 
ADD COLUMN new_email VARCHAR(255);

-- Step 2: Populate new column
UPDATE customers 
SET new_email = email 
WHERE new_email IS NULL;

-- Step 3: Add constraint
ALTER TABLE customers 
ALTER COLUMN new_email SET NOT NULL;

-- Step 4: Add unique constraint
ALTER TABLE customers 
ADD CONSTRAINT unique_new_email UNIQUE (new_email);

-- Step 5: Update application to use new column
-- Deploy application changes

-- Step 6: Drop old column
ALTER TABLE customers 
DROP COLUMN email;

-- Step 7: Rename new column
ALTER TABLE customers 
RENAME COLUMN new_email TO email;
```

**5. Data Migration:**
```sql
-- Complex data transformation
-- Migration: Split full_name into first_name and last_name
ALTER TABLE customers 
ADD COLUMN first_name VARCHAR(50),
ADD COLUMN last_name VARCHAR(50);

-- Migrate existing data
UPDATE customers 
SET 
    first_name = SPLIT_PART(full_name, ' ', 1),
    last_name = CASE 
        WHEN POSITION(' ' IN full_name) > 0 
        THEN SUBSTRING(full_name FROM POSITION(' ' IN full_name) + 1)
        ELSE ''
    END
WHERE first_name IS NULL;

-- Validate migration
SELECT 
    full_name,
    first_name,
    last_name,
    CONCAT(first_name, ' ', last_name) as reconstructed
FROM customers 
WHERE full_name != CONCAT(first_name, ' ', last_name)
LIMIT 10;

-- Drop old column after validation
ALTER TABLE customers DROP COLUMN full_name;
```

### 35. What are database connection pooling and its benefits?
**Answer:**

**Connection Pooling**: Technique to maintain a cache of database connections for reuse.

**1. Connection Pool Configuration:**
```sql
-- PgBouncer configuration (pgbouncer.ini)
[databases]
myapp = host=localhost port=5432 dbname=myapp user=app_user

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = md5
auth_file = userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
max_db_connections = 100
```

**2. Application-level Pooling:**
```python
# Python example with psycopg2
import psycopg2.pool

# Create connection pool
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    host="localhost",
    database="myapp",
    user="app_user",
    password="password"
)

def execute_query(query, params=None):
    conn = None
    try:
        # Get connection from pool
        conn = connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            # Return connection to pool
            connection_pool.putconn(conn)
```

**3. Pool Monitoring:**
```sql
-- Monitor connection usage
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    temp_files,
    temp_bytes
FROM pg_stat_database 
WHERE datname = 'myapp';

-- Check active connections
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    state_change
FROM pg_stat_activity 
WHERE datname = 'myapp';
```

**Benefits:**
- **Performance**: Eliminates connection overhead
- **Resource Management**: Controls database connections
- **Scalability**: Handles more concurrent users
- **Stability**: Prevents connection exhaustion

**Pool Types:**
- **Session Pooling**: One connection per session
- **Transaction Pooling**: Connection returned after transaction
- **Statement Pooling**: Connection returned after each statement

### 36. How do you implement database security best practices?
**Answer:**

**Database Security**: Protecting data from unauthorized access and threats.

**1. Authentication and Authorization:**
```sql
-- Create roles with specific permissions
CREATE ROLE app_read_only;
CREATE ROLE app_read_write;
CREATE ROLE app_admin;

-- Grant table-level permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_read_only;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_read_write;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_admin;

-- Create users and assign roles
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT app_read_write TO app_user;

-- Column-level security
GRANT SELECT (customer_id, name, email) ON customers TO app_read_only;
-- Exclude sensitive columns like SSN, credit_card_number
```

**2. Row Level Security (RLS):**
```sql
-- Enable RLS on table
ALTER TABLE customer_data ENABLE ROW LEVEL SECURITY;

-- Create policy for data access
CREATE POLICY customer_data_policy ON customer_data
    FOR ALL TO app_user
    USING (customer_id = current_setting('app.current_user_id')::INT);

-- Users can only see their own data
SET app.current_user_id = 123;
SELECT * FROM customer_data; -- Only returns data for customer_id = 123
```

**3. Data Encryption:**
```sql
-- Column-level encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt sensitive data
CREATE TABLE secure_customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    ssn_encrypted BYTEA, -- Encrypted SSN
    credit_card_encrypted BYTEA -- Encrypted credit card
);

-- Insert encrypted data
INSERT INTO secure_customers (name, ssn_encrypted, credit_card_encrypted)
VALUES (
    'John Doe',
    pgp_sym_encrypt('123-45-6789', 'encryption_key'),
    pgp_sym_encrypt('4111-1111-1111-1111', 'encryption_key')
);

-- Decrypt data (only with proper key)
SELECT 
    name,
    pgp_sym_decrypt(ssn_encrypted, 'encryption_key') as ssn,
    pgp_sym_decrypt(credit_card_encrypted, 'encryption_key') as credit_card
FROM secure_customers;
```

**4. Audit Logging:**
```sql
-- Enable audit logging
-- postgresql.conf
log_statement = 'all'
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '

-- Custom audit table
CREATE TABLE audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    operation VARCHAR(10),
    user_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_values JSONB,
    new_values JSONB,
    ip_address INET
);

-- Audit trigger
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (
        table_name, operation, user_name, old_values, new_values, ip_address
    ) VALUES (
        TG_TABLE_NAME,
        TG_OP,
        current_user,
        CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP = 'INSERT' THEN row_to_json(NEW) ELSE row_to_json(NEW) END,
        inet_client_addr()
    );
    
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger to sensitive tables
CREATE TRIGGER audit_customers
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

**5. Network Security:**
```sql
-- SSL/TLS configuration
-- postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ca_file = 'ca.crt'

-- Require SSL connections
-- pg_hba.conf
hostssl all all 0.0.0.0/0 md5

-- Connection string with SSL
postgresql://user:password@host:5432/database?sslmode=require
```

**6. Data Masking:**
```sql
-- Create masked view for non-production environments
CREATE VIEW customers_masked AS
SELECT 
    customer_id,
    'Customer_' || customer_id as name, -- Mask real names
    CONCAT('user', customer_id, '@example.com') as email, -- Mask emails
    '***-**-' || RIGHT(ssn, 4) as ssn_masked, -- Mask SSN
    created_at
FROM customers;

-- Grant access to masked view instead of real table
GRANT SELECT ON customers_masked TO dev_users;
REVOKE ALL ON customers FROM dev_users;
```

### 37. What are database performance monitoring techniques?
**Answer:**

**Performance Monitoring**: Tracking database metrics to identify and resolve performance issues.

**1. Query Performance Analysis:**
```sql
-- Enable query statistics
-- postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all

-- Analyze slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Query execution plan analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT c.name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 5;
```

**2. Index Usage Monitoring:**
```sql
-- Check index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;

-- Identify unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes 
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Missing index suggestions
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    seq_tup_read / seq_scan as avg_tup_read
FROM pg_stat_user_tables 
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC;
```

**3. Connection and Lock Monitoring:**
```sql
-- Monitor active connections
SELECT 
    datname,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    now() - query_start as duration,
    query
FROM pg_stat_activity 
WHERE state != 'idle'
ORDER BY query_start;

-- Check for blocking queries
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

**4. Resource Usage Monitoring:**
```sql
-- Database size monitoring
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database 
ORDER BY pg_database_size(datname) DESC;

-- Table size monitoring
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename)) as index_size
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Buffer cache hit ratio
SELECT 
    datname,
    blks_read,
    blks_hit,
    round(blks_hit::numeric / (blks_hit + blks_read) * 100, 2) as hit_ratio
FROM pg_stat_database 
WHERE blks_read > 0;
```

**5. Custom Monitoring Queries:**
```sql
-- Create monitoring views
CREATE VIEW database_health AS
SELECT 
    'connections' as metric,
    count(*) as value,
    current_timestamp as measured_at
FROM pg_stat_activity
UNION ALL
SELECT 
    'active_queries' as metric,
    count(*) as value,
    current_timestamp as measured_at
FROM pg_stat_activity 
WHERE state = 'active'
UNION ALL
SELECT 
    'database_size_mb' as metric,
    pg_database_size(current_database()) / 1024 / 1024 as value,
    current_timestamp as measured_at;

-- Performance metrics collection
CREATE TABLE performance_metrics (
    metric_name VARCHAR(100),
    metric_value NUMERIC,
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automated metrics collection
CREATE OR REPLACE FUNCTION collect_performance_metrics()
RETURNS VOID AS $$
BEGIN
    INSERT INTO performance_metrics (metric_name, metric_value)
    SELECT 
        'avg_query_time_ms',
        AVG(mean_time)
    FROM pg_stat_statements;
    
    INSERT INTO performance_metrics (metric_name, metric_value)
    SELECT 
        'cache_hit_ratio',
        round(sum(blks_hit)::numeric / (sum(blks_hit) + sum(blks_read)) * 100, 2)
    FROM pg_stat_database;
END;
$$ LANGUAGE plpgsql;
```

### 38. How do you design for data archiving and retention?
**Answer:**

**Data Archiving**: Moving old data to separate storage while maintaining accessibility.

**1. Time-based Archiving:**
```sql
-- Create archive tables
CREATE TABLE orders_archive (
    LIKE orders INCLUDING ALL
);

-- Partition main table by date
CREATE TABLE orders (
    order_id BIGSERIAL,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (order_date);

-- Create partitions for different periods
CREATE TABLE orders_2023 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Archive old partitions
CREATE OR REPLACE FUNCTION archive_old_orders(cutoff_date DATE)
RETURNS VOID AS $$
DECLARE
    partition_name TEXT;
BEGIN
    -- Move old partition to archive
    FOR partition_name IN 
        SELECT schemaname||'.'||tablename 
        FROM pg_tables 
        WHERE tablename LIKE 'orders_%' 
        AND tablename < 'orders_' || EXTRACT(YEAR FROM cutoff_date)
    LOOP
        EXECUTE 'ALTER TABLE ' || partition_name || ' SET SCHEMA archive';
        EXECUTE 'CREATE INDEX ON archive.' || split_part(partition_name, '.', 2) || ' (customer_id)';
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

**2. Tiered Storage Strategy:**
```sql
-- Hot tier (current data)
CREATE TABLE transactions_hot (
    transaction_id BIGSERIAL PRIMARY KEY,
    account_id INT,
    amount DECIMAL(15,2),
    transaction_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) WHERE created_at >= CURRENT_DATE - INTERVAL '90 days';

-- Warm tier (recent historical data)
CREATE TABLE transactions_warm (
    transaction_id BIGINT PRIMARY KEY,
    account_id INT,
    amount DECIMAL(15,2),
    transaction_date DATE,
    created_at TIMESTAMP
) WHERE created_at >= CURRENT_DATE - INTERVAL '2 years' 
  AND created_at < CURRENT_DATE - INTERVAL '90 days';

-- Cold tier (old historical data)
CREATE TABLE transactions_cold (
    transaction_id BIGINT PRIMARY KEY,
    account_id INT,
    amount DECIMAL(15,2),
    transaction_date DATE,
    created_at TIMESTAMP,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) WHERE created_at < CURRENT_DATE - INTERVAL '2 years';

-- Union view for seamless access
CREATE VIEW transactions_all AS
SELECT * FROM transactions_hot
UNION ALL
SELECT transaction_id, account_id, amount, transaction_date, created_at 
FROM transactions_warm
UNION ALL
SELECT transaction_id, account_id, amount, transaction_date, created_at 
FROM transactions_cold;
```

**3. Automated Archiving Process:**
```sql
-- Archiving procedure
CREATE OR REPLACE PROCEDURE archive_old_data()
LANGUAGE plpgsql AS $$
DECLARE
    archive_date DATE := CURRENT_DATE - INTERVAL '1 year';
    archived_count INT;
BEGIN
    -- Archive orders
    WITH archived_orders AS (
        DELETE FROM orders 
        WHERE order_date < archive_date
        RETURNING *
    )
    INSERT INTO orders_archive 
    SELECT * FROM archived_orders;
    
    GET DIAGNOSTICS archived_count = ROW_COUNT;
    
    -- Log archiving activity
    INSERT INTO archive_log (table_name, archived_count, archive_date)
    VALUES ('orders', archived_count, CURRENT_TIMESTAMP);
    
    -- Update statistics
    ANALYZE orders_archive;
    
    COMMIT;
END;
$$;

-- Schedule archiving (using pg_cron extension)
SELECT cron.schedule('archive-old-data', '0 2 1 * *', 'CALL archive_old_data();');
```

**4. Data Retention Policies:**
```sql
-- Retention policy configuration
CREATE TABLE retention_policies (
    table_name VARCHAR(100) PRIMARY KEY,
    retention_period INTERVAL,
    archive_enabled BOOLEAN DEFAULT TRUE,
    delete_after_archive BOOLEAN DEFAULT FALSE,
    last_processed TIMESTAMP
);

INSERT INTO retention_policies VALUES
('orders', '2 years', TRUE, FALSE, NULL),
('user_sessions', '30 days', FALSE, TRUE, NULL),
('audit_logs', '7 years', TRUE, FALSE, NULL);

-- Apply retention policies
CREATE OR REPLACE FUNCTION apply_retention_policies()
RETURNS VOID AS $$
DECLARE
    policy RECORD;
    cutoff_date TIMESTAMP;
BEGIN
    FOR policy IN SELECT * FROM retention_policies LOOP
        cutoff_date := CURRENT_TIMESTAMP - policy.retention_period;
        
        IF policy.archive_enabled THEN
            -- Archive old data
            EXECUTE format('
                INSERT INTO %I_archive 
                SELECT * FROM %I 
                WHERE created_at < %L',
                policy.table_name, policy.table_name, cutoff_date);
        END IF;
        
        IF policy.delete_after_archive OR NOT policy.archive_enabled THEN
            -- Delete old data
            EXECUTE format('
                DELETE FROM %I 
                WHERE created_at < %L',
                policy.table_name, cutoff_date);
        END IF;
        
        -- Update last processed timestamp
        UPDATE retention_policies 
        SET last_processed = CURRENT_TIMESTAMP 
        WHERE table_name = policy.table_name;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### 39. What are common data modeling mistakes and how to avoid them?
**Answer:**

**Common Data Modeling Mistakes** and their solutions:

**1. Over-normalization:**
```sql
-- MISTAKE: Excessive normalization hurting performance
CREATE TABLE addresses (
    address_id SERIAL PRIMARY KEY,
    street_number VARCHAR(10),
    street_name VARCHAR(100),
    street_type_id INT, -- References street_types table
    city_id INT,        -- References cities table
    state_id INT,       -- References states table
    country_id INT      -- References countries table
);

CREATE TABLE street_types (
    street_type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(20) -- 'Street', 'Avenue', 'Boulevard'
);

-- SOLUTION: Reasonable denormalization for performance
CREATE TABLE addresses (
    address_id SERIAL PRIMARY KEY,
    street_number VARCHAR(10),
    street_name VARCHAR(100),
    street_type VARCHAR(20), -- Denormalized
    city VARCHAR(100),       -- Denormalized
    state VARCHAR(50),       -- Denormalized
    country VARCHAR(50),     -- Denormalized
    postal_code VARCHAR(20)
);
```

**2. Inadequate Primary Keys:**
```sql
-- MISTAKE: Using business data as primary key
CREATE TABLE customers (
    email VARCHAR(255) PRIMARY KEY, -- Business data can change
    name VARCHAR(100),
    phone VARCHAR(20)
);

-- SOLUTION: Use surrogate keys
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY, -- Surrogate key
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    phone VARCHAR(20)
);
```

**3. Missing Constraints:**
```sql
-- MISTAKE: No data validation
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(50)
);

-- SOLUTION: Proper constraints
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    status VARCHAR(50) NOT NULL DEFAULT 'pending' 
        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**4. Ignoring Indexing Strategy:**
```sql
-- MISTAKE: No indexes on frequently queried columns
CREATE TABLE user_activities (
    activity_id BIGSERIAL PRIMARY KEY,
    user_id INT,
    activity_type VARCHAR(50),
    activity_date TIMESTAMP,
    data JSONB
);

-- SOLUTION: Strategic indexing
CREATE TABLE user_activities (
    activity_id BIGSERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data JSONB
);

-- Add appropriate indexes
CREATE INDEX idx_user_activities_user_id ON user_activities(user_id);
CREATE INDEX idx_user_activities_date ON user_activities(activity_date);
CREATE INDEX idx_user_activities_type ON user_activities(activity_type);
CREATE INDEX idx_user_activities_user_date ON user_activities(user_id, activity_date);
```

**5. Poor Handling of Hierarchical Data:**
```sql
-- MISTAKE: Inefficient adjacency list for deep hierarchies
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_id INT
);

-- Querying all descendants requires recursive queries
WITH RECURSIVE category_tree AS (
    SELECT category_id, name, parent_id, 0 as level
    FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.category_id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.category_id
)
SELECT * FROM category_tree;

-- SOLUTION: Consider nested sets or closure tables for read-heavy scenarios
CREATE TABLE category_closure (
    ancestor_id INT,
    descendant_id INT,
    depth INT,
    PRIMARY KEY (ancestor_id, descendant_id)
);

-- Efficient descendant query
SELECT c.name 
FROM categories c
JOIN category_closure cc ON c.category_id = cc.descendant_id
WHERE cc.ancestor_id = 1;
```

**6. Inconsistent Naming Conventions:**
```sql
-- MISTAKE: Inconsistent naming
CREATE TABLE Customer (           -- Mixed case
    CustomerID INT,              -- PascalCase
    customer_name VARCHAR(100),  -- snake_case
    emailAddress VARCHAR(255),   -- camelCase
    Phone VARCHAR(20)            -- No prefix/suffix consistency
);

-- SOLUTION: Consistent naming convention
CREATE TABLE customers (         -- Plural, lowercase
    customer_id SERIAL PRIMARY KEY,  -- snake_case throughout
    customer_name VARCHAR(100) NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20)
);
```

**7. Not Planning for Growth:**
```sql
-- MISTAKE: Fixed-size fields that may not scale
CREATE TABLE products (
    product_id INT PRIMARY KEY,     -- May run out of INT range
    sku VARCHAR(10),               -- May need longer SKUs
    price DECIMAL(8,2)             -- May need higher precision
);

-- SOLUTION: Plan for growth
CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,  -- BIGINT for large scale
    sku VARCHAR(50),                   -- Flexible SKU length
    price DECIMAL(15,4),               -- Higher precision for international
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 40. How do you implement data quality checks in database design?
**Answer:**

**Data Quality**: Ensuring data is accurate, complete, consistent, and reliable.

**1. Constraint-based Quality Checks:**
```sql
-- Domain constraints
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL 
        CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    age INT CHECK (age >= 0 AND age <= 150),
    phone VARCHAR(20) CHECK (phone ~ '^\+?[1-9]\d{1,14}$'),
    registration_date DATE NOT NULL 
        CHECK (registration_date <= CURRENT_DATE),
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'suspended', 'deleted'))
);

-- Referential integrity
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount > 0),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);
```

**2. Custom Validation Functions:**
```sql
-- Credit card validation function
CREATE OR REPLACE FUNCTION validate_credit_card(card_number TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    cleaned_number TEXT;
    digit_sum INT := 0;
    digit INT;
    i INT;
BEGIN
    -- Remove spaces and dashes
    cleaned_number := regexp_replace(card_number, '[^0-9]', '', 'g');
    
    -- Check length
    IF length(cleaned_number) NOT BETWEEN 13 AND 19 THEN
        RETURN FALSE;
    END IF;
    
    -- Luhn algorithm
    FOR i IN 1..length(cleaned_number) LOOP
        digit := substring(cleaned_number, length(cleaned_number) - i + 1, 1)::INT;
        
        IF i % 2 = 0 THEN
            digit := digit * 2;
            IF digit > 9 THEN
                digit := digit - 9;
            END IF;
        END IF;
        
        digit_sum := digit_sum + digit;
    END LOOP;
    
    RETURN digit_sum % 10 = 0;
END;
$$ LANGUAGE plpgsql;

-- Use validation in table constraint
ALTER TABLE payment_methods 
ADD CONSTRAINT valid_credit_card 
CHECK (validate_credit_card(card_number));
```

**3. Data Quality Monitoring:**
```sql
-- Data quality metrics table
CREATE TABLE data_quality_metrics (
    metric_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    metric_type VARCHAR(50), -- 'completeness', 'uniqueness', 'validity'
    metric_value DECIMAL(5,2),
    threshold_value DECIMAL(5,2),
    status VARCHAR(20), -- 'pass', 'fail', 'warning'
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Completeness check
CREATE OR REPLACE FUNCTION check_completeness(
    p_table_name TEXT,
    p_column_name TEXT,
    p_threshold DECIMAL DEFAULT 95.0
)
RETURNS VOID AS $$
DECLARE
    total_count INT;
    non_null_count INT;
    completeness_pct DECIMAL(5,2);
    status VARCHAR(20);
BEGIN
    -- Count total and non-null records
    EXECUTE format('SELECT COUNT(*) FROM %I', p_table_name) INTO total_count;
    EXECUTE format('SELECT COUNT(%I) FROM %I', p_column_name, p_table_name) INTO non_null_count;
    
    -- Calculate completeness percentage
    completeness_pct := (non_null_count::DECIMAL / total_count) * 100;
    
    -- Determine status
    status := CASE 
        WHEN completeness_pct >= p_threshold THEN 'pass'
        WHEN completeness_pct >= p_threshold * 0.9 THEN 'warning'
        ELSE 'fail'
    END;
    
    -- Insert metric
    INSERT INTO data_quality_metrics (
        table_name, column_name, metric_type, metric_value, threshold_value, status
    ) VALUES (
        p_table_name, p_column_name, 'completeness', completeness_pct, p_threshold, status
    );
END;
$$ LANGUAGE plpgsql;

-- Uniqueness check
CREATE OR REPLACE FUNCTION check_uniqueness(
    p_table_name TEXT,
    p_column_name TEXT,
    p_threshold DECIMAL DEFAULT 100.0
)
RETURNS VOID AS $$
DECLARE
    total_count INT;
    unique_count INT;
    uniqueness_pct DECIMAL(5,2);
    status VARCHAR(20);
BEGIN
    EXECUTE format('SELECT COUNT(*) FROM %I', p_table_name) INTO total_count;
    EXECUTE format('SELECT COUNT(DISTINCT %I) FROM %I', p_column_name, p_table_name) INTO unique_count;
    
    uniqueness_pct := (unique_count::DECIMAL / total_count) * 100;
    
    status := CASE 
        WHEN uniqueness_pct >= p_threshold THEN 'pass'
        WHEN uniqueness_pct >= p_threshold * 0.95 THEN 'warning'
        ELSE 'fail'
    END;
    
    INSERT INTO data_quality_metrics (
        table_name, column_name, metric_type, metric_value, threshold_value, status
    ) VALUES (
        p_table_name, p_column_name, 'uniqueness', uniqueness_pct, p_threshold, status
    );
END;
$$ LANGUAGE plpgsql;
```

**4. Data Quality Rules Engine:**
```sql
-- Data quality rules configuration
CREATE TABLE data_quality_rules (
    rule_id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100),
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    rule_type VARCHAR(50), -- 'range', 'pattern', 'lookup', 'custom'
    rule_definition JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample rules
INSERT INTO data_quality_rules (rule_name, table_name, column_name, rule_type, rule_definition) VALUES
('email_format', 'customers', 'email', 'pattern', '{"pattern": "^[\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,}$"}'),
('age_range', 'customers', 'age', 'range', '{"min": 0, "max": 150}'),
('valid_status', 'orders', 'status', 'lookup', '{"values": ["pending", "processing", "shipped", "delivered", "cancelled"]}');

-- Rule execution function
CREATE OR REPLACE FUNCTION execute_quality_rules()
RETURNS TABLE(rule_name TEXT, violations_count INT) AS $$
DECLARE
    rule RECORD;
    violation_count INT;
    query_text TEXT;
BEGIN
    FOR rule IN SELECT * FROM data_quality_rules WHERE is_active = TRUE LOOP
        CASE rule.rule_type
            WHEN 'pattern' THEN
                query_text := format('SELECT COUNT(*) FROM %I WHERE %I !~ %L',
                    rule.table_name, rule.column_name, rule.rule_definition->>'pattern');
            WHEN 'range' THEN
                query_text := format('SELECT COUNT(*) FROM %I WHERE %I NOT BETWEEN %s AND %s',
                    rule.table_name, rule.column_name, 
                    rule.rule_definition->>'min', rule.rule_definition->>'max');
            WHEN 'lookup' THEN
                query_text := format('SELECT COUNT(*) FROM %I WHERE %I NOT IN (%s)',
                    rule.table_name, rule.column_name,
                    array_to_string(ARRAY(SELECT jsonb_array_elements_text(rule.rule_definition->'values')), ','));
        END CASE;
        
        EXECUTE query_text INTO violation_count;
        
        RETURN QUERY SELECT rule.rule_name, violation_count;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

**5. Automated Quality Reporting:**
```sql
-- Quality dashboard view
CREATE VIEW data_quality_dashboard AS
SELECT 
    table_name,
    COUNT(*) as total_checks,
    COUNT(*) FILTER (WHERE status = 'pass') as passed_checks,
    COUNT(*) FILTER (WHERE status = 'warning') as warning_checks,
    COUNT(*) FILTER (WHERE status = 'fail') as failed_checks,
    ROUND(COUNT(*) FILTER (WHERE status = 'pass')::DECIMAL / COUNT(*) * 100, 2) as pass_rate,
    MAX(measured_at) as last_check
FROM data_quality_metrics
WHERE measured_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY table_name
ORDER BY pass_rate DESC;

-- Quality trend analysis
CREATE VIEW data_quality_trends AS
SELECT 
    table_name,
    column_name,
    metric_type,
    DATE_TRUNC('day', measured_at) as check_date,
    AVG(metric_value) as avg_metric_value,
    MIN(metric_value) as min_metric_value,
    MAX(metric_value) as max_metric_value
FROM data_quality_metrics
WHERE measured_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY table_name, column_name, metric_type, DATE_TRUNC('day', measured_at)
ORDER BY table_name, column_name, check_date;
```

---

This completes the first 40 basic level questions. Each question includes comprehensive answers with practical SQL examples and real-world scenarios.
## Basic Level Questions (41-50)

### 41. What is the difference between OLTP and OLAP systems?
**Answer:**

**OLTP (Online Transaction Processing)** vs **OLAP (Online Analytical Processing)**:

| Aspect | OLTP | OLAP |
|--------|------|------|
| **Purpose** | Day-to-day operations | Business intelligence and reporting |
| **Data Model** | Normalized (3NF) | Denormalized (Star/Snowflake) |
| **Query Type** | Simple, frequent | Complex, ad-hoc |
| **Data Volume** | Current data | Historical data |
| **Response Time** | Milliseconds | Seconds to minutes |
| **Users** | Many concurrent users | Fewer analytical users |
| **Updates** | Frequent INSERT/UPDATE/DELETE | Batch loads, rare updates |

**OLTP Example:**
```sql
-- E-commerce transaction system
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Typical OLTP queries
INSERT INTO orders (customer_id, total_amount) VALUES (123, 99.99);
UPDATE orders SET status = 'shipped' WHERE order_id = 456;
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
```

**OLAP Example:**
```sql
-- Data warehouse fact table
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT,
    product_key INT,
    customer_key INT,
    store_key INT,
    quantity_sold INT,
    revenue DECIMAL(12,2),
    cost DECIMAL(12,2),
    profit DECIMAL(12,2)
);

-- Typical OLAP queries
SELECT 
    d.year,
    d.quarter,
    p.category,
    SUM(f.revenue) as total_revenue,
    SUM(f.profit) as total_profit
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
WHERE d.year IN (2023, 2024)
GROUP BY d.year, d.quarter, p.category
ORDER BY d.year, d.quarter, total_revenue DESC;
```

### 42. How do you model many-to-many relationships with attributes?
**Answer:**

**Associative Entity**: Junction table with additional attributes beyond the foreign keys.

**Example: Students and Courses with Enrollment Details**
```sql
-- Basic entities
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(255)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(10),
    course_name VARCHAR(100),
    credits INT
);

-- Associative entity with additional attributes
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    semester VARCHAR(20),
    year INT,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    grade VARCHAR(2),
    status VARCHAR(20) DEFAULT 'enrolled',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE(student_id, course_id, semester, year)
);

-- Query examples
-- Get all courses for a student in a specific semester
SELECT c.course_code, c.course_name, e.grade, e.status
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
WHERE e.student_id = 123 AND e.semester = 'Fall' AND e.year = 2024;

-- Get enrollment statistics by course
SELECT 
    c.course_name,
    COUNT(*) as total_enrollments,
    AVG(CASE WHEN e.grade IN ('A', 'B', 'C', 'D', 'F') 
        THEN CASE e.grade 
            WHEN 'A' THEN 4.0 
            WHEN 'B' THEN 3.0 
            WHEN 'C' THEN 2.0 
            WHEN 'D' THEN 1.0 
            WHEN 'F' THEN 0.0 
        END 
    END) as avg_gpa
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
WHERE e.semester = 'Fall' AND e.year = 2024
GROUP BY c.course_id, c.course_name;
```

### 43. What are database design patterns for handling money and currency?
**Answer:**

**Money Handling**: Critical considerations for financial data accuracy.

**1. Decimal Precision:**
```sql
-- WRONG: Using FLOAT for money (precision issues)
CREATE TABLE transactions_bad (
    transaction_id SERIAL PRIMARY KEY,
    amount FLOAT -- Precision errors!
);

-- CORRECT: Using DECIMAL for exact precision
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    amount DECIMAL(15,4), -- 15 digits total, 4 decimal places
    currency_code CHAR(3) DEFAULT 'USD'
);
```

**2. Multi-Currency Support:**
```sql
-- Currency reference table
CREATE TABLE currencies (
    currency_code CHAR(3) PRIMARY KEY,
    currency_name VARCHAR(100),
    decimal_places INT DEFAULT 2,
    symbol VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO currencies VALUES
('USD', 'US Dollar', 2, '$', TRUE),
('EUR', 'Euro', 2, '€', TRUE),
('JPY', 'Japanese Yen', 0, '¥', TRUE),
('BTC', 'Bitcoin', 8, '₿', TRUE);

-- Transactions with currency
CREATE TABLE financial_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    amount DECIMAL(20,8), -- Support crypto precision
    currency_code CHAR(3) NOT NULL,
    base_amount DECIMAL(20,8), -- Amount in base currency (USD)
    exchange_rate DECIMAL(12,6),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (currency_code) REFERENCES currencies(currency_code)
);
```

**3. Exchange Rate Handling:**
```sql
-- Historical exchange rates
CREATE TABLE exchange_rates (
    rate_id SERIAL PRIMARY KEY,
    from_currency CHAR(3),
    to_currency CHAR(3),
    rate DECIMAL(12,6),
    effective_date DATE,
    source VARCHAR(50), -- 'central_bank', 'market', etc.
    PRIMARY KEY (from_currency, to_currency, effective_date)
);

-- Function to convert currency
CREATE OR REPLACE FUNCTION convert_currency(
    p_amount DECIMAL(20,8),
    p_from_currency CHAR(3),
    p_to_currency CHAR(3),
    p_date DATE DEFAULT CURRENT_DATE
)
RETURNS DECIMAL(20,8) AS $$
DECLARE
    v_rate DECIMAL(12,6);
BEGIN
    IF p_from_currency = p_to_currency THEN
        RETURN p_amount;
    END IF;
    
    SELECT rate INTO v_rate
    FROM exchange_rates
    WHERE from_currency = p_from_currency
    AND to_currency = p_to_currency
    AND effective_date <= p_date
    ORDER BY effective_date DESC
    LIMIT 1;
    
    IF v_rate IS NULL THEN
        RAISE EXCEPTION 'Exchange rate not found for % to % on %', 
            p_from_currency, p_to_currency, p_date;
    END IF;
    
    RETURN p_amount * v_rate;
END;
$$ LANGUAGE plpgsql;
```

**4. Money Data Type (PostgreSQL):**
```sql
-- Using built-in MONEY type
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    amount MONEY, -- Built-in money type
    currency_code CHAR(3) DEFAULT 'USD'
);

-- Set locale for money formatting
SET lc_monetary = 'en_US.UTF-8';
INSERT INTO payments (amount) VALUES ('$1,234.56');
```

### 44. How do you design for data consistency across distributed systems?
**Answer:**

**Distributed Data Consistency**: Ensuring data remains consistent across multiple database instances.

**1. Two-Phase Commit (2PC):**
```sql
-- Coordinator database
CREATE TABLE distributed_transactions (
    transaction_id UUID PRIMARY KEY,
    status VARCHAR(20), -- 'preparing', 'committed', 'aborted'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    participants TEXT[] -- Array of participant database URLs
);

-- Participant preparation
CREATE OR REPLACE FUNCTION prepare_transaction(p_transaction_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    -- Validate transaction can be committed
    -- Lock resources
    -- Return TRUE if can commit, FALSE otherwise
    
    -- Log preparation
    INSERT INTO transaction_log (transaction_id, phase, status)
    VALUES (p_transaction_id, 'prepare', 'ready');
    
    RETURN TRUE;
EXCEPTION
    WHEN OTHERS THEN
        INSERT INTO transaction_log (transaction_id, phase, status, error_message)
        VALUES (p_transaction_id, 'prepare', 'failed', SQLERRM);
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;
```

**2. Saga Pattern:**
```sql
-- Saga orchestration table
CREATE TABLE saga_transactions (
    saga_id UUID PRIMARY KEY,
    saga_type VARCHAR(50),
    current_step INT DEFAULT 1,
    status VARCHAR(20) DEFAULT 'running',
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE saga_steps (
    step_id SERIAL PRIMARY KEY,
    saga_id UUID,
    step_number INT,
    service_name VARCHAR(100),
    action VARCHAR(100),
    compensation_action VARCHAR(100),
    status VARCHAR(20), -- 'pending', 'completed', 'failed', 'compensated'
    request_data JSONB,
    response_data JSONB,
    executed_at TIMESTAMP,
    FOREIGN KEY (saga_id) REFERENCES saga_transactions(saga_id)
);

-- Example: Order processing saga
INSERT INTO saga_transactions (saga_id, saga_type, data) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'order_processing', 
 '{"order_id": 123, "customer_id": 456, "amount": 99.99}');

INSERT INTO saga_steps (saga_id, step_number, service_name, action, compensation_action) VALUES
('550e8400-e29b-41d4-a716-446655440000', 1, 'inventory_service', 'reserve_items', 'release_items'),
('550e8400-e29b-41d4-a716-446655440000', 2, 'payment_service', 'charge_payment', 'refund_payment'),
('550e8400-e29b-41d4-a716-446655440000', 3, 'shipping_service', 'create_shipment', 'cancel_shipment');
```

**3. Event Sourcing:**
```sql
-- Event store
CREATE TABLE event_store (
    event_id UUID PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    event_version INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(aggregate_id, event_version)
);

-- Example events for order aggregate
INSERT INTO event_store (event_id, aggregate_id, aggregate_type, event_type, event_data, event_version) VALUES
(gen_random_uuid(), '123e4567-e89b-12d3-a456-426614174000', 'Order', 'OrderCreated', 
 '{"customer_id": 456, "items": [{"product_id": 789, "quantity": 2}]}', 1),
(gen_random_uuid(), '123e4567-e89b-12d3-a456-426614174000', 'Order', 'PaymentProcessed',
 '{"payment_id": "pay_123", "amount": 99.99}', 2),
(gen_random_uuid(), '123e4567-e89b-12d3-a456-426614174000', 'Order', 'OrderShipped',
 '{"tracking_number": "TRK123456", "carrier": "UPS"}', 3);

-- Rebuild aggregate state from events
CREATE OR REPLACE FUNCTION rebuild_order_state(p_order_id UUID)
RETURNS JSONB AS $$
DECLARE
    event RECORD;
    order_state JSONB := '{}';
BEGIN
    FOR event IN 
        SELECT event_type, event_data 
        FROM event_store 
        WHERE aggregate_id = p_order_id 
        ORDER BY event_version
    LOOP
        CASE event.event_type
            WHEN 'OrderCreated' THEN
                order_state := order_state || event.event_data || '{"status": "created"}';
            WHEN 'PaymentProcessed' THEN
                order_state := order_state || '{"status": "paid"}' || jsonb_build_object('payment', event.event_data);
            WHEN 'OrderShipped' THEN
                order_state := order_state || '{"status": "shipped"}' || jsonb_build_object('shipping', event.event_data);
        END CASE;
    END LOOP;
    
    RETURN order_state;
END;
$$ LANGUAGE plpgsql;
```

### 45. What are the considerations for designing real-time data models?
**Answer:**

**Real-time Data Modeling**: Designing for low-latency, high-throughput data processing.

**1. Time-Series Optimization:**
```sql
-- Optimized for time-series inserts
CREATE TABLE sensor_readings (
    sensor_id INT,
    timestamp TIMESTAMP,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    pressure DECIMAL(7,2),
    PRIMARY KEY (sensor_id, timestamp)
) PARTITION BY RANGE (timestamp);

-- Create time-based partitions
CREATE TABLE sensor_readings_2024_01 PARTITION OF sensor_readings
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Indexes for real-time queries
CREATE INDEX idx_sensor_readings_timestamp ON sensor_readings (timestamp DESC);
CREATE INDEX idx_sensor_readings_sensor_time ON sensor_readings (sensor_id, timestamp DESC);
```

**2. Streaming Data Structure:**
```sql
-- Event stream table
CREATE TABLE event_stream (
    event_id BIGSERIAL,
    event_type VARCHAR(50),
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    partition_key VARCHAR(100), -- For sharding
    event_data JSONB,
    processed BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (partition_key, event_id)
) PARTITION BY HASH (partition_key);

-- Create hash partitions for parallel processing
CREATE TABLE event_stream_0 PARTITION OF event_stream
    FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE event_stream_1 PARTITION OF event_stream
    FOR VALUES WITH (modulus 4, remainder 1);
CREATE TABLE event_stream_2 PARTITION OF event_stream
    FOR VALUES WITH (modulus 4, remainder 2);
CREATE TABLE event_stream_3 PARTITION OF event_stream
    FOR VALUES WITH (modulus 4, remainder 3);
```

**3. Real-time Aggregation Tables:**
```sql
-- Pre-computed aggregations for real-time dashboards
CREATE TABLE real_time_metrics (
    metric_key VARCHAR(100),
    time_window TIMESTAMP,
    window_size INTERVAL,
    metric_value DECIMAL(15,4),
    sample_count INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (metric_key, time_window, window_size)
);

-- Function to update real-time metrics
CREATE OR REPLACE FUNCTION update_real_time_metric(
    p_metric_key VARCHAR(100),
    p_value DECIMAL(15,4),
    p_window_size INTERVAL DEFAULT '1 minute'
)
RETURNS VOID AS $$
DECLARE
    v_time_window TIMESTAMP;
BEGIN
    -- Round timestamp to window boundary
    v_time_window := date_trunc('minute', CURRENT_TIMESTAMP);
    
    -- Upsert metric value
    INSERT INTO real_time_metrics (metric_key, time_window, window_size, metric_value, sample_count)
    VALUES (p_metric_key, v_time_window, p_window_size, p_value, 1)
    ON CONFLICT (metric_key, time_window, window_size)
    DO UPDATE SET
        metric_value = (real_time_metrics.metric_value * real_time_metrics.sample_count + p_value) / (real_time_metrics.sample_count + 1),
        sample_count = real_time_metrics.sample_count + 1,
        last_updated = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;
```

**4. Change Data Capture (CDC) Model:**
```sql
-- CDC log table
CREATE TABLE change_log (
    change_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    operation VARCHAR(10), -- INSERT, UPDATE, DELETE
    record_id VARCHAR(100),
    old_values JSONB,
    new_values JSONB,
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_id BIGINT
);

-- Trigger for CDC
CREATE OR REPLACE FUNCTION cdc_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO change_log (
        table_name, operation, record_id, old_values, new_values, transaction_id
    ) VALUES (
        TG_TABLE_NAME,
        TG_OP,
        CASE 
            WHEN TG_OP = 'DELETE' THEN OLD.id::TEXT
            ELSE NEW.id::TEXT
        END,
        CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP = 'INSERT' THEN row_to_json(NEW) ELSE row_to_json(NEW) END,
        txid_current()
    );
    
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$ LANGUAGE plpgsql;
```

### 46. How do you handle data modeling for microservices architecture?
**Answer:**

**Microservices Data Modeling**: Each service owns its data with bounded contexts.

**1. Database per Service:**
```sql
-- User Service Database
CREATE DATABASE user_service;

-- User service tables
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    bio TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Order Service Database  
CREATE DATABASE order_service;

-- Order service tables (separate database)
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID, -- Reference to user service (no FK constraint)
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
    item_id UUID PRIMARY KEY,
    order_id UUID,
    product_id UUID, -- Reference to product service
    quantity INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

**2. Event-Driven Data Synchronization:**
```sql
-- Event outbox pattern
CREATE TABLE outbox_events (
    event_id UUID PRIMARY KEY,
    aggregate_id UUID,
    event_type VARCHAR(100),
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- Trigger to publish events
CREATE OR REPLACE FUNCTION publish_user_event()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO outbox_events (event_id, aggregate_id, event_type, event_data)
    VALUES (
        gen_random_uuid(),
        NEW.user_id,
        CASE 
            WHEN TG_OP = 'INSERT' THEN 'UserCreated'
            WHEN TG_OP = 'UPDATE' THEN 'UserUpdated'
        END,
        row_to_json(NEW)
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_event_trigger
    AFTER INSERT OR UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION publish_user_event();
```

**3. Saga Pattern for Distributed Transactions:**
```sql
-- Order service saga state
CREATE TABLE order_saga (
    saga_id UUID PRIMARY KEY,
    order_id UUID,
    current_step VARCHAR(50),
    saga_data JSONB,
    status VARCHAR(20) DEFAULT 'started',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Saga step definitions
CREATE TABLE saga_step_definitions (
    step_name VARCHAR(50) PRIMARY KEY,
    service_name VARCHAR(50),
    action VARCHAR(100),
    compensation_action VARCHAR(100)
);

INSERT INTO saga_step_definitions VALUES
('reserve_inventory', 'inventory_service', 'reserve_items', 'release_items'),
('process_payment', 'payment_service', 'charge_card', 'refund_payment'),
('create_shipment', 'shipping_service', 'create_shipment', 'cancel_shipment');
```

**4. API Composition and Data Aggregation:**
```sql
-- Read model for cross-service queries
CREATE TABLE order_summary_view (
    order_id UUID PRIMARY KEY,
    user_id UUID,
    username VARCHAR(50), -- Denormalized from user service
    user_email VARCHAR(255), -- Denormalized from user service
    order_date TIMESTAMP,
    status VARCHAR(20),
    total_amount DECIMAL(10,2),
    item_count INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Update read model when events are received
CREATE OR REPLACE FUNCTION update_order_summary(
    p_event_type VARCHAR(100),
    p_event_data JSONB
)
RETURNS VOID AS $$
BEGIN
    CASE p_event_type
        WHEN 'OrderCreated' THEN
            INSERT INTO order_summary_view (
                order_id, user_id, order_date, status, total_amount, item_count
            ) VALUES (
                (p_event_data->>'order_id')::UUID,
                (p_event_data->>'user_id')::UUID,
                (p_event_data->>'order_date')::TIMESTAMP,
                p_event_data->>'status',
                (p_event_data->>'total_amount')::DECIMAL,
                (p_event_data->>'item_count')::INT
            );
        WHEN 'UserUpdated' THEN
            UPDATE order_summary_view 
            SET username = p_event_data->>'username',
                user_email = p_event_data->>'email',
                last_updated = CURRENT_TIMESTAMP
            WHERE user_id = (p_event_data->>'user_id')::UUID;
    END CASE;
END;
$$ LANGUAGE plpgsql;
```

### 47. What are the best practices for handling NULL values in data models?
**Answer:**

**NULL Handling**: Strategies for dealing with missing or unknown data.

**1. Understanding NULL Semantics:**
```sql
-- NULL behavior examples
SELECT 
    NULL = NULL,        -- Returns NULL (not TRUE)
    NULL <> NULL,       -- Returns NULL (not FALSE)
    NULL IS NULL,       -- Returns TRUE
    NULL IS NOT NULL,   -- Returns FALSE
    1 + NULL,          -- Returns NULL
    'Hello' || NULL;   -- Returns NULL

-- Three-valued logic with NULLs
CREATE TABLE test_nulls (
    id INT,
    value INT
);

INSERT INTO test_nulls VALUES (1, 10), (2, NULL), (3, 20);

-- These queries behave differently
SELECT * FROM test_nulls WHERE value = 10;     -- Returns 1 row
SELECT * FROM test_nulls WHERE value <> 10;    -- Returns 1 row (not 2!)
SELECT * FROM test_nulls WHERE value IS NULL;  -- Returns 1 row
```

**2. NULL Constraints and Defaults:**
```sql
-- Explicit NULL handling
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,           -- Required field
    phone VARCHAR(20),                     -- Optional field (allows NULL)
    middle_name VARCHAR(50),               -- Optional field
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    last_login TIMESTAMP,                  -- NULL means never logged in
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    
    -- Check constraints with NULL handling
    CONSTRAINT valid_phone CHECK (phone IS NULL OR phone ~ '^\+?[1-9]\d{1,14}$')
);

-- Handle NULLs in business logic
CREATE OR REPLACE FUNCTION get_customer_display_name(
    p_first_name VARCHAR(50),
    p_middle_name VARCHAR(50),
    p_last_name VARCHAR(50)
)
RETURNS VARCHAR(200) AS $$
BEGIN
    RETURN TRIM(
        COALESCE(p_first_name, '') || ' ' ||
        COALESCE(p_middle_name || ' ', '') ||
        COALESCE(p_last_name, '')
    );
END;
$$ LANGUAGE plpgsql;
```

**3. NULL-Safe Operations:**
```sql
-- Safe aggregations with NULLs
SELECT 
    COUNT(*) as total_customers,           -- Counts all rows
    COUNT(phone) as customers_with_phone,  -- Counts non-NULL phones
    COUNT(DISTINCT phone) as unique_phones, -- Counts distinct non-NULL phones
    AVG(COALESCE(rating, 0)) as avg_rating_zero_default,
    AVG(rating) as avg_rating_null_ignored -- NULLs ignored in AVG
FROM customers;

-- NULL-safe comparisons
SELECT *
FROM products p1
JOIN products p2 ON (
    p1.category = p2.category OR 
    (p1.category IS NULL AND p2.category IS NULL)
);

-- Using COALESCE for NULL handling
SELECT 
    customer_id,
    COALESCE(phone, 'No phone provided') as phone_display,
    COALESCE(last_login, registration_date) as last_activity,
    COALESCE(middle_name, '') as middle_name_safe
FROM customers;
```

**4. Alternative Approaches to NULLs:**
```sql
-- Option 1: Use sentinel values instead of NULL
CREATE TABLE products_sentinel (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1000) NOT NULL DEFAULT 'No description available',
    weight_grams INT NOT NULL DEFAULT -1, -- -1 means unknown weight
    discontinued_date DATE NOT NULL DEFAULT '9999-12-31' -- Far future means active
);

-- Option 2: Separate tables for optional data
CREATE TABLE customers_required (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    registration_date DATE NOT NULL
);

CREATE TABLE customer_optional_data (
    customer_id INT PRIMARY KEY,
    phone VARCHAR(20),
    middle_name VARCHAR(50),
    last_login TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers_required(customer_id)
);

-- Option 3: JSON for optional fields
CREATE TABLE customers_json (
    customer_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    required_data JSONB NOT NULL,
    optional_data JSONB -- Can be NULL or contain optional fields
);

INSERT INTO customers_json VALUES (
    1, 
    'john@email.com',
    '{"registration_date": "2024-01-15"}',
    '{"phone": "555-1234", "preferences": {"newsletter": true}}'
);
```

**5. NULL Handling in Queries:**
```sql
-- Safe sorting with NULLs
SELECT customer_id, last_login
FROM customers
ORDER BY last_login NULLS LAST; -- NULLs at the end

-- Conditional logic with NULLs
SELECT 
    customer_id,
    CASE 
        WHEN last_login IS NULL THEN 'Never logged in'
        WHEN last_login < CURRENT_DATE - INTERVAL '30 days' THEN 'Inactive'
        ELSE 'Active'
    END as activity_status
FROM customers;

-- Window functions with NULL handling
SELECT 
    customer_id,
    order_date,
    total_amount,
    -- Fill NULLs with previous non-NULL value
    COALESCE(
        total_amount, 
        LAG(total_amount) IGNORE NULLS OVER (
            PARTITION BY customer_id 
            ORDER BY order_date
        )
    ) as amount_filled
FROM orders;
```

### 48. How do you design for data privacy and GDPR compliance?
**Answer:**

**Data Privacy Design**: Building privacy protection into data models from the start.

**1. Data Classification and Minimization:**
```sql
-- Data classification table
CREATE TABLE data_classification (
    table_name VARCHAR(100),
    column_name VARCHAR(100),
    classification VARCHAR(20), -- 'public', 'internal', 'confidential', 'restricted'
    contains_pii BOOLEAN DEFAULT FALSE,
    retention_period INTERVAL,
    legal_basis VARCHAR(100), -- GDPR legal basis
    PRIMARY KEY (table_name, column_name)
);

-- Customer table with privacy considerations
CREATE TABLE customers (
    customer_id UUID PRIMARY KEY,
    -- Minimal necessary data
    email VARCHAR(255) NOT NULL,
    email_hash VARCHAR(64), -- For analytics without exposing email
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Separate PII data
    consent_given BOOLEAN DEFAULT FALSE,
    consent_date TIMESTAMP,
    data_retention_until DATE,
    
    -- Audit fields
    last_accessed TIMESTAMP,
    access_count INT DEFAULT 0
);

-- Separate table for sensitive PII
CREATE TABLE customer_pii (
    customer_id UUID PRIMARY KEY,
    first_name_encrypted BYTEA,
    last_name_encrypted BYTEA,
    phone_encrypted BYTEA,
    address_encrypted BYTEA,
    encryption_key_id VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**2. Encryption and Pseudonymization:**
```sql
-- Encryption functions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt PII data
CREATE OR REPLACE FUNCTION encrypt_pii(
    p_plaintext TEXT,
    p_key_id VARCHAR(50) DEFAULT 'default'
)
RETURNS BYTEA AS $$
DECLARE
    v_key TEXT;
BEGIN
    -- Get encryption key (in practice, from secure key management)
    SELECT encryption_key INTO v_key 
    FROM encryption_keys 
    WHERE key_id = p_key_id AND is_active = TRUE;
    
    IF v_key IS NULL THEN
        RAISE EXCEPTION 'Encryption key not found: %', p_key_id;
    END IF;
    
    RETURN pgp_sym_encrypt(p_plaintext, v_key);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Decrypt PII data (restricted access)
CREATE OR REPLACE FUNCTION decrypt_pii(
    p_ciphertext BYTEA,
    p_key_id VARCHAR(50) DEFAULT 'default'
)
RETURNS TEXT AS $$
DECLARE
    v_key TEXT;
BEGIN
    -- Check access permissions
    IF NOT has_pii_access(current_user) THEN
        RAISE EXCEPTION 'Access denied: insufficient privileges for PII decryption';
    END IF;
    
    SELECT encryption_key INTO v_key 
    FROM encryption_keys 
    WHERE key_id = p_key_id AND is_active = TRUE;
    
    RETURN pgp_sym_decrypt(p_ciphertext, v_key);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Pseudonymization for analytics
CREATE OR REPLACE FUNCTION pseudonymize_email(p_email TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN 'user_' || encode(digest(p_email || 'salt', 'sha256'), 'hex');
END;
$$ LANGUAGE plpgsql;
```

**3. Consent Management:**
```sql
-- Consent tracking
CREATE TABLE consent_records (
    consent_id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    purpose VARCHAR(100), -- 'marketing', 'analytics', 'service_improvement'
    consent_given BOOLEAN,
    consent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    consent_method VARCHAR(50), -- 'web_form', 'email', 'phone'
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP,
    withdrawn_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Function to check consent
CREATE OR REPLACE FUNCTION has_valid_consent(
    p_customer_id UUID,
    p_purpose VARCHAR(100)
)
RETURNS BOOLEAN AS $$
DECLARE
    v_consent_valid BOOLEAN := FALSE;
BEGIN
    SELECT consent_given AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
           AND withdrawn_at IS NULL
    INTO v_consent_valid
    FROM consent_records
    WHERE customer_id = p_customer_id 
    AND purpose = p_purpose
    ORDER BY consent_date DESC
    LIMIT 1;
    
    RETURN COALESCE(v_consent_valid, FALSE);
END;
$$ LANGUAGE plpgsql;
```

**4. Right to be Forgotten (Data Erasure):**
```sql
-- Data erasure log
CREATE TABLE data_erasure_requests (
    request_id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    tables_affected TEXT[],
    verification_code VARCHAR(100)
);

-- Erasure procedure
CREATE OR REPLACE PROCEDURE erase_customer_data(p_customer_id UUID)
LANGUAGE plpgsql AS $$
DECLARE
    v_request_id UUID;
    v_tables_affected TEXT[] := ARRAY[]::TEXT[];
BEGIN
    -- Create erasure request
    INSERT INTO data_erasure_requests (request_id, customer_id, status)
    VALUES (gen_random_uuid(), p_customer_id, 'processing')
    RETURNING request_id INTO v_request_id;
    
    -- Erase from main tables
    DELETE FROM customer_pii WHERE customer_id = p_customer_id;
    v_tables_affected := array_append(v_tables_affected, 'customer_pii');
    
    -- Anonymize instead of delete (for analytics)
    UPDATE customers 
    SET email = 'deleted_' || customer_id::TEXT || '@deleted.com',
        email_hash = NULL
    WHERE customer_id = p_customer_id;
    v_tables_affected := array_append(v_tables_affected, 'customers');
    
    -- Delete consent records
    DELETE FROM consent_records WHERE customer_id = p_customer_id;
    v_tables_affected := array_append(v_tables_affected, 'consent_records');
    
    -- Update erasure request
    UPDATE data_erasure_requests
    SET processed_at = CURRENT_TIMESTAMP,
        status = 'completed',
        tables_affected = v_tables_affected
    WHERE request_id = v_request_id;
    
    COMMIT;
END;
$$;
```

**5. Data Access Logging:**
```sql
-- Access audit log
CREATE TABLE pii_access_log (
    access_id UUID PRIMARY KEY,
    customer_id UUID,
    accessed_by VARCHAR(100),
    access_purpose VARCHAR(100),
    accessed_fields TEXT[],
    access_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    session_id VARCHAR(100)
);

-- Trigger to log PII access
CREATE OR REPLACE FUNCTION log_pii_access()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO pii_access_log (
        access_id, customer_id, accessed_by, accessed_fields
    ) VALUES (
        gen_random_uuid(),
        NEW.customer_id,
        current_user,
        ARRAY['first_name', 'last_name', 'phone', 'address']
    );
    
    -- Update access counter
    UPDATE customers 
    SET last_accessed = CURRENT_TIMESTAMP,
        access_count = access_count + 1
    WHERE customer_id = NEW.customer_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER pii_access_trigger
    AFTER SELECT ON customer_pii
    FOR EACH ROW EXECUTE FUNCTION log_pii_access();
```

### 49. What are the considerations for modeling IoT and sensor data?
**Answer:**

**IoT Data Modeling**: Handling high-volume, time-series data from connected devices.

**1. Device and Sensor Hierarchy:**
```sql
-- Device registry
CREATE TABLE devices (
    device_id UUID PRIMARY KEY,
    device_type VARCHAR(50), -- 'temperature_sensor', 'humidity_sensor', 'gateway'
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    firmware_version VARCHAR(20),
    location JSONB, -- {"building": "A", "floor": 2, "room": "201"}
    installed_date DATE,
    last_seen TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'maintenance'
    configuration JSONB
);

-- Sensor definitions
CREATE TABLE sensors (
    sensor_id UUID PRIMARY KEY,
    device_id UUID NOT NULL,
    sensor_type VARCHAR(50), -- 'temperature', 'humidity', 'pressure'
    unit_of_measure VARCHAR(20), -- 'celsius', 'fahrenheit', 'percent', 'pascal'
    min_value DECIMAL(10,4),
    max_value DECIMAL(10,4),
    precision_digits INT DEFAULT 2,
    sampling_rate_seconds INT DEFAULT 60,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

-- Create indexes for efficient queries
CREATE INDEX idx_devices_type ON devices(device_type);
CREATE INDEX idx_devices_status ON devices(status);
CREATE INDEX idx_sensors_device ON sensors(device_id);
CREATE INDEX idx_sensors_type ON sensors(sensor_type);
```

**2. Time-Series Data Storage:**
```sql
-- Partitioned sensor readings table
CREATE TABLE sensor_readings (
    reading_id BIGSERIAL,
    sensor_id UUID NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    value DECIMAL(15,6),
    quality_score DECIMAL(3,2), -- 0.0 to 1.0 indicating data quality
    raw_value TEXT, -- Original raw value from sensor
    metadata JSONB, -- Additional sensor-specific data
    PRIMARY KEY (sensor_id, timestamp, reading_id)
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions
CREATE TABLE sensor_readings_2024_01 PARTITION OF sensor_readings
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE sensor_readings_2024_02 PARTITION OF sensor_readings
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Indexes for time-series queries
CREATE INDEX idx_sensor_readings_timestamp ON sensor_readings (timestamp DESC);
CREATE INDEX idx_sensor_readings_sensor_time ON sensor_readings (sensor_id, timestamp DESC);
```

**3. Data Aggregation and Rollups:**
```sql
-- Pre-computed aggregations for different time windows
CREATE TABLE sensor_aggregates (
    sensor_id UUID,
    time_bucket TIMESTAMP,
    window_size INTERVAL,
    min_value DECIMAL(15,6),
    max_value DECIMAL(15,6),
    avg_value DECIMAL(15,6),
    sum_value DECIMAL(15,6),
    count_readings INT,
    stddev_value DECIMAL(15,6),
    first_reading_time TIMESTAMP,
    last_reading_time TIMESTAMP,
    PRIMARY KEY (sensor_id, time_bucket, window_size)
);

-- Function to compute aggregates
CREATE OR REPLACE FUNCTION compute_sensor_aggregates(
    p_sensor_id UUID,
    p_start_time TIMESTAMP,
    p_end_time TIMESTAMP,
    p_window_size INTERVAL
)
RETURNS VOID AS $$
DECLARE
    v_bucket_start TIMESTAMP;
    v_bucket_end TIMESTAMP;
BEGIN
    v_bucket_start := date_trunc(
        CASE 
            WHEN p_window_size = INTERVAL '1 hour' THEN 'hour'
            WHEN p_window_size = INTERVAL '1 day' THEN 'day'
            ELSE 'hour'
        END, 
        p_start_time
    );
    
    WHILE v_bucket_start < p_end_time LOOP
        v_bucket_end := v_bucket_start + p_window_size;
        
        INSERT INTO sensor_aggregates (
            sensor_id, time_bucket, window_size,
            min_value, max_value, avg_value, sum_value, count_readings, stddev_value,
            first_reading_time, last_reading_time
        )
        SELECT 
            p_sensor_id,
            v_bucket_start,
            p_window_size,
            MIN(value),
            MAX(value),
            AVG(value),
            SUM(value),
            COUNT(*),
            STDDEV(value),
            MIN(timestamp),
            MAX(timestamp)
        FROM sensor_readings
        WHERE sensor_id = p_sensor_id
        AND timestamp >= v_bucket_start
        AND timestamp < v_bucket_end
        ON CONFLICT (sensor_id, time_bucket, window_size) DO UPDATE SET
            min_value = EXCLUDED.min_value,
            max_value = EXCLUDED.max_value,
            avg_value = EXCLUDED.avg_value,
            sum_value = EXCLUDED.sum_value,
            count_readings = EXCLUDED.count_readings,
            stddev_value = EXCLUDED.stddev_value,
            first_reading_time = EXCLUDED.first_reading_time,
            last_reading_time = EXCLUDED.last_reading_time;
        
        v_bucket_start := v_bucket_end;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

**4. Anomaly Detection and Alerts:**
```sql
-- Anomaly detection rules
CREATE TABLE anomaly_rules (
    rule_id UUID PRIMARY KEY,
    sensor_id UUID,
    rule_type VARCHAR(50), -- 'threshold', 'rate_of_change', 'statistical'
    rule_config JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

-- Sample anomaly rules
INSERT INTO anomaly_rules (rule_id, sensor_id, rule_type, rule_config) VALUES
(gen_random_uuid(), 'sensor-123', 'threshold', 
 '{"min_value": -10, "max_value": 50, "severity": "high"}'),
(gen_random_uuid(), 'sensor-123', 'rate_of_change',
 '{"max_change_per_minute": 5, "severity": "medium"}');

-- Anomaly detection results
CREATE TABLE anomalies (
    anomaly_id UUID PRIMARY KEY,
    sensor_id UUID NOT NULL,
    rule_id UUID NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    anomaly_type VARCHAR(50),
    severity VARCHAR(20), -- 'low', 'medium', 'high', 'critical'
    description TEXT,
    sensor_value DECIMAL(15,6),
    expected_range JSONB,
    resolved_at TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id),
    FOREIGN KEY (rule_id) REFERENCES anomaly_rules(rule_id)
);

-- Function to detect anomalies
CREATE OR REPLACE FUNCTION detect_anomalies(p_sensor_id UUID, p_value DECIMAL(15,6))
RETURNS VOID AS $$
DECLARE
    rule RECORD;
    v_anomaly_detected BOOLEAN := FALSE;
BEGIN
    FOR rule IN 
        SELECT * FROM anomaly_rules 
        WHERE sensor_id = p_sensor_id AND is_active = TRUE
    LOOP
        CASE rule.rule_type
            WHEN 'threshold' THEN
                IF p_value < (rule.rule_config->>'min_value')::DECIMAL OR 
                   p_value > (rule.rule_config->>'max_value')::DECIMAL THEN
                    v_anomaly_detected := TRUE;
                END IF;
            WHEN 'rate_of_change' THEN
                -- Check rate of change logic here
                NULL;
        END CASE;
        
        IF v_anomaly_detected THEN
            INSERT INTO anomalies (
                anomaly_id, sensor_id, rule_id, anomaly_type, severity, 
                description, sensor_value
            ) VALUES (
                gen_random_uuid(), p_sensor_id, rule.rule_id, rule.rule_type,
                rule.rule_config->>'severity',
                'Value ' || p_value || ' outside expected range',
                p_value
            );
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### 50. How do you design data models for machine learning applications?
**Answer:**

**ML Data Modeling**: Structuring data to support machine learning workflows and model lifecycle.

**1. Feature Store Design:**
```sql
-- Feature definitions
CREATE TABLE feature_definitions (
    feature_id UUID PRIMARY KEY,
    feature_name VARCHAR(100) UNIQUE NOT NULL,
    feature_type VARCHAR(50), -- 'numerical', 'categorical', 'text', 'embedding'
    data_type VARCHAR(50), -- 'int', 'float', 'varchar', 'jsonb'
    description TEXT,
    source_table VARCHAR(100),
    source_column VARCHAR(100),
    transformation_logic TEXT,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Feature values storage
CREATE TABLE feature_values (
    entity_id VARCHAR(100), -- Customer ID, Product ID, etc.
    feature_id UUID,
    feature_value JSONB, -- Flexible storage for different data types
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INT DEFAULT 1,
    PRIMARY KEY (entity_id, feature_id, version),
    FOREIGN KEY (feature_id) REFERENCES feature_definitions(feature_id)
) PARTITION BY HASH (entity_id);

-- Create partitions for parallel processing
CREATE TABLE feature_values_0 PARTITION OF feature_values
    FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE feature_values_1 PARTITION OF feature_values
    FOR VALUES WITH (modulus 4, remainder 1);
CREATE TABLE feature_values_2 PARTITION OF feature_values
    FOR VALUES WITH (modulus 4, remainder 2);
CREATE TABLE feature_values_3 PARTITION OF feature_values
    FOR VALUES WITH (modulus 4, remainder 3);
```

**2. Training Data Management:**
```sql
-- Training datasets
CREATE TABLE training_datasets (
    dataset_id UUID PRIMARY KEY,
    dataset_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    target_variable VARCHAR(100),
    feature_list JSONB, -- Array of feature IDs
    data_split JSONB, -- {"train": 0.7, "validation": 0.15, "test": 0.15}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    version INT DEFAULT 1
);

-- Training samples
CREATE TABLE training_samples (
    sample_id UUID PRIMARY KEY,
    dataset_id UUID NOT NULL,
    entity_id VARCHAR(100),
    features JSONB, -- Feature vector
    target_value JSONB, -- Target variable value
    split_type VARCHAR(20), -- 'train', 'validation', 'test'
    sample_weight DECIMAL(10,6) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dataset_id) REFERENCES training_datasets(dataset_id)
) PARTITION BY HASH (dataset_id);

-- Function to create training dataset
CREATE OR REPLACE FUNCTION create_training_dataset(
    p_dataset_name VARCHAR(100),
    p_feature_ids UUID[],
    p_target_feature_id UUID,
    p_entity_ids VARCHAR(100)[] DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_dataset_id UUID := gen_random_uuid();
    v_entity_id VARCHAR(100);
    v_features JSONB := '{}';
    v_target_value JSONB;
    v_feature_id UUID;
BEGIN
    -- Create dataset record
    INSERT INTO training_datasets (dataset_id, dataset_name, feature_list, target_variable)
    VALUES (v_dataset_id, p_dataset_name, to_jsonb(p_feature_ids), 
            (SELECT feature_name FROM feature_definitions WHERE feature_id = p_target_feature_id));
    
    -- Generate training samples
    FOR v_entity_id IN 
        SELECT DISTINCT entity_id FROM feature_values 
        WHERE (p_entity_ids IS NULL OR entity_id = ANY(p_entity_ids))
        AND feature_id = ANY(p_feature_ids || p_target_feature_id)
    LOOP
        -- Collect features for this entity
        v_features := '{}';
        FOR v_feature_id IN SELECT unnest(p_feature_ids) LOOP
            SELECT jsonb_build_object(
                (SELECT feature_name FROM feature_definitions WHERE feature_id = v_feature_id),
                feature_value
            ) INTO v_features
            FROM feature_values 
            WHERE entity_id = v_entity_id AND feature_id = v_feature_id
            ORDER BY version DESC LIMIT 1;
        END LOOP;
        
        -- Get target value
        SELECT feature_value INTO v_target_value
        FROM feature_values
        WHERE entity_id = v_entity_id AND feature_id = p_target_feature_id
        ORDER BY version DESC LIMIT 1;
        
        -- Insert training sample
        INSERT INTO training_samples (sample_id, dataset_id, entity_id, features, target_value)
        VALUES (gen_random_uuid(), v_dataset_id, v_entity_id, v_features, v_target_value);
    END LOOP;
    
    RETURN v_dataset_id;
END;
$$ LANGUAGE plpgsql;
```

**3. Model Registry and Versioning:**
```sql
-- Model registry
CREATE TABLE ml_models (
    model_id UUID PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50), -- 'classification', 'regression', 'clustering'
    algorithm VARCHAR(100), -- 'random_forest', 'neural_network', 'svm'
    version VARCHAR(20),
    training_dataset_id UUID,
    hyperparameters JSONB,
    performance_metrics JSONB,
    model_artifact_path TEXT, -- Path to serialized model
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    status VARCHAR(20) DEFAULT 'training', -- 'training', 'ready', 'deployed', 'archived'
    FOREIGN KEY (training_dataset_id) REFERENCES training_datasets(dataset_id)
);

-- Model performance tracking
CREATE TABLE model_performance (
    performance_id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    metric_name VARCHAR(50), -- 'accuracy', 'precision', 'recall', 'f1_score', 'auc'
    metric_value DECIMAL(10,6),
    dataset_type VARCHAR(20), -- 'train', 'validation', 'test'
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ml_models(model_id)
);

-- Model deployment tracking
CREATE TABLE model_deployments (
    deployment_id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    environment VARCHAR(50), -- 'staging', 'production'
    endpoint_url TEXT,
    deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deployed_by VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'rollback'
    traffic_percentage DECIMAL(5,2) DEFAULT 100.0,
    FOREIGN KEY (model_id) REFERENCES ml_models(model_id)
);
```

**4. Prediction Logging and Monitoring:**
```sql
-- Prediction requests and responses
CREATE TABLE prediction_logs (
    prediction_id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    entity_id VARCHAR(100),
    input_features JSONB,
    prediction_result JSONB,
    confidence_score DECIMAL(10,6),
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_time_ms INT,
    model_version VARCHAR(20),
    FOREIGN KEY (model_id) REFERENCES ml_models(model_id)
) PARTITION BY RANGE (prediction_timestamp);

-- Create monthly partitions for prediction logs
CREATE TABLE prediction_logs_2024_01 PARTITION OF prediction_logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Model drift detection
CREATE TABLE model_drift_metrics (
    drift_id UUID PRIMARY KEY,
    model_id UUID NOT NULL,
    metric_type VARCHAR(50), -- 'feature_drift', 'prediction_drift', 'performance_drift'
    drift_score DECIMAL(10,6),
    threshold DECIMAL(10,6),
    is_drift_detected BOOLEAN,
    measurement_period JSONB, -- {"start": "2024-01-01", "end": "2024-01-07"}
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES ml_models(model_id)
);

-- Function to detect feature drift
CREATE OR REPLACE FUNCTION detect_feature_drift(
    p_model_id UUID,
    p_start_date TIMESTAMP,
    p_end_date TIMESTAMP
)
RETURNS VOID AS $$
DECLARE
    v_baseline_stats JSONB;
    v_current_stats JSONB;
    v_drift_score DECIMAL(10,6);
BEGIN
    -- Calculate baseline statistics (from training data)
    SELECT jsonb_agg(
        jsonb_build_object(
            'feature', feature_name,
            'mean', avg_value,
            'std', std_value
        )
    ) INTO v_baseline_stats
    FROM (
        SELECT 
            key as feature_name,
            AVG((value->>'value')::DECIMAL) as avg_value,
            STDDEV((value->>'value')::DECIMAL) as std_value
        FROM training_samples ts,
        jsonb_each(ts.features)
        WHERE ts.dataset_id = (
            SELECT training_dataset_id FROM ml_models WHERE model_id = p_model_id
        )
        GROUP BY key
    ) baseline;
    
    -- Calculate current statistics (from recent predictions)
    SELECT jsonb_agg(
        jsonb_build_object(
            'feature', feature_name,
            'mean', avg_value,
            'std', std_value
        )
    ) INTO v_current_stats
    FROM (
        SELECT 
            key as feature_name,
            AVG((value->>'value')::DECIMAL) as avg_value,
            STDDEV((value->>'value')::DECIMAL) as std_value
        FROM prediction_logs pl,
        jsonb_each(pl.input_features)
        WHERE pl.model_id = p_model_id
        AND pl.prediction_timestamp BETWEEN p_start_date AND p_end_date
        GROUP BY key
    ) current;
    
    -- Calculate drift score (simplified KL divergence approximation)
    v_drift_score := 0.5; -- Placeholder calculation
    
    -- Insert drift detection result
    INSERT INTO model_drift_metrics (
        drift_id, model_id, metric_type, drift_score, threshold, is_drift_detected,
        measurement_period
    ) VALUES (
        gen_random_uuid(), p_model_id, 'feature_drift', v_drift_score, 0.1,
        v_drift_score > 0.1,
        jsonb_build_object('start', p_start_date, 'end', p_end_date)
    );
END;
$$ LANGUAGE plpgsql;
```

---

This completes the basic level questions (1-50). Each question provides comprehensive answers with practical examples, SQL code, and real-world scenarios that demonstrate proper data modeling techniques and best practices.