# Data Warehousing Interview Questions

## Basic Level (0-2 years)

### 1. What is a data warehouse and how does it differ from a database?
**Answer:**
- **Data Warehouse**: Centralized repository for integrated data from multiple sources, optimized for analytics
- **Database**: Operational system optimized for transactions (OLTP)

**Key Differences:**
- Purpose: Analytics vs Operations
- Schema: Denormalized vs Normalized
- Queries: Complex analytical vs Simple transactional
- Data: Historical vs Current

### 2. Explain the difference between OLTP and OLAP systems.
**Answer:**
- **OLTP (Online Transaction Processing)**: Handles day-to-day operations
  - Fast, simple queries
  - Normalized data
  - Current data
  - High concurrency
- **OLAP (Online Analytical Processing)**: Handles analytical queries
  - Complex queries
  - Denormalized data
  - Historical data
  - Lower concurrency

### 3. What is a fact table and dimension table?
**Answer:**
- **Fact Table**: Contains measurable business metrics (facts)
  - Quantitative data (sales amount, quantity)
  - Foreign keys to dimensions
  - Large number of rows
- **Dimension Table**: Contains descriptive attributes
  - Qualitative data (customer name, product category)
  - Provides context to facts
  - Smaller number of rows

## Intermediate Level (2-5 years)

### 4. Explain different types of slowly changing dimensions (SCD).
**Answer:**
- **Type 0**: No changes allowed
- **Type 1**: Overwrite old values
- **Type 2**: Create new record for changes
- **Type 3**: Add new column for changes
- **Type 4**: Separate history table
- **Type 6**: Combination of Types 1, 2, and 3

**Example SCD Type 2:**
```sql
-- Original record
INSERT INTO dim_customer VALUES (1, 'John', 'New York', '2024-01-01', NULL, TRUE);

-- Customer moves to California
UPDATE dim_customer SET end_date = '2024-06-01', is_current = FALSE WHERE customer_key = 1;
INSERT INTO dim_customer VALUES (2, 'John', 'California', '2024-06-01', NULL, TRUE);
```

### 5. What is data partitioning in data warehouses?
**Answer:**
Dividing large tables into smaller, manageable pieces based on specific criteria.

**Types:**
- **Range Partitioning**: By date ranges
- **Hash Partitioning**: By hash function
- **List Partitioning**: By specific values

**Benefits:**
- Improved query performance
- Parallel processing
- Easier maintenance
- Better resource utilization

## Advanced Level (5+ years)

### 6. How would you design a modern data warehouse architecture?
**Answer:**
**Modern Architecture Components:**
- **Data Sources**: Operational systems, APIs, files
- **Ingestion Layer**: Batch and streaming ingestion
- **Storage Layer**: Data lake + data warehouse
- **Processing Layer**: ETL/ELT engines
- **Serving Layer**: Data marts, OLAP cubes
- **Access Layer**: BI tools, APIs

**Design Principles:**
- Scalability and elasticity
- Schema flexibility
- Real-time capabilities
- Cost optimization
- Data governance

### 7. Explain the concept of a data lakehouse.
**Answer:**
Combines benefits of data lakes and data warehouses:
- **Storage**: Cheap object storage like data lakes
- **Performance**: Query performance like data warehouses
- **ACID Transactions**: Data consistency
- **Schema Evolution**: Flexible schema handling
- **Unified Analytics**: Batch and streaming in one platform

**Technologies**: Delta Lake, Apache Iceberg, Apache Hudi