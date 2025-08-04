# Google Cloud Platform (GCP) Services Reference for Data Engineering

## 🎯 Overview
This document provides a comprehensive reference of GCP services used in data engineering, their use cases, and official documentation links.

## 📊 Storage Services

### Google Cloud Storage
**What it is**: Object storage service for storing and accessing data on Google Cloud.

**Use Cases**:
- Data lakes and archives
- Content distribution
- Backup and disaster recovery
- Static website hosting
- Big data analytics storage

**Storage Classes**:
- **Standard**: Frequently accessed data
- **Nearline**: Data accessed less than once per month
- **Coldline**: Data accessed less than once per quarter
- **Archive**: Data accessed less than once per year

**Key Features**:
- 99.999999999% (11 9's) durability
- Global edge caching
- Lifecycle management
- Object versioning
- Event notifications

**Reference Links**:
- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Cloud Storage Client Libraries](https://cloud.google.com/storage/docs/reference/libraries)
- [Cloud Storage API Reference](https://cloud.google.com/storage/docs/json_api)

### Persistent Disk
**What it is**: High-performance block storage for Compute Engine instances.

**Use Cases**:
- Database storage
- File systems
- Boot disks
- High-performance computing

**Disk Types**:
- **Standard Persistent Disk**: HDD storage
- **SSD Persistent Disk**: SSD storage
- **Balanced Persistent Disk**: Cost-effective SSD
- **Extreme Persistent Disk**: Highest performance SSD

**Reference Links**:
- [Persistent Disk Documentation](https://cloud.google.com/compute/docs/disks)
- [Disk Types Comparison](https://cloud.google.com/compute/docs/disks/performance)

### Filestore
**What it is**: Fully managed NFS file system.

**Use Cases**:
- Shared storage across instances
- Content repositories
- Application migration
- High-performance computing

**Reference Links**:
- [Filestore Documentation](https://cloud.google.com/filestore/docs)
- [Filestore Quickstart](https://cloud.google.com/filestore/docs/quickstart-console)

## 💻 Compute Services

### Compute Engine
**What it is**: Virtual machines running on Google's infrastructure.

**Use Cases**:
- Web applications
- Data processing
- Development environments
- High-performance computing

**Machine Types**:
- **General Purpose**: E2, N2, N2D, N1
- **Compute Optimized**: C2
- **Memory Optimized**: M2, M1
- **Accelerator Optimized**: A2

**Reference Links**:
- [Compute Engine Documentation](https://cloud.google.com/compute/docs)
- [Machine Types](https://cloud.google.com/compute/docs/machine-types)
- [Compute Engine Quickstart](https://cloud.google.com/compute/docs/quickstart-linux)

### Cloud Functions
**What it is**: Serverless execution environment for building and connecting cloud services.

**Use Cases**:
- Event-driven data processing
- Real-time file processing
- API backends
- ETL operations
- Webhooks

**Supported Runtimes**:
- Node.js
- Python
- Go
- Java
- .NET
- Ruby
- PHP

**Reference Links**:
- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Cloud Functions Quickstart](https://cloud.google.com/functions/docs/quickstart)
- [Cloud Functions Samples](https://cloud.google.com/functions/docs/samples)

### Cloud Run
**What it is**: Fully managed serverless platform for containerized applications.

**Use Cases**:
- Microservices
- APIs
- Data processing jobs
- Web applications

**Reference Links**:
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts)

### Dataproc
**What it is**: Managed Apache Spark and Hadoop service.

**Use Cases**:
- Big data processing
- Machine learning
- Data transformation
- ETL operations
- Log analysis

**Supported Tools**:
- Apache Spark
- Apache Hadoop
- Apache Hive
- Apache Pig
- Presto
- Jupyter notebooks

**Reference Links**:
- [Dataproc Documentation](https://cloud.google.com/dataproc/docs)
- [Dataproc Quickstart](https://cloud.google.com/dataproc/docs/quickstarts)
- [Dataproc Tutorials](https://cloud.google.com/dataproc/docs/tutorials)

## 🗄️ Database Services

### Cloud SQL
**What it is**: Fully managed relational database service.

**Use Cases**:
- Web applications
- E-commerce platforms
- CRM systems
- ERP applications

**Supported Engines**:
- MySQL
- PostgreSQL
- SQL Server

**Key Features**:
- Automatic backups
- Point-in-time recovery
- High availability
- Read replicas
- Automatic storage increase

**Reference Links**:
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Cloud SQL for MySQL](https://cloud.google.com/sql/docs/mysql)
- [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)

### Cloud Spanner
**What it is**: Globally distributed, strongly consistent database service.

**Use Cases**:
- Global applications
- Financial services
- Gaming
- Supply chain management

**Key Features**:
- Horizontal scaling
- Strong consistency
- ACID transactions
- SQL interface
- 99.999% availability

**Reference Links**:
- [Cloud Spanner Documentation](https://cloud.google.com/spanner/docs)
- [Spanner Quickstart](https://cloud.google.com/spanner/docs/quickstart-console)

### Firestore
**What it is**: NoSQL document database for mobile and web applications.

**Use Cases**:
- Mobile applications
- Real-time applications
- Social platforms
- Gaming

**Reference Links**:
- [Firestore Documentation](https://cloud.google.com/firestore/docs)
- [Firestore Quickstart](https://cloud.google.com/firestore/docs/quickstart-servers)

### Bigtable
**What it is**: NoSQL wide-column database for large analytical and operational workloads.

**Use Cases**:
- IoT data
- Time-series data
- Financial data
- Advertising data
- Personalization

**Reference Links**:
- [Bigtable Documentation](https://cloud.google.com/bigtable/docs)
- [Bigtable Quickstart](https://cloud.google.com/bigtable/docs/quickstart-cbt)

## 📈 Analytics Services

### BigQuery
**What it is**: Serverless, highly scalable data warehouse.

**Use Cases**:
- Business intelligence
- Data warehousing
- Analytics
- Machine learning
- Real-time analytics

**Key Features**:
- Serverless architecture
- Standard SQL
- Petabyte scale
- Built-in ML
- Real-time analytics
- Data sharing

**Reference Links**:
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [BigQuery Quickstart](https://cloud.google.com/bigquery/docs/quickstarts)
- [BigQuery SQL Reference](https://cloud.google.com/bigquery/docs/reference/standard-sql)

### Dataflow
**What it is**: Fully managed service for stream and batch data processing.

**Use Cases**:
- ETL operations
- Real-time analytics
- Data integration
- Stream processing
- Batch processing

**Based On**: Apache Beam

**Reference Links**:
- [Dataflow Documentation](https://cloud.google.com/dataflow/docs)
- [Dataflow Quickstart](https://cloud.google.com/dataflow/docs/quickstarts)
- [Dataflow Templates](https://cloud.google.com/dataflow/docs/guides/templates/overview)

### Pub/Sub
**What it is**: Messaging service for event-driven systems and streaming analytics.

**Use Cases**:
- Real-time messaging
- Event ingestion
- Streaming analytics
- Application integration
- IoT data collection

**Key Features**:
- At-least-once delivery
- Global message ordering
- Message filtering
- Dead letter topics
- Replay and seek

**Reference Links**:
- [Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)
- [Pub/Sub Quickstart](https://cloud.google.com/pubsub/docs/quickstart-console)
- [Pub/Sub Client Libraries](https://cloud.google.com/pubsub/docs/reference/libraries)

### Data Fusion
**What it is**: Fully managed, cloud-native data integration service.

**Use Cases**:
- ETL/ELT operations
- Data pipeline creation
- Data integration
- Data preparation

**Reference Links**:
- [Data Fusion Documentation](https://cloud.google.com/data-fusion/docs)
- [Data Fusion Quickstart](https://cloud.google.com/data-fusion/docs/quickstart)

### Dataprep
**What it is**: Intelligent data service for visually exploring and preparing data.

**Use Cases**:
- Data cleaning
- Data transformation
- Data exploration
- Data preparation for analytics

**Reference Links**:
- [Dataprep Documentation](https://cloud.google.com/dataprep/docs)
- [Dataprep Quickstart](https://cloud.google.com/dataprep/docs/quickstart)

### Looker Studio (formerly Data Studio)
**What it is**: Business intelligence platform for creating reports and dashboards.

**Use Cases**:
- Business dashboards
- Data visualization
- Reporting
- Self-service analytics

**Reference Links**:
- [Looker Studio Documentation](https://support.google.com/looker-studio)
- [Looker Studio Help Center](https://support.google.com/looker-studio/answer/6283323)

## 🤖 AI/ML Services

### Vertex AI
**What it is**: Unified ML platform for building, deploying, and scaling ML models.

**Use Cases**:
- Machine learning model development
- AutoML
- Model deployment
- MLOps

**Reference Links**:
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Vertex AI Quickstart](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)

### AutoML
**What it is**: Suite of machine learning products for custom model training.

**Products**:
- AutoML Vision
- AutoML Natural Language
- AutoML Translation
- AutoML Tables

**Reference Links**:
- [AutoML Documentation](https://cloud.google.com/automl/docs)

## 🔄 Integration Services

### Cloud Composer
**What it is**: Fully managed workflow orchestration service built on Apache Airflow.

**Use Cases**:
- Data pipeline orchestration
- Workflow automation
- ETL scheduling
- Multi-cloud workflows

**Reference Links**:
- [Cloud Composer Documentation](https://cloud.google.com/composer/docs)
- [Composer Quickstart](https://cloud.google.com/composer/docs/quickstart)

### Cloud Scheduler
**What it is**: Fully managed cron job service.

**Use Cases**:
- Scheduled tasks
- Batch job triggering
- Periodic data processing
- Automated workflows

**Reference Links**:
- [Cloud Scheduler Documentation](https://cloud.google.com/scheduler/docs)
- [Scheduler Quickstart](https://cloud.google.com/scheduler/docs/quickstart)

### Cloud Tasks
**What it is**: Asynchronous task execution service.

**Use Cases**:
- Background processing
- Task queuing
- Asynchronous workflows
- Rate limiting

**Reference Links**:
- [Cloud Tasks Documentation](https://cloud.google.com/tasks/docs)
- [Tasks Quickstart](https://cloud.google.com/tasks/docs/quickstart)

## 🔐 Security Services

### Identity and Access Management (IAM)
**What it is**: Service for managing access control across Google Cloud resources.

**Use Cases**:
- User authentication
- Permission management
- Service account management
- Resource access control

**Key Components**:
- Members (users, groups, service accounts)
- Roles (collections of permissions)
- Policies (bindings of members to roles)

**Reference Links**:
- [IAM Documentation](https://cloud.google.com/iam/docs)
- [IAM Quickstart](https://cloud.google.com/iam/docs/quickstart)

### Cloud KMS (Key Management Service)
**What it is**: Managed service for creating and managing encryption keys.

**Use Cases**:
- Data encryption
- Key rotation
- Compliance requirements
- Digital signing

**Reference Links**:
- [Cloud KMS Documentation](https://cloud.google.com/kms/docs)
- [KMS Quickstart](https://cloud.google.com/kms/docs/quickstart)

### Secret Manager
**What it is**: Secure storage system for API keys, passwords, and other sensitive data.

**Use Cases**:
- API key management
- Database credentials
- Certificate storage
- Configuration secrets

**Reference Links**:
- [Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [Secret Manager Quickstart](https://cloud.google.com/secret-manager/docs/quickstart)

## 📊 Monitoring Services

### Cloud Monitoring (formerly Stackdriver)
**What it is**: Infrastructure and application monitoring service.

**Use Cases**:
- Performance monitoring
- Alerting
- Dashboards
- SLA monitoring

**Reference Links**:
- [Cloud Monitoring Documentation](https://cloud.google.com/monitoring/docs)
- [Monitoring Quickstart](https://cloud.google.com/monitoring/quickstart)

### Cloud Logging (formerly Stackdriver Logging)
**What it is**: Real-time log management and analysis service.

**Use Cases**:
- Log aggregation
- Log analysis
- Troubleshooting
- Compliance auditing

**Reference Links**:
- [Cloud Logging Documentation](https://cloud.google.com/logging/docs)
- [Logging Quickstart](https://cloud.google.com/logging/docs/quickstart)

### Cloud Trace
**What it is**: Distributed tracing system for Google Cloud applications.

**Use Cases**:
- Performance analysis
- Latency troubleshooting
- Request flow analysis
- Bottleneck identification

**Reference Links**:
- [Cloud Trace Documentation](https://cloud.google.com/trace/docs)
- [Trace Quickstart](https://cloud.google.com/trace/docs/quickstart)

## 🌐 Networking Services

### Virtual Private Cloud (VPC)
**What it is**: Global virtual network for Google Cloud resources.

**Use Cases**:
- Network isolation
- Hybrid connectivity
- Multi-region deployments
- Security boundaries

**Reference Links**:
- [VPC Documentation](https://cloud.google.com/vpc/docs)
- [VPC Quickstart](https://cloud.google.com/vpc/docs/quickstart)

### Cloud Interconnect
**What it is**: Options for connecting external networks to Google Cloud.

**Types**:
- **Dedicated Interconnect**: Direct physical connection
- **Partner Interconnect**: Connection through service provider

**Reference Links**:
- [Cloud Interconnect Documentation](https://cloud.google.com/network-connectivity/docs/interconnect)

### Cloud VPN
**What it is**: Secure connection between Google Cloud and external networks.

**Use Cases**:
- Hybrid cloud connectivity
- Site-to-site VPN
- Remote access
- Multi-cloud connectivity

**Reference Links**:
- [Cloud VPN Documentation](https://cloud.google.com/network-connectivity/docs/vpn)

## 🚀 Additional Resources

### Google Cloud Architecture Framework
- [Architecture Framework](https://cloud.google.com/architecture/framework)
- [Architecture Center](https://cloud.google.com/architecture)
- [Solution Guides](https://cloud.google.com/architecture/all-guides)

### Google Cloud Training and Certification
- [Cloud Training](https://cloud.google.com/training)
- [Cloud Certification](https://cloud.google.com/certification)
- [Cloud Skills Boost](https://www.cloudskillsboost.google/)

### Pricing and Cost Management
- [Pricing Calculator](https://cloud.google.com/products/calculator)
- [Cost Management](https://cloud.google.com/cost-management)
- [Billing Documentation](https://cloud.google.com/billing/docs)

### Developer Tools
- [Cloud SDK](https://cloud.google.com/sdk/docs)
- [Cloud Shell](https://cloud.google.com/shell/docs)
- [Cloud Console](https://cloud.google.com/cloud-console)

### Best Practices
- [Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)
- [Security Best Practices](https://cloud.google.com/security/best-practices)
- [Cost Optimization](https://cloud.google.com/architecture/framework/cost-optimization)

This reference provides a comprehensive overview of Google Cloud Platform services commonly used in data engineering. Each service includes practical use cases and direct links to official GCP documentation for detailed implementation guidance.