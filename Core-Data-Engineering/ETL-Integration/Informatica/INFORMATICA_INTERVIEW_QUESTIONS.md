# Informatica Interview Questions for Data Engineers

## Basic Level Questions

### 1. What is Informatica PowerCenter and its key components?
**Answer**: Informatica PowerCenter is an enterprise data integration platform that provides ETL capabilities. Key components:
- **PowerCenter Designer**: Development environment for creating mappings
- **Workflow Manager**: Create and manage workflows and sessions
- **Workflow Monitor**: Monitor and troubleshoot workflows
- **Repository Manager**: Manage metadata repository
- **Administration Console**: Configure and manage PowerCenter services

```
Repository Structure:
├── Sources (Tables, Files, Applications)
├── Targets (Tables, Files, Applications)  
├── Transformations (Expression, Aggregator, Lookup, etc.)
├── Mappings (Data flow logic)
├── Sessions (Execution instructions)
├── Workflows (Orchestration logic)
└── Mapplets (Reusable mapping logic)
```

### 2. Explain the difference between connected and unconnected transformations
**Answer**: 
- **Connected Transformations**: Part of the data flow pipeline, receive data from upstream transformations
- **Unconnected Transformations**: Called from other transformations, not part of main data flow

```
Connected Lookup Example:
Source → Lookup → Target
(Data flows through lookup transformation)

Unconnected Lookup Example:
Source → Expression → Target
         ↓
    :LKP.LOOKUP_TRANSFORMATION(input_port)
(Lookup called from Expression transformation)
```

**Connected Lookup Configuration**:
- Return multiple columns
- Cache all lookup data
- Part of data flow

**Unconnected Lookup Configuration**:
- Return single value
- Called on-demand
- Better performance for selective lookups

### 3. What are the different types of Informatica transformations?
**Answer**: Informatica transformations categorized by functionality:

**Active Transformations** (change number of rows):
- **Aggregator**: Group and calculate aggregate functions
- **Filter**: Filter rows based on conditions
- **Joiner**: Join data from multiple sources
- **Normalizer**: Convert denormalized data to normalized
- **Rank**: Rank data and return top/bottom records
- **Router**: Route data to multiple targets based on conditions
- **Sorter**: Sort data
- **Union**: Combine data from multiple sources

**Passive Transformations** (don't change number of rows):
- **Expression**: Calculate values, string manipulation
- **Lookup**: Look up reference data
- **Sequence Generator**: Generate sequential numbers
- **Stored Procedure**: Call database stored procedures
- **Update Strategy**: Determine insert/update/delete operations

### 4. How do you handle slowly changing dimensions (SCD) in Informatica?
**Answer**: SCD implementation strategies:

**SCD Type 1 (Overwrite)**:
```
Mapping Flow:
Source → Expression (data cleansing) → Lookup (existing records) → 
Expression (flag new/existing) → Update Strategy → Target

Update Strategy Transformation:
- DD_UPDATE for existing records
- DD_INSERT for new records
```

**SCD Type 2 (Historical Tracking)**:
```
Mapping Flow:
Source → Lookup (check for changes) → Router → 
├── Insert Flow (new records)
├── Update Flow (expire old records)  
└── Insert Flow (new versions)

Router Conditions:
- New Records: ISNULL(LKP_KEY)
- Changed Records: NOT ISNULL(LKP_KEY) AND (SRC_COL != LKP_COL)
- Unchanged Records: NOT ISNULL(LKP_KEY) AND (SRC_COL = LKP_COL)
```

### 5. What is the difference between Joiner and Lookup transformations?
**Answer**: 

**Joiner Transformation**:
- Joins data from two sources
- Both sources must be sorted for sorted join
- Supports inner, outer, full outer, and detail outer joins
- Memory intensive for unsorted joins
- Returns all matching records

**Lookup Transformation**:
- Looks up reference data
- Can be connected or unconnected
- Supports only equi-joins
- Can cache lookup data for performance
- Returns first matching record (unless configured otherwise)

```
Joiner Example:
Source1 (Orders) → Joiner ← Source2 (Customers)
Join Condition: Orders.customer_id = Customers.customer_id

Lookup Example:
Source (Orders) → Lookup (Customers) → Target
Lookup Condition: Orders.customer_id = Customers.customer_id
Return: Customer_name
```

## Intermediate Level Questions

### 6. How do you optimize Informatica mapping performance?
**Answer**: Performance optimization techniques:

**Source Optimization**:
- Use source qualifier filters
- Select only required columns
- Use database hints
- Implement source-side joins when possible

```
Source Qualifier SQL Override:
SELECT order_id, customer_id, order_date, total_amount
FROM orders 
WHERE order_date >= SYSDATE - 30
AND status = 'COMPLETED'
```

**Transformation Optimization**:
- Use Sorter transformation before Aggregator
- Enable sorted input for Aggregator when data is pre-sorted
- Use Filter transformation early in the flow
- Minimize data type conversions

**Target Optimization**:
- Use bulk loading when possible
- Disable database logging for large loads
- Use parallel processing
- Implement proper indexing strategy

**Session Configuration**:
```
Performance Settings:
- DTM Buffer Size: 64MB - 128MB
- Commit Interval: 10,000 - 50,000
- Tracing Level: Normal (not Verbose)
- Collect Performance Data: Enabled
- Pushdown Optimization: Full or Partial
```

### 7. Explain Informatica session and workflow configuration
**Answer**: 

**Session Configuration**:
- **Mapping**: Associates session with mapping
- **Source/Target Connections**: Database connections
- **Config Object**: Runtime parameters and variables
- **Performance**: Buffer sizes, commit intervals
- **Error Handling**: Error thresholds and logging

**Workflow Configuration**:
```
Workflow Components:
├── Start Task (Begin workflow execution)
├── Session Tasks (Execute mappings)
├── Command Tasks (Execute shell commands)
├── Email Tasks (Send notifications)
├── Decision Tasks (Conditional logic)
├── Assignment Tasks (Set variables)
├── Timer Tasks (Schedule delays)
└── Control Tasks (Workflow control)

Workflow Links:
- Success Link: Execute on successful completion
- Failure Link: Execute on failure
- Unconditional Link: Always execute
```

**Parameter File Example**:
```
[Global]
$$DBConnection_Source=Oracle_Source
$$DBConnection_Target=Oracle_Target

[Session1]
$PMSourceFileDir=/data/input
$PMTargetFileDir=/data/output
$$ErrorThreshold=100
```

### 8. How do you implement error handling in Informatica?
**Answer**: Comprehensive error handling strategies:

**Session-Level Error Handling**:
```
Error Handling Configuration:
- Stop on Errors: 0 (continue processing)
- Error Threshold: 1000 (stop after 1000 errors)
- Error Log Type: Database/File
- Save Session Log: Enabled
- Session Log Filter: Detailed/Normal/Terse
```

**Transformation-Level Error Handling**:
```
Expression Transformation:
ERROR_OUTPUT = IIF(ISNULL(INPUT_COLUMN), 
                   'NULL_VALUE_ERROR', 
                   'SUCCESS')

Router Transformation:
- Valid Data Group: NOT ISNULL(customer_id) AND LEN(customer_id) > 0
- Error Data Group: ISNULL(customer_id) OR LEN(customer_id) = 0
```

**Workflow-Level Error Handling**:
```
Workflow Design:
Session1 → Decision Task → Email Task (on failure)
         → Session2 (on success)

Decision Task Condition:
$Session1.Status = SUCCEEDED
```

### 9. What are Informatica mapplets and when would you use them?
**Answer**: Mapplets are reusable mapping components that contain transformation logic:

**Benefits**:
- Code reusability across mappings
- Standardized business logic
- Easier maintenance and updates
- Modular design approach

**Mapplet Structure**:
```
Mapplet Components:
├── Input Transformation (receive data)
├── Business Logic Transformations
├── Output Transformation (return data)
└── Input/Output Ports Definition

Example: Address Standardization Mapplet
Input → Expression (clean address) → 
Lookup (validate zip code) → 
Expression (format address) → Output
```

**Using Mapplets**:
```
Main Mapping:
Source → Mapplet (Address_Standardization) → Target

Mapplet Call:
- Input: Raw address fields
- Output: Standardized address fields
- Reusable across multiple mappings
```

### 10. How do you implement incremental data loading in Informatica?
**Answer**: Incremental loading strategies:

**Timestamp-Based Incremental Loading**:
```
Mapping Design:
Source → Source Qualifier → Filter → Target

Source Qualifier Filter:
last_modified_date > $$LAST_EXTRACT_DATE

Session Parameter:
$$LAST_EXTRACT_DATE = 2024-01-01 00:00:00
```

**Change Data Capture (CDC)**:
```
CDC Mapping Flow:
CDC Source → Expression (determine operation) → 
Router → Insert/Update/Delete Targets

Router Groups:
- Insert: CDC_OPERATION = 'I'
- Update: CDC_OPERATION = 'U'  
- Delete: CDC_OPERATION = 'D'
```

**Key-Based Incremental Loading**:
```
Mapping Flow:
Source → Lookup (existing records) → 
Expression (compare values) → 
Router (new/changed/unchanged) → Targets

Lookup Query:
SELECT key_column, checksum_column 
FROM target_table

Comparison Logic:
CHANGED_FLAG = IIF(ISNULL(LKP_KEY), 'NEW',
                   IIF(SRC_CHECKSUM != LKP_CHECKSUM, 'CHANGED', 'UNCHANGED'))
```

## Advanced Level Questions

### 11. How do you implement complex data integration patterns in Informatica?
**Answer**: Advanced integration patterns:

**Hub and Spoke Pattern**:
```
Architecture:
Multiple Sources → Staging Area → Data Warehouse → Data Marts

Implementation:
1. Extract workflows: Source systems → Staging tables
2. Transform workflows: Staging → Dimensional model
3. Load workflows: Dimensional model → Data marts
```

**Real-time Data Integration**:
```
PowerExchange Real-time:
Source System → PowerExchange → Informatica → Target

Configuration:
- PowerExchange Listener: Capture changes
- PowerExchange Navigator: Route changes
- Real-time Session: Process changes immediately
```

**Master Data Management (MDM)**:
```
MDM Workflow:
Multiple Sources → Data Quality → Match/Merge → 
Golden Record → Distribute to Systems

Transformations:
- Data Standardization (Expression)
- Duplicate Detection (Match transformation)
- Record Consolidation (Merge transformation)
- Survivorship Rules (Expression)
```

### 12. How do you implement data quality and data profiling in Informatica?
**Answer**: Data quality implementation using Informatica Data Quality (IDQ):

**Data Profiling**:
```
Profiling Workflow:
Source → Profiler Transformation → Profile Results

Profile Analysis:
- Column Analysis: Data types, patterns, null values
- Dependency Analysis: Functional dependencies
- Redundancy Analysis: Duplicate detection
- Domain Discovery: Value frequency analysis
```

**Data Quality Rules**:
```
Rule Specifications:
1. Completeness Rules:
   - NOT NULL checks
   - Required field validation
   
2. Validity Rules:
   - Format validation (email, phone)
   - Range validation (dates, amounts)
   
3. Consistency Rules:
   - Cross-field validation
   - Business rule validation

Implementation:
Source → Rule Specification → 
Scoreboard (quality metrics) → 
Cleansed Data Output
```

**Address Validation**:
```
Address Validation Flow:
Raw Address → Address Validator → 
Standardized Address + Quality Score

Output Fields:
- Validated Address
- Confidence Score
- Validation Status
- Standardization Level
```

### 13. How do you implement Informatica Cloud (IICS) for modern data integration?
**Answer**: Informatica Intelligent Cloud Services (IICS) implementation:

**Cloud Data Integration**:
```
IICS Components:
├── Data Integration (Cloud ETL)
├── Application Integration (API management)
├── Data Quality (Cloud DQ)
├── Master Data Management (Cloud MDM)
└── Data Governance (Axon)

Mapping Design:
Cloud Source → Transformation → Cloud Target
- Pre-built connectors for SaaS applications
- Serverless compute environment
- Auto-scaling capabilities
```

**Hybrid Integration**:
```
Architecture:
On-premises Sources → Secure Agent → 
IICS Cloud → Cloud Targets

Secure Agent:
- Lightweight runtime engine
- Installed on-premises or private cloud
- Secure connection to IICS
- Handles data movement and transformation
```

**API Integration**:
```
REST API Mapping:
API Source → JSON Parser → 
Data Transformation → Target

Configuration:
- Authentication (OAuth, API Key)
- Request/Response handling
- Error handling and retry logic
- Rate limiting compliance
```

### 14. How do you implement Informatica B2B Data Exchange?
**Answer**: B2B Data Exchange for partner integration:

**B2B Gateway Configuration**:
```
B2B Components:
├── Trading Partner Management
├── Document Standards (EDI, XML, JSON)
├── Protocol Support (AS2, FTP, HTTP)
├── Transformation Engine
└── Monitoring and Tracking

Partner Setup:
- Partner Profile Configuration
- Certificate Management
- Protocol Configuration
- Document Type Definitions
```

**EDI Processing**:
```
EDI Workflow:
Inbound: Partner → B2B Gateway → Parse → 
Transform → Validate → Application

Outbound: Application → Transform → 
Generate EDI → B2B Gateway → Partner

Document Types:
- 850 (Purchase Order)
- 810 (Invoice)
- 856 (Advance Ship Notice)
- 997 (Functional Acknowledgment)
```

### 15. How do you implement Informatica PowerCenter performance monitoring and tuning?
**Answer**: Comprehensive performance monitoring and optimization:

**Performance Monitoring**:
```
Monitoring Tools:
1. Workflow Monitor:
   - Session performance statistics
   - Transformation-level metrics
   - Error analysis and debugging

2. Repository Reports:
   - Mapping analysis reports
   - Session performance reports
   - Workflow dependency reports

3. Performance Counters:
   - Throughput (rows/second)
   - Buffer utilization
   - CPU and memory usage
```

**Advanced Tuning Techniques**:
```
Pushdown Optimization:
- Full Pushdown: All transformations to database
- Partial Pushdown: Selected transformations
- Source-side Pushdown: Joins and filters at source

Configuration:
Session Properties → Config Object → 
Advanced → Pushdown Optimization = Full

Partitioning:
- Round-robin partitioning
- Hash partitioning  
- Key range partitioning
- Pass-through partitioning

Partition Configuration:
Transformation → Properties → Partition → 
Partition Type = Hash Auto-Keys
```

**Memory and Buffer Tuning**:
```
DTM Configuration:
- Buffer Block Size: 64KB (default)
- Index Cache Size: 1,000,000 bytes
- Data Cache Size: 2,000,000 bytes
- Buffer Pool Size: Auto (recommended)

Session Configuration:
- Commit Interval: 10,000 rows
- Target Load Type: Bulk (when possible)
- Collect Performance Data: Yes
- Write Backward Compatible Session Log: No
```

## Data Engineering Specific Questions

### 16. How do you implement data lineage and impact analysis in Informatica?
**Answer**: Data lineage tracking and impact analysis:

**Metadata Management**:
```
Lineage Components:
├── Source Systems (Tables, Files, APIs)
├── Transformations (Business Logic)
├── Target Systems (Data Warehouse, Data Lake)
└── Dependencies (Upstream/Downstream)

Repository Queries:
- REP_SESS_LOG: Session execution history
- REP_LOAD_SUMMARY: Data load statistics  
- REP_TASK_INST_LOG: Task instance details
```

**Impact Analysis Queries**:
```sql
-- Find all mappings using a specific source table
SELECT DISTINCT m.mapping_name, m.version_number
FROM OPB_MAPPING m
JOIN OPB_MAPPING_PARAMS mp ON m.mapping_id = mp.mapping_id
WHERE mp.param_name = 'SOURCE_TABLE_NAME'
AND mp.param_value = 'CUSTOMERS';

-- Find downstream dependencies
SELECT s.subject_name as source_object,
       d.subject_name as dependent_object,
       dep.dependency_type
FROM OPB_SUBJECT s
JOIN OPB_DEPENDENCY dep ON s.subject_id = dep.subject_id
JOIN OPB_SUBJECT d ON dep.depends_on_id = d.subject_id
WHERE s.subject_name = 'CUSTOMER_MAPPING';
```

### 17. How do you implement data archiving and retention policies?
**Answer**: Data archiving strategies in Informatica:

**Archival Workflow Design**:
```
Archive Process:
1. Identify Archive Candidates:
   Source → Filter (archive criteria) → 
   Archive Target + Delete Source

2. Staged Archival:
   Source → Staging → Validation → 
   Archive Target → Source Cleanup

Archive Criteria Examples:
- Date-based: Records older than 7 years
- Status-based: Closed/Completed records
- Business rules: Inactive customers
```

**Retention Policy Implementation**:
```
Mapping Logic:
Source → Expression → Router → Multiple Targets

Expression Transformation:
ARCHIVE_FLAG = IIF(
    MONTHS_BETWEEN(SYSDATE, LAST_ACTIVITY_DATE) > 84, -- 7 years
    'ARCHIVE',
    'RETAIN'
)

Router Groups:
- Archive Group: ARCHIVE_FLAG = 'ARCHIVE'
- Retain Group: ARCHIVE_FLAG = 'RETAIN'
```

### 18. How do you implement Informatica for big data processing?
**Answer**: Big data integration with Informatica:

**Hadoop Integration**:
```
Big Data Components:
├── Informatica Big Data Management (BDM)
├── Blaze Engine (In-memory processing)
├── Hadoop Connectors (HDFS, Hive, HBase)
└── Spark Integration

Mapping Design:
HDFS Source → Blaze Transformation → 
Hive Target

Configuration:
- Blaze Engine: High-performance processing
- Cluster Mode: Distribute processing
- Memory Optimization: In-memory operations
```

**Data Lake Integration**:
```
Data Lake Architecture:
Raw Data → Informatica → Processed Data

Processing Layers:
1. Bronze (Raw): Direct ingestion from sources
2. Silver (Cleansed): Data quality and standardization  
3. Gold (Curated): Business-ready datasets

Informatica Role:
- Data ingestion from multiple sources
- Schema evolution handling
- Data quality and governance
- Metadata management
```

This comprehensive Informatica interview question set covers essential knowledge for data engineers, from basic PowerCenter concepts to advanced enterprise integration patterns and big data processing capabilities.