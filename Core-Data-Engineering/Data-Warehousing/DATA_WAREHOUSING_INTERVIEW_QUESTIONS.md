# Data Warehousing Interview Questions

## 📋 Table of Contents
1. [Basic Level (0-2 years)](#basic-level-0-2-years)
2. [Intermediate Level (2-5 years)](#intermediate-level-2-5-years)
3. [Advanced Level (5+ years)](#advanced-level-5-years)
4. [Theoretical & Conceptual Questions](#theoretical--conceptual-questions)
5. [Scenario-Based Questions](#scenario-based-questions)
6. [Architecture & Design Questions](#architecture--design-questions)
7. [Performance & Optimization](#performance--optimization)
8. [Modern Data Warehousing](#modern-data-warehousing)

---

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

---

## Theoretical & Conceptual Questions

### 8. What are the key principles of dimensional modeling?
**Answer:**
**Kimball's Four-Step Process:**
1. **Select Business Process**: Choose specific business activity
2. **Declare Grain**: Define level of detail for fact table
3. **Identify Dimensions**: Choose context for measurements
4. **Identify Facts**: Choose measurable business metrics

**Core Principles:**
- **Conformed Dimensions**: Shared across fact tables
- **Slowly Changing Dimensions**: Handle attribute changes over time
- **Fact Table Grain**: Atomic level for maximum flexibility
- **Star Schema**: Denormalized for query performance

### 9. Explain the difference between star schema and snowflake schema.
**Answer:**
**Star Schema:**
- Denormalized dimension tables
- Single join between fact and dimension
- Better query performance
- More storage space
- Simpler to understand

**Snowflake Schema:**
- Normalized dimension tables
- Multiple joins required
- Less storage space
- More complex queries
- Better for data integrity

**Galaxy Schema (Fact Constellation):**
- Multiple fact tables sharing dimensions
- Most complex but most flexible

### 10. What is data lineage and why is it important?
**Answer:**
**Definition**: Complete trail of data from source to destination, including transformations.

**Importance:**
- **Impact Analysis**: Understand downstream effects of changes
- **Root Cause Analysis**: Trace data quality issues
- **Compliance**: Meet regulatory requirements (GDPR, SOX)
- **Data Governance**: Maintain data quality and trust
- **Documentation**: Understand data flow and dependencies

**Tools**: Apache Atlas, DataHub, Collibra, Informatica Axon

### 11. Explain different data warehouse testing strategies.
**Answer:**
**Types of Testing:**
- **Data Completeness**: All expected data loaded
- **Data Accuracy**: Values match source systems
- **Data Consistency**: Referential integrity maintained
- **Data Transformation**: Business rules applied correctly
- **Performance Testing**: Query response times acceptable
- **Regression Testing**: Changes don't break existing functionality

**Testing Approaches:**
- **Source-to-Target Testing**: Compare source and target data
- **Metadata Testing**: Validate data types, lengths, constraints
- **ETL Testing**: Validate extraction, transformation, loading
- **BI Report Testing**: Validate analytical outputs

### 12. What is data vault modeling and when would you use it?
**Answer:**
**Components:**
- **Hubs**: Unique business keys
- **Links**: Relationships between hubs
- **Satellites**: Descriptive attributes and history

**Benefits:**
- **Auditability**: Complete history preserved
- **Flexibility**: Easy to add new data sources
- **Parallel Loading**: Independent loading of components
- **Compliance**: Meets regulatory requirements

**When to Use:**
- Highly regulated industries
- Frequently changing requirements
- Multiple source systems
- Need for detailed audit trails

### 13. Explain the concept of data governance in data warehousing.
**Answer:**
**Key Components:**
- **Data Quality**: Accuracy, completeness, consistency
- **Data Security**: Access controls, encryption, masking
- **Data Privacy**: PII protection, consent management
- **Metadata Management**: Data catalogs, documentation
- **Data Lifecycle**: Retention, archival, deletion policies

**Governance Framework:**
- **Policies**: Rules and standards
- **Processes**: Workflows and procedures
- **People**: Roles and responsibilities
- **Technology**: Tools and platforms

**Roles:**
- **Data Stewards**: Day-to-day data management
- **Data Owners**: Business accountability
- **Data Custodians**: Technical implementation

---

## Scenario-Based Questions

### 14. Design a data warehouse for an e-commerce company.
**Answer:**
**Business Requirements:**
- Track sales, customers, products, orders
- Analyze trends, customer behavior, inventory
- Support real-time dashboards and batch reports

**Dimensional Model:**
```
Fact Tables:
- fact_sales (order_key, customer_key, product_key, date_key, sales_amount, quantity)
- fact_inventory (product_key, date_key, stock_level, reorder_point)

Dimension Tables:
- dim_customer (customer_key, name, email, address, segment)
- dim_product (product_key, name, category, brand, price)
- dim_date (date_key, date, month, quarter, year, is_holiday)
- dim_geography (geo_key, city, state, country, region)
```

**Architecture:**
- **Source Systems**: E-commerce platform, CRM, inventory system
- **Staging Area**: Raw data landing zone
- **ETL Process**: Data validation, transformation, loading
- **Data Warehouse**: Star schema implementation
- **Data Marts**: Sales, customer, inventory specific views

### 15. How would you handle a situation where source data quality is poor?
**Answer:**
**Data Quality Assessment:**
- **Profiling**: Analyze data patterns, distributions, anomalies
- **Validation Rules**: Define business rules and constraints
- **Quality Metrics**: Completeness, accuracy, consistency, timeliness

**Remediation Strategies:**
- **Source System Fixes**: Work with source teams to improve quality
- **Data Cleansing**: Standardize, deduplicate, correct errors
- **Default Values**: Use business-approved defaults for missing data
- **Quarantine Process**: Isolate bad data for manual review
- **Quality Monitoring**: Continuous monitoring and alerting

**Implementation:**
```sql
-- Example data quality check
SELECT 
    'Customer Email' as check_name,
    COUNT(*) as total_records,
    COUNT(email) as non_null_count,
    COUNT(CASE WHEN email LIKE '%@%' THEN 1 END) as valid_email_count,
    ROUND(COUNT(CASE WHEN email LIKE '%@%' THEN 1 END) * 100.0 / COUNT(*), 2) as quality_score
FROM staging.customers;
```

### 16. Design an ETL process for handling late-arriving data.
**Answer:**
**Challenge**: Data arrives after the reporting period has closed.

**Solution Approach:**
1. **Grace Period**: Allow time window for late data
2. **Reprocessing**: Ability to rerun ETL for specific periods
3. **Versioning**: Track different versions of the same data
4. **Notification**: Alert stakeholders of data changes

**Implementation Strategy:**
```sql
-- Track data arrival times
CREATE TABLE data_arrival_log (
    batch_id VARCHAR(50),
    source_system VARCHAR(50),
    business_date DATE,
    arrival_timestamp TIMESTAMP,
    record_count INTEGER,
    status VARCHAR(20)
);

-- Handle late arriving facts
MERGE INTO fact_sales f
USING staging_sales s ON f.transaction_id = s.transaction_id
WHEN MATCHED THEN UPDATE SET
    f.amount = s.amount,
    f.last_updated = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN INSERT VALUES
    (s.transaction_id, s.customer_key, s.amount, CURRENT_TIMESTAMP);
```

### 17. How would you migrate from an on-premises data warehouse to cloud?
**Answer:**
**Migration Strategy:**
1. **Assessment**: Analyze current architecture, data volumes, dependencies
2. **Planning**: Choose cloud platform, migration approach, timeline
3. **Pilot**: Start with non-critical workloads
4. **Parallel Run**: Run both systems simultaneously
5. **Cutover**: Switch to cloud system
6. **Optimization**: Tune performance and costs

**Migration Approaches:**
- **Lift and Shift**: Move existing architecture as-is
- **Re-platforming**: Modify for cloud optimization
- **Re-architecting**: Complete redesign for cloud-native

**Considerations:**
- **Data Transfer**: Network bandwidth, security, costs
- **Downtime**: Minimize business impact
- **Testing**: Validate data integrity and performance
- **Training**: Upskill team on cloud technologies
- **Compliance**: Meet regulatory requirements

---

## Architecture & Design Questions

### 18. Compare different data warehouse architectures.
**Answer:**
**Traditional Architecture (Inmon):**
- Normalized enterprise data warehouse
- Data marts built from EDW
- Top-down approach
- Better data consistency

**Dimensional Architecture (Kimball):**
- Dimensional modeling throughout
- Conformed dimensions
- Bottom-up approach
- Faster implementation

**Modern Cloud Architecture:**
- Separation of compute and storage
- Auto-scaling capabilities
- Pay-per-use pricing
- Managed services

**Lambda Architecture:**
- Batch layer for historical data
- Speed layer for real-time data
- Serving layer for queries
- Handles both batch and streaming

**Kappa Architecture:**
- Stream processing only
- Simpler than Lambda
- Real-time focus
- Event-driven

### 19. Design a real-time data warehouse architecture.
**Answer:**
**Components:**
- **Stream Ingestion**: Kafka, Kinesis, Pub/Sub
- **Stream Processing**: Spark Streaming, Flink, Storm
- **Storage**: Delta Lake, Iceberg for ACID transactions
- **Serving**: Real-time OLAP engines
- **Monitoring**: Data quality, latency, throughput

**Architecture Pattern:**
```
Sources → Message Queue → Stream Processor → Storage → Serving Layer
   ↓           ↓              ↓            ↓         ↓
 Apps      Kafka/Kinesis   Spark/Flink   Delta    Real-time
 APIs      Event Hub       Storm         Lake     Analytics
 IoT       Pub/Sub         Kafka         Iceberg  Dashboards
           Pulsar          Streams       Hudi     APIs
```

**Challenges:**
- **Exactly-once processing**: Avoid duplicates
- **Late data handling**: Out-of-order events
- **Schema evolution**: Handle changing data structures
- **Backpressure**: Handle varying data volumes
- **Fault tolerance**: System resilience

### 20. How would you implement data warehouse security?
**Answer:**
**Security Layers:**

**1. Network Security:**
- VPC/VNet isolation
- Private endpoints
- Firewall rules
- VPN/ExpressRoute connections

**2. Authentication & Authorization:**
- Multi-factor authentication
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- Integration with Active Directory/LDAP

**3. Data Security:**
- Encryption at rest and in transit
- Column-level security
- Row-level security
- Data masking/tokenization

**4. Monitoring & Auditing:**
- Access logging
- Query auditing
- Anomaly detection
- Compliance reporting

**Implementation Example:**
```sql
-- Row-level security
CREATE POLICY customer_policy ON customer_data
FOR SELECT TO sales_role
USING (region = current_user_region());

-- Column-level security
GRANT SELECT (customer_id, name) ON customer_data TO analyst_role;
GRANT SELECT ON customer_data TO admin_role;
```

---

## Performance & Optimization

### 21. What are the key performance optimization techniques for data warehouses?
**Answer:**
**Query Optimization:**
- **Indexing**: B-tree, bitmap, columnstore indexes
- **Partitioning**: Horizontal and vertical partitioning
- **Materialized Views**: Pre-computed aggregations
- **Query Rewriting**: Optimize SQL execution plans

**Storage Optimization:**
- **Compression**: Reduce storage footprint
- **Columnar Storage**: Better for analytical queries
- **Data Distribution**: Minimize data movement
- **Clustering**: Co-locate related data

**ETL Optimization:**
- **Parallel Processing**: Utilize multiple cores/nodes
- **Incremental Loading**: Process only changed data
- **Bulk Operations**: Minimize row-by-row processing
- **Pipeline Optimization**: Eliminate bottlenecks

**Example Optimization:**
```sql
-- Partition by date for time-series data
CREATE TABLE fact_sales (
    sale_date DATE,
    customer_id INT,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

-- Create partitions
CREATE TABLE fact_sales_2024_q1 PARTITION OF fact_sales
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

### 22. How do you monitor and troubleshoot data warehouse performance?
**Answer:**
**Key Metrics:**
- **Query Performance**: Response time, throughput
- **Resource Utilization**: CPU, memory, I/O, network
- **Concurrency**: Active sessions, queue times
- **Data Freshness**: ETL completion times, data latency

**Monitoring Tools:**
- **Native Tools**: Database-specific monitoring
- **Third-party**: DataDog, New Relic, Grafana
- **Custom Dashboards**: Business-specific metrics
- **Alerting**: Proactive issue detection

**Troubleshooting Process:**
1. **Identify**: Use monitoring to detect issues
2. **Analyze**: Examine query plans, resource usage
3. **Diagnose**: Root cause analysis
4. **Resolve**: Apply fixes (indexing, partitioning, etc.)
5. **Validate**: Confirm performance improvement
6. **Document**: Record solutions for future reference

---

## Modern Data Warehousing

### 23. Explain the concept of a cloud-native data warehouse.
**Answer:**
**Characteristics:**
- **Serverless**: No infrastructure management
- **Auto-scaling**: Automatic resource adjustment
- **Pay-per-use**: Cost optimization
- **Managed Services**: Reduced operational overhead
- **API-first**: Programmatic access

**Benefits:**
- **Elasticity**: Handle varying workloads
- **Cost Efficiency**: Pay only for what you use
- **Rapid Deployment**: Quick time to value
- **Global Scale**: Multi-region deployment
- **Integration**: Native cloud service integration

**Examples:**
- **Snowflake**: Multi-cloud data warehouse
- **BigQuery**: Google's serverless data warehouse
- **Redshift Serverless**: AWS serverless option
- **Synapse Analytics**: Microsoft's cloud DW

### 24. What is the role of machine learning in modern data warehouses?
**Answer:**
**ML Applications:**
- **Query Optimization**: Automatic performance tuning
- **Anomaly Detection**: Identify data quality issues
- **Predictive Analytics**: Forecast resource needs
- **Auto-scaling**: Intelligent resource management
- **Data Classification**: Automatic data discovery

**Implementation Patterns:**
- **In-database ML**: SQL-based ML functions
- **External ML**: Integration with ML platforms
- **Feature Stores**: Centralized feature management
- **MLOps Integration**: ML pipeline automation

**Example:**
```sql
-- BigQuery ML example
CREATE MODEL customer_segmentation
OPTIONS(model_type='kmeans', num_clusters=4)
AS
SELECT
    customer_id,
    total_purchases,
    avg_order_value,
    days_since_last_purchase
FROM customer_metrics;
```

### 25. How do you implement data mesh principles in data warehousing?
**Answer:**
**Data Mesh Principles:**
1. **Domain-oriented**: Decentralized data ownership
2. **Data as a Product**: Treat data like products
3. **Self-serve Infrastructure**: Enable domain autonomy
4. **Federated Governance**: Distributed but coordinated

**Implementation:**
- **Domain Data Warehouses**: Department-specific DWs
- **Data Products**: Well-defined data interfaces
- **Shared Infrastructure**: Common platform services
- **Global Governance**: Consistent standards and policies

**Architecture:**
```
Domain A DW ←→ Data Mesh Platform ←→ Domain B DW
     ↓              ↓                    ↓
Data Products   Shared Services    Data Products
     ↓              ↓                    ↓
Consumers      Governance Tools     Consumers
```

**Benefits:**
- **Scalability**: Distributed ownership
- **Agility**: Faster domain-specific development
- **Quality**: Domain expertise applied to data
- **Innovation**: Reduced central bottlenecks