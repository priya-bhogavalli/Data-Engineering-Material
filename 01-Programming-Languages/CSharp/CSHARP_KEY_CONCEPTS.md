# C# Key Concepts

## 1. C# Fundamentals
**What is C#**: Object-oriented programming language developed by Microsoft for .NET platform.

**Key Features**:
- **Type-safe**: Strong typing system
- **Memory managed**: Automatic garbage collection
- **Cross-platform**: .NET Core/5+ runs on multiple OS
- **Object-oriented**: Classes, inheritance, polymorphism
- **Async programming**: Built-in async/await support

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

// Basic syntax
namespace DataEngineering
{
    public class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("Hello Data Engineering!");
            
            // Variables and types
            int recordCount = 1000;
            double averageValue = 45.67;
            string dataSource = "PostgreSQL";
            bool isProcessed = true;
            var inferredType = "Auto-inferred string";
            
            // Arrays and collections
            int[] numbers = {1, 2, 3, 4, 5};
            List<string> databases = new List<string> {"MySQL", "PostgreSQL", "MongoDB"};
        }
    }
}
```

## 2. Object-Oriented Programming
```csharp
// Class definition
public class DataPipeline
{
    // Properties
    public string Name { get; set; }
    public string Source { get; private set; }
    public string Destination { get; private set; }
    public DateTime LastRun { get; set; }
    
    // Auto-implemented property with backing field
    private bool _isRunning;
    public bool IsRunning 
    { 
        get => _isRunning; 
        set 
        { 
            _isRunning = value;
            Console.WriteLine($"Pipeline {Name} is now {(value ? "running" : "stopped")}");
        } 
    }
    
    // Constructor
    public DataPipeline(string name, string source, string destination)
    {
        Name = name ?? throw new ArgumentNullException(nameof(name));
        Source = source;
        Destination = destination;
        LastRun = DateTime.MinValue;
    }
    
    // Methods
    public virtual async Task<bool> ExecuteAsync()
    {
        IsRunning = true;
        
        try
        {
            await ExtractDataAsync();
            await TransformDataAsync();
            await LoadDataAsync();
            
            LastRun = DateTime.Now;
            return true;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Pipeline failed: {ex.Message}");
            return false;
        }
        finally
        {
            IsRunning = false;
        }
    }
    
    protected virtual async Task ExtractDataAsync()
    {
        Console.WriteLine($"Extracting data from {Source}");
        await Task.Delay(1000); // Simulate work
    }
    
    protected virtual async Task TransformDataAsync()
    {
        Console.WriteLine("Transforming data");
        await Task.Delay(500);
    }
    
    protected virtual async Task LoadDataAsync()
    {
        Console.WriteLine($"Loading data to {Destination}");
        await Task.Delay(800);
    }
}

// Inheritance
public class StreamingPipeline : DataPipeline
{
    public TimeSpan ProcessingInterval { get; set; }
    
    public StreamingPipeline(string name, string source, string destination, TimeSpan interval) 
        : base(name, source, destination)
    {
        ProcessingInterval = interval;
    }
    
    public override async Task<bool> ExecuteAsync()
    {
        Console.WriteLine($"Starting streaming pipeline with {ProcessingInterval} interval");
        return await base.ExecuteAsync();
    }
}

// Interface
public interface IDataProcessor
{
    Task<ProcessingResult> ProcessAsync(IEnumerable<DataRecord> records);
    bool CanProcess(DataRecord record);
}

// Implementation
public class SalesDataProcessor : IDataProcessor
{
    public async Task<ProcessingResult> ProcessAsync(IEnumerable<DataRecord> records)
    {
        var processedCount = 0;
        var errors = new List<string>();
        
        foreach (var record in records)
        {
            try
            {
                if (CanProcess(record))
                {
                    await ProcessRecordAsync(record);
                    processedCount++;
                }
            }
            catch (Exception ex)
            {
                errors.Add($"Record {record.Id}: {ex.Message}");
            }
        }
        
        return new ProcessingResult(processedCount, errors);
    }
    
    public bool CanProcess(DataRecord record)
    {
        return record != null && !string.IsNullOrEmpty(record.Id);
    }
    
    private async Task ProcessRecordAsync(DataRecord record)
    {
        // Processing logic
        await Task.Delay(10);
    }
}
```

## 3. Collections and LINQ
```csharp
using System.Linq;

public class DataAnalyzer
{
    public void AnalyzeSalesData()
    {
        var salesData = new List<SalesRecord>
        {
            new SalesRecord { Id = 1, Product = "Laptop", Amount = 1200, Date = DateTime.Now.AddDays(-5) },
            new SalesRecord { Id = 2, Product = "Phone", Amount = 800, Date = DateTime.Now.AddDays(-3) },
            new SalesRecord { Id = 3, Product = "Tablet", Amount = 600, Date = DateTime.Now.AddDays(-1) }
        };
        
        // LINQ queries
        var highValueSales = salesData
            .Where(s => s.Amount > 1000)
            .OrderByDescending(s => s.Amount)
            .ToList();
        
        var salesByProduct = salesData
            .GroupBy(s => s.Product)
            .Select(g => new { Product = g.Key, TotalSales = g.Sum(s => s.Amount) })
            .ToList();
        
        var recentSales = salesData
            .Where(s => s.Date >= DateTime.Now.AddDays(-7))
            .Select(s => new { s.Product, s.Amount })
            .ToList();
        
        // Aggregations
        var totalRevenue = salesData.Sum(s => s.Amount);
        var averageOrderValue = salesData.Average(s => s.Amount);
        var topProduct = salesData
            .GroupBy(s => s.Product)
            .OrderByDescending(g => g.Sum(s => s.Amount))
            .First().Key;
        
        // Complex queries
        var monthlyTrends = salesData
            .GroupBy(s => new { Year = s.Date.Year, Month = s.Date.Month })
            .Select(g => new
            {
                Period = $"{g.Key.Year}-{g.Key.Month:D2}",
                Revenue = g.Sum(s => s.Amount),
                OrderCount = g.Count()
            })
            .OrderBy(x => x.Period)
            .ToList();
    }
}

public class SalesRecord
{
    public int Id { get; set; }
    public string Product { get; set; }
    public decimal Amount { get; set; }
    public DateTime Date { get; set; }
}
```

## 4. Asynchronous Programming
```csharp
public class DataService
{
    private readonly HttpClient _httpClient;
    
    public DataService()
    {
        _httpClient = new HttpClient();
    }
    
    // Async method
    public async Task<List<DataRecord>> FetchDataAsync(string apiUrl)
    {
        try
        {
            var response = await _httpClient.GetStringAsync(apiUrl);
            return JsonSerializer.Deserialize<List<DataRecord>>(response);
        }
        catch (HttpRequestException ex)
        {
            Console.WriteLine($"HTTP error: {ex.Message}");
            return new List<DataRecord>();
        }
    }
    
    // Parallel processing
    public async Task<List<ProcessingResult>> ProcessMultipleSourcesAsync(List<string> sources)
    {
        var tasks = sources.Select(async source =>
        {
            var data = await FetchDataAsync(source);
            return await ProcessDataAsync(data);
        });
        
        return (await Task.WhenAll(tasks)).ToList();
    }
    
    // Task with timeout
    public async Task<DataRecord> FetchWithTimeoutAsync(string url, TimeSpan timeout)
    {
        using var cts = new CancellationTokenSource(timeout);
        
        try
        {
            var data = await FetchDataAsync(url);
            return data.FirstOrDefault();
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("Operation timed out");
            return null;
        }
    }
    
    // Background processing
    public async Task StartBackgroundProcessingAsync(CancellationToken cancellationToken)
    {
        while (!cancellationToken.IsCancellationRequested)
        {
            try
            {
                await ProcessPendingDataAsync();
                await Task.Delay(TimeSpan.FromMinutes(5), cancellationToken);
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Background processing cancelled");
                break;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Background processing error: {ex.Message}");
                await Task.Delay(TimeSpan.FromMinutes(1), cancellationToken);
            }
        }
    }
    
    private async Task<ProcessingResult> ProcessDataAsync(List<DataRecord> data)
    {
        // Simulate processing
        await Task.Delay(1000);
        return new ProcessingResult(data.Count, new List<string>());
    }
    
    private async Task ProcessPendingDataAsync()
    {
        // Background processing logic
        await Task.Delay(100);
    }
}
```

## 5. Error Handling and Logging
```csharp
using Microsoft.Extensions.Logging;

public class DataProcessor
{
    private readonly ILogger<DataProcessor> _logger;
    
    public DataProcessor(ILogger<DataProcessor> logger)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
    
    public async Task<ProcessingResult> ProcessDataAsync(IEnumerable<DataRecord> records)
    {
        _logger.LogInformation("Starting data processing for {RecordCount} records", records.Count());
        
        var processedCount = 0;
        var errors = new List<string>();
        
        try
        {
            foreach (var record in records)
            {
                try
                {
                    ValidateRecord(record);
                    await ProcessSingleRecordAsync(record);
                    processedCount++;
                    
                    if (processedCount % 100 == 0)
                    {
                        _logger.LogDebug("Processed {ProcessedCount} records", processedCount);
                    }
                }
                catch (ValidationException ex)
                {
                    _logger.LogWarning("Validation failed for record {RecordId}: {Error}", 
                        record.Id, ex.Message);
                    errors.Add($"Record {record.Id}: {ex.Message}");
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Unexpected error processing record {RecordId}", record.Id);
                    errors.Add($"Record {record.Id}: Unexpected error");
                }
            }
            
            _logger.LogInformation("Processing completed. Processed: {ProcessedCount}, Errors: {ErrorCount}", 
                processedCount, errors.Count);
            
            return new ProcessingResult(processedCount, errors);
        }
        catch (Exception ex)
        {
            _logger.LogCritical(ex, "Critical error during data processing");
            throw new DataProcessingException("Critical processing failure", ex);
        }
    }
    
    private void ValidateRecord(DataRecord record)
    {
        if (record == null)
            throw new ValidationException("Record cannot be null");
            
        if (string.IsNullOrEmpty(record.Id))
            throw new ValidationException("Record ID is required");
            
        if (record.Amount < 0)
            throw new ValidationException("Amount cannot be negative");
    }
    
    private async Task ProcessSingleRecordAsync(DataRecord record)
    {
        // Processing logic
        await Task.Delay(10);
    }
}

// Custom exceptions
public class DataProcessingException : Exception
{
    public DataProcessingException(string message) : base(message) { }
    public DataProcessingException(string message, Exception innerException) : base(message, innerException) { }
}

public class ValidationException : Exception
{
    public ValidationException(string message) : base(message) { }
}
```

## 6. Dependency Injection and Configuration
```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;

// Startup configuration
public class Program
{
    public static async Task Main(string[] args)
    {
        var host = CreateHostBuilder(args).Build();
        
        var dataService = host.Services.GetRequiredService<IDataService>();
        await dataService.ProcessDataAsync();
        
        await host.RunAsync();
    }
    
    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureServices((context, services) =>
            {
                // Configuration
                var configuration = context.Configuration;
                services.Configure<DatabaseOptions>(configuration.GetSection("Database"));
                services.Configure<ApiOptions>(configuration.GetSection("Api"));
                
                // Services
                services.AddHttpClient();
                services.AddScoped<IDataService, DataService>();
                services.AddScoped<IDataProcessor, SalesDataProcessor>();
                services.AddSingleton<IDataCache, MemoryDataCache>();
                
                // Background services
                services.AddHostedService<DataProcessingService>();
            });
}

// Configuration classes
public class DatabaseOptions
{
    public string ConnectionString { get; set; }
    public int CommandTimeout { get; set; } = 30;
    public int MaxRetries { get; set; } = 3;
}

public class ApiOptions
{
    public string BaseUrl { get; set; }
    public string ApiKey { get; set; }
    public TimeSpan Timeout { get; set; } = TimeSpan.FromSeconds(30);
}

// Service interfaces
public interface IDataService
{
    Task ProcessDataAsync();
}

public interface IDataCache
{
    Task<T> GetAsync<T>(string key);
    Task SetAsync<T>(string key, T value, TimeSpan expiration);
}

// Background service
public class DataProcessingService : BackgroundService
{
    private readonly IDataService _dataService;
    private readonly ILogger<DataProcessingService> _logger;
    
    public DataProcessingService(IDataService dataService, ILogger<DataProcessingService> logger)
    {
        _dataService = dataService;
        _logger = logger;
    }
    
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await _dataService.ProcessDataAsync();
                await Task.Delay(TimeSpan.FromHours(1), stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in background data processing");
                await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
            }
        }
    }
}
```

## 7. Database Operations
```csharp
using System.Data;
using System.Data.SqlClient;
using Dapper;

public class DatabaseService
{
    private readonly string _connectionString;
    
    public DatabaseService(string connectionString)
    {
        _connectionString = connectionString ?? throw new ArgumentNullException(nameof(connectionString));
    }
    
    // ADO.NET example
    public async Task<List<Customer>> GetCustomersAsync()
    {
        var customers = new List<Customer>();
        
        using var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync();
        
        var command = new SqlCommand("SELECT Id, Name, Email FROM Customers WHERE IsActive = 1", connection);
        
        using var reader = await command.ExecuteReaderAsync();
        while (await reader.ReadAsync())
        {
            customers.Add(new Customer
            {
                Id = reader.GetInt32("Id"),
                Name = reader.GetString("Name"),
                Email = reader.GetString("Email")
            });
        }
        
        return customers;
    }
    
    // Dapper example
    public async Task<IEnumerable<Order>> GetOrdersByCustomerAsync(int customerId)
    {
        using var connection = new SqlConnection(_connectionString);
        
        var sql = @"
            SELECT o.Id, o.OrderDate, o.TotalAmount, c.Name as CustomerName
            FROM Orders o
            INNER JOIN Customers c ON o.CustomerId = c.Id
            WHERE o.CustomerId = @CustomerId
            ORDER BY o.OrderDate DESC";
        
        return await connection.QueryAsync<Order>(sql, new { CustomerId = customerId });
    }
    
    // Bulk operations
    public async Task BulkInsertSalesDataAsync(IEnumerable<SalesRecord> records)
    {
        using var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync();
        
        using var transaction = connection.BeginTransaction();
        
        try
        {
            var dataTable = new DataTable();
            dataTable.Columns.Add("Product", typeof(string));
            dataTable.Columns.Add("Amount", typeof(decimal));
            dataTable.Columns.Add("Date", typeof(DateTime));
            
            foreach (var record in records)
            {
                dataTable.Rows.Add(record.Product, record.Amount, record.Date);
            }
            
            using var bulkCopy = new SqlBulkCopy(connection, SqlBulkCopyOptions.Default, transaction);
            bulkCopy.DestinationTableName = "SalesData";
            bulkCopy.BatchSize = 1000;
            
            await bulkCopy.WriteToServerAsync(dataTable);
            transaction.Commit();
        }
        catch
        {
            transaction.Rollback();
            throw;
        }
    }
}

public class Customer
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
}

public class Order
{
    public int Id { get; set; }
    public DateTime OrderDate { get; set; }
    public decimal TotalAmount { get; set; }
    public string CustomerName { get; set; }
}
```

## 8. File and Stream Processing
```csharp
using System.IO;
using System.Text.Json;
using CsvHelper;

public class FileProcessor
{
    public async Task<List<DataRecord>> ReadCsvFileAsync(string filePath)
    {
        var records = new List<DataRecord>();
        
        using var reader = new StreamReader(filePath);
        using var csv = new CsvReader(reader, CultureInfo.InvariantCulture);
        
        await foreach (var record in csv.GetRecordsAsync<DataRecord>())
        {
            records.Add(record);
        }
        
        return records;
    }
    
    public async Task WriteJsonFileAsync<T>(string filePath, IEnumerable<T> data)
    {
        var options = new JsonSerializerOptions
        {
            WriteIndented = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };
        
        using var stream = File.Create(filePath);
        await JsonSerializer.SerializeAsync(stream, data, options);
    }
    
    public async Task ProcessLargeFileAsync(string inputPath, string outputPath, 
        Func<string, string> processor)
    {
        using var reader = new StreamReader(inputPath);
        using var writer = new StreamWriter(outputPath);
        
        string line;
        while ((line = await reader.ReadLineAsync()) != null)
        {
            var processedLine = processor(line);
            await writer.WriteLineAsync(processedLine);
        }
    }
    
    // Memory-efficient processing
    public async IAsyncEnumerable<DataRecord> ReadLargeFileAsync(string filePath)
    {
        using var reader = new StreamReader(filePath);
        using var csv = new CsvReader(reader, CultureInfo.InvariantCulture);
        
        await foreach (var record in csv.GetRecordsAsync<DataRecord>())
        {
            yield return record;
        }
    }
}
```

## 9. Performance and Memory Management
```csharp
public class PerformanceOptimizedProcessor
{
    // Use Span<T> for memory efficiency
    public void ProcessData(ReadOnlySpan<byte> data)
    {
        for (int i = 0; i < data.Length; i++)
        {
            // Process each byte without allocation
            var value = data[i];
            // Processing logic
        }
    }
    
    // Object pooling
    private readonly ObjectPool<StringBuilder> _stringBuilderPool;
    
    public string BuildString(IEnumerable<string> parts)
    {
        var sb = _stringBuilderPool.Get();
        try
        {
            foreach (var part in parts)
            {
                sb.Append(part);
            }
            return sb.ToString();
        }
        finally
        {
            _stringBuilderPool.Return(sb);
        }
    }
    
    // Parallel processing
    public async Task<List<ProcessingResult>> ProcessInParallelAsync(IEnumerable<DataRecord> records)
    {
        var partitioner = Partitioner.Create(records, true);
        var results = new ConcurrentBag<ProcessingResult>();
        
        await Task.Run(() =>
        {
            Parallel.ForEach(partitioner, record =>
            {
                var result = ProcessRecord(record);
                results.Add(result);
            });
        });
        
        return results.ToList();
    }
    
    private ProcessingResult ProcessRecord(DataRecord record)
    {
        // Processing logic
        return new ProcessingResult(1, new List<string>());
    }
}
```

## 10. Testing
```csharp
using Xunit;
using Moq;

public class DataProcessorTests
{
    [Fact]
    public async Task ProcessDataAsync_ValidRecords_ReturnsSuccessResult()
    {
        // Arrange
        var logger = new Mock<ILogger<DataProcessor>>();
        var processor = new DataProcessor(logger.Object);
        
        var records = new List<DataRecord>
        {
            new DataRecord { Id = "1", Amount = 100 },
            new DataRecord { Id = "2", Amount = 200 }
        };
        
        // Act
        var result = await processor.ProcessDataAsync(records);
        
        // Assert
        Assert.Equal(2, result.ProcessedCount);
        Assert.Empty(result.Errors);
    }
    
    [Theory]
    [InlineData(null)]
    [InlineData("")]
    public async Task ProcessDataAsync_InvalidId_ReturnsError(string invalidId)
    {
        // Arrange
        var logger = new Mock<ILogger<DataProcessor>>();
        var processor = new DataProcessor(logger.Object);
        
        var records = new List<DataRecord>
        {
            new DataRecord { Id = invalidId, Amount = 100 }
        };
        
        // Act
        var result = await processor.ProcessDataAsync(records);
        
        // Assert
        Assert.Equal(0, result.ProcessedCount);
        Assert.Single(result.Errors);
    }
}

public class DataRecord
{
    public string Id { get; set; }
    public decimal Amount { get; set; }
}

public class ProcessingResult
{
    public int ProcessedCount { get; }
    public List<string> Errors { get; }
    
    public ProcessingResult(int processedCount, List<string> errors)
    {
        ProcessedCount = processedCount;
        Errors = errors ?? new List<string>();
    }
}
```