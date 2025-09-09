
### Q1: What are the key principles of relational database design?
**Answer:**

**ACID Properties:**
- **Atomicity**: Transactions are all-or-nothing
- **Consistency**: Database remains in valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

**Codd's 12 Rules:**
- Information stored in tables (relations)
- Guaranteed access through primary keys
- Systematic treatment of null values
- Dynamic online catalog based on relational model
- Comprehensive data sublanguage (SQL)

**Example Implementation:**
```sql
-- ACID Transaction Example
BEGIN TRANSACTION;

-- Atomicity: Either both operations succeed or both fail
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'A001';
UPDATE accounts SET balance = balance + 100 WHERE account_id = 'A002';

-- Consistency: Check business rules
IF (SELECT balance FROM accounts WHERE account_id = 'A001') < 0
    ROLLBACK TRANSACTION;
ELSE
    COMMIT TRANSACTION;
```

### Q2: Explain database normalization and its normal forms.
**Answer:**

**First Normal Form (1NF):**
```sql
-- Violates 1NF: Multiple values in single column
CREATE TABLE customers_bad (
    customer_id INT,
    name VARCHAR(100),
    phone_numbers VARCHAR(200)  -- "123-456-7890, 098-765-4321"
);

-- Follows 1NF: Atomic values only
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE customer_phones (
    customer_id INT,
    phone_number VARCHAR(15),
    phone_type VARCHAR(10),  -- 'mobile', 'home', 'work'
    PRIMARY KEY (customer_id, phone_number),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**Second Normal Form (2NF):**
```sql
-- Violates 2NF: Partial dependency on composite key
CREATE TABLE order_items_bad (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id
    product_price DECIMAL(10,2), -- Depends only on product_id
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- Follows 2NF: Remove partial dependencies
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_price DECIMAL(10,2)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

**Third Normal Form (3NF):**
```sql
-- Violates 3NF: Transitive dependency
CREATE TABLE employees_bad (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT,
    department_name VARCHAR(50),  -- Depends on department_id, not employee_id
    department_location VARCHAR(100) -- Transitive dependency
);

-- Follows 3NF: Remove transitive dependencies
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50),
    department_location VARCHAR(100)
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
```

### Q3: When would you denormalize a database and why?
**Answer:**

**Denormalization Scenarios:**
```sql
-- Normalized structure (3NF)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_id)
);

-- Denormalized for reporting performance
CREATE TABLE order_summary_denormalized (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),    -- Denormalized from customers
    customer_email VARCHAR(100),   -- Denormalized from customers
    order_date DATE,
    total_items INT,               -- Calculated field
    total_amount DECIMAL(12,2),    -- Calculated field
    order_status VARCHAR(20)
);

-- Materialized view for complex aggregations
CREATE MATERIALIZED VIEW customer_metrics AS
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as total_orders,
    SUM(oi.quantity * oi.unit_price) as lifetime_value,
    AVG(oi.quantity * oi.unit_price) as avg_order_value,
    MAX(o.order_date) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name;
```

**Trade-offs:**
- **Benefits**: Faster queries, reduced joins, better read performance
- **Costs**: Data redundancy, update complexity, storage overhead

## 🔑 Keys and Constraints

### Q4: Explain different types of database keys and their purposes.
**Answer:**

**Primary Keys:**
```sql
-- Simple primary key
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2)
);

-- Composite primary key
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- Auto-incrementing primary key
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,  -- PostgreSQL
    -- customer_id INT IDENTITY(1,1) PRIMARY KEY,  -- SQL Server
    customer_name VARCHAR(100) NOT NULL
);
```

**Foreign Keys and Referential Integrity:**
```sql
-- Foreign key with cascade options
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE      -- Delete orders when customer is deleted
        ON UPDATE CASCADE      -- Update order.customer_id when customer.customer_id changes
);

-- Self-referencing foreign key
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);
```

**Unique Keys and Indexes:**
```sql
-- Unique constraint
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Composite unique constraint
CREATE TABLE user_roles (
    user_id INT,
    role_id INT,
    assigned_date DATE,
    UNIQUE (user_id, role_id),  -- User can have each role only once
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
```

### Q5: How do you implement complex constraints and business rules?
**Answer:**

**Check Constraints:**
```sql
-- Simple check constraints
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) CHECK (price > 0),
    discount_percentage DECIMAL(5,2) CHECK (discount_percentage BETWEEN 0 AND 100),
    category VARCHAR(50) CHECK (category IN ('Electronics', 'Clothing', 'Books', 'Home'))
);

-- Complex check constraints
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    birth_date DATE,
    hire_date DATE,
    salary DECIMAL(10,2),
    CHECK (hire_date > birth_date),
    CHECK (EXTRACT(YEAR FROM AGE(hire_date, birth_date)) >= 18),  -- Must be 18+ when hired
    CHECK (salary > 0)
);
```

**Triggers for Business Logic:**
```sql
-- Audit trigger
CREATE OR REPLACE FUNCTION audit_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, new_values, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, 'INSERT', row_to_json(NEW), current_user, now());
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, old_values, new_values, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, 'UPDATE', row_to_json(OLD), row_to_json(NEW), current_user, now());
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, old_values, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, 'DELETE', row_to_json(OLD), current_user, now());
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables
CREATE TRIGGER customers_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION audit_changes();

-- Business rule trigger: Update inventory
CREATE OR REPLACE FUNCTION update_inventory()
RETURNS TRIGGER AS $$
BEGIN
    -- Decrease inventory when order item is added
    IF TG_OP = 'INSERT' THEN
        UPDATE products 
        SET stock_quantity = stock_quantity - NEW.quantity
        WHERE product_id = NEW.product_id;
        
        -- Check if stock goes negative
        IF (SELECT stock_quantity FROM products WHERE product_id = NEW.product_id) < 0 THEN
            RAISE EXCEPTION 'Insufficient stock for product %', NEW.product_id;
        END IF;
        
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_items_inventory_trigger
    AFTER INSERT ON order_items
    FOR EACH ROW EXECUTE FUNCTION update_inventory();
```

## 📊 Query Optimization & Indexing

### Q6: How do you optimize database queries and design effective indexes?
**Answer:**

**Index Types and Strategies:**
```sql
-- B-tree indexes (default)
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Composite indexes
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_products_category_price ON products(category, price);

-- Partial indexes
CREATE INDEX idx_active_customers ON customers(customer_id) 
WHERE status = 'active';

CREATE INDEX idx_recent_orders ON orders(order_date) 
WHERE order_date >= '2023-01-01';

-- Functional indexes
CREATE INDEX idx_customers_upper_name ON customers(UPPER(customer_name));
CREATE INDEX idx_orders_year ON orders(EXTRACT(YEAR FROM order_date));

-- Hash indexes (for equality comparisons)
CREATE INDEX idx_products_sku_hash ON products USING HASH(sku);
```

**Query Optimization Techniques:**
```sql
-- Use EXPLAIN to analyze query plans
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.customer_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.registration_date >= '2023-01-01'
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(o.order_id) > 5;

-- Optimize with proper indexing
CREATE INDEX idx_customers_registration_date ON customers(registration_date);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Rewrite subqueries as joins when possible
-- Slow subquery
SELECT * FROM customers 
WHERE customer_id IN (
    SELECT customer_id FROM orders 
    WHERE order_date >= '2023-01-01'
);

-- Faster join
SELECT DISTINCT c.* 
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2023-01-01';

-- Use window functions for complex analytics
SELECT 
    customer_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS UNBOUNDED PRECEDING
    ) as running_total,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date DESC
    ) as order_rank
FROM orders;
```

### Q7: How do you handle database transactions and concurrency?
**Answer:**

**Transaction Isolation Levels:**
```sql
-- Read Uncommitted (lowest isolation)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- Can read uncommitted changes (dirty reads)

-- Read Committed (default in most databases)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Only reads committed data, but non-repeatable reads possible

-- Repeatable Read
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Same data read multiple times in transaction, but phantom reads possible

-- Serializable (highest isolation)
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Complete isolation, no concurrent anomalies
```

**Concurrency Control:**
```sql
-- Optimistic locking with version numbers
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    version_number INT DEFAULT 1,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Update with version check
UPDATE products 
SET price = 29.99, 
    version_number = version_number + 1,
    updated_at = CURRENT_TIMESTAMP
WHERE product_id = 123 
  AND version_number = 5;  -- Only update if version matches

-- Pessimistic locking
BEGIN TRANSACTION;

-- Lock row for update
SELECT * FROM accounts 
WHERE account_id = 'A001' 
FOR UPDATE;

-- Perform operations
UPDATE accounts 
SET balance = balance - 100 
WHERE account_id = 'A001';

COMMIT;

-- Deadlock prevention with ordered locking
-- Always lock resources in same order (e.g., by ID)
BEGIN TRANSACTION;

-- Lock accounts in ID order to prevent deadlocks
SELECT * FROM accounts 
WHERE account_id IN ('A001', 'A002')
ORDER BY account_id
FOR UPDATE;

-- Perform transfers
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'A001';
UPDATE accounts SET balance = balance + 100 WHERE account_id = 'A002';

COMMIT;
```

## 🏗️ Advanced Relational Concepts

### Q8: How do you model hierarchical data in relational databases?
**Answer:**

**Adjacency List Model:**
```sql
-- Simple parent-child relationship
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100),
    parent_category_id INT,
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
);

-- Recursive query to get hierarchy
WITH RECURSIVE category_hierarchy AS (
    -- Base case: root categories
    SELECT category_id, category_name, parent_category_id, 0 as level
    FROM categories
    WHERE parent_category_id IS NULL
    
    UNION ALL
    
    -- Recursive case: child categories
    SELECT c.category_id, c.category_name, c.parent_category_id, ch.level + 1
    FROM categories c
    INNER JOIN category_hierarchy ch ON c.parent_category_id = ch.category_id
)
SELECT * FROM category_hierarchy ORDER BY level, category_name;
```

**Nested Set Model:**
```sql
-- More efficient for read-heavy hierarchies
CREATE TABLE categories_nested (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100),
    left_bound INT,
    right_bound INT
);

-- Insert sample data
INSERT INTO categories_nested VALUES
(1, 'Electronics', 1, 14),
(2, 'Computers', 2, 9),
(3, 'Laptops', 3, 6),
(4, 'Gaming Laptops', 4, 5),
(5, 'Desktops', 7, 8),
(6, 'Mobile Phones', 10, 13),
(7, 'Smartphones', 11, 12);

-- Get all descendants of a category
SELECT child.*
FROM categories_nested parent, categories_nested child
WHERE child.left_bound BETWEEN parent.left_bound AND parent.right_bound
  AND parent.category_id = 1;  -- Electronics

-- Get path to root
SELECT ancestor.*
FROM categories_nested ancestor, categories_nested descendant
WHERE descendant.left_bound BETWEEN ancestor.left_bound AND ancestor.right_bound
  AND descendant.category_id = 4  -- Gaming Laptops
ORDER BY ancestor.left_bound;
```

**Materialized Path Model:**
```sql
-- Store full path as string
CREATE TABLE categories_path (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100),
    path VARCHAR(500)  -- e.g., '/1/2/3/'
);

-- Find all descendants
SELECT * FROM categories_path
WHERE path LIKE '/1/2/%';  -- All under category 2

-- Find ancestors
SELECT * FROM categories_path
WHERE '/1/2/3/' LIKE path || '%';
```

### Q9: How do you implement temporal data and audit trails?
**Answer:**

**Temporal Tables (System-Versioned):**
```sql
-- SQL Server temporal table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    valid_from DATETIME2 GENERATED ALWAYS AS ROW START,
    valid_to DATETIME2 GENERATED ALWAYS AS ROW END,
    PERIOD FOR SYSTEM_TIME (valid_from, valid_to)
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.employees_history));

-- Query historical data
SELECT * FROM employees 
FOR SYSTEM_TIME AS OF '2023-06-01'
WHERE employee_id = 123;

-- Query changes over time
SELECT * FROM employees 
FOR SYSTEM_TIME BETWEEN '2023-01-01' AND '2023-12-31'
WHERE employee_id = 123;
```

**Manual Audit Implementation:**
```sql
-- Audit table structure
CREATE TABLE audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    operation VARCHAR(10),  -- INSERT, UPDATE, DELETE
    record_id VARCHAR(50),
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100),
    application VARCHAR(50)
);

-- Comprehensive audit trigger
CREATE OR REPLACE FUNCTION comprehensive_audit()
RETURNS TRIGGER AS $$
DECLARE
    old_data JSONB;
    new_data JSONB;
    changed_fields JSONB;
BEGIN
    -- Capture old and new data
    IF TG_OP = 'DELETE' THEN
        old_data = to_jsonb(OLD);
        new_data = NULL;
    ELSIF TG_OP = 'INSERT' THEN
        old_data = NULL;
        new_data = to_jsonb(NEW);
    ELSE  -- UPDATE
        old_data = to_jsonb(OLD);
        new_data = to_jsonb(NEW);
        
        -- Calculate changed fields only
        SELECT jsonb_object_agg(key, value)
        INTO changed_fields
        FROM jsonb_each(new_data)
        WHERE value != old_data->key OR old_data->key IS NULL;
    END IF;
    
    -- Insert audit record
    INSERT INTO audit_log (
        table_name, operation, record_id, 
        old_values, new_values, changed_by,
        session_id, application
    ) VALUES (
        TG_TABLE_NAME, TG_OP, 
        COALESCE(NEW.id::TEXT, OLD.id::TEXT),
        old_data, COALESCE(changed_fields, new_data),
        current_user, 
        current_setting('application_name', true),
        current_setting('myapp.session_id', true)
    );
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

## 🎯 Key Takeaways

**Normalization Benefits:**
- **Eliminates redundancy** and update anomalies
- **Ensures data integrity** through constraints
- **Reduces storage space** requirements
- **Simplifies maintenance** operations

**When to Denormalize:**
- **Read-heavy workloads** with complex joins
- **Reporting and analytics** requirements
- **Performance critical** applications
- **Data warehousing** scenarios

**Key Design Principles:**
- **Choose appropriate keys** (primary, foreign, unique)
- **Implement proper constraints** for data integrity
- **Design effective indexes** for query performance
- **Handle concurrency** with appropriate isolation levels

**Advanced Concepts:**
- **Hierarchical data modeling** (adjacency list, nested sets)
- **Temporal data** and audit trails
- **Transaction management** and ACID properties
- **Query optimization** techniques