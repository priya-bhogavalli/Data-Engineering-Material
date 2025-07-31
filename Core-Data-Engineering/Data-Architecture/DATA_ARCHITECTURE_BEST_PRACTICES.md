# Data Architecture Best Practices

## 1. Data Modeling Best Practices

### Design for Business Requirements First
Always start with understanding business needs before technical implementation.

```sql
-- Good: Business-focused naming and structure
CREATE TABLE customer_orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    order_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bad: Technical-focused naming
CREATE TABLE tbl_ord_001 (
    id BIGSERIAL PRIMARY KEY,
    cust_fk INTEGER,
    dt DATE,
    amt DECIMAL(10,2),
    sts CHAR(1)
);
```

### Use Consistent Naming Conventions
Establish and follow consistent naming patterns across all data objects.

```sql
-- Consistent naming convention example
-- Tables: plural nouns (customers, orders, products)
-- Columns: snake_case (first_name, order_date, total_amount)
-- Primary keys: table_name + _id (customer_id, order_id)
-- Foreign keys: referenced_table + _id (customer_id in orders table)
-- Indexes: idx_table_column (idx_orders_customer_id)

CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email_address VARCHAR(100) UNIQUE NOT NULL,
    registration_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_address TEXT
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
```

### Implement Proper Data Types and Constraints
Choose appropriate data types and implement constraints to ensure data integrity.

```sql
-- Good: Proper data types and constraints
CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_code VARCHAR(20) UNIQUE NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL CHECK (unit_price > 0),
    category_id INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_products_category 
        FOREIGN KEY (category_id) REFERENCES categories(category_id),
    CONSTRAINT chk_product_name_length 
        CHECK (LENGTH(product_name) >= 3)
);

-- Add triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON products 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Document Your Data Model
Maintain comprehensive documentation for all data structures.

```sql
-- Add comments to tables and columns
COMMENT ON TABLE customers IS 'Customer master data including contact information and registration details';
COMMENT ON COLUMN customers.customer_id IS 'Unique identifier for customer records';
COMMENT ON COLUMN customers.email_address IS 'Primary email address for customer communication';
COMMENT ON COLUMN customers.registration_date IS 'Date when customer first registered with the system';

-- Create data dictionary views
CREATE VIEW data_dictionary AS
SELECT 
    t.table_name,
    c.column_name,
    c.data_type,
    c.is_nullable,
    c.column_default,
    col_description(pgc.oid, c.ordinal_position) as column_comment
FROM information_schema.tables t
JOIN information_schema.columns c ON t.table_name = c.table_name
JOIN pg_class pgc ON pgc.relname = t.table_name
WHERE t.table_schema = 'public'
ORDER BY t.table_name, c.ordinal_position;
```

## 2. Data Warehouse Design Best Practices

### Implement Dimensional Modeling Correctly
Follow Kimball methodology for dimensional modeling.

```sql
-- Fact table design
CREATE TABLE fact_sales (
    -- Surrogate key
    sale_key BIGSERIAL PRIMARY KEY,
    
    -- Foreign keys to dimensions
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    
    -- Degenerate dimensions (transaction-level attributes)
    transaction_id VARCHAR(50) NOT NULL,
    receipt_number VARCHAR(20),
    
    -- Measures (additive facts)
    quantity_sold INTEGER NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(8,2) DEFAULT 0,
    tax_amount DECIMAL(8,2) NOT NULL,
    
    -- Semi-additive facts
    inventory_balance INTEGER,
    
    -- Non-additive facts (ratios, percentages)
    profit_margin_percent DECIMAL(5,2),
    
    -- Audit columns
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT USER,
    
    -- Foreign key constraints
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);

-- Dimension table design with SCD Type 2
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    
    -- Natural key
    customer_id VARCHAR(50) NOT NULL,
    
    -- Descriptive attributes
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(100) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
    email_address VARCHAR(100),
    phone_number VARCHAR(20),
    
    -- Address attributes
    street_address VARCHAR(200),
    city VARCHAR(50),
    state_province VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    
    -- Derived attributes
    age_group VARCHAR(20),
    customer_segment VARCHAR(30),
    lifetime_value_tier VARCHAR(20),
    
    -- SCD Type 2 attributes
    effective_date DATE NOT NULL,
    expiration_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN DEFAULT TRUE,
    version_number INTEGER DEFAULT 1,
    
    -- Audit attributes
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_source VARCHAR(50) NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_dim_customer_natural_key ON dim_customer(customer_id, is_current);
CREATE INDEX idx_dim_customer_effective_date ON dim_customer(effective_date);
CREATE INDEX idx_fact_sales_date_key ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_customer_key ON fact_sales(customer_key);
```

### Design Efficient Date Dimensions
Create comprehensive date dimensions for time-based analysis.

```sql
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    
    -- Day attributes
    day_of_month INTEGER NOT NULL,
    day_of_year INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_name_short VARCHAR(3) NOT NULL,
    
    -- Week attributes
    week_of_year INTEGER NOT NULL,
    week_of_month INTEGER NOT NULL,
    week_start_date DATE NOT NULL,
    week_end_date DATE NOT NULL,
    
    -- Month attributes
    month_number INTEGER NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    month_name_short VARCHAR(3) NOT NULL,
    month_start_date DATE NOT NULL,
    month_end_date DATE NOT NULL,
    
    -- Quarter attributes
    quarter_number INTEGER NOT NULL,
    quarter_name VARCHAR(2) NOT NULL,
    quarter_start_date DATE NOT NULL,
    quarter_end_date DATE NOT NULL,
    
    -- Year attributes
    year_number INTEGER NOT NULL,
    year_start_date DATE NOT NULL,
    year_end_date DATE NOT NULL,
    
    -- Business attributes
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT FALSE,
    holiday_name VARCHAR(50),
    is_business_day BOOLEAN NOT NULL,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    fiscal_month INTEGER,
    
    -- Relative date attributes
    days_from_today INTEGER,
    is_current_day BOOLEAN DEFAULT FALSE,
    is_current_week BOOLEAN DEFAULT FALSE,
    is_current_month BOOLEAN DEFAULT FALSE,
    is_current_quarter BOOLEAN DEFAULT FALSE,
    is_current_year BOOLEAN DEFAULT FALSE
);

-- Populate date dimension
INSERT INTO dim_date (
    date_key, full_date, day_of_month, day_of_year, day_of_week,
    day_name, day_name_short, week_of_year, month_number, month_name,
    month_name_short, quarter_number, quarter_name, year_number,
    is_weekend, is_business_day
)
SELECT 
    TO_CHAR(date_series, 'YYYYMMDD')::INTEGER as date_key,
    date_series as full_date,
    EXTRACT(DAY FROM date_series) as day_of_month,
    EXTRACT(DOY FROM date_series) as day_of_year,
    EXTRACT(DOW FROM date_series) as day_of_week,
    TO_CHAR(date_series, 'Day') as day_name,
    TO_CHAR(date_series, 'Dy') as day_name_short,
    EXTRACT(WEEK FROM date_series) as week_of_year,
    EXTRACT(MONTH FROM date_series) as month_number,
    TO_CHAR(date_series, 'Month') as month_name,
    TO_CHAR(date_series, 'Mon') as month_name_short,
    EXTRACT(QUARTER FROM date_series) as quarter_number,
    'Q' || EXTRACT(QUARTER FROM date_series) as quarter_name,
    EXTRACT(YEAR FROM date_series) as year_number,
    CASE WHEN EXTRACT(DOW FROM date_series) IN (0, 6) THEN TRUE ELSE FALSE END as is_weekend,
    CASE WHEN EXTRACT(DOW FROM date_series) BETWEEN 1 AND 5 THEN TRUE ELSE FALSE END as is_business_day
FROM generate_series('2020-01-01'::DATE, '2030-12-31'::DATE, '1 day'::INTERVAL) as date_series;
```

### Implement Proper Partitioning Strategy
Use partitioning for large tables to improve performance.

```sql
-- Partition fact table by date
CREATE TABLE fact_sales_partitioned (
    sale_key BIGSERIAL,
    date_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (date_key);

-- Create monthly partitions
CREATE TABLE fact_sales_202401 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20240101) TO (20240201);

CREATE TABLE fact_sales_202402 PARTITION OF fact_sales_partitioned
    FOR VALUES FROM (20240201) TO (20240301);

-- Create indexes on partitions
CREATE INDEX idx_fact_sales_202401_customer ON fact_sales_202401(customer_key);
CREATE INDEX idx_fact_sales_202402_customer ON fact_sales_202402(customer_key);

-- Automated partition creation function
CREATE OR REPLACE FUNCTION create_monthly_partition(table_name TEXT, start_date DATE)
RETURNS VOID AS $$
DECLARE
    partition_name TEXT;
    start_key INTEGER;
    end_key INTEGER;
BEGIN
    partition_name := table_name || '_' || TO_CHAR(start_date, 'YYYYMM');
    start_key := TO_CHAR(start_date, 'YYYYMMDD')::INTEGER;
    end_key := TO_CHAR(start_date + INTERVAL '1 month', 'YYYYMMDD')::INTEGER;
    
    EXECUTE format('CREATE TABLE %I PARTITION OF %I FOR VALUES FROM (%s) TO (%s)',
                   partition_name, table_name, start_key, end_key);
    
    EXECUTE format('CREATE INDEX idx_%s_customer ON %I(customer_key)',
                   partition_name, partition_name);
END;
$$ LANGUAGE plpgsql;
```

## 3. Data Quality Best Practices

### Implement Comprehensive Data Validation
Create robust data validation frameworks.

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd
import logging

class DataQualityRule(ABC):
    """Abstract base class for data quality rules"""
    
    def __init__(self, name: str, description: str, severity: str = 'ERROR'):
        self.name = name
        self.description = description
        self.severity = severity
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        pass

class CompletenessRule(DataQualityRule):
    """Validate data completeness"""
    
    def __init__(self, columns: List[str], threshold: float = 0.95):
        super().__init__(
            name="completeness_check",
            description=f"Check completeness for columns: {columns}",
            severity="ERROR"
        )
        self.columns = columns
        self.threshold = threshold
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {}
        
        for column in self.columns:
            if column not in data.columns:
                results[f"{column}_completeness"] = {
                    "passed": False,
                    "error": f"Column {column} not found in data",
                    "severity": self.severity
                }
                continue
            
            total_rows = len(data)
            non_null_rows = data[column].notna().sum()
            completeness_rate = non_null_rows / total_rows if total_rows > 0 else 0
            
            results[f"{column}_completeness"] = {
                "passed": completeness_rate >= self.threshold,
                "completeness_rate": completeness_rate,
                "threshold": self.threshold,
                "total_rows": total_rows,
                "non_null_rows": non_null_rows,
                "severity": self.severity
            }
        
        return results

class UniquenessRule(DataQualityRule):
    """Validate data uniqueness"""
    
    def __init__(self, columns: List[str], threshold: float = 1.0):
        super().__init__(
            name="uniqueness_check",
            description=f"Check uniqueness for columns: {columns}",
            severity="ERROR"
        )
        self.columns = columns
        self.threshold = threshold
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        results = {}
        
        for column in self.columns:
            if column not in data.columns:
                results[f"{column}_uniqueness"] = {
                    "passed": False,
                    "error": f"Column {column} not found in data",
                    "severity": self.severity
                }
                continue
            
            total_rows = len(data)
            unique_rows = data[column].nunique()
            uniqueness_rate = unique_rows / total_rows if total_rows > 0 else 0
            
            results[f"{column}_uniqueness"] = {
                "passed": uniqueness_rate >= self.threshold,
                "uniqueness_rate": uniqueness_rate,
                "threshold": self.threshold,
                "total_rows": total_rows,
                "unique_rows": unique_rows,
                "duplicate_count": total_rows - unique_rows,
                "severity": self.severity
            }
        
        return results

class RangeValidationRule(DataQualityRule):
    """Validate numeric ranges"""
    
    def __init__(self, column: str, min_value: float = None, max_value: float = None):
        super().__init__(
            name="range_validation",
            description=f"Validate range for {column}: [{min_value}, {max_value}]",
            severity="WARNING"
        )
        self.column = column
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, data: pd.DataFrame) -> Dict[str, Any]:
        if self.column not in data.columns:
            return {
                f"{self.column}_range": {
                    "passed": False,
                    "error": f"Column {self.column} not found in data",
                    "severity": self.severity
                }
            }
        
        column_data = data[self.column].dropna()
        total_valid_rows = len(column_data)
        
        violations = []
        if self.min_value is not None:
            violations.extend(column_data[column_data < self.min_value])
        if self.max_value is not None:
            violations.extend(column_data[column_data > self.max_value])
        
        violation_count = len(violations)
        pass_rate = (total_valid_rows - violation_count) / total_valid_rows if total_valid_rows > 0 else 1
        
        return {
            f"{self.column}_range": {
                "passed": violation_count == 0,
                "pass_rate": pass_rate,
                "total_valid_rows": total_valid_rows,
                "violation_count": violation_count,
                "min_value": self.min_value,
                "max_value": self.max_value,
                "severity": self.severity
            }
        }

class DataQualityFramework:
    """Comprehensive data quality framework"""
    
    def __init__(self):
        self.rules = []
        self.logger = logging.getLogger(__name__)
    
    def add_rule(self, rule: DataQualityRule):
        """Add a data quality rule"""
        self.rules.append(rule)
    
    def validate_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run all validation rules on data"""
        all_results = {}
        
        for rule in self.rules:
            try:
                rule_results = rule.validate(data)
                all_results.update(rule_results)
            except Exception as e:
                self.logger.error(f"Error running rule {rule.name}: {str(e)}")
                all_results[f"{rule.name}_error"] = {
                    "passed": False,
                    "error": str(e),
                    "severity": "ERROR"
                }
        
        # Calculate overall quality score
        total_checks = len(all_results)
        passed_checks = sum(1 for result in all_results.values() if result.get("passed", False))
        quality_score = passed_checks / total_checks if total_checks > 0 else 0
        
        return {
            "overall_quality_score": quality_score,
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": total_checks - passed_checks,
            "detailed_results": all_results
        }
    
    def generate_quality_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate human-readable quality report"""
        report = []
        report.append("=" * 50)
        report.append("DATA QUALITY REPORT")
        report.append("=" * 50)
        report.append(f"Overall Quality Score: {validation_results['overall_quality_score']:.2%}")
        report.append(f"Total Checks: {validation_results['total_checks']}")
        report.append(f"Passed: {validation_results['passed_checks']}")
        report.append(f"Failed: {validation_results['failed_checks']}")
        report.append("")
        
        # Group results by severity
        errors = []
        warnings = []
        
        for check_name, result in validation_results['detailed_results'].items():
            if not result.get("passed", True):
                if result.get("severity") == "ERROR":
                    errors.append((check_name, result))
                else:
                    warnings.append((check_name, result))
        
        if errors:
            report.append("ERRORS:")
            report.append("-" * 20)
            for check_name, result in errors:
                report.append(f"❌ {check_name}: {result.get('error', 'Check failed')}")
            report.append("")
        
        if warnings:
            report.append("WARNINGS:")
            report.append("-" * 20)
            for check_name, result in warnings:
                report.append(f"⚠️  {check_name}: {result.get('error', 'Check failed')}")
        
        return "\n".join(report)

# Usage example
def setup_data_quality_framework():
    """Setup data quality framework with common rules"""
    framework = DataQualityFramework()
    
    # Add completeness rules
    framework.add_rule(CompletenessRule(['customer_id', 'order_date', 'total_amount'], threshold=0.95))
    
    # Add uniqueness rules
    framework.add_rule(UniquenessRule(['customer_id'], threshold=1.0))
    
    # Add range validation rules
    framework.add_rule(RangeValidationRule('total_amount', min_value=0, max_value=100000))
    framework.add_rule(RangeValidationRule('quantity', min_value=1, max_value=1000))
    
    return framework
```

### Implement Data Lineage Tracking
Track data lineage for transparency and debugging.

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import json

@dataclass
class DataLineageNode:
    """Represents a node in data lineage"""
    id: str
    name: str
    type: str  # 'source', 'transformation', 'destination'
    description: str
    schema: Dict[str, str]
    location: str
    created_at: datetime
    updated_at: datetime

@dataclass
class DataLineageEdge:
    """Represents a relationship in data lineage"""
    source_id: str
    target_id: str
    transformation_type: str
    transformation_logic: str
    created_at: datetime

class DataLineageTracker:
    """Track and manage data lineage"""
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
    
    def add_node(self, node: DataLineageNode):
        """Add a node to lineage graph"""
        self.nodes[node.id] = node
    
    def add_edge(self, edge: DataLineageEdge):
        """Add an edge to lineage graph"""
        if edge.source_id not in self.nodes or edge.target_id not in self.nodes:
            raise ValueError("Source and target nodes must exist before adding edge")
        self.edges.append(edge)
    
    def get_upstream_lineage(self, node_id: str, depth: int = None) -> List[DataLineageNode]:
        """Get upstream lineage for a node"""
        upstream_nodes = []
        visited = set()
        
        def traverse_upstream(current_id, current_depth):
            if depth is not None and current_depth >= depth:
                return
            if current_id in visited:
                return
            
            visited.add(current_id)
            
            for edge in self.edges:
                if edge.target_id == current_id:
                    upstream_nodes.append(self.nodes[edge.source_id])
                    traverse_upstream(edge.source_id, current_depth + 1)
        
        traverse_upstream(node_id, 0)
        return upstream_nodes
    
    def get_downstream_lineage(self, node_id: str, depth: int = None) -> List[DataLineageNode]:
        """Get downstream lineage for a node"""
        downstream_nodes = []
        visited = set()
        
        def traverse_downstream(current_id, current_depth):
            if depth is not None and current_depth >= depth:
                return
            if current_id in visited:
                return
            
            visited.add(current_id)
            
            for edge in self.edges:
                if edge.source_id == current_id:
                    downstream_nodes.append(self.nodes[edge.target_id])
                    traverse_downstream(edge.target_id, current_depth + 1)
        
        traverse_downstream(node_id, 0)
        return downstream_nodes
    
    def export_lineage_graph(self) -> Dict:
        """Export lineage graph as JSON"""
        return {
            "nodes": [
                {
                    "id": node.id,
                    "name": node.name,
                    "type": node.type,
                    "description": node.description,
                    "schema": node.schema,
                    "location": node.location,
                    "created_at": node.created_at.isoformat(),
                    "updated_at": node.updated_at.isoformat()
                }
                for node in self.nodes.values()
            ],
            "edges": [
                {
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "transformation_type": edge.transformation_type,
                    "transformation_logic": edge.transformation_logic,
                    "created_at": edge.created_at.isoformat()
                }
                for edge in self.edges
            ]
        }
```

## 4. Performance Optimization Best Practices

### Implement Proper Indexing Strategy
Create indexes based on query patterns and performance requirements.

```sql
-- Analyze query patterns first
-- Common query: Find orders by customer and date range
SELECT * FROM orders 
WHERE customer_id = 12345 
AND order_date BETWEEN '2024-01-01' AND '2024-01-31';

-- Create composite index for this query pattern
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- For queries that filter by status and order by date
SELECT * FROM orders 
WHERE status = 'pending' 
ORDER BY order_date DESC;

-- Create index with status first, then date for sorting
CREATE INDEX idx_orders_status_date ON orders(status, order_date DESC);

-- For analytical queries that aggregate by date
SELECT DATE_TRUNC('month', order_date) as month, SUM(total_amount)
FROM orders 
GROUP BY DATE_TRUNC('month', order_date);

-- Create functional index
CREATE INDEX idx_orders_month ON orders(DATE_TRUNC('month', order_date));

-- Partial indexes for frequently filtered data
CREATE INDEX idx_orders_active ON orders(order_date) 
WHERE status IN ('pending', 'processing');

-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Optimize Query Performance
Write efficient queries and use proper optimization techniques.

```sql
-- Use EXISTS instead of IN for better performance
-- Good
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_date >= '2024-01-01'
);

-- Avoid
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
WHERE c.customer_id IN (
    SELECT o.customer_id FROM orders o 
    WHERE o.order_date >= '2024-01-01'
);

-- Use proper JOIN syntax and conditions
-- Good: Use specific JOIN conditions
SELECT 
    c.customer_id,
    c.first_name,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id 
    AND o.order_date >= '2024-01-01'
GROUP BY c.customer_id, c.first_name;

-- Use LIMIT with ORDER BY for pagination
SELECT customer_id, first_name, last_name, email_address
FROM customers
ORDER BY customer_id
LIMIT 50 OFFSET 1000;

-- Use window functions for analytical queries
SELECT 
    customer_id,
    order_date,
    total_amount,
    SUM(total_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date DESC
    ) as order_rank
FROM orders;

-- Use CTEs for complex queries
WITH customer_metrics AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent,
        AVG(total_amount) as avg_order_value,
        MAX(order_date) as last_order_date
    FROM orders
    WHERE order_date >= '2023-01-01'
    GROUP BY customer_id
),
customer_segments AS (
    SELECT 
        customer_id,
        order_count,
        total_spent,
        avg_order_value,
        last_order_date,
        CASE 
            WHEN total_spent >= 10000 THEN 'VIP'
            WHEN total_spent >= 5000 THEN 'Premium'
            WHEN total_spent >= 1000 THEN 'Regular'
            ELSE 'New'
        END as customer_segment
    FROM customer_metrics
)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    cs.customer_segment,
    cs.total_spent,
    cs.order_count
FROM customers c
JOIN customer_segments cs ON c.customer_id = cs.customer_id;
```

### Implement Effective Caching Strategies
Use caching to improve performance for frequently accessed data.

```python
import redis
import json
from typing import Any, Optional
from datetime import datetime, timedelta
import hashlib

class DataCache:
    """Redis-based caching for data operations"""
    
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        self.redis_client = redis.Redis(
            host=redis_host, 
            port=redis_port, 
            db=redis_db,
            decode_responses=True
        )
    
    def generate_cache_key(self, prefix: str, **kwargs) -> str:
        """Generate consistent cache key"""
        key_parts = [prefix]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        
        key_string = ":".join(key_parts)
        # Hash long keys to avoid Redis key length limits
        if len(key_string) > 200:
            key_hash = hashlib.md5(key_string.encode()).hexdigest()
            return f"{prefix}:hash:{key_hash}"
        
        return key_string
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            cached_value = self.redis_client.get(key)
            if cached_value:
                return json.loads(cached_value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        try:
            serialized_value = json.dumps(value, default=str)
            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache invalidate error: {e}")
            return 0

class CachedDataService:
    """Data service with caching layer"""
    
    def __init__(self, database_connection, cache: DataCache):
        self.db = database_connection
        self.cache = cache
    
    def get_customer_summary(self, customer_id: int, force_refresh: bool = False):
        """Get customer summary with caching"""
        cache_key = self.cache.generate_cache_key(
            "customer_summary", 
            customer_id=customer_id
        )
        
        # Try cache first (unless force refresh)
        if not force_refresh:
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result
        
        # Query database
        query = """
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email_address,
            COUNT(o.order_id) as total_orders,
            COALESCE(SUM(o.total_amount), 0) as total_spent,
            COALESCE(AVG(o.total_amount), 0) as avg_order_value,
            MAX(o.order_date) as last_order_date
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        WHERE c.customer_id = %s
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email_address
        """
        
        result = self.db.execute(query, (customer_id,)).fetchone()
        
        if result:
            customer_data = dict(result)
            # Cache for 1 hour
            self.cache.set(cache_key, customer_data, ttl=3600)
            return customer_data
        
        return None
    
    def invalidate_customer_cache(self, customer_id: int):
        """Invalidate all cache entries for a customer"""
        pattern = f"customer_*:customer_id:{customer_id}*"
        return self.cache.invalidate_pattern(pattern)
    
    def get_popular_products(self, days: int = 30, limit: int = 10):
        """Get popular products with longer cache TTL"""
        cache_key = self.cache.generate_cache_key(
            "popular_products",
            days=days,
            limit=limit
        )
        
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        query = """
        SELECT 
            p.product_id,
            p.product_name,
            p.category,
            COUNT(oi.order_item_id) as order_count,
            SUM(oi.quantity) as total_quantity_sold
        FROM products p
        JOIN order_items oi ON p.product_id = oi.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_date >= CURRENT_DATE - INTERVAL '%s days'
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_quantity_sold DESC
        LIMIT %s
        """
        
        results = self.db.execute(query, (days, limit)).fetchall()
        popular_products = [dict(row) for row in results]
        
        # Cache for 4 hours (less frequent changes)
        self.cache.set(cache_key, popular_products, ttl=14400)
        return popular_products
```

This comprehensive set of best practices covers the essential aspects of data architecture, from basic modeling principles to advanced performance optimization techniques. Following these practices will help ensure robust, scalable, and maintainable data systems.