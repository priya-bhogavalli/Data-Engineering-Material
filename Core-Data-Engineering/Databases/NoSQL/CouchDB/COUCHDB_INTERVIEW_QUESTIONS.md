# 🗄️ CouchDB Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Architecture](#architecture)
- [Data Model](#data-model)
- [Queries & Views](#queries--views)
- [Replication](#replication)
- [Performance](#performance)
- [Advanced Topics](#advanced-topics)

---

## Basic Concepts

### 1. What is Apache CouchDB and its key features?
**Answer:**
CouchDB is a document-oriented NoSQL database that uses JSON for documents and JavaScript for MapReduce queries.

**Key Features:**
- **Document-oriented**: Stores JSON documents
- **RESTful API**: HTTP-based interface
- **Multi-master replication**: Bi-directional sync
- **ACID compliance**: Document-level transactions
- **Schema-free**: Flexible document structure
- **Offline-first**: Works without network

### 2. What is the CouchDB data model?
**Answer:**
CouchDB stores data as JSON documents with unique IDs.

**Document Structure:**
```json
{
  "_id": "user123",
  "_rev": "1-967a00dff5e02add41819138abb3284d",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}
```

**Key Elements:**
- **_id**: Unique document identifier
- **_rev**: Revision identifier for MVCC
- **Fields**: Arbitrary JSON data

### 3. Explain CouchDB's MVCC (Multi-Version Concurrency Control).
**Answer:**
MVCC prevents conflicts by maintaining document versions.

**How it works:**
- Each document has revision ID (_rev)
- Updates create new revision
- Old revisions kept temporarily
- Conflicts detected via revision mismatch

**Example:**
```bash
# Initial document
PUT /db/doc1
{"name": "John", "_rev": "1-abc123"}

# Update requires current revision
PUT /db/doc1
{"name": "Jane", "_rev": "1-abc123"}
# Returns: "_rev": "2-def456"

# Conflict if wrong revision used
PUT /db/doc1
{"name": "Bob", "_rev": "1-abc123"}
# Returns: 409 Conflict
```

### 4. What are CouchDB design documents?
**Answer:**
Design documents contain application code like views, shows, and lists.

**Structure:**
```json
{
  "_id": "_design/users",
  "views": {
    "by_age": {
      "map": "function(doc) { if(doc.age) emit(doc.age, doc); }"
    }
  },
  "shows": {
    "profile": "function(doc, req) { return '<h1>' + doc.name + '</h1>'; }"
  }
}
```

**Functions:**
- **Views**: MapReduce queries
- **Shows**: Transform documents to other formats
- **Lists**: Transform view results
- **Updates**: Server-side document updates

### 5. How does CouchDB handle conflicts?
**Answer:**
CouchDB uses deterministic conflict resolution.

**Conflict Detection:**
- Occurs during replication
- Multiple revisions of same document
- CouchDB picks "winning" revision

**Resolution Strategy:**
```javascript
// Automatic resolution (deterministic)
// CouchDB picks revision with:
// 1. Most edits (highest revision number)
// 2. Lexicographically largest revision ID

// Manual resolution
function resolveConflict(doc) {
  // Get all conflicting revisions
  db.get(doc._id, {conflicts: true}, function(err, doc) {
    if (doc._conflicts) {
      // Merge conflicting versions
      // Save resolved version
      // Delete conflicting revisions
    }
  });
}
```

---

## Architecture

### 6. Describe CouchDB's architecture and components.
**Answer:**
**Core Components:**
- **HTTP API**: RESTful interface
- **Storage Engine**: B+ tree based
- **View Engine**: MapReduce processing
- **Replication**: Multi-master sync
- **Clustering**: Distributed setup (CouchDB 2.0+)

**Architecture:**
```
Client Applications
        ↓
    HTTP API
        ↓
   Query Engine
        ↓
   Storage Engine
        ↓
    File System
```

### 7. What is CouchDB clustering and how does it work?
**Answer:**
CouchDB 2.0+ supports horizontal scaling through clustering.

**Cluster Setup:**
```bash
# Setup cluster nodes
curl -X PUT http://admin:pass@node1:5984/_cluster_setup \
  -d '{"action":"enable_cluster","bind_address":"0.0.0.0","username":"admin","password":"pass"}'

# Add nodes to cluster
curl -X POST http://admin:pass@node1:5984/_cluster_setup \
  -d '{"action":"add_node","host":"node2","port":"5984","username":"admin","password":"pass"}'
```

**Features:**
- **Automatic sharding**: Data distributed across nodes
- **Fault tolerance**: Handles node failures
- **Load balancing**: Requests distributed
- **Consistent hashing**: Determines data placement

### 8. How does CouchDB replication work?
**Answer:**
CouchDB uses incremental replication with change feeds.

**Replication Process:**
1. **Changes feed**: Source tracks document changes
2. **Comparison**: Target compares document revisions
3. **Transfer**: Missing/newer documents copied
4. **Conflict resolution**: Handles conflicts automatically

**Setup Replication:**
```bash
# One-time replication
curl -X POST http://localhost:5984/_replicate \
  -d '{"source":"db1","target":"db2"}'

# Continuous replication
curl -X POST http://localhost:5984/_replicate \
  -d '{"source":"db1","target":"db2","continuous":true}'
```

### 9. What is the CouchDB changes feed?
**Answer:**
Changes feed provides real-time notifications of document changes.

**Usage:**
```bash
# Get changes since sequence 0
GET /db/_changes

# Continuous changes feed
GET /db/_changes?feed=continuous

# Filter changes
GET /db/_changes?filter=_design/app/_view/important
```

**Applications:**
- Real-time synchronization
- Event-driven architectures
- Cache invalidation
- Audit logging

### 10. How do you secure CouchDB?
**Answer:**
**Security Features:**
- **Authentication**: User accounts and sessions
- **Authorization**: Database-level permissions
- **SSL/TLS**: Encrypted connections
- **Admin party**: Default insecure mode

**Configuration:**
```bash
# Create admin user
curl -X PUT http://localhost:5984/_config/admins/admin \
  -d '"password"'

# Set database security
curl -X PUT http://admin:pass@localhost:5984/db/_security \
  -d '{"admins":{"names":["admin"],"roles":[]},"members":{"names":["user1"],"roles":["users"]}}'
```

---

## Data Model

### 11. How do you design documents in CouchDB?
**Answer:**
**Best Practices:**
- **Denormalize data**: Include related data in documents
- **Use meaningful IDs**: Hierarchical or semantic IDs
- **Avoid deep nesting**: Keep documents flat when possible
- **Include type field**: Distinguish document types

**Example:**
```json
{
  "_id": "user:john.doe",
  "type": "user",
  "name": "John Doe",
  "email": "john@example.com",
  "profile": {
    "bio": "Software developer",
    "location": "San Francisco"
  },
  "preferences": {
    "theme": "dark",
    "language": "en"
  },
  "created_at": "2024-03-01T10:00:00Z"
}
```

### 12. How do you handle relationships in CouchDB?
**Answer:**
**Strategies:**

**1. Embedding (One-to-Few):**
```json
{
  "_id": "order:12345",
  "customer": "John Doe",
  "items": [
    {"product": "Laptop", "price": 999, "qty": 1},
    {"product": "Mouse", "price": 25, "qty": 2}
  ]
}
```

**2. Referencing (One-to-Many):**
```json
// User document
{"_id": "user:123", "name": "John"}

// Order documents
{"_id": "order:456", "user_id": "user:123", "total": 100}
{"_id": "order:789", "user_id": "user:123", "total": 200}
```

**3. Denormalization:**
```json
{
  "_id": "order:456",
  "user_id": "user:123",
  "user_name": "John Doe",  // Denormalized
  "user_email": "john@example.com"  // Denormalized
}
```

### 13. What are CouchDB attachments?
**Answer:**
Attachments store binary data alongside documents.

**Adding Attachments:**
```bash
# Add attachment to document
curl -X PUT http://localhost:5984/db/doc1/photo.jpg?rev=1-abc123 \
  --data-binary @photo.jpg \
  -H "Content-Type: image/jpeg"
```

**Document with Attachment:**
```json
{
  "_id": "doc1",
  "_rev": "2-def456",
  "title": "My Document",
  "_attachments": {
    "photo.jpg": {
      "content_type": "image/jpeg",
      "length": 12345,
      "stub": true
    }
  }
}
```

**Use Cases:**
- Images and media files
- PDF documents
- Binary data storage

### 14. How do you implement validation in CouchDB?
**Answer:**
Use validate_doc_update functions in design documents.

**Validation Function:**
```javascript
{
  "_id": "_design/validation",
  "validate_doc_update": "function(newDoc, oldDoc, userCtx) {\
    if (newDoc.type === 'user') {\
      if (!newDoc.email) {\
        throw({forbidden: 'Email is required'});\
      }\
      if (!/^[^@]+@[^@]+$/.test(newDoc.email)) {\
        throw({forbidden: 'Invalid email format'});\
      }\
    }\
  }"
}
```

**Validation Rules:**
- Required fields
- Data format validation
- Business logic enforcement
- User permission checks

### 15. How do you handle document versioning?
**Answer:**
**Built-in Versioning:**
CouchDB automatically maintains revision history.

**Custom Versioning:**
```json
{
  "_id": "doc123",
  "version": "2.1",
  "title": "Document Title",
  "content": "Updated content",
  "history": [
    {
      "version": "1.0",
      "modified_by": "user1",
      "modified_at": "2024-01-01T10:00:00Z"
    },
    {
      "version": "2.0",
      "modified_by": "user2",
      "modified_at": "2024-02-01T10:00:00Z"
    }
  ]
}
```

---

## Queries & Views

### 16. How do you create and use views in CouchDB?
**Answer:**
Views use MapReduce to query documents.

**Map Function:**
```javascript
{
  "_id": "_design/users",
  "views": {
    "by_age": {
      "map": "function(doc) {\
        if (doc.type === 'user' && doc.age) {\
          emit(doc.age, {name: doc.name, email: doc.email});\
        }\
      }"
    }
  }
}
```

**Querying Views:**
```bash
# Get all users by age
GET /db/_design/users/_view/by_age

# Get users aged 25-35
GET /db/_design/users/_view/by_age?startkey=25&endkey=35

# Get specific age
GET /db/_design/users/_view/by_age?key=30
```

### 17. What are reduce functions and when to use them?
**Answer:**
Reduce functions aggregate map results.

**Example:**
```javascript
{
  "views": {
    "age_stats": {
      "map": "function(doc) {\
        if (doc.type === 'user' && doc.age) {\
          emit('age', doc.age);\
        }\
      }",
      "reduce": "function(keys, values, rereduce) {\
        if (rereduce) {\
          return {\
            sum: values.reduce((a,b) => a.sum + b.sum, 0),\
            count: values.reduce((a,b) => a.count + b.count, 0)\
          };\
        } else {\
          return {\
            sum: values.reduce((a,b) => a + b, 0),\
            count: values.length\
          };\
        }\
      }"
    }
  }
}
```

**Built-in Reduces:**
- `_count`: Count documents
- `_sum`: Sum values
- `_stats`: Statistics (sum, count, min, max)

### 18. How do you implement full-text search in CouchDB?
**Answer:**
**Options:**

**1. Lucene Integration:**
```javascript
{
  "_id": "_design/search",
  "fulltext": {
    "by_content": {
      "index": "function(doc) {\
        var ret = new Document();\
        ret.add(doc.title);\
        ret.add(doc.content);\
        return ret;\
      }"
    }
  }
}
```

**2. External Search (Elasticsearch):**
```javascript
// Use changes feed to sync to Elasticsearch
// Query Elasticsearch for search
// Return CouchDB document IDs
```

**3. Simple Text Matching:**
```javascript
{
  "views": {
    "search": {
      "map": "function(doc) {\
        if (doc.content) {\
          var words = doc.content.toLowerCase().split(/\\s+/);\
          words.forEach(function(word) {\
            emit(word, doc._id);\
          });\
        }\
      }"
    }
  }
}
```

### 19. How do you optimize view performance?
**Answer:**
**Optimization Strategies:**

**1. Efficient Map Functions:**
```javascript
// Good: Emit only necessary data
emit(doc.category, {name: doc.name, price: doc.price});

// Bad: Emit entire document
emit(doc.category, doc);
```

**2. Use Startkey/Endkey:**
```bash
# Efficient range query
GET /db/_view/by_date?startkey="2024-01-01"&endkey="2024-01-31"
```

**3. Limit Results:**
```bash
# Paginate large result sets
GET /db/_view/all?limit=100&skip=200
```

**4. View Collation:**
```javascript
// Use arrays for complex sorting
emit([doc.category, doc.date], doc);
```

### 20. What are list and show functions?
**Answer:**
**Show Functions** transform single documents:
```javascript
{
  "shows": {
    "html": "function(doc, req) {\
      return {\
        body: '<h1>' + doc.title + '</h1><p>' + doc.content + '</p>',\
        headers: {'Content-Type': 'text/html'}\
      };\
    }"
  }
}
```

**List Functions** transform view results:
```javascript
{
  "lists": {
    "csv": "function(head, req) {\
      var row;\
      send('Name,Age\\n');\
      while(row = getRow()) {\
        send(row.value.name + ',' + row.value.age + '\\n');\
      }\
    }"
  }
}
```

**Usage:**
```bash
# Show function
GET /db/_design/app/_show/html/doc123

# List function
GET /db/_design/app/_list/csv/by_age
```

---

## Replication

### 21. How do you set up master-master replication?
**Answer:**
**Bidirectional Replication:**
```bash
# Replicate A to B
curl -X POST http://localhost:5984/_replicate \
  -d '{"source":"http://serverA:5984/db","target":"http://serverB:5984/db","continuous":true}'

# Replicate B to A
curl -X POST http://localhost:5984/_replicate \
  -d '{"source":"http://serverB:5984/db","target":"http://serverA:5984/db","continuous":true}'
```

**Conflict Handling:**
- Automatic conflict detection
- Deterministic winner selection
- Manual conflict resolution available

### 22. How do you implement filtered replication?
**Answer:**
**Filter Functions:**
```javascript
{
  "_id": "_design/filters",
  "filters": {
    "important": "function(doc, req) {\
      return doc.priority === 'high';\
    }",
    "by_user": "function(doc, req) {\
      return doc.user_id === req.query.user_id;\
    }"
  }
}
```

**Filtered Replication:**
```bash
# Replicate only important documents
curl -X POST http://localhost:5984/_replicate \
  -d '{"source":"db1","target":"db2","filter":"filters/important"}'

# Replicate user-specific documents
curl -X POST http://localhost:5984/_replicate \
  -d '{"source":"db1","target":"db2","filter":"filters/by_user","query_params":{"user_id":"123"}}'
```

### 23. How do you handle replication conflicts?
**Answer:**
**Conflict Resolution Strategies:**

**1. Automatic (Default):**
```javascript
// CouchDB picks winner deterministically
// Losing revisions marked as conflicts
```

**2. Manual Resolution:**
```javascript
function resolveConflicts(db, docId) {
  db.get(docId, {conflicts: true}, function(err, doc) {
    if (doc._conflicts) {
      // Get all conflicting revisions
      var promises = doc._conflicts.map(function(rev) {
        return db.get(docId, {rev: rev});
      });
      
      Promise.all(promises).then(function(conflicts) {
        // Merge logic here
        var merged = mergeDocuments([doc].concat(conflicts));
        
        // Save merged document
        db.put(merged).then(function() {
          // Delete conflicting revisions
          conflicts.forEach(function(conflict) {
            db.remove(conflict._id, conflict._rev);
          });
        });
      });
    }
  });
}
```

### 24. What is PouchDB and how does it relate to CouchDB?
**Answer:**
PouchDB is a JavaScript database that syncs with CouchDB.

**Features:**
- **Browser/Node.js**: Runs in browsers and Node.js
- **Offline-first**: Works without network
- **Sync**: Bidirectional sync with CouchDB
- **Same API**: Compatible with CouchDB

**Usage:**
```javascript
// Create PouchDB instance
var db = new PouchDB('mydb');

// Sync with CouchDB
var remoteDB = new PouchDB('http://localhost:5984/mydb');
db.sync(remoteDB, {
  live: true,
  retry: true
});

// Use same API as CouchDB
db.put({
  _id: 'doc1',
  title: 'Hello World'
});
```

### 25. How do you implement offline-first applications?
**Answer:**
**Architecture:**
```javascript
// Local PouchDB for offline storage
var localDB = new PouchDB('local_app_data');

// Remote CouchDB for server sync
var remoteDB = new PouchDB('https://server.com/app_data');

// Sync when online
function syncWhenOnline() {
  if (navigator.onLine) {
    localDB.sync(remoteDB, {
      live: true,
      retry: true
    }).on('change', function(info) {
      console.log('Sync change:', info);
    }).on('error', function(err) {
      console.log('Sync error:', err);
    });
  }
}

// Handle online/offline events
window.addEventListener('online', syncWhenOnline);
window.addEventListener('offline', function() {
  console.log('App is offline');
});
```

---

## Performance

### 26. How do you optimize CouchDB performance?
**Answer:**
**Optimization Strategies:**

**1. Database Configuration:**
```ini
[couchdb]
max_document_size = 4294967296
os_process_timeout = 5000

[httpd]
max_connections = 2048

[query_servers]
javascript = couchjs /usr/share/couchdb/server/main.js
```

**2. View Optimization:**
- Use efficient map functions
- Minimize emitted data
- Use built-in reduces when possible
- Index frequently queried fields

**3. Document Design:**
- Keep documents reasonably sized
- Avoid deep nesting
- Use appropriate document IDs

### 27. How do you monitor CouchDB performance?
**Answer:**
**Monitoring Tools:**

**1. Built-in Stats:**
```bash
# Database info
GET /db

# Server stats
GET /_stats

# Active tasks
GET /_active_tasks
```

**2. Key Metrics:**
- Document count and size
- View index size and update frequency
- Replication lag
- HTTP request rates
- Disk usage

**3. External Monitoring:**
```javascript
// Custom monitoring script
function checkCouchDBHealth() {
  fetch('http://localhost:5984/_up')
    .then(response => {
      if (response.ok) {
        console.log('CouchDB is healthy');
      }
    })
    .catch(err => {
      console.error('CouchDB health check failed:', err);
    });
}
```

### 28. How do you handle large datasets in CouchDB?
**Answer:**
**Strategies:**

**1. Pagination:**
```bash
# Use skip and limit
GET /db/_all_docs?limit=100&skip=1000

# Use startkey for better performance
GET /db/_all_docs?startkey="doc1000"&limit=100
```

**2. Partitioning:**
```javascript
// Partition by date
{
  "_id": "2024-03-01:event123",
  "date": "2024-03-01",
  "type": "event"
}

// Query specific partition
GET /db/_partition/2024-03-01/_all_docs
```

**3. Compaction:**
```bash
# Compact database
POST /db/_compact

# Compact views
POST /db/_compact/design_doc_name
```

### 29. What are CouchDB best practices?
**Answer:**
**Design Best Practices:**

**1. Document Structure:**
- Include document type field
- Use meaningful document IDs
- Avoid large documents (>1MB)
- Denormalize for read performance

**2. View Design:**
- Create views for all query patterns
- Use collation for sorting
- Minimize map function complexity
- Use built-in reduce functions

**3. Replication:**
- Use filtered replication when appropriate
- Monitor replication lag
- Handle conflicts gracefully
- Test offline scenarios

### 30. How do you backup and restore CouchDB?
**Answer:**
**Backup Methods:**

**1. Replication Backup:**
```bash
# Replicate to backup database
curl -X POST http://localhost:5984/_replicate \
  -d '{"source":"production_db","target":"backup_db"}'
```

**2. File System Backup:**
```bash
# Stop CouchDB
sudo service couchdb stop

# Backup data directory
tar -czf couchdb_backup.tar.gz /var/lib/couchdb/

# Start CouchDB
sudo service couchdb start
```

**3. Continuous Backup:**
```javascript
// Continuous replication to backup server
{
  "source": "production_db",
  "target": "http://backup-server:5984/production_db",
  "continuous": true,
  "create_target": true
}
```

---

## Advanced Topics

### 31. How do you implement multi-tenancy in CouchDB?
**Answer:**
**Strategies:**

**1. Database per Tenant:**
```javascript
// Create database for each tenant
function createTenantDB(tenantId) {
  var dbName = 'tenant_' + tenantId;
  return new PouchDB('http://localhost:5984/' + dbName);
}
```

**2. Document-level Isolation:**
```json
{
  "_id": "tenant1:doc123",
  "tenant_id": "tenant1",
  "type": "document",
  "data": "..."
}
```

**3. Filtered Views:**
```javascript
{
  "views": {
    "by_tenant": {
      "map": "function(doc) {\
        if (doc.tenant_id) {\
          emit([doc.tenant_id, doc.type], doc);\
        }\
      }"
    }
  }
}
```

### 32. How do you implement caching with CouchDB?
**Answer:**
**Caching Strategies:**

**1. Application-level Caching:**
```javascript
var cache = new Map();

function getCachedDoc(id) {
  if (cache.has(id)) {
    return Promise.resolve(cache.get(id));
  }
  
  return db.get(id).then(function(doc) {
    cache.set(id, doc);
    return doc;
  });
}

// Invalidate cache on changes
db.changes({live: true}).on('change', function(change) {
  cache.delete(change.id);
});
```

**2. HTTP Caching:**
```javascript
// Use ETags for conditional requests
fetch('/db/doc123', {
  headers: {
    'If-None-Match': lastETag
  }
});
```

### 33. How do you migrate from SQL to CouchDB?
**Answer:**
**Migration Steps:**

**1. Schema Analysis:**
```sql
-- Analyze existing SQL schema
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'mydb';
```

**2. Document Design:**
```javascript
// Convert normalized tables to documents
// SQL: users, orders, order_items tables
// CouchDB: order documents with embedded items
{
  "_id": "order:12345",
  "type": "order",
  "user": {
    "id": "user123",
    "name": "John Doe"
  },
  "items": [
    {"product": "Laptop", "price": 999, "qty": 1}
  ],
  "total": 999
}
```

**3. Data Migration:**
```javascript
// ETL process
function migrateOrders() {
  // Extract from SQL
  var orders = sqlDB.query('SELECT * FROM orders');
  
  // Transform to CouchDB format
  orders.forEach(function(order) {
    var doc = {
      _id: 'order:' + order.id,
      type: 'order',
      // ... transform data
    };
    
    // Load into CouchDB
    couchDB.put(doc);
  });
}
```

### 34. How do you implement real-time features with CouchDB?
**Answer:**
**Real-time Implementation:**

**1. Changes Feed:**
```javascript
// Listen for real-time changes
db.changes({
  live: true,
  since: 'now',
  include_docs: true
}).on('change', function(change) {
  // Update UI in real-time
  updateUI(change.doc);
});
```

**2. WebSocket Integration:**
```javascript
// Server-side: Forward changes to WebSocket
db.changes({live: true}).on('change', function(change) {
  wss.clients.forEach(function(client) {
    client.send(JSON.stringify(change));
  });
});

// Client-side: Receive real-time updates
ws.onmessage = function(event) {
  var change = JSON.parse(event.data);
  updateUI(change);
};
```

### 35. What are CouchDB 3.0 new features?
**Answer:**
**Key Features:**

**1. Partitioned Databases:**
```bash
# Create partitioned database
PUT /db?partitioned=true

# Query partition
GET /db/_partition/partition_key/_all_docs
```

**2. Improved Clustering:**
- Better node management
- Improved rebalancing
- Enhanced monitoring

**3. Performance Improvements:**
- Faster view indexing
- Better memory management
- Optimized replication

**4. New Query Features:**
- Enhanced Mango queries
- Better index selection
- Improved query planning

---

*This comprehensive guide covers 35+ essential CouchDB interview questions with detailed answers and practical examples for data engineering interviews.*