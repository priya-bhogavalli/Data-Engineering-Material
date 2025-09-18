# 🚀 Go Programming Advanced Interview Questions (41-80)

## 📋 Advanced Topics Continued

### 41. What is the difference between buffered and unbuffered channels?
**Answer:**
```go
// Unbuffered channel - synchronous
ch1 := make(chan int)
go func() {
    ch1 <- 42 // Blocks until receiver ready
}()
value := <-ch1 // Blocks until sender ready

// Buffered channel - asynchronous
ch2 := make(chan int, 3)
ch2 <- 1 // Doesn't block (buffer has space)
ch2 <- 2
ch2 <- 3
ch2 <- 4 // Would block (buffer full)
```
- **Unbuffered**: Synchronous, zero capacity
- **Buffered**: Asynchronous up to buffer size

### 42. How do you implement a timeout for goroutines?
**Answer:**
```go
func doWorkWithTimeout(timeout time.Duration) error {
    done := make(chan bool)
    
    go func() {
        // Simulate work
        time.Sleep(2 * time.Second)
        done <- true
    }()
    
    select {
    case <-done:
        return nil
    case <-time.After(timeout):
        return errors.New("operation timed out")
    }
}

// Usage
err := doWorkWithTimeout(1 * time.Second)
```

### 43. What are method sets in Go?
**Answer:**
```go
type T struct{}

func (t T) ValueMethod() {}    // Value receiver
func (t *T) PointerMethod() {} // Pointer receiver

var t T
var p *T = &t

// Method sets:
// T has methods: ValueMethod
// *T has methods: ValueMethod, PointerMethod

t.ValueMethod()    // OK
// t.PointerMethod() // Error: T doesn't have PointerMethod

p.ValueMethod()    // OK (Go automatically dereferences)
p.PointerMethod()  // OK
```

### 44. How do you implement custom marshaling/unmarshaling in Go?
**Answer:**
```go
type Person struct {
    Name      string
    BirthDate time.Time
}

func (p Person) MarshalJSON() ([]byte, error) {
    type Alias Person
    return json.Marshal(&struct {
        BirthDate string `json:"birth_date"`
        *Alias
    }{
        BirthDate: p.BirthDate.Format("2006-01-02"),
        Alias:     (*Alias)(&p),
    })
}

func (p *Person) UnmarshalJSON(data []byte) error {
    type Alias Person
    aux := &struct {
        BirthDate string `json:"birth_date"`
        *Alias
    }{
        Alias: (*Alias)(p),
    }
    
    if err := json.Unmarshal(data, &aux); err != nil {
        return err
    }
    
    var err error
    p.BirthDate, err = time.Parse("2006-01-02", aux.BirthDate)
    return err
}
```

### 45. What is the init() function and how is it used?
**Answer:**
```go
package main

import "fmt"

var globalVar int

func init() {
    globalVar = 42
    fmt.Println("Package initialized")
}

func init() {
    // Multiple init functions allowed
    fmt.Println("Second init function")
}

func main() {
    fmt.Println("Main function")
    fmt.Println("Global var:", globalVar)
}
```
- **Execution order**: init() before main()
- **Multiple init()**: Executed in order of appearance
- **Package initialization**: Runs when package is imported

### 46. How do you handle panics and recovery in Go?
**Answer:**
```go
func safeDivide(a, b float64) (result float64, err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic recovered: %v", r)
        }
    }()
    
    if b == 0 {
        panic("division by zero")
    }
    
    return a / b, nil
}

// Usage
result, err := safeDivide(10, 0)
if err != nil {
    fmt.Println("Error:", err)
}
```

### 47. What are Go's memory ordering guarantees?
**Answer:**
- **Happens-before relationship**: Defines memory ordering
- **Channel operations**: Provide synchronization
- **Mutex operations**: Establish happens-before
- **sync/atomic**: Atomic operations
```go
var a, b int

func f() {
    a = 1
    b = 2
}

func g() {
    print(b) // Might print 0, 2
    print(a) // Might print 0, 1
}

// Use synchronization for ordering guarantees
var mu sync.Mutex

func f() {
    mu.Lock()
    a = 1
    b = 2
    mu.Unlock()
}
```

### 48. How do you implement a singleton pattern in Go?
**Answer:**
```go
type Singleton struct {
    value string
}

var instance *Singleton
var once sync.Once

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{value: "singleton"}
    })
    return instance
}

// Alternative with package-level variable
var singleton = &Singleton{value: "singleton"}

func GetSingleton() *Singleton {
    return singleton
}
```

### 49. What are Go's calling conventions?
**Answer:**
- **Pass by value**: Default for all types
- **Pointers**: For reference semantics
- **Slices/maps/channels**: Reference types (header passed by value)
```go
func modifyValue(x int) {
    x = 100 // Doesn't affect original
}

func modifyPointer(x *int) {
    *x = 100 // Modifies original
}

func modifySlice(s []int) {
    s[0] = 100 // Modifies original slice elements
    s = append(s, 200) // Doesn't affect original slice header
}
```

### 50. How do you implement custom error types?
**Answer:**
```go
// Simple custom error
type ValidationError struct {
    Field   string
    Message string
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("validation error in field %s: %s", e.Field, e.Message)
}

// Error with wrapping
type DatabaseError struct {
    Operation string
    Err       error
}

func (e DatabaseError) Error() string {
    return fmt.Sprintf("database error during %s: %v", e.Operation, e.Err)
}

func (e DatabaseError) Unwrap() error {
    return e.Err
}

// Usage with errors.Is and errors.As
var dbErr DatabaseError
if errors.As(err, &dbErr) {
    fmt.Println("Database operation:", dbErr.Operation)
}
```

### 51. What is the difference between make() and new()?
**Answer:**
```go
// new() - allocates zeroed memory, returns pointer
p := new(int)        // *int, points to 0
s := new([]int)      // *[]int, points to nil slice

// make() - initializes slices, maps, channels
slice := make([]int, 5)      // []int with length 5
m := make(map[string]int)    // initialized map
ch := make(chan int, 10)     // buffered channel

// Key differences:
// new(T) returns *T
// make(T) returns T (for reference types)
```

### 52. How do you implement worker pools in Go?
**Answer:**
```go
type Job struct {
    ID   int
    Data string
}

type Result struct {
    Job Job
    Sum int
}

func worker(id int, jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        // Simulate work
        sum := 0
        for _, char := range job.Data {
            sum += int(char)
        }
        
        results <- Result{Job: job, Sum: sum}
    }
}

func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)
    
    // Start workers
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }
    
    // Send jobs
    for j := 1; j <= 5; j++ {
        jobs <- Job{ID: j, Data: fmt.Sprintf("job-%d", j)}
    }
    close(jobs)
    
    // Collect results
    for r := 1; r <= 5; r++ {
        result := <-results
        fmt.Printf("Job %d result: %d\n", result.Job.ID, result.Sum)
    }
}
```

### 53. What are Go's build constraints and how do you use them?
**Answer:**
```go
// Legacy syntax
// +build linux,amd64 darwin,amd64
// +build !windows

// Modern syntax (Go 1.17+)
//go:build (linux && amd64) || (darwin && amd64)
//go:build !windows

package main

// File will only be included in builds for:
// - Linux on AMD64
// - macOS on AMD64
// - Not on Windows

// Common build tags:
// - Operating systems: linux, darwin, windows, freebsd
// - Architectures: amd64, arm64, 386
// - Custom tags: debug, integration, race
```

### 54. How do you implement graceful degradation in Go services?
**Answer:**
```go
type Service struct {
    cache    Cache
    database Database
    fallback bool
}

func (s *Service) GetUser(id string) (*User, error) {
    // Try cache first
    if user, err := s.cache.Get(id); err == nil {
        return user, nil
    }
    
    // Try database
    user, err := s.database.GetUser(id)
    if err != nil {
        if s.fallback {
            // Return default user or cached stale data
            return s.getFallbackUser(id), nil
        }
        return nil, err
    }
    
    // Update cache asynchronously
    go s.cache.Set(id, user)
    
    return user, nil
}

func (s *Service) getFallbackUser(id string) *User {
    return &User{ID: id, Name: "Unknown User"}
}
```

### 55. What are Go's atomic operations and when to use them?
**Answer:**
```go
import "sync/atomic"

type Counter struct {
    value int64
}

func (c *Counter) Increment() {
    atomic.AddInt64(&c.value, 1)
}

func (c *Counter) Get() int64 {
    return atomic.LoadInt64(&c.value)
}

func (c *Counter) Set(value int64) {
    atomic.StoreInt64(&c.value, value)
}

// Compare and swap
func (c *Counter) CompareAndSwap(old, new int64) bool {
    return atomic.CompareAndSwapInt64(&c.value, old, new)
}

// Use atomic for:
// - Simple counters
// - Flags
// - Lock-free data structures
// - Performance-critical code
```

### 56. How do you implement circuit breaker pattern in Go?
**Answer:**
```go
type CircuitBreaker struct {
    maxFailures int
    resetTimeout time.Duration
    failures     int
    lastFailTime time.Time
    state        string // "closed", "open", "half-open"
    mutex        sync.Mutex
}

func (cb *CircuitBreaker) Call(fn func() error) error {
    cb.mutex.Lock()
    defer cb.mutex.Unlock()
    
    if cb.state == "open" {
        if time.Since(cb.lastFailTime) > cb.resetTimeout {
            cb.state = "half-open"
            cb.failures = 0
        } else {
            return errors.New("circuit breaker is open")
        }
    }
    
    err := fn()
    if err != nil {
        cb.failures++
        cb.lastFailTime = time.Now()
        
        if cb.failures >= cb.maxFailures {
            cb.state = "open"
        }
        return err
    }
    
    cb.failures = 0
    cb.state = "closed"
    return nil
}
```

### 57. What are Go's escape analysis rules?
**Answer:**
Variables escape to heap when:
- **Returned by reference**: `return &x`
- **Assigned to interface**: `var i interface{} = x`
- **Sent to channel**: `ch <- &x`
- **Assigned to slice/map**: `slice[0] = &x`
- **Too large for stack**: Large arrays/structs
- **Unknown size at compile time**: `make([]int, n)`

```go
func escapes() *int {
    x := 42
    return &x // x escapes to heap
}

func noEscape() int {
    x := 42
    return x // x stays on stack
}

// Check with: go build -gcflags=-m
```

### 58. How do you implement rate limiting in Go?
**Answer:**
```go
import "golang.org/x/time/rate"

// Token bucket rate limiter
limiter := rate.NewLimiter(rate.Limit(10), 5) // 10 requests/sec, burst of 5

func handleRequest(w http.ResponseWriter, r *http.Request) {
    if !limiter.Allow() {
        http.Error(w, "Rate limit exceeded", http.StatusTooManyRequests)
        return
    }
    
    // Process request
    fmt.Fprintf(w, "Request processed")
}

// Per-user rate limiting
type UserLimiter struct {
    limiters map[string]*rate.Limiter
    mu       sync.RWMutex
}

func (ul *UserLimiter) GetLimiter(userID string) *rate.Limiter {
    ul.mu.RLock()
    limiter, exists := ul.limiters[userID]
    ul.mu.RUnlock()
    
    if !exists {
        ul.mu.Lock()
        limiter = rate.NewLimiter(rate.Limit(10), 5)
        ul.limiters[userID] = limiter
        ul.mu.Unlock()
    }
    
    return limiter
}
```

### 59. What are Go's memory alignment rules?
**Answer:**
```go
type BadStruct struct {
    a bool   // 1 byte
    b int64  // 8 bytes (7 bytes padding after a)
    c bool   // 1 byte (7 bytes padding after c)
}
// Total: 24 bytes

type GoodStruct struct {
    b int64  // 8 bytes
    a bool   // 1 byte
    c bool   // 1 byte (6 bytes padding after c)
}
// Total: 16 bytes

// Check alignment with unsafe.Sizeof()
fmt.Println(unsafe.Sizeof(BadStruct{}))  // 24
fmt.Println(unsafe.Sizeof(GoodStruct{})) // 16

// Rules:
// - Fields aligned to their size
// - Struct size multiple of largest field alignment
// - Order fields by size (largest first) for optimal packing
```

### 60. How do you implement dependency injection in Go?
**Answer:**
```go
// Interface-based DI
type UserRepository interface {
    GetUser(id string) (*User, error)
}

type UserService struct {
    repo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

// Constructor injection
type DatabaseUserRepository struct {
    db *sql.DB
}

func NewDatabaseUserRepository(db *sql.DB) UserRepository {
    return &DatabaseUserRepository{db: db}
}

// Wire it up
func main() {
    db := setupDatabase()
    repo := NewDatabaseUserRepository(db)
    service := NewUserService(repo)
}

// Using wire (Google's DI framework)
//go:generate wire
func InitializeUserService() *UserService {
    wire.Build(
        setupDatabase,
        NewDatabaseUserRepository,
        NewUserService,
    )
    return nil
}
```

### 61. What are Go's string internals and optimization?
**Answer:**
```go
// String structure
type StringHeader struct {
    Data uintptr // Pointer to byte array
    Len  int     // Length
}

// Strings are immutable
s1 := "hello"
s2 := s1 + " world" // Creates new string

// Efficient string building
var builder strings.Builder
builder.Grow(100) // Pre-allocate capacity
for i := 0; i < 10; i++ {
    builder.WriteString("hello")
}
result := builder.String()

// String to []byte conversion (copy)
s := "hello"
b := []byte(s) // Copies data

// Unsafe conversion (no copy, but dangerous)
b := *(*[]byte)(unsafe.Pointer(&reflect.SliceHeader{
    Data: (*reflect.StringHeader)(unsafe.Pointer(&s)).Data,
    Len:  len(s),
    Cap:  len(s),
}))
```

### 62. How do you implement middleware in Go HTTP servers?
**Answer:**
```go
type Middleware func(http.Handler) http.Handler

func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token == "" {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        next.ServeHTTP(w, r)
    })
}

// Chain middlewares
func ChainMiddleware(h http.Handler, middlewares ...Middleware) http.Handler {
    for i := len(middlewares) - 1; i >= 0; i-- {
        h = middlewares[i](h)
    }
    return h
}

// Usage
handler := ChainMiddleware(
    http.HandlerFunc(homeHandler),
    LoggingMiddleware,
    AuthMiddleware,
)
```

### 63. What are Go's compilation phases?
**Answer:**
1. **Lexical analysis**: Source code → tokens
2. **Parsing**: Tokens → AST (Abstract Syntax Tree)
3. **Type checking**: Verify types and semantics
4. **Escape analysis**: Determine stack vs heap allocation
5. **Inlining**: Inline small functions
6. **Optimization**: Dead code elimination, constant folding
7. **Code generation**: AST → machine code
8. **Linking**: Combine object files → executable

```bash
# See compilation steps
go build -x main.go

# See AST
go tool compile -W main.go

# See assembly
go tool compile -S main.go
```

### 64. How do you implement custom sorting with multiple criteria?
**Answer:**
```go
type Person struct {
    Name string
    Age  int
    City string
}

type MultiSorter struct {
    people []Person
    less   []func(p1, p2 *Person) bool
}

func (ms *MultiSorter) Sort(people []Person) {
    ms.people = people
    sort.Sort(ms)
}

func (ms *MultiSorter) OrderBy(less func(p1, p2 *Person) bool) *MultiSorter {
    ms.less = append(ms.less, less)
    return ms
}

func (ms *MultiSorter) Len() int { return len(ms.people) }

func (ms *MultiSorter) Swap(i, j int) {
    ms.people[i], ms.people[j] = ms.people[j], ms.people[i]
}

func (ms *MultiSorter) Less(i, j int) bool {
    p1, p2 := &ms.people[i], &ms.people[j]
    for _, less := range ms.less {
        if less(p1, p2) {
            return true
        }
        if less(p2, p1) {
            return false
        }
    }
    return false
}

// Usage
people := []Person{...}
sorter := &MultiSorter{}
sorter.OrderBy(func(p1, p2 *Person) bool { return p1.Age < p2.Age }).
       OrderBy(func(p1, p2 *Person) bool { return p1.Name < p2.Name }).
       Sort(people)
```

### 65. What are Go's runtime functions and GOMAXPROCS?
**Answer:**
```go
import "runtime"

// Get/set number of OS threads
fmt.Println("GOMAXPROCS:", runtime.GOMAXPROCS(0))
runtime.GOMAXPROCS(4) // Set to 4 threads

// Get number of goroutines
fmt.Println("Goroutines:", runtime.NumGoroutine())

// Get memory stats
var m runtime.MemStats
runtime.ReadMemStats(&m)
fmt.Printf("Alloc: %d KB", m.Alloc/1024)
fmt.Printf("Sys: %d KB", m.Sys/1024)

// Force garbage collection
runtime.GC()

// Get caller information
pc, file, line, ok := runtime.Caller(0)
if ok {
    fmt.Printf("Called from %s:%d\n", file, line)
}

// Set finalizer
runtime.SetFinalizer(obj, (*Object).cleanup)
```

### 66. How do you implement connection pooling in Go?
**Answer:**
```go
type Pool struct {
    connections chan net.Conn
    factory     func() (net.Conn, error)
    close       func(net.Conn) error
}

func NewPool(maxConnections int, factory func() (net.Conn, error), 
             close func(net.Conn) error) *Pool {
    return &Pool{
        connections: make(chan net.Conn, maxConnections),
        factory:     factory,
        close:       close,
    }
}

func (p *Pool) Get() (net.Conn, error) {
    select {
    case conn := <-p.connections:
        return conn, nil
    default:
        return p.factory()
    }
}

func (p *Pool) Put(conn net.Conn) error {
    select {
    case p.connections <- conn:
        return nil
    default:
        return p.close(conn)
    }
}

func (p *Pool) Close() {
    close(p.connections)
    for conn := range p.connections {
        p.close(conn)
    }
}

// Usage with database
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(25)
db.SetConnMaxLifetime(5 * time.Minute)
```

### 67. What are Go's unsafe operations and when to use them?
**Answer:**
```go
import "unsafe"

// Convert string to []byte without copying
func StringToBytes(s string) []byte {
    return *(*[]byte)(unsafe.Pointer(
        &struct {
            string
            Cap int
        }{s, len(s)},
    ))
}

// Convert []byte to string without copying
func BytesToString(b []byte) string {
    return *(*string)(unsafe.Pointer(&b))
}

// Get struct field offset
type Person struct {
    Name string
    Age  int
}

nameOffset := unsafe.Offsetof(Person{}.Name)
ageOffset := unsafe.Offsetof(Person{}.Age)

// Pointer arithmetic (dangerous!)
p := &Person{Name: "John", Age: 30}
agePtr := (*int)(unsafe.Pointer(uintptr(unsafe.Pointer(p)) + ageOffset))
*agePtr = 31

// Use unsafe only when:
// - Performance critical
// - Interfacing with C code
// - Low-level system programming
// - You understand the risks
```

### 68. How do you implement custom HTTP transport in Go?
**Answer:**
```go
// Custom transport with connection pooling and timeouts
transport := &http.Transport{
    MaxIdleConns:        100,
    MaxIdleConnsPerHost: 10,
    IdleConnTimeout:     90 * time.Second,
    TLSHandshakeTimeout: 10 * time.Second,
    DialContext: (&net.Dialer{
        Timeout:   30 * time.Second,
        KeepAlive: 30 * time.Second,
    }).DialContext,
}

client := &http.Client{
    Transport: transport,
    Timeout:   30 * time.Second,
}

// Custom RoundTripper for middleware
type LoggingTransport struct {
    Transport http.RoundTripper
}

func (lt *LoggingTransport) RoundTrip(req *http.Request) (*http.Response, error) {
    start := time.Now()
    resp, err := lt.Transport.RoundTrip(req)
    log.Printf("%s %s %v", req.Method, req.URL, time.Since(start))
    return resp, err
}

client.Transport = &LoggingTransport{
    Transport: transport,
}
```

### 69. What are Go's signal handling capabilities?
**Answer:**
```go
import (
    "os"
    "os/signal"
    "syscall"
)

func main() {
    // Create channel to receive signals
    sigChan := make(chan os.Signal, 1)
    
    // Register signals to catch
    signal.Notify(sigChan, 
        syscall.SIGINT,  // Ctrl+C
        syscall.SIGTERM, // Termination
        syscall.SIGHUP,  // Hangup
    )
    
    // Handle signals in goroutine
    go func() {
        for sig := range sigChan {
            switch sig {
            case syscall.SIGINT:
                log.Println("Received SIGINT, shutting down...")
                cleanup()
                os.Exit(0)
            case syscall.SIGTERM:
                log.Println("Received SIGTERM, shutting down...")
                cleanup()
                os.Exit(0)
            case syscall.SIGHUP:
                log.Println("Received SIGHUP, reloading config...")
                reloadConfig()
            }
        }
    }()
    
    // Main application logic
    select {} // Block forever
}

func cleanup() {
    // Cleanup resources
}

func reloadConfig() {
    // Reload configuration
}
```

### 70. How do you implement custom JSON marshaling for complex types?
**Answer:**
```go
type Duration time.Duration

func (d Duration) MarshalJSON() ([]byte, error) {
    return json.Marshal(time.Duration(d).String())
}

func (d *Duration) UnmarshalJSON(data []byte) error {
    var s string
    if err := json.Unmarshal(data, &s); err != nil {
        return err
    }
    
    duration, err := time.ParseDuration(s)
    if err != nil {
        return err
    }
    
    *d = Duration(duration)
    return nil
}

type Config struct {
    Timeout Duration `json:"timeout"`
    Retries int      `json:"retries"`
}

// Usage
config := Config{
    Timeout: Duration(30 * time.Second),
    Retries: 3,
}

data, _ := json.Marshal(config)
// {"timeout":"30s","retries":3}

var newConfig Config
json.Unmarshal(data, &newConfig)
```

### 71. What are Go's build modes and how do you use them?
**Answer:**
```bash
# Default executable
go build -buildmode=exe main.go

# Shared library
go build -buildmode=c-shared -o lib.so main.go

# Static library
go build -buildmode=c-archive -o lib.a main.go

# Plugin (Linux/macOS only)
go build -buildmode=plugin -o plugin.so plugin.go

# PIE (Position Independent Executable)
go build -buildmode=pie main.go
```

```go
// For c-shared/c-archive
//export Add
func Add(a, b int) int {
    return a + b
}

func main() {} // Required but not used

// For plugin
var Greeter greeter

type greeter struct{}

func (g greeter) Greet(name string) string {
    return "Hello, " + name
}
```

### 72. How do you implement custom flag parsing in Go?
**Answer:**
```go
import "flag"

// Custom flag type
type StringSlice []string

func (s *StringSlice) String() string {
    return strings.Join(*s, ",")
}

func (s *StringSlice) Set(value string) error {
    *s = append(*s, value)
    return nil
}

// Custom flag with validation
type Port int

func (p *Port) String() string {
    return fmt.Sprintf("%d", *p)
}

func (p *Port) Set(value string) error {
    port, err := strconv.Atoi(value)
    if err != nil {
        return err
    }
    if port < 1 || port > 65535 {
        return fmt.Errorf("port must be between 1 and 65535")
    }
    *p = Port(port)
    return nil
}

func main() {
    var hosts StringSlice
    var port Port = 8080
    
    flag.Var(&hosts, "host", "Host to connect to (can be repeated)")
    flag.Var(&port, "port", "Port to listen on")
    
    flag.Parse()
    
    fmt.Printf("Hosts: %v, Port: %d\n", hosts, port)
}
```

### 73. What are Go's execution tracer capabilities?
**Answer:**
```go
import (
    "os"
    "runtime/trace"
)

func main() {
    // Create trace file
    f, err := os.Create("trace.out")
    if err != nil {
        panic(err)
    }
    defer f.Close()
    
    // Start tracing
    err = trace.Start(f)
    if err != nil {
        panic(err)
    }
    defer trace.Stop()
    
    // Your application code here
    doWork()
}

func doWork() {
    // Create custom trace regions
    ctx := context.Background()
    
    trace.WithRegion(ctx, "database-query", func() {
        // Database operation
        time.Sleep(100 * time.Millisecond)
    })
    
    trace.WithRegion(ctx, "api-call", func() {
        // API call
        time.Sleep(50 * time.Millisecond)
    })
}

// Analyze trace:
// go tool trace trace.out
```

### 74. How do you implement custom HTTP client with retries?
**Answer:**
```go
type RetryClient struct {
    client      *http.Client
    maxRetries  int
    backoff     time.Duration
    retryableStatusCodes map[int]bool
}

func NewRetryClient(maxRetries int, backoff time.Duration) *RetryClient {
    return &RetryClient{
        client:     &http.Client{Timeout: 30 * time.Second},
        maxRetries: maxRetries,
        backoff:    backoff,
        retryableStatusCodes: map[int]bool{
            http.StatusInternalServerError: true,
            http.StatusBadGateway:          true,
            http.StatusServiceUnavailable:  true,
            http.StatusGatewayTimeout:      true,
        },
    }
}

func (rc *RetryClient) Do(req *http.Request) (*http.Response, error) {
    var resp *http.Response
    var err error
    
    for attempt := 0; attempt <= rc.maxRetries; attempt++ {
        // Clone request body for retries
        var bodyReader io.Reader
        if req.Body != nil {
            bodyBytes, _ := io.ReadAll(req.Body)
            bodyReader = bytes.NewReader(bodyBytes)
            req.Body = io.NopCloser(bytes.NewReader(bodyBytes))
        }
        
        resp, err = rc.client.Do(req)
        
        if err == nil && !rc.shouldRetry(resp.StatusCode) {
            return resp, nil
        }
        
        if attempt < rc.maxRetries {
            time.Sleep(rc.backoff * time.Duration(attempt+1))
            if bodyReader != nil {
                req.Body = io.NopCloser(bodyReader)
            }
        }
    }
    
    return resp, err
}

func (rc *RetryClient) shouldRetry(statusCode int) bool {
    return rc.retryableStatusCodes[statusCode]
}
```

### 75. What are Go's compiler directives and pragmas?
**Answer:**
```go
// Build constraints
//go:build linux && amd64

// Generate directive
//go:generate stringer -type=Status

// Embed directive (Go 1.16+)
//go:embed config.json
var configData []byte

//go:embed templates/*.html
var templates embed.FS

// Compiler directives
//go:noinline
func expensiveFunction() {
    // This function won't be inlined
}

//go:nosplit
func criticalFunction() {
    // This function won't check for stack overflow
}

//go:norace
func unsafeFunction() {
    // Race detector will ignore this function
}

//go:linkname localname importpath.name
// Links local name to external symbol

// Assembly function declaration
//go:noescape
func add(a, b int) int
```

### 76. How do you implement custom context values and cancellation?
**Answer:**
```go
type contextKey string

const (
    UserIDKey    contextKey = "userID"
    RequestIDKey contextKey = "requestID"
)

// Custom context with values
func WithUserID(ctx context.Context, userID string) context.Context {
    return context.WithValue(ctx, UserIDKey, userID)
}

func GetUserID(ctx context.Context) (string, bool) {
    userID, ok := ctx.Value(UserIDKey).(string)
    return userID, ok
}

// Custom cancellation
type CancelFunc func()

func WithCustomCancel(parent context.Context) (context.Context, CancelFunc) {
    ctx, cancel := context.WithCancel(parent)
    
    // Custom cleanup logic
    customCancel := func() {
        log.Println("Custom cleanup before cancellation")
        cancel()
    }
    
    return ctx, customCancel
}

// Usage
func processRequest(ctx context.Context) error {
    userID, ok := GetUserID(ctx)
    if !ok {
        return errors.New("user ID not found in context")
    }
    
    select {
    case <-ctx.Done():
        return ctx.Err()
    case <-time.After(5 * time.Second):
        log.Printf("Processing complete for user %s", userID)
        return nil
    }
}
```

### 77. What are Go's memory profiling techniques?
**Answer:**
```go
import (
    _ "net/http/pprof"
    "runtime/pprof"
)

// HTTP profiling endpoint
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()

// Manual memory profiling
func profileMemory() {
    f, err := os.Create("mem.prof")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()
    
    runtime.GC() // Force GC before profiling
    if err := pprof.WriteHeapProfile(f); err != nil {
        log.Fatal(err)
    }
}

// CPU profiling
func profileCPU() {
    f, err := os.Create("cpu.prof")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()
    
    if err := pprof.StartCPUProfile(f); err != nil {
        log.Fatal(err)
    }
    defer pprof.StopCPUProfile()
    
    // Your code here
}

// Analyze profiles:
// go tool pprof mem.prof
// go tool pprof cpu.prof
// go tool pprof http://localhost:6060/debug/pprof/heap
```

### 78. How do you implement custom serialization formats?
**Answer:**
```go
// Custom binary serialization
type Person struct {
    Name string
    Age  int32
}

func (p *Person) MarshalBinary() ([]byte, error) {
    buf := new(bytes.Buffer)
    
    // Write name length and name
    nameBytes := []byte(p.Name)
    binary.Write(buf, binary.LittleEndian, int32(len(nameBytes)))
    buf.Write(nameBytes)
    
    // Write age
    binary.Write(buf, binary.LittleEndian, p.Age)
    
    return buf.Bytes(), nil
}

func (p *Person) UnmarshalBinary(data []byte) error {
    buf := bytes.NewReader(data)
    
    // Read name length
    var nameLen int32
    if err := binary.Read(buf, binary.LittleEndian, &nameLen); err != nil {
        return err
    }
    
    // Read name
    nameBytes := make([]byte, nameLen)
    if _, err := buf.Read(nameBytes); err != nil {
        return err
    }
    p.Name = string(nameBytes)
    
    // Read age
    return binary.Read(buf, binary.LittleEndian, &p.Age)
}

// Protocol Buffers integration
//go:generate protoc --go_out=. person.proto

// MessagePack integration
import "github.com/vmihailenco/msgpack/v5"

func marshalMsgPack(v interface{}) ([]byte, error) {
    return msgpack.Marshal(v)
}

func unmarshalMsgPack(data []byte, v interface{}) error {
    return msgpack.Unmarshal(data, v)
}
```

### 79. What are Go's cross-compilation capabilities?
**Answer:**
```bash
# Cross-compile for different platforms
GOOS=linux GOARCH=amd64 go build -o app-linux main.go
GOOS=windows GOARCH=amd64 go build -o app-windows.exe main.go
GOOS=darwin GOARCH=amd64 go build -o app-macos main.go
GOOS=linux GOARCH=arm64 go build -o app-linux-arm64 main.go

# List supported platforms
go tool dist list

# Build for multiple platforms
#!/bin/bash
platforms=("windows/amd64" "linux/amd64" "darwin/amd64" "linux/arm64")

for platform in "${platforms[@]}"
do
    platform_split=(${platform//\// })
    GOOS=${platform_split[0]}
    GOARCH=${platform_split[1]}
    output_name='app-'$GOOS'-'$GOARCH
    if [ $GOOS = "windows" ]; then
        output_name+='.exe'
    fi
    
    env GOOS=$GOOS GOARCH=$GOARCH go build -o $output_name main.go
done
```

```go
// Platform-specific code
//go:build windows
package main

import "syscall"

func platformSpecific() {
    // Windows-specific code
    syscall.LoadLibrary("kernel32.dll")
}

//go:build linux
package main

import "syscall"

func platformSpecific() {
    // Linux-specific code
    syscall.Getpid()
}
```

### 80. How do you implement advanced Go testing patterns?
**Answer:**
```go
// Table-driven tests with subtests
func TestCalculator(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        op       string
        expected int
        wantErr  bool
    }{
        {"add positive", 2, 3, "+", 5, false},
        {"add negative", -2, 3, "+", 1, false},
        {"divide by zero", 5, 0, "/", 0, true},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result, err := Calculate(tt.a, tt.b, tt.op)
            
            if tt.wantErr {
                assert.Error(t, err)
                return
            }
            
            assert.NoError(t, err)
            assert.Equal(t, tt.expected, result)
        })
    }
}

// Test helpers and fixtures
func setupTestDB(t *testing.T) *sql.DB {
    db, err := sql.Open("sqlite3", ":memory:")
    require.NoError(t, err)
    
    t.Cleanup(func() {
        db.Close()
    })
    
    return db
}

// Mocking with interfaces
type UserService interface {
    GetUser(id string) (*User, error)
}

type MockUserService struct {
    users map[string]*User
}

func (m *MockUserService) GetUser(id string) (*User, error) {
    user, exists := m.users[id]
    if !exists {
        return nil, errors.New("user not found")
    }
    return user, nil
}

// Benchmark tests
func BenchmarkStringConcat(b *testing.B) {
    for i := 0; i < b.N; i++ {
        result := ""
        for j := 0; j < 1000; j++ {
            result += "hello"
        }
    }
}

func BenchmarkStringBuilder(b *testing.B) {
    for i := 0; i < b.N; i++ {
        var builder strings.Builder
        for j := 0; j < 1000; j++ {
            builder.WriteString("hello")
        }
        _ = builder.String()
    }
}

// Fuzzing (Go 1.18+)
func FuzzReverse(f *testing.F) {
    testcases := []string{"Hello, world", " ", "!12345"}
    for _, tc := range testcases {
        f.Add(tc)
    }
    
    f.Fuzz(func(t *testing.T, orig string) {
        rev := Reverse(orig)
        doubleRev := Reverse(rev)
        if orig != doubleRev {
            t.Errorf("Before: %q, after: %q", orig, doubleRev)
        }
    })
}
```

---

*This completes the comprehensive Go programming interview questions covering 80 essential topics with detailed answers and practical code examples.*