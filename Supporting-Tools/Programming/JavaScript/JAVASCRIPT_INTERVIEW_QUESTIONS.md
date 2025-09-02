# JavaScript Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-20)](#core-concepts-questions-1-20)
2. [Asynchronous Programming (21-35)](#asynchronous-programming-21-35)
3. [Data Structures & Algorithms (36-50)](#data-structures--algorithms-36-50)
4. [API Development & Integration (51-65)](#api-development--integration-51-65)
5. [Performance & Optimization (66-80)](#performance--optimization-66-80)

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

## Core Concepts Questions (1-20)

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
function memoize(fn) {
    const cache = new Map();
    
    return function(...args) {
        const key = JSON.stringify(args);
        
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

// Module pattern with closures
const DataAnalyzer = (function() {
    let datasets = [];
    let analysisCache = new Map();
    
    return {
        addDataset: function(name, data) {
            datasets.push({ name, data, timestamp: Date.now() });
        },
        
        analyze: function(datasetName, analysisType) {
            const cacheKey = `${datasetName}-${analysisType}`;
            
            if (analysisCache.has(cacheKey)) {
                return analysisCache.get(cacheKey);
            }
            
            const dataset = datasets.find(d => d.name === datasetName);
            if (!dataset) {
                throw new Error(`Dataset ${datasetName} not found`);
            }
            
            const result = performAnalysis(dataset.data, analysisType);
            analysisCache.set(cacheKey, result);
            
            return result;
        },
        
        clearCache: function() {
            analysisCache.clear();
        }
    };
})();
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

// Advanced array operations
function processDataBatch(data, batchSize = 100) {
    const batches = [];
    
    for (let i = 0; i < data.length; i += batchSize) {
        batches.push(data.slice(i, i + batchSize));
    }
    
    return batches.map(batch => ({
        size: batch.length,
        total: batch.reduce((sum, item) => sum + item.amount, 0),
        average: batch.reduce((sum, item) => sum + item.amount, 0) / batch.length
    }));
}

// Object manipulation
const customerData = {
    personal: {
        name: 'John Doe',
        email: 'john@example.com',
        age: 30
    },
    orders: [
        { id: 1, total: 100 },
        { id: 2, total: 150 }
    ],
    preferences: {
        newsletter: true,
        notifications: false
    }
};

// Deep cloning
function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }
    
    if (obj instanceof Date) {
        return new Date(obj.getTime());
    }
    
    if (obj instanceof Array) {
        return obj.map(item => deepClone(item));
    }
    
    const cloned = {};
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            cloned[key] = deepClone(obj[key]);
        }
    }
    
    return cloned;
}

// Object property access
function getNestedProperty(obj, path) {
    return path.split('.').reduce((current, key) => {
        return current && current[key] !== undefined ? current[key] : undefined;
    }, obj);
}

// Usage
const customerName = getNestedProperty(customerData, 'personal.name');
const firstOrderTotal = getNestedProperty(customerData, 'orders.0.total');

// Object transformation
function transformCustomerData(customer) {
    return {
        id: customer.id,
        fullName: `${customer.personal.firstName} ${customer.personal.lastName}`,
        contactInfo: {
            email: customer.personal.email,
            phone: customer.personal.phone
        },
        orderSummary: {
            totalOrders: customer.orders.length,
            totalSpent: customer.orders.reduce((sum, order) => sum + order.total, 0),
            averageOrder: customer.orders.reduce((sum, order) => sum + order.total, 0) / customer.orders.length
        }
    };
}
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

// Hoisting examples
console.log(hoistedVar); // undefined (not ReferenceError)
var hoistedVar = 'I am hoisted';

// console.log(letVar); // ReferenceError (temporal dead zone)
let letVar = 'I am not hoisted';

// Function hoisting
console.log(hoistedFunction()); // "I am hoisted!"

function hoistedFunction() {
    return "I am hoisted!";
}

// Arrow functions and scope
const DataProcessor = {
    name: 'Main Processor',
    data: [],
    
    // Regular function - has its own 'this'
    processWithRegular: function(callback) {
        this.data.forEach(function(item) {
            // 'this' refers to global object or undefined in strict mode
            callback(item);
        });
    },
    
    // Arrow function - inherits 'this' from enclosing scope
    processWithArrow: function(callback) {
        this.data.forEach((item) => {
            // 'this' refers to DataProcessor object
            callback(item, this.name);
        });
    }
};

// Scope chain example
function outerFunction(outerParam) {
    const outerVar = 'outer';
    
    function middleFunction(middleParam) {
        const middleVar = 'middle';
        
        function innerFunction(innerParam) {
            const innerVar = 'inner';
            
            // Has access to all outer scopes
            console.log(innerVar);   // 'inner'
            console.log(middleVar);  // 'middle'
            console.log(outerVar);   // 'outer'
            console.log(innerParam); // inner parameter
            console.log(middleParam); // middle parameter
            console.log(outerParam); // outer parameter
        }
        
        return innerFunction;
    }
    
    return middleFunction;
}

const processor = outerFunction('outer')('middle');
processor('inner');
```

---

## Asynchronous Programming (21-35)

### 21. Explain Promises and async/await for data processing.
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

// Handle partial failures with Promise.allSettled
async function fetchUsersWithErrorHandling(userIds) {
    const userPromises = userIds.map(id => fetchUserData(id));
    const results = await Promise.allSettled(userPromises);
    
    const successful = results
        .filter(result => result.status === 'fulfilled')
        .map(result => result.value);
    
    const failed = results
        .filter(result => result.status === 'rejected')
        .map(result => result.reason);
    
    return { successful, failed };
}

// Race conditions with Promise.race
async function fetchWithTimeout(promise, timeout = 5000) {
    const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Operation timed out')), timeout);
    });
    
    return Promise.race([promise, timeoutPromise]);
}

// Data processing pipeline with async/await
class DataPipeline {
    constructor() {
        this.stages = [];
    }
    
    addStage(stageFn) {
        this.stages.push(stageFn);
        return this;
    }
    
    async process(initialData) {
        let data = initialData;
        
        for (const [index, stage] of this.stages.entries()) {
            try {
                console.log(`Processing stage ${index + 1}...`);
                data = await stage(data);
            } catch (error) {
                console.error(`Error in stage ${index + 1}:`, error);
                throw error;
            }
        }
        
        return data;
    }
}

// Usage
const pipeline = new DataPipeline()
    .addStage(async (data) => {
        // Stage 1: Fetch additional data
        const enriched = await Promise.all(
            data.map(async (item) => ({
                ...item,
                details: await fetchItemDetails(item.id)
            }))
        );
        return enriched;
    })
    .addStage(async (data) => {
        // Stage 2: Transform data
        return data.map(item => ({
            id: item.id,
            name: item.name,
            value: item.details.value * 1.1 // Apply 10% markup
        }));
    })
    .addStage(async (data) => {
        // Stage 3: Save to database
        await saveToDatabase(data);
        return data;
    });

// Execute pipeline
const initialData = [{ id: 1, name: 'Item 1' }, { id: 2, name: 'Item 2' }];
pipeline.process(initialData)
    .then(result => console.log('Pipeline completed:', result))
    .catch(error => console.error('Pipeline failed:', error));
```

### 22. How do you handle errors in asynchronous operations?
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

// Error handling middleware
async function withErrorHandling(operation, context = {}) {
    try {
        return await operation();
    } catch (error) {
        // Log error with context
        console.error('Operation failed:', {
            error: error.message,
            stack: error.stack,
            context,
            timestamp: new Date().toISOString()
        });
        
        // Transform error if needed
        if (error.name === 'ValidationError') {
            throw new DataProcessingError(
                `Validation failed: ${error.message}`,
                'VALIDATION_FAILED',
                error.data
            );
        }
        
        throw error;
    }
}

// Circuit breaker pattern
class CircuitBreaker {
    constructor(threshold = 5, timeout = 60000) {
        this.threshold = threshold;
        this.timeout = timeout;
        this.failureCount = 0;
        this.lastFailureTime = null;
        this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    }
    
    async execute(operation) {
        if (this.state === 'OPEN') {
            if (Date.now() - this.lastFailureTime > this.timeout) {
                this.state = 'HALF_OPEN';
            } else {
                throw new Error('Circuit breaker is OPEN');
            }
        }
        
        try {
            const result = await operation();
            this.onSuccess();
            return result;
        } catch (error) {
            this.onFailure();
            throw error;
        }
    }
    
    onSuccess() {
        this.failureCount = 0;
        this.state = 'CLOSED';
    }
    
    onFailure() {
        this.failureCount++;
        this.lastFailureTime = Date.now();
        
        if (this.failureCount >= this.threshold) {
            this.state = 'OPEN';
        }
    }
}

// Usage
const circuitBreaker = new CircuitBreaker(3, 30000);

async function fetchDataWithCircuitBreaker(url) {
    return circuitBreaker.execute(async () => {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
    });
}
```

---

## Data Structures & Algorithms (36-50)

### 36. How do you implement efficient data structures for processing?
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

// Binary Search Tree for sorted data
class BSTNode {
    constructor(value, data = null) {
        this.value = value;
        this.data = data;
        this.left = null;
        this.right = null;
    }
}

class BinarySearchTree {
    constructor() {
        this.root = null;
    }
    
    insert(value, data = null) {
        const newNode = new BSTNode(value, data);
        
        if (!this.root) {
            this.root = newNode;
            return;
        }
        
        let current = this.root;
        while (true) {
            if (value < current.value) {
                if (!current.left) {
                    current.left = newNode;
                    break;
                }
                current = current.left;
            } else {
                if (!current.right) {
                    current.right = newNode;
                    break;
                }
                current = current.right;
            }
        }
    }
    
    search(value) {
        let current = this.root;
        
        while (current) {
            if (value === current.value) {
                return current.data;
            } else if (value < current.value) {
                current = current.left;
            } else {
                current = current.right;
            }
        }
        
        return null;
    }
    
    inOrderTraversal(callback) {
        this.inOrder(this.root, callback);
    }
    
    inOrder(node, callback) {
        if (node) {
            this.inOrder(node.left, callback);
            callback(node.value, node.data);
            this.inOrder(node.right, callback);
        }
    }
    
    findRange(min, max) {
        const results = [];
        this.rangeSearch(this.root, min, max, results);
        return results;
    }
    
    rangeSearch(node, min, max, results) {
        if (!node) return;
        
        if (node.value >= min && node.value <= max) {
            results.push({ value: node.value, data: node.data });
        }
        
        if (node.value > min) {
            this.rangeSearch(node.left, min, max, results);
        }
        
        if (node.value < max) {
            this.rangeSearch(node.right, min, max, results);
        }
    }
}

// Usage examples
const userLookup = new HashMap();
userLookup.set('user123', { name: 'John', email: 'john@example.com' });
userLookup.set('user456', { name: 'Jane', email: 'jane@example.com' });

const productTrie = new Trie();
productTrie.insert('laptop', { id: 1, price: 999 });
productTrie.insert('laptop-pro', { id: 2, price: 1299 });
productTrie.insert('mouse', { id: 3, price: 29 });

const suggestions = productTrie.startsWith('lap');
console.log(suggestions); // [{ word: 'laptop', data: {...} }, { word: 'laptop-pro', data: {...} }]

const priceBST = new BinarySearchTree();
priceBST.insert(100, { product: 'Mouse' });
priceBST.insert(500, { product: 'Keyboard' });
priceBST.insert(1000, { product: 'Monitor' });

const midRangeProducts = priceBST.findRange(200, 800);
console.log(midRangeProducts); // Products in price range 200-800
```

---

## API Development & Integration (51-65)

### 51. How do you build RESTful APIs with JavaScript?
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
    
    async getAggregatedData(req, res) {
        try {
            const { dataset } = req.params;
            const { groupBy, aggregations, timeRange } = req.query;
            
            if (!groupBy || !aggregations) {
                return res.status(400).json({
                    error: 'groupBy and aggregations parameters are required'
                });
            }
            
            const groupByFields = groupBy.split(',');
            const aggFunctions = aggregations.split(',');
            
            const result = await this.dataService.aggregate(dataset, {
                groupBy: groupByFields,
                aggregations: aggFunctions,
                timeRange: timeRange ? JSON.parse(timeRange) : null
            });
            
            res.json({
                success: true,
                data: result,
                metadata: {
                    groupBy: groupByFields,
                    aggregations: aggFunctions,
                    generatedAt: new Date().toISOString()
                }
            });
            
        } catch (error) {
            this.handleError(res, error);
        }
    }
    
    async createData(req, res) {
        try {
            const { dataset } = req.params;
            const data = req.body;
            
            // Validate data
            const validation = await this.validateData(dataset, data);
            if (!validation.isValid) {
                return res.status(400).json({
                    error: 'Validation failed',
                    details: validation.errors
                });
            }
            
            // Create record
            const result = await this.dataService.create(dataset, data);
            
            res.status(201).json({
                success: true,
                data: result,
                message: 'Data created successfully'
            });
            
        } catch (error) {
            this.handleError(res, error);
        }
    }
    
    async batchOperation(req, res) {
        try {
            const { dataset } = req.params;
            const { operations } = req.body;
            
            if (!Array.isArray(operations)) {
                return res.status(400).json({
                    error: 'Operations must be an array'
                });
            }
            
            const results = await Promise.allSettled(
                operations.map(op => this.processBatchOperation(dataset, op))
            );
            
            const successful = results.filter(r => r.status === 'fulfilled').length;
            const failed = results.filter(r => r.status === 'rejected').length;
            
            res.json({
                success: true,
                summary: {
                    total: operations.length,
                    successful,
                    failed
                },
                results: results.map((result, index) => ({
                    operation: index,
                    status: result.status,
                    data: result.status === 'fulfilled' ? result.value : null,
                    error: result.status === 'rejected' ? result.reason.message : null
                }))
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
    
    handleError(res, error) {
        console.error('Request error:', error);
        
        if (error.name === 'ValidationError') {
            return res.status(400).json({
                error: 'Validation failed',
                details: error.details
            });
        }
        
        if (error.name === 'NotFoundError') {
            return res.status(404).json({
                error: 'Resource not found'
            });
        }
        
        res.status(500).json({
            error: 'Internal server error',
            timestamp: new Date().toISOString()
        });
    }
    
    start(port = 3000) {
        this.app.listen(port, () => {
            console.log(`Data API server running on port ${port}`);
        });
    }
}

// Usage
const api = new DataAPI();
api.start(3000);
```

---

## Performance & Optimization (66-80)

### 66. How do you optimize JavaScript performance for data processing?
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

// Usage examples
const optimizer = new PerformanceOptimizer();

// Memoized expensive calculation
const expensiveCalculation = optimizer.memoize((data) => {
    return data.reduce((sum, item) => sum + Math.sqrt(item.value), 0);
});

// Lazy sequence processing
const largeDataset = Array.from({ length: 1000000 }, (_, i) => ({ id: i, value: Math.random() * 100 }));
const lazySequence = optimizer.createLazySequence(largeDataset);

const result = lazySequence
    .filter(item => item.value > 50)
    .map(item => ({ ...item, processed: true }))
    .take(100)
    .toArray();

// Object pooling for frequent operations
const dataPointPool = optimizer.createObjectPool(
    () => ({ x: 0, y: 0, processed: false }),
    (obj) => { obj.x = 0; obj.y = 0; obj.processed = false; }
);

// Performance monitoring
const monitoredFunction = optimizer.measurePerformance('Data Processing', async (data) => {
    return data.map(item => item.value * 2);
});
```

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

---

**Remember**: JavaScript's versatility makes it valuable across the entire data engineering stack. Focus on understanding both client-side and server-side applications, with emphasis on asynchronous programming and performance optimization.