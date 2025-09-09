
### What are windowing functions?
**Answer:**
Window functions perform calculations across a set of table rows related to the current row, without collapsing the result set like aggregate functions.

**Key Characteristics:**
- Operate on a "window" of rows
- Don't reduce the number of rows in output
- Use OVER clause to define the window
- Can include ORDER BY and PARTITION BY

**Common Window Functions:**
```sql
-- ROW_NUMBER: Assigns unique sequential numbers
SELECT name, salary, 
       ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;

-- RANK: Assigns ranks with gaps for ties
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- DENSE_RANK: Assigns ranks without gaps
SELECT name, salary,
       DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;

-- LAG/LEAD: Access previous/next row values
SELECT name, salary,
       LAG(salary, 1) OVER (ORDER BY hire_date) as prev_salary,
       LEAD(salary, 1) OVER (ORDER BY hire_date) as next_salary
FROM employees;

-- Running totals and moving averages
SELECT order_date, amount,
       SUM(amount) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) as running_total,
       AVG(amount) OVER (ORDER BY order_date ROWS 2 PRECEDING) as moving_avg
FROM orders;
```

## Stored Procedures

### What is a stored procedure?
**Answer:**
A stored procedure is a precompiled collection of SQL statements stored in the database that can be executed as a single unit.

**Key Features:**
- Precompiled for better performance
- Can accept input/output parameters
- Support control flow (IF, WHILE, loops)
- Can return multiple result sets
- Provide security through controlled access

```sql
-- Example stored procedure
CREATE PROCEDURE GetEmployeesByDepartment(
    @DepartmentName VARCHAR(50),
    @MinSalary DECIMAL(10,2) = 0
)
AS
BEGIN
    SELECT employee_id, name, salary, hire_date
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    WHERE d.department_name = @DepartmentName
      AND e.salary >= @MinSalary
    ORDER BY e.salary DESC;
END;

-- Execute procedure
EXEC GetEmployeesByDepartment 'Engineering', 75000;
```

### Why would you use stored procedures?
**Answer:**
**Benefits:**
- **Performance**: Precompiled execution plans
- **Security**: Controlled data access, prevent SQL injection
- **Maintainability**: Centralized business logic
- **Network Traffic**: Reduced data transfer
- **Reusability**: Can be called from multiple applications

**Drawbacks:**
- **Database Lock-in**: Not portable across database systems
- **Version Control**: Harder to manage in source control
- **Debugging**: More difficult to debug than application code
- **Scalability**: Can become bottleneck in high-load scenarios

## Database Design

### What are atomic attributes?
**Answer:**
Atomic attributes are indivisible data elements that cannot be broken down into smaller meaningful components within the context of the database design.

**Characteristics:**
- Single-valued (not multi-valued)
- Indivisible in the given context
- Conform to First Normal Form (1NF)

**Examples:**
```sql
-- NON-ATOMIC (violates 1NF)
CREATE TABLE employees_bad (
    employee_id INT,
    name VARCHAR(100),
    phone_numbers VARCHAR(200) -- '555-1234, 555-5678, 555-9012'
);

-- ATOMIC (follows 1NF)
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),  -- Atomic
    last_name VARCHAR(50),   -- Atomic
    email VARCHAR(100)       -- Atomic
);

CREATE TABLE employee_phones (
    employee_id INT,
    phone_number VARCHAR(20), -- Each phone is atomic
    phone_type VARCHAR(20),   -- 'mobile', 'home', 'work'
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);
```

### Explain ACID properties of a database
**Answer:**
ACID properties ensure database reliability and data integrity:

**Atomicity:**
- All operations in a transaction succeed or fail together
- "All or nothing" principle
- If any part fails, entire transaction is rolled back

**Consistency:**
- Database moves from one valid state to another
- All constraints and rules are maintained
- Data integrity is preserved

**Isolation:**
- Concurrent transactions don't interfere with each other
- Each transaction appears to run in isolation
- Prevents dirty reads, phantom reads, etc.

**Durability:**
- Committed changes persist permanently
- Survive system crashes and power failures
- Changes are written to permanent storage

```sql
-- Example demonstrating ACID properties
BEGIN TRANSACTION;
    -- Atomicity: Both operations must succeed
    UPDATE accounts SET balance = balance - 1000 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE account_id = 2;
    
    -- Consistency: Check business rules
    IF (SELECT balance FROM accounts WHERE account_id = 1) < 0
        ROLLBACK TRANSACTION;
    ELSE
        COMMIT TRANSACTION; -- Durability: Changes are permanent
END;
```

## Query Optimization

### How to optimize queries?
**Answer:**
**Indexing Strategies:**
```sql
-- Create appropriate indexes
CREATE INDEX idx_employee_dept_salary ON employees(department_id, salary);
CREATE INDEX idx_order_date ON orders(order_date);

-- Use covering indexes
CREATE INDEX idx_employee_covering ON employees(department_id) INCLUDE (name, salary);
```

**Query Writing Best Practices:**
```sql
-- Use EXISTS instead of IN for large datasets
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Avoid functions on columns in WHERE clause
-- BAD:
SELECT * FROM orders WHERE YEAR(order_date) = 2024;
-- GOOD:
SELECT * FROM orders WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';

-- Use LIMIT to restrict results
SELECT * FROM large_table ORDER BY created_date DESC LIMIT 100;

-- Use appropriate JOIN types
SELECT c.name, COUNT(o.order_id)
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

**Execution Plan Analysis:**
```sql
-- Analyze query execution
EXPLAIN ANALYZE SELECT * FROM employees WHERE department_id = 5;

-- Check for table scans, index usage, join algorithms
```

## JOIN Types

### What are the different types of JOIN (CROSS, INNER, OUTER)?
**Answer:**

**INNER JOIN:**
- Returns only matching records from both tables
- Most common and restrictive join

**LEFT OUTER JOIN (LEFT JOIN):**
- Returns all records from left table
- Matching records from right table (NULL if no match)

**RIGHT OUTER JOIN (RIGHT JOIN):**
- Returns all records from right table  
- Matching records from left table (NULL if no match)

**FULL OUTER JOIN:**
- Returns all records from both tables
- NULL values where no match exists

**CROSS JOIN:**
- Cartesian product of both tables
- Every row from first table combined with every row from second table

```sql
-- Sample data
CREATE TABLE customers (id INT, name VARCHAR(50));
CREATE TABLE orders (id INT, customer_id INT, amount DECIMAL(10,2));

INSERT INTO customers VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie');
INSERT INTO orders VALUES (101, 1, 100.00), (102, 1, 200.00), (103, 2, 150.00);

-- INNER JOIN - only customers with orders
SELECT c.name, o.amount
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;
-- Result: Alice (100.00), Alice (200.00), Bob (150.00)

-- LEFT JOIN - all customers, with/without orders
SELECT c.name, o.amount
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
-- Result: Alice (100.00), Alice (200.00), Bob (150.00), Charlie (NULL)

-- CROSS JOIN - all combinations
SELECT c.name, o.amount
FROM customers c
CROSS JOIN orders o;
-- Result: 9 rows (3 customers × 3 orders)
```

## Index Types

### What is the difference between Clustered Index and Non-Clustered Index - with examples?
**Answer:**

**Clustered Index:**
- Physically reorders table data
- Data pages stored in order of index key
- One per table (usually primary key)
- Faster for range queries and sorting

**Non-Clustered Index:**
- Separate structure pointing to data rows
- Multiple allowed per table
- Contains key values and row locators
- Faster for specific value lookups

```sql
-- Clustered Index (implicit with PRIMARY KEY)
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,  -- Clustered index
    name VARCHAR(100),
    department_id INT,
    salary DECIMAL(10,2),
    hire_date DATE
);

-- Non-clustered indexes
CREATE INDEX idx_department ON employees(department_id);  -- Non-clustered
CREATE INDEX idx_salary ON employees(salary);             -- Non-clustered
CREATE INDEX idx_name_dept ON employees(name, department_id); -- Composite non-clustered

-- Performance comparison
-- Clustered index scan (fast for ranges)
SELECT * FROM employees 
WHERE employee_id BETWEEN 1000 AND 2000;

-- Non-clustered index seek (fast for specific values)
SELECT * FROM employees 
WHERE department_id = 5;

-- Covering index (includes all needed columns)
CREATE INDEX idx_dept_covering ON employees(department_id) INCLUDE (name, salary);

-- This query can be satisfied entirely from the index
SELECT name, salary 
FROM employees 
WHERE department_id = 5;
```

**Key Differences:**
- **Storage**: Clustered physically orders data, non-clustered creates separate structure
- **Quantity**: One clustered per table, multiple non-clustered allowed
- **Performance**: Clustered faster for ranges, non-clustered faster for seeks
- **Space**: Clustered uses less space, non-clustered requires additional storage