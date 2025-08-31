# Data Architecture Interview Questions

## Basic Level Questions

### 1. What is the difference between OLTP and OLAP systems?

**Answer:**
OLTP (Online Transaction Processing) and OLAP (Online Analytical Processing) serve different purposes:

**OLTP Systems:**
- Designed for day-to-day operational transactions
- Optimized for INSERT, UPDATE, DELETE operations
- Normalized data structure (3NF) to reduce redundancy
- Fast response times for individual transactions
- High concurrency with many users
- Examples: E-commerce systems, banking applications, CRM systems

**OLAP Systems:**
- Designed for analytical queries and reporting
- Optimized for SELECT operations and complex queries
- Denormalized data structure (star/snowflake schema)
- Can handle complex aggregations across large datasets
- Fewer concurrent users but complex queries
- Examples: Data warehouses, business intelligence systems

```sql
-- OLTP Example: Customer order transaction
BEGIN TRANSACTION;
INSERT INTO orders (customer_id, order_date, total_amount) 
VALUES (12345, '2024-01-15', 299.99);

INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES (LAST_INSERT_ID(), 'PROD001', 2, 149.99);

UPDATE inventory SET quantity = quantity - 2 
WHERE product_id = 'PROD001';
COMMIT;

-- OLAP Example: Sales analysis query
SELECT 
    p.category,
    DATE_TRUNC('month', o.order_date) as month,
    SUM(oi.quantity * oi.price) as total_revenue,
    COUNT(DISTINCT o.customer_id) as unique_customers
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2023-01-01'
GROUP BY p.category, DATE_TRUNC('month', o.order_date)
ORDER BY month, total_revenue DESC;
```

### 2. Explain the concept of data normalization and its normal forms.

**Answer:**
Data normalization is the process of organizing data to reduce redundancy and improve data integrity.

**First Normal Form (1NF):**
- Each column contains atomic (indivisible) values
- Each column contains values of the same type
- Each column has a unique name
- Order of rows and columns doesn't matter

```sql
-- Violates 1NF (multiple values in one column)
CREATE TABLE customers_bad (
    customer_id INT,
    name VARCHAR(100),
    phone_numbers VARCHAR(200)  -- "123-456-7890, 987-654-3210"
);

-- Follows 1NF
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE customer_phones (
    customer_id INT,
    phone_number VARCHAR(15),
    phone_type VARCHAR(10),
    PRIMARY KEY (customer_id, phone_number)
);
```

**Second Normal Form (2NF):**
- Must be in 1NF
- All non-key attributes must be fully functionally dependent on the primary key

```sql
-- Violates 2NF (partial dependency)
CREATE TABLE order_items_bad (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id
    quantity INT,
    unit_price DECIMAL(8,2),
    PRIMARY KEY (order_id, product_id)
);

-- Follows 2NF
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100)
);
```

**Third Normal Form (3NF):**
- Must be in 2NF
- No transitive dependencies (non-key attributes should not depend on other non-key attributes)

```sql
-- Violates 3NF (transitive dependency)
CREATE TABLE employees_bad (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT,
    department_name VARCHAR(50),  -- Depends on department_id, not employee_id
    salary DECIMAL(10,2)
);

-- Follows 3NF
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(100),
    department_id INT,
    salary DECIMAL(10,2)
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);
```

### 3. What is a data warehouse and how does it differ from a database?

**Answer:**
A data warehouse is a centralized repository designed for analytical processing and reporting, while a database is typically used for operational transactions.

**Key Differences:**

| Aspect | Database (OLTP) | Data Warehouse (OLAP) |
|--------|----------------|----------------------|
| Purpose | Day-to-day operations | Analysis and reporting |
| Data Structure | Normalized (3NF) | Denormalized (star/snowflake) |
| Query Types | Simple, frequent | Complex, analytical |
| Data Volume | Current data | Historical data |
| Users | Many concurrent | Fewer, analytical users |
| Response Time | Milliseconds | Seconds to minutes |

**Data Warehouse Architecture:**
```python
# Data Warehouse ETL Process
class DataWarehouseETL:
    def __init__(self, source_systems, staging_area, warehouse):
        self.source_systems = source_systems
        self.staging_area = staging_area
        self.warehouse = warehouse
    
    def extract(self):
        """Extract data from multiple source systems"""
        extracted_data = {}
        for system_name, system in self.source_systems.items():
            extracted_data[system_name] = system.extract_data()
        return extracted_data
    
    def transform(self, raw_data):
        """Transform data for analytical purposes"""
        transformed_data = {}
        
        for source, data in raw_data.items():
            # Data cleansing
            cleaned_data = self.clean_data(data)
            
            # Data integration
            integrated_data = self.integrate_data(cleaned_data)
            
            # Business rule application
            business_data = self.apply_business_rules(integrated_data)
            
            transformed_data[source] = business_data
        
        return transformed_data
    
    def load(self, transformed_data):
        """Load data into data warehouse"""
        # Load into staging tables first
        self.load_to_staging(transformed_data)
        
        # Then load into dimension tables
        self.load_dimensions()
        
        # Finally load into fact tables
        self.load_facts()
```

### 4. Explain the star schema and snowflake schema designs.

**Answer:**

**Star Schema:**
- Central fact table surrounded by dimension tables
- Dimension tables are denormalized
- Simple structure, easy to understand
- Better query performance
- More storage space due to denormalization

```sql
-- Star Schema Example
-- Fact Table (center of star)
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    total_amount DECIMAL(10,2),
    discount_amount DECIMAL(8,2)
);

-- Dimension Tables (denormalized)
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    age_group VARCHAR(20),
    customer_segment VARCHAR(30)
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(100),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    brand VARCHAR(50),
    supplier_name VARCHAR(100),  -- Denormalized
    supplier_country VARCHAR(50) -- Denormalized
);
```

**Snowflake Schema:**
- Normalized dimension tables
- Dimension tables are broken into sub-dimensions
- More complex structure
- Less storage space
- More complex queries due to additional joins

```sql
-- Snowflake Schema Example
-- Same fact table as star schema
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    quantity INT,
    unit_price DECIMAL(8,2),
    total_amount DECIMAL(10,2)
);

-- Normalized dimension tables
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50),
    product_name VARCHAR(100),
    category_key INT,  -- Foreign key to category table
    brand_key INT,     -- Foreign key to brand table
    supplier_key INT   -- Foreign key to supplier table
);

CREATE TABLE dim_category (
    category_key INT PRIMARY KEY,
    category VARCHAR(50),
    subcategory VARCHAR(50)
);

CREATE TABLE dim_brand (
    brand_key INT PRIMARY KEY,
    brand_name VARCHAR(50)
);

CREATE TABLE dim_supplier (
    supplier_key INT PRIMARY KEY,
    supplier_name VARCHAR(100),
    supplier_country VARCHAR(50)
);
```

### 5. What are slowly changing dimensions (SCDs) and their types?

**Answer:**
Slowly Changing Dimensions (SCDs) are dimensions that change slowly over time. There are several types:

**Type 0 - Retain Original:**
- Never change the data
- Historical accuracy is not important

**Type 1 - Overwrite:**
- Simply overwrite the old value with the new value
- No history is maintained

```sql
-- Type 1 SCD Example
UPDATE dim_customer 
SET city = 'New York', state = 'NY'
WHERE customer_id = 'CUST001';
```

**Type 2 - Add New Record:**
- Create a new record for each change
- Maintain full history
- Most commonly used

```sql
-- Type 2 SCD Example
CREATE TABLE dim_customer_scd2 (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    effective_date DATE,
    expiration_date DATE,
    is_current BOOLEAN,
    version_number INT
);

-- Insert new record
INSERT INTO dim_customer_scd2 (
    customer_id, first_name, last_name, city, state,
    effective_date, expiration_date, is_current, version_number
) VALUES (
    'CUST001', 'John', 'Doe', 'New York', 'NY',
    '2024-01-15', '9999-12-31', TRUE, 2
);

-- Update previous record
UPDATE dim_customer_scd2 
SET expiration_date = '2024-01-14', is_current = FALSE
WHERE customer_id = 'CUST001' AND is_current = TRUE 
AND customer_key != (SELECT MAX(customer_key) FROM dim_customer_scd2 WHERE customer_id = 'CUST001');
```

**Type 3 - Add New Attribute:**
- Add new columns to track changes
- Limited history (usually current and previous)

```sql
-- Type 3 SCD Example
CREATE TABLE dim_customer_scd3 (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    current_city VARCHAR(50),
    previous_city VARCHAR(50),
    current_state VARCHAR(50),
    previous_state VARCHAR(50),
    change_date DATE
);
```

## Intermediate Level Questions

### 6. Explain the Data Vault 2.0 methodology and its components.

**Answer:**
Data Vault 2.0 is a data modeling methodology designed for enterprise data warehouses that provides flexibility, scalability, and auditability.

**Core Components:**

**1. Hubs - Business Keys:**
```sql
CREATE TABLE hub_customer (
    customer_hk CHAR(32) PRIMARY KEY,  -- Hash of business key
    customer_id VARCHAR(50) NOT NULL,  -- Natural business key
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    UNIQUE(customer_id)
);
```

**2. Satellites - Descriptive Data:**
```sql
CREATE TABLE sat_customer_details (
    customer_hk CHAR(32),
    load_date TIMESTAMP,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(200),
    hash_diff CHAR(32) NOT NULL,  -- Hash of all attributes
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_hk, load_date),
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk)
);
```

**3. Links - Relationships:**
```sql
CREATE TABLE link_customer_order (
    customer_order_hk CHAR(32) PRIMARY KEY,  -- Hash of relationship
    customer_hk CHAR(32) NOT NULL,
    order_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk),
    FOREIGN KEY (order_hk) REFERENCES hub_order(order_hk)
);
```

**Data Vault Loading Process:**
```python
import hashlib
from datetime import datetime

class DataVaultLoader:
    def __init__(self, connection):
        self.connection = connection
    
    def generate_hash_key(self, *args):
        """Generate hash key from business key components"""
        concatenated = '||'.join(str(arg).upper().strip() for arg in args if arg)
        return hashlib.md5(concatenated.encode()).hexdigest().upper()
    
    def load_hub(self, table_name, business_key_cols, data, record_source):
        """Load hub table with new business keys"""
        hub_data = []
        
        for row in data:
            # Generate hash key
            bk_values = [row[col] for col in business_key_cols]
            hash_key = self.generate_hash_key(*bk_values)
            
            hub_record = {
                f'{table_name}_hk': hash_key,
                'load_date': datetime.now(),
                'record_source': record_source
            }
            
            # Add business key columns
            for col in business_key_cols:
                hub_record[col] = row[col]
            
            hub_data.append(hub_record)
        
        # Insert only new records
        self.insert_new_records(f'hub_{table_name}', hub_data, f'{table_name}_hk')
    
    def load_satellite(self, hub_name, sat_name, attribute_cols, data, record_source):
        """Load satellite table with descriptive data"""
        sat_data = []
        
        for row in data:
            # Generate hub hash key
            hub_hk = self.generate_hash_key(row['business_key'])
            
            # Generate hash diff for change detection
            attr_values = [str(row.get(col, '')) for col in attribute_cols]
            hash_diff = self.generate_hash_key(*attr_values)
            
            sat_record = {
                f'{hub_name}_hk': hub_hk,
                'load_date': datetime.now(),
                'hash_diff': hash_diff,
                'record_source': record_source
            }
            
            # Add attribute columns
            for col in attribute_cols:
                sat_record[col] = row.get(col)
            
            sat_data.append(sat_record)
        
        # Insert only records with different hash_diff
        self.insert_changed_records(f'sat_{sat_name}', sat_data)
```

### 7. What is Data Mesh architecture and how does it differ from traditional data architecture?

**Answer:**
Data Mesh is a decentralized data architecture that treats data as a product, with domain-oriented ownership and self-serve data infrastructure.

**Four Core Principles:**

**1. Domain-Oriented Decentralized Data Ownership:**
```python
# Domain-specific data product
class CustomerDataProduct:
    def __init__(self):
        self.domain = "customer_experience"
        self.owner = "customer_team"
        self.data_sources = ["crm", "support_tickets", "surveys"]
    
    def get_customer_360_view(self, customer_id):
        """Provide comprehensive customer view"""
        return {
            "profile": self.get_customer_profile(customer_id),
            "interactions": self.get_customer_interactions(customer_id),
            "satisfaction": self.get_satisfaction_metrics(customer_id)
        }
```

**2. Data as a Product:**
```yaml
# Data Product Contract
apiVersion: datamesh.io/v1
kind: DataProduct
metadata:
  name: customer-analytics
  domain: customer-experience
spec:
  sla:
    availability: 99.9%
    freshness: "< 1 hour"
    accuracy: "> 99%"
  
  interfaces:
    - type: rest-api
      endpoint: "/api/v1/customers"
    - type: streaming
      topic: "customer-events"
    - type: batch
      location: "s3://data-products/customer-analytics/"
  
  schema:
    version: "1.2.0"
    format: "avro"
    registry: "schema-registry.company.com"
```

**3. Self-Serve Data Infrastructure Platform:**
```python
class DataPlatform:
    """Self-serve data infrastructure platform"""
    
    def create_data_product(self, domain, product_spec):
        """Create infrastructure for new data product"""
        infrastructure = {
            "storage": self.provision_storage(domain, product_spec),
            "compute": self.provision_compute(domain, product_spec),
            "networking": self.setup_networking(domain),
            "monitoring": self.setup_monitoring(domain, product_spec),
            "security": self.apply_security_policies(domain)
        }
        return infrastructure
    
    def provision_storage(self, domain, spec):
        """Provision storage based on requirements"""
        if spec.get("storage_type") == "analytical":
            return self.create_data_lake_bucket(domain)
        elif spec.get("storage_type") == "operational":
            return self.create_database(domain, spec.get("database_type", "postgres"))
    
    def setup_data_pipeline(self, source_domain, target_domain, transformation_logic):
        """Setup automated data pipeline between domains"""
        pipeline = {
            "source": f"{source_domain}-data-product",
            "target": f"{target_domain}-data-product",
            "transformation": transformation_logic,
            "schedule": "hourly",
            "monitoring": True,
            "alerting": True
        }
        return self.deploy_pipeline(pipeline)
```

**4. Federated Computational Governance:**
```python
class FederatedGovernance:
    """Federated governance framework"""
    
    def __init__(self):
        self.global_policies = self.load_global_policies()
        self.domain_policies = {}
    
    def register_domain_policies(self, domain, policies):
        """Register domain-specific policies"""
        # Validate against global policies
        validated_policies = self.validate_policies(policies, self.global_policies)
        self.domain_policies[domain] = validated_policies
    
    def validate_data_product(self, domain, data_product):
        """Validate data product against governance policies"""
        global_compliance = self.check_global_compliance(data_product)
        domain_compliance = self.check_domain_compliance(domain, data_product)
        
        return {
            "compliant": global_compliance and domain_compliance,
            "global_checks": global_compliance,
            "domain_checks": domain_compliance,
            "recommendations": self.get_compliance_recommendations(data_product)
        }
    
    def enforce_interoperability(self, source_product, target_product):
        """Ensure data products can interoperate"""
        schema_compatibility = self.check_schema_compatibility(
            source_product.schema, target_product.schema
        )
        
        sla_compatibility = self.check_sla_compatibility(
            source_product.sla, target_product.sla
        )
        
        return schema_compatibility and sla_compatibility
```

**Comparison with Traditional Architecture:**

| Aspect | Traditional (Centralized) | Data Mesh (Decentralized) |
|--------|---------------------------|---------------------------|
| Ownership | Central data team | Domain teams |
| Data Processing | ETL to central warehouse | Domain-specific processing |
| Governance | Centralized policies | Federated governance |
| Scalability | Vertical scaling | Horizontal scaling |
| Innovation Speed | Bottlenecked by central team | Autonomous domain teams |
| Data Quality | Central responsibility | Domain ownership |

### 8. Explain DataOps and how it applies DevOps principles to data engineering.

**Answer:**
DataOps applies DevOps principles to data analytics, emphasizing collaboration, automation, and continuous improvement in data pipelines.

**Key DataOps Principles:**

**1. Continuous Integration/Continuous Deployment (CI/CD):**
```yaml
# .github/workflows/data-pipeline-ci.yml
name: Data Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  data-quality-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install great-expectations pytest
    
    - name: Run data quality tests
      run: |
        great_expectations checkpoint run data_quality_checkpoint
    
    - name: Run unit tests
      run: pytest tests/unit/ -v
    
    - name: Run integration tests
      run: pytest tests/integration/ -v
      env:
        TEST_DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
    
    - name: Validate pipeline configuration
      run: python scripts/validate_pipeline_config.py

  deploy-to-staging:
    needs: data-quality-tests
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to staging
      run: |
        # Deploy data pipeline to staging environment
        python scripts/deploy_pipeline.py --env staging
        
    - name: Run smoke tests
      run: python scripts/smoke_tests.py --env staging
```

**2. Infrastructure as Code:**
```python
# infrastructure/data_pipeline_infrastructure.py
import pulumi
import pulumi_aws as aws
import pulumi_kubernetes as k8s

class DataPipelineInfrastructure:
    def __init__(self, environment):
        self.environment = environment
        self.setup_storage()
        self.setup_compute()
        self.setup_monitoring()
    
    def setup_storage(self):
        """Setup data storage infrastructure"""
        self.data_bucket = aws.s3.Bucket(
            f"data-pipeline-{self.environment}",
            versioning=aws.s3.BucketVersioningArgs(enabled=True),
            lifecycle_rules=[
                aws.s3.BucketLifecycleRuleArgs(
                    enabled=True,
                    transitions=[
                        aws.s3.BucketLifecycleRuleTransitionArgs(
                            days=30,
                            storage_class="STANDARD_IA"
                        ),
                        aws.s3.BucketLifecycleRuleTransitionArgs(
                            days=90,
                            storage_class="GLACIER"
                        )
                    ]
                )
            ]
        )
    
    def setup_compute(self):
        """Setup compute infrastructure for data processing"""
        self.spark_cluster = k8s.apps.v1.Deployment(
            f"spark-cluster-{self.environment}",
            spec=k8s.apps.v1.DeploymentSpecArgs(
                replicas=3,
                selector=k8s.meta.v1.LabelSelectorArgs(
                    match_labels={"app": f"spark-{self.environment}"}
                ),
                template=k8s.core.v1.PodTemplateSpecArgs(
                    metadata=k8s.meta.v1.ObjectMetaArgs(
                        labels={"app": f"spark-{self.environment}"}
                    ),
                    spec=k8s.core.v1.PodSpecArgs(
                        containers=[
                            k8s.core.v1.ContainerArgs(
                                name="spark-worker",
                                image="bitnami/spark:3.4",
                                resources=k8s.core.v1.ResourceRequirementsArgs(
                                    requests={
                                        "memory": "2Gi",
                                        "cpu": "1"
                                    },
                                    limits={
                                        "memory": "4Gi",
                                        "cpu": "2"
                                    }
                                )
                            )
                        ]
                    )
                )
            )
        )
```

**3. Automated Testing Framework:**
```python
# tests/data_quality_tests.py
import pytest
import pandas as pd
from great_expectations.core import ExpectationSuite
from great_expectations.dataset import PandasDataset

class DataQualityTests:
    def __init__(self):
        self.expectation_suite = ExpectationSuite("data_quality_suite")
    
    def test_data_completeness(self, df: pd.DataFrame):
        """Test data completeness"""
        ge_df = PandasDataset(df)
        
        # Test required columns exist
        result = ge_df.expect_table_columns_to_match_ordered_list([
            'customer_id', 'order_date', 'total_amount', 'status'
        ])
        assert result.success, f"Column structure test failed: {result.result}"
        
        # Test no null values in critical columns
        for column in ['customer_id', 'order_date', 'total_amount']:
            result = ge_df.expect_column_values_to_not_be_null(column)
            assert result.success, f"Null check failed for {column}: {result.result}"
    
    def test_data_validity(self, df: pd.DataFrame):
        """Test data validity"""
        ge_df = PandasDataset(df)
        
        # Test amount is positive
        result = ge_df.expect_column_values_to_be_between(
            'total_amount', min_value=0, max_value=100000
        )
        assert result.success, f"Amount validity test failed: {result.result}"
        
        # Test status values are valid
        result = ge_df.expect_column_values_to_be_in_set(
            'status', ['pending', 'completed', 'cancelled', 'refunded']
        )
        assert result.success, f"Status validity test failed: {result.result}"
    
    def test_data_consistency(self, df: pd.DataFrame):
        """Test data consistency"""
        ge_df = PandasDataset(df)
        
        # Test unique customer IDs
        result = ge_df.expect_column_values_to_be_unique('customer_id')
        assert result.success, f"Uniqueness test failed: {result.result}"
        
        # Test date format consistency
        result = ge_df.expect_column_values_to_match_strftime_format(
            'order_date', '%Y-%m-%d'
        )
        assert result.success, f"Date format test failed: {result.result}"

# Integration test example
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003'],
        'order_date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'total_amount': [100.50, 250.75, 75.25],
        'status': ['completed', 'pending', 'completed']
    })

def test_end_to_end_pipeline(sample_data):
    """Test complete data pipeline"""
    # Test data extraction
    extracted_data = extract_data_from_source()
    assert len(extracted_data) > 0, "No data extracted"
    
    # Test data transformation
    transformed_data = transform_data(extracted_data)
    
    # Run data quality tests
    quality_tests = DataQualityTests()
    quality_tests.test_data_completeness(transformed_data)
    quality_tests.test_data_validity(transformed_data)
    quality_tests.test_data_consistency(transformed_data)
    
    # Test data loading
    load_result = load_data_to_warehouse(transformed_data)
    assert load_result.success, "Data loading failed"
```

**4. Monitoring and Observability:**
```python
# monitoring/data_pipeline_monitoring.py
import logging
import time
from dataclasses import dataclass
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge

@dataclass
class PipelineMetrics:
    """Data pipeline metrics"""
    records_processed = Counter('pipeline_records_processed_total', 'Total records processed')
    processing_duration = Histogram('pipeline_processing_duration_seconds', 'Processing duration')
    data_quality_score = Gauge('pipeline_data_quality_score', 'Data quality score')
    pipeline_errors = Counter('pipeline_errors_total', 'Total pipeline errors')

class DataPipelineMonitor:
    def __init__(self):
        self.metrics = PipelineMetrics()
        self.logger = logging.getLogger(__name__)
    
    def monitor_pipeline_execution(self, pipeline_func):
        """Decorator to monitor pipeline execution"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                # Execute pipeline
                result = pipeline_func(*args, **kwargs)
                
                # Record success metrics
                self.metrics.records_processed.inc(len(result))
                self.metrics.processing_duration.observe(time.time() - start_time)
                
                # Calculate and record data quality score
                quality_score = self.calculate_quality_score(result)
                self.metrics.data_quality_score.set(quality_score)
                
                self.logger.info(f"Pipeline {pipeline_func.__name__} completed successfully")
                return result
                
            except Exception as e:
                # Record error metrics
                self.metrics.pipeline_errors.inc()
                self.logger.error(f"Pipeline {pipeline_func.__name__} failed: {str(e)}")
                
                # Send alert
                self.send_alert(pipeline_func.__name__, str(e))
                raise
        
        return wrapper
    
    def calculate_quality_score(self, data) -> float:
        """Calculate data quality score"""
        if not data:
            return 0.0
        
        # Implement quality scoring logic
        completeness_score = self.check_completeness(data)
        validity_score = self.check_validity(data)
        consistency_score = self.check_consistency(data)
        
        return (completeness_score + validity_score + consistency_score) / 3
    
    def send_alert(self, pipeline_name: str, error_message: str):
        """Send alert for pipeline failures"""
        alert_payload = {
            "pipeline": pipeline_name,
            "error": error_message,
            "timestamp": time.time(),
            "severity": "high"
        }
        
        # Send to alerting system (Slack, PagerDuty, etc.)
        self.logger.critical(f"ALERT: {alert_payload}")
```

---

## Advanced Level Questions

### 9. Design a modern data architecture for a multi-cloud environment.
**Answer:**
**Architecture Components:**

```python
class MultiCloudDataArchitecture:
    def __init__(self):
        self.cloud_providers = {
            'aws': self.setup_aws_services(),
            'azure': self.setup_azure_services(),
            'gcp': self.setup_gcp_services()
        }
        self.data_fabric = self.setup_data_fabric()
    
    def setup_aws_services(self):
        return {
            'storage': 'S3',
            'compute': 'EMR/Glue',
            'warehouse': 'Redshift',
            'streaming': 'Kinesis',
            'ml': 'SageMaker'
        }
    
    def setup_data_fabric(self):
        """Unified data management layer"""
        return {
            'catalog': 'Apache Atlas',
            'governance': 'Collibra',
            'lineage': 'DataHub',
            'quality': 'Great Expectations',
            'security': 'Apache Ranger'
        }
```

**Key Considerations:**
- **Data Sovereignty**: Comply with regional regulations
- **Vendor Lock-in**: Avoid dependency on single provider
- **Cost Optimization**: Leverage best pricing across clouds
- **Disaster Recovery**: Cross-cloud backup strategies
- **Network Connectivity**: Secure inter-cloud communication

### 10. Explain event-driven architecture in data systems.
**Answer:**
**Core Concepts:**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import json

class Event:
    def __init__(self, event_type: str, data: Dict[Any, Any], metadata: Dict[str, Any] = None):
        self.event_type = event_type
        self.data = data
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()
        self.event_id = str(uuid.uuid4())

class EventHandler(ABC):
    @abstractmethod
    def handle(self, event: Event) -> None:
        pass

class CustomerEventHandler(EventHandler):
    def handle(self, event: Event) -> None:
        if event.event_type == 'customer_created':
            self.create_customer_profile(event.data)
        elif event.event_type == 'customer_updated':
            self.update_customer_profile(event.data)

class EventBus:
    def __init__(self):
        self.handlers = {}
    
    def subscribe(self, event_type: str, handler: EventHandler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def publish(self, event: Event):
        if event.event_type in self.handlers:
            for handler in self.handlers[event.event_type]:
                handler.handle(event)
```

**Benefits:**
- **Loose Coupling**: Services communicate through events
- **Scalability**: Independent scaling of components
- **Resilience**: Failure isolation
- **Real-time Processing**: Immediate response to changes

---

## Scenario-Based Questions

### 11. Design a data architecture for real-time fraud detection.
**Answer:**
**Architecture Overview:**

```
Transaction Stream → Kafka → Stream Processor → ML Model → Alert System
                           ↓
                    Feature Store ← Historical Data
```

**Implementation:**
```python
class FraudDetectionArchitecture:
    def __init__(self):
        self.setup_streaming_layer()
        self.setup_feature_store()
        self.setup_ml_pipeline()
        self.setup_alerting()
    
    def setup_streaming_layer(self):
        """Real-time transaction processing"""
        return {
            'ingestion': 'Apache Kafka',
            'processing': 'Apache Flink',
            'windowing': '5-minute tumbling windows',
            'state_management': 'RocksDB'
        }
    
    def process_transaction(self, transaction):
        """Process incoming transaction"""
        # Extract features
        features = self.extract_features(transaction)
        
        # Get historical features
        historical_features = self.feature_store.get_features(
            transaction['customer_id']
        )
        
        # Combine features
        combined_features = {**features, **historical_features}
        
        # Score transaction
        fraud_score = self.ml_model.predict(combined_features)
        
        # Take action based on score
        if fraud_score > 0.8:
            self.block_transaction(transaction)
            self.send_alert(transaction, fraud_score)
        elif fraud_score > 0.5:
            self.flag_for_review(transaction, fraud_score)
        
        return fraud_score
```

**Key Components:**
- **Stream Processing**: Sub-second latency
- **Feature Engineering**: Real-time and batch features
- **Model Serving**: Low-latency ML inference
- **Feedback Loop**: Continuous model improvement

### 12. How would you handle data architecture for GDPR compliance?
**Answer:**
**GDPR Requirements:**
- **Right to be Forgotten**: Data deletion capabilities
- **Data Portability**: Export user data
- **Consent Management**: Track consent status
- **Data Minimization**: Collect only necessary data
- **Privacy by Design**: Built-in privacy protection

**Architecture Implementation:**
```python
class GDPRCompliantArchitecture:
    def __init__(self):
        self.consent_service = ConsentManagementService()
        self.data_catalog = DataCatalogService()
        self.encryption_service = EncryptionService()
        self.audit_service = AuditService()
    
    def collect_data(self, user_id, data, purpose):
        """Collect data with consent validation"""
        # Check consent
        if not self.consent_service.has_consent(user_id, purpose):
            raise ConsentError(f"No consent for {purpose}")
        
        # Classify data
        classification = self.classify_data(data)
        
        # Apply appropriate protection
        if classification == 'PII':
            data = self.encryption_service.encrypt(data)
        
        # Store with metadata
        self.store_data(user_id, data, {
            'purpose': purpose,
            'classification': classification,
            'retention_period': self.get_retention_period(purpose),
            'collected_at': datetime.utcnow()
        })
        
        # Log for audit
        self.audit_service.log_data_collection(user_id, purpose)
    
    def handle_deletion_request(self, user_id):
        """Handle right to be forgotten request"""
        # Find all data for user
        user_data_locations = self.data_catalog.find_user_data(user_id)
        
        # Delete from all systems
        for location in user_data_locations:
            self.delete_user_data(location, user_id)
        
        # Verify deletion
        remaining_data = self.data_catalog.find_user_data(user_id)
        if remaining_data:
            raise DeletionError(f"Data still exists: {remaining_data}")
        
        # Log deletion
        self.audit_service.log_data_deletion(user_id)
```

### 13. Design a data architecture for IoT sensor data processing.
**Answer:**
**Architecture Layers:**

```python
class IoTDataArchitecture:
    def __init__(self):
        self.edge_layer = self.setup_edge_processing()
        self.ingestion_layer = self.setup_data_ingestion()
        self.processing_layer = self.setup_stream_processing()
        self.storage_layer = self.setup_data_storage()
        self.analytics_layer = self.setup_analytics()
    
    def setup_edge_processing(self):
        """Edge computing for immediate processing"""
        return {
            'devices': 'IoT sensors with edge computing',
            'preprocessing': 'Data filtering and aggregation',
            'local_storage': 'Time-series database (InfluxDB)',
            'connectivity': 'MQTT/CoAP protocols'
        }
    
    def setup_data_ingestion(self):
        """Scalable data ingestion"""
        return {
            'message_queue': 'Apache Kafka',
            'schema_registry': 'Confluent Schema Registry',
            'data_formats': 'Avro/Protobuf',
            'partitioning': 'By device_id and timestamp'
        }
    
    def process_sensor_data(self, sensor_data):
        """Process incoming sensor data"""
        # Validate data quality
        if not self.validate_sensor_data(sensor_data):
            self.handle_invalid_data(sensor_data)
            return
        
        # Detect anomalies
        anomaly_score = self.detect_anomalies(sensor_data)
        
        # Real-time aggregations
        aggregated_data = self.aggregate_data(sensor_data)
        
        # Store in appropriate storage
        self.store_raw_data(sensor_data)  # For detailed analysis
        self.store_aggregated_data(aggregated_data)  # For dashboards
        
        # Trigger alerts if needed
        if anomaly_score > threshold:
            self.trigger_alert(sensor_data, anomaly_score)
```

**Storage Strategy:**
- **Hot Data**: Recent data in fast storage (Redis/MemSQL)
- **Warm Data**: Last 30 days in columnar storage (Parquet)
- **Cold Data**: Historical data in object storage (S3/Glacier)

---

## Performance & Optimization

### 14. How do you optimize data architecture for performance?
**Answer:**
**Optimization Strategies:**

**1. Data Partitioning:**
```sql
-- Time-based partitioning
CREATE TABLE sensor_data (
    sensor_id VARCHAR(50),
    timestamp TIMESTAMP,
    value DECIMAL(10,4),
    location VARCHAR(100)
) PARTITION BY RANGE (timestamp) (
    PARTITION p2024_01 VALUES LESS THAN ('2024-02-01'),
    PARTITION p2024_02 VALUES LESS THAN ('2024-03-01'),
    PARTITION p2024_03 VALUES LESS THAN ('2024-04-01')
);

-- Hash partitioning for even distribution
CREATE TABLE user_events (
    user_id BIGINT,
    event_type VARCHAR(50),
    event_data JSON,
    created_at TIMESTAMP
) PARTITION BY HASH(user_id) PARTITIONS 16;
```

**2. Indexing Strategy:**
```sql
-- Composite index for common query patterns
CREATE INDEX idx_sensor_time_location 
ON sensor_data (sensor_id, timestamp, location);

-- Partial index for specific conditions
CREATE INDEX idx_high_value_sensors 
ON sensor_data (sensor_id, timestamp) 
WHERE value > 100;
```

**3. Caching Layer:**
```python
class DataCacheManager:
    def __init__(self):
        self.redis_client = redis.Redis()
        self.cache_ttl = 3600  # 1 hour
    
    def get_cached_data(self, cache_key):
        """Get data from cache"""
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        return None
    
    def cache_data(self, cache_key, data):
        """Cache data with TTL"""
        self.redis_client.setex(
            cache_key, 
            self.cache_ttl, 
            json.dumps(data)
        )
    
    def get_aggregated_metrics(self, metric_type, time_range):
        """Get metrics with caching"""
        cache_key = f"metrics:{metric_type}:{time_range}"
        
        # Try cache first
        cached_result = self.get_cached_data(cache_key)
        if cached_result:
            return cached_result
        
        # Calculate and cache
        result = self.calculate_metrics(metric_type, time_range)
        self.cache_data(cache_key, result)
        
        return result
```

### 15. Explain data compression strategies in data architecture.
**Answer:**
**Compression Techniques:**

**1. Columnar Compression:**
```python
# Parquet with different compression algorithms
import pandas as pd

# Different compression options
compression_options = {
    'snappy': 'Fast compression/decompression',
    'gzip': 'Better compression ratio',
    'lz4': 'Balanced speed and compression',
    'brotli': 'Best compression for cold data'
}

# Save with optimal compression
df.to_parquet(
    'data.parquet',
    compression='snappy',  # For hot data
    engine='pyarrow'
)

# For cold storage
df.to_parquet(
    'archive_data.parquet',
    compression='brotli',  # Maximum compression
    engine='pyarrow'
)
```

**2. Dictionary Encoding:**
```sql
-- Automatic dictionary encoding in columnar databases
CREATE TABLE products (
    product_id BIGINT,
    category VARCHAR(50) ENCODING DICT,  -- Dictionary encoded
    brand VARCHAR(50) ENCODING DICT,
    price DECIMAL(8,2)
);
```

**3. Delta Compression:**
```python
class DeltaCompression:
    def compress_timestamps(self, timestamps):
        """Delta compress timestamp series"""
        if not timestamps:
            return []
        
        compressed = [timestamps[0]]  # Store first value
        
        for i in range(1, len(timestamps)):
            delta = timestamps[i] - timestamps[i-1]
            compressed.append(delta)
        
        return compressed
    
    def decompress_timestamps(self, compressed):
        """Decompress delta-compressed timestamps"""
        if not compressed:
            return []
        
        decompressed = [compressed[0]]
        
        for i in range(1, len(compressed)):
            value = decompressed[i-1] + compressed[i]
            decompressed.append(value)
        
        return decompressed
```

---

## Modern Data Architecture Patterns

### 16. Explain the Lambda vs Kappa architecture patterns.
**Answer:**

**Lambda Architecture:**
```python
class LambdaArchitecture:
    def __init__(self):
        self.batch_layer = BatchLayer()
        self.speed_layer = SpeedLayer()
        self.serving_layer = ServingLayer()
    
    def process_data(self, data_stream):
        """Process data through both layers"""
        # Batch layer - high latency, high throughput
        self.batch_layer.process(data_stream)
        
        # Speed layer - low latency, approximate results
        self.speed_layer.process(data_stream)
        
        # Serving layer - merge results
        batch_results = self.batch_layer.get_results()
        speed_results = self.speed_layer.get_results()
        
        return self.serving_layer.merge_views(batch_results, speed_results)
```

**Kappa Architecture:**
```python
class KappaArchitecture:
    def __init__(self):
        self.stream_processor = StreamProcessor()
        self.storage = StreamStorage()
    
    def process_data(self, data_stream):
        """Single stream processing path"""
        # All processing through stream processor
        processed_data = self.stream_processor.process(data_stream)
        
        # Store in stream-friendly storage
        self.storage.store(processed_data)
        
        return processed_data
    
    def reprocess_historical_data(self, start_time, end_time):
        """Reprocess historical data using same stream logic"""
        historical_stream = self.storage.replay(start_time, end_time)
        return self.stream_processor.process(historical_stream)
```

**Comparison:**
| Aspect | Lambda | Kappa |
|--------|--------|-------|
| Complexity | High (two codebases) | Low (single codebase) |
| Latency | Mixed (batch + real-time) | Consistent (stream-only) |
| Accuracy | High (batch correction) | Depends on stream processing |
| Maintenance | Complex | Simpler |

### 17. Design a data architecture for machine learning operations (MLOps).
**Answer:**

```python
class MLOpsDataArchitecture:
    def __init__(self):
        self.feature_store = FeatureStore()
        self.model_registry = ModelRegistry()
        self.experiment_tracking = ExperimentTracker()
        self.monitoring = ModelMonitoring()
    
    def setup_feature_pipeline(self):
        """Setup feature engineering pipeline"""
        return {
            'raw_data': 'Data lake (S3/ADLS)',
            'feature_engineering': 'Spark/Databricks',
            'feature_store': 'Feast/Tecton',
            'feature_serving': 'Redis/DynamoDB'
        }
    
    def train_model(self, experiment_config):
        """Model training with tracking"""
        # Start experiment
        experiment = self.experiment_tracking.start_experiment(
            experiment_config['name']
        )
        
        # Get features
        features = self.feature_store.get_training_data(
            experiment_config['feature_set'],
            experiment_config['time_range']
        )
        
        # Train model
        model = self.train_ml_model(features, experiment_config)
        
        # Log metrics and artifacts
        experiment.log_metrics(model.metrics)
        experiment.log_artifacts(model.artifacts)
        
        # Register model
        model_version = self.model_registry.register_model(
            model, experiment_config['model_name']
        )
        
        return model_version
    
    def deploy_model(self, model_version, deployment_config):
        """Deploy model with monitoring"""
        # Deploy model
        endpoint = self.deploy_to_endpoint(model_version, deployment_config)
        
        # Setup monitoring
        self.monitoring.setup_model_monitoring(
            endpoint, model_version, {
                'data_drift': True,
                'model_performance': True,
                'prediction_distribution': True
            }
        )
        
        return endpoint
```

**Key Components:**
- **Feature Store**: Centralized feature management
- **Model Registry**: Version control for models
- **Experiment Tracking**: ML experiment management
- **Model Monitoring**: Production model health
- **A/B Testing**: Model performance comparison

This comprehensive approach to DataOps ensures reliable, scalable, and maintainable data pipelines through automation, testing, and continuous monitoring.