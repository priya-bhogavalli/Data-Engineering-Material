# 🎯 Scala Programming Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Object-Oriented Programming](#object-oriented-programming)
- [Functional Programming](#functional-programming)
- [Collections](#collections)
- [Pattern Matching](#pattern-matching)
- [Concurrency](#concurrency)
- [Advanced Topics](#advanced-topics)

---

## Basic Concepts

### 1. What is Scala and what are its key features?
**Answer:**
Scala is a multi-paradigm programming language that combines object-oriented and functional programming.

**Key Features:**
- **Statically typed**: Type safety at compile time
- **JVM-based**: Runs on Java Virtual Machine
- **Functional + OOP**: Supports both paradigms
- **Concise syntax**: Less boilerplate than Java
- **Immutable by default**: Encourages immutability
- **Pattern matching**: Powerful matching capabilities

**Example:**
```scala
object HelloWorld {
  def main(args: Array[String]): Unit = {
    println("Hello, Scala!")
  }
}
```

### 2. Explain Scala's type system and type inference.
**Answer:**
**Type System:**
```scala
// Explicit types
val name: String = "John"
val age: Int = 30
val height: Double = 5.9

// Type inference
val inferredName = "Jane"        // String
val inferredAge = 25             // Int
val inferredHeight = 6.1         // Double

// Generic types
val numbers: List[Int] = List(1, 2, 3)
val pairs: Map[String, Int] = Map("a" -> 1, "b" -> 2)

// Function types
val add: (Int, Int) => Int = (x, y) => x + y
val multiply = (x: Int, y: Int) => x * y  // Inferred type
```

### 3. What are val, var, and def in Scala?
**Answer:**
**val (Immutable Value):**
```scala
val x = 10
// x = 20  // Compilation error - cannot reassign

val list = List(1, 2, 3)
// list = List(4, 5, 6)  // Error - cannot reassign reference
// But can modify mutable contents if applicable
```

**var (Mutable Variable):**
```scala
var y = 10
y = 20  // OK - can reassign

var mutableList = scala.collection.mutable.ListBuffer(1, 2, 3)
mutableList += 4  // OK - can modify
```

**def (Method/Function Definition):**
```scala
def square(x: Int): Int = x * x

// Lazy evaluation - computed each time called
def currentTime = System.currentTimeMillis()

// Method with multiple parameter lists
def multiply(x: Int)(y: Int): Int = x * y
```

### 4. How do you define and use functions in Scala?
**Answer:**
**Function Definition:**
```scala
// Method definition
def add(x: Int, y: Int): Int = x + y

// Function value
val addFunc: (Int, Int) => Int = (x, y) => x + y

// Anonymous function
val square = (x: Int) => x * x

// Higher-order function
def applyTwice(f: Int => Int, x: Int): Int = f(f(x))

val result = applyTwice(square, 3)  // 81

// Curried function
def curriedAdd(x: Int)(y: Int): Int = x + y
val addFive = curriedAdd(5) _  // Partial application
```

### 5. What are case classes and objects in Scala?
**Answer:**
**Case Classes:**
```scala
case class Person(name: String, age: Int)

// Automatic features:
val person1 = Person("John", 30)  // No 'new' keyword needed
val person2 = Person("John", 30)

println(person1 == person2)  // true - structural equality
println(person1.name)        // Automatic getter methods

// Copy with modifications
val olderPerson = person1.copy(age = 31)

// Pattern matching support
person1 match {
  case Person(name, age) => println(s"$name is $age years old")
}
```

**Objects (Singletons):**
```scala
object MathUtils {
  val PI = 3.14159
  
  def square(x: Double): Double = x * x
  def circle Area(radius: Double): Double = PI * square(radius)
}

// Usage
val area = MathUtils.circleArea(5.0)

// Companion object
class BankAccount(initialBalance: Double) {
  private var balance = initialBalance
  
  def deposit(amount: Double): Unit = balance += amount
  def getBalance: Double = balance
}

object BankAccount {
  def apply(initialBalance: Double): BankAccount = 
    new BankAccount(initialBalance)
}

val account = BankAccount(1000.0)  // Using companion object
```

---

## Object-Oriented Programming

### 6. How does inheritance work in Scala?
**Answer:**
**Class Inheritance:**
```scala
abstract class Animal {
  def name: String
  def makeSound(): String
  
  def introduce(): String = s"I'm $name and I $makeSound"
}

class Dog(val name: String) extends Animal {
  override def makeSound(): String = "bark"
}

class Cat(val name: String) extends Animal {
  override def makeSound(): String = "meow"
  
  // Additional method
  def purr(): String = "purr"
}

val dog = new Dog("Buddy")
val cat = new Cat("Whiskers")

println(dog.introduce())  // "I'm Buddy and I bark"
println(cat.introduce())  // "I'm Whiskers and I meow"
```

### 7. What are traits in Scala?
**Answer:**
Traits are similar to interfaces but can contain concrete implementations.

**Basic Traits:**
```scala
trait Flyable {
  def fly(): String = "Flying high!"
}

trait Swimmable {
  def swim(): String = "Swimming fast!"
}

class Duck extends Flyable with Swimmable {
  def quack(): String = "Quack!"
}

val duck = new Duck()
println(duck.fly())   // "Flying high!"
println(duck.swim())  // "Swimming fast!"
println(duck.quack()) // "Quack!"
```

**Trait Linearization:**
```scala
trait A {
  def message: String = "A"
}

trait B extends A {
  override def message: String = "B" + super.message
}

trait C extends A {
  override def message: String = "C" + super.message
}

class D extends B with C
val d = new D()
println(d.message)  // "CBA" - linearization order: D -> C -> B -> A
```

### 8. How do you implement polymorphism in Scala?
**Answer:**
**Subtype Polymorphism:**
```scala
abstract class Shape {
  def area: Double
  def perimeter: Double
}

class Circle(radius: Double) extends Shape {
  def area: Double = math.Pi * radius * radius
  def perimeter: Double = 2 * math.Pi * radius
}

class Rectangle(width: Double, height: Double) extends Shape {
  def area: Double = width * height
  def perimeter: Double = 2 * (width + height)
}

def printShapeInfo(shape: Shape): Unit = {
  println(s"Area: ${shape.area}, Perimeter: ${shape.perimeter}")
}

val shapes: List[Shape] = List(
  new Circle(5.0),
  new Rectangle(4.0, 6.0)
)

shapes.foreach(printShapeInfo)  // Polymorphic behavior
```

**Parametric Polymorphism (Generics):**
```scala
class Container[T](value: T) {
  def get: T = value
  def map[U](f: T => U): Container[U] = new Container(f(value))
}

val intContainer = new Container(42)
val stringContainer = intContainer.map(_.toString)
```

### 9. What are abstract classes vs traits?
**Answer:**
**Abstract Classes:**
```scala
abstract class Vehicle(val wheels: Int) {
  def start(): Unit  // Abstract method
  def stop(): Unit = println("Vehicle stopped")  // Concrete method
}

class Car extends Vehicle(4) {
  def start(): Unit = println("Car started")
}
```

**Traits:**
```scala
trait Drivable {
  def drive(): Unit = println("Driving...")
}

trait Flyable {
  def fly(): Unit = println("Flying...")
}

// Multiple trait inheritance
class FlyingCar extends Vehicle(4) with Drivable with Flyable {
  def start(): Unit = println("Flying car started")
}
```

**Key Differences:**
- Abstract classes can have constructor parameters
- Classes can extend only one abstract class but multiple traits
- Traits support multiple inheritance with linearization

### 10. How do access modifiers work in Scala?
**Answer:**
**Access Levels:**
```scala
package com.example

class AccessExample {
  private val privateField = "private"           // Only within this class
  protected val protectedField = "protected"     // This class and subclasses
  val publicField = "public"                     // Everywhere
  
  private[this] val objectPrivate = "object"     // Only this instance
  private[example] val packagePrivate = "pkg"    // Within package
  
  def demonstrateAccess(): Unit = {
    println(privateField)      // OK
    println(protectedField)    // OK
    println(publicField)       // OK
    println(objectPrivate)     // OK
    println(packagePrivate)    // OK
  }
}

class SubClass extends AccessExample {
  def subClassMethod(): Unit = {
    // println(privateField)      // Error - not accessible
    println(protectedField)       // OK
    println(publicField)          // OK
    // println(objectPrivate)     // Error - not accessible
    println(packagePrivate)       // OK (same package)
  }
}
```

---

## Functional Programming

### 11. What are higher-order functions in Scala?
**Answer:**
Higher-order functions take other functions as parameters or return functions.

**Examples:**
```scala
// Function that takes another function as parameter
def applyOperation(x: Int, y: Int, op: (Int, Int) => Int): Int = op(x, y)

val add = (x: Int, y: Int) => x + y
val multiply = (x: Int, y: Int) => x * y

println(applyOperation(5, 3, add))      // 8
println(applyOperation(5, 3, multiply)) // 15

// Function that returns a function
def createMultiplier(factor: Int): Int => Int = {
  (x: Int) => x * factor
}

val double = createMultiplier(2)
val triple = createMultiplier(3)

println(double(5))  // 10
println(triple(5))  // 15

// Using with collections
val numbers = List(1, 2, 3, 4, 5)
val doubled = numbers.map(_ * 2)           // List(2, 4, 6, 8, 10)
val evens = numbers.filter(_ % 2 == 0)     // List(2, 4)
val sum = numbers.reduce(_ + _)            // 15
```

### 12. How do closures work in Scala?
**Answer:**
Closures capture variables from their enclosing scope.

**Examples:**
```scala
def createCounter(start: Int): () => Int = {
  var count = start
  () => {
    count += 1
    count
  }
}

val counter1 = createCounter(0)
val counter2 = createCounter(10)

println(counter1())  // 1
println(counter1())  // 2
println(counter2())  // 11
println(counter1())  // 3

// Closure capturing external variable
var multiplier = 2
val multiplyByExternal = (x: Int) => x * multiplier

println(multiplyByExternal(5))  // 10
multiplier = 3
println(multiplyByExternal(5))  // 15
```

### 13. What are currying and partial application?
**Answer:**
**Currying:**
```scala
// Regular function
def add(x: Int, y: Int, z: Int): Int = x + y + z

// Curried function
def curriedAdd(x: Int)(y: Int)(z: Int): Int = x + y + z

// Partial application
val addFive = curriedAdd(5) _
val addFiveAndThree = addFive(3)
val result = addFiveAndThree(2)  // 10

// Converting regular function to curried
val curriedVersion = (add _).curried
val partiallyApplied = curriedVersion(1)(2)
println(partiallyApplied(3))  // 6
```

**Practical Example:**
```scala
def log(level: String)(message: String): Unit = {
  println(s"[$level] $message")
}

val info = log("INFO") _
val error = log("ERROR") _

info("Application started")     // [INFO] Application started
error("Something went wrong")   // [ERROR] Something went wrong
```

### 14. How do you work with immutable data structures?
**Answer:**
**Immutable Collections:**
```scala
// Lists (immutable by default)
val originalList = List(1, 2, 3)
val newList = 0 :: originalList        // List(0, 1, 2, 3)
val appendedList = originalList :+ 4   // List(1, 2, 3, 4)

// Maps
val originalMap = Map("a" -> 1, "b" -> 2)
val updatedMap = originalMap + ("c" -> 3)     // Add element
val removedMap = originalMap - "a"            // Remove element

// Sets
val originalSet = Set(1, 2, 3)
val newSet = originalSet + 4 - 2  // Set(1, 3, 4)

// Functional updates
case class Person(name: String, age: Int, address: String)

val person = Person("John", 30, "123 Main St")
val olderPerson = person.copy(age = 31)
val movedPerson = person.copy(address = "456 Oak Ave")

// Working with nested immutable structures
case class Address(street: String, city: String)
case class Employee(name: String, address: Address)

val employee = Employee("Jane", Address("123 Main", "NYC"))
val updatedEmployee = employee.copy(
  address = employee.address.copy(city = "Boston")
)
```

### 15. What are monads and how are they used in Scala?
**Answer:**
**Option Monad:**
```scala
def divide(x: Double, y: Double): Option[Double] = {
  if (y != 0) Some(x / y) else None
}

val result1 = divide(10, 2)  // Some(5.0)
val result2 = divide(10, 0)  // None

// Chaining operations
val computation = for {
  a <- divide(10, 2)
  b <- divide(a, 2)
  c <- divide(b, 2.5)
} yield c

println(computation)  // Some(1.0)

// Using map and flatMap
val mapped = divide(10, 2).map(_ * 2)           // Some(10.0)
val flatMapped = divide(10, 2).flatMap(x => divide(x, 2))  // Some(2.5)
```

**Try Monad:**
```scala
import scala.util.{Try, Success, Failure}

def parseInteger(s: String): Try[Int] = Try(s.toInt)

val result = for {
  a <- parseInteger("10")
  b <- parseInteger("20")
} yield a + b

result match {
  case Success(value) => println(s"Result: $value")
  case Failure(exception) => println(s"Error: ${exception.getMessage}")
}
```

---

## Collections

### 16. What are the main collection types in Scala?
**Answer:**
**Sequence Types:**
```scala
// List - immutable linked list
val list = List(1, 2, 3, 4)
val head = list.head        // 1
val tail = list.tail        // List(2, 3, 4)

// Vector - immutable indexed sequence
val vector = Vector(1, 2, 3, 4)
val element = vector(2)     // 3 (efficient random access)

// Array - mutable indexed sequence
val array = Array(1, 2, 3, 4)
array(0) = 10              // Mutation allowed

// ListBuffer - mutable list
import scala.collection.mutable.ListBuffer
val buffer = ListBuffer(1, 2, 3)
buffer += 4                // ListBuffer(1, 2, 3, 4)
```

**Map Types:**
```scala
// Immutable Map
val immutableMap = Map("a" -> 1, "b" -> 2)
val updated = immutableMap + ("c" -> 3)

// Mutable Map
import scala.collection.mutable
val mutableMap = mutable.Map("a" -> 1, "b" -> 2)
mutableMap("c") = 3        // Direct mutation
```

**Set Types:**
```scala
// Immutable Set
val immutableSet = Set(1, 2, 3)
val withFour = immutableSet + 4

// Mutable Set
val mutableSet = mutable.Set(1, 2, 3)
mutableSet += 4            // Direct mutation
```

### 17. How do you use map, filter, and reduce operations?
**Answer:**
**Map - Transform Elements:**
```scala
val numbers = List(1, 2, 3, 4, 5)

val doubled = numbers.map(_ * 2)           // List(2, 4, 6, 8, 10)
val strings = numbers.map(_.toString)      // List("1", "2", "3", "4", "5")
val lengths = List("hello", "world").map(_.length)  // List(5, 5)

// Map with index
val withIndex = numbers.zipWithIndex.map { case (value, index) => 
  s"$index: $value" 
}
```

**Filter - Select Elements:**
```scala
val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

val evens = numbers.filter(_ % 2 == 0)     // List(2, 4, 6, 8, 10)
val greaterThanFive = numbers.filter(_ > 5) // List(6, 7, 8, 9, 10)

// filterNot (opposite of filter)
val odds = numbers.filterNot(_ % 2 == 0)   // List(1, 3, 5, 7, 9)
```

**Reduce and Fold:**
```scala
val numbers = List(1, 2, 3, 4, 5)

val sum = numbers.reduce(_ + _)            // 15
val product = numbers.reduce(_ * _)        // 120
val max = numbers.reduce(math.max)         // 5

// Fold with initial value
val sumWithZero = numbers.fold(0)(_ + _)   // 15
val sumWithTen = numbers.fold(10)(_ + _)   // 25

// FoldLeft and foldRight
val concatenated = List("a", "b", "c").foldLeft("")(_ + _)  // "abc"
val reversed = List("a", "b", "c").foldRight("")(_ + _)     // "abc"
```

### 18. What are for-comprehensions in Scala?
**Answer:**
For-comprehensions provide syntactic sugar for map, flatMap, filter, and foreach.

**Basic Syntax:**
```scala
val numbers = List(1, 2, 3, 4, 5)

// Simple for-comprehension
val doubled = for (n <- numbers) yield n * 2
// Equivalent to: numbers.map(_ * 2)

// With filter
val evenDoubled = for {
  n <- numbers
  if n % 2 == 0
} yield n * 2
// Equivalent to: numbers.filter(_ % 2 == 0).map(_ * 2)

// Multiple generators
val pairs = for {
  x <- List(1, 2, 3)
  y <- List("a", "b")
} yield (x, y)
// Result: List((1,a), (1,b), (2,a), (2,b), (3,a), (3,b))
```

**Complex Examples:**
```scala
case class Person(name: String, age: Int)
val people = List(
  Person("Alice", 25),
  Person("Bob", 30),
  Person("Charlie", 35)
)

// Nested for-comprehension
val result = for {
  person <- people
  if person.age > 25
  name = person.name.toUpperCase
  char <- name.toCharArray
} yield char

// With Option
def findPerson(name: String): Option[Person] = 
  people.find(_.name == name)

val ageSum = for {
  alice <- findPerson("Alice")
  bob <- findPerson("Bob")
} yield alice.age + bob.age
```

### 19. How do you work with lazy collections and streams?
**Answer:**
**Lazy Collections:**
```scala
// LazyList (formerly Stream in Scala 2.12)
val lazyNumbers = LazyList.from(1)  // Infinite lazy sequence

val firstTen = lazyNumbers.take(10).toList  // List(1, 2, 3, ..., 10)

// Lazy evaluation with view (deprecated in Scala 2.13+)
val numbers = (1 to 1000000).view
val result = numbers
  .filter(_ % 2 == 0)
  .map(_ * 2)
  .take(5)
  .toList  // Only computed when toList is called

// Iterator (lazy by nature)
val iterator = Iterator.from(1)
val evenIterator = iterator.filter(_ % 2 == 0)
val firstFiveEvens = evenIterator.take(5).toList
```

**Custom Lazy Structures:**
```scala
// Fibonacci sequence using LazyList
def fibonacci: LazyList[Int] = {
  def fib(a: Int, b: Int): LazyList[Int] = 
    a #:: fib(b, a + b)
  fib(0, 1)
}

val firstTenFib = fibonacci.take(10).toList
// List(0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
```

### 20. What are parallel collections in Scala?
**Answer:**
**Parallel Collections:**
```scala
val largeList = (1 to 1000000).toList

// Sequential processing
val sequentialResult = largeList.map(_ * 2).filter(_ % 4 == 0).sum

// Parallel processing
val parallelResult = largeList.par.map(_ * 2).filter(_ % 4 == 0).sum

// Converting between sequential and parallel
val parallelCollection = largeList.par
val backToSequential = parallelCollection.seq

// Custom parallel operations
val numbers = (1 to 100).par
val evenSum = numbers.filter(_ % 2 == 0).sum
val oddProduct = numbers.filter(_ % 2 == 1).reduce(_ * _)

// Configuring parallelism
import scala.collection.parallel.ForkJoinTaskSupport
import java.util.concurrent.ForkJoinPool

val customTaskSupport = new ForkJoinTaskSupport(new ForkJoinPool(4))
val parallelVector = Vector.fill(1000)(1).par
parallelVector.tasksupport = customTaskSupport
```

---

## Pattern Matching

### 21. How does pattern matching work in Scala?
**Answer:**
**Basic Pattern Matching:**
```scala
def describe(x: Any): String = x match {
  case 1 => "one"
  case "hello" => "greeting"
  case true => "truth"
  case Nil => "empty list"
  case _ => "something else"
}

// Matching with guards
def classifyNumber(x: Int): String = x match {
  case n if n < 0 => "negative"
  case 0 => "zero"
  case n if n > 0 && n < 10 => "single digit positive"
  case _ => "large positive"
}

// Matching types
def processValue(value: Any): String = value match {
  case s: String => s"String: $s"
  case i: Int => s"Integer: $i"
  case l: List[_] => s"List with ${l.length} elements"
  case _ => "Unknown type"
}
```

### 22. How do you use pattern matching with case classes?
**Answer:**
**Case Class Matching:**
```scala
sealed trait Animal
case class Dog(name: String, breed: String) extends Animal
case class Cat(name: String, color: String) extends Animal
case class Bird(name: String, canFly: Boolean) extends Animal

def animalSound(animal: Animal): String = animal match {
  case Dog(name, _) => s"$name barks"
  case Cat(name, "black") => s"$name meows mysteriously"
  case Cat(name, color) => s"$name the $color cat meows"
  case Bird(name, true) => s"$name chirps while flying"
  case Bird(name, false) => s"$name chirps from the ground"
}

// Nested pattern matching
case class Person(name: String, address: Address)
case class Address(street: String, city: String)

def getCity(person: Person): String = person match {
  case Person(_, Address(_, city)) => city
}

// Pattern matching in variable assignment
val Dog(dogName, dogBreed) = Dog("Buddy", "Golden Retriever")
println(s"Dog name: $dogName, breed: $dogBreed")
```

### 23. What are extractors and unapply methods?
**Answer:**
**Custom Extractors:**
```scala
object Email {
  def apply(user: String, domain: String): String = s"$user@$domain"
  
  def unapply(email: String): Option[(String, String)] = {
    val parts = email.split("@")
    if (parts.length == 2) Some((parts(0), parts(1)))
    else None
  }
}

// Usage
val email = Email("john", "example.com")  // "john@example.com"

email match {
  case Email(user, domain) => println(s"User: $user, Domain: $domain")
  case _ => println("Invalid email")
}

// Boolean extractor
object Even {
  def unapply(n: Int): Boolean = n % 2 == 0
}

def checkNumber(n: Int): String = n match {
  case Even() => "even number"
  case _ => "odd number"
}
```

### 24. How do you use pattern matching with collections?
**Answer:**
**List Pattern Matching:**
```scala
def processList(list: List[Int]): String = list match {
  case Nil => "empty list"
  case head :: Nil => s"single element: $head"
  case head :: tail => s"head: $head, tail: $tail"
}

// More specific patterns
def listPatterns(list: List[Int]): String = list match {
  case List() => "empty"
  case List(x) => s"single: $x"
  case List(x, y) => s"pair: $x, $y"
  case x :: y :: rest => s"starts with $x, $y, has ${rest.length} more"
}

// Array pattern matching
def processArray(arr: Array[Int]): String = arr match {
  case Array() => "empty array"
  case Array(x) => s"single element: $x"
  case Array(x, y, _*) => s"starts with $x, $y"
}

// Map pattern matching
def processMap(map: Map[String, Int]): String = map match {
  case Map() => "empty map"
  case m if m.contains("key") => s"contains key: ${m("key")}"
  case _ => "other map"
}
```

### 25. What are sealed traits and exhaustive matching?
**Answer:**
**Sealed Traits:**
```scala
sealed trait Color
case object Red extends Color
case object Green extends Color
case object Blue extends Color

// Compiler ensures exhaustive matching
def colorName(color: Color): String = color match {
  case Red => "red"
  case Green => "green"
  case Blue => "blue"
  // No need for default case - compiler knows all possibilities
}

// Adding new case requires updating all matches
sealed trait Shape
case class Circle(radius: Double) extends Shape
case class Rectangle(width: Double, height: Double) extends Shape
case class Triangle(base: Double, height: Double) extends Shape

def area(shape: Shape): Double = shape match {
  case Circle(r) => math.Pi * r * r
  case Rectangle(w, h) => w * h
  case Triangle(b, h) => 0.5 * b * h
}

// Compiler warning if not exhaustive
def partialMatch(shape: Shape): String = shape match {
  case Circle(_) => "circle"
  case Rectangle(_, _) => "rectangle"
  // Warning: match may not be exhaustive (missing Triangle)
}
```

---

## Concurrency

### 26. How do you work with Futures in Scala?
**Answer:**
**Basic Futures:**
```scala
import scala.concurrent.{Future, ExecutionContext}
import scala.util.{Success, Failure}

implicit val ec: ExecutionContext = ExecutionContext.global

// Creating futures
val future1 = Future {
  Thread.sleep(1000)
  42
}

val future2 = Future.successful(100)  // Already completed
val future3 = Future.failed(new RuntimeException("Error"))

// Handling results
future1.onComplete {
  case Success(value) => println(s"Result: $value")
  case Failure(exception) => println(s"Error: ${exception.getMessage}")
}

// Transforming futures
val doubled = future1.map(_ * 2)
val stringified = future1.map(_.toString)

// Chaining futures
def fetchUser(id: Int): Future[String] = Future(s"User$id")
def fetchUserPosts(user: String): Future[List[String]] = 
  Future(List(s"${user}_post1", s"${user}_post2"))

val userPosts = for {
  user <- fetchUser(123)
  posts <- fetchUserPosts(user)
} yield posts
```

### 27. How do you combine multiple Futures?
**Answer:**
**Combining Futures:**
```scala
import scala.concurrent.Future

val future1 = Future(10)
val future2 = Future(20)
val future3 = Future(30)

// Combining with for-comprehension
val combined = for {
  a <- future1
  b <- future2
  c <- future3
} yield a + b + c

// Using Future.sequence
val futureList = List(future1, future2, future3)
val sequenced: Future[List[Int]] = Future.sequence(futureList)

// Using Future.traverse
val numbers = List(1, 2, 3, 4, 5)
val futureResults = Future.traverse(numbers)(n => Future(n * 2))

// Racing futures (first to complete)
val fastest = Future.firstCompletedOf(List(future1, future2, future3))

// Recovering from failures
val recovered = future1.recover {
  case _: RuntimeException => 0
}

val recoveredWith = future1.recoverWith {
  case _: RuntimeException => Future.successful(0)
}
```

### 28. What are Actors and the Actor model?
**Answer:**
**Akka Actors:**
```scala
import akka.actor.{Actor, ActorRef, ActorSystem, Props}

// Define messages
case class Greet(name: String)
case object GetCount

// Actor implementation
class GreeterActor extends Actor {
  private var greetCount = 0
  
  def receive: Receive = {
    case Greet(name) =>
      greetCount += 1
      println(s"Hello, $name! (count: $greetCount)")
      sender() ! s"Greeted $name"
      
    case GetCount =>
      sender() ! greetCount
  }
}

// Usage
val system = ActorSystem("GreeterSystem")
val greeter = system.actorOf(Props[GreeterActor], "greeter")

greeter ! Greet("Alice")
greeter ! Greet("Bob")
greeter ! GetCount

// Typed Actors (Akka Typed)
import akka.actor.typed.{ActorRef, Behavior}
import akka.actor.typed.scaladsl.Behaviors

object TypedGreeter {
  sealed trait Command
  case class Greet(name: String, replyTo: ActorRef[String]) extends Command
  
  def apply(): Behavior[Command] = Behaviors.receive { (context, message) =>
    message match {
      case Greet(name, replyTo) =>
        context.log.info(s"Hello $name!")
        replyTo ! s"Hello $name!"
        Behaviors.same
    }
  }
}
```

### 29. How do you handle parallel processing in Scala?
**Answer:**
**Parallel Collections:**
```scala
val largeCollection = (1 to 1000000).toVector

// Sequential processing
val sequentialResult = largeCollection
  .filter(_ % 2 == 0)
  .map(math.sqrt)
  .sum

// Parallel processing
val parallelResult = largeCollection.par
  .filter(_ % 2 == 0)
  .map(math.sqrt)
  .sum

// Custom thread pool
import java.util.concurrent.ForkJoinPool
import scala.collection.parallel.ForkJoinTaskSupport

val customThreadPool = new ForkJoinPool(4)
val parCollection = largeCollection.par
parCollection.tasksupport = new ForkJoinTaskSupport(customThreadPool)
```

**Future-based Parallelism:**
```scala
import scala.concurrent.{Future, ExecutionContext}
import java.util.concurrent.Executors

// Custom execution context
implicit val ec: ExecutionContext = ExecutionContext.fromExecutor(
  Executors.newFixedThreadPool(4)
)

def processChunk(chunk: List[Int]): Future[Int] = Future {
  chunk.map(_ * 2).sum
}

val data = (1 to 1000).toList
val chunks = data.grouped(100).toList

val futureResults = chunks.map(processChunk)
val finalResult = Future.sequence(futureResults).map(_.sum)
```

### 30. What are the different concurrency models in Scala?
**Answer:**
**Thread-based Concurrency:**
```scala
import java.util.concurrent.{Executors, CountDownLatch}

val executor = Executors.newFixedThreadPool(4)
val latch = new CountDownLatch(4)

(1 to 4).foreach { i =>
  executor.submit(new Runnable {
    def run(): Unit = {
      println(s"Task $i running on ${Thread.currentThread().getName}")
      Thread.sleep(1000)
      latch.countDown()
    }
  })
}

latch.await()  // Wait for all tasks to complete
executor.shutdown()
```

**Reactive Streams:**
```scala
import akka.stream.scaladsl.{Source, Sink}
import akka.stream.ActorMaterializer
import akka.actor.ActorSystem

implicit val system = ActorSystem("StreamSystem")
implicit val materializer = ActorMaterializer()

val source = Source(1 to 100)
val sink = Sink.foreach[Int](println)

val runnable = source
  .filter(_ % 2 == 0)
  .map(_ * 2)
  .to(sink)

runnable.run()
```

---

## Advanced Topics

### 31. What are implicits in Scala?
**Answer:**
**Implicit Parameters:**
```scala
// Implicit parameter
def greet(name: String)(implicit greeting: String): String = 
  s"$greeting, $name!"

implicit val defaultGreeting: String = "Hello"

println(greet("Alice"))  // "Hello, Alice!"

// Implicit class (extension methods)
implicit class StringOps(s: String) {
  def isPalindrome: Boolean = s == s.reverse
  def wordCount: Int = s.split("\\s+").length
}

println("racecar".isPalindrome)  // true
println("hello world".wordCount) // 2
```

**Type Classes:**
```scala
trait Show[T] {
  def show(value: T): String
}

implicit val intShow: Show[Int] = new Show[Int] {
  def show(value: Int): String = value.toString
}

implicit val stringShow: Show[String] = new Show[String] {
  def show(value: String): String = s"'$value'"
}

def display[T](value: T)(implicit shower: Show[T]): String = 
  shower.show(value)

println(display(42))        // "42"
println(display("hello"))   // "'hello'"
```

### 32. How do macros work in Scala?
**Answer:**
**Compile-time Macros:**
```scala
import scala.language.experimental.macros
import scala.reflect.macros.blackbox

// Macro definition
def debug(param: Any): Unit = macro debugImpl

def debugImpl(c: blackbox.Context)(param: c.Expr[Any]): c.Expr[Unit] = {
  import c.universe._
  val paramRep = show(param.tree)
  val paramRepTree = Literal(Constant(paramRep))
  val paramRepExpr = c.Expr[String](paramRepTree)
  reify {
    println(s"${paramRepExpr.splice} = ${param.splice}")
  }
}

// Usage
val x = 42
debug(x)  // Prints: "x = 42"
```

**Annotation Macros:**
```scala
import scala.annotation.StaticAnnotation
import scala.language.experimental.macros

class toString extends StaticAnnotation {
  def macroTransform(annottees: Any*): Any = macro toStringMacro.impl
}

object toStringMacro {
  def impl(c: blackbox.Context)(annottees: c.Expr[Any]*): c.Expr[Any] = {
    // Macro implementation to generate toString method
    ???
  }
}

@toString
case class Person(name: String, age: Int)
```

### 33. What are type-level programming techniques?
**Answer:**
**Phantom Types:**
```scala
sealed trait State
sealed trait Open extends State
sealed trait Closed extends State

class Door[S <: State] private (val isOpen: Boolean)

object Door {
  def apply(): Door[Closed] = new Door[Closed](false)
}

implicit class OpenDoor(door: Door[Closed]) {
  def open(): Door[Open] = new Door[Open](true)
}

implicit class CloseDoor(door: Door[Open]) {
  def close(): Door[Closed] = new Door[Closed](false)
}

val door = Door()           // Door[Closed]
val openDoor = door.open()  // Door[Open]
val closedDoor = openDoor.close()  // Door[Closed]
// door.close()  // Compile error - can't close already closed door
```

**Dependent Types:**
```scala
trait Nat
case object Zero extends Nat
case class Succ[N <: Nat](n: N) extends Nat

type _0 = Zero.type
type _1 = Succ[_0]
type _2 = Succ[_1]
type _3 = Succ[_2]

case class Vec[N <: Nat, T](elements: List[T]) {
  def head: T = elements.head
  def tail: Vec[Succ[N], T] = Vec(elements.tail)
}

val vec3: Vec[_3, Int] = Vec(List(1, 2, 3))
val vec2: Vec[_2, Int] = vec3.tail
```

### 34. How do you work with variance in Scala?
**Answer:**
**Covariance and Contravariance:**
```scala
// Covariant (Producer)
trait Producer[+T] {
  def produce(): T
}

class AnimalProducer extends Producer[Animal] {
  def produce(): Animal = new Animal
}

class DogProducer extends Producer[Dog] {
  def produce(): Dog = new Dog
}

// Dog <: Animal, so Producer[Dog] <: Producer[Animal]
val animalProducer: Producer[Animal] = new DogProducer

// Contravariant (Consumer)
trait Consumer[-T] {
  def consume(item: T): Unit
}

class AnimalConsumer extends Consumer[Animal] {
  def consume(animal: Animal): Unit = println("Consuming animal")
}

// Animal >: Dog, so Consumer[Animal] <: Consumer[Dog]
val dogConsumer: Consumer[Dog] = new AnimalConsumer

// Invariant
trait Container[T] {
  def get(): T
  def set(item: T): Unit
}

// Function variance
val f1: Animal => Dog = (animal: Animal) => new Dog
val f2: Dog => Animal = f1  // Contravariant in parameter, covariant in return
```

### 35. What are best practices for Scala development?
**Answer:**
**Code Style:**
```scala
// Prefer immutability
val immutableList = List(1, 2, 3)
val newList = 0 :: immutableList

// Use case classes for data
case class User(id: Long, name: String, email: String)

// Prefer Option over null
def findUser(id: Long): Option[User] = {
  // Return Some(user) or None
  ???
}

// Use for-comprehensions for sequential operations
val result = for {
  user <- findUser(123)
  profile <- findProfile(user.id)
  settings <- findSettings(profile.id)
} yield (user, profile, settings)

// Prefer tail recursion
@annotation.tailrec
def factorial(n: Int, acc: Int = 1): Int = {
  if (n <= 1) acc
  else factorial(n - 1, n * acc)
}
```

**Error Handling:**
```scala
import scala.util.{Try, Success, Failure}

// Use Try for operations that might fail
def parseInteger(s: String): Try[Int] = Try(s.toInt)

// Use Either for domain errors
sealed trait ValidationError
case class InvalidEmail(email: String) extends ValidationError
case class InvalidAge(age: Int) extends ValidationError

def validateUser(email: String, age: Int): Either[ValidationError, User] = {
  if (!email.contains("@")) Left(InvalidEmail(email))
  else if (age < 0) Left(InvalidAge(age))
  else Right(User(1L, "User", email))
}
```

**Performance Tips:**
```scala
// Use lazy evaluation when appropriate
lazy val expensiveComputation = {
  // Computed only when first accessed
  (1 to 1000000).map(_ * 2).sum
}

// Use builders for efficient collection construction
val builder = List.newBuilder[Int]
(1 to 1000).foreach(builder += _)
val result = builder.result()

// Prefer tail recursion and trampolines for deep recursion
import scala.util.control.TailCalls._

def evenOdd(n: Int): TailRec[String] = {
  if (n == 0) done("even")
  else if (n == 1) done("odd")
  else tailcall(evenOdd(n - 2))
}
```

---

*This comprehensive guide covers 35+ essential Scala programming interview questions with detailed answers and practical examples for functional and object-oriented programming interviews.*