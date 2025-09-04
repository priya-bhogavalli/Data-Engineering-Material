# Apache Pig Key Concepts

## 📋 Table of Contents
1. [What is Apache Pig?](#what-is-apache-pig)
2. [Core Architecture](#core-architecture)
3. [Pig Latin Language](#pig-latin-language)
4. [Data Types](#data-types)
5. [Execution Modes](#execution-modes)
6. [Key Operations](#key-operations)
7. [Performance Optimization](#performance-optimization)
8. [Integration with Hadoop Ecosystem](#integration-with-hadoop-ecosystem)

---

## What is Apache Pig?

Apache Pig is a high-level platform for creating programs that run on Apache Hadoop. It provides a high-level scripting language called **Pig Latin** that allows developers to express data analysis programs in a more intuitive way than writing raw MapReduce jobs.

### Key Benefits
- **Ease of Programming**: Reduces development time by 10x compared to MapReduce
- **Optimization**: Automatic optimization of execution plans
- **Extensibility**: Support for User Defined Functions (UDFs)
- **Multi-query Optimization**: Efficient execution of multiple queries
- **Schema Flexibility**: Works with structured and unstructured data

---

## Core Architecture

### Pig Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Pig Latin     │────│   Pig Compiler   │────│   MapReduce     │
│   Scripts       │    │   (Optimizer)    │    │   Jobs          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Parser        │    │   Logical Plan   │    │   Hadoop        │
│                 │    │   Physical Plan  │    │   Cluster       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Execution Process
1. **Parsing**: Pig Latin script is parsed and syntax checked
2. **Logical Plan**: Creates logical plan with operators
3. **Optimization**: Optimizes the logical plan
4. **Physical Plan**: Converts to physical plan with MapReduce jobs
5. **Execution**: Submits jobs to Hadoop cluster

---

## Pig Latin Language

### Basic Syntax
```pig
-- Load data
data = LOAD 'input.txt' AS (name:chararray, age:int, salary:double);

-- Transform data
adults = FILTER data BY age >= 18;
high_earners = FILTER adults BY salary > 50000;

-- Group and aggregate
by_age = GROUP adults BY age;
age_stats = FOREACH by_age GENERATE 
    group AS age, 
    COUNT(adults) AS count,
    AVG(adults.salary) AS avg_salary;

-- Store results
STORE age_stats INTO 'output';
```

### Key Language Features
- **Declarative**: Describes what to do, not how to do it
- **Dataflow**: Operations form a directed acyclic graph (DAG)
- **Lazy Evaluation**: Operations are not executed until STORE or DUMP
- **Schema Optional**: Can work with or without schema definitions

---

## Data Types

### Simple Types
| Type | Description | Example |
|------|-------------|---------|
| `int` | 32-bit signed integer | `42` |
| `long` | 64-bit signed integer | `1234567890L` |
| `float` | 32-bit floating point | `3.14f` |
| `double` | 64-bit floating point | `3.14159` |
| `chararray` | String (UTF-8) | `'Hello World'` |
| `bytearray` | Blob | Binary data |

### Complex Types
```pig
-- Tuple: Ordered set of fields
customer = (123, 'John Doe', 25);

-- Bag: Collection of tuples
orders = {(1, 100.0), (2, 250.0), (3, 75.0)};

-- Map: Key-value pairs
metadata = ['country'#'USA', 'state'#'CA', 'city'#'SF'];
```

### Schema Definition
```pig
-- With schema
customers = LOAD 'customers.txt' AS (
    id:int,
    name:chararray,
    age:int,
    orders:bag{order:(order_id:int, amount:double)},
    metadata:map[]
);

-- Without schema (all fields are bytearray)
raw_data = LOAD 'data.txt';
```

---

## Execution Modes

### Local Mode
- Runs on single machine
- Uses local file system
- Good for development and testing

```bash
pig -x local script.pig
```

### MapReduce Mode (Hadoop Mode)
- Runs on Hadoop cluster
- Uses HDFS
- Production environment

```bash
pig -x mapreduce script.pig
```

### Tez Mode
- Uses Apache Tez execution engine
- Better performance than MapReduce
- Supports complex DAGs

```bash
pig -x tez script.pig
```

---

## Key Operations

### Data Loading and Storing
```pig
-- Basic load
data = LOAD 'input.txt';

-- Load with schema and custom delimiter
data = LOAD 'input.csv' USING PigStorage(',') 
    AS (id:int, name:chararray, age:int);

-- Load from HDFS
data = LOAD 'hdfs://namenode:port/path/input.txt' AS (field1, field2);

-- Store with compression
STORE result INTO 'output' USING PigStorage(',', '-c gz');
```

### Filtering and Selection
```pig
-- Simple filter
adults = FILTER customers BY age >= 18;

-- Complex conditions
qualified = FILTER customers BY 
    age >= 18 AND age <= 65 AND 
    salary > 30000 AND 
    name IS NOT NULL;

-- Pattern matching
tech_employees = FILTER employees BY position MATCHES '.*Engineer.*';
```

### Grouping and Aggregation
```pig
-- Group by single field
by_department = GROUP employees BY department;

-- Group by multiple fields
by_dept_location = GROUP employees BY (department, location);

-- Group all records
all_employees = GROUP employees ALL;

-- Aggregation functions
stats = FOREACH by_department GENERATE 
    group AS department,
    COUNT(employees) AS employee_count,
    AVG(employees.salary) AS avg_salary,
    MIN(employees.salary) AS min_salary,
    MAX(employees.salary) AS max_salary;
```

### Joins
```pig
-- Inner join
result = JOIN customers BY id, orders BY customer_id;

-- Left outer join
result = JOIN customers BY id LEFT OUTER, orders BY customer_id;

-- Multiple table join
result = JOIN customers BY id, orders BY customer_id, products BY id;

-- Replicated join (for small tables)
result = JOIN large_table BY key, small_table BY key USING 'replicated';
```

### Sorting and Ordering
```pig
-- Order by single field
sorted = ORDER customers BY name;

-- Order by multiple fields
sorted = ORDER customers BY department ASC, salary DESC;

-- Limit results
top_10 = LIMIT sorted 10;
```

---

## Performance Optimization

### Multi-query Optimization
```pig
-- Pig automatically optimizes shared operations
data = LOAD 'input' AS (name:chararray, age:int, salary:double);
adults = FILTER data BY age >= 18;

-- These two operations share the 'adults' relation
high_earners = FILTER adults BY salary > 50000;
seniors = FILTER adults BY age >= 65;

STORE high_earners INTO 'high_earners';
STORE seniors INTO 'seniors';
```

### Join Optimization
```pig
-- Use appropriate join strategy
-- Replicated join for small tables
small_lookup = LOAD 'lookup.txt' AS (id:int, description:chararray);
large_data = LOAD 'data.txt' AS (id:int, value:double);
result = JOIN large_data BY id, small_lookup BY id USING 'replicated';

-- Skewed join for data with hot keys
result = JOIN table1 BY key, table2 BY key USING 'skewed';

-- Merge join for pre-sorted data
sorted1 = ORDER table1 BY key;
sorted2 = ORDER table2 BY key;
result = JOIN sorted1 BY key, sorted2 BY key USING 'merge';
```

### Parallelism Control
```pig
-- Set default parallelism
SET default_parallel 10;

-- Set parallelism for specific operations
grouped = GROUP data BY category PARALLEL 5;
ordered = ORDER data BY timestamp PARALLEL 8;
```

### Memory Management
```pig
-- Configure memory settings
SET pig.cachedbag.memusage 0.2;
SET pig.spill.size.threshold 5000000;
SET pig.spill.gc.activation.size 40000000;
```

---

## Integration with Hadoop Ecosystem

### HBase Integration
```pig
-- Load from HBase
raw = LOAD 'hbase://users' 
    USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
        'info:name info:age', '-loadKey true'
    ) AS (rowkey:chararray, name:chararray, age:int);

-- Store to HBase
STORE processed INTO 'hbase://processed_users' 
    USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
        'info:name info:age'
    );
```

### Hive Integration
```pig
-- Use HCatalog to access Hive tables
raw = LOAD 'database.table' USING org.apache.hive.hcatalog.pig.HCatLoader();

-- Store to Hive table
STORE processed INTO 'database.processed_table' 
    USING org.apache.hive.hcatalog.pig.HCatStorer();
```

### Streaming with External Programs
```pig
-- Use external scripts
data = LOAD 'input.txt' AS (line:chararray);
processed = STREAM data THROUGH 'python process.py' AS (result:chararray);

-- Custom streaming with serializers
DEFINE CMD 'python process.py' 
    INPUT(stdin USING PigStreaming(','))
    OUTPUT(stdout USING PigStreaming(','));
```

### User Defined Functions (UDFs)
```java
// Java UDF example
public class UPPER extends EvalFunc<String> {
    public String exec(Tuple input) throws IOException {
        if (input == null || input.size() == 0) return null;
        String str = (String) input.get(0);
        return str.toUpperCase();
    }
}
```

```pig
-- Register and use UDF
REGISTER 'myudfs.jar';
DEFINE UPPER com.example.UPPER();

data = LOAD 'input' AS (name:chararray);
result = FOREACH data GENERATE UPPER(name);
```

---

## Best Practices

### Development Best Practices
1. **Use Schemas**: Define schemas for better performance and error detection
2. **Filter Early**: Apply filters as early as possible in the pipeline
3. **Avoid Unnecessary Operations**: Remove unused columns and operations
4. **Use Appropriate Data Types**: Choose the right data types for your data
5. **Test with Small Datasets**: Develop and test with small datasets first

### Performance Best Practices
1. **Optimize Joins**: Use appropriate join strategies (replicated, skewed, merge)
2. **Control Parallelism**: Set appropriate parallelism levels
3. **Minimize Data Movement**: Reduce shuffling by optimizing operations
4. **Use Combiners**: Enable combiners for aggregation operations
5. **Monitor Execution**: Use Pig's built-in monitoring and profiling tools

### Production Best Practices
1. **Error Handling**: Implement comprehensive error handling
2. **Logging**: Use proper logging for debugging and monitoring
3. **Configuration Management**: Use external configuration files
4. **Resource Management**: Monitor and manage cluster resources
5. **Security**: Implement proper security measures for data access

---

## Common Use Cases

### ETL Processing
```pig
-- Extract, Transform, Load pipeline
raw_data = LOAD 'raw/sales_data.txt' AS (
    date:chararray, product:chararray, 
    quantity:int, price:double, customer:chararray
);

-- Clean and validate data
clean_data = FILTER raw_data BY 
    date IS NOT NULL AND 
    quantity > 0 AND 
    price > 0;

-- Transform data
transformed = FOREACH clean_data GENERATE 
    ToDate(date, 'yyyy-MM-dd') AS sale_date,
    UPPER(product) AS product_name,
    quantity,
    price,
    quantity * price AS total_amount,
    UPPER(customer) AS customer_name;

-- Aggregate by product
product_sales = GROUP transformed BY product_name;
product_summary = FOREACH product_sales GENERATE 
    group AS product,
    SUM(transformed.total_amount) AS total_sales,
    COUNT(transformed) AS transaction_count;

STORE product_summary INTO 'output/product_sales';
```

### Log Analysis
```pig
-- Web log analysis
logs = LOAD 'access.log' AS (
    ip:chararray, timestamp:chararray, 
    method:chararray, url:chararray, 
    status:int, size:long
);

-- Filter successful requests
successful = FILTER logs BY status >= 200 AND status < 300;

-- Extract page views
page_views = FOREACH successful GENERATE 
    ip, 
    REGEX_EXTRACT(url, '([^?]+)', 1) AS page;

-- Count page views
page_counts = GROUP page_views BY page;
popular_pages = FOREACH page_counts GENERATE 
    group AS page,
    COUNT(page_views) AS view_count;

-- Top 10 pages
top_pages = ORDER popular_pages BY view_count DESC;
top_10 = LIMIT top_pages 10;

STORE top_10 INTO 'output/top_pages';
```

---

## 🎯 Key Takeaways

1. **High-Level Abstraction**: Pig provides a higher-level abstraction than MapReduce
2. **Dataflow Programming**: Think in terms of data transformations and flows
3. **Automatic Optimization**: Pig automatically optimizes execution plans
4. **Extensibility**: UDFs allow custom functionality
5. **Ecosystem Integration**: Works well with other Hadoop ecosystem tools
6. **Schema Flexibility**: Can work with or without predefined schemas
7. **Performance Tuning**: Understanding execution model is key to optimization

Apache Pig is particularly well-suited for ETL operations, data preparation, and ad-hoc analysis tasks where the procedural nature of Pig Latin provides more control than SQL-like languages.