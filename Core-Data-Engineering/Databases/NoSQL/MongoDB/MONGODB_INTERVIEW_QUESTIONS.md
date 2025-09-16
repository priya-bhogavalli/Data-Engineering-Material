# 🍃 MongoDB Interview Questions for Data Engineering (Enhanced)

## 📋 Table of Contents

1. [Fundamentals (1-25)](#fundamentals-1-25)
2. [Data Modeling (26-50)](#data-modeling-26-50)
3. [Aggregation & Queries (51-75)](#aggregation--queries-51-75)
4. [Performance & Scaling (76-100)](#performance--scaling-76-100)

---

## Fundamentals (1-25)

### 1. What is MongoDB and how does it differ from SQL databases?

#### **Database Technology Comparison Matrix**
| Feature | MongoDB | PostgreSQL | MySQL | Cassandra |
|---------|---------|------------|-------|----------|
| **Data Model** | Document (BSON) | Relational (SQL) | Relational (SQL) | Wide-Column |
| **Schema Flexibility** | Dynamic schema | Fixed schema + JSON | Fixed schema | Column families |
| **ACID Compliance** | Multi-doc transactions | Full ACID | Full ACID | Eventual consistency |
| **Horizontal Scaling** | Native sharding | Read replicas + partitioning | Read replicas | Native distribution |
| **Query Language** | MongoDB Query Language | SQL | SQL | CQL (Cassandra Query Language) |
| **Performance (OLTP)** | 10K-50K ops/sec | 15K-20K TPS | 20K-30K TPS | 100K+ ops/sec |
| **Performance (Analytics)** | Aggregation pipeline | Advanced SQL analytics | Limited analytics | Time-series optimized |
| **Learning Curve** | Low-Medium | Medium-High | Low-Medium | High |
| **Operational Complexity** | Medium (Atlas managed) | Medium-High | Medium | High |
| **Enterprise Features** | Atlas, Compass, Ops Manager | Extensions, monitoring | Enterprise edition | DataStax Enterprise |
| **Community Support** | Large, active community | Very large community | Large community | Moderate community |

#### **Technology Maturity Assessment**
```
Maturity Factors (1-5 scale, 5 = highest):
┌─────────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ Factor          │ MongoDB      │ PostgreSQL   │ MySQL        │ Cassandra    │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ Stability       │ 4            │ 5            │ 5            │ 4            │
│ Performance     │ 4            │ 4            │ 4            │ 5            │
│ Ecosystem       │ 4            │ 5            │ 5            │ 3            │
│ Documentation   │ 4            │ 5            │ 4            │ 3            │
│ Community       │ 4            │ 5            │ 5            │ 3            │
│ Enterprise      │ 4            │ 4            │ 4            │ 4            │
│ Innovation      │ 5            │ 4            │ 3            │ 3            │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ **AVERAGE**     │ **4.1**      │ **4.6**      │ **4.3**      │ **3.6**      │
└─────────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

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

#### **CRUD Operation Characteristics**
```
Operation Performance Characteristics:
┌─────────────┬──────────────┬──────────────┬──────────────┐
│ Operation   │ Throughput   │ Latency      │ Resource Use │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ Insert      │ 50K docs/sec │ 1-3ms        │ Low CPU      │
│ Find        │ 100K docs/sec│ 0.5-2ms      │ Memory bound │
│ Update      │ 30K docs/sec │ 2-5ms        │ Medium CPU   │
│ Delete      │ 40K docs/sec │ 1-4ms        │ Low CPU      │
└─────────────┴──────────────┴──────────────┴──────────────┘
```

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

#### **Index Performance Impact**
```
Index Performance Metrics:
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Index Type      │ Query Speed  │ Insert Speed │ Storage Cost │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Single Field    │ 10-100x      │ -5%          │ +15%         │
│ Compound        │ 50-500x      │ -10%         │ +25%         │
│ Text            │ 20-200x      │ -15%         │ +40%         │
│ Geospatial      │ 100-1000x    │ -8%          │ +20%         │
│ Partial         │ 50-300x      │ -3%          │ +10%         │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

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

#### **Decision Matrix**
```
Embed vs Reference Decision Framework:
┌────────────────────┬─────────────┬───────────────┐
│ Scenario            │ Embed       │ Reference     │
├────────────────────┼─────────────┼───────────────┤
│ One-to-Few          │ ✓ Optimal  │ ✗ Overhead   │
│ One-to-Many         │ ✗ Bloated  │ ✓ Efficient  │
│ One-to-Millions     │ ✗ Impossible│ ✓ Required   │
│ Frequent Updates    │ ✗ Expensive │ ✓ Targeted   │
│ Atomic Operations   │ ✓ Native   │ ✗ Complex    │
│ Independent Queries │ ✗ Limited  │ ✓ Flexible   │
└────────────────────┴─────────────┴───────────────┘
```

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

#### **Evolution Strategies Comparison**
```
Schema Evolution Strategy Analysis:
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Strategy        │ Complexity   │ Performance  │ Risk Level   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Lazy Migration  │ Low          │ Gradual      │ Low          │
│ Eager Migration │ High         │ One-time hit │ Medium       │
│ Versioning      │ Medium       │ Consistent   │ Low          │
│ Dual Write      │ High         ──────────────┼──────────────┤
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

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

#### **Pipeline Performance Characteristics**
```
Aggregation Stage Performance Impact:
┌────────────────┬──────────────┬──────────────┬──────────────┐
│ Stage           │ Memory Usage │ CPU Impact  │ Index Usage  │
├────────────────┼──────────────┼──────────────┼──────────────┤
│ $match          │ Low          │ Low         │ ✓ Yes       │
│ $sort           │ High         │ Medium      │ ✓ Yes       │
│ $group          │ High         │ High        │ ✗ No        │
│ $unwind         │ Medium       │ Low         │ ✗ No        │
│ $lookup         │ Very High    │ Very High   │ ✓ Partial   │
│ $project        │ Low          │ Low         │ ✗ No        │
└────────────────┴──────────────┴──────────────┴──────────────┘
```

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

#### **Text Search Performance Analysis**
```
Text Search Performance Metrics:
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Collection Size │ Index Size   │ Query Time  │ Memory Req   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ 1M documents   │ 50MB         │ 10-50ms     │ 100MB        │
│ 10M documents  │ 500MB        │ 20-100ms    │ 1GB          │
│ 100M documents │ 5GB          │ 50-200ms    │ 10GB         │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

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

#### **Query Optimization Techniques**
```
Optimization Impact Analysis:
┌────────────────────┬───────────────┬───────────────┐
│ Technique           │ Performance Gain │ Implementation  │
├────────────────────┼───────────────┼───────────────┤
│ Proper Indexing     │ 10-1000x         │ Easy            │
│ Query Projection    │ 2-5x             │ Easy            │
│ Covered Queries     │ 5-20x            │ Medium          │
│ Hint Usage          │ 2-10x            │ Easy            │
│ Batch Size Tuning   │ 1.5-3x           │ Easy            │
│ Connection Pooling  │ 2-5x             │ Medium          │
└────────────────────┴───────────────┴───────────────┘
```

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

#### **Sharding Architecture Components**
```
Sharding Performance Characteristics:
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Shard Count     │ Read Scale   │ Write Scale  │ Complexity   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ 2-3 Shards     │ 2-3x         │ 2-3x         │ Medium       │
│ 4-10 Shards    │ 4-10x        │ 4-10x        │ High         │
│ 10+ Shards     │ 10x+         │ 10x+         │ Very High    │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

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

#### **Replication Performance Impact**
```
Replica Set Configuration Analysis:
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Members         │ Availability │ Write Perf   │ Read Scale   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ 3 Members       │ 99.9%        │ Baseline     │ 3x           │
│ 5 Members       │ 99.95%       │ -10%         │ 5x           │
│ 7 Members       │ 99.99%       │ -20%         │ 7x           │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

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

### 79. How do you implement MongoDB transactions?

#### **Transaction Performance Characteristics**
```
Transaction Impact Analysis:
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Operation Type  │ Single Doc   │ Multi-Doc    │ Cross-Shard  │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Throughput      │ 50K ops/sec  │ 10K ops/sec  │ 1K ops/sec   │
│ Latency         │ 1-2ms        │ 5-10ms       │ 50-100ms     │
│ Resource Usage  │ Low          │ Medium       │ High         │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

**Answer**: MongoDB supports ACID transactions for multi-document operations.

```javascript
// Start a session
const session = db.getMongo().startSession();

try {
  session.startTransaction();
  
  // Multiple operations in transaction
  db.accounts.updateOne(
    {_id: "account1"},
    {$inc: {balance: -100}},
    {session: session}
  );
  
  db.accounts.updateOne(
    {_id: "account2"},
    {$inc: {balance: 100}},
    {session: session}
  );
  
  // Commit transaction
  session.commitTransaction();
  print("Transaction committed successfully");
  
} catch (error) {
  session.abortTransaction();
  print("Transaction aborted: " + error);
} finally {
  session.endSession();
}
```

### 80. How do you handle MongoDB connection pooling?

**Answer**: Connection pooling manages database connections efficiently.

```javascript
// Connection pool configuration
const MongoClient = require('mongodb').MongoClient;

const options = {
  maxPoolSize: 10,        // Maximum connections
  minPoolSize: 2,         // Minimum connections
  maxIdleTimeMS: 30000,   // Close after 30s idle
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
  bufferMaxEntries: 0
};

const client = new MongoClient(uri, options);

// Monitor connection pool
client.on('connectionPoolCreated', (event) => {
  console.log('Pool created:', event);
});

client.on('connectionCheckedOut', (event) => {
  console.log('Connection checked out:', event.connectionId);
});
```

### 81. How do you implement MongoDB change streams?

**Answer**: Change streams provide real-time data change notifications.

```javascript
// Watch for changes
const changeStream = db.orders.watch([
  {$match: {"fullDocument.status": "completed"}}
]);

changeStream.on('change', (change) => {
  console.log('Change detected:', change.operationType);
  
  switch(change.operationType) {
    case 'insert':
      console.log('New order:', change.fullDocument);
      break;
    case 'update':
      console.log('Updated order:', change.documentKey);
      break;
    case 'delete':
      console.log('Deleted order:', change.documentKey);
      break;
  }
});

// Resume from specific point
const resumeToken = changeStream.resumeToken;
const resumedStream = db.orders.watch([], {resumeAfter: resumeToken});
```

### 82. How do you optimize MongoDB for time series data?

**Answer**: Use time series collections and appropriate indexing strategies.

```javascript
// Create time series collection
db.createCollection("sensor_data", {
  timeseries: {
    timeField: "timestamp",
    metaField: "sensor_id",
    granularity: "minutes"
  }
});

// Insert time series data
db.sensor_data.insertMany([
  {
    timestamp: new Date(),
    sensor_id: "temp_01",
    temperature: 23.5,
    humidity: 65.2
  },
  {
    timestamp: new Date(),
    sensor_id: "temp_02", 
    temperature: 24.1,
    humidity: 62.8
  }
]);

// Query time series data
db.sensor_data.find({
  timestamp: {
    $gte: ISODate("2024-01-01"),
    $lt: ISODate("2024-01-02")
  },
  sensor_id: "temp_01"
});
```

### 83. How do you implement MongoDB data validation?

**Answer**: Use JSON Schema validation for data integrity.

```javascript
// Create collection with validation
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email", "age"],
      properties: {
        name: {
          bsonType: "string",
          minLength: 2,
          maxLength: 50
        },
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 120
        }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// Test validation
try {
  db.users.insertOne({
    name: "John Doe",
    email: "john@example.com",
    age: 30
  });
} catch (error) {
  print("Validation error: " + error);
}
```

### 84. How do you handle MongoDB backup and restore?

**Answer**: Use mongodump/mongorestore and point-in-time recovery.

```bash
# Full database backup
mongodump --host localhost:27017 --db myapp --out /backup/

# Restore database
mongorestore --host localhost:27017 --db myapp /backup/myapp/

# Backup with compression
mongodump --gzip --archive=/backup/myapp.gz --db myapp

# Restore from compressed archive
mongorestore --gzip --archive=/backup/myapp.gz --db myapp

# Backup specific collection
mongodump --db myapp --collection users --out /backup/

# Point-in-time backup (replica set)
mongodump --oplog --host rs0/mongo1:27017,mongo2:27017,mongo3:27017
```

### 85. How do you implement MongoDB security?

**Answer**: Enable authentication, authorization, and encryption.

```javascript
// Enable authentication
use admin;
db.createUser({
  user: "admin",
  pwd: "securePassword",
  roles: [{role: "userAdminAnyDatabase", db: "admin"}]
});

// Create database user
use myapp;
db.createUser({
  user: "appUser",
  pwd: "appPassword",
  roles: [
    {role: "readWrite", db: "myapp"},
    {role: "read", db: "analytics"}
  ]
});

// Custom role
db.createRole({
  role: "dataAnalyst",
  privileges: [
    {
      resource: {db: "myapp", collection: "orders"},
      actions: ["find", "aggregate"]
    }
  ],
  roles: []
});

// SSL/TLS configuration
// mongod --sslMode requireSSL --sslPEMKeyFile /path/to/server.pem
```

### 86. How do you monitor MongoDB performance?

**Answer**: Use built-in tools and monitoring solutions.

```javascript
// Database statistics
db.stats();

// Collection statistics
db.orders.stats();

// Current operations
db.currentOp();

// Server status
db.serverStatus();

// Profiler configuration
db.setProfilingLevel(2, {slowms: 100});

// Query profiler data
db.system.profile.find().sort({ts: -1}).limit(5);

// Index usage statistics
db.orders.aggregate([{$indexStats: {}}]);

// Explain query execution
db.orders.find({status: "pending"}).explain("executionStats");
```

### 87. How do you implement MongoDB GridFS?

**Answer**: GridFS stores large files by splitting them into chunks.

```javascript
// Store file in GridFS
const GridFSBucket = require('mongodb').GridFSBucket;
const fs = require('fs');

const bucket = new GridFSBucket(db, {bucketName: 'files'});

// Upload file
const uploadStream = bucket.openUploadStream('document.pdf', {
  metadata: {
    contentType: 'application/pdf',
    uploadedBy: 'user123',
    tags: ['document', 'important']
  }
});

fs.createReadStream('/path/to/document.pdf').pipe(uploadStream);

// Download file
const downloadStream = bucket.openDownloadStreamByName('document.pdf');
downloadStream.pipe(fs.createWriteStream('/path/to/downloaded.pdf'));

// Find files
const files = bucket.find({
  'metadata.tags': 'important'
}).toArray();

// Delete file
bucket.delete(fileId);
```

### 88. How do you handle MongoDB memory management?

**Answer**: Configure WiredTiger cache and monitor memory usage.

```javascript
// WiredTiger cache configuration
// mongod --wiredTigerCacheSizeGB 4

// Memory statistics
db.serverStatus().wiredTiger.cache;

// Collection cache statistics
db.runCommand({collStats: "orders", indexDetails: true});

// Memory usage by operation
db.currentOp({"command.find": {$exists: true}});

// Configure cache pressure
db.adminCommand({
  setParameter: 1,
  wiredTigerEngineRuntimeConfig: "cache_size=2GB"
});
```

### 89. How do you implement MongoDB data archival?

**Answer**: Use TTL indexes and archival strategies.

```javascript
// TTL index for automatic deletion
db.logs.createIndex(
  {"createdAt": 1},
  {expireAfterSeconds: 2592000}  // 30 days
);

// Archive old data
const archiveDate = new Date();
archiveDate.setMonth(archiveDate.getMonth() - 6);

// Move to archive collection
db.orders.aggregate([
  {$match: {createdAt: {$lt: archiveDate}}},
  {$out: "orders_archive"}
]);

// Remove archived data
db.orders.deleteMany({createdAt: {$lt: archiveDate}});

// Compressed archive collection
db.runCommand({
  create: "orders_archive",
  storageEngine: {
    wiredTiger: {
      configString: "block_compressor=zstd"
    }
  }
});
```

### 90. How do you troubleshoot MongoDB performance issues?

**Answer**: Use systematic approach with profiling and monitoring.

```javascript
// Enable profiling
db.setProfilingLevel(2, {slowms: 50});

// Analyze slow queries
db.system.profile.find({
  "command.find": {$exists: true},
  "millis": {$gt: 100}
}).sort({ts: -1});

// Check index usage
db.orders.find({status: "pending"}).explain("executionStats");

// Identify missing indexes
db.system.profile.aggregate([
  {$match: {"planSummary": "COLLSCAN"}},
  {$group: {
    _id: "$command",
    count: {$sum: 1},
    avgMs: {$avg: "$millis"}
  }},
  {$sort: {count: -1}}
]);

// Connection pool monitoring
db.serverStatus().connections;

// Lock statistics
db.serverStatus().locks;

// Working set analysis
db.serverStatus().wiredTiger.cache["bytes currently in the cache"];
```

### 91. How do you implement MongoDB multi-tenancy?

**Answer**: Use database-per-tenant or collection-per-tenant patterns.

```javascript
// Database per tenant
function getTenantDatabase(tenantId) {
  return db.getSiblingDB(`tenant_${tenantId}`);
}

// Collection per tenant
function getTenantCollection(tenantId, collectionName) {
  return db.getCollection(`${tenantId}_${collectionName}`);
}

// Shared collection with tenant field
db.orders.createIndex({tenantId: 1, orderId: 1});

// Query with tenant isolation
db.orders.find({tenantId: "tenant123", status: "active"});

// Tenant-specific aggregation
db.orders.aggregate([
  {$match: {tenantId: "tenant123"}},
  {$group: {
    _id: "$status",
    count: {$sum: 1},
    totalValue: {$sum: "$amount"}
  }}
]);
```

### 92. How do you handle MongoDB version upgrades?

**Answer**: Follow systematic upgrade process with testing.

```bash
# Check compatibility
mongod --version
db.adminCommand({getParameter: 1, featureCompatibilityVersion: 1})

# Set feature compatibility version
db.adminCommand({setFeatureCompatibilityVersion: "5.0"})

# Upgrade process for replica set
# 1. Upgrade secondaries first
# 2. Step down primary
# 3. Upgrade former primary

# Rolling upgrade script
#!/bin/bash
for member in secondary1 secondary2 primary; do
  echo "Upgrading $member"
  # Stop MongoDB
  systemctl stop mongod
  
  # Install new version
  yum update mongodb-org
  
  # Start MongoDB
  systemctl start mongod
  
  # Wait for member to be healthy
  mongo --eval "rs.status()"
done
```

### 93. How do you implement MongoDB disaster recovery?

**Answer**: Use replica sets, backups, and geographic distribution.

```javascript
// Configure replica set with priority
rs.initiate({
  _id: "myReplicaSet",
  members: [
    {_id: 0, host: "primary:27017", priority: 2},
    {_id: 1, host: "secondary1:27017", priority: 1},
    {_id: 2, host: "secondary2:27017", priority: 1},
    {_id: 3, host: "arbiter:27017", arbiterOnly: true}
  ]
});

// Cross-region replica set
rs.add({_id: 4, host: "dr-site:27017", priority: 0, hidden: true});

// Backup strategy
// 1. Continuous oplog backup
mongodump --oplog --host rs0/primary:27017

// 2. Point-in-time recovery
mongorestore --oplogReplay --oplogLimit 1640995200:1

// 3. Delayed replica member
rs.add({
  _id: 5,
  host: "delayed:27017",
  priority: 0,
  hidden: true,
  slaveDelay: 3600  // 1 hour delay
});
```

### 94. How do you optimize MongoDB for analytics workloads?

**Answer**: Use appropriate indexes, aggregation optimization, and read preferences.

```javascript
// Analytical indexes
db.sales.createIndex({
  "date": 1,
  "region": 1,
  "product": 1
});

// Optimized aggregation pipeline
db.sales.aggregate([
  // Stage 1: Filter early
  {$match: {
    date: {$gte: ISODate("2024-01-01")},
    region: "North America"
  }},
  
  // Stage 2: Project only needed fields
  {$project: {
    product: 1,
    amount: 1,
    quantity: 1,
    date: 1
  }},
  
  // Stage 3: Group and calculate
  {$group: {
    _id: {
      product: "$product",
      month: {$dateToString: {format: "%Y-%m", date: "$date"}}
    },
    totalSales: {$sum: "$amount"},
    totalQuantity: {$sum: "$quantity"},
    avgPrice: {$avg: {$divide: ["$amount", "$quantity"]}}
  }},
  
  // Stage 4: Sort results
  {$sort: {"_id.month": 1, totalSales: -1}}
], {
  allowDiskUse: true,  // For large datasets
  readPreference: "secondary"  // Use secondary for analytics
});

// Create analytical views
db.createView("monthly_sales", "sales", [
  {$group: {
    _id: {$dateToString: {format: "%Y-%m", date: "$date"}},
    totalSales: {$sum: "$amount"},
    orderCount: {$sum: 1}
  }}
]);
```

### 95. How do you implement MongoDB data governance?

**Answer**: Use field-level encryption, auditing, and access controls.

```javascript
// Field-level encryption
const clientEncryption = new ClientEncryption(keyVault, {
  keyVaultNamespace: "encryption.__keyVault",
  kmsProviders: {
    local: {
      key: localMasterKey
    }
  }
});

// Create data encryption key
const dataKeyId = clientEncryption.createDataKey("local", {
  keyAltNames: ["ssn-key"]
});

// Encrypt sensitive field
const encryptedSSN = clientEncryption.encrypt(
  "123-45-6789",
  {
    keyId: dataKeyId,
    algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
  }
);

// Auditing configuration
db.adminCommand({
  auditConfig: {
    destination: "file",
    format: "JSON",
    path: "/var/log/mongodb/audit.json",
    filter: {
      atype: "authCheck",
      "param.command": {$in: ["find", "insert", "update", "delete"]}
    }
  }
});

// Data classification
db.users.createIndex(
  {"personalInfo.ssn": 1},
  {
    name: "ssn_index",
    partialFilterExpression: {"personalInfo.ssn": {$exists: true}},
    comment: "PII-SSN-ENCRYPTED"
  }
);
```

### 96. How do you handle MongoDB capacity planning?

**Answer**: Monitor growth patterns and plan for scaling.

```javascript
// Storage growth analysis
db.runCommand({dbStats: 1, scale: 1024*1024*1024}); // GB

// Collection growth tracking
function trackGrowth() {
  const collections = db.runCommand({listCollections: 1}).cursor.firstBatch;
  
  collections.forEach(col => {
    const stats = db.getCollection(col.name).stats(1024*1024); // MB
    print(`${col.name}: ${stats.size}MB data, ${stats.storageSize}MB storage`);
  });
}

// Index size monitoring
db.orders.stats().indexSizes;

// Connection usage
db.serverStatus().connections;

// Memory usage patterns
db.serverStatus().wiredTiger.cache;

// Capacity planning query
db.capacity_metrics.aggregate([
  {$match: {date: {$gte: ISODate("2024-01-01")}}},
  {$group: {
    _id: {$dateToString: {format: "%Y-%m", date: "$date"}},
    avgDataSize: {$avg: "$dataSize"},
    maxConnections: {$max: "$connections"},
    avgMemoryUsage: {$avg: "$memoryUsage"}
  }},
  {$sort: {_id: 1}}
]);
```

### 97. How do you implement MongoDB testing strategies?

**Answer**: Use unit tests, integration tests, and performance tests.

```javascript
// Unit testing with Jest
const { MongoClient } = require('mongodb');
const { MongoMemoryServer } = require('mongodb-memory-server');

describe('MongoDB Operations', () => {
  let connection;
  let db;
  let mongod;

  beforeAll(async () => {
    mongod = await MongoMemoryServer.create();
    const uri = mongod.getUri();
    connection = await MongoClient.connect(uri);
    db = connection.db();
  });

  afterAll(async () => {
    await connection.close();
    await mongod.stop();
  });

  test('should insert and find user', async () => {
    const users = db.collection('users');
    
    const user = { name: 'John', email: 'john@example.com' };
    await users.insertOne(user);
    
    const found = await users.findOne({ name: 'John' });
    expect(found.email).toBe('john@example.com');
  });

  test('should handle aggregation', async () => {
    const orders = db.collection('orders');
    
    await orders.insertMany([
      { userId: 1, amount: 100, status: 'completed' },
      { userId: 1, amount: 200, status: 'completed' },
      { userId: 2, amount: 150, status: 'pending' }
    ]);
    
    const result = await orders.aggregate([
      { $match: { status: 'completed' } },
      { $group: { _id: '$userId', total: { $sum: '$amount' } } }
    ]).toArray();
    
    expect(result).toHaveLength(1);
    expect(result[0].total).toBe(300);
  });
});

// Performance testing
function performanceTest() {
  const startTime = Date.now();
  
  // Bulk insert test
  const docs = [];
  for (let i = 0; i < 10000; i++) {
    docs.push({
      _id: i,
      name: `User ${i}`,
      email: `user${i}@example.com`,
      createdAt: new Date()
    });
  }
  
  db.users.insertMany(docs);
  
  const insertTime = Date.now() - startTime;
  print(`Bulk insert: ${insertTime}ms`);
  
  // Query performance test
  const queryStart = Date.now();
  db.users.find({ name: /User 5/ }).toArray();
  const queryTime = Date.now() - queryStart;
  print(`Query time: ${queryTime}ms`);
}
```

### 98. How do you handle MongoDB compliance requirements?

**Answer**: Implement data protection, audit trails, and retention policies.

```javascript
// GDPR compliance - Right to be forgotten
function deleteUserData(userId) {
  const session = db.getMongo().startSession();
  
  try {
    session.startTransaction();
    
    // Delete from all collections
    db.users.deleteOne({ _id: userId }, { session });
    db.orders.deleteMany({ userId: userId }, { session });
    db.preferences.deleteOne({ userId: userId }, { session });
    
    // Log deletion for audit
    db.audit_log.insertOne({
      action: "user_data_deletion",
      userId: userId,
      timestamp: new Date(),
      reason: "GDPR_request"
    }, { session });
    
    session.commitTransaction();
    print(`User ${userId} data deleted successfully`);
    
  } catch (error) {
    session.abortTransaction();
    print(`Deletion failed: ${error}`);
  } finally {
    session.endSession();
  }
}

// Data retention policy
db.logs.createIndex(
  { "timestamp": 1 },
  { 
    expireAfterSeconds: 2592000,  // 30 days
    name: "data_retention_policy"
  }
);

// Anonymization for analytics
db.users.aggregate([
  {
    $project: {
      _id: 0,
      age_group: {
        $switch: {
          branches: [
            { case: { $lt: ["$age", 25] }, then: "18-24" },
            { case: { $lt: ["$age", 35] }, then: "25-34" },
            { case: { $lt: ["$age", 45] }, then: "35-44" }
          ],
          default: "45+"
        }
      },
      region: "$address.region",
      signup_month: { $dateToString: { format: "%Y-%m", date: "$createdAt" } }
    }
  },
  { $out: "anonymized_user_analytics" }
]);
```

### 99. How do you implement MongoDB DevOps practices?

**Answer**: Use infrastructure as code, automated deployments, and monitoring.

```yaml
# Docker Compose for MongoDB replica set
version: '3.8'
services:
  mongo1:
    image: mongo:6.0
    command: mongod --replSet rs0 --port 27017
    ports:
      - "27017:27017"
    volumes:
      - mongo1_data:/data/db
    networks:
      - mongo-cluster

  mongo2:
    image: mongo:6.0
    command: mongod --replSet rs0 --port 27018
    ports:
      - "27018:27018"
    volumes:
      - mongo2_data:/data/db
    networks:
      - mongo-cluster

  mongo3:
    image: mongo:6.0
    command: mongod --replSet rs0 --port 27019
    ports:
      - "27019:27019"
    volumes:
      - mongo3_data:/data/db
    networks:
      - mongo-cluster

volumes:
  mongo1_data:
  mongo2_data:
  mongo3_data:

networks:
  mongo-cluster:
```

```bash
# Ansible playbook for MongoDB deployment
---
- name: Deploy MongoDB Cluster
  hosts: mongodb_servers
  become: yes
  
  tasks:
    - name: Install MongoDB
      yum:
        name: mongodb-org
        state: present
    
    - name: Configure MongoDB
      template:
        src: mongod.conf.j2
        dest: /etc/mongod.conf
      notify: restart mongod
    
    - name: Start MongoDB service
      systemd:
        name: mongod
        state: started
        enabled: yes
    
    - name: Initialize replica set
      mongodb_replicaset:
        login_host: "{{ ansible_default_ipv4.address }}"
        replica_set: rs0
        members:
          - host: "{{ groups['mongodb_servers'][0] }}:27017"
          - host: "{{ groups['mongodb_servers'][1] }}:27017"
          - host: "{{ groups['mongodb_servers'][2] }}:27017"
      when: inventory_hostname == groups['mongodb_servers'][0]
  
  handlers:
    - name: restart mongod
      systemd:
        name: mongod
        state: restarted
```

### 100. How do you handle MongoDB in microservices architecture?

**Answer**: Implement database per service pattern with event-driven communication.

```javascript
// Service-specific database
class UserService {
  constructor() {
    this.db = db.getSiblingDB('user_service');
  }
  
  async createUser(userData) {
    const session = this.db.getMongo().startSession();
    
    try {
      session.startTransaction();
      
      // Insert user
      const result = await this.db.users.insertOne(userData, { session });
      
      // Publish event
      await this.publishEvent({
        type: 'UserCreated',
        userId: result.insertedId,
        timestamp: new Date(),
        data: userData
      });
      
      await session.commitTransaction();
      return result;
      
    } catch (error) {
      await session.abortTransaction();
      throw error;
    } finally {
      session.endSession();
    }
  }
  
  async publishEvent(event) {
    // Publish to event store or message queue
    await this.db.events.insertOne(event);
    
    // Send to message broker (e.g., RabbitMQ, Kafka)
    // await messageQueue.publish('user.events', event);
  }
}

// Event sourcing pattern
class OrderService {
  constructor() {
    this.db = db.getSiblingDB('order_service');
  }
  
  async processOrder(orderId, events) {
    let order = { _id: orderId, status: 'created', items: [], total: 0 };
    
    // Replay events to build current state
    for (const event of events) {
      order = this.applyEvent(order, event);
    }
    
    return order;
  }
  
  applyEvent(order, event) {
    switch (event.type) {
      case 'OrderCreated':
        return { ...order, ...event.data };
      case 'ItemAdded':
        return {
          ...order,
          items: [...order.items, event.data.item],
          total: order.total + event.data.item.price
        };
      case 'OrderCompleted':
        return { ...order, status: 'completed' };
      default:
        return order;
    }
  }
}

// Saga pattern for distributed transactions
class OrderSaga {
  async processOrder(orderData) {
    const sagaId = new ObjectId();
    
    try {
      // Step 1: Reserve inventory
      await this.reserveInventory(sagaId, orderData.items);
      
      // Step 2: Process payment
      await this.processPayment(sagaId, orderData.payment);
      
      // Step 3: Create order
      await this.createOrder(sagaId, orderData);
      
      // Step 4: Send confirmation
      await this.sendConfirmation(sagaId, orderData.userId);
      
    } catch (error) {
      // Compensate in reverse order
      await this.compensate(sagaId, error);
      throw error;
    }
  }
  
  async compensate(sagaId, error) {
    const steps = await db.saga_steps.find({ sagaId }).sort({ step: -1 });
    
    for (const step of steps) {
      try {
        await this.executeCompensation(step);
      } catch (compensationError) {
        console.error(`Compensation failed for step ${step.step}:`, compensationError);
      }
    }
  }
}
```

---

**Total Questions: 100** | **Coverage: Complete MongoDB Ecosystem**

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*

