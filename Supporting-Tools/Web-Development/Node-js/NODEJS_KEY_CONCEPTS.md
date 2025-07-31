# Node.js Key Concepts

## 1. Node.js Fundamentals
**What is Node.js**: JavaScript runtime built on Chrome's V8 engine for server-side development.

**Key Features**:
- **Event-driven**: Non-blocking I/O operations
- **Single-threaded**: Event loop with worker threads
- **NPM**: Package manager with extensive ecosystem
- **Cross-platform**: Runs on multiple operating systems
- **Fast execution**: V8 JavaScript engine

```javascript
// Basic Node.js server
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
        method: req.method,
        path: parsedUrl.pathname,
        query: parsedUrl.query,
        timestamp: new Date().toISOString()
    }));
});

server.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

## 2. Express.js Framework
```javascript
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // CORS support
app.use(express.json({ limit: '10mb' })); // JSON parsing
app.use(express.urlencoded({ extended: true })); // URL encoding

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Routes
app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Data processing endpoint
app.post('/api/data/process', async (req, res) => {
    try {
        const { data, options } = req.body;
        
        // Validate input
        if (!data || !Array.isArray(data)) {
            return res.status(400).json({
                error: 'Invalid data format. Expected array.'
            });
        }
        
        // Process data
        const processedData = await processDataAsync(data, options);
        
        res.json({
            success: true,
            processed_count: processedData.length,
            data: processedData
        });
        
    } catch (error) {
        console.error('Data processing error:', error);
        res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
});

// Error handling middleware
app.use((error, req, res, next) => {
    console.error('Unhandled error:', error);
    res.status(500).json({
        error: 'Internal server error',
        timestamp: new Date().toISOString()
    });
});

async function processDataAsync(data, options = {}) {
    return data.map(item => ({
        ...item,
        processed: true,
        timestamp: new Date().toISOString(),
        ...options
    }));
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

## 3. Asynchronous Programming
```javascript
const fs = require('fs').promises;
const path = require('path');
const { promisify } = require('util');
const { pipeline } = require('stream');
const pipelineAsync = promisify(pipeline);

// Promises and async/await
async function readDataFiles(directory) {
    try {
        const files = await fs.readdir(directory);
        const dataFiles = files.filter(file => file.endsWith('.json'));
        
        const results = await Promise.all(
            dataFiles.map(async (file) => {
                const filePath = path.join(directory, file);
                const content = await fs.readFile(filePath, 'utf8');
                return {
                    filename: file,
                    data: JSON.parse(content)
                };
            })
        );
        
        return results;
    } catch (error) {
        console.error('Error reading data files:', error);
        throw error;
    }
}

// Event-driven processing
const EventEmitter = require('events');

class DataProcessor extends EventEmitter {
    constructor() {
        super();
        this.queue = [];
        this.processing = false;
    }
    
    addData(data) {
        this.queue.push(data);
        this.emit('dataAdded', data);
        
        if (!this.processing) {
            this.processQueue();
        }
    }
    
    async processQueue() {
        this.processing = true;
        this.emit('processingStarted');
        
        while (this.queue.length > 0) {
            const data = this.queue.shift();
            
            try {
                const result = await this.processItem(data);
                this.emit('itemProcessed', result);
            } catch (error) {
                this.emit('processingError', error, data);
            }
        }
        
        this.processing = false;
        this.emit('processingCompleted');
    }
    
    async processItem(data) {
        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 100));
        return { ...data, processed: true };
    }
}

// Usage
const processor = new DataProcessor();

processor.on('dataAdded', (data) => {
    console.log('Data added to queue:', data.id);
});

processor.on('itemProcessed', (result) => {
    console.log('Item processed:', result.id);
});

processor.on('processingError', (error, data) => {
    console.error('Processing error for item', data.id, ':', error.message);
});

// Worker threads for CPU-intensive tasks
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

if (isMainThread) {
    // Main thread
    async function processLargeDataset(data) {
        const numWorkers = require('os').cpus().length;
        const chunkSize = Math.ceil(data.length / numWorkers);
        
        const workers = [];
        const promises = [];
        
        for (let i = 0; i < numWorkers; i++) {
            const start = i * chunkSize;
            const end = Math.min(start + chunkSize, data.length);
            const chunk = data.slice(start, end);
            
            if (chunk.length > 0) {
                const worker = new Worker(__filename, {
                    workerData: { chunk }
                });
                
                workers.push(worker);
                promises.push(new Promise((resolve, reject) => {
                    worker.on('message', resolve);
                    worker.on('error', reject);
                }));
            }
        }
        
        const results = await Promise.all(promises);
        
        // Cleanup workers
        workers.forEach(worker => worker.terminate());
        
        return results.flat();
    }
} else {
    // Worker thread
    const { chunk } = workerData;
    
    // CPU-intensive processing
    const processedChunk = chunk.map(item => {
        // Complex calculations
        let result = 0;
        for (let i = 0; i < 1000000; i++) {
            result += Math.sqrt(item.value * i);
        }
        
        return {
            ...item,
            processed_value: result
        };
    });
    
    parentPort.postMessage(processedChunk);
}
```

## 4. Database Integration
```javascript
// PostgreSQL with pg library
const { Pool } = require('pg');

class DatabaseService {
    constructor(config) {
        this.pool = new Pool({
            host: config.host,
            port: config.port,
            database: config.database,
            user: config.user,
            password: config.password,
            max: 20, // Maximum number of clients
            idleTimeoutMillis: 30000,
            connectionTimeoutMillis: 2000,
        });
        
        this.pool.on('error', (err) => {
            console.error('Database pool error:', err);
        });
    }
    
    async query(text, params) {
        const client = await this.pool.connect();
        try {
            const result = await client.query(text, params);
            return result;
        } finally {
            client.release();
        }
    }
    
    async transaction(queries) {
        const client = await this.pool.connect();
        try {
            await client.query('BEGIN');
            
            const results = [];
            for (const { text, params } of queries) {
                const result = await client.query(text, params);
                results.push(result);
            }
            
            await client.query('COMMIT');
            return results;
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        } finally {
            client.release();
        }
    }
    
    async bulkInsert(tableName, columns, data) {
        const client = await this.pool.connect();
        try {
            const placeholders = columns.map((_, i) => `$${i + 1}`).join(', ');
            const query = `INSERT INTO ${tableName} (${columns.join(', ')}) VALUES (${placeholders})`;
            
            await client.query('BEGIN');
            
            for (const row of data) {
                await client.query(query, row);
            }
            
            await client.query('COMMIT');
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        } finally {
            client.release();
        }
    }
    
    async close() {
        await this.pool.end();
    }
}

// MongoDB with mongoose
const mongoose = require('mongoose');

// Schema definition
const salesSchema = new mongoose.Schema({
    customerId: { type: String, required: true, index: true },
    productId: { type: String, required: true },
    amount: { type: Number, required: true, min: 0 },
    saleDate: { type: Date, default: Date.now, index: true },
    metadata: { type: mongoose.Schema.Types.Mixed }
}, {
    timestamps: true
});

// Indexes
salesSchema.index({ customerId: 1, saleDate: -1 });
salesSchema.index({ saleDate: 1, amount: -1 });

const Sale = mongoose.model('Sale', salesSchema);

class MongoService {
    async connect(connectionString) {
        await mongoose.connect(connectionString, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
            maxPoolSize: 10,
            serverSelectionTimeoutMS: 5000,
            socketTimeoutMS: 45000,
        });
        
        console.log('Connected to MongoDB');
    }
    
    async createSale(saleData) {
        const sale = new Sale(saleData);
        return await sale.save();
    }
    
    async getSalesByCustomer(customerId, limit = 100) {
        return await Sale.find({ customerId })
            .sort({ saleDate: -1 })
            .limit(limit)
            .lean();
    }
    
    async aggregateSales(pipeline) {
        return await Sale.aggregate(pipeline);
    }
    
    async bulkWrite(operations) {
        return await Sale.bulkWrite(operations);
    }
}
```

## 5. File Processing and Streams
```javascript
const fs = require('fs');
const csv = require('csv-parser');
const { Transform, Writable } = require('stream');
const zlib = require('zlib');

// CSV processing with streams
function processCsvFile(inputPath, outputPath) {
    return new Promise((resolve, reject) => {
        const results = [];
        let processedCount = 0;
        
        const transformStream = new Transform({
            objectMode: true,
            transform(chunk, encoding, callback) {
                try {
                    // Data transformation
                    const transformed = {
                        ...chunk,
                        amount: parseFloat(chunk.amount) || 0,
                        processed_at: new Date().toISOString(),
                        valid: chunk.amount && chunk.customer_id
                    };
                    
                    processedCount++;
                    
                    if (processedCount % 1000 === 0) {
                        console.log(`Processed ${processedCount} records`);
                    }
                    
                    callback(null, transformed);
                } catch (error) {
                    callback(error);
                }
            }
        });
        
        const writeStream = fs.createWriteStream(outputPath);
        
        fs.createReadStream(inputPath)
            .pipe(csv())
            .pipe(transformStream)
            .pipe(new Writable({
                objectMode: true,
                write(chunk, encoding, callback) {
                    writeStream.write(JSON.stringify(chunk) + '\n');
                    callback();
                }
            }))
            .on('finish', () => {
                writeStream.end();
                resolve(processedCount);
            })
            .on('error', reject);
    });
}

// Large file processing with backpressure handling
async function processLargeFile(inputPath, processor) {
    const readStream = fs.createReadStream(inputPath, { highWaterMark: 64 * 1024 });
    
    return new Promise((resolve, reject) => {
        let lineBuffer = '';
        let lineCount = 0;
        
        readStream.on('data', (chunk) => {
            lineBuffer += chunk.toString();
            const lines = lineBuffer.split('\n');
            lineBuffer = lines.pop(); // Keep incomplete line
            
            for (const line of lines) {
                if (line.trim()) {
                    try {
                        processor(line, lineCount++);
                    } catch (error) {
                        console.error(`Error processing line ${lineCount}:`, error);
                    }
                }
            }
        });
        
        readStream.on('end', () => {
            if (lineBuffer.trim()) {
                processor(lineBuffer, lineCount++);
            }
            resolve(lineCount);
        });
        
        readStream.on('error', reject);
    });
}

// Compressed file handling
function processGzipFile(inputPath, outputPath) {
    return pipelineAsync(
        fs.createReadStream(inputPath),
        zlib.createGunzip(),
        new Transform({
            transform(chunk, encoding, callback) {
                // Process decompressed data
                const processed = chunk.toString().toUpperCase();
                callback(null, processed);
            }
        }),
        zlib.createGzip(),
        fs.createWriteStream(outputPath)
    );
}
```

## 6. API Development
```javascript
const express = require('express');
const { body, param, validationResult } = require('express-validator');
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');

const app = express();

// Authentication middleware
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
        return res.status(401).json({ error: 'Access token required' });
    }
    
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Invalid token' });
        }
        req.user = user;
        next();
    });
}

// Validation middleware
const validateSalesData = [
    body('customer_id').notEmpty().withMessage('Customer ID is required'),
    body('amount').isFloat({ min: 0 }).withMessage('Amount must be a positive number'),
    body('product_id').notEmpty().withMessage('Product ID is required'),
    body('sale_date').optional().isISO8601().withMessage('Invalid date format')
];

// Rate limiting for different endpoints
const createLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 10, // limit each IP to 10 requests per windowMs
    message: 'Too many create requests, please try again later'
});

const queryLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: 'Too many query requests, please try again later'
});

// API Routes
app.post('/api/sales', 
    createLimiter,
    authenticateToken,
    validateSalesData,
    async (req, res) => {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({
                    error: 'Validation failed',
                    details: errors.array()
                });
            }
            
            const saleData = {
                ...req.body,
                created_by: req.user.id,
                created_at: new Date()
            };
            
            const result = await createSale(saleData);
            
            res.status(201).json({
                success: true,
                data: result,
                message: 'Sale created successfully'
            });
            
        } catch (error) {
            console.error('Error creating sale:', error);
            res.status(500).json({
                error: 'Internal server error',
                message: error.message
            });
        }
    }
);

app.get('/api/sales/:customerId',
    queryLimiter,
    authenticateToken,
    param('customerId').notEmpty().withMessage('Customer ID is required'),
    async (req, res) => {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({
                    error: 'Validation failed',
                    details: errors.array()
                });
            }
            
            const { customerId } = req.params;
            const { limit = 50, offset = 0, startDate, endDate } = req.query;
            
            const filters = { customer_id: customerId };
            if (startDate || endDate) {
                filters.sale_date = {};
                if (startDate) filters.sale_date.$gte = new Date(startDate);
                if (endDate) filters.sale_date.$lte = new Date(endDate);
            }
            
            const sales = await getSales(filters, {
                limit: parseInt(limit),
                offset: parseInt(offset)
            });
            
            res.json({
                success: true,
                data: sales,
                pagination: {
                    limit: parseInt(limit),
                    offset: parseInt(offset),
                    total: sales.length
                }
            });
            
        } catch (error) {
            console.error('Error fetching sales:', error);
            res.status(500).json({
                error: 'Internal server error',
                message: error.message
            });
        }
    }
);

// Bulk operations endpoint
app.post('/api/sales/bulk',
    authenticateToken,
    body('sales').isArray().withMessage('Sales must be an array'),
    body('sales.*.customer_id').notEmpty(),
    body('sales.*.amount').isFloat({ min: 0 }),
    async (req, res) => {
        try {
            const errors = validationResult(req);
            if (!errors.isEmpty()) {
                return res.status(400).json({
                    error: 'Validation failed',
                    details: errors.array()
                });
            }
            
            const { sales } = req.body;
            
            if (sales.length > 1000) {
                return res.status(400).json({
                    error: 'Batch size too large',
                    message: 'Maximum 1000 records per batch'
                });
            }
            
            const results = await bulkCreateSales(sales, req.user.id);
            
            res.json({
                success: true,
                data: results,
                message: `${results.length} sales created successfully`
            });
            
        } catch (error) {
            console.error('Error in bulk create:', error);
            res.status(500).json({
                error: 'Internal server error',
                message: error.message
            });
        }
    }
);
```

## 7. Testing
```javascript
const request = require('supertest');
const app = require('../app');
const { expect } = require('chai');
const sinon = require('sinon');

describe('Sales API', () => {
    let authToken;
    
    beforeEach(async () => {
        // Setup test data
        authToken = generateTestToken();
    });
    
    afterEach(() => {
        // Cleanup
        sinon.restore();
    });
    
    describe('POST /api/sales', () => {
        it('should create a new sale with valid data', async () => {
            const saleData = {
                customer_id: 'CUST001',
                product_id: 'PROD001',
                amount: 99.99
            };
            
            const response = await request(app)
                .post('/api/sales')
                .set('Authorization', `Bearer ${authToken}`)
                .send(saleData)
                .expect(201);
            
            expect(response.body.success).to.be.true;
            expect(response.body.data).to.have.property('id');
            expect(response.body.data.amount).to.equal(99.99);
        });
        
        it('should return validation error for invalid data', async () => {
            const invalidData = {
                customer_id: '',
                amount: -10
            };
            
            const response = await request(app)
                .post('/api/sales')
                .set('Authorization', `Bearer ${authToken}`)
                .send(invalidData)
                .expect(400);
            
            expect(response.body.error).to.equal('Validation failed');
            expect(response.body.details).to.be.an('array');
        });
        
        it('should return 401 without authentication', async () => {
            const saleData = {
                customer_id: 'CUST001',
                amount: 99.99
            };
            
            await request(app)
                .post('/api/sales')
                .send(saleData)
                .expect(401);
        });
    });
    
    describe('GET /api/sales/:customerId', () => {
        it('should return sales for valid customer', async () => {
            const customerId = 'CUST001';
            
            // Mock database response
            const mockSales = [
                { id: 1, customer_id: customerId, amount: 99.99 },
                { id: 2, customer_id: customerId, amount: 149.99 }
            ];
            
            sinon.stub(require('../services/salesService'), 'getSales')
                .resolves(mockSales);
            
            const response = await request(app)
                .get(`/api/sales/${customerId}`)
                .set('Authorization', `Bearer ${authToken}`)
                .expect(200);
            
            expect(response.body.success).to.be.true;
            expect(response.body.data).to.have.length(2);
        });
    });
});

// Unit tests for business logic
describe('Sales Service', () => {
    const salesService = require('../services/salesService');
    
    describe('calculateTotal', () => {
        it('should calculate total correctly', () => {
            const sales = [
                { amount: 100 },
                { amount: 200 },
                { amount: 50 }
            ];
            
            const total = salesService.calculateTotal(sales);
            expect(total).to.equal(350);
        });
        
        it('should handle empty array', () => {
            const total = salesService.calculateTotal([]);
            expect(total).to.equal(0);
        });
    });
});

// Integration tests
describe('Database Integration', () => {
    let db;
    
    before(async () => {
        db = await setupTestDatabase();
    });
    
    after(async () => {
        await cleanupTestDatabase(db);
    });
    
    it('should save and retrieve sales data', async () => {
        const saleData = {
            customer_id: 'TEST001',
            amount: 99.99,
            product_id: 'PROD001'
        };
        
        const savedSale = await db.sales.create(saleData);
        expect(savedSale.id).to.exist;
        
        const retrievedSale = await db.sales.findById(savedSale.id);
        expect(retrievedSale.amount).to.equal(99.99);
    });
});

function generateTestToken() {
    return jwt.sign(
        { id: 'test-user', role: 'admin' },
        process.env.JWT_SECRET || 'test-secret',
        { expiresIn: '1h' }
    );
}
```

## 8. Performance and Optimization
```javascript
// Caching with Redis
const redis = require('redis');
const client = redis.createClient({
    host: process.env.REDIS_HOST || 'localhost',
    port: process.env.REDIS_PORT || 6379,
    retry_strategy: (options) => {
        if (options.error && options.error.code === 'ECONNREFUSED') {
            return new Error('Redis server connection refused');
        }
        if (options.total_retry_time > 1000 * 60 * 60) {
            return new Error('Retry time exhausted');
        }
        return Math.min(options.attempt * 100, 3000);
    }
});

class CacheService {
    async get(key) {
        try {
            const value = await client.get(key);
            return value ? JSON.parse(value) : null;
        } catch (error) {
            console.error('Cache get error:', error);
            return null;
        }
    }
    
    async set(key, value, ttl = 3600) {
        try {
            await client.setex(key, ttl, JSON.stringify(value));
        } catch (error) {
            console.error('Cache set error:', error);
        }
    }
    
    async del(key) {
        try {
            await client.del(key);
        } catch (error) {
            console.error('Cache delete error:', error);
        }
    }
}

// Memory optimization
function optimizeMemoryUsage() {
    // Use streams for large data processing
    const processLargeDataset = (inputStream, outputStream) => {
        return new Promise((resolve, reject) => {
            const batchSize = 1000;
            let batch = [];
            let processedCount = 0;
            
            inputStream
                .on('data', (chunk) => {
                    batch.push(chunk);
                    
                    if (batch.length >= batchSize) {
                        processBatch(batch);
                        batch = []; // Clear batch to free memory
                    }
                })
                .on('end', () => {
                    if (batch.length > 0) {
                        processBatch(batch);
                    }
                    resolve(processedCount);
                })
                .on('error', reject);
            
            function processBatch(items) {
                const processed = items.map(item => ({
                    ...item,
                    processed: true
                }));
                
                processed.forEach(item => {
                    outputStream.write(JSON.stringify(item) + '\n');
                });
                
                processedCount += processed.length;
            }
        });
    };
    
    // Object pooling for frequently created objects
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
    
    // Usage example
    const bufferPool = new ObjectPool(
        () => Buffer.alloc(1024),
        (buffer) => buffer.fill(0),
        50
    );
}

// Clustering for CPU-intensive tasks
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

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
    const app = require('./app');
    const PORT = process.env.PORT || 3000;
    
    app.listen(PORT, () => {
        console.log(`Worker ${process.pid} started on port ${PORT}`);
    });
}
```

## 9. Security Best Practices
```javascript
const bcrypt = require('bcrypt');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const validator = require('validator');

// Password hashing
class AuthService {
    async hashPassword(password) {
        const saltRounds = 12;
        return await bcrypt.hash(password, saltRounds);
    }
    
    async verifyPassword(password, hash) {
        return await bcrypt.compare(password, hash);
    }
    
    generateSecureToken() {
        return require('crypto').randomBytes(32).toString('hex');
    }
}

// Input validation and sanitization
function validateAndSanitizeInput(req, res, next) {
    const { email, name, amount } = req.body;
    
    // Validate email
    if (email && !validator.isEmail(email)) {
        return res.status(400).json({
            error: 'Invalid email format'
        });
    }
    
    // Sanitize string inputs
    if (name) {
        req.body.name = validator.escape(name.trim());
    }
    
    // Validate numeric inputs
    if (amount !== undefined) {
        if (!validator.isFloat(amount.toString(), { min: 0 })) {
            return res.status(400).json({
                error: 'Amount must be a positive number'
            });
        }
        req.body.amount = parseFloat(amount);
    }
    
    next();
}

// Security middleware setup
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            scriptSrc: ["'self'"],
            imgSrc: ["'self'", "data:", "https:"]
        }
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    }
}));

// Advanced rate limiting
const createAdvancedLimiter = (options) => {
    return rateLimit({
        windowMs: options.windowMs,
        max: options.max,
        keyGenerator: (req) => {
            // Use user ID if authenticated, otherwise IP
            return req.user ? req.user.id : req.ip;
        },
        handler: (req, res) => {
            res.status(429).json({
                error: 'Too many requests',
                retryAfter: Math.round(options.windowMs / 1000)
            });
        },
        standardHeaders: true,
        legacyHeaders: false
    });
};

// SQL injection prevention
class SecureDatabase {
    constructor(pool) {
        this.pool = pool;
    }
    
    async query(text, params = []) {
        // Always use parameterized queries
        const client = await this.pool.connect();
        try {
            const result = await client.query(text, params);
            return result;
        } finally {
            client.release();
        }
    }
    
    // Safe dynamic query building
    buildWhereClause(filters) {
        const conditions = [];
        const values = [];
        let paramIndex = 1;
        
        for (const [field, value] of Object.entries(filters)) {
            // Whitelist allowed fields
            const allowedFields = ['customer_id', 'product_id', 'amount', 'sale_date'];
            if (!allowedFields.includes(field)) {
                continue;
            }
            
            conditions.push(`${field} = $${paramIndex}`);
            values.push(value);
            paramIndex++;
        }
        
        return {
            whereClause: conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '',
            values
        };
    }
}
```

## 10. Deployment and Production
```javascript
// Environment configuration
const config = {
    development: {
        port: 3000,
        database: {
            host: 'localhost',
            port: 5432,
            database: 'myapp_dev'
        },
        redis: {
            host: 'localhost',
            port: 6379
        },
        logLevel: 'debug'
    },
    production: {
        port: process.env.PORT || 8080,
        database: {
            host: process.env.DB_HOST,
            port: process.env.DB_PORT,
            database: process.env.DB_NAME,
            ssl: true
        },
        redis: {
            host: process.env.REDIS_HOST,
            port: process.env.REDIS_PORT,
            password: process.env.REDIS_PASSWORD
        },
        logLevel: 'info'
    }
};

const env = process.env.NODE_ENV || 'development';
module.exports = config[env];

// Graceful shutdown
process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

async function gracefulShutdown(signal) {
    console.log(`Received ${signal}. Starting graceful shutdown...`);
    
    // Stop accepting new requests
    server.close(async () => {
        console.log('HTTP server closed');
        
        try {
            // Close database connections
            await database.close();
            console.log('Database connections closed');
            
            // Close Redis connection
            await redis.quit();
            console.log('Redis connection closed');
            
            // Close other resources
            await cleanup();
            
            console.log('Graceful shutdown completed');
            process.exit(0);
        } catch (error) {
            console.error('Error during shutdown:', error);
            process.exit(1);
        }
    });
    
    // Force shutdown after timeout
    setTimeout(() => {
        console.error('Forced shutdown due to timeout');
        process.exit(1);
    }, 10000);
}

// Health check endpoint
app.get('/health', async (req, res) => {
    const health = {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        version: process.env.npm_package_version
    };
    
    try {
        // Check database connectivity
        await database.query('SELECT 1');
        health.database = 'connected';
        
        // Check Redis connectivity
        await redis.ping();
        health.redis = 'connected';
        
        res.json(health);
    } catch (error) {
        health.status = 'unhealthy';
        health.error = error.message;
        res.status(503).json(health);
    }
});

// Docker configuration
// Dockerfile
/*
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

USER node

EXPOSE 8080

CMD ["node", "server.js"]
*/

// docker-compose.yml
/*
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DB_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis
  
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
*/
```