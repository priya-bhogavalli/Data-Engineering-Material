# AWS Lambda - Interview Questions

## Basic Concepts

### 1. What is AWS Lambda and what are its key benefits?
**Answer:** AWS Lambda is a serverless computing service that runs code in response to events. Key benefits:
- **No Server Management**: AWS handles all infrastructure provisioning and management
- **Automatic Scaling**: Scales from zero to thousands of concurrent executions automatically
- **Pay-per-Use**: Only pay for actual compute time consumed, not idle time
- **Event-Driven**: Executes code in response to various AWS service events
- **Multiple Runtimes**: Supports Python, Node.js, Java, C#, Go, Ruby, and custom runtimes
- **Built-in Monitoring**: Integrated with CloudWatch for logging and monitoring
- **High Availability**: Automatically distributed across multiple AZs

### 2. How does AWS Lambda pricing work?
**Answer:** Lambda pricing is based on two components:
- **Request Charges**: $0.20 per 1 million requests after free tier
- **Duration Charges**: Based on allocated memory and execution time (GB-seconds)
- **Free Tier**: 1 million free requests and 400,000 GB-seconds per month
- **Provisioned Concurrency**: Additional charges for pre-warmed instances
- **Data Transfer**: Standard AWS data transfer charges apply
- **No Charges**: No charges when code is not running
Example: 128MB function running for 100ms costs approximately $0.000000208

### 3. What are the different ways to invoke AWS Lambda functions?
**Answer:** Lambda functions can be invoked in three ways:
- **Synchronous (Request-Response)**: API Gateway, ALB, direct invocation via SDK
- **Asynchronous (Event)**: S3, SNS, CloudWatch Events, SES
- **Stream-Based (Poll-Based)**: DynamoDB Streams, Kinesis, SQS, MSK
Each invocation type has different retry behaviors and error handling mechanisms.

### 4. What are Lambda layers and how are they used?
**Answer:** Lambda layers are a distribution mechanism for libraries and custom runtimes:
- **Shared Code**: Share common code across multiple functions
- **Dependency Management**: Package libraries separately from function code
- **Version Control**: Manage different versions of shared components
- **Size Limits**: Each layer can be up to 50MB zipped, 250MB unzipped
- **Layer Limit**: Up to 5 layers per function
- **Runtime Support**: Can include custom runtimes and language extensions
- **Deployment**: Deployed independently from function code

### 5. What are the limitations of AWS Lambda?
**Answer:** Key Lambda limitations include:
- **Execution Time**: Maximum 15-minute execution timeout
- **Memory**: 128MB to 10GB memory allocation
- **Temporary Storage**: 512MB to 10GB in /tmp directory
- **Deployment Package**: 50MB zipped, 250MB unzipped
- **Environment Variables**: 4KB total size limit
- **Concurrent Executions**: 1000 concurrent executions per region (can be increased)
- **File Descriptors**: 1024 file descriptors per function
- **Processes/Threads**: 1024 processes and threads combined

## Intermediate Concepts

### 6. Explain the concept of cold starts in Lambda and how to minimize them.
**Answer:** Cold starts occur when Lambda creates a new execution environment:
**Causes:**
- First invocation of a function
- Scaling up due to increased traffic
- Function hasn't been invoked recently
- Code or configuration changes

**Minimization Strategies:**
- **Provisioned Concurrency**: Pre-warm function instances
- **Optimize Package Size**: Reduce deployment package size
- **Connection Pooling**: Reuse database connections outside handler
- **Language Choice**: Some runtimes have faster cold start times
- **Memory Allocation**: Higher memory can reduce cold start duration

### 7. How do you handle errors and retries in Lambda functions?
**Answer:** Error handling varies by invocation type:
**Synchronous Invocation:**
- Errors returned immediately to caller
- No automatic retries by Lambda
- Client responsible for retry logic

**Asynchronous Invocation:**
- Automatic retries (2 attempts by default)
- Dead Letter Queues for failed events
- Configurable retry behavior

**Stream-Based Invocation:**
- Retries until success or data expires
- Configurable retry attempts and batch size
- Error records can block processing

**Best Practices:**
- Implement idempotent functions
- Use appropriate exception handling
- Configure dead letter queues
- Monitor error rates and patterns

### 8. How do you implement database connections in Lambda functions?
**Answer:** Database connection best practices:
**Connection Management:**
- Initialize connections outside the handler function
- Reuse connections across invocations
- Implement connection pooling
- Handle connection timeouts and failures

**RDS Proxy:**
- Use RDS Proxy for connection pooling
- Reduces connection overhead
- Handles connection lifecycle automatically
- Supports IAM authentication

**Example Pattern:**
```python
import pymysql
# Initialize outside handler
connection = None

def lambda_handler(event, context):
    global connection
    if not connection:
        connection = pymysql.connect(...)
    # Use connection for database operations
```

### 9. What is Lambda@Edge and when would you use it?
**Answer:** Lambda@Edge runs Lambda functions at CloudFront edge locations:
**Use Cases:**
- **Request/Response Manipulation**: Modify headers, URLs, or content
- **Authentication**: Implement custom authentication logic
- **A/B Testing**: Route traffic based on custom logic
- **SEO Optimization**: Generate dynamic content for crawlers
- **Security**: Implement custom security headers

**Limitations:**
- Shorter timeout (5 seconds for viewer events, 30 seconds for origin events)
- Limited memory (128MB for viewer events, 3GB for origin events)
- No environment variables
- Limited runtime support

### 10. How do you implement monitoring and observability for Lambda functions?
**Answer:** Comprehensive monitoring approach:
**CloudWatch Metrics:**
- Invocations, Duration, Errors, Throttles
- Custom metrics using CloudWatch API
- Alarms for error rates and performance

**CloudWatch Logs:**
- Automatic log collection
- Structured logging with JSON
- Log retention configuration

**AWS X-Ray:**
- Distributed tracing across services
- Performance analysis and bottleneck identification
- Service map visualization

**Custom Monitoring:**
- Application-specific metrics
- Business logic monitoring
- Performance benchmarking

## Advanced Concepts

### 11. How do you implement a serverless ETL pipeline using Lambda?
**Answer:** Serverless ETL pipeline architecture:
**Components:**
- **S3**: Data lake storage for raw and processed data
- **Lambda**: ETL processing functions
- **Step Functions**: Orchestrate complex workflows
- **Glue Catalog**: Metadata management
- **Athena**: Query processed data

**Implementation Pattern:**
1. **Extract**: Lambda triggered by S3 events
2. **Transform**: Process data using Lambda functions
3. **Load**: Store processed data back to S3 or databases
4. **Orchestration**: Use Step Functions for complex workflows
5. **Monitoring**: CloudWatch and X-Ray for observability

**Best Practices:**
- Use appropriate memory allocation for data size
- Implement checkpointing for large datasets
- Handle partial failures gracefully
- Use parallel processing where possible

### 12. How do you handle state management in serverless applications?
**Answer:** State management strategies:
**External State Storage:**
- **DynamoDB**: Fast NoSQL database for application state
- **RDS**: Relational database for complex state
- **ElastiCache**: In-memory caching for temporary state
- **S3**: Object storage for large state objects

**State Machines:**
- **Step Functions**: Coordinate stateful workflows
- **Event-driven architecture**: Use events to maintain state
- **Saga pattern**: Handle distributed transactions

**Caching Strategies:**
- **Function-level caching**: Cache data in global variables
- **External caching**: Use ElastiCache or DynamoDB
- **CDN caching**: Cache responses at CloudFront edge

### 13. How do you implement security best practices for Lambda functions?
**Answer:** Security implementation strategies:
**IAM and Access Control:**
- Use least privilege principle for execution roles
- Implement resource-based policies for function access
- Use IAM conditions for fine-grained control

**Network Security:**
- Deploy functions in VPC for private resource access
- Use security groups and NACLs appropriately
- Implement VPC endpoints for AWS service access

**Data Protection:**
- Encrypt environment variables with KMS
- Use AWS Secrets Manager for sensitive data
- Implement input validation and sanitization
- Enable encryption in transit and at rest

**Code Security:**
- Regular dependency updates
- Static code analysis
- Secure coding practices
- Runtime security monitoring

### 14. How do you optimize Lambda functions for performance and cost?
**Answer:** Optimization strategies:
**Performance Optimization:**
- Right-size memory allocation (affects CPU)
- Minimize cold start impact
- Optimize code efficiency
- Use connection pooling
- Implement appropriate caching

**Cost Optimization:**
- Monitor and analyze usage patterns
- Optimize memory allocation for cost/performance balance
- Use provisioned concurrency judiciously
- Implement efficient algorithms
- Consider alternative architectures for long-running tasks

**Monitoring and Tuning:**
- Use CloudWatch metrics for optimization insights
- Implement performance benchmarking
- Regular performance reviews
- A/B testing for optimization changes

### 15. How do you implement disaster recovery for Lambda-based applications?
**Answer:** Disaster recovery strategies:
**Multi-Region Deployment:**
- Deploy functions across multiple regions
- Use Route 53 for traffic routing
- Implement cross-region replication for data

**Backup and Recovery:**
- Version control for function code
- Automated deployment pipelines
- Infrastructure as Code (CloudFormation/CDK)
- Regular backup of configuration and data

**Monitoring and Alerting:**
- Cross-region monitoring setup
- Automated failover mechanisms
- Health checks and synthetic monitoring
- Incident response procedures

## Real-World Scenarios

### 16. How would you design a real-time data processing system using Lambda?
**Answer:** Real-time processing architecture:
**Components:**
- **Kinesis Data Streams**: Ingest streaming data
- **Lambda**: Process stream records in real-time
- **DynamoDB**: Store processed results
- **CloudWatch**: Monitor processing metrics

**Implementation:**
- Configure Kinesis as event source for Lambda
- Implement batch processing for efficiency
- Handle partial batch failures appropriately
- Use DLQ for failed records
- Implement monitoring and alerting

**Scaling Considerations:**
- Shard count affects parallelism
- Lambda concurrency limits
- Downstream system capacity
- Error handling and retry logic

### 17. Describe how you would migrate a monolithic application to serverless using Lambda.
**Answer:** Migration strategy:
**Assessment Phase:**
- Analyze current application architecture
- Identify microservice boundaries
- Assess data dependencies
- Evaluate performance requirements

**Decomposition Strategy:**
- **Strangler Fig Pattern**: Gradually replace components
- **Database per Service**: Separate data stores
- **API Gateway**: Unified API interface
- **Event-driven Communication**: Decouple services

**Implementation Phases:**
1. Extract stateless components first
2. Implement new features as Lambda functions
3. Gradually migrate existing functionality
4. Optimize and refine architecture

### 18. How would you handle high-volume batch processing with Lambda?
**Answer:** Batch processing strategies:
**Architecture Patterns:**
- **Fan-out Pattern**: Distribute work across multiple functions
- **Step Functions**: Orchestrate complex batch workflows
- **SQS**: Queue-based processing for reliability
- **S3 Event Processing**: Process files as they arrive

**Implementation Considerations:**
- Break large jobs into smaller chunks
- Use appropriate memory allocation
- Implement checkpointing for long processes
- Handle partial failures gracefully
- Monitor processing progress

**Cost Optimization:**
- Balance function duration vs. invocation count
- Use appropriate memory allocation
- Consider Fargate for very long-running tasks
- Implement efficient algorithms

### 19. How would you implement a serverless API with authentication and authorization?
**Answer:** Serverless API implementation:
**Components:**
- **API Gateway**: HTTP API endpoint
- **Lambda Authorizer**: Custom authorization logic
- **Cognito**: User authentication and management
- **Lambda Functions**: Business logic implementation

**Authentication Options:**
- **Cognito User Pools**: Built-in user management
- **Lambda Authorizer**: Custom authorization logic
- **IAM**: AWS credential-based access
- **JWT**: Token-based authentication

**Security Implementation:**
- Input validation and sanitization
- Rate limiting and throttling
- CORS configuration
- API key management
- Request/response logging

### 20. How would you troubleshoot performance issues in a Lambda-based application?
**Answer:** Troubleshooting methodology:
**Performance Analysis:**
- CloudWatch metrics analysis (duration, memory usage)
- X-Ray tracing for bottleneck identification
- Cold start impact assessment
- Memory allocation optimization

**Common Issues and Solutions:**
- **High Duration**: Optimize code, increase memory, improve algorithms
- **Cold Starts**: Use provisioned concurrency, optimize package size
- **Timeouts**: Increase timeout, optimize code, break into smaller functions
- **Memory Issues**: Right-size memory allocation, optimize data structures

**Monitoring Tools:**
- CloudWatch dashboards and alarms
- X-Ray service maps and traces
- Custom metrics and logging
- Performance benchmarking tools

**Optimization Process:**
- Establish performance baselines
- Implement gradual optimizations
- A/B testing for changes
- Continuous monitoring and improvement