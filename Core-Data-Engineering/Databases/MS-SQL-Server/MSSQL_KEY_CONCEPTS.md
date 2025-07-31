# Microsoft SQL Server Key Concepts

## 1. Database Engine Architecture
**What it is**: Relational database management system with enterprise-grade features.

**Core Components**:
- **Database Engine**: Core service for storing and processing data
- **SQL Server Agent**: Job scheduling and automation
- **Analysis Services**: OLAP and data mining
- **Integration Services (SSIS)**: ETL platform
- **Reporting Services (SSRS)**: Report generation

```sql
-- Database creation with file groups
CREATE DATABASE SalesDB
ON 
( NAME = 'SalesDB_Data',
  FILENAME = 'C:\Data\SalesDB_Data.mdf',
  SIZE = 100MB,
  MAXSIZE = 1GB,
  FILEGROWTH = 10MB )
LOG ON 
( NAME = 'SalesDB_Log',
  FILENAME = 'C:\Data\SalesDB_Log.ldf',
  SIZE = 10MB,
  FILEGROWTH = 10% );
```

## 2. T-SQL (Transact-SQL)
**What it is**: Microsoft's extension to SQL with procedural programming capabilities.

**Key Features**:
```sql
-- Variables and control flow
DECLARE @CustomerCount INT;
SET @CustomerCount = (SELECT COUNT(*) FROM Customers);

IF @CustomerCount > 1000
BEGIN
    PRINT 'Large customer base';
END
ELSE
BEGIN
    PRINT 'Growing customer base';
END

-- Common Table Expressions (CTEs)
WITH SalesRanking AS (
    SELECT 
        CustomerID,
        TotalSales,
        ROW_NUMBER() OVER (ORDER BY TotalSales DESC) as Rank
    FROM CustomerSales
)
SELECT * FROM SalesRanking WHERE Rank <= 10;

-- Window functions
SELECT 
    CustomerID,
    OrderDate,
    Amount,
    SUM(Amount) OVER (PARTITION BY CustomerID ORDER BY OrderDate) as RunningTotal,
    LAG(Amount, 1) OVER (PARTITION BY CustomerID ORDER BY OrderDate) as PreviousAmount
FROM Orders;
```

## 3. Stored Procedures and Functions
**Stored Procedures**: Precompiled SQL statements for better performance and security.

```sql
-- Stored procedure with parameters
CREATE PROCEDURE GetCustomerOrders
    @CustomerID INT,
    @StartDate DATE = NULL,
    @EndDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        OrderID,
        OrderDate,
        TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
        AND (@StartDate IS NULL OR OrderDate >= @StartDate)
        AND (@EndDate IS NULL OR OrderDate <= @EndDate)
    ORDER BY OrderDate DESC;
END;

-- Execute procedure
EXEC GetCustomerOrders @CustomerID = 123, @StartDate = '2024-01-01';

-- User-defined function
CREATE FUNCTION CalculateDiscount(@Amount DECIMAL(10,2), @CustomerType VARCHAR(20))
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @Discount DECIMAL(10,2) = 0;
    
    IF @CustomerType = 'Premium'
        SET @Discount = @Amount * 0.15;
    ELSE IF @CustomerType = 'Standard'
        SET @Discount = @Amount * 0.10;
    
    RETURN @Discount;
END;
```

## 4. Indexing Strategy
**Index Types and Usage**:

```sql
-- Clustered index (one per table)
CREATE CLUSTERED INDEX IX_Orders_OrderDate 
ON Orders (OrderDate);

-- Non-clustered index
CREATE NONCLUSTERED INDEX IX_Customers_LastName 
ON Customers (LastName)
INCLUDE (FirstName, Email);

-- Composite index
CREATE INDEX IX_Orders_Customer_Date 
ON Orders (CustomerID, OrderDate);

-- Filtered index
CREATE INDEX IX_Orders_Active 
ON Orders (OrderDate)
WHERE Status = 'Active';

-- Columnstore index for analytics
CREATE COLUMNSTORE INDEX IX_Sales_Columnstore 
ON SalesData (CustomerID, ProductID, SaleDate, Amount);
```

**Index Maintenance**:
```sql
-- Check index fragmentation
SELECT 
    i.name as IndexName,
    s.avg_fragmentation_in_percent,
    s.page_count
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED') s
JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
WHERE s.avg_fragmentation_in_percent > 10;

-- Rebuild fragmented indexes
ALTER INDEX IX_Orders_OrderDate ON Orders REBUILD;
```

## 5. Partitioning
**Table Partitioning**: Divide large tables for better performance and maintenance.

```sql
-- Create partition function
CREATE PARTITION FUNCTION SalesDateRange (DATE)
AS RANGE RIGHT FOR VALUES 
('2023-01-01', '2023-04-01', '2023-07-01', '2023-10-01', '2024-01-01');

-- Create partition scheme
CREATE PARTITION SCHEME SalesDateScheme
AS PARTITION SalesDateRange
TO (FileGroup1, FileGroup2, FileGroup3, FileGroup4, FileGroup5);

-- Create partitioned table
CREATE TABLE SalesData (
    SaleID INT IDENTITY(1,1),
    SaleDate DATE,
    CustomerID INT,
    Amount DECIMAL(10,2),
    CONSTRAINT PK_SalesData PRIMARY KEY (SaleID, SaleDate)
) ON SalesDateScheme(SaleDate);

-- Query specific partition
SELECT * FROM SalesData
WHERE SaleDate >= '2024-01-01' AND SaleDate < '2024-04-01';
```

## 6. Transaction Management
**ACID Properties**: Atomicity, Consistency, Isolation, Durability.

```sql
-- Explicit transaction
BEGIN TRANSACTION;

BEGIN TRY
    UPDATE Accounts SET Balance = Balance - 1000 WHERE AccountID = 1;
    UPDATE Accounts SET Balance = Balance + 1000 WHERE AccountID = 2;
    
    INSERT INTO TransactionLog (FromAccount, ToAccount, Amount, TransactionDate)
    VALUES (1, 2, 1000, GETDATE());
    
    COMMIT TRANSACTION;
    PRINT 'Transfer completed successfully';
END TRY
BEGIN CATCH
    ROLLBACK TRANSACTION;
    PRINT 'Transfer failed: ' + ERROR_MESSAGE();
END CATCH;

-- Isolation levels
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Options: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE, SNAPSHOT
```

## 7. Security Features
**Authentication and Authorization**:

```sql
-- Create login and user
CREATE LOGIN DataAnalyst WITH PASSWORD = 'SecurePassword123!';
USE SalesDB;
CREATE USER DataAnalyst FOR LOGIN DataAnalyst;

-- Grant permissions
GRANT SELECT ON Sales TO DataAnalyst;
GRANT EXECUTE ON GetCustomerOrders TO DataAnalyst;

-- Role-based security
CREATE ROLE SalesReaders;
GRANT SELECT ON Sales TO SalesReaders;
ALTER ROLE SalesReaders ADD MEMBER DataAnalyst;

-- Row-level security
CREATE FUNCTION fn_SecurityPredicate(@CustomerID INT)
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS result 
WHERE @CustomerID = USER_ID() OR IS_MEMBER('SalesManagers') = 1;

CREATE SECURITY POLICY CustomerFilter
ADD FILTER PREDICATE fn_SecurityPredicate(CustomerID) ON Sales
WITH (STATE = ON);
```

## 8. High Availability and Disaster Recovery
**Always On Availability Groups**:

```sql
-- Create availability group
CREATE AVAILABILITY GROUP SalesAG
WITH (
    AUTOMATED_BACKUP_PREFERENCE = SECONDARY,
    DB_FAILOVER = ON,
    DTC_SUPPORT = NONE
)
FOR DATABASE SalesDB
REPLICA ON 
    'SQL-PRIMARY' WITH (
        ENDPOINT_URL = 'TCP://SQL-PRIMARY:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC
    ),
    'SQL-SECONDARY' WITH (
        ENDPOINT_URL = 'TCP://SQL-SECONDARY:5022',
        AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT,
        FAILOVER_MODE = MANUAL
    );
```

**Backup Strategy**:
```sql
-- Full backup
BACKUP DATABASE SalesDB 
TO DISK = 'C:\Backups\SalesDB_Full.bak'
WITH COMPRESSION, CHECKSUM;

-- Differential backup
BACKUP DATABASE SalesDB 
TO DISK = 'C:\Backups\SalesDB_Diff.bak'
WITH DIFFERENTIAL, COMPRESSION;

-- Transaction log backup
BACKUP LOG SalesDB 
TO DISK = 'C:\Backups\SalesDB_Log.trn';
```

## 9. Performance Monitoring
**Dynamic Management Views (DMVs)**:

```sql
-- Top resource-consuming queries
SELECT TOP 10
    qs.total_elapsed_time / qs.execution_count as avg_elapsed_time,
    qs.total_logical_reads / qs.execution_count as avg_logical_reads,
    qs.execution_count,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset
            WHEN -1 THEN DATALENGTH(qt.text)
            ELSE qs.statement_end_offset
        END - qs.statement_start_offset)/2)+1) as query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;

-- Index usage statistics
SELECT 
    i.name as IndexName,
    s.user_seeks,
    s.user_scans,
    s.user_lookups,
    s.user_updates
FROM sys.dm_db_index_usage_stats s
JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
WHERE s.database_id = DB_ID();

-- Wait statistics
SELECT TOP 10
    wait_type,
    wait_time_ms,
    signal_wait_time_ms,
    waiting_tasks_count
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN ('CLR_SEMAPHORE', 'LAZYWRITER_SLEEP', 'RESOURCE_QUEUE')
ORDER BY wait_time_ms DESC;
```

## 10. Integration and ETL
**SQL Server Integration Services (SSIS)**:

```sql
-- Bulk insert for large data loads
BULK INSERT SalesData
FROM 'C:\Data\sales_data.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
    BATCHSIZE = 10000,
    TABLOCK
);

-- Merge statement for upsert operations
MERGE CustomerDimension AS target
USING CustomerStaging AS source
ON target.CustomerID = source.CustomerID
WHEN MATCHED THEN
    UPDATE SET 
        CustomerName = source.CustomerName,
        LastModified = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (CustomerID, CustomerName, CreatedDate)
    VALUES (source.CustomerID, source.CustomerName, GETDATE());
```

**Linked Servers**:
```sql
-- Create linked server
EXEC sp_addlinkedserver 
    @server = 'ORACLE_SERVER',
    @srvproduct = 'Oracle',
    @provider = 'OraOLEDB.Oracle',
    @datasrc = 'OracleDB';

-- Query linked server
SELECT * FROM ORACLE_SERVER.HR.dbo.Employees;
```