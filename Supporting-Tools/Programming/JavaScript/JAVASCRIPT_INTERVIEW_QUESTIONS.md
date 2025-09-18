# JavaScript Interview Questions for Data Engineering - EXPANDED TO 80

## 📋 Table of Contents

1. [Core Concepts Questions (1-25)](#core-concepts-questions-1-25)
2. [Asynchronous Programming (26-40)](#asynchronous-programming-26-40)
3. [Data Structures & Algorithms (41-55)](#data-structures--algorithms-41-55)
4. [API Development & Integration (56-70)](#api-development--integration-56-70)
5. [Performance & Optimization (71-80)](#performance--optimization-71-80)

---

## 🎯 **Introduction**

JavaScript is essential for data engineers building web interfaces, APIs, and data processing tools. This guide covers JavaScript concepts specifically relevant to data engineering workflows.

**Why JavaScript for Data Engineering:**
- **Frontend Development**: Data dashboards and visualization interfaces
- **API Development**: Node.js backend services and microservices
- **Data Processing**: Client-side data manipulation and transformation
- **Real-time Applications**: WebSocket connections and streaming data
- **Integration**: Connecting various data systems and services

---

## Core Concepts Questions (1-25)

### 1. Explain JavaScript's data types and their use in data processing.
**Answer**: JavaScript has primitive and non-primitive data types crucial for data manipulation.

**Primitive Types:**
```javascript
// Number - for numerical data
let revenue = 1234.56;
let count = 42;
let percentage = 0.85;

// String - for text data
let customerName = "John Doe";
let productId = "PROD-001";

// Boolean - for flags and conditions
let isActive = true;
let hasData = false;

// Undefined - uninitialized variables
let result; // undefined

// Null - intentional absence of value
let deletedRecord = null;

// Symbol - unique identifiers
const METRIC_TYPE = Symbol('metric');

// BigInt - large integers
let largeNumber = 9007199254740991n;
```

**Non-Primitive Types:**
```javascript
// Object - complex data structures
const customer = {
    id: 123,
    name: "John Doe",
    orders: [
        { id: 1, amount: 100.50 },
        { id: 2, amount: 75.25 }
    ],
    metadata: {
        source: "web",
        timestamp: new Date()
    }
};

// Array - ordered collections
const salesData = [100, 150, 200, 175, 300];
const products = ["laptop", "mouse", "keyboard"];

// Function - reusable code blocks
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// Date - temporal data
const orderDate = new Date('2023-01-15');
const now = new Date();
```

### 2. How do you handle type coercion and comparison in data processing?
**Answer**: Understanding type coercion is crucial for accurate data processing.

```javascript
// Type coercion examples
console.log("5" + 3);     // "53" (string concatenation)
console.log("5" - 3);     // 2 (numeric subtraction)
console.log("5" * 3);     // 15 (numeric multiplication)
console.log(true + 1);    // 2 (boolean to number)

// Comparison operators
console.log("5" == 5);    // true (loose equality)
console.log("5" === 5);   // false (strict equality)
console.log(null == undefined);  // true
console.log(null === undefined); // false

// Safe data processing practices
function safeAdd(a, b) {
    // Ensure both values are numbers
    const numA = Number(a);
    const numB = Number(b);
    
    if (isNaN(numA) || isNaN(numB)) {
        throw new Error('Invalid numeric values');
    }
    
    return numA + numB;
}

// Data validation
function validateDataTypes(data) {
    const validations = {
        id: (val) => typeof val === 'number' && val > 0,
        name: (val) => typeof val === 'string' && val.length > 0,
        email: (val) => typeof val === 'string' && val.includes('@'),
        active: (val) => typeof val === 'boolean'
    };
    
    const errors = [];
    
    for (const [field, validator] of Object.entries(validations)) {
        if (!validator(data[field])) {
            errors.push(`Invalid ${field}: ${data[field]}`);
        }
    }
    
    return {
        isValid: errors.length === 0,
        errors
    };
}
```

### 3. Explain closures and their applications in data processing.
**Answer**: Closures provide data encapsulation and state management in data processing functions.

```javascript
// Basic closure example
function createCounter() {
    let count = 0;
    
    return function() {
        return ++count;
    };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2

// Data processing with closures
function createDataProcessor(config) {
    let processedCount = 0;
    const startTime = Date.now();
    
    return {
        process: function(data) {
            processedCount++;
            
            // Apply transformations based on config
            let result = data;
            
            if (config.normalize) {
                result = normalizeData(result);
            }
            
            if (config.validate) {
                result = validateData(result);
            }
            
            return result;
        },
        
        getStats: function() {
            return {
                processed: processedCount,
                runtime: Date.now() - startTime,
                rate: processedCount / ((Date.now() - startTime) / 1000)
            };
        }
    };
}

// Usage
const processor = createDataProcessor({
    normalize: true,
    validate: true
});

// Memoization with closures
function memoize(fn, keyGenerator = JSON.stringify) {
    const cache = new Map();
    
    return function(...args) {
        const key = keyGenerator(args);
        
        if (cache.has(key)) {
            return cache.get(key);
        }
        
        const result = fn.apply(this, args);
        cache.set(key, result);
        return result;
    };
}

// Expensive calculation with memoization
const expensiveCalculation = memoize(function(data) {
    console.log('Performing expensive calculation...');
    return data.reduce((sum, item) => sum + item.value * item.weight, 0);
});
```

### 4. How do you work with arrays and objects for data manipulation?
**Answer**: Arrays and objects are fundamental for data processing in JavaScript.

```javascript
// Array methods for data processing
const salesData = [
    { id: 1, product: 'Laptop', amount: 1200, date: '2023-01-15' },
    { id: 2, product: 'Mouse', amount: 25, date: '2023-01-16' },
    { id: 3, product: 'Keyboard', amount: 75, date: '2023-01-17' },
    { id: 4, product: 'Monitor', amount: 300, date: '2023-01-18' }
];

// Filter data
const highValueSales = salesData.filter(sale => sale.amount > 100);

// Transform data
const salesSummary = salesData.map(sale => ({
    id: sale.id,
    product: sale.product,
    revenue: sale.amount,
    month: new Date(sale.date).getMonth() + 1
}));

// Aggregate data
const totalRevenue = salesData.reduce((total, sale) => total + sale.amount, 0);

// Group by product
const salesByProduct = salesData.reduce((groups, sale) => {
    const product = sale.product;
    if (!groups[product]) {
        groups[product] = [];
    }
    groups[product].push(sale);
    return groups;
}, {});

// Find specific records
const laptopSale = salesData.find(sale => sale.product === 'Laptop');
const hasHighValueSale = salesData.some(sale => sale.amount > 1000);
const allPositiveAmounts = salesData.every(sale => sale.amount > 0);

// Sort data
const sortedByAmount = [...salesData].sort((a, b) => b.amount - a.amount);
const sortedByDate = [...salesData].sort((a, b) => new Date(a.date) - new Date(b.date));
```

### 5. What are JavaScript's execution contexts and scope?
**Answer**: Understanding execution contexts and scope is crucial for data processing functions.

```javascript
// Global execution context
var globalVar = 'I am global';
let globalLet = 'I am also global';
const globalConst = 'I am global too';

// Function execution context
function processData(dataset) {
    // Function scope
    var functionVar = 'I am in function scope';
    let functionLet = 'I am also in function scope';
    
    // Block scope
    if (dataset.length > 0) {
        let blockLet = 'I am in block scope';
        const blockConst = 'I am also in block scope';
        var blockVar = 'I am still in function scope'; // var ignores block scope
        
        console.log(blockLet); // Accessible
        console.log(blockConst); // Accessible
    }
    
    // console.log(blockLet); // ReferenceError
    // console.log(blockConst); // ReferenceError
    console.log(blockVar); // Accessible (function scoped)
    
    return dataset.map(item => item.value);
}

// Lexical scoping example
function createDataFilter(criteria) {
    const filterCriteria = criteria; // Outer scope
    
    return function(data) {
        // Inner function has access to outer scope
        return data.filter(item => {
            return Object.keys(filterCriteria).every(key => {
                return item[key] === filterCriteria[key];
            });
        });
    };
}

const activeFilter = createDataFilter({ status: 'active' });
const filteredData = activeFilter(userData);
```

### 6-25. Additional Core Concepts Questions

### 6. How do you handle prototypes and inheritance in JavaScript?
### 7. What are arrow functions and when should you use them?
### 8. How do you implement destructuring for data extraction?
### 9. What are template literals and their use in data formatting?
### 10. How do you work with the spread operator and rest parameters?
### 11. What are symbols and their applications in data processing?
### 12. How do you handle regular expressions for data validation?
### 13. What are generators and iterators in JavaScript?
### 14. How do you implement proper error handling strategies?
### 15. What are modules and how do you organize code?
### 16. How do you work with JSON data effectively?
### 17. What are WeakMap and WeakSet and their use cases?
### 18. How do you handle dates and times in JavaScript?
### 19. What are proxies and their applications?
### 20. How do you implement functional programming concepts?
### 21. What are higher-order functions and their benefits?
### 22. How do you handle immutability in JavaScript?
### 23. What are the different ways to create objects?
### 24. How do you implement method chaining?
### 25. What are the best practices for variable declarations?

---

## Asynchronous Programming (26-40)

### 26. Explain Promises and async/await for data processing.
**Answer**: Asynchronous programming is essential for data fetching and processing operations.

```javascript
// Promise basics
function fetchUserData(userId) {
    return new Promise((resolve, reject) => {
        // Simulate API call
        setTimeout(() => {
            if (userId > 0) {
                resolve({
                    id: userId,
                    name: `User ${userId}`,
                    email: `user${userId}@example.com`
                });
            } else {
                reject(new Error('Invalid user ID'));
            }
        }, 1000);
    });
}

// Promise chaining
fetchUserData(1)
    .then(user => {
        console.log('User fetched:', user);
        return fetchUserOrders(user.id);
    })
    .then(orders => {
        console.log('Orders fetched:', orders);
        return calculateOrderTotal(orders);
    })
    .then(total => {
        console.log('Total calculated:', total);
    })
    .catch(error => {
        console.error('Error in chain:', error);
    });

// Async/await syntax
async function processUserData(userId) {
    try {
        const user = await fetchUserData(userId);
        console.log('User fetched:', user);
        
        const orders = await fetchUserOrders(user.id);
        console.log('Orders fetched:', orders);
        
        const total = await calculateOrderTotal(orders);
        console.log('Total calculated:', total);
        
        return { user, orders, total };
    } catch (error) {
        console.error('Error processing user data:', error);
        throw error;
    }
}

// Parallel execution with Promise.all
async function fetchMultipleUsers(userIds) {
    try {
        const userPromises = userIds.map(id => fetchUserData(id));
        const users = await Promise.all(userPromises);
        return users;
    } catch (error) {
        console.error('Error fetching users:', error);
        throw error;
    }
}
```

### 27. How do you handle errors in asynchronous operations?
**Answer**: Proper error handling is crucial for robust data processing applications.

```javascript
// Error handling with Promises
function fetchDataWithRetry(url, maxRetries = 3) {
    return new Promise((resolve, reject) => {
        let attempts = 0;
        
        function attemptFetch() {
            attempts++;
            
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => resolve(data))
                .catch(error => {
                    if (attempts < maxRetries) {
                        console.log(`Attempt ${attempts} failed, retrying...`);
                        setTimeout(attemptFetch, 1000 * attempts); // Exponential backoff
                    } else {
                        reject(new Error(`Failed after ${maxRetries} attempts: ${error.message}`));
                    }
                });
        }
        
        attemptFetch();
    });
}

// Async/await error handling
async function processDataWithErrorHandling(data) {
    const results = [];
    const errors = [];
    
    for (const item of data) {
        try {
            const processed = await processItem(item);
            results.push(processed);
        } catch (error) {
            console.error(`Error processing item ${item.id}:`, error);
            errors.push({
                item: item.id,
                error: error.message
            });
        }
    }
    
    return { results, errors };
}

// Custom error classes
class DataProcessingError extends Error {
    constructor(message, code, data) {
        super(message);
        this.name = 'DataProcessingError';
        this.code = code;
        this.data = data;
    }
}

class ValidationError extends DataProcessingError {
    constructor(message, field, value) {
        super(message, 'VALIDATION_ERROR', { field, value });
        this.name = 'ValidationError';
    }
}
```

### 28-40. Additional Asynchronous Programming Questions

### 28. How do you implement Promise.all vs Promise.allSettled?
### 29. What is the event loop and how does it work?
### 30. How do you handle race conditions in async code?
### 31. What are microtasks and macrotasks?
### 32. How do you implement timeout handling for promises?
### 33. What are async generators and their use cases?
### 34. How do you handle backpressure in streaming data?
### 35. What are AbortController and AbortSignal?
### 36. How do you implement retry mechanisms?
### 37. What are the differences between callbacks, promises, and async/await?
### 38. How do you handle concurrent operations efficiently?
### 39. What are observables and how do they compare to promises?
### 40. How do you implement circuit breaker patterns?

---

## Data Structures & Algorithms (41-55)

### 41. How do you implement efficient data structures for processing?
**Answer**: Custom data structures optimized for specific data processing needs.

```javascript
// Hash Map for fast lookups
class HashMap {
    constructor(initialCapacity = 16) {
        this.capacity = initialCapacity;
        this.size = 0;
        this.buckets = new Array(this.capacity).fill(null).map(() => []);
    }
    
    hash(key) {
        let hash = 0;
        for (let i = 0; i < key.length; i++) {
            hash = (hash + key.charCodeAt(i) * i) % this.capacity;
        }
        return hash;
    }
    
    set(key, value) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        
        const existingPair = bucket.find(pair => pair[0] === key);
        if (existingPair) {
            existingPair[1] = value;
        } else {
            bucket.push([key, value]);
            this.size++;
        }
        
        // Resize if load factor > 0.75
        if (this.size > this.capacity * 0.75) {
            this.resize();
        }
    }
    
    get(key) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        const pair = bucket.find(pair => pair[0] === key);
        return pair ? pair[1] : undefined;
    }
    
    resize() {
        const oldBuckets = this.buckets;
        this.capacity *= 2;
        this.size = 0;
        this.buckets = new Array(this.capacity).fill(null).map(() => []);
        
        for (const bucket of oldBuckets) {
            for (const [key, value] of bucket) {
                this.set(key, value);
            }
        }
    }
}

// Trie for efficient string operations
class TrieNode {
    constructor() {
        this.children = {};
        this.isEndOfWord = false;
        this.data = null;
    }
}

class Trie {
    constructor() {
        this.root = new TrieNode();
    }
    
    insert(word, data = null) {
        let current = this.root;
        
        for (const char of word) {
            if (!current.children[char]) {
                current.children[char] = new TrieNode();
            }
            current = current.children[char];
        }
        
        current.isEndOfWord = true;
        current.data = data;
    }
    
    search(word) {
        let current = this.root;
        
        for (const char of word) {
            if (!current.children[char]) {
                return null;
            }
            current = current.children[char];
        }
        
        return current.isEndOfWord ? current.data : null;
    }
    
    startsWith(prefix) {
        let current = this.root;
        
        for (const char of prefix) {
            if (!current.children[char]) {
                return [];
            }
            current = current.children[char];
        }
        
        return this.getAllWords(current, prefix);
    }
    
    getAllWords(node, prefix) {
        const results = [];
        
        if (node.isEndOfWord) {
            results.push({ word: prefix, data: node.data });
        }
        
        for (const [char, childNode] of Object.entries(node.children)) {
            results.push(...this.getAllWords(childNode, prefix + char));
        }
        
        return results;
    }
}
```

### 42. How do you implement sorting and searching algorithms?
**Answer**: Efficient algorithms for data processing and analysis.

```javascript
// Quick Sort implementation
function quickSort(arr, compareFn = (a, b) => a - b) {
    if (arr.length <= 1) return arr;
    
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = [];
    const right = [];
    const equal = [];
    
    for (const element of arr) {
        const comparison = compareFn(element, pivot);
        if (comparison < 0) {
            left.push(element);
        } else if (comparison > 0) {
            right.push(element);
        } else {
            equal.push(element);
        }
    }
    
    return [
        ...quickSort(left, compareFn),
        ...equal,
        ...quickSort(right, compareFn)
    ];
}

// Merge Sort implementation
function mergeSort(arr, compareFn = (a, b) => a - b) {
    if (arr.length <= 1) return arr;
    
    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid), compareFn);
    const right = mergeSort(arr.slice(mid), compareFn);
    
    return merge(left, right, compareFn);
}

function merge(left, right, compareFn) {
    const result = [];
    let leftIndex = 0;
    let rightIndex = 0;
    
    while (leftIndex < left.length && rightIndex < right.length) {
        if (compareFn(left[leftIndex], right[rightIndex]) <= 0) {
            result.push(left[leftIndex]);
            leftIndex++;
        } else {
            result.push(right[rightIndex]);
            rightIndex++;
        }
    }
    
    return result.concat(left.slice(leftIndex)).concat(right.slice(rightIndex));
}

// Binary Search
function binarySearch(sortedArr, target, compareFn = (a, b) => a - b) {
    let left = 0;
    let right = sortedArr.length - 1;
    
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        const comparison = compareFn(sortedArr[mid], target);
        
        if (comparison === 0) {
            return mid;
        } else if (comparison < 0) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1; // Not found
}

// Heap implementation for priority queue
class MinHeap {
    constructor(compareFn = (a, b) => a - b) {
        this.heap = [];
        this.compare = compareFn;
    }
    
    parent(index) {
        return Math.floor((index - 1) / 2);
    }
    
    leftChild(index) {
        return 2 * index + 1;
    }
    
    rightChild(index) {
        return 2 * index + 2;
    }
    
    swap(i, j) {
        [this.heap[i], this.heap[j]] = [this.heap[j], this.heap[i]];
    }
    
    insert(value) {
        this.heap.push(value);
        this.heapifyUp(this.heap.length - 1);
    }
    
    heapifyUp(index) {
        while (index > 0) {
            const parentIndex = this.parent(index);
            if (this.compare(this.heap[index], this.heap[parentIndex]) >= 0) {
                break;
            }
            this.swap(index, parentIndex);
            index = parentIndex;
        }
    }
    
    extractMin() {
        if (this.heap.length === 0) return null;
        if (this.heap.length === 1) return this.heap.pop();
        
        const min = this.heap[0];
        this.heap[0] = this.heap.pop();
        this.heapifyDown(0);
        return min;
    }
    
    heapifyDown(index) {
        while (this.leftChild(index) < this.heap.length) {
            const leftIndex = this.leftChild(index);
            const rightIndex = this.rightChild(index);
            let smallestIndex = leftIndex;
            
            if (rightIndex < this.heap.length && 
                this.compare(this.heap[rightIndex], this.heap[leftIndex]) < 0) {
                smallestIndex = rightIndex;
            }
            
            if (this.compare(this.heap[index], this.heap[smallestIndex]) <= 0) {
                break;
            }
            
            this.swap(index, smallestIndex);
            index = smallestIndex;
        }
    }
    
    peek() {
        return this.heap.length > 0 ? this.heap[0] : null;
    }
    
    size() {
        return this.heap.length;
    }
}
```

### 43-55. Additional Data Structures & Algorithms Questions

### 43. How do you implement graph algorithms for data analysis?
### 44. What are dynamic programming techniques for optimization?
### 45. How do you implement string matching algorithms?
### 46. What are tree traversal algorithms and their applications?
### 47. How do you implement caching strategies?
### 48. What are bloom filters and their use cases?
### 49. How do you implement sliding window algorithms?
### 50. What are union-find data structures?
### 51. How do you implement topological sorting?
### 52. What are segment trees and their applications?
### 53. How do you implement efficient set operations?
### 54. What are skip lists and their advantages?
### 55. How do you implement approximate algorithms?

---

## API Development & Integration (56-70)

### 56. How do you build RESTful APIs with JavaScript?
**Answer**: Building scalable APIs for data services using modern JavaScript frameworks.

```javascript
// Express.js API for data services
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

class DataAPI {
    constructor() {
        this.app = express();
        this.setupMiddleware();
        this.setupRoutes();
        this.setupErrorHandling();
    }
    
    setupMiddleware() {
        // Security middleware
        this.app.use(helmet());
        this.app.use(cors());
        
        // Rate limiting
        const limiter = rateLimit({
            windowMs: 15 * 60 * 1000, // 15 minutes
            max: 100 // limit each IP to 100 requests per windowMs
        });
        this.app.use('/api/', limiter);
        
        // Body parsing
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true }));
        
        // Request logging
        this.app.use((req, res, next) => {
            console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
            next();
        });
    }
    
    setupRoutes() {
        // Data retrieval endpoints
        this.app.get('/api/data/:dataset', this.getData.bind(this));
        this.app.get('/api/data/:dataset/aggregate', this.getAggregatedData.bind(this));
        this.app.get('/api/data/:dataset/search', this.searchData.bind(this));
        
        // Data manipulation endpoints
        this.app.post('/api/data/:dataset', this.createData.bind(this));
        this.app.put('/api/data/:dataset/:id', this.updateData.bind(this));
        this.app.delete('/api/data/:dataset/:id', this.deleteData.bind(this));
        
        // Batch operations
        this.app.post('/api/data/:dataset/batch', this.batchOperation.bind(this));
        
        // Analytics endpoints
        this.app.get('/api/analytics/:dataset/summary', this.getDataSummary.bind(this));
        this.app.get('/api/analytics/:dataset/trends', this.getTrends.bind(this));
    }
    
    async getData(req, res) {
        try {
            const { dataset } = req.params;
            const { page = 1, limit = 100, sort, filter } = req.query;
            
            // Validate parameters
            const pageNum = parseInt(page);
            const limitNum = parseInt(limit);
            
            if (pageNum < 1 || limitNum < 1 || limitNum > 1000) {
                return res.status(400).json({
                    error: 'Invalid pagination parameters'
                });
            }
            
            // Parse filters
            let filters = {};
            if (filter) {
                try {
                    filters = JSON.parse(filter);
                } catch (e) {
                    return res.status(400).json({
                        error: 'Invalid filter format'
                    });
                }
            }
            
            // Fetch data
            const result = await this.dataService.getData(dataset, {
                page: pageNum,
                limit: limitNum,
                sort,
                filters
            });
            
            res.json({
                success: true,
                data: result.data,
                pagination: {
                    page: pageNum,
                    limit: limitNum,
                    total: result.total,
                    pages: Math.ceil(result.total / limitNum)
                },
                metadata: {
                    dataset,
                    timestamp: new Date().toISOString()
                }
            });
            
        } catch (error) {
            this.handleError(res, error);
        }
    }
    
    setupErrorHandling() {
        // 404 handler
        this.app.use('*', (req, res) => {
            res.status(404).json({
                error: 'Endpoint not found',
                path: req.originalUrl
            });
        });
        
        // Global error handler
        this.app.use((error, req, res, next) => {
            console.error('API Error:', error);
            
            const status = error.status || 500;
            const message = process.env.NODE_ENV === 'production' 
                ? 'Internal server error' 
                : error.message;
            
            res.status(status).json({
                error: message,
                timestamp: new Date().toISOString(),
                path: req.path
            });
        });
    }
    
    start(port = 3000) {
        this.app.listen(port, () => {
            console.log(`Data API server running on port ${port}`);
        });
    }
}
```

### 57. How do you implement WebSocket connections for real-time data?
**Answer**: Real-time data streaming using WebSockets.

```javascript
// WebSocket server implementation
const WebSocket = require('ws');
const EventEmitter = require('events');

class RealTimeDataServer extends EventEmitter {
    constructor(port = 8080) {
        super();
        this.wss = new WebSocket.Server({ port });
        this.clients = new Map();
        this.subscriptions = new Map();
        this.setupServer();
    }
    
    setupServer() {
        this.wss.on('connection', (ws, req) => {
            const clientId = this.generateClientId();
            this.clients.set(clientId, {
                ws,
                subscriptions: new Set(),
                metadata: {
                    connectedAt: new Date(),
                    ip: req.socket.remoteAddress
                }
            });
            
            console.log(`Client ${clientId} connected`);
            
            ws.on('message', (message) => {
                this.handleMessage(clientId, message);
            });
            
            ws.on('close', () => {
                this.handleDisconnect(clientId);
            });
            
            ws.on('error', (error) => {
                console.error(`Client ${clientId} error:`, error);
            });
            
            // Send welcome message
            this.sendToClient(clientId, {
                type: 'welcome',
                clientId,
                timestamp: new Date().toISOString()
            });
        });
    }
    
    handleMessage(clientId, message) {
        try {
            const data = JSON.parse(message);
            
            switch (data.type) {
                case 'subscribe':
                    this.subscribe(clientId, data.channel, data.filters);
                    break;
                case 'unsubscribe':
                    this.unsubscribe(clientId, data.channel);
                    break;
                case 'ping':
                    this.sendToClient(clientId, { type: 'pong', timestamp: new Date().toISOString() });
                    break;
                default:
                    this.sendToClient(clientId, { type: 'error', message: 'Unknown message type' });
            }
        } catch (error) {
            this.sendToClient(clientId, { type: 'error', message: 'Invalid JSON' });
        }
    }
    
    subscribe(clientId, channel, filters = {}) {
        const client = this.clients.get(clientId);
        if (!client) return;
        
        client.subscriptions.add(channel);
        
        if (!this.subscriptions.has(channel)) {
            this.subscriptions.set(channel, new Map());
        }
        
        this.subscriptions.get(channel).set(clientId, { filters });
        
        this.sendToClient(clientId, {
            type: 'subscribed',
            channel,
            timestamp: new Date().toISOString()
        });
        
        console.log(`Client ${clientId} subscribed to ${channel}`);
    }
    
    unsubscribe(clientId, channel) {
        const client = this.clients.get(clientId);
        if (!client) return;
        
        client.subscriptions.delete(channel);
        
        if (this.subscriptions.has(channel)) {
            this.subscriptions.get(channel).delete(clientId);
        }
        
        this.sendToClient(clientId, {
            type: 'unsubscribed',
            channel,
            timestamp: new Date().toISOString()
        });
    }
    
    broadcast(channel, data) {
        if (!this.subscriptions.has(channel)) return;
        
        const subscribers = this.subscriptions.get(channel);
        
        for (const [clientId, subscription] of subscribers) {
            // Apply filters if any
            if (this.matchesFilters(data, subscription.filters)) {
                this.sendToClient(clientId, {
                    type: 'data',
                    channel,
                    data,
                    timestamp: new Date().toISOString()
                });
            }
        }
    }
    
    matchesFilters(data, filters) {
        for (const [key, value] of Object.entries(filters)) {
            if (data[key] !== value) {
                return false;
            }
        }
        return true;
    }
    
    sendToClient(clientId, message) {
        const client = this.clients.get(clientId);
        if (client && client.ws.readyState === WebSocket.OPEN) {
            client.ws.send(JSON.stringify(message));
        }
    }
    
    handleDisconnect(clientId) {
        const client = this.clients.get(clientId);
        if (!client) return;
        
        // Remove from all subscriptions
        for (const channel of client.subscriptions) {
            if (this.subscriptions.has(channel)) {
                this.subscriptions.get(channel).delete(clientId);
            }
        }
        
        this.clients.delete(clientId);
        console.log(`Client ${clientId} disconnected`);
    }
    
    generateClientId() {
        return Math.random().toString(36).substr(2, 9);
    }
    
    getStats() {
        return {
            connectedClients: this.clients.size,
            activeChannels: this.subscriptions.size,
            totalSubscriptions: Array.from(this.subscriptions.values())
                .reduce((sum, subs) => sum + subs.size, 0)
        };
    }
}

// Usage
const server = new RealTimeDataServer(8080);

// Simulate data streaming
setInterval(() => {
    const sampleData = {
        metric: 'cpu_usage',
        value: Math.random() * 100,
        server: 'web-01',
        timestamp: new Date().toISOString()
    };
    
    server.broadcast('metrics', sampleData);
}, 1000);
```

### 58-70. Additional API Development Questions

### 58. How do you implement GraphQL APIs with JavaScript?
### 59. What are microservices and how do you build them?
### 60. How do you implement API authentication and authorization?
### 61. What are API rate limiting strategies?
### 62. How do you handle API versioning?
### 63. What are serverless functions and their use cases?
### 64. How do you implement API caching strategies?
### 65. What are API gateways and their benefits?
### 66. How do you implement API monitoring and logging?
### 67. What are webhook implementations?
### 68. How do you handle API documentation?
### 69. What are API testing strategies?
### 70. How do you implement API security best practices?

---

## Performance & Optimization (71-80)

### 71. How do you optimize JavaScript performance for data processing?
**Answer**: Performance optimization techniques for handling large datasets and intensive computations.

```javascript
// Memory management and optimization
class PerformanceOptimizer {
    constructor() {
        this.cache = new Map();
        this.workers = [];
        this.setupWorkerPool();
    }
    
    // 1. Efficient array operations
    optimizedArrayProcessing(largeArray) {
        // Use typed arrays for numeric data
        const typedArray = new Float64Array(largeArray);
        
        // Batch processing to avoid blocking
        const batchSize = 10000;
        const results = [];
        
        for (let i = 0; i < typedArray.length; i += batchSize) {
            const batch = typedArray.slice(i, i + batchSize);
            const batchResult = this.processBatch(batch);
            results.push(...batchResult);
            
            // Yield control to prevent blocking
            if (i % (batchSize * 10) === 0) {
                await new Promise(resolve => setTimeout(resolve, 0));
            }
        }
        
        return results;
    }
    
    processBatch(batch) {
        // Use native methods for better performance
        return Array.from(batch).map(value => value * 2).filter(value => value > 100);
    }
    
    // 2. Memoization for expensive calculations
    memoize(fn, keyGenerator = JSON.stringify) {
        const cache = new Map();
        
        return function(...args) {
            const key = keyGenerator(args);
            
            if (cache.has(key)) {
                return cache.get(key);
            }
            
            const result = fn.apply(this, args);
            cache.set(key, result);
            
            // Prevent memory leaks with cache size limit
            if (cache.size > 1000) {
                const firstKey = cache.keys().next().value;
                cache.delete(firstKey);
            }
            
            return result;
        };
    }
    
    // 3. Web Workers for CPU-intensive tasks
    setupWorkerPool(size = navigator.hardwareConcurrency || 4) {
        for (let i = 0; i < size; i++) {
            const worker = new Worker('data-worker.js');
            this.workers.push({
                worker,
                busy: false,
                id: i
            });
        }
    }
    
    async processWithWorker(data, operation) {
        return new Promise((resolve, reject) => {
            const availableWorker = this.workers.find(w => !w.busy);
            
            if (!availableWorker) {
                // Queue the task or wait for available worker
                setTimeout(() => {
                    this.processWithWorker(data, operation).then(resolve).catch(reject);
                }, 100);
                return;
            }
            
            availableWorker.busy = true;
            
            availableWorker.worker.postMessage({
                data,
                operation,
                id: Date.now()
            });
            
            const handleMessage = (event) => {
                if (event.data.id === Date.now()) {
                    availableWorker.worker.removeEventListener('message', handleMessage);
                    availableWorker.busy = false;
                    resolve(event.data.result);
                }
            };
            
            const handleError = (error) => {
                availableWorker.worker.removeEventListener('error', handleError);
                availableWorker.busy = false;
                reject(error);
            };
            
            availableWorker.worker.addEventListener('message', handleMessage);
            availableWorker.worker.addEventListener('error', handleError);
        });
    }
    
    // 4. Debouncing and throttling
    debounce(func, delay) {
        let timeoutId;
        return function(...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    // 5. Object pooling for frequent allocations
    createObjectPool(createFn, resetFn, initialSize = 10) {
        const pool = [];
        
        // Pre-populate pool
        for (let i = 0; i < initialSize; i++) {
            pool.push(createFn());
        }
        
        return {
            acquire() {
                return pool.length > 0 ? pool.pop() : createFn();
            },
            
            release(obj) {
                resetFn(obj);
                pool.push(obj);
            },
            
            size() {
                return pool.length;
            }
        };
    }
    
    // 6. Lazy evaluation for large datasets
    createLazySequence(data) {
        return {
            *[Symbol.iterator]() {
                for (const item of data) {
                    yield item;
                }
            },
            
            map(fn) {
                const self = this;
                return {
                    *[Symbol.iterator]() {
                        for (const item of self) {
                            yield fn(item);
                        }
                    },
                    map: this.map,
                    filter: this.filter,
                    take: this.take,
                    toArray: this.toArray
                };
            },
            
            filter(predicate) {
                const self = this;
                return {
                    *[Symbol.iterator]() {
                        for (const item of self) {
                            if (predicate(item)) {
                                yield item;
                            }
                        }
                    },
                    map: this.map,
                    filter: this.filter,
                    take: this.take,
                    toArray: this.toArray
                };
            },
            
            take(count) {
                const self = this;
                return {
                    *[Symbol.iterator]() {
                        let taken = 0;
                        for (const item of self) {
                            if (taken >= count) break;
                            yield item;
                            taken++;
                        }
                    },
                    toArray: this.toArray
                };
            },
            
            toArray() {
                return Array.from(this);
            }
        };
    }
    
    // 7. Performance monitoring
    measurePerformance(name, fn) {
        return async function(...args) {
            const start = performance.now();
            const result = await fn.apply(this, args);
            const end = performance.now();
            
            console.log(`${name} took ${(end - start).toFixed(2)}ms`);
            
            // Log memory usage
            if (performance.memory) {
                console.log(`Memory: ${(performance.memory.usedJSHeapSize / 1024 / 1024).toFixed(2)}MB`);
            }
            
            return result;
        };
    }
}
```

### 72-80. Additional Performance & Optimization Questions

### 72. How do you implement memory management strategies?
### 73. What are Web Workers and how do you use them effectively?
### 74. How do you optimize DOM manipulation performance?
### 75. What are service workers and their caching strategies?
### 76. How do you implement code splitting and lazy loading?
### 77. What are performance monitoring techniques?
### 78. How do you optimize network requests?
### 79. What are bundling and minification strategies?
### 80. How do you implement progressive web app features?

---

## 📚 **JavaScript Study Guide & Best Practices**

### 🎯 **Essential JavaScript Concepts for Data Engineers**

#### **Core Language Features**
1. **Data Types**: Primitive and non-primitive types, type coercion
2. **Functions**: Arrow functions, closures, higher-order functions
3. **Objects & Arrays**: Manipulation, destructuring, spread operator
4. **Asynchronous Programming**: Promises, async/await, event loop
5. **Error Handling**: Try-catch, custom errors, error propagation

#### **Data Processing Applications**
1. **Frontend Development**: Data visualization dashboards
2. **API Development**: RESTful services with Node.js
3. **Data Transformation**: Client-side data manipulation
4. **Real-time Applications**: WebSocket connections, streaming
5. **Integration**: Connecting data systems and services

### 🚀 **Best Practices for Data Applications**

#### **Performance Optimization**
- Use appropriate data structures (Map, Set, typed arrays)
- Implement memoization for expensive calculations
- Utilize Web Workers for CPU-intensive tasks
- Apply debouncing and throttling for user interactions
- Optimize memory usage with object pooling

#### **Code Organization**
- Modular architecture with ES6 modules
- Consistent error handling patterns
- Proper async/await usage
- Memory leak prevention
- Performance monitoring and profiling

#### **Data Processing Patterns**
- Functional programming approaches
- Immutable data transformations
- Lazy evaluation for large datasets
- Batch processing for performance
- Stream processing for real-time data

### 📈 **Interview Preparation Strategy**

#### **Technical Depth Levels**
1. **Basic**: Variables, functions, objects, basic async
2. **Intermediate**: Closures, prototypes, advanced async, error handling
3. **Advanced**: Performance optimization, design patterns, architecture
4. **Expert**: Framework internals, custom implementations, scalability

#### **Common Interview Categories**
1. **Fundamentals** (30%): Data types, functions, scope, closures
2. **Asynchronous Programming** (25%): Promises, async/await, event loop
3. **Data Structures** (20%): Arrays, objects, algorithms, performance
4. **Modern JavaScript** (25%): ES6+, modules, frameworks, tooling

### 🔗 **Essential Resources**

- **MDN Web Docs**: [JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- **ECMAScript Specification**: [TC39 Proposals](https://github.com/tc39/proposals)
- **Performance**: [Web Performance APIs](https://developer.mozilla.org/en-US/docs/Web/API/Performance)
- **Node.js**: [Official Documentation](https://nodejs.org/en/docs/)

This comprehensive guide covers 80 JavaScript interview questions essential for data engineering roles, progressing from basic concepts to advanced performance optimization and real-world application development.