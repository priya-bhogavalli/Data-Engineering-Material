# Analytical Stores Interview Questions

## 🏪 Analytical Store Fundamentals

### Q1: What are analytical stores and how do they differ from transactional systems?
**Answer:**

**Analytical Stores (OLAP):**
- Optimized for read-heavy workloads
- Denormalized data structures
- Historical data storage
- Complex queries and aggregations
- Batch processing oriented

**Transactional Systems (OLTP):**
- Optimized for write-heavy workloads
- Normalized data structures
- Current state data
- Simple CRUD operations
- Real-time processing

**Key Differences:**
```sql
-- OLTP: Normalized structure
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2)
);

-- OLAP: Denormalized structure
CREATE TABLE sales_fact (
    order_id INT,
    customer_id INT,
    product_id INT,
    order_date DATE,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    category VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    profit_margin DECIMAL(5,2)
);
```

### Q2: Explain different types of analytical stores.
**Answer:**

**Data Warehouses:**
- Centralized repository
- Structured data
- ETL processes
- Historical analysis

**Data Lakes:**
- Raw data storage
- Multiple formats (structured, semi-structured, unstructured)
- ELT processes
- Exploratory analysis

**Data Marts:**
- Subject-specific subsets
- Departmental focus
- Faster query performance
- Simplified access

**Lakehouse Architecture:**
```python
# Modern lakehouse combining warehouse and lake benefits
class LakehouseArchitecture:
    def __init__(self):
        self.storage_layer = "S3/ADLS"  # Object storage
        self.metadata_layer = "Delta Lake/Iceberg"  # ACID transactions
        self.compute_layer = "Spark/Databricks"  # Processing engine
        self.serving_layer = "BI Tools/APIs"  # Analytics interface
    
    def process_data(self, raw_data):
        # Bronze layer: Raw data
        bronze_path = f"{self.storage_layer}/bronze/raw_data/"
        self.write_raw_data(raw_data, bronze_path)
        
        # Silver layer: Cleaned data
        silver_path = f"{self.storage_layer}/silver/cleaned_data/"
        cleaned_data = self.clean_and_validate(raw_data)
        self.write_delta_table(cleaned_data, silver_path)
        
        # Gold layer: Business-ready data
        gold_path = f"{self.storage_layer}/gold/aggregated_data/"
        aggregated_data = self.create_business_metrics(cleaned_data)
        self.write_delta_table(aggregated_data, gold_path)
```

## 🏗️ Data Warehouse Architecture

### Q3: Describe the components of a modern data warehouse architecture.
**Answer:**

**Traditional Data Warehouse Components:**
```python
# ETL Pipeline Architecture
class DataWarehouseETL:
    def __init__(self):
        self.staging_area = StagingDatabase()
        self.data_warehouse = DataWarehouse()
        self.data_marts = {}
    
    def extract(self, source_systems):
        """Extract data from various sources"""
        extracted_data = {}
        
        for system_name, connection in source_systems.items():
            if system_name == 'crm':
                extracted_data[system_name] = self.extract_crm_data(connection)
            elif system_name == 'erp':
                extracted_data[system_name] = self.extract_erp_data(connection)
            elif system_name == 'web_logs':
                extracted_data[system_name] = self.extract_log_data(connection)
        
        return extracted_data
    
    def transform(self, raw_data):
        """Transform and clean data"""
        transformed_data = {}
        
        for source, data in raw_data.items():
            # Data cleaning
            cleaned_data = self.clean_data(data)
            
            # Data standardization
            standardized_data = self.standardize_formats(cleaned_data)
            
            # Business rule application
            business_data = self.apply_business_rules(standardized_data)
            
            transformed_data[source] = business_data
        
        return transformed_data
    
    def load(self, transformed_data):
        """Load data into warehouse"""
        # Load into staging
        for source, data in transformed_data.items():
            self.staging_area.load_data(f"staging_{source}", data)
        
        # Load into warehouse dimensions and facts
        self.load_dimensions(transformed_data)
        self.load_facts(transformed_data)
        
        # Update data marts
        self.refresh_data_marts()
```

**Modern Cloud Data Warehouse:**
```python
# Snowflake/BigQuery/Redshift Architecture
class CloudDataWarehouse:
    def __init__(self, platform='snowflake'):
        self.platform = platform
        self.compute_clusters = {}
        self.storage_layer = "Separated storage"
        self.metadata_service = "Automatic optimization"
    
    def create_virtual_warehouse(self, name, size='MEDIUM'):
        """Create compute cluster for specific workloads"""
        if self.platform == 'snowflake':
            return f"""
            CREATE WAREHOUSE {name}
            WITH WAREHOUSE_SIZE = '{size}'
                 AUTO_SUSPEND = 300
                 AUTO_RESUME = TRUE
                 INITIALLY_SUSPENDED = TRUE;
            """
    
    def implement_zero_copy_cloning(self, source_db, target_db):
        """Instant database cloning for dev/test"""
        return f"CREATE DATABASE {target_db} CLONE {source_db};"
    
    def setup_time_travel(self, table_name, retention_days=7):
        """Point-in-time data recovery"""
        return f"""
        ALTER TABLE {table_name} 
        SET DATA_RETENTION_TIME_IN_DAYS = {retention_days};
        """
```

### Q4: How do you design fact and dimension tables?
**Answer:**

**Star Schema Design:**
```sql
-- Dimension Tables
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,  -- Surrogate key
    customer_id VARCHAR(50),       -- Natural key
    customer_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    customer_segment VARCHAR(20),
    effective_date DATE,           -- SCD Type 2
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(100),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10,2),
    effective_date DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,      -- YYYYMMDD format
    full_date DATE,
    day_of_week INT,
    day_name VARCHAR(10),
    month_number INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    fiscal_year INT,
    fiscal_quarter INT
);

-- Fact Table
CREATE TABLE fact_sales (
    sales_key BIGINT PRIMARY KEY,
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    date_key INT REFERENCES dim_date(date_key),
    order_id VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    cost_amount DECIMAL(10,2),
    profit_amount DECIMAL(10,2)
);
```

**Slowly Changing Dimensions (SCD):**
```python
# SCD Type 2 Implementation
class SCDType2Handler:
    def update_customer_dimension(self, customer_data):
        """Handle customer changes with history preservation"""
        
        # Check if customer exists
        existing_customer = self.get_current_customer(customer_data['customer_id'])
        
        if existing_customer:
            # Check if data has changed
            if self.has_changes(existing_customer, customer_data):
                # Close current record
                self.close_current_record(existing_customer['customer_key'])
                
                # Insert new record
                new_customer_key = self.insert_new_customer_record(customer_data)
                
                return new_customer_key
            else:
                return existing_customer['customer_key']
        else:
            # New customer
            return self.insert_new_customer_record(customer_data)
    
    def close_current_record(self, customer_key):
        """Close current SCD record"""
        query = """
        UPDATE dim_customer 
        SET expiry_date = CURRENT_DATE - 1,
            is_current = FALSE
        WHERE customer_key = %s AND is_current = TRUE
        """
        self.execute_query(query, (customer_key,))
    
    def insert_new_customer_record(self, customer_data):
        """Insert new SCD record"""
        query = """
        INSERT INTO dim_customer (
            customer_id, customer_name, email, phone, address,
            city, state, country, customer_segment,
            effective_date, expiry_date, is_current
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            CURRENT_DATE, '9999-12-31', TRUE
        ) RETURNING customer_key
        """
        return self.execute_query(query, tuple(customer_data.values())).fetchone()[0]
```

## 📊 Columnar Storage & Optimization

### Q5: Explain columnar storage and its benefits for analytical workloads.
**Answer:**

**Row vs Column Storage:**
```python
# Row-oriented storage (traditional RDBMS)
class RowStorage:
    def store_data(self, records):
        """Store complete records together"""
        # Record 1: [ID=1, Name="John", Age=25, Salary=50000]
        # Record 2: [ID=2, Name="Jane", Age=30, Salary=60000]
        # Record 3: [ID=3, Name="Bob", Age=35, Salary=70000]
        
        # Good for: OLTP, full record access
        # Bad for: Analytical queries on specific columns
        pass

# Column-oriented storage (analytical systems)
class ColumnStorage:
    def store_data(self, records):
        """Store columns separately"""
        # ID column: [1, 2, 3]
        # Name column: ["John", "Jane", "Bob"]
        # Age column: [25, 30, 35]
        # Salary column: [50000, 60000, 70000]
        
        # Benefits:

### Q6: How do you implement data partitioning strategies?
**Answer:**

**Partitioning Strategies:**
```sql
-- Range Partitioning (by date)
CREATE TABLE sales_2023 (
    sale_id BIGINT,
    customer_id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2023_q1 PARTITION OF sales_2023
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');

CREATE TABLE sales_2023_q2 PARTITION OF sales_2023
    FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');

-- Hash Partitioning (by customer_id)
CREATE TABLE customer_orders (
    order_id BIGINT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
) PARTITION BY HASH (customer_id);

CREATE TABLE customer_orders_p1 PARTITION OF customer_orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE customer_orders_p2 PARTITION OF customer_orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
```

**Dynamic Partitioning in Spark:**
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import year, month, dayofmonth

spark = SparkSession.builder.appName("DataPartitioning").getOrCreate()

class PartitioningStrategy:
    def __init__(self, spark_session):
        self.spark = spark_session
    
    def partition_by_date_hierarchy(self, df, date_column):
        """Partition data by year/month/day hierarchy"""
        partitioned_df = df.withColumn("year", year(date_column)) \
                          .withColumn("month", month(date_column)) \
                          .withColumn("day", dayofmonth(date_column))
        
        # Write with hierarchical partitioning
        partitioned_df.write \
            .partitionBy("year", "month", "day") \
            .mode("overwrite") \
            .parquet("s3://data-lake/sales/")
        
        return partitioned_df
    
    def partition_by_business_logic(self, df):
        """Partition by business-relevant dimensions"""
        # Add partition columns based on business logic
        partitioned_df = df.withColumn("region", 
                                     when(col("country").isin(["US", "CA"]), "North America")
                                     .when(col("country").isin(["UK", "DE", "FR"]), "Europe")
                                     .otherwise("Other"))
        
        # Partition by region and product category
        partitioned_df.write \
            .partitionBy("region", "product_category") \
            .mode("overwrite") \
            .parquet("s3://data-lake/sales_by_region/")
        
        return partitioned_df
    
    def optimize_partition_size(self, df, target_size_mb=128):
        """Optimize partition sizes for query performance"""
        # Calculate optimal number of partitions
        total_size_mb = df.count() * df.schema.simpleString().count(',') * 8 / (1024 * 1024)  # Rough estimate
        optimal_partitions = max(1, int(total_size_mb / target_size_mb))
        
        # Repartition for optimal size
        optimized_df = df.repartition(optimal_partitions)
        
        return optimized_df
```

## 🚀 Performance Optimization

### Q7: How do you optimize analytical query performance?
**Answer:**

**Indexing Strategies:**
```sql
-- Bitmap indexes for low-cardinality columns
CREATE BITMAP INDEX idx_product_category ON sales_fact(product_category);

-- Clustered columnstore index (SQL Server)
CREATE CLUSTERED COLUMNSTORE INDEX cci_sales_fact ON sales_fact;

-- Materialized views for common aggregations
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT 
    DATE_TRUNC('month', sale_date) as month,
    product_category,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count,
    AVG(amount) as avg_transaction_value
FROM sales_fact
GROUP BY DATE_TRUNC('month', sale_date), product_category;

-- Automatic refresh
ALTER MATERIALIZED VIEW mv_monthly_sales SET (auto_refresh = true);
```

**Query Optimization Techniques:**
```python
class QueryOptimizer:
    def __init__(self, connection):
        self.conn = connection
    
    def optimize_aggregation_query(self):
        """Use pre-aggregated tables for better performance"""
        
        # Instead of scanning full fact table
        slow_query = """
        SELECT customer_segment, SUM(total_amount)
        FROM fact_sales fs
        JOIN dim_customer dc ON fs.customer_key = dc.customer_key
        WHERE sale_date >= '2023-01-01'
        GROUP BY customer_segment
        """
        
        # Use pre-aggregated summary table
        fast_query = """
        SELECT customer_segment, SUM(daily_total)
        FROM daily_sales_summary
        WHERE sale_date >= '2023-01-01'
        GROUP BY customer_segment
        """
        
        return fast_query
    
    def implement_query_caching(self, query, cache_duration=3600):
        """Implement result caching for expensive queries"""
        import hashlib
        import json
        from datetime import datetime, timedelta
        
        # Generate cache key
        query_hash = hashlib.md5(query.encode()).hexdigest()
        cache_key = f"query_cache:{query_hash}"
        
        # Check cache
        cached_result = self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        
        # Execute query
        result = self.conn.execute(query).fetchall()
        
        # Cache result
        self.redis_client.setex(
            cache_key, 
            cache_duration, 
            json.dumps(result, default=str)
        )
        
        return result
    
    def partition_pruning_example(self):
        """Demonstrate partition pruning benefits"""
        
        # Query with partition pruning
        optimized_query = """
        SELECT product_name, SUM(quantity)
        FROM sales_partitioned
        WHERE sale_date BETWEEN '2023-06-01' AND '2023-06-30'  -- Only scans June partition
        GROUP BY product_name
        """
        
        # Query without partition pruning
        unoptimized_query = """
        SELECT product_name, SUM(quantity)
        FROM sales_unpartitioned
        WHERE EXTRACT(MONTH FROM sale_date) = 6  -- Scans all partitions
        GROUP BY product_name
        """
        
        return optimized_query
```

## 🎯 Key Takeaways

**Analytical Store Types:**
- **Data Warehouses**: Structured, centralized, ETL-based
- **Data Lakes**: Raw data, multiple formats, ELT-based
- **Data Marts**: Subject-specific, departmental focus
- **Lakehouses**: Combined benefits of warehouses and lakes

**Design Principles:**
- **Dimensional modeling**: Star/snowflake schemas
- **Columnar storage**: Better compression and query performance
- **Partitioning**: Improved query performance and maintenance
- **Indexing**: Bitmap, columnstore, and specialized indexes

**Performance Optimization:**
- **Materialized views** for common aggregations
- **Query result caching** for expensive operations
- **Partition pruning** to reduce data scanned
- **Pre-aggregation** for faster reporting

**Modern Trends:**
- **Cloud-native** architectures (Snowflake, BigQuery, Redshift)
- **Separation of compute and storage**
- **Auto-scaling** and **serverless** options
- **Real-time analytics** capabilities