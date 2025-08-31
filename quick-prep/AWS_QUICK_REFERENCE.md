# ☁️ AWS Quick Reference for Data Engineering

## 🗄️ **Storage Services**
```
S3 (Simple Storage Service)
├── Data Lake storage
├── Bucket policies & lifecycle rules
├── Storage classes: Standard, IA, Glacier
└── Cross-region replication

EBS (Elastic Block Store)
├── High-performance block storage
├── gp3, io2 for databases
└── Snapshot backups

EFS (Elastic File System)
└── Shared file storage across EC2
```

## 🔄 **Data Processing**
```
Glue
├── Serverless ETL service
├── Data Catalog & Crawlers
├── Job bookmarks for incremental processing
└── Glue Studio for visual ETL

EMR (Elastic MapReduce)
├── Managed Hadoop/Spark clusters
├── Auto-scaling capabilities
├── Spot instances for cost optimization
└── Notebooks for development

Kinesis
├── Data Streams: Real-time data ingestion
├── Data Firehose: Load to S3/Redshift
├── Data Analytics: SQL on streaming data
└── Video Streams: Video processing
```

## 🏢 **Data Warehousing**
```
Redshift
├── Columnar storage
├── Massively parallel processing (MPP)
├── Spectrum for S3 queries
└── Concurrency scaling

Athena
├── Serverless SQL queries on S3
├── Presto-based engine
├── Pay per query
└── ACID transactions with Iceberg
```

## 🗃️ **Databases**
```
RDS (Relational Database Service)
├── PostgreSQL, MySQL, Oracle, SQL Server
├── Multi-AZ for high availability
├── Read replicas for scaling
└── Automated backups

DynamoDB
├── NoSQL key-value store
├── Single-digit millisecond latency
├── Auto-scaling
└── Global tables for multi-region
```

## 🔐 **Security & Access**
```
IAM (Identity & Access Management)
├── Users, Groups, Roles
├── Policies (JSON-based permissions)
├── Principle of least privilege
└── Cross-account access

VPC (Virtual Private Cloud)
├── Private subnets for databases
├── Security groups (stateful firewall)
├── NACLs (stateless firewall)
└── VPC endpoints for private access
```

## 📊 **Monitoring & Management**
```
CloudWatch
├── Metrics & alarms
├── Logs aggregation
├── Custom metrics
└── Dashboards

CloudTrail
├── API call logging
├── Compliance & auditing
└── Event history
```

## 💰 **Cost Optimization Tips**
- Use S3 Intelligent Tiering for automatic cost optimization
- Leverage Spot instances for EMR clusters
- Set up lifecycle policies for S3 objects
- Use Reserved Instances for predictable workloads
- Monitor with Cost Explorer and set billing alerts