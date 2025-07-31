# JavaScript Key Concepts

## 1. JavaScript Fundamentals
**What is JavaScript**: High-level, interpreted programming language for web development and server-side applications.

**Key Features**:
- **Dynamic typing**: Variables can hold different types
- **First-class functions**: Functions are values
- **Prototype-based OOP**: Object inheritance through prototypes
- **Event-driven**: Asynchronous programming model
- **Interpreted**: No compilation step required

```javascript
// Variable declarations
let name = "Data Engineer";
const PI = 3.14159;
var age = 30; // Function-scoped (avoid in modern JS)

// Data types
let number = 42;
let string = "Hello World";
let boolean = true;
let array = [1, 2, 3, 4, 5];
let object = { name: "John", role: "Engineer" };
let nullValue = null;
let undefinedValue = undefined;
```

## 2. Functions and Scope
```javascript
// Function declaration
function processData(data) {
    return data.map(item => item * 2);
}

// Function expression
const analyzeData = function(dataset) {
    return dataset.reduce((sum, val) => sum + val, 0);
};

// Arrow functions
const filterData = (data, threshold) => data.filter(x => x > threshold);

// Higher-order functions
const transformData = (data, transformer) => data.map(transformer);

// Closures
function createCounter() {
    let count = 0;
    return function() {
        return ++count;
    };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2

// IIFE (Immediately Invoked Function Expression)
(function() {
    const privateVar = "Hidden";
    // Code here runs immediately
})();
```

## 3. Objects and Prototypes
```javascript
// Object creation
const dataEngineer = {
    name: "Alice",
    skills: ["Python", "SQL", "Spark"],
    experience: 5,
    
    // Method
    introduce() {
        return `Hi, I'm ${this.name}, a data engineer with ${this.experience} years experience`;
    },
    
    // Getter
    get skillCount() {
        return this.skills.length;
    },
    
    // Setter
    set addSkill(skill) {
        this.skills.push(skill);
    }
};

// Constructor function
function DataPipeline(name, source, destination) {
    this.name = name;
    this.source = source;
    this.destination = destination;
    this.isRunning = false;
}

DataPipeline.prototype.start = function() {
    this.isRunning = true;
    console.log(`${this.name} pipeline started`);
};

// ES6 Classes
class ETLPipeline {
    constructor(name, config) {
        this.name = name;
        this.config = config;
        this.status = 'idle';
    }
    
    async extract() {
        console.log('Extracting data...');
        // Extraction logic
    }
    
    transform(data) {
        return data.map(record => ({
            ...record,
            processed_at: new Date().toISOString()
        }));
    }
    
    async load(data) {
        console.log('Loading data...');
        // Loading logic
    }
    
    static createFromConfig(config) {
        return new ETLPipeline(config.name, config);
    }
}
```

## 4. Asynchronous Programming
```javascript
// Callbacks
function fetchData(callback) {
    setTimeout(() => {
        const data = { records: 1000, status: 'success' };
        callback(null, data);
    }, 1000);
}

fetchData((error, data) => {
    if (error) {
        console.error('Error:', error);
    } else {
        console.log('Data:', data);
    }
});

// Promises
function fetchDataPromise() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const success = Math.random() > 0.5;
            if (success) {
                resolve({ records: 1000, status: 'success' });
            } else {
                reject(new Error('Failed to fetch data'));
            }
        }, 1000);
    });
}

fetchDataPromise()
    .then(data => console.log('Success:', data))
    .catch(error => console.error('Error:', error))
    .finally(() => console.log('Operation completed'));

// Async/Await
async function processDataPipeline() {
    try {
        const rawData = await fetchDataPromise();
        const transformedData = await transformData(rawData);
        const result = await saveData(transformedData);
        return result;
    } catch (error) {
        console.error('Pipeline failed:', error);
        throw error;
    }
}

// Promise.all for parallel execution
async function processMultipleSources() {
    const sources = ['db1', 'db2', 'api'];
    const promises = sources.map(source => fetchFromSource(source));
    
    try {
        const results = await Promise.all(promises);
        return results;
    } catch (error) {
        console.error('One or more sources failed:', error);
    }
}
```

## 5. Array Methods and Data Manipulation
```javascript
const salesData = [
    { id: 1, product: 'Laptop', amount: 1200, date: '2024-01-15' },
    { id: 2, product: 'Phone', amount: 800, date: '2024-01-16' },
    { id: 3, product: 'Tablet', amount: 600, date: '2024-01-17' }
];

// Map - transform each element
const amounts = salesData.map(sale => sale.amount);
const enrichedData = salesData.map(sale => ({
    ...sale,
    category: sale.amount > 1000 ? 'high-value' : 'standard'
}));

// Filter - select elements based on condition
const highValueSales = salesData.filter(sale => sale.amount > 1000);
const recentSales = salesData.filter(sale => new Date(sale.date) > new Date('2024-01-16'));

// Reduce - aggregate data
const totalRevenue = salesData.reduce((sum, sale) => sum + sale.amount, 0);
const salesByProduct = salesData.reduce((acc, sale) => {
    acc[sale.product] = (acc[sale.product] || 0) + sale.amount;
    return acc;
}, {});

// Find and includes
const laptopSale = salesData.find(sale => sale.product === 'Laptop');
const hasHighValue = salesData.some(sale => sale.amount > 1000);
const allPositive = salesData.every(sale => sale.amount > 0);

// Sort
const sortedByAmount = [...salesData].sort((a, b) => b.amount - a.amount);
const sortedByDate = [...salesData].sort((a, b) => new Date(a.date) - new Date(b.date));

// Advanced array operations
const flatData = [[1, 2], [3, 4], [5, 6]].flat();
const uniqueProducts = [...new Set(salesData.map(sale => sale.product))];
```

## 6. Error Handling
```javascript
// Try-catch blocks
function parseJSON(jsonString) {
    try {
        return JSON.parse(jsonString);
    } catch (error) {
        console.error('Invalid JSON:', error.message);
        return null;
    }
}

// Custom errors
class DataValidationError extends Error {
    constructor(message, field) {
        super(message);
        this.name = 'DataValidationError';
        this.field = field;
    }
}

function validateData(data) {
    if (!data.id) {
        throw new DataValidationError('ID is required', 'id');
    }
    if (!data.amount || data.amount <= 0) {
        throw new DataValidationError('Amount must be positive', 'amount');
    }
}

// Error handling with async/await
async function safeDataProcessing(data) {
    try {
        validateData(data);
        const result = await processData(data);
        return { success: true, data: result };
    } catch (error) {
        if (error instanceof DataValidationError) {
            return { success: false, error: `Validation failed: ${error.message}` };
        }
        return { success: false, error: 'Processing failed' };
    }
}

// Global error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
```

## 7. Modules and Imports
```javascript
// ES6 Modules - export
// dataUtils.js
export const API_BASE_URL = 'https://api.example.com';

export function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

export class DataProcessor {
    constructor(config) {
        this.config = config;
    }
    
    process(data) {
        return data.map(this.transform.bind(this));
    }
    
    transform(record) {
        return {
            ...record,
            processed: true,
            timestamp: Date.now()
        };
    }
}

export default class DatabaseConnection {
    constructor(connectionString) {
        this.connectionString = connectionString;
    }
    
    async connect() {
        // Connection logic
    }
}

// ES6 Modules - import
// main.js
import DatabaseConnection, { DataProcessor, formatCurrency, API_BASE_URL } from './dataUtils.js';
import * as utils from './dataUtils.js';

// Dynamic imports
async function loadModule() {
    const { DataProcessor } = await import('./dataUtils.js');
    return new DataProcessor();
}

// CommonJS (Node.js)
// module.exports = { DataProcessor, formatCurrency };
// const { DataProcessor } = require('./dataUtils');
```

## 8. DOM Manipulation and Events
```javascript
// DOM selection
const button = document.getElementById('processBtn');
const dataTable = document.querySelector('.data-table');
const rows = document.querySelectorAll('tr');

// DOM manipulation
function createDataRow(data) {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${data.id}</td>
        <td>${data.name}</td>
        <td>${formatCurrency(data.amount)}</td>
    `;
    return row;
}

function updateTable(data) {
    const tbody = dataTable.querySelector('tbody');
    tbody.innerHTML = ''; // Clear existing rows
    
    data.forEach(item => {
        const row = createDataRow(item);
        tbody.appendChild(row);
    });
}

// Event handling
button.addEventListener('click', async (event) => {
    event.preventDefault();
    
    try {
        button.disabled = true;
        button.textContent = 'Processing...';
        
        const data = await fetchData();
        updateTable(data);
        
        // Show success message
        showNotification('Data processed successfully', 'success');
    } catch (error) {
        showNotification('Processing failed', 'error');
    } finally {
        button.disabled = false;
        button.textContent = 'Process Data';
    }
});

// Event delegation
dataTable.addEventListener('click', (event) => {
    if (event.target.classList.contains('delete-btn')) {
        const row = event.target.closest('tr');
        const id = row.dataset.id;
        deleteRecord(id);
    }
});
```

## 9. Modern JavaScript Features
```javascript
// Destructuring
const user = { name: 'John', age: 30, role: 'Engineer' };
const { name, age, role } = user;
const { name: userName, ...rest } = user;

const numbers = [1, 2, 3, 4, 5];
const [first, second, ...remaining] = numbers;

// Spread operator
const newUser = { ...user, department: 'Data' };
const allNumbers = [...numbers, 6, 7, 8];

// Template literals
const message = `Hello ${name}, you are ${age} years old`;
const query = `
    SELECT *
    FROM users
    WHERE role = '${role}'
    AND age > ${age}
`;

// Optional chaining
const userCity = user?.address?.city ?? 'Unknown';
const firstPhone = user?.phones?.[0];

// Nullish coalescing
const displayName = user.displayName ?? user.name ?? 'Anonymous';

// Object shorthand
const createUser = (name, age) => ({ name, age, active: true });

// Computed property names
const dynamicKey = 'role';
const userObj = {
    name: 'John',
    [dynamicKey]: 'Engineer',
    [`${dynamicKey}Level`]: 'Senior'
};

// Array.from and Set
const uniqueValues = Array.from(new Set([1, 2, 2, 3, 3, 4]));
const range = Array.from({ length: 5 }, (_, i) => i + 1); // [1, 2, 3, 4, 5]
```

## 10. Performance and Best Practices
```javascript
// Debouncing
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

const debouncedSearch = debounce((query) => {
    // Perform search
    console.log('Searching for:', query);
}, 300);

// Throttling
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

const expensiveCalculation = memoize((n) => {
    console.log('Calculating...');
    return n * n * n;
});

// Memory management
function processLargeDataset(data) {
    // Process in chunks to avoid memory issues
    const chunkSize = 1000;
    const results = [];
    
    for (let i = 0; i < data.length; i += chunkSize) {
        const chunk = data.slice(i, i + chunkSize);
        const processed = chunk.map(processItem);
        results.push(...processed);
        
        // Allow garbage collection
        if (i % 10000 === 0) {
            await new Promise(resolve => setTimeout(resolve, 0));
        }
    }
    
    return results;
}

// Performance monitoring
function measurePerformance(fn, name) {
    return function(...args) {
        const start = performance.now();
        const result = fn.apply(this, args);
        const end = performance.now();
        console.log(`${name} took ${end - start} milliseconds`);
        return result;
    };
}

const optimizedFunction = measurePerformance(expensiveOperation, 'Data Processing');
```