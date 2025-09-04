# Apache Pig Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#core-concepts)
2. [Pig Latin Language](#pig-latin-language)
3. [Data Operations](#data-operations)
4. [Performance Optimization](#performance-optimization)
5. [Integration & Use Cases](#integration--use-cases)

---

## Core Concepts

### 1. What is Apache Pig and how does it differ from MapReduce?

**Answer:**
Apache Pig is a high-level platform for creating programs that run on Apache Hadoop, using a language called Pig Latin.

**Key Differences:**
| Aspect | Apache Pig | MapReduce |
|--------|------------|-----------|
| **Language** | Pig Latin (SQL-like) | Java/Python/etc |
| **Code Length** | 10x shorter | Verbose |
| **Development Time** | Faster | Slower |
| **Optimization** | Automatic | Manual |
| **Learning Curve** | Easier | Steeper |

**Pig Architecture:**
```
Pig Script → Parser → Logical Plan → Optimizer → Physical Plan → MapReduce Jobs
```

### 2. Explain Pig's execution modes and when to use each.

**Answer:**
Pig supports two execution modes for different development and production scenarios.

**Local Mode:**
```bash
# Run Pig in local mode (single machine)
pig -x local

# Example: Process local files
grunt> A = LOAD '/local/path/data.txt' USING PigStorage(',');
grunt> DUMP A;
```

**MapReduce Mode:**
```bash
# Run Pig on Hadoop cluster
pig -x mapreduce

# Example: Process HDFS files
grunt> A = LOAD '/hdfs/path/data.txt' USING PigStorage(',');
grunt> STORE A INTO '/hdfs/output/';
```

**When to Use:**
- **Local Mode**: Development, testing, small datasets
- **MapReduce Mode**: Production, large datasets, distributed processing

---

## Pig Latin Language

### 3. What are the basic data types and structures in Pig Latin?

**Answer:**
Pig Latin supports various data types for handling different kinds of data.

**Primitive Types:**
```pig
-- Scalar types
int_field: int
long_field: long  
float_field: float
double_field: double
chararray_field: chararray
bytearray_field: bytearray
boolean_field: boolean
datetime_field: datetime
```

**Complex Types:**
```pig
-- Tuple: ordered set of fields
customer_info: (name: chararray, age: int, email: chararray)

-- Bag: collection of tuples
orders: {order: (order_id: int, amount: double, date: chararray)}

-- Map: key-value pairs
preferences: [chararray]
```

**Example Usage:**
```pig
-- Load data with schema
customers = LOAD 'customers.txt' USING PigStorage(',') 
    AS (id: int, name: chararray, age: int, city: chararray);

-- Complex data structure
customer_orders = LOAD 'orders.txt' USING PigStorage(',')
    AS (customer_id: int, orders: bag{order: tuple(order_id: int, amount: double)});
```

### 4. How do you perform data loading and storing operations in Pig?

**Answer:**
Pig provides flexible loading and storing mechanisms for various data formats.

**Loading Data:**
```pig
-- Basic load with delimiter
data = LOAD 'input.txt' USING PigStorage(',');

-- Load with schema
customers = LOAD 'customers.csv' USING PigStorage(',') 
    AS (id: int, name: chararray, email: chararray, city: chararray);

-- Load JSON data
json_data = LOAD 'data.json' USING JsonLoader('id: int, name: chararray, details: map[]');

-- Load from HBase
hbase_data = LOAD 'hbase://customers' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
    'info:name info:email info:phone', '-loadKey true'
) AS (key: chararray, name: chararray, email: chararray, phone: chararray);
```

**Storing Data:**
```pig
-- Store with delimiter
STORE processed_data INTO 'output' USING PigStorage(',');

-- Store as JSON
STORE result INTO 'output.json' USING JsonStorage();

-- Store to HBase
STORE customer_updates INTO 'hbase://customers' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
    'info:name info:email info:phone'
);

-- Store with compression
STORE large_dataset INTO 'compressed_output' USING PigStorage(',', '-schema');
```

---

## Data Operations

### 5. How do you perform filtering, grouping, and joining operations in Pig?

**Answer:**
Pig Latin provides powerful operators for data manipulation and analysis.

**Filtering:**
```pig
-- Basic filtering
high_value_customers = FILTER customers BY age > 25;

-- Complex filtering with multiple conditions
active_customers = FILTER customers BY (age > 18 AND age < 65) AND city IS NOT NULL;

-- Filtering with regular expressions
gmail_users = FILTER customers BY email MATCHES '.*@gmail\\.com';

-- Filtering nested data
large_orders = FILTER orders BY order_amount > 100.0;
```

**Grouping:**
```pig
-- Group by single field
customers_by_city = GROUP customers BY city;

-- Group by multiple fields
orders_by_customer_month = GROUP orders BY (customer_id, SUBSTRING(order_date, 0, 7));

-- Group all records
all_customers = GROUP customers ALL;

-- Process grouped data
city_stats = FOREACH customers_by_city GENERATE 
    group AS city,
    COUNT(customers) AS customer_count,
    AVG(customers.age) AS avg_age;
```

**Joining:**
```pig
-- Inner join
customer_orders = JOIN customers BY id, orders BY customer_id;

-- Left outer join
all_customers_with_orders = JOIN customers BY id LEFT OUTER, orders BY customer_id;

-- Multiple joins
complete_data = JOIN customers BY id, orders BY customer_id, products BY id;

-- Self join
customer_pairs = JOIN customers BY city, customers BY city;
```

### 6. How do you implement User Defined Functions (UDFs) in Pig?

**Answer:**
UDFs extend Pig's functionality with custom processing logic.

**Java UDF Example:**
```java
// EmailDomainUDF.java
package com.company.pig.udfs;

import java.io.IOException;
import org.apache.pig.EvalFunc;
import org.apache.pig.data.Tuple;

public class EmailDomainUDF extends EvalFunc<String> {
    @Override
    public String exec(Tuple input) throws IOException {
        if (input == null || input.size() == 0 || input.get(0) == null) {
            return null;
        }
        
        String email = (String) input.get(0);
        int atIndex = email.indexOf('@');
        
        if (atIndex == -1) {
            return null;
        }
        
        return email.substring(atIndex + 1);
    }
}
```

**Using UDF in Pig:**
```pig
-- Register UDF
REGISTER 'pig-udfs.jar';
DEFINE ExtractDomain com.company.pig.udfs.EmailDomainUDF();

-- Use UDF
customers_with_domain = FOREACH customers GENERATE 
    id,
    name,
    email,
    ExtractDomain(email) AS email_domain;

-- Group by domain
domain_stats = GROUP customers_with_domain BY email_domain;
domain_counts = FOREACH domain_stats GENERATE 
    group AS domain,
    COUNT(customers_with_domain) AS user_count;
```

**Python UDF:**
```python
# python_udfs.py
@outputSchema("word_count: int")
def count_words(text):
    if text is None:
        return 0
    return len(text.split())

@outputSchema("upper_text: chararray")  
def to_upper(text):
    if text is None:
        return None
    return text.upper()
```

```pig
-- Register Python UDF
REGISTER 'python_udfs.py' USING jython AS py_udfs;

-- Use Python UDF
processed_text = FOREACH raw_data GENERATE 
    py_udfs.count_words(description) AS word_count,
    py_udfs.to_upper(title) AS upper_title;
```

---

## Performance Optimization

### 7. How do you optimize Pig script performance?

**Answer:**
Several optimization techniques can improve Pig script performance significantly.

**Data Loading Optimization:**
```pig
-- Use appropriate storage formats
-- For columnar data
data = LOAD 'data.parquet' USING org.apache.pig.piggybank.storage.ParquetLoader();

-- For compressed data
compressed_data = LOAD 'data.gz' USING PigStorage(',');

-- Specify schema to avoid type inference
customers = LOAD 'customers.txt' USING PigStorage(',') 
    AS (id: int, name: chararray, age: int, city: chararray);
```

**Join Optimization:**
```pig
-- Use replicated join for small tables
small_lookup = LOAD 'lookup.txt' USING PigStorage(',') AS (code: chararray, description: chararray);
large_data = LOAD 'large_data.txt' USING PigStorage(',') AS (id: int, code: chararray, value: double);

-- Replicated join (broadcast small table)
result = JOIN large_data BY code, small_lookup BY code USING 'replicated';

-- Skewed join for data with skewed keys
skewed_result = JOIN table1 BY key, table2 BY key USING 'skewed';
```

**Memory Management:**
```pig
-- Increase memory for operations
SET mapreduce.map.memory.mb 2048;
SET mapreduce.reduce.memory.mb 4096;

-- Control parallelism
SET default_parallel 20;

-- Use PARALLEL clause
grouped_data = GROUP large_dataset BY category PARALLEL 50;
```

### 8. How do you handle data skew in Pig operations?

**Answer:**
Data skew can significantly impact performance and requires specific handling strategies.

**Identifying Skew:**
```pig
-- Check data distribution
data_sample = SAMPLE input_data 0.1;
key_distribution = GROUP data_sample BY key;
key_counts = FOREACH key_distribution GENERATE group, COUNT(data_sample);
ordered_counts = ORDER key_counts BY $1 DESC;
DUMP ordered_counts;
```

**Handling Skewed Joins:**
```pig
-- Use skewed join
customers = LOAD 'customers.txt' AS (id: int, name: chararray, city: chararray);
orders = LOAD 'orders.txt' AS (customer_id: int, amount: double, date: chararray);

-- Specify skewed keys
skewed_join = JOIN customers BY id, orders BY customer_id USING 'skewed';

-- Alternative: Use sampling to identify skewed keys
DEFINE SkewedJoin org.apache.pig.backend.hadoop.executionengine.physicalLayer.relationalOperators.POSkewedJoin('customers::id');
result = JOIN customers BY id, orders BY customer_id USING SkewedJoin;
```

**Skewed Group By:**
```pig
-- Handle skewed grouping
sales_data = LOAD 'sales.txt' AS (product_id: int, sale_amount: double, region: chararray);

-- Use random partitioning for skewed groups
random_partitioned = FOREACH sales_data GENERATE 
    product_id,
    sale_amount,
    region,
    RANDOM() AS rand_key;

-- Group with random key to distribute load
temp_grouped = GROUP random_partitioned BY (product_id, (int)(rand_key * 10));
temp_aggregated = FOREACH temp_grouped GENERATE 
    FLATTEN(group.product_id) AS product_id,
    SUM(random_partitioned.sale_amount) AS partial_sum;

-- Final aggregation
final_grouped = GROUP temp_aggregated BY product_id;
final_result = FOREACH final_grouped GENERATE 
    group AS product_id,
    SUM(temp_aggregated.partial_sum) AS total_sales;
```

---

## Integration & Use Cases

### 9. How do you integrate Pig with other Hadoop ecosystem tools?

**Answer:**
Pig integrates seamlessly with various Hadoop ecosystem components.

**Hive Integration:**
```pig
-- Use HCatalog to access Hive tables
REGISTER '/usr/lib/hive-hcatalog/share/hcatalog/hive-hcatalog-core.jar';

-- Load from Hive table
hive_data = LOAD 'database.table_name' USING org.apache.hive.hcatalog.pig.HCatLoader();

-- Store to Hive table
STORE processed_data INTO 'database.output_table' USING org.apache.hive.hcatalog.pig.HCatStorer();
```

**HBase Integration:**
```pig
-- Load from HBase
hbase_customers = LOAD 'hbase://customers' 
    USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
        'info:name info:email info:phone', '-loadKey true'
    ) AS (key: chararray, name: chararray, email: chararray, phone: chararray);

-- Store to HBase
STORE customer_updates INTO 'hbase://customers' 
    USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
        'info:name info:email info:phone'
    );
```

**Spark Integration:**
```pig
-- Use Pig with Spark execution engine
SET pig.exec.mapreduce.engine spark;

-- Configure Spark settings
SET spark.executor.memory 4g;
SET spark.executor.cores 2;

-- Run Pig script on Spark
customers = LOAD 'customers.txt' AS (id: int, name: chararray);
processed = FOREACH customers GENERATE id, UPPER(name);
STORE processed INTO 'output';
```

### 10. What are common use cases for Apache Pig in data engineering?

**Answer:**
Pig excels in ETL operations, data preparation, and ad-hoc analysis scenarios.

**ETL Pipeline:**
```pig
-- Extract: Load raw data
raw_logs = LOAD 'web_logs.txt' USING PigStorage('\t') 
    AS (timestamp: chararray, ip: chararray, url: chararray, status: int, size: long);

-- Transform: Clean and process data
cleaned_logs = FILTER raw_logs BY status == 200 AND size > 0;

parsed_logs = FOREACH cleaned_logs GENERATE 
    ToDate(timestamp, 'yyyy-MM-dd HH:mm:ss') AS log_date,
    ip,
    REGEX_EXTRACT(url, '([^?]+)', 1) AS clean_url,
    status,
    size;

-- Aggregate data
daily_stats = GROUP parsed_logs BY (GetDay(log_date), clean_url);
url_stats = FOREACH daily_stats GENERATE 
    FLATTEN(group) AS (day, url),
    COUNT(parsed_logs) AS hit_count,
    SUM(parsed_logs.size) AS total_bytes;

-- Load: Store processed data
STORE url_stats INTO 'processed_logs' USING PigStorage(',');
```

**Data Quality Checks:**
```pig
-- Load customer data
customers = LOAD 'customers.csv' USING PigStorage(',') 
    AS (id: int, name: chararray, email: chararray, age: int, city: chararray);

-- Data quality validation
null_ids = FILTER customers BY id IS NULL;
invalid_emails = FILTER customers BY email IS NULL OR NOT (email MATCHES '.*@.*\\..*');
invalid_ages = FILTER customers BY age IS NULL OR age < 0 OR age > 120;

-- Generate quality report
quality_report = UNION 
    (FOREACH null_ids GENERATE 'NULL_ID' AS issue_type, id, name, email),
    (FOREACH invalid_emails GENERATE 'INVALID_EMAIL' AS issue_type, id, name, email),
    (FOREACH invalid_ages GENERATE 'INVALID_AGE' AS issue_type, id, name, email);

STORE quality_report INTO 'data_quality_issues';
```

**Log Analysis:**
```pig
-- Parse and analyze server logs
server_logs = LOAD 'access.log' USING PigStorage(' ') 
    AS (ip: chararray, timestamp: chararray, method: chararray, 
        url: chararray, status: int, size: long);

-- Extract hour from timestamp
hourly_logs = FOREACH server_logs GENERATE 
    ip,
    REGEX_EXTRACT(timestamp, '\\[(\\d{2}/\\w{3}/\\d{4}:\\d{2})', 1) AS hour,
    method,
    url,
    status,
    size;

-- Analyze traffic patterns
hourly_traffic = GROUP hourly_logs BY hour;
traffic_stats = FOREACH hourly_traffic GENERATE 
    group AS hour,
    COUNT(hourly_logs) AS request_count,
    SUM(hourly_logs.size) AS total_bytes,
    COUNT(FILTER hourly_logs BY status >= 400) AS error_count;

-- Find top URLs
url_groups = GROUP hourly_logs BY url;
url_stats = FOREACH url_groups GENERATE 
    group AS url,
    COUNT(hourly_logs) AS hit_count;

top_urls = ORDER url_stats BY hit_count DESC;
top_10_urls = LIMIT top_urls 10;

STORE traffic_stats INTO 'hourly_traffic_stats';
STORE top_10_urls INTO 'top_urls';
```

---

## Summary

Apache Pig provides high-level data processing capabilities with:

1. **Ease of Use**: Pig Latin language reduces development time
2. **Flexibility**: Handles structured and unstructured data
3. **Extensibility**: Custom UDFs for specialized processing
4. **Optimization**: Automatic query optimization and execution planning
5. **Integration**: Works with Hadoop ecosystem tools (Hive, HBase, Spark)