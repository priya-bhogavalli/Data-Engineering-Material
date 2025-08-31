# CouchDB - Interview Questions

## Basic Questions

### 1. What is CouchDB and what makes it different from other NoSQL databases?
**Answer:** CouchDB is a document-oriented NoSQL database that stores JSON documents and uses HTTP as its API. It's unique because of its multi-master replication, offline-first design, and web-native architecture that allows direct browser access.

### 2. Explain CouchDB's replication model.
**Answer:** CouchDB uses multi-master replication where:
- Any database can replicate to any other database
- Replication is bidirectional and continuous
- Conflicts are automatically detected and flagged
- Applications handle conflict resolution
- Works offline and syncs when connectivity returns

### 3. How does CouchDB handle ACID properties?
**Answer:**
- **Atomicity**: Document-level atomicity only
- **Consistency**: Eventually consistent across replicas
- **Isolation**: MVCC prevents read/write conflicts
- **Durability**: Append-only B-tree ensures data persistence

## Intermediate Questions

### 4. What are CouchDB views and how do they work?
**Answer:** Views are MapReduce-based indexes written in JavaScript:
```javascript
// Map function
function(doc) {
  if (doc.type === 'user') {
    emit(doc.email, doc.name);
  }
}

// Reduce function (optional)
function(keys, values, rereduce) {
  return sum(values);
}
```
Views are incrementally updated and provide efficient querying.

### 5. How does conflict resolution work in CouchDB?
**Answer:** CouchDB handles conflicts by:
- Detecting conflicting document revisions
- Marking documents as conflicted
- Choosing a "winning" revision deterministically
- Storing all conflicting revisions
- Allowing applications to resolve conflicts manually

### 6. What is the difference between CouchDB and PouchDB?
**Answer:**
- **CouchDB**: Server-side database
- **PouchDB**: JavaScript library for browsers/Node.js
- **Compatibility**: PouchDB replicates with CouchDB
- **Use case**: PouchDB enables offline-first web applications

## Advanced Questions

### 7. How would you design a real-time collaborative application using CouchDB?
**Answer:**
```javascript
// Document structure
{
  "_id": "doc123",
  "_rev": "1-abc",
  "type": "document",
  "content": "Hello world",
  "collaborators": ["user1", "user2"],
  "last_modified": "2023-01-01T10:00:00Z"
}

// Continuous replication for real-time sync
db.replicate.to('http://server/db', {
  live: true,
  retry: true
});

// Changes feed for real-time updates
db.changes({
  since: 'now',
  live: true,
  include_docs: true
}).on('change', function(change) {
  updateUI(change.doc);
});
```

### 8. What are the performance considerations for CouchDB?
**Answer:**
- **View Performance**: Pre-build views for common queries
- **Document Size**: Keep documents reasonably sized
- **Replication**: Monitor replication lag
- **Compaction**: Regular database compaction
- **Indexing**: Create appropriate views/indexes
- **Bulk Operations**: Use bulk APIs for multiple documents

### 9. How would you implement security in CouchDB?
**Answer:**
- **Authentication**: Built-in user authentication
- **Authorization**: Database-level and document-level permissions
- **Validation Functions**: Server-side document validation
- **HTTPS**: Encrypt data in transit
- **Admin Party**: Disable for production
```javascript
// Validation function
function(newDoc, oldDoc, userCtx) {
  if (userCtx.name !== newDoc.owner) {
    throw({forbidden: 'Only owner can modify'});
  }
}
```

### 10. What are the limitations of CouchDB?
**Answer:**
- **Query Limitations**: No ad-hoc queries without views
- **Joins**: No native join operations
- **Transactions**: No multi-document transactions
- **Storage Overhead**: Document revisions consume space
- **Complex Queries**: Limited compared to SQL databases
- **Learning Curve**: Different paradigm from relational databases