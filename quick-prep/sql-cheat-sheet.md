# 🗄️ SQL Cheat Sheet for Data Engineering

## 🔍 **Basic Queries**
```sql
-- Select with conditions
SELECT column1, column2 
FROM table_name 
WHERE condition 
ORDER BY column1 DESC;

-- Aggregations
SELECT department, COUNT(*), AVG(salary)
FROM employees 
GROUP BY department 
HAVING COUNT(*) > 5;
```

## 🔗 **JOINs**
```sql
-- Inner Join
SELECT a.*, b.name
FROM orders a
INNER JOIN customers b ON a.customer_id = b.id;

-- Left Join (keep all from left table)
SELECT a.*, b.name
FROM orders a
LEFT JOIN customers b ON a.customer_id = b.id;
```

## 📊 **Window Functions**
```sql
-- Running total
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- Rank within groups
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;
```

## 🔄 **CTEs (Common Table Expressions)**
```sql
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', order_date) as month,
           SUM(amount) as total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT month, total_sales,
       LAG(total_sales) OVER (ORDER BY month) as prev_month
FROM monthly_sales;
```

## 🚀 **Performance Tips**
- Use `LIMIT` when testing queries
- Index frequently queried columns
- Use `EXPLAIN` to analyze query plans
- Avoid `SELECT *` in production
- Use `WHERE` before `GROUP BY`