# 🚀 Go Programming Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Data Types & Variables](#data-types--variables)
- [Functions & Methods](#functions--methods)
- [Concurrency](#concurrency)
- [Interfaces & Structs](#interfaces--structs)
- [Error Handling](#error-handling)
- [Performance & Best Practices](#performance--best-practices)

---

## Basic Concepts

### 1. What is Go and what are its key features?
**Answer:**
Go is a statically typed, compiled programming language developed by Google.

**Key Features:**
- **Fast compilation**: Quick build times
- **Garbage collection**: Automatic memory management
- **Concurrency**: Built-in goroutines and channels
- **Simple syntax**: Easy to learn and read
- **Static typing**: Type safety at compile time
- **Cross-platform**: Compiles to multiple architectures

**Example:**
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

### 2. Explain Go's package system and imports.
**Answer:**
Go organizes code into packages for modularity and reusability.

**Package Declaration:**
```go
package main  // Executable package

package utils // Library package
```

**Imports:**
```go
import (
    "fmt"           // Standard library
    "net/http"      // Standard library
    "github.com/user/repo"  // External package
    . "math"        // Dot import (not recommended)
    _ "database/sql/driver"  // Blank import
)
```

### 3. What are goroutines and how do they work?
**Answer:**
Goroutines are lightweight threads managed by Go runtime.

**Basic Usage:**
```go
func main() {
    go sayHello()  // Start goroutine
    go func() {    // Anonymous goroutine
        fmt.Println("Anonymous goroutine")
    }()
    
    time.Sleep(time.Second) // Wait for goroutines
}

func sayHello() {
    fmt.Println("Hello from goroutine")
}
```

**Characteristics:**
- Lightweight (2KB initial stack)
- Multiplexed onto OS threads
- Managed by Go scheduler

### 4. Explain channels in Go.
**Answer:**
Channels are used for communication between goroutines.

**Channel Types:**
```go
// Unbuffered channel
ch := make(chan int)

// Buffered channel
ch := make(chan int, 5)

// Send and receive
ch <- 42        // Send
value := <-ch   // Receive

// Close channel
close(ch)
```

**Channel Directions:**
```go
func send(ch chan<- int) {  // Send-only
    ch <- 42
}

func receive(ch <-chan int) {  // Receive-only
    value := <-ch
}
```

### 5. What is the difference between arrays and slices?
**Answer:**
**Arrays:**
- Fixed size
- Value types
- Size is part of type

**Slices:**
- Dynamic size
- Reference types
- Built on arrays

**Examples:**
```go
// Array
var arr [5]int = [5]int{1, 2, 3, 4, 5}

// Slice
var slice []int = []int{1, 2, 3, 4, 5}
slice = append(slice, 6)  // Dynamic growth

// Slice from array
s := arr[1:4]  // Elements 1, 2, 3
```

---

## Data Types & Variables

### 6. What are Go's basic data types?
**Answer:**
**Numeric Types:**
```go
// Integers
var i int = 42
var i8 int8 = 127
var ui uint = 42

// Floating point
var f32 float32 = 3.14
var f64 float64 = 3.14159

// Complex
var c complex64 = 1 + 2i
```

**Other Types:**
```go
// Boolean
var b bool = true

// String
var s string = "Hello"

// Byte (alias for uint8)
var bt byte = 255

// Rune (alias for int32)
var r rune = 'A'
```

### 7. Explain variable declaration in Go.
**Answer:**
**Declaration Methods:**
```go
// Explicit type
var name string = "John"

// Type inference
var age = 30

// Short declaration (inside functions only)
city := "New York"

// Multiple variables
var (
    x int
    y string
    z bool
)

// Multiple assignment
a, b := 1, 2
```

### 8. What are pointers in Go?
**Answer:**
Pointers store memory addresses of variables.

**Basic Usage:**
```go
func main() {
    x := 42
    p := &x    // Get address of x
    
    fmt.Println(*p)  // Dereference pointer (42)
    *p = 100         // Modify value through pointer
    fmt.Println(x)   // x is now 100
}
```

**Pointer vs Value:**
```go
func modifyValue(x int) {
    x = 100  // Only modifies copy
}

func modifyPointer(x *int) {
    *x = 100  // Modifies original value
}
```

### 9. Explain structs in Go.
**Answer:**
Structs group related data together.

**Definition and Usage:**
```go
type Person struct {
    Name string
    Age  int
    City string
}

// Creation
p1 := Person{Name: "John", Age: 30, City: "NYC"}
p2 := Person{"Jane", 25, "LA"}  // Positional

// Access fields
fmt.Println(p1.Name)
p1.Age = 31
```

**Embedded Structs:**
```go
type Address struct {
    Street string
    City   string
}

type Employee struct {
    Person   // Embedded struct
    Address  // Embedded struct
    Salary   int
}
```

### 10. What are maps in Go?
**Answer:**
Maps are key-value data structures.

**Basic Operations:**
```go
// Declaration
m := make(map[string]int)
m2 := map[string]int{
    "apple":  5,
    "banana": 3,
}

// Operations
m["key"] = 42           // Set
value := m["key"]       // Get
delete(m, "key")        // Delete

// Check existence
value, ok := m["key"]
if ok {
    fmt.Println("Key exists:", value)
}
```

---

## Functions & Methods

### 11. How do you define functions in Go?
**Answer:**
**Basic Function:**
```go
func add(a, b int) int {
    return a + b
}

// Multiple return values
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Named return values
func calculate(a, b int) (sum, product int) {
    sum = a + b
    product = a * b
    return  // Naked return
}
```

### 12. What are methods in Go?
**Answer:**
Methods are functions with receiver arguments.

**Method Definition:**
```go
type Rectangle struct {
    Width, Height float64
}

// Value receiver
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// Pointer receiver
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}

// Usage
rect := Rectangle{Width: 10, Height: 5}
fmt.Println(rect.Area())  // 50
rect.Scale(2)             // Modifies rect
```

### 13. Explain variadic functions in Go.
**Answer:**
Variadic functions accept variable number of arguments.

**Definition:**
```go
func sum(numbers ...int) int {
    total := 0
    for _, num := range numbers {
        total += num
    }
    return total
}

// Usage
result1 := sum(1, 2, 3)
result2 := sum(1, 2, 3, 4, 5)

// Spread slice
nums := []int{1, 2, 3, 4}
result3 := sum(nums...)
```

### 14. What are closures in Go?
**Answer:**
Closures are functions that capture variables from outer scope.

**Example:**
```go
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

func main() {
    c1 := counter()
    c2 := counter()
    
    fmt.Println(c1()) // 1
    fmt.Println(c1()) // 2
    fmt.Println(c2()) // 1 (separate closure)
}
```

### 15. How do you handle function types and callbacks?
**Answer:**
Functions are first-class citizens in Go.

**Function Types:**
```go
type Operation func(int, int) int

func add(a, b int) int { return a + b }
func multiply(a, b int) int { return a * b }

func calculate(a, b int, op Operation) int {
    return op(a, b)
}

// Usage
result1 := calculate(5, 3, add)      // 8
result2 := calculate(5, 3, multiply) // 15

// Anonymous function
result3 := calculate(5, 3, func(a, b int) int {
    return a - b
})
```

---

## Concurrency

### 16. Explain the select statement in Go.
**Answer:**
Select allows goroutine to wait on multiple channel operations.

**Basic Select:**
```go
func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)
    
    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- "from ch1"
    }()
    
    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "from ch2"
    }()
    
    select {
    case msg1 := <-ch1:
        fmt.Println(msg1)
    case msg2 := <-ch2:
        fmt.Println(msg2)
    case <-time.After(3 * time.Second):
        fmt.Println("timeout")
    }
}
```

### 17. What is the sync package and when to use it?
**Answer:**
Sync package provides synchronization primitives.

**Mutex:**
```go
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}
```

**WaitGroup:**
```go
func main() {
    var wg sync.WaitGroup
    
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Worker %d done\n", id)
        }(i)
    }
    
    wg.Wait()
    fmt.Println("All workers completed")
}
```

### 18. How do you implement worker pools in Go?
**Answer:**
Worker pools manage concurrent task processing.

**Implementation:**
```go
func workerPool(jobs <-chan int, results chan<- int) {
    for job := range jobs {
        // Simulate work
        time.Sleep(time.Millisecond * 100)
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    
    // Start workers
    for w := 1; w <= 3; w++ {
        go workerPool(jobs, results)
    }
    
    // Send jobs
    for j := 1; j <= 9; j++ {
        jobs <- j
    }
    close(jobs)
    
    // Collect results
    for r := 1; r <= 9; r++ {
        <-results
    }
}
```

### 19. What are context and cancellation in Go?
**Answer:**
Context carries deadlines, cancellation signals, and request-scoped values.

**Usage:**
```go
func doWork(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()  // Cancelled or timed out
        default:
            // Do work
            time.Sleep(100 * time.Millisecond)
        }
    }
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()
    
    if err := doWork(ctx); err != nil {
        fmt.Println("Work cancelled:", err)
    }
}
```

### 20. How do you prevent race conditions?
**Answer:**
**Detection:**
```bash
go run -race main.go  # Race detector
```

**Prevention Methods:**
```go
// 1. Mutex
type SafeCounter struct {
    mu sync.Mutex
    v  map[string]int
}

func (c *SafeCounter) Inc(key string) {
    c.mu.Lock()
    c.v[key]++
    c.mu.Unlock()
}

// 2. Channels
func safeIncrement(ch chan int) {
    for i := 0; i < 1000; i++ {
        ch <- 1
    }
}

// 3. Atomic operations
var counter int64

func atomicIncrement() {
    atomic.AddInt64(&counter, 1)
}
```

---

## Interfaces & Structs

### 21. How do interfaces work in Go?
**Answer:**
Interfaces define method signatures and are implemented implicitly.

**Definition:**
```go
type Writer interface {
    Write([]byte) (int, error)
}

type Shape interface {
    Area() float64
    Perimeter() float64
}

// Implementation (implicit)
type Rectangle struct {
    Width, Height float64
}

func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

func (r Rectangle) Perimeter() float64 {
    return 2 * (r.Width + r.Height)
}
```

### 22. What is the empty interface?
**Answer:**
Empty interface can hold values of any type.

**Usage:**
```go
func describe(i interface{}) {
    fmt.Printf("Type: %T, Value: %v\n", i, i)
}

func main() {
    describe(42)
    describe("hello")
    describe([]int{1, 2, 3})
}

// Type assertion
func process(i interface{}) {
    switch v := i.(type) {
    case int:
        fmt.Printf("Integer: %d\n", v)
    case string:
        fmt.Printf("String: %s\n", v)
    default:
        fmt.Printf("Unknown type: %T\n", v)
    }
}
```

### 23. Explain struct embedding and composition.
**Answer:**
Go uses composition over inheritance through embedding.

**Embedding:**
```go
type Engine struct {
    Power int
}

func (e Engine) Start() {
    fmt.Println("Engine started")
}

type Car struct {
    Engine  // Embedded struct
    Brand   string
    Model   string
}

func main() {
    car := Car{
        Engine: Engine{Power: 200},
        Brand:  "Toyota",
        Model:  "Camry",
    }
    
    car.Start()  // Method promoted from Engine
    fmt.Println(car.Power)  // Field promoted from Engine
}
```

### 24. How do you implement polymorphism in Go?
**Answer:**
Polymorphism through interfaces and method sets.

**Example:**
```go
type Animal interface {
    Speak() string
}

type Dog struct {
    Name string
}

func (d Dog) Speak() string {
    return "Woof!"
}

type Cat struct {
    Name string
}

func (c Cat) Speak() string {
    return "Meow!"
}

func makeSound(a Animal) {
    fmt.Println(a.Speak())
}

func main() {
    animals := []Animal{
        Dog{Name: "Buddy"},
        Cat{Name: "Whiskers"},
    }
    
    for _, animal := range animals {
        makeSound(animal)  // Polymorphic behavior
    }
}
```

### 25. What are method sets in Go?
**Answer:**
Method sets determine which methods are available for a type.

**Rules:**
```go
type T struct{}

func (t T) ValueMethod() {}     // Value receiver
func (t *T) PointerMethod() {}  // Pointer receiver

// Method sets:
// T has method set: ValueMethod
// *T has method set: ValueMethod, PointerMethod

func main() {
    var t T
    var pt *T = &t
    
    t.ValueMethod()    // OK
    pt.ValueMethod()   // OK (automatic dereferencing)
    pt.PointerMethod() // OK
    // t.PointerMethod() // Would work due to automatic addressing
}
```

---

## Error Handling

### 26. How does error handling work in Go?
**Answer:**
Go uses explicit error values instead of exceptions.

**Basic Error Handling:**
```go
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)
}
```

### 27. How do you create custom errors?
**Answer:**
**Custom Error Types:**
```go
type ValidationError struct {
    Field   string
    Message string
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("validation error in field '%s': %s", e.Field, e.Message)
}

func validateAge(age int) error {
    if age < 0 {
        return ValidationError{
            Field:   "age",
            Message: "must be non-negative",
        }
    }
    return nil
}

// Error wrapping (Go 1.13+)
func processUser(id int) error {
    user, err := getUser(id)
    if err != nil {
        return fmt.Errorf("failed to process user %d: %w", id, err)
    }
    // Process user...
    return nil
}
```

### 28. What is panic and recover?
**Answer:**
Panic stops normal execution; recover regains control.

**Usage:**
```go
func riskyFunction() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered from panic:", r)
        }
    }()
    
    panic("something went wrong")
    fmt.Println("This won't be printed")
}

func main() {
    riskyFunction()
    fmt.Println("Program continues")
}
```

**When to Use:**
- Panic: Unrecoverable errors
- Recover: Cleanup in defer functions
- Prefer errors over panic for normal error handling

### 29. How do you handle errors in concurrent code?
**Answer:**
**Error Channels:**
```go
func worker(id int, jobs <-chan int, results chan<- int, errors chan<- error) {
    for job := range jobs {
        if job < 0 {
            errors <- fmt.Errorf("worker %d: invalid job %d", id, job)
            continue
        }
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 5)
    results := make(chan int, 5)
    errors := make(chan error, 5)
    
    go worker(1, jobs, results, errors)
    
    // Send jobs
    for i := -1; i <= 3; i++ {
        jobs <- i
    }
    close(jobs)
    
    // Handle results and errors
    for i := 0; i < 5; i++ {
        select {
        case result := <-results:
            fmt.Println("Result:", result)
        case err := <-errors:
            fmt.Println("Error:", err)
        }
    }
}
```

### 30. What are best practices for error handling?
**Answer:**
**Best Practices:**
```go
// 1. Check errors immediately
file, err := os.Open("file.txt")
if err != nil {
    return err
}
defer file.Close()

// 2. Wrap errors with context
func readConfig() error {
    data, err := ioutil.ReadFile("config.json")
    if err != nil {
        return fmt.Errorf("failed to read config: %w", err)
    }
    // Process data...
    return nil
}

// 3. Use sentinel errors for expected conditions
var ErrNotFound = errors.New("item not found")

func findItem(id int) (*Item, error) {
    // Search logic...
    if !found {
        return nil, ErrNotFound
    }
    return item, nil
}

// 4. Handle errors at appropriate level
func main() {
    if err := run(); err != nil {
        log.Fatal(err)
    }
}
```

---

## Performance & Best Practices

### 31. How do you optimize Go code performance?
**Answer:**
**Profiling:**
```go
import _ "net/http/pprof"

func main() {
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()
    
    // Your application code
}
```

**Optimization Techniques:**
```go
// 1. Use string builder for concatenation
var builder strings.Builder
for i := 0; i < 1000; i++ {
    builder.WriteString("hello")
}
result := builder.String()

// 2. Preallocate slices
slice := make([]int, 0, 1000)  // Capacity 1000

// 3. Use sync.Pool for object reuse
var pool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 1024)
    },
}

buf := pool.Get().([]byte)
defer pool.Put(buf)
```

### 32. What are Go's memory management best practices?
**Answer:**
**Memory Optimization:**
```go
// 1. Avoid memory leaks in slices
func processLargeSlice(data []int) []int {
    // Bad: keeps reference to large underlying array
    return data[100:110]
    
    // Good: copy to new slice
    result := make([]int, 10)
    copy(result, data[100:110])
    return result
}

// 2. Use pointers for large structs
type LargeStruct struct {
    data [1000]int
}

func processStruct(s *LargeStruct) {  // Pass by pointer
    // Process struct
}

// 3. Be careful with goroutine leaks
func leakyGoroutine() {
    ch := make(chan int)
    go func() {
        for {
            select {
            case <-ch:
                return
            default:
                // Work that never ends - LEAK!
            }
        }
    }()
    // Forgot to close ch or send signal
}
```

### 33. How do you write testable Go code?
**Answer:**
**Testing Structure:**
```go
// math.go
func Add(a, b int) int {
    return a + b
}

// math_test.go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -1, -2, -3},
        {"zero", 0, 5, 5},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", 
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

**Benchmarking:**
```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(1, 2)
    }
}
```

### 34. What are Go modules and dependency management?
**Answer:**
**Module Management:**
```bash
# Initialize module
go mod init github.com/user/project

# Add dependency
go get github.com/gorilla/mux

# Update dependencies
go mod tidy

# Vendor dependencies
go mod vendor
```

**go.mod file:**
```go
module github.com/user/project

go 1.19

require (
    github.com/gorilla/mux v1.8.0
    github.com/stretchr/testify v1.7.0
)

replace github.com/old/package => github.com/new/package v1.0.0
```

### 35. What are Go's coding conventions and best practices?
**Answer:**
**Naming Conventions:**
```go
// Exported (public) - starts with capital letter
func PublicFunction() {}
type PublicStruct struct{}

// Unexported (private) - starts with lowercase
func privateFunction() {}
type privateStruct struct{}

// Interface naming
type Reader interface{}  // -er suffix
type Writer interface{}
```

**Code Organization:**
```go
// Package structure
project/
├── cmd/           // Main applications
├── internal/      // Private application code
├── pkg/          // Public library code
├── api/          // API definitions
├── web/          // Web application assets
└── scripts/      // Build and deployment scripts
```

**Best Practices:**
- Keep functions small and focused
- Use meaningful variable names
- Handle errors explicitly
- Write tests for public APIs
- Use gofmt for consistent formatting
- Run golint and go vet regularly

---

*This comprehensive guide covers 35+ essential Go programming interview questions with detailed answers and practical examples for software engineering interviews.*