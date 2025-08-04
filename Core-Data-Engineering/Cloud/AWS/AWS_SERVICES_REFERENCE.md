# AWS Services Reference for Data Engineering

## 🎯 Overview
This document provides a comprehensive reference of AWS services used in data engineering, their use cases, and official documentation links.

## 📊 Storage Services

### Amazon S3 (Simple Storage Service)
**What it is**: Object storage service for storing and retrieving any amount of data from anywhere.

**Use Cases**:
- Data lakes and data archiving
- Static website hosting
- Backup and restore
- Content distribution
- Big data analytics storage

**Key Features**:
- 99.999999999% (11 9's) durability
- Multiple storage classes (Standard, IA, Glacier, Deep Archive)
- Lifecycle management
- Cross-region replication
- Event notifications

**Reference Links**:
- [Official Documentation](https://docs.aws.amazon.com/s3/)
- [S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
- [S3 API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/)

### Amazon EBS (Elastic Block Store)
**What it is**: High-performance block storage for EC2 instances.

**Use Cases**:
- Database storage
- File systems
- Boot volumes
- Enterprise applications

**Storage Types**:
- **gp3/gp2**: General purpose SSD
- **io2/io1**: Provisioned IOPS SSD
- **st1**: Throughput optimized HDD
- **sc1**: Cold HDD

**Reference Links**:
- [EBS Documentation](https://docs.aws.amazon.com/ebs/)
- [EBS Volume Types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)

### Amazon EFS (Elastic File System)
**What it is**: Managed NFS file system for EC2 instances.

**Use Cases**:
- Shared storage across multiple instances
- Content repositories
- Web serving
- Data analytics

**Reference Links**:
- [EFS Documentation](https://docs.aws.amazon.com/efs/)
- [EFS User Guide](https://docs.aws.amazon.com/efs/latest/ug/)

## 💻 Compute Services

### Amazon EC2 (Elastic Compute Cloud)
**What it is**: Resizable compute capacity in the cloud.

**Use Cases**:
- Web applications
- Data processing
- Development environments
- High-performance computing

**Instance Types**:
- **General Purpose**: t3, m5, m6i
- **Compute Optimized**: c5, c6i
- **Memory Optimized**: r5, r6i, x1e
- **Storage Optimized**: i3, d2, h1
- **Accelerated Computing**: p3, g4, f1

**Reference Links**:
- [EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
- [EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)

### AWS Lambda
**What it is**: Serverless compute service that runs code in response to events.

**Use Cases**:
- Event-driven data processing
- Real-time file processing
- API backends
- ETL operations
- Data validation

**Key Features**:
- Automatic scaling
- Pay-per-request pricing
- Multiple runtime support
- Event source integrations

**Reference Links**:
- [Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Lambda API Reference](https://docs.aws.amazon.com/lambda/latest/api/)

### Amazon EMR (Elastic MapReduce)
**What it is**: Managed cluster platform for big data frameworks.

**Use Cases**:
- Big data processing
- Machine learning
- Data transformation
- Log analysis
- ETL operations

**Supported Frameworks**:
- Apache Spark
- Apache Hadoop
- Apache Hive
- Apache HBase
- Presto
- Apache Flink

**Reference Links**:
- [EMR Documentation](https://docs.aws.amazon.com/emr/)
- [EMR Management Guide](https://docs.aws.amazon.com/emr/latest/ManagementGuide/)
- [EMR Release Guide](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/)

## 🗄️ Database Services

### Amazon RDS (Relational Database Service)
**What it is**: Managed relational database service.

**Use Cases**:
- Web applications
- E-commerce
- Mobile applications
- Online gaming

**Supported Engines**:
- MySQL
- PostgreSQL
- MariaDB
- Oracle
- SQL Server
- Amazon Aurora

**Reference Links**:
- [RDS Documentation](https://docs.aws.amazon.com/rds/)
- [RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/)
- [Aurora User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/)

### Amazon DynamoDB
**What it is**: Fully managed NoSQL database service.

**Use Cases**:
- Mobile applications
- Web applications
- Gaming
- IoT
- Real-time bidding

**Key Features**:
- Single-digit millisecond latency
- Automatic scaling
- Global tables
- Point-in-time recovery
- DynamoDB Streams

**Reference Links**:
- [DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/)
- [DynamoDB API Reference](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/)

### Amazon Redshift
**What it is**: Fully managed data warehouse service.

**Use Cases**:
- Business intelligence
- Data warehousing
- Analytics
- Reporting

**Key Features**:
- Columnar storage
- Massively parallel processing
- Advanced compression
- Result caching
- Concurrency scaling

**Reference Links**:
- [Redshift Documentation](https://docs.aws.amazon.com/redshift/)
- [Redshift Database Developer Guide](https://docs.aws.amazon.com/redshift/latest/dg/)
- [Redshift Management Guide](https://docs.aws.amazon.com/redshift/latest/mgmt/)

## 📈 Analytics Services

### Amazon Athena
**What it is**: Interactive query service for analyzing data in S3 using SQL.

**Use Cases**:
- Ad-hoc querying
- Log analysis
- Data exploration
- Business intelligence
- Cost analysis

**Key Features**:
- Serverless
- Standard SQL
- Multiple data formats
- Integration with AWS Glue
- Federated queries

**Reference Links**:
- [Athena Documentation](https://docs.aws.amazon.com/athena/)
- [Athena User Guide](https://docs.aws.amazon.com/athena/latest/ug/)
- [Athena API Reference](https://docs.aws.amazon.com/athena/latest/APIReference/)

### AWS Glue
**What it is**: Fully managed ETL service and data catalog.

**Use Cases**:
- ETL operations
- Data catalog management
- Schema discovery
- Data preparation
- Data integration

**Components**:
- **Glue Data Catalog**: Metadata repository
- **Glue ETL**: Serverless ETL jobs
- **Glue Crawlers**: Schema discovery
- **Glue DataBrew**: Visual data preparation

**Reference Links**:
- [Glue Documentation](https://docs.aws.amazon.com/glue/)
- [Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/)
- [Glue API Reference](https://docs.aws.amazon.com/glue/latest/webapi/)

### Amazon Kinesis
**What it is**: Platform for streaming data on AWS.

**Use Cases**:
- Real-time analytics
- Log and event data collection
- IoT data ingestion
- Clickstream analysis

**Services**:
- **Kinesis Data Streams**: Real-time data streaming
- **Kinesis Data Firehose**: Data delivery to destinations
- **Kinesis Data Analytics**: Real-time analytics
- **Kinesis Video Streams**: Video streaming

**Reference Links**:
- [Kinesis Documentation](https://docs.aws.amazon.com/kinesis/)
- [Kinesis Data Streams Guide](https://docs.aws.amazon.com/streams/latest/dev/)
- [Kinesis Data Firehose Guide](https://docs.aws.amazon.com/firehose/latest/dev/)

### Amazon QuickSight
**What it is**: Business intelligence service for creating visualizations and dashboards.

**Use Cases**:
- Business dashboards
- Ad-hoc analysis
- Embedded analytics
- Mobile BI

**Key Features**:
- SPICE in-memory engine
- ML insights
- Embedded analytics
- Pay-per-session pricing

**Reference Links**:
- [QuickSight Documentation](https://docs.aws.amazon.com/quicksight/)
- [QuickSight User Guide](https://docs.aws.amazon.com/quicksight/latest/user/)
- [QuickSight API Reference](https://docs.aws.amazon.com/quicksight/latest/APIReference/)

## 🔄 Integration Services

### Amazon SQS (Simple Queue Service)
**What it is**: Fully managed message queuing service.

**Use Cases**:
- Decoupling applications
- Batch processing
- Microservices communication
- Event-driven architectures

**Queue Types**:
- **Standard Queues**: At-least-once delivery
- **FIFO Queues**: Exactly-once processing

**Reference Links**:
- [SQS Documentation](https://docs.aws.amazon.com/sqs/)
- [SQS Developer Guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/)

### Amazon SNS (Simple Notification Service)
**What it is**: Fully managed messaging service for pub/sub patterns.

**Use Cases**:
- Application alerts
- Push notifications
- Email/SMS notifications
- Fan-out messaging

**Reference Links**:
- [SNS Documentation](https://docs.aws.amazon.com/sns/)
- [SNS Developer Guide](https://docs.aws.amazon.com/sns/latest/dg/)

### AWS Step Functions
**What it is**: Serverless workflow orchestration service.

**Use Cases**:
- Data processing workflows
- Microservices orchestration
- ETL pipelines
- Machine learning workflows

**Reference Links**:
- [Step Functions Documentation](https://docs.aws.amazon.com/step-functions/)
- [Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)

## 🔐 Security Services

### AWS IAM (Identity and Access Management)
**What it is**: Service for managing access to AWS services and resources.

**Use Cases**:
- User authentication
- Permission management
- Role-based access control
- Cross-account access

**Key Components**:
- Users
- Groups
- Roles
- Policies

**Reference Links**:
- [IAM Documentation](https://docs.aws.amazon.com/iam/)
- [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/)

### AWS KMS (Key Management Service)
**What it is**: Managed service for creating and managing encryption keys.

**Use Cases**:
- Data encryption
- Key rotation
- Compliance requirements
- Digital signing

**Reference Links**:
- [KMS Documentation](https://docs.aws.amazon.com/kms/)
- [KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/)

## 📊 Monitoring Services

### Amazon CloudWatch
**What it is**: Monitoring and observability service.

**Use Cases**:
- Application monitoring
- Log management
- Performance tracking
- Alerting

**Components**:
- **CloudWatch Metrics**: Performance data
- **CloudWatch Logs**: Log file monitoring
- **CloudWatch Alarms**: Automated actions
- **CloudWatch Events**: Event-driven automation

**Reference Links**:
- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/)

### AWS CloudTrail
**What it is**: Service for logging API calls and account activity.

**Use Cases**:
- Compliance auditing
- Security analysis
- Troubleshooting
- Change tracking

**Reference Links**:
- [CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail/)
- [CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/)

## 🌐 Networking Services

### Amazon VPC (Virtual Private Cloud)
**What it is**: Isolated cloud resources in a virtual network.

**Use Cases**:
- Network isolation
- Hybrid cloud connectivity
- Multi-tier applications
- Security compliance

**Reference Links**:
- [VPC Documentation](https://docs.aws.amazon.com/vpc/)
- [VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)

### AWS Direct Connect
**What it is**: Dedicated network connection to AWS.

**Use Cases**:
- Hybrid cloud architectures
- Large data transfers
- Consistent network performance
- Reduced bandwidth costs

**Reference Links**:
- [Direct Connect Documentation](https://docs.aws.amazon.com/directconnect/)
- [Direct Connect User Guide](https://docs.aws.amazon.com/directconnect/latest/UserGuide/)

## 🚀 Additional Resources

### AWS Well-Architected Framework
- [Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Data Analytics Lens](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/)

### AWS Training and Certification
- [AWS Training](https://aws.amazon.com/training/)
- [AWS Certification](https://aws.amazon.com/certification/)
- [AWS Skill Builder](https://skillbuilder.aws/)

### AWS Architecture Center
- [Architecture Center](https://aws.amazon.com/architecture/)
- [Reference Architectures](https://aws.amazon.com/architecture/reference-architecture-diagrams/)
- [AWS Solutions](https://aws.amazon.com/solutions/)

### Pricing Information
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)

This reference provides a comprehensive overview of AWS services commonly used in data engineering. Each service includes practical use cases and direct links to official AWS documentation for detailed implementation guidance.