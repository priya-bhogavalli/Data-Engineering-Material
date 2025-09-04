# Apache Pig Interview Questions & Answers

## 📋 Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Pig Latin Language](#pig-latin-language)
3. [Data Types & Operations](#data-types--operations)
4. [Performance & Optimization](#performance--optimization)
5. [Integration & Ecosystem](#integration--ecosystem)
6. [Advanced Topics](#advanced-topics)
7. [Troubleshooting](#troubleshooting)

---

## Basic Concepts

### 1. What is Apache Pig and what are its main advantages?

**Answer:**
Apache Pig is a high-level platform for creating programs that run on Apache Hadoop. It provides a high-level scripting language called Pig Latin for data analysis.

**Key Advantages:**
- **Ease of Programming**: Pig Latin is easier than writing MapReduce jobs
- **Optimization**: Automatic optimization of execution plans
- **Extensibility**: Support for User Defined Functions (UDFs)
- **Multi-query Optimization**: Efficient execution of multiple queries
- **Schema Flexibility**: Works with structured and unstructured data

**Example:**
```pig
-- Simple word count in Pig Latin
lines = LOAD 'input.txt' AS (line:chararray);
words = FOREACH lines GENERATE FLATTEN(TOKENIZE(line)) AS word;
grouped = GROUP words BY word;
counts = FOREACH grouped GENERATE group, COUNT(words);
STORE counts INTO 'output';
```

### 2. Explain the difference between Pig and Hive.

**Answer:**

| Aspect | Apache Pig | Apache Hive |
|--------|------------|-------------|
| **Language** | Pig Latin (procedural) | HiveQL (declarative, SQL-like) |
| **Data Model** | Schema-on-read | Schema-on-write |
| **Use Case** | ETL, data transformation | Data warehousing, analytics |
| **Learning Curve** | Moderate | Easy for SQL users |
| **Optimization** | Manual + automatic | Automatic query optimization |
| **Target Users** | Developers, data engineers | Analysts, SQL users |

### 3. What are the execution modes in Pig?

**Answer:**
Pig has two execution modes:

**1. Local Mode:**
- Runs on single machine
- Uses local file system
- Good for development and testing
```bash
pig -x local script.pig
```

**2. MapReduce Mode (Hadoop Mode):**
- Runs on Hadoop cluster
- Uses HDFS
- Production environment
```bash
pig -x mapreduce script.pig
```

### 4. Explain Pig's execution process.

**Answer:**
Pig execution follows these steps:

1. **Parsing**: Pig Latin script is parsed and checked for syntax
2. **Logical Plan**: Creates logical plan with operators
3. **Optimization**: Optimizes the logical plan
4. **Physical Plan**: Converts to physical plan with MapReduce jobs
5. **Execution**: Submits jobs to Hadoop cluster

```pig
-- Each line creates part of the execution plan
data = LOAD 'input' AS (name:chararray, age:int);  -- Load operator
filtered = FILTER data BY age > 25;                -- Filter operator
result = ORDER filtered BY name;                   -- Order operator
STORE result INTO 'output';                        -- Store operator
```

---

## Pig Latin Language

### 5. What are the main data types in Pig?

**Answer:**

**Simple Types:**
- `int`: 32-bit signed integer
- `long`: 64-bit signed integer
- `float`: 32-bit floating point
- `double`: 64-bit floating point
- `chararray`: String (UTF-8)
- `bytearray`: Blob

**Complex Types:**
- `tuple`: Ordered set of fields
- `bag`: Collection of tuples
- `map`: Key-value pairs

**Example:**
```pig
-- Schema definition
data = LOAD 'input' AS (
    id:int,
    name:chararray,
    scores:bag{t:(subject:chararray, score:int)},
    metadata:map[]
);
```

### 6. Explain the LOAD and STORE operations in Pig.

**Answer:**

**LOAD Operation:**
```pig
-- Basic load
data = LOAD 'input.txt';

-- Load with schema
data = LOAD 'input.txt' AS (name:chararray, age:int, salary:double);

-- Load with custom loader
data = LOAD 'input.json' USING JsonLoader('name:chararray, age:int');

-- Load from HDFS
data = LOAD 'hdfs://namenode:port/path/input.txt' AS (field1, field2);
```

**STORE Operation:**
```pig
-- Basic store
STORE result INTO 'output';

-- Store with custom format
STORE result INTO 'output' USING PigStorage(',');

-- Store as JSON
STORE result INTO 'output.json' USING JsonStorage();
```

### 7. What are the different JOIN operations in Pig?

**Answer:**

**1. Inner Join:**
```pig
customers = LOAD 'customers' AS (id:int, name:chararray);
orders = LOAD 'orders' AS (order_id:int, customer_id:int, amount:double);
result = JOIN customers BY id, orders BY customer_id;
```

**2. Left Outer Join:**
```pig
result = JOIN customers BY id LEFT OUTER, orders BY customer_id;
```

**3. Right Outer Join:**
```pig
result = JOIN customers BY id RIGHT OUTER, orders BY customer_id;
```

**4. Full Outer Join:**
```pig
result = JOIN customers BY id FULL OUTER, orders BY customer_id;
```

**5. Self Join:**
```pig
employees = LOAD 'employees' AS (id:int, name:chararray, manager_id:int);
result = JOIN employees BY manager_id, employees BY id;
```

### 8. Explain GROUP BY and its variations in Pig.

**Answer:**

**Basic GROUP BY:**
```pig
sales = LOAD 'sales' AS (region:chararray, product:chararray, amount:double);
grouped = GROUP sales BY region;
-- Result: {group: region, sales: {(region, product, amount)}}
```

**GROUP BY Multiple Fields:**
```pig
grouped = GROUP sales BY (region, product);
```

**GROUP ALL:**
```pig
all_grouped = GROUP sales ALL;
-- Creates single group with all records
```

**Nested GROUP BY:**
```pig
by_region = GROUP sales BY region;
result = FOREACH by_region {
    by_product = GROUP sales BY product;
    GENERATE group AS region, by_product;
};
```

---

## Data Types & Operations

### 9. How do you handle nested data structures in Pig?

**Answer:**

**Working with Bags:**
```pig
-- Sample data with nested structure
students = LOAD 'students' AS (
    name:chararray, 
    courses:bag{t:(course:chararray, grade:int)}
);

-- Flatten nested data
flattened = FOREACH students GENERATE 
    name, 
    FLATTEN(courses) AS (course, grade);

-- Aggregate nested data
summary = FOREACH students GENERATE 
    name,
    COUNT(courses) AS course_count,
    AVG(courses.grade) AS avg_grade;
```

**Working with Maps:**
```pig
-- Load data with map
user_data = LOAD 'users' AS (id:int, metadata:map[]);

-- Access map values
result = FOREACH user_data GENERATE 
    id,
    metadata#'country' AS country,
    metadata#'age' AS age;
```

### 10. What are User Defined Functions (UDFs) in Pig?

**Answer:**
UDFs extend Pig's functionality with custom logic.

**Types of UDFs:**
1. **Eval Functions**: Process individual tuples
2. **Aggregate Functions**: Process bags of tuples
3. **Filter Functions**: Return boolean values

**Java UDF Example:**
```java
public class UPPER extends EvalFunc<String> {
    public String exec(Tuple input) throws IOException {
        if (input == null || input.size() == 0)
            return null;
        String str = (String) input.get(0);
        return str.toUpperCase();
    }
}
```

**Using UDF in Pig:**
```pig
REGISTER 'myudfs.jar';
DEFINE UPPER com.example.UPPER();

data = LOAD 'input' AS (name:chararray);
result = FOREACH data GENERATE UPPER(name);
```

### 11. Explain FILTER operation with examples.

**Answer:**

**Basic Filtering:**
```pig
employees = LOAD 'employees' AS (name:chararray, age:int, salary:double);

-- Simple filter
adults = FILTER employees BY age >= 18;

-- Multiple conditions
high_earners = FILTER employees BY age > 25 AND salary > 50000;

-- String operations
tech_employees = FILTER employees BY name MATCHES '.*Engineer.*';

-- Null handling
valid_data = FILTER employees BY name IS NOT NULL AND age IS NOT NULL;
```

**Complex Filtering:**
```pig
-- Filter with nested conditions
sales = LOAD 'sales' AS (region:chararray, amount:double, date:chararray);
recent_high_sales = FILTER sales BY 
    amount > 1000 AND 
    (region == 'North' OR region == 'South') AND
    date >= '2023-01-01';
```

---

## Performance & Optimization

### 12. What are the optimization techniques in Pig?

**Answer:**

**1. Multi-query Optimization:**
```pig
-- Pig automatically optimizes multiple queries sharing common operations
data = LOAD 'input' AS (name:chararray, age:int, salary:double);
adults = FILTER data BY age >= 18;
high_earners = FILTER adults BY salary > 50000;
seniors = FILTER adults BY age >= 65;
-- Pig optimizes to avoid recomputing 'adults'
```

**2. Join Optimization:**
```pig
-- Use replicated join for small datasets
small_table = LOAD 'small_data' AS (id:int, name:chararray);
large_table = LOAD 'large_data' AS (id:int, value:double);
result = JOIN large_table BY id, small_table BY id USING 'replicated';
```

**3. Projection Pushdown:**
```pig
-- Load only required fields
data = LOAD 'input' AS (f1, f2, f3, f4, f5);
result = FOREACH data GENERATE f1, f3;  -- Only f1, f3 are processed
```

### 13. How do you optimize JOIN operations in Pig?

**Answer:**

**1. Replicated Join (Fragment-Replicate Join):**
```pig
-- For small tables that fit in memory
large_table = LOAD 'large_data' AS (id:int, value:double);
small_table = LOAD 'small_data' AS (id:int, name:chararray);
result = JOIN large_table BY id, small_table BY id USING 'replicated';
```

**2. Skewed Join:**
```pig
-- For data with skewed keys
result = JOIN table1 BY key, table2 BY key USING 'skewed';
```

**3. Merge Join:**
```pig
-- For pre-sorted data
sorted1 = ORDER table1 BY key;
sorted2 = ORDER table2 BY key;
result = JOIN sorted1 BY key, sorted2 BY key USING 'merge';
```

**4. Join Order Optimization:**
```pig
-- Place largest table first
result = JOIN large_table BY key, medium_table BY key, small_table BY key;
```

### 14. What is the PARALLEL clause and how does it affect performance?

**Answer:**
The PARALLEL clause controls the number of reduce tasks for operations.

**Usage:**
```pig
-- Set parallelism for specific operation
grouped = GROUP data BY category PARALLEL 10;

-- Set default parallelism
SET default_parallel 20;

-- Different operations with parallelism
data = LOAD 'input' AS (category:chararray, value:int);
grouped = GROUP data BY category PARALLEL 5;
ordered = ORDER grouped BY group PARALLEL 3;
```

**Guidelines:**
- **Too few reducers**: Underutilized cluster, slow processing
- **Too many reducers**: Overhead, small files
- **Rule of thumb**: 1 reducer per 1GB of data

---

## Integration & Ecosystem

### 15. How does Pig integrate with HBase?

**Answer:**

**Loading from HBase:**
```pig
-- Load from HBase table
REGISTER 'hbase-client.jar';
raw = LOAD 'hbase://users' 
    USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
        'info:name info:age contact:email', 
        '-loadKey true'
    ) AS (
        rowkey:chararray, 
        name:chararray, 
        age:int, 
        email:chararray
    );
```

**Storing to HBase:**
```pig
-- Store to HBase
processed_data = FOREACH raw GENERATE 
    rowkey, 
    name, 
    age, 
    email;

STORE processed_data INTO 'hbase://processed_users' 
    USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
        'info:name info:age contact:email'
    );
```

### 16. How do you use Pig with Amazon S3?

**Answer:**

**Loading from S3:**
```pig
-- Load from S3 bucket
data = LOAD 's3://my-bucket/input/data.txt' AS (field1, field2, field3);

-- Load with credentials (not recommended for production)
data = LOAD 's3://my-bucket/input/' AS (field1, field2);
```

**Storing to S3:**
```pig
-- Store to S3
STORE result INTO 's3://my-bucket/output/';

-- Store with compression
STORE result INTO 's3://my-bucket/output/' USING PigStorage(',', '-c gz');
```

**Configuration:**
```pig
-- Set S3 configuration
SET fs.s3a.access.key 'your-access-key';
SET fs.s3a.secret.key 'your-secret-key';
SET fs.s3a.endpoint 's3.amazonaws.com';
```

---

## Advanced Topics

### 17. What is the difference between COGROUP and JOIN?

**Answer:**

**JOIN:**
- Performs inner join by default
- Flattens the result
- Only matching records

**COGROUP:**
- Groups data from multiple relations
- Preserves bag structure
- Includes non-matching records

**Example:**
```pig
customers = LOAD 'customers' AS (id:int, name:chararray);
orders = LOAD 'orders' AS (customer_id:int, amount:double);

-- JOIN result: flat structure
joined = JOIN customers BY id, orders BY customer_id;
-- Result: (id, name, customer_id, amount)

-- COGROUP result: nested structure
cogrouped = COGROUP customers BY id, orders BY customer_id;
-- Result: (group, customers: {(id, name)}, orders: {(customer_id, amount)})
```

### 18. Explain streaming in Pig.

**Answer:**
Streaming allows you to use external programs in Pig scripts.

**Basic Streaming:**
```pig
-- Use external script
data = LOAD 'input.txt' AS (line:chararray);
processed = STREAM data THROUGH 'python process.py' AS (result:chararray);
```

**Advanced Streaming:**
```pig
-- Stream with custom serializer/deserializer
DEFINE CMD 'python process.py' 
    INPUT(stdin USING PigStreaming(','))
    OUTPUT(stdout USING PigStreaming(','));

data = LOAD 'input' AS (f1:int, f2:chararray);
result = STREAM data THROUGH CMD AS (output1:int, output2:chararray);
```

**Python Script Example (process.py):**
```python
#!/usr/bin/env python
import sys

for line in sys.stdin:
    fields = line.strip().split(',')
    # Process fields
    processed = ','.join([field.upper() for field in fields])
    print(processed)
```

### 19. How do you handle schema evolution in Pig?

**Answer:**

**Flexible Schema Loading:**
```pig
-- Load without strict schema
data = LOAD 'input' AS (f1, f2, f3);

-- Handle missing fields
safe_data = FOREACH data GENERATE 
    (f1 IS NULL ? 'default' : f1) AS field1,
    (f2 IS NULL ? 0 : f2) AS field2,
    (f3 IS NULL ? 'unknown' : f3) AS field3;
```

**Schema Validation:**
```pig
-- Validate and clean data
raw_data = LOAD 'input' AS (id, name, age, salary);
clean_data = FILTER raw_data BY 
    id IS NOT NULL AND 
    name IS NOT NULL AND 
    age IS NOT NULL;
```

**Handling Different File Formats:**
```pig
-- Union data from different sources
old_format = LOAD 'old_data' AS (id:int, name:chararray);
new_format = LOAD 'new_data' AS (id:int, name:chararray, email:chararray);

-- Normalize schemas
old_normalized = FOREACH old_format GENERATE id, name, '' AS email;
combined = UNION old_normalized, new_format;
```

---

## Troubleshooting

### 20. What are common performance issues in Pig and how to resolve them?

**Answer:**

**1. Data Skew:**
```pig
-- Problem: Uneven data distribution
-- Solution: Use skewed join or sampling
result = JOIN table1 BY key, table2 BY key USING 'skewed';

-- Or use custom partitioner
SET pig.exec.reducers.bytes.per.reducer 1000000000;
```

**2. Small Files Problem:**
```pig
-- Problem: Too many small output files
-- Solution: Increase parallelism or use fewer reducers
SET default_parallel 1;
STORE result INTO 'output';
```

**3. Memory Issues:**
```pig
-- Problem: Out of memory errors
-- Solution: Increase heap size and optimize operations
SET mapred.child.java.opts '-Xmx2048m';
SET pig.cachedbag.memusage 0.2;
```

**4. Inefficient Joins:**
```pig
-- Problem: Large cross products
-- Solution: Filter before join
filtered1 = FILTER table1 BY condition;
filtered2 = FILTER table2 BY condition;
result = JOIN filtered1 BY key, filtered2 BY key;
```

### 21. How do you debug Pig scripts?

**Answer:**

**1. Use DESCRIBE and EXPLAIN:**
```pig
data = LOAD 'input' AS (name:chararray, age:int);
DESCRIBE data;  -- Shows schema
EXPLAIN data;   -- Shows execution plan
```

**2. Use DUMP for small datasets:**
```pig
sample_data = LIMIT data 10;
DUMP sample_data;  -- Shows actual data
```

**3. Use ILLUSTRATE:**
```pig
ILLUSTRATE data;  -- Shows sample data flow
```

**4. Enable Debug Logging:**
```bash
pig -debug DEBUG script.pig
```

**5. Check Intermediate Results:**
```pig
-- Store intermediate results for debugging
intermediate = FILTER data BY age > 25;
STORE intermediate INTO 'debug/intermediate';
final_result = ORDER intermediate BY name;
```

### 22. What are the limitations of Apache Pig?

**Answer:**

**Limitations:**
1. **No Real-time Processing**: Batch processing only
2. **Limited SQL Features**: No advanced SQL operations like window functions
3. **Schema Flexibility**: Can lead to runtime errors
4. **Learning Curve**: Pig Latin syntax is unique
5. **Performance**: Generally slower than optimized MapReduce or Spark
6. **Limited Ecosystem**: Fewer tools compared to Spark/Hive
7. **No ACID Properties**: No transaction support
8. **Debugging Difficulty**: Limited debugging tools

**When to Use Pig:**
- ETL operations on large datasets
- Data transformation and cleaning
- Prototyping data processing workflows
- When you need procedural data processing

**When Not to Use Pig:**
- Real-time processing requirements
- Complex analytical queries (use Hive/Spark SQL)
- Small datasets (overhead not justified)
- When team prefers SQL-like syntax

---

## 🎯 Key Takeaways

1. **Pig is ideal for ETL**: Great for data transformation and preparation
2. **Procedural approach**: Different from SQL's declarative approach
3. **Optimization matters**: Understanding execution plans improves performance
4. **Schema flexibility**: Both advantage and challenge
5. **Integration capabilities**: Works well with Hadoop ecosystem
6. **UDF extensibility**: Custom functions extend capabilities
7. **Debugging tools**: Use DESCRIBE, EXPLAIN, and ILLUSTRATE effectively

---

*This comprehensive guide covers the most important Apache Pig interview questions. Practice with real datasets and understand the execution model for better performance in interviews.*