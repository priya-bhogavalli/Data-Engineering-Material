# MongoDB Interview Questions

## Table of Contents

1. [Basic MongoDB Concepts](#basic-mongodb-concepts)
2. [Data Modeling](#data-modeling)
3. [Querying and Aggregation](#querying-and-aggregation)
4. [Performance and Indexing](#performance-and-indexing)
5. [Replication and Sharding](#replication-and-sharding)
6. [Data Engineering Scenarios](#data-engineering-scenarios)

---

## Basic MongoDB Concepts

### Q1: What is MongoDB and how does it differ from relational databases?

**Answer:**
MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents (BSON). Unlike relational databases with fixed schemas and tables, MongoDB uses collections of documents with dynamic schemas.

**Key Differences:**
- **Schema**: Flexible vs Fixed
- **Data Model**: Document-oriented vs Table-based
- **Relationships**: Embedded documents/references vs Foreign keys
- **Scaling**: Horizontal (sharding) vs Vertical primarily

**Code Example:**
```javascript
// MongoDB document structure
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "John Doe",
  "email": "john@example.com",
  "addresses": [
    {
      "type": "home",
      "street": "123 Main St",
      "city": "New York"
    }
  ],
  "orders": [
    {
      "order_id": "ORD001",
      "amount": 99.99,
      "date": ISODate("2023-01-15")
    }
  ]
}
```

### Q2: Explain BSON and its advantages over JSON.

**Answer:**
BSON (Binary JSON) is MongoDB's binary representation of JSON documents. It extends JSON with additional data types and is optimized for storage and traversal.

**Advantages:**
- **Additional Types**: Date, ObjectId, Binary data, Decimal128
- **Performance**: Faster parsing and encoding
- **Size Efficiency**: More compact for certain data types
- **Traversal**: Includes length prefixes for faster navigation

**Code Example:**
```javascript
// BSON supports additional types not in JSON
{
  "date": ISODate("2023-01-15T10:30:00Z"),
  "objectId": ObjectId("507f1f77bcf86cd799439011"),
  "binary": BinData(0, "SGVsbG8gV29ybGQ="),
  "decimal": NumberDecimal("99.99"),
  "long": NumberLong("9223372036854775807")
}
```

### Q3: What are the different types of relationships in MongoDB?

**Answer:**
MongoDB supports three types of relationships: One-to-One, One-to-Many, and Many-to-Many, implemented through embedding or referencing.

**Implementation Strategies:**
- **Embedding**: Store related data within the same document
- **Referencing**: Store references (ObjectIds) to other documents

**Code Example:**
```javascript
// One-to-One (Embedded)
{
  "_id": ObjectId("..."),
  "name": "John Doe",
  "profile": {
    "bio": "Software Engineer",
    "avatar": "profile.jpg"
  }
}

// One-to-Many (Embedded)
{
  "_id": ObjectId("..."),
  "title": "Blog Post",
  "comments": [
    {"author": "Alice", "text": "Great post!"},
    {"author": "Bob", "text": "Thanks for sharing"}
  ]
}

// One-to-Many (Referenced)
// User document
{
  "_id": ObjectId("user1"),
  "name": "John Doe"
}

// Order documents
{
  "_id": ObjectId("order1"),
  "user_id": ObjectId("user1"),
  "amount": 99.99
}
```

## Data Modeling

### Q4: When should you embed vs reference documents in MongoDB?

**Answer:**
Choose embedding for data that is accessed together and has a clear containment relationship. Choose referencing for data that is accessed independently or when documents would become too large.

**Embed When:**
- Data is accessed together frequently
- One-to-few relationships
- Data doesn't change often
- Document size remains manageable (<16MB)

**Reference When:**
- Data is accessed independently
- One-to-many with large "many" side
- Data changes frequently
- Need to avoid document growth

**Code Example:**
```javascript
// Good for embedding (user profile)
{
  "_id": ObjectId("..."),
  "username": "johndoe",
  "profile": {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com"
  }
}

// Good for referencing (user orders)
// User
{
  "_id": ObjectId("user1"),
  "username": "johndoe"
}

// Orders (separate collection)
{
  "_id": ObjectId("order1"),
  "userId": ObjectId("user1"),
  "items": [...],
  "total": 299.99
}
```

### Q5: How do you handle schema evolution in MongoDB?

**Answer:**
MongoDB's flexible schema allows gradual migration without downtime. Use versioning, default values, and application-level handling for schema changes.

**Strategies:**
- **Versioning**: Add schema version field
- **Gradual Migration**: Update documents as accessed
- **Default Values**: Handle missing fields in application
- **Migration Scripts**: Bulk update for major changes

**Code Example:**
```javascript
// Schema versioning approach
{
  "_id": ObjectId("..."),
  "schemaVersion": 2,
  "name": "John Doe",
  "contactInfo": {  // v2: restructured from separate fields
    "email": "john@example.com",
    "phone": "+1234567890"
  }
}

// Application code handling versions
function getUser(doc) {
  if (doc.schemaVersion === 1) {
    // Handle old schema
    return {
      name: doc.name,
      email: doc.email,
      phone: doc.phone
    };
  } else {
    // Handle new schema
    return {
      name: doc.name,
      email: doc.contactInfo.email,
      phone: doc.contactInfo.phone
    };
  }
}
```

## Querying and Aggregation

### Q6: Explain MongoDB's aggregation pipeline and provide a complex example.

**Answer:**
The aggregation pipeline processes documents through multiple stages, each transforming the data. It's MongoDB's framework for data analysis and transformation.

**Common Stages:**
- `$match`: Filter documents
- `$group`: Group and aggregate
- `$project`: Reshape documents
- `$sort`: Sort results
- `$lookup`: Join collections

**Code Example:**
```javascript
// Complex aggregation: Sales analysis by region and product category
db.orders.aggregate([
  // Stage 1: Filter recent orders
  {
    $match: {
      orderDate: {
        $gte: ISODate("2023-01-01"),
        $lt: ISODate("2024-01-01")
      },
      status: "completed"
    }
  },
  
  // Stage 2: Unwind order items
  {
    $unwind: "$items"
  },
  
  // Stage 3: Lookup product details
  {
    $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "productInfo"
    }
  },
  
  // Stage 4: Unwind product info
  {
    $unwind: "$productInfo"
  },
  
  // Stage 5: Group by region and category
  {
    $group: {
      _id: {
        region: "$shippingAddress.region",
        category: "$productInfo.category"
      },
      totalRevenue: {
        $sum: {
          $multiply: ["$items.quantity", "$items.price"]
        }
      },
      totalQuantity: { $sum: "$items.quantity" },
      orderCount: { $sum: 1 },
      avgOrderValue: { $avg: "$items.price" }
    }
  },
  
  // Stage 6: Sort by revenue
  {
    $sort: { totalRevenue: -1 }
  },
  
  // Stage 7: Project final structure
  {
    $project: {
      _id: 0,
      region: "$_id.region",
      category: "$_id.category",
      totalRevenue: { $round: ["$totalRevenue", 2] },
      totalQuantity: 1,
      orderCount: 1,
      avgOrderValue: { $round: ["$avgOrderValue", 2] }
    }
  }
]);

// Output example:
[
  {
    "region": "North America",
    "category": "Electronics",
    "totalRevenue": 125000.50,
    "totalQuantity": 450,
    "orderCount": 89,
    "avgOrderValue": 278.65
  }
]
```

### Q7: How do you optimize MongoDB queries for better performance?

**Answer:**
Query optimization involves proper indexing, query structure, and understanding execution plans.

**Optimization Techniques:**
- **Indexing**: Create appropriate indexes
- **Query Structure**: Use efficient operators
- **Projection**: Limit returned fields
- **Explain Plans**: Analyze query execution

**Code Example:**
```javascript
// Before optimization
db.users.find({
  "profile.age": { $gte: 25, $lte: 35 },
  "location.city": "New York",
  "interests": "technology"
});

// Create compound index
db.users.createIndex({
  "location.city": 1,
  "profile.age": 1,
  "interests": 1
});

// Optimized query with projection
db.users.find(
  {
    "location.city": "New York",
    "profile.age": { $gte: 25, $lte: 35 },
    "interests": "technology"
  },
  {
    "name": 1,
    "email": 1,
    "profile.age": 1
  }
);

// Analyze query performance
db.users.find({...}).explain("executionStats");
```

## Performance and Indexing

### Q8: Explain different types of indexes in MongoDB and when to use each.

**Answer:**
MongoDB supports various index types optimized for different query patterns and data types.

**Index Types:**
- **Single Field**: Basic index on one field
- **Compound**: Index on multiple fields
- **Multikey**: Automatically created for array fields
- **Text**: Full-text search
- **Geospatial**: Location-based queries
- **Hashed**: Sharding and equality queries

**Code Example:**
```javascript
// Single field index
db.users.createIndex({ "email": 1 });

// Compound index (order matters)
db.orders.createIndex({ 
  "customerId": 1, 
  "orderDate": -1, 
  "status": 1 
});

// Text index for search
db.products.createIndex({ 
  "name": "text", 
  "description": "text" 
});

// Geospatial index
db.stores.createIndex({ "location": "2dsphere" });

// Partial index (conditional)
db.users.createIndex(
  { "email": 1 },
  { 
    partialFilterExpression: { 
      "email": { $exists: true } 
    } 
  }
);

// TTL index (auto-delete)
db.sessions.createIndex(
  { "createdAt": 1 },
  { expireAfterSeconds: 3600 }
);
```

## Replication and Sharding

### Q9: Explain MongoDB replication and its benefits.

**Answer:**
MongoDB replication maintains multiple copies of data across different servers using replica sets, providing high availability and data redundancy.

**Components:**
- **Primary**: Receives all write operations
- **Secondary**: Replicates primary's data
- **Arbiter**: Participates in elections only

**Benefits:**
- High availability
- Data redundancy
- Read scaling
- Automatic failover

**Code Example:**
```javascript
// Replica set configuration
rs.initiate({
  _id: "myReplicaSet",
  members: [
    { _id: 0, host: "mongodb1.example.com:27017" },
    { _id: 1, host: "mongodb2.example.com:27017" },
    { _id: 2, host: "mongodb3.example.com:27017" }
  ]
});

// Read preference configuration
db.users.find().readPref("secondary");

// Connection string with replica set
mongodb://mongodb1.example.com:27017,mongodb2.example.com:27017,mongodb3.example.com:27017/mydb?replicaSet=myReplicaSet
```

### Q10: When and how do you implement sharding in MongoDB?

**Answer:**
Sharding distributes data across multiple machines to handle large datasets and high throughput operations that exceed single server capacity.

**When to Shard:**
- Dataset exceeds single server capacity
- Write operations exceed single server capability
- Working set exceeds server RAM

**Sharding Components:**
- **Shard**: Data partition
- **Config Servers**: Metadata storage
- **Query Router (mongos)**: Routes queries

**Code Example:**
```javascript
// Enable sharding for database
sh.enableSharding("ecommerce");

// Choose shard key (critical decision)
sh.shardCollection("ecommerce.orders", { "customerId": 1, "orderDate": 1 });

// Shard key considerations:
// Good: High cardinality, even distribution
// Bad: Monotonically increasing values

// Example of compound shard key
sh.shardCollection("ecommerce.products", { 
  "category": 1, 
  "_id": "hashed" 
});
```

## Data Engineering Scenarios

### Q11: How would you design a real-time analytics system using MongoDB?

**Answer:**
Design involves change streams for real-time data capture, aggregation pipelines for processing, and proper indexing for query performance.

**Architecture Components:**
- Change streams for real-time updates
- Aggregation pipelines for data processing
- Time-series collections for metrics
- Proper indexing strategy

**Code Example:**
```javascript
// Real-time order processing system
// 1. Set up change stream
const changeStream = db.orders.watch([
  { $match: { "operationType": "insert" } }
]);

changeStream.on("change", (change) => {
  const order = change.fullDocument;
  
  // Update real-time metrics
  db.metrics.updateOne(
    { 
      date: new Date().toISOString().split('T')[0],
      region: order.region 
    },
    {
      $inc: {
        totalOrders: 1,
        totalRevenue: order.total
      }
    },
    { upsert: true }
  );
});

// 2. Aggregation for dashboard metrics
db.orders.aggregate([
  {
    $match: {
      orderDate: {
        $gte: new Date(Date.now() - 24*60*60*1000) // Last 24 hours
      }
    }
  },
  {
    $group: {
      _id: {
        hour: { $hour: "$orderDate" },
        region: "$region"
      },
      orderCount: { $sum: 1 },
      revenue: { $sum: "$total" },
      avgOrderValue: { $avg: "$total" }
    }
  }
]);

// 3. Time-series collection for metrics
db.createCollection("hourlyMetrics", {
  timeseries: {
    timeField: "timestamp",
    metaField: "region",
    granularity: "hours"
  }
});
```

### Q12: How do you handle large data migrations in MongoDB?

**Answer:**
Large migrations require careful planning, chunking, monitoring, and rollback strategies to minimize downtime and ensure data integrity.

**Migration Strategies:**
- **Bulk Operations**: Use bulk writes for efficiency
- **Chunking**: Process data in manageable batches
- **Monitoring**: Track progress and performance
- **Rollback Plan**: Prepare for failure scenarios

**Code Example:**
```javascript
// Large-scale data migration script
async function migrateUserData() {
  const batchSize = 1000;
  let processed = 0;
  let cursor = db.users.find({}).batchSize(batchSize);
  
  while (await cursor.hasNext()) {
    const batch = [];
    
    // Collect batch
    for (let i = 0; i < batchSize && await cursor.hasNext(); i++) {
      const doc = await cursor.next();
      
      // Transform document
      const transformed = {
        updateOne: {
          filter: { _id: doc._id },
          update: {
            $set: {
              fullName: `${doc.firstName} ${doc.lastName}`,
              updatedAt: new Date()
            },
            $unset: {
              firstName: "",
              lastName: ""
            }
          }
        }
      };
      
      batch.push(transformed);
    }
    
    // Execute batch
    if (batch.length > 0) {
      try {
        const result = await db.users.bulkWrite(batch, {
          ordered: false
        });
        
        processed += result.modifiedCount;
        console.log(`Processed: ${processed} documents`);
        
        // Add delay to avoid overwhelming the system
        await new Promise(resolve => setTimeout(resolve, 100));
        
      } catch (error) {
        console.error(`Batch failed:`, error);
        // Log failed batch for retry
      }
    }
  }
  
  console.log(`Migration completed. Total processed: ${processed}`);
}

// Run migration
migrateUserData();
```

### Q13: How do you implement data validation and schema enforcement in MongoDB?

**Answer:**
MongoDB provides JSON Schema validation to enforce document structure and data types while maintaining flexibility.

**Validation Levels:**
- **strict**: Apply to all inserts/updates
- **moderate**: Apply to valid documents only

**Code Example:**
```javascript
// Create collection with validation
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "price", "category"],
      properties: {
        name: {
          bsonType: "string",
          description: "Product name is required and must be a string"
        },
        price: {
          bsonType: "number",
          minimum: 0,
          description: "Price must be a positive number"
        },
        category: {
          bsonType: "string",
          enum: ["Electronics", "Clothing", "Books", "Home"],
          description: "Category must be one of the predefined values"
        },
        tags: {
          bsonType: "array",
          items: {
            bsonType: "string"
          },
          description: "Tags must be an array of strings"
        },
        specifications: {
          bsonType: "object",
          properties: {
            weight: { bsonType: "number" },
            dimensions: {
              bsonType: "object",
              properties: {
                length: { bsonType: "number" },
                width: { bsonType: "number" },
                height: { bsonType: "number" }
              }
            }
          }
        }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// Update validation rules
db.runCommand({
  collMod: "products",
  validator: {
    $jsonSchema: {
      // Updated schema
    }
  }
});
```

### Q14: How do you monitor and troubleshoot MongoDB performance issues?

**Answer:**
MongoDB performance monitoring involves database profiler, explain plans, monitoring tools, and key metrics analysis.

**Monitoring Tools:**
- **Database Profiler**: Captures slow operations
- **Explain Plans**: Analyzes query execution
- **mongostat/mongotop**: Real-time statistics
- **MongoDB Compass**: GUI monitoring

**Code Example:**
```javascript
// Enable profiler for slow operations
db.setProfilingLevel(1, { slowms: 100 });

// Analyze slow queries
db.system.profile.find().sort({ ts: -1 }).limit(5);

// Query explain plan
db.users.find({ "profile.age": { $gte: 25 } }).explain("executionStats");

// Index usage statistics
db.users.aggregate([
  { $indexStats: {} }
]);

// Current operations
db.currentOp();

// Server status
db.serverStatus();

// Collection statistics
db.users.stats();

// Performance monitoring script
function monitorPerformance() {
  const stats = db.serverStatus();
  
  console.log("Performance Metrics:");
  console.log(`Connections: ${stats.connections.current}/${stats.connections.available}`);
  console.log(`Operations/sec: ${stats.opcounters.query + stats.opcounters.insert + stats.opcounters.update + stats.opcounters.delete}`);
  console.log(`Memory Usage: ${Math.round(stats.mem.resident)}MB resident, ${Math.round(stats.mem.virtual)}MB virtual`);
  console.log(`Active Clients: ${stats.globalLock.activeClients.total}`);
  
  // Check for slow operations
  const slowOps = db.currentOp({ "secs_running": { $gte: 5 } });
  if (slowOps.inprog.length > 0) {
    console.log(`Warning: ${slowOps.inprog.length} slow operations detected`);
  }
}
```

---

## Key Takeaways

1. **Document Design**: Choose embedding vs referencing based on access patterns
2. **Indexing Strategy**: Create indexes that support your query patterns
3. **Aggregation Pipeline**: Leverage for complex data analysis and transformations
4. **Scaling**: Use replication for availability, sharding for horizontal scaling
5. **Performance**: Monitor with profiler and explain plans
6. **Schema Validation**: Implement validation rules while maintaining flexibility
7. **Real-time Processing**: Use change streams for reactive applications
8. **Migration Planning**: Handle large data migrations with proper batching and monitoring