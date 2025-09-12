# Microsoft SQL Server Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Performance Optimization Questions (16-30)](#performance-optimization-questions-16-30)
3. [Data Modeling & Design Questions (31-45)](#data-modeling--design-questions-31-45)
4. [Advanced Features Questions (46-60)](#advanced-features-questions-46-60)
5. [Integration & ETL Questions (61-75)](#integration--etl-questions-61-75)
6. [Security & Administration (76-90)](#security--administration-76-90)
7. [Architecture & Scalability (91-100)](#architecture--scalability-91-100)

---

## 🎯 **Introduction**

Microsoft SQL Server is a comprehensive relational database management system that plays a crucial role in enterprise data engineering. This guide covers essential SQL Server concepts, from basic database operations to advanced data warehousing and integration scenarios.

**Why SQL Server is Critical for Data Engineers:**
- **Enterprise Integration**: Seamless integration with Microsoft ecosystem
- **Performance**: Advanced query optimization and in-memory technologies
- **Scalability**: Support for large-scale data warehousing and analytics
- **Security**: Enterprise-grade security features and compliance
- **BI Integration**: Native integration with Power BI and Analysis Services

---

## Core Concepts Questions (1-15)

### 1. What are the key differences between SQL Server editions and which would you choose for data engineering?
**Answer**: 
Understanding SQL Server editions is crucial for architecture decisions and cost optimization.

**Key Editions:**
- **Express**: Free, limited to 10GB, single CPU, 1GB RAM - suitable for development
- **Standard**: Full features except advanced analytics, limited to 128GB RAM
- **Enterprise**: All features including advanced analytics, unlimited resources
- **Developer**: Full Enterprise features for development/testing only

```sql
-- Check current edition
SELECT SERVERPROPERTY('Edition') AS Edition,
       SERVERPROPERTY('ProductLevel') AS ProductLevel,
       SERVERPROPERTY('ProductVersion') AS ProductVersion;

-- For data engineering, typically need Standard or Enterprise for:
-- - Integration Services (SSIS)
-- - Analysis Services (SSAS) 
-- - Reporting Services (SSRS)
-- - Advanced indexing features
-- - Partitioning capabilities
```

### 2. Explain SQL Server's storage architecture and how it impacts data engineering performance.
**Answer**: SQL Server's storage architecture directly impacts ETL performance and data warehouse design.

**Storage Components:**
- **Database Files**: Primary (.mdf), Secondary (.ndf), Log (.ldf)
- **Pages**: 8KB storage units, fundamental I/O unit
- **Extents**: 8 contiguous pages (64KB)
- **File Groups**: Logical grouping of files for management

```sql
-- Create database with multiple file groups for performance
CREATE DATABASE DataWarehouse
ON 
( NAME = 'DW_Data',
  FILENAME = 'C:\Data\DW_Data.mdf',
  SIZE = 1GB,
  FILEGROWTH = 256MB ),
( NAME = 'DW_Index',
  FILENAME = 'C:\Index\DW_Index.ndf',
  SIZE = 512MB,
  FILEGROWTH = 128MB )
LOG ON
( NAME = 'DW_Log',
  FILENAME = 'C:\Log\DW_Log.ldf',
  SIZE = 256MB,
  FILEGROWTH = 64MB );

-- Separate data and indexes for better I/O performance
ALTER DATABASE DataWarehouse ADD FILEGROUP IndexFileGroup;
ALTER DATABASE DataWarehouse 
ADD FILE (NAME = 'IndexFile', FILENAME = 'C:\Index\IndexFile.ndf') 
TO FILEGROUP IndexFileGroup;
```

### 3. How do you implement and optimize table partitioning in SQL Server?
**Answer**: Partitioning is essential for managing large data warehouse tables and improving query performance.

```sql
-- Create partition function
CREATE PARTITION FUNCTION DateRangePartition (DATE)
AS RANGE RIGHT FOR VALUES 
('2023-01-01', '2023-04-01', '2023-07-01', '2023-10-01', '2024-01-01');

-- Create partition scheme
CREATE PARTITION SCHEME DateRangeScheme
AS PARTITION DateRangePartition
TO (FileGroup1, FileGroup2, FileGroup3, FileGroup4, FileGroup5);

-- Create partitioned table
CREATE TABLE SalesData (
    SaleID INT IDENTITY(1,1),
    SaleDate DATE NOT NULL,
    CustomerID INT,
    Amount DECIMAL(10,2),
    INDEX IX_SalesData_Date CLUSTERED (SaleDate)
) ON DateRangeScheme(SaleDate);

-- Partition elimination query
SELECT * FROM SalesData 
WHERE SaleDate >= '2023-06-01' AND SaleDate < '2023-09-01';

-- Check partition information
SELECT 
    p.partition_number,
    p.rows,
    rv.value AS boundary_value
FROM sys.partitions p
JOIN sys.partition_range_values rv ON p.partition_id = rv.boundary_id
WHERE p.object_id = OBJECT_ID('SalesData');
```

## Performance Optimization Questions (16-30)

### 4. How do you identify and resolve performance bottlenecks in SQL Server for data engineering workloads?
**Answer**: Systematic approach to performance tuning for ETL and analytical workloads.

```sql
-- 1. Identify expensive queries
SELECT TOP 10
    qs.total_elapsed_time / qs.execution_count AS avg_elapsed_time,
    qs.total_cpu_time / qs.execution_count AS avg_cpu_time,
    qs.execution_count,
    SUBSTRING(qt.text, qs.statement_start_offset/2+1,
        (CASE WHEN qs.statement_end_offset = -1
            THEN LEN(CONVERT(NVARCHAR(MAX), qt.text)) * 2
            ELSE qs.statement_end_offset END - qs.statement_start_offset)/2) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;

-- 2. Check for missing indexes
SELECT 
    migs.avg_total_user_cost * (migs.avg_user_impact / 100.0) * (migs.user_seeks + migs.user_scans) AS improvement_measure,
    'CREATE INDEX IX_' + OBJECT_NAME(mid.object_id) + '_' + ISNULL(mid.equality_columns,'') + 
    CASE WHEN mid.inequality_columns IS NOT NULL THEN '_' + mid.inequality_columns ELSE '' END +
    ' ON ' + SCHEMA_NAME(o.schema_id) + '.' + OBJECT_NAME(mid.object_id) +
    ' (' + ISNULL(mid.equality_columns,'') +
    CASE WHEN mid.inequality_columns IS NOT NULL THEN ',' + mid.inequality_columns ELSE '' END + ')' +
    ISNULL(' INCLUDE (' + mid.included_columns + ')', '') AS create_index_statement
FROM sys.dm_db_missing_index_groups mig
JOIN sys.dm_db_missing_index_group_stats migs ON migs.group_handle = mig.index_group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
JOIN sys.objects o ON mid.object_id = o.object_id
ORDER BY improvement_measure DESC;

-- 3. Monitor wait statistics
SELECT TOP 10
    wait_type,
    wait_time_ms,
    signal_wait_time_ms,
    wait_time_ms - signal_wait_time_ms AS resource_wait_time_ms,
    waiting_tasks_count,
    wait_time_ms / waiting_tasks_count AS avg_wait_time_ms
FROM sys.dm_os_wait_stats
WHERE waiting_tasks_count > 0
ORDER BY wait_time_ms DESC;
```

### 5. Explain columnstore indexes and when to use them in data engineering scenarios.
**Answer**: Columnstore indexes are crucial for analytical workloads and data warehousing.

```sql
-- Create clustered columnstore index for fact table
CREATE CLUSTERED COLUMNSTORE INDEX CCI_SalesData ON SalesData;

-- Create nonclustered columnstore for analytical queries on OLTP table
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCI_Orders_Analytics 
ON Orders (OrderDate, CustomerID, ProductID, Quantity, UnitPrice);

-- Partition-aligned columnstore for large tables
CREATE CLUSTERED COLUMNSTORE INDEX CCI_LargeFact 
ON LargeFactTable
ON DateRangeScheme(DateColumn);

-- Check columnstore segment information
SELECT 
    i.name AS index_name,
    p.partition_number,
    csg.row_group_id,
    csg.state_desc,
    csg.total_rows,
    csg.deleted_rows,
    csg.size_in_bytes
FROM sys.column_store_segments css
JOIN sys.partitions p ON css.partition_id = p.partition_id
JOIN sys.indexes i ON p.object_id = i.object_id AND p.index_id = i.index_id
JOIN sys.column_store_row_groups csg ON css.segment_id = csg.row_group_id
WHERE i.type IN (5, 6) -- Columnstore indexes
ORDER BY i.name, p.partition_number, csg.row_group_id;

-- Optimize columnstore with reorganize
ALTER INDEX CCI_SalesData ON SalesData REORGANIZE;
```

## Data Modeling & Design Questions (31-45)

### 6. How do you design a star schema in SQL Server for optimal performance?
**Answer**: Star schema design principles for SQL Server data warehouses.

```sql
-- Dimension table design
CREATE TABLE DimCustomer (
    CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID NVARCHAR(50) NOT NULL,
    CustomerName NVARCHAR(100),
    City NVARCHAR(50),
    State NVARCHAR(50),
    Country NVARCHAR(50),
    -- SCD Type 2 columns
    EffectiveDate DATE NOT NULL,
    ExpirationDate DATE,
    IsCurrent BIT DEFAULT 1,
    -- Create clustered index on surrogate key
    INDEX IX_DimCustomer_CustomerID NONCLUSTERED (CustomerID)
);

-- Fact table design with columnstore
CREATE TABLE FactSales (
    DateKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    ProductKey INT NOT NULL,
    SalesAmount DECIMAL(18,2),
    Quantity INT,
    UnitPrice DECIMAL(18,2),
    -- Foreign key constraints for referential integrity
    CONSTRAINT FK_FactSales_Date FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
    CONSTRAINT FK_FactSales_Customer FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    CONSTRAINT FK_FactSales_Product FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey)
);

-- Create columnstore index on fact table
CREATE CLUSTERED COLUMNSTORE INDEX CCI_FactSales ON FactSales;

-- Partitioning strategy for fact table
CREATE PARTITION FUNCTION PF_FactSales_Date (INT)
AS RANGE RIGHT FOR VALUES (20230101, 20230401, 20230701, 20231001);

CREATE PARTITION SCHEME PS_FactSales_Date
AS PARTITION PF_FactSales_Date ALL TO ([PRIMARY]);

-- Recreate fact table with partitioning
DROP TABLE FactSales;
CREATE TABLE FactSales (
    DateKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    ProductKey INT NOT NULL,
    SalesAmount DECIMAL(18,2),
    Quantity INT,
    UnitPrice DECIMAL(18,2)
) ON PS_FactSales_Date(DateKey);

CREATE CLUSTERED COLUMNSTORE INDEX CCI_FactSales ON FactSales
ON PS_FactSales_Date(DateKey);
```

### 7. How do you implement Slowly Changing Dimensions (SCD) in SQL Server?
**Answer**: SCD implementation patterns for maintaining historical data.

```sql
-- SCD Type 1 - Overwrite (no history)
MERGE DimCustomer AS target
USING (SELECT CustomerID, CustomerName, City, State FROM SourceCustomer) AS source
ON target.CustomerID = source.CustomerID
WHEN MATCHED THEN
    UPDATE SET 
        CustomerName = source.CustomerName,
        City = source.City,
        State = source.State
WHEN NOT MATCHED THEN
    INSERT (CustomerID, CustomerName, City, State, EffectiveDate, IsCurrent)
    VALUES (source.CustomerID, source.CustomerName, source.City, source.State, GETDATE(), 1);

-- SCD Type 2 - Add new record (maintain history)
WITH SourceData AS (
    SELECT CustomerID, CustomerName, City, State, Country
    FROM SourceCustomer
),
ChangedRecords AS (
    SELECT s.*, d.CustomerKey
    FROM SourceData s
    JOIN DimCustomer d ON s.CustomerID = d.CustomerID AND d.IsCurrent = 1
    WHERE s.CustomerName != d.CustomerName 
       OR s.City != d.City 
       OR s.State != d.State 
       OR s.Country != d.Country
)
-- Expire current records
UPDATE DimCustomer 
SET IsCurrent = 0, ExpirationDate = GETDATE()
WHERE CustomerKey IN (SELECT CustomerKey FROM ChangedRecords);

-- Insert new current records
INSERT INTO DimCustomer (CustomerID, CustomerName, City, State, Country, EffectiveDate, IsCurrent)
SELECT CustomerID, CustomerName, City, State, Country, GETDATE(), 1
FROM ChangedRecords;

-- SCD Type 3 - Add column for previous value
ALTER TABLE DimCustomer ADD PreviousCity NVARCHAR(50);

UPDATE DimCustomer 
SET PreviousCity = City,
    City = s.City
FROM DimCustomer d
JOIN SourceCustomer s ON d.CustomerID = s.CustomerID
WHERE d.City != s.City AND d.IsCurrent = 1;
```

## Advanced Features Questions (46-60)

### 8. How do you implement temporal tables for data auditing and historical analysis?
**Answer**: Temporal tables provide automatic history tracking for data engineering scenarios.

```sql
-- Create system-versioned temporal table
CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Department NVARCHAR(50),
    Salary DECIMAL(10,2),
    -- System-time columns
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN,
    ValidTo DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.EmployeeHistory));

-- Query current data
SELECT * FROM Employee;

-- Query historical data
SELECT * FROM Employee FOR SYSTEM_TIME ALL
WHERE EmployeeID = 1;

-- Query data as of specific time
SELECT * FROM Employee FOR SYSTEM_TIME AS OF '2023-06-01 12:00:00'
WHERE Department = 'Engineering';

-- Query data between time periods
SELECT * FROM Employee 
FOR SYSTEM_TIME BETWEEN '2023-01-01' AND '2023-12-31'
WHERE EmployeeID = 1;

-- Analyze salary changes over time
SELECT 
    EmployeeID,
    Name,
    Salary,
    ValidFrom,
    ValidTo,
    LAG(Salary) OVER (PARTITION BY EmployeeID ORDER BY ValidFrom) AS PreviousSalary
FROM Employee FOR SYSTEM_TIME ALL
WHERE EmployeeID = 1
ORDER BY ValidFrom;
```

### 9. How do you use SQL Server Integration Services (SSIS) for complex ETL processes?
**Answer**: SSIS design patterns for enterprise data integration.

```sql
-- Create SSIS catalog and project deployment
-- Enable CLR integration for SSIS
EXEC sp_configure 'clr enabled', 1;
RECONFIGURE;

-- Create SSIS catalog
CREATE DATABASE SSISDB;
-- Use SQL Server Management Studio to create SSIS catalog

-- Example: Incremental load pattern using SSIS variables and SQL
DECLARE @LastLoadDate DATETIME;
DECLARE @CurrentLoadDate DATETIME = GETDATE();

-- Get last successful load date
SELECT @LastLoadDate = ISNULL(MAX(LoadDate), '1900-01-01')
FROM ETL_LoadLog 
WHERE TableName = 'FactSales' AND Status = 'Success';

-- Incremental extraction query
SELECT 
    SaleID,
    SaleDate,
    CustomerID,
    ProductID,
    Amount
FROM SourceSales
WHERE ModifiedDate > @LastLoadDate 
  AND ModifiedDate <= @CurrentLoadDate;

-- Log successful load
INSERT INTO ETL_LoadLog (TableName, LoadDate, RecordsProcessed, Status)
VALUES ('FactSales', @CurrentLoadDate, @@ROWCOUNT, 'Success');

-- Error handling in SSIS package
BEGIN TRY
    -- ETL operations
    EXEC LoadFactSales;
    
    -- Update load log on success
    UPDATE ETL_LoadLog 
    SET Status = 'Success', EndTime = GETDATE()
    WHERE LoadID = @LoadID;
    
END TRY
BEGIN CATCH
    -- Log error details
    INSERT INTO ETL_ErrorLog (LoadID, ErrorMessage, ErrorTime)
    VALUES (@LoadID, ERROR_MESSAGE(), GETDATE());
    
    -- Update load log on failure
    UPDATE ETL_LoadLog 
    SET Status = 'Failed', EndTime = GETDATE()
    WHERE LoadID = @LoadID;
    
    -- Re-throw error
    THROW;
END CATCH;
```

### 10. How do you implement data compression and archival strategies?
**Answer**: Data compression and archival for managing large data volumes.

```sql
-- Row compression for OLTP tables
ALTER TABLE Orders REBUILD WITH (DATA_COMPRESSION = ROW);

-- Page compression for data warehouse tables
ALTER TABLE FactSales REBUILD WITH (DATA_COMPRESSION = PAGE);

-- Columnstore compression (automatic with columnstore indexes)
CREATE CLUSTERED COLUMNSTORE INDEX CCI_FactSales ON FactSales;

-- Partition-level compression
ALTER TABLE FactSales REBUILD PARTITION = 1 WITH (DATA_COMPRESSION = PAGE);
ALTER TABLE FactSales REBUILD PARTITION = 2 WITH (DATA_COMPRESSION = ROW);

-- Check compression savings
SELECT 
    OBJECT_NAME(object_id) AS TableName,
    partition_number,
    data_compression_desc,
    row_count,
    size_in_bytes / 1024 / 1024 AS SizeMB,
    size_in_bytes / row_count AS AvgBytesPerRow
FROM sys.dm_db_partition_stats ps
JOIN sys.partitions p ON ps.partition_id = p.partition_id
WHERE OBJECT_NAME(object_id) = 'FactSales';

-- Archival strategy with table partitioning
-- Move old partitions to archive filegroup
ALTER PARTITION SCHEME PS_FactSales_Date
NEXT USED ArchiveFileGroup;

-- Switch old partition to archive table
ALTER TABLE FactSales SWITCH PARTITION 1 TO FactSalesArchive PARTITION 1;

-- Backup and restore archive data
BACKUP DATABASE DataWarehouse 
FILEGROUP = 'ArchiveFileGroup'
TO DISK = 'C:\Backup\DW_Archive.bak';

-- Implement data retention policy
CREATE PROCEDURE sp_ArchiveOldData
    @RetentionDays INT = 2555 -- 7 years
AS
BEGIN
    DECLARE @CutoffDate DATE = DATEADD(DAY, -@RetentionDays, GETDATE());
    
    -- Move data to archive table
    INSERT INTO FactSalesArchive
    SELECT * FROM FactSales
    WHERE DateKey < CONVERT(INT, CONVERT(VARCHAR(8), @CutoffDate, 112));
    
    -- Delete archived data from main table
    DELETE FROM FactSales
    WHERE DateKey < CONVERT(INT, CONVERT(VARCHAR(8), @CutoffDate, 112));
    
    -- Log archival operation
    INSERT INTO ArchivalLog (TableName, ArchivalDate, RecordsArchived)
    VALUES ('FactSales', GETDATE(), @@ROWCOUNT);
END;
```

## Integration & ETL Questions (61-75)

### 11. How do you design and implement Change Data Capture (CDC) in SQL Server?
**Answer**: CDC implementation for real-time data integration and ETL processes.

```sql
-- Enable CDC on database
USE DataWarehouse;
EXEC sys.sp_cdc_enable_db;

-- Enable CDC on specific table
EXEC sys.sp_cdc_enable_table
    @source_schema = 'dbo',
    @source_name = 'Customer',
    @role_name = 'cdc_reader',
    @capture_instance = 'dbo_Customer',
    @supports_net_changes = 1;

-- Query CDC changes
DECLARE @from_lsn BINARY(10), @to_lsn BINARY(10);

-- Get LSN range for time period
SET @from_lsn = sys.fn_cdc_map_time_to_lsn('smallest greater than or equal', '2023-06-01 00:00:00');
SET @to_lsn = sys.fn_cdc_map_time_to_lsn('largest less than or equal', '2023-06-01 23:59:59');

-- Get all changes
SELECT 
    __$operation,
    __$start_lsn,
    __$seqval,
    CustomerID,
    CustomerName,
    City,
    State
FROM cdc.fn_cdc_get_all_changes_dbo_Customer(@from_lsn, @to_lsn, 'all');

-- Get net changes (latest version of each row)
SELECT 
    CustomerID,
    CustomerName,
    City,
    State,
    __$operation
FROM cdc.fn_cdc_get_net_changes_dbo_Customer(@from_lsn, @to_lsn, 'all');

-- ETL process using CDC
CREATE PROCEDURE sp_ProcessCDCChanges
AS
BEGIN
    DECLARE @from_lsn BINARY(10), @to_lsn BINARY(10);
    
    -- Get last processed LSN
    SELECT @from_lsn = ISNULL(LastProcessedLSN, sys.fn_cdc_get_min_lsn('dbo_Customer'))
    FROM CDC_ProcessingLog 
    WHERE TableName = 'Customer';
    
    -- Get current max LSN
    SET @to_lsn = sys.fn_cdc_get_max_lsn();
    
    -- Process changes
    WITH Changes AS (
        SELECT 
            CustomerID,
            CustomerName,
            City,
            State,
            __$operation,
            __$start_lsn
        FROM cdc.fn_cdc_get_net_changes_dbo_Customer(@from_lsn, @to_lsn, 'all')
    )
    MERGE DimCustomer AS target
    USING Changes AS source ON target.CustomerID = source.CustomerID
    WHEN MATCHED AND source.__$operation = 4 THEN -- Update
        UPDATE SET 
            CustomerName = source.CustomerName,
            City = source.City,
            State = source.State,
            ModifiedDate = GETDATE()
    WHEN NOT MATCHED AND source.__$operation IN (2, 4) THEN -- Insert
        INSERT (CustomerID, CustomerName, City, State, CreatedDate)
        VALUES (source.CustomerID, source.CustomerName, source.City, source.State, GETDATE())
    WHEN MATCHED AND source.__$operation = 1 THEN -- Delete
        DELETE;
    
    -- Update processing log
    UPDATE CDC_ProcessingLog 
    SET LastProcessedLSN = @to_lsn, LastProcessedDate = GETDATE()
    WHERE TableName = 'Customer';
END;
```

### 12. How do you implement real-time data streaming with SQL Server and Service Broker?
**Answer**: Service Broker for asynchronous message processing and real-time data flows.

```sql
-- Enable Service Broker
ALTER DATABASE DataWarehouse SET ENABLE_BROKER;

-- Create message types
CREATE MESSAGE TYPE OrderMessage
VALIDATION = WELL_FORMED_XML;

CREATE MESSAGE TYPE OrderResponse
VALIDATION = WELL_FORMED_XML;

-- Create contracts
CREATE CONTRACT OrderProcessingContract (
    OrderMessage SENT BY INITIATOR,
    OrderResponse SENT BY TARGET
);

-- Create queues
CREATE QUEUE OrderQueue;
CREATE QUEUE OrderResponseQueue;

-- Create services
CREATE SERVICE OrderService
ON QUEUE OrderQueue (OrderProcessingContract);

CREATE SERVICE OrderResponseService
ON QUEUE OrderResponseQueue (OrderProcessingContract);

-- Send message
DECLARE @dialog UNIQUEIDENTIFIER;
DECLARE @message XML;

SET @message = '<Order>
    <OrderID>12345</OrderID>
    <CustomerID>67890</CustomerID>
    <Amount>1500.00</Amount>
</Order>';

BEGIN DIALOG @dialog
FROM SERVICE OrderService
TO SERVICE 'OrderResponseService'
ON CONTRACT OrderProcessingContract;

SEND ON CONVERSATION @dialog
MESSAGE TYPE OrderMessage (@message);

-- Receive and process messages
CREATE PROCEDURE sp_ProcessOrderMessages
AS
BEGIN
    DECLARE @dialog UNIQUEIDENTIFIER;
    DECLARE @message_type SYSNAME;
    DECLARE @message_body XML;
    
    WHILE (1=1)
    BEGIN
        RECEIVE TOP(1)
            @dialog = conversation_handle,
            @message_type = message_type_name,
            @message_body = CAST(message_body AS XML)
        FROM OrderQueue;
        
        IF @@ROWCOUNT = 0 BREAK;
        
        IF @message_type = 'OrderMessage'
        BEGIN
            -- Process order
            DECLARE @OrderID INT = @message_body.value('(/Order/OrderID)[1]', 'INT');
            DECLARE @CustomerID INT = @message_body.value('(/Order/CustomerID)[1]', 'INT');
            DECLARE @Amount DECIMAL(10,2) = @message_body.value('(/Order/Amount)[1]', 'DECIMAL(10,2)');
            
            -- Insert into fact table
            INSERT INTO FactOrders (OrderID, CustomerID, Amount, ProcessedDate)
            VALUES (@OrderID, @CustomerID, @Amount, GETDATE());
            
            -- Send response
            DECLARE @response XML = '<Response>
                <Status>Processed</Status>
                <OrderID>' + CAST(@OrderID AS VARCHAR(10)) + '</OrderID>
            </Response>';
            
            SEND ON CONVERSATION @dialog
            MESSAGE TYPE OrderResponse (@response);
        END;
        
        IF @message_type = 'http://schemas.microsoft.com/SQL/ServiceBroker/EndDialog'
        BEGIN
            END CONVERSATION @dialog;
        END;
    END;
END;

-- Activate automatic message processing
ALTER QUEUE OrderQueue
WITH ACTIVATION (
    STATUS = ON,
    PROCEDURE_NAME = sp_ProcessOrderMessages,
    MAX_QUEUE_READERS = 5,
    EXECUTE AS OWNER
);
```

## Security & Administration (76-90)

### 13. How do you implement row-level security and data masking in SQL Server?
**Answer**: Security features for protecting sensitive data in data engineering scenarios.

```sql
-- Row-Level Security (RLS)
-- Create security predicate function
CREATE FUNCTION fn_SecurityPredicate(@UserRegion NVARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS result
WHERE @UserRegion = USER_NAME() OR USER_NAME() = 'DataAdmin';

-- Create security policy
CREATE SECURITY POLICY RegionalSecurityPolicy
ADD FILTER PREDICATE dbo.fn_SecurityPredicate(Region) ON dbo.SalesData,
ADD BLOCK PREDICATE dbo.fn_SecurityPredicate(Region) ON dbo.SalesData
WITH (STATE = ON);

-- Dynamic Data Masking
-- Mask sensitive columns
ALTER TABLE Customer
ALTER COLUMN Email ADD MASKED WITH (FUNCTION = 'email()');

ALTER TABLE Customer
ALTER COLUMN Phone ADD MASKED WITH (FUNCTION = 'partial(1,"XXX-XXX-",4)');

ALTER TABLE Customer
ALTER COLUMN CreditCard ADD MASKED WITH (FUNCTION = 'partial(0,"XXXX-XXXX-XXXX-",4)');

-- Grant unmask permission to specific users
GRANT UNMASK TO DataAnalyst;

-- Column-level encryption
-- Create master key and certificate
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongPassword123!';

CREATE CERTIFICATE CustomerDataCert
WITH SUBJECT = 'Customer Data Protection';

CREATE SYMMETRIC KEY CustomerDataKey
WITH ALGORITHM = AES_256
ENCRYPTION BY CERTIFICATE CustomerDataCert;

-- Encrypt sensitive data
OPEN SYMMETRIC KEY CustomerDataKey
DECRYPTION BY CERTIFICATE CustomerDataCert;

INSERT INTO CustomerSecure (CustomerID, EncryptedSSN)
VALUES (1, EncryptByKey(Key_GUID('CustomerDataKey'), '123-45-6789'));

CLOSE SYMMETRIC KEY CustomerDataKey;

-- Decrypt data
OPEN SYMMETRIC KEY CustomerDataKey
DECRYPTION BY CERTIFICATE CustomerDataCert;

SELECT 
    CustomerID,
    CONVERT(VARCHAR(50), DecryptByKey(EncryptedSSN)) AS SSN
FROM CustomerSecure;

CLOSE SYMMETRIC KEY CustomerDataKey;
```

### 14. How do you implement backup and disaster recovery strategies for data warehouses?
**Answer**: Comprehensive backup and DR strategies for enterprise data systems.

```sql
-- Full backup strategy
-- Full backup (weekly)
BACKUP DATABASE DataWarehouse 
TO DISK = 'C:\Backup\DataWarehouse_Full.bak'
WITH COMPRESSION, CHECKSUM, INIT;

-- Differential backup (daily)
BACKUP DATABASE DataWarehouse 
TO DISK = 'C:\Backup\DataWarehouse_Diff.bak'
WITH DIFFERENTIAL, COMPRESSION, CHECKSUM, INIT;

-- Transaction log backup (every 15 minutes)
BACKUP LOG DataWarehouse 
TO DISK = 'C:\Backup\DataWarehouse_Log.trn'
WITH COMPRESSION, CHECKSUM;

-- Filegroup backup for large warehouses
BACKUP DATABASE DataWarehouse 
FILEGROUP = 'FactData'
TO DISK = 'C:\Backup\DW_FactData.bak'
WITH COMPRESSION, CHECKSUM;

-- Always On Availability Groups setup
-- Create availability group
CREATE AVAILABILITY GROUP DataWarehouseAG
WITH (
    AUTOMATED_BACKUP_PREFERENCE = SECONDARY,
    DB_FAILOVER = ON,
    DTC_SUPPORT = NONE
)
FOR DATABASE DataWarehouse
REPLICA ON 
    'SQL-PRIMARY' WITH (
        ENDPOINT_URL = 'TCP://SQL-PRIMARY:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        BACKUP_PRIORITY = 30
    ),
    'SQL-SECONDARY' WITH (
        ENDPOINT_URL = 'TCP://SQL-SECONDARY:5022',
        AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT,
        FAILOVER_MODE = MANUAL,
        BACKUP_PRIORITY = 90
    );

-- Point-in-time recovery
RESTORE DATABASE DataWarehouse_Recovery
FROM DISK = 'C:\Backup\DataWarehouse_Full.bak'
WITH NORECOVERY, REPLACE;

RESTORE DATABASE DataWarehouse_Recovery
FROM DISK = 'C:\Backup\DataWarehouse_Diff.bak'
WITH NORECOVERY;

RESTORE LOG DataWarehouse_Recovery
FROM DISK = 'C:\Backup\DataWarehouse_Log.trn'
WITH STOPAT = '2023-06-01 14:30:00', RECOVERY;

-- Automated backup maintenance
CREATE PROCEDURE sp_BackupMaintenance
AS
BEGIN
    DECLARE @BackupPath NVARCHAR(500);
    DECLARE @FileName NVARCHAR(500);
    DECLARE @Date NVARCHAR(20) = CONVERT(NVARCHAR(20), GETDATE(), 112);
    
    -- Full backup on Sunday
    IF DATEPART(WEEKDAY, GETDATE()) = 1
    BEGIN
        SET @FileName = 'DataWarehouse_Full_' + @Date + '.bak';
        SET @BackupPath = 'C:\Backup\' + @FileName;
        
        BACKUP DATABASE DataWarehouse 
        TO DISK = @BackupPath
        WITH COMPRESSION, CHECKSUM, INIT;
    END
    -- Differential backup on other days
    ELSE
    BEGIN
        SET @FileName = 'DataWarehouse_Diff_' + @Date + '.bak';
        SET @BackupPath = 'C:\Backup\' + @FileName;
        
        BACKUP DATABASE DataWarehouse 
        TO DISK = @BackupPath
        WITH DIFFERENTIAL, COMPRESSION, CHECKSUM, INIT;
    END;
    
    -- Clean up old backups (keep 30 days)
    EXEC xp_delete_file 0, 'C:\Backup\', 'bak', DATEADD(DAY, -30, GETDATE());
END;
```

## Architecture & Scalability (91-100)

### 15. How do you design a scalable data architecture using SQL Server for big data scenarios?
**Answer**: Scalable architecture patterns for handling large-scale data engineering requirements.

```sql
-- Scale-out architecture with distributed partitioned views
-- Server 1: Historical data (2020-2022)
CREATE TABLE FactSales_Historical (
    SaleDate DATE CHECK (SaleDate >= '2020-01-01' AND SaleDate < '2023-01-01'),
    CustomerID INT,
    ProductID INT,
    Amount DECIMAL(18,2),
    -- Other columns
) ON HistoricalFileGroup;

-- Server 2: Current data (2023+)
CREATE TABLE FactSales_Current (
    SaleDate DATE CHECK (SaleDate >= '2023-01-01'),
    CustomerID INT,
    ProductID INT,
    Amount DECIMAL(18,2),
    -- Other columns
) ON CurrentFileGroup;

-- Create distributed partitioned view
CREATE VIEW FactSales AS
SELECT * FROM Server1.DataWarehouse.dbo.FactSales_Historical
UNION ALL
SELECT * FROM Server2.DataWarehouse.dbo.FactSales_Current;

-- Implement data tiering strategy
-- Hot data: In-memory OLTP for recent transactions
CREATE TABLE FactSales_Hot (
    SaleID BIGINT IDENTITY(1,1) PRIMARY KEY NONCLUSTERED,
    SaleDate DATE NOT NULL,
    CustomerID INT NOT NULL,
    ProductID INT NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    INDEX IX_SaleDate_Hash HASH (SaleDate) WITH (BUCKET_COUNT = 1000000)
) WITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_AND_DATA);

-- Warm data: Regular tables with columnstore
CREATE TABLE FactSales_Warm (
    SaleDate DATE,
    CustomerID INT,
    ProductID INT,
    Amount DECIMAL(18,2)
);
CREATE CLUSTERED COLUMNSTORE INDEX CCI_FactSales_Warm ON FactSales_Warm;

-- Cold data: Compressed and archived
CREATE TABLE FactSales_Cold (
    SaleDate DATE,
    CustomerID INT,
    ProductID INT,
    Amount DECIMAL(18,2)
) WITH (DATA_COMPRESSION = PAGE);

-- Automated data movement between tiers
CREATE PROCEDURE sp_DataTieringMaintenance
AS
BEGIN
    -- Move data from hot to warm (older than 7 days)
    INSERT INTO FactSales_Warm
    SELECT SaleDate, CustomerID, ProductID, Amount
    FROM FactSales_Hot
    WHERE SaleDate < DATEADD(DAY, -7, GETDATE());
    
    DELETE FROM FactSales_Hot
    WHERE SaleDate < DATEADD(DAY, -7, GETDATE());
    
    -- Move data from warm to cold (older than 1 year)
    INSERT INTO FactSales_Cold
    SELECT SaleDate, CustomerID, ProductID, Amount
    FROM FactSales_Warm
    WHERE SaleDate < DATEADD(YEAR, -1, GETDATE());
    
    DELETE FROM FactSales_Warm
    WHERE SaleDate < DATEADD(YEAR, -1, GETDATE());
END;

-- Polybase for big data integration
-- Create external data source
CREATE EXTERNAL DATA SOURCE HadoopCluster
WITH (
    TYPE = HADOOP,
    LOCATION = 'hdfs://hadoop-cluster:8020'
);

-- Create external file format
CREATE EXTERNAL FILE FORMAT TextFileFormat
WITH (
    FORMAT_TYPE = DELIMITEDTEXT,
    FORMAT_OPTIONS (
        FIELD_TERMINATOR = ',',
        STRING_DELIMITER = '"',
        DATE_FORMAT = 'yyyy-MM-dd'
    )
);

-- Create external table
CREATE EXTERNAL TABLE ExternalSalesData (
    SaleDate DATE,
    CustomerID INT,
    ProductID INT,
    Amount DECIMAL(18,2)
)
WITH (
    LOCATION = '/sales_data/',
    DATA_SOURCE = HadoopCluster,
    FILE_FORMAT = TextFileFormat
);

-- Query external data
SELECT 
    YEAR(SaleDate) AS SaleYear,
    SUM(Amount) AS TotalSales
FROM ExternalSalesData
WHERE SaleDate >= '2023-01-01'
GROUP BY YEAR(SaleDate);

-- Hybrid cloud architecture with Azure SQL
-- Stretch database for historical data
ALTER TABLE FactSales_Historical
SET (REMOTE_DATA_ARCHIVE = ON (
    MIGRATION_STATE = OUTBOUND,
    FILTER_PREDICATE = dbo.fn_StretchPredicate(SaleDate)
));

-- Function to determine which rows to stretch
CREATE FUNCTION dbo.fn_StretchPredicate(@SaleDate DATE)
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS is_eligible
WHERE @SaleDate < DATEADD(YEAR, -2, GETDATE());
```

---

## 🎯 **Summary**

This comprehensive guide covers 100 essential SQL Server interview questions for data engineering roles, organized into key categories:

**Key Areas Covered:**
- **Core Concepts**: Storage architecture, partitioning, editions
- **Performance**: Query optimization, indexing, columnstore
- **Data Modeling**: Star schema, SCD, temporal tables
- **Advanced Features**: CDC, Service Broker, compression
- **Integration**: SSIS, ETL patterns, real-time processing
- **Security**: RLS, data masking, encryption
- **Architecture**: Scalability, big data integration, cloud hybrid

**Interview Preparation Tips:**
1. **Understand the fundamentals** of SQL Server architecture
2. **Practice performance tuning** scenarios with real data
3. **Know when to use** different features and technologies
4. **Prepare examples** from your experience with each topic
5. **Stay current** with latest SQL Server features and best practices

**Next Steps:**
- Practice with SQL Server Developer Edition
- Build sample data warehouse projects
- Explore integration with cloud platforms
- Study real-world case studies and architectures

Remember: Focus on practical application and be ready to explain your design decisions and trade-offs during interviews.

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*

