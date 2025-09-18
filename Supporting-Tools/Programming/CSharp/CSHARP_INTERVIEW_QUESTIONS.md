
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

### Q26: How do you implement custom collections in C#?
**Answer:**
```csharp
// Custom collection implementing IEnumerable<T>
public class CircularBuffer<T> : IEnumerable<T>, ICollection<T>
{
    private readonly T[] _buffer;
    private int _head;
    private int _tail;
    private int _count;
    private readonly int _capacity;
    
    public CircularBuffer(int capacity)
    {
        _capacity = capacity;
        _buffer = new T[capacity];
        _head = 0;
        _tail = 0;
        _count = 0;
    }
    
    public int Count => _count;
    public bool IsReadOnly => false;
    
    public void Add(T item)
    {
        _buffer[_tail] = item;
        _tail = (_tail + 1) % _capacity;
        
        if (_count < _capacity)
        {
            _count++;
        }
        else
        {
            _head = (_head + 1) % _capacity;
        }
    }
    
    public bool Remove(T item)
    {
        // Implementation for removing specific item
        for (int i = 0; i < _count; i++)
        {
            int index = (_head + i) % _capacity;
            if (EqualityComparer<T>.Default.Equals(_buffer[index], item))
            {
                // Shift elements
                for (int j = i; j < _count - 1; j++)
                {
                    int currentIndex = (_head + j) % _capacity;
                    int nextIndex = (_head + j + 1) % _capacity;
                    _buffer[currentIndex] = _buffer[nextIndex];
                }
                _count--;
                _tail = (_tail - 1 + _capacity) % _capacity;
                return true;
            }
        }
        return false;
    }
    
    public IEnumerator<T> GetEnumerator()
    {
        for (int i = 0; i < _count; i++)
        {
            yield return _buffer[(_head + i) % _capacity];
        }
    }
    
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    
    public void Clear()
    {
        _head = 0;
        _tail = 0;
        _count = 0;
        Array.Clear(_buffer, 0, _capacity);
    }
    
    public bool Contains(T item) => this.Any(x => EqualityComparer<T>.Default.Equals(x, item));
    
    public void CopyTo(T[] array, int arrayIndex)
    {
        if (array == null) throw new ArgumentNullException(nameof(array));
        if (arrayIndex < 0 || arrayIndex + _count > array.Length)
            throw new ArgumentException("Invalid array index");
            
        int index = 0;
        foreach (var item in this)
        {
            array[arrayIndex + index++] = item;
        }
    }
}
```

### Q27: How do you implement the Repository pattern with Entity Framework?
**Answer:**
```csharp
// Generic repository interface
public interface IRepository<T> where T : class
{
    Task<T> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate);
    Task AddAsync(T entity);
    Task AddRangeAsync(IEnumerable<T> entities);
    void Update(T entity);
    void Remove(T entity);
    void RemoveRange(IEnumerable<T> entities);
}

// Generic repository implementation
public class Repository<T> : IRepository<T> where T : class
{
    protected readonly DbContext _context;
    protected readonly DbSet<T> _dbSet;
    
    public Repository(DbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }
    
    public virtual async Task<T> GetByIdAsync(int id)
    {
        return await _dbSet.FindAsync(id);
    }
    
    public virtual async Task<IEnumerable<T>> GetAllAsync()
    {
        return await _dbSet.ToListAsync();
    }
    
    public virtual async Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate)
    {
        return await _dbSet.Where(predicate).ToListAsync();
    }
    
    public virtual async Task AddAsync(T entity)
    {
        await _dbSet.AddAsync(entity);
    }
    
    public virtual async Task AddRangeAsync(IEnumerable<T> entities)
    {
        await _dbSet.AddRangeAsync(entities);
    }
    
    public virtual void Update(T entity)
    {
        _dbSet.Update(entity);
    }
    
    public virtual void Remove(T entity)
    {
        _dbSet.Remove(entity);
    }
    
    public virtual void RemoveRange(IEnumerable<T> entities)
    {
        _dbSet.RemoveRange(entities);
    }
}

// Unit of Work pattern
public interface IUnitOfWork : IDisposable
{
    IRepository<Customer> Customers { get; }
    IRepository<Order> Orders { get; }
    Task<int> SaveChangesAsync();
    Task BeginTransactionAsync();
    Task CommitTransactionAsync();
    Task RollbackTransactionAsync();
}

public class UnitOfWork : IUnitOfWork
{
    private readonly ApplicationDbContext _context;
    private IDbContextTransaction _transaction;
    
    public UnitOfWork(ApplicationDbContext context)
    {
        _context = context;
        Customers = new Repository<Customer>(_context);
        Orders = new Repository<Order>(_context);
    }
    
    public IRepository<Customer> Customers { get; }
    public IRepository<Order> Orders { get; }
    
    public async Task<int> SaveChangesAsync()
    {
        return await _context.SaveChangesAsync();
    }
    
    public async Task BeginTransactionAsync()
    {
        _transaction = await _context.Database.BeginTransactionAsync();
    }
    
    public async Task CommitTransactionAsync()
    {
        await _transaction?.CommitAsync();
    }
    
    public async Task RollbackTransactionAsync()
    {
        await _transaction?.RollbackAsync();
    }
    
    public void Dispose()
    {
        _transaction?.Dispose();
        _context?.Dispose();
    }
}
```

### Q28: How do you implement caching strategies in C#?
**Answer:**
```csharp
// Memory caching with IMemoryCache
public class CacheService
{
    private readonly IMemoryCache _cache;
    private readonly ILogger<CacheService> _logger;
    
    public CacheService(IMemoryCache cache, ILogger<CacheService> logger)
    {
        _cache = cache;
        _logger = logger;
    }
    
    public async Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> getItem, TimeSpan? expiry = null)
    {
        if (_cache.TryGetValue(key, out T cachedValue))
        {
            _logger.LogInformation("Cache hit for key: {Key}", key);
            return cachedValue;
        }
        
        _logger.LogInformation("Cache miss for key: {Key}", key);
        var item = await getItem();
        
        var cacheOptions = new MemoryCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = expiry ?? TimeSpan.FromMinutes(30),
            SlidingExpiration = TimeSpan.FromMinutes(5),
            Priority = CacheItemPriority.Normal
        };
        
        _cache.Set(key, item, cacheOptions);
        return item;
    }
    
    public void Remove(string key)
    {
        _cache.Remove(key);
    }
}

// Distributed caching with Redis
public class DistributedCacheService
{
    private readonly IDistributedCache _cache;
    private readonly ILogger<DistributedCacheService> _logger;
    
    public DistributedCacheService(IDistributedCache cache, ILogger<DistributedCacheService> logger)
    {
        _cache = cache;
        _logger = logger;
    }
    
    public async Task<T> GetAsync<T>(string key) where T : class
    {
        var cachedValue = await _cache.GetStringAsync(key);
        if (cachedValue == null)
            return null;
            
        return JsonSerializer.Deserialize<T>(cachedValue);
    }
    
    public async Task SetAsync<T>(string key, T value, TimeSpan? expiry = null) where T : class
    {
        var options = new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = expiry ?? TimeSpan.FromHours(1)
        };
        
        var serializedValue = JsonSerializer.Serialize(value);
        await _cache.SetStringAsync(key, serializedValue, options);
    }
    
    public async Task RemoveAsync(string key)
    {
        await _cache.RemoveAsync(key);
    }
}

// Cache-aside pattern implementation
public class ProductService
{
    private readonly IRepository<Product> _repository;
    private readonly CacheService _cache;
    
    public ProductService(IRepository<Product> repository, CacheService cache)
    {
        _repository = repository;
        _cache = cache;
    }
    
    public async Task<Product> GetProductAsync(int id)
    {
        string cacheKey = $"product_{id}";
        
        return await _cache.GetOrSetAsync(cacheKey, 
            async () => await _repository.GetByIdAsync(id),
            TimeSpan.FromMinutes(15));
    }
    
    public async Task UpdateProductAsync(Product product)
    {
        await _repository.UpdateAsync(product);
        
        // Invalidate cache
        string cacheKey = $"product_{product.Id}";
        _cache.Remove(cacheKey);
    }
}
```

### Q29: How do you implement message queuing in C#?
**Answer:**
```csharp
// Message queue interface
public interface IMessageQueue<T>
{
    Task PublishAsync(T message);
    Task SubscribeAsync(Func<T, Task> handler);
    Task<T> ReceiveAsync(CancellationToken cancellationToken = default);
}

// In-memory message queue implementation
public class InMemoryMessageQueue<T> : IMessageQueue<T>
{
    private readonly Channel<T> _channel;
    private readonly ChannelWriter<T> _writer;
    private readonly ChannelReader<T> _reader;
    
    public InMemoryMessageQueue(int capacity = 1000)
    {
        var options = new BoundedChannelOptions(capacity)
        {
            FullMode = BoundedChannelFullMode.Wait,
            SingleReader = false,
            SingleWriter = false
        };
        
        _channel = Channel.CreateBounded<T>(options);
        _writer = _channel.Writer;
        _reader = _channel.Reader;
    }
    
    public async Task PublishAsync(T message)
    {
        await _writer.WriteAsync(message);
    }
    
    public async Task SubscribeAsync(Func<T, Task> handler)
    {
        await foreach (var message in _reader.ReadAllAsync())
        {
            try
            {
                await handler(message);
            }
            catch (Exception ex)
            {
                // Log error but continue processing
                Console.WriteLine($"Error processing message: {ex.Message}");
            }
        }
    }
    
    public async Task<T> ReceiveAsync(CancellationToken cancellationToken = default)
    {
        return await _reader.ReadAsync(cancellationToken);
    }
}

// RabbitMQ implementation
public class RabbitMQService : IDisposable
{
    private readonly IConnection _connection;
    private readonly IModel _channel;
    private readonly string _queueName;
    
    public RabbitMQService(string connectionString, string queueName)
    {
        var factory = new ConnectionFactory { Uri = new Uri(connectionString) };
        _connection = factory.CreateConnection();
        _channel = _connection.CreateModel();
        _queueName = queueName;
        
        _channel.QueueDeclare(queue: _queueName, durable: true, exclusive: false, autoDelete: false);
    }
    
    public void PublishMessage<T>(T message)
    {
        var json = JsonSerializer.Serialize(message);
        var body = Encoding.UTF8.GetBytes(json);
        
        var properties = _channel.CreateBasicProperties();
        properties.Persistent = true;
        
        _channel.BasicPublish(exchange: "", routingKey: _queueName, basicProperties: properties, body: body);
    }
    
    public void Subscribe<T>(Func<T, Task> handler)
    {
        var consumer = new EventingBasicConsumer(_channel);
        
        consumer.Received += async (model, ea) =>
        {
            try
            {
                var body = ea.Body.ToArray();
                var json = Encoding.UTF8.GetString(body);
                var message = JsonSerializer.Deserialize<T>(json);
                
                await handler(message);
                
                _channel.BasicAck(deliveryTag: ea.DeliveryTag, multiple: false);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error processing message: {ex.Message}");
                _channel.BasicNack(deliveryTag: ea.DeliveryTag, multiple: false, requeue: true);
            }
        };
        
        _channel.BasicConsume(queue: _queueName, autoAck: false, consumer: consumer);
    }
    
    public void Dispose()
    {
        _channel?.Close();
        _connection?.Close();
    }
}

// Message handler with retry logic
public class MessageProcessor<T>
{
    private readonly ILogger<MessageProcessor<T>> _logger;
    private readonly int _maxRetries;
    
    public MessageProcessor(ILogger<MessageProcessor<T>> logger, int maxRetries = 3)
    {
        _logger = logger;
        _maxRetries = maxRetries;
    }
    
    public async Task ProcessWithRetryAsync(T message, Func<T, Task> processor)
    {
        int attempt = 0;
        
        while (attempt < _maxRetries)
        {
            try
            {
                await processor(message);
                return;
            }
            catch (Exception ex)
            {
                attempt++;
                _logger.LogWarning("Processing attempt {Attempt} failed: {Error}", attempt, ex.Message);
                
                if (attempt >= _maxRetries)
                {
                    _logger.LogError("Max retries exceeded for message processing");
                    throw;
                }
                
                // Exponential backoff
                await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, attempt)));
            }
        }
    }
}
```

### Q30: How do you implement background services in C#?
**Answer:**
```csharp
// Background service for data processing
public class DataProcessingService : BackgroundService
{
    private readonly ILogger<DataProcessingService> _logger;
    private readonly IServiceProvider _serviceProvider;
    private readonly IConfiguration _configuration;
    
    public DataProcessingService(
        ILogger<DataProcessingService> logger,
        IServiceProvider serviceProvider,
        IConfiguration configuration)
    {
        _logger = logger;
        _serviceProvider = serviceProvider;
        _configuration = configuration;
    }
    
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var interval = _configuration.GetValue<int>("DataProcessing:IntervalMinutes", 5);
        
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                _logger.LogInformation("Data processing started at: {Time}", DateTimeOffset.Now);
                
                using var scope = _serviceProvider.CreateScope();
                var dataService = scope.ServiceProvider.GetRequiredService<IDataService>();
                
                await ProcessDataAsync(dataService, stoppingToken);
                
                _logger.LogInformation("Data processing completed at: {Time}", DateTimeOffset.Now);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred during data processing");
            }
            
            await Task.Delay(TimeSpan.FromMinutes(interval), stoppingToken);
        }
    }
    
    private async Task ProcessDataAsync(IDataService dataService, CancellationToken cancellationToken)
    {
        var pendingItems = await dataService.GetPendingItemsAsync();
        
        var tasks = pendingItems.Select(async item =>
        {
            try
            {
                await dataService.ProcessItemAsync(item);
                _logger.LogDebug("Processed item: {ItemId}", item.Id);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to process item: {ItemId}", item.Id);
            }
        });
        
        await Task.WhenAll(tasks);
    }
}

// Hosted service with timer
public class TimerHostedService : IHostedService, IDisposable
{
    private readonly ILogger<TimerHostedService> _logger;
    private Timer _timer;
    
    public TimerHostedService(ILogger<TimerHostedService> logger)
    {
        _logger = logger;
    }
    
    public Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Timer Hosted Service running.");
        
        _timer = new Timer(DoWork, null, TimeSpan.Zero, TimeSpan.FromMinutes(1));
        
        return Task.CompletedTask;
    }
    
    private void DoWork(object state)
    {
        _logger.LogInformation("Timer Hosted Service is working. Count: {Count}", DateTime.Now);
        
        // Perform background work
        Task.Run(async () =>
        {
            try
            {
                await PerformBackgroundTaskAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in background task");
            }
        });
    }
    
    private async Task PerformBackgroundTaskAsync()
    {
        // Simulate work
        await Task.Delay(1000);
        _logger.LogInformation("Background task completed");
    }
    
    public Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Timer Hosted Service is stopping.");
        
        _timer?.Change(Timeout.Infinite, 0);
        
        return Task.CompletedTask;
    }
    
    public void Dispose()
    {
        _timer?.Dispose();
    }
}

// Queue-based background service
public class QueuedHostedService : BackgroundService
{
    private readonly ILogger<QueuedHostedService> _logger;
    private readonly IBackgroundTaskQueue _taskQueue;
    
    public QueuedHostedService(
        IBackgroundTaskQueue taskQueue,
        ILogger<QueuedHostedService> logger)
    {
        _taskQueue = taskQueue;
        _logger = logger;
    }
    
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await BackgroundProcessing(stoppingToken);
    }
    
    private async Task BackgroundProcessing(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var workItem = await _taskQueue.DequeueAsync(stoppingToken);
            
            try
            {
                await workItem(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred executing {WorkItem}.", nameof(workItem));
            }
        }
    }
}

public interface IBackgroundTaskQueue
{
    ValueTask QueueBackgroundWorkItemAsync(Func<CancellationToken, ValueTask> workItem);
    ValueTask<Func<CancellationToken, ValueTask>> DequeueAsync(CancellationToken cancellationToken);
}

public class BackgroundTaskQueue : IBackgroundTaskQueue
{
    private readonly Channel<Func<CancellationToken, ValueTask>> _queue;
    
    public BackgroundTaskQueue(int capacity)
    {
        var options = new BoundedChannelOptions(capacity)
        {
            FullMode = BoundedChannelFullMode.Wait
        };
        _queue = Channel.CreateBounded<Func<CancellationToken, ValueTask>>(options);
    }
    
    public async ValueTask QueueBackgroundWorkItemAsync(Func<CancellationToken, ValueTask> workItem)
    {
        if (workItem == null)
            throw new ArgumentNullException(nameof(workItem));
            
        await _queue.Writer.WriteAsync(workItem);
    }
    
    public async ValueTask<Func<CancellationToken, ValueTask>> DequeueAsync(CancellationToken cancellationToken)
    {
        var workItem = await _queue.Reader.ReadAsync(cancellationToken);
        return workItem;
    }
}
```

### Q31: How do you implement custom middleware in ASP.NET Core?
**Answer:**
```csharp
// Custom logging middleware
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;
    
    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();
        var requestId = Guid.NewGuid().ToString();
        
        // Log request
        _logger.LogInformation(
            "Request {RequestId}: {Method} {Path} started",
            requestId, context.Request.Method, context.Request.Path);
        
        // Add request ID to response headers
        context.Response.Headers.Add("X-Request-ID", requestId);
        
        try
        {
            await _next(context);
        }
        finally
        {
            stopwatch.Stop();
            
            _logger.LogInformation(
                "Request {RequestId}: {Method} {Path} completed in {ElapsedMs}ms with status {StatusCode}",
                requestId, context.Request.Method, context.Request.Path, 
                stopwatch.ElapsedMilliseconds, context.Response.StatusCode);
        }
    }
}

// Exception handling middleware
public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;
    
    public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "An unhandled exception occurred");
            await HandleExceptionAsync(context, ex);
        }
    }
    
    private static async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.ContentType = "application/json";
        
        var response = new
        {
            error = new
            {
                message = "An error occurred while processing your request.",
                details = exception.Message,
                timestamp = DateTime.UtcNow
            }
        };
        
        context.Response.StatusCode = exception switch
        {
            ArgumentException => StatusCodes.Status400BadRequest,
            UnauthorizedAccessException => StatusCodes.Status401Unauthorized,
            FileNotFoundException => StatusCodes.Status404NotFound,
            _ => StatusCodes.Status500InternalServerError
        };
        
        var jsonResponse = JsonSerializer.Serialize(response);
        await context.Response.WriteAsync(jsonResponse);
    }
}

// Rate limiting middleware
public class RateLimitingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly IMemoryCache _cache;
    private readonly RateLimitOptions _options;
    
    public RateLimitingMiddleware(RequestDelegate next, IMemoryCache cache, RateLimitOptions options)
    {
        _next = next;
        _cache = cache;
        _options = options;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        var clientId = GetClientIdentifier(context);
        var key = $"rate_limit_{clientId}";
        
        if (_cache.TryGetValue(key, out RateLimitInfo rateLimitInfo))
        {
            if (rateLimitInfo.RequestCount >= _options.MaxRequests)
            {
                context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
                await context.Response.WriteAsync("Rate limit exceeded. Try again later.");
                return;
            }
            
            rateLimitInfo.RequestCount++;
        }
        else
        {
            rateLimitInfo = new RateLimitInfo { RequestCount = 1 };
            _cache.Set(key, rateLimitInfo, _options.TimeWindow);
        }
        
        await _next(context);
    }
    
    private string GetClientIdentifier(HttpContext context)
    {
        // Use IP address or user ID
        return context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
    }
}

public class RateLimitOptions
{
    public int MaxRequests { get; set; } = 100;
    public TimeSpan TimeWindow { get; set; } = TimeSpan.FromMinutes(1);
}

public class RateLimitInfo
{
    public int RequestCount { get; set; }
}

// Middleware registration
public class Startup
{
    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        app.UseMiddleware<ExceptionHandlingMiddleware>();
        app.UseMiddleware<RequestLoggingMiddleware>();
        app.UseMiddleware<RateLimitingMiddleware>(new RateLimitOptions
        {
            MaxRequests = 100,
            TimeWindow = TimeSpan.FromMinutes(1)
        });
        
        // Other middleware...
    }
}
```

### Q32: How do you implement custom attributes and reflection?
**Answer:**
```csharp
// Custom validation attribute
[AttributeUsage(AttributeTargets.Property)]
public class EmailValidationAttribute : ValidationAttribute
{
    private readonly string _pattern = @"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$";
    
    public override bool IsValid(object value)
    {
        if (value == null) return true; // Let Required attribute handle null
        
        if (value is string email)
        {
            return Regex.IsMatch(email, _pattern);
        }
        
        return false;
    }
    
    public override string FormatErrorMessage(string name)
    {
        return $"The {name} field must be a valid email address.";
    }
}

// Custom caching attribute
[AttributeUsage(AttributeTargets.Method)]
public class CacheAttribute : Attribute
{
    public int DurationMinutes { get; set; } = 5;
    public string KeyPrefix { get; set; }
    
    public CacheAttribute(int durationMinutes = 5, string keyPrefix = null)
    {
        DurationMinutes = durationMinutes;
        KeyPrefix = keyPrefix;
    }
}

// Interceptor using Castle DynamicProxy
public class CacheInterceptor : IInterceptor
{
    private readonly IMemoryCache _cache;
    private readonly ILogger<CacheInterceptor> _logger;
    
    public CacheInterceptor(IMemoryCache cache, ILogger<CacheInterceptor> logger)
    {
        _cache = cache;
        _logger = logger;
    }
    
    public void Intercept(IInvocation invocation)
    {
        var cacheAttribute = invocation.Method.GetCustomAttribute<CacheAttribute>();
        if (cacheAttribute == null)
        {
            invocation.Proceed();
            return;
        }
        
        var cacheKey = GenerateCacheKey(invocation, cacheAttribute.KeyPrefix);
        
        if (_cache.TryGetValue(cacheKey, out var cachedResult))
        {
            _logger.LogDebug("Cache hit for key: {CacheKey}", cacheKey);
            invocation.ReturnValue = cachedResult;
            return;
        }
        
        invocation.Proceed();
        
        if (invocation.ReturnValue != null)
        {
            var cacheOptions = new MemoryCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(cacheAttribute.DurationMinutes)
            };
            
            _cache.Set(cacheKey, invocation.ReturnValue, cacheOptions);
            _logger.LogDebug("Cached result for key: {CacheKey}", cacheKey);
        }
    }
    
    private string GenerateCacheKey(IInvocation invocation, string keyPrefix)
    {
        var methodName = invocation.Method.Name;
        var parameters = string.Join("_", invocation.Arguments.Select(arg => arg?.ToString() ?? "null"));
        
        return $"{keyPrefix ?? methodName}_{parameters}";
    }
}

// Reflection utilities
public static class ReflectionHelper
{
    public static T CreateInstance<T>(params object[] args) where T : class
    {
        var type = typeof(T);
        var constructors = type.GetConstructors();
        
        foreach (var constructor in constructors)
        {
            var parameters = constructor.GetParameters();
            if (parameters.Length == args.Length)
            {
                try
                {
                    return (T)Activator.CreateInstance(type, args);
                }
                catch
                {
                    continue;
                }
            }
        }
        
        throw new InvalidOperationException($"No suitable constructor found for type {type.Name}");
    }
    
    public static void CopyProperties<T>(T source, T destination) where T : class
    {
        var properties = typeof(T).GetProperties(BindingFlags.Public | BindingFlags.Instance)
            .Where(p => p.CanRead && p.CanWrite);
            
        foreach (var property in properties)
        {
            var value = property.GetValue(source);
            property.SetValue(destination, value);
        }
    }
    
    public static Dictionary<string, object> GetPropertyValues<T>(T obj) where T : class
    {
        var result = new Dictionary<string, object>();
        var properties = typeof(T).GetProperties(BindingFlags.Public | BindingFlags.Instance)
            .Where(p => p.CanRead);
            
        foreach (var property in properties)
        {
            result[property.Name] = property.GetValue(obj);
        }
        
        return result;
    }
    
    public static void SetPropertyValues<T>(T obj, Dictionary<string, object> values) where T : class
    {
        var properties = typeof(T).GetProperties(BindingFlags.Public | BindingFlags.Instance)
            .Where(p => p.CanWrite)
            .ToDictionary(p => p.Name, p => p);
            
        foreach (var kvp in values)
        {
            if (properties.TryGetValue(kvp.Key, out var property))
            {
                var convertedValue = Convert.ChangeType(kvp.Value, property.PropertyType);
                property.SetValue(obj, convertedValue);
            }
        }
    }
    
    public static IEnumerable<T> GetAttributesFromAssembly<T>(Assembly assembly) where T : Attribute
    {
        return assembly.GetTypes()
            .SelectMany(type => type.GetCustomAttributes<T>())
            .Concat(assembly.GetTypes()
                .SelectMany(type => type.GetMethods())
                .SelectMany(method => method.GetCustomAttributes<T>()))
            .Concat(assembly.GetTypes()
                .SelectMany(type => type.GetProperties())
                .SelectMany(property => property.GetCustomAttributes<T>()));
    }
}

// Usage example
public class UserService
{
    [Cache(DurationMinutes = 10, KeyPrefix = "user")]
    public virtual async Task<User> GetUserByIdAsync(int id)
    {
        // Simulate database call
        await Task.Delay(100);
        return new User { Id = id, Name = $"User {id}" };
    }
}

public class User
{
    public int Id { get; set; }
    
    [Required]
    public string Name { get; set; }
    
    [EmailValidation]
    public string Email { get; set; }
}
```

### Q33: How do you implement custom serialization in C#?
**Answer:**
```csharp
// Custom JSON converter
public class DateTimeConverter : JsonConverter<DateTime>
{
    private readonly string _format;
    
    public DateTimeConverter(string format = "yyyy-MM-dd HH:mm:ss")
    {
        _format = format;
    }
    
    public override DateTime Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        var value = reader.GetString();
        if (DateTime.TryParseExact(value, _format, CultureInfo.InvariantCulture, DateTimeStyles.None, out var result))
        {
            return result;
        }
        throw new JsonException($"Unable to parse '{value}' as DateTime with format '{_format}'");
    }
    
    public override void Write(Utf8JsonWriter writer, DateTime value, JsonSerializerOptions options)
    {
        writer.WriteStringValue(value.ToString(_format));
    }
}

// Custom binary serialization
[Serializable]
public class CustomSerializableClass : ISerializable
{
    public int Id { get; set; }
    public string Name { get; set; }
    public DateTime CreatedDate { get; set; }
    public List<string> Tags { get; set; }
    
    public CustomSerializableClass() { }
    
    // Deserialization constructor
    protected CustomSerializableClass(SerializationInfo info, StreamingContext context)
    {
        Id = info.GetInt32(nameof(Id));
        Name = info.GetString(nameof(Name));
        CreatedDate = info.GetDateTime(nameof(CreatedDate));
        Tags = (List<string>)info.GetValue(nameof(Tags), typeof(List<string>));
    }
    
    // Serialization method
    public void GetObjectData(SerializationInfo info, StreamingContext context)
    {
        info.AddValue(nameof(Id), Id);
        info.AddValue(nameof(Name), Name);
        info.AddValue(nameof(CreatedDate), CreatedDate);
        info.AddValue(nameof(Tags), Tags);
    }
}

// Protocol Buffers serialization
[ProtoContract]
public class ProtobufMessage
{
    [ProtoMember(1)]
    public int Id { get; set; }
    
    [ProtoMember(2)]
    public string Content { get; set; }
    
    [ProtoMember(3)]
    public DateTime Timestamp { get; set; }
    
    [ProtoMember(4)]
    public List<string> Metadata { get; set; }
}

// Custom serialization service
public interface ISerializationService
{
    byte[] Serialize<T>(T obj);
    T Deserialize<T>(byte[] data);
    string SerializeToJson<T>(T obj);
    T DeserializeFromJson<T>(string json);
}

public class SerializationService : ISerializationService
{
    private readonly JsonSerializerOptions _jsonOptions;
    
    public SerializationService()
    {
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            WriteIndented = true,
            Converters = { new DateTimeConverter() }
        };
    }
    
    public byte[] Serialize<T>(T obj)
    {
        using var stream = new MemoryStream();
        using var writer = new BinaryWriter(stream);
        
        var json = JsonSerializer.Serialize(obj, _jsonOptions);
        writer.Write(json);
        
        return stream.ToArray();
    }
    
    public T Deserialize<T>(byte[] data)
    {
        using var stream = new MemoryStream(data);
        using var reader = new BinaryReader(stream);
        
        var json = reader.ReadString();
        return JsonSerializer.Deserialize<T>(json, _jsonOptions);
    }
    
    public string SerializeToJson<T>(T obj)
    {
        return JsonSerializer.Serialize(obj, _jsonOptions);
    }
    
    public T DeserializeFromJson<T>(string json)
    {
        return JsonSerializer.Deserialize<T>(json, _jsonOptions);
    }
    
    // Protobuf serialization
    public byte[] SerializeProtobuf<T>(T obj) where T : class
    {
        using var stream = new MemoryStream();
        Serializer.Serialize(stream, obj);
        return stream.ToArray();
    }
    
    public T DeserializeProtobuf<T>(byte[] data) where T : class
    {
        using var stream = new MemoryStream(data);
        return Serializer.Deserialize<T>(stream);
    }
}

// MessagePack serialization
public class MessagePackService
{
    private readonly MessagePackSerializerOptions _options;
    
    public MessagePackService()
    {
        _options = MessagePackSerializerOptions.Standard
            .WithResolver(ContractlessStandardResolver.Instance);
    }
    
    public byte[] Serialize<T>(T obj)
    {
        return MessagePackSerializer.Serialize(obj, _options);
    }
    
    public T Deserialize<T>(byte[] data)
    {
        return MessagePackSerializer.Deserialize<T>(data, _options);
    }
    
    public async Task<byte[]> SerializeAsync<T>(T obj)
    {
        using var stream = new MemoryStream();
        await MessagePackSerializer.SerializeAsync(stream, obj, _options);
        return stream.ToArray();
    }
    
    public async Task<T> DeserializeAsync<T>(Stream stream)
    {
        return await MessagePackSerializer.DeserializeAsync<T>(stream, _options);
    }
}
```

### Q34: How do you implement custom configuration providers?
**Answer:**
```csharp
// Custom configuration provider for database
public class DatabaseConfigurationProvider : ConfigurationProvider
{
    private readonly string _connectionString;
    private readonly string _tableName;
    
    public DatabaseConfigurationProvider(string connectionString, string tableName)
    {
        _connectionString = connectionString;
        _tableName = tableName;
    }
    
    public override void Load()
    {
        Data = LoadFromDatabase();
    }
    
    private Dictionary<string, string> LoadFromDatabase()
    {
        var data = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        
        using var connection = new SqlConnection(_connectionString);
        connection.Open();
        
        var command = new SqlCommand($"SELECT [Key], [Value] FROM {_tableName}", connection);
        using var reader = command.ExecuteReader();
        
        while (reader.Read())
        {
            var key = reader.GetString("Key");
            var value = reader.GetString("Value");
            data[key] = value;
        }
        
        return data;
    }
}

public class DatabaseConfigurationSource : IConfigurationSource
{
    private readonly string _connectionString;
    private readonly string _tableName;
    
    public DatabaseConfigurationSource(string connectionString, string tableName)
    {
        _connectionString = connectionString;
        _tableName = tableName;
    }
    
    public IConfigurationProvider Build(IConfigurationBuilder builder)
    {
        return new DatabaseConfigurationProvider(_connectionString, _tableName);
    }
}

// Extension method for easy registration
public static class DatabaseConfigurationExtensions
{
    public static IConfigurationBuilder AddDatabase(this IConfigurationBuilder builder,
        string connectionString, string tableName)
    {
        return builder.Add(new DatabaseConfigurationSource(connectionString, tableName));
    }
}

// Custom configuration for Azure Key Vault
public class KeyVaultConfigurationProvider : ConfigurationProvider
{
    private readonly SecretClient _secretClient;
    private readonly string _prefix;
    
    public KeyVaultConfigurationProvider(SecretClient secretClient, string prefix = null)
    {
        _secretClient = secretClient;
        _prefix = prefix;
    }
    
    public override void Load()
    {
        Data = LoadFromKeyVault();
    }
    
    private Dictionary<string, string> LoadFromKeyVault()
    {
        var data = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        
        try
        {
            var secrets = _secretClient.GetPropertiesOfSecrets();
            
            foreach (var secretProperties in secrets)
            {
                if (!string.IsNullOrEmpty(_prefix) && !secretProperties.Name.StartsWith(_prefix))
                    continue;
                    
                try
                {
                    var secret = _secretClient.GetSecret(secretProperties.Name);
                    var key = string.IsNullOrEmpty(_prefix) 
                        ? secretProperties.Name 
                        : secretProperties.Name.Substring(_prefix.Length);
                        
                    data[key.Replace("--", ConfigurationPath.KeyDelimiter)] = secret.Value.Value;
                }
                catch (Exception ex)
                {
                    // Log error but continue loading other secrets
                    Console.WriteLine($"Failed to load secret {secretProperties.Name}: {ex.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Failed to load secrets from Key Vault: {ex.Message}");
        }
        
        return data;
    }
}

// Strongly typed configuration
public class AppSettings
{
    public DatabaseSettings Database { get; set; }
    public CacheSettings Cache { get; set; }
    public LoggingSettings Logging { get; set; }
}

public class DatabaseSettings
{
    public string ConnectionString { get; set; }
    public int CommandTimeout { get; set; } = 30;
    public int MaxRetryCount { get; set; } = 3;
    public bool EnableSensitiveDataLogging { get; set; } = false;
}

public class CacheSettings
{
    public bool Enabled { get; set; } = true;
    public int DefaultExpirationMinutes { get; set; } = 30;
    public string RedisConnectionString { get; set; }
}

public class LoggingSettings
{
    public string LogLevel { get; set; } = "Information";
    public bool EnableConsoleLogging { get; set; } = true;
    public bool EnableFileLogging { get; set; } = false;
    public string LogFilePath { get; set; }
}

// Configuration validation
public class AppSettingsValidator : IValidateOptions<AppSettings>
{
    public ValidateOptionsResult Validate(string name, AppSettings options)
    {
        var errors = new List<string>();
        
        if (string.IsNullOrEmpty(options.Database?.ConnectionString))
        {
            errors.Add("Database connection string is required");
        }
        
        if (options.Database?.CommandTimeout <= 0)
        {
            errors.Add("Database command timeout must be greater than 0");
        }
        
        if (options.Cache?.Enabled == true && string.IsNullOrEmpty(options.Cache.RedisConnectionString))
        {
            errors.Add("Redis connection string is required when caching is enabled");
        }
        
        if (errors.Any())
        {
            return ValidateOptionsResult.Fail(errors);
        }
        
        return ValidateOptionsResult.Success;
    }
}

// Usage in Startup
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        // Add custom configuration providers
        var configuration = new ConfigurationBuilder()
            .AddJsonFile("appsettings.json")
            .AddDatabase(connectionString, "Configuration")
            .AddEnvironmentVariables()
            .Build();
        
        // Configure strongly typed settings
        services.Configure<AppSettings>(configuration);
        services.AddSingleton<IValidateOptions<AppSettings>, AppSettingsValidator>();
        
        // Register configuration as singleton
        services.AddSingleton<IConfiguration>(configuration);
    }
}
```

### Q35: How do you implement custom health checks?
**Answer:**
```csharp
// Custom health check for database
public class DatabaseHealthCheck : IHealthCheck
{
    private readonly string _connectionString;
    private readonly ILogger<DatabaseHealthCheck> _logger;
    
    public DatabaseHealthCheck(string connectionString, ILogger<DatabaseHealthCheck> logger)
    {
        _connectionString = connectionString;
        _logger = logger;
    }
    
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, 
        CancellationToken cancellationToken = default)
    {
        try
        {
            using var connection = new SqlConnection(_connectionString);
            await connection.OpenAsync(cancellationToken);
            
            var command = new SqlCommand("SELECT 1", connection);
            var result = await command.ExecuteScalarAsync(cancellationToken);
            
            if (result?.ToString() == "1")
            {
                return HealthCheckResult.Healthy("Database is accessible");
            }
            
            return HealthCheckResult.Unhealthy("Database query returned unexpected result");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Database health check failed");
            return HealthCheckResult.Unhealthy($"Database is not accessible: {ex.Message}");
        }
    }
}

// Custom health check for external API
public class ApiHealthCheck : IHealthCheck
{
    private readonly HttpClient _httpClient;
    private readonly string _apiUrl;
    private readonly ILogger<ApiHealthCheck> _logger;
    
    public ApiHealthCheck(HttpClient httpClient, string apiUrl, ILogger<ApiHealthCheck> logger)
    {
        _httpClient = httpClient;
        _apiUrl = apiUrl;
        _logger = logger;
    }
    
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, 
        CancellationToken cancellationToken = default)
    {
        try
        {
            var stopwatch = Stopwatch.StartNew();
            var response = await _httpClient.GetAsync(_apiUrl, cancellationToken);
            stopwatch.Stop();
            
            var data = new Dictionary<string, object>
            {
                ["url"] = _apiUrl,
                ["status_code"] = (int)response.StatusCode,
                ["response_time_ms"] = stopwatch.ElapsedMilliseconds
            };
            
            if (response.IsSuccessStatusCode)
            {
                if (stopwatch.ElapsedMilliseconds > 5000) // 5 seconds
                {
                    return HealthCheckResult.Degraded(
                        $"API is responding but slowly ({stopwatch.ElapsedMilliseconds}ms)", 
                        data: data);
                }
                
                return HealthCheckResult.Healthy(
                    $"API is responding normally ({stopwatch.ElapsedMilliseconds}ms)", 
                    data: data);
            }
            
            return HealthCheckResult.Unhealthy(
                $"API returned status code {response.StatusCode}", 
                data: data);
        }
        catch (TaskCanceledException)
        {
            return HealthCheckResult.Unhealthy("API health check timed out");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "API health check failed");
            return HealthCheckResult.Unhealthy($"API is not accessible: {ex.Message}");
        }
    }
}

// Custom health check for external API
public class ApiHealthCheck : IHealthCheck
{
    private readonly HttpClient _httpClient;
    private readonly string _apiUrl;
    private readonly ILogger<ApiHealthCheck> _logger;
    
    public ApiHealthCheck(HttpClient httpClient, string apiUrl, ILogger<ApiHealthCheck> logger)
    {
        _httpClient = httpClient;
        _apiUrl = apiUrl;
        _logger = logger;
    }
    
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, 
        CancellationToken cancellationToken = default)
    {
        try
        {
            var stopwatch = Stopwatch.StartNew();
            var response = await _httpClient.GetAsync(_apiUrl, cancellationToken);
            stopwatch.Stop();
            
            var data = new Dictionary<string, object>
            {
                ["url"] = _apiUrl,
                ["status_code"] = (int)response.StatusCode,
                ["response_time_ms"] = stopwatch.ElapsedMilliseconds
            };
            
            if (response.IsSuccessStatusCode)
            {
                if (stopwatch.ElapsedMilliseconds > 5000) // 5 seconds
                {
                    return HealthCheckResult.Degraded(
                        $"API is responding but slowly ({stopwatch.ElapsedMilliseconds}ms)", 
                        data: data);
                }
                
                return HealthCheckResult.Healthy(
                    $"API is responding normally ({stopwatch.ElapsedMilliseconds}ms)", 
                    data: data);
            }
            
            return HealthCheckResult.Unhealthy(
                $"API returned status code {response.StatusCode}", 
                data: data);
        }
        catch (TaskCanceledException)
        {
            return HealthCheckResult.Unhealthy("API health check timed out");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "API health check failed");
            return HealthCheckResult.Unhealthy($"API is not accessible: {ex.Message}");
        }
    }
}

// Memory usage health check
public class MemoryHealthCheck : IHealthCheck
{
    private readonly long _thresholdBytes;
    
    public MemoryHealthCheck(long thresholdBytes = 1024 * 1024 * 1024) // 1GB default
    {
        _thresholdBytes = thresholdBytes;
    }
    
    public Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, 
        CancellationToken cancellationToken = default)
    {
        var allocated = GC.GetTotalMemory(false);
        var data = new Dictionary<string, object>
        {
            ["allocated_bytes"] = allocated,
            ["allocated_mb"] = allocated / 1024 / 1024,
            ["threshold_bytes"] = _thresholdBytes,
            ["threshold_mb"] = _thresholdBytes / 1024 / 1024
        };
        
        if (allocated >= _thresholdBytes)
        {
            return Task.FromResult(HealthCheckResult.Unhealthy(
                $"Memory usage is high: {allocated / 1024 / 1024} MB", 
                data: data));
        }
        
        if (allocated >= _thresholdBytes * 0.8) // 80% of threshold
        {
            return Task.FromResult(HealthCheckResult.Degraded(
                $"Memory usage is elevated: {allocated / 1024 / 1024} MB", 
                data: data));
        }
        
        return Task.FromResult(HealthCheckResult.Healthy(
            $"Memory usage is normal: {allocated / 1024 / 1024} MB", 
            data: data));
    }
}

// Composite health check
public class CompositeHealthCheck : IHealthCheck
{
    private readonly IEnumerable<IHealthCheck> _healthChecks;
    private readonly ILogger<CompositeHealthCheck> _logger;
    
    public CompositeHealthCheck(IEnumerable<IHealthCheck> healthChecks, ILogger<CompositeHealthCheck> logger)
    {
        _healthChecks = healthChecks;
        _logger = logger;
    }
    
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, 
        CancellationToken cancellationToken = default)
    {
        var results = new List<HealthCheckResult>();
        var data = new Dictionary<string, object>();
        
        foreach (var healthCheck in _healthChecks)
        {
            try
            {
                var result = await healthCheck.CheckHealthAsync(context, cancellationToken);
                results.Add(result);
                
                var checkName = healthCheck.GetType().Name;
                data[checkName] = new
                {
                    status = result.Status.ToString(),
                    description = result.Description,
                    data = result.Data
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Health check {HealthCheck} failed", healthCheck.GetType().Name);
                results.Add(HealthCheckResult.Unhealthy($"Health check failed: {ex.Message}"));
            }
        }
        
        var overallStatus = results.Any(r => r.Status == HealthStatus.Unhealthy)
            ? HealthStatus.Unhealthy
            : results.Any(r => r.Status == HealthStatus.Degraded)
                ? HealthStatus.Degraded
                : HealthStatus.Healthy;
        
        var description = $"Composite health check: {results.Count(r => r.Status == HealthStatus.Healthy)} healthy, " +
                         $"{results.Count(r => r.Status == HealthStatus.Degraded)} degraded, " +
                         $"{results.Count(r => r.Status == HealthStatus.Unhealthy)} unhealthy";
        
        return new HealthCheckResult(overallStatus, description, data: data);
    }
}

// Health check registration and configuration
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddHealthChecks()
            .AddCheck<DatabaseHealthCheck>("database")
            .AddCheck<MemoryHealthCheck>("memory")
            .AddCheck<ApiHealthCheck>("external_api")
            .AddCheck("disk_space", () =>
            {
                var drive = new DriveInfo("C:");
                var freeSpaceGB = drive.AvailableFreeSpace / 1024 / 1024 / 1024;
                
                return freeSpaceGB > 10
                    ? HealthCheckResult.Healthy($"Disk space: {freeSpaceGB} GB available")
                    : HealthCheckResult.Unhealthy($"Low disk space: {freeSpaceGB} GB available");
            });
    }
    
    public void Configure(IApplicationBuilder app)
    {
        app.UseHealthChecks("/health", new HealthCheckOptions
        {
            ResponseWriter = async (context, report) =>
            {
                context.Response.ContentType = "application/json";
                
                var response = new
                {
                    status = report.Status.ToString(),
                    duration = report.TotalDuration.TotalMilliseconds,
                    checks = report.Entries.Select(entry => new
                    {
                        name = entry.Key,
                        status = entry.Value.Status.ToString(),
                        description = entry.Value.Description,
                        duration = entry.Value.Duration.TotalMilliseconds,
                        data = entry.Value.Data
                    })
                };
                
                await context.Response.WriteAsync(JsonSerializer.Serialize(response));
            }
        });
        
        // Separate endpoint for readiness checks
        app.UseHealthChecks("/ready", new HealthCheckOptions
        {
            Predicate = check => check.Tags.Contains("ready")
        });
        
        // Separate endpoint for liveness checks
        app.UseHealthChecks("/live", new HealthCheckOptions
        {
            Predicate = check => check.Tags.Contains("live")
        });
    }
}
```

### Q36: How do you implement real-time data processing with SignalR?
**Answer:**
```csharp
// SignalR Hub for real-time data streaming
public class DataStreamingHub : Hub
{
    private readonly IDataStreamService _dataStreamService;
    private readonly ILogger<DataStreamingHub> _logger;
    
    public DataStreamingHub(IDataStreamService dataStreamService, ILogger<DataStreamingHub> logger)
    {
        _dataStreamService = dataStreamService;
        _logger = logger;
    }
    
    public async Task JoinDataStream(string streamName)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, streamName);
        _logger.LogInformation("Client {ConnectionId} joined stream {StreamName}", 
            Context.ConnectionId, streamName);
    }
    
    public async Task LeaveDataStream(string streamName)
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, streamName);
        _logger.LogInformation("Client {ConnectionId} left stream {StreamName}", 
            Context.ConnectionId, streamName);
    }
    
    public async Task<IEnumerable<DataPoint>> GetHistoricalData(string streamName, DateTime from, DateTime to)
    {
        return await _dataStreamService.GetHistoricalDataAsync(streamName, from, to);
    }
}

// Real-time data streaming service
public class RealTimeDataProcessor : BackgroundService
{
    private readonly IHubContext<DataStreamingHub> _hubContext;
    private readonly IDataSource _dataSource;
    private readonly ILogger<RealTimeDataProcessor> _logger;
    
    public RealTimeDataProcessor(
        IHubContext<DataStreamingHub> hubContext,
        IDataSource dataSource,
        ILogger<RealTimeDataProcessor> logger)
    {
        _hubContext = hubContext;
        _dataSource = dataSource;
        _logger = logger;
    }
    
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var dataPoint in _dataSource.GetDataStreamAsync(stoppingToken))
        {
            try
            {
                // Process data point
                var processedData = ProcessDataPoint(dataPoint);
                
                // Send to all clients in the stream group
                await _hubContext.Clients.Group(dataPoint.StreamName)
                    .SendAsync("DataUpdate", processedData, stoppingToken);
                
                // Send alerts if thresholds are exceeded
                if (processedData.Value > processedData.AlertThreshold)
                {
                    await _hubContext.Clients.Group($"{dataPoint.StreamName}_alerts")
                        .SendAsync("Alert", new { 
                            Message = $"Threshold exceeded: {processedData.Value}",
                            Severity = "High",
                            Timestamp = DateTime.UtcNow
                        }, stoppingToken);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing data point: {DataPoint}", dataPoint);
            }
        }
    }
    
    private ProcessedDataPoint ProcessDataPoint(RawDataPoint dataPoint)
    {
        // Apply transformations, aggregations, etc.
        return new ProcessedDataPoint
        {
            StreamName = dataPoint.StreamName,
            Timestamp = dataPoint.Timestamp,
            Value = dataPoint.Value * 1.1, // Example transformation
            MovingAverage = CalculateMovingAverage(dataPoint),
            AlertThreshold = 100.0
        };
    }
}
```

### Q37: How do you implement distributed caching with Redis?
**Answer:**
```csharp
// Redis distributed cache implementation
public class RedisDistributedCache : IDistributedCacheService
{
    private readonly IDatabase _database;
    private readonly ILogger<RedisDistributedCache> _logger;
    private readonly JsonSerializerOptions _jsonOptions;
    
    public RedisDistributedCache(IConnectionMultiplexer redis, ILogger<RedisDistributedCache> logger)
    {
        _database = redis.GetDatabase();
        _logger = logger;
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };
    }
    
    public async Task<T> GetAsync<T>(string key) where T : class
    {
        try
        {
            var value = await _database.StringGetAsync(key);
            if (!value.HasValue)
                return null;
                
            return JsonSerializer.Deserialize<T>(value, _jsonOptions);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting cache key: {Key}", key);
            return null;
        }
    }
    
    public async Task SetAsync<T>(string key, T value, TimeSpan? expiry = null) where T : class
    {
        try
        {
            var serializedValue = JsonSerializer.Serialize(value, _jsonOptions);
            await _database.StringSetAsync(key, serializedValue, expiry);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error setting cache key: {Key}", key);
        }
    }
    
    public async Task<bool> ExistsAsync(string key)
    {
        return await _database.KeyExistsAsync(key);
    }
    
    public async Task RemoveAsync(string key)
    {
        await _database.KeyDeleteAsync(key);
    }
    
    public async Task RemoveByPatternAsync(string pattern)
    {
        var server = _database.Multiplexer.GetServer(_database.Multiplexer.GetEndPoints().First());
        var keys = server.Keys(pattern: pattern);
        
        foreach (var key in keys)
        {
            await _database.KeyDeleteAsync(key);
        }
    }
    
    // Cache-aside pattern implementation
    public async Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> factory, TimeSpan? expiry = null) where T : class
    {
        var cached = await GetAsync<T>(key);
        if (cached != null)
            return cached;
            
        var value = await factory();
        if (value != null)
        {
            await SetAsync(key, value, expiry);
        }
        
        return value;
    }
    
    // Distributed locking
    public async Task<IDisposable> AcquireLockAsync(string lockKey, TimeSpan expiry, TimeSpan timeout)
    {
        var lockValue = Guid.NewGuid().ToString();
        var endTime = DateTime.UtcNow.Add(timeout);
        
        while (DateTime.UtcNow < endTime)
        {
            if (await _database.StringSetAsync(lockKey, lockValue, expiry, When.NotExists))
            {
                return new RedisLock(_database, lockKey, lockValue);
            }
            
            await Task.Delay(100);
        }
        
        throw new TimeoutException($"Could not acquire lock for key: {lockKey}");
    }
}

public class RedisLock : IDisposable
{
    private readonly IDatabase _database;
    private readonly string _key;
    private readonly string _value;
    private bool _disposed;
    
    public RedisLock(IDatabase database, string key, string value)
    {
        _database = database;
        _key = key;
        _value = value;
    }
    
    public void Dispose()
    {
        if (!_disposed)
        {
            // Lua script to ensure we only delete our lock
            const string script = @"
                if redis.call('GET', KEYS[1]) == ARGV[1] then
                    return redis.call('DEL', KEYS[1])
                else
                    return 0
                end";
                
            _database.ScriptEvaluate(script, new RedisKey[] { _key }, new RedisValue[] { _value });
            _disposed = true;
        }
    }
}
```

### Q38: How do you implement event sourcing in C#?
**Answer:**
```csharp
// Event sourcing implementation
public abstract class Event
{
    public Guid Id { get; } = Guid.NewGuid();
    public DateTime Timestamp { get; } = DateTime.UtcNow;
    public string EventType => GetType().Name;
}

public abstract class AggregateRoot
{
    private readonly List<Event> _uncommittedEvents = new List<Event>();
    
    public Guid Id { get; protected set; }
    public int Version { get; private set; }
    
    protected void RaiseEvent(Event @event)
    {
        ApplyEvent(@event);
        _uncommittedEvents.Add(@event);
    }
    
    public void LoadFromHistory(IEnumerable<Event> events)
    {
        foreach (var @event in events)
        {
            ApplyEvent(@event);
            Version++;
        }
    }
    
    public IEnumerable<Event> GetUncommittedEvents()
    {
        return _uncommittedEvents.AsReadOnly();
    }
    
    public void MarkEventsAsCommitted()
    {
        _uncommittedEvents.Clear();
    }
    
    protected abstract void ApplyEvent(Event @event);
}

// Example aggregate
public class CustomerAccount : AggregateRoot
{
    public string CustomerName { get; private set; }
    public decimal Balance { get; private set; }
    public bool IsActive { get; private set; }
    
    public CustomerAccount() { }
    
    public CustomerAccount(Guid id, string customerName, decimal initialBalance)
    {
        RaiseEvent(new AccountCreatedEvent(id, customerName, initialBalance));
    }
    
    public void Deposit(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Deposit amount must be positive");
            
        RaiseEvent(new MoneyDepositedEvent(Id, amount));
    }
    
    public void Withdraw(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Withdrawal amount must be positive");
            
        if (Balance < amount)
            throw new InvalidOperationException("Insufficient funds");
            
        RaiseEvent(new MoneyWithdrawnEvent(Id, amount));
    }
    
    public void Deactivate()
    {
        if (!IsActive)
            throw new InvalidOperationException("Account is already inactive");
            
        RaiseEvent(new AccountDeactivatedEvent(Id));
    }
    
    protected override void ApplyEvent(Event @event)
    {
        switch (@event)
        {
            case AccountCreatedEvent e:
                Id = e.AccountId;
                CustomerName = e.CustomerName;
                Balance = e.InitialBalance;
                IsActive = true;
                break;
                
            case MoneyDepositedEvent e:
                Balance += e.Amount;
                break;
                
            case MoneyWithdrawnEvent e:
                Balance -= e.Amount;
                break;
                
            case AccountDeactivatedEvent e:
                IsActive = false;
                break;
        }
    }
}

// Events
public class AccountCreatedEvent : Event
{
    public Guid AccountId { get; }
    public string CustomerName { get; }
    public decimal InitialBalance { get; }
    
    public AccountCreatedEvent(Guid accountId, string customerName, decimal initialBalance)
    {
        AccountId = accountId;
        CustomerName = customerName;
        InitialBalance = initialBalance;
    }
}

public class MoneyDepositedEvent : Event
{
    public Guid AccountId { get; }
    public decimal Amount { get; }
    
    public MoneyDepositedEvent(Guid accountId, decimal amount)
    {
        AccountId = accountId;
        Amount = amount;
    }
}

// Event store
public interface IEventStore
{
    Task SaveEventsAsync(Guid aggregateId, IEnumerable<Event> events, int expectedVersion);
    Task<IEnumerable<Event>> GetEventsAsync(Guid aggregateId);
    Task<IEnumerable<Event>> GetEventsAsync(Guid aggregateId, int fromVersion);
}

public class SqlEventStore : IEventStore
{
    private readonly string _connectionString;
    private readonly ILogger<SqlEventStore> _logger;
    
    public SqlEventStore(string connectionString, ILogger<SqlEventStore> logger)
    {
        _connectionString = connectionString;
        _logger = logger;
    }
    
    public async Task SaveEventsAsync(Guid aggregateId, IEnumerable<Event> events, int expectedVersion)
    {
        using var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync();
        
        using var transaction = await connection.BeginTransactionAsync();
        
        try
        {
            // Check current version
            var currentVersion = await GetCurrentVersionAsync(connection, transaction, aggregateId);
            if (currentVersion != expectedVersion)
            {
                throw new ConcurrencyException($"Expected version {expectedVersion}, but current version is {currentVersion}");
            }
            
            // Save events
            foreach (var @event in events)
            {
                await SaveEventAsync(connection, transaction, aggregateId, @event, ++currentVersion);
            }
            
            await transaction.CommitAsync();
        }
        catch
        {
            await transaction.RollbackAsync();
            throw;
        }
    }
    
    public async Task<IEnumerable<Event>> GetEventsAsync(Guid aggregateId)
    {
        return await GetEventsAsync(aggregateId, 0);
    }
    
    public async Task<IEnumerable<Event>> GetEventsAsync(Guid aggregateId, int fromVersion)
    {
        using var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync();
        
        var sql = @"
            SELECT EventType, EventData, Version
            FROM Events
            WHERE AggregateId = @AggregateId AND Version > @FromVersion
            ORDER BY Version";
            
        var command = new SqlCommand(sql, connection);
        command.Parameters.AddWithValue("@AggregateId", aggregateId);
        command.Parameters.AddWithValue("@FromVersion", fromVersion);
        
        var events = new List<Event>();
        using var reader = await command.ExecuteReaderAsync();
        
        while (await reader.ReadAsync())
        {
            var eventType = reader.GetString("EventType");
            var eventData = reader.GetString("EventData");
            
            var @event = DeserializeEvent(eventType, eventData);
            events.Add(@event);
        }
        
        return events;
    }
    
    private Event DeserializeEvent(string eventType, string eventData)
    {
        var type = Type.GetType($"YourNamespace.{eventType}");
        return (Event)JsonSerializer.Deserialize(eventData, type);
    }
}
```

### Q39: How do you implement CQRS (Command Query Responsibility Segregation)?
**Answer:**
```csharp
// CQRS implementation with MediatR
public interface ICommand : IRequest<CommandResult> { }
public interface IQuery<TResult> : IRequest<TResult> { }

public class CommandResult
{
    public bool Success { get; set; }
    public string Message { get; set; }
    public object Data { get; set; }
    
    public static CommandResult Ok(object data = null) => new CommandResult { Success = true, Data = data };
    public static CommandResult Fail(string message) => new CommandResult { Success = false, Message = message };
}

// Commands
public class CreateCustomerCommand : ICommand
{
    public string Name { get; set; }
    public string Email { get; set; }
    public string Phone { get; set; }
}

public class UpdateCustomerCommand : ICommand
{
    public Guid CustomerId { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public string Phone { get; set; }
}

// Queries
public class GetCustomerQuery : IQuery<CustomerDto>
{
    public Guid CustomerId { get; set; }
}

public class GetCustomersQuery : IQuery<IEnumerable<CustomerDto>>
{
    public string SearchTerm { get; set; }
    public int Page { get; set; } = 1;
    public int PageSize { get; set; } = 10;
}

// Command Handlers
public class CreateCustomerCommandHandler : IRequestHandler<CreateCustomerCommand, CommandResult>
{
    private readonly ICustomerWriteRepository _repository;
    private readonly IEventBus _eventBus;
    private readonly ILogger<CreateCustomerCommandHandler> _logger;
    
    public CreateCustomerCommandHandler(
        ICustomerWriteRepository repository,
        IEventBus eventBus,
        ILogger<CreateCustomerCommandHandler> logger)
    {
        _repository = repository;
        _eventBus = eventBus;
        _logger = logger;
    }
    
    public async Task<CommandResult> Handle(CreateCustomerCommand request, CancellationToken cancellationToken)
    {
        try
        {
            // Validate command
            var validationResult = await ValidateCommand(request);
            if (!validationResult.IsValid)
            {
                return CommandResult.Fail(string.Join(", ", validationResult.Errors));
            }
            
            // Create customer
            var customer = new Customer
            {
                Id = Guid.NewGuid(),
                Name = request.Name,
                Email = request.Email,
                Phone = request.Phone,
                CreatedAt = DateTime.UtcNow
            };
            
            await _repository.AddAsync(customer);
            await _repository.SaveChangesAsync();
            
            // Publish domain event
            await _eventBus.PublishAsync(new CustomerCreatedEvent
            {
                CustomerId = customer.Id,
                Name = customer.Name,
                Email = customer.Email
            });
            
            _logger.LogInformation("Customer created: {CustomerId}", customer.Id);
            
            return CommandResult.Ok(new { CustomerId = customer.Id });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating customer");
            return CommandResult.Fail("Failed to create customer");
        }
    }
    
    private async Task<ValidationResult> ValidateCommand(CreateCustomerCommand command)
    {
        var validator = new CreateCustomerCommandValidator();
        return await validator.ValidateAsync(command);
    }
}

// Query Handlers
public class GetCustomerQueryHandler : IRequestHandler<GetCustomerQuery, CustomerDto>
{
    private readonly ICustomerReadRepository _repository;
    private readonly IMapper _mapper;
    
    public GetCustomerQueryHandler(ICustomerReadRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }
    
    public async Task<CustomerDto> Handle(GetCustomerQuery request, CancellationToken cancellationToken)
    {
        var customer = await _repository.GetByIdAsync(request.CustomerId);
        return _mapper.Map<CustomerDto>(customer);
    }
}

public class GetCustomersQueryHandler : IRequestHandler<GetCustomersQuery, IEnumerable<CustomerDto>>
{
    private readonly ICustomerReadRepository _repository;
    private readonly IMapper _mapper;
    
    public GetCustomersQueryHandler(ICustomerReadRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }
    
    public async Task<IEnumerable<CustomerDto>> Handle(GetCustomersQuery request, CancellationToken cancellationToken)
    {
        var customers = await _repository.SearchAsync(request.SearchTerm, request.Page, request.PageSize);
        return _mapper.Map<IEnumerable<CustomerDto>>(customers);
    }
}

// Separate read and write models
public interface ICustomerWriteRepository
{
    Task AddAsync(Customer customer);
    Task UpdateAsync(Customer customer);
    Task DeleteAsync(Guid id);
    Task SaveChangesAsync();
}

public interface ICustomerReadRepository
{
    Task<CustomerReadModel> GetByIdAsync(Guid id);
    Task<IEnumerable<CustomerReadModel>> SearchAsync(string searchTerm, int page, int pageSize);
    Task<IEnumerable<CustomerReadModel>> GetAllAsync();
}

// Read model (optimized for queries)
public class CustomerReadModel
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public string Phone { get; set; }
    public DateTime CreatedAt { get; set; }
    public int TotalOrders { get; set; }
    public decimal TotalSpent { get; set; }
    public string Status { get; set; }
}

// Write model (optimized for commands)
public class Customer
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public string Phone { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}

// Controller using CQRS
[ApiController]
[Route("api/[controller]")]
public class CustomersController : ControllerBase
{
    private readonly IMediator _mediator;
    
    public CustomersController(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    [HttpPost]
    public async Task<IActionResult> CreateCustomer([FromBody] CreateCustomerCommand command)
    {
        var result = await _mediator.Send(command);
        
        if (result.Success)
        {
            return CreatedAtAction(nameof(GetCustomer), new { id = ((dynamic)result.Data).CustomerId }, result.Data);
        }
        
        return BadRequest(result.Message);
    }
    
    [HttpGet("{id}")]
    public async Task<IActionResult> GetCustomer(Guid id)
    {
        var customer = await _mediator.Send(new GetCustomerQuery { CustomerId = id });
        
        if (customer == null)
        {
            return NotFound();
        }
        
        return Ok(customer);
    }
    
    [HttpGet]
    public async Task<IActionResult> GetCustomers([FromQuery] GetCustomersQuery query)
    {
        var customers = await _mediator.Send(query);
        return Ok(customers);
    }
}
```

### Q40: How do you implement microservices communication patterns?
**Answer:**
```csharp
// Service-to-service communication with HTTP
public class OrderService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<OrderService> _logger;
    private readonly ICircuitBreaker _circuitBreaker;
    
    public OrderService(HttpClient httpClient, ILogger<OrderService> logger, ICircuitBreaker circuitBreaker)
    {
        _httpClient = httpClient;
        _logger = logger;
        _circuitBreaker = circuitBreaker;
    }
    
    public async Task<OrderResult> CreateOrderAsync(CreateOrderRequest request)
    {
        try
        {
            // Call inventory service to check availability
            var inventoryResult = await _circuitBreaker.ExecuteAsync(async () =>
            {
                var response = await _httpClient.PostAsJsonAsync(
                    "http://inventory-service/api/inventory/check",
                    new { ProductIds = request.Items.Select(i => i.ProductId) }
                );
                
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadFromJsonAsync<InventoryCheckResult>();
            });
            
            if (!inventoryResult.AllItemsAvailable)
            {
                return OrderResult.Fail("Some items are not available");
            }
            
            // Call payment service
            var paymentResult = await _circuitBreaker.ExecuteAsync(async () =>
            {
                var response = await _httpClient.PostAsJsonAsync(
                    "http://payment-service/api/payments/process",
                    new { Amount = request.TotalAmount, CustomerId = request.CustomerId }
                );
                
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadFromJsonAsync<PaymentResult>();
            });
            
            if (!paymentResult.Success)
            {
                return OrderResult.Fail("Payment failed");
            }
            
            // Create order
            var order = new Order
            {
                Id = Guid.NewGuid(),
                CustomerId = request.CustomerId,
                Items = request.Items,
                TotalAmount = request.TotalAmount,
                Status = OrderStatus.Confirmed,
                CreatedAt = DateTime.UtcNow
            };
            
            // Save order and publish event
            await SaveOrderAsync(order);
            await PublishOrderCreatedEventAsync(order);
            
            return OrderResult.Success(order.Id);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating order");
            return OrderResult.Fail("Internal error occurred");
        }
    }
}

// Message-based communication with RabbitMQ
public class EventBus : IEventBus
{
    private readonly IConnection _connection;
    private readonly IModel _channel;
    private readonly ILogger<EventBus> _logger;
    
    public EventBus(IConnection connection, ILogger<EventBus> logger)
    {
        _connection = connection;
        _channel = _connection.CreateModel();
        _logger = logger;
    }
    
    public async Task PublishAsync<T>(T @event) where T : class
    {
        var eventName = typeof(T).Name;
        var message = JsonSerializer.Serialize(@event);
        var body = Encoding.UTF8.GetBytes(message);
        
        var properties = _channel.CreateBasicProperties();
        properties.Persistent = true;
        properties.MessageId = Guid.NewGuid().ToString();
        properties.Timestamp = new AmqpTimestamp(DateTimeOffset.UtcNow.ToUnixTimeSeconds());
        
        _channel.BasicPublish(
            exchange: "events",
            routingKey: eventName,
            basicProperties: properties,
            body: body
        );
        
        _logger.LogInformation("Published event {EventName} with ID {MessageId}", 
            eventName, properties.MessageId);
    }
    
    public void Subscribe<T>(Func<T, Task> handler) where T : class
    {
        var eventName = typeof(T).Name;
        var queueName = $"{Environment.MachineName}_{eventName}";
        
        _channel.QueueDeclare(queue: queueName, durable: true, exclusive: false, autoDelete: false);
        _channel.QueueBind(queue: queueName, exchange: "events", routingKey: eventName);
        
        var consumer = new EventingBasicConsumer(_channel);
        consumer.Received += async (model, ea) =>
        {
            try
            {
                var body = ea.Body.ToArray();
                var message = Encoding.UTF8.GetString(body);
                var @event = JsonSerializer.Deserialize<T>(message);
                
                await handler(@event);
                
                _channel.BasicAck(deliveryTag: ea.DeliveryTag, multiple: false);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing event {EventName}", eventName);
                _channel.BasicNack(deliveryTag: ea.DeliveryTag, multiple: false, requeue: true);
            }
        };
        
        _channel.BasicConsume(queue: queueName, autoAck: false, consumer: consumer);
    }
}

// Saga pattern for distributed transactions
public class OrderSaga
{
    private readonly IEventBus _eventBus;
    private readonly IOrderRepository _orderRepository;
    private readonly ILogger<OrderSaga> _logger;
    
    public OrderSaga(IEventBus eventBus, IOrderRepository orderRepository, ILogger<OrderSaga> logger)
    {
        _eventBus = eventBus;
        _orderRepository = orderRepository;
        _logger = logger;
        
        // Subscribe to events
        _eventBus.Subscribe<OrderCreatedEvent>(HandleOrderCreatedAsync);
        _eventBus.Subscribe<PaymentProcessedEvent>(HandlePaymentProcessedAsync);
        _eventBus.Subscribe<PaymentFailedEvent>(HandlePaymentFailedAsync);
        _eventBus.Subscribe<InventoryReservedEvent>(HandleInventoryReservedAsync);
        _eventBus.Subscribe<InventoryReservationFailedEvent>(HandleInventoryReservationFailedAsync);
    }
    
    private async Task HandleOrderCreatedAsync(OrderCreatedEvent @event)
    {
        _logger.LogInformation("Starting saga for order {OrderId}", @event.OrderId);
        
        // Step 1: Reserve inventory
        await _eventBus.PublishAsync(new ReserveInventoryCommand
        {
            OrderId = @event.OrderId,
            Items = @event.Items
        });
    }
    
    private async Task HandleInventoryReservedAsync(InventoryReservedEvent @event)
    {
        _logger.LogInformation("Inventory reserved for order {OrderId}", @event.OrderId);
        
        // Step 2: Process payment
        await _eventBus.PublishAsync(new ProcessPaymentCommand
        {
            OrderId = @event.OrderId,
            Amount = @event.TotalAmount,
            CustomerId = @event.CustomerId
        });
    }
    
    private async Task HandlePaymentProcessedAsync(PaymentProcessedEvent @event)
    {
        _logger.LogInformation("Payment processed for order {OrderId}", @event.OrderId);
        
        // Step 3: Confirm order
        var order = await _orderRepository.GetByIdAsync(@event.OrderId);
        order.Status = OrderStatus.Confirmed;
        await _orderRepository.UpdateAsync(order);
        
        await _eventBus.PublishAsync(new OrderConfirmedEvent
        {
            OrderId = @event.OrderId,
            CustomerId = order.CustomerId
        });
    }
    
    private async Task HandlePaymentFailedAsync(PaymentFailedEvent @event)
    {
        _logger.LogWarning("Payment failed for order {OrderId}, starting compensation", @event.OrderId);
        
        // Compensate: Release inventory reservation
        await _eventBus.PublishAsync(new ReleaseInventoryCommand
        {
            OrderId = @event.OrderId
        });
        
        // Cancel order
        var order = await _orderRepository.GetByIdAsync(@event.OrderId);
        order.Status = OrderStatus.Cancelled;
        await _orderRepository.UpdateAsync(order);
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

### Q41: How do you implement GraphQL in C#?
**Answer:**
```csharp
// GraphQL implementation with HotChocolate
public class Query
{
    public async Task<IEnumerable<Customer>> GetCustomersAsync([Service] ICustomerRepository repository)
    {
        return await repository.GetAllAsync();
    }
    
    public async Task<Customer> GetCustomerAsync(Guid id, [Service] ICustomerRepository repository)
    {
        return await repository.GetByIdAsync(id);
    }
    
    [UseFiltering]
    [UseSorting]
    [UsePaging]
    public IQueryable<Order> GetOrders([Service] IOrderRepository repository)
    {
        return repository.GetQueryable();
    }
}

public class Mutation
{
    public async Task<CustomerPayload> CreateCustomerAsync(
        CreateCustomerInput input,
        [Service] ICustomerRepository repository)
    {
        var customer = new Customer
        {
            Id = Guid.NewGuid(),
            Name = input.Name,
            Email = input.Email
        };
        
        await repository.AddAsync(customer);
        
        return new CustomerPayload(customer);
    }
}

public class Subscription
{
    [Subscribe]
    public CustomerCreatedEvent OnCustomerCreated([EventMessage] CustomerCreatedEvent customerCreated)
    {
        return customerCreated;
    }
}
```

### Q42: How do you implement gRPC services in C#?
**Answer:**
```csharp
// gRPC service implementation
public class CustomerService : CustomerGrpc.CustomerGrpcBase
{
    private readonly ICustomerRepository _repository;
    private readonly ILogger<CustomerService> _logger;
    
    public CustomerService(ICustomerRepository repository, ILogger<CustomerService> logger)
    {
        _repository = repository;
        _logger = logger;
    }
    
    public override async Task<GetCustomerResponse> GetCustomer(
        GetCustomerRequest request, 
        ServerCallContext context)
    {
        var customer = await _repository.GetByIdAsync(Guid.Parse(request.Id));
        
        if (customer == null)
        {
            throw new RpcException(new Status(StatusCode.NotFound, "Customer not found"));
        }
        
        return new GetCustomerResponse
        {
            Customer = new CustomerDto
            {
                Id = customer.Id.ToString(),
                Name = customer.Name,
                Email = customer.Email
            }
        };
    }
    
    public override async Task GetCustomers(
        GetCustomersRequest request,
        IServerStreamWriter<CustomerDto> responseStream,
        ServerCallContext context)
    {
        var customers = await _repository.GetAllAsync();
        
        foreach (var customer in customers)
        {
            if (context.CancellationToken.IsCancellationRequested)
                break;
                
            await responseStream.WriteAsync(new CustomerDto
            {
                Id = customer.Id.ToString(),
                Name = customer.Name,
                Email = customer.Email
            });
        }
    }
}
```

### Q43: How do you implement OAuth 2.0 and JWT authentication?
**Answer:**
```csharp
// JWT authentication implementation
public class JwtAuthenticationService
{
    private readonly IConfiguration _configuration;
    private readonly IUserRepository _userRepository;
    
    public JwtAuthenticationService(IConfiguration configuration, IUserRepository userRepository)
    {
        _configuration = configuration;
        _userRepository = userRepository;
    }
    
    public async Task<AuthenticationResult> AuthenticateAsync(string email, string password)
    {
        var user = await _userRepository.GetByEmailAsync(email);
        
        if (user == null || !VerifyPassword(password, user.PasswordHash))
        {
            return AuthenticationResult.Failed("Invalid credentials");
        }
        
        var token = GenerateJwtToken(user);
        var refreshToken = GenerateRefreshToken();
        
        // Store refresh token
        user.RefreshToken = refreshToken;
        user.RefreshTokenExpiry = DateTime.UtcNow.AddDays(7);
        await _userRepository.UpdateAsync(user);
        
        return AuthenticationResult.Success(token, refreshToken);
    }
    
    private string GenerateJwtToken(User user)
    {
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
        
        var claims = new[]
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new Claim(ClaimTypes.Email, user.Email),
            new Claim(ClaimTypes.Name, user.Name),
            new Claim("role", user.Role)
        };
        
        var token = new JwtSecurityToken(
            issuer: _configuration["Jwt:Issuer"],
            audience: _configuration["Jwt:Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(15),
            signingCredentials: credentials
        );
        
        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}

// OAuth 2.0 implementation
public class OAuth2Service
{
    private readonly HttpClient _httpClient;
    private readonly IConfiguration _configuration;
    
    public OAuth2Service(HttpClient httpClient, IConfiguration configuration)
    {
        _httpClient = httpClient;
        _configuration = configuration;
    }
    
    public async Task<TokenResponse> ExchangeCodeForTokenAsync(string code, string redirectUri)
    {
        var tokenRequest = new Dictionary<string, string>
        {
            ["grant_type"] = "authorization_code",
            ["code"] = code,
            ["redirect_uri"] = redirectUri,
            ["client_id"] = _configuration["OAuth:ClientId"],
            ["client_secret"] = _configuration["OAuth:ClientSecret"]
        };
        
        var content = new FormUrlEncodedContent(tokenRequest);
        var response = await _httpClient.PostAsync(_configuration["OAuth:TokenEndpoint"], content);
        
        if (!response.IsSuccessStatusCode)
        {
            throw new OAuth2Exception("Failed to exchange code for token");
        }
        
        var json = await response.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<TokenResponse>(json);
    }
}
```

### Q44: How do you implement data validation and sanitization?
**Answer:**
```csharp
// Comprehensive data validation
public class DataValidator
{
    public ValidationResult ValidateCustomer(CustomerDto customer)
    {
        var result = new ValidationResult();
        
        // Required field validation
        if (string.IsNullOrWhiteSpace(customer.Name))
        {
            result.AddError("Name", "Name is required");
        }
        
        // Email validation
        if (!IsValidEmail(customer.Email))
        {
            result.AddError("Email", "Invalid email format");
        }
        
        // Phone validation
        if (!IsValidPhoneNumber(customer.Phone))
        {
            result.AddError("Phone", "Invalid phone number format");
        }
        
        // Business rule validation
        if (customer.Age < 18)
        {
            result.AddError("Age", "Customer must be at least 18 years old");
        }
        
        return result;
    }
    
    private bool IsValidEmail(string email)
    {
        if (string.IsNullOrWhiteSpace(email))
            return false;
            
        try
        {
            var addr = new MailAddress(email);
            return addr.Address == email;
        }
        catch
        {
            return false;
        }
    }
    
    private bool IsValidPhoneNumber(string phone)
    {
        if (string.IsNullOrWhiteSpace(phone))
            return false;
            
        var phoneRegex = new Regex(@"^\+?[1-9]\d{1,14}$");
        return phoneRegex.IsMatch(phone.Replace(" ", "").Replace("-", ""));
    }
}

// Data sanitization
public class DataSanitizer
{
    public string SanitizeHtml(string input)
    {
        if (string.IsNullOrEmpty(input))
            return input;
            
        // Remove HTML tags
        var htmlRegex = new Regex("<.*?>");
        var sanitized = htmlRegex.Replace(input, string.Empty);
        
        // Decode HTML entities
        sanitized = HttpUtility.HtmlDecode(sanitized);
        
        return sanitized.Trim();
    }
    
    public string SanitizeSql(string input)
    {
        if (string.IsNullOrEmpty(input))
            return input;
            
        // Remove SQL injection patterns
        var sqlPatterns = new[]
        {
            @"('|(\-\-)|(;)|(\||\|)|(\*|\*))",
            @"(exec(ute)?\s+)|(select\s+)|(insert\s+)|(update\s+)|(delete\s+)|(drop\s+)|(create\s+)|(alter\s+)"
        };
        
        foreach (var pattern in sqlPatterns)
        {
            input = Regex.Replace(input, pattern, string.Empty, RegexOptions.IgnoreCase);
        }
        
        return input.Trim();
    }
    
    public string SanitizeFileName(string fileName)
    {
        if (string.IsNullOrEmpty(fileName))
            return fileName;
            
        // Remove invalid file name characters
        var invalidChars = Path.GetInvalidFileNameChars();
        foreach (var invalidChar in invalidChars)
        {
            fileName = fileName.Replace(invalidChar, '_');
        }
        
        // Limit length
        if (fileName.Length > 255)
        {
            var extension = Path.GetExtension(fileName);
            var nameWithoutExtension = Path.GetFileNameWithoutExtension(fileName);
            fileName = nameWithoutExtension.Substring(0, 255 - extension.Length) + extension;
        }
        
        return fileName;
    }
}
```

### Q45: How do you implement data encryption and security?
**Answer:**
```csharp
// Data encryption service
public class EncryptionService
{
    private readonly string _encryptionKey;
    
    public EncryptionService(IConfiguration configuration)
    {
        _encryptionKey = configuration["Encryption:Key"];
    }
    
    public string Encrypt(string plainText)
    {
        if (string.IsNullOrEmpty(plainText))
            return plainText;
            
        using var aes = Aes.Create();
        aes.Key = Convert.FromBase64String(_encryptionKey);
        aes.GenerateIV();
        
        using var encryptor = aes.CreateEncryptor();
        using var msEncrypt = new MemoryStream();
        using var csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write);
        using var swEncrypt = new StreamWriter(csEncrypt);
        
        swEncrypt.Write(plainText);
        swEncrypt.Close();
        
        var encrypted = msEncrypt.ToArray();
        var result = new byte[aes.IV.Length + encrypted.Length];
        
        Array.Copy(aes.IV, 0, result, 0, aes.IV.Length);
        Array.Copy(encrypted, 0, result, aes.IV.Length, encrypted.Length);
        
        return Convert.ToBase64String(result);
    }
    
    public string Decrypt(string cipherText)
    {
        if (string.IsNullOrEmpty(cipherText))
            return cipherText;
            
        var fullCipher = Convert.FromBase64String(cipherText);
        
        using var aes = Aes.Create();
        aes.Key = Convert.FromBase64String(_encryptionKey);
        
        var iv = new byte[aes.IV.Length];
        var cipher = new byte[fullCipher.Length - iv.Length];
        
        Array.Copy(fullCipher, iv, iv.Length);
        Array.Copy(fullCipher, iv.Length, cipher, 0, cipher.Length);
        
        aes.IV = iv;
        
        using var decryptor = aes.CreateDecryptor();
        using var msDecrypt = new MemoryStream(cipher);
        using var csDecrypt = new CryptoStream(msDecrypt, decryptor, CryptoStreamMode.Read);
        using var srDecrypt = new StreamReader(csDecrypt);
        
        return srDecrypt.ReadToEnd();
    }
    
    public string HashPassword(string password)
    {
        using var rng = RandomNumberGenerator.Create();
        var salt = new byte[32];
        rng.GetBytes(salt);
        
        using var pbkdf2 = new Rfc2898DeriveBytes(password, salt, 10000, HashAlgorithmName.SHA256);
        var hash = pbkdf2.GetBytes(32);
        
        var hashBytes = new byte[64];
        Array.Copy(salt, 0, hashBytes, 0, 32);
        Array.Copy(hash, 0, hashBytes, 32, 32);
        
        return Convert.ToBase64String(hashBytes);
    }
    
    public bool VerifyPassword(string password, string hash)
    {
        var hashBytes = Convert.FromBase64String(hash);
        var salt = new byte[32];
        Array.Copy(hashBytes, 0, salt, 0, 32);
        
        using var pbkdf2 = new Rfc2898DeriveBytes(password, salt, 10000, HashAlgorithmName.SHA256);
        var computedHash = pbkdf2.GetBytes(32);
        
        for (int i = 0; i < 32; i++)
        {
            if (hashBytes[i + 32] != computedHash[i])
                return false;
        }
        
        return true;
    }
}
```

### **Common Patterns:**
- Repository pattern for data access
- Pipeline pattern for ETL processes
- Factory pattern for creating data processors
- Observer pattern for monitoring and notifications
- Strategy pattern for different processing algorithms
- CQRS for separating read and write operations
- Event sourcing for audit trails
- Microservices communication patterns