# Talend - Quick Reference Guide

## 🚀 **Essential Components**

### **Input Components**
```
tFileInputDelimited    - Read delimited files (CSV, TSV)
tFileInputExcel        - Read Excel files
tMysqlInput           - Read from MySQL database
tOracleInput          - Read from Oracle database
tPostgresqlInput      - Read from PostgreSQL database
tMongoDBInput         - Read from MongoDB
tKafkaInput           - Read from Kafka topics
tRestClient           - Call REST APIs
```

### **Processing Components**
```
tMap                  - Main transformation component
tFilterRow            - Filter records based on conditions
tSortRow              - Sort data by specified columns
tUniqRow              - Remove duplicate records
tAggregate            - Aggregate data (sum, count, avg)
tJoin                 - Join two data flows
tDenormalize          - Convert normalized to denormalized data
tNormalize            - Convert denormalized to normalized data
```

### **Output Components**
```
tFileOutputDelimited  - Write to delimited files
tFileOutputExcel      - Write to Excel files
tMysqlOutput          - Write to MySQL database
tOracleOutput         - Write to Oracle database
tPostgresqlOutput     - Write to PostgreSQL database
tMongoDBOutput        - Write to MongoDB
tKafkaOutput          - Write to Kafka topics
tLogRow               - Log data for debugging
```

### **Flow Control Components**
```
tRunJob               - Execute child jobs
tLoop                 - Simple loop execution
tFlowToIterate        - Convert flow to iteration
tIterateToFlow        - Convert iteration to flow
tIf                   - Conditional execution
tDie                  - Stop job execution
tWarn                 - Generate warnings
```

## 🔧 **Common Functions**

### **String Functions**
```java
StringHandling.UPCASE(input.column)           // Convert to uppercase
StringHandling.DOWNCASE(input.column)         // Convert to lowercase
StringHandling.LEN(input.column)              // Get string length
StringHandling.LEFT(input.column, 5)          // Get left 5 characters
StringHandling.RIGHT(input.column, 3)         // Get right 3 characters
StringHandling.TRIM(input.column)             // Remove leading/trailing spaces
StringHandling.REPLACE(input.column, "old", "new") // Replace text
```

### **Date Functions**
```java
TalendDate.getCurrentDate()                   // Get current date
TalendDate.formatDate("yyyy-MM-dd", input.date) // Format date
TalendDate.parseDate("yyyy-MM-dd", input.dateStr) // Parse date string
TalendDate.addDate(input.date, 30, "dd")      // Add 30 days
TalendDate.diffDate(date1, date2, "dd")       // Difference in days
```

### **Numeric Functions**
```java
Numeric.sequence("seq1", 1, 1)                // Generate sequence
Math.abs(input.number)                        // Absolute value
Math.round(input.decimal)                     // Round to nearest integer
Math.ceil(input.decimal)                      // Round up
Math.floor(input.decimal)                     // Round down
```

### **Conditional Functions**
```java
input.column == null ? "default" : input.column  // Null check
input.amount > 1000 ? "High" : "Low"             // Conditional assignment
```

## 📊 **tMap Configuration**

### **Join Types**
```
Inner Join    - Only matching records
Left Join     - All left records + matching right
Right Join    - All right records + matching left
Full Join     - All records from both sides
```

### **Lookup Settings**
```
Load once                    - Load at job start
Reload at each row          - Reload for each main row
Reload at each row (cache)  - Cached reload
Store temp                  - Temporary storage
```

### **Expression Examples**
```java
// Concatenation
input.first_name + " " + input.last_name

// Conditional logic
input.age >= 18 ? "Adult" : "Minor"

// Date calculations
TalendDate.addDate(input.order_date, 30, "dd")

// String manipulation
StringHandling.UPCASE(StringHandling.TRIM(input.name))
```

## 🔄 **Context Variables**

### **System Contexts**
```
context.projectName       - Current project name
context.jobName          - Current job name
context.jobVersion       - Job version
context.pid              - Process ID
```

### **Custom Context Usage**
```java
// In job
context.db_host          // Database host
context.db_port          // Database port
context.file_path        // File path
context.batch_size       // Batch size
```

## 🗄️ **Database Connections**

### **Connection Properties**
```
Host: context.db_host
Port: context.db_port
Database: context.db_name
Username: context.db_user
Password: context.db_password
```

### **Common SQL Patterns**
```sql
-- Incremental load
SELECT * FROM table WHERE modified_date > ?

-- Upsert pattern
MERGE INTO target USING source ON (key_match)
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...

-- Delete before insert
DELETE FROM target WHERE condition;
INSERT INTO target SELECT * FROM source;
```

## 🔍 **Debugging Tips**

### **Data Inspection**
```
tLogRow               - View data in console
tFileOutputDelimited  - Write data to file for inspection
Statistics            - Enable to see row counts
Traces               - Enable for detailed logging
```

### **Error Handling**
```
Die on Error: false   - Continue on errors
Reject links         - Capture error records
tLogCatcher          - Catch and log errors
tWarn                - Generate warnings
```

## 📈 **Performance Tips**

### **Memory Optimization**
```
tMap buffer size: Adjust based on data volume
JVM settings: -Xms2g -Xmx8g
Streaming: Use for large datasets
Parallel execution: Enable where possible
```

### **Database Performance**
```
Batch size: 1000-10000 records
Connection pooling: Enable
Bulk operations: Use tBulkExec
Indexes: Ensure proper indexing
```

## 🚀 **Deployment Commands**

### **Command Line Execution**
```bash
# Windows
job_name.bat --context_param db_host=localhost

# Linux
./job_name.sh --context_param db_host=localhost

# With additional parameters
./job_name.sh --context_param db_host=prod-server --context_param batch_size=5000
```

### **TAC Deployment**
```
1. Export job as .zip file
2. Import to TAC
3. Configure contexts for target environment
4. Schedule or execute manually
```

## 🔒 **Security Quick Reference**

### **Context Encryption**
```
1. Right-click context variable
2. Select "Encrypt"
3. Provide encryption password
4. Use encrypted value in jobs
```

### **Database Security**
```
SSL connections: Enable in connection properties
Encrypted passwords: Use context encryption
Parameterized queries: Prevent SQL injection
Access controls: Implement proper user permissions
```

## 📋 **Common Patterns**

### **ETL Pattern**
```
Source → tMap (Transform) → Target
Source → tFilterRow → tMap → Target
Source → tMap → tFileOutput (for validation)
```

### **Error Handling Pattern**
```
Source → tMap → Target
       ↓ (reject)
       tLogRow → tFileOutput (errors)
```

### **Lookup Pattern**
```
Main Input → tMap ← Lookup Input
           ↓
         Output
```

### **Incremental Load Pattern**
```
Source → tMap (filter by timestamp) → Target
Context: last_run_timestamp
Update context after successful run
```