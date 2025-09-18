# 🦀 Rust Programming Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Ownership & Borrowing](#ownership--borrowing)
- [Data Types & Structs](#data-types--structs)
- [Error Handling](#error-handling)
- [Traits & Generics](#traits--generics)
- [Concurrency](#concurrency)
- [Advanced Topics](#advanced-topics)

---

## Basic Concepts

### 1. What is Rust and what are its key features?
**Answer:**
Rust is a systems programming language focused on safety, speed, and concurrency.

**Key Features:**
- **Memory safety**: No null pointers, buffer overflows, or memory leaks
- **Zero-cost abstractions**: High-level features with no runtime overhead
- **Ownership system**: Unique approach to memory management
- **Concurrency**: Safe concurrent programming
- **Performance**: Comparable to C and C++
- **Cross-platform**: Runs on many architectures

**Example:**
```rust
fn main() {
    println!("Hello, World!");
}
```

### 2. Explain Rust's ownership system.
**Answer:**
Ownership is Rust's unique approach to memory management without garbage collection.

**Ownership Rules:**
1. Each value has a single owner
2. When owner goes out of scope, value is dropped
3. Ownership can be transferred (moved)

**Example:**
```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;  // s1 is moved to s2
    
    // println!("{}", s1);  // Error: s1 no longer valid
    println!("{}", s2);     // OK: s2 owns the string
}

fn take_ownership(s: String) {
    println!("{}", s);
}  // s goes out of scope and is dropped
```

### 3. What are borrowing and references?
**Answer:**
Borrowing allows using values without taking ownership.

**Immutable References:**
```rust
fn main() {
    let s = String::from("hello");
    let len = calculate_length(&s);  // Borrow s
    println!("Length of '{}' is {}", s, len);  // s still valid
}

fn calculate_length(s: &String) -> usize {
    s.len()
}  // s goes out of scope but doesn't drop the value
```

**Mutable References:**
```rust
fn main() {
    let mut s = String::from("hello");
    change(&mut s);
    println!("{}", s);  // "hello, world"
}

fn change(s: &mut String) {
    s.push_str(", world");
}
```

### 4. What are lifetimes in Rust?
**Answer:**
Lifetimes ensure references are valid for as long as needed.

**Lifetime Annotations:**
```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// Struct with lifetime
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }
}
```

### 5. Explain Rust's type system and variables.
**Answer:**
**Variable Declaration:**
```rust
fn main() {
    let x = 5;              // Immutable
    let mut y = 10;         // Mutable
    
    // Type annotations
    let z: i32 = 15;
    let name: String = String::from("Rust");
    
    // Shadowing
    let x = x + 1;          // New variable, shadows previous x
    let x = x * 2;          // x is now 12
}
```

**Constants:**
```rust
const MAX_POINTS: u32 = 100_000;
```

---

## Ownership & Borrowing

### 6. What are the borrowing rules in Rust?
**Answer:**
**Borrowing Rules:**
1. Any number of immutable references OR one mutable reference
2. References must always be valid
3. No dangling references

**Examples:**
```rust
fn main() {
    let mut s = String::from("hello");
    
    // Multiple immutable references - OK
    let r1 = &s;
    let r2 = &s;
    println!("{} and {}", r1, r2);
    
    // Mutable reference after immutable ones are done - OK
    let r3 = &mut s;
    println!("{}", r3);
    
    // This would be an error:
    // let r4 = &s;  // Cannot borrow as immutable while mutable exists
}
```

### 7. How does move semantics work in Rust?
**Answer:**
**Move Semantics:**
```rust
fn main() {
    // Simple types (Copy trait) - copied, not moved
    let x = 5;
    let y = x;  // x is copied to y, both valid
    
    // Complex types - moved
    let s1 = String::from("hello");
    let s2 = s1;  // s1 is moved to s2
    
    // Clone to avoid move
    let s3 = String::from("world");
    let s4 = s3.clone();  // Deep copy, both valid
    
    println!("{} {}", s3, s4);
}

// Function parameters
fn takes_ownership(s: String) {
    println!("{}", s);
}  // s is dropped here

fn makes_copy(x: i32) {
    println!("{}", x);
}  // x goes out of scope, nothing special happens
```

### 8. What is the difference between Copy and Clone traits?
**Answer:**
**Copy Trait:**
- Implicit, automatic copying
- Only for types stored entirely on stack
- Cannot be implemented if type implements Drop

**Clone Trait:**
- Explicit copying via `.clone()`
- Can be expensive operation
- Works for any type

**Examples:**
```rust
// Copy types
let x = 5;
let y = x;  // Automatic copy

// Clone types
let s1 = String::from("hello");
let s2 = s1.clone();  // Explicit clone

// Custom struct with Copy
#[derive(Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

// Custom struct with Clone only
#[derive(Clone)]
struct Person {
    name: String,
    age: u32,
}
```

### 9. How do you handle ownership in collections?
**Answer:**
**Vec Ownership:**
```rust
fn main() {
    let mut v = Vec::new();
    v.push(String::from("hello"));
    v.push(String::from("world"));
    
    // Taking ownership from vector
    let first = v.remove(0);  // Removes and returns owned value
    
    // Borrowing from vector
    let second = &v[0];       // Immutable borrow
    
    // Iterating with different ownership
    for item in &v {          // Borrow each item
        println!("{}", item);
    }
    
    for item in v {           // Take ownership of each item
        println!("{}", item);
    }
    // v is no longer valid after consuming iterator
}
```

### 10. What are smart pointers in Rust?
**Answer:**
**Common Smart Pointers:**

**Box<T> - Heap Allocation:**
```rust
fn main() {
    let b = Box::new(5);
    println!("b = {}", b);
}

// Recursive type with Box
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

**Rc<T> - Reference Counting:**
```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(5);
    let b = Rc::clone(&a);
    let c = Rc::clone(&a);
    
    println!("Reference count: {}", Rc::strong_count(&a));  // 3
}
```

**RefCell<T> - Interior Mutability:**
```rust
use std::cell::RefCell;

fn main() {
    let value = RefCell::new(5);
    
    *value.borrow_mut() += 10;
    println!("Value: {}", value.borrow());
}
```

---

## Data Types & Structs

### 11. What are Rust's primitive data types?
**Answer:**
**Integer Types:**
```rust
let a: i8 = -128;      // 8-bit signed
let b: u8 = 255;       // 8-bit unsigned
let c: i32 = -2147483648;  // 32-bit signed (default)
let d: u64 = 18446744073709551615;  // 64-bit unsigned
let e: isize = -9223372036854775808;  // Architecture dependent
```

**Floating Point:**
```rust
let f: f32 = 3.14;     // 32-bit float
let g: f64 = 2.71828;  // 64-bit float (default)
```

**Other Types:**
```rust
let h: bool = true;
let i: char = '🦀';    // Unicode scalar value
let j: &str = "hello"; // String slice
```

### 12. How do you define and use structs?
**Answer:**
**Struct Types:**
```rust
// Classic struct
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

// Tuple struct
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

// Unit struct
struct AlwaysEqual;

// Usage
fn main() {
    let user1 = User {
        email: String::from("user@example.com"),
        username: String::from("user123"),
        active: true,
        sign_in_count: 1,
    };
    
    // Struct update syntax
    let user2 = User {
        email: String::from("another@example.com"),
        ..user1  // Use remaining fields from user1
    };
    
    let black = Color(0, 0, 0);
    let origin = Point(0, 0, 0);
}
```

### 13. What are enums and pattern matching?
**Answer:**
**Enum Definition:**
```rust
enum IpAddrKind {
    V4,
    V6,
}

enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

**Pattern Matching:**
```rust
fn main() {
    let ip = IpAddr::V4(127, 0, 0, 1);
    
    match ip {
        IpAddr::V4(a, b, c, d) => {
            println!("IPv4: {}.{}.{}.{}", a, b, c, d);
        }
        IpAddr::V6(addr) => {
            println!("IPv6: {}", addr);
        }
    }
    
    // if let for single pattern
    if let IpAddr::V4(127, 0, 0, 1) = ip {
        println!("Localhost IPv4");
    }
}
```

### 14. How do you work with Option and Result types?
**Answer:**
**Option<T>:**
```rust
fn divide(numerator: f64, denominator: f64) -> Option<f64> {
    if denominator == 0.0 {
        None
    } else {
        Some(numerator / denominator)
    }
}

fn main() {
    let result = divide(2.0, 3.0);
    
    match result {
        Some(x) => println!("Result: {}", x),
        None => println!("Cannot divide by 0"),
    }
    
    // Using unwrap_or
    let value = result.unwrap_or(0.0);
    
    // Using map
    let doubled = result.map(|x| x * 2.0);
}
```

**Result<T, E>:**
```rust
use std::fs::File;
use std::io::ErrorKind;

fn main() {
    let f = File::open("hello.txt");
    
    let f = match f {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => {
                match File::create("hello.txt") {
                    Ok(fc) => fc,
                    Err(e) => panic!("Problem creating file: {:?}", e),
                }
            }
            other_error => {
                panic!("Problem opening file: {:?}", other_error)
            }
        },
    };
}
```

### 15. What are arrays, vectors, and slices?
**Answer:**
**Arrays (Fixed Size):**
```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
let b = [3; 5];  // [3, 3, 3, 3, 3]

let first = a[0];
let slice = &a[1..3];  // [2, 3]
```

**Vectors (Dynamic):**
```rust
let mut v: Vec<i32> = Vec::new();
v.push(5);
v.push(6);

let v2 = vec![1, 2, 3];

// Accessing elements
let third: &i32 = &v2[2];
match v2.get(2) {
    Some(third) => println!("Third element: {}", third),
    None => println!("No third element"),
}

// Iterating
for i in &v2 {
    println!("{}", i);
}
```

**Slices:**
```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }
    
    &s[..]
}
```

---

## Error Handling

### 16. How does error handling work in Rust?
**Answer:**
**Result Type:**
```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut f = File::open("hello.txt")?;  // ? operator
    let mut s = String::new();
    f.read_to_string(&mut s)?;
    Ok(s)
}

// Equivalent without ? operator
fn read_username_verbose() -> Result<String, io::Error> {
    let f = File::open("hello.txt");
    
    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e),
    };
    
    let mut s = String::new();
    
    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
}
```

### 17. How do you create custom error types?
**Answer:**
**Custom Error Types:**
```rust
use std::fmt;

#[derive(Debug)]
enum MathError {
    DivisionByZero,
    NegativeLogarithm,
    NegativeSquareRoot,
}

impl fmt::Display for MathError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            MathError::DivisionByZero => write!(f, "Cannot divide by zero"),
            MathError::NegativeLogarithm => write!(f, "Cannot take log of negative number"),
            MathError::NegativeSquareRoot => write!(f, "Cannot take square root of negative number"),
        }
    }
}

impl std::error::Error for MathError {}

fn divide(a: f64, b: f64) -> Result<f64, MathError> {
    if b == 0.0 {
        Err(MathError::DivisionByZero)
    } else {
        Ok(a / b)
    }
}
```

### 18. What is the ? operator and how does it work?
**Answer:**
The ? operator is syntactic sugar for early return on errors.

**Usage:**
```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file() -> Result<String, io::Error> {
    let mut file = File::open("test.txt")?;  // Returns early if Err
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;     // Returns early if Err
    Ok(contents)                             // Returns Ok if all succeed
}

// Works with Option too
fn get_first_char(s: &str) -> Option<char> {
    s.chars().next()
}

fn get_first_char_of_first_line(text: &str) -> Option<char> {
    text.lines().next()?.chars().next()
}
```

### 19. How do you handle multiple error types?
**Answer:**
**Using Box<dyn Error>:**
```rust
use std::error::Error;
use std::fs::File;
use std::io::Read;

fn run() -> Result<(), Box<dyn Error>> {
    let mut file = File::open("hello.txt")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    
    let num: i32 = contents.trim().parse()?;
    println!("Number: {}", num);
    
    Ok(())
}
```

**Custom Error Enum:**
```rust
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
}

impl From<std::io::Error> for AppError {
    fn from(error: std::io::Error) -> Self {
        AppError::Io(error)
    }
}

impl From<std::num::ParseIntError> for AppError {
    fn from(error: std::num::ParseIntError) -> Self {
        AppError::Parse(error)
    }
}

fn run_app() -> Result<i32, AppError> {
    let mut file = File::open("number.txt")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    let num: i32 = contents.trim().parse()?;
    Ok(num)
}
```

### 20. When should you use panic! vs Result?
**Answer:**
**Use panic! when:**
- Unrecoverable errors
- Programming errors (bugs)
- Prototype/example code

**Use Result when:**
- Recoverable errors
- Expected failure conditions
- Library code

**Examples:**
```rust
// panic! for unrecoverable errors
fn get_item(index: usize, items: &[String]) -> &String {
    if index >= items.len() {
        panic!("Index {} out of bounds for length {}", index, items.len());
    }
    &items[index]
}

// Result for recoverable errors
fn safe_get_item(index: usize, items: &[String]) -> Option<&String> {
    if index < items.len() {
        Some(&items[index])
    } else {
        None
    }
}

// Custom panic message
fn divide(a: f64, b: f64) -> f64 {
    if b == 0.0 {
        panic!("Division by zero is not allowed!");
    }
    a / b
}
```

---

## Traits & Generics

### 21. What are traits in Rust?
**Answer:**
Traits define shared behavior across types.

**Trait Definition:**
```rust
trait Summary {
    fn summarize(&self) -> String;
    
    // Default implementation
    fn summarize_author(&self) -> String {
        format!("(Read more from {}...)", self.summarize())
    }
}

struct NewsArticle {
    headline: String,
    location: String,
    author: String,
    content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

struct Tweet {
    username: String,
    content: String,
    reply: bool,
    retweet: bool,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}
```

### 22. How do generics work in Rust?
**Answer:**
**Generic Functions:**
```rust
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut largest = list[0];
    
    for &item in list {
        if item > largest {
            largest = item;
        }
    }
    
    largest
}

// Multiple type parameters
fn compare<T, U>(a: T, b: U) -> bool 
where
    T: PartialEq<U>,
{
    a == b
}
```

**Generic Structs:**
```rust
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn new(x: T, y: T) -> Self {
        Point { x, y }
    }
}

impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

### 23. What are trait bounds and where clauses?
**Answer:**
**Trait Bounds:**
```rust
// Inline trait bounds
fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

// Multiple trait bounds
fn notify_display<T: Summary + Display>(item: &T) {
    println!("{}", item);
}

// Where clause for complex bounds
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{
    // Function body
    0
}
```

**Trait Objects:**
```rust
// Static dispatch
fn notify_static<T: Summary>(item: &T) {
    println!("{}", item.summarize());
}

// Dynamic dispatch
fn notify_dynamic(item: &dyn Summary) {
    println!("{}", item.summarize());
}

// Vector of trait objects
let articles: Vec<Box<dyn Summary>> = vec![
    Box::new(NewsArticle { /* ... */ }),
    Box::new(Tweet { /* ... */ }),
];
```

### 24. How do you implement common traits?
**Answer:**
**Derive Macros:**
```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Person {
    name: String,
    age: u32,
}

// Manual implementation
impl Display for Person {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} (age {})", self.name, self.age)
    }
}

impl PartialOrd for Person {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Person {
    fn cmp(&self, other: &Self) -> Ordering {
        self.age.cmp(&other.age)
    }
}
```

### 25. What are associated types in traits?
**Answer:**
**Associated Types:**
```rust
trait Iterator {
    type Item;  // Associated type
    
    fn next(&mut self) -> Option<Self::Item>;
}

struct Counter {
    current: usize,
    max: usize,
}

impl Iterator for Counter {
    type Item = usize;  // Concrete type
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.max {
            let current = self.current;
            self.current += 1;
            Some(current)
        } else {
            None
        }
    }
}

// Generic vs Associated Types
trait Add<Rhs = Self> {  // Generic type parameter
    type Output;         // Associated type
    
    fn add(self, rhs: Rhs) -> Self::Output;
}
```

---

## Concurrency

### 26. How does Rust handle concurrency?
**Answer:**
**Thread Creation:**
```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {} from spawned thread!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });
    
    for i in 1..5 {
        println!("hi number {} from main thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
    
    handle.join().unwrap();  // Wait for thread to finish
}
```

**Moving Data:**
```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];
    
    let handle = thread::spawn(move || {
        println!("Vector: {:?}", v);
    });
    
    handle.join().unwrap();
}
```

### 27. What are channels and how do you use them?
**Answer:**
**Message Passing:**
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
    });
    
    let received = rx.recv().unwrap();
    println!("Got: {}", received);
}

// Multiple producers
fn multiple_producers() {
    let (tx, rx) = mpsc::channel();
    
    let tx1 = tx.clone();
    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];
        
        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });
    
    thread::spawn(move || {
        let vals = vec![
            String::from("more"),
            String::from("messages"),
            String::from("for"),
            String::from("you"),
        ];
        
        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });
    
    for received in rx {
        println!("Got: {}", received);
    }
}
```

### 28. How do you share state between threads?
**Answer:**
**Mutex:**
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];
    
    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("Result: {}", *counter.lock().unwrap());
}
```

**RwLock:**
```rust
use std::sync::{Arc, RwLock};
use std::thread;

fn main() {
    let data = Arc::new(RwLock::new(vec![1, 2, 3]));
    let mut handles = vec![];
    
    // Multiple readers
    for i in 0..5 {
        let data = Arc::clone(&data);
        let handle = thread::spawn(move || {
            let data = data.read().unwrap();
            println!("Reader {}: {:?}", i, *data);
        });
        handles.push(handle);
    }
    
    // One writer
    let data_clone = Arc::clone(&data);
    let handle = thread::spawn(move || {
        let mut data = data_clone.write().unwrap();
        data.push(4);
    });
    handles.push(handle);
    
    for handle in handles {
        handle.join().unwrap();
    }
}
```

### 29. What are async/await and futures?
**Answer:**
**Async Functions:**
```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("Result: {}", result);
}

async fn fetch_data() -> String {
    // Simulate async work
    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
    "Data fetched".to_string()
}

// Multiple async operations
async fn fetch_multiple() {
    let (result1, result2) = tokio::join!(
        fetch_data(),
        fetch_data()
    );
    
    println!("Results: {} and {}", result1, result2);
}
```

**Custom Future:**
```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct TimerFuture {
    shared_state: Arc<Mutex<SharedState>>,
}

struct SharedState {
    completed: bool,
    waker: Option<Waker>,
}

impl Future for TimerFuture {
    type Output = ();
    
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let mut shared_state = self.shared_state.lock().unwrap();
        if shared_state.completed {
            Poll::Ready(())
        } else {
            shared_state.waker = Some(cx.waker().clone());
            Poll::Pending
        }
    }
}
```

### 30. How do you handle errors in concurrent code?
**Answer:**
**Thread Error Handling:**
```rust
use std::thread;
use std::panic;

fn main() {
    let handle = thread::spawn(|| {
        panic!("Thread panicked!");
    });
    
    match handle.join() {
        Ok(_) => println!("Thread completed successfully"),
        Err(e) => println!("Thread panicked: {:?}", e),
    }
}

// Catching panics
fn safe_thread_execution() {
    let result = panic::catch_unwind(|| {
        // Code that might panic
        panic!("Something went wrong!");
    });
    
    match result {
        Ok(_) => println!("No panic occurred"),
        Err(_) => println!("Panic was caught"),
    }
}
```

**Channel Error Handling:**
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    thread::spawn(move || {
        for i in 0..5 {
            if tx.send(i).is_err() {
                println!("Receiver has been dropped");
                break;
            }
        }
    });
    
    // Receive only first 3 messages
    for _ in 0..3 {
        match rx.recv() {
            Ok(value) => println!("Received: {}", value),
            Err(_) => println!("Sender has been dropped"),
        }
    }
    // rx is dropped here, causing send to fail
}
```

---

## Advanced Topics

### 31. What are macros in Rust?
**Answer:**
**Declarative Macros:**
```rust
macro_rules! vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}

// Custom macro
macro_rules! say_hello {
    () => {
        println!("Hello!");
    };
    ($name:expr) => {
        println!("Hello, {}!", $name);
    };
}

fn main() {
    say_hello!();
    say_hello!("World");
}
```

**Procedural Macros:**
```rust
// In Cargo.toml: proc-macro = true

use proc_macro::TokenStream;
use quote::quote;
use syn;

#[proc_macro_derive(HelloMacro)]
pub fn hello_macro_derive(input: TokenStream) -> TokenStream {
    let ast = syn::parse(input).unwrap();
    impl_hello_macro(&ast)
}

fn impl_hello_macro(ast: &syn::DeriveInput) -> TokenStream {
    let name = &ast.ident;
    let gen = quote! {
        impl HelloMacro for #name {
            fn hello_macro() {
                println!("Hello, Macro! My name is {}!", stringify!(#name));
            }
        }
    };
    gen.into()
}
```

### 32. How do you work with unsafe Rust?
**Answer:**
**Unsafe Superpowers:**
```rust
fn main() {
    let mut num = 5;
    
    let r1 = &num as *const i32;      // Raw pointer
    let r2 = &mut num as *mut i32;    // Mutable raw pointer
    
    unsafe {
        println!("r1 is: {}", *r1);   // Dereference raw pointer
        println!("r2 is: {}", *r2);
    }
}

// Unsafe function
unsafe fn dangerous() {
    // Unsafe operations
}

fn main() {
    unsafe {
        dangerous();  // Must be called in unsafe block
    }
}

// Safe abstraction over unsafe code
use std::slice;

fn split_at_mut(slice: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = slice.len();
    let ptr = slice.as_mut_ptr();
    
    assert!(mid <= len);
    
    unsafe {
        (
            slice::from_raw_parts_mut(ptr, mid),
            slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}
```

### 33. What are closures and how do they work?
**Answer:**
**Closure Syntax:**
```rust
fn main() {
    let expensive_closure = |num: u32| -> u32 {
        println!("calculating slowly...");
        thread::sleep(Duration::from_secs(2));
        num
    };
    
    // Type inference
    let add_one = |x| x + 1;
    let add_one_v2 = |x: i32| -> i32 { x + 1 };
    
    println!("Result: {}", expensive_closure(5));
}

// Capturing environment
fn main() {
    let x = 4;
    
    let equal_to_x = |z| z == x;  // Captures x
    
    println!("{}", equal_to_x(4));
}

// Move closures
fn main() {
    let x = vec![1, 2, 3];
    
    let equal_to_x = move |z| z == x;  // Takes ownership of x
    
    // println!("can't use x here: {:?}", x);  // Error: x moved
    
    let y = vec![1, 2, 3];
    assert!(equal_to_x(y));
}
```

### 34. How do you implement iterators?
**Answer:**
**Iterator Trait:**
```rust
struct Counter {
    current: usize,
    max: usize,
}

impl Counter {
    fn new(max: usize) -> Counter {
        Counter { current: 0, max }
    }
}

impl Iterator for Counter {
    type Item = usize;
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.max {
            let current = self.current;
            self.current += 1;
            Some(current)
        } else {
            None
        }
    }
}

fn main() {
    let mut counter = Counter::new(5);
    
    // Using iterator
    for num in counter {
        println!("{}", num);
    }
    
    // Iterator adaptors
    let sum: usize = Counter::new(5)
        .zip(Counter::new(5).skip(1))
        .map(|(a, b)| a * b)
        .filter(|x| x % 3 == 0)
        .sum();
    
    println!("Sum: {}", sum);
}
```

### 35. What are Rust's performance characteristics and optimization techniques?
**Answer:**
**Zero-Cost Abstractions:**
```rust
// High-level code compiles to same assembly as low-level
let sum: i32 = (0..1_000_000)
    .map(|x| x * x)
    .filter(|x| x % 2 == 0)
    .sum();

// Equivalent low-level code
let mut sum = 0;
for i in 0..1_000_000 {
    let square = i * i;
    if square % 2 == 0 {
        sum += square;
    }
}
```

**Performance Tips:**
```rust
// 1. Use appropriate data structures
use std::collections::HashMap;
let mut map = HashMap::with_capacity(1000);  // Pre-allocate

// 2. Avoid unnecessary allocations
fn process_string(s: &str) -> &str {  // Use &str instead of String
    // Process without allocation
    s
}

// 3. Use iterators instead of loops
let doubled: Vec<i32> = numbers.iter().map(|x| x * 2).collect();

// 4. Profile and benchmark
#[cfg(test)]
mod benches {
    use test::Bencher;
    
    #[bench]
    fn bench_function(b: &mut Bencher) {
        b.iter(|| {
            // Code to benchmark
        });
    }
}
```

---

*This comprehensive guide covers 35+ essential Rust programming interview questions with detailed answers and practical examples for systems programming interviews.*