# Data Architecture Key Concepts for Data Engineering

## 1. Data Modeling Fundamentals
**What it is**: The process of creating a conceptual representation of data objects, their relationships, and the rules that govern them.

**Why important**: Data modeling is the foundation of any data system. It determines how data is stored, accessed, and maintained. Good data models ensure data integrity, performance, and scalability while supporting business requirements.

**When to use**: 
- Designing new data systems
- Migrating legacy systems
- Optimizing existing data structures
- Ensuring data consistency across systems

**Conceptual Data Modeling**:
```sql
-- Entity-Relationship concepts
-- Entities: Customer, Order, Product
-- Relationships: Customer places Order, Order contains Product
-- Attributes: Customer has name, email; Order has date, total

-- Example conceptual model
ENTITY Customer {
    customer_id (Primary Key)
    first_name
    last_name
    email
    registration_date
}

ENTITY Order {
    order_id (Primary Key)
    customer_id (Foreign Key)
    order_date
    total_amount
    status
}

RELATIONSHIP Customer_Order {
    One Customer can have Many Orders
    One Order belongs to One Customer
}
```

**Logical Data Modeling**:
```sql
-- Normalized logical model (3NF)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    registration_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit_price DECIMAL(8,2) NOT NULL
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL
);
```

**Physical Data Modeling**:
```sql
-- Physical implementation with indexes and partitioning
CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (order_date);

-- Create partitions for performance
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

-- Indexes for performance
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);
```

## 2. Dimensional Modeling
**What it is**: A data modeling technique optimized for data warehousing and analytics, organizing data into facts and dimensions.

**Why important**: Dimensional modeling provides intuitive, high-performance structures for analytical queries. It enables business users to easily understand and query data while maintaining good performance for complex analytical workloads.

**When to use**:
- Building data warehouses
- Creating data marts for specific business areas
- Designing OLAP systems
- Supporting business intelligence and reporting

**Star Schema Design**:
```sql
-- Fact table (center of star)
CREATE TABLE fact_sales (
    sale_id BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(8,2) DEFAULT 0,
    tax_amount DECIMAL(8,2) NOT NULL
);

-- Dimension tables (points of star)
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week VARCHAR(10),
    day_of_month INTEGER,
    month_name VARCHAR(10),
    month_number INTEGER,
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    age_group VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    customer_segment VARCHAR(30)
);

CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(100),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    brand VARCHAR(50),
    unit_cost DECIMAL(8,2),
    unit_price DECIMAL(8,2)
);
```

**Slowly Changing Dimensions (SCD)**:
```sql
-- Type 2 SCD: Track historical changes
CREATE TABLE dim_customer_scd2 (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    version_number INTEGER DEFAULT 1
);

-- Example of SCD Type 2 update process
INSERT INTO dim_customer_scd2 (
    customer_id, first_name, last_name, email, city, state,
    effective_date, expiration_date, is_current, version_number
)
SELECT 
    customer_id, first_name, last_name, email, 'New City', state,
    CURRENT_DATE, NULL, TRUE, version_number + 1
FROM dim_customer_scd2 
WHERE customer_id = 'CUST001' AND is_current = TRUE;

-- Expire old record
UPDATE dim_customer_scd2 
SET expiration_date = CURRENT_DATE - 1, is_current = FALSE
WHERE customer_id = 'CUST001' AND is_current = TRUE 
AND customer_key != (SELECT MAX(customer_key) FROM dim_customer_scd2 WHERE customer_id = 'CUST001');
```

## 3. Data Vault 2.0 Methodology
**What it is**: A data modeling methodology designed for enterprise data warehouses that provides flexibility, scalability, and auditability.

**Why important**: Data Vault 2.0 addresses the challenges of traditional data warehousing by providing a methodology that can adapt to changing business requirements while maintaining data lineage and historical accuracy.

**When to use**:
- Enterprise data warehouses with complex source systems
- Environments with frequently changing business requirements
- Systems requiring detailed audit trails
- Agile data warehouse development

**Core Components**:
```sql
-- Hub: Unique business keys
CREATE TABLE hub_customer (
    customer_hk CHAR(32) PRIMARY KEY,  -- Hash key
    customer_id VARCHAR(50) NOT NULL,  -- Business key
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Satellite: Descriptive attributes
CREATE TABLE sat_customer_details (
    customer_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    birth_date DATE,
    hash_diff CHAR(32) NOT NULL,  -- Hash of all attributes
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_hk, load_date),
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk)
);

-- Link: Relationships between hubs
CREATE TABLE link_customer_order (
    customer_order_hk CHAR(32) PRIMARY KEY,
    customer_hk CHAR(32) NOT NULL,
    order_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk),
    FOREIGN KEY (order_hk) REFERENCES hub_order(order_hk)
);

-- Hash key generation example
CREATE OR REPLACE FUNCTION generate_hash_key(input_text TEXT)
RETURNS CHAR(32) AS $$
BEGIN
    RETURN UPPER(MD5(UPPER(TRIM(input_text))));
END;
$$ LANGUAGE plpgsql;
```

**Data Vault Loading Pattern**:
```python
import hashlib
import pandas as pd
from datetime import datetime

def generate_hash_key(*args):
    """Generate hash key from business key components."""
    concatenated = '||'.join(str(arg).upper().strip() for arg in args)
    return hashlib.md5(concatenated.encode()).hexdigest().upper()

def load_hub_customer(df, record_source):
    """Load customer hub table."""
    df['customer_hk'] = df['customer_id'].apply(generate_hash_key)
    df['load_date'] = datetime.now()
    df['record_source'] = record_source
    
    # Select only new business keys
    hub_df = df[['customer_hk', 'customer_id', 'load_date', 'record_source']].drop_duplicates()
    
    return hub_df

def load_sat_customer_details(df, record_source):
    """Load customer satellite table."""
    df['customer_hk'] = df['customer_id'].apply(generate_hash_key)
    df['load_date'] = datetime.now()
    df['record_source'] = record_source
    
    # Generate hash diff for change detection
    attribute_cols = ['first_name', 'last_name', 'email', 'phone', 'birth_date']
    df['hash_diff'] = df[attribute_cols].apply(
        lambda row: generate_hash_key(*row.values), axis=1
    )
    
    sat_df = df[['customer_hk', 'load_date', 'first_name', 'last_name', 
                 'email', 'phone', 'birth_date', 'hash_diff', 'record_source']]
    
    return sat_df
```

## 4. Data Mesh Architecture
**What it is**: A decentralized data architecture that treats data as a product, with domain-oriented ownership and self-serve data infrastructure.

**Why important**: Data Mesh addresses the scalability and organizational challenges of centralized data platforms by distributing data ownership to domain teams while maintaining interoperability and governance.

**When to use**:
- Large organizations with multiple business domains
- Companies struggling with centralized data team bottlenecks
- Organizations wanting to scale data capabilities across teams
- Environments requiring domain expertise for data products

**Core Principles**:
```yaml
# Data Mesh Principles Configuration
data_mesh_principles:
  domain_ownership:
    description: "Domain teams own their data products"
    implementation:
      - domain_data_teams
      - business_logic_ownership
      - end_to_end_responsibility
  
  data_as_product:
    description: "Treat data with product thinking"
    characteristics:
      - discoverable
      - addressable
      - understandable
      - trustworthy
      - secure
      - interoperable
  
  self_serve_platform:
    description: "Infrastructure as a platform"
    capabilities:
      - data_pipeline_creation
      - data_product_deployment
      - monitoring_observability
      - data_governance_tools
  
  federated_governance:
    description: "Decentralized governance with global standards"
    components:
      - global_policies
      - domain_specific_rules
      - automated_compliance
```

**Data Product Implementation**:
```python
class DataProduct:
    def __init__(self, domain, name, version):
        self.domain = domain
        self.name = name
        self.version = version
        self.metadata = self._load_metadata()
    
    def _load_metadata(self):
        return {
            'schema': self._get_schema(),
            'sla': self._get_sla(),
            'quality_metrics': self._get_quality_metrics(),
            'lineage': self._get_lineage(),
            'access_policies': self._get_access_policies()
        }
    
    def _get_schema(self):
        return {
            'format': 'parquet',
            'fields': [
                {'name': 'customer_id', 'type': 'string', 'required': True},
                {'name': 'order_date', 'type': 'timestamp', 'required': True},
                {'name': 'total_amount', 'type': 'decimal', 'required': True}
            ]
        }
    
    def _get_sla(self):
        return {
            'freshness': '1 hour',
            'availability': '99.9%',
            'completeness': '95%',
            'accuracy': '99%'
        }
    
    def publish(self, data_platform):
        """Publish data product to the mesh."""
        data_platform.register_product(self)
        data_platform.deploy_pipeline(self)
        data_platform.setup_monitoring(self)
```

## 5. DataOps Methodology
**What it is**: A methodology that applies DevOps principles to data analytics, emphasizing collaboration, automation, and continuous improvement.

**Why important**: DataOps improves the speed, quality, and reliability of data analytics by implementing automated testing, continuous integration, and monitoring throughout the data lifecycle.

**When to use**:
- Organizations with complex data pipelines
- Teams needing faster time-to-market for analytics
- Environments requiring high data quality and reliability
- Companies wanting to scale data operations

**DataOps Pipeline**:
```yaml
# DataOps CI/CD Pipeline Configuration
name: dataops-pipeline

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
      - name: Run Data Quality Tests
        run: |
          python -m pytest tests/data_quality/
          python -m great_expectations checkpoint run data_quality_checkpoint
  
  schema-validation:
    runs-on: ubuntu-latest
    steps:
      - name: Validate Schema Changes
        run: |
          python scripts/validate_schema_evolution.py
          python scripts/check_backward_compatibility.py
  
  deploy-to-staging:
    needs: [data-quality-tests, schema-validation]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        run: |
          terraform apply -var-file=staging.tfvars
          python scripts/run_integration_tests.py
  
  deploy-to-production:
    needs: deploy-to-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: |
          terraform apply -var-file=production.tfvars
          python scripts/smoke_tests.py
```

**Data Quality Testing**:
```python
import great_expectations as ge
import pandas as pd
from datetime import datetime, timedelta

class DataQualityValidator:
    def __init__(self, data_context_path):
        self.context = ge.get_context(context_root_dir=data_context_path)
    
    def validate_customer_data(self, df):
        """Validate customer data quality."""
        suite_name = "customer_data_quality_suite"
        
        # Create expectation suite
        suite = self.context.create_expectation_suite(
            expectation_suite_name=suite_name,
            overwrite_existing=True
        )
        
        # Define expectations
        validator = self.context.get_validator(
            batch_request=self._create_batch_request(df),
            expectation_suite_name=suite_name
        )
        
        # Data quality expectations
        validator.expect_column_to_exist("customer_id")
        validator.expect_column_values_to_not_be_null("customer_id")
        validator.expect_column_values_to_be_unique("customer_id")
        validator.expect_column_values_to_match_regex(
            "email", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
        validator.expect_column_values_to_be_between(
            "age", min_value=0, max_value=120
        )
        
        # Run validation
        results = validator.validate()
        return results
    
    def _create_batch_request(self, df):
        return {
            "datasource_name": "pandas_datasource",
            "data_connector_name": "default_runtime_data_connector_name",
            "data_asset_name": "customer_data",
            "runtime_parameters": {"batch_data": df},
            "batch_identifiers": {"default_identifier_name": "default_identifier"}
        }
```

## 6. Lambda Architecture
**What it is**: A data processing architecture that handles both batch and real-time data processing to provide comprehensive and accurate views.

**Why important**: Lambda architecture enables organizations to process both historical batch data and real-time streaming data, providing both accuracy (batch layer) and low latency (speed layer).

**When to use**:
- Systems requiring both batch and real-time processing
- Applications needing low-latency responses with eventual consistency
- Environments with high-volume data streams
- Use cases requiring reprocessing of historical data

**Architecture Components**:
```python
# Lambda Architecture Implementation
class LambdaArchitecture:
    def __init__(self):
        self.batch_layer = BatchLayer()
        self.speed_layer = SpeedLayer()
        self.serving_layer = ServingLayer()
    
    def process_data(self, data_stream):
        """Process data through both batch and speed layers."""
        # Batch layer processes all data
        self.batch_layer.append_data(data_stream)
        
        # Speed layer processes real-time data
        self.speed_layer.process_stream(data_stream)
        
        # Serving layer merges results
        return self.serving_layer.query()

class BatchLayer:
    def __init__(self):
        self.master_dataset = []
    
    def append_data(self, data):
        """Append data to master dataset (immutable)."""
        self.master_dataset.extend(data)
    
    def compute_batch_views(self):
        """Compute batch views from master dataset."""
        # Example: Compute daily aggregations
        batch_views = {}
        for record in self.master_dataset:
            date = record['timestamp'].date()
            if date not in batch_views:
                batch_views[date] = {'count': 0, 'sum': 0}
            batch_views[date]['count'] += 1
            batch_views[date]['sum'] += record['value']
        return batch_views

class SpeedLayer:
    def __init__(self):
        self.real_time_views = {}
    
    def process_stream(self, data_stream):
        """Process real-time data stream."""
        for record in data_stream:
            self._update_real_time_view(record)
    
    def _update_real_time_view(self, record):
        """Update real-time views incrementally."""
        key = record['key']
        if key not in self.real_time_views:
            self.real_time_views[key] = {'count': 0, 'sum': 0}
        self.real_time_views[key]['count'] += 1
        self.real_time_views[key]['sum'] += record['value']

class ServingLayer:
    def __init__(self, batch_layer, speed_layer):
        self.batch_layer = batch_layer
        self.speed_layer = speed_layer
    
    def query(self, key):
        """Query combining batch and speed layer results."""
        batch_result = self.batch_layer.get_view(key)
        speed_result = self.speed_layer.get_view(key)
        
        # Merge results (speed layer overwrites batch for recent data)
        return self._merge_views(batch_result, speed_result)
```

## 7. Kappa Architecture
**What it is**: A simplified streaming architecture that processes all data as streams, eliminating the complexity of separate batch and speed layers.

**Why important**: Kappa architecture reduces complexity by using a single stream processing engine for both real-time and batch processing, making it easier to maintain and reason about.

**When to use**:
- Stream-first organizations
- Systems where reprocessing can be done via stream replay
- Applications requiring consistent processing logic
- Environments with strong stream processing capabilities

**Implementation Example**:
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class KappaArchitecture:
    def __init__(self, pipeline_options):
        self.pipeline_options = pipeline_options
    
    def create_pipeline(self):
        """Create unified stream processing pipeline."""
        with beam.Pipeline(options=self.pipeline_options) as pipeline:
            # Read from stream (can replay for batch processing)
            events = (
                pipeline
                | 'Read from Kafka' >> beam.io.ReadFromKafka(
                    consumer_config={'bootstrap.servers': 'localhost:9092'},
                    topics=['user_events']
                )
                | 'Parse JSON' >> beam.Map(self._parse_json)
            )
            
            # Real-time aggregations
            real_time_metrics = (
                events
                | 'Window into fixed intervals' >> beam.WindowInto(
                    beam.window.FixedWindows(60)  # 1-minute windows
                )
                | 'Group by key' >> beam.GroupByKey()
                | 'Compute metrics' >> beam.Map(self._compute_metrics)
                | 'Write to real-time store' >> beam.io.WriteToBigQuery(
                    table='project:dataset.real_time_metrics'
                )
            )
            
            # Historical aggregations (same logic, different window)
            historical_metrics = (
                events
                | 'Window into daily intervals' >> beam.WindowInto(
                    beam.window.FixedWindows(24 * 60 * 60)  # Daily windows
                )
                | 'Group by key daily' >> beam.GroupByKey()
                | 'Compute daily metrics' >> beam.Map(self._compute_metrics)
                | 'Write to historical store' >> beam.io.WriteToBigQuery(
                    table='project:dataset.historical_metrics'
                )
            )
    
    def _parse_json(self, kafka_message):
        import json
        return json.loads(kafka_message.value.decode('utf-8'))
    
    def _compute_metrics(self, grouped_data):
        key, values = grouped_data
        return {
            'key': key,
            'count': len(values),
            'sum': sum(v['amount'] for v in values),
            'avg': sum(v['amount'] for v in values) / len(values)
        }
```

These key concepts form the foundation of modern data architecture, enabling organizations to build scalable, maintainable, and efficient data systems that can adapt to changing business requirements while ensuring data quality and governance.tribute_cols = ['first_name', 'last_name', 'email', 'phone', 'birth_date']
    df['hash_diff'] = df[attribute_cols].apply(
        lambda row: generate_hash_key(*row.values), axis=1
    )
    
    return df[['customer_hk', 'load_date'] + attribute_cols + ['hash_diff', 'record_source']]
```

## 4. Data Mesh Architecture
**What it is**: A decentralized data architecture that treats data as a product, with domain-oriented ownership and self-serve data infrastructure.

**Why important**: Data Mesh addresses the scalability and organizational challenges of centralized data platforms by distributing data ownership to domain teams while maintaining interoperability and governance.

**When to use**:
- Large organizations with multiple business domains
- Companies struggling with centralized data team bottlenecks
- Organizations wanting to scale data capabilities
- Environments requiring domain expertise in data products

**Core Principles Implementation**:
```yaml
# Data Product Specification
apiVersion: datamesh.io/v1
kind: DataProduct
metadata:
  name: customer-analytics
  domain: customer-experience
  owner: customer-experience-team
spec:
  description: "Customer behavior and analytics data product"
  
  # Domain Ownership
  domain:
    name: customer-experience
    team: customer-experience-team
    contact: team-lead@company.com
  
  # Data as a Product
  product:
    sla:
      availability: 99.9%
      freshness: "< 1 hour"
      accuracy: "> 99%"
    
    # Self-serve Infrastructure
    infrastructure:
      compute: kubernetes
      storage: s3
      processing: spark
      serving: api-gateway
    
    # Federated Governance
    governance:
      classification: internal
      retention: 7-years
      privacy: pii-compliant
      quality:
        - completeness > 95%
        - uniqueness > 99%
        - validity > 98%
```

**Data Product Implementation**:
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataProductMetadata:
    name: str
    version: str
    domain: str
    owner: str
    description: str
    sla: Dict[str, Any]
    schema_version: str

class DataProduct(ABC):
    """Abstract base class for data products."""
    
    def __init__(self, metadata: DataProductMetadata):
        self.metadata = metadata
        self._quality_metrics = {}
    
    @abstractmethod
    def extract(self) -> Any:
        """Extract data from source systems."""
        pass
    
    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Transform data according to business rules."""
        pass
    
    @abstractmethod
    def serve(self, data: Any) -> Any:
        """Serve data through defined interfaces."""
        pass
    
    def validate_quality(self, data: Any) -> Dict[str, float]:
        """Validate data quality against SLA."""
        # Implement quality checks
        return self._quality_metrics
    
    def get_lineage(self) -> Dict[str, Any]:
        """Return data lineage information."""
        return {
            'source_systems': self._get_source_systems(),
            'transformations': self._get_transformations(),
            'dependencies': self._get_dependencies()
        }

class CustomerAnalyticsProduct(DataProduct):
    """Customer analytics data product implementation."""
    
    def extract(self) -> pd.DataFrame:
        # Extract from multiple sources
        crm_data = self._extract_from_crm()
        web_data = self._extract_from_web_analytics()
        transaction_data = self._extract_from_transactions()
        
        return self._combine_sources(crm_data, web_data, transaction_data)
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        # Apply business transformations
        data = self._calculate_customer_metrics(data)
        data = self._apply_segmentation(data)
        data = self._enrich_with_external_data(data)
        
        return data
    
    def serve(self, data: pd.DataFrame) -> Dict[str, Any]:
        # Serve through multiple interfaces
        return {
            'api_endpoint': self._create_api_endpoint(data),
            'data_lake_location': self._store_in_data_lake(data),
            'streaming_topic': self._publish_to_stream(data)
        }
```

## 5. DataOps Practices
**What it is**: A methodology that applies DevOps principles to data analytics, emphasizing collaboration, automation, and continuous improvement in data pipelines.

**Why important**: DataOps improves the speed, quality, and reliability of data analytics by implementing automated testing, continuous integration, and monitoring for data pipelines.

**When to use**:
- Managing complex data pipelines
- Teams requiring rapid iteration on data products
- Organizations needing reliable data delivery
- Environments with multiple data stakeholders

**Pipeline as Code**:
```python
# data_pipeline.py
from dataclasses import dataclass
from typing import List, Dict, Any
import yaml

@dataclass
class PipelineConfig:
    name: str
    version: str
    schedule: str
    dependencies: List[str]
    parameters: Dict[str, Any]
    
    @classmethod
    def from_yaml(cls, yaml_file: str):
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
        return cls(**config)

class DataPipeline:
    """DataOps-enabled data pipeline."""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.metrics = {}
        self.tests = []
    
    def add_data_test(self, test_func, description: str):
        """Add data quality test."""
        self.tests.append({
            'function': test_func,
            'description': description
        })
    
    def run_tests(self, data: Any) -> Dict[str, bool]:
        """Run all data quality tests."""
        results = {}
        for test in self.tests:
            try:
                result = test['function'](data)
                results[test['description']] = result
            except Exception as e:
                results[test['description']] = False
                self._log_error(f"Test failed: {test['description']}, Error: {e}")
        
        return results
    
    def execute(self):
        """Execute pipeline with DataOps practices."""
        try:
            # Pre-execution validation
            self._validate_dependencies()
            
            # Extract data
            data = self._extract()
            
            # Run data quality tests
            test_results = self.run_tests(data)
            if not all(test_results.values()):
                raise Exception(f"Data quality tests failed: {test_results}")
            
            # Transform data
            transformed_data = self._transform(data)
            
            # Post-transformation tests
            post_test_results = self.run_tests(transformed_data)
            if not all(post_test_results.values()):
                raise Exception(f"Post-transformation tests failed: {post_test_results}")
            
            # Load data
            self._load(transformed_data)
            
            # Record metrics
            self._record_metrics()
            
        except Exception as e:
            self._handle_failure(e)
            raise
```

**CI/CD for Data Pipelines**:
```yaml
# .github/workflows/data-pipeline-ci.yml
name: Data Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run unit tests
      run: pytest tests/unit/ -v --cov=src/
    
    - name: Run data quality tests
      run: pytest tests/data_quality/ -v
    
    - name: Run integration tests
      run: pytest tests/integration/ -v
      env:
        TEST_DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
    
    - name: Validate pipeline configuration
      run: python scripts/validate_config.py
    
    - name: Check data lineage
      run: python scripts/check_lineage.py

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    steps:
    - name: Deploy to staging
      run: |
        # Deploy pipeline to staging environment
        python scripts/deploy.py --env staging
    
    - name: Run smoke tests
      run: python scripts/smoke_tests.py --env staging

  deploy-production:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      run: |
        # Deploy pipeline to production environment
        python scripts/deploy.py --env production
    
    - name: Run production validation
      run: python scripts/production_validation.py
```

## 6. Data Governance Framework
**What it is**: A framework of policies, procedures, and controls that ensure data is managed as a valuable asset throughout its lifecycle.

**Why important**: Data governance ensures data quality, compliance, security, and proper usage across the organization. It's essential for regulatory compliance and building trust in data-driven decisions.

**When to use**:
- Organizations handling sensitive or regulated data
- Companies requiring data quality assurance
- Environments with multiple data consumers
- Systems needing audit trails and compliance

**Data Catalog Implementation**:
```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class DataFormat(Enum):
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    AVRO = "avro"
    DATABASE_TABLE = "database_table"

@dataclass
class DataAsset:
    """Represents a cataloged data asset."""
    id: str
    name: str
    description: str
    owner: str
    steward: str
    classification: DataClassification
    format: DataFormat
    location: str
    schema: Dict[str, str]
    tags: List[str]
    created_date: datetime
    last_updated: datetime
    retention_period: int  # days
    
class DataCatalog:
    """Data catalog for governance and discovery."""
    
    def __init__(self):
        self._assets = {}
        self._lineage = {}
        self._access_logs = []
    
    def register_asset(self, asset: DataAsset) -> None:
        """Register a new data asset."""
        self._assets[asset.id] = asset
        self._log_access("REGISTER", asset.id, asset.owner)
    
    def search_assets(self, query: str, classification: Optional[DataClassification] = None) -> List[DataAsset]:
        """Search for data assets."""
        results = []
        for asset in self._assets.values():
            if classification and asset.classification != classification:
                continue
            
            if (query.lower() in asset.name.lower() or 
                query.lower() in asset.description.lower() or
                any(query.lower() in tag.lower() for tag in asset.tags)):
                results.append(asset)
        
        return results
    
    def get_lineage(self, asset_id: str) -> Dict[str, List[str]]:
        """Get data lineage for an asset."""
        return self._lineage.get(asset_id, {"upstream": [], "downstream": []})
    
    def add_lineage(self, source_id: str, target_id: str) -> None:
        """Add lineage relationship."""
        if source_id not in self._lineage:
            self._lineage[source_id] = {"upstream": [], "downstream": []}
        if target_id not in self._lineage:
            self._lineage[target_id] = {"upstream": [], "downstream": []}
        
        self._lineage[source_id]["downstream"].append(target_id)
        self._lineage[target_id]["upstream"].append(source_id)
    
    def _log_access(self, action: str, asset_id: str, user: str) -> None:
        """Log access to data assets."""
        self._access_logs.append({
            "timestamp": datetime.now(),
            "action": action,
            "asset_id": asset_id,
            "user": user
        })
```

**Data Quality Framework**:
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import pandas as pd

class DataQualityRule(ABC):
    """Abstract base class for data quality rules."""
    
    @abstractmethod
    def validate(self, data: Any) -> Dict[str, Any]:
        pass

class CompletenessRule(DataQualityRule):
    """Check for missing values in required columns."""
    
    def __init__(self, required_columns: List[str]):
        self.required_columns = required_columns
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {}
        for column in self.required_columns:
            if column in data.columns:
                missing_count = data[column].isnull().sum()
                total_count = len(data)
                completeness_rate = (total_count - missing_count) / total_count
                
                results[f"{column}_completeness"] = {
                    "rule": "completeness",
                    "column": column,
                    "rate": completeness_rate,
                    "missing_count": missing_count,
                    "total_count": total_count,
                    "passed": completeness_rate >= 0.95
                }
        
        return results

class UniquenessRule(DataQualityRule):
    """Check for duplicate values in unique columns."""
    
    def __init__(self, unique_columns: List[str]):
        self.unique_columns = unique_columns
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {}
        for column in self.unique_columns:
            if column in data.columns:
                total_count = len(data)
                unique_count = data[column].nunique()
                duplicate_count = total_count - unique_count
                uniqueness_rate = unique_count / total_count
                
                results[f"{column}_uniqueness"] = {
                    "rule": "uniqueness",
                    "column": column,
                    "rate": uniqueness_rate,
                    "duplicate_count": duplicate_count,
                    "total_count": total_count,
                    "passed": uniqueness_rate >= 0.99
                }
        
        return results

class DataQualityEngine:
    """Engine for running data quality checks."""
    
    def __init__(self):
        self.rules = []
    
    def add_rule(self, rule: DataQualityRule) -> None:
        """Add a data quality rule."""
        self.rules.append(rule)
    
    def run_quality_checks(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run all quality checks on data."""
        all_results = {}
        
        for rule in self.rules:
            rule_results = rule.validate(data)
            all_results.update(rule_results)
        
        # Calculate overall quality score
        passed_checks = sum(1 for result in all_results.values() if result["passed"])
        total_checks = len(all_results)
        overall_score = passed_checks / total_checks if total_checks > 0 else 0
        
        return {
            "overall_quality_score": overall_score,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "detailed_results": all_results
        }
```

## 7. Modern Data Stack Architecture
**What it is**: A collection of modern, cloud-native tools and technologies that work together to create a comprehensive data platform.

**Why important**: The modern data stack provides flexibility, scalability, and cost-effectiveness compared to traditional monolithic data platforms. It enables organizations to choose best-of-breed tools for each component.

**When to use**:
- Building new data platforms
- Modernizing legacy data infrastructure
- Organizations requiring flexible, scalable solutions
- Teams wanting to leverage cloud-native technologies

**Architecture Components**:
```yaml
# Modern Data Stack Configuration
data_stack:
  # Data Ingestion Layer
  ingestion:
    batch:
      - tool: airbyte
        sources: [postgres, mysql, salesforce, hubspot]
        destinations: [snowflake, s3]
      - tool: fivetran
        sources: [google_analytics, facebook_ads]
        destinations: [snowflake]
    
    streaming:
      - tool: kafka
        topics: [user_events, transaction_events]
      - tool: kinesis
        streams: [clickstream, iot_data]
  
  # Data Storage Layer
  storage:
    data_lake:
      - tool: s3
        buckets: [raw-data, processed-data, archive]
        lifecycle_policies: enabled
    
    data_warehouse:
      - tool: snowflake
        databases: [raw, staging, analytics, marts]
        compute_warehouses: [xs, s, m, l]
    
    operational:
      - tool: postgres
        databases: [app_db, user_db]
  
  # Data Transformation Layer
  transformation:
    - tool: dbt
      models: [staging, intermediate, marts]
      tests: [data_quality, business_logic]
    
    - tool: spark
      jobs: [heavy_transformations, ml_preprocessing]
  
  # Data Orchestration Layer
  orchestration:
    - tool: airflow
      dags: [daily_etl, hourly_streaming, ml_training]
    
    - tool: prefect
      flows: [data_quality_monitoring, alerting]
  
  # Data Observability Layer
  observability:
    - tool: monte_carlo
      monitors: [data_freshness, volume_anomalies, schema_changes]
    
    - tool: great_expectations
      expectations: [data_quality, business_rules]
  
  # Data Consumption Layer
  consumption:
    analytics:
      - tool: looker
        dashboards: [executive, operational, self_service]
      
      - tool: tableau
        workbooks: [financial_reporting, sales_analytics]
    
    ml_ops:
      - tool: mlflow
        experiments: [model_training, hyperparameter_tuning]
      
      - tool: kubeflow
        pipelines: [feature_engineering, model_deployment]
```

**Infrastructure as Code**:
```python
# terraform/main.tf equivalent in Python using Pulumi
import pulumi
import pulumi_aws as aws
import pulumi_snowflake as snowflake

# S3 Data Lake
raw_data_bucket = aws.s3.Bucket("raw-data-bucket",
    bucket="company-raw-data",
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

# Snowflake Data Warehouse
snowflake_database = snowflake.Database("analytics_db",
    name="ANALYTICS",
    comment="Main analytics database"
)

snowflake_schema = snowflake.Schema("raw_schema",
    database=snowflake_database.name,
    name="RAW",
    comment="Raw data schema"
)

# Compute Warehouse
compute_warehouse = snowflake.Warehouse("analytics_warehouse",
    name="ANALYTICS_WH",
    warehouse_size="MEDIUM",
    auto_suspend=300,
    auto_resume=True,
    initially_suspended=True
)

# Export important values
pulumi.export("raw_data_bucket_name", raw_data_bucket.bucket)
pulumi.export("snowflake_database_name", snowflake_database.name)
pulumi.export("compute_warehouse_name", compute_warehouse.name)
```

This comprehensive Data Architecture documentation covers all the essential concepts that data engineers need to understand, from basic data modeling to modern data stack implementation. Each section provides both theoretical understanding and practical implementation examples.