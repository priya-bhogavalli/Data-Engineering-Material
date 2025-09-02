# SQL All Features Reference

## 🎯 Overview
Comprehensive reference for SQL features across different database engines, performance optimization, advanced functions, and data engineering patterns.

## 📍 Legend

### Feature Support
- 🟢 **Full Support** - Complete implementation
- 🟡 **Partial Support** - Limited or non-standard implementation
- 🔴 **No Support** - Feature not available
- ⚫ **Deprecated** - Being phased out

### SQL Standards
- **SQL-92** - Basic standard (ANSI SQL)
- **SQL:1999** - Regular expressions, arrays
- **SQL:2003** - Window functions, XML
- **SQL:2006** - Import/export, more XML
- **SQL:2008** - MERGE, INSTEAD OF triggers
- **SQL:2011** - Temporal data, enhanced window functions
- **SQL:2016** - JSON support, row pattern recognition

## 🏗️ Core SQL Features by Database Engine

| Feature | PostgreSQL | MySQL | SQL Server | Oracle | SQLite | BigQuery | Snowflake | Redshift |
|---------|------------|-------|------------|--------|--------|----------|-----------|----------|
| **Window Functions** | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **CTEs (WITH)** | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **Recursive CTEs** | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 |
| **JSON Support** | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 |
| **Array Types** | 🟢 | 🟡 | 🔴 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 |
| **Full Text Search** | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 |
| **Partitioning** | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 |
| **Materialized Views** | 🟢 | 🔴 | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 | 🟢 |
| **Stored Procedures** | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 |
| **User-Defined Functions** | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 |

## 📊 Window Functions Comprehensive Guide

### Ranking Functions
| Function | Purpose | Ties Handling | Use Cases | Example |
|----------|---------|---------------|-----------|---------|
| **ROW_NUMBER()** | Sequential numbering | No ties | Pagination, deduplication | `ROW_NUMBER() OVER (ORDER BY salary DESC)` |
| **RANK()** | Ranking with gaps | Gaps for ties | Top N with ties | `RANK() OVER (ORDER BY score DESC)` |
| **DENSE_RANK()** | Ranking without gaps | No gaps | Continuous ranking | `DENSE_RANK() OVER (ORDER BY score DESC)` |
| **NTILE(n)** | Divide into buckets | Even distribution | Quartiles, percentiles | `NTILE(4) OVER (ORDER BY salary)` |
| **PERCENT_RANK()** | Percentage rank | 0 to 1 scale | Relative positioning | `PERCENT_RANK() OVER (ORDER BY score)` |
| **CUME_DIST()** | Cumulative distribution | 0 to 1 scale | Percentile calculation | `CUME_DIST() OVER (ORDER BY salary)` |

### Aggregate Window Functions
| Function | Purpose | Frame Behavior | Use Cases | Example |
|----------|---------|----------------|-----------|---------|
| **SUM() OVER** | Running totals | Cumulative | Running totals, YTD | `SUM(amount) OVER (ORDER BY date)` |
| **AVG() OVER** | Moving averages | Sliding window | Trend analysis | `AVG(price) OVER (ORDER BY date ROWS 7 PRECEDING)` |
| **COUNT() OVER** | Running counts | Cumulative | Progress tracking | `COUNT(*) OVER (ORDER BY date)` |
| **MIN/MAX() OVER** | Running min/max | Cumulative | Peak detection | `MAX(temperature) OVER (ORDER BY date)` |

### Offset Functions
| Function | Purpose | Default Value | Use Cases | Example |
|----------|---------|---------------|-----------|---------|
| **LAG(col, n)** | Previous row value | NULL | Period-over-period | `LAG(sales, 1) OVER (ORDER BY month)` |
| **LEAD(col, n)** | Next row value | NULL | Forward looking | `LEAD(price, 1) OVER (ORDER BY date)` |
| **FIRST_VALUE()** | First in window | N/A | Baseline comparison | `FIRST_VALUE(price) OVER (ORDER BY date)` |
| **LAST_VALUE()** | Last in window | N/A | Latest value | `LAST_VALUE(price) OVER (ORDER BY date ROWS UNBOUNDED FOLLOWING)` |
| **NTH_VALUE(col, n)** | Nth value in window | NULL | Specific position | `NTH_VALUE(price, 2) OVER (ORDER BY date)` |

## 🔧 Advanced SQL Patterns

### Data Deduplication
| Pattern | Use Case | Performance | Complexity | Example |
|---------|----------|-------------|------------|---------|
| **ROW_NUMBER()** | Remove duplicates | Good | Medium | `DELETE FROM t WHERE id NOT IN (SELECT MIN(id) FROM t GROUP BY key)` |
| **EXISTS** | Check duplicates | Good | Low | `DELETE t1 FROM table t1, table t2 WHERE t1.id > t2.id AND t1.key = t2.key` |
| **DISTINCT ON** | PostgreSQL specific | Excellent | Low | `SELECT DISTINCT ON (key) * FROM table ORDER BY key, date DESC` |
| **Window + CTE** | Complex deduplication | Good | High | `WITH ranked AS (SELECT *, ROW_NUMBER() OVER (...) rn FROM t) DELETE FROM ranked WHERE rn > 1` |

### Pivot and Unpivot Operations
| Database | Pivot Syntax | Unpivot Syntax | Dynamic Pivot | Limitations |
|----------|--------------|----------------|---------------|-------------|
| **SQL Server** | `PIVOT` operator | `UNPIVOT` operator | Dynamic SQL | Fixed columns |
| **Oracle** | `PIVOT` operator | `UNPIVOT` operator | Dynamic SQL | Fixed columns |
| **PostgreSQL** | `crosstab()` | Manual UNION | Dynamic SQL | Extension required |
| **MySQL** | Manual CASE | Manual UNION | Dynamic SQL | No native support |
| **BigQuery** | `PIVOT` operator | `UNPIVOT` operator | Dynamic SQL | Limited |
| **Snowflake** | `PIVOT` operator | Manual UNION | Dynamic SQL | Partial support |

### Hierarchical Data Queries
| Pattern | Database Support | Performance | Use Cases | Complexity |
|---------|------------------|-------------|-----------|------------|
| **Recursive CTEs** | Most modern DBs | Good | Org charts, categories | Medium |
| **CONNECT BY** | Oracle | Excellent | Tree traversal | Medium |
| **Nested Sets** | All | Excellent | Read-heavy trees | High |
| **Path Enumeration** | All | Good | Simple hierarchies | Low |
| **Closure Tables** | All | Good | Complex relationships | High |

## 📈 Performance Optimization Techniques

### Index Strategies
| Index Type | Best For | Overhead | Maintenance | Use Cases |
|------------|----------|----------|-------------|-----------|
| **B-Tree** | Equality, range queries | Low | Low | Primary keys, foreign keys |
| **Hash** | Equality only | Very Low | Low | Exact matches |
| **Bitmap** | Low cardinality | Medium | Medium | Data warehouses |
| **Partial** | Filtered data | Low | Low | Sparse data |
| **Composite** | Multiple columns | Medium | Medium | Complex WHERE clauses |
| **Covering** | Include columns | Medium | High | Avoid table lookups |
| **Functional** | Expressions | Medium | Medium | Computed values |

### Query Optimization Patterns
| Pattern | Performance Gain | Complexity | Use Cases | Example |
|---------|------------------|------------|-----------|---------|
| **EXISTS vs IN** | Variable | Low | Subqueries | `EXISTS (SELECT 1 FROM ...)` vs `col IN (SELECT ...)` |
| **JOIN vs Subquery** | High | Medium | Related data | `INNER JOIN` vs correlated subquery |
| **UNION ALL vs UNION** | High | Low | Combining results | Avoid DISTINCT when not needed |
| **Limit with ORDER BY** | High | Low | Top N queries | Use appropriate indexes |
| **Batch Processing** | Very High | Medium | Large updates | Process in chunks |

### Execution Plan Analysis
| Database | Tool | Key Metrics | Cost Model | Optimization Hints |
|----------|------|-------------|------------|-------------------|
| **PostgreSQL** | EXPLAIN ANALYZE | Actual time, rows | Cost-based | Limited hints |
| **MySQL** | EXPLAIN FORMAT=JSON | Cost, filtered | Cost-based | Index hints |
| **SQL Server** | Execution Plan | CPU, I/O, duration | Cost-based | Query hints |
| **Oracle** | EXPLAIN PLAN | Cost, cardinality | Cost-based | Extensive hints |
| **BigQuery** | Query Plan | Slot time, shuffle | Cost-based | No hints |
| **Snowflake** | Query Profile | Credits, partitions | Cost-based | Limited hints |

## 🔄 Data Transformation Patterns

### Date and Time Operations
| Operation | PostgreSQL | MySQL | SQL Server | Oracle | BigQuery | Snowflake |
|-----------|------------|-------|------------|--------|----------|-----------|
| **Current Timestamp** | `NOW()` | `NOW()` | `GETDATE()` | `SYSDATE` | `CURRENT_TIMESTAMP()` | `CURRENT_TIMESTAMP()` |
| **Date Arithmetic** | `+ INTERVAL` | `+ INTERVAL` | `DATEADD()` | `+ INTERVAL` | `DATE_ADD()` | `DATEADD()` |
| **Date Truncation** | `DATE_TRUNC()` | `DATE()` | `DATEPART()` | `TRUNC()` | `DATE_TRUNC()` | `DATE_TRUNC()` |
| **Extract Parts** | `EXTRACT()` | `EXTRACT()` | `DATEPART()` | `EXTRACT()` | `EXTRACT()` | `EXTRACT()` |
| **Format Dates** | `TO_CHAR()` | `DATE_FORMAT()` | `FORMAT()` | `TO_CHAR()` | `FORMAT_DATE()` | `TO_CHAR()` |

### String Manipulation
| Function | Purpose | PostgreSQL | MySQL | SQL Server | Oracle | BigQuery | Snowflake |
|----------|---------|------------|-------|------------|--------|----------|-----------|
| **Concatenation** | Join strings | `\|\|` or `CONCAT()` | `CONCAT()` | `+` or `CONCAT()` | `\|\|` | `CONCAT()` | `\|\|` |
| **Substring** | Extract part | `SUBSTRING()` | `SUBSTRING()` | `SUBSTRING()` | `SUBSTR()` | `SUBSTR()` | `SUBSTRING()` |
| **Replace** | Replace text | `REPLACE()` | `REPLACE()` | `REPLACE()` | `REPLACE()` | `REPLACE()` | `REPLACE()` |
| **Split** | Split strings | `STRING_TO_ARRAY()` | `SUBSTRING_INDEX()` | `STRING_SPLIT()` | `REGEXP_SUBSTR()` | `SPLIT()` | `SPLIT()` |
| **Regex** | Pattern matching | `~` operator | `REGEXP` | `PATINDEX()` | `REGEXP_LIKE()` | `REGEXP_CONTAINS()` | `REGEXP()` |

### Conditional Logic
| Pattern | Syntax | Use Cases | Performance | Readability |
|---------|--------|-----------|-------------|-------------|
| **CASE WHEN** | `CASE WHEN condition THEN value END` | Complex conditions | Good | High |
| **IIF** | `IIF(condition, true_value, false_value)` | Simple conditions | Excellent | Medium |
| **COALESCE** | `COALESCE(val1, val2, val3)` | NULL handling | Excellent | High |
| **NULLIF** | `NULLIF(val1, val2)` | Convert to NULL | Excellent | Medium |
| **GREATEST/LEAST** | `GREATEST(val1, val2, val3)` | Min/max of values | Excellent | High |

## 🌐 JSON and Semi-Structured Data

### JSON Functions by Database
| Function | PostgreSQL | MySQL | SQL Server | Oracle | BigQuery | Snowflake |
|----------|------------|-------|------------|--------|----------|-----------|
| **Extract Value** | `->`, `->>` | `JSON_EXTRACT()` | `JSON_VALUE()` | `JSON_VALUE()` | `JSON_EXTRACT()` | `GET()` |
| **Extract Array** | `json_array_elements()` | `JSON_TABLE()` | `OPENJSON()` | `JSON_TABLE()` | `JSON_EXTRACT_ARRAY()` | `FLATTEN()` |
| **Path Exists** | `?` operator | `JSON_CONTAINS_PATH()` | `ISJSON()` | `JSON_EXISTS()` | N/A | N/A |
| **Modify JSON** | `jsonb_set()` | `JSON_SET()` | `JSON_MODIFY()` | `JSON_MERGEPATCH()` | N/A | `OBJECT_CONSTRUCT()` |
| **Validate JSON** | Built-in | `JSON_VALID()` | `ISJSON()` | `JSON_VALID()` | N/A | `TRY_PARSE_JSON()` |

### Array Operations
| Operation | PostgreSQL | BigQuery | Snowflake | Oracle | Use Cases |
|-----------|------------|----------|-----------|--------|-----------|
| **Create Array** | `ARRAY[1,2,3]` | `[1,2,3]` | `ARRAY_CONSTRUCT()` | `ARRAY[1,2,3]` | Data aggregation |
| **Array Length** | `array_length()` | `ARRAY_LENGTH()` | `ARRAY_SIZE()` | `CARDINALITY()` | Validation |
| **Array Contains** | `@>` operator | `value IN UNNEST(array)` | `ARRAY_CONTAINS()` | `value MEMBER OF array` | Filtering |
| **Array Unnest** | `unnest()` | `UNNEST()` | `FLATTEN()` | `TABLE()` | Normalization |
| **Array Aggregation** | `array_agg()` | `ARRAY_AGG()` | `ARRAY_AGG()` | `COLLECT()` | Grouping |

## 🔒 Security and Access Control

### SQL Injection Prevention
| Technique | Effectiveness | Implementation | Performance Impact | Use Cases |
|-----------|---------------|----------------|-------------------|-----------|
| **Parameterized Queries** | Very High | Application code | None | All dynamic SQL |
| **Stored Procedures** | High | Database | Minimal | Complex operations |
| **Input Validation** | Medium | Application code | Minimal | User inputs |
| **Least Privilege** | High | Database permissions | None | Access control |
| **SQL Escaping** | Medium | Application code | Minimal | Legacy systems |

### Row-Level Security
| Database | Feature | Granularity | Performance | Use Cases |
|----------|---------|-------------|-------------|-----------|
| **PostgreSQL** | RLS Policies | Row-level | Good | Multi-tenant apps |
| **SQL Server** | Security Predicates | Row-level | Good | Data privacy |
| **Oracle** | VPD (Virtual Private Database) | Row/column | Excellent | Enterprise security |
| **BigQuery** | Row-level security | Row-level | Good | Data governance |
| **Snowflake** | Row Access Policies | Row-level | Good | Data sharing |

## 📊 Analytics and Reporting Functions

### Statistical Functions
| Function | Purpose | Database Support | Use Cases | Example |
|----------|---------|------------------|-----------|---------|
| **STDDEV()** | Standard deviation | Most | Data analysis | `STDDEV(salary) OVER (PARTITION BY dept)` |
| **VARIANCE()** | Variance | Most | Statistical analysis | `VARIANCE(sales)` |
| **CORR()** | Correlation | PostgreSQL, Oracle | Relationship analysis | `CORR(x, y)` |
| **PERCENTILE_CONT()** | Continuous percentile | Most | Median, quartiles | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)` |
| **PERCENTILE_DISC()** | Discrete percentile | Most | Actual values | `PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY salary)` |

### Time Series Analysis
| Pattern | Use Cases | Complexity | Performance | Example |
|---------|-----------|------------|-------------|---------|
| **Gap and Island** | Consecutive sequences | High | Medium | Find continuous periods |
| **Running Totals** | Cumulative metrics | Low | Good | YTD calculations |
| **Period-over-Period** | Growth analysis | Medium | Good | Month-over-month comparison |
| **Moving Averages** | Trend smoothing | Medium | Good | 7-day moving average |
| **Seasonal Analysis** | Cyclical patterns | High | Medium | Year-over-year comparison |

## 🚀 Modern SQL Features

### Common Table Expressions (CTEs)
| Feature | Use Cases | Performance | Readability | Reusability |
|---------|-----------|-------------|-------------|-------------|
| **Simple CTE** | Query organization | Same as subquery | High | Within query |
| **Recursive CTE** | Hierarchical data | Variable | Medium | Within query |
| **Multiple CTEs** | Complex transformations | Good | Very High | Within query |
| **Materialized CTE** | Performance optimization | Excellent | High | Database-specific |

### MERGE Statement
| Database | Syntax | Features | Performance | Use Cases |
|----------|--------|----------|-------------|-----------|
| **SQL Server** | Full MERGE | INSERT/UPDATE/DELETE | Excellent | Data synchronization |
| **Oracle** | Full MERGE | INSERT/UPDATE/DELETE | Excellent | ETL operations |
| **PostgreSQL** | ON CONFLICT | INSERT/UPDATE only | Good | Upsert operations |
| **MySQL** | ON DUPLICATE KEY** | INSERT/UPDATE only | Good | Data loading |
| **BigQuery** | MERGE | INSERT/UPDATE/DELETE | Excellent | Data warehousing |
| **Snowflake** | MERGE | INSERT/UPDATE/DELETE | Excellent | Data pipelines |

## 🔧 Database-Specific Optimizations

### PostgreSQL Specific
| Feature | Use Case | Performance Impact | Configuration |
|---------|----------|-------------------|---------------|
| **VACUUM** | Reclaim space | High | Regular maintenance |
| **ANALYZE** | Update statistics | High | After data changes |
| **Partial Indexes** | Filtered data | Very High | `WHERE` clause in index |
| **Expression Indexes** | Computed columns | High | Function-based indexes |
| **Parallel Queries** | Large datasets | Very High | `max_parallel_workers` |

### BigQuery Specific
| Feature | Use Case | Cost Impact | Performance Impact |
|---------|----------|-------------|-------------------|
| **Partitioning** | Time-based data | Very High | Very High |
| **Clustering** | Frequently filtered columns | High | High |
| **Materialized Views** | Repeated queries | Medium | Very High |
| **BI Engine** | Interactive queries | Low | Very High |
| **Approximate Functions** | Large datasets | Very High | High |

### Snowflake Specific
| Feature | Use Case | Credit Impact | Performance Impact |
|---------|----------|---------------|-------------------|
| **Clustering Keys** | Large tables | Low | Very High |
| **Result Caching** | Repeated queries | Very High | Very High |
| **Automatic Clustering** | Maintenance-free | Medium | High |
| **Multi-cluster Warehouses** | Concurrency | Variable | High |
| **Zero-copy Cloning** | Development/testing | Very High | N/A |

## 📚 Learning and Certification Paths

### Skill Progression
| Level | Focus Areas | Time Investment | Key Skills | Certifications |
|-------|-------------|-----------------|------------|----------------|
| **Beginner** | Basic CRUD, JOINs | 1-3 months | SELECT, INSERT, UPDATE, DELETE | None |
| **Intermediate** | Window functions, CTEs | 3-6 months | Analytics, performance tuning | Vendor-specific |
| **Advanced** | Query optimization, indexing | 6-12 months | Database internals, troubleshooting | Professional certs |
| **Expert** | Database design, architecture | 1+ years | System design, mentoring | Architect certs |

### Practice Resources
| Resource | Type | Focus | Difficulty | Cost |
|----------|------|-------|------------|------|
| **SQLBolt** | Interactive | Basics | Beginner | Free |
| **HackerRank SQL** | Challenges | Problem solving | All levels | Free |
| **LeetCode Database** | Challenges | Interview prep | Intermediate+ | Freemium |
| **SQLZoo** | Interactive | Comprehensive | All levels | Free |
| **Mode Analytics** | Tutorials | Real-world scenarios | Intermediate | Free |
| **DataCamp** | Courses | Structured learning | All levels | Paid |