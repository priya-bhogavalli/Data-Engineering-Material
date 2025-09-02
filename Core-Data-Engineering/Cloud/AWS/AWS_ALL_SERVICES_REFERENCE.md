# ☁️ Complete AWS Services Reference

> **Ultimate comprehensive guide to all 320+ AWS services with interactive decision-making features, cost analysis, and architecture patterns**

## 📋 Table of Contents

- [🎯 AWS Service Selection Wizard](#-aws-service-selection-wizard)
- [📊 Complete AWS Services Overview](#-complete-aws-services-overview)
- [🏗️ AWS Architecture Patterns](#️-aws-architecture-patterns)
- [⚡ Performance & Scalability](#-performance--scalability)
- [💰 Cost Analysis & Optimization](#-cost-analysis--optimization)
- [🔗 Service Integration Matrix](#-service-integration-matrix)
- [📚 Learning & Certification](#-learning--certification)
- [🆚 Service Comparison & Selection](#-service-comparison--selection)

## 🎯 AWS Service Selection Wizard

### Step 1: What's Your Primary Use Case?
- **Web Applications** → EC2, ALB, RDS, CloudFront, Route 53
- **Data Analytics** → S3, Glue, Athena, Redshift, QuickSight
- **Machine Learning** → SageMaker, Bedrock, Comprehend, Rekognition
- **Mobile/IoT** → Amplify, IoT Core, Cognito, AppSync
- **Enterprise Migration** → Migration Hub, DMS, Server Migration Service

### Step 2: What's Your Scale Requirements?
- **Startup/Small** → Lightsail, RDS, S3, CloudFront
- **Growing Business** → EC2, ELB, RDS Multi-AZ, CloudWatch
- **Enterprise** → Auto Scaling, Multi-region, Reserved Instances
- **Global Scale** → Global Accelerator, CloudFront, Route 53

### Step 3: What's Your Budget Range?
- **Free Tier Only** → EC2 t2.micro, RDS db.t2.micro, S3 5GB
- **<$100/month** → Small EC2 instances, basic RDS, moderate S3
- **$100-1000/month** → Production workloads, multiple services
- **$1000+/month** → Enterprise features, premium support

### Step 4: What's Your Expertise Level?
- **Beginner** → Lightsail, Elastic Beanstalk, RDS
- **Intermediate** → EC2, VPC, Lambda, API Gateway
- **Advanced** → EKS, ECS, Custom VPC, Multi-account
- **Expert** → Landing Zones, Organizations, Custom Solutions

## 📊 Complete AWS Services Overview

### Compute Services (25+ Services)
| Service | Type | Use Case | Pricing Model | Free Tier | Complexity |
|---------|------|----------|---------------|-----------|------------|
| **EC2** | Virtual Machines | General compute | Per hour/second | 750 hours/month | Medium |
| **Lambda** | Serverless | Event-driven compute | Per request | 1M requests/month | Low |
| **ECS** | Container Service | Docker containers | EC2 + ECS charges | Limited | Medium |
| **EKS** | Kubernetes | Container orchestration | $0.10/hour + nodes | No | High |
| **Fargate** | Serverless Containers | Managed containers | Per vCPU/memory | Limited | Low |
| **Lightsail** | VPS | Simple applications | Fixed monthly | 1 month free | Low |
| **Batch** | Batch Computing | Large-scale processing | EC2 pricing | Limited | Medium |
| **Elastic Beanstalk** | PaaS | Web applications | Underlying resources | Yes | Low |
| **App Runner** | Container Service | Web apps from source | Per vCPU/memory | No | Low |
| **Outposts** | Hybrid | On-premises AWS | Hardware + software | No | High |

### Storage Services (15+ Services)
| Service | Type | Use Case | Durability | Availability | Cost/GB/Month |
|---------|------|----------|------------|--------------|---------------|
| **S3** | Object Storage | Web apps, backup | 99.999999999% | 99.99% | $0.023 |
| **EBS** | Block Storage | EC2 volumes | 99.999% | 99.999% | $0.10 |
| **EFS** | File Storage | Shared file system | 99.999999999% | 99.99% | $0.30 |
| **FSx** | Managed File Systems | High-performance | 99.999% | 99.99% | $0.65+ |
| **S3 Glacier** | Archive Storage | Long-term backup | 99.999999999% | 99.99% | $0.004 |
| **Storage Gateway** | Hybrid Storage | On-premises integration | Varies | 99.9% | Varies |
| **DataSync** | Data Transfer | Migration/sync | N/A | 99.9% | $0.0125/GB |
| **Snow Family** | Data Migration | Petabyte transfers | N/A | Physical | Device rental |
| **Backup** | Backup Service | Centralized backup | 99.999999999% | 99.9% | $0.05/GB |

### Database Services (20+ Services)
| Service | Type | Engine | Use Case | Pricing | Managed |
|---------|------|--------|----------|---------|---------|
| **RDS** | Relational | MySQL, PostgreSQL, etc. | OLTP | Per hour + storage | Yes |
| **Aurora** | Relational | MySQL/PostgreSQL compatible | High performance | Per hour + I/O | Yes |
| **DynamoDB** | NoSQL | Key-value/document | High scale | Per request/storage | Yes |
| **DocumentDB** | Document | MongoDB compatible | Document apps | Per hour | Yes |
| **Neptune** | Graph | Property graph/RDF | Graph queries | Per hour | Yes |
| **Timestream** | Time-series | Time-series data | IoT/monitoring | Per query/storage | Yes |
| **QLDB** | Ledger | Immutable ledger | Financial records | Per request | Yes |
| **ElastiCache** | In-memory | Redis/Memcached | Caching | Per hour | Yes |
| **Redshift** | Data Warehouse | Columnar | Analytics | Per hour | Yes |
| **EMR** | Big Data | Hadoop/Spark | Big data processing | Per hour | Partial |

### Networking & Content Delivery (20+ Services)
| Service | Type | Use Case | Global | Performance | Cost Model |
|---------|------|----------|--------|-------------|------------|
| **VPC** | Virtual Network | Network isolation | Regional | High | Free |
| **CloudFront** | CDN | Content delivery | Global | Excellent | Per request/GB |
| **Route 53** | DNS | Domain management | Global | High | Per query |
| **ELB** | Load Balancer | Traffic distribution | Regional | High | Per hour + LCU |
| **API Gateway** | API Management | REST/GraphQL APIs | Regional | Good | Per request |
| **Direct Connect** | Dedicated Network | Hybrid connectivity | Regional | Excellent | Port hours + data |
| **Transit Gateway** | Network Hub | Multi-VPC connectivity | Regional | High | Per hour + data |
| **Global Accelerator** | Network Accelerator | Global performance | Global | Excellent | Fixed + data |
| **App Mesh** | Service Mesh | Microservices | Regional | Good | Free |
| **Cloud Map** | Service Discovery | Service registry | Regional | Good | Per query |

### Security & Identity (25+ Services)
| Service | Type | Use Case | Integration | Compliance | Cost |
|---------|------|----------|-------------|------------|------|
| **IAM** | Identity Management | Access control | All services | SOC/PCI | Free |
| **Cognito** | User Management | App authentication | Mobile/web | HIPAA | Per MAU |
| **SSO** | Single Sign-On | Enterprise SSO | SAML/OIDC | SOC | Per user |
| **Directory Service** | Managed AD | Windows authentication | EC2/RDS | HIPAA | Per hour |
| **Secrets Manager** | Secret Storage | API keys/passwords | All services | FIPS | Per secret |
| **KMS** | Key Management | Encryption keys | All services | FIPS 140-2 | Per key/request |
| **CloudHSM** | Hardware Security | Dedicated HSM | Limited | FIPS 140-2 L3 | Per hour |
| **Certificate Manager** | SSL/TLS Certs | Certificate management | ELB/CloudFront | Free | Free |
| **WAF** | Web Firewall | Application protection | ALB/CloudFront | OWASP | Per rule/request |
| **Shield** | DDoS Protection | DDoS mitigation | Global | Advanced | Free/Premium |

### Analytics & Big Data (20+ Services)
| Service | Type | Use Case | Data Sources | Query Language | Pricing |
|---------|------|----------|--------------|----------------|---------|
| **Athena** | Query Service | S3 data analysis | S3 | SQL | Per query |
| **Glue** | ETL Service | Data preparation | Multiple | Python/Scala | Per DPU hour |
| **EMR** | Big Data | Hadoop/Spark | Multiple | Multiple | Per hour |
| **Redshift** | Data Warehouse | Analytics | Multiple | SQL | Per hour |
| **QuickSight** | BI Tool | Dashboards | Multiple | Visual | Per user |
| **Kinesis** | Streaming | Real-time data | Multiple | SQL/Java | Per shard/record |
| **MSK** | Kafka | Message streaming | Applications | Kafka API | Per broker hour |
| **Data Pipeline** | Workflow | Data movement | Multiple | JSON | Per pipeline |
| **Lake Formation** | Data Lake | Data lake setup | S3 | SQL | Storage costs |
| **DataBrew** | Data Prep | Visual data prep | Multiple | Visual | Per session |

### Machine Learning & AI (30+ Services)
| Service | Type | Use Case | Skill Level | Pre-trained | Custom Training |
|---------|------|----------|-------------|-------------|-----------------|
| **SageMaker** | ML Platform | Full ML lifecycle | Advanced | Limited | Yes |
| **Bedrock** | Generative AI | LLM applications | Intermediate | Yes | Limited |
| **Comprehend** | NLP | Text analysis | Beginner | Yes | Yes |
| **Rekognition** | Computer Vision | Image/video analysis | Beginner | Yes | Yes |
| **Polly** | Text-to-Speech | Voice synthesis | Beginner | Yes | No |
| **Transcribe** | Speech-to-Text | Audio transcription | Beginner | Yes | Yes |
| **Translate** | Translation | Language translation | Beginner | Yes | No |
| **Textract** | Document Analysis | Text extraction | Beginner | Yes | No |
| **Forecast** | Forecasting | Time series prediction | Intermediate | Yes | Yes |
| **Personalize** | Recommendations | Recommendation engine | Intermediate | Yes | Yes |

### Developer Tools (15+ Services)
| Service | Type | Use Case | Integration | Pricing | Complexity |
|---------|------|----------|-------------|---------|------------|
| **CodeCommit** | Git Repository | Source control | CodePipeline | Per user | Low |
| **CodeBuild** | Build Service | CI/CD builds | Multiple | Per build minute | Medium |
| **CodeDeploy** | Deployment | Application deployment | EC2/Lambda | Free | Medium |
| **CodePipeline** | CI/CD Pipeline | Release automation | Multiple | Per pipeline | Medium |
| **Cloud9** | IDE | Cloud development | Multiple | EC2 costs | Low |
| **X-Ray** | Tracing | Application monitoring | Multiple | Per trace | Low |
| **CloudFormation** | IaC | Infrastructure as code | All services | Free | High |
| **CDK** | IaC Framework | Programmatic IaC | CloudFormation | Free | Medium |
| **Systems Manager** | Operations | System management | EC2 | Free/Premium | Medium |
| **CloudWatch** | Monitoring | Metrics and logs | All services | Per metric/log | Low |

## 🏗️ AWS Architecture Patterns

### Three-Tier Web Application
```
Internet Gateway
    ↓
Application Load Balancer (Public Subnet)
    ↓
EC2 Instances (Private Subnet)
    ↓
RDS Database (Private Subnet)
```
**Services**: VPC, ALB, EC2, RDS, Route 53, CloudFront
**Cost**: $200-500/month for small-medium scale

### Serverless Web Application
```
Route 53 → CloudFront → S3 (Static) → API Gateway → Lambda → DynamoDB
```
**Services**: S3, CloudFront, API Gateway, Lambda, DynamoDB, Cognito
**Cost**: $50-200/month for moderate traffic

### Data Lake Architecture
```
Data Sources → Kinesis → S3 Data Lake → Glue ETL → Redshift/Athena → QuickSight
```
**Services**: Kinesis, S3, Glue, Athena, Redshift, QuickSight, Lake Formation
**Cost**: $500-5000/month depending on data volume

### Microservices on EKS
```
ALB → EKS Cluster → Microservices → RDS/DynamoDB
                 → Service Mesh (App Mesh)
```
**Services**: EKS, ALB, RDS, DynamoDB, App Mesh, ECR, CloudWatch
**Cost**: $1000-10000/month depending on scale

### Machine Learning Pipeline
```
S3 Data → SageMaker Processing → SageMaker Training → SageMaker Endpoints
       → SageMaker Pipelines → Model Registry
```
**Services**: SageMaker, S3, ECR, CloudWatch, IAM
**Cost**: $500-5000/month depending on compute requirements

## ⚡ Performance & Scalability

### Compute Performance Comparison
| Service | vCPU Performance | Memory Options | Network Performance | Storage Performance |
|---------|------------------|----------------|-------------------|-------------------|
| **EC2 (c5.large)** | 2 vCPU (3.0 GHz) | 4 GB | Up to 10 Gbps | EBS-optimized |
| **Lambda** | Variable | 128MB - 10GB | Good | Ephemeral only |
| **Fargate** | 0.25-4 vCPU | 0.5-30 GB | Good | Ephemeral + EFS |
| **ECS on EC2** | EC2 performance | EC2 memory | EC2 network | EC2 storage |

### Database Performance Benchmarks
| Service | Read IOPS | Write IOPS | Latency | Max Connections | Scaling |
|---------|-----------|------------|---------|-----------------|---------|
| **RDS MySQL** | 3,000-40,000 | 1,000-20,000 | 1-5ms | 16,000 | Vertical |
| **Aurora MySQL** | 500,000+ | 100,000+ | <1ms | 16,000 | Auto-scaling |
| **DynamoDB** | Unlimited | Unlimited | <10ms | Unlimited | Auto-scaling |
| **ElastiCache Redis** | 250,000+ | 100,000+ | <1ms | 65,000 | Cluster mode |

### Storage Performance Comparison
| Service | Throughput | IOPS | Latency | Durability | Availability |
|---------|------------|------|---------|------------|--------------|
| **EBS gp3** | 1,000 MB/s | 16,000 | Single-digit ms | 99.999% | 99.999% |
| **EBS io2** | 4,000 MB/s | 64,000 | Single-digit ms | 99.999% | 99.999% |
| **EFS** | 10+ GB/s | 500,000+ | Low ms | 99.999999999% | 99.99% |
| **S3** | 5,500 requests/s | N/A | 100-200ms | 99.999999999% | 99.99% |

### Network Performance
| Service | Bandwidth | Latency | Global Reach | Availability |
|---------|-----------|---------|--------------|--------------|
| **CloudFront** | 100+ Tbps | <50ms | 400+ PoPs | 99.99% |
| **Global Accelerator** | AWS backbone | 60% improvement | Global | 99.99% |
| **Direct Connect** | 1-100 Gbps | <10ms | Regional | 99.9% |
| **VPC Peering** | 25 Gbps | <1ms | Regional/Cross-region | 99.99% |

## 💰 Cost Analysis & Optimization

### Service Cost Comparison (Monthly estimates)
| Service Category | Small Workload | Medium Workload | Large Workload | Enterprise |
|------------------|----------------|-----------------|----------------|------------|
| **Compute (EC2)** | $20-100 | $200-1,000 | $2,000-10,000 | $20,000+ |
| **Storage (S3)** | $5-25 | $50-250 | $500-2,500 | $5,000+ |
| **Database (RDS)** | $15-75 | $150-750 | $1,500-7,500 | $15,000+ |
| **Networking** | $10-50 | $100-500 | $1,000-5,000 | $10,000+ |
| **Analytics** | $10-100 | $100-1,000 | $1,000-10,000 | $25,000+ |

### Cost Optimization Strategies
| Strategy | Potential Savings | Implementation Effort | Risk Level |
|----------|------------------|----------------------|------------|
| **Reserved Instances** | 30-60% | Low | Low |
| **Spot Instances** | 50-90% | Medium | Medium |
| **Right-sizing** | 20-40% | Medium | Low |
| **S3 Storage Classes** | 30-80% | Low | Low |
| **Auto Scaling** | 20-50% | Medium | Low |
| **Lambda vs EC2** | 20-70% | High | Medium |

### Free Tier Limits (12 months)
| Service | Free Tier Limit | Value | After Free Tier |
|---------|-----------------|-------|-----------------|
| **EC2** | 750 hours t2.micro | $8.50/month | $8.50/month |
| **RDS** | 750 hours db.t2.micro | $15/month | $15/month |
| **S3** | 5 GB storage | $0.12/month | $0.023/GB |
| **Lambda** | 1M requests | $0.20/month | $0.20/1M requests |
| **CloudFront** | 50 GB data transfer | $4.25/month | $0.085/GB |

### Regional Pricing Differences
| Service | US East (N. Virginia) | US West (Oregon) | Europe (Ireland) | Asia Pacific (Tokyo) |
|---------|----------------------|------------------|------------------|---------------------|
| **EC2 t3.medium** | $0.0416/hour | $0.0416/hour | $0.0464/hour | $0.0544/hour |
| **RDS db.t3.micro** | $0.017/hour | $0.017/hour | $0.019/hour | $0.022/hour |
| **S3 Standard** | $0.023/GB | $0.023/GB | $0.024/GB | $0.025/GB |
| **Data Transfer** | $0.09/GB | $0.09/GB | $0.09/GB | $0.14/GB |

## 🔗 Service Integration Matrix

### Compute Integration
| Service | Storage | Database | Networking | Security | Monitoring |
|---------|---------|----------|------------|----------|------------|
| **EC2** | EBS, EFS, S3 | RDS, DynamoDB | VPC, ELB | IAM, Security Groups | CloudWatch |
| **Lambda** | S3, EFS | DynamoDB, RDS Proxy | API Gateway, VPC | IAM, Resource Policies | CloudWatch, X-Ray |
| **ECS** | EBS, EFS, S3 | RDS, DynamoDB | ALB, Service Discovery | IAM, Task Roles | CloudWatch, X-Ray |
| **EKS** | EBS, EFS, S3 | RDS, DynamoDB | ALB, Ingress | IAM, RBAC | CloudWatch, Prometheus |

### Data Services Integration
| Service | Data Sources | Processing | Storage | Analytics | Visualization |
|---------|--------------|------------|---------|-----------|---------------|
| **S3** | All services | Glue, EMR | Native | Athena, Redshift | QuickSight |
| **Glue** | S3, RDS, Redshift | Native ETL | S3, Redshift | Athena | QuickSight |
| **Athena** | S3, Glue Catalog | Presto engine | S3 | Native SQL | QuickSight |
| **Redshift** | S3, RDS, DynamoDB | Native | Native | Native SQL | QuickSight, Tableau |

### Security Integration
| Service | Identity | Encryption | Network | Compliance | Monitoring |
|---------|----------|------------|---------|------------|------------|
| **IAM** | All services | KMS integration | VPC policies | CloudTrail | CloudWatch |
| **Cognito** | Web/mobile apps | KMS | API Gateway | HIPAA ready | CloudWatch |
| **KMS** | All services | Native | VPC endpoints | FIPS 140-2 | CloudTrail |
| **WAF** | ALB, CloudFront | TLS | Regional/Global | OWASP | CloudWatch |

## 📚 Learning & Certification Paths

### AWS Certification Roadmap
| Level | Certification | Prerequisites | Study Time | Validity | Cost |
|-------|---------------|---------------|------------|----------|------|
| **Foundational** | Cloud Practitioner | None | 1-2 months | 3 years | $100 |
| **Associate** | Solutions Architect | 6 months experience | 2-3 months | 3 years | $150 |
| **Associate** | Developer | 1 year development | 2-3 months | 3 years | $150 |
| **Associate** | SysOps Administrator | 1 year operations | 2-3 months | 3 years | $150 |
| **Professional** | Solutions Architect | Associate level | 4-6 months | 3 years | $300 |
| **Professional** | DevOps Engineer | Associate level | 4-6 months | 3 years | $300 |
| **Specialty** | Security | 2 years security | 3-4 months | 3 years | $300 |
| **Specialty** | Machine Learning | ML experience | 3-4 months | 3 years | $300 |

### Learning Resources by Service Category
| Category | Getting Started | Hands-on Labs | Documentation | Community |
|----------|----------------|---------------|---------------|-----------|
| **Compute** | [EC2 Getting Started](https://docs.aws.amazon.com/ec2/latest/userguide/EC2_GetStarted.html) | [AWS Workshops](https://workshops.aws/) | [EC2 User Guide](https://docs.aws.amazon.com/ec2/) | r/aws (300K+) |
| **Storage** | [S3 Getting Started](https://docs.aws.amazon.com/s3/latest/userguide/GetStartedWithS3.html) | [S3 Workshops](https://s3workshops.com/) | [S3 User Guide](https://docs.aws.amazon.com/s3/) | AWS Forums |
| **Database** | [RDS Getting Started](https://docs.aws.amazon.com/rds/latest/userguide/CHAP_GettingStarted.html) | [Database Workshops](https://github.com/aws-samples/aws-database-migration-samples) | [RDS User Guide](https://docs.aws.amazon.com/rds/) | AWS Database Blog |
| **Analytics** | [Analytics Getting Started](https://aws.amazon.com/big-data/getting-started/) | [Analytics Workshops](https://github.com/aws-samples/aws-analytics-reference-architecture) | [Analytics Documentation](https://docs.aws.amazon.com/analytics/) | AWS Big Data Blog |

### Hands-on Learning Platforms
| Platform | Cost | Content Quality | Hands-on Labs | Certification Prep |
|----------|------|----------------|---------------|-------------------|
| **AWS Training** | Free/Paid | Excellent | Yes | Official |
| **A Cloud Guru** | $39/month | Good | Yes | Excellent |
| **Linux Academy** | $49/month | Excellent | Yes | Excellent |
| **Udemy** | $10-200/course | Variable | Limited | Good |
| **Coursera** | $39/month | Good | Limited | Good |
| **Pluralsight** | $29/month | Good | Limited | Good |

## 🆚 Service Comparison & Selection

### Compute Service Selection
| Use Case | Recommended Service | Alternative | Reason |
|----------|-------------------|-------------|--------|
| **Web Applications** | EC2 + ALB | Lightsail | More control and scalability |
| **APIs** | Lambda + API Gateway | ECS Fargate | Cost-effective for variable load |
| **Batch Processing** | Batch | EC2 Spot | Managed service with auto-scaling |
| **Containers** | EKS | ECS | Better for complex orchestration |
| **Simple Websites** | Lightsail | EC2 | Fixed pricing and simplicity |

### Database Service Selection
| Use Case | Recommended Service | Alternative | Reason |
|----------|-------------------|-------------|--------|
| **OLTP Applications** | RDS | Aurora | Cost-effective for moderate scale |
| **High Performance** | Aurora | RDS | Better performance and scaling |
| **NoSQL/Flexible** | DynamoDB | DocumentDB | Serverless and auto-scaling |
| **Analytics** | Redshift | Athena | Better for complex queries |
| **Caching** | ElastiCache | DynamoDB DAX | More flexible caching options |

### Storage Service Selection
| Use Case | Recommended Service | Alternative | Reason |
|----------|-------------------|-------------|--------|
| **Web Assets** | S3 + CloudFront | EFS | Better performance and global reach |
| **File Shares** | EFS | FSx | POSIX compliance and scalability |
| **Backup/Archive** | S3 Glacier | S3 IA | Lower cost for long-term storage |
| **High Performance** | EBS io2 | EFS | Consistent high IOPS |
| **Big Data** | S3 | EFS | Better integration with analytics |

### Analytics Service Selection
| Use Case | Recommended Service | Alternative | Reason |
|----------|-------------------|-------------|--------|
| **Ad-hoc Queries** | Athena | Redshift | Pay-per-query model |
| **Data Warehouse** | Redshift | Athena | Better for complex analytics |
| **ETL Processing** | Glue | EMR | Serverless and managed |
| **Real-time Analytics** | Kinesis Analytics | EMR | Stream processing capabilities |
| **Business Intelligence** | QuickSight | Tableau on EC2 | Native AWS integration |

## 🎯 Decision Framework

### Choose Based on Your Architecture

#### Startup/MVP (< $1K/month)
- **Compute**: Lambda + API Gateway
- **Database**: DynamoDB
- **Storage**: S3
- **CDN**: CloudFront
- **Monitoring**: CloudWatch (basic)

#### Growing Business ($1K-10K/month)
- **Compute**: EC2 + Auto Scaling
- **Database**: RDS Multi-AZ
- **Storage**: S3 + EBS
- **Load Balancing**: ALB
- **Monitoring**: CloudWatch + X-Ray

#### Enterprise ($10K+/month)
- **Compute**: EKS or ECS
- **Database**: Aurora + DynamoDB
- **Storage**: S3 + EFS + FSx
- **Networking**: Transit Gateway
- **Security**: Organizations + SSO
- **Monitoring**: Full observability stack

#### Data-Intensive Applications
- **Storage**: S3 Data Lake
- **Processing**: Glue + EMR
- **Analytics**: Athena + Redshift
- **ML**: SageMaker
- **Visualization**: QuickSight

## 📈 Market Trends & Future Outlook

### Growing AWS Services (2024-2026)
- **Bedrock**: Generative AI and LLM services
- **EKS**: Container orchestration adoption
- **SageMaker**: Machine learning democratization
- **Lambda**: Serverless computing expansion
- **Aurora Serverless**: Auto-scaling databases

### Stable Services
- **EC2**: Core compute foundation
- **S3**: Object storage standard
- **RDS**: Managed database leader
- **CloudFront**: CDN market leader
- **IAM**: Identity and access management

### Evolving Services
- **Lightsail**: Competing with DigitalOcean/Linode
- **WorkSpaces**: Remote work solutions
- **AppStream**: Application streaming
- **Ground Station**: Satellite data processing
- **Braket**: Quantum computing

### Service Retirement/Deprecation
- **SimpleDB**: Replaced by DynamoDB
- **Cloud9**: Limited adoption
- **CodeStar**: Integrated into other services
- **Mobile Hub**: Replaced by Amplify

---

*Last Updated: December 2024 | Services Covered: 320+ | Regions: 31 | Availability Zones: 99*

**🎯 Quick Navigation**: [Azure Services](../Azure/) | [GCP Services](../GCP/) | [Data Processing](../../Data-Processing/) | [DevOps Tools](../../../Supporting-Tools/DevOps-Automation/)