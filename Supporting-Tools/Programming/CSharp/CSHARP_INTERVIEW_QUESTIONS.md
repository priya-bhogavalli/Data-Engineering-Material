# C# Interview Questions for Data Engineering

## 📋 Table of Contents
1. [Basic C# Concepts](#basic-c-concepts)
2. [Object-Oriented Programming](#object-oriented-programming)
3. [Data Structures & Collections](#data-structures--collections)
4. [LINQ & Data Processing](#linq--data-processing)
5. [File I/O & Data Handling](#file-io--data-handling)
6. [Database Connectivity](#database-connectivity)
7. [Async Programming](#async-programming)
8. [Performance & Memory Management](#performance--memory-management)
9. [Data Engineering Specific](#data-engineering-specific)
10. [Advanced Topics](#advanced-topics)

---

## Basic C# Concepts

### Q1: What are the main differences between C# and Python for data processing?
**Answer:**
- **Type System**: C# is statically typed, Python is dynamically typed
- **Performance**: C# generally faster execution, better for large-scale processing
- **Memory Management**: C# has automatic garbage collection with more control
- **Ecosystem**: Python has richer data science libraries, C# has strong enterprise integration
- **Syntax**: Python more concise, C# more verbose but explicit
- **Deployment**: C# compiles to bytecode, easier enterprise deployment

### Q2: Explain value types vs reference types in C#
**Answer:**
```csharp
// Value types - stored on stack
int number = 42;
DateTime date = DateTime.Now;
struct Point { public int X, Y; }

// Reference types - stored on heap
string text = "Hello";
List<int> numbers = new List<int>();
class Person { public string Name; }
```
- **Value types**: int, double, bool, struct, enum - copied by value
- **Reference types**: string, array, class, interface - copied by reference
- **Boxing/Unboxing**: Converting between value and reference types

### Q3: What is the difference between `string` and `StringBuilder`?
**Answer:**
```csharp
// String - immutable, creates new objects
string result = "";
for (int i = 0; i < 1000; i++)
    result += i.ToString(); // Creates 1000 string objects

// StringBuilder - mutable, efficient for concatenation
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++)
    sb.Append(i); // Reuses internal buffer
string result = sb.ToString();
```
- Use `StringBuilder` for multiple concatenations
- Use `string` for simple operations and immutability

---

## Object-Oriented Programming

### Q4: Explain inheritance vs composition in C#
**Answer:**
```csharp
// Inheritance - "is-a" relationship
public class DataProcessor : BaseProcessor
{
    public override void Process() { /* implementation */ }
}

// Composition - "has-a" relationship
public class ETLPipeline
{
    private readonly IDataExtractor _extractor;
    private readonly IDataTransformer _transformer;
    
    public ETLPipeline(IDataExtractor extractor, IDataTransformer transformer)
    {
        _extractor = extractor;
        _transformer = transformer;
    }
}
```
- **Inheritance**: Code reuse, polymorphism, tight coupling
- **Composition**: Flexibility, loose coupling, dependency injection

### Q5: What are interfaces and when to use them?
**Answer:**
```csharp
public interface IDataSource
{
    Task<IEnumerable<T>> GetDataAsync<T>();
    bool IsConnected { get; }
}

public class DatabaseSource : IDataSource
{
    public async Task<IEnumerable<T>> GetDataAsync<T>() { /* implementation */ }
    public bool IsConnected => _connection.State == ConnectionState.Open;
}

public class FileSource : IDataSource
{
    public async Task<IEnumerable<T>> GetDataAsync<T>() { /* implementation */ }
    public bool IsConnected => File.Exists(_filePath);
}
```
- **Use interfaces for**: Abstraction, testability, multiple implementations
- **Benefits**: Loose coupling, dependency injection, polymorphism

---

## Data Structures & Collections

### Q6: Compare List<T>, Array, and IEnumerable<T>
**Answer:**
```csharp
// Array - fixed size, fastest access
int[] numbers = new int[1000];
numbers[0] = 42; // O(1) access

// List<T> - dynamic size, good performance
List<int> list = new List<int>();
list.Add(42); // Amortized O(1)

// IEnumerable<T> - deferred execution, memory efficient
IEnumerable<int> query = data.Where(x => x > 0).Select(x => x * 2);
// No execution until enumerated
```
- **Array**: Best for fixed-size, high-performance scenarios
- **List<T>**: Best for dynamic collections with random access
- **IEnumerable<T>**: Best for streaming, deferred execution

### Q7: Explain Dictionary<TKey, TValue> performance characteristics
**Answer:**
```csharp
Dictionary<string, Customer> customers = new Dictionary<string, Customer>();

// O(1) average case operations
customers.Add("CUST001", customer);
Customer found = customers["CUST001"];
bool exists = customers.ContainsKey("CUST001");

// For data engineering - fast lookups
var customerLookup = customers.ToDictionary(c => c.Id, c => c);
var enrichedOrders = orders.Select(o => new {
    Order = o,
    Customer = customerLookup[o.CustomerId]
});
```
- **Time Complexity**: O(1) average for add, get, remove
- **Space Complexity**: O(n)
- **Use cases**: Lookups, joins, caching

---

## LINQ & Data Processing

### Q8: Explain deferred execution in LINQ
**Answer:**
```csharp
var data = new List<int> { 1, 2, 3, 4, 5 };

// Deferred execution - query not executed
var query = data.Where(x => x > 2).Select(x => x * 2);

data.Add(6); // Affects query result

// Execution happens here
var result = query.ToList(); // [6, 8, 10, 12]

// Immediate execution
var immediate = data.Where(x => x > 2).Select(x => x * 2).ToList();
data.Add(7); // Doesn't affect immediate result
```
- **Deferred**: Where, Select, Take, Skip
- **Immediate**: ToList, ToArray, Count, First, Any

### Q9: Write a LINQ query to group and aggregate data
**Answer:**
```csharp
public class SalesRecord
{
    public string Region { get; set; }
    public string Product { get; set; }
    public decimal Amount { get; set; }
    public DateTime Date { get; set; }
}

var salesData = GetSalesData();

// Group by region and calculate totals
var regionSummary = salesData
    .GroupBy(s => s.Region)
    .Select(g => new {
        Region = g.Key,
        TotalSales = g.Sum(s => s.Amount),
        AverageSale = g.Average(s => s.Amount),
        TransactionCount = g.Count(),
        TopProduct = g.GroupBy(s => s.Product)
                      .OrderByDescending(p => p.Sum(s => s.Amount))
                      .First().Key
    })
    .OrderByDescending(r => r.TotalSales);
```

### Q10: How do you handle large datasets with LINQ efficiently?
**Answer:**
```csharp
// Use streaming with IEnumerable
public IEnumerable<ProcessedRecord> ProcessLargeDataset(IEnumerable<RawRecord> data)
{
    return data
        .Where(r => r.IsValid)
        .Select(r => ProcessRecord(r))
        .Where(p => p != null);
    // No ToList() - keeps streaming
}

// Parallel processing for CPU-intensive operations
var results = largeDataset
    .AsParallel()
    .WithDegreeOfParallelism(Environment.ProcessorCount)
    .Where(item => IsValidItem(item))
    .Select(item => ProcessItem(item))
    .ToList();

// Batch processing
var batches = data.Batch(1000); // Extension method
foreach (var batch in batches)
{
    ProcessBatch(batch.ToList());
}
```

---

## File I/O & Data Handling

### Q11: How do you read large files efficiently in C#?
**Answer:**
```csharp
// Streaming approach for large files
public async IAsyncEnumerable<string> ReadLargeFileAsync(string filePath)
{
    using var reader = new StreamReader(filePath);
    string line;
    while ((line = await reader.ReadLineAsync()) != null)
    {
        yield return line;
    }
}

// Usage
await foreach (var line in ReadLargeFileAsync("large-file.txt"))
{
    ProcessLine(line);
}

// CSV processing with streaming
public async IAsyncEnumerable<T> ReadCsvAsync<T>(string filePath) 
    where T : class, new()
{
    using var reader = new StreamReader(filePath);
    var csv = new CsvReader(reader, CultureInfo.InvariantCulture);
    
    await foreach (var record in csv.GetRecordsAsync<T>())
    {
        yield return record;
    }
}
```

### Q12: How do you handle different file formats in C#?
**Answer:**
```csharp
// JSON processing
public class JsonDataProcessor
{
    public async Task<List<T>> ReadJsonAsync<T>(string filePath)
    {
        var json = await File.ReadAllTextAsync(filePath);
        return JsonSerializer.Deserialize<List<T>>(json);
    }
    
    public async Task WriteJsonAsync<T>(string filePath, T data)
    {
        var options = new JsonSerializerOptions { WriteIndented = true };
        var json = JsonSerializer.Serialize(data, options);
        await File.WriteAllTextAsync(filePath, json);
    }
}

// XML processing
public class XmlDataProcessor
{
    public List<T> ReadXml<T>(string filePath) where T : class
    {
        var serializer = new XmlSerializer(typeof(List<T>));
        using var reader = new FileStream(filePath, FileMode.Open);
        return (List<T>)serializer.Deserialize(reader);
    }
}

// Excel processing (using EPPlus)
public class ExcelProcessor
{
    public List<T> ReadExcel<T>(string filePath, string worksheetName) where T : class, new()
    {
        using var package = new ExcelPackage(new FileInfo(filePath));
        var worksheet = package.Workbook.Worksheets[worksheetName];
        return worksheet.ConvertSheetToObjects<T>().ToList();
    }
}
```

---

## Database Connectivity

### Q13: How do you implement database operations efficiently?
**Answer:**
```csharp
// Using Entity Framework Core
public class DataContext : DbContext
{
    public DbSet<Customer> Customers { get; set; }
    public DbSet<Order> Orders { get; set; }
    
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlServer(connectionString);
    }
}

// Repository pattern
public class CustomerRepository
{
    private readonly DataContext _context;
    
    public async Task<List<Customer>> GetCustomersByRegionAsync(string region)
    {
        return await _context.Customers
            .Where(c => c.Region == region)
            .Include(c => c.Orders)
            .ToListAsync();
    }
    
    public async Task BulkInsertAsync(List<Customer> customers)
    {
        _context.Customers.AddRange(customers);
        await _context.SaveChangesAsync();
    }
}

// Raw SQL for performance-critical operations
public async Task<List<SalesReport>> GetSalesReportAsync(DateTime startDate, DateTime endDate)
{
    var sql = @"
        SELECT 
            c.Region,
            SUM(o.Amount) as TotalSales,
            COUNT(*) as OrderCount
        FROM Customers c
        INNER JOIN Orders o ON c.Id = o.CustomerId
        WHERE o.OrderDate BETWEEN @StartDate AND @EndDate
        GROUP BY c.Region";
        
    return await _context.Database
        .SqlQueryRaw<SalesReport>(sql, 
            new SqlParameter("@StartDate", startDate),
            new SqlParameter("@EndDate", endDate))
        .ToListAsync();
}
```

### Q14: How do you handle database transactions?
**Answer:**
```csharp
// Using transactions for data consistency
public async Task ProcessOrderAsync(Order order, List<OrderItem> items)
{
    using var transaction = await _context.Database.BeginTransactionAsync();
    try
    {
        // Insert order
        _context.Orders.Add(order);
        await _context.SaveChangesAsync();
        
        // Update inventory
        foreach (var item in items)
        {
            var product = await _context.Products.FindAsync(item.ProductId);
            product.Stock -= item.Quantity;
        }
        
        // Insert order items
        _context.OrderItems.AddRange(items);
        await _context.SaveChangesAsync();
        
        await transaction.CommitAsync();
    }
    catch
    {
        await transaction.RollbackAsync();
        throw;
    }
}
```

---

## Async Programming

### Q15: Explain async/await and when to use it
**Answer:**
```csharp
// Async method for I/O operations
public async Task<List<Customer>> GetCustomersAsync()
{
    using var client = new HttpClient();
    var response = await client.GetStringAsync("https://api.example.com/customers");
    return JsonSerializer.Deserialize<List<Customer>>(response);
}

// Parallel async operations
public async Task<(List<Customer> customers, List<Order> orders)> GetDataAsync()
{
    var customersTask = GetCustomersAsync();
    var ordersTask = GetOrdersAsync();
    
    await Task.WhenAll(customersTask, ordersTask);
    
    return (await customersTask, await ordersTask);
}

// Async enumerable for streaming
public async IAsyncEnumerable<ProcessedData> ProcessDataStreamAsync(
    IAsyncEnumerable<RawData> dataStream)
{
    await foreach (var item in dataStream)
    {
        var processed = await ProcessItemAsync(item);
        yield return processed;
    }
}
```

### Q16: How do you handle exceptions in async code?
**Answer:**
```csharp
public async Task<ApiResponse<T>> SafeApiCallAsync<T>(string endpoint)
{
    try
    {
        using var client = new HttpClient();
        client.Timeout = TimeSpan.FromSeconds(30);
        
        var response = await client.GetStringAsync(endpoint);
        var data = JsonSerializer.Deserialize<T>(response);
        
        return new ApiResponse<T> { Success = true, Data = data };
    }
    catch (HttpRequestException ex)
    {
        return new ApiResponse<T> 
        { 
            Success = false, 
            Error = $"HTTP Error: {ex.Message}" 
        };
    }
    catch (TaskCanceledException ex)
    {
        return new ApiResponse<T> 
        { 
            Success = false, 
            Error = "Request timeout" 
        };
    }
    catch (JsonException ex)
    {
        return new ApiResponse<T> 
        { 
            Success = false, 
            Error = $"JSON parsing error: {ex.Message}" 
        };
    }
}
```

---

## Performance & Memory Management

### Q17: How do you optimize memory usage in data processing?
**Answer:**
```csharp
// Use streaming instead of loading all data
public IEnumerable<ProcessedRecord> ProcessLargeDataset(string filePath)
{
    using var reader = new StreamReader(filePath);
    string line;
    while ((line = reader.ReadLine()) != null)
    {
        var record = ParseRecord(line);
        if (record.IsValid)
        {
            yield return ProcessRecord(record);
        }
    }
    // Memory is released as we go
}

// Use object pooling for frequently created objects
public class RecordProcessor
{
    private readonly ObjectPool<StringBuilder> _stringBuilderPool;
    
    public string ProcessRecord(RawRecord record)
    {
        var sb = _stringBuilderPool.Get();
        try
        {
            sb.Clear();
            sb.Append(record.Field1);
            sb.Append(",");
            sb.Append(record.Field2);
            return sb.ToString();
        }
        finally
        {
            _stringBuilderPool.Return(sb);
        }
    }
}

// Dispose resources properly
public class DataProcessor : IDisposable
{
    private readonly FileStream _fileStream;
    private bool _disposed = false;
    
    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }
    
    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed && disposing)
        {
            _fileStream?.Dispose();
        }
        _disposed = true;
    }
}
```

### Q18: How do you profile and optimize C# applications?
**Answer:**
```csharp
// Use Stopwatch for timing
public class PerformanceProfiler
{
    public async Task<T> MeasureAsync<T>(string operationName, Func<Task<T>> operation)
    {
        var stopwatch = Stopwatch.StartNew();
        try
        {
            var result = await operation();
            stopwatch.Stop();
            Console.WriteLine($"{operationName}: {stopwatch.ElapsedMilliseconds}ms");
            return result;
        }
        catch
        {
            stopwatch.Stop();
            Console.WriteLine($"{operationName} failed after: {stopwatch.ElapsedMilliseconds}ms");
            throw;
        }
    }
}

// Memory usage monitoring
public class MemoryMonitor
{
    public void LogMemoryUsage(string checkpoint)
    {
        var memoryBefore = GC.GetTotalMemory(false);
        GC.Collect();
        GC.WaitForPendingFinalizers();
        var memoryAfter = GC.GetTotalMemory(true);
        
        Console.WriteLine($"{checkpoint}: {memoryAfter / 1024 / 1024} MB");
    }
}

// Use BenchmarkDotNet for detailed profiling
[MemoryDiagnoser]
public class DataProcessingBenchmark
{
    [Benchmark]
    public List<int> ProcessWithLinq() => data.Where(x => x > 0).ToList();
    
    [Benchmark]
    public List<int> ProcessWithLoop()
    {
        var result = new List<int>();
        foreach (var item in data)
            if (item > 0) result.Add(item);
        return result;
    }
}
```

---

## Data Engineering Specific

### Q19: How would you implement a data pipeline in C#?
**Answer:**
```csharp
public class DataPipeline
{
    private readonly IDataExtractor _extractor;
    private readonly IDataTransformer _transformer;
    private readonly IDataLoader _loader;
    private readonly ILogger _logger;
    
    public async Task<PipelineResult> ExecuteAsync(PipelineConfig config)
    {
        var result = new PipelineResult();
        
        try
        {
            // Extract
            _logger.LogInformation("Starting data extraction");
            var rawData = await _extractor.ExtractAsync(config.Source);
            result.RecordsExtracted = rawData.Count();
            
            // Transform
            _logger.LogInformation("Starting data transformation");
            var transformedData = await _transformer.TransformAsync(rawData, config.Rules);
            result.RecordsTransformed = transformedData.Count();
            
            // Load
            _logger.LogInformation("Starting data loading");
            await _loader.LoadAsync(transformedData, config.Destination);
            result.RecordsLoaded = transformedData.Count();
            
            result.Success = true;
            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Pipeline execution failed");
            result.Success = false;
            result.Error = ex.Message;
            return result;
        }
    }
}

// Data validation
public class DataValidator
{
    public ValidationResult ValidateRecord<T>(T record) where T : class
    {
        var context = new ValidationContext(record);
        var results = new List<ValidationResult>();
        
        var isValid = Validator.TryValidateObject(record, context, results, true);
        
        return new ValidationResult
        {
            IsValid = isValid,
            Errors = results.Select(r => r.ErrorMessage).ToList()
        };
    }
}
```

### Q20: How do you implement data quality checks?
**Answer:**
```csharp
public class DataQualityChecker
{
    public DataQualityReport CheckDataQuality<T>(IEnumerable<T> data, 
        DataQualityRules rules) where T : class
    {
        var report = new DataQualityReport();
        var records = data.ToList();
        
        // Completeness check
        report.CompletenessScore = CheckCompleteness(records, rules.RequiredFields);
        
        // Uniqueness check
        report.UniquenessScore = CheckUniqueness(records, rules.UniqueFields);
        
        // Validity check
        report.ValidityScore = CheckValidity(records, rules.ValidationRules);
        
        // Consistency check
        report.ConsistencyScore = CheckConsistency(records, rules.ConsistencyRules);
        
        return report;
    }
    
    private double CheckCompleteness<T>(List<T> records, List<string> requiredFields)
    {
        var totalChecks = records.Count * requiredFields.Count;
        var passedChecks = 0;
        
        foreach (var record in records)
        {
            foreach (var field in requiredFields)
            {
                var property = typeof(T).GetProperty(field);
                var value = property?.GetValue(record);
                
                if (value != null && !string.IsNullOrWhiteSpace(value.ToString()))
                {
                    passedChecks++;
                }
            }
        }
        
        return (double)passedChecks / totalChecks * 100;
    }
}

public class DataQualityReport
{
    public double CompletenessScore { get; set; }
    public double UniquenessScore { get; set; }
    public double ValidityScore { get; set; }
    public double ConsistencyScore { get; set; }
    public List<string> Issues { get; set; } = new List<string>();
    
    public double OverallScore => 
        (CompletenessScore + UniquenessScore + ValidityScore + ConsistencyScore) / 4;
}
```

---

## Advanced Topics

### Q21: How do you implement dependency injection in a data processing application?
**Answer:**
```csharp
// Service registration
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        // Register data services
        services.AddScoped<IDataExtractor, DatabaseExtractor>();
        services.AddScoped<IDataTransformer, JsonTransformer>();
        services.AddScoped<IDataLoader, FileLoader>();
        
        // Register pipeline
        services.AddScoped<DataPipeline>();
        
        // Register configuration
        services.Configure<DatabaseConfig>(Configuration.GetSection("Database"));
        services.Configure<FileConfig>(Configuration.GetSection("Files"));
        
        // Register logging
        services.AddLogging(builder => builder.AddConsole());
    }
}

// Service implementation with DI
public class DatabaseExtractor : IDataExtractor
{
    private readonly IOptions<DatabaseConfig> _config;
    private readonly ILogger<DatabaseExtractor> _logger;
    
    public DatabaseExtractor(IOptions<DatabaseConfig> config, 
        ILogger<DatabaseExtractor> logger)
    {
        _config = config;
        _logger = logger;
    }
    
    public async Task<IEnumerable<RawData>> ExtractAsync(string source)
    {
        _logger.LogInformation($"Extracting data from {source}");
        // Implementation
    }
}
```

### Q22: How do you implement configuration management?
**Answer:**
```csharp
// Configuration classes
public class AppConfig
{
    public DatabaseConfig Database { get; set; }
    public FileConfig Files { get; set; }
    public ProcessingConfig Processing { get; set; }
}

public class DatabaseConfig
{
    public string ConnectionString { get; set; }
    public int CommandTimeout { get; set; } = 30;
    public int MaxRetries { get; set; } = 3;
}

// Configuration usage
public class ConfigurationService
{
    private readonly IConfiguration _configuration;
    private readonly IOptionsMonitor<AppConfig> _appConfig;
    
    public ConfigurationService(IConfiguration configuration, 
        IOptionsMonitor<AppConfig> appConfig)
    {
        _configuration = configuration;
        _appConfig = appConfig;
    }
    
    public T GetSection<T>(string sectionName) where T : class, new()
    {
        var section = _configuration.GetSection(sectionName);
        var config = new T();
        section.Bind(config);
        return config;
    }
}

// appsettings.json
{
  "Database": {
    "ConnectionString": "Server=localhost;Database=DataWarehouse;",
    "CommandTimeout": 60,
    "MaxRetries": 5
  },
  "Files": {
    "InputPath": "C:\\Data\\Input",
    "OutputPath": "C:\\Data\\Output",
    "ArchivePath": "C:\\Data\\Archive"
  },
  "Processing": {
    "BatchSize": 1000,
    "MaxParallelism": 4
  }
}
```

### Q23: How do you implement logging and monitoring?
**Answer:**
```csharp
// Structured logging with Serilog
public class DataProcessor
{
    private readonly ILogger<DataProcessor> _logger;
    
    public async Task ProcessDataAsync(string source, int batchId)
    {
        using var scope = _logger.BeginScope(new Dictionary<string, object>
        {
            ["BatchId"] = batchId,
            ["Source"] = source,
            ["Operation"] = "DataProcessing"
        });
        
        _logger.LogInformation("Starting data processing for batch {BatchId} from {Source}", 
            batchId, source);
        
        try
        {
            var stopwatch = Stopwatch.StartNew();
            var recordCount = await ProcessBatchAsync(source, batchId);
            stopwatch.Stop();
            
            _logger.LogInformation(
                "Completed processing {RecordCount} records in {ElapsedMs}ms for batch {BatchId}",
                recordCount, stopwatch.ElapsedMilliseconds, batchId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to process batch {BatchId} from {Source}", 
                batchId, source);
            throw;
        }
    }
}

// Custom metrics
public class MetricsCollector
{
    private readonly IMetrics _metrics;
    
    public void RecordProcessingTime(string operation, double milliseconds)
    {
        _metrics.Measure.Timer.Time(
            MetricsRegistry.ProcessingTime, 
            TimeSpan.FromMilliseconds(milliseconds),
            new MetricTags("operation", operation));
    }
    
    public void IncrementRecordCount(string source, int count)
    {
        _metrics.Measure.Counter.Increment(
            MetricsRegistry.RecordsProcessed, 
            count,
            new MetricTags("source", source));
    }
}
```

### Q24: How do you handle errors and implement retry logic?
**Answer:**
```csharp
// Retry policy with Polly
public class ResilientDataService
{
    private readonly IAsyncPolicy _retryPolicy;
    private readonly ILogger<ResilientDataService> _logger;
    
    public ResilientDataService(ILogger<ResilientDataService> logger)
    {
        _logger = logger;
        _retryPolicy = Policy
            .Handle<HttpRequestException>()
            .Or<SqlException>()
            .Or<TimeoutException>()
            .WaitAndRetryAsync(
                retryCount: 3,
                sleepDurationProvider: retryAttempt => 
                    TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)), // Exponential backoff
                onRetry: (outcome, timespan, retryCount, context) =>
                {
                    _logger.LogWarning(
                        "Retry {RetryCount} for {Operation} in {Delay}ms. Error: {Error}",
                        retryCount, context.OperationKey, timespan.TotalMilliseconds, 
                        outcome.Exception?.Message);
                });
    }
    
    public async Task<T> ExecuteWithRetryAsync<T>(string operation, Func<Task<T>> action)
    {
        var context = new Context(operation);
        return await _retryPolicy.ExecuteAsync(async (ctx) =>
        {
            _logger.LogDebug("Executing {Operation}", ctx.OperationKey);
            return await action();
        }, context);
    }
}

// Circuit breaker pattern
public class CircuitBreakerService
{
    private readonly IAsyncPolicy _circuitBreakerPolicy;
    
    public CircuitBreakerService()
    {
        _circuitBreakerPolicy = Policy
            .Handle<HttpRequestException>()
            .CircuitBreakerAsync(
                handledEventsAllowedBeforeBreaking: 3,
                durationOfBreak: TimeSpan.FromMinutes(1),
                onBreak: (exception, duration) =>
                {
                    Console.WriteLine($"Circuit breaker opened for {duration}");
                },
                onReset: () =>
                {
                    Console.WriteLine("Circuit breaker reset");
                });
    }
}
```

### Q25: How do you implement unit testing for data processing code?
**Answer:**
```csharp
// Unit test example with xUnit and Moq
public class DataProcessorTests
{
    private readonly Mock<IDataExtractor> _extractorMock;
    private readonly Mock<IDataTransformer> _transformerMock;
    private readonly Mock<IDataLoader> _loaderMock;
    private readonly Mock<ILogger<DataProcessor>> _loggerMock;
    private readonly DataProcessor _processor;
    
    public DataProcessorTests()
    {
        _extractorMock = new Mock<IDataExtractor>();
        _transformerMock = new Mock<IDataTransformer>();
        _loaderMock = new Mock<IDataLoader>();
        _loggerMock = new Mock<ILogger<DataProcessor>>();
        
        _processor = new DataProcessor(
            _extractorMock.Object,
            _transformerMock.Object,
            _loaderMock.Object,
            _loggerMock.Object);
    }
    
    [Fact]
    public async Task ProcessAsync_WithValidData_ShouldReturnSuccess()
    {
        // Arrange
        var rawData = new List<RawRecord> { new RawRecord { Id = 1, Name = "Test" } };
        var transformedData = new List<ProcessedRecord> { new ProcessedRecord { Id = 1, ProcessedName = "TEST" } };
        
        _extractorMock.Setup(x => x.ExtractAsync(It.IsAny<string>()))
            .ReturnsAsync(rawData);
        _transformerMock.Setup(x => x.TransformAsync(It.IsAny<IEnumerable<RawRecord>>()))
            .ReturnsAsync(transformedData);
        _loaderMock.Setup(x => x.LoadAsync(It.IsAny<IEnumerable<ProcessedRecord>>()))
            .Returns(Task.CompletedTask);
        
        // Act
        var result = await _processor.ProcessAsync("test-source");
        
        // Assert
        Assert.True(result.Success);
        Assert.Equal(1, result.RecordsProcessed);
        
        _extractorMock.Verify(x => x.ExtractAsync("test-source"), Times.Once);
        _transformerMock.Verify(x => x.TransformAsync(rawData), Times.Once);
        _loaderMock.Verify(x => x.LoadAsync(transformedData), Times.Once);
    }
    
    [Fact]
    public async Task ProcessAsync_WhenExtractorFails_ShouldReturnFailure()
    {
        // Arrange
        _extractorMock.Setup(x => x.ExtractAsync(It.IsAny<string>()))
            .ThrowsAsync(new InvalidOperationException("Extraction failed"));
        
        // Act
        var result = await _processor.ProcessAsync("test-source");
        
        // Assert
        Assert.False(result.Success);
        Assert.Contains("Extraction failed", result.Error);
    }
}

// Integration test
public class DataPipelineIntegrationTests : IClassFixture<TestDatabaseFixture>
{
    private readonly TestDatabaseFixture _fixture;
    
    public DataPipelineIntegrationTests(TestDatabaseFixture fixture)
    {
        _fixture = fixture;
    }
    
    [Fact]
    public async Task FullPipeline_WithRealDatabase_ShouldProcessCorrectly()
    {
        // Arrange
        var testData = GenerateTestData(100);
        await _fixture.SeedDataAsync(testData);
        
        var pipeline = new DataPipeline(
            new DatabaseExtractor(_fixture.ConnectionString),
            new StandardTransformer(),
            new DatabaseLoader(_fixture.ConnectionString));
        
        // Act
        var result = await pipeline.ExecuteAsync();
        
        // Assert
        Assert.True(result.Success);
        Assert.Equal(100, result.RecordsProcessed);
        
        var processedData = await _fixture.GetProcessedDataAsync();
        Assert.Equal(100, processedData.Count);
    }
}
```

---

## 🎯 Key Takeaways

### **Essential C# Concepts for Data Engineering:**
1. **Strong typing and performance** - Better for large-scale processing
2. **LINQ for data manipulation** - Powerful querying capabilities
3. **Async/await for I/O operations** - Essential for data pipelines
4. **Memory management** - Important for processing large datasets
5. **Dependency injection** - Clean architecture and testability
6. **Error handling and resilience** - Critical for production systems

### **Best Practices:**
- Use streaming for large datasets
- Implement proper error handling and retry logic
- Write comprehensive unit and integration tests
- Use structured logging and monitoring
- Follow SOLID principles and clean architecture
- Optimize for performance and memory usage

### **Common Patterns:**
- Repository pattern for data access
- Pipeline pattern for ETL processes
- Factory pattern for creating data processors
- Observer pattern for monitoring and notifications
- Strategy pattern for different processing algorithms