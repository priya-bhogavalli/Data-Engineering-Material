# GraphQL Interview Questions for Data Engineers

## Basic Level Questions

### 1. What is GraphQL and how does it differ from REST APIs?
**Answer**: GraphQL is a query language and runtime for APIs that allows clients to request exactly the data they need. Key differences from REST:
- **Single Endpoint**: One URL for all operations vs multiple REST endpoints
- **Flexible Queries**: Clients specify exactly what data they need
- **Strong Type System**: Schema-first approach with type definitions
- **Real-time Subscriptions**: Built-in support for real-time data
- **No Over/Under-fetching**: Get exactly what you request

```graphql
# GraphQL Query Example
query GetUserOrders($userId: ID!) {
  user(id: $userId) {
    name
    email
    orders(limit: 10) {
      id
      total
      status
      items {
        product {
          name
          price
        }
        quantity
      }
    }
  }
}

# REST equivalent would require multiple requests:
# GET /users/123
# GET /users/123/orders
# GET /orders/456/items
# GET /products/789 (for each item)
```

### 2. Explain GraphQL schema and type system
**Answer**: GraphQL schema defines the structure and capabilities of an API:
- **Scalar Types**: Int, Float, String, Boolean, ID
- **Object Types**: Custom types with fields
- **Query Type**: Entry point for read operations
- **Mutation Type**: Entry point for write operations
- **Subscription Type**: Entry point for real-time updates

```graphql
# Schema Definition Language (SDL)
type User {
  id: ID!
  name: String!
  email: String!
  orders: [Order!]!
  createdAt: DateTime!
}

type Order {
  id: ID!
  user: User!
  items: [OrderItem!]!
  total: Float!
  status: OrderStatus!
  createdAt: DateTime!
}

type OrderItem {
  id: ID!
  product: Product!
  quantity: Int!
  price: Float!
}

type Product {
  id: ID!
  name: String!
  description: String
  price: Float!
  category: Category!
}

enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  order(id: ID!): Order
  orders(status: OrderStatus): [Order!]!
  products(category: String): [Product!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  createOrder(input: CreateOrderInput!): Order!
  updateOrderStatus(id: ID!, status: OrderStatus!): Order!
}

type Subscription {
  orderStatusChanged(userId: ID!): Order!
  newOrder: Order!
}
```

### 3. How do you implement GraphQL resolvers?
**Answer**: Resolvers are functions that fetch data for each field in the schema:

```javascript
// Node.js with Apollo Server
const resolvers = {
  Query: {
    user: async (parent, { id }, context) => {
      return await context.dataSources.userAPI.getUserById(id);
    },
    
    users: async (parent, { limit = 10, offset = 0 }, context) => {
      return await context.dataSources.userAPI.getUsers(limit, offset);
    },
    
    orders: async (parent, { status }, context) => {
      return await context.dataSources.orderAPI.getOrders({ status });
    }
  },
  
  Mutation: {
    createUser: async (parent, { input }, context) => {
      const user = await context.dataSources.userAPI.createUser(input);
      
      // Publish to subscription
      context.pubsub.publish('USER_CREATED', { userCreated: user });
      
      return user;
    },
    
    createOrder: async (parent, { input }, context) => {
      const order = await context.dataSources.orderAPI.createOrder(input);
      
      // Publish to subscription
      context.pubsub.publish('ORDER_CREATED', { newOrder: order });
      
      return order;
    }
  },
  
  Subscription: {
    newOrder: {
      subscribe: (parent, args, context) => {
        return context.pubsub.asyncIterator(['ORDER_CREATED']);
      }
    },
    
    orderStatusChanged: {
      subscribe: (parent, { userId }, context) => {
        return context.pubsub.asyncIterator([`ORDER_STATUS_${userId}`]);
      }
    }
  },
  
  // Field resolvers
  User: {
    orders: async (user, args, context) => {
      return await context.dataSources.orderAPI.getOrdersByUserId(user.id);
    }
  },
  
  Order: {
    user: async (order, args, context) => {
      return await context.dataSources.userAPI.getUserById(order.userId);
    },
    
    items: async (order, args, context) => {
      return await context.dataSources.orderAPI.getOrderItems(order.id);
    }
  },
  
  OrderItem: {
    product: async (item, args, context) => {
      return await context.dataSources.productAPI.getProductById(item.productId);
    }
  }
};
```

### 4. What are GraphQL data sources and how do you implement them?
**Answer**: Data sources provide a consistent API for fetching data from various backends:

```javascript
// RESTDataSource for external APIs
const { RESTDataSource } = require('apollo-datasource-rest');

class UserAPI extends RESTDataSource {
  constructor() {
    super();
    this.baseURL = 'https://api.users.com/';
  }
  
  willSendRequest(request) {
    request.headers.set('Authorization', this.context.token);
  }
  
  async getUserById(id) {
    const user = await this.get(`users/${id}`);
    return this.userReducer(user);
  }
  
  async getUsers(limit, offset) {
    const response = await this.get('users', {
      limit,
      offset
    });
    return response.users.map(user => this.userReducer(user));
  }
  
  async createUser(userData) {
    const response = await this.post('users', userData);
    return this.userReducer(response.user);
  }
  
  userReducer(user) {
    return {
      id: user.id,
      name: user.full_name,
      email: user.email_address,
      createdAt: user.created_at
    };
  }
}

// Database DataSource
const { DataSource } = require('apollo-datasource');

class OrderAPI extends DataSource {
  constructor({ store }) {
    super();
    this.store = store;
  }
  
  initialize(config) {
    this.context = config.context;
  }
  
  async getOrderById(id) {
    const order = await this.store.orders.findByPk(id);
    return order;
  }
  
  async getOrdersByUserId(userId) {
    const orders = await this.store.orders.findAll({
      where: { userId }
    });
    return orders;
  }
  
  async createOrder(orderData) {
    const order = await this.store.orders.create({
      ...orderData,
      userId: this.context.user.id
    });
    return order;
  }
  
  async getOrders(filters = {}) {
    const where = {};
    
    if (filters.status) {
      where.status = filters.status;
    }
    
    const orders = await this.store.orders.findAll({ where });
    return orders;
  }
}
```

### 5. How do you handle authentication and authorization in GraphQL?
**Answer**: Authentication and authorization strategies:

```javascript
// Authentication middleware
const jwt = require('jsonwebtoken');

const getUser = async (token) => {
  try {
    if (token) {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      const user = await User.findById(decoded.id);
      return user;
    }
    return null;
  } catch (error) {
    return null;
  }
};

// Apollo Server setup with auth context
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: async ({ req }) => {
    const token = req.headers.authorization || '';
    const user = await getUser(token.replace('Bearer ', ''));
    
    return {
      user,
      dataSources: {
        userAPI: new UserAPI(),
        orderAPI: new OrderAPI({ store })
      }
    };
  }
});

// Authorization in resolvers
const resolvers = {
  Query: {
    me: (parent, args, context) => {
      if (!context.user) {
        throw new AuthenticationError('You must be logged in');
      }
      return context.user;
    },
    
    adminUsers: (parent, args, context) => {
      if (!context.user || context.user.role !== 'ADMIN') {
        throw new ForbiddenError('Admin access required');
      }
      return context.dataSources.userAPI.getAllUsers();
    }
  },
  
  Mutation: {
    updateUser: async (parent, { id, input }, context) => {
      if (!context.user) {
        throw new AuthenticationError('You must be logged in');
      }
      
      // Users can only update their own profile
      if (context.user.id !== id && context.user.role !== 'ADMIN') {
        throw new ForbiddenError('You can only update your own profile');
      }
      
      return await context.dataSources.userAPI.updateUser(id, input);
    }
  }
};

// Schema-level authorization with directives
const typeDefs = gql`
  directive @auth(requires: Role = USER) on OBJECT | FIELD_DEFINITION
  
  enum Role {
    ADMIN
    USER
    GUEST
  }
  
  type Query {
    me: User @auth(requires: USER)
    users: [User!]! @auth(requires: ADMIN)
    orders: [Order!]! @auth(requires: USER)
  }
  
  type Mutation {
    createUser(input: CreateUserInput!): User!
    updateUser(id: ID!, input: UpdateUserInput!): User! @auth(requires: USER)
    deleteUser(id: ID!): Boolean! @auth(requires: ADMIN)
  }
`;
```

## Intermediate Level Questions

### 6. How do you optimize GraphQL queries and prevent N+1 problems?
**Answer**: Query optimization techniques:

```javascript
// DataLoader for batching and caching
const DataLoader = require('dataloader');

class UserAPI extends DataSource {
  constructor() {
    super();
    this.userLoader = new DataLoader(this.batchUsers.bind(this));
    this.ordersByUserLoader = new DataLoader(this.batchOrdersByUser.bind(this));
  }
  
  // Batch function for users
  async batchUsers(userIds) {
    const users = await this.store.users.findAll({
      where: { id: userIds }
    });
    
    // Return users in the same order as requested IDs
    return userIds.map(id => users.find(user => user.id === id));
  }
  
  // Batch function for orders by user
  async batchOrdersByUser(userIds) {
    const orders = await this.store.orders.findAll({
      where: { userId: userIds }
    });
    
    // Group orders by userId
    const ordersByUser = userIds.map(userId => 
      orders.filter(order => order.userId === userId)
    );
    
    return ordersByUser;
  }
  
  // Use DataLoader in resolvers
  async getUserById(id) {
    return await this.userLoader.load(id);
  }
  
  async getOrdersByUserId(userId) {
    return await this.ordersByUserLoader.load(userId);
  }
}

// Query complexity analysis
const depthLimit = require('graphql-depth-limit');
const costAnalysis = require('graphql-cost-analysis');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(10), // Limit query depth
    costAnalysis({
      maximumCost: 1000,
      defaultCost: 1,
      scalarCost: 1,
      objectCost: 2,
      listFactor: 10,
      introspectionCost: 1000
    })
  ]
});

// Field-level caching
const resolvers = {
  User: {
    orders: async (user, args, context, info) => {
      const cacheKey = `user:${user.id}:orders`;
      
      // Check cache first
      let orders = await context.cache.get(cacheKey);
      
      if (!orders) {
        orders = await context.dataSources.orderAPI.getOrdersByUserId(user.id);
        // Cache for 5 minutes
        await context.cache.set(cacheKey, orders, { ttl: 300 });
      }
      
      return orders;
    }
  }
};
```

### 7. How do you implement GraphQL subscriptions for real-time data?
**Answer**: Real-time subscriptions implementation:

```javascript
// Subscription setup with Redis PubSub
const { RedisPubSub } = require('graphql-redis-subscriptions');
const Redis = require('ioredis');

const redis = new Redis({
  host: 'localhost',
  port: 6379,
  retryDelayOnFailover: 100,
  enableOfflineQueue: false,
  lazyConnect: true
});

const pubsub = new RedisPubSub({
  publisher: redis,
  subscriber: redis
});

// Subscription resolvers
const resolvers = {
  Subscription: {
    orderUpdated: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(['ORDER_UPDATED']),
        (payload, variables, context) => {
          // Filter subscriptions based on user permissions
          return payload.orderUpdated.userId === context.user.id ||
                 context.user.role === 'ADMIN';
        }
      )
    },
    
    orderStatusChanged: {
      subscribe: withFilter(
        () => pubsub.asyncIterator(['ORDER_STATUS_CHANGED']),
        (payload, variables) => {
          return payload.orderStatusChanged.id === variables.orderId;
        }
      )
    },
    
    newNotification: {
      subscribe: (parent, args, context) => {
        if (!context.user) {
          throw new AuthenticationError('Authentication required');
        }
        
        return pubsub.asyncIterator([`NOTIFICATION_${context.user.id}`]);
      }
    }
  },
  
  Mutation: {
    updateOrderStatus: async (parent, { id, status }, context) => {
      const order = await context.dataSources.orderAPI.updateOrderStatus(id, status);
      
      // Publish to subscribers
      pubsub.publish('ORDER_UPDATED', { orderUpdated: order });
      pubsub.publish('ORDER_STATUS_CHANGED', { orderStatusChanged: order });
      
      // Send notification to user
      pubsub.publish(`NOTIFICATION_${order.userId}`, {
        newNotification: {
          type: 'ORDER_STATUS_UPDATE',
          message: `Your order ${order.id} status changed to ${status}`,
          orderId: order.id
        }
      });
      
      return order;
    }
  }
};

// WebSocket server setup
const { createServer } = require('http');
const { ApolloServerPluginDrainHttpServer } = require('apollo-server-core');
const { makeExecutableSchema } = require('@graphql-tools/schema');
const { WebSocketServer } = require('ws');
const { useServer } = require('graphql-ws/lib/use/ws');

const schema = makeExecutableSchema({ typeDefs, resolvers });

const httpServer = createServer();

const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql'
});

const serverCleanup = useServer({
  schema,
  context: async (ctx) => {
    // Extract token from connection params
    const token = ctx.connectionParams?.authorization;
    const user = await getUser(token);
    
    return {
      user,
      dataSources: {
        orderAPI: new OrderAPI({ store })
      }
    };
  }
}, wsServer);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          }
        };
      }
    }
  ]
});
```

### 8. How do you implement GraphQL federation for microservices?
**Answer**: Apollo Federation for distributed GraphQL:

```javascript
// User Service (Subgraph)
const { buildSubgraphSchema } = require('@apollo/subgraph');

const userTypeDefs = gql`
  type User @key(fields: "id") {
    id: ID!
    name: String!
    email: String!
  }
  
  type Query {
    user(id: ID!): User
    users: [User!]!
  }
  
  type Mutation {
    createUser(input: CreateUserInput!): User!
  }
`;

const userResolvers = {
  Query: {
    user: (parent, { id }) => getUserById(id),
    users: () => getAllUsers()
  },
  
  Mutation: {
    createUser: (parent, { input }) => createUser(input)
  },
  
  User: {
    __resolveReference: (user) => getUserById(user.id)
  }
};

const userSchema = buildSubgraphSchema({
  typeDefs: userTypeDefs,
  resolvers: userResolvers
});

// Order Service (Subgraph)
const orderTypeDefs = gql`
  type User @key(fields: "id") @extends {
    id: ID! @external
    orders: [Order!]!
  }
  
  type Order @key(fields: "id") {
    id: ID!
    userId: ID!
    total: Float!
    status: OrderStatus!
    user: User!
  }
  
  enum OrderStatus {
    PENDING
    CONFIRMED
    SHIPPED
    DELIVERED
  }
  
  type Query {
    order(id: ID!): Order
    orders: [Order!]!
  }
`;

const orderResolvers = {
  Query: {
    order: (parent, { id }) => getOrderById(id),
    orders: () => getAllOrders()
  },
  
  Order: {
    __resolveReference: (order) => getOrderById(order.id),
    user: (order) => ({ __typename: 'User', id: order.userId })
  },
  
  User: {
    orders: (user) => getOrdersByUserId(user.id)
  }
};

const orderSchema = buildSubgraphSchema({
  typeDefs: orderTypeDefs,
  resolvers: orderResolvers
});

// Gateway Configuration
const { ApolloGateway } = require('@apollo/gateway');

const gateway = new ApolloGateway({
  serviceList: [
    { name: 'users', url: 'http://localhost:4001/graphql' },
    { name: 'orders', url: 'http://localhost:4002/graphql' },
    { name: 'products', url: 'http://localhost:4003/graphql' }
  ],
  
  // Optional: Custom fetcher for service discovery
  buildService({ url }) {
    return new RemoteGraphQLDataSource({
      url,
      willSendRequest({ request, context }) {
        request.http.headers.set('authorization', context.authToken);
      }
    });
  }
});

const gatewayServer = new ApolloServer({
  gateway,
  subscriptions: false, // Disable subscriptions in gateway
  context: ({ req }) => ({
    authToken: req.headers.authorization
  })
});
```

### 9. How do you implement error handling and validation in GraphQL?
**Answer**: Comprehensive error handling strategies:

```javascript
// Custom error types
const { ApolloError, UserInputError, ForbiddenError } = require('apollo-server-express');

class ValidationError extends ApolloError {
  constructor(message, field) {
    super(message, 'VALIDATION_ERROR', { field });
  }
}

class BusinessLogicError extends ApolloError {
  constructor(message, code) {
    super(message, code);
  }
}

// Input validation with Joi
const Joi = require('joi');

const createUserSchema = Joi.object({
  name: Joi.string().min(2).max(50).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(18).max(120)
});

const resolvers = {
  Mutation: {
    createUser: async (parent, { input }, context) => {
      // Validate input
      const { error, value } = createUserSchema.validate(input);
      if (error) {
        throw new UserInputError('Invalid input', {
          validationErrors: error.details.map(detail => ({
            field: detail.path.join('.'),
            message: detail.message
          }))
        });
      }
      
      try {
        // Check if user already exists
        const existingUser = await context.dataSources.userAPI.getUserByEmail(value.email);
        if (existingUser) {
          throw new BusinessLogicError('User with this email already exists', 'USER_EXISTS');
        }
        
        const user = await context.dataSources.userAPI.createUser(value);
        return user;
        
      } catch (error) {
        if (error instanceof ApolloError) {
          throw error;
        }
        
        // Log unexpected errors
        console.error('Unexpected error creating user:', error);
        throw new ApolloError('Internal server error', 'INTERNAL_ERROR');
      }
    }
  }
};

// Global error formatting
const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (error) => {
    // Log errors for monitoring
    console.error('GraphQL Error:', {
      message: error.message,
      code: error.extensions?.code,
      path: error.path,
      timestamp: new Date().toISOString()
    });
    
    // Don't expose internal errors to clients
    if (error.extensions?.code === 'INTERNAL_ERROR') {
      return new Error('Internal server error');
    }
    
    return {
      message: error.message,
      code: error.extensions?.code,
      path: error.path,
      ...(error.extensions?.validationErrors && {
        validationErrors: error.extensions.validationErrors
      })
    };
  }
});

// Schema validation with custom scalars
const { GraphQLScalarType } = require('graphql');
const { Kind } = require('graphql/language');

const EmailType = new GraphQLScalarType({
  name: 'Email',
  description: 'Email custom scalar type',
  serialize: (value) => {
    if (!isValidEmail(value)) {
      throw new Error('Invalid email format');
    }
    return value;
  },
  parseValue: (value) => {
    if (!isValidEmail(value)) {
      throw new Error('Invalid email format');
    }
    return value;
  },
  parseLiteral: (ast) => {
    if (ast.kind !== Kind.STRING) {
      throw new Error('Email must be a string');
    }
    if (!isValidEmail(ast.value)) {
      throw new Error('Invalid email format');
    }
    return ast.value;
  }
});

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### 10. How do you implement GraphQL caching strategies?
**Answer**: Multi-level caching implementation:

```javascript
// Response caching with Apollo Server
const { ApolloServer } = require('apollo-server-express');
const { responseCachePlugin } = require('apollo-server-plugin-response-cache');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    responseCachePlugin({
      sessionId: (requestContext) => {
        return requestContext.request.http.headers.get('authorization') || null;
      },
      shouldReadFromCache: (requestContext) => {
        // Don't cache mutations
        return requestContext.request.operationName !== 'mutation';
      },
      shouldWriteToCache: (requestContext) => {
        return !requestContext.errors;
      }
    })
  ],
  cacheControl: {
    defaultMaxAge: 300, // 5 minutes default
    stripFormattedExtensions: false,
    calculateHttpHeaders: false
  }
});

// Field-level cache hints
const resolvers = {
  Query: {
    users: (parent, args, context, info) => {
      info.cacheControl.setCacheHint({ maxAge: 60 }); // 1 minute
      return context.dataSources.userAPI.getUsers();
    },
    
    user: (parent, { id }, context, info) => {
      info.cacheControl.setCacheHint({ maxAge: 300 }); // 5 minutes
      return context.dataSources.userAPI.getUserById(id);
    }
  },
  
  User: {
    orders: (user, args, context, info) => {
      // Private data - shorter cache
      info.cacheControl.setCacheHint({ 
        maxAge: 30,
        scope: 'PRIVATE' 
      });
      return context.dataSources.orderAPI.getOrdersByUserId(user.id);
    }
  }
};

// Redis caching layer
const Redis = require('ioredis');
const redis = new Redis();

class CachedUserAPI extends RESTDataSource {
  async getUserById(id) {
    const cacheKey = `user:${id}`;
    
    // Try cache first
    const cached = await redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }
    
    // Fetch from API
    const user = await this.get(`users/${id}`);
    
    // Cache for 10 minutes
    await redis.setex(cacheKey, 600, JSON.stringify(user));
    
    return user;
  }
  
  async invalidateUserCache(id) {
    await redis.del(`user:${id}`);
    // Also invalidate related caches
    await redis.del(`user:${id}:orders`);
  }
}

// Persisted queries for client-side caching
const { createPersistedQueryLink } = require('@apollo/client/link/persisted-queries');
const { createHttpLink } = require('@apollo/client/link/http');
const { InMemoryCache } = require('@apollo/client');

const httpLink = createHttpLink({
  uri: '/graphql'
});

const persistedQueriesLink = createPersistedQueryLink({
  sha256: require('crypto-js/sha256')
});

const client = new ApolloClient({
  link: persistedQueriesLink.concat(httpLink),
  cache: new InMemoryCache({
    typePolicies: {
      User: {
        fields: {
          orders: {
            merge(existing = [], incoming) {
              return [...existing, ...incoming];
            }
          }
        }
      }
    }
  })
});
```

## Advanced Level Questions

### 11. How do you implement GraphQL security best practices?
**Answer**: Comprehensive security implementation:

```javascript
// Query complexity analysis and rate limiting
const depthLimit = require('graphql-depth-limit');
const costAnalysis = require('graphql-cost-analysis');
const { shield, rule, and, or } = require('graphql-shield');
const rateLimit = require('express-rate-limit');

// Rate limiting middleware
const createRateLimiter = (windowMs, max) => rateLimit({
  windowMs,
  max,
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false
});

// Authentication rules
const isAuthenticated = rule({ cache: 'contextual' })(
  async (parent, args, context) => {
    return context.user !== null;
  }
);

const isAdmin = rule({ cache: 'contextual' })(
  async (parent, args, context) => {
    return context.user && context.user.role === 'ADMIN';
  }
);

const isOwner = rule({ cache: 'strict' })(
  async (parent, args, context) => {
    return context.user && context.user.id === args.id;
  }
);

// Permission shield
const permissions = shield({
  Query: {
    me: isAuthenticated,
    users: isAdmin,
    user: or(isAdmin, isOwner),
    orders: isAuthenticated
  },
  Mutation: {
    createUser: isAdmin,
    updateUser: or(isAdmin, isOwner),
    deleteUser: isAdmin,
    createOrder: isAuthenticated
  },
  User: {
    email: or(isAdmin, isOwner), // Sensitive field
    orders: or(isAdmin, isOwner)
  }
}, {
  allowExternalErrors: true,
  fallbackError: 'Access denied'
});

// Query whitelist for production
const queryWhitelist = new Set([
  'query GetUser($id: ID!) { user(id: $id) { id name email } }',
  'query GetOrders { orders { id total status } }',
  'mutation CreateOrder($input: CreateOrderInput!) { createOrder(input: $input) { id total } }'
]);

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(10),
    costAnalysis({
      maximumCost: 1000,
      defaultCost: 1,
      createError: (max, actual) => {
        return new Error(`Query cost ${actual} exceeds maximum cost ${max}`);
      }
    })
  ],
  plugins: [
    {
      requestDidStart() {
        return {
          didResolveOperation({ request, operationName }) {
            // Query whitelist check in production
            if (process.env.NODE_ENV === 'production') {
              const query = request.query.replace(/\s+/g, ' ').trim();
              if (!queryWhitelist.has(query)) {
                throw new Error('Query not in whitelist');
              }
            }
          }
        };
      }
    }
  ],
  introspection: process.env.NODE_ENV !== 'production',
  playground: process.env.NODE_ENV !== 'production'
});

// Input sanitization
const DOMPurify = require('isomorphic-dompurify');

const sanitizeInput = (input) => {
  if (typeof input === 'string') {
    return DOMPurify.sanitize(input);
  }
  if (typeof input === 'object' && input !== null) {
    const sanitized = {};
    for (const [key, value] of Object.entries(input)) {
      sanitized[key] = sanitizeInput(value);
    }
    return sanitized;
  }
  return input;
};

// SQL injection prevention with parameterized queries
class SecureUserAPI extends DataSource {
  async getUserById(id) {
    // Use parameterized queries
    const query = 'SELECT * FROM users WHERE id = $1';
    const result = await this.db.query(query, [id]);
    return result.rows[0];
  }
  
  async searchUsers(searchTerm) {
    // Sanitize search input
    const sanitizedTerm = DOMPurify.sanitize(searchTerm);
    const query = 'SELECT * FROM users WHERE name ILIKE $1';
    const result = await this.db.query(query, [`%${sanitizedTerm}%`]);
    return result.rows;
  }
}
```

### 12. How do you implement GraphQL monitoring and observability?
**Answer**: Comprehensive monitoring and observability:

```javascript
// Apollo Studio integration
const { ApolloServerPluginUsageReporting } = require('apollo-server-core');

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { all: true },
      sendHeaders: { all: true }
    })
  ]
});

// Custom metrics collection
const prometheus = require('prom-client');

// Create metrics
const httpRequestDuration = new prometheus.Histogram({
  name: 'graphql_request_duration_seconds',
  help: 'Duration of GraphQL requests in seconds',
  labelNames: ['operation_name', 'operation_type', 'status']
});

const resolverDuration = new prometheus.Histogram({
  name: 'graphql_resolver_duration_seconds',
  help: 'Duration of GraphQL resolvers in seconds',
  labelNames: ['field_name', 'type_name']
});

const errorCounter = new prometheus.Counter({
  name: 'graphql_errors_total',
  help: 'Total number of GraphQL errors',
  labelNames: ['error_code', 'operation_name']
});

// Metrics plugin
const metricsPlugin = {
  requestDidStart() {
    const startTime = Date.now();
    
    return {
      didResolveOperation({ request, operationName }) {
        this.operationName = operationName;
        this.operationType = request.operationName;
      },
      
      willSendResponse({ response }) {
        const duration = (Date.now() - startTime) / 1000;
        const status = response.errors ? 'error' : 'success';
        
        httpRequestDuration
          .labels(this.operationName, this.operationType, status)
          .observe(duration);
      },
      
      didEncounterErrors({ errors }) {
        errors.forEach(error => {
          errorCounter
            .labels(error.extensions?.code || 'UNKNOWN', this.operationName)
            .inc();
        });
      }
    };
  }
};

// Resolver-level tracing
const tracingResolvers = {
  Query: {
    users: async (parent, args, context, info) => {
      const startTime = Date.now();
      
      try {
        const result = await context.dataSources.userAPI.getUsers();
        
        const duration = (Date.now() - startTime) / 1000;
        resolverDuration
          .labels('users', 'Query')
          .observe(duration);
        
        return result;
      } catch (error) {
        errorCounter
          .labels('RESOLVER_ERROR', 'users')
          .inc();
        throw error;
      }
    }
  }
};

// Distributed tracing with OpenTelemetry
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');

const sdk = new NodeSDK({
  instrumentations: [getNodeAutoInstrumentations()]
});

sdk.start();

// Custom tracing for GraphQL operations
const opentelemetry = require('@opentelemetry/api');

const tracingPlugin = {
  requestDidStart() {
    return {
      didResolveOperation({ request, operationName }) {
        const span = opentelemetry.trace.getActiveSpan();
        if (span) {
          span.setAttributes({
            'graphql.operation.name': operationName,
            'graphql.operation.type': request.operationName,
            'graphql.query': request.query
          });
        }
      }
    };
  }
};

// Health check endpoint
const express = require('express');
const app = express();

app.get('/health', async (req, res) => {
  try {
    // Check database connectivity
    await context.dataSources.userAPI.healthCheck();
    
    // Check external services
    const externalServiceHealth = await checkExternalServices();
    
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: externalServiceHealth
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Metrics endpoint
app.get('/metrics', (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(prometheus.register.metrics());
});
```

### 13. How do you implement GraphQL testing strategies?
**Answer**: Comprehensive testing approach:

```javascript
// Unit testing resolvers
const { createTestClient } = require('apollo-server-testing');
const { gql } = require('apollo-server-express');

describe('User Resolvers', () => {
  let server, query, mutate;
  
  beforeEach(() => {
    // Mock data sources
    const mockUserAPI = {
      getUserById: jest.fn(),
      createUser: jest.fn(),
      getUsers: jest.fn()
    };
    
    server = new ApolloServer({
      typeDefs,
      resolvers,
      dataSources: () => ({
        userAPI: mockUserAPI
      }),
      context: () => ({
        user: { id: '1', role: 'USER' }
      })
    });
    
    const testClient = createTestClient(server);
    query = testClient.query;
    mutate = testClient.mutate;
  });
  
  test('should get user by ID', async () => {
    const mockUser = { id: '1', name: 'John Doe', email: 'john@example.com' };
    server.dataSources().userAPI.getUserById.mockResolvedValue(mockUser);
    
    const GET_USER = gql`
      query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
          email
        }
      }
    `;
    
    const response = await query({
      query: GET_USER,
      variables: { id: '1' }
    });
    
    expect(response.errors).toBeUndefined();
    expect(response.data.user).toEqual(mockUser);
    expect(server.dataSources().userAPI.getUserById).toHaveBeenCalledWith('1');
  });
  
  test('should handle authentication errors', async () => {
    // Test without authentication
    server = new ApolloServer({
      typeDefs,
      resolvers,
      context: () => ({ user: null })
    });
    
    const testClient = createTestClient(server);
    
    const GET_ME = gql`
      query GetMe {
        me {
          id
          name
        }
      }
    `;
    
    const response = await testClient.query({ query: GET_ME });
    
    expect(response.errors).toBeDefined();
    expect(response.errors[0].extensions.code).toBe('UNAUTHENTICATED');
  });
});

// Integration testing
const request = require('supertest');
const { createServer } = require('http');

describe('GraphQL Integration Tests', () => {
  let app, httpServer;
  
  beforeAll(async () => {
    // Setup test database
    await setupTestDatabase();
    
    const server = new ApolloServer({
      typeDefs,
      resolvers,
      dataSources: () => ({
        userAPI: new UserAPI({ store: testDb })
      })
    });
    
    await server.start();
    
    app = express();
    server.applyMiddleware({ app });
    httpServer = createServer(app);
  });
  
  afterAll(async () => {
    await cleanupTestDatabase();
    httpServer.close();
  });
  
  test('should create and retrieve user', async () => {
    // Create user
    const createUserMutation = `
      mutation CreateUser($input: CreateUserInput!) {
        createUser(input: $input) {
          id
          name
          email
        }
      }
    `;
    
    const createResponse = await request(httpServer)
      .post('/graphql')
      .send({
        query: createUserMutation,
        variables: {
          input: {
            name: 'Test User',
            email: 'test@example.com'
          }
        }
      });
    
    expect(createResponse.status).toBe(200);
    expect(createResponse.body.data.createUser.name).toBe('Test User');
    
    const userId = createResponse.body.data.createUser.id;
    
    // Retrieve user
    const getUserQuery = `
      query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
          email
        }
      }
    `;
    
    const getResponse = await request(httpServer)
      .post('/graphql')
      .send({
        query: getUserQuery,
        variables: { id: userId }
      });
    
    expect(getResponse.status).toBe(200);
    expect(getResponse.body.data.user.name).toBe('Test User');
  });
});

// Load testing with Artillery
// artillery-config.yml
/*
config:
  target: 'http://localhost:4000'
  phases:
    - duration: 60
      arrivalRate: 10
  payload:
    path: 'queries.csv'
    fields:
      - query
      - variables

scenarios:
  - name: 'GraphQL Load Test'
    weight: 100
    engine: http
    requests:
      - post:
          url: '/graphql'
          headers:
            Content-Type: 'application/json'
          json:
            query: '{{ query }}'
            variables: '{{ variables }}'
*/

// Performance testing
const { performance } = require('perf_hooks');

describe('Performance Tests', () => {
  test('should handle complex queries within time limit', async () => {
    const complexQuery = gql`
      query ComplexQuery {
        users(limit: 100) {
          id
          name
          orders(limit: 10) {
            id
            total
            items {
              product {
                name
                category {
                  name
                }
              }
            }
          }
        }
      }
    `;
    
    const startTime = performance.now();
    
    const response = await query({ query: complexQuery });
    
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    expect(response.errors).toBeUndefined();
    expect(duration).toBeLessThan(1000); // Should complete within 1 second
  });
});
```

This comprehensive GraphQL interview question set covers essential knowledge for data engineers, from basic concepts to advanced implementation patterns including federation, security, monitoring, and testing strategies.