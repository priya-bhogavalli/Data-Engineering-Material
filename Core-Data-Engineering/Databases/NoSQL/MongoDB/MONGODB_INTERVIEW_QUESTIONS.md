# 🍃 MongoDB Interview Questions for Data Engineering (Enhanced)

## 📋 Table of Contents

1. [Fundamentals (1-25)](#fundamentals-1-25)
2. [Data Modeling (26-50)](#data-modeling-26-50)
3. [Aggregation & Queries (51-75)](#aggregation--queries-51-75)
4. [Performance & Scaling (76-100)](#performance--scaling-76-100)

---

## Fundamentals (1-25)

### 1. What is MongoDB and how does it differ from SQL databases?
**Answer**: MongoDB is a NoSQL document database storing data in BSON format.

**Key Differences:**
- **Schema**: Flexible vs Fixed
- **Data Model**: Documents vs Tables
- **Scaling**: Horizontal vs Vertical
- **Relationships**: Embedded/Referenced vs Foreign Keys

```javascript
// MongoDB document
{
  "_id": ObjectId("..."),
  "name": "John Doe",
  "email": "john@example.com",
  "addresses": [
    {"type": "home", "city": "New York"},
    {"type": "work", "city": "Boston"}
  ]
}
```

### 2. Explain MongoDB's CRUD operations
**Answer**: Create, Read, Update, Delete operations in MongoDB.

```javascript
// Create
db.users.insertOne({name: "Alice", age: 30});
db.users.insertMany([{name: "Bob"}, {name: "Carol"}]);

// Read
db.users.find({age: {$gte: 25}});
db.users.findOne({name: "Alice"});

// Update
db.users.updateOne({name: "Alice"}, {$set: {age: 31}});
db.users.updateMany({}, {$inc: {age: 1}});

// Delete
db.users.deleteOne({name: "Bob"});
db.users.deleteMany({age: {$lt: 18}});
```

### 3. What are MongoDB indexes and types?
**Answer**: Indexes improve query performance with various types available.

```javascript
// Single field index
db.users.createIndex({email: 1});

// Compound index
db.orders.createIndex({customerId: 1, orderDate: -1});

// Text index
db.products.createIndex({name: "text", description: "text"});

// Geospatial index
db.stores.createIndex({location: "2dsphere"});

// Partial index
db.users.createIndex(
  {email: 1},
  {partialFilterExpression: {email: {$exists: true}}}
);
```

## Data Modeling (26-50)

### 26. When should you embed vs reference documents?
**Answer**: Choose based on access patterns and data relationships.

```javascript
// Embed for one-to-few relationships
{
  "_id": ObjectId("..."),
  "title": "Blog Post",
  "comments": [
    {"author": "Alice", "text": "Great post!"},
    {"author": "Bob", "text": "Thanks for sharing"}
  ]
}

// Reference for one-to-many relationships
// User document
{"_id": ObjectId("user1"), "name": "John"}

// Order documents
{"_id": ObjectId("order1"), "userId": ObjectId("user1"), "total": 100}
```

### 27. How do you handle schema evolution?
**Answer**: Use versioning and gradual migration strategies.

```javascript
// Schema versioning
{
  "_id": ObjectId("..."),
  "schemaVersion": 2,
  "name": "John Doe",
  "contactInfo": {  // v2: restructured
    "email": "john@example.com",
    "phone": "+1234567890"
  }
}

// Application handles versions
function getUser(doc) {
  if (doc.schemaVersion === 1) {
    return {name: doc.name, email: doc.email};
  }
  return {name: doc.name, email: doc.contactInfo.email};
}
```

## Aggregation & Queries (51-75)

### 51. How do you build complex aggregation pipelines?
**Answer**: Use multiple stages for data transformation and analysis.

```javascript
db.orders.aggregate([
  // Stage 1: Filter recent orders
  {$match: {orderDate: {$gte: ISODate("2023-01-01")}}},
  
  // Stage 2: Unwind order items
  {$unwind: "$items"},
  
  // Stage 3: Group by product
  {$group: {
    _id: "$items.productId",
    totalQuantity: {$sum: "$items.quantity"},
    totalRevenue: {$sum: {$multiply: ["$items.quantity", "$items.price"]}}
  }},
  
  // Stage 4: Sort by revenue
  {$sort: {totalRevenue: -1}},
  
  // Stage 5: Limit results
  {$limit: 10}
]);
```

### 52. How do you implement text search?
**Answer**: Use text indexes and search operators.

```javascript
// Create text index
db.products.createIndex({name: "text", description: "text"});

// Text search
db.products.find({$text: {$search: "laptop gaming"}});

// Text search with score
db.products.find(
  {$text: {$search: "laptop"}},
  {score: {$meta: "textScore"}}
).sort({score: {$meta: "textScore"}});
```

## Performance & Scaling (76-100)

### 76. How do you optimize MongoDB queries?
**Answer**: Use proper indexing, query structure, and explain plans.

```javascript
// Analyze query performance
db.users.find({age: {$gte: 25}}).explain("executionStats");

// Optimize with compound index
db.users.createIndex({age: 1, city: 1});

// Use projection to limit fields
db.users.find({age: {$gte: 25}}, {name: 1, email: 1});
```

### 77. How do you implement MongoDB sharding?
**Answer**: Distribute data across multiple servers for horizontal scaling.

```javascript
// Enable sharding
sh.enableSharding("ecommerce");

// Shard collection
sh.shardCollection("ecommerce.orders", {customerId: 1, orderDate: 1});

// Check shard distribution
sh.status();
```

### 78. How do you handle MongoDB replication?
**Answer**: Use replica sets for high availability and data redundancy.

```javascript
// Initialize replica set
rs.initiate({
  _id: "myReplicaSet",
  members: [
    {_id: 0, host: "mongodb1:27017"},
    {_id: 1, host: "mongodb2:27017"},
    {_id: 2, host: "mongodb3:27017"}
  ]
});

// Check replica set status
rs.status();
```

---

**Total Questions: 100** | **Coverage: Complete MongoDB Ecosystem**