# Data Warehousing Key Concepts for Data Engineering

## 1. Data Warehouse Architecture
**What it is**: The structural design of a data warehouse system including its components and data flow.

**Components**:
- **Source Systems**: Operational databases, files, APIs
- **Staging Area**: Temporary storage for data transformation
- **Data Warehouse**: Central repository for integrated data
- **Data Marts**: Subject-specific subsets of data warehouse
- **Metadata Repository**: Information about data structure and lineage

```python
# Data warehouse architecture implementation
class DataWarehouseArchitecture:
    def __init__(self):
        self.staging_area = StagingArea()
        self.data_warehouse = DataWarehouse()
        self.data_marts = {}
        self.metadata_repository = MetadataRepository()
    
    def extract_from_sources(self, sources):
        """Extract data from multiple source systems"""
        extracted_data = {}
        
        for source_name, source in sources.items():
            try:
                data = source.extract()
                extracted_data[source_name] = data
                
                # Log metadata
                self.metadata_repository.log_extraction(
                    source_name, len(data), datetime.now()
                )
                
            except Exception as e:
                print(f"Failed to extract from {source_name}: {e}")
        
        return extracted_data
    
    def load_to_staging(self, extracted_data):
        """Load extracted data to staging area"""
        for source_name, data in extracted_data.items():
            staging_table = f"stg_{source_name}"
            self.staging_area.create_table(staging_table, data)
            self.staging_area.load_data(staging_table, data)
    
    def transform_and_load(self):
        """Transform data in staging and load to warehouse"""
        # Data cleansing
        cleaned_data = self.staging_area.clean_data()
        
        # Data integration
        integrated_data = self.staging_area.integrate_data()
        
        # Load to warehouse
        self.data_warehouse.load_dimensions(integrated_data['dimensions'])
        self.data_warehouse.load_facts(integrated_data['facts'])
    
    def create_data_marts(self, mart_definitions):
        """Create subject-specific data marts"""
        for mart_name, definition in mart_definitions.items():
            mart = DataMart(mart_name)
            mart.create_from_warehouse(self.data_warehouse, definition)
            self.data_marts[mart_name] = mart

# Example usage
dw_architecture = DataWarehouseArchitecture()

# Define source systems
sources = {
    'crm': CRMSource(),
    'erp': ERPSource(),
    'web_analytics': WebAnalyticsSource()
}

# ETL process
extracted_data = dw_architecture.extract_from_sources(sources)
dw_architecture.load_to_staging(extracted_data)
dw_architecture.transform_and_load()

# Create data marts
mart_definitions = {
    'sales_mart': {
        'tables': ['dim_customer', 'dim_product', 'fact_sales'],
        'filters': {'date_range': '2024-01-01 to 2024-12-31'}
    },
    'marketing_mart': {
        'tables': ['dim_customer', 'dim_campaign', 'fact_marketing'],
        'filters': {'active_campaigns': True}
    }
}

dw_architecture.create_data_marts(mart_definitions)
```

## 2. Dimensional Modeling
**What it is**: A design technique for structuring data warehouses using facts and dimensions for optimal query performance.

**Key Concepts**:
- **Facts**: Measurable business events (sales, orders, clicks)
- **Dimensions**: Context for facts (time, customer, product)
- **Star Schema**: Central fact table with dimension tables
- **Snowflake Schema**: Normalized dimension tables

```sql
-- Star Schema Implementation
-- Fact Table (center of star)
CREATE TABLE fact_sales (
    sale_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    
    -- Measures (facts)
    quantity_sold INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) NOT NULL,
    cost_amount DECIMAL(10,2) NOT NULL,
    
    -- Foreign key constraints
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);

-- Dimension Tables
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(100),
    customer_type VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    customer_segment VARCHAR(30),
    
    -- SCD Type 2 attributes
    effective_date DATE NOT NULL,
    expiration_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE,
    version_number INTEGER DEFAULT 1
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(100),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    brand VARCHAR(50),
    unit_cost DECIMAL(8,2),
    unit_price DECIMAL(8,2),
    
    -- Product hierarchy
    category_id INTEGER,
    subcategory_id INTEGER,
    brand_id INTEGER
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    month_number INTEGER,
    month_name VARCHAR(10),
    quarter_number INTEGER,
    year_number INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER
);

-- Analytical queries on star schema
SELECT 
    d.year_number,
    d.quarter_number,
    p.category,
    c.customer_segment,
    SUM(f.total_amount) as total_revenue,
    SUM(f.quantity_sold) as total_quantity,
    COUNT(DISTINCT f.customer_key) as unique_customers
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE d.year_number = 2024
GROUP BY d.year_number, d.quarter_number, p.category, c.customer_segment
ORDER BY total_revenue DESC;
```

## 3. Slowly Changing Dimensions (SCD)
**What it is**: Techniques to handle changes in dimension data over time while preserving historical accuracy.

**SCD Types**:
- **Type 0**: Retain original (no changes)
- **Type 1**: Overwrite (no history)
- **Type 2**: Add new record (full history)
- **Type 3**: Add new attribute (limited history)

```python
# SCD Type 2 Implementation
class SCDType2Handler:
    def __init__(self, connection):
        self.conn = connection
    
    def update_customer_dimension(self, new_customer_data):
        """Handle SCD Type 2 updates for customer dimension"""
        
        for customer in new_customer_data:
            customer_id = customer['customer_id']
            
            # Get current record
            current_record = self.get_current_customer(customer_id)
            
            if current_record is None:
                # New customer - insert new record
                self.insert_new_customer(customer)
            else:
                # Check if data has changed
                if self.has_customer_changed(current_record, customer):
                    # Expire current record
                    self.expire_current_record(current_record['customer_key'])
                    
                    # Insert new version
                    self.insert_new_customer_version(customer, current_record['version_number'] + 1)
    
    def get_current_customer(self, customer_id):
        """Get current active customer record"""
        query = """
        SELECT customer_key, customer_id, customer_name, city, state, 
               effective_date, version_number
        FROM dim_customer 
        WHERE customer_id = %s AND is_current = TRUE
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        
        if result:
            return {
                'customer_key': result[0],
                'customer_id': result[1],
                'customer_name': result[2],
                'city': result[3],
                'state': result[4],
                'effective_date': result[5],
                'version_number': result[6]
            }
        return None
    
    def has_customer_changed(self, current_record, new_data):
        """Check if customer data has changed"""
        tracked_fields = ['customer_name', 'city', 'state', 'customer_segment']
        
        for field in tracked_fields:
            if current_record.get(field) != new_data.get(field):
                return True
        
        return False
    
    def expire_current_record(self, customer_key):
        """Expire current customer record"""
        query = """
        UPDATE dim_customer 
        SET expiration_date = CURRENT_DATE - 1,
            is_current = FALSE
        WHERE customer_key = %s
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (customer_key,))
        self.conn.commit()
    
    def insert_new_customer_version(self, customer_data, version_number):
        """Insert new version of customer record"""
        query = """
        INSERT INTO dim_customer (
            customer_id, customer_name, city, state, customer_segment,
            effective_date, expiration_date, is_current, version_number
        ) VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, '9999-12-31', TRUE, %s)
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (
            customer_data['customer_id'],
            customer_data['customer_name'],
            customer_data['city'],
            customer_data['state'],
            customer_data['customer_segment'],
            version_number
        ))
        self.conn.commit()
    
    def insert_new_customer(self, customer_data):
        """Insert completely new customer"""
        self.insert_new_customer_version(customer_data, 1)

# Usage example
scd_handler = SCDType2Handler(database_connection)

# Sample customer updates
customer_updates = [
    {
        'customer_id': 'CUST001',
        'customer_name': 'John Doe',
        'city': 'New York',  # Changed from 'Boston'
        'state': 'NY',       # Changed from 'MA'
        'customer_segment': 'Premium'
    }
]

scd_handler.update_customer_dimension(customer_updates)
```

## 4. Data Warehouse Performance Optimization
**What it is**: Techniques to improve query performance and system efficiency in data warehouses.

```sql
-- Indexing strategies for data warehouses
-- 1. Clustered indexes on fact table date columns
CREATE CLUSTERED INDEX idx_fact_sales_date 
ON fact_sales(date_key);

-- 2. Non-clustered indexes on frequently queried dimensions
CREATE INDEX idx_fact_sales_customer 
ON fact_sales(customer_key);

CREATE INDEX idx_fact_sales_product 
ON fact_sales(product_key);

-- 3. Composite indexes for common query patterns
CREATE INDEX idx_fact_sales_date_customer 
ON fact_sales(date_key, customer_key);

-- 4. Covering indexes to avoid key lookups
CREATE INDEX idx_customer_covering 
ON dim_customer(customer_id, customer_name, city, state) 
WHERE is_current = TRUE;

-- Partitioning for large fact tables
CREATE TABLE fact_sales_partitioned (
    sale_key BIGSERIAL,
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    created_date DATE NOT NULL
) PARTITION BY RANGE (date_key);

-- Create monthly partitions
CREATE TABLE fact_sales_202401 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20240101) TO (20240201);

CREATE TABLE fact_sales_202402 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20240201) TO (20240301);

-- Materialized views for common aggregations
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT 
    DATE_TRUNC('month', d.full_date) as month,
    p.category,
    c.customer_segment,
    SUM(f.total_amount) as total_revenue,
    COUNT(*) as transaction_count,
    COUNT(DISTINCT f.customer_key) as unique_customers
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_customer c ON f.customer_key = c.customer_key AND c.is_current = TRUE
GROUP BY DATE_TRUNC('month', d.full_date), p.category, c.customer_segment;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW mv_monthly_sales;

-- Query optimization techniques
-- Use EXISTS instead of IN for better performance
SELECT c.customer_name
FROM dim_customer c
WHERE c.is_current = TRUE
AND EXISTS (
    SELECT 1 FROM fact_sales f 
    WHERE f.customer_key = c.customer_key 
    AND f.date_key >= 20240101
);

-- Use window functions for analytical queries
SELECT 
    customer_key,
    total_amount,
    date_key,
    SUM(total_amount) OVER (
        PARTITION BY customer_key 
        ORDER BY date_key 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total,
    RANK() OVER (
        PARTITION BY date_key 
        ORDER BY total_amount DESC
    ) as daily_rank
FROM fact_sales
WHERE date_key >= 20240101;
```

## 5. Data Warehouse Testing and Quality Assurance
**What it is**: Systematic approach to ensure data warehouse accuracy, completeness, and reliability.

```python
# Data warehouse testing framework
import pandas as pd
from typing import Dict, List, Any
import logging

class DataWarehouseTestSuite:
    def __init__(self, connection):
        self.conn = connection
        self.test_results = []
        self.logger = logging.getLogger(__name__)
    
    def test_data_completeness(self, table_name: str, expected_count: int = None):
        """Test if data loading is complete"""
        query = f"SELECT COUNT(*) FROM {table_name}"
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        actual_count = cursor.fetchone()[0]
        
        test_result = {
            'test_name': f'{table_name}_completeness',
            'test_type': 'completeness',
            'expected': expected_count,
            'actual': actual_count,
            'passed': True if expected_count is None else actual_count == expected_count,
            'message': f'Table {table_name} has {actual_count} records'
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def test_referential_integrity(self, fact_table: str, dim_table: str, 
                                 fact_key: str, dim_key: str):
        """Test referential integrity between fact and dimension tables"""
        query = f"""
        SELECT COUNT(*) 
        FROM {fact_table} f
        LEFT JOIN {dim_table} d ON f.{fact_key} = d.{dim_key}
        WHERE d.{dim_key} IS NULL
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        orphaned_records = cursor.fetchone()[0]
        
        test_result = {
            'test_name': f'{fact_table}_{dim_table}_referential_integrity',
            'test_type': 'referential_integrity',
            'expected': 0,
            'actual': orphaned_records,
            'passed': orphaned_records == 0,
            'message': f'Found {orphaned_records} orphaned records in {fact_table}'
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def test_data_freshness(self, table_name: str, date_column: str, 
                          max_age_hours: int = 24):
        """Test if data is fresh (recently updated)"""
        query = f"""
        SELECT MAX({date_column}) as latest_date
        FROM {table_name}
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        latest_date = cursor.fetchone()[0]
        
        if latest_date:
            from datetime import datetime, timedelta
            age_hours = (datetime.now() - latest_date).total_seconds() / 3600
            is_fresh = age_hours <= max_age_hours
        else:
            age_hours = float('inf')
            is_fresh = False
        
        test_result = {
            'test_name': f'{table_name}_data_freshness',
            'test_type': 'freshness',
            'expected': f'<= {max_age_hours} hours',
            'actual': f'{age_hours:.1f} hours',
            'passed': is_fresh,
            'message': f'Data in {table_name} is {age_hours:.1f} hours old'
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def test_business_rules(self, table_name: str, rule_name: str, rule_query: str):
        """Test custom business rules"""
        cursor = self.conn.cursor()
        cursor.execute(rule_query)
        violations = cursor.fetchone()[0]
        
        test_result = {
            'test_name': f'{table_name}_{rule_name}',
            'test_type': 'business_rule',
            'expected': 0,
            'actual': violations,
            'passed': violations == 0,
            'message': f'Found {violations} violations of {rule_name} rule'
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def test_dimension_uniqueness(self, dim_table: str, key_column: str):
        """Test dimension table key uniqueness"""
        query = f"""
        SELECT COUNT(*) - COUNT(DISTINCT {key_column}) as duplicates
        FROM {dim_table}
        WHERE is_current = TRUE
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        duplicates = cursor.fetchone()[0]
        
        test_result = {
            'test_name': f'{dim_table}_key_uniqueness',
            'test_type': 'uniqueness',
            'expected': 0,
            'actual': duplicates,
            'passed': duplicates == 0,
            'message': f'Found {duplicates} duplicate keys in {dim_table}'
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def run_full_test_suite(self):
        """Run comprehensive test suite"""
        # Test fact table completeness
        self.test_data_completeness('fact_sales')
        
        # Test referential integrity
        self.test_referential_integrity('fact_sales', 'dim_customer', 
                                      'customer_key', 'customer_key')
        self.test_referential_integrity('fact_sales', 'dim_product', 
                                      'product_key', 'product_key')
        self.test_referential_integrity('fact_sales', 'dim_date', 
                                      'date_key', 'date_key')
        
        # Test data freshness
        self.test_data_freshness('fact_sales', 'created_date', max_age_hours=24)
        
        # Test dimension uniqueness
        self.test_dimension_uniqueness('dim_customer', 'customer_id')
        self.test_dimension_uniqueness('dim_product', 'product_id')
        
        # Test business rules
        self.test_business_rules('fact_sales', 'positive_amounts', 
                               "SELECT COUNT(*) FROM fact_sales WHERE total_amount <= 0")
        
        self.test_business_rules('fact_sales', 'valid_quantities',
                               "SELECT COUNT(*) FROM fact_sales WHERE quantity_sold <= 0")
        
        return self.generate_test_report()
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test['passed'])
        failed_tests = total_tests - passed_tests
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            'detailed_results': self.test_results,
            'failed_tests': [test for test in self.test_results if not test['passed']]
        }
        
        return report

# Usage
test_suite = DataWarehouseTestSuite(database_connection)
test_report = test_suite.run_full_test_suite()

print(f"Test Results: {test_report['summary']['passed_tests']}/{test_report['summary']['total_tests']} passed")
print(f"Success Rate: {test_report['summary']['success_rate']:.1f}%")

# Print failed tests
for failed_test in test_report['failed_tests']:
    print(f"FAILED: {failed_test['test_name']} - {failed_test['message']}")
```

## 6. Data Warehouse Automation and Orchestration
**What it is**: Automating data warehouse processes including ETL, testing, and deployment.

```python
# Data warehouse orchestration with Apache Airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sql_operator import SQLCheckOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    'owner': 'data-engineering-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

# Create DAG
dag = DAG(
    'data_warehouse_etl',
    default_args=default_args,
    description='Daily data warehouse ETL process',
    schedule_interval='0 2 * * *',  # Run at 2 AM daily
    catchup=False,
    max_active_runs=1
)

def extract_source_data(**context):
    """Extract data from source systems"""
    from data_warehouse_etl import SourceExtractor
    
    extractor = SourceExtractor()
    
    # Extract from multiple sources
    crm_data = extractor.extract_crm_data(context['ds'])
    erp_data = extractor.extract_erp_data(context['ds'])
    web_data = extractor.extract_web_analytics(context['ds'])
    
    # Store in staging area
    extractor.store_in_staging({
        'crm': crm_data,
        'erp': erp_data,
        'web': web_data
    })
    
    return f"Extracted data for {context['ds']}"

def transform_and_load(**context):
    """Transform data and load to warehouse"""
    from data_warehouse_etl import DataTransformer
    
    transformer = DataTransformer()
    
    # Transform staging data
    transformer.clean_and_integrate_data(context['ds'])
    
    # Load dimensions (SCD handling)
    transformer.load_dimensions(context['ds'])
    
    # Load facts
    transformer.load_facts(context['ds'])
    
    return f"Transformed and loaded data for {context['ds']}"

def run_data_quality_tests(**context):
    """Run data quality tests"""
    test_suite = DataWarehouseTestSuite(get_warehouse_connection())
    test_report = test_suite.run_full_test_suite()
    
    if test_report['summary']['success_rate'] < 95:
        raise Exception(f"Data quality tests failed. Success rate: {test_report['summary']['success_rate']:.1f}%")
    
    return f"Data quality tests passed: {test_report['summary']['success_rate']:.1f}%"

# Define tasks
extract_task = PythonOperator(
    task_id='extract_source_data',
    python_callable=extract_source_data,
    dag=dag
)

transform_load_task = PythonOperator(
    task_id='transform_and_load',
    python_callable=transform_and_load,
    dag=dag
)

# SQL check tasks
referential_integrity_check = SQLCheckOperator(
    task_id='check_referential_integrity',
    sql="""
    SELECT COUNT(*) 
    FROM fact_sales f
    LEFT JOIN dim_customer c ON f.customer_key = c.customer_key
    WHERE c.customer_key IS NULL
    """,
    dag=dag
)

data_freshness_check = SQLCheckOperator(
    task_id='check_data_freshness',
    sql="""
    SELECT CASE 
        WHEN MAX(created_date) >= CURRENT_DATE - INTERVAL '1 day' THEN 1 
        ELSE 0 
    END
    FROM fact_sales
    """,
    dag=dag
)

quality_tests_task = PythonOperator(
    task_id='run_quality_tests',
    python_callable=run_data_quality_tests,
    dag=dag
)

# Update materialized views
refresh_views_task = BashOperator(
    task_id='refresh_materialized_views',
    bash_command="""
    psql -h {{ params.host }} -d {{ params.database }} -c "REFRESH MATERIALIZED VIEW mv_monthly_sales;"
    psql -h {{ params.host }} -d {{ params.database }} -c "REFRESH MATERIALIZED VIEW mv_customer_summary;"
    """,
    params={
        'host': 'warehouse.company.com',
        'database': 'datawarehouse'
    },
    dag=dag
)

# Set task dependencies
extract_task >> transform_load_task >> [referential_integrity_check, data_freshness_check]
[referential_integrity_check, data_freshness_check] >> quality_tests_task >> refresh_views_task
```

These data warehousing concepts provide the foundation for building robust, scalable, and maintainable analytical data systems that support business intelligence and decision-making processes.