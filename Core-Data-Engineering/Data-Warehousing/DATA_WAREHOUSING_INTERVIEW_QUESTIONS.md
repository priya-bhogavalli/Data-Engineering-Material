# Data Warehousing Interview Questions

## Data Warehousing Fundamentals

### Q1: What is a data warehouse and how does it differ from a database?
**Answer**: 
- **Data Warehouse**: Centralized repository optimized for analytical queries and reporting
- **Database**: Operational system optimized for transactional processing (OLTP)
- **Key Differences**: 
  - Purpose: Analytics vs transactions
  - Schema: Denormalized vs normalized
  - Query patterns: Complex analytical vs simple transactional
  - Data volume: Large historical datasets vs current operational data
- **Integration**: Data warehouse integrates data from multiple operational systems

### Q2: Explain the difference between OLTP and OLAP systems
**Answer**:
- **OLTP (Online Transaction Processing)**: 
  - Real-time transaction processing
  - Normalized schemas, row-oriented storage
  - High concurrency, low latency
  - Current data focus
- **OLAP (Online Analytical Processing)**:
  - Complex analytical queries
  - Denormalized schemas, column-oriented storage
  - Lower concurrency, higher throughput
  - Historical data analysis
- **Use Cases**: OLTP for operations, OLAP for business intelligence

### Q3: What are the key components of a data warehouse architecture?
**Answer**:
- **Data Sources**: Operational systems, external data, files
- **ETL Layer**: Extract, Transform, Load processes
- **Staging Area**: Temporary storage for data transformation
- **Data Warehouse**: Core repository with integrated, cleaned data
- **Data Marts**: Subject-specific subsets of the warehouse
- **Presentation Layer**: Reporting tools, dashboards, OLAP cubes
- **Metadata Repository**: Data about data, lineage, and definitions

## Dimensional Modeling

### Q4: Explain dimensional modeling and its key concepts
**Answer**:
- **Purpose**: Optimize data warehouse design for analytical queries
- **Fact Tables**: Contain measures/metrics and foreign keys to dimensions
- **Dimension Tables**: Contain descriptive attributes for analysis
- **Star Schema**: Central fact table surrounded by dimension tables
- **Snowflake Schema**: Normalized dimension tables with hierarchies
- **Benefits**: Query performance, business user friendliness, consistent metrics

### Q5: What are the different types of fact tables?
**Answer**:
- **Transaction Facts**: Record individual business events (sales, orders)
- **Snapshot Facts**: Capture state at specific points in time (account balances)
- **Accumulating Facts**: Track progress through business processes (order lifecycle)
- **Factless Facts**: Record events without measures (student enrollment)
- **Aggregate Facts**: Pre-calculated summaries for performance
- **Design Considerations**: Grain definition, additive vs non-additive measures

### Q6: How do you handle slowly changing dimensions (SCDs)?
**Answer**:
- **Type 0**: Retain original (no changes allowed)
- **Type 1**: Overwrite (lose history) - for corrections
- **Type 2**: Add new record (preserve history) - most common
- **Type 3**: Add new attribute (limited history)
- **Type 4**: History table (separate current and historical)
- **Type 6**: Hybrid approach (combines Types 1, 2, and 3)
- **Implementation**: Effective dates, version numbers, current flags

## ETL and Data Integration

### Q7: What are the key phases of the ETL process?
**Answer**:
- **Extract**: Retrieve data from source systems
  - Full extraction vs incremental extraction
  - Change data capture (CDC) techniques
- **Transform**: Clean, validate, and restructure data
  - Data cleansing, standardization, business rule application
  - Lookups, aggregations, calculations
- **Load**: Insert data into target warehouse
  - Initial load vs incremental load
  - Bulk loading techniques for performance

### Q8: Compare ETL vs ELT approaches in data warehousing
**Answer**:
- **ETL (Extract-Transform-Load)**:
  - Transform data before loading
  - Suitable for structured data and predefined schemas
  - Better for data warehouses with limited compute power
- **ELT (Extract-Load-Transform)**:
  - Load raw data first, then transform
  - Leverages target system's compute power
  - Better for cloud data warehouses and big data
- **Modern Trend**: ELT gaining popularity with cloud platforms

### Q9: How do you handle data quality in ETL processes?
**Answer**:
- **Data Profiling**: Analyze source data characteristics and quality
- **Validation Rules**: Check completeness, accuracy, consistency
- **Cleansing**: Standardize formats, correct errors, handle nulls
- **Exception Handling**: Quarantine bad data, error reporting
- **Monitoring**: Track data quality metrics and trends
- **Feedback**: Communicate issues back to source systems
- **Documentation**: Maintain data quality rules and procedures

## Performance Optimization

### Q10: What techniques do you use to optimize data warehouse query performance?
**Answer**:
- **Indexing**: Create appropriate indexes on frequently queried columns
- **Partitioning**: Divide large tables by date, region, or other criteria
- **Materialized Views**: Pre-compute expensive aggregations
- **Columnar Storage**: Optimize for analytical query patterns
- **Compression**: Reduce storage and I/O requirements
- **Statistics**: Keep table statistics updated for query optimizer
- **Query Optimization**: Analyze execution plans and rewrite queries

### Q11: How do you design partitioning strategies for large fact tables?
**Answer**:
- **Partition Keys**: Choose based on query patterns (usually date)
- **Partition Pruning**: Ensure queries can eliminate unnecessary partitions
- **Partition Size**: Balance between too many small vs few large partitions
- **Maintenance**: Automated partition creation and dropping
- **Indexing**: Partition-wise indexing strategies
- **Parallel Processing**: Leverage partition-wise operations
- **Monitoring**: Track partition usage and performance

### Q12: What are aggregate tables and when should you use them?
**Answer**:
- **Purpose**: Pre-calculated summaries for faster query response
- **Types**: Daily, weekly, monthly aggregates at different grain levels
- **Benefits**: Improved query performance, reduced resource usage
- **Trade-offs**: Storage overhead, maintenance complexity, data freshness
- **Automation**: Automated aggregate creation and refresh
- **Query Rewriting**: Transparent use of aggregates by query optimizer
- **Maintenance**: Regular refresh and validation processes

## Modern Data Warehouse Technologies

### Q13: Compare traditional on-premises vs cloud data warehouses
**Answer**:
- **On-Premises**: 
  - Fixed capacity, high upfront costs
  - Full control over infrastructure and security
  - Predictable performance, complex maintenance
- **Cloud**: 
  - Elastic scaling, pay-as-you-go pricing
  - Managed services, reduced operational overhead
  - Global availability, built-in disaster recovery
- **Hybrid**: Combination approach for specific requirements
- **Migration**: Strategies for moving from on-premises to cloud

### Q14: What are the advantages of columnar storage in data warehouses?
**Answer**:
- **Analytical Queries**: Optimized for reading specific columns
- **Compression**: Better compression ratios due to similar data types
- **I/O Reduction**: Read only required columns, not entire rows
- **Vectorized Processing**: Efficient CPU utilization for analytics
- **Aggregation Performance**: Faster sum, count, average operations
- **Trade-offs**: Slower for transactional workloads, row reconstruction overhead
- **Examples**: Amazon Redshift, Google BigQuery, Snowflake

### Q15: Explain the concept of a data lakehouse and its benefits
**Answer**:
- **Definition**: Architecture combining data lake flexibility with warehouse performance
- **Key Features**: ACID transactions, schema enforcement, time travel
- **Benefits**: Single platform for all analytics, cost-effective, open standards
- **Technologies**: Delta Lake, Apache Iceberg, Apache Hudi
- **Use Cases**: Organizations wanting both flexibility and performance
- **Challenges**: Technology maturity, skill requirements, migration complexity

## Data Warehouse Design Patterns

### Q16: What is a conformed dimension and why is it important?
**Answer**:
- **Definition**: Dimension shared across multiple fact tables with consistent structure
- **Benefits**: Consistent reporting across business processes, drill-across queries
- **Examples**: Customer, product, time dimensions used in multiple marts
- **Implementation**: Master dimension tables, standardized attributes
- **Challenges**: Organizational alignment, change management
- **Governance**: Centralized ownership and maintenance processes

### Q17: How do you handle real-time requirements in data warehousing?
**Answer**:
- **Near Real-Time**: Frequent micro-batch loading (every few minutes)
- **Streaming Integration**: Direct streaming into warehouse (Kafka, Kinesis)
- **Change Data Capture**: Real-time capture of source system changes
- **Operational Data Store**: Intermediate layer for real-time operational reporting
- **Hybrid Architecture**: Combine batch and streaming processing
- **Trade-offs**: Complexity vs latency, consistency vs availability

### Q18: What are data marts and how do they relate to the enterprise data warehouse?
**Answer**:
- **Definition**: Subject-specific subsets of the enterprise data warehouse
- **Types**: Dependent (sourced from EDW) vs independent (sourced directly)
- **Benefits**: Focused on specific business areas, improved performance
- **Design**: Star schema optimized for specific analytical needs
- **Governance**: Balance between centralization and decentralization
- **Integration**: Ensure consistency with enterprise data warehouse

## Data Warehouse Administration

### Q19: How do you monitor and maintain data warehouse performance?
**Answer**:
- **Performance Metrics**: Query response times, throughput, resource utilization
- **Monitoring Tools**: Database-specific and third-party monitoring solutions
- **Capacity Planning**: Forecast growth and resource requirements
- **Maintenance Tasks**: Index rebuilding, statistics updates, partition management
- **Alerting**: Proactive notifications for performance issues
- **Optimization**: Regular performance tuning and query optimization
- **Documentation**: Maintain runbooks and troubleshooting guides

### Q20: What strategies do you use for data warehouse backup and recovery?
**Answer**:
- **Backup Types**: Full, incremental, differential backups
- **Recovery Models**: Point-in-time recovery, disaster recovery
- **Cloud Strategies**: Automated backups, cross-region replication
- **Testing**: Regular restore testing and disaster recovery drills
- **Documentation**: Recovery procedures and contact information
- **RTO/RPO**: Define recovery time and point objectives
- **Compliance**: Meet regulatory requirements for data retention

### Q21: How do you handle data warehouse security and access control?
**Answer**:
- **Authentication**: User identity verification and management
- **Authorization**: Role-based access control (RBAC)
- **Row-Level Security**: Restrict data access based on user attributes
- **Column-Level Security**: Hide sensitive columns from unauthorized users
- **Data Masking**: Protect sensitive data in non-production environments
- **Audit Logging**: Track data access and modifications
- **Encryption**: Protect data at rest and in transit

## Advanced Topics

### Q22: How do you implement data lineage in a data warehouse environment?
**Answer**:
- **Source-to-Target Mapping**: Document data flow from sources to warehouse
- **ETL Documentation**: Capture transformation logic and business rules
- **Impact Analysis**: Understand effects of changes on downstream systems
- **Automated Tools**: Use metadata management tools for lineage tracking
- **Visualization**: Graphical representation of data flows
- **Governance**: Maintain lineage documentation as part of change management
- **Compliance**: Support audit and regulatory requirements

### Q23: What are the considerations for multi-tenant data warehouse design?
**Answer**:
- **Isolation Models**: Separate databases, schemas, or row-level security
- **Performance**: Ensure one tenant doesn't impact others
- **Scalability**: Design for varying tenant sizes and growth
- **Security**: Strong isolation and access controls
- **Customization**: Support tenant-specific requirements
- **Monitoring**: Per-tenant performance and usage tracking
- **Cost Allocation**: Fair billing and resource allocation

### Q24: How do you handle data warehouse modernization and migration?
**Answer**:
- **Assessment**: Evaluate current state and identify modernization opportunities
- **Strategy**: Big bang vs phased migration approach
- **Data Migration**: ETL processes for moving historical data
- **Application Migration**: Update reporting and analytics applications
- **Testing**: Comprehensive testing of migrated data and applications
- **Rollback Plan**: Procedures for reverting if issues arise
- **Training**: User education on new platform capabilities
- **Optimization**: Leverage new platform features for improved performance

### Q25: What are the emerging trends in data warehousing?
**Answer**:
- **Cloud-Native**: Fully managed, serverless data warehouse services
- **Separation of Compute and Storage**: Independent scaling capabilities
- **Real-Time Analytics**: Integration with streaming and real-time processing
- **AI/ML Integration**: Built-in machine learning capabilities
- **Data Mesh**: Decentralized data ownership and management
- **Lakehouse Architecture**: Combining data lake and warehouse benefits
- **Automated Optimization**: Self-tuning and self-managing capabilities
- **Multi-Cloud**: Support for hybrid and multi-cloud deployments