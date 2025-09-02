# AWS All Services Reference (300+ Services)

## 🎯 Overview
Comprehensive table of all AWS services with descriptions, primary use cases, and official documentation links.

## 📊 Complete AWS Services Table

| Service Name | Category | Status | Description | Primary Use Cases | Pricing Model | Key Integrations | Documentation Link |
|--------------|----------|--------|-------------|-------------------|---------------|------------------|-------------------|
| **Amazon EC2** | Compute | 🟢 GA | Resizable virtual servers providing secure, scalable compute capacity in the cloud with various instance types optimized for different workloads | Web applications, data processing, development environments, high-performance computing, enterprise applications | Pay-per-hour, Reserved Instances, Spot Instances | VPC, EBS, ELB, Auto Scaling, CloudWatch | [docs.aws.amazon.com/ec2](https://docs.aws.amazon.com/ec2/) |
| **AWS Lambda** | Compute | 🟢 GA | Event-driven serverless compute service that runs code without provisioning servers, automatically scaling and charging only for compute time used | Real-time file processing, stream processing, API backends, ETL operations, IoT backends, chatbots | Pay-per-request, Pay-per-duration | API Gateway, S3, DynamoDB, EventBridge, CloudWatch | [docs.aws.amazon.com/lambda](https://docs.aws.amazon.com/lambda/) |
| **Amazon ECS** | Compute | 🟢 GA | Fully managed container orchestration service that makes it easy to deploy, manage, and scale containerized applications using Docker | Microservices architectures, batch processing, machine learning applications, web applications | Pay for underlying EC2/Fargate resources | ECR, Fargate, ELB, CloudWatch, VPC | [docs.aws.amazon.com/ecs](https://docs.aws.amazon.com/ecs/) |
| **Amazon EKS** | Compute | 🟢 GA | Fully managed Kubernetes service that runs upstream Kubernetes and is certified Kubernetes conformant for predictable behavior | Cloud-native applications, microservices, CI/CD pipelines, machine learning workloads, hybrid deployments | $0.10/hour per cluster + worker node costs | EC2, Fargate, ECR, ELB, VPC, IAM | [docs.aws.amazon.com/eks](https://docs.aws.amazon.com/eks/) |
| **AWS Fargate** | Compute | 🟢 GA | Serverless compute engine for containers that removes the need to provision and manage servers, letting you focus on applications | Containerized applications without infrastructure management, microservices, batch jobs, web applications | Pay-per-vCPU and memory per second | ECS, EKS, ECR, CloudWatch, VPC | [docs.aws.amazon.com/fargate](https://docs.aws.amazon.com/fargate/) |
| **AWS Batch** | Compute | 🟢 GA | Fully managed service for running batch computing workloads at any scale, dynamically provisioning optimal compute resources | Scientific computing, financial risk modeling, drug discovery, image processing, genomics analysis | Pay for underlying compute resources | EC2, Spot Instances, ECS, CloudWatch | [docs.aws.amazon.com/batch](https://docs.aws.amazon.com/batch/) |
| **Amazon Lightsail** | Compute | 🟢 GA | Easy-to-use virtual private server instances, containers, storage, databases, and networking with predictable pricing | Simple web applications, development environments, small business websites, e-commerce sites | Fixed monthly pricing plans | Route 53, CloudFront, Load Balancer | [docs.aws.amazon.com/lightsail](https://docs.aws.amazon.com/lightsail/) |
| **AWS Outposts** | Compute | 🟢 GA | Fully managed service that extends AWS infrastructure, services, APIs, and tools to on-premises facilities for hybrid cloud architecture | Low-latency applications, local data processing, data residency requirements, hybrid cloud workloads | Monthly subscription + hardware costs | EC2, EBS, S3, VPC, ECS, EKS | [docs.aws.amazon.com/outposts](https://docs.aws.amazon.com/outposts/) |
| **AWS Wavelength** | Compute | 🟢 GA | Infrastructure deployments that embed AWS compute and storage services at 5G network edge to minimize latency for mobile applications | Augmented/virtual reality, autonomous vehicles, IoT applications, real-time gaming, live video streaming | Pay-per-use for compute and storage | EC2, EBS, VPC, carrier networks | [docs.aws.amazon.com/wavelength](https://docs.aws.amazon.com/wavelength/) |
| **AWS Local Zones** | Compute | 🟢 GA | Infrastructure deployments that place compute, storage, database, and other AWS services closer to end-users for ultra-low latency | Real-time gaming, live streaming, augmented reality, machine learning inference at the edge | Standard AWS pricing for services | EC2, EBS, FSx, ELB, VPC | [docs.aws.amazon.com/local-zones](https://docs.aws.amazon.com/local-zones/) |
| **Amazon S3** | Storage | Highly scalable object storage service offering industry-leading durability, availability, performance, and security for data lakes, websites, backup, and analytics | Data lakes, backup and restore, disaster recovery, static website hosting, content distribution, big data analytics | [docs.aws.amazon.com/s3](https://docs.aws.amazon.com/s3/) |
| **Amazon EBS** | Storage | High-performance block storage service designed for use with EC2 instances for both throughput and transaction intensive workloads | Database storage, file systems, boot volumes, enterprise applications, distributed file systems | [docs.aws.amazon.com/ebs](https://docs.aws.amazon.com/ebs/) |
| **Amazon EFS** | Storage | Fully managed, elastic NFS file system that provides shared storage for EC2 instances with automatic scaling and high availability | Content repositories, web serving, data analytics, WordPress sites, enterprise applications requiring shared storage | [docs.aws.amazon.com/efs](https://docs.aws.amazon.com/efs/) |
| **Amazon FSx** | Storage | Fully managed file systems optimized for compute-intensive workloads including high-performance computing, machine learning, and media processing | High-performance computing, machine learning training, media processing, financial modeling, electronic design automation | [docs.aws.amazon.com/fsx](https://docs.aws.amazon.com/fsx/) |
| **AWS Storage Gateway** | Storage | Hybrid cloud storage service that connects on-premises environments to AWS cloud storage services like S3, Glacier, and EBS | Backup to cloud, disaster recovery, data archiving, content distribution, hybrid cloud storage | [docs.aws.amazon.com/storagegateway](https://docs.aws.amazon.com/storagegateway/) |
| **AWS Backup** | Storage | Centralized backup service that automates and consolidates backup tasks across AWS services with policy-based backup solutions | Data protection, compliance requirements, disaster recovery, centralized backup management across AWS services | [docs.aws.amazon.com/backup](https://docs.aws.amazon.com/backup/) |
| **Amazon S3 Glacier** | Storage | Secure, durable, and extremely low-cost cloud storage service for data archiving and long-term backup with retrieval options from minutes to hours | Long-term archiving, digital preservation, compliance, backup, disaster recovery, media asset archiving | [docs.aws.amazon.com/glacier](https://docs.aws.amazon.com/glacier/) |
| **AWS Snow Family** | Storage | Physical data transport devices that help move large amounts of data into and out of AWS using secure, portable devices | Large-scale data migrations, disaster recovery, content distribution, data center decommission, remote data collection | [docs.aws.amazon.com/snow](https://docs.aws.amazon.com/snow/) |
| **Amazon RDS** | Database | Fully managed relational database service supporting MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Amazon Aurora with automated backups, patching, and scaling | Web applications, e-commerce platforms, enterprise applications, online gaming, mobile applications | [docs.aws.amazon.com/rds](https://docs.aws.amazon.com/rds/) |
| **Amazon Aurora** | Database | MySQL and PostgreSQL-compatible relational database with up to 5x better performance than MySQL and 3x better than PostgreSQL with cloud-native architecture | Enterprise applications, SaaS applications, web applications requiring high performance and availability | [docs.aws.amazon.com/aurora](https://docs.aws.amazon.com/aurora/) |
| **Amazon DynamoDB** | Database | Fully managed NoSQL database service providing fast and predictable performance with seamless scalability and single-digit millisecond latency | Mobile applications, web applications, gaming, IoT, real-time bidding, social media applications | [docs.aws.amazon.com/dynamodb](https://docs.aws.amazon.com/dynamodb/) |
| **Amazon DocumentDB** | Database | Fully managed document database service compatible with MongoDB workloads, providing scalability, durability, and security | Content management, catalogs, user profiles, document-based applications, mobile applications | [docs.aws.amazon.com/documentdb](https://docs.aws.amazon.com/documentdb/) |
| **Amazon Neptune** | Database | Fully managed graph database service optimized for storing billions of relationships with millisecond latency for highly connected datasets | Social networking, recommendation engines, fraud detection, knowledge graphs, network security, life sciences | [docs.aws.amazon.com/neptune](https://docs.aws.amazon.com/neptune/) |
| **Amazon Redshift** | Database | Fully managed petabyte-scale data warehouse service using columnar storage and massively parallel processing for fast query performance | Business intelligence, reporting, data analytics, data lakes, machine learning, real-time analytics | [docs.aws.amazon.com/redshift](https://docs.aws.amazon.com/redshift/) |
| **Amazon ElastiCache** | Database | Fully managed in-memory caching service supporting Redis and Memcached for microsecond latency and high throughput applications | Session stores, gaming leaderboards, streaming, analytics, caching, chat/messaging applications | [docs.aws.amazon.com/elasticache](https://docs.aws.amazon.com/elasticache/) |
| **Amazon Timestream** | Database | Fully managed time series database service for IoT and operational applications with built-in time series analytics functions | IoT applications, DevOps monitoring, application monitoring, industrial telemetry, smart city applications | [docs.aws.amazon.com/timestream](https://docs.aws.amazon.com/timestream/) |
| **Amazon QLDB** | Database | Fully managed ledger database providing transparent, immutable, and cryptographically verifiable transaction log for applications requiring complete audit trail | Financial transactions, supply chain, registrations, claims processing, centralized digital records | [docs.aws.amazon.com/qldb](https://docs.aws.amazon.com/qldb/) |
| **Amazon Keyspaces** | Database | Scalable, highly available, and managed Apache Cassandra-compatible database service for applications requiring fast performance at scale | High-scale applications, IoT applications, time-series data, personalization, real-time recommendations | [docs.aws.amazon.com/keyspaces](https://docs.aws.amazon.com/keyspaces/) |
| **Amazon MemoryDB** | Database | Redis-compatible, durable, in-memory database service delivering ultra-fast performance with Multi-AZ durability and strong consistency | Real-time applications, caching, session stores, gaming leaderboards, geospatial applications, machine learning | [docs.aws.amazon.com/memorydb](https://docs.aws.amazon.com/memorydb/) |
| **AWS VPC** | Networking | Virtual private cloud providing isolated network environment with complete control over virtual networking including IP address ranges, subnets, route tables, and network gateways | Network isolation, multi-tier applications, hybrid cloud architectures, secure application hosting | [docs.aws.amazon.com/vpc](https://docs.aws.amazon.com/vpc/) |
| **Amazon CloudFront** | Networking | Global content delivery network service that securely delivers data, videos, applications, and APIs with low latency and high transfer speeds | Global content distribution, video streaming, API acceleration, static/dynamic web content delivery | [docs.aws.amazon.com/cloudfront](https://docs.aws.amazon.com/cloudfront/) |
| **AWS Direct Connect** | Networking | Dedicated network connection service that provides private connectivity between AWS and your datacenter, office, or colocation environment | Hybrid cloud connectivity, large data transfers, consistent network performance, regulatory compliance | [docs.aws.amazon.com/directconnect](https://docs.aws.amazon.com/directconnect/) |
| **Elastic Load Balancing** | Networking | Automatically distributes incoming application traffic across multiple targets such as EC2 instances, containers, and IP addresses in multiple Availability Zones | High availability applications, fault tolerance, auto scaling, microservices architectures | [docs.aws.amazon.com/elasticloadbalancing](https://docs.aws.amazon.com/elasticloadbalancing/) |
| **Amazon Route 53** | Networking | Highly available and scalable Domain Name System (DNS) web service with domain registration and health checking capabilities | Domain registration, DNS routing, traffic management, health monitoring, hybrid cloud architectures | [docs.aws.amazon.com/route53](https://docs.aws.amazon.com/route53/) |
| **AWS Global Accelerator** | Networking | Networking service that improves performance of applications with global users by directing traffic through AWS global network infrastructure | Global application acceleration, improved application performance, DDoS protection, traffic management | [docs.aws.amazon.com/global-accelerator](https://docs.aws.amazon.com/global-accelerator/) |
| **AWS Transit Gateway** | Networking | Network transit hub that connects VPCs and on-premises networks through a central hub, simplifying network architecture | Multi-VPC connectivity, hybrid cloud networking, network segmentation, centralized connectivity management | [docs.aws.amazon.com/transit-gateway](https://docs.aws.amazon.com/transit-gateway/) |
| **AWS PrivateLink** | Networking | Provides private connectivity between VPCs, AWS services, and on-premises applications without exposing traffic to the public internet | Secure service access, compliance requirements, private API access, hybrid architectures | [docs.aws.amazon.com/privatelink](https://docs.aws.amazon.com/privatelink/) |
| **AWS App Mesh** | Networking | Service mesh that provides application-level networking for microservices with end-to-end visibility and traffic control | Microservices communication, service discovery, traffic management, observability, canary deployments | [docs.aws.amazon.com/app-mesh](https://docs.aws.amazon.com/app-mesh/) |
| **AWS Cloud Map** | Networking | Service discovery service for cloud resources that maintains a map of backend services and their health status | Dynamic service discovery, microservices architectures, container orchestration, health monitoring | [docs.aws.amazon.com/cloud-map](https://docs.aws.amazon.com/cloud-map/) |
| **Amazon API Gateway** | Networking | Fully managed service for creating, publishing, maintaining, monitoring, and securing REST, HTTP, and WebSocket APIs at any scale | REST APIs, WebSocket APIs, serverless applications, microservices, mobile backends, API monetization | [docs.aws.amazon.com/apigateway](https://docs.aws.amazon.com/apigateway/) |
| **AWS IAM** | Security | Identity and Access Management service providing fine-grained access control across AWS services with users, groups, roles, and policies for secure resource access | User authentication, authorization, role-based access control, federated access, API security, compliance | [docs.aws.amazon.com/iam](https://docs.aws.amazon.com/iam/) |
| **AWS Cognito** | Security | User identity and data synchronization service providing authentication, authorization, and user management for web and mobile applications | User sign-up/sign-in, social identity providers, multi-factor authentication, mobile app user management | [docs.aws.amazon.com/cognito](https://docs.aws.amazon.com/cognito/) |
| **AWS Directory Service** | Security | Managed Microsoft Active Directory service enabling existing corporate credentials to access AWS resources and applications | Enterprise identity integration, single sign-on, LDAP applications, SharePoint, SQL Server integration | [docs.aws.amazon.com/directory-service](https://docs.aws.amazon.com/directory-service/) |
| **AWS KMS** | Security | Key Management Service for creating and controlling encryption keys used to encrypt data across AWS services and applications | Encryption key management, data protection, compliance, digital signing, envelope encryption | [docs.aws.amazon.com/kms](https://docs.aws.amazon.com/kms/) |
| **AWS CloudHSM** | Security | Cloud-based hardware security modules providing secure key storage and cryptographic operations in tamper-resistant hardware | High-security key storage, regulatory compliance, SSL/TLS processing, database encryption, code signing | [docs.aws.amazon.com/cloudhsm](https://docs.aws.amazon.com/cloudhsm/) |
| **AWS Secrets Manager** | Security | Service for securely storing, managing, and retrieving database credentials, API keys, and other secrets with automatic rotation | Database credentials, API keys, OAuth tokens, passwords management, automatic rotation, compliance | [docs.aws.amazon.com/secretsmanager](https://docs.aws.amazon.com/secretsmanager/) |
| **AWS Certificate Manager** | Security | Service for provisioning, managing, and deploying SSL/TLS certificates for use with AWS services and internal connected resources | SSL/TLS certificate provisioning, certificate renewal, load balancer certificates, CloudFront certificates | [docs.aws.amazon.com/acm](https://docs.aws.amazon.com/acm/) |
| **AWS WAF** | Security | Web application firewall protecting web applications from common web exploits and bots that could affect availability or security | SQL injection protection, cross-site scripting prevention, bot mitigation, API protection, DDoS protection | [docs.aws.amazon.com/waf](https://docs.aws.amazon.com/waf/) |
| **AWS Shield** | Security | Managed DDoS protection service safeguarding applications running on AWS against distributed denial of service attacks | DDoS protection, application availability, attack mitigation, real-time attack diagnostics, 24/7 support | [docs.aws.amazon.com/shield](https://docs.aws.amazon.com/shield/) |
| **Amazon GuardDuty** | Security | Threat detection service using machine learning to continuously monitor for malicious activity and unauthorized behavior | Malware detection, cryptocurrency mining, reconnaissance attacks, data exfiltration, compromised instances | [docs.aws.amazon.com/guardduty](https://docs.aws.amazon.com/guardduty/) |
| **Amazon Inspector** | Security | Automated security assessment service for applications to improve security and compliance by identifying vulnerabilities | Vulnerability assessment, security compliance, application security testing, network reachability analysis | [docs.aws.amazon.com/inspector](https://docs.aws.amazon.com/inspector/) |
| **AWS Security Hub** | Security | Central security service providing comprehensive view of security alerts and security posture across AWS accounts | Centralized security findings, compliance monitoring, security standards, automated remediation, security dashboards | [docs.aws.amazon.com/securityhub](https://docs.aws.amazon.com/securityhub/) |
| **AWS Macie** | Security | Data security service using machine learning to automatically discover, classify, and protect sensitive data in AWS | Sensitive data discovery, data classification, PII protection, compliance monitoring, data security analytics | [docs.aws.amazon.com/macie](https://docs.aws.amazon.com/macie/) |
| **AWS Config** | Security | Configuration management | Compliance monitoring | [docs.aws.amazon.com/config](https://docs.aws.amazon.com/config/) |
| **AWS CloudTrail** | Security | API logging service | Audit trails, compliance | [docs.aws.amazon.com/cloudtrail](https://docs.aws.amazon.com/cloudtrail/) |
| **Amazon Athena** | Analytics | Interactive query service | SQL queries on S3 data | [docs.aws.amazon.com/athena](https://docs.aws.amazon.com/athena/) |
| **AWS Glue** | Analytics | ETL service | Data preparation, cataloging | [docs.aws.amazon.com/glue](https://docs.aws.amazon.com/glue/) |
| **Amazon EMR** | Analytics | Big data platform | Spark, Hadoop processing | [docs.aws.amazon.com/emr](https://docs.aws.amazon.com/emr/) |
| **Amazon Kinesis** | Analytics | Real-time data streaming | Stream processing, analytics | [docs.aws.amazon.com/kinesis](https://docs.aws.amazon.com/kinesis/) |
| **Amazon QuickSight** | Analytics | Business intelligence service | Dashboards, visualizations | [docs.aws.amazon.com/quicksight](https://docs.aws.amazon.com/quicksight/) |
| **AWS Data Pipeline** | Analytics | Data workflow service | ETL orchestration | [docs.aws.amazon.com/datapipeline](https://docs.aws.amazon.com/datapipeline/) |
| **Amazon Elasticsearch** | Analytics | Search and analytics engine | Log analysis, search | [docs.aws.amazon.com/elasticsearch-service](https://docs.aws.amazon.com/elasticsearch-service/) |
| **AWS Lake Formation** | Analytics | Data lake service | Data lake setup, governance | [docs.aws.amazon.com/lake-formation](https://docs.aws.amazon.com/lake-formation/) |
| **Amazon MSK** | Analytics | Managed Kafka service | Stream processing | [docs.aws.amazon.com/msk](https://docs.aws.amazon.com/msk/) |
| **AWS Data Exchange** | Analytics | Data marketplace | Third-party data access | [docs.aws.amazon.com/data-exchange](https://docs.aws.amazon.com/data-exchange/) |
| **Amazon Forecast** | ML/AI | Time series forecasting | Demand forecasting | [docs.aws.amazon.com/forecast](https://docs.aws.amazon.com/forecast/) |
| **Amazon Personalize** | ML/AI | Recommendation engine | Personalized recommendations | [docs.aws.amazon.com/personalize](https://docs.aws.amazon.com/personalize/) |
| **Amazon Rekognition** | ML/AI | Image and video analysis | Computer vision applications | [docs.aws.amazon.com/rekognition](https://docs.aws.amazon.com/rekognition/) |
| **Amazon Textract** | ML/AI | Document text extraction | Document processing | [docs.aws.amazon.com/textract](https://docs.aws.amazon.com/textract/) |
| **Amazon Comprehend** | ML/AI | Natural language processing | Text analysis, sentiment | [docs.aws.amazon.com/comprehend](https://docs.aws.amazon.com/comprehend/) |
| **Amazon Translate** | ML/AI | Language translation service | Multi-language translation | [docs.aws.amazon.com/translate](https://docs.aws.amazon.com/translate/) |
| **Amazon Polly** | ML/AI | Text-to-speech service | Voice applications | [docs.aws.amazon.com/polly](https://docs.aws.amazon.com/polly/) |
| **Amazon Transcribe** | ML/AI | Speech-to-text service | Audio transcription | [docs.aws.amazon.com/transcribe](https://docs.aws.amazon.com/transcribe/) |
| **Amazon Lex** | ML/AI | Conversational AI service | Chatbots, voice interfaces | [docs.aws.amazon.com/lex](https://docs.aws.amazon.com/lex/) |
| **Amazon SageMaker** | ML/AI | Machine learning platform | ML model development | [docs.aws.amazon.com/sagemaker](https://docs.aws.amazon.com/sagemaker/) |
| **AWS DeepLens** | ML/AI | Deep learning camera | Computer vision projects | [docs.aws.amazon.com/deeplens](https://docs.aws.amazon.com/deeplens/) |
| **Amazon Bedrock** | ML/AI | Foundation models service | Generative AI applications | [docs.aws.amazon.com/bedrock](https://docs.aws.amazon.com/bedrock/) |
| **Amazon CodeWhisperer** | ML/AI | AI coding assistant | Code generation, suggestions | [docs.aws.amazon.com/codewhisperer](https://docs.aws.amazon.com/codewhisperer/) |
| **AWS CloudFormation** | Management | Infrastructure as code | Resource provisioning | [docs.aws.amazon.com/cloudformation](https://docs.aws.amazon.com/cloudformation/) |
| **AWS CloudWatch** | Management | Monitoring and observability | Metrics, logs, alarms | [docs.aws.amazon.com/cloudwatch](https://docs.aws.amazon.com/cloudwatch/) |
| **AWS Systems Manager** | Management | Operations management | System administration | [docs.aws.amazon.com/systems-manager](https://docs.aws.amazon.com/systems-manager/) |
| **AWS Organizations** | Management | Account management | Multi-account governance | [docs.aws.amazon.com/organizations](https://docs.aws.amazon.com/organizations/) |
| **AWS Control Tower** | Management | Landing zone setup | Multi-account setup | [docs.aws.amazon.com/controltower](https://docs.aws.amazon.com/controltower/) |
| **AWS Service Catalog** | Management | Service portfolio management | Standardized deployments | [docs.aws.amazon.com/servicecatalog](https://docs.aws.amazon.com/servicecatalog/) |
| **AWS Trusted Advisor** | Management | Best practices recommendations | Cost optimization, security | [docs.aws.amazon.com/support/trusted-advisor](https://docs.aws.amazon.com/support/trusted-advisor/) |
| **AWS Personal Health Dashboard** | Management | Service health notifications | Personalized service alerts | [docs.aws.amazon.com/health](https://docs.aws.amazon.com/health/) |
| **AWS License Manager** | Management | License tracking | Software license management | [docs.aws.amazon.com/license-manager](https://docs.aws.amazon.com/license-manager/) |
| **AWS Well-Architected Tool** | Management | Architecture review | Best practices assessment | [docs.aws.amazon.com/wellarchitected](https://docs.aws.amazon.com/wellarchitected/) |
| **AWS Resource Groups** | Management | Resource organization | Resource grouping and tagging | [docs.aws.amazon.com/resource-groups](https://docs.aws.amazon.com/resource-groups/) |
| **AWS Tag Editor** | Management | Resource tagging | Bulk resource tagging | [docs.aws.amazon.com/resource-groups/latest/userguide/tag-editor.html](https://docs.aws.amazon.com/resource-groups/latest/userguide/tag-editor.html) |
| **Amazon SES** | Application Integration | Email service | Transactional emails | [docs.aws.amazon.com/ses](https://docs.aws.amazon.com/ses/) |
| **Amazon SNS** | Application Integration | Notification service | Push notifications, messaging | [docs.aws.amazon.com/sns](https://docs.aws.amazon.com/sns/) |
| **Amazon SQS** | Application Integration | Message queuing service | Decoupled applications | [docs.aws.amazon.com/sqs](https://docs.aws.amazon.com/sqs/) |
| **AWS Step Functions** | Application Integration | Workflow orchestration | Serverless workflows | [docs.aws.amazon.com/step-functions](https://docs.aws.amazon.com/step-functions/) |
| **Amazon EventBridge** | Application Integration | Event bus service | Event-driven architectures | [docs.aws.amazon.com/eventbridge](https://docs.aws.amazon.com/eventbridge/) |
| **AWS AppSync** | Application Integration | GraphQL service | Real-time APIs | [docs.aws.amazon.com/appsync](https://docs.aws.amazon.com/appsync/) |
| **Amazon MQ** | Application Integration | Managed message broker | Enterprise messaging | [docs.aws.amazon.com/amazon-mq](https://docs.aws.amazon.com/amazon-mq/) |
| **AWS CodeCommit** | Developer Tools | Git repositories | Source code management | [docs.aws.amazon.com/codecommit](https://docs.aws.amazon.com/codecommit/) |
| **AWS CodeBuild** | Developer Tools | Build service | Continuous integration | [docs.aws.amazon.com/codebuild](https://docs.aws.amazon.com/codebuild/) |
| **AWS CodeDeploy** | Developer Tools | Deployment service | Application deployment | [docs.aws.amazon.com/codedeploy](https://docs.aws.amazon.com/codedeploy/) |
| **AWS CodePipeline** | Developer Tools | CI/CD pipeline | Continuous delivery | [docs.aws.amazon.com/codepipeline](https://docs.aws.amazon.com/codepipeline/) |
| **AWS CodeStar** | Developer Tools | Development projects | Project templates | [docs.aws.amazon.com/codestar](https://docs.aws.amazon.com/codestar/) |
| **AWS Cloud9** | Developer Tools | Cloud IDE | Web-based development | [docs.aws.amazon.com/cloud9](https://docs.aws.amazon.com/cloud9/) |
| **AWS X-Ray** | Developer Tools | Application tracing | Performance analysis | [docs.aws.amazon.com/xray](https://docs.aws.amazon.com/xray/) |
| **AWS CodeArtifact** | Developer Tools | Artifact repository | Package management | [docs.aws.amazon.com/codeartifact](https://docs.aws.amazon.com/codeartifact/) |
| **AWS CodeGuru** | Developer Tools | Code review and profiling | Code optimization | [docs.aws.amazon.com/codeguru](https://docs.aws.amazon.com/codeguru/) |
| **AWS Amplify** | Mobile | Full-stack development | Mobile/web app development | [docs.aws.amazon.com/amplify](https://docs.aws.amazon.com/amplify/) |
| **AWS Device Farm** | Mobile | Mobile testing service | App testing on real devices | [docs.aws.amazon.com/devicefarm](https://docs.aws.amazon.com/devicefarm/) |
| **Amazon Pinpoint** | Mobile | Customer engagement | Marketing campaigns | [docs.aws.amazon.com/pinpoint](https://docs.aws.amazon.com/pinpoint/) |
| **AWS AppSync** | Mobile | GraphQL backend | Real-time mobile APIs | [docs.aws.amazon.com/appsync](https://docs.aws.amazon.com/appsync/) |
| **Amazon Location Service** | Mobile | Location-based services | Maps, geocoding, routing | [docs.aws.amazon.com/location](https://docs.aws.amazon.com/location/) |
| **AWS IoT Core** | IoT | IoT device connectivity | Device management | [docs.aws.amazon.com/iot](https://docs.aws.amazon.com/iot/) |
| **AWS IoT Device Management** | IoT | IoT device fleet management | Device provisioning | [docs.aws.amazon.com/iot-device-management](https://docs.aws.amazon.com/iot-device-management/) |
| **AWS IoT Analytics** | IoT | IoT data analytics | IoT data processing | [docs.aws.amazon.com/iotanalytics](https://docs.aws.amazon.com/iotanalytics/) |
| **AWS IoT Events** | IoT | IoT event detection | Event monitoring | [docs.aws.amazon.com/iotevents](https://docs.aws.amazon.com/iotevents/) |
| **AWS IoT Greengrass** | IoT | Edge computing for IoT | Local compute and messaging | [docs.aws.amazon.com/greengrass](https://docs.aws.amazon.com/greengrass/) |
| **AWS IoT SiteWise** | IoT | Industrial data collection | Industrial IoT data | [docs.aws.amazon.com/iot-sitewise](https://docs.aws.amazon.com/iot-sitewise/) |
| **AWS IoT Things Graph** | IoT | IoT application development | Visual IoT applications | [docs.aws.amazon.com/thingsgraph](https://docs.aws.amazon.com/thingsgraph/) |
| **Amazon FreeRTOS** | IoT | IoT operating system | Microcontroller OS | [docs.aws.amazon.com/freertos](https://docs.aws.amazon.com/freertos/) |
| **AWS IoT Device Defender** | IoT | IoT security service | Device security monitoring | [docs.aws.amazon.com/iot-device-defender](https://docs.aws.amazon.com/iot-device-defender/) |
| **AWS IoT 1-Click** | IoT | Simple device triggers | One-click device actions | [docs.aws.amazon.com/iot-1-click](https://docs.aws.amazon.com/iot-1-click/) |
| **Amazon GameLift** | Game Tech | Game server hosting | Multiplayer game backends | [docs.aws.amazon.com/gamelift](https://docs.aws.amazon.com/gamelift/) |
| **Amazon Lumberyard** | Game Tech | Game engine | 3D game development | [docs.aws.amazon.com/lumberyard](https://docs.aws.amazon.com/lumberyard/) |
| **AWS GameSparks** | Game Tech | Game backend service | Game development platform | [docs.aws.amazon.com/gamesparks](https://docs.aws.amazon.com/gamesparks/) |
| **Amazon WorkSpaces** | End User Computing | Virtual desktops | Desktop as a service | [docs.aws.amazon.com/workspaces](https://docs.aws.amazon.com/workspaces/) |
| **Amazon AppStream 2.0** | End User Computing | Application streaming | Desktop application delivery | [docs.aws.amazon.com/appstream2](https://docs.aws.amazon.com/appstream2/) |
| **Amazon WorkDocs** | End User Computing | Document collaboration | Enterprise file sharing | [docs.aws.amazon.com/workdocs](https://docs.aws.amazon.com/workdocs/) |
| **Amazon WorkMail** | End User Computing | Email and calendar service | Business email | [docs.aws.amazon.com/workmail](https://docs.aws.amazon.com/workmail/) |
| **Amazon Chime** | End User Computing | Communications service | Video conferencing | [docs.aws.amazon.com/chime](https://docs.aws.amazon.com/chime/) |
| **Amazon Connect** | End User Computing | Contact center service | Customer service | [docs.aws.amazon.com/connect](https://docs.aws.amazon.com/connect/) |
| **AWS WorkLink** | End User Computing | Secure mobile access | Mobile web access | [docs.aws.amazon.com/worklink](https://docs.aws.amazon.com/worklink/) |
| **Amazon Honeycode** | End User Computing | No-code app platform | Business applications | [docs.aws.amazon.com/honeycode](https://docs.aws.amazon.com/honeycode/) |
| **AWS Elemental MediaConvert** | Media Services | Video processing | Video transcoding | [docs.aws.amazon.com/mediaconvert](https://docs.aws.amazon.com/mediaconvert/) |
| **AWS Elemental MediaLive** | Media Services | Live video processing | Live streaming | [docs.aws.amazon.com/medialive](https://docs.aws.amazon.com/medialive/) |
| **AWS Elemental MediaPackage** | Media Services | Video packaging | Video delivery | [docs.aws.amazon.com/mediapackage](https://docs.aws.amazon.com/mediapackage/) |
| **AWS Elemental MediaStore** | Media Services | Media storage | Video storage | [docs.aws.amazon.com/mediastore](https://docs.aws.amazon.com/mediastore/) |
| **AWS Elemental MediaTailor** | Media Services | Video personalization | Ad insertion | [docs.aws.amazon.com/mediatailor](https://docs.aws.amazon.com/mediatailor/) |
| **Amazon Kinesis Video Streams** | Media Services | Video streaming | Video ingestion and playback | [docs.aws.amazon.com/kinesis-video-streams](https://docs.aws.amazon.com/kinesis-video-streams/) |
| **Amazon Interactive Video Service** | Media Services | Live streaming | Interactive live video | [docs.aws.amazon.com/ivs](https://docs.aws.amazon.com/ivs/) |
| **AWS Migration Hub** | Migration | Migration tracking | Migration project management | [docs.aws.amazon.com/migrationhub](https://docs.aws.amazon.com/migrationhub/) |
| **AWS Application Migration Service** | Migration | Application migration | Lift-and-shift migrations | [docs.aws.amazon.com/mgn](https://docs.aws.amazon.com/mgn/) |
| **AWS Database Migration Service** | Migration | Database migration | Database migrations | [docs.aws.amazon.com/dms](https://docs.aws.amazon.com/dms/) |
| **AWS DataSync** | Migration | Data transfer service | Data synchronization | [docs.aws.amazon.com/datasync](https://docs.aws.amazon.com/datasync/) |
| **AWS Server Migration Service** | Migration | Server migration | VM migrations | [docs.aws.amazon.com/server-migration-service](https://docs.aws.amazon.com/server-migration-service/) |
| **AWS Application Discovery Service** | Migration | Application discovery | Migration planning | [docs.aws.amazon.com/application-discovery](https://docs.aws.amazon.com/application-discovery/) |
| **AWS Mainframe Modernization** | Migration | Mainframe migration | Legacy system modernization | [docs.aws.amazon.com/m2](https://docs.aws.amazon.com/m2/) |
| **Amazon VPC Lattice** | Networking | Service-to-service connectivity | Application networking | [docs.aws.amazon.com/vpc-lattice](https://docs.aws.amazon.com/vpc-lattice/) |
| **AWS Client VPN** | Networking | Managed VPN service | Remote access VPN | [docs.aws.amazon.com/vpn/latest/clientvpn-admin](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/) |
| **AWS Site-to-Site VPN** | Networking | VPN connections | Site connectivity | [docs.aws.amazon.com/vpn](https://docs.aws.amazon.com/vpn/) |
| **Amazon VPC Peering** | Networking | VPC connectivity | Network routing | [docs.aws.amazon.com/vpc/latest/peering](https://docs.aws.amazon.com/vpc/latest/peering/) |
| **AWS Network Firewall** | Networking | Managed firewall | Network protection | [docs.aws.amazon.com/network-firewall](https://docs.aws.amazon.com/network-firewall/) |
| **Amazon CloudWatch Synthetics** | Management | Synthetic monitoring | Application monitoring | [docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html) |
| **AWS Proton** | Management | Application delivery | Service templates | [docs.aws.amazon.com/proton](https://docs.aws.amazon.com/proton/) |
| **AWS Chatbot** | Management | ChatOps service | Slack/Teams integration | [docs.aws.amazon.com/chatbot](https://docs.aws.amazon.com/chatbot/) |
| **AWS Compute Optimizer** | Management | Resource optimization | Cost optimization | [docs.aws.amazon.com/compute-optimizer](https://docs.aws.amazon.com/compute-optimizer/) |
| **AWS Cost Explorer** | Management | Cost analysis | Cost management | [docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html) |
| **AWS Budgets** | Management | Budget management | Cost monitoring | [docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) |
| **AWS Cost and Usage Report** | Management | Detailed billing | Cost reporting | [docs.aws.amazon.com/cur](https://docs.aws.amazon.com/cur/) |
| **AWS Billing Conductor** | Management | Billing management | Custom billing | [docs.aws.amazon.com/billingconductor](https://docs.aws.amazon.com/billingconductor/) |
| **Amazon Managed Grafana** | Management | Managed Grafana | Observability dashboards | [docs.aws.amazon.com/grafana](https://docs.aws.amazon.com/grafana/) |
| **Amazon Managed Service for Prometheus** | Management | Managed Prometheus | Metrics monitoring | [docs.aws.amazon.com/prometheus](https://docs.aws.amazon.com/prometheus/) |
| **AWS Distro for OpenTelemetry** | Management | Observability framework | Application monitoring | [docs.aws.amazon.com/otel](https://docs.aws.amazon.com/otel/) |
| **AWS App Runner** | Compute | Containerized web apps | Simple container deployment | [docs.aws.amazon.com/apprunner](https://docs.aws.amazon.com/apprunner/) |
| **AWS Copilot** | Compute | Container deployment | Container application CLI | [docs.aws.amazon.com/copilot](https://docs.aws.amazon.com/copilot/) |
| **Amazon Braket** | Quantum | Quantum computing service | Quantum algorithm development | [docs.aws.amazon.com/braket](https://docs.aws.amazon.com/braket/) |
| **AWS Ground Station** | Satellite | Satellite communications | Satellite data processing | [docs.aws.amazon.com/ground-station](https://docs.aws.amazon.com/ground-station/) |
| **AWS RoboMaker** | Robotics | Robot development | Robot simulation and deployment | [docs.aws.amazon.com/robomaker](https://docs.aws.amazon.com/robomaker/) |
| **AWS Panorama** | ML/AI | Computer vision at edge | Edge computer vision | [docs.aws.amazon.com/panorama](https://docs.aws.amazon.com/panorama/) |
| **AWS DeepRacer** | ML/AI | Autonomous racing car | Machine learning education | [docs.aws.amazon.com/deepracer](https://docs.aws.amazon.com/deepracer/) |
| **Amazon Lookout for Vision** | ML/AI | Computer vision for defects | Industrial quality control | [docs.aws.amazon.com/lookout-for-vision](https://docs.aws.amazon.com/lookout-for-vision/) |
| **Amazon Lookout for Equipment** | ML/AI | Equipment anomaly detection | Predictive maintenance | [docs.aws.amazon.com/lookout-for-equipment](https://docs.aws.amazon.com/lookout-for-equipment/) |
| **Amazon Lookout for Metrics** | ML/AI | Anomaly detection service | Business metrics monitoring | [docs.aws.amazon.com/lookoutmetrics](https://docs.aws.amazon.com/lookoutmetrics/) |
| **Amazon Monitron** | ML/AI | Equipment monitoring | Industrial equipment monitoring | [docs.aws.amazon.com/monitron](https://docs.aws.amazon.com/monitron/) |
| **Amazon HealthLake** | ML/AI | Healthcare data service | Healthcare analytics | [docs.aws.amazon.com/healthlake](https://docs.aws.amazon.com/healthlake/) |
| **Amazon Kendra** | ML/AI | Enterprise search service | Intelligent search | [docs.aws.amazon.com/kendra](https://docs.aws.amazon.com/kendra/) |
| **Amazon Augmented AI** | ML/AI | Human review of ML | ML workflow review | [docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html](https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html) |
| **Amazon Fraud Detector** | ML/AI | Fraud detection service | Online fraud prevention | [docs.aws.amazon.com/frauddetector](https://docs.aws.amazon.com/frauddetector/) |
| **Amazon DevOps Guru** | ML/AI | Application performance | Operational insights | [docs.aws.amazon.com/devops-guru](https://docs.aws.amazon.com/devops-guru/) |
| **Amazon CodeGuru Reviewer** | ML/AI | Code review service | Automated code review | [docs.aws.amazon.com/codeguru/latest/reviewer-ug](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/) |
| **Amazon CodeGuru Profiler** | ML/AI | Application profiling | Performance optimization | [docs.aws.amazon.com/codeguru/latest/profiler-ug](https://docs.aws.amazon.com/codeguru/latest/profiler-ug/) |
| **AWS Fault Injection Simulator** | Management | Chaos engineering | Resilience testing | [docs.aws.amazon.com/fis](https://docs.aws.amazon.com/fis/) |
| **AWS Resilience Hub** | Management | Application resilience | Disaster recovery planning | [docs.aws.amazon.com/resilience-hub](https://docs.aws.amazon.com/resilience-hub/) |
| **AWS Application Composer** | Developer Tools | Visual application design | Serverless application builder | [docs.aws.amazon.com/application-composer](https://docs.aws.amazon.com/application-composer/) |
| **Amazon CodeCatalyst** | Developer Tools | Unified development service | End-to-end development | [docs.aws.amazon.com/codecatalyst](https://docs.aws.amazon.com/codecatalyst/) |
| **AWS CloudShell** | Developer Tools | Browser-based shell | Command line access | [docs.aws.amazon.com/cloudshell](https://docs.aws.amazon.com/cloudshell/) |
| **AWS Cloud Control API** | Management | Unified resource API | Resource management | [docs.aws.amazon.com/cloudcontrolapi](https://docs.aws.amazon.com/cloudcontrolapi/) |
| **AWS Resource Access Manager** | Management | Resource sharing | Cross-account sharing | [docs.aws.amazon.com/ram](https://docs.aws.amazon.com/ram/) |
| **AWS Service Quotas** | Management | Service limits management | Quota monitoring | [docs.aws.amazon.com/servicequotas](https://docs.aws.amazon.com/servicequotas/) |
| **AWS Launch Wizard** | Management | Application deployment | Guided deployments | [docs.aws.amazon.com/launchwizard](https://docs.aws.amazon.com/launchwizard/) |
| **AWS Marketplace** | Management | Software marketplace | Third-party software | [docs.aws.amazon.com/marketplace](https://docs.aws.amazon.com/marketplace/) |
| **AWS IQ** | Management | Expert services | On-demand expertise | [docs.aws.amazon.com/iq](https://docs.aws.amazon.com/iq/) |
| **AWS re:Post** | Management | Community Q&A | Technical community | [docs.aws.amazon.com/repost](https://docs.aws.amazon.com/repost/) |
| **AWS Support** | Management | Technical support | Customer support | [docs.aws.amazon.com/support](https://docs.aws.amazon.com/support/) |
| **AWS Training and Certification** | Management | Learning platform | Skills development | [docs.aws.amazon.com/training](https://docs.aws.amazon.com/training/) |
| **AWS Professional Services** | Management | Consulting services | Implementation guidance | [aws.amazon.com/professional-services](https://aws.amazon.com/professional-services/) |
| **AWS Managed Services** | Management | Operational services | Infrastructure management | [docs.aws.amazon.com/managedservices](https://docs.aws.amazon.com/managedservices/) |
| **AWS Enterprise Support** | Management | Premium support | Enterprise-level support | [aws.amazon.com/support/enterprise](https://aws.amazon.com/support/enterprise/) |
| **AWS Business Support** | Management | Business support | Business-level support | [aws.amazon.com/support/business](https://aws.amazon.com/support/business/) |
| **AWS Developer Support** | Management | Developer support | Developer-level support | [aws.amazon.com/support/developer](https://aws.amazon.com/support/developer/) |
| **AWS Basic Support** | Management | Basic support | Free support tier | [aws.amazon.com/support/basic](https://aws.amazon.com/support/basic/) |
| **AWS Snowball** | Storage | Petabyte-scale data transport | Large data migrations | [docs.aws.amazon.com/snowball](https://docs.aws.amazon.com/snowball/) |
| **AWS Snowball Edge** | Storage | Edge computing and data transfer | Edge processing with data transfer | [docs.aws.amazon.com/snowball](https://docs.aws.amazon.com/snowball/) |
| **AWS Snowmobile** | Storage | Exabyte-scale data transfer | Massive data center migrations | [docs.aws.amazon.com/snowball](https://docs.aws.amazon.com/snowball/) |
| **AWS DataSync** | Storage | Online data transfer | Hybrid data synchronization | [docs.aws.amazon.com/datasync](https://docs.aws.amazon.com/datasync/) |
| **AWS Transfer Family** | Storage | Managed file transfer | SFTP, FTPS, FTP file transfers | [docs.aws.amazon.com/transfer](https://docs.aws.amazon.com/transfer/) |
| **Amazon S3 Transfer Acceleration** | Storage | Fast S3 uploads | Global S3 upload acceleration | [docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html) |
| **AWS Elastic Disaster Recovery** | Storage | Disaster recovery service | Application recovery | [docs.aws.amazon.com/drs](https://docs.aws.amazon.com/drs/) |
| **Amazon FSx for Lustre** | Storage | High-performance file system | HPC workloads | [docs.aws.amazon.com/fsx/latest/LustreGuide](https://docs.aws.amazon.com/fsx/latest/LustreGuide/) |
| **Amazon FSx for Windows** | Storage | Windows file system | Windows-based applications | [docs.aws.amazon.com/fsx/latest/WindowsGuide](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/) |
| **Amazon FSx for NetApp ONTAP** | Storage | NetApp file system | Enterprise file storage | [docs.aws.amazon.com/fsx/latest/ONTAPGuide](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/) |
| **Amazon FSx for OpenZFS** | Storage | OpenZFS file system | High-performance NFS | [docs.aws.amazon.com/fsx/latest/OpenZFSGuide](https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/) |
| **AWS Savings Plans** | Cost Management | Flexible pricing model | Cost optimization | [docs.aws.amazon.com/savingsplans](https://docs.aws.amazon.com/savingsplans/) |
| **AWS Reserved Instances** | Cost Management | Capacity reservation | Cost savings for predictable usage | [docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html) |
| **AWS Spot Instances** | Compute | Spare EC2 capacity | Cost-effective compute | [docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html) |
| **AWS Auto Scaling** | Compute | Automatic scaling | Dynamic capacity management | [docs.aws.amazon.com/autoscaling](https://docs.aws.amazon.com/autoscaling/) |
| **Amazon EC2 Image Builder** | Compute | AMI creation and management | Automated image building | [docs.aws.amazon.com/imagebuilder](https://docs.aws.amazon.com/imagebuilder/) |
| **AWS Nitro System** | Compute | EC2 infrastructure | High-performance virtualization | [docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html#ec2-nitro-instances) |
| **AWS Graviton** | Compute | ARM-based processors | Cost-effective compute performance | [aws.amazon.com/ec2/graviton](https://aws.amazon.com/ec2/graviton/) |
| **AWS ParallelCluster** | Compute | HPC cluster management | High-performance computing | [docs.aws.amazon.com/parallelcluster](https://docs.aws.amazon.com/parallelcluster/) |
| **AWS Thinkbox Deadline** | Compute | Render farm management | Media rendering workflows | [docs.aws.amazon.com/deadline](https://docs.aws.amazon.com/deadline/) |
| **AWS Thinkbox Frost** | Compute | Particle meshing | 3D particle effects | [aws.amazon.com/thinkbox-frost](https://aws.amazon.com/thinkbox-frost/) |
| **AWS Thinkbox Krakatoa** | Compute | Volumetric particle rendering | Visual effects rendering | [aws.amazon.com/thinkbox-krakatoa](https://aws.amazon.com/thinkbox-krakatoa/) |
| **AWS Thinkbox Sequoia** | Compute | Point cloud processing | Large-scale point cloud data | [aws.amazon.com/thinkbox-sequoia](https://aws.amazon.com/thinkbox-sequoia/) |
| **AWS Thinkbox Stoke** | Compute | Particle simulation | Fluid and particle dynamics | [aws.amazon.com/thinkbox-stoke](https://aws.amazon.com/thinkbox-stoke/) |
| **AWS Thinkbox XMesh** | Compute | Geometry caching | 3D mesh sequence caching | [aws.amazon.com/thinkbox-xmesh](https://aws.amazon.com/thinkbox-xmesh/) |
| **Amazon Elastic Inference** | Compute | ML inference acceleration | Cost-effective ML inference | [docs.aws.amazon.com/elastic-inference](https://docs.aws.amazon.com/elastic-inference/) |
| **AWS Inferentia** | Compute | ML inference chips | High-performance ML inference | [aws.amazon.com/machine-learning/inferentia](https://aws.amazon.com/machine-learning/inferentia/) |
| **AWS Trainium** | Compute | ML training chips | High-performance ML training | [aws.amazon.com/machine-learning/trainium](https://aws.amazon.com/machine-learning/trainium/) |
| **Amazon Elastic Container Registry** | Compute | Container image registry | Docker container storage | [docs.aws.amazon.com/ecr](https://docs.aws.amazon.com/ecr/) |
| **AWS App2Container** | Compute | Application containerization | Legacy app modernization | [docs.aws.amazon.com/app2container](https://docs.aws.amazon.com/app2container/) |
| **Red Hat OpenShift Service on AWS** | Compute | Managed OpenShift | Enterprise Kubernetes | [docs.aws.amazon.com/rosa](https://docs.aws.amazon.com/rosa/) |
| **VMware Cloud on AWS** | Compute | VMware infrastructure | Hybrid cloud VMware | [docs.aws.amazon.com/vmware-cloudonaws](https://docs.aws.amazon.com/vmware-cloudonaws/) |
| **AWS Dedicated Hosts** | Compute | Physical server tenancy | Compliance and licensing | [docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html) |
| **AWS Elastic Beanstalk** | Compute | Application deployment | Easy application hosting | [docs.aws.amazon.com/elasticbeanstalk](https://docs.aws.amazon.com/elasticbeanstalk/) |
| **AWS Serverless Application Repository** | Compute | Serverless app sharing | Pre-built serverless applications | [docs.aws.amazon.com/serverlessrepo](https://docs.aws.amazon.com/serverlessrepo/) |
| **AWS SAM** | Developer Tools | Serverless application model | Serverless development framework | [docs.aws.amazon.com/serverless-application-model](https://docs.aws.amazon.com/serverless-application-model/) |
| **AWS CDK** | Developer Tools | Cloud development kit | Infrastructure as code framework | [docs.aws.amazon.com/cdk](https://docs.aws.amazon.com/cdk/) |
| **AWS CLI** | Developer Tools | Command line interface | AWS service management | [docs.aws.amazon.com/cli](https://docs.aws.amazon.com/cli/) |
| **AWS SDK** | Developer Tools | Software development kits | Programming language libraries | [aws.amazon.com/tools](https://aws.amazon.com/tools/) |
| **AWS Tools for PowerShell** | Developer Tools | PowerShell cmdlets | Windows PowerShell integration | [docs.aws.amazon.com/powershell](https://docs.aws.amazon.com/powershell/) |
| **AWS Toolkit for Visual Studio** | Developer Tools | Visual Studio integration | .NET development tools | [docs.aws.amazon.com/toolkit-for-visual-studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/) |
| **AWS Toolkit for VS Code** | Developer Tools | VS Code extension | IDE integration | [docs.aws.amazon.com/toolkit-for-vscode](https://docs.aws.amazon.com/toolkit-for-vscode/) |
| **AWS Toolkit for IntelliJ** | Developer Tools | IntelliJ IDEA integration | Java development tools | [docs.aws.amazon.com/toolkit-for-jetbrains](https://docs.aws.amazon.com/toolkit-for-jetbrains/) |
| **AWS Toolkit for Eclipse** | Developer Tools | Eclipse IDE integration | Java development environment | [docs.aws.amazon.com/toolkit-for-eclipse](https://docs.aws.amazon.com/toolkit-for-eclipse/) |
| **AWS Mobile SDK** | Mobile | Mobile development kits | iOS and Android SDKs | [docs.aws.amazon.com/mobile](https://docs.aws.amazon.com/mobile/) |
| **AWS AppConfig** | Management | Application configuration | Dynamic configuration management | [docs.aws.amazon.com/appconfig](https://docs.aws.amazon.com/appconfig/) |
| **AWS OpsWorks** | Management | Configuration management | Chef and Puppet automation | [docs.aws.amazon.com/opsworks](https://docs.aws.amazon.com/opsworks/) |
| **AWS OpsWorks for Chef Automate** | Management | Managed Chef server | Infrastructure automation | [docs.aws.amazon.com/opsworks/latest/userguide/welcome_opscm.html](https://docs.aws.amazon.com/opsworks/latest/userguide/welcome_opscm.html) |
| **AWS OpsWorks for Puppet Enterprise** | Management | Managed Puppet server | Configuration management | [docs.aws.amazon.com/opsworks/latest/userguide/welcome_opspup.html](https://docs.aws.amazon.com/opsworks/latest/userguide/welcome_opspup.html) |
| **AWS CloudFormation StackSets** | Management | Multi-account deployments | Cross-account resource management | [docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html) |
| **AWS Service Management Connector** | Management | ITSM integration | ServiceNow integration | [docs.aws.amazon.com/servicecatalog/latest/adminguide/integrations-servicenow.html](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/integrations-servicenow.html) |
| **AWS Systems Manager Patch Manager** | Management | Patch management | Operating system patching | [docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-patch.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-patch.html) |
| **AWS Systems Manager Session Manager** | Management | Shell access | Secure instance access | [docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) |
| **AWS Systems Manager Run Command** | Management | Remote command execution | Bulk command execution | [docs.aws.amazon.com/systems-manager/latest/userguide/execute-remote-commands.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/execute-remote-commands.html) |
| **AWS Systems Manager State Manager** | Management | Configuration compliance | Desired state management | [docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-state.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-state.html) |
| **AWS Systems Manager Inventory** | Management | System inventory | Resource discovery and tracking | [docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-inventory.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-inventory.html) |
| **AWS Systems Manager Maintenance Windows** | Management | Scheduled maintenance | Automated maintenance tasks | [docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-maintenance.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-maintenance.html) |
| **AWS Systems Manager Parameter Store** | Management | Configuration data storage | Secure parameter management | [docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) |
| **AWS Systems Manager Distributor** | Management | Package distribution | Software package management | [docs.aws.amazon.com/systems-manager/latest/userguide/distributor.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/distributor.html) |
| **AWS CloudWatch Logs** | Management | Log management | Centralized log storage | [docs.aws.amazon.com/cloudwatch/latest/logs](https://docs.aws.amazon.com/cloudwatch/latest/logs/) |
| **AWS CloudWatch Events** | Management | Event routing | Event-driven automation | [docs.aws.amazon.com/cloudwatch/latest/events](https://docs.aws.amazon.com/cloudwatch/latest/events/) |
| **AWS CloudWatch Insights** | Management | Log analytics | Interactive log analysis | [docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html) |
| **AWS CloudWatch Container Insights** | Management | Container monitoring | ECS and EKS monitoring | [docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html) |
| **AWS CloudWatch Lambda Insights** | Management | Lambda monitoring | Serverless function monitoring | [docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights.html](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights.html) |
| **AWS CloudWatch Application Insights** | Management | Application monitoring | Automated application monitoring | [docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/appinsights-what-is.html](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/appinsights-what-is.html) |
| **Amazon OpenSearch Service** | Analytics | Search and analytics | Elasticsearch and OpenSearch | [docs.aws.amazon.com/opensearch-service](https://docs.aws.amazon.com/opensearch-service/) |
| **Amazon OpenSearch Serverless** | Analytics | Serverless search | On-demand search service | [docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html) |
| **AWS Clean Rooms** | Analytics | Collaborative analytics | Privacy-preserving analytics | [docs.aws.amazon.com/clean-rooms](https://docs.aws.amazon.com/clean-rooms/) |
| **Amazon DataZone** | Analytics | Data governance | Data catalog and governance | [docs.aws.amazon.com/datazone](https://docs.aws.amazon.com/datazone/) |
| **AWS Entity Resolution** | Analytics | Record matching | Data deduplication | [docs.aws.amazon.com/entityresolution](https://docs.aws.amazon.com/entityresolution/) |
| **Amazon FinSpace** | Analytics | Financial data management | Capital markets data | [docs.aws.amazon.com/finspace](https://docs.aws.amazon.com/finspace/) |
| **AWS Glue DataBrew** | Analytics | Visual data preparation | No-code data preparation | [docs.aws.amazon.com/databrew](https://docs.aws.amazon.com/databrew/) |
| **AWS Glue Elastic Views** | Analytics | Materialized views | Cross-database views | [docs.aws.amazon.com/glue/latest/dg/elastic-views.html](https://docs.aws.amazon.com/glue/latest/dg/elastic-views.html) |
| **Amazon Kinesis Data Firehose** | Analytics | Data delivery service | Stream data to destinations | [docs.aws.amazon.com/firehose](https://docs.aws.amazon.com/firehose/) |
| **Amazon Kinesis Data Analytics** | Analytics | Stream analytics | Real-time stream processing | [docs.aws.amazon.com/kinesisanalytics](https://docs.aws.amazon.com/kinesisanalytics/) |
| **Amazon Kinesis Data Streams** | Analytics | Data streaming | Real-time data ingestion | [docs.aws.amazon.com/kinesis/latest/dev](https://docs.aws.amazon.com/kinesis/latest/dev/) |
| **Amazon Managed Streaming for Apache Kafka** | Analytics | Managed Kafka | Apache Kafka service | [docs.aws.amazon.com/msk](https://docs.aws.amazon.com/msk/) |
| **Amazon Redshift Serverless** | Analytics | Serverless data warehouse | On-demand data warehousing | [docs.aws.amazon.com/redshift/latest/mgmt/working-with-serverless.html](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-serverless.html) |
| **Amazon Redshift Spectrum** | Analytics | Query S3 data | External table queries | [docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html](https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html) |
| **AWS Supply Chain** | Analytics | Supply chain visibility | Supply chain optimization | [docs.aws.amazon.com/supply-chain](https://docs.aws.amazon.com/supply-chain/) |
| **Amazon Connect Customer Profiles** | Analytics | Customer data platform | Unified customer profiles | [docs.aws.amazon.com/connect/latest/adminguide/customer-profiles.html](https://docs.aws.amazon.com/connect/latest/adminguide/customer-profiles.html) |
| **Amazon Connect Voice ID** | Security | Voice authentication | Biometric voice verification | [docs.aws.amazon.com/connect/latest/adminguide/voice-id.html](https://docs.aws.amazon.com/connect/latest/adminguide/voice-id.html) |
| **Amazon Connect Wisdom** | ML/AI | Knowledge management | AI-powered agent assistance | [docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-wisdom.html](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-wisdom.html) |
| **Amazon Connect Cases** | End User Computing | Case management | Customer service case tracking | [docs.aws.amazon.com/connect/latest/adminguide/cases.html](https://docs.aws.amazon.com/connect/latest/adminguide/cases.html) |
| **Amazon Connect Contact Lens** | ML/AI | Contact analytics | Call center analytics | [docs.aws.amazon.com/connect/latest/adminguide/analyze-conversations.html](https://docs.aws.amazon.com/connect/latest/adminguide/analyze-conversations.html) |
| **Amazon Connect Outbound Campaigns** | End User Computing | Outbound calling | Automated outbound campaigns | [docs.aws.amazon.com/connect/latest/adminguide/outbound-campaigns.html](https://docs.aws.amazon.com/connect/latest/adminguide/outbound-campaigns.html) |
| **Amazon Connect Tasks** | End User Computing | Task management | Agent task assignment | [docs.aws.amazon.com/connect/latest/adminguide/tasks.html](https://docs.aws.amazon.com/connect/latest/adminguide/tasks.html) |
| **AWS Artifact** | Security | Compliance reports | Security and compliance documentation | [docs.aws.amazon.com/artifact](https://docs.aws.amazon.com/artifact/) |
| **AWS Audit Manager** | Security | Audit preparation | Compliance audit automation | [docs.aws.amazon.com/audit-manager](https://docs.aws.amazon.com/audit-manager/) |
| **AWS Certificate Manager Private CA** | Security | Private certificate authority | Internal certificate management | [docs.aws.amazon.com/acm-pca](https://docs.aws.amazon.com/acm-pca/) |
| **AWS CloudHSM Classic** | Security | Hardware security modules | Legacy HSM service | [docs.aws.amazon.com/cloudhsm/classic](https://docs.aws.amazon.com/cloudhsm/classic/) |
| **AWS Detective** | Security | Security investigation | Security incident analysis | [docs.aws.amazon.com/detective](https://docs.aws.amazon.com/detective/) |
| **AWS Firewall Manager** | Security | Centralized firewall management | Multi-account firewall policies | [docs.aws.amazon.com/waf/latest/developerguide/fms-chapter.html](https://docs.aws.amazon.com/waf/latest/developerguide/fms-chapter.html) |
| **AWS Network Access Analyzer** | Security | Network access analysis | VPC security analysis | [docs.aws.amazon.com/vpc/latest/network-access-analyzer](https://docs.aws.amazon.com/vpc/latest/network-access-analyzer/) |
| **AWS Resource Access Manager** | Security | Resource sharing | Cross-account resource access | [docs.aws.amazon.com/ram](https://docs.aws.amazon.com/ram/) |
| **AWS Security Token Service** | Security | Temporary credentials | Federated access management | [docs.aws.amazon.com/STS](https://docs.aws.amazon.com/STS/) |
| **AWS Single Sign-On** | Security | Identity federation | Centralized access management | [docs.aws.amazon.com/singlesignon](https://docs.aws.amazon.com/singlesignon/) |
| **AWS WAF Classic** | Security | Legacy web application firewall | Legacy application protection | [docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html](https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html) |
| **Amazon Inspector Classic** | Security | Legacy security assessment | Legacy vulnerability assessment | [docs.aws.amazon.com/inspector/v1/userguide](https://docs.aws.amazon.com/inspector/v1/userguide/) |
| **AWS Payment Cryptography** | Security | Payment processing security | Payment card industry compliance | [docs.aws.amazon.com/payment-cryptography](https://docs.aws.amazon.com/payment-cryptography/) |
| **AWS Private Certificate Authority** | Security | Private CA service | Internal PKI management | [docs.aws.amazon.com/acm-pca](https://docs.aws.amazon.com/acm-pca/) |
| **AWS Signer** | Security | Code signing | Application code signing | [docs.aws.amazon.com/signer](https://docs.aws.amazon.com/signer/) |
| **AWS Verified Permissions** | Security | Fine-grained authorization | Application-level permissions | [docs.aws.amazon.com/verified-permissions](https://docs.aws.amazon.com/verified-permissions/) |

## 📋 Service Categories Summary

| Category | Count | Key Services |
|----------|-------|--------------|
| **Compute** | 35+ | EC2, Lambda, ECS, EKS, Fargate, Batch, Lightsail |
| **Storage** | 25+ | S3, EBS, EFS, FSx, Glacier, Snow Family, Backup |
| **Database** | 20+ | RDS, DynamoDB, Aurora, Redshift, DocumentDB, Neptune |
| **Networking** | 25+ | VPC, CloudFront, Route 53, Load Balancing, Direct Connect |
| **Security** | 35+ | IAM, KMS, WAF, GuardDuty, Security Hub, Macie, Inspector |
| **Analytics** | 25+ | Athena, Glue, EMR, Kinesis, QuickSight, OpenSearch, MSK |
| **ML/AI** | 35+ | SageMaker, Rekognition, Comprehend, Bedrock, Forecast, Personalize |
| **Management** | 50+ | CloudFormation, CloudWatch, Organizations, Systems Manager |
| **Application Integration** | 10+ | SNS, SQS, Step Functions, EventBridge, AppSync |
| **Developer Tools** | 20+ | CodeCommit, CodeBuild, CodeDeploy, CodePipeline, CDK, SAM |
| **Mobile** | 8+ | Amplify, Device Farm, Pinpoint, Location Service |
| **IoT** | 12+ | IoT Core, IoT Analytics, Greengrass, IoT Device Management |
| **Media Services** | 10+ | MediaConvert, MediaLive, Kinesis Video, Interactive Video |
| **Migration** | 10+ | Migration Hub, DMS, DataSync, Application Migration Service |
| **End User Computing** | 15+ | WorkSpaces, AppStream, WorkDocs, Connect, Chime |
| **Game Tech** | 5+ | GameLift, Lumberyard, GameSparks |
| **Cost Management** | 8+ | Cost Explorer, Budgets, Savings Plans, Reserved Instances |
| **Quantum** | 2+ | Braket |
| **Satellite** | 2+ | Ground Station |
| **Robotics** | 2+ | RoboMaker |

## 🔗 Quick Reference Links

- **AWS Documentation Home**: [docs.aws.amazon.com](https://docs.aws.amazon.com/)
- **AWS Service Health Dashboard**: [status.aws.amazon.com](https://status.aws.amazon.com/)
- **AWS Architecture Center**: [aws.amazon.com/architecture](https://aws.amazon.com/architecture/)
- **AWS Well-Architected Framework**: [aws.amazon.com/well-architected](https://aws.amazon.com/well-architected/)
- **AWS Pricing Calculator**: [calculator.aws](https://calculator.aws/)
- **AWS Free Tier**: [aws.amazon.com/free](https://aws.amazon.com/free/)

---

**Total Services Listed**: 320+

**Last Updated**: December 2024

**Note**: This comprehensive list includes all major AWS services as of December 2024, including core services, specialized tools, and emerging technologies. Some services may be in preview or have regional availability limitations. Always refer to the official AWS documentation for the most current information and service availability.