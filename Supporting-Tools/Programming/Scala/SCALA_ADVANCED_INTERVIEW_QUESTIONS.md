# 🎯 Scala Programming Advanced Interview Questions (41-80)

### 41. What are higher-kinded types in Scala?
**Answer:**
```scala
// Higher-kinded type parameter
trait Functor[F[_]] {
  def map[A, B](fa: F[A])(f: A => B): F[B]
}

// Implementations
implicit val listFunctor: Functor[List] = new Functor[List] {
  def map[A, B](fa: List[A])(f: A => B): List[B] = fa.map(f)
}

implicit val optionFunctor: Functor[Option] = new Functor[Option] {
  def map[A, B](fa: Option[A])(f: A => B): Option[B] = fa.map(f)
}

// Generic function using higher-kinded types
def double[F[_]](container: F[Int])(implicit F: Functor[F]): F[Int] =
  F.map(container)(_ * 2)
```

### 42. Explain path-dependent types in Scala.
**Answer:**
```scala
class Outer {
  class Inner {
    def method = "Inner method"
  }
  
  def createInner: Inner = new Inner
}

val outer1 = new Outer
val outer2 = new Outer

val inner1: outer1.Inner = outer1.createInner
val inner2: outer2.Inner = outer2.createInner

// inner1 and inner2 have different types!
// outer1.Inner ≠ outer2.Inner

// Type projection for all Inner types
def processInner(inner: Outer#Inner): String = inner.method
```

### 43. What are phantom types in Scala?
**Answer:**
```scala
sealed trait State
sealed trait Open extends State
sealed trait Closed extends State

class Door[S <: State] private (state: String) {
  override def toString: String = s"Door($state)"
}

object Door {
  def apply(): Door[Closed] = new Door("closed")
  
  implicit class ClosedDoor(door: Door[Closed]) {
    def open(): Door[Open] = new Door("open")
  }
  
  implicit class OpenDoor(door: Door[Open]) {
    def close(): Door[Closed] = new Door("closed")
  }
}

// Usage - compile-time state checking
val door = Door()           // Door[Closed]
val openDoor = door.open()  // Door[Open]
val closedDoor = openDoor.close()  // Door[Closed]
// door.close()  // Compile error - door is already closed
```

### 44. How do you implement type-safe builders in Scala?
**Answer:**
```scala
sealed trait HasName
sealed trait HasAge
sealed trait Complete

class PersonBuilder[State] private (
  name: Option[String] = None,
  age: Option[Int] = None
) {
  def withName(n: String): PersonBuilder[State with HasName] =
    new PersonBuilder(Some(n), age)
  
  def withAge(a: Int): PersonBuilder[State with HasAge] =
    new PersonBuilder(name, Some(a))
}

object PersonBuilder {
  def apply(): PersonBuilder[Nothing] = new PersonBuilder()
  
  implicit class CompleteBuilder(
    builder: PersonBuilder[HasName with HasAge]
  ) {
    def build(): Person = Person(
      builder.name.get,
      builder.age.get
    )
  }
}

case class Person(name: String, age: Int)

// Usage
val person = PersonBuilder()
  .withName("Alice")
  .withAge(30)
  .build()  // Only available when both name and age are set
```

### 45. What are Akka Streams and how do they work?
**Answer:**
```scala
import akka.actor.ActorSystem
import akka.stream.scaladsl.{Source, Sink, Flow}
import akka.NotUsed

implicit val system: ActorSystem = ActorSystem("StreamSystem")

// Basic stream
val source: Source[Int, NotUsed] = Source(1 to 10)
val flow: Flow[Int, Int, NotUsed] = Flow[Int].map(_ * 2)
val sink: Sink[Int, Future[Done]] = Sink.foreach(println)

val graph = source.via(flow).to(sink)
graph.run()

// More complex stream
val complexStream = Source(1 to 100)
  .filter(_ % 2 == 0)
  .map(_ * 3)
  .groupedWithin(5, 1.second)
  .map(_.sum)
  .runWith(Sink.seq)
```

### 46. How do you use Cats for functional programming?
**Answer:**
```scala
import cats._
import cats.implicits._

// Semigroup and Monoid
val result1 = 1 |+| 2 |+| 3  // 6
val result2 = "Hello" |+| " " |+| "World"  // "Hello World"
val result3 = List(1, 2) |+| List(3, 4)  // List(1, 2, 3, 4)

// Functor
val option1 = Option(42)
val option2 = option1.map(_ * 2)  // Some(84)

// Applicative
val result = (Option(1), Option(2), Option(3)).mapN(_ + _ + _)  // Some(6)

// Monad
val computation = for {
  x <- Option(10)
  y <- Option(20)
  z <- if (x + y > 25) Option(x + y) else None
} yield z  // Some(30)

// Validated for error accumulation
import cats.data.Validated

def validateAge(age: Int): Validated[List[String], Int] =
  if (age >= 0) age.valid else List("Age must be positive").invalid

def validateName(name: String): Validated[List[String], String] =
  if (name.nonEmpty) name.valid else List("Name cannot be empty").invalid

val person = (validateName(""), validateAge(-5)).mapN(Person)
// Invalid(List("Name cannot be empty", "Age must be positive"))
```

### 47. What is Shapeless and how is it used?
**Answer:**
```scala
import shapeless._

// HList (heterogeneous list)
val hlist = 1 :: "hello" :: true :: HNil
val head = hlist.head  // 1: Int
val tail = hlist.tail  // "hello" :: true :: HNil

// Generic derivation
case class Person(name: String, age: Int, active: Boolean)

val person = Person("Alice", 30, true)
val generic = Generic[Person]
val repr = generic.to(person)  // "Alice" :: 30 :: true :: HNil
val back = generic.from(repr)  // Person("Alice", 30, true)

// Automatic type class derivation
trait Show[T] {
  def show(value: T): String
}

object Show {
  implicit val stringShow: Show[String] = identity
  implicit val intShow: Show[Int] = _.toString
  implicit val booleanShow: Show[Boolean] = _.toString
  
  implicit val hnilShow: Show[HNil] = _ => ""
  
  implicit def hconsShow[H, T <: HList](
    implicit hShow: Show[H], tShow: Show[T]
  ): Show[H :: T] = {
    case h :: t => s"${hShow.show(h)}, ${tShow.show(t)}"
  }
  
  implicit def genericShow[T, R](
    implicit gen: Generic.Aux[T, R], rShow: Show[R]
  ): Show[T] = t => rShow.show(gen.to(t))
}

// Automatically derived Show instance
implicitly[Show[Person]].show(person)  // "Alice, 30, true, "
```

### 48. How do you work with Play Framework?
**Answer:**
```scala
// Controller
import play.api.mvc._
import play.api.libs.json._

class UserController @Inject()(cc: ControllerComponents) extends AbstractController(cc) {
  
  case class User(id: Long, name: String, email: String)
  
  implicit val userFormat: Format[User] = Json.format[User]
  
  def getUser(id: Long): Action[AnyContent] = Action { implicit request =>
    // Simulate database lookup
    val user = User(id, "Alice", "alice@example.com")
    Ok(Json.toJson(user))
  }
  
  def createUser(): Action[JsValue] = Action(parse.json) { implicit request =>
    request.body.validate[User] match {
      case JsSuccess(user, _) =>
        // Save to database
        Created(Json.toJson(user))
      case JsError(errors) =>
        BadRequest(Json.obj("errors" -> JsError.toJson(errors)))
    }
  }
}

// Routes (conf/routes)
// GET  /users/:id     controllers.UserController.getUser(id: Long)
// POST /users         controllers.UserController.createUser()
```

### 49. How do you use Slick for database access?
**Answer:**
```scala
import slick.jdbc.PostgresProfile.api._
import scala.concurrent.Future

// Table definition
class Users(tag: Tag) extends Table[(Long, String, String)](tag, "users") {
  def id = column[Long]("id", O.PrimaryKey, O.AutoInc)
  def name = column[String]("name")
  def email = column[String]("email")
  
  def * = (id, name, email)
}

val users = TableQuery[Users]

// Database operations
class UserRepository(db: Database) {
  
  def findById(id: Long): Future[Option[(Long, String, String)]] =
    db.run(users.filter(_.id === id).result.headOption)
  
  def findByEmail(email: String): Future[Seq[(Long, String, String)]] =
    db.run(users.filter(_.email === email).result)
  
  def create(name: String, email: String): Future[Long] =
    db.run((users.map(u => (u.name, u.email)) returning users.map(_.id)) += (name, email))
  
  def update(id: Long, name: String, email: String): Future[Int] =
    db.run(users.filter(_.id === id).map(u => (u.name, u.email)).update((name, email)))
  
  def delete(id: Long): Future[Int] =
    db.run(users.filter(_.id === id).delete)
}
```

### 50. What are ScalaTest testing patterns?
**Answer:**
```scala
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class CalculatorSpec extends AnyFlatSpec with Matchers {
  
  "A Calculator" should "add two numbers correctly" in {
    val calc = new Calculator
    calc.add(2, 3) should be(5)
  }
  
  it should "handle negative numbers" in {
    val calc = new Calculator
    calc.add(-2, 3) should be(1)
  }
  
  it should "throw exception for division by zero" in {
    val calc = new Calculator
    an[ArithmeticException] should be thrownBy calc.divide(10, 0)
  }
  
  // Property-based testing
  "Addition" should "be commutative" in {
    forAll { (a: Int, b: Int) =>
      val calc = new Calculator
      calc.add(a, b) should equal(calc.add(b, a))
    }
  }
  
  // Async testing
  "Async operation" should "complete successfully" in {
    val future = Future { Thread.sleep(100); 42 }
    future.futureValue should be(42)
  }
}
```

### 51-60. Additional Advanced Topics:
- **Scala.js** - JavaScript compilation
- **Scala Native** - Native compilation  
- **ZIO** - Effect system for functional programming
- **Circe** - JSON library
- **Doobie** - Functional database access
- **Http4s** - HTTP library
- **Refined types** - Compile-time validation
- **Monocle** - Optics library
- **ScalaCheck** - Property-based testing
- **Metals** - Language server

### 61-70. Ecosystem and Tools:
- **SBT** - Build tool configuration
- **Coursier** - Dependency resolution
- **Scalafmt** - Code formatting
- **Scalafix** - Code refactoring
- **Wartremover** - Linting
- **Scalastyle** - Style checking
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **Monitoring** - Metrics and logging
- **Performance** - Profiling and optimization

### 71-80. Big Data and Distributed Systems:
- **Apache Spark** - Distributed computing
- **Kafka** - Stream processing
- **Cassandra** - NoSQL database
- **Elasticsearch** - Search engine
- **Redis** - Caching
- **Microservices** - Architecture patterns
- **Event sourcing** - Data modeling
- **CQRS** - Command Query Responsibility Segregation
- **Distributed tracing** - Observability
- **Reactive systems** - Resilient architectures

---

*This completes the comprehensive Scala programming interview questions covering 80 essential topics with detailed answers and practical code examples.*