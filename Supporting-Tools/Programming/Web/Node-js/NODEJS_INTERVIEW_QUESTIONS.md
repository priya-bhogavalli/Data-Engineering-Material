# Node.js Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Asynchronous Programming (16-25)](#asynchronous-programming-16-25)
3. [Data Processing & APIs (26-35)](#data-processing--apis-26-35)
4. [Performance & Scalability (36-45)](#performance--scalability-36-45)
5. [Database Integration (46-55)](#database-integration-46-55)
6. [Real-time Data & Streaming (56-65)](#real-time-data--streaming-56-65)
7. [Testing & Deployment (66-75)](#testing--deployment-66-75)

---

## 🎯 **Introduction**

Node.js is crucial for data engineers building APIs, real-time data processing systems, and microservices. This guide covers Node.js concepts specifically relevant to data engineering workflows.

**Why Node.js for Data Engineering:**
- **High Performance I/O**: Non-blocking operations for data pipelines
- **Real-time Processing**: WebSockets and streaming capabilities
- **API Development**: RESTful and GraphQL APIs for data services
- **Microservices**: Scalable data processing services
- **Integration**: Easy integration with databases and cloud services

---

## Core Concepts Questions (1-15)

### 1. What is the Event Loop in Node.js and why is it important for data processing?
**Answer**: The Event Loop is Node.js's core mechanism for handling asynchronous operations, crucial for data processing applications.

**Event Loop Phases:**
1. **Timer Phase**: Executes setTimeout() and setInterval() callbacks
2. **Pending Callbacks**: Executes I/O callbacks deferred to next loop iteration
3. **Idle, Prepare**: Internal use only
4. **Poll Phase**: Fetches new I/O events; executes I/O callbacks
5. **Check Phase**: Executes setImmediate() callbacks
6. **Close Callbacks**: Executes close event callbacks

```javascript
// Data processing example using Event Loop
const fs = require('fs');
const path = require('path');

async function processDataFiles(directory) {
    console.log('1. Starting file processing');
    
    // Non-blocking file operations
    const files = await fs.promises.readdir(directory);
    
    console.log('2. Files read, processing...');
    
    const results = await Promise.all(
        files.map(async (file) => {
            const data = await fs.promises.readFile(path.join(directory, file), 'utf8');
            return processData(data);
        })
    );
    
    console.log('3. All files processed');
    return results;
}

function processData(data) {
    // CPU-intensive operation
    return data.split('\n').filter(line => line.includes('ERROR')).length;
}
```

### 2. Explain the difference between process.nextTick() and setImmediate().
**Answer**: Both schedule callbacks but at different phases of the Event Loop.

```javascript
// Execution order demonstration
console.log('Start');

setImmediate(() => console.log('setImmediate'));
process.nextTick(() => console.log('nextTick'));

setTimeout(() => console.log('setTimeout'), 0);

console.log('End');

// Output:
// Start
// End
// nextTick
// setTimeout
// setImmediate
```

**Key Differences:**
- **process.nextTick()**: Executes before any other asynchronous operation
- **setImmediate()**: Executes in the Check phase of Event Loop
- **Use Cases**: nextTick for error handling, setImmediate for breaking up CPU-intensive tasks

### 3. How do you handle memory management in Node.js data processing applications?
**Answer**: Memory management strategies for data-intensive applications:

```javascript
// Memory monitoring and management
const v8 = require('v8');
const process = require('process');

class MemoryManager {
    static getMemoryUsage() {
        const usage = process.memoryUsage();
        const heapStats = v8.getHeapStatistics();
        
        return {
            rss: Math.round(usage.rss / 1024 / 1024) + ' MB',
            heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + ' MB',
            heapTotal: Math.round(usage.heapTotal / 1024 / 1024) + ' MB',
            external: Math.round(usage.external / 1024 / 1024) + ' MB',
            heapLimit: Math.round(heapStats.heap_size_limit / 1024 / 1024) + ' MB'
        };
    }
    
    static forceGarbageCollection() {
        if (global.gc) {
            global.gc();
        }
    }
    
    static monitorMemory(threshold = 500) {
        setInterval(() => {
            const usage = process.memoryUsage();
            const heapUsedMB = usage.heapUsed / 1024 / 1024;
            
            if (heapUsedMB > threshold) {
                console.warn(`High memory usage: ${heapUsedMB.toFixed(2)} MB`);
                this.forceGarbageCollection();
            }
        }, 10000);
    }
}

// Stream processing to avoid memory issues
const fs = require('fs');
const readline = require('readline');

async function processLargeFile(filePath) {
    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });
    
    let lineCount = 0;
    for await (const line of rl) {
        // Process line by line to avoid loading entire file
        processLine(line);
        lineCount++;
        
        if (lineCount % 10000 === 0) {
            console.log(`Processed ${lineCount} lines`);
        }
    }
}
```

### 4. What are Streams in Node.js and how are they used for data processing?
**Answer**: Streams are objects that handle reading/writing data piece by piece, essential for processing large datasets.

```javascript
const fs = require('fs');
const { Transform, pipeline } = require('stream');
const csv = require('csv-parser');

// Custom Transform stream for data processing
class DataProcessor extends Transform {
    constructor(options) {
        super({ objectMode: true });
        this.processedCount = 0;
    }
    
    _transform(chunk, encoding, callback) {
        try {
            // Process each data chunk
            const processed = this.processRecord(chunk);
            this.processedCount++;
            
            if (this.processedCount % 1000 === 0) {
                console.log(`Processed ${this.processedCount} records`);
            }
            
            callback(null, processed);
        } catch (error) {
            callback(error);
        }
    }
    
    processRecord(record) {
        // Data transformation logic
        return {
            ...record,
            timestamp: new Date().toISOString(),
            processed: true
        };
    }
}

// Pipeline for CSV processing
async function processCsvFile(inputPath, outputPath) {
    return new Promise((resolve, reject) => {
        pipeline(
            fs.createReadStream(inputPath),
            csv(),
            new DataProcessor(),
            fs.createWriteStream(outputPath),
            (error) => {
                if (error) reject(error);
                else resolve();
            }
        );
    });
}
```

### 5. How do you implement error handling in Node.js data pipelines?
**Answer**: Comprehensive error handling strategies:

```javascript
const EventEmitter = require('events');

class DataPipeline extends EventEmitter {
    constructor() {
        super();
        this.errors = [];
        this.setupErrorHandling();
    }
    
    setupErrorHandling() {
        // Global error handlers
        process.on('uncaughtException', (error) => {
            console.error('Uncaught Exception:', error);
            this.handleCriticalError(error);
        });
        
        process.on('unhandledRejection', (reason, promise) => {
            console.error('Unhandled Rejection at:', promise, 'reason:', reason);
            this.handleCriticalError(reason);
        });
    }
    
    async processWithRetry(operation, maxRetries = 3, delay = 1000) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                return await operation();
            } catch (error) {
                console.warn(`Attempt ${attempt} failed:`, error.message);
                
                if (attempt === maxRetries) {
                    this.logError(error);
                    throw error;
                }
                
                await this.sleep(delay * attempt);
            }
        }
    }
    
    async safeAsyncOperation(operation, fallback = null) {
        try {
            return await operation();
        } catch (error) {
            this.logError(error);
            this.emit('error', error);
            return fallback;
        }
    }
    
    logError(error) {
        const errorInfo = {
            message: error.message,
            stack: error.stack,
            timestamp: new Date().toISOString(),
            type: error.constructor.name
        };
        
        this.errors.push(errorInfo);
        console.error('Pipeline Error:', errorInfo);
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    handleCriticalError(error) {
        // Graceful shutdown
        console.error('Critical error, shutting down...');
        process.exit(1);
    }
}
```

---

## Asynchronous Programming (16-25)

### 16. Compare callbacks, Promises, and async/await for data processing tasks.
**Answer**: Evolution of asynchronous patterns in Node.js:

```javascript
// 1. Callback Pattern (Callback Hell)
function processDataCallback(data, callback) {
    validateData(data, (err, validData) => {
        if (err) return callback(err);
        
        transformData(validData, (err, transformedData) => {
            if (err) return callback(err);
            
            saveData(transformedData, (err, result) => {
                if (err) return callback(err);
                callback(null, result);
            });
        });
    });
}

// 2. Promise Pattern
function processDataPromise(data) {
    return validateDataPromise(data)
        .then(validData => transformDataPromise(validData))
        .then(transformedData => saveDataPromise(transformedData))
        .catch(error => {
            console.error('Processing failed:', error);
            throw error;
        });
}

// 3. Async/Await Pattern (Recommended)
async function processDataAsync(data) {
    try {
        const validData = await validateDataPromise(data);
        const transformedData = await transformDataPromise(validData);
        const result = await saveDataPromise(transformedData);
        return result;
    } catch (error) {
        console.error('Processing failed:', error);
        throw error;
    }
}

// Parallel processing with async/await
async function processBatchData(dataArray) {
    try {
        // Process all items in parallel
        const results = await Promise.all(
            dataArray.map(data => processDataAsync(data))
        );
        return results;
    } catch (error) {
        console.error('Batch processing failed:', error);
        throw error;
    }
}
```

### 17. How do you implement rate limiting for API calls in data ingestion?
**Answer**: Rate limiting strategies for external API integration:

```javascript
class RateLimiter {
    constructor(maxRequests, timeWindow) {
        this.maxRequests = maxRequests;
        this.timeWindow = timeWindow;
        this.requests = [];
    }
    
    async throttle() {
        const now = Date.now();
        
        // Remove old requests outside time window
        this.requests = this.requests.filter(
            timestamp => now - timestamp < this.timeWindow
        );
        
        if (this.requests.length >= this.maxRequests) {
            const oldestRequest = Math.min(...this.requests);
            const waitTime = this.timeWindow - (now - oldestRequest);
            await this.sleep(waitTime);
            return this.throttle();
        }
        
        this.requests.push(now);
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Data ingestion with rate limiting
class DataIngestionService {
    constructor() {
        this.rateLimiter = new RateLimiter(100, 60000); // 100 requests per minute
        this.queue = [];
        this.processing = false;
    }
    
    async ingestData(apiEndpoints) {
        for (const endpoint of apiEndpoints) {
            this.queue.push(endpoint);
        }
        
        if (!this.processing) {
            this.processQueue();
        }
    }
    
    async processQueue() {
        this.processing = true;
        
        while (this.queue.length > 0) {
            const endpoint = this.queue.shift();
            
            try {
                await this.rateLimiter.throttle();
                const data = await this.fetchData(endpoint);
                await this.processData(data);
            } catch (error) {
                console.error(`Failed to process ${endpoint}:`, error);
                // Optionally re-queue failed requests
                this.queue.push(endpoint);
            }
        }
        
        this.processing = false;
    }
    
    async fetchData(endpoint) {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    }
}
```

---

## Data Processing & APIs (26-35)

### 26. How do you build RESTful APIs for data services in Node.js?
**Answer**: Building scalable data APIs with Express.js:

```javascript
const express = require('express');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const compression = require('compression');

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
        
        // Compression
        this.app.use(compression());
        
        // Rate limiting
        const limiter = rateLimit({
            windowMs: 15 * 60 * 1000, // 15 minutes
            max: 100 // limit each IP to 100 requests per windowMs
        });
        this.app.use('/api/', limiter);
        
        // Body parsing
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ extended: true }));
    }
    
    setupRoutes() {
        // Data retrieval endpoints
        this.app.get('/api/data/:dataset', this.getDataset.bind(this));
        this.app.get('/api/data/:dataset/aggregate', this.getAggregatedData.bind(this));
        
        // Data ingestion endpoints
        this.app.post('/api/data/:dataset', this.ingestData.bind(this));
        this.app.put('/api/data/:dataset/batch', this.batchIngest.bind(this));
        
        // Analytics endpoints
        this.app.get('/api/analytics/:dataset/summary', this.getDataSummary.bind(this));
        this.app.get('/api/analytics/:dataset/trends', this.getTrends.bind(this));
    }
    
    async getDataset(req, res) {
        try {
            const { dataset } = req.params;
            const { page = 1, limit = 100, filter } = req.query;
            
            const data = await this.dataService.getData(dataset, {
                page: parseInt(page),
                limit: parseInt(limit),
                filter: filter ? JSON.parse(filter) : {}
            });
            
            res.json({
                success: true,
                data: data.records,
                pagination: {
                    page: data.page,
                    limit: data.limit,
                    total: data.total,
                    pages: Math.ceil(data.total / data.limit)
                }
            });
        } catch (error) {
            this.handleError(res, error);
        }
    }
    
    async getAggregatedData(req, res) {
        try {
            const { dataset } = req.params;
            const { groupBy, aggregation, timeRange } = req.query;
            
            const result = await this.dataService.aggregate(dataset, {
                groupBy: groupBy ? groupBy.split(',') : [],
                aggregation: aggregation || 'count',
                timeRange: timeRange ? JSON.parse(timeRange) : null
            });
            
            res.json({
                success: true,
                data: result,
                metadata: {
                    groupBy,
                    aggregation,
                    generatedAt: new Date().toISOString()
                }
            });
        } catch (error) {
            this.handleError(res, error);
        }
    }
    
    async ingestData(req, res) {
        try {
            const { dataset } = req.params;
            const data = req.body;
            
            // Validate data
            const validationResult = await this.validateData(data);
            if (!validationResult.valid) {
                return res.status(400).json({
                    success: false,
                    error: 'Validation failed',
                    details: validationResult.errors
                });
            }
            
            // Process and store data
            const result = await this.dataService.ingest(dataset, data);
            
            res.status(201).json({
                success: true,
                message: 'Data ingested successfully',
                recordsProcessed: result.count,
                id: result.id
            });
        } catch (error) {
            this.handleError(res, error);
        }
    }
    
    setupErrorHandling() {
        this.app.use((error, req, res, next) => {
            console.error('API Error:', error);
            
            res.status(error.status || 500).json({
                success: false,
                error: error.message || 'Internal server error',
                timestamp: new Date().toISOString()
            });
        });
    }
    
    handleError(res, error) {
        const status = error.status || 500;
        res.status(status).json({
            success: false,
            error: error.message,
            timestamp: new Date().toISOString()
        });
    }
}
```

### 27. How do you implement data validation and sanitization in Node.js?
**Answer**: Comprehensive data validation framework:

```javascript
const Joi = require('joi');
const validator = require('validator');

class DataValidator {
    constructor() {
        this.schemas = new Map();
        this.setupSchemas();
    }
    
    setupSchemas() {
        // User data schema
        this.schemas.set('user', Joi.object({
            id: Joi.string().uuid().required(),
            email: Joi.string().email().required(),
            name: Joi.string().min(2).max(100).required(),
            age: Joi.number().integer().min(0).max(150),
            createdAt: Joi.date().iso(),
            metadata: Joi.object().unknown(true)
        }));
        
        // Transaction data schema
        this.schemas.set('transaction', Joi.object({
            transactionId: Joi.string().required(),
            userId: Joi.string().uuid().required(),
            amount: Joi.number().positive().precision(2).required(),
            currency: Joi.string().length(3).uppercase().required(),
            timestamp: Joi.date().iso().required(),
            category: Joi.string().valid('food', 'transport', 'entertainment', 'other')
        }));
    }
    
    validate(data, schemaName) {
        const schema = this.schemas.get(schemaName);
        if (!schema) {
            throw new Error(`Schema '${schemaName}' not found`);
        }
        
        const { error, value } = schema.validate(data, {
            abortEarly: false,
            stripUnknown: true
        });
        
        if (error) {
            return {
                valid: false,
                errors: error.details.map(detail => ({
                    field: detail.path.join('.'),
                    message: detail.message,
                    value: detail.context.value
                }))
            };
        }
        
        return { valid: true, data: value };
    }
    
    sanitizeString(str) {
        if (typeof str !== 'string') return str;
        
        return validator.escape(
            validator.trim(str)
        );
    }
    
    sanitizeObject(obj) {
        const sanitized = {};
        
        for (const [key, value] of Object.entries(obj)) {
            if (typeof value === 'string') {
                sanitized[key] = this.sanitizeString(value);
            } else if (typeof value === 'object' && value !== null) {
                sanitized[key] = this.sanitizeObject(value);
            } else {
                sanitized[key] = value;
            }
        }
        
        return sanitized;
    }
    
    validateAndSanitize(data, schemaName) {
        // First sanitize
        const sanitized = this.sanitizeObject(data);
        
        // Then validate
        return this.validate(sanitized, schemaName);
    }
}

// Usage in data processing pipeline
class DataProcessor {
    constructor() {
        this.validator = new DataValidator();
        this.processedCount = 0;
        this.errorCount = 0;
    }
    
    async processBatch(records, schemaName) {
        const results = {
            processed: [],
            errors: []
        };
        
        for (const record of records) {
            try {
                const validation = this.validator.validateAndSanitize(record, schemaName);
                
                if (validation.valid) {
                    const processed = await this.processRecord(validation.data);
                    results.processed.push(processed);
                    this.processedCount++;
                } else {
                    results.errors.push({
                        record,
                        errors: validation.errors
                    });
                    this.errorCount++;
                }
            } catch (error) {
                results.errors.push({
                    record,
                    error: error.message
                });
                this.errorCount++;
            }
        }
        
        return results;
    }
    
    async processRecord(record) {
        // Business logic processing
        return {
            ...record,
            processedAt: new Date().toISOString(),
            version: '1.0'
        };
    }
    
    getStats() {
        return {
            processed: this.processedCount,
            errors: this.errorCount,
            successRate: this.processedCount / (this.processedCount + this.errorCount) * 100
        };
    }
}
```

---

## Performance & Scalability (36-45)

### 36. How do you optimize Node.js applications for high-throughput data processing?
**Answer**: Performance optimization strategies:

```javascript
const cluster = require('cluster');
const os = require('os');
const { Worker } = require('worker_threads');

// 1. Cluster-based scaling
class ClusterManager {
    static start() {
        const numCPUs = os.cpus().length;
        
        if (cluster.isMaster) {
            console.log(`Master ${process.pid} is running`);
            
            // Fork workers
            for (let i = 0; i < numCPUs; i++) {
                cluster.fork();
            }
            
            cluster.on('exit', (worker, code, signal) => {
                console.log(`Worker ${worker.process.pid} died`);
                cluster.fork(); // Restart worker
            });
        } else {
            // Worker process
            const app = new DataProcessingApp();
            app.start();
            console.log(`Worker ${process.pid} started`);
        }
    }
}

// 2. Worker threads for CPU-intensive tasks
class WorkerPool {
    constructor(poolSize = os.cpus().length) {
        this.poolSize = poolSize;
        this.workers = [];
        this.queue = [];
        this.initializeWorkers();
    }
    
    initializeWorkers() {
        for (let i = 0; i < this.poolSize; i++) {
            const worker = new Worker('./cpu-intensive-worker.js');
            worker.on('message', this.handleWorkerMessage.bind(this));
            worker.on('error', this.handleWorkerError.bind(this));
            this.workers.push({ worker, busy: false });
        }
    }
    
    async processTask(data) {
        return new Promise((resolve, reject) => {
            const task = { data, resolve, reject };
            
            const availableWorker = this.workers.find(w => !w.busy);
            if (availableWorker) {
                this.assignTask(availableWorker, task);
            } else {
                this.queue.push(task);
            }
        });
    }
    
    assignTask(workerInfo, task) {
        workerInfo.busy = true;
        workerInfo.currentTask = task;
        workerInfo.worker.postMessage(task.data);
    }
    
    handleWorkerMessage(result) {
        const workerInfo = this.workers.find(w => w.worker === result.worker);
        if (workerInfo && workerInfo.currentTask) {
            workerInfo.currentTask.resolve(result.data);
            workerInfo.busy = false;
            workerInfo.currentTask = null;
            
            // Process next task in queue
            if (this.queue.length > 0) {
                const nextTask = this.queue.shift();
                this.assignTask(workerInfo, nextTask);
            }
        }
    }
}

// 3. Memory-efficient streaming
class OptimizedDataProcessor {
    constructor() {
        this.workerPool = new WorkerPool();
        this.batchSize = 1000;
        this.concurrency = 10;
    }
    
    async processLargeDataset(inputStream) {
        const results = [];
        let batch = [];
        let activeTasks = 0;
        
        return new Promise((resolve, reject) => {
            inputStream.on('data', async (chunk) => {
                batch.push(chunk);
                
                if (batch.length >= this.batchSize) {
                    const currentBatch = batch.splice(0, this.batchSize);
                    
                    if (activeTasks >= this.concurrency) {
                        inputStream.pause();
                    }
                    
                    activeTasks++;
                    this.processBatch(currentBatch)
                        .then(result => {
                            results.push(...result);
                            activeTasks--;
                            
                            if (activeTasks < this.concurrency) {
                                inputStream.resume();
                            }
                        })
                        .catch(reject);
                }
            });
            
            inputStream.on('end', async () => {
                if (batch.length > 0) {
                    const finalResult = await this.processBatch(batch);
                    results.push(...finalResult);
                }
                resolve(results);
            });
            
            inputStream.on('error', reject);
        });
    }
    
    async processBatch(batch) {
        const chunks = this.chunkArray(batch, Math.ceil(batch.length / this.workerPool.poolSize));
        const promises = chunks.map(chunk => this.workerPool.processTask(chunk));
        const results = await Promise.all(promises);
        return results.flat();
    }
    
    chunkArray(array, chunkSize) {
        const chunks = [];
        for (let i = 0; i < array.length; i += chunkSize) {
            chunks.push(array.slice(i, i + chunkSize));
        }
        return chunks;
    }
}

// 4. Connection pooling and caching
class DatabaseManager {
    constructor() {
        this.pool = new Pool({
            host: process.env.DB_HOST,
            port: process.env.DB_PORT,
            database: process.env.DB_NAME,
            user: process.env.DB_USER,
            password: process.env.DB_PASSWORD,
            max: 20, // Maximum connections
            idleTimeoutMillis: 30000,
            connectionTimeoutMillis: 2000
        });
        
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }
    
    async query(sql, params, useCache = false) {
        const cacheKey = useCache ? `${sql}:${JSON.stringify(params)}` : null;
        
        if (useCache && this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTimeout) {
                return cached.data;
            }
            this.cache.delete(cacheKey);
        }
        
        const client = await this.pool.connect();
        try {
            const result = await client.query(sql, params);
            
            if (useCache) {
                this.cache.set(cacheKey, {
                    data: result.rows,
                    timestamp: Date.now()
                });
            }
            
            return result.rows;
        } finally {
            client.release();
        }
    }
}
```

---

## Database Integration (46-55)

### 46. How do you integrate Node.js with different databases for data engineering?
**Answer**: Multi-database integration patterns:

```javascript
// Database abstraction layer
class DatabaseFactory {
    static create(type, config) {
        switch (type) {
            case 'postgresql':
                return new PostgreSQLAdapter(config);
            case 'mongodb':
                return new MongoDBAdapter(config);
            case 'redis':
                return new RedisAdapter(config);
            case 'elasticsearch':
                return new ElasticsearchAdapter(config);
            default:
                throw new Error(`Unsupported database type: ${type}`);
        }
    }
}

// PostgreSQL adapter
class PostgreSQLAdapter {
    constructor(config) {
        this.pool = new Pool(config);
    }
    
    async query(sql, params) {
        const client = await this.pool.connect();
        try {
            const result = await client.query(sql, params);
            return result.rows;
        } finally {
            client.release();
        }
    }
    
    async bulkInsert(table, records) {
        const client = await this.pool.connect();
        try {
            await client.query('BEGIN');
            
            const columns = Object.keys(records[0]);
            const values = records.map(record => 
                columns.map(col => record[col])
            );
            
            const placeholders = values.map((_, i) => 
                `(${columns.map((_, j) => `$${i * columns.length + j + 1}`).join(', ')})`
            ).join(', ');
            
            const sql = `INSERT INTO ${table} (${columns.join(', ')}) VALUES ${placeholders}`;
            await client.query(sql, values.flat());
            
            await client.query('COMMIT');
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        } finally {
            client.release();
        }
    }
}

// MongoDB adapter
class MongoDBAdapter {
    constructor(config) {
        this.client = new MongoClient(config.url);
        this.db = this.client.db(config.database);
    }
    
    async find(collection, query, options = {}) {
        return this.db.collection(collection).find(query, options).toArray();
    }
    
    async insertMany(collection, documents) {
        return this.db.collection(collection).insertMany(documents);
    }
    
    async aggregate(collection, pipeline) {
        return this.db.collection(collection).aggregate(pipeline).toArray();
    }
    
    async bulkWrite(collection, operations) {
        return this.db.collection(collection).bulkWrite(operations);
    }
}

// Data synchronization service
class DataSyncService {
    constructor() {
        this.postgres = DatabaseFactory.create('postgresql', pgConfig);
        this.mongodb = DatabaseFactory.create('mongodb', mongoConfig);
        this.redis = DatabaseFactory.create('redis', redisConfig);
    }
    
    async syncUserData() {
        try {
            // Get data from PostgreSQL
            const users = await this.postgres.query(
                'SELECT * FROM users WHERE updated_at > $1',
                [this.getLastSyncTime()]
            );
            
            if (users.length === 0) return;
            
            // Transform for MongoDB
            const mongoUsers = users.map(user => ({
                _id: user.id,
                profile: {
                    name: user.name,
                    email: user.email,
                    createdAt: user.created_at
                },
                metadata: {
                    lastSync: new Date(),
                    source: 'postgresql'
                }
            }));
            
            // Bulk upsert to MongoDB
            const bulkOps = mongoUsers.map(user => ({
                updateOne: {
                    filter: { _id: user._id },
                    update: { $set: user },
                    upsert: true
                }
            }));
            
            await this.mongodb.bulkWrite('users', bulkOps);
            
            // Cache frequently accessed data in Redis
            for (const user of users) {
                await this.redis.setex(
                    `user:${user.id}`,
                    3600, // 1 hour TTL
                    JSON.stringify(user)
                );
            }
            
            this.updateLastSyncTime();
            console.log(`Synced ${users.length} users`);
            
        } catch (error) {
            console.error('Sync failed:', error);
            throw error;
        }
    }
}
```

---

## Real-time Data & Streaming (56-65)

### 56. How do you implement real-time data processing with WebSockets?
**Answer**: Real-time data streaming architecture:

```javascript
const WebSocket = require('ws');
const EventEmitter = require('events');

class RealTimeDataProcessor extends EventEmitter {
    constructor() {
        super();
        this.clients = new Set();
        this.dataBuffer = [];
        this.bufferSize = 100;
        this.setupWebSocketServer();
        this.setupDataProcessing();
    }
    
    setupWebSocketServer() {
        this.wss = new WebSocket.Server({ port: 8080 });
        
        this.wss.on('connection', (ws, req) => {
            console.log('Client connected');
            this.clients.add(ws);
            
            // Send initial data
            ws.send(JSON.stringify({
                type: 'welcome',
                data: this.getRecentData()
            }));
            
            ws.on('message', (message) => {
                this.handleClientMessage(ws, message);
            });
            
            ws.on('close', () => {
                console.log('Client disconnected');
                this.clients.delete(ws);
            });
            
            ws.on('error', (error) => {
                console.error('WebSocket error:', error);
                this.clients.delete(ws);
            });
        });
    }
    
    setupDataProcessing() {
        // Simulate real-time data ingestion
        setInterval(() => {
            const data = this.generateSampleData();
            this.processRealTimeData(data);
        }, 1000);
        
        // Batch processing every 5 seconds
        setInterval(() => {
            if (this.dataBuffer.length > 0) {
                this.processBatch(this.dataBuffer.splice(0));
            }
        }, 5000);
    }
    
    processRealTimeData(data) {
        // Add to buffer
        this.dataBuffer.push(data);
        
        // Keep buffer size manageable
        if (this.dataBuffer.length > this.bufferSize) {
            this.dataBuffer.shift();
        }
        
        // Real-time analytics
        const analytics = this.calculateRealTimeMetrics(data);
        
        // Broadcast to all connected clients
        this.broadcast({
            type: 'realtime_data',
            data: data,
            analytics: analytics,
            timestamp: new Date().toISOString()
        });
        
        // Emit event for other services
        this.emit('data_received', data);
    }
    
    calculateRealTimeMetrics(data) {
        const recentData = this.dataBuffer.slice(-10);
        
        return {
            average: recentData.reduce((sum, item) => sum + item.value, 0) / recentData.length,
            trend: this.calculateTrend(recentData),
            anomaly: this.detectAnomaly(data, recentData)
        };
    }
    
    calculateTrend(data) {
        if (data.length < 2) return 'stable';
        
        const recent = data.slice(-3).map(d => d.value);
        const older = data.slice(-6, -3).map(d => d.value);
        
        const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
        const olderAvg = older.reduce((a, b) => a + b, 0) / older.length;
        
        const change = (recentAvg - olderAvg) / olderAvg * 100;
        
        if (change > 5) return 'increasing';
        if (change < -5) return 'decreasing';
        return 'stable';
    }
    
    detectAnomaly(current, historical) {
        const values = historical.map(d => d.value);
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
        const stdDev = Math.sqrt(variance);
        
        const zScore = Math.abs((current.value - mean) / stdDev);
        return zScore > 2; // Anomaly if z-score > 2
    }
    
    broadcast(message) {
        const data = JSON.stringify(message);
        
        this.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(data);
            }
        });
    }
    
    handleClientMessage(ws, message) {
        try {
            const parsed = JSON.parse(message);
            
            switch (parsed.type) {
                case 'subscribe':
                    this.handleSubscription(ws, parsed.channels);
                    break;
                case 'query':
                    this.handleQuery(ws, parsed.query);
                    break;
                default:
                    ws.send(JSON.stringify({
                        type: 'error',
                        message: 'Unknown message type'
                    }));
            }
        } catch (error) {
            ws.send(JSON.stringify({
                type: 'error',
                message: 'Invalid message format'
            }));
        }
    }
    
    generateSampleData() {
        return {
            id: Math.random().toString(36).substr(2, 9),
            value: Math.random() * 100,
            category: ['A', 'B', 'C'][Math.floor(Math.random() * 3)],
            timestamp: new Date().toISOString()
        };
    }
}

// Usage
const processor = new RealTimeDataProcessor();

processor.on('data_received', (data) => {
    // Additional processing or storage
    console.log('Processing data:', data.id);
});
```

---

## Testing & Deployment (66-75)

### 66. How do you implement comprehensive testing for Node.js data applications?
**Answer**: Testing strategies for data applications:

```javascript
// Test setup with Jest
const request = require('supertest');
const { MongoMemoryServer } = require('mongodb-memory-server');
const Redis = require('ioredis-mock');

describe('Data Processing API', () => {
    let app;
    let mongoServer;
    let redisClient;
    
    beforeAll(async () => {
        // Setup in-memory MongoDB
        mongoServer = await MongoMemoryServer.create();
        const mongoUri = mongoServer.getUri();
        
        // Setup mock Redis
        redisClient = new Redis();
        
        // Initialize app with test dependencies
        app = new DataAPI({
            mongodb: { uri: mongoUri },
            redis: redisClient
        });
    });
    
    afterAll(async () => {
        await mongoServer.stop();
        redisClient.disconnect();
    });
    
    describe('Data Ingestion', () => {
        test('should ingest valid data', async () => {
            const testData = {
                userId: 'test-user-123',
                events: [
                    { type: 'click', timestamp: '2023-01-01T00:00:00Z' },
                    { type: 'view', timestamp: '2023-01-01T00:01:00Z' }
                ]
            };
            
            const response = await request(app)
                .post('/api/data/events')
                .send(testData)
                .expect(201);
            
            expect(response.body.success).toBe(true);
            expect(response.body.recordsProcessed).toBe(2);
        });
        
        test('should reject invalid data', async () => {
            const invalidData = {
                userId: 'invalid',
                events: [
                    { type: 'invalid_type', timestamp: 'invalid_date' }
                ]
            };
            
            const response = await request(app)
                .post('/api/data/events')
                .send(invalidData)
                .expect(400);
            
            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('Validation failed');
        });
    });
    
    describe('Data Processing', () => {
        test('should process batch data correctly', async () => {
            const processor = new DataProcessor();
            const testRecords = [
                { id: 1, value: 10, category: 'A' },
                { id: 2, value: 20, category: 'B' },
                { id: 3, value: 30, category: 'A' }
            ];
            
            const result = await processor.processBatch(testRecords, 'test');
            
            expect(result.processed).toHaveLength(3);
            expect(result.errors).toHaveLength(0);
            
            // Verify transformations
            result.processed.forEach(record => {
                expect(record).toHaveProperty('processedAt');
                expect(record).toHaveProperty('version', '1.0');
            });
        });
        
        test('should handle processing errors gracefully', async () => {
            const processor = new DataProcessor();
            const invalidRecords = [
                { id: 1, value: 'invalid_number', category: 'A' }
            ];
            
            const result = await processor.processBatch(invalidRecords, 'test');
            
            expect(result.processed).toHaveLength(0);
            expect(result.errors).toHaveLength(1);
            expect(result.errors[0]).toHaveProperty('errors');
        });
    });
    
    describe('Performance Tests', () => {
        test('should handle high throughput', async () => {
            const startTime = Date.now();
            const promises = [];
            
            // Simulate 100 concurrent requests
            for (let i = 0; i < 100; i++) {
                const promise = request(app)
                    .get('/api/data/test')
                    .query({ page: 1, limit: 10 });
                promises.push(promise);
            }
            
            const responses = await Promise.all(promises);
            const endTime = Date.now();
            
            // All requests should succeed
            responses.forEach(response => {
                expect(response.status).toBe(200);
            });
            
            // Should complete within reasonable time
            expect(endTime - startTime).toBeLessThan(5000);
        });
        
        test('should handle memory efficiently', async () => {
            const initialMemory = process.memoryUsage().heapUsed;
            
            // Process large dataset
            const largeDataset = Array.from({ length: 10000 }, (_, i) => ({
                id: i,
                data: `test_data_${i}`.repeat(100)
            }));
            
            const processor = new DataProcessor();
            await processor.processBatch(largeDataset, 'test');
            
            // Force garbage collection
            if (global.gc) global.gc();
            
            const finalMemory = process.memoryUsage().heapUsed;
            const memoryIncrease = finalMemory - initialMemory;
            
            // Memory increase should be reasonable
            expect(memoryIncrease).toBeLessThan(100 * 1024 * 1024); // 100MB
        });
    });
});

// Integration tests
describe('Database Integration', () => {
    let dbManager;
    
    beforeEach(async () => {
        dbManager = new DatabaseManager();
        await dbManager.migrate(); // Run migrations
    });
    
    afterEach(async () => {
        await dbManager.cleanup(); // Clean test data
    });
    
    test('should sync data between databases', async () => {
        const syncService = new DataSyncService();
        
        // Insert test data in PostgreSQL
        await dbManager.postgres.query(
            'INSERT INTO users (id, name, email) VALUES ($1, $2, $3)',
            ['test-123', 'Test User', 'test@example.com']
        );
        
        // Run sync
        await syncService.syncUserData();
        
        // Verify data in MongoDB
        const mongoUser = await dbManager.mongodb.find('users', { _id: 'test-123' });
        expect(mongoUser).toHaveLength(1);
        expect(mongoUser[0].profile.name).toBe('Test User');
        
        // Verify cache in Redis
        const cachedUser = await dbManager.redis.get('user:test-123');
        expect(JSON.parse(cachedUser).name).toBe('Test User');
    });
});
```

### 67. How do you deploy Node.js data applications for production?
**Answer**: Production deployment strategies:

```javascript
// Docker configuration
// Dockerfile
/*
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Change ownership
RUN chown -R nodejs:nodejs /app
USER nodejs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

CMD ["node", "server.js"]
*/

// Production server configuration
class ProductionServer {
    constructor() {
        this.app = express();
        this.setupMiddleware();
        this.setupRoutes();
        this.setupErrorHandling();
        this.setupGracefulShutdown();
    }
    
    setupMiddleware() {
        // Security headers
        this.app.use(helmet({
            contentSecurityPolicy: {
                directives: {
                    defaultSrc: ["'self'"],
                    styleSrc: ["'self'", "'unsafe-inline'"],
                    scriptSrc: ["'self'"],
                    imgSrc: ["'self'", "data:", "https:"]
                }
            }
        }));
        
        // Request logging
        this.app.use(morgan('combined', {
            stream: fs.createWriteStream('./logs/access.log', { flags: 'a' })
        }));
        
        // Rate limiting
        this.app.use(rateLimit({
            windowMs: 15 * 60 * 1000,
            max: 100,
            message: 'Too many requests from this IP'
        }));
        
        // Request size limits
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.urlencoded({ limit: '10mb', extended: true }));
        
        // Compression
        this.app.use(compression());
    }
    
    setupErrorHandling() {
        // Global error handler
        this.app.use((error, req, res, next) => {
            const errorId = uuidv4();
            
            // Log error with correlation ID
            logger.error('Request error', {
                errorId,
                error: error.message,
                stack: error.stack,
                url: req.url,
                method: req.method,
                ip: req.ip,
                userAgent: req.get('User-Agent')
            });
            
            // Don't expose internal errors in production
            const message = process.env.NODE_ENV === 'production' 
                ? 'Internal server error' 
                : error.message;
            
            res.status(error.status || 500).json({
                success: false,
                error: message,
                errorId: errorId
            });
        });
        
        // Handle uncaught exceptions
        process.on('uncaughtException', (error) => {
            logger.fatal('Uncaught exception', { error: error.message, stack: error.stack });
            this.gracefulShutdown();
        });
        
        process.on('unhandledRejection', (reason, promise) => {
            logger.fatal('Unhandled rejection', { reason, promise });
            this.gracefulShutdown();
        });
    }
    
    setupGracefulShutdown() {
        const signals = ['SIGTERM', 'SIGINT'];
        
        signals.forEach(signal => {
            process.on(signal, () => {
                logger.info(`Received ${signal}, starting graceful shutdown`);
                this.gracefulShutdown();
            });
        });
    }
    
    async gracefulShutdown() {
        try {
            // Stop accepting new requests
            this.server.close(() => {
                logger.info('HTTP server closed');
            });
            
            // Close database connections
            await this.closeConnections();
            
            // Wait for ongoing requests to complete
            await this.waitForRequests();
            
            logger.info('Graceful shutdown completed');
            process.exit(0);
        } catch (error) {
            logger.error('Error during shutdown', { error: error.message });
            process.exit(1);
        }
    }
    
    start() {
        const port = process.env.PORT || 3000;
        this.server = this.app.listen(port, () => {
            logger.info(`Server started on port ${port}`);
        });
    }
}

// Health check endpoint
class HealthCheck {
    constructor(dependencies) {
        this.dependencies = dependencies;
    }
    
    async check() {
        const results = {
            status: 'healthy',
            timestamp: new Date().toISOString(),
            uptime: process.uptime(),
            memory: process.memoryUsage(),
            dependencies: {}
        };
        
        // Check database connections
        for (const [name, db] of Object.entries(this.dependencies)) {
            try {
                await db.ping();
                results.dependencies[name] = { status: 'healthy' };
            } catch (error) {
                results.dependencies[name] = { 
                    status: 'unhealthy', 
                    error: error.message 
                };
                results.status = 'unhealthy';
            }
        }
        
        return results;
    }
}

// Monitoring and metrics
class MetricsCollector {
    constructor() {
        this.metrics = {
            requests: 0,
            errors: 0,
            responseTime: [],
            memoryUsage: []
        };
        
        this.startCollection();
    }
    
    startCollection() {
        // Collect metrics every minute
        setInterval(() => {
            this.collectSystemMetrics();
        }, 60000);
    }
    
    collectSystemMetrics() {
        const usage = process.memoryUsage();
        this.metrics.memoryUsage.push({
            timestamp: Date.now(),
            heapUsed: usage.heapUsed,
            heapTotal: usage.heapTotal,
            external: usage.external
        });
        
        // Keep only last 100 measurements
        if (this.metrics.memoryUsage.length > 100) {
            this.metrics.memoryUsage.shift();
        }
    }
    
    recordRequest(responseTime) {
        this.metrics.requests++;
        this.metrics.responseTime.push(responseTime);
        
        if (this.metrics.responseTime.length > 1000) {
            this.metrics.responseTime.shift();
        }
    }
    
    recordError() {
        this.metrics.errors++;
    }
    
    getMetrics() {
        const avgResponseTime = this.metrics.responseTime.length > 0
            ? this.metrics.responseTime.reduce((a, b) => a + b, 0) / this.metrics.responseTime.length
            : 0;
        
        return {
            ...this.metrics,
            averageResponseTime: avgResponseTime,
            errorRate: this.metrics.errors / this.metrics.requests * 100
        };
    }
}
```

---

## 📚 **Node.js Study Guide & Best Practices**

### 🎯 **Essential Node.js Concepts for Data Engineers**

#### **Core Architecture Understanding**
1. **Event Loop**: Non-blocking I/O operations
2. **Streams**: Efficient data processing for large datasets
3. **Clustering**: Multi-process scaling
4. **Worker Threads**: CPU-intensive task handling
5. **Memory Management**: Garbage collection and optimization

#### **Data Processing Patterns**
1. **ETL Pipelines**: Extract, transform, load workflows
2. **Real-time Processing**: WebSocket and streaming data
3. **Batch Processing**: Efficient bulk data operations
4. **API Development**: RESTful and GraphQL services
5. **Database Integration**: Multi-database connectivity

### 🚀 **Production Best Practices**

#### **Performance Optimization**
- Use clustering for CPU-bound tasks
- Implement connection pooling
- Cache frequently accessed data
- Stream large datasets
- Monitor memory usage

#### **Security Considerations**
- Input validation and sanitization
- Rate limiting and DDoS protection
- Secure headers with Helmet.js
- Environment variable management
- Authentication and authorization

#### **Monitoring & Debugging**
- Structured logging
- Health check endpoints
- Performance metrics collection
- Error tracking and alerting
- Graceful shutdown handling

### 📈 **Interview Preparation Strategy**

#### **Technical Depth Levels**
1. **Basic**: Event loop, callbacks, basic API development
2. **Intermediate**: Streams, error handling, database integration
3. **Advanced**: Performance optimization, clustering, real-time processing
4. **Expert**: Architecture design, scalability, production deployment

#### **Common Interview Categories**
1. **Fundamentals** (30%): Event loop, asynchronous programming
2. **Data Processing** (25%): Streams, batch processing, ETL
3. **Performance** (20%): Optimization, scaling, memory management
4. **Integration** (25%): Databases, APIs, real-time systems

---

**Remember**: Node.js excels in I/O-intensive data engineering tasks. Focus on understanding asynchronous patterns, streaming data processing, and building scalable APIs for data services.