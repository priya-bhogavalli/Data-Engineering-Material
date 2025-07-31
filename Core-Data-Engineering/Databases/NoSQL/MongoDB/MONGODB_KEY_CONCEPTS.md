# MongoDB Key Concepts

## 🎯 What is MongoDB?
Document-oriented NoSQL database that stores data in flexible, JSON-like documents.

## 🏗️ Core Architecture

### Document Structure
```json
{
  "_id": ObjectId("..."),
  "name": "John Doe",
  "age": 30,
  "address": {
    "street": "123 Main St",
    "city": "New York"
  },
  "hobbies": ["reading", "swimming"]
}
```

### Key Components
- **Database** - Container for collections
- **Collection** - Group of documents (like table)
- **Document** - Individual record (like row)
- **Field** - Key-value pair (like column)

## 🔧 Essential Operations

### CRUD Operations
```javascript
// Create
db.users.insertOne({name: "Alice", age: 25})

// Read
db.users.find({age: {$gte: 18}})

// Update
db.users.updateOne({name: "Alice"}, {$set: {age: 26}})

// Delete
db.users.deleteOne({name: "Alice"})
```

### Aggregation Pipeline
```javascript
db.orders.aggregate([
  {$match: {status: "completed"}},
  {$group: {_id: "$customerId", total: {$sum: "$amount"}}},
  {$sort: {total: -1}}
])
```

## 📊 Data Modeling

### Embedding vs Referencing
```javascript
// Embedded (denormalized)
{
  "user": "john",
  "posts": [
    {"title": "Post 1", "content": "..."},
    {"title": "Post 2", "content": "..."}
  ]
}

// Referenced (normalized)
{
  "user": "john",
  "postIds": [ObjectId("..."), ObjectId("...")]
}
```

## 🚀 Performance Features

### Indexing
```javascript
// Create index
db.users.createIndex({email: 1})

// Compound index
db.users.createIndex({name: 1, age: -1})

// Text index
db.posts.createIndex({title: "text", content: "text"})
```

### Sharding
- Horizontal partitioning across multiple servers
- Automatic data distribution
- High availability and scalability

## 🔒 Security & Best Practices

### Authentication
```javascript
// Create user
db.createUser({
  user: "dataEngineer",
  pwd: "securePassword",
  roles: ["readWrite"]
})
```

### Best Practices
- Use appropriate data types
- Design schema for query patterns
- Implement proper indexing strategy
- Monitor performance metrics
- Regular backups and replica sets

## 🎯 Use Cases
- Content management systems
- Real-time analytics
- IoT data collection
- Product catalogs
- User profiles and personalization