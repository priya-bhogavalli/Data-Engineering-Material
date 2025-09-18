# 🚀 JavaScript Advanced Interview Questions & Answers

## 📋 Table of Contents
- [Advanced Language Features](#advanced-language-features)
- [Asynchronous Programming](#asynchronous-programming)
- [Performance Optimization](#performance-optimization)
- [Modern JavaScript (ES6+)](#modern-javascript-es6)
- [Node.js & Backend](#nodejs--backend)
- [Testing & Debugging](#testing--debugging)

---

## Advanced Language Features

### 1. Explain closures and their practical applications.
**Answer:**
**Closure Fundamentals:**
```javascript
// Basic closure
function outerFunction(x) {
    return function innerFunction(y) {
        return x + y; // Inner function has access to outer scope
    };
}

const addFive = outerFunction(5);
console.log(addFive(3)); // 8

// Module pattern using closures
const counterModule = (function() {
    let count = 0; // Private variable
    
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
})();

console.log(counterModule.getCount()); // 0
counterModule.increment();
console.log(counterModule.getCount()); // 1
```

**Practical Applications:**
```javascript
// Function factories
function createValidator(pattern) {
    return function(value) {
        return pattern.test(value);
    };
}

const emailValidator = createValidator(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
const phoneValidator = createValidator(/^\d{10}$/);

// Memoization
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

const expensiveFunction = memoize((n) => {
    console.log('Computing...');
    return n * n;
});
```

### 2. How does prototypal inheritance work in JavaScript?
**Answer:**
**Prototype Chain:**
```javascript
// Constructor function approach
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    return `${this.name} makes a sound`;
};

function Dog(name, breed) {
    Animal.call(this, name); // Call parent constructor
    this.breed = breed;
}

// Set up inheritance
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.bark = function() {
    return `${this.name} barks`;
};

const dog = new Dog('Buddy', 'Golden Retriever');
console.log(dog.speak()); // "Buddy makes a sound"
console.log(dog.bark());  // "Buddy barks"
```

**Modern Class Syntax:**
```javascript
class Animal {
    constructor(name) {
        this.name = name;
    }
    
    speak() {
        return `${this.name} makes a sound`;
    }
}

class Dog extends Animal {
    constructor(name, breed) {
        super(name);
        this.breed = breed;
    }
    
    bark() {
        return `${this.name} barks`;
    }
    
    speak() {
        return `${super.speak()} - specifically barks`;
    }
}

// Mixins for multiple inheritance
const Flyable = {
    fly() {
        return `${this.name} is flying`;
    }
};

Object.assign(Dog.prototype, Flyable);
```

### 3. What are Symbols and their use cases?
**Answer:**
**Symbol Basics:**
```javascript
// Creating symbols
const sym1 = Symbol('description');
const sym2 = Symbol('description');
console.log(sym1 === sym2); // false - each symbol is unique

// Well-known symbols
const obj = {
    [Symbol.iterator]: function* () {
        yield 1;
        yield 2;
        yield 3;
    }
};

for (const value of obj) {
    console.log(value); // 1, 2, 3
}
```

**Practical Use Cases:**
```javascript
// Private properties simulation
const _private = Symbol('private');

class MyClass {
    constructor() {
        this[_private] = 'This is private';
        this.public = 'This is public';
    }
    
    getPrivate() {
        return this[_private];
    }
}

// Object property keys that won't conflict
const CACHE_KEY = Symbol('cache');
const API_KEY = Symbol('apiKey');

const config = {
    [CACHE_KEY]: new Map(),
    [API_KEY]: 'secret-key',
    normalProperty: 'visible'
};

// Global symbol registry
const globalSym = Symbol.for('app.config');
const sameSym = Symbol.for('app.config');
console.log(globalSym === sameSym); // true
```

### 4. Explain the event loop and microtask queue.
**Answer:**
**Event Loop Mechanics:**
```javascript
console.log('1'); // Synchronous

setTimeout(() => console.log('2'), 0); // Macrotask

Promise.resolve().then(() => console.log('3')); // Microtask

console.log('4'); // Synchronous

// Output: 1, 4, 3, 2
```

**Detailed Example:**
```javascript
console.log('Start');

setTimeout(() => console.log('Timeout 1'), 0);

Promise.resolve()
    .then(() => {
        console.log('Promise 1');
        return Promise.resolve();
    })
    .then(() => console.log('Promise 2'));

setTimeout(() => console.log('Timeout 2'), 0);

Promise.resolve().then(() => {
    console.log('Promise 3');
    setTimeout(() => console.log('Timeout in Promise'), 0);
});

console.log('End');

// Output: Start, End, Promise 1, Promise 3, Promise 2, Timeout 1, Timeout 2, Timeout in Promise
```

**Microtask vs Macrotask:**
```javascript
// Microtasks (higher priority)
// - Promise.then/catch/finally
// - queueMicrotask()
// - MutationObserver

// Macrotasks (lower priority)
// - setTimeout/setInterval
// - setImmediate (Node.js)
// - I/O operations
// - UI rendering

function demonstrateEventLoop() {
    console.log('1');
    
    queueMicrotask(() => console.log('Microtask 1'));
    
    setTimeout(() => console.log('Macrotask 1'), 0);
    
    Promise.resolve().then(() => {
        console.log('Microtask 2');
        queueMicrotask(() => console.log('Nested Microtask'));
    });
    
    console.log('2');
}
```

### 5. How do you implement deep cloning in JavaScript?
**Answer:**
**Deep Clone Implementations:**
```javascript
// Structured cloning (modern browsers)
function deepClone(obj) {
    return structuredClone(obj);
}

// Custom implementation
function customDeepClone(obj, visited = new WeakMap()) {
    // Handle primitives and null
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }
    
    // Handle circular references
    if (visited.has(obj)) {
        return visited.get(obj);
    }
    
    // Handle Date
    if (obj instanceof Date) {
        return new Date(obj.getTime());
    }
    
    // Handle RegExp
    if (obj instanceof RegExp) {
        return new RegExp(obj.source, obj.flags);
    }
    
    // Handle Arrays
    if (Array.isArray(obj)) {
        const cloned = [];
        visited.set(obj, cloned);
        for (let i = 0; i < obj.length; i++) {
            cloned[i] = customDeepClone(obj[i], visited);
        }
        return cloned;
    }
    
    // Handle Objects
    const cloned = {};
    visited.set(obj, cloned);
    
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            cloned[key] = customDeepClone(obj[key], visited);
        }
    }
    
    return cloned;
}

// Using Lodash (production recommended)
const _ = require('lodash');
const cloned = _.cloneDeep(originalObject);
```

---

## Asynchronous Programming

### 6. Compare Promises, async/await, and callbacks for error handling.
**Answer:**
**Callback Pattern:**
```javascript
// Callback hell
function fetchUserData(userId, callback) {
    getUserById(userId, (err, user) => {
        if (err) return callback(err);
        
        getPostsByUser(user.id, (err, posts) => {
            if (err) return callback(err);
            
            getCommentsForPosts(posts, (err, comments) => {
                if (err) return callback(err);
                
                callback(null, { user, posts, comments });
            });
        });
    });
}
```

**Promise Pattern:**
```javascript
function fetchUserData(userId) {
    return getUserById(userId)
        .then(user => {
            return getPostsByUser(user.id)
                .then(posts => {
                    return getCommentsForPosts(posts)
                        .then(comments => ({ user, posts, comments }));
                });
        })
        .catch(error => {
            console.error('Error:', error);
            throw error;
        });
}

// Better Promise chaining
function fetchUserDataBetter(userId) {
    let userData = {};
    
    return getUserById(userId)
        .then(user => {
            userData.user = user;
            return getPostsByUser(user.id);
        })
        .then(posts => {
            userData.posts = posts;
            return getCommentsForPosts(posts);
        })
        .then(comments => {
            userData.comments = comments;
            return userData;
        })
        .catch(error => {
            console.error('Error in fetchUserData:', error);
            throw new Error(`Failed to fetch user data: ${error.message}`);
        });
}
```

**Async/Await Pattern:**
```javascript
async function fetchUserData(userId) {
    try {
        const user = await getUserById(userId);
        const posts = await getPostsByUser(user.id);
        const comments = await getCommentsForPosts(posts);
        
        return { user, posts, comments };
    } catch (error) {
        console.error('Error in fetchUserData:', error);
        throw new Error(`Failed to fetch user data: ${error.message}`);
    }
}

// Parallel execution with async/await
async function fetchUserDataParallel(userId) {
    try {
        const user = await getUserById(userId);
        
        // Execute in parallel
        const [posts, profile, settings] = await Promise.all([
            getPostsByUser(user.id),
            getUserProfile(user.id),
            getUserSettings(user.id)
        ]);
        
        return { user, posts, profile, settings };
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
```

### 7. How do you implement custom Promise-like functionality?
**Answer:**
**Basic Promise Implementation:**
```javascript
class MyPromise {
    constructor(executor) {
        this.state = 'pending';
        this.value = undefined;
        this.reason = undefined;
        this.onFulfilledCallbacks = [];
        this.onRejectedCallbacks = [];
        
        const resolve = (value) => {
            if (this.state === 'pending') {
                this.state = 'fulfilled';
                this.value = value;
                this.onFulfilledCallbacks.forEach(callback => callback(value));
            }
        };
        
        const reject = (reason) => {
            if (this.state === 'pending') {
                this.state = 'rejected';
                this.reason = reason;
                this.onRejectedCallbacks.forEach(callback => callback(reason));
            }
        };
        
        try {
            executor(resolve, reject);
        } catch (error) {
            reject(error);
        }
    }
    
    then(onFulfilled, onRejected) {
        return new MyPromise((resolve, reject) => {
            const handleFulfilled = (value) => {
                try {
                    const result = onFulfilled ? onFulfilled(value) : value;
                    resolve(result);
                } catch (error) {
                    reject(error);
                }
            };
            
            const handleRejected = (reason) => {
                try {
                    const result = onRejected ? onRejected(reason) : reason;
                    resolve(result);
                } catch (error) {
                    reject(error);
                }
            };
            
            if (this.state === 'fulfilled') {
                setTimeout(() => handleFulfilled(this.value), 0);
            } else if (this.state === 'rejected') {
                setTimeout(() => handleRejected(this.reason), 0);
            } else {
                this.onFulfilledCallbacks.push(handleFulfilled);
                this.onRejectedCallbacks.push(handleRejected);
            }
        });
    }
    
    catch(onRejected) {
        return this.then(null, onRejected);
    }
    
    static resolve(value) {
        return new MyPromise(resolve => resolve(value));
    }
    
    static reject(reason) {
        return new MyPromise((_, reject) => reject(reason));
    }
}
```

### 8. How do you handle concurrent async operations efficiently?
**Answer:**
**Concurrency Patterns:**
```javascript
// Promise.all - All must succeed
async function fetchAllUserData(userIds) {
    try {
        const users = await Promise.all(
            userIds.map(id => fetchUser(id))
        );
        return users;
    } catch (error) {
        // If any fails, all fail
        console.error('One or more requests failed:', error);
        throw error;
    }
}

// Promise.allSettled - Get all results regardless of failures
async function fetchAllUserDataSafe(userIds) {
    const results = await Promise.allSettled(
        userIds.map(id => fetchUser(id))
    );
    
    const successful = results
        .filter(result => result.status === 'fulfilled')
        .map(result => result.value);
    
    const failed = results
        .filter(result => result.status === 'rejected')
        .map(result => result.reason);
    
    return { successful, failed };
}

// Promise.race - First to complete wins
async function fetchWithTimeout(url, timeout = 5000) {
    return Promise.race([
        fetch(url),
        new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Timeout')), timeout)
        )
    ]);
}

// Controlled concurrency
async function processWithConcurrencyLimit(items, processor, limit = 3) {
    const results = [];
    
    for (let i = 0; i < items.length; i += limit) {
        const batch = items.slice(i, i + limit);
        const batchResults = await Promise.all(
            batch.map(item => processor(item))
        );
        results.push(...batchResults);
    }
    
    return results;
}
```

---

## Performance Optimization

### 9. How do you optimize JavaScript performance?
**Answer:**
**Code Optimization:**
```javascript
// Avoid frequent DOM queries
// Bad
for (let i = 0; i < 1000; i++) {
    document.getElementById('container').innerHTML += '<div>Item</div>';
}

// Good
const container = document.getElementById('container');
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
    const div = document.createElement('div');
    div.textContent = 'Item';
    fragment.appendChild(div);
}
container.appendChild(fragment);

// Debouncing for expensive operations
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

const expensiveSearch = debounce((query) => {
    // Expensive search operation
    console.log('Searching for:', query);
}, 300);

// Throttling for frequent events
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

const handleScroll = throttle(() => {
    console.log('Scroll event handled');
}, 100);
```

**Memory Management:**
```javascript
// Avoid memory leaks
class ComponentManager {
    constructor() {
        this.eventListeners = new Map();
        this.timers = new Set();
    }
    
    addEventListener(element, event, handler) {
        element.addEventListener(event, handler);
        
        if (!this.eventListeners.has(element)) {
            this.eventListeners.set(element, new Map());
        }
        this.eventListeners.get(element).set(event, handler);
    }
    
    setTimeout(callback, delay) {
        const timerId = setTimeout(callback, delay);
        this.timers.add(timerId);
        return timerId;
    }
    
    cleanup() {
        // Remove all event listeners
        for (const [element, events] of this.eventListeners) {
            for (const [event, handler] of events) {
                element.removeEventListener(event, handler);
            }
        }
        this.eventListeners.clear();
        
        // Clear all timers
        for (const timerId of this.timers) {
            clearTimeout(timerId);
        }
        this.timers.clear();
    }
}

// Object pooling for frequent allocations
class ObjectPool {
    constructor(createFn, resetFn, initialSize = 10) {
        this.createFn = createFn;
        this.resetFn = resetFn;
        this.pool = [];
        
        for (let i = 0; i < initialSize; i++) {
            this.pool.push(this.createFn());
        }
    }
    
    acquire() {
        return this.pool.length > 0 ? this.pool.pop() : this.createFn();
    }
    
    release(obj) {
        this.resetFn(obj);
        this.pool.push(obj);
    }
}
```

### 10. How do you implement lazy loading and code splitting?
**Answer:**
**Dynamic Imports:**
```javascript
// Lazy loading modules
async function loadFeature() {
    try {
        const { default: FeatureModule } = await import('./feature-module.js');
        return new FeatureModule();
    } catch (error) {
        console.error('Failed to load feature:', error);
        throw error;
    }
}

// Conditional loading
async function loadPolyfill() {
    if (!window.IntersectionObserver) {
        await import('intersection-observer-polyfill');
    }
}

// Route-based code splitting (React example)
const LazyComponent = React.lazy(() => import('./LazyComponent'));

function App() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <LazyComponent />
        </Suspense>
    );
}
```

**Image Lazy Loading:**
```javascript
class LazyImageLoader {
    constructor() {
        this.observer = new IntersectionObserver(
            this.handleIntersection.bind(this),
            { threshold: 0.1 }
        );
    }
    
    observe(img) {
        this.observer.observe(img);
    }
    
    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                this.loadImage(img);
                this.observer.unobserve(img);
            }
        });
    }
    
    loadImage(img) {
        const src = img.dataset.src;
        if (src) {
            img.src = src;
            img.classList.add('loaded');
        }
    }
}

// Usage
const lazyLoader = new LazyImageLoader();
document.querySelectorAll('img[data-src]').forEach(img => {
    lazyLoader.observe(img);
});
```

---

## Modern JavaScript (ES6+)

### 11. How do you use advanced destructuring and spread operators?
**Answer:**
**Advanced Destructuring:**
```javascript
// Nested destructuring
const user = {
    name: 'John',
    address: {
        street: '123 Main St',
        city: 'New York',
        coordinates: { lat: 40.7128, lng: -74.0060 }
    },
    hobbies: ['reading', 'swimming']
};

const {
    name,
    address: {
        city,
        coordinates: { lat, lng }
    },
    hobbies: [firstHobby, ...otherHobbies]
} = user;

// Function parameter destructuring
function processUser({
    name,
    age = 18,
    address: { city } = {},
    ...rest
}) {
    console.log(`${name} from ${city}, age ${age}`);
    console.log('Other properties:', rest);
}

// Array destructuring with rest
const [first, second, ...remaining] = [1, 2, 3, 4, 5];

// Swapping variables
let a = 1, b = 2;
[a, b] = [b, a];
```

**Advanced Spread Usage:**
```javascript
// Object merging with precedence
const defaults = { theme: 'light', language: 'en' };
const userPrefs = { theme: 'dark' };
const config = { ...defaults, ...userPrefs }; // userPrefs overrides defaults

// Conditional spreading
const createUser = (name, isAdmin) => ({
    name,
    ...(isAdmin && { role: 'admin', permissions: ['read', 'write'] })
});

// Function arguments
function sum(...numbers) {
    return numbers.reduce((total, num) => total + num, 0);
}

const numbers = [1, 2, 3, 4, 5];
console.log(sum(...numbers));

// Array operations
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];
const withNewItems = [...arr1, 'new', ...arr2];
```

### 12. How do you use Proxy and Reflect for metaprogramming?
**Answer:**
**Proxy Applications:**
```javascript
// Property validation
function createValidatedObject(target, validators) {
    return new Proxy(target, {
        set(obj, prop, value) {
            if (validators[prop]) {
                const isValid = validators[prop](value);
                if (!isValid) {
                    throw new Error(`Invalid value for ${prop}: ${value}`);
                }
            }
            obj[prop] = value;
            return true;
        }
    });
}

const userValidators = {
    age: value => typeof value === 'number' && value >= 0,
    email: value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
};

const user = createValidatedObject({}, userValidators);

// Observable object
function createObservable(target, onChange) {
    return new Proxy(target, {
        set(obj, prop, value) {
            const oldValue = obj[prop];
            obj[prop] = value;
            onChange(prop, value, oldValue);
            return true;
        }
    });
}

const data = createObservable({}, (prop, newVal, oldVal) => {
    console.log(`${prop} changed from ${oldVal} to ${newVal}`);
});

// API wrapper
function createAPIWrapper(baseURL) {
    return new Proxy({}, {
        get(target, prop) {
            return async (...args) => {
                const url = `${baseURL}/${prop}`;
                const response = await fetch(url, ...args);
                return response.json();
            };
        }
    });
}

const api = createAPIWrapper('https://api.example.com');
// api.users() -> GET https://api.example.com/users
```

### 13. How do you implement generators and iterators?
**Answer:**
**Generator Functions:**
```javascript
// Basic generator
function* numberGenerator() {
    let i = 0;
    while (true) {
        yield i++;
    }
}

const gen = numberGenerator();
console.log(gen.next().value); // 0
console.log(gen.next().value); // 1

// Fibonacci generator
function* fibonacci() {
    let [a, b] = [0, 1];
    while (true) {
        yield a;
        [a, b] = [b, a + b];
    }
}

// Take first n values
function* take(n, iterable) {
    let count = 0;
    for (const value of iterable) {
        if (count >= n) break;
        yield value;
        count++;
    }
}

const firstTenFib = [...take(10, fibonacci())];

// Async generator
async function* fetchPages(urls) {
    for (const url of urls) {
        try {
            const response = await fetch(url);
            const data = await response.json();
            yield data;
        } catch (error) {
            yield { error: error.message, url };
        }
    }
}

// Custom iterator
class Range {
    constructor(start, end, step = 1) {
        this.start = start;
        this.end = end;
        this.step = step;
    }
    
    *[Symbol.iterator]() {
        for (let i = this.start; i < this.end; i += this.step) {
            yield i;
        }
    }
}

const range = new Range(0, 10, 2);
console.log([...range]); // [0, 2, 4, 6, 8]
```

---

## Node.js & Backend

### 14. How do you handle streams and buffers in Node.js?
**Answer:**
**Stream Processing:**
```javascript
const fs = require('fs');
const { Transform, pipeline } = require('stream');
const { promisify } = require('util');

// Transform stream
class UpperCaseTransform extends Transform {
    _transform(chunk, encoding, callback) {
        this.push(chunk.toString().toUpperCase());
        callback();
    }
}

// Pipeline with error handling
const pipelineAsync = promisify(pipeline);

async function processFile(inputPath, outputPath) {
    try {
        await pipelineAsync(
            fs.createReadStream(inputPath),
            new UpperCaseTransform(),
            fs.createWriteStream(outputPath)
        );
        console.log('File processed successfully');
    } catch (error) {
        console.error('Pipeline error:', error);
    }
}

// Readable stream from array
const { Readable } = require('stream');

class ArrayReadable extends Readable {
    constructor(array) {
        super({ objectMode: true });
        this.array = array;
        this.index = 0;
    }
    
    _read() {
        if (this.index < this.array.length) {
            this.push(this.array[this.index++]);
        } else {
            this.push(null); // End of stream
        }
    }
}

// Buffer operations
function processBuffer(data) {
    const buffer = Buffer.from(data, 'utf8');
    
    // Buffer manipulation
    const slice = buffer.slice(0, 10);
    const concatenated = Buffer.concat([buffer, Buffer.from(' - processed')]);
    
    return {
        original: buffer.toString(),
        slice: slice.toString(),
        concatenated: concatenated.toString()
    };
}
```

### 15. How do you implement middleware and error handling in Express?
**Answer:**
**Middleware Implementation:**
```javascript
const express = require('express');
const app = express();

// Logging middleware
const logger = (req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`${req.method} ${req.url} - ${res.statusCode} - ${duration}ms`);
    });
    
    next();
};

// Authentication middleware
const authenticate = async (req, res, next) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: 'No token provided' });
        }
        
        const user = await verifyToken(token);
        req.user = user;
        next();
    } catch (error) {
        res.status(401).json({ error: 'Invalid token' });
    }
};

// Rate limiting middleware
const rateLimit = (windowMs, maxRequests) => {
    const requests = new Map();
    
    return (req, res, next) => {
        const key = req.ip;
        const now = Date.now();
        const windowStart = now - windowMs;
        
        if (!requests.has(key)) {
            requests.set(key, []);
        }
        
        const userRequests = requests.get(key);
        const validRequests = userRequests.filter(time => time > windowStart);
        
        if (validRequests.length >= maxRequests) {
            return res.status(429).json({ error: 'Too many requests' });
        }
        
        validRequests.push(now);
        requests.set(key, validRequests);
        next();
    };
};

// Error handling middleware
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    
    if (err.name === 'ValidationError') {
        return res.status(400).json({
            error: 'Validation Error',
            details: err.message
        });
    }
    
    if (err.name === 'CastError') {
        return res.status(400).json({
            error: 'Invalid ID format'
        });
    }
    
    res.status(500).json({
        error: 'Internal Server Error',
        message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
    });
};

// Apply middleware
app.use(logger);
app.use(express.json());
app.use('/api', rateLimit(15 * 60 * 1000, 100)); // 100 requests per 15 minutes

// Protected routes
app.use('/api/protected', authenticate);

// Error handling (must be last)
app.use(errorHandler);
```

---

## Testing & Debugging

### 16. How do you implement comprehensive testing strategies?
**Answer:**
**Unit Testing with Jest:**
```javascript
// mathUtils.js
export const add = (a, b) => a + b;
export const divide = (a, b) => {
    if (b === 0) throw new Error('Division by zero');
    return a / b;
};

// mathUtils.test.js
import { add, divide } from './mathUtils';

describe('Math Utils', () => {
    describe('add', () => {
        test('should add two positive numbers', () => {
            expect(add(2, 3)).toBe(5);
        });
        
        test('should handle negative numbers', () => {
            expect(add(-1, 1)).toBe(0);
        });
    });
    
    describe('divide', () => {
        test('should divide two numbers', () => {
            expect(divide(10, 2)).toBe(5);
        });
        
        test('should throw error for division by zero', () => {
            expect(() => divide(10, 0)).toThrow('Division by zero');
        });
    });
});

// Async testing
describe('API Service', () => {
    test('should fetch user data', async () => {
        const mockFetch = jest.fn().mockResolvedValue({
            json: () => Promise.resolve({ id: 1, name: 'John' })
        });
        global.fetch = mockFetch;
        
        const user = await fetchUser(1);
        
        expect(mockFetch).toHaveBeenCalledWith('/api/users/1');
        expect(user).toEqual({ id: 1, name: 'John' });
    });
});
```

**Integration Testing:**
```javascript
// API integration test
const request = require('supertest');
const app = require('../app');

describe('User API', () => {
    let server;
    
    beforeAll(() => {
        server = app.listen(0);
    });
    
    afterAll(() => {
        server.close();
    });
    
    test('POST /users should create a user', async () => {
        const userData = {
            name: 'John Doe',
            email: 'john@example.com'
        };
        
        const response = await request(app)
            .post('/users')
            .send(userData)
            .expect(201);
        
        expect(response.body).toMatchObject(userData);
        expect(response.body.id).toBeDefined();
    });
    
    test('GET /users/:id should return user', async () => {
        const response = await request(app)
            .get('/users/1')
            .expect(200);
        
        expect(response.body).toHaveProperty('id', 1);
    });
});
```

**Mocking and Spies:**
```javascript
// Service with dependencies
class UserService {
    constructor(database, emailService) {
        this.database = database;
        this.emailService = emailService;
    }
    
    async createUser(userData) {
        const user = await this.database.save(userData);
        await this.emailService.sendWelcomeEmail(user.email);
        return user;
    }
}

// Test with mocks
describe('UserService', () => {
    let userService;
    let mockDatabase;
    let mockEmailService;
    
    beforeEach(() => {
        mockDatabase = {
            save: jest.fn()
        };
        mockEmailService = {
            sendWelcomeEmail: jest.fn()
        };
        userService = new UserService(mockDatabase, mockEmailService);
    });
    
    test('should create user and send welcome email', async () => {
        const userData = { name: 'John', email: 'john@example.com' };
        const savedUser = { id: 1, ...userData };
        
        mockDatabase.save.mockResolvedValue(savedUser);
        mockEmailService.sendWelcomeEmail.mockResolvedValue();
        
        const result = await userService.createUser(userData);
        
        expect(mockDatabase.save).toHaveBeenCalledWith(userData);
        expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(userData.email);
        expect(result).toEqual(savedUser);
    });
});
```

---

*This comprehensive guide covers 16+ advanced JavaScript interview questions with detailed answers and practical examples for senior JavaScript developer interviews.*