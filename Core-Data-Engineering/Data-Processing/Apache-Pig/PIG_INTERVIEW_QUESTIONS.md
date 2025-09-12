
### Q1: What is Apache Pig and what problems does it solve?
**Answer:**
Apache Pig is a high-level platform for creating programs that run on Apache Hadoop, using a language called Pig Latin.

**Key Problems Solved:**
- **Simplifies MapReduce**: Abstracts complex MapReduce programming
- **Data Flow Language**: Procedural language for data transformations
- **Rapid Development**: Faster development than Java MapReduce
- **ETL Processing**: Ideal for Extract, Transform, Load operations
- **Ad-hoc Analysis**: Quick data exploration and analysis

**Core Features:**
- Pig Latin scripting language
- Automatic optimization of data flow
- Extensible with User Defined Functions (UDFs)
- Integration with Hadoop ecosystem
- Support for complex data types

### Q2: Explain the difference between Pig and Hive
**Answer:**
**Apache Pig vs Apache Hive:**

| Aspect | Pig | Hive |
|--------|-----|------|
| **Language** | Pig Latin (Procedural) | HiveQL (Declarative/SQL-like) |
| **Approach** | Data flow oriented | Database/warehouse oriented |
| **Learning Curve** | Moderate | Easy for SQL users |
| **Flexibility** | High procedural control | Limited procedural control |
| **Schema** | Schema optional | Schema required |
| **Use Case** | ETL, data processing | Data warehousing, analytics |
| **Optimization** | Manual optimization | Automatic query optimization |
| **Target Users** | Developers, data engineers | Analysts, business users |

**Example Comparison:**
```pig
-- Pig Latin
data = LOAD 'input.txt' AS (name:chararray, age:int);
filtered = FILTER data BY age > 25;
grouped = GROUP filtered BY name;
result = FOREACH grouped GENERATE group, COUNT(filtered);
STORE result INTO 'output';
```

```sql
-- HiveQL
SELECT name, COUNT(*) 
FROM input_table 
WHERE age > 25 
GROUP BY name;
```

### Q3: What are the advantages and limitations of Apache Pig?
**Answer:**
**Advantages:**
- Easier than writing MapReduce jobs
- Handles complex data types (bags, tuples, maps)
- Automatic optimization and parallelization
- Extensible with UDFs in multiple languages
- Good for ETL and data transformation tasks
- Schema flexibility (schema-on-read)
- Integration with Hadoop ecosystem

**Limitations:**
- Learning curve for Pig Latin syntax
- Not suitable for real-time processing
- Limited debugging capabilities
- No built-in support for iterative algorithms
- Slower than optimized MapReduce for some tasks
- Limited SQL-like features compared to Hive
- Not ideal for interactive queries

---

## 🐷 Pig Latin Language

### Q4: Explain Pig Latin syntax and basic operations
**Answer:**
**Pig Latin Syntax:**
Pig Latin is a data flow language with procedural programming style.

**Basic Structure:**
```pig
-- Load data
data = LOAD 'input.txt' USING PigStorage(',') 
       AS (id:int, name:chararray, age:int, salary:double);

-- Transform data
filtered_data = FILTER data BY age > 25;
projected_data = FOREACH filtered_data GENERATE id, name, salary;
grouped_data = GROUP projected_data BY name;

-- Store results
STORE grouped_data INTO 'output' USING PigStorage(',');
```

**Key Characteristics:**
- Case-insensitive keywords
- Relations (datasets) are assigned to aliases
- Operations are applied to relations
- Lazy evaluation (execution happens at STORE/DUMP)
- Comments start with --

**Basic Operations:**
- **LOAD**: Read data from storage
- **STORE**: Write data to storage
- **FILTER**: Select records based on conditions
- **FOREACH**: Transform records
- **GROUP**: Group records by key
- **JOIN**: Combine relations
- **ORDER**: Sort records
- **DISTINCT**: Remove duplicates

### Q5: Explain Pig execution modes
**Answer:**
**Pig Execution Modes:**

1. **Local Mode**
   - Runs on single machine
   - Uses local file system
   - Good for development and testing
   - Limited data processing capability

```bash
# Start Pig in local mode
pig -x local

# Run script in local mode
pig -x local script.pig
```

2. **MapReduce Mode (Default)**
   - Runs on Hadoop cluster
   - Uses HDFS for storage
   - Converts Pig Latin to MapReduce jobs
   - Production mode for large datasets

```bash
# Start Pig in MapReduce mode
pig

# Run script in MapReduce mode
pig script.pig
```

3. **Tez Mode**
   - Uses Apache Tez execution engine
   - Better performance than MapReduce
   - Directed Acyclic Graph (DAG) execution
   - Reduced latency

```bash
# Start Pig with Tez
pig -x tez
```

**Mode Comparison:**
| Mode | Performance | Scalability | Use Case |
|------|-------------|-------------|----------|
| Local | Fast startup | Limited | Development/Testing |
| MapReduce | Good | High | Production batch processing |
| Tez | Better | High | Interactive/faster processing |

### Q6: What are the different data loading and storing options in Pig?
**Answer:**
**Data Loading Options:**

1. **PigStorage (Default)**
```pig
-- Load CSV data
data = LOAD 'input.csv' USING PigStorage(',') 
       AS (id:int, name:chararray, age:int);

-- Custom delimiter
data = LOAD 'input.txt' USING PigStorage('\t');
```

2. **TextLoader**
```pig
-- Load as single field
lines = LOAD 'input.txt' USING TextLoader() AS (line:chararray);
```

3. **BinStorage**
```pig
-- Binary format for intermediate storage
STORE processed_data INTO 'temp' USING BinStorage();
temp_data = LOAD 'temp' USING BinStorage();
```

4. **JsonLoader**
```pig
-- Load JSON data
json_data = LOAD 'input.json' USING JsonLoader(
    'id:int, name:chararray, details:map[]'
);
```

5. **HBaseStorage**
```pig
-- Load from HBase
hbase_data = LOAD 'hbase://table_name' 
             USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
                 'cf:col1 cf:col2'
             );
```

**Data Storing Options:**
```pig
-- Store with custom delimiter
STORE result INTO 'output' USING PigStorage('|');

-- Store as JSON
STORE result INTO 'output.json' USING JsonStorage();

-- Store to HBase
STORE result INTO 'hbase://output_table' 
      USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
          'cf:col1 cf:col2'
      );
```

---

## 📊 Data Types & Operations

### Q7: Explain Pig data types and their usage
**Answer:**
**Pig Data Types:**

**Scalar Types:**
```pig
-- int: 32-bit signed integer
age = 25;

-- long: 64-bit signed integer  
population = 1000000L;

-- float: 32-bit floating point
price = 19.99f;

-- double: 64-bit floating point
salary = 50000.0;

-- chararray: String
name = 'John Doe';

-- bytearray: Binary data
data = (bytearray)'binary data';

-- boolean: True/False
is_active = true;

-- datetime: Date and time
created_date = ToDate('2023-12-01', 'yyyy-MM-dd');
```

**Complex Types:**
```pig
-- Tuple: Ordered collection of fields
employee = (1, 'John', 25, 50000.0);

-- Bag: Collection of tuples
employees = {(1, 'John'), (2, 'Jane'), (3, 'Bob')};

-- Map: Key-value pairs
properties = ['color'#'blue', 'size'#'large', 'weight'#'10kg'];
```

**Schema Definition:**
```pig
data = LOAD 'input.txt' AS (
    id:int,
    name:chararray,
    details:tuple(age:int, salary:double),
    tags:bag{t:(tag:chararray)},
    properties:map[chararray]
);
```

### Q8: Explain GROUP and JOIN operations in Pig
**Answer:**
**GROUP Operation:**

1. **Simple Grouping:**
```pig
-- Group by single field
sales = LOAD 'sales.txt' AS (product:chararray, amount:double, region:chararray);
grouped = GROUP sales BY region;
-- Result: {group: region, sales: {(product, amount, region)}}

-- Group by multiple fields
grouped_multi = GROUP sales BY (product, region);
```

2. **Group All:**
```pig
-- Group all records together
all_grouped = GROUP sales ALL;
-- Result: {group: 'all', sales: {all records}}
```

3. **Aggregation after Grouping:**
```pig
grouped = GROUP sales BY region;
summary = FOREACH grouped GENERATE 
    group AS region,
    COUNT(sales) AS total_sales,
    SUM(sales.amount) AS total_amount,
    AVG(sales.amount) AS avg_amount;
```

**JOIN Operations:**

1. **Inner Join:**
```pig
customers = LOAD 'customers.txt' AS (id:int, name:chararray);
orders = LOAD 'orders.txt' AS (order_id:int, customer_id:int, amount:double);

joined = JOIN customers BY id, orders BY customer_id;
```

2. **Outer Joins:**
```pig
-- Left outer join
left_joined = JOIN customers BY id LEFT OUTER, orders BY customer_id;

-- Right outer join  
right_joined = JOIN customers BY id RIGHT OUTER, orders BY customer_id;

-- Full outer join
full_joined = JOIN customers BY id FULL OUTER, orders BY customer_id;
```

3. **Self Join:**
```pig
employees = LOAD 'employees.txt' AS (id:int, name:chararray, manager_id:int);
emp_mgr = JOIN employees BY manager_id, employees BY id;
```

4. **Multiple Joins:**
```pig
result = JOIN customers BY id, orders BY customer_id, products BY id;
```

### Q9: How do you handle nested data structures in Pig?
**Answer:**
**Working with Nested Data:**

1. **Accessing Nested Fields:**
```pig
-- Sample data with nested structure
data = LOAD 'nested.txt' AS (
    id:int,
    person:tuple(name:chararray, age:int),
    addresses:bag{addr:tuple(street:chararray, city:chararray)},
    properties:map[chararray]
);

-- Access tuple fields
names = FOREACH data GENERATE id, person.name, person.age;

-- Access map values
colors = FOREACH data GENERATE id, properties#'color';
```

2. **FLATTEN Operation:**
```pig
-- Flatten bag to create multiple rows
flattened = FOREACH data GENERATE id, FLATTEN(addresses);
-- Result: (id, street, city) for each address

-- Flatten tuple (removes tuple structure)
flat_person = FOREACH data GENERATE id, FLATTEN(person);
-- Result: (id, name, age)
```

3. **Nested FOREACH:**
```pig
-- Process nested bags
processed = FOREACH data {
    filtered_addr = FILTER addresses BY city == 'New York';
    GENERATE id, COUNT(filtered_addr) AS ny_addresses;
}
```

4. **Complex Nested Operations:**
```pig
-- Group and process nested data
grouped = GROUP data BY person.name;
result = FOREACH grouped {
    total_addresses = FLATTEN(data.addresses);
    unique_cities = DISTINCT total_addresses.city;
    GENERATE group AS name, COUNT(unique_cities) AS city_count;
}
```

---

## 🔧 Built-in Functions

### Q10: Explain commonly used built-in functions in Pig
**Answer:**
**Pig Built-in Functions:**

**String Functions:**
```pig
data = LOAD 'input.txt' AS (text:chararray);

string_ops = FOREACH data GENERATE
    UPPER(text) AS upper_text,           -- Convert to uppercase
    LOWER(text) AS lower_text,           -- Convert to lowercase  
    SUBSTRING(text, 0, 5) AS first_5,    -- Extract substring
    SIZE(text) AS text_length,           -- String length
    TRIM(text) AS trimmed,               -- Remove whitespace
    REPLACE(text, 'old', 'new') AS replaced, -- Replace text
    SPLIT(text, ',') AS split_text;      -- Split string
```

**Math Functions:**
```pig
numbers = LOAD 'numbers.txt' AS (value:double);

math_ops = FOREACH numbers GENERATE
    ABS(value) AS absolute,              -- Absolute value
    CEIL(value) AS ceiling,              -- Round up
    FLOOR(value) AS floor_val,           -- Round down
    ROUND(value) AS rounded,             -- Round to nearest
    SQRT(value) AS square_root,          -- Square root
    LOG(value) AS logarithm,             -- Natural log
    RANDOM() AS random_val;              -- Random number
```

**Date/Time Functions:**
```pig
dates = LOAD 'dates.txt' AS (date_str:chararray);

date_ops = FOREACH dates GENERATE
    ToDate(date_str, 'yyyy-MM-dd') AS parsed_date,
    CurrentTime() AS current_time,
    GetYear(ToDate(date_str, 'yyyy-MM-dd')) AS year,
    GetMonth(ToDate(date_str, 'yyyy-MM-dd')) AS month,
    AddDuration(ToDate(date_str, 'yyyy-MM-dd'), 'P1D') AS next_day;
```

**Aggregate Functions:**
```pig
sales = LOAD 'sales.txt' AS (product:chararray, amount:double);
grouped = GROUP sales BY product;

aggregates = FOREACH grouped GENERATE
    group AS product,
    COUNT(sales) AS count,               -- Count records
    SUM(sales.amount) AS total,          -- Sum values
    AVG(sales.amount) AS average,        -- Average
    MIN(sales.amount) AS minimum,        -- Minimum value
    MAX(sales.amount) AS maximum;        -- Maximum value
```

**Bag/Tuple Functions:**
```pig
data = LOAD 'input.txt' AS (items:bag{t:(item:chararray)});

bag_ops = FOREACH data GENERATE
    SIZE(items) AS item_count,           -- Count items in bag
    IsEmpty(items) AS is_empty,          -- Check if bag is empty
    FLATTEN(items) AS flattened_items;   -- Flatten bag
```

### Q11: How do you use FILTER and FOREACH operations effectively?
**Answer:**
**FILTER Operation:**

1. **Basic Filtering:**
```pig
sales = LOAD 'sales.txt' AS (product:chararray, amount:double, date:chararray);

-- Simple condition
high_sales = FILTER sales BY amount > 1000;

-- Multiple conditions
filtered = FILTER sales BY amount > 500 AND product == 'laptop';

-- String operations
recent = FILTER sales BY date MATCHES '2023-.*';

-- Null handling
clean_data = FILTER sales BY amount IS NOT NULL;
```

2. **Complex Filtering:**
```pig
-- Nested field filtering
customers = LOAD 'customers.txt' AS (
    id:int, 
    details:tuple(age:int, city:chararray)
);
adults = FILTER customers BY details.age >= 18;

-- Bag filtering
orders = LOAD 'orders.txt' AS (
    customer_id:int,
    items:bag{item:tuple(product:chararray, quantity:int)}
);
bulk_orders = FILTER orders BY SIZE(items) > 5;
```

**FOREACH Operation:**

1. **Basic Transformation:**
```pig
employees = LOAD 'employees.txt' AS (id:int, name:chararray, salary:double);

-- Simple projection
names = FOREACH employees GENERATE name;

-- Calculated fields
enhanced = FOREACH employees GENERATE 
    id,
    name,
    salary,
    salary * 1.1 AS increased_salary,
    (salary > 50000 ? 'High' : 'Low') AS salary_category;
```

2. **Complex FOREACH:**
```pig
-- Nested FOREACH
sales_data = LOAD 'sales.txt' AS (
    region:chararray,
    sales:bag{s:tuple(product:chararray, amount:double)}
);

processed = FOREACH sales_data {
    high_value = FILTER sales BY amount > 1000;
    sorted_sales = ORDER sales BY amount DESC;
    GENERATE 
        region,
        COUNT(high_value) AS high_value_count,
        FLATTEN(TOP(3, 1, sorted_sales)) AS top_sales;
}
```

3. **FOREACH with UDFs:**
```pig
-- Using built-in functions
text_data = LOAD 'text.txt' AS (content:chararray);
processed_text = FOREACH text_data GENERATE
    UPPER(content) AS upper_content,
    SIZE(TOKENIZE(content)) AS word_count,
    REGEX_EXTRACT(content, '(\\d+)', 1) AS extracted_number;
```

---

## 🔧 User Defined Functions (UDFs)

### Q12: How do you create and use UDFs in Pig?
**Answer:**
**Creating UDFs in Different Languages:**

**1. Java UDF:**
```java
// Java UDF example
package com.example.pig.udf;

import java.io.IOException;
import org.apache.pig.EvalFunc;
import org.apache.pig.data.Tuple;

public class StringLength extends EvalFunc<Integer> {
    public Integer exec(Tuple input) throws IOException {
        if (input == null || input.size() == 0) {
            return null;
        }
        
        String str = (String) input.get(0);
        return str != null ? str.length() : null;
    }
}
```

**2. Python UDF:**
```python
# Python UDF example
@outputSchema("word_count:int")
def count_words(text):
    if text is None:
        return None
    return len(text.split())
```

**3. JavaScript UDF:**
```javascript
// JavaScript UDF
pig.defineUDF('reverse_string', 'string', function(input) {
    return input.split('').reverse().join('');
});
```

**Using UDFs in Pig Scripts:**

1. **Java UDF Usage:**
```pig
-- Register JAR file
REGISTER 'myudf.jar';

-- Define UDF
DEFINE StringLength com.example.pig.udf.StringLength();

-- Use UDF
data = LOAD 'input.txt' AS (text:chararray);
result = FOREACH data GENERATE text, StringLength(text) AS length;
```

2. **Python UDF Usage:**
```pig
-- Register Python script
REGISTER 'myudf.py' USING jython AS myfuncs;

-- Use Python UDF
data = LOAD 'input.txt' AS (text:chararray);
result = FOREACH data GENERATE text, myfuncs.count_words(text) AS word_count;
```

3. **JavaScript UDF Usage:**
```pig
-- Register JavaScript file
REGISTER 'myudf.js' USING javascript AS js_funcs;

-- Use JavaScript UDF
data = LOAD 'input.txt' AS (text:chararray);
result = FOREACH data GENERATE text, js_funcs.reverse_string(text) AS reversed;
```

### Q13: What are the different types of UDFs in Pig?
**Answer:**
**Pig UDF Types:**

**1. Eval Functions (EvalFunc)**
- Most common type
- Takes tuple as input, returns single value
- Used in FOREACH statements

```java
public class MyEvalFunc extends EvalFunc<String> {
    public String exec(Tuple input) throws IOException {
        // Process input tuple and return result
        return processedResult;
    }
}
```

**2. Aggregate Functions (Algebraic)**
- Used for aggregations like SUM, COUNT
- Implements Algebraic interface for optimization
- Can be combined in MapReduce combiner

```java
public class MySum extends EvalFunc<Long> implements Algebraic {
    public String getInitial() { return Initial.class.getName(); }
    public String getIntermed() { return Intermediate.class.getName(); }
    public String getFinal() { return Final.class.getName(); }
    
    // Implementation classes for different phases
    public static class Initial extends EvalFunc<Tuple> { ... }
    public static class Intermediate extends EvalFunc<Tuple> { ... }
    public static class Final extends EvalFunc<Long> { ... }
}
```

**3. Filter Functions (FilterFunc)**
- Used in FILTER statements
- Returns boolean value
- Determines which records to keep

```java
public class MyFilter extends FilterFunc {
    public Boolean exec(Tuple input) throws IOException {
        // Return true to keep record, false to filter out
        return shouldKeepRecord(input);
    }
}
```

**4. Load/Store Functions**
- Custom data loading and storing
- Implements LoadFunc or StoreFunc interfaces

```java
public class MyLoader extends LoadFunc {
    public Tuple getNext() throws IOException {
        // Read and return next tuple
    }
    
    public InputFormat getInputFormat() throws IOException {
        // Return appropriate InputFormat
    }
}
```

---

## ⚡ Performance Optimization

### Q14: What are the key performance optimization techniques in Pig?
**Answer:**
**Pig Performance Optimization Techniques:**

**1. Execution Engine Optimization:**
```pig
-- Use Tez instead of MapReduce
SET pig.exec.mapPartAgg true;
SET pig.exec.mapPartAgg.minReduction 10;

-- Enable multiquery optimization
SET opt.multiquery true;
```

**2. Data Loading Optimization:**
```pig
-- Use appropriate storage formats
data = LOAD 'input.orc' USING OrcStorage();

-- Specify schema to avoid type inference
data = LOAD 'input.txt' USING PigStorage(',') 
       AS (id:int, name:chararray, amount:double);

-- Use LIMIT for testing
sample_data = LIMIT data 1000;
```

**3. Join Optimization:**
```pig
-- Use replicated join for small tables
small_table = LOAD 'small.txt' AS (id:int, name:chararray);
large_table = LOAD 'large.txt' AS (id:int, value:double);

-- Replicated join (broadcast small table)
joined = JOIN large_table BY id, small_table BY id USING 'replicated';

-- Skewed join for data with skew
skewed_join = JOIN table1 BY key, table2 BY key USING 'skewed';

-- Merge join for sorted data
sorted_join = JOIN table1 BY key, table2 BY key USING 'merge';
```

**4. Memory and Parallelism:**
```pig
-- Set parallelism explicitly
SET default_parallel 20;

-- Or per operation
grouped = GROUP data BY category PARALLEL 10;

-- Increase memory for operations
SET pig.cachedbag.memusage 0.2;
SET pig.skewedjoin.reduce.memusage 0.3;
```

**5. Data Organization:**
```pig
-- Use DISTINCT to remove duplicates early
unique_data = DISTINCT raw_data;

-- Filter early in the pipeline
filtered = FILTER raw_data BY amount > 0;
processed = FOREACH filtered GENERATE ...;

-- Use appropriate data types
optimized = FOREACH data GENERATE 
    (int)id,                    -- Cast to smaller type
    (float)amount;              -- Use float instead of double if precision allows
```

### Q15: How do you handle data skew in Pig?
**Answer:**
**Data Skew Handling Strategies:**

**1. Skewed Join:**
```pig
-- Identify skewed keys
customers = LOAD 'customers.txt' AS (id:int, name:chararray);
orders = LOAD 'orders.txt' AS (customer_id:int, amount:double);

-- Use skewed join
result = JOIN customers BY id, orders BY customer_id USING 'skewed';
```

**2. Sampling and Analysis:**
```pig
-- Sample data to identify skew
sample = SAMPLE orders 0.01;  -- 1% sample
key_counts = FOREACH (GROUP sample BY customer_id) 
             GENERATE group, COUNT(sample) AS count;
sorted_counts = ORDER key_counts BY count DESC;
DUMP sorted_counts;
```

**3. Custom Partitioning:**
```pig
-- Use custom partitioner for better distribution
SET pig.exec.reducers.bytes.per.reducer 1000000000;  -- 1GB per reducer
SET pig.exec.reducers.max 999;

-- Manual load balancing
balanced = FOREACH orders GENERATE 
    customer_id,
    amount,
    RANDOM() AS rand_key;  -- Add random key for distribution

grouped = GROUP balanced BY (customer_id, (int)(rand_key * 10));
```

**4. Two-Phase Aggregation:**
```pig
-- First phase: partial aggregation with random key
phase1 = FOREACH orders GENERATE 
    customer_id,
    amount,
    (int)(RANDOM() * 10) AS partition_key;

partial_agg = FOREACH (GROUP phase1 BY (customer_id, partition_key))
              GENERATE 
                  FLATTEN(group.customer_id) AS customer_id,
                  SUM(phase1.amount) AS partial_sum;

-- Second phase: final aggregation
final_result = FOREACH (GROUP partial_agg BY customer_id)
               GENERATE 
                   group AS customer_id,
                   SUM(partial_agg.partial_sum) AS total_amount;
```

**5. Replicated Join for Skewed Data:**
```pig
-- If one side is small, use replicated join
small_customers = FILTER customers BY premium_customer == true;
all_orders = LOAD 'orders.txt' AS (customer_id:int, amount:double);

-- Broadcast small table to avoid skew
premium_orders = JOIN all_orders BY customer_id, 
                      small_customers BY id USING 'replicated';
```

---

## 🔗 Integration & Ecosystem

### Q16: How does Pig integrate with other Hadoop ecosystem tools?
**Answer:**
**Pig Integration with Hadoop Ecosystem:**

**1. HDFS Integration:**
```pig
-- Read from HDFS
data = LOAD 'hdfs://namenode:port/path/to/data' AS (field1:int, field2:chararray);

-- Write to HDFS
STORE result INTO 'hdfs://namenode:port/output/path';

-- Use HDFS commands within Pig
fs -ls /user/data/
fs -mkdir /user/output/
```

**2. HBase Integration:**
```pig
-- Load from HBase
REGISTER 'hbase-client.jar';
hbase_data = LOAD 'hbase://table_name' 
             USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
                 'cf1:col1 cf1:col2 cf2:col3'
             ) AS (col1:chararray, col2:int, col3:double);

-- Store to HBase
STORE processed_data INTO 'hbase://output_table'
      USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
          'cf:col1 cf:col2'
      );
```

**3. Hive Integration:**
```pig
-- Use Hive tables in Pig
REGISTER 'hive-exec.jar';
hive_data = LOAD 'hive_table' 
            USING org.apache.hive.hcatalog.pig.HCatLoader();

-- Store to Hive table
STORE result INTO 'hive_output_table' 
      USING org.apache.hive.hcatalog.pig.HCatStorer();
```

**4. Spark Integration:**
```pig
-- Run Pig on Spark (Spork)
SET pig.exec.mapPartAgg true;
SET pig.exec.mapPartAgg.minReduction 10;

-- Pig scripts can be converted to Spark jobs
-- using tools like Spork or PigSpark
```

**5. Oozie Integration:**
```xml
<!-- Oozie workflow with Pig action -->
<workflow-app name="pig-workflow" xmlns="uri:oozie:workflow:0.5">
    <start to="pig-node"/>
    
    <action name="pig-node">
        <pig>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>pig-script.pig</script>
            <param>INPUT=${inputDir}</param>
            <param>OUTPUT=${outputDir}</param>
        </pig>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Pig job failed</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

### Q17: How do you use Pig with streaming data?
**Answer:**
**Pig with Streaming Data:**

**1. Kafka Integration:**
```pig
-- Register Kafka libraries
REGISTER 'kafka-clients.jar';
REGISTER 'pig-kafka.jar';

-- Load from Kafka
kafka_data = LOAD 'kafka://topic_name' 
             USING KafkaStorage('localhost:9092')
             AS (key:chararray, value:chararray, partition:int, offset:long);

-- Process streaming data
processed = FOREACH kafka_data GENERATE 
    key,
    REGEX_EXTRACT(value, '(\\d+)', 1) AS extracted_id,
    CurrentTime() AS processing_time;
```

**2. Flume Integration:**
```pig
-- Process Flume spooled data
flume_data = LOAD '/flume/spool/dir/*' 
             USING PigStorage('\t')
             AS (timestamp:chararray, level:chararray, message:chararray);

-- Real-time processing pattern
recent_data = FILTER flume_data BY 
    ToDate(timestamp, 'yyyy-MM-dd HH:mm:ss') > 
    SubtractDuration(CurrentTime(), 'PT1H');  -- Last hour
```

**3. Micro-batch Processing:**
```pig
-- Process data in time windows
windowed_data = LOAD 'streaming/input/${date}/${hour}/*'
                USING PigStorage(',')
                AS (id:int, event:chararray, timestamp:long);

-- Aggregate by time windows
grouped = GROUP windowed_data BY (id, timestamp / 300000);  -- 5-minute windows
aggregated = FOREACH grouped GENERATE 
    FLATTEN(group) AS (id, window),
    COUNT(windowed_data) AS event_count,
    MAX(windowed_data.timestamp) AS max_timestamp;
```

**4. Stream Processing Pattern:**
```bash
#!/bin/bash
# Continuous processing script
while true; do
    # Get current hour directory
    CURRENT_HOUR=$(date +%Y/%m/%d/%H)
    
    # Run Pig script for current hour
    pig -param input_path="/streaming/data/$CURRENT_HOUR" \
        -param output_path="/processed/data/$CURRENT_HOUR" \
        streaming_processor.pig
    
    # Wait for next processing cycle
    sleep 3600  # Process every hour
done
```

---

## 🐛 Error Handling & Debugging

### Q18: How do you debug Pig scripts and handle errors?
**Answer:**
**Pig Debugging Techniques:**

**1. Interactive Debugging:**
```pig
-- Use DESCRIBE to check schema
data = LOAD 'input.txt' AS (id:int, name:chararray, amount:double);
DESCRIBE data;

-- Use ILLUSTRATE to see sample data flow
ILLUSTRATE data;

-- Use DUMP for small datasets
sample = LIMIT data 10;
DUMP sample;

-- Use EXPLAIN to see execution plan
EXPLAIN processed_data;
```

**2. Error Handling:**
```pig
-- Handle null values
clean_data = FILTER data BY amount IS NOT NULL AND amount > 0;

-- Use conditional expressions
safe_division = FOREACH data GENERATE 
    id,
    (amount == 0 ? 0 : total/amount) AS ratio;

-- Validate data types
validated = FILTER data BY id IS NOT NULL AND (int)id == id;
```

**3. Logging and Monitoring:**
```pig
-- Enable debug logging
SET pig.logfile pig_debug.log;
SET pig.log.level DEBUG;

-- Add custom logging in UDFs
public class MyUDF extends EvalFunc<String> {
    private static final Log log = LogFactory.getLog(MyUDF.class);
    
    public String exec(Tuple input) throws IOException {
        log.info("Processing tuple: " + input);
        // ... processing logic
        return result;
    }
}
```

**4. Data Quality Checks:**
```pig
-- Count nulls and invalid data
data = LOAD 'input.txt' AS (id:int, name:chararray, amount:double);

quality_check = FOREACH (GROUP data ALL) GENERATE 
    COUNT(data) AS total_records,
    COUNT(data.id) AS valid_ids,
    COUNT(data.name) AS valid_names,
    COUNT(data.amount) AS valid_amounts;

DUMP quality_check;

-- Identify problematic records
invalid_records = FILTER data BY 
    id IS NULL OR 
    name IS NULL OR 
    SIZE(name) == 0 OR
    amount IS NULL OR 
    amount < 0;

STORE invalid_records INTO 'error_records';
```

**5. Performance Debugging:**
```pig
-- Monitor job progress
SET pig.exec.mapPartAgg true;
SET pig.exec.mapPartAgg.minReduction 10;

-- Check data distribution
distribution_check = FOREACH (GROUP data BY (id % 10)) 
                     GENERATE group, COUNT(data) AS count;
DUMP distribution_check;

-- Identify bottlenecks
SET pig.exec.reducers.bytes.per.reducer 1000000000;
SET pig.exec.reducers.max 999;
```

### Q19: What are common Pig errors and how to resolve them?
**Answer:**
**Common Pig Errors and Solutions:**

**1. Schema Mismatch Errors:**
```pig
-- Error: Type mismatch
-- Solution: Explicit casting
data = LOAD 'input.txt' AS (id:chararray, amount:chararray);
corrected = FOREACH data GENERATE 
    (int)id AS id,
    (double)amount AS amount;
```

**2. Out of Memory Errors:**
```pig
-- Error: Java heap space
-- Solution: Increase memory and optimize
SET pig.cachedbag.memusage 0.1;
SET pig.skewedjoin.reduce.memusage 0.2;

-- Use LIMIT for testing
test_data = LIMIT large_dataset 1000;
```

**3. File Not Found Errors:**
```pig
-- Error: Input path does not exist
-- Solution: Check path and use wildcards carefully
data = LOAD '/path/to/data/{2023,2024}/*/*.txt' AS (field:chararray);

-- Verify path exists
fs -ls /path/to/data/
```

**4. Serialization Errors:**
```pig
-- Error: Cannot serialize complex types
-- Solution: Flatten or convert complex types
complex_data = LOAD 'input' AS (id:int, items:bag{t:(item:chararray)});

-- Flatten before storing
flattened = FOREACH complex_data GENERATE id, FLATTEN(items);
STORE flattened INTO 'output';
```

**5. Join Errors:**
```pig
-- Error: Cannot join on different types
-- Solution: Cast to same type
table1 = LOAD 'data1.txt' AS (id:int, value:chararray);
table2 = LOAD 'data2.txt' AS (id:chararray, name:chararray);

-- Cast to same type
joined = JOIN table1 BY (chararray)id, table2 BY id;
```

---

## 🌟 Real-world Scenarios

### Q20: Design a log processing pipeline using Pig
**Answer:**
**Log Processing Pipeline Design:**

**1. Raw Log Structure:**
```
192.168.1.1 - - [01/Dec/2023:10:30:45 +0000] "GET /api/users HTTP/1.1" 200 1234 "http://example.com" "Mozilla/5.0"
```

**2. Log Processing Script:**
```pig
-- Load raw web logs
raw_logs = LOAD '/logs/access_log*' USING TextLoader() AS (line:chararray);

-- Parse log entries using regex
parsed_logs = FOREACH raw_logs GENERATE 
    REGEX_EXTRACT(line, '^([\\d\\.]+)', 1) AS ip_address,
    REGEX_EXTRACT(line, '\\[([^\\]]+)\\]', 1) AS timestamp,
    REGEX_EXTRACT(line, '"(\\w+)\\s+([^\\s]+)\\s+HTTP', 1) AS method,
    REGEX_EXTRACT(line, '"(\\w+)\\s+([^\\s]+)\\s+HTTP', 2) AS url,
    REGEX_EXTRACT(line, 'HTTP/1\\.[01]"\\s+(\\d+)', 1) AS status_code,
    REGEX_EXTRACT(line, 'HTTP/1\\.[01]"\\s+\\d+\\s+(\\d+)', 1) AS response_size;

-- Filter out invalid entries
valid_logs = FILTER parsed_logs BY 
    ip_address IS NOT NULL AND 
    status_code IS NOT NULL AND
    url IS NOT NULL;

-- Convert data types
typed_logs = FOREACH valid_logs GENERATE 
    ip_address,
    ToDate(timestamp, 'dd/MMM/yyyy:HH:mm:ss Z') AS parsed_timestamp,
    method,
    url,
    (int)status_code AS status,
    (long)response_size AS bytes_sent;

-- Extract additional fields
enriched_logs = FOREACH typed_logs GENERATE 
    *,
    GetHour(parsed_timestamp) AS hour,
    GetDay(parsed_timestamp) AS day,
    REGEX_EXTRACT(url, '^/([^/]+)', 1) AS url_category,
    (status >= 400 ? 'Error' : 'Success') AS status_category;

-- Hourly traffic analysis
hourly_grouped = GROUP enriched_logs BY (day, hour);
hourly_stats = FOREACH hourly_grouped GENERATE 
    FLATTEN(group) AS (day, hour),
    COUNT(enriched_logs) AS request_count,
    SUM(enriched_logs.bytes_sent) AS total_bytes,
    COUNT(FILTER enriched_logs BY status_category == 'Error') AS error_count;

-- Top URLs analysis
url_grouped = GROUP enriched_logs BY url;
top_urls = FOREACH url_grouped GENERATE 
    group AS url,
    COUNT(enriched_logs) AS hit_count,
    AVG(enriched_logs.bytes_sent) AS avg_response_size;

top_urls_sorted = ORDER top_urls BY hit_count DESC;
top_10_urls = LIMIT top_urls_sorted 10;

-- IP address analysis
ip_grouped = GROUP enriched_logs BY ip_address;
ip_stats = FOREACH ip_grouped GENERATE 
    group AS ip_address,
    COUNT(enriched_logs) AS request_count,
    COUNT(DISTINCT enriched_logs.url) AS unique_urls,
    MAX(enriched_logs.parsed_timestamp) AS last_access;

-- Store results
STORE hourly_stats INTO '/output/hourly_traffic' USING PigStorage(',');
STORE top_10_urls INTO '/output/top_urls' USING PigStorage(',');
STORE ip_stats INTO '/output/ip_analysis' USING PigStorage(',');

-- Store processed logs for further analysis
STORE enriched_logs INTO '/output/processed_logs' USING PigStorage('\t');
```

### Q21: Implement a recommendation system data pipeline using Pig
**Answer:**
**Recommendation System Pipeline:**

**1. Data Sources:**
```pig
-- Load user interactions
user_interactions = LOAD '/data/interactions.txt' USING PigStorage(',')
    AS (user_id:int, item_id:int, rating:double, timestamp:long);

-- Load item metadata
items = LOAD '/data/items.txt' USING PigStorage(',')
    AS (item_id:int, title:chararray, category:chararray, price:double);

-- Load user profiles
users = LOAD '/data/users.txt' USING PigStorage(',')
    AS (user_id:int, age:int, gender:chararray, location:chararray);
```

**2. Data Preprocessing:**
```pig
-- Filter valid interactions (rating >= 1)
valid_interactions = FILTER user_interactions BY 
    rating IS NOT NULL AND rating >= 1.0;

-- Calculate user statistics
user_stats = FOREACH (GROUP valid_interactions BY user_id) GENERATE 
    group AS user_id,
    COUNT(valid_interactions) AS interaction_count,
    AVG(valid_interactions.rating) AS avg_rating,
    COUNT(DISTINCT valid_interactions.item_id) AS unique_items;

-- Filter active users (at least 5 interactions)
active_users = FILTER user_stats BY interaction_count >= 5;

-- Calculate item statistics
item_stats = FOREACH (GROUP valid_interactions BY item_id) GENERATE 
    group AS item_id,
    COUNT(valid_interactions) AS rating_count,
    AVG(valid_interactions.rating) AS avg_rating,
    STDDEV(valid_interactions.rating) AS rating_stddev;

-- Filter popular items (at least 10 ratings)
popular_items = FILTER item_stats BY rating_count >= 10;
```

**3. User-Item Matrix Creation:**
```pig
-- Create user-item pairs with ratings
user_item_matrix = FOREACH valid_interactions GENERATE 
    user_id,
    item_id,
    rating;

-- Normalize ratings (mean-centered)
user_means = FOREACH (GROUP valid_interactions BY user_id) GENERATE 
    group AS user_id,
    AVG(valid_interactions.rating) AS mean_rating;

normalized_ratings = JOIN user_item_matrix BY user_id, user_means BY user_id;
normalized_matrix = FOREACH normalized_ratings GENERATE 
    user_item_matrix::user_id AS user_id,
    user_item_matrix::item_id AS item_id,
    user_item_matrix::rating - user_means::mean_rating AS normalized_rating;
```

**4. Collaborative Filtering - User Similarity:**
```pig
-- Create user pairs for similarity calculation
user_pairs = JOIN normalized_matrix BY item_id, normalized_matrix BY item_id;
user_pairs_filtered = FILTER user_pairs BY 
    normalized_matrix::user_id < normalized_matrix::user_id;

-- Calculate cosine similarity between users
user_similarity = FOREACH (GROUP user_pairs_filtered BY 
    (normalized_matrix::user_id, normalized_matrix::user_id)) {
    
    dot_product = SUM(normalized_matrix::normalized_rating * 
                     normalized_matrix::normalized_rating);
    magnitude1 = SQRT(SUM(normalized_matrix::normalized_rating * 
                         normalized_matrix::normalized_rating));
    magnitude2 = SQRT(SUM(normalized_matrix::normalized_rating * 
                         normalized_matrix::normalized_rating));
    
    GENERATE 
        FLATTEN(group) AS (user1, user2),
        (magnitude1 * magnitude2 > 0 ? 
         dot_product / (magnitude1 * magnitude2) : 0.0) AS similarity;
}

-- Filter similar users (similarity > 0.3)
similar_users = FILTER user_similarity BY similarity > 0.3;
```

**5. Generate Recommendations:**
```pig
-- Find items rated by similar users but not by target user
user_items = FOREACH (GROUP normalized_matrix BY user_id) GENERATE 
    group AS user_id,
    normalized_matrix.item_id AS rated_items;

recommendations_candidates = JOIN similar_users BY user2, 
                            normalized_matrix BY user_id;

-- Filter out items already rated by target user
filtered_candidates = JOIN recommendations_candidates BY 
    (similar_users::user1, normalized_matrix::item_id) LEFT OUTER,
    user_items BY (user_id, rated_items);

new_recommendations = FILTER filtered_candidates BY 
    user_items::user_id IS NULL;

-- Calculate weighted ratings for recommendations
weighted_recommendations = FOREACH (GROUP new_recommendations BY 
    (similar_users::user1, normalized_matrix::item_id)) {
    
    weighted_sum = SUM(similar_users::similarity * 
                      normalized_matrix::normalized_rating);
    similarity_sum = SUM(similar_users::similarity);
    
    GENERATE 
        FLATTEN(group) AS (user_id, item_id),
        (similarity_sum > 0 ? weighted_sum / similarity_sum : 0.0) AS predicted_rating;
}

-- Top recommendations per user
top_recommendations = FOREACH (GROUP weighted_recommendations BY user_id) {
    sorted = ORDER weighted_recommendations BY predicted_rating DESC;
    top_10 = LIMIT sorted 10;
    GENERATE group AS user_id, top_10;
}
```

**6. Content-Based Filtering:**
```pig
-- Category-based recommendations
user_categories = JOIN valid_interactions BY item_id, items BY item_id;
user_category_prefs = FOREACH (GROUP user_categories BY 
    (valid_interactions::user_id, items::category)) GENERATE 
    FLATTEN(group) AS (user_id, category),
    AVG(valid_interactions::rating) AS avg_category_rating,
    COUNT(valid_interactions) AS category_interactions;

-- Recommend items from preferred categories
preferred_categories = FILTER user_category_prefs BY 
    avg_category_rating >= 4.0 AND category_interactions >= 3;

content_recommendations = JOIN preferred_categories BY category, 
                         items BY category;

content_filtered = FILTER content_recommendations BY 
    items::item_id NOT IN (SELECT item_id FROM user_interactions 
                          WHERE user_id == preferred_categories::user_id);
```

**7. Store Results:**
```pig
-- Store collaborative filtering recommendations
STORE top_recommendations INTO '/output/collaborative_recommendations' 
      USING PigStorage(',');

-- Store content-based recommendations  
STORE content_filtered INTO '/output/content_recommendations' 
      USING PigStorage(',');

-- Store user and item statistics for monitoring
STORE user_stats INTO '/output/user_statistics' USING PigStorage(',');
STORE item_stats INTO '/output/item_statistics' USING PigStorage(',');
```

---

## 📚 Additional Resources

### Best Practices Summary
1. **Script Organization**: Use meaningful variable names and comments
2. **Performance**: Optimize joins, use appropriate parallelism
3. **Data Quality**: Validate and clean data early in pipeline
4. **Error Handling**: Implement proper error checking and logging
5. **Testing**: Use LIMIT and SAMPLE for development and testing

### Recommended Reading
- "Programming Pig" by Alan Gates
- Apache Pig Official Documentation
- Hadoop Ecosystem Integration Guides

### Hands-on Practice
- Cloudera Quickstart VM
- Hortonworks Sandbox
- AWS EMR with Pig
- Local Pig installation for development

---

*This comprehensive guide covers essential Apache Pig concepts and interview questions for data engineering roles. Practice with real datasets and complex transformations to master Pig Latin programming.*