# Data Vault 2.0 Key Concepts

## 🎯 What is Data Vault 2.0?
Modeling methodology for building scalable, flexible, and auditable data warehouses using hubs, links, and satellites.

## 🏗️ Core Components

### 1. Hubs
```sql
-- Hub: Business keys and metadata
CREATE TABLE hub_customer (
    customer_hk CHAR(32) PRIMARY KEY,  -- Hash key
    customer_bk VARCHAR(50) NOT NULL,  -- Business key
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Hash key generation
SELECT 
    MD5(UPPER(TRIM(customer_id))) as customer_hk,
    customer_id as customer_bk,
    CURRENT_TIMESTAMP as load_date,
    'CRM_SYSTEM' as record_source
FROM source_customers;
```

### 2. Links
```sql
-- Link: Relationships between business entities
CREATE TABLE link_customer_order (
    customer_order_hk CHAR(32) PRIMARY KEY,
    customer_hk CHAR(32) NOT NULL,
    order_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk),
    FOREIGN KEY (order_hk) REFERENCES hub_order(order_hk)
);

-- Composite hash key
SELECT 
    MD5(CONCAT(customer_hk, '|', order_hk)) as customer_order_hk,
    customer_hk,
    order_hk,
    CURRENT_TIMESTAMP as load_date,
    'ORDER_SYSTEM' as record_source
FROM staging_orders;
```

### 3. Satellites
```sql
-- Satellite: Descriptive attributes
CREATE TABLE sat_customer_details (
    customer_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    hash_diff CHAR(32) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_hk, load_date),
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk)
);

-- Hash diff for change detection
SELECT 
    customer_hk,
    CURRENT_TIMESTAMP as load_date,
    MD5(CONCAT(first_name, '|', last_name, '|', email)) as hash_diff,
    first_name,
    last_name,
    email,
    'CRM_SYSTEM' as record_source
FROM staging_customer_details;
```

## 🔧 Advanced Patterns

### Multi-Active Satellites
```sql
-- Multiple active records per business key
CREATE TABLE sat_customer_address (
    customer_hk CHAR(32) NOT NULL,
    address_type VARCHAR(20) NOT NULL,  -- HOME, WORK, BILLING
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    hash_diff CHAR(32) NOT NULL,
    street_address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(20),
    zip_code VARCHAR(10),
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_hk, address_type, load_date)
);
```

### Point-in-Time Tables (PIT)
```sql
-- Snapshot of data at specific points in time
CREATE TABLE pit_customer (
    customer_hk CHAR(32) NOT NULL,
    snapshot_date DATE NOT NULL,
    sat_customer_details_date TIMESTAMP,
    sat_customer_address_date TIMESTAMP,
    sat_customer_preferences_date TIMESTAMP,
    PRIMARY KEY (customer_hk, snapshot_date)
);
```

### Bridge Tables
```sql
-- Optimized query performance
CREATE TABLE bridge_customer_current (
    customer_hk CHAR(32) PRIMARY KEY,
    customer_bk VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    current_address VARCHAR(200),
    last_updated TIMESTAMP
);
```

## 🚀 Loading Patterns

### Python ETL Implementation
```python
import hashlib
import pandas as pd
from datetime import datetime

class DataVaultLoader:
    def __init__(self, connection):
        self.conn = connection
        self.load_date = datetime.now()
        self.record_source = 'ETL_PROCESS'
    
    def generate_hash_key(self, business_key):
        """Generate hash key from business key"""
        return hashlib.md5(str(business_key).upper().strip().encode()).hexdigest()
    
    def generate_hash_diff(self, attributes):
        """Generate hash diff from attributes"""
        concat_attrs = '|'.join([str(attr) for attr in attributes])
        return hashlib.md5(concat_attrs.encode()).hexdigest()
    
    def load_hub(self, df, hub_table, business_key_col):
        """Load hub table"""
        df['hash_key'] = df[business_key_col].apply(self.generate_hash_key)
        df['load_date'] = self.load_date
        df['record_source'] = self.record_source
        
        # Insert only new business keys
        insert_sql = f"""
        INSERT INTO {hub_table} (hash_key, business_key, load_date, record_source)
        SELECT hash_key, {business_key_col}, load_date, record_source
        FROM staging_table
        WHERE hash_key NOT IN (SELECT hash_key FROM {hub_table})
        """
        
        self.conn.execute(insert_sql)
    
    def load_satellite(self, df, sat_table, hub_key_col, attribute_cols):
        """Load satellite table with change detection"""
        df['hash_diff'] = df[attribute_cols].apply(
            lambda row: self.generate_hash_diff(row.values), axis=1
        )
        df['load_date'] = self.load_date
        df['record_source'] = self.record_source
        
        # Insert only changed records
        insert_sql = f"""
        INSERT INTO {sat_table} 
        SELECT * FROM staging_table s
        WHERE NOT EXISTS (
            SELECT 1 FROM {sat_table} sat
            WHERE sat.{hub_key_col} = s.{hub_key_col}
            AND sat.hash_diff = s.hash_diff
            AND sat.load_end_date IS NULL
        )
        """
        
        # End-date previous records
        update_sql = f"""
        UPDATE {sat_table} 
        SET load_end_date = %s
        WHERE {hub_key_col} IN (SELECT DISTINCT {hub_key_col} FROM staging_table)
        AND load_end_date IS NULL
        """
        
        self.conn.execute(update_sql, (self.load_date,))
        self.conn.execute(insert_sql)
```

## 🎯 Benefits
- Auditability and traceability
- Flexibility for changing requirements
- Parallel loading capabilities
- Historical data preservation
- Scalable architecture

## 🔧 Best Practices
- Use consistent naming conventions
- Implement proper indexing strategy
- Monitor hash key distribution
- Automate quality checks
- Document business rules
- Use staging areas for data preparation

## ⚠️ Considerations
- Storage overhead from normalization
- Complex query patterns
- Learning curve for developers
- Performance tuning required
- Tooling and automation needs