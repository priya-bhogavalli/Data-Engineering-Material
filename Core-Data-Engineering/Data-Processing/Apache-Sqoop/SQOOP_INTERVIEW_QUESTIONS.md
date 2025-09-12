
### Q1: What is Apache Sqoop and what problems does it solve?
**Answer:**
Apache Sqoop is a tool designed for efficiently transferring bulk data between Apache Hadoop and structured datastores such as relational databases.

**Key Problems Solved:**
- **Data Integration**: Bridge between RDBMS and Hadoop ecosystem
- **Bulk Data Transfer**: Efficient large-scale data movement
- **ETL Operations**: Extract data from RDBMS, transform, and load into Hadoop
- **Bi-directional Transfer**: Both import (RDBMS → Hadoop) and export (Hadoop → RDBMS)
- **Automation**: Scheduled and incremental data transfers

**Core Features:**
- Parallel data transfer using MapReduce
- Support for major databases (MySQL, PostgreSQL, Oracle, SQL Server)
- Integration with Hive and HBase
- Incremental import capabilities
- Compression and file format options

### Q2: Explain Sqoop architecture and how it works
**Answer:**
**Sqoop Architecture:**

```
Client → Sqoop Client → JDBC Driver → Database
   ↓
MapReduce Jobs → HDFS/Hive/HBase
```

**Key Components:**

1. **Sqoop Client**
   - Command-line interface
   - Parses user commands
   - Generates MapReduce jobs

2. **JDBC Drivers**
   - Database-specific connectors
   - Handle database communication
   - Execute SQL queries

3. **MapReduce Framework**
   - Parallel data processing
   - Fault tolerance
   - Scalable data transfer

**How Sqoop Works:**

1. **Metadata Discovery**: Sqoop connects to database and retrieves table schema
2. **Job Generation**: Creates MapReduce job based on import/export requirements
3. **Data Splitting**: Divides data into chunks for parallel processing
4. **Parallel Transfer**: Multiple mappers transfer data simultaneously
5. **Data Writing**: Writes data to HDFS, Hive, or HBase

### Q3: What are the differences between Sqoop 1 and Sqoop 2?
**Answer:**
**Sqoop 1 vs Sqoop 2:**

| Feature | Sqoop 1 | Sqoop 2 |
|---------|---------|---------|
| **Architecture** | Client-only | Client-Server |
| **Security** | Limited | Enhanced security model |
| **Connectors** | Built-in | Pluggable connectors |
| **Web UI** | No | Yes |
| **REST API** | No | Yes |
| **Job Management** | Command-line only | Web-based management |
| **Metadata** | No central repository | Centralized metadata |
| **Multi-tenancy** | Limited | Better support |

**Sqoop 2 Advantages:**
- Centralized server for better management
- Web-based interface for non-technical users
- Better security and authentication
- Pluggable connector architecture
- REST API for integration

**Current Status:**
- Sqoop 1 is more mature and widely used
- Sqoop 2 development has been slower
- Most production environments use Sqoop 1

---

## 📥 Import Operations

### Q4: Explain different types of Sqoop import operations
**Answer:**
**Sqoop Import Types:**

**1. Full Table Import:**
```bash
# Import entire table
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers
```

**2. Query-based Import:**
```bash
# Import with custom query
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --query 'SELECT * FROM customers WHERE age > 25 AND $CONDITIONS' \
  --target-dir /user/data/adult_customers \
  --split-by customer_id
```

**3. Column Subset Import:**
```bash
# Import specific columns
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --columns "customer_id,first_name,last_name,email" \
  --target-dir /user/data/customer_subset
```

**4. Conditional Import:**
```bash
# Import with WHERE clause
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table orders \
  --where "order_date >= '2023-01-01'" \
  --target-dir /user/data/recent_orders
```

### Q5: How do you handle data types and null values in Sqoop imports?
**Answer:**
**Data Type Handling:**

**1. Automatic Type Mapping:**
```bash
# Sqoop automatically maps database types to Hadoop types
# MySQL INT → Hadoop IntWritable
# MySQL VARCHAR → Hadoop Text
# MySQL DECIMAL → Hadoop DoubleWritable
```

**2. Custom Type Mapping:**
```bash
# Override default mappings
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table products \
  --map-column-java product_price=String,created_date=String \
  --target-dir /user/data/products
```

**Null Value Handling:**

**1. Default Null Handling:**
```bash
# Default: null values become "null" string
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers
```

**2. Custom Null Value Replacement:**
```bash
# Replace nulls with custom values
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --null-string '\\N' \
  --null-non-string -1 \
  --target-dir /user/data/customers
```

**3. Handling Different Data Types:**
```bash
# Comprehensive null handling
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table orders \
  --null-string 'NULL' \
  --null-non-string 0 \
  --fields-terminated-by ',' \
  --lines-terminated-by '\n' \
  --target-dir /user/data/orders
```

### Q6: Explain Sqoop's parallelism and split-by parameter
**Answer:**
**Sqoop Parallelism:**

**1. Default Parallelism:**
```bash
# Default: 4 mappers
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers
# Creates 4 part files: part-m-00000, part-m-00001, part-m-00002, part-m-00003
```

**2. Custom Parallelism:**
```bash
# Specify number of mappers
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --num-mappers 8 \
  --target-dir /user/data/customers
```

**Split-by Parameter:**

**1. Automatic Split-by:**
```bash
# Sqoop automatically uses primary key for splitting
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers
# Uses primary key (customer_id) for splitting
```

**2. Custom Split-by:**
```bash
# Specify split column
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table orders \
  --split-by order_date \
  --target-dir /user/data/orders
```

**3. Single Mapper (No Split):**
```bash
# Use single mapper when split-by is not suitable
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table lookup_table \
  --num-mappers 1 \
  --target-dir /user/data/lookup
```

**Split-by Requirements:**
- Column should be indexed for performance
- Column should have good data distribution
- Numeric or date columns work best
- Avoid columns with many duplicate values

---

## 📤 Export Operations

### Q7: How do you export data from Hadoop to relational databases using Sqoop?
**Answer:**
**Sqoop Export Operations:**

**1. Basic Export:**
```bash
# Export HDFS data to database table
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers_export \
  --export-dir /user/data/processed_customers
```

**2. Export with Field Mapping:**
```bash
# Specify field delimiters and formatting
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table sales_summary \
  --export-dir /user/data/sales_summary \
  --fields-terminated-by ',' \
  --lines-terminated-by '\n'
```

**3. Export with Column Mapping:**
```bash
# Map specific columns
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customer_updates \
  --export-dir /user/data/customer_changes \
  --columns "customer_id,email,phone,last_updated"
```

**4. Update Export:**
```bash
# Update existing records
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --export-dir /user/data/customer_updates \
  --update-key customer_id \
  --update-mode allowinsert
```

### Q8: What are the different export modes in Sqoop?
**Answer:**
**Sqoop Export Modes:**

**1. Insert Mode (Default):**
```bash
# Insert new records only
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table new_customers \
  --export-dir /user/data/new_customers
# Fails if duplicate keys exist
```

**2. Update Mode:**
```bash
# Update existing records only
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --export-dir /user/data/customer_updates \
  --update-key customer_id \
  --update-mode updateonly
```

**3. Upsert Mode (Update + Insert):**
```bash
# Update existing, insert new records
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --export-dir /user/data/customer_changes \
  --update-key customer_id \
  --update-mode allowinsert
```

**4. Staging Table Export:**
```bash
# Use staging table for safe exports
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --staging-table customers_staging \
  --export-dir /user/data/customers \
  --clear-staging-table
```

**Export Mode Comparison:**
| Mode | Use Case | Behavior on Duplicates |
|------|----------|----------------------|
| Insert | New data only | Fails |
| Update | Modify existing | Ignores new records |
| Upsert | Mixed operations | Updates existing, inserts new |
| Staging | Safe bulk operations | Uses intermediate table |

---

## 🔄 Incremental Imports

### Q9: Explain incremental import strategies in Sqoop
**Answer:**
**Incremental Import Types:**

**1. Append Mode (for growing tables):**
```bash
# Initial import
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table orders \
  --target-dir /user/data/orders \
  --check-column order_id \
  --incremental append \
  --last-value 0

# Subsequent incremental import
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table orders \
  --target-dir /user/data/orders \
  --check-column order_id \
  --incremental append \
  --last-value 1000
```

**2. Last-Modified Mode (for updated records):**
```bash
# Import based on timestamp
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers \
  --check-column last_updated \
  --incremental lastmodified \
  --last-value '2023-12-01 00:00:00'
```

**3. Automated Incremental Import:**
```bash
# Create saved job for incremental imports
sqoop job --create incremental_orders -- import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table orders \
  --target-dir /user/data/orders \
  --check-column order_id \
  --incremental append \
  --last-value 0

# Execute saved job
sqoop job --exec incremental_orders

# List and show job details
sqoop job --list
sqoop job --show incremental_orders
```

### Q10: How do you handle incremental imports with merge operations?
**Answer:**
**Merge Operations for Incremental Data:**

**1. Merge Tool Usage:**
```bash
# Step 1: Initial full import
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers_full

# Step 2: Incremental import to separate directory
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers_incremental \
  --where "last_updated > '2023-12-01'"

# Step 3: Merge datasets
sqoop merge \
  --new-data /user/data/customers_incremental \
  --onto /user/data/customers_full \
  --target-dir /user/data/customers_merged \
  --jar-file /path/to/customers.jar \
  --class-name customers \
  --merge-key customer_id
```

**2. Hive-based Merge Strategy:**
```bash
# Import incremental data to Hive
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --hive-import \
  --hive-table customers_staging \
  --where "last_updated > '2023-12-01'"

# Use Hive to merge data
hive -e "
INSERT OVERWRITE TABLE customers
SELECT 
  COALESCE(s.customer_id, c.customer_id) as customer_id,
  COALESCE(s.name, c.name) as name,
  COALESCE(s.email, c.email) as email,
  COALESCE(s.last_updated, c.last_updated) as last_updated
FROM customers c
FULL OUTER JOIN customers_staging s
ON c.customer_id = s.customer_id
"
```

**3. Custom Merge Logic:**
```bash
# Export merged data back to database
sqoop export \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers_merged \
  --export-dir /user/data/customers_final \
  --update-key customer_id \
  --update-mode allowinsert
```

---

## ⚡ Performance Optimization

### Q11: What are the key performance optimization techniques for Sqoop?
**Answer:**
**Sqoop Performance Optimization:**

**1. Optimal Number of Mappers:**
```bash
# Calculate optimal mappers based on data size
# Rule of thumb: 1 mapper per 64-128MB of data
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table large_table \
  --num-mappers 16 \
  --target-dir /user/data/large_table
```

**2. Efficient Split-by Column:**
```bash
# Use indexed, well-distributed column
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table orders \
  --split-by order_date \  # Indexed date column
  --boundary-query "SELECT MIN(order_date), MAX(order_date) FROM orders" \
  --target-dir /user/data/orders
```

**3. Database Connection Optimization:**
```bash
# Optimize fetch size and connection parameters
sqoop import \
  --connect "jdbc:mysql://localhost/retail_db?useSSL=false&useCursorFetch=true" \
  --username root \
  --password password \
  --table customers \
  --fetch-size 1000 \
  --target-dir /user/data/customers
```

**4. Compression:**
```bash
# Enable compression to reduce I/O
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table large_table \
  --compress \
  --compression-codec org.apache.hadoop.io.compress.SnappyCodec \
  --target-dir /user/data/large_table_compressed
```

**5. Direct Mode (MySQL/PostgreSQL):**
```bash
# Use database-specific fast import tools
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --direct \
  --target-dir /user/data/customers_direct
```

### Q12: How do you handle large table imports efficiently?
**Answer:**
**Large Table Import Strategies:**

**1. Partitioned Import:**
```bash
# Import by date partitions
for date in 2023-01-01 2023-02-01 2023-03-01; do
  sqoop import \
    --connect jdbc:mysql://localhost/retail_db \
    --username root \
    --password password \
    --table transactions \
    --where "transaction_date >= '$date' AND transaction_date < DATE_ADD('$date', INTERVAL 1 MONTH)" \
    --target-dir /user/data/transactions/$date \
    --num-mappers 8
done
```

**2. Column Subset Strategy:**
```bash
# Import only required columns
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table large_table \
  --columns "id,name,status,created_date" \
  --where "status = 'ACTIVE'" \
  --target-dir /user/data/active_records
```

**3. Parallel Processing:**
```bash
# Increase mappers for large tables
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table huge_table \
  --num-mappers 32 \
  --split-by id \
  --target-dir /user/data/huge_table
```

**4. Memory Optimization:**
```bash
# Configure mapper memory
export HADOOP_OPTS="-Xmx2048m"
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table large_table \
  -D mapreduce.map.memory.mb=2048 \
  -D mapreduce.map.java.opts=-Xmx1638m \
  --target-dir /user/data/large_table
```

**5. Database Optimization:**
```sql
-- Optimize database for Sqoop imports
-- Add index on split-by column
CREATE INDEX idx_split_column ON large_table(split_column);

-- Optimize MySQL for bulk reads
SET SESSION tx_isolation='READ-UNCOMMITTED';
SET SESSION query_cache_type=OFF;
```

---

## 🔗 Integration & Formats

### Q13: How does Sqoop integrate with Hive and HBase?
**Answer:**
**Hive Integration:**

**1. Direct Hive Import:**
```bash
# Import directly to Hive table
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --hive-import \
  --hive-table retail.customers \
  --create-hive-table
```

**2. Hive Partitioned Import:**
```bash
# Import to partitioned Hive table
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table orders \
  --hive-import \
  --hive-table retail.orders \
  --hive-partition-key order_date \
  --hive-partition-value '2023-12-01'
```

**3. Custom Hive Database:**
```bash
# Import to specific Hive database
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table products \
  --hive-import \
  --hive-database warehouse \
  --hive-table products \
  --hive-overwrite
```

**HBase Integration:**

**1. Direct HBase Import:**
```bash
# Import to HBase table
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --hbase-table customers_hbase \
  --column-family cf \
  --hbase-row-key customer_id
```

**2. HBase with Column Mapping:**
```bash
# Map specific columns to HBase
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --columns "customer_id,first_name,last_name,email" \
  --hbase-table customers \
  --column-family personal \
  --hbase-row-key customer_id
```

### Q14: What file formats does Sqoop support and how do you use them?
**Answer:**
**Sqoop File Format Support:**

**1. Text Format (Default):**
```bash
# Default delimited text format
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --fields-terminated-by ',' \
  --lines-terminated-by '\n' \
  --target-dir /user/data/customers_text
```

**2. Sequence File:**
```bash
# Binary sequence file format
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --as-sequencefile \
  --target-dir /user/data/customers_seq
```

**3. Avro Format:**
```bash
# Avro format with schema evolution support
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --as-avrodatafile \
  --target-dir /user/data/customers_avro
```

**4. Parquet Format:**
```bash
# Columnar Parquet format
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --as-parquetfile \
  --target-dir /user/data/customers_parquet
```

**5. Custom Delimiters:**
```bash
# Custom field and record delimiters
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --fields-terminated-by '\001' \
  --lines-terminated-by '\002' \
  --escaped-by '\\' \
  --enclosed-by '"' \
  --target-dir /user/data/customers_custom
```

**Format Comparison:**
| Format | Use Case | Compression | Schema Evolution |
|--------|----------|-------------|------------------|
| Text | Human readable, simple processing | Good | No |
| SequenceFile | Hadoop native, splittable | Good | No |
| Avro | Schema evolution, cross-language | Good | Yes |
| Parquet | Analytics, columnar queries | Excellent | Limited |

---

## 🔒 Security & Authentication

### Q15: How do you implement security in Sqoop operations?
**Answer:**
**Sqoop Security Implementation:**

**1. Password Security:**
```bash
# Method 1: Password file
echo "mypassword" > /user/sqoop/.password
hdfs dfs -chmod 400 /user/sqoop/.password

sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password-file /user/sqoop/.password \
  --table customers \
  --target-dir /user/data/customers

# Method 2: Environment variable
export SQOOP_PASSWORD="mypassword"
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password ${SQOOP_PASSWORD} \
  --table customers \
  --target-dir /user/data/customers
```

**2. Kerberos Authentication:**
```bash
# Kerberos-enabled Sqoop
kinit -kt /path/to/keytab sqoop_user@REALM.COM

sqoop import \
  --connect "jdbc:mysql://localhost/retail_db?useSSL=true" \
  --username sqoop_user \
  --password-file /user/sqoop/.password \
  --table customers \
  --target-dir /user/data/customers
```

**3. SSL/TLS Connections:**
```bash
# SSL-enabled database connection
sqoop import \
  --connect "jdbc:mysql://localhost:3306/retail_db?useSSL=true&requireSSL=true&verifyServerCertificate=true" \
  --username root \
  --password-file /user/sqoop/.password \
  --table customers \
  --target-dir /user/data/customers
```

**4. HDFS Permissions:**
```bash
# Set appropriate HDFS permissions
hdfs dfs -mkdir /user/data/secure_data
hdfs dfs -chmod 750 /user/data/secure_data
hdfs dfs -chown sqoop_user:sqoop_group /user/data/secure_data

sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password-file /user/sqoop/.password \
  --table sensitive_data \
  --target-dir /user/data/secure_data/sensitive_data
```

**5. Data Encryption:**
```bash
# Import with encryption
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password-file /user/sqoop/.password \
  --table customers \
  --target-dir /user/data/customers_encrypted \
  --compress \
  --compression-codec org.apache.hadoop.io.compress.SnappyCodec
```

### Q16: How do you handle sensitive data and PII in Sqoop?
**Answer:**
**Sensitive Data Handling:**

**1. Column Filtering:**
```bash
# Exclude sensitive columns
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password-file /user/sqoop/.password \
  --table customers \
  --columns "customer_id,first_name,last_name,city,state" \
  --target-dir /user/data/customers_filtered
# Excludes SSN, credit_card, etc.
```

**2. Data Masking with Custom Query:**
```bash
# Mask sensitive data during import
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password-file /user/sqoop/.password \
  --query "SELECT 
    customer_id,
    first_name,
    last_name,
    CONCAT('***-**-', RIGHT(ssn, 4)) as masked_ssn,
    CONCAT('****-****-****-', RIGHT(credit_card, 4)) as masked_cc,
    email
  FROM customers WHERE \$CONDITIONS" \
  --split-by customer_id \
  --target-dir /user/data/customers_masked
```

**3. Separate Sensitive Data:**
```bash
# Import non-sensitive data
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password-file /user/sqoop/.password \
  --table customers \
  --columns "customer_id,first_name,last_name,email,city,state" \
  --target-dir /user/data/customers_public

# Import sensitive data to secure location
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password-file /user/sqoop/.password \
  --table customers \
  --columns "customer_id,ssn,credit_card,phone" \
  --target-dir /user/secure/customers_pii
```

**4. Encryption at Rest:**
```bash
# Use HDFS encryption zones
hdfs crypto -createZone -keyName customer_key -path /user/secure/customers

sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password-file /user/sqoop/.password \
  --table customers \
  --target-dir /user/secure/customers/data
```

---

## 🔧 Troubleshooting

### Q17: What are common Sqoop errors and how do you resolve them?
**Answer:**
**Common Sqoop Errors and Solutions:**

**1. Connection Errors:**
```bash
# Error: Could not establish connection to database
# Solution: Check JDBC URL, credentials, and network connectivity

# Verify connection
sqoop list-databases \
  --connect jdbc:mysql://localhost:3306/ \
  --username root \
  --password password

# Common fixes:
# - Correct JDBC URL format
# - Verify database server is running
# - Check firewall settings
# - Ensure JDBC driver is in classpath
```

**2. Split-by Column Issues:**
```bash
# Error: Split by column not found or not suitable
# Solution: Use appropriate split-by column

# Check table structure
sqoop eval \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --query "DESCRIBE customers"

# Use indexed column for split-by
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --split-by customer_id \  # Use primary key
  --target-dir /user/data/customers
```

**3. Memory Issues:**
```bash
# Error: OutOfMemoryError
# Solution: Optimize memory settings

# Increase mapper memory
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table large_table \
  -D mapreduce.map.memory.mb=4096 \
  -D mapreduce.map.java.opts=-Xmx3276m \
  --num-mappers 4 \
  --target-dir /user/data/large_table
```

**4. Data Type Conversion Errors:**
```bash
# Error: Cannot convert database type to Hadoop type
# Solution: Use custom type mapping

sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table products \
  --map-column-java price=String,created_date=String \
  --target-dir /user/data/products
```

**5. Permission Errors:**
```bash
# Error: Permission denied writing to HDFS
# Solution: Check HDFS permissions

# Create directory with proper permissions
hdfs dfs -mkdir -p /user/data/customers
hdfs dfs -chown sqoop_user:hadoop /user/data/customers
hdfs dfs -chmod 755 /user/data/customers
```

### Q18: How do you monitor and debug Sqoop jobs?
**Answer:**
**Sqoop Monitoring and Debugging:**

**1. Verbose Logging:**
```bash
# Enable verbose output
sqoop import \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --table customers \
  --target-dir /user/data/customers \
  --verbose
```

**2. Job Tracking:**
```bash
# Monitor MapReduce job progress
# Check Hadoop job tracker UI: http://namenode:8088
# View job logs and counters

# Command line job monitoring
yarn application -list
yarn logs -applicationId application_id
```

**3. Data Validation:**
```bash
# Validate import results
# Check record count
sqoop eval \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --query "SELECT COUNT(*) FROM customers"

# Check HDFS file count
hdfs dfs -cat /user/data/customers/part-m-* | wc -l

# Compare checksums
sqoop eval \
  --connect jdbc:mysql://localhost/retail_db \
  --username root \
  --password password \
  --query "SELECT SUM(CRC32(CONCAT_WS('|', customer_id, first_name, last_name))) FROM customers"
```

**4. Performance Monitoring:**
```bash
# Monitor resource usage
# Check mapper execution time
# Analyze data distribution across mappers
# Monitor database connection pool

# Custom counters in logs
grep "Records" /path/to/sqoop/logs/sqoop.log
grep "Bytes" /path/to/sqoop/logs/sqoop.log
```

**5. Error Analysis:**
```bash
# Analyze common error patterns
# Check database locks and timeouts
# Monitor network connectivity
# Validate data consistency

# Debug specific mapper failures
yarn logs -applicationId application_id -containerId container_id
```

---

## 🌟 Real-world Scenarios

### Q19: Design a complete ETL pipeline using Sqoop for a retail analytics system
**Answer:**
**Retail Analytics ETL Pipeline:**

**1. Data Sources and Architecture:**
```
MySQL (OLTP) → Sqoop → HDFS → Hive → Analytics/BI Tools
```

**2. Initial Full Load:**
```bash
#!/bin/bash
# full_load.sh - Initial data load script

# Database connection parameters
DB_HOST="mysql-server"
DB_NAME="retail_db"
DB_USER="sqoop_user"
PASSWORD_FILE="/user/sqoop/.password"
HDFS_BASE="/user/data/retail"

# Create HDFS directories
hdfs dfs -mkdir -p $HDFS_BASE/{customers,products,orders,order_items}

# Import customers table
sqoop import \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --table customers \
  --target-dir $HDFS_BASE/customers \
  --split-by customer_id \
  --num-mappers 8 \
  --compress \
  --compression-codec org.apache.hadoop.io.compress.SnappyCodec

# Import products table
sqoop import \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --table products \
  --target-dir $HDFS_BASE/products \
  --split-by product_id \
  --num-mappers 4

# Import orders table with partitioning
sqoop import \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --table orders \
  --target-dir $HDFS_BASE/orders \
  --split-by order_id \
  --num-mappers 12

# Import order_items table
sqoop import \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --table order_items \
  --target-dir $HDFS_BASE/order_items \
  --split-by order_item_id \
  --num-mappers 16
```

**3. Incremental Load Setup:**
```bash
#!/bin/bash
# incremental_setup.sh - Setup incremental jobs

# Create incremental job for orders
sqoop job --create incremental_orders -- import \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --table orders \
  --target-dir $HDFS_BASE/orders_incremental \
  --check-column order_date \
  --incremental lastmodified \
  --last-value '1970-01-01 00:00:00'

# Create incremental job for customers
sqoop job --create incremental_customers -- import \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --table customers \
  --target-dir $HDFS_BASE/customers_incremental \
  --check-column last_updated \
  --incremental lastmodified \
  --last-value '1970-01-01 00:00:00'
```

**4. Daily ETL Process:**
```bash
#!/bin/bash
# daily_etl.sh - Daily ETL execution

DATE=$(date +%Y-%m-%d)
LOG_FILE="/var/log/sqoop/daily_etl_$DATE.log"

echo "Starting daily ETL process at $(date)" >> $LOG_FILE

# Execute incremental imports
sqoop job --exec incremental_orders >> $LOG_FILE 2>&1
if [ $? -eq 0 ]; then
    echo "Orders incremental import completed successfully" >> $LOG_FILE
else
    echo "Orders incremental import failed" >> $LOG_FILE
    exit 1
fi

sqoop job --exec incremental_customers >> $LOG_FILE 2>&1
if [ $? -eq 0 ]; then
    echo "Customers incremental import completed successfully" >> $LOG_FILE
else
    echo "Customers incremental import failed" >> $LOG_FILE
    exit 1
fi

# Merge incremental data with base data
echo "Starting data merge process" >> $LOG_FILE

# Process orders data
hdfs dfs -mkdir -p $HDFS_BASE/orders_merged_$DATE

sqoop merge \
  --new-data $HDFS_BASE/orders_incremental \
  --onto $HDFS_BASE/orders \
  --target-dir $HDFS_BASE/orders_merged_$DATE \
  --jar-file /tmp/orders.jar \
  --class-name orders \
  --merge-key order_id

# Replace old data with merged data
hdfs dfs -rm -r $HDFS_BASE/orders_old
hdfs dfs -mv $HDFS_BASE/orders $HDFS_BASE/orders_old
hdfs dfs -mv $HDFS_BASE/orders_merged_$DATE $HDFS_BASE/orders

echo "Daily ETL process completed at $(date)" >> $LOG_FILE
```

**5. Data Quality Validation:**
```bash
#!/bin/bash
# data_validation.sh - Validate imported data

# Count validation
DB_COUNT=$(sqoop eval \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --query "SELECT COUNT(*) FROM orders WHERE order_date >= CURDATE()" | tail -1)

HDFS_COUNT=$(hdfs dfs -cat $HDFS_BASE/orders_incremental/part-* | wc -l)

if [ "$DB_COUNT" -eq "$HDFS_COUNT" ]; then
    echo "Data count validation passed: $DB_COUNT records"
else
    echo "Data count validation failed: DB=$DB_COUNT, HDFS=$HDFS_COUNT"
    exit 1
fi

# Data integrity checks
sqoop eval \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --query "SELECT 'DB_CHECKSUM', SUM(CRC32(CONCAT(order_id, customer_id, order_total))) FROM orders WHERE order_date >= CURDATE()"

echo "Data validation completed successfully"
```

### Q20: Implement a real-time data synchronization solution using Sqoop
**Answer:**
**Real-time Data Synchronization Solution:**

**1. Change Data Capture (CDC) Setup:**
```bash
#!/bin/bash
# cdc_setup.sh - Setup CDC for real-time sync

# Create CDC tracking table in source database
sqoop eval \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --query "CREATE TABLE IF NOT EXISTS cdc_tracking (
    table_name VARCHAR(50),
    last_sync_timestamp TIMESTAMP,
    last_sync_id BIGINT,
    PRIMARY KEY (table_name)
  )"

# Initialize tracking records
sqoop eval \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --query "INSERT INTO cdc_tracking VALUES 
    ('customers', '1970-01-01 00:00:00', 0),
    ('orders', '1970-01-01 00:00:00', 0),
    ('products', '1970-01-01 00:00:00', 0)
  ON DUPLICATE KEY UPDATE table_name=table_name"
```

**2. Micro-batch Processing:**
```bash
#!/bin/bash
# micro_batch_sync.sh - Process micro-batches every 5 minutes

BATCH_SIZE=1000
SYNC_INTERVAL=300  # 5 minutes

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "Starting micro-batch sync at $TIMESTAMP"
    
    # Get last sync timestamp for customers
    LAST_SYNC=$(sqoop eval \
      --connect jdbc:mysql://$DB_HOST/$DB_NAME \
      --username $DB_USER \
      --password-file $PASSWORD_FILE \
      --query "SELECT last_sync_timestamp FROM cdc_tracking WHERE table_name='customers'" | tail -1)
    
    # Import changed customers
    sqoop import \
      --connect jdbc:mysql://$DB_HOST/$DB_NAME \
      --username $DB_USER \
      --password-file $PASSWORD_FILE \
      --query "SELECT * FROM customers 
               WHERE last_updated > '$LAST_SYNC' 
               AND \$CONDITIONS 
               ORDER BY last_updated 
               LIMIT $BATCH_SIZE" \
      --split-by customer_id \
      --target-dir /user/data/cdc/customers/$(date +%Y%m%d_%H%M%S) \
      --num-mappers 4
    
    if [ $? -eq 0 ]; then
        # Update tracking table
        sqoop eval \
          --connect jdbc:mysql://$DB_HOST/$DB_NAME \
          --username $DB_USER \
          --password-file $PASSWORD_FILE \
          --query "UPDATE cdc_tracking 
                   SET last_sync_timestamp = '$TIMESTAMP' 
                   WHERE table_name = 'customers'"
    fi
    
    sleep $SYNC_INTERVAL
done
```

**3. Stream Processing Integration:**
```bash
#!/bin/bash
# stream_processor.sh - Process CDC data streams

# Monitor HDFS directory for new CDC files
inotifywait -m -r -e create /user/data/cdc/ --format '%w%f' | while read file; do
    if [[ $file == *.txt ]]; then
        echo "Processing new CDC file: $file"
        
        # Process with Spark Streaming or Kafka
        spark-submit \
          --class com.example.CDCProcessor \
          --master yarn \
          --deploy-mode cluster \
          cdc-processor.jar $file
        
        # Move processed file to archive
        hdfs dfs -mv $file /user/data/cdc/archive/
    fi
done
```

**4. Conflict Resolution:**
```bash
#!/bin/bash
# conflict_resolution.sh - Handle data conflicts

# Implement last-writer-wins strategy
sqoop export \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --table customers_staging \
  --export-dir /user/data/cdc/customers/processed \
  --update-key customer_id \
  --update-mode allowinsert

# Resolve conflicts using business rules
sqoop eval \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --query "
    UPDATE customers c
    JOIN customers_staging s ON c.customer_id = s.customer_id
    SET c.first_name = s.first_name,
        c.last_name = s.last_name,
        c.email = s.email,
        c.last_updated = GREATEST(c.last_updated, s.last_updated)
    WHERE s.last_updated > c.last_updated
  "
```

**5. Monitoring and Alerting:**
```bash
#!/bin/bash
# monitoring.sh - Monitor sync health

# Check sync lag
CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
LAG_THRESHOLD=600  # 10 minutes

LAG_SECONDS=$(sqoop eval \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --query "SELECT TIMESTAMPDIFF(SECOND, last_sync_timestamp, '$CURRENT_TIME') 
           FROM cdc_tracking WHERE table_name='customers'" | tail -1)

if [ $LAG_SECONDS -gt $LAG_THRESHOLD ]; then
    echo "ALERT: Sync lag is $LAG_SECONDS seconds for customers table"
    # Send alert notification
    curl -X POST -H 'Content-type: application/json' \
      --data '{"text":"Sqoop sync lag alert: '$LAG_SECONDS' seconds"}' \
      $SLACK_WEBHOOK_URL
fi

# Check data consistency
DB_CHECKSUM=$(sqoop eval \
  --connect jdbc:mysql://$DB_HOST/$DB_NAME \
  --username $DB_USER \
  --password-file $PASSWORD_FILE \
  --query "SELECT SUM(CRC32(CONCAT(customer_id, first_name, last_name))) FROM customers" | tail -1)

echo "Database checksum: $DB_CHECKSUM"
echo "Sync monitoring completed at $(date)"
```

---

## 📚 Additional Resources

### Best Practices Summary
1. **Performance**: Use optimal number of mappers and appropriate split-by columns
2. **Security**: Implement proper authentication and data protection
3. **Monitoring**: Set up comprehensive logging and alerting
4. **Data Quality**: Validate data integrity and implement error handling
5. **Automation**: Create reusable jobs and automated workflows

### Recommended Reading
- Apache Sqoop Official Documentation
- "Hadoop: The Definitive Guide" by Tom White
- Database-specific JDBC documentation

### Hands-on Practice
- Cloudera Quickstart VM
- Hortonworks Sandbox
- AWS EMR with Sqoop
- Local Hadoop cluster setup

---

*This comprehensive guide covers essential Apache Sqoop concepts and interview questions for data engineering roles. Practice with real databases and large datasets to master Sqoop operations.*