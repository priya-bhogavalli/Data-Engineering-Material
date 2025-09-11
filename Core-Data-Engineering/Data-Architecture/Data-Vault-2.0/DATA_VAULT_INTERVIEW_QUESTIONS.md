# Data Vault 2.0 Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-200)](#architecture--performance-151-200)
5. [Implementation & ETL (201-250)](#implementation--etl-201-250)
6. [Production & Operations (251-300)](#production--operations-251-300)
7. [Scenario-Based Questions (301-350)](#scenario-based-questions-301-350)

---

## Basic Level Questions (1-50)

### 1. What is Data Vault 2.0 and how does it differ from traditional data modeling approaches?

**Answer:** Data Vault 2.0 is a data modeling methodology designed for building scalable, flexible, and auditable data warehouses using three core components: Hubs, Links, and Satellites.

#### **Key Differences from Traditional Approaches:**

| Feature | Data Vault 2.0 | Dimensional (Kimball) | Normalized (Inmon) |
|---------|----------------|----------------------|-------------------|
| **Flexibility** | Very High | Medium | Low |
| **Auditability** | Complete | Limited | Good |
| **Time to Market** | Fast | Medium | Slow |
| **Schema Changes** | Easy | Difficult | Very Difficult |
| **Historical Tracking** | Complete | Type 2 SCD | Good |
| **Parallel Development** | Excellent | Limited | Limited |

#### **Core Principles:**
- **Insert-Only**: No updates or deletes in raw vault
- **Auditability**: Complete historical tracking
- **Flexibility**: Easy accommodation of changing requirements
- **Scalability**: Parallel loading capabilities

```sql
-- Data Vault Structure Example
-- Hub: Business keys
CREATE TABLE hub_customer (
    customer_hk CHAR(32) PRIMARY KEY,
    customer_bk VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Link: Relationships
CREATE TABLE link_customer_order (
    customer_order_hk CHAR(32) PRIMARY KEY,
    customer_hk CHAR(32) NOT NULL,
    order_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);

-- Satellite: Descriptive data
CREATE TABLE sat_customer_details (
    customer_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    hash_diff CHAR(32) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_hk, load_date)
);
```

### 2. Explain the three core components of Data Vault: Hubs, Links, and Satellites.

**Answer:** The three core components form the foundation of Data Vault architecture.

#### **Hubs - Business Entity Keys**
- **Purpose**: Store unique business keys and metadata
- **Content**: Business keys, hash keys, load dates, record sources
- **Characteristics**: Insert-only, no descriptive data

```sql
-- Hub Example
CREATE TABLE hub_product (
    product_hk CHAR(32) PRIMARY KEY,        -- Hash of business key
    product_code VARCHAR(50) NOT NULL,      -- Business key
    load_date TIMESTAMP NOT NULL,           -- When first loaded
    record_source VARCHAR(50) NOT NULL      -- Source system
);

INSERT INTO hub_product VALUES 
('a1b2c3d4e5f6...', 'PROD001', '2024-01-01 10:00:00', 'ERP_SYSTEM');
```

#### **Links - Relationships Between Entities**
- **Purpose**: Capture associations and transactions
- **Content**: Foreign keys to hubs, load metadata
- **Characteristics**: Many-to-many relationships, temporal tracking

```sql
-- Link Example
CREATE TABLE link_order_product (
    order_product_hk CHAR(32) PRIMARY KEY,  -- Hash of all FKs
    order_hk CHAR(32) NOT NULL,             -- FK to order hub
    product_hk CHAR(32) NOT NULL,           -- FK to product hub
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (order_hk) REFERENCES hub_order(order_hk),
    FOREIGN KEY (product_hk) REFERENCES hub_product(product_hk)
);
```

#### **Satellites - Descriptive Attributes**
- **Purpose**: Store all descriptive data and context
- **Content**: Attributes, change tracking, effective dates
- **Characteristics**: Type 2 SCD, hash diff for change detection

```sql
-- Satellite Example
CREATE TABLE sat_product_details (
    product_hk CHAR(32) NOT NULL,           -- FK to hub
    load_date TIMESTAMP NOT NULL,           -- Effective date
    load_end_date TIMESTAMP,                -- End date (NULL = current)
    hash_diff CHAR(32) NOT NULL,            -- Change detection
    product_name VARCHAR(100),              -- Descriptive attributes
    category VARCHAR(50),
    price DECIMAL(10,2),
    description TEXT,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (product_hk, load_date)
);
```

### 3. What is a hash key and why is it used in Data Vault?

**Answer:** Hash keys are MD5 or SHA hash values generated from business keys, used as surrogate keys in Data Vault for performance and consistency.

#### **Benefits of Hash Keys:**
- **Deterministic**: Same input always produces same hash
- **Performance**: Fixed-length keys improve join performance
- **Distribution**: Even distribution across partitions
- **Integration**: Consistent across different systems
- **Collision Avoidance**: Extremely low probability of duplicates

#### **Hash Key Generation:**
```python
import hashlib

def generate_hash_key(*business_keys):
    """Generate MD5 hash key from business keys"""
    # Concatenate and normalize business keys
    concat_keys = ''.join([str(key).upper().strip() for key in business_keys if key])
    
    # Generate MD5 hash
    return hashlib.md5(concat_keys.encode('utf-8')).hexdigest()

# Examples
customer_hk = generate_hash_key('CUST001')
print(f"Customer Hash Key: {customer_hk}")
# Output: Customer Hash Key: 7d865e959b2466918c9863afca942d0f

# Link hash key (multiple business keys)
order_product_hk = generate_hash_key('ORD001', 'PROD001')
print(f"Link Hash Key: {order_product_hk}")
# Output: Link Hash Key: 2c6ee24b987b5d5b8d0f2b5b5d5b8d0f
```

#### **SQL Implementation:**
```sql
-- Hash key generation in SQL
SELECT 
    MD5(UPPER(TRIM(customer_id))) as customer_hk,
    customer_id as customer_bk
FROM source_data;

-- Link hash key (concatenate multiple keys)
SELECT 
    MD5(CONCAT(
        COALESCE(MD5(UPPER(TRIM(customer_id))), ''),
        COALESCE(MD5(UPPER(TRIM(order_id))), '')
    )) as customer_order_hk
FROM source_data;
```

### 4. What is hash diff and how is it used for change detection?

**Answer:** Hash diff is a hash value generated from all descriptive attributes in a satellite, used to efficiently detect changes without comparing individual columns.

#### **Purpose and Benefits:**
- **Change Detection**: Quickly identify if any attribute changed
- **Performance**: Single hash comparison vs multiple column comparisons
- **Efficiency**: Reduces satellite loading time
- **Accuracy**: Detects any change in source data

#### **Hash Diff Generation:**
```python
def generate_hash_diff(**attributes):
    """Generate hash diff for change detection"""
    # Sort attributes by key for consistency
    sorted_attrs = sorted(attributes.items())
    
    # Concatenate all attribute values
    concat_attrs = ''.join([
        str(value) if value is not None else '' 
        for key, value in sorted_attrs
    ])
    
    return hashlib.md5(concat_attrs.encode('utf-8')).hexdigest()

# Example
hash_diff = generate_hash_diff(
    first_name='John',
    last_name='Doe',
    email='john.doe@email.com',
    phone='555-1234',
    address='123 Main St'
)
print(f"Hash Diff: {hash_diff}")
# Output: Hash Diff: 8f14e45fceea167a5a36dedd4bea2543
```

#### **Satellite Loading with Hash Diff:**
```sql
-- Satellite loading with change detection
WITH new_records AS (
    SELECT 
        MD5(UPPER(TRIM(customer_id))) as customer_hk,
        MD5(CONCAT(
            COALESCE(first_name, ''),
            COALESCE(last_name, ''),
            COALESCE(email, ''),
            COALESCE(phone, ''),
            COALESCE(address, '')
        )) as hash_diff,
        first_name,
        last_name,
        email,
        phone,
        address,
        CURRENT_TIMESTAMP as load_date,
        'CRM_SYSTEM' as record_source
    FROM staging.customer_data
),
changed_records AS (
    SELECT n.*
    FROM new_records n
    LEFT JOIN sat_customer_details s ON n.customer_hk = s.customer_hk 
        AND s.load_end_date IS NULL
    WHERE s.hash_diff IS NULL OR s.hash_diff != n.hash_diff
)
-- Insert only changed records
INSERT INTO sat_customer_details 
SELECT * FROM changed_records;
```

### 5. Explain the loading sequence in Data Vault (Hubs → Links → Satellites).

**Answer:** Data Vault follows a specific loading sequence to maintain referential integrity and optimize performance.

#### **Loading Sequence:**
1. **Hubs First**: Load business keys and establish entities
2. **Links Second**: Load relationships (requires hub keys to exist)
3. **Satellites Last**: Load descriptive data (requires hub/link keys)

#### **Why This Sequence Matters:**
- **Referential Integrity**: Links need hub keys, satellites need hub/link keys
- **Parallel Processing**: Can load multiple hubs simultaneously
- **Error Handling**: Failed hub loads don't affect links/satellites
- **Performance**: Optimizes database constraints and indexing

#### **Implementation Example:**
```sql
-- Step 1: Load Hubs (can be parallel)
-- Load Customer Hub
INSERT INTO hub_customer (customer_hk, customer_bk, load_date, record_source)
SELECT DISTINCT
    MD5(UPPER(TRIM(customer_id))) as customer_hk,
    customer_id as customer_bk,
    CURRENT_TIMESTAMP as load_date,
    'CRM_SYSTEM' as record_source
FROM staging.customer_data s
WHERE NOT EXISTS (
    SELECT 1 FROM hub_customer h 
    WHERE h.customer_hk = MD5(UPPER(TRIM(s.customer_id)))
);

-- Load Order Hub (parallel with customer hub)
INSERT INTO hub_order (order_hk, order_bk, load_date, record_source)
SELECT DISTINCT
    MD5(UPPER(TRIM(order_id))) as order_hk,
    order_id as order_bk,
    CURRENT_TIMESTAMP as load_date,
    'ORDER_SYSTEM' as record_source
FROM staging.order_data s
WHERE NOT EXISTS (
    SELECT 1 FROM hub_order h 
    WHERE h.order_hk = MD5(UPPER(TRIM(s.order_id)))
);

-- Step 2: Load Links (after hubs are loaded)
INSERT INTO link_customer_order (customer_order_hk, customer_hk, order_hk, load_date, record_source)
SELECT DISTINCT
    MD5(CONCAT(
        MD5(UPPER(TRIM(s.customer_id))),
        MD5(UPPER(TRIM(s.order_id)))
    )) as customer_order_hk,
    MD5(UPPER(TRIM(s.customer_id))) as customer_hk,
    MD5(UPPER(TRIM(s.order_id))) as order_hk,
    CURRENT_TIMESTAMP as load_date,
    'ORDER_SYSTEM' as record_source
FROM staging.order_data s
WHERE EXISTS (SELECT 1 FROM hub_customer h WHERE h.customer_hk = MD5(UPPER(TRIM(s.customer_id))))
  AND EXISTS (SELECT 1 FROM hub_order o WHERE o.order_hk = MD5(UPPER(TRIM(s.order_id))))
  AND NOT EXISTS (
    SELECT 1 FROM link_customer_order l 
    WHERE l.customer_order_hk = MD5(CONCAT(
        MD5(UPPER(TRIM(s.customer_id))),
        MD5(UPPER(TRIM(s.order_id)))
    ))
);

-- Step 3: Load Satellites (after hubs/links are loaded)
-- Load Customer Details Satellite
WITH new_records AS (
    SELECT 
        MD5(UPPER(TRIM(customer_id))) as customer_hk,
        MD5(CONCAT(
            COALESCE(first_name, ''),
            COALESCE(last_name, ''),
            COALESCE(email, '')
        )) as hash_diff,
        first_name,
        last_name,
        email,
        CURRENT_TIMESTAMP as load_date,
        'CRM_SYSTEM' as record_source
    FROM staging.customer_data
    WHERE EXISTS (
        SELECT 1 FROM hub_customer h 
        WHERE h.customer_hk = MD5(UPPER(TRIM(customer_id)))
    )
)
INSERT INTO sat_customer_details 
SELECT * FROM new_records n
WHERE NOT EXISTS (
    SELECT 1 FROM sat_customer_details s 
    WHERE s.customer_hk = n.customer_hk 
    AND s.hash_diff = n.hash_diff
    AND s.load_end_date IS NULL
);
```

### 6. What are the different types of satellites in Data Vault?

**Answer:** Data Vault supports several satellite types to handle different data patterns and requirements.

#### **1. Standard Satellites**
- **Purpose**: Store regular descriptive attributes
- **Pattern**: One record per entity per time period
- **Use Case**: Customer details, product information

```sql
CREATE TABLE sat_customer_details (
    customer_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    hash_diff CHAR(32) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_hk, load_date)
);
```

#### **2. Multi-Active Satellites**
- **Purpose**: Track multiple active records simultaneously
- **Pattern**: Multiple concurrent records per entity
- **Use Case**: Phone numbers, addresses, skills

```sql
CREATE TABLE sat_customer_phone_ma (
    customer_hk CHAR(32) NOT NULL,
    phone_type VARCHAR(20) NOT NULL,    -- Part of primary key
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    hash_diff CHAR(32) NOT NULL,
    phone_number VARCHAR(20),
    is_primary BOOLEAN,
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (customer_hk, phone_type, load_date)
);

-- Sample data showing multiple active phone numbers
INSERT INTO sat_customer_phone_ma VALUES 
('a1b2c3d4e5f6...', 'HOME', '2024-01-01 10:00:00', NULL, 
 'h1a2s3h4...', '555-1234', TRUE, 'CRM_SYSTEM'),
('a1b2c3d4e5f6...', 'MOBILE', '2024-01-01 10:00:00', NULL, 
 'h5a6s7h8...', '555-5678', FALSE, 'CRM_SYSTEM'),
('a1b2c3d4e5f6...', 'WORK', '2024-01-15 14:30:00', NULL, 
 'h9a0s1h2...', '555-9999', FALSE, 'CRM_SYSTEM');
```

#### **3. Non-Historized Satellites**
- **Purpose**: Store reference data that doesn't need history
- **Pattern**: Current state only, no end dating
- **Use Case**: Static lookups, configuration data

```sql
CREATE TABLE sat_product_category_nh (
    product_hk CHAR(32) PRIMARY KEY,
    load_date TIMESTAMP NOT NULL,
    hash_diff CHAR(32) NOT NULL,
    category_code VARCHAR(10),
    category_name VARCHAR(50),
    category_description TEXT,
    record_source VARCHAR(50) NOT NULL
    -- No load_end_date - always current
);
```

#### **4. Status Tracking Satellites**
- **Purpose**: Track status changes and workflow states
- **Pattern**: Optimized for status transitions
- **Use Case**: Order status, approval workflows

```sql
CREATE TABLE sat_order_status (
    order_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    hash_diff CHAR(32) NOT NULL,
    status_code VARCHAR(20),
    status_description VARCHAR(100),
    status_reason VARCHAR(200),
    changed_by VARCHAR(50),
    record_source VARCHAR(50) NOT NULL,
    PRIMARY KEY (order_hk, load_date)
);
```

### 7. How do you handle slowly changing dimensions in Data Vault?

**Answer:** Data Vault naturally handles slowly changing dimensions through satellite versioning and effective dating.

#### **Type 1 SCD (Overwrite)**
- **Implementation**: Update hash_diff and attributes
- **Use Case**: Corrections, data quality fixes

```sql
-- Type 1: Overwrite (rare in Data Vault)
UPDATE sat_customer_details 
SET 
    hash_diff = MD5(CONCAT(first_name, last_name, 'corrected@email.com')),
    email = 'corrected@email.com',
    record_source = 'DATA_CORRECTION'
WHERE customer_hk = 'a1b2c3d4e5f6...' 
  AND load_end_date IS NULL;
```

#### **Type 2 SCD (Add New Version)**
- **Implementation**: Close current record, insert new version
- **Use Case**: Most common pattern in Data Vault

```sql
-- Type 2: Add new version (standard Data Vault pattern)
-- Step 1: Close current record
UPDATE sat_customer_details 
SET load_end_date = CURRENT_TIMESTAMP
WHERE customer_hk = 'a1b2c3d4e5f6...' 
  AND load_end_date IS NULL;

-- Step 2: Insert new version
INSERT INTO sat_customer_details VALUES (
    'a1b2c3d4e5f6...',                    -- customer_hk
    CURRENT_TIMESTAMP,                     -- load_date
    NULL,                                  -- load_end_date (current)
    'new_hash_diff_value',                 -- hash_diff
    'John',                                -- first_name
    'Doe',                                 -- last_name
    'john.doe@newemail.com',              -- email (changed)
    'CRM_SYSTEM'                          -- record_source
);
```

#### **Type 3 SCD (Add New Attribute)**
- **Implementation**: Add new columns to satellite
- **Use Case**: Track previous values

```sql
-- Type 3: Add new attribute
ALTER TABLE sat_customer_details 
ADD COLUMN previous_email VARCHAR(100);

-- Update with previous value tracking
INSERT INTO sat_customer_details VALUES (
    'a1b2c3d4e5f6...',
    CURRENT_TIMESTAMP,
    NULL,
    'updated_hash_diff',
    'John',
    'Doe',
    'john.doe@latest.com',                 -- current email
    'john.doe@previous.com',               -- previous email
    'CRM_SYSTEM'
);
```

#### **Querying Historical Data:**
```sql
-- Get current version
SELECT h.customer_bk, s.first_name, s.last_name, s.email
FROM hub_customer h
JOIN sat_customer_details s ON h.customer_hk = s.customer_hk
WHERE s.load_end_date IS NULL;

-- Get version as of specific date
SELECT h.customer_bk, s.first_name, s.last_name, s.email
FROM hub_customer h
JOIN sat_customer_details s ON h.customer_hk = s.customer_hk
WHERE s.load_date <= '2024-01-15 00:00:00'
  AND (s.load_end_date IS NULL OR s.load_end_date > '2024-01-15 00:00:00');

-- Get all versions (history)
SELECT h.customer_bk, s.load_date, s.load_end_date, s.email
FROM hub_customer h
JOIN sat_customer_details s ON h.customer_hk = s.customer_hk
ORDER BY h.customer_bk, s.load_date;
```

### 8. What is the Business Vault and how does it differ from Raw Vault?

**Answer:** The Business Vault is a layer built on top of the Raw Vault that contains calculated, derived, and business rule-driven data.

#### **Raw Vault vs Business Vault:**

| Aspect | Raw Vault | Business Vault |
|--------|-----------|----------------|
| **Purpose** | Store raw source data | Apply business logic |
| **Data Type** | As-is from source | Calculated/derived |
| **Business Rules** | None (hard rules only) | Soft business rules |
| **Changeability** | Immutable | Can change with business |
| **Auditability** | Complete source audit | Business logic audit |
| **Performance** | Optimized for loading | Optimized for business queries |

#### **Business Vault Components:**

**1. Calculated Satellites**
```sql
-- Business Vault: Customer Lifetime Value
CREATE TABLE bv_customer_lifetime_value (
    customer_hk CHAR(32) NOT NULL,
    calculation_date DATE NOT NULL,
    total_orders INTEGER,
    total_spent DECIMAL(10,2),
    avg_order_value DECIMAL(10,2),
    customer_lifetime_value DECIMAL(10,2),
    customer_segment VARCHAR(20),
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, calculation_date)
);

-- Business rule implementation
INSERT INTO bv_customer_lifetime_value
SELECT 
    c.customer_hk,
    CURRENT_DATE as calculation_date,
    COUNT(DISTINCT l.order_hk) as total_orders,
    SUM(od.total_amount) as total_spent,
    AVG(od.total_amount) as avg_order_value,
    SUM(od.total_amount) * 1.5 as customer_lifetime_value,  -- Business rule
    CASE 
        WHEN SUM(od.total_amount) > 10000 THEN 'Premium'
        WHEN SUM(od.total_amount) > 5000 THEN 'Gold'
        WHEN SUM(od.total_amount) > 1000 THEN 'Silver'
        ELSE 'Bronze'
    END as customer_segment,
    CURRENT_TIMESTAMP as load_date,
    'BUSINESS_VAULT' as record_source
FROM hub_customer c
JOIN link_customer_order l ON c.customer_hk = l.customer_hk
JOIN sat_order_details od ON l.order_hk = od.order_hk
WHERE od.load_end_date IS NULL
GROUP BY c.customer_hk;
```

**2. Derived Links**
```sql
-- Business Vault: Customer Hierarchy (derived from multiple sources)
CREATE TABLE bv_link_customer_hierarchy (
    customer_hierarchy_hk CHAR(32) PRIMARY KEY,
    parent_customer_hk CHAR(32) NOT NULL,
    child_customer_hk CHAR(32) NOT NULL,
    hierarchy_level INTEGER,
    hierarchy_type VARCHAR(20),
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL
);
```

**3. Business Keys**
```sql
-- Business Vault: Alternative business keys
CREATE TABLE bv_hub_customer_alt_bk (
    customer_hk CHAR(32) NOT NULL,
    alt_business_key VARCHAR(50),
    key_type VARCHAR(20),
    is_primary BOOLEAN,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, alt_business_key, key_type)
);
```

### 9. How do you implement Point-in-Time (PIT) tables?

**Answer:** Point-in-Time tables provide efficient access to historical data by pre-calculating the effective satellite records for specific time periods.

#### **Purpose of PIT Tables:**
- **Performance**: Avoid complex temporal joins
- **Simplicity**: Single table for historical queries
- **Consistency**: Guaranteed point-in-time consistency

#### **PIT Table Structure:**
```sql
-- Point-in-Time table for Customer
CREATE TABLE pit_customer (
    customer_hk CHAR(32) NOT NULL,
    snapshot_date DATE NOT NULL,
    sat_customer_details_load_date TIMESTAMP,
    sat_customer_address_load_date TIMESTAMP,
    sat_customer_phone_load_date TIMESTAMP,
    sat_customer_preferences_load_date TIMESTAMP,
    
    PRIMARY KEY (customer_hk, snapshot_date)
);
```

#### **PIT Table Population:**
```sql
-- Populate PIT table with daily snapshots
INSERT INTO pit_customer
SELECT 
    h.customer_hk,
    d.snapshot_date,
    -- Get the latest load_date for each satellite up to snapshot_date
    (SELECT MAX(load_date) 
     FROM sat_customer_details sd 
     WHERE sd.customer_hk = h.customer_hk 
     AND sd.load_date <= d.snapshot_date) as sat_customer_details_load_date,
     
    (SELECT MAX(load_date) 
     FROM sat_customer_address sa 
     WHERE sa.customer_hk = h.customer_hk 
     AND sa.load_date <= d.snapshot_date) as sat_customer_address_load_date,
     
    (SELECT MAX(load_date) 
     FROM sat_customer_phone sp 
     WHERE sp.customer_hk = h.customer_hk 
     AND sp.load_date <= d.snapshot_date) as sat_customer_phone_load_date,
     
    (SELECT MAX(load_date) 
     FROM sat_customer_preferences spr 
     WHERE spr.customer_hk = h.customer_hk 
     AND spr.load_date <= d.snapshot_date) as sat_customer_preferences_load_date
     
FROM hub_customer h
CROSS JOIN (
    -- Generate date range for snapshots
    SELECT DISTINCT DATE(load_date) as snapshot_date 
    FROM sat_customer_details
    UNION
    SELECT DISTINCT DATE(load_date) as snapshot_date 
    FROM sat_customer_address
    UNION
    SELECT DISTINCT DATE(load_date) as snapshot_date 
    FROM sat_customer_phone
) d
WHERE d.snapshot_date >= h.load_date;
```

#### **Using PIT Tables for Queries:**
```sql
-- Query customer data as of specific date using PIT
SELECT 
    h.customer_bk,
    sd.first_name,
    sd.last_name,
    sd.email,
    sa.address,
    sp.phone_number
FROM pit_customer p
JOIN hub_customer h ON p.customer_hk = h.customer_hk
LEFT JOIN sat_customer_details sd ON p.customer_hk = sd.customer_hk 
    AND p.sat_customer_details_load_date = sd.load_date
LEFT JOIN sat_customer_address sa ON p.customer_hk = sa.customer_hk 
    AND p.sat_customer_address_load_date = sa.load_date
LEFT JOIN sat_customer_phone sp ON p.customer_hk = sp.customer_hk 
    AND p.sat_customer_phone_load_date = sp.load_date
WHERE p.snapshot_date = '2024-01-15';
```

### 10. What are Bridge tables and when are they used?

**Answer:** Bridge tables resolve many-to-many relationships and provide efficient access patterns for complex queries.

#### **Purpose of Bridge Tables:**
- **Performance**: Pre-join related entities
- **Simplification**: Reduce complex multi-table joins
- **Aggregation**: Support dimensional modeling patterns

#### **Bridge Table Types:**

**1. Hub Bridge (Entity Grouping)**
```sql
-- Bridge table for customer groupings
CREATE TABLE bridge_customer_group (
    customer_group_hk CHAR(32) NOT NULL,
    customer_hk CHAR(32) NOT NULL,
    group_type VARCHAR(20),
    effective_date DATE,
    expiry_date DATE,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_group_hk, customer_hk, effective_date)
);

-- Population example
INSERT INTO bridge_customer_group
SELECT 
    MD5('PREMIUM_CUSTOMERS') as customer_group_hk,
    c.customer_hk,
    'PREMIUM' as group_type,
    CURRENT_DATE as effective_date,
    NULL as expiry_date,
    CURRENT_TIMESTAMP as load_date,
    'BUSINESS_RULES' as record_source
FROM hub_customer c
JOIN bv_customer_lifetime_value clv ON c.customer_hk = clv.customer_hk
WHERE clv.customer_segment = 'Premium';
```

**2. Link Bridge (Relationship Aggregation)**
```sql
-- Bridge table for order summaries
CREATE TABLE bridge_customer_order_summary (
    customer_hk CHAR(32) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_orders INTEGER,
    total_amount DECIMAL(10,2),
    avg_order_value DECIMAL(10,2),
    first_order_date DATE,
    last_order_date DATE,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, period_start, period_end)
);
```

**3. Satellite Bridge (Attribute Flattening)**
```sql
-- Bridge table flattening multiple satellites
CREATE TABLE bridge_customer_complete (
    customer_hk CHAR(32) NOT NULL,
    snapshot_date DATE NOT NULL,
    -- From customer details satellite
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    -- From address satellite
    street_address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(20),
    zip_code VARCHAR(10),
    -- From phone satellite
    primary_phone VARCHAR(20),
    mobile_phone VARCHAR(20),
    -- From preferences satellite
    communication_preference VARCHAR(20),
    marketing_opt_in BOOLEAN,
    
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, snapshot_date)
);
```

---

## Basic Level Questions (11-50)

### 11. How do you handle data quality in Data Vault?

**Answer:** Data Vault implements multiple layers of data quality controls throughout the architecture.

#### **Data Quality Layers:**

**1. Source System Quality (Pre-Vault)**
```sql
-- Staging area with quality checks
CREATE TABLE staging_customer_quality (
    customer_id VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    -- Quality flags
    is_valid_email BOOLEAN,
    is_valid_phone BOOLEAN,
    completeness_score DECIMAL(3,2),
    quality_status VARCHAR(20),
    error_description TEXT
);

-- Quality validation during staging
INSERT INTO staging_customer_quality
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    -- Email validation
    CASE WHEN email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' 
         THEN TRUE ELSE FALSE END as is_valid_email,
    -- Phone validation
    CASE WHEN phone REGEXP '^[0-9]{3}-[0-9]{3}-[0-9]{4}$' 
         THEN TRUE ELSE FALSE END as is_valid_phone,
    -- Completeness score
    (CASE WHEN customer_id IS NOT NULL THEN 0.2 ELSE 0 END +
     CASE WHEN first_name IS NOT NULL THEN 0.2 ELSE 0 END +
     CASE WHEN last_name IS NOT NULL THEN 0.2 ELSE 0 END +
     CASE WHEN email IS NOT NULL THEN 0.2 ELSE 0 END +
     CASE WHEN phone IS NOT NULL THEN 0.2 ELSE 0 END) as completeness_score,
    -- Overall quality status
    CASE 
        WHEN customer_id IS NULL THEN 'REJECTED'
        WHEN (first_name IS NULL AND last_name IS NULL) THEN 'REJECTED'
        ELSE 'ACCEPTED'
    END as quality_status,
    -- Error descriptions
    CONCAT_WS('; ',
        CASE WHEN customer_id IS NULL THEN 'Missing customer ID' END,
        CASE WHEN first_name IS NULL AND last_name IS NULL THEN 'Missing name' END,
        CASE WHEN email IS NOT NULL AND NOT email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' 
             THEN 'Invalid email format' END
    ) as error_description
FROM source_customer_data;
```

**2. Vault-Level Quality (Error Satellites)**
```sql
-- Error satellite to track data quality issues
CREATE TABLE sat_customer_errors (
    customer_hk CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    error_type VARCHAR(50),
    error_description TEXT,
    error_severity VARCHAR(20),
    source_column VARCHAR(50),
    source_value TEXT,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, load_date, error_type)
);

-- Load errors during vault processing
INSERT INTO sat_customer_errors
SELECT 
    MD5(UPPER(TRIM(customer_id))) as customer_hk,
    CURRENT_TIMESTAMP as load_date,
    'INVALID_EMAIL' as error_type,
    'Email format validation failed' as error_description,
    'WARNING' as error_severity,
    'email' as source_column,
    email as source_value,
    'DATA_QUALITY_CHECK' as record_source
FROM staging_customer_quality
WHERE is_valid_email = FALSE AND email IS NOT NULL;
```

**3. Business Vault Quality (Quality Metrics)**
```sql
-- Business vault quality metrics
CREATE TABLE bv_data_quality_metrics (
    table_name VARCHAR(100) NOT NULL,
    metric_date DATE NOT NULL,
    total_records BIGINT,
    complete_records BIGINT,
    incomplete_records BIGINT,
    error_records BIGINT,
    completeness_percentage DECIMAL(5,2),
    quality_score DECIMAL(5,2),
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (table_name, metric_date)
);

-- Calculate daily quality metrics
INSERT INTO bv_data_quality_metrics
SELECT 
    'sat_customer_details' as table_name,
    CURRENT_DATE as metric_date,
    COUNT(*) as total_records,
    COUNT(CASE WHEN first_name IS NOT NULL AND last_name IS NOT NULL 
               AND email IS NOT NULL THEN 1 END) as complete_records,
    COUNT(CASE WHEN first_name IS NULL OR last_name IS NULL 
               OR email IS NULL THEN 1 END) as incomplete_records,
    (SELECT COUNT(*) FROM sat_customer_errors 
     WHERE DATE(load_date) = CURRENT_DATE) as error_records,
    (COUNT(CASE WHEN first_name IS NOT NULL AND last_name IS NOT NULL 
                AND email IS NOT NULL THEN 1 END) * 100.0 / COUNT(*)) as completeness_percentage,
    -- Overall quality score calculation
    GREATEST(0, 100 - 
        (COUNT(CASE WHEN first_name IS NULL OR last_name IS NULL 
                    OR email IS NULL THEN 1 END) * 10.0 / COUNT(*)) -
        ((SELECT COUNT(*) FROM sat_customer_errors 
          WHERE DATE(load_date) = CURRENT_DATE) * 5.0 / COUNT(*))
    ) as quality_score,
    CURRENT_TIMESTAMP as load_date,
    'QUALITY_METRICS' as record_source
FROM sat_customer_details
WHERE DATE(load_date) = CURRENT_DATE;
```

### 12. What is the difference between hard and soft business rules in Data Vault?

**Answer:** Data Vault distinguishes between hard rules (immutable) and soft rules (changeable) to maintain flexibility and auditability.

#### **Hard Business Rules (Raw Vault)**
- **Definition**: Immutable rules that never change
- **Location**: Applied during Raw Vault loading
- **Examples**: Data type conversions, basic validations
- **Characteristics**: Cannot be modified without reloading history

```sql
-- Hard rule example: Data type standardization
INSERT INTO hub_customer (customer_hk, customer_bk, load_date, record_source)
SELECT 
    MD5(UPPER(TRIM(customer_id))) as customer_hk,
    UPPER(TRIM(customer_id)) as customer_bk,  -- Hard rule: always uppercase
    CURRENT_TIMESTAMP as load_date,
    'CRM_SYSTEM' as record_source
FROM staging_customer
WHERE customer_id IS NOT NULL  -- Hard rule: must have business key
  AND LENGTH(TRIM(customer_id)) > 0;  -- Hard rule: not empty
```

#### **Soft Business Rules (Business Vault)**
- **Definition**: Changeable rules that evolve with business needs
- **Location**: Applied in Business Vault layer
- **Examples**: Calculations, categorizations, derived values
- **Characteristics**: Can be modified and recalculated

```sql
-- Soft rule example: Customer segmentation (can change over time)
CREATE TABLE bv_customer_segmentation_v1 (
    customer_hk CHAR(32) NOT NULL,
    calculation_date DATE NOT NULL,
    total_spent DECIMAL(10,2),
    segment VARCHAR(20),
    segment_logic_version VARCHAR(10),
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, calculation_date, segment_logic_version)
);

-- Version 1 of segmentation logic
INSERT INTO bv_customer_segmentation_v1
SELECT 
    customer_hk,
    CURRENT_DATE as calculation_date,
    total_spent,
    CASE 
        WHEN total_spent >= 10000 THEN 'PREMIUM'
        WHEN total_spent >= 5000 THEN 'GOLD'
        WHEN total_spent >= 1000 THEN 'SILVER'
        ELSE 'BRONZE'
    END as segment,
    'V1.0' as segment_logic_version,
    CURRENT_TIMESTAMP as load_date,
    'BUSINESS_RULES_V1' as record_source
FROM customer_spending_summary;

-- Version 2 of segmentation logic (changed business rules)
INSERT INTO bv_customer_segmentation_v2
SELECT 
    customer_hk,
    CURRENT_DATE as calculation_date,
    total_spent,
    order_frequency,
    CASE 
        WHEN total_spent >= 15000 AND order_frequency >= 12 THEN 'PLATINUM'
        WHEN total_spent >= 8000 THEN 'PREMIUM'
        WHEN total_spent >= 3000 THEN 'GOLD'
        WHEN total_spent >= 500 THEN 'SILVER'
        ELSE 'BRONZE'
    END as segment,
    'V2.0' as segment_logic_version,
    CURRENT_TIMESTAMP as load_date,
    'BUSINESS_RULES_V2' as record_source
FROM customer_spending_summary;
```

#### **Rule Comparison:**

| Aspect | Hard Rules | Soft Rules |
|--------|------------|------------|
| **Location** | Raw Vault | Business Vault |
| **Changeability** | Immutable | Changeable |
| **Impact of Change** | Requires full reload | Recalculation only |
| **Examples** | Data types, formats | Calculations, categories |
| **Auditability** | Source system audit | Business logic audit |
| **Performance** | Load-time impact | Query-time flexibility |

### 13. How do you implement data lineage in Data Vault?

**Answer:** Data Vault provides natural data lineage through its architecture and metadata tracking capabilities.

#### **Built-in Lineage Features:**
- **Record Source**: Tracks which system provided each record
- **Load Date**: When data was loaded
- **Hash Keys**: Link data across tables
- **Satellite Versioning**: Shows data evolution over time

#### **Lineage Tracking Implementation:**

**1. Enhanced Record Source Tracking**
```sql
-- Enhanced record source with detailed lineage
CREATE TABLE hub_customer (
    customer_hk CHAR(32) PRIMARY KEY,
    customer_bk VARCHAR(50) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(50) NOT NULL,
    -- Enhanced lineage fields
    source_system VARCHAR(50),
    source_table VARCHAR(100),
    source_file VARCHAR(200),
    batch_id VARCHAR(50),
    etl_process_id VARCHAR(50)
);

-- Loading with detailed lineage
INSERT INTO hub_customer 
SELECT 
    MD5(UPPER(TRIM(customer_id))) as customer_hk,
    customer_id as customer_bk,
    CURRENT_TIMESTAMP as load_date,
    'CRM_SYSTEM' as record_source,
    'SALESFORCE' as source_system,
    'Account' as source_table,
    'customer_export_20240101.csv' as source_file,
    'BATCH_20240101_001' as batch_id,
    'ETL_CUSTOMER_DAILY' as etl_process_id
FROM staging_customer;
```

**2. Lineage Metadata Tables**
```sql
-- Data lineage tracking table
CREATE TABLE data_lineage (
    lineage_id VARCHAR(50) PRIMARY KEY,
    source_table VARCHAR(100),
    target_table VARCHAR(100),
    transformation_type VARCHAR(50),
    transformation_logic TEXT,
    dependency_level INTEGER,
    load_date TIMESTAMP NOT NULL,
    created_by VARCHAR(50)
);

-- Process lineage tracking
CREATE TABLE process_lineage (
    process_id VARCHAR(50) PRIMARY KEY,
    process_name VARCHAR(100),
    process_type VARCHAR(50),
    input_tables TEXT,
    output_tables TEXT,
    transformation_rules TEXT,
    execution_date TIMESTAMP,
    execution_status VARCHAR(20),
    execution_duration INTEGER
);

-- Column lineage tracking
CREATE TABLE column_lineage (
    lineage_id VARCHAR(50),
    source_column VARCHAR(100),
    target_column VARCHAR(100),
    transformation_function VARCHAR(200),
    data_type_source VARCHAR(50),
    data_type_target VARCHAR(50),
    
    FOREIGN KEY (lineage_id) REFERENCES data_lineage(lineage_id)
);
```

**3. Lineage Query Examples**
```sql
-- Trace data lineage for a specific customer
WITH RECURSIVE lineage_trace AS (
    -- Start with the target record
    SELECT 
        'sat_customer_details' as table_name,
        customer_hk,
        record_source,
        load_date,
        1 as level
    FROM sat_customer_details 
    WHERE customer_hk = 'a1b2c3d4e5f6...'
    
    UNION ALL
    
    -- Trace back through dependencies
    SELECT 
        dl.source_table as table_name,
        lt.customer_hk,
        'DERIVED' as record_source,
        lt.load_date,
        lt.level + 1
    FROM lineage_trace lt
    JOIN data_lineage dl ON lt.table_name = dl.target_table
    WHERE lt.level < 10  -- Prevent infinite recursion
)
SELECT * FROM lineage_trace ORDER BY level, load_date;

-- Get transformation history for a business key
SELECT 
    h.customer_bk,
    s.load_date,
    s.record_source,
    s.source_system,
    s.etl_process_id,
    'Customer details updated' as change_description
FROM hub_customer h
JOIN sat_customer_details s ON h.customer_hk = s.customer_hk
WHERE h.customer_bk = 'CUST001'
ORDER BY s.load_date;
```

### 14. What are the advantages and disadvantages of Data Vault?

**Answer:** Data Vault offers significant benefits but also has some limitations to consider.

#### **Advantages:**

**1. Flexibility and Agility**
- Easy to accommodate changing business requirements
- New data sources can be added without impacting existing structures
- Schema changes don't require rebuilding existing data

**2. Auditability and Compliance**
- Complete historical tracking of all changes
- Immutable raw data layer
- Full data lineage and provenance

**3. Scalability and Performance**
- Parallel loading capabilities
- Insert-only operations are faster
- Can scale horizontally across multiple systems

**4. Integration-Friendly**
- Handles multiple source systems naturally
- Consistent approach across different data types
- Supports real-time and batch processing

#### **Disadvantages:**

**1. Complexity**
- Requires specialized knowledge and training
- More complex than traditional approaches initially
- Steeper learning curve for developers

**2. Storage Overhead**
- More tables and relationships than dimensional models
- Historical data storage requirements
- Potential for data duplication

**3. Query Complexity**
- Complex joins required for business queries
- Need for Information Marts for end-user access
- Point-in-time queries can be challenging

**4. Tool Support**
- Limited native support in some BI tools
- May require custom ETL development
- Fewer pre-built accelerators available

#### **Comparison Summary:**

| Aspect | Advantage | Disadvantage |
|--------|-----------|--------------|
| **Development Speed** | Fast for new sources | Slower initial setup |
| **Maintenance** | Low ongoing maintenance | High initial complexity |
| **Performance** | Excellent for loading | May need optimization for queries |
| **Flexibility** | Extremely flexible | Can be over-engineered |
| **Skills Required** | Specialized but learnable | Requires training investment |
| **Tool Support** | Growing ecosystem | Limited compared to dimensional |

### 15. How do you handle referential integrity in Data Vault?

**Answer:** Data Vault maintains referential integrity through loading sequences, validation checks, and error handling mechanisms.

#### **Referential Integrity Strategies:**

**1. Loading Sequence Enforcement**
```sql
-- Ensure hubs exist before loading links
INSERT INTO link_customer_order (customer_order_hk, customer_hk, order_hk, load_date, record_source)
SELECT DISTINCT
    MD5(CONCAT(
        MD5(UPPER(TRIM(s.customer_id))),
        MD5(UPPER(TRIM(s.order_id)))
    )) as customer_order_hk,
    MD5(UPPER(TRIM(s.customer_id))) as customer_hk,
    MD5(UPPER(TRIM(s.order_id))) as order_hk,
    CURRENT_TIMESTAMP as load_date,
    'ORDER_SYSTEM' as record_source
FROM staging.order_data s
-- Referential integrity checks
WHERE EXISTS (
    SELECT 1 FROM hub_customer h 
    WHERE h.customer_hk = MD5(UPPER(TRIM(s.customer_id)))
)
AND EXISTS (
    SELECT 1 FROM hub_order o 
    WHERE o.order_hk = MD5(UPPER(TRIM(s.order_id)))
)
-- Avoid duplicates
AND NOT EXISTS (
    SELECT 1 FROM link_customer_order l 
    WHERE l.customer_order_hk = MD5(CONCAT(
        MD5(UPPER(TRIM(s.customer_id))),
        MD5(UPPER(TRIM(s.order_id)))
    ))
);
```

**2. Orphan Record Handling**
```sql
-- Create staging table for orphaned records
CREATE TABLE staging_orphaned_records (
    source_table VARCHAR(100),
    source_key VARCHAR(200),
    parent_table VARCHAR(100),
    missing_parent_key VARCHAR(200),
    error_description TEXT,
    load_date TIMESTAMP,
    resolution_status VARCHAR(20)
);

-- Identify and log orphaned link records
INSERT INTO staging_orphaned_records
SELECT 
    'link_customer_order' as source_table,
    CONCAT(s.customer_id, '|', s.order_id) as source_key,
    'hub_customer' as parent_table,
    s.customer_id as missing_parent_key,
    'Customer hub record missing for link' as error_description,
    CURRENT_TIMESTAMP as load_date,
    'PENDING' as resolution_status
FROM staging.order_data s
WHERE NOT EXISTS (
    SELECT 1 FROM hub_customer h 
    WHERE h.customer_hk = MD5(UPPER(TRIM(s.customer_id)))
);
```

**3. Foreign Key Constraints (Optional)**
```sql
-- Add foreign key constraints for strict enforcement
ALTER TABLE link_customer_order 
ADD CONSTRAINT fk_link_customer_order_customer 
FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk);

ALTER TABLE link_customer_order 
ADD CONSTRAINT fk_link_customer_order_order 
FOREIGN KEY (order_hk) REFERENCES hub_order(order_hk);

ALTER TABLE sat_customer_details 
ADD CONSTRAINT fk_sat_customer_details_hub 
FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk);
```

**4. Referential Integrity Monitoring**
```sql
-- Monitor referential integrity violations
CREATE VIEW v_referential_integrity_check AS
SELECT 
    'link_customer_order' as table_name,
    'Missing customer hub' as violation_type,
    COUNT(*) as violation_count
FROM link_customer_order l
LEFT JOIN hub_customer h ON l.customer_hk = h.customer_hk
WHERE h.customer_hk IS NULL

UNION ALL

SELECT 
    'sat_customer_details' as table_name,
    'Missing customer hub' as violation_type,
    COUNT(*) as violation_count
FROM sat_customer_details s
LEFT JOIN hub_customer h ON s.customer_hk = h.customer_hk
WHERE h.customer_hk IS NULL;

-- Daily referential integrity report
SELECT 
    table_name,
    violation_type,
    violation_count,
    CURRENT_DATE as check_date
FROM v_referential_integrity_check
WHERE violation_count > 0;
```

### 16-50. Additional Basic Level Questions

**16. What is the purpose of the record_source field?**
**Answer:** Tracks which source system provided each record for auditability and lineage.

**17. How do you handle duplicate business keys from different sources?**
**Answer:** Use composite business keys or source-specific hubs with same-as links.

**18. What is a same-as link and when is it used?**
**Answer:** Links that identify the same business entity across different source systems.

**19. How do you implement data archiving in Data Vault?**
**Answer:** Use tiered storage and retention policies based on load_date and business rules.

**20. What are the naming conventions for Data Vault objects?**
**Answer:** hub_, link_, sat_, pit_, bridge_ prefixes with descriptive names.

**21. How do you handle NULL values in Data Vault?**
**Answer:** Store NULLs as-is in satellites, use hash diff to detect changes including NULL transitions.

**22. What is the difference between a hub and a reference hub?**
**Answer:** Reference hubs store lookup/master data, regular hubs store transactional entities.

**23. How do you implement data validation rules?**
**Answer:** Use staging area validation, error satellites, and quality metrics tracking.

**24. What is the role of staging area in Data Vault?**
**Answer:** Temporary storage for data cleansing, validation, and transformation before vault loading.

**25. How do you handle late-arriving data?**
**Answer:** Data Vault naturally handles late data through insert-only pattern and effective dating.

**26. What are the different types of links in Data Vault?**
**Answer:** Transactional links, hierarchical links, same-as links, and non-historized links.

**27. How do you implement data retention policies?**
**Answer:** Use automated processes based on load_date and business requirements for archival.

**28. What is the purpose of hash keys in performance optimization?**
**Answer:** Fixed-length keys improve join performance and enable consistent partitioning.

**29. How do you handle schema changes in source systems?**
**Answer:** Add new satellites or extend existing ones without impacting current structure.

**30. What is the difference between effective dating and load dating?**
**Answer:** Load dating tracks when data entered the vault, effective dating tracks business validity.

**31. How do you implement data masking in Data Vault?**
**Answer:** Apply masking in Information Marts while preserving raw data in vault.

**32. What are the security considerations for Data Vault?**
**Answer:** Row-level security, column masking, audit logging, and access controls.

**33. How do you handle data from real-time sources?**
**Answer:** Use micro-batch loading or streaming ETL with same Data Vault patterns.

**34. What is the role of business keys in Data Vault?**
**Answer:** Natural identifiers from source systems that provide business meaning.

**35. How do you implement data profiling in Data Vault?**
**Answer:** Profile data in staging area and track quality metrics in business vault.

**36. What are the different loading patterns for satellites?**
**Answer:** Full load, incremental load, change data capture, and real-time streaming.

**37. How do you handle hierarchical data in Data Vault?**
**Answer:** Use hierarchical links and recursive relationships with level indicators.

**38. What is the purpose of load_end_date in satellites?**
**Answer:** Marks when a record became inactive, NULL indicates current active record.

**39. How do you implement data compression in Data Vault?**
**Answer:** Use database compression features and columnar storage for satellites.

**40. What are the monitoring requirements for Data Vault?**
**Answer:** Load statistics, data quality metrics, referential integrity, and performance monitoring.

**41. How do you handle multi-source data conflicts?**
**Answer:** Use source-specific satellites and business vault for conflict resolution.

**42. What is the role of Information Marts in Data Vault?**
**Answer:** Dimensional models built from vault for specific business reporting needs.

**43. How do you implement data governance in Data Vault?**
**Answer:** Metadata management, data lineage tracking, and policy enforcement.

**44. What are the backup and recovery strategies for Data Vault?**
**Answer:** Point-in-time recovery, incremental backups, and disaster recovery planning.

**45. How do you handle data migration to Data Vault?**
**Answer:** Phased approach with parallel running and gradual cutover strategies.

**46. What is the impact of Data Vault on ETL processes?**
**Answer:** Simplified ETL with standardized patterns and parallel processing capabilities.

**47. How do you implement data cataloging for Data Vault?**
**Answer:** Automated metadata extraction and business glossary integration.

**48. What are the testing strategies for Data Vault?**
**Answer:** Unit testing for transformations, integration testing, and data quality validation.

**49. How do you handle performance tuning in Data Vault?**
**Answer:** Indexing strategies, partitioning, and query optimization techniques.

**50. What is the future of Data Vault methodology?**
**Answer:** Cloud-native implementations, automation tools, and integration with modern data platforms.

---

*[Continuing with remaining sections in next parts to avoid file size issues...]*

## Intermediate Level Questions (51-100)

### 51. How do you implement incremental loading in Data Vault?

**Answer:** Incremental loading in Data Vault uses change detection and delta processing to load only new or changed records.

#### **Incremental Loading Strategies:**

**1. Timestamp-Based Incremental Loading**
```sql
-- Track last successful load timestamp
CREATE TABLE etl_control (
    table_name VARCHAR(100) PRIMARY KEY,
    last_load_timestamp TIMESTAMP,
    last_load_status VARCHAR(20),
    records_processed BIGINT,
    load_date TIMESTAMP
);

-- Incremental hub loading
INSERT INTO hub_customer (customer_hk, customer_bk, load_date, record_source)
SELECT DISTINCT
    MD5(UPPER(TRIM(customer_id))) as customer_hk,
    customer_id as customer_bk,
    CURRENT_TIMESTAMP as load_date,
    'CRM_SYSTEM' as record_source
FROM staging.customer_data s
WHERE s.last_modified > (
    SELECT COALESCE(last_load_timestamp, '1900-01-01') 
    FROM etl_control 
    WHERE table_name = 'hub_customer'
)
AND NOT EXISTS (
    SELECT 1 FROM hub_customer h 
    WHERE h.customer_hk = MD5(UPPER(TRIM(s.customer_id)))
);

-- Update control table
UPDATE etl_control 
SET 
    last_load_timestamp = CURRENT_TIMESTAMP,
    last_load_status = 'SUCCESS',
    records_processed = @@ROWCOUNT,
    load_date = CURRENT_TIMESTAMP
WHERE table_name = 'hub_customer';
```

**2. Change Data Capture (CDC) Integration**
```sql
-- CDC-based satellite loading
WITH cdc_changes AS (
    SELECT 
        customer_id,
        first_name,
        last_name,
        email,
        phone,
        cdc_operation,
        cdc_timestamp
    FROM cdc.customer_changes
    WHERE cdc_timestamp > (
        SELECT COALESCE(last_load_timestamp, '1900-01-01') 
        FROM etl_control 
        WHERE table_name = 'sat_customer_details'
    )
),
processed_changes AS (
    SELECT 
        MD5(UPPER(TRIM(customer_id))) as customer_hk,
        MD5(CONCAT(
            COALESCE(first_name, ''),
            COALESCE(last_name, ''),
            COALESCE(email, ''),
            COALESCE(phone, '')
        )) as hash_diff,
        first_name,
        last_name,
        email,
        phone,
        cdc_timestamp as load_date,
        'CRM_CDC' as record_source
    FROM cdc_changes
    WHERE cdc_operation IN ('INSERT', 'UPDATE')
)
-- Insert only records with different hash_diff
INSERT INTO sat_customer_details 
SELECT p.*
FROM processed_changes p
LEFT JOIN sat_customer_details s ON p.customer_hk = s.customer_hk 
    AND s.load_end_date IS NULL
WHERE s.hash_diff IS NULL OR s.hash_diff != p.hash_diff;
```

**3. Watermark-Based Loading**
```sql
-- High-water mark tracking
CREATE TABLE load_watermarks (
    source_system VARCHAR(50),
    table_name VARCHAR(100),
    watermark_column VARCHAR(50),
    watermark_value VARCHAR(200),
    watermark_timestamp TIMESTAMP,
    
    PRIMARY KEY (source_system, table_name, watermark_column)
);

-- Incremental loading with watermark
DECLARE @last_watermark VARCHAR(200);
SELECT @last_watermark = watermark_value 
FROM load_watermarks 
WHERE source_system = 'CRM' AND table_name = 'customers';

-- Load incremental data
INSERT INTO hub_customer (customer_hk, customer_bk, load_date, record_source)
SELECT DISTINCT
    MD5(UPPER(TRIM(customer_id))) as customer_hk,
    customer_id as customer_bk,
    CURRENT_TIMESTAMP as load_date,
    'CRM_SYSTEM' as record_source
FROM staging.customer_data s
WHERE s.row_version > @last_watermark
AND NOT EXISTS (
    SELECT 1 FROM hub_customer h 
    WHERE h.customer_hk = MD5(UPPER(TRIM(s.customer_id)))
);

-- Update watermark
UPDATE load_watermarks 
SET 
    watermark_value = (SELECT MAX(row_version) FROM staging.customer_data),
    watermark_timestamp = CURRENT_TIMESTAMP
WHERE source_system = 'CRM' AND table_name = 'customers';
```

### 52. How do you handle multi-active satellites with complex business rules?

**Answer:** Multi-active satellites require careful design to handle multiple concurrent records with business-specific logic.

#### **Advanced Multi-Active Patterns:**

**1. Weighted Multi-Active Satellite**
```sql
-- Customer skills with proficiency levels
CREATE TABLE sat_customer_skills_ma (
    customer_hk CHAR(32) NOT NULL,
    skill_code VARCHAR(20) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    hash_diff CHAR(32) NOT NULL,
    skill_name VARCHAR(100),
    proficiency_level INTEGER,
    years_experience INTEGER,
    certification_level VARCHAR(20),
    is_primary_skill BOOLEAN,
    skill_weight DECIMAL(3,2),
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, skill_code, load_date)
);

-- Business rule: Ensure skill weights sum to 1.0 per customer
CREATE TRIGGER trg_validate_skill_weights
BEFORE INSERT ON sat_customer_skills_ma
FOR EACH ROW
BEGIN
    DECLARE total_weight DECIMAL(5,2);
    
    SELECT SUM(skill_weight) INTO total_weight
    FROM sat_customer_skills_ma
    WHERE customer_hk = NEW.customer_hk
      AND load_end_date IS NULL
      AND skill_code != NEW.skill_code;
    
    IF (COALESCE(total_weight, 0) + NEW.skill_weight) > 1.0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Total skill weights cannot exceed 1.0';
    END IF;
END;
```

**2. Hierarchical Multi-Active Satellite**
```sql
-- Customer addresses with hierarchy
CREATE TABLE sat_customer_address_ma (
    customer_hk CHAR(32) NOT NULL,
    address_type VARCHAR(20) NOT NULL,
    address_sequence INTEGER NOT NULL,
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    hash_diff CHAR(32) NOT NULL,
    address_line1 VARCHAR(100),
    address_line2 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(20),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    is_primary BOOLEAN,
    is_billing BOOLEAN,
    is_shipping BOOLEAN,
    priority_order INTEGER,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, address_type, address_sequence, load_date)
);

-- Business rule implementation for address priority
WITH address_priority AS (
    SELECT 
        customer_hk,
        address_type,
        address_sequence,
        ROW_NUMBER() OVER (
            PARTITION BY customer_hk 
            ORDER BY 
                CASE WHEN is_primary THEN 1 ELSE 2 END,
                priority_order,
                load_date DESC
        ) as calculated_priority
    FROM sat_customer_address_ma
    WHERE load_end_date IS NULL
)
UPDATE sat_customer_address_ma s
SET priority_order = ap.calculated_priority
FROM address_priority ap
WHERE s.customer_hk = ap.customer_hk
  AND s.address_type = ap.address_type
  AND s.address_sequence = ap.address_sequence
  AND s.load_end_date IS NULL;
```

**3. Conditional Multi-Active Satellite**
```sql
-- Customer phone numbers with business rules
CREATE TABLE sat_customer_phone_ma (
    customer_hk CHAR(32) NOT NULL,
    phone_type VARCHAR(20) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    hash_diff CHAR(32) NOT NULL,
    phone_number VARCHAR(20),
    country_code VARCHAR(5),
    extension VARCHAR(10),
    is_primary BOOLEAN,
    is_verified BOOLEAN,
    verification_date TIMESTAMP,
    can_text BOOLEAN,
    can_call BOOLEAN,
    preferred_time_start TIME,
    preferred_time_end TIME,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (customer_hk, phone_type, load_date),
    
    -- Business rule constraints
    CONSTRAINT chk_primary_phone CHECK (
        NOT is_primary OR phone_type IN ('HOME', 'MOBILE', 'WORK')
    ),
    CONSTRAINT chk_verified_phone CHECK (
        NOT is_verified OR verification_date IS NOT NULL
    )
);

-- Ensure only one primary phone per customer
CREATE UNIQUE INDEX idx_one_primary_phone 
ON sat_customer_phone_ma (customer_hk) 
WHERE is_primary = TRUE AND load_end_date IS NULL;
```

### 53. How do you implement data vault automation and code generation?

**Answer:** Data Vault automation reduces manual effort and ensures consistency through metadata-driven code generation.

#### **Automation Approaches:**

**1. Metadata-Driven Table Generation**
```python
# Python script for Data Vault table generation
import yaml
import jinja2

class DataVaultGenerator:
    def __init__(self, metadata_file):
        with open(metadata_file, 'r') as f:
            self.metadata = yaml.safe_load(f)
        
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('templates')
        )
    
    def generate_hub(self, hub_config):
        template = self.env.get_template('hub_template.sql')
        
        return template.render(
            hub_name=hub_config['name'],
            business_key=hub_config['business_key'],
            columns=hub_config.get('additional_columns', [])
        )
    
    def generate_satellite(self, sat_config):
        template = self.env.get_template('satellite_template.sql')
        
        return template.render(
            satellite_name=sat_config['name'],
            parent_hub=sat_config['parent_hub'],
            attributes=sat_config['attributes'],
            is_multi_active=sat_config.get('multi_active', False),
            multi_active_key=sat_config.get('multi_active_key')
        )
    
    def generate_loading_procedures(self, entity_config):
        template = self.env.get_template('loading_procedure_template.sql')
        
        return template.render(
            entity_name=entity_config['name'],
            source_table=entity_config['source_table'],
            business_key_mapping=entity_config['business_key_mapping'],
            attribute_mappings=entity_config['attribute_mappings']
        )

# Metadata configuration example
metadata_config = """
entities:
  customer:
    hub:
      name: hub_customer
      business_key: customer_id
      additional_columns:
        - name: customer_type
          type: VARCHAR(20)
    
    satellites:
      - name: sat_customer_details
        parent_hub: hub_customer
        attributes:
          - name: first_name
            type: VARCHAR(50)
          - name: last_name
            type: VARCHAR(50)
          - name: email
            type: VARCHAR(100)
      
      - name: sat_customer_phone_ma
        parent_hub: hub_customer
        multi_active: true
        multi_active_key: phone_type
        attributes:
          - name: phone_number
            type: VARCHAR(20)
          - name: is_primary
            type: BOOLEAN
    
    loading:
      source_table: staging.customer_data
      business_key_mapping:
        customer_id: customer_id
      attribute_mappings:
        first_name: first_name
        last_name: last_name
        email: email_address
"""
```

**2. ETL Code Generation Templates**
```sql
-- Jinja2 template for hub loading procedure
-- File: templates/hub_loading_template.sql
CREATE OR REPLACE PROCEDURE load_{{ hub_name }}()
LANGUAGE plpgsql
AS $$
DECLARE
    v_rows_processed INTEGER := 0;
BEGIN
    -- Load {{ hub_name }}
    INSERT INTO {{ hub_name }} (
        {{ business_key_column }}_hk,
        {{ business_key_column }}_bk,
        load_date,
        record_source
    )
    SELECT DISTINCT
        MD5(UPPER(TRIM({{ source_business_key }}))) as {{ business_key_column }}_hk,
        {{ source_business_key }} as {{ business_key_column }}_bk,
        CURRENT_TIMESTAMP as load_date,
        '{{ source_system }}' as record_source
    FROM {{ source_table }} s
    WHERE {{ source_business_key }} IS NOT NULL
      AND LENGTH(TRIM({{ source_business_key }})) > 0
      AND NOT EXISTS (
          SELECT 1 FROM {{ hub_name }} h 
          WHERE h.{{ business_key_column }}_hk = MD5(UPPER(TRIM(s.{{ source_business_key }})))
      );
    
    GET DIAGNOSTICS v_rows_processed = ROW_COUNT;
    
    -- Log results
    INSERT INTO etl_log (
        procedure_name,
        table_name,
        rows_processed,
        execution_time,
        status
    ) VALUES (
        'load_{{ hub_name }}',
        '{{ hub_name }}',
        v_rows_processed,
        CURRENT_TIMESTAMP,
        'SUCCESS'
    );
    
    RAISE NOTICE '{{ hub_name }}: % rows processed', v_rows_processed;
END;
$$;
```

**3. Automated Testing Generation**
```python
# Test case generation for Data Vault structures
class DataVaultTestGenerator:
    def generate_hub_tests(self, hub_config):
        return f"""
-- Test cases for {hub_config['name']}
-- Test 1: Duplicate business key handling
INSERT INTO staging.{hub_config['source_table']} VALUES 
('TEST001', 'Test Customer 1'),
('TEST001', 'Test Customer 1 Duplicate');

CALL load_{hub_config['name']}();

-- Verify only one record created
SELECT COUNT(*) as record_count 
FROM {hub_config['name']} 
WHERE {hub_config['business_key']}_bk = 'TEST001';
-- Expected: 1

-- Test 2: NULL business key handling
INSERT INTO staging.{hub_config['source_table']} VALUES 
(NULL, 'Test Customer with NULL key');

CALL load_{hub_config['name']}();

-- Verify NULL key not loaded
SELECT COUNT(*) as null_key_count 
FROM {hub_config['name']} 
WHERE {hub_config['business_key']}_bk IS NULL;
-- Expected: 0
"""
    
    def generate_satellite_tests(self, sat_config):
        return f"""
-- Test cases for {sat_config['name']}
-- Test 1: Change detection
INSERT INTO staging.{sat_config['source_table']} VALUES 
('TEST001', 'John', 'Doe', 'john@email.com');

CALL load_{sat_config['name']}();

-- Update data
UPDATE staging.{sat_config['source_table']} 
SET email = 'john.doe@newemail.com' 
WHERE customer_id = 'TEST001';

CALL load_{sat_config['name']}();

-- Verify two versions exist
SELECT COUNT(*) as version_count 
FROM {sat_config['name']} s
JOIN hub_customer h ON s.customer_hk = h.customer_hk
WHERE h.customer_bk = 'TEST001';
-- Expected: 2
"""
```

### 54. How do you implement real-time Data Vault loading?

**Answer:** Real-time Data Vault loading uses streaming technologies and micro-batch processing to maintain near real-time data availability.

#### **Real-Time Loading Architectures:**

**1. Kafka-Based Streaming**
```python
# Apache Kafka consumer for real-time Data Vault loading
from kafka import KafkaConsumer
import json
import hashlib
import psycopg2
from datetime import datetime

class RealTimeDataVaultLoader:
    def __init__(self, db_config, kafka_config):
        self.db_conn = psycopg2.connect(**db_config)
        self.consumer = KafkaConsumer(
            'customer_changes',
            bootstrap_servers=kafka_config['servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
    
    def generate_hash_key(self, business_key):
        return hashlib.md5(str(business_key).upper().strip().encode()).hexdigest()
    
    def generate_hash_diff(self, attributes):
        concat_attrs = ''.join([str(v) for v in attributes.values() if v is not None])
        return hashlib.md5(concat_attrs.encode()).hexdigest()
    
    def load_hub_customer(self, customer_data):
        customer_hk = self.generate_hash_key(customer_data['customer_id'])
        
        cursor = self.db_conn.cursor()
        cursor.execute("""
            INSERT INTO hub_customer (customer_hk, customer_bk, load_date, record_source)
            SELECT %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM hub_customer WHERE customer_hk = %s
            )
        """, (customer_hk, customer_data['customer_id'], datetime.now(), 
              'KAFKA_STREAM', customer_hk))
        
        self.db_conn.commit()
        cursor.close()
    
    def load_satellite_customer_details(self, customer_data):
        customer_hk = self.generate_hash_key(customer_data['customer_id'])
        
        attributes = {
            'first_name': customer_data.get('first_name'),
            'last_name': customer_data.get('last_name'),
            'email': customer_data.get('email'),
            'phone': customer_data.get('phone')
        }
        
        hash_diff = self.generate_hash_diff(attributes)
        
        cursor = self.db_conn.cursor()
        
        # Check if change is needed
        cursor.execute("""
            SELECT hash_diff FROM sat_customer_details 
            WHERE customer_hk = %s AND load_end_date IS NULL
        """, (customer_hk,))
        
        current_hash = cursor.fetchone()
        
        if not current_hash or current_hash[0] != hash_diff:
            # Close current record
            cursor.execute("""
                UPDATE sat_customer_details 
                SET load_end_date = %s 
                WHERE customer_hk = %s AND load_end_date IS NULL
            """, (datetime.now(), customer_hk))
            
            # Insert new record
            cursor.execute("""
                INSERT INTO sat_customer_details 
                (customer_hk, load_date, hash_diff, first_name, last_name, email, phone, record_source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (customer_hk, datetime.now(), hash_diff, 
                  attributes['first_name'], attributes['last_name'],
                  attributes['email'], attributes['phone'], 'KAFKA_STREAM'))
        
        self.db_conn.commit()
        cursor.close()
    
    def process_messages(self):
        for message in self.consumer:
            try:
                customer_data = message.value
                
                # Load hub first
                self.load_hub_customer(customer_data)
                
                # Load satellite
                self.load_satellite_customer_details(customer_data)
                
                print(f"Processed customer: {customer_data['customer_id']}")
                
            except Exception as e:
                print(f"Error processing message: {e}")
                # Log error or send to dead letter queue

# Usage
loader = RealTimeDataVaultLoader(
    db_config={'host': 'localhost', 'database': 'datavault', 'user': 'user', 'password': 'pass'},
    kafka_config={'servers': ['localhost:9092']}
)
loader.process_messages()
```

**2. Change Data Capture (CDC) Integration**
```sql
-- CDC-based real-time loading procedure
CREATE OR REPLACE FUNCTION process_cdc_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- Handle INSERT operations
    IF TG_OP = 'INSERT' THEN
        -- Load hub
        INSERT INTO hub_customer (customer_hk, customer_bk, load_date, record_source)
        SELECT 
            MD5(UPPER(TRIM(NEW.customer_id))),
            NEW.customer_id,
            CURRENT_TIMESTAMP,
            'CDC_REALTIME'
        WHERE NOT EXISTS (
            SELECT 1 FROM hub_customer 
            WHERE customer_hk = MD5(UPPER(TRIM(NEW.customer_id)))
        );
        
        -- Load satellite
        INSERT INTO sat_customer_details (
            customer_hk, load_date, hash_diff, first_name, last_name, email, record_source
        )
        VALUES (
            MD5(UPPER(TRIM(NEW.customer_id))),
            CURRENT_TIMESTAMP,
            MD5(CONCAT(
                COALESCE(NEW.first_name, ''),
                COALESCE(NEW.last_name, ''),
                COALESCE(NEW.email, '')
            )),
            NEW.first_name,
            NEW.last_name,
            NEW.email,
            'CDC_REALTIME'
        );
        
        RETURN NEW;
    END IF;
    
    -- Handle UPDATE operations
    IF TG_OP = 'UPDATE' THEN
        DECLARE
            v_customer_hk CHAR(32);
            v_new_hash_diff CHAR(32);
            v_current_hash_diff CHAR(32);
        BEGIN
            v_customer_hk := MD5(UPPER(TRIM(NEW.customer_id)));
            v_new_hash_diff := MD5(CONCAT(
                COALESCE(NEW.first_name, ''),
                COALESCE(NEW.last_name, ''),
                COALESCE(NEW.email, '')
            ));
            
            -- Get current hash_diff
            SELECT hash_diff INTO v_current_hash_diff
            FROM sat_customer_details
            WHERE customer_hk = v_customer_hk AND load_end_date IS NULL;
            
            -- Only process if data changed
            IF v_current_hash_diff IS NULL OR v_current_hash_diff != v_new_hash_diff THEN
                -- Close current record
                UPDATE sat_customer_details 
                SET load_end_date = CURRENT_TIMESTAMP
                WHERE customer_hk = v_customer_hk AND load_end_date IS NULL;
                
                -- Insert new record
                INSERT INTO sat_customer_details (
                    customer_hk, load_date, hash_diff, first_name, last_name, email, record_source
                )
                VALUES (
                    v_customer_hk,
                    CURRENT_TIMESTAMP,
                    v_new_hash_diff,
                    NEW.first_name,
                    NEW.last_name,
                    NEW.email,
                    'CDC_REALTIME'
                );
            END IF;
        END;
        
        RETURN NEW;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for real-time processing
CREATE TRIGGER trg_customer_cdc_realtime
    AFTER INSERT OR UPDATE ON source_customers
    FOR EACH ROW
    EXECUTE FUNCTION process_cdc_changes();
```

**3. Micro-Batch Processing**
```python
# Apache Spark Structured Streaming for Data Vault
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

class SparkDataVaultStreaming:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("DataVaultStreaming") \
            .config("spark.sql.adaptive.enabled", "true") \
            .getOrCreate()
    
    def process_customer_stream(self):
        # Read from Kafka
        customer_stream = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "customer_changes") \
            .load()
        
        # Parse JSON data
        customer_schema = StructType([
            StructField("customer_id", StringType(), True),
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("email", StringType(), True),
            StructField("operation", StringType(), True)
        ])
        
        parsed_stream = customer_stream.select(
            from_json(col("value").cast("string"), customer_schema).alias("data")
        ).select("data.*")
        
        # Generate hash keys
        enriched_stream = parsed_stream.withColumn(
            "customer_hk", 
            md5(upper(trim(col("customer_id"))))
        ).withColumn(
            "hash_diff",
            md5(concat(
                coalesce(col("first_name"), lit("")),
                coalesce(col("last_name"), lit("")),
                coalesce(col("email"), lit(""))
            ))
        ).withColumn(
            "load_date",
            current_timestamp()
        ).withColumn(
            "record_source",
            lit("SPARK_STREAMING")
        )
        
        # Write to Data Vault tables
        def write_to_vault(batch_df, batch_id):
            if batch_df.count() > 0:
                # Write to hub_customer
                hub_data = batch_df.select(
                    "customer_hk", "customer_id", "load_date", "record_source"
                ).distinct()
                
                hub_data.write \
                    .format("jdbc") \
                    .option("url", "jdbc:postgresql://localhost:5432/datavault") \
                    .option("dbtable", "hub_customer") \
                    .option("user", "user") \
                    .option("password", "password") \
                    .mode("append") \
                    .save()
                
                # Write to sat_customer_details
                sat_data = batch_df.select(
                    "customer_hk", "load_date", "hash_diff", 
                    "first_name", "last_name", "email", "record_source"
                )
                
                sat_data.write \
                    .format("jdbc") \
                    .option("url", "jdbc:postgresql://localhost:5432/datavault") \
                    .option("dbtable", "sat_customer_details") \
                    .option("user", "user") \
                    .option("password", "password") \
                    .mode("append") \
                    .save()
        
        # Start streaming query
        query = enriched_stream.writeStream \
            .foreachBatch(write_to_vault) \
            .outputMode("append") \
            .option("checkpointLocation", "/tmp/datavault_checkpoint") \
            .trigger(processingTime="10 seconds") \
            .start()
        
        return query

# Usage
streaming_loader = SparkDataVaultStreaming()
query = streaming_loader.process_customer_stream()
query.awaitTermination()
```

### 55. How do you implement data vault in cloud environments?

**Answer:** Cloud Data Vault implementations leverage cloud-native services for scalability, performance, and cost optimization.

#### **Cloud-Specific Implementations:**

**1. AWS Data Vault Architecture**
```yaml
# AWS CloudFormation template for Data Vault infrastructure
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Data Vault 2.0 on AWS'

Resources:
  # Redshift cluster for Data Vault
  DataVaultCluster:
    Type: AWS::Redshift::Cluster
    Properties:
      ClusterType: multi-node
      NodeType: dc2.large
      NumberOfNodes: 3
      DBName: datavault
      MasterUsername: admin
      MasterUserPassword: !Ref DBPassword
      VpcSecurityGroupIds:
        - !Ref DataVaultSecurityGroup
      ClusterSubnetGroupName: !Ref DataVaultSubnetGroup
      
  # S3 bucket for staging data
  StagingBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::StackName}-datavault-staging'
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: DeleteOldVersions
            Status: Enabled
            NoncurrentVersionExpirationInDays: 30
            
  # Glue ETL jobs for Data Vault loading
  DataVaultETLJob:
    Type: AWS::Glue::Job
    Properties:
      Name: datavault-etl-job
      Role: !GetAtt GlueServiceRole.Arn
      Command:
        Name: glueetl
        ScriptLocation: !Sub 's3://${StagingBucket}/scripts/datavault_etl.py'
        PythonVersion: '3'
      DefaultArguments:
        '--TempDir': !Sub 's3://${StagingBucket}/temp/'
        '--job-bookmark-option': 'job-bookmark-enable'
        '--redshift-connection': !Ref RedshiftConnection
        
  # Lambda function for real-time processing
  RealTimeProcessor:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: datavault-realtime-processor
      Runtime: python3.9
      Handler: lambda_function.lambda_handler
      Code:
        ZipFile: |
          import json
          import boto3
          import hashlib
          from datetime import datetime
          
          def lambda_handler(event, context):
              # Process Kinesis records
              for record in event['Records']:
                  # Decode data
                  payload = json.loads(
                      base64.b64decode(record['kinesis']['data']).decode('utf-8')
                  )
                  
                  # Generate hash keys
                  customer_hk = hashlib.md5(
                      payload['customer_id'].upper().strip().encode()
                  ).hexdigest()
                  
                  # Load to Redshift via Data API
                  redshift_data = boto3.client('redshift-data')
                  
                  # Insert hub record
                  redshift_data.execute_statement(
                      ClusterIdentifier='datavault-cluster',
                      Database='datavault',
                      Sql=f"""
                          INSERT INTO hub_customer 
                          SELECT '{customer_hk}', '{payload['customer_id']}', 
                                 GETDATE(), 'KINESIS_LAMBDA'
                          WHERE NOT EXISTS (
                              SELECT 1 FROM hub_customer 
                              WHERE customer_hk = '{customer_hk}'
                          )
                      """
                  )
              
              return {'statusCode': 200, 'body': 'Processed successfully'}
      
      Environment:
        Variables:
          REDSHIFT_CLUSTER: !Ref DataVaultCluster
```

**2. Azure Data Vault with Synapse**
```python
# Azure Synapse pipeline for Data Vault loading
import pyodbc
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import pandas as pd

class AzureDataVaultLoader:
    def __init__(self, synapse_config, storage_config):
        self.synapse_conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={synapse_config['server']};"
            f"DATABASE={synapse_config['database']};"
            f"Authentication=ActiveDirectoryIntegrated"
        )
        
        self.blob_client = BlobServiceClient(
            account_url=f"https://{storage_config['account']}.blob.core.windows.net",
            credential=DefaultAzureCredential()
        )
    
    def load_from_data_lake(self, container, blob_path):
        # Read from Azure Data Lake
        blob_client = self.blob_client.get_blob_client(
            container=container, 
            blob=blob_path
        )
        
        # Download and process data
        data = blob_client.download_blob().readall()
        df = pd.read_parquet(io.BytesIO(data))
        
        return df
    
    def bulk_load_hub(self, df, hub_name, business_key_col):
        # Generate hash keys
        df['hash_key'] = df[business_key_col].apply(
            lambda x: hashlib.md5(str(x).upper().strip().encode()).hexdigest()
        )
        
        # Prepare data for bulk insert
        df['load_date'] = pd.Timestamp.now()
        df['record_source'] = 'AZURE_SYNAPSE'
        
        # Use Synapse COPY command for bulk loading
        cursor = self.synapse_conn.cursor()
        
        # Create temporary external table
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM sys.external_tables WHERE name = 'temp_{hub_name}')
            CREATE EXTERNAL TABLE temp_{hub_name} (
                hash_key NVARCHAR(32),
                business_key NVARCHAR(100),
                load_date DATETIME2,
                record_source NVARCHAR(50)
            )
            WITH (
                LOCATION = 'temp/{hub_name}/',
                DATA_SOURCE = staging_data_source,
                FILE_FORMAT = parquet_file_format
            )
        """)
        
        # Bulk insert with deduplication
        cursor.execute(f"""
            INSERT INTO {hub_name} (hash_key, business_key, load_date, record_source)
            SELECT DISTINCT t.hash_key, t.business_key, t.load_date, t.record_source
            FROM temp_{hub_name} t
            LEFT JOIN {hub_name} h ON t.hash_key = h.hash_key
            WHERE h.hash_key IS NULL
        """)
        
        self.synapse_conn.commit()
        cursor.close()
```

**3. Google Cloud Data Vault with BigQuery**
```python
# Google Cloud BigQuery Data Vault implementation
from google.cloud import bigquery
from google.cloud import storage
import pandas as pd
import hashlib

class GCPDataVaultLoader:
    def __init__(self, project_id, dataset_id):
        self.client = bigquery.Client(project=project_id)
        self.dataset_id = dataset_id
        self.project_id = project_id
    
    def create_vault_tables(self):
        # Create hub table
        hub_schema = [
            bigquery.SchemaField("customer_hk", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_bk", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("load_date", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("record_source", "STRING", mode="REQUIRED"),
        ]
        
        hub_table_id = f"{self.project_id}.{self.dataset_id}.hub_customer"
        hub_table = bigquery.Table(hub_table_id, schema=hub_schema)
        
        # Partition by load_date for performance
        hub_table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="load_date"
        )
        
        self.client.create_table(hub_table, exists_ok=True)
        
        # Create satellite table
        sat_schema = [
            bigquery.SchemaField("customer_hk", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("load_date", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("load_end_date", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("hash_diff", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("email", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("record_source", "STRING", mode="REQUIRED"),
        ]
        
        sat_table_id = f"{self.project_id}.{self.dataset_id}.sat_customer_details"
        sat_table = bigquery.Table(sat_table_id, schema=sat_schema)
        
        # Cluster by customer_hk for performance
        sat_table.clustering_fields = ["customer_hk"]
        sat_table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="load_date"
        )
        
        self.client.create_table(sat_table, exists_ok=True)
    
    def load_hub_from_gcs(self, gcs_uri):
        # Load hub using BigQuery's native capabilities
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )
        
        # Use SQL for deduplication during load
        query = f"""
            INSERT INTO `{self.project_id}.{self.dataset_id}.hub_customer`
            SELECT DISTINCT
                TO_HEX(MD5(UPPER(TRIM(customer_id)))) as customer_hk,
                customer_id as customer_bk,
                CURRENT_TIMESTAMP() as load_date,
                'GCS_LOAD' as record_source
            FROM (
                SELECT * FROM EXTERNAL_QUERY(
                    'projects/{self.project_id}/locations/us/connections/gcs-connection',
                    '''SELECT customer_id FROM `{gcs_uri}`'''
                )
            ) source
            WHERE customer_id IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1 FROM `{self.project_id}.{self.dataset_id}.hub_customer` h
                  WHERE h.customer_hk = TO_HEX(MD5(UPPER(TRIM(source.customer_id))))
              )
        """
        
        query_job = self.client.query(query)
        query_job.result()  # Wait for completion
        
        print(f"Loaded {query_job.num_dml_affected_rows} rows into hub_customer")
    
    def implement_scd_type2(self, source_table):
        # Implement Type 2 SCD using BigQuery SQL
        query = f"""
            -- Close existing records that have changed
            UPDATE `{self.project_id}.{self.dataset_id}.sat_customer_details` sat
            SET load_end_date = CURRENT_TIMESTAMP()
            WHERE sat.customer_hk IN (
                SELECT DISTINCT TO_HEX(MD5(UPPER(TRIM(s.customer_id))))
                FROM `{source_table}` s
                JOIN `{self.project_id}.{self.dataset_id}.sat_customer_details` existing
                  ON TO_HEX(MD5(UPPER(TRIM(s.customer_id)))) = existing.customer_hk
                WHERE existing.load_end_date IS NULL
                  AND existing.hash_diff != TO_HEX(MD5(CONCAT(
                      COALESCE(s.first_name, ''),
                      COALESCE(s.last_name, ''),
                      COALESCE(s.email, '')
                  )))
            )
            AND sat.load_end_date IS NULL;
            
            -- Insert new/changed records
            INSERT INTO `{self.project_id}.{self.dataset_id}.sat_customer_details`
            SELECT 
                TO_HEX(MD5(UPPER(TRIM(customer_id)))) as customer_hk,
                CURRENT_TIMESTAMP() as load_date,
                NULL as load_end_date,
                TO_HEX(MD5(CONCAT(
                    COALESCE(first_name, ''),
                    COALESCE(last_name, ''),
                    COALESCE(email, '')
                ))) as hash_diff,
                first_name,
                last_name,
                email,
                'BIGQUERY_LOAD' as record_source
            FROM `{source_table}` s
            WHERE NOT EXISTS (
                SELECT 1 FROM `{self.project_id}.{self.dataset_id}.sat_customer_details` existing
                WHERE existing.customer_hk = TO_HEX(MD5(UPPER(TRIM(s.customer_id))))
                  AND existing.load_end_date IS NULL
                  AND existing.hash_diff = TO_HEX(MD5(CONCAT(
                      COALESCE(s.first_name, ''),
                      COALESCE(s.last_name, ''),
                      COALESCE(s.email, '')
                  )))
            )
        """
        
        query_job = self.client.query(query)
        query_job.result()
        
        print(f"SCD Type 2 processing completed")
```

---

*[Continue with remaining sections...]*
## Advanced Level Questions (101-150)

### 101. How do you implement Data Vault with graph databases?

**Answer:** Graph databases can complement Data Vault by providing alternative query patterns and relationship analysis capabilities.

#### **Neo4j Integration with Data Vault:**

**1. Graph Model Mapping**
```cypher
// Create nodes for hubs
CREATE CONSTRAINT customer_hk_unique FOR (c:Customer) REQUIRE c.customer_hk IS UNIQUE;
CREATE CONSTRAINT order_hk_unique FOR (o:Order) REQUIRE o.order_hk IS UNIQUE;
CREATE CONSTRAINT product_hk_unique FOR (p:Product) REQUIRE p.product_hk IS UNIQUE;

// Load hub data as nodes
LOAD CSV WITH HEADERS FROM 'file:///hub_customer.csv' AS row
CREATE (c:Customer {
    customer_hk: row.customer_hk,
    customer_bk: row.customer_bk,
    load_date: datetime(row.load_date),
    record_source: row.record_source
});

// Load satellite data as node properties
LOAD CSV WITH HEADERS FROM 'file:///sat_customer_details.csv' AS row
MATCH (c:Customer {customer_hk: row.customer_hk})
WHERE row.load_end_date IS NULL  // Current records only
SET c.first_name = row.first_name,
    c.last_name = row.last_name,
    c.email = row.email,
    c.phone = row.phone;

// Create relationships from links
LOAD CSV WITH HEADERS FROM 'file:///link_customer_order.csv' AS row
MATCH (c:Customer {customer_hk: row.customer_hk})
MATCH (o:Order {order_hk: row.order_hk})
CREATE (c)-[:PLACED_ORDER {
    link_hk: row.customer_order_hk,
    load_date: datetime(row.load_date),
    record_source: row.record_source
}]->(o);
```

**2. Advanced Graph Queries**
```cypher
// Find customer purchase patterns
MATCH (c:Customer)-[r:PLACED_ORDER]->(o:Order)-[:CONTAINS]->(p:Product)
WHERE c.customer_segment = 'Premium'
WITH c, collect(DISTINCT p.category) as categories, count(o) as order_count
WHERE size(categories) > 3  // Cross-category buyers
RETURN c.customer_bk, c.first_name, c.last_name, categories, order_count
ORDER BY order_count DESC;

// Identify customer clusters based on purchase behavior
MATCH (c1:Customer)-[:PLACED_ORDER]->(:Order)-[:CONTAINS]->(p:Product)<-[:CONTAINS]-(:Order)<-[:PLACED_ORDER]-(c2:Customer)
WHERE c1 <> c2
WITH c1, c2, count(p) as common_products
WHERE common_products > 5
CREATE (c1)-[:SIMILAR_BUYER {similarity_score: common_products}]->(c2);

// Find influential customers (high connectivity)
MATCH (c:Customer)
WITH c, size((c)-[:PLACED_ORDER]->()) as order_count,
     size((c)-[:SIMILAR_BUYER]->()) as similar_buyers
WHERE order_count > 10 AND similar_buyers > 5
RETURN c.customer_bk, c.first_name, c.last_name, order_count, similar_buyers
ORDER BY (order_count * similar_buyers) DESC;
```

**3. Hybrid Architecture Implementation**
```python
# Python integration between Data Vault and Neo4j
from neo4j import GraphDatabase
import psycopg2
import pandas as pd

class DataVaultGraphIntegration:
    def __init__(self, postgres_config, neo4j_config):
        self.pg_conn = psycopg2.connect(**postgres_config)
        self.neo4j_driver = GraphDatabase.driver(
            neo4j_config['uri'], 
            auth=(neo4j_config['user'], neo4j_config['password'])
        )
    
    def sync_vault_to_graph(self):
        # Extract current state from Data Vault
        query = """
            SELECT 
                h.customer_hk,
                h.customer_bk,
                s.first_name,
                s.last_name,
                s.email,
                s.load_date
            FROM hub_customer h
            JOIN sat_customer_details s ON h.customer_hk = s.customer_hk
            WHERE s.load_end_date IS NULL
        """
        
        df = pd.read_sql(query, self.pg_conn)
        
        # Load into Neo4j
        with self.neo4j_driver.session() as session:
            for _, row in df.iterrows():
                session.run("""
                    MERGE (c:Customer {customer_hk: $customer_hk})
                    SET c.customer_bk = $customer_bk,
                        c.first_name = $first_name,
                        c.last_name = $last_name,
                        c.email = $email,
                        c.last_updated = datetime($load_date)
                """, **row.to_dict())
    
    def analyze_customer_journey(self, customer_hk):
        with self.neo4j_driver.session() as session:
            result = session.run("""
                MATCH path = (c:Customer {customer_hk: $customer_hk})-[:PLACED_ORDER*1..5]->(o:Order)
                WITH c, o, length(path) as journey_length
                ORDER BY o.order_date
                RETURN c.customer_bk, 
                       collect({order_id: o.order_bk, order_date: o.order_date, journey_step: journey_length}) as journey
            """, customer_hk=customer_hk)
            
            return result.single()
    
    def find_recommendation_candidates(self, customer_hk, limit=10):
        with self.neo4j_driver.session() as session:
            result = session.run("""
                MATCH (target:Customer {customer_hk: $customer_hk})-[:PLACED_ORDER]->(:Order)-[:CONTAINS]->(p:Product)
                WITH target, collect(DISTINCT p.product_hk) as target_products
                
                MATCH (similar:Customer)-[:PLACED_ORDER]->(:Order)-[:CONTAINS]->(p:Product)
                WHERE similar <> target AND p.product_hk IN target_products
                WITH target, similar, count(p) as common_products, 
                     collect(DISTINCT p.product_hk) as similar_products
                WHERE common_products > 2
                
                MATCH (similar)-[:PLACED_ORDER]->(:Order)-[:CONTAINS]->(rec:Product)
                WHERE NOT rec.product_hk IN target_products
                WITH rec, count(DISTINCT similar) as recommendation_strength
                ORDER BY recommendation_strength DESC
                LIMIT $limit
                
                RETURN rec.product_bk, rec.product_name, recommendation_strength
            """, customer_hk=customer_hk, limit=limit)
            
            return [record.data() for record in result]
```

### 102. How do you implement Data Vault with time-series data?

**Answer:** Time-series data in Data Vault requires specialized patterns to handle high-volume, time-ordered data efficiently.

#### **Time-Series Patterns:**

**1. Time-Series Satellite Design**
```sql
-- Time-series satellite for IoT sensor data
CREATE TABLE sat_sensor_readings_ts (
    sensor_hk CHAR(32) NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL,
    load_date TIMESTAMP NOT NULL,
    hash_diff CHAR(32) NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    pressure DECIMAL(7,2),
    battery_level INTEGER,
    signal_strength INTEGER,
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (sensor_hk, reading_timestamp),
    
    -- Partition by time for performance
    PARTITION BY RANGE (reading_timestamp) (
        PARTITION p2024_01 VALUES LESS THAN ('2024-02-01'),
        PARTITION p2024_02 VALUES LESS THAN ('2024-03-01'),
        PARTITION p2024_03 VALUES LESS THAN ('2024-04-01')
    )
);

-- Indexes for time-series queries
CREATE INDEX idx_sensor_readings_ts_time ON sat_sensor_readings_ts (reading_timestamp);
CREATE INDEX idx_sensor_readings_ts_sensor_time ON sat_sensor_readings_ts (sensor_hk, reading_timestamp);
```

**2. Aggregated Time-Series Satellites**
```sql
-- Pre-aggregated time-series data for performance
CREATE TABLE sat_sensor_hourly_agg (
    sensor_hk CHAR(32) NOT NULL,
    hour_timestamp TIMESTAMP NOT NULL,
    load_date TIMESTAMP NOT NULL,
    hash_diff CHAR(32) NOT NULL,
    avg_temperature DECIMAL(5,2),
    min_temperature DECIMAL(5,2),
    max_temperature DECIMAL(5,2),
    avg_humidity DECIMAL(5,2),
    min_humidity DECIMAL(5,2),
    max_humidity DECIMAL(5,2),
    reading_count INTEGER,
    quality_score DECIMAL(3,2),
    record_source VARCHAR(50) NOT NULL,
    
    PRIMARY KEY (sensor_hk, hour_timestamp)
);

-- Populate hourly aggregations
INSERT INTO sat_sensor_hourly_agg
SELECT 
    sensor_hk,
    DATE_TRUNC('hour', reading_timestamp) as hour_timestamp,
    CURRENT_TIMESTAMP as load_date,
    MD5(CONCAT(
        AVG(temperature)::TEXT,
        MIN(temperature)::TEXT,
        MAX(temperature)::TEXT,
        AVG(humidity)::TEXT,
        COUNT(*)::TEXT
    )) as hash_diff,
    AVG(temperature) as avg_temperature,
    MIN(temperature) as min_temperature,
    MAX(temperature) as max_temperature,
    AVG(humidity) as avg_humidity,
    MIN(humidity) as min_humidity,
    MAX(humidity) as max_humidity,
    COUNT(*) as reading_count,
    -- Quality score based on data completeness
    (COUNT(*) * 100.0 / 3600) as quality_score,  -- Assuming 1 reading per second
    'HOURLY_AGGREGATION' as record_source
FROM sat_sensor_readings_ts
WHERE reading_timestamp >= CURRENT_DATE - INTERVAL '1 day'
  AND reading_timestamp < CURRENT_DATE
GROUP BY sensor_hk, DATE_TRUNC('hour', reading_timestamp);
```

**3. Time-Series Analytics Implementation**
```python
# Python implementation for time-series Data Vault analytics
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import psycopg2

class TimeSeriesDataVault:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
    
    def load_time_series_batch(self, sensor_data_batch):
        """Load batch of time-series data with deduplication"""
        cursor = self.conn.cursor()
        
        # Prepare batch insert with conflict resolution
        insert_query = """
            INSERT INTO sat_sensor_readings_ts (
                sensor_hk, reading_timestamp, load_date, hash_diff,
                temperature, humidity, pressure, battery_level, signal_strength, record_source
            )
            VALUES %s
            ON CONFLICT (sensor_hk, reading_timestamp) 
            DO UPDATE SET
                load_date = EXCLUDED.load_date,
                hash_diff = EXCLUDED.hash_diff,
                temperature = EXCLUDED.temperature,
                humidity = EXCLUDED.humidity,
                pressure = EXCLUDED.pressure,
                battery_level = EXCLUDED.battery_level,
                signal_strength = EXCLUDED.signal_strength,
                record_source = EXCLUDED.record_source
            WHERE sat_sensor_readings_ts.hash_diff != EXCLUDED.hash_diff
        """
        
        # Prepare data tuples
        data_tuples = []
        for reading in sensor_data_batch:
            sensor_hk = hashlib.md5(reading['sensor_id'].encode()).hexdigest()
            hash_diff = hashlib.md5(
                f"{reading['temperature']}{reading['humidity']}{reading['pressure']}"
                f"{reading['battery_level']}{reading['signal_strength']}".encode()
            ).hexdigest()
            
            data_tuples.append((
                sensor_hk,
                reading['timestamp'],
                datetime.now(),
                hash_diff,
                reading['temperature'],
                reading['humidity'],
                reading['pressure'],
                reading['battery_level'],
                reading['signal_strength'],
                'IOT_BATCH_LOAD'
            ))
        
        # Execute batch insert
        psycopg2.extras.execute_values(
            cursor, insert_query, data_tuples, template=None, page_size=1000
        )
        
        self.conn.commit()
        cursor.close()
    
    def detect_anomalies(self, sensor_hk, hours_back=24):
        """Detect anomalies in time-series data"""
        query = """
            WITH sensor_stats AS (
                SELECT 
                    AVG(temperature) as avg_temp,
                    STDDEV(temperature) as stddev_temp,
                    AVG(humidity) as avg_humidity,
                    STDDEV(humidity) as stddev_humidity
                FROM sat_sensor_readings_ts
                WHERE sensor_hk = %s
                  AND reading_timestamp >= NOW() - INTERVAL '%s hours'
            ),
            readings_with_zscore AS (
                SELECT 
                    s.*,
                    ABS(s.temperature - st.avg_temp) / NULLIF(st.stddev_temp, 0) as temp_zscore,
                    ABS(s.humidity - st.avg_humidity) / NULLIF(st.stddev_humidity, 0) as humidity_zscore
                FROM sat_sensor_readings_ts s
                CROSS JOIN sensor_stats st
                WHERE s.sensor_hk = %s
                  AND s.reading_timestamp >= NOW() - INTERVAL '%s hours'
            )
            SELECT 
                reading_timestamp,
                temperature,
                humidity,
                temp_zscore,
                humidity_zscore,
                CASE 
                    WHEN temp_zscore > 3 OR humidity_zscore > 3 THEN 'HIGH'
                    WHEN temp_zscore > 2 OR humidity_zscore > 2 THEN 'MEDIUM'
                    ELSE 'NORMAL'
                END as anomaly_level
            FROM readings_with_zscore
            WHERE temp_zscore > 2 OR humidity_zscore > 2
            ORDER BY reading_timestamp DESC
        """
        
        return pd.read_sql(query, self.conn, params=[sensor_hk, hours_back, sensor_hk, hours_back])
    
    def calculate_time_series_features(self, sensor_hk, window_hours=24):
        """Calculate time-series features for ML"""
        query = """
            WITH time_series AS (
                SELECT 
                    reading_timestamp,
                    temperature,
                    humidity,
                    pressure,
                    LAG(temperature, 1) OVER (ORDER BY reading_timestamp) as prev_temp,
                    LAG(temperature, 12) OVER (ORDER BY reading_timestamp) as temp_12h_ago,
                    LAG(temperature, 24) OVER (ORDER BY reading_timestamp) as temp_24h_ago
                FROM sat_sensor_readings_ts
                WHERE sensor_hk = %s
                  AND reading_timestamp >= NOW() - INTERVAL '%s hours'
                ORDER BY reading_timestamp
            ),
            features AS (
                SELECT 
                    reading_timestamp,
                    temperature,
                    humidity,
                    pressure,
                    -- Trend features
                    temperature - prev_temp as temp_change,
                    temperature - temp_12h_ago as temp_change_12h,
                    temperature - temp_24h_ago as temp_change_24h,
                    -- Rolling statistics
                    AVG(temperature) OVER (
                        ORDER BY reading_timestamp 
                        ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
                    ) as temp_rolling_avg_12,
                    STDDEV(temperature) OVER (
                        ORDER BY reading_timestamp 
                        ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
                    ) as temp_rolling_std_12,
                    -- Seasonal features
                    EXTRACT(hour FROM reading_timestamp) as hour_of_day,
                    EXTRACT(dow FROM reading_timestamp) as day_of_week
                FROM time_series
            )
            SELECT * FROM features
            WHERE temp_change IS NOT NULL
            ORDER BY reading_timestamp DESC
        """
        
        return pd.read_sql(query, self.conn, params=[sensor_hk, window_hours])
```

### 103. How do you implement Data Vault with blockchain integration?

**Answer:** Blockchain integration with Data Vault provides immutable audit trails and decentralized data verification capabilities.

#### **Blockchain Integration Patterns:**

**1. Immutable Audit Trail**
```python
# Blockchain integration for Data Vault audit trail
import hashlib
import json
from datetime import datetime
from web3 import Web3
import psycopg2

class BlockchainDataVaultAudit:
    def __init__(self, db_config, blockchain_config):
        self.db_conn = psycopg2.connect(**db_config)
        self.w3 = Web3(Web3.HTTPProvider(blockchain_config['provider_url']))
        self.contract_address = blockchain_config['contract_address']
        self.private_key = blockchain_config['private_key']
        self.account = self.w3.eth.account.from_key(self.private_key)
        
        # Smart contract ABI for audit logging
        self.contract_abi = [
            {
                "inputs": [
                    {"name": "dataHash", "type": "bytes32"},
                    {"name": "tableName", "type": "string"},
                    {"name": "operation", "type": "string"},
                    {"name": "timestamp", "type": "uint256"}
                ],
                "name": "logDataChange",
                "outputs": [],
                "type": "function"
            }
        ]
        
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
    
    def log_vault_change_to_blockchain(self, table_name, operation, data_hash):
        """Log Data Vault changes to blockchain for immutable audit"""
        try:
            # Prepare transaction
            transaction = self.contract.functions.logDataChange(
                Web3.toBytes(hexstr=data_hash),
                table_name,
                operation,
                int(datetime.now().timestamp())
            ).buildTransaction({
                'from': self.account.address,
                'gas': 100000,
                'gasPrice': self.w3.toWei('20', 'gwei'),
                'nonce': self.w3.eth.getTransactionCount(self.account.address)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            
            # Wait for confirmation
            receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            
            return {
                'transaction_hash': receipt.transactionHash.hex(),
                'block_number': receipt.blockNumber,
                'gas_used': receipt.gasUsed
            }
            
        except Exception as e:
            print(f"Blockchain logging failed: {e}")
            return None
    
    def enhanced_satellite_load_with_blockchain(self, satellite_data):
        """Load satellite with blockchain audit trail"""
        cursor = self.db_conn.cursor()
        
        try:
            # Calculate data hash for blockchain
            data_string = json.dumps(satellite_data, sort_keys=True)
            data_hash = hashlib.sha256(data_string.encode()).hexdigest()
            
            # Insert into satellite
            cursor.execute("""
                INSERT INTO sat_customer_details (
                    customer_hk, load_date, hash_diff, first_name, last_name, email, 
                    record_source, blockchain_hash, blockchain_tx_hash
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                satellite_data['customer_hk'],
                datetime.now(),
                satellite_data['hash_diff'],
                satellite_data['first_name'],
                satellite_data['last_name'],
                satellite_data['email'],
                'BLOCKCHAIN_VERIFIED',
                data_hash,
                None  # Will be updated after blockchain confirmation
            ))
            
            # Log to blockchain
            blockchain_result = self.log_vault_change_to_blockchain(
                'sat_customer_details', 
                'INSERT', 
                data_hash
            )
            
            if blockchain_result:
                # Update record with blockchain transaction hash
                cursor.execute("""
                    UPDATE sat_customer_details 
                    SET blockchain_tx_hash = %s,
                        blockchain_block_number = %s
                    WHERE customer_hk = %s 
                      AND load_date = %s
                      AND blockchain_hash = %s
                """, (
                    blockchain_result['transaction_hash'],
                    blockchain_result['block_number'],
                    satellite_data['customer_hk'],
                    satellite_data['load_date'],
                    data_hash
                ))
            
            self.db_conn.commit()
            return True
            
        except Exception as e:
            self.db_conn.rollback()
            print(f"Enhanced satellite load failed: {e}")
            return False
        finally:
            cursor.close()
    
    def verify_data_integrity(self, customer_hk, load_date):
        """Verify data integrity against blockchain"""
        cursor = self.db_conn.cursor()
        
        # Get record from database
        cursor.execute("""
            SELECT blockchain_hash, blockchain_tx_hash, first_name, last_name, email
            FROM sat_customer_details
            WHERE customer_hk = %s AND load_date = %s
        """, (customer_hk, load_date))
        
        record = cursor.fetchone()
        if not record:
            return {'status': 'NOT_FOUND'}
        
        stored_hash, tx_hash, first_name, last_name, email = record
        
        # Recalculate hash from current data
        current_data = {
            'customer_hk': customer_hk,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        current_hash = hashlib.sha256(
            json.dumps(current_data, sort_keys=True).encode()
        ).hexdigest()
        
        # Verify against blockchain
        if tx_hash:
            try:
                receipt = self.w3.eth.getTransactionReceipt(tx_hash)
                # Decode transaction data to verify hash
                # (Implementation depends on specific smart contract)
                blockchain_verified = True  # Simplified for example
            except:
                blockchain_verified = False
        else:
            blockchain_verified = False
        
        return {
            'status': 'VERIFIED' if current_hash == stored_hash and blockchain_verified else 'TAMPERED',
            'stored_hash': stored_hash,
            'current_hash': current_hash,
            'blockchain_verified': blockchain_verified,
            'transaction_hash': tx_hash
        }
```

**2. Decentralized Data Verification**
```solidity
// Smart contract for Data Vault audit trail
pragma solidity ^0.8.0;

contract DataVaultAudit {
    struct AuditRecord {
        bytes32 dataHash;
        string tableName;
        string operation;
        uint256 timestamp;
        address submitter;
        bool verified;
    }
    
    mapping(bytes32 => AuditRecord) public auditRecords;
    mapping(address => bool) public authorizedSubmitters;
    
    event DataChangeLogged(
        bytes32 indexed dataHash,
        string tableName,
        string operation,
        uint256 timestamp,
        address submitter
    );
    
    event DataVerified(
        bytes32 indexed dataHash,
        address verifier
    );
    
    modifier onlyAuthorized() {
        require(authorizedSubmitters[msg.sender], "Not authorized");
        _;
    }
    
    constructor() {
        authorizedSubmitters[msg.sender] = true;
    }
    
    function addAuthorizedSubmitter(address submitter) external onlyAuthorized {
        authorizedSubmitters[submitter] = true;
    }
    
    function logDataChange(
        bytes32 dataHash,
        string memory tableName,
        string memory operation,
        uint256 timestamp
    ) external onlyAuthorized {
        require(auditRecords[dataHash].timestamp == 0, "Record already exists");
        
        auditRecords[dataHash] = AuditRecord({
            dataHash: dataHash,
            tableName: tableName,
            operation: operation,
            timestamp: timestamp,
            submitter: msg.sender,
            verified: false
        });
        
        emit DataChangeLogged(dataHash, tableName, operation, timestamp, msg.sender);
    }
    
    function verifyData(bytes32 dataHash) external onlyAuthorized {
        require(auditRecords[dataHash].timestamp != 0, "Record does not exist");
        require(!auditRecords[dataHash].verified, "Already verified");
        
        auditRecords[dataHash].verified = true;
        emit DataVerified(dataHash, msg.sender);
    }
    
    function getAuditRecord(bytes32 dataHash) external view returns (
        string memory tableName,
        string memory operation,
        uint256 timestamp,
        address submitter,
        bool verified
    ) {
        AuditRecord memory record = auditRecords[dataHash];
        return (
            record.tableName,
            record.operation,
            record.timestamp,
            record.submitter,
            record.verified
        );
    }
}
```

### 104. How do you implement Data Vault with machine learning integration?

**Answer:** ML integration with Data Vault enables automated data quality, pattern detection, and predictive analytics while maintaining data lineage.

#### **ML Integration Patterns:**

**1. Automated Data Quality with ML**
```python
# ML-powered data quality for Data Vault
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import psycopg2
import joblib

class MLDataQualityEngine:
    def __init__(self, db_config):
        self.db_conn = psycopg2.connect(**db_config)
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        
    def train_anomaly_detection_model(self, table_name, training_days=30):
        """Train anomaly detection model on historical data"""
        query = f"""
            SELECT 
                LENGTH(first_name) as first_name_len,
                LENGTH(last_name) as last_name_len,
                LENGTH(email) as email_len,
                CASE WHEN email LIKE '%@%.%' THEN 1 ELSE 0 END as email_valid_format,
                EXTRACT(hour FROM load_date) as load_hour,
                EXTRACT(dow FROM load_date) as load_dow
            FROM {table_name}
            WHERE load_date >= CURRENT_DATE - INTERVAL '{training_days} days'
              AND first_name IS NOT NULL 
              AND last_name IS NOT NULL 
              AND email IS NOT NULL
        """
        
        df = pd.read_sql(query, self.db_conn)
        
        # Prepare features
        features = self.scaler.fit_transform(df)
        
        # Train anomaly detection model
        self.anomaly_detector.fit(features)
        
        # Save model
        joblib.dump(self.anomaly_detector, f'models/{table_name}_anomaly_detector.pkl')
        joblib.dump(self.scaler, f'models/{table_name}_scaler.pkl')
        
        return {
            'training_samples': len(df),
            'model_path': f'models/{table_name}_anomaly_detector.pkl'
        }
    
    def detect_data_anomalies(self, new_data_batch):
        """Detect anomalies in new data batch"""
        # Prepare features for new data
        feature_df = pd.DataFrame([
            {
                'first_name_len': len(record.get('first_name', '')),
                'last_name_len': len(record.get('last_name', '')),
                'email_len': len(record.get('email', '')),
                'email_valid_format': 1 if '@' in record.get('email', '') and '.' in record.get('email', '') else 0,
                'load_hour': record.get('load_hour', 0),
                'load_dow': record.get('load_dow', 0)
            }
            for record in new_data_batch
        ])
        
        # Scale features
        features_scaled = self.scaler.transform(feature_df)
        
        # Predict anomalies
        anomaly_scores = self.anomaly_detector.decision_function(features_scaled)
        anomaly_predictions = self.anomaly_detector.predict(features_scaled)
        
        # Create anomaly satellite records
        anomaly_records = []
        for i, (record, score, prediction) in enumerate(zip(new_data_batch, anomaly_scores, anomaly_predictions)):
            if prediction == -1:  # Anomaly detected
                anomaly_records.append({
                    'customer_hk': record['customer_hk'],
                    'anomaly_type': 'DATA_QUALITY',
                    'anomaly_score': float(score),
                    'anomaly_description': f'Unusual data pattern detected (score: {score:.3f})',
                    'detection_method': 'ISOLATION_FOREST',
                    'load_date': record['load_date'],
                    'record_source': 'ML_ANOMALY_DETECTION'
                })
        
        return anomaly_records
    
    def create_ml_quality_satellite(self):
        """Create satellite for ML-detected quality issues"""
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sat_data_quality_ml (
                customer_hk CHAR(32) NOT NULL,
                load_date TIMESTAMP NOT NULL,
                hash_diff CHAR(32) NOT NULL,
                anomaly_type VARCHAR(50),
                anomaly_score DECIMAL(10,6),
                anomaly_description TEXT,
                detection_method VARCHAR(50),
                confidence_level DECIMAL(5,2),
                false_positive_flag BOOLEAN DEFAULT FALSE,
                reviewed_by VARCHAR(50),
                review_date TIMESTAMP,
                record_source VARCHAR(50) NOT NULL,
                
                PRIMARY KEY (customer_hk, load_date, anomaly_type)
            )
        """)
        self.db_conn.commit()
        cursor.close()
```

**2. Predictive Analytics Integration**
```python
# Predictive analytics for Data Vault
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import mlflow
import mlflow.sklearn

class DataVaultPredictiveAnalytics:
    def __init__(self, db_config, mlflow_config):
        self.db_conn = psycopg2.connect(**db_config)
        mlflow.set_tracking_uri(mlflow_config['tracking_uri'])
        mlflow.set_experiment(mlflow_config['experiment_name'])
        
    def create_customer_churn_features(self):
        """Create features for customer churn prediction from Data Vault"""
        query = """
            WITH customer_metrics AS (
                SELECT 
                    h.customer_hk,
                    h.customer_bk,
                    -- Customer details
                    cd.first_name,
                    cd.last_name,
                    cd.email,
                    -- Order metrics
                    COUNT(DISTINCT l.order_hk) as total_orders,
                    SUM(od.total_amount) as total_spent,
                    AVG(od.total_amount) as avg_order_value,
                    MAX(od.order_date) as last_order_date,
                    MIN(od.order_date) as first_order_date,
                    -- Recency, Frequency, Monetary
                    EXTRACT(days FROM CURRENT_DATE - MAX(od.order_date)) as days_since_last_order,
                    COUNT(DISTINCT l.order_hk) / NULLIF(EXTRACT(days FROM MAX(od.order_date) - MIN(od.order_date)), 0) * 365 as order_frequency_yearly,
                    -- Customer lifetime
                    EXTRACT(days FROM CURRENT_DATE - MIN(cd.load_date)) as customer_lifetime_days
                FROM hub_customer h
                JOIN sat_customer_details cd ON h.customer_hk = cd.customer_hk AND cd.load_end_date IS NULL
                LEFT JOIN link_customer_order l ON h.customer_hk = l.customer_hk
                LEFT JOIN sat_order_details od ON l.order_hk = od.order_hk AND od.load_end_date IS NULL
                WHERE h.load_date >= CURRENT_DATE - INTERVAL '2 years'
                GROUP BY h.customer_hk, h.customer_bk, cd.first_name, cd.last_name, cd.email, cd.load_date
            ),
            churn_labels AS (
                SELECT 
                    customer_hk,
                    CASE 
                        WHEN days_since_last_order > 90 THEN 1  -- Churned
                        ELSE 0  -- Active
                    END as churned
                FROM customer_metrics
                WHERE total_orders > 0  -- Only customers with purchase history
            )
            SELECT 
                cm.*,
                cl.churned
            FROM customer_metrics cm
            JOIN churn_labels cl ON cm.customer_hk = cl.customer_hk
        """
        
        return pd.read_sql(query, self.db_conn)
    
    def train_churn_prediction_model(self):
        """Train customer churn prediction model"""
        with mlflow.start_run():
            # Get training data
            df = self.create_customer_churn_features()
            
            # Prepare features
            feature_columns = [
                'total_orders', 'total_spent', 'avg_order_value',
                'days_since_last_order', 'order_frequency_yearly', 'customer_lifetime_days'
            ]
            
            X = df[feature_columns].fillna(0)
            y = df['churned']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            accuracy = model.score(X_test, y_test)
            
            # Log metrics
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_param("n_estimators", 100)
            mlflow.sklearn.log_model(model, "churn_model")
            
            # Feature importance
            feature_importance = pd.DataFrame({
                'feature': feature_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("Model Performance:")
            print(classification_report(y_test, y_pred))
            print("\nFeature Importance:")
            print(feature_importance)
            
            return model, feature_importance
    
    def create_prediction_satellite(self):
        """Create satellite for storing ML predictions"""
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sat_customer_predictions (
                customer_hk CHAR(32) NOT NULL,
                prediction_date DATE NOT NULL,
                load_date TIMESTAMP NOT NULL,
                hash_diff CHAR(32) NOT NULL,
                model_name VARCHAR(100),
                model_version VARCHAR(20),
                churn_probability DECIMAL(5,4),
                churn_prediction BOOLEAN,
                confidence_score DECIMAL(5,4),
                feature_contributions JSON,
                prediction_explanation TEXT,
                record_source VARCHAR(50) NOT NULL,
                
                PRIMARY KEY (customer_hk, prediction_date, model_name)
            )
        """)
        self.db_conn.commit()
        cursor.close()
    
    def generate_daily_predictions(self, model):
        """Generate daily churn predictions for all active customers"""
        # Get current customer features
        df = self.create_customer_churn_features()
        active_customers = df[df['churned'] == 0]  # Only active customers
        
        feature_columns = [
            'total_orders', 'total_spent', 'avg_order_value',
            'days_since_last_order', 'order_frequency_yearly', 'customer_lifetime_days'
        ]
        
        X = active_customers[feature_columns].fillna(0)
        
        # Generate predictions
        churn_probabilities = model.predict_proba(X)[:, 1]  # Probability of churn
        churn_predictions = model.predict(X)
        
        # Store predictions in satellite
        cursor = self.db_conn.cursor()
        
        for i, (_, customer) in enumerate(active_customers.iterrows()):
            hash_diff = hashlib.md5(
                f"{churn_probabilities[i]}{churn_predictions[i]}{datetime.now().date()}".encode()
            ).hexdigest()
            
            cursor.execute("""
                INSERT INTO sat_customer_predictions (
                    customer_hk, prediction_date, load_date, hash_diff,
                    model_name, model_version, churn_probability, churn_prediction,
                    confidence_score, record_source
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (customer_hk, prediction_date, model_name) 
                DO UPDATE SET
                    load_date = EXCLUDED.load_date,
                    hash_diff = EXCLUDED.hash_diff,
                    churn_probability = EXCLUDED.churn_probability,
                    churn_prediction = EXCLUDED.churn_prediction,
                    confidence_score = EXCLUDED.confidence_score
            """, (
                customer['customer_hk'],
                datetime.now().date(),
                datetime.now(),
                hash_diff,
                'RandomForestChurn',
                'v1.0',
                float(churn_probabilities[i]),
                bool(churn_predictions[i]),
                float(max(churn_probabilities[i], 1 - churn_probabilities[i])),
                'ML_DAILY_BATCH'
            ))
        
        self.db_conn.commit()
        cursor.close()
        
        return len(active_customers)
```

---

*[Continue with remaining sections...]*