# Apache Pig Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Components](#-core-components)
   - [Pig Latin Language](#pig-latin-language)
   - [Execution Engine](#execution-engine)
   - [Data Model](#data-model)
3. [Pig Architecture](#-pig-architecture)
4. [Data Types & Operations](#-data-types--operations)
5. [User Defined Functions (UDFs)](#-user-defined-functions-udfs)
6. [Performance Optimization](#-performance-optimization)
   - [Multi-query Optimization](#1-multi-query-optimization)
   - [Join Optimization](#2-join-optimization)
   - [Data Locality](#3-data-locality)
7. [Configuration](#️-configuration)
8. [Integration](#-integration)
9. [When to Use Pig](#-when-to-use-pig)
10. [Interview Focus Areas](#-interview-focus-areas)
11. [Quick References](#-quick-references)

---

## 🎯 Overview

Apache Pig is a high-level platform for creating programs that run on Apache Hadoop. It provides a high-level scripting language called Pig Latin that allows developers to express data analysis programs in a more natural way than writing MapReduce jobs directly.

**Key Benefits:**
- **Ease of Programming**: Pig Latin is simpler than writing MapReduce jobs
- **Automatic Optimization**: Built-in optimization of execution plans
- **Extensibility**: Support for User Defined Functions (UDFs)
- **Multi-query Optimization**: Efficient execution of multiple queries
- **Schema Flexibility**: Works with structured and unstructured data

## 📦 Core Components

### Pig Latin Language
**Definition**: High-level scripting language for data analysis that compiles to MapReduce jobs.

**Key Characteristics**:
- **Procedural**: Step-by-step data transformation
- **Dataflow-oriented**: Operations on datasets
- **Schema-optional**: Can work with or without predefined schemas
- **Extensible**: Support for custom functions

```pig
-- Simple data processing pipeline
data = LOAD 'input.txt' AS (name:chararray, age:int, salary:double);
adults = FILTER data BY age >= 18;
high_earners = FILTER adults BY salary > 50000;
result = ORDER high_earners BY salary DESC;
STORE result INTO 'output';
```

### Execution Engine
**Definition**: Converts Pig Latin scripts into optimized MapReduce jobs.

**Execution Process**:
1. **Parsing**: Parse Pig Latin script and check syntax
2. **Logical Plan**: Create logical plan with operators
3. **Optimization**: Apply optimization rules
4. **Physical Plan**: Convert to MapReduce jobs
5. **Execution**: Submit jobs to Hadoop cluster

### Data Model
**Definition**: Pig's data model consists of atoms, tuples, bags, and maps.

**Data Types**:
- **Atoms**: Simple data types (int, long, float, double, chararray, bytearray)
- **Tuples**: Ordered collection of fields
- **Bags**: Collection of tuples (can contain duplicates)
- **Maps**: Key-value pairs

```pig
-- Schema definition example
users = LOAD 'users.txt' AS (
    id:int,
    name:chararray,
    contacts:bag{t:(type:chararray, value:chararray)},
    metadata:map[]
);
```

## 🏗️ Pig Architecture

**Definition**: Pig architecture consists of the Pig Engine that converts Pig Latin scripts into MapReduce jobs.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                PIG ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   PIG SCRIPT    │    │   PIG ENGINE    │    │     HADOOP      │             │
│  │                 │    │                 │    │    CLUSTER      │             │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │             │
│  │ │ Pig Latin   │ │───►│ │   Parser    │ │    │ │ MapReduce   │ │             │
│  │ │   Script    │ │    │ │             │ │    │ │    Jobs     │ │             │
│  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │             │
│  │                 │    │        │        │    │        ▲        │             │
│  │                 │    │        ▼        │    │        │        │             │
│  │                 │    │ ┌─────────────┐ │    │        │        │             │
│  │                 │    │ │Logical Plan │ │    │        │        │             │
│  │                 │    │ │  Generator  │ │    │        │        │             │
│  │                 │    │ └─────────────┘ │    │        │        │             │
│  │                 │    │        │        │    │        │        │             │
│  │                 │    │        ▼        │    │        │        │             │
│  │                 │    │ ┌─────────────┐ │    │        │        │             │
│  │                 │    │ │  Optimizer  │ │    │        │        │             │
│  │                 │    │ └─────────────┘ │    │        │        │             │
│  │                 │    │        │        │    │        │        │             │
│  │                 │    │        ▼        │    │        │        │             │
│  │                 │    │ ┌─────────────┐ │    │        │        │             │
│  │                 │    │ │Physical Plan│ │────┼────────┘        │             │
│  │                 │    │ │  Generator  │ │    │                 │             │
│  │                 │    │ └─────────────┘ │    │                 │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

                                EXECUTION FLOW
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  1. User writes Pig Latin script                                               │
│  2. Parser validates syntax and creates parse tree                             │
│  3. Logical Plan Generator creates logical operators                            │
│  4. Optimizer applies optimization rules                                       │
│  5. Physical Plan Generator converts to MapReduce jobs                         │
│  6. Jobs are submitted to Hadoop cluster for execution                         │
│  7. Results are written to specified output location                           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Core Components**:
- **Parser**: Validates Pig Latin syntax and creates parse tree
- **Logical Plan Generator**: Creates logical operators from parse tree
- **Optimizer**: Applies optimization rules to improve performance
- **Physical Plan Generator**: Converts logical plan to MapReduce jobs
- **Execution Engine**: Submits and monitors MapReduce jobs

```pig
-- Example showing execution plan
EXPLAIN result;  -- Shows the execution plan
ILLUSTRATE result;  -- Shows sample data flow
```

## 📊 Data Types & Operations

**Definition**: Pig supports various data types and operations for data manipulation.

### Data Types

**Simple Types**:
```pig
-- Numeric types
age:int                    -- 32-bit signed integer
population:long            -- 64-bit signed integer
price:float               -- 32-bit floating point
salary:double             -- 64-bit floating point

-- Text and binary
name:chararray            -- UTF-8 string
data:bytearray           -- Binary data
```

**Complex Types**:
```pig
-- Tuple: ordered collection of fields
person:(name:chararray, age:int)

-- Bag: collection of tuples
scores:bag{t:(subject:chararray, score:int)}

-- Map: key-value pairs
metadata:map[]
```

### Core Operations

**Data Loading and Storing**:
```pig
-- Load data with schema
data = LOAD 'input.txt' AS (name:chararray, age:int, salary:double);

-- Load without schema (all fields as bytearray)
raw_data = LOAD 'input.txt';

-- Store results
STORE result INTO 'output' USING PigStorage(',');
```

**Filtering and Projection**:
```pig
-- Filter records
adults = FILTER data BY age >= 18;
high_earners = FILTER data BY salary > 50000 AND age > 25;

-- Project specific fields
names_ages = FOREACH data GENERATE name, age;

-- Generate new fields
enriched = FOREACH data GENERATE 
    name, 
    age, 
    salary,
    (salary * 12) AS annual_salary;
```

**Grouping and Aggregation**:
```pig
-- Group by single field
by_age = GROUP data BY age;

-- Group by multiple fields
by_age_dept = GROUP data BY (age, department);

-- Aggregate functions
summary = FOREACH by_age GENERATE 
    group AS age,
    COUNT(data) AS count,
    AVG(data.salary) AS avg_salary,
    MAX(data.salary) AS max_salary;
```

**Joins**:
```pig
-- Inner join
customers = LOAD 'customers' AS (id:int, name:chararray);
orders = LOAD 'orders' AS (order_id:int, customer_id:int, amount:double);
result = JOIN customers BY id, orders BY customer_id;

-- Outer joins
left_result = JOIN customers BY id LEFT OUTER, orders BY customer_id;
right_result = JOIN customers BY id RIGHT OUTER, orders BY customer_id;
full_result = JOIN customers BY id FULL OUTER, orders BY customer_id;
```

## 🔧 User Defined Functions (UDFs)

**Definition**: Custom functions that extend Pig's built-in functionality.

### Types of UDFs

**1. Eval Functions**: Process individual tuples
```java
public class UPPER extends EvalFunc<String> {
    public String exec(Tuple input) throws IOException {
        if (input == null || input.size() == 0) return null;
        String str = (String) input.get(0);
        return str.toUpperCase();
    }
}
```

**2. Aggregate Functions**: Process bags of tuples
```java
public class COUNT extends EvalFunc<Long> {
    public Long exec(Tuple input) throws IOException {
        DataBag bag = (DataBag) input.get(0);
        return bag.size();
    }
}
```

**3. Filter Functions**: Return boolean values
```java
public class IsEven extends FilterFunc {
    public Boolean exec(Tuple input) throws IOException {
        Integer value = (Integer) input.get(0);
        return value % 2 == 0;
    }
}
```

**Using UDFs**:
```pig
-- Register UDF
REGISTER 'myudfs.jar';
DEFINE UPPER com.example.UPPER();
DEFINE IsEven com.example.IsEven();

-- Use UDF
data = LOAD 'input' AS (name:chararray, value:int);
result = FOREACH data GENERATE UPPER(name), value;
even_values = FILTER data BY IsEven(value);
```

## ⚡ Performance Optimization

**Definition**: Techniques to improve Pig script performance and reduce execution time.

### 1. Multi-query Optimization
**Definition**: Pig automatically optimizes multiple queries that share common operations.

```pig
-- Pig optimizes these queries to share common operations
data = LOAD 'sales' AS (region:chararray, product:chararray, amount:double);
by_region = GROUP data BY region;
by_product = GROUP data BY product;

region_totals = FOREACH by_region GENERATE group, SUM(data.amount);
product_totals = FOREACH by_product GENERATE group, SUM(data.amount);

STORE region_totals INTO 'region_output';
STORE product_totals INTO 'product_output';
```

### 2. Join Optimization
**Definition**: Choose appropriate join strategies based on data size.

```pig
-- Replicated join for small datasets
small_table = LOAD 'lookup' AS (id:int, name:chararray);
large_table = LOAD 'transactions' AS (id:int, amount:double);
result = JOIN large_table BY id, small_table BY id USING 'replicated';

-- Skewed join for data with skewed keys
skewed_result = JOIN table1 BY key, table2 BY key USING 'skewed';

-- Merge join for sorted data
sorted_result = JOIN table1 BY key, table2 BY key USING 'merge';
```

### 3. Data Locality
**Definition**: Optimize data placement and access patterns.

```pig
-- Use appropriate data formats
-- Parquet for columnar access
data = LOAD 'data.parquet' USING parquet.pig.ParquetLoader();

-- Use compression
STORE result INTO 'output' USING PigStorage(',', '-c gzip');

-- Partition data appropriately
partitioned = FOREACH data GENERATE 
    year, month, day, 
    name, amount;
STORE partitioned INTO 'partitioned_output' 
    USING PigStorage() 
    PARTITION BY (year, month);
```

## 🛠️ Configuration

**Definition**: Settings that control Pig execution behavior and performance.

### Execution Modes
```bash
# Local mode (single machine)
pig -x local script.pig

# MapReduce mode (Hadoop cluster)
pig -x mapreduce script.pig

# Tez mode (faster execution engine)
pig -x tez script.pig
```

### Performance Configuration
```pig
-- Set parallelism
SET default_parallel 20;

-- Configure memory
SET pig.cachedbag.memusage 0.2;
SET pig.skewedjoin.reduce.memusage 0.3;

-- Enable optimization
SET pig.exec.mapPartAgg true;
SET pig.optimizer.rules 'LoadTypeCastInserter,MergeFilter,PushUpFilter,MergeForEach,PushUpForEachFlatten,LimitOptimizer,ColumnMapKeyPrune,AddForEach,GroupByConstParallelSetter';
```

### Resource Management
```pig
-- Set job properties
SET mapred.job.name 'My Pig Job';
SET mapred.map.tasks.speculative.execution false;
SET mapred.reduce.tasks.speculative.execution false;

-- Configure splits
SET pig.maxCombinedSplitSize 268435456;  -- 256MB
SET pig.splitCombination true;
```

## 🔗 Integration

**Definition**: How Pig integrates with other tools in the Hadoop ecosystem.

### Hadoop Integration
```pig
-- HDFS integration
data = LOAD 'hdfs://namenode:port/path/input' AS (field1, field2);
STORE result INTO 'hdfs://namenode:port/path/output';

-- HBase integration
REGISTER 'hbase-pig.jar';
raw = LOAD 'hbase://mytable' 
    USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
        'cf1:col1 cf1:col2 cf2:col3'
    ) AS (col1, col2, col3);
```

### Hive Integration
```pig
-- Use Hive tables
SET hive.metastore.uris 'thrift://metastore:9083';
data = LOAD 'hive_table' USING org.apache.hive.hcatalog.pig.HCatLoader();
```

### Streaming Integration
```pig
-- Use streaming commands
data = LOAD 'input' AS (line:chararray);
processed = STREAM data THROUGH 'python process.py' AS (result:chararray);
```

## 📊 When to Use Pig

**Use Pig When:**
- **ETL Operations**: Complex data transformations and cleaning
- **Ad-hoc Analysis**: Exploratory data analysis and prototyping
- **Data Pipeline**: Building data processing workflows
- **Schema Evolution**: Working with evolving data schemas
- **Custom Logic**: Need for custom UDFs and complex operations

**Don't Use Pig When:**
- **Real-time Processing**: Need low-latency processing
- **Simple Queries**: Basic SQL queries (use Hive instead)
- **Interactive Analysis**: Need interactive query capabilities
- **Small Data**: Data fits in memory on single machine
- **Complex Analytics**: Advanced analytics and machine learning

## 🎯 Interview Focus Areas

1. **Architecture**: Pig execution process and optimization
2. **Pig Latin**: Language syntax and operations
3. **Data Types**: Complex data structures and nested operations
4. **UDFs**: Custom function development and usage
5. **Performance**: Optimization techniques and best practices
6. **Joins**: Different join types and optimization strategies
7. **Integration**: Working with Hadoop ecosystem tools
8. **Troubleshooting**: Common issues and debugging techniques
9. **Comparison**: Pig vs Hive vs MapReduce trade-offs
10. **Use Cases**: When to choose Pig for data processing

## 📚 Quick References

- [Pig Documentation](https://pig.apache.org/docs/)
- [Pig Latin Reference](https://pig.apache.org/docs/latest/basic.html)
- [Built-in Functions](https://pig.apache.org/docs/latest/func.html)
- [UDF Development Guide](https://pig.apache.org/docs/latest/udf.html)