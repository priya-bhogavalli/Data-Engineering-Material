# Azure Databricks - Interview Questions

## Basic Concepts

### 1. What is Azure Databricks and how does it differ from Apache Spark?
**Answer:** Azure Databricks is a unified analytics platform built on Apache Spark with Azure integration. Key differences:
- **Managed Service**: Fully managed Spark infrastructure
- **Collaborative Workspace**: Shared notebooks and team collaboration
- **Azure Integration**: Native integration with Azure services
- **Enhanced Security**: Enterprise-grade security and governance
- **Optimized Performance**: Performance optimizations beyond open-source Spark
- **MLflow Integration**: Built-in ML lifecycle management
- **Delta Lake**: ACID transactions for data lakes

### 2. What are the main components of Azure Databricks workspace?
**Answer:** Main workspace components:
- **Notebooks**: Interactive development environment
- **Clusters**: Managed Spark compute resources
- **Jobs**: Scheduled and automated workflows
- **Libraries**: Package and dependency management
- **Data**: Data sources and file management
- **Models**: ML model registry and management
- **SQL**: SQL analytics and dashboards

### 3. What types of clusters are available in Azure Databricks?
**Answer:** Cluster types include:
- **All-Purpose Clusters**: Interactive development and ad-hoc analysis
- **Job Clusters**: Dedicated clusters for automated jobs
- **High Concurrency Clusters**: Support multiple users simultaneously
- **Single Node Clusters**: Single-machine clusters for small workloads
- **GPU Clusters**: GPU-enabled clusters for ML and deep learning
- **Spot Instance Clusters**: Cost-optimized using Azure Spot VMs

### 4. How does Delta Lake enhance data lake capabilities in Databricks?
**Answer:** Delta Lake provides:
- **ACID Transactions**: Reliable data operations with consistency
- **Schema Evolution**: Handle schema changes without breaking pipelines
- **Time Travel**: Query historical versions of data
- **Concurrent Operations**: Support multiple concurrent readers/writers
- **Data Versioning**: Track data changes and lineage
- **Performance Optimization**: Z-ordering and compaction
- **Unified Batch/Streaming**: Single API for batch and streaming

### 5. What is MLflow and how does it integrate with Azure Databricks?
**Answer:** MLflow is an ML lifecycle management platform:
- **Experiment Tracking**: Track ML experiments and parameters
- **Model Registry**: Centralized model versioning and management
- **Model Deployment**: Deploy models to various serving platforms
- **Project Packaging**: Package ML code for reproducibility
- **Native Integration**: Built into Databricks workspace
- **Collaboration**: Share experiments and models across teams

## Intermediate Concepts

### 6. How do you optimize cluster performance in Azure Databricks?
**Answer:** Performance optimization strategies:
- **Right-Sizing**: Choose appropriate VM types and sizes
- **Auto-Scaling**: Enable auto-scaling for variable workloads
- **Spot Instances**: Use spot VMs for cost-effective processing
- **Cluster Pools**: Reuse clusters to reduce startup time
- **Custom Images**: Use custom Docker images for faster startup
- **Memory Configuration**: Optimize Spark memory settings
- **Parallelism**: Configure appropriate parallelism levels

### 7. How do you handle data security and access control in Databricks?
**Answer:** Security implementation:
- **Azure AD Integration**: Single sign-on with Azure Active Directory
- **Table ACLs**: Fine-grained table and column permissions
- **Cluster Policies**: Governance policies for cluster creation
- **Secret Management**: Secure credential storage with Azure Key Vault
- **Network Security**: VNet integration and private endpoints
- **Audit Logging**: Comprehensive activity monitoring
- **Data Encryption**: Encryption in transit and at rest

### 8. What are the different ways to ingest data into Databricks?
**Answer:** Data ingestion methods:
- **Batch Ingestion**: Load data from files, databases, APIs
- **Streaming Ingestion**: Real-time data from Kafka, Event Hubs
- **Auto Loader**: Incrementally process new files in cloud storage
- **COPY INTO**: Efficient bulk data loading into Delta tables
- **Partner Connectors**: Third-party data integration tools
- **Azure Data Factory**: Orchestrated data pipelines
- **REST APIs**: Programmatic data ingestion

### 9. How do you implement streaming analytics in Azure Databricks?
**Answer:** Streaming implementation:
- **Structured Streaming**: Spark's stream processing engine
- **Event Sources**: Kafka, Event Hubs, IoT Hub integration
- **Windowing**: Time-based and session-based windows
- **Watermarking**: Handle late-arriving data
- **Checkpointing**: Fault-tolerant stream processing
- **Output Modes**: Append, complete, and update modes
- **Monitoring**: Stream monitoring and alerting

### 10. How do you manage libraries and dependencies in Databricks?
**Answer:** Library management approaches:
- **Cluster Libraries**: Install libraries at cluster level
- **Notebook Libraries**: Install libraries within notebooks
- **Init Scripts**: Custom initialization scripts for clusters
- **Custom Images**: Docker images with pre-installed packages
- **Maven/PyPI**: Install from public repositories
- **Upload Libraries**: Upload custom JAR/wheel files
- **Environment Management**: Consistent environments across clusters

## Advanced Concepts

### 11. How do you implement CI/CD for Databricks workflows?
**Answer:** CI/CD implementation:
- **Git Integration**: Version control for notebooks and code
- **Databricks CLI**: Command-line interface for automation
- **REST APIs**: Programmatic workspace management
- **Azure DevOps**: Integration with Azure DevOps pipelines
- **Testing**: Automated testing of notebooks and jobs
- **Environment Promotion**: Deploy across dev/test/prod environments
- **Monitoring**: Automated monitoring and alerting

### 12. How do you optimize costs in Azure Databricks?
**Answer:** Cost optimization strategies:
- **Auto-Termination**: Automatically terminate idle clusters
- **Spot Instances**: Use Azure Spot VMs for significant savings
- **Right-Sizing**: Match cluster size to workload requirements
- **Cluster Pools**: Reuse clusters to reduce startup costs
- **Job Scheduling**: Schedule jobs during off-peak hours
- **Monitoring**: Track usage and identify optimization opportunities
- **Reserved Instances**: Use reserved capacity for predictable workloads

### 13. How do you handle large-scale data processing in Databricks?
**Answer:** Large-scale processing techniques:
- **Data Partitioning**: Optimize data layout for parallel processing
- **Caching**: Cache frequently accessed datasets
- **Broadcast Variables**: Efficiently share read-only data
- **Repartitioning**: Optimize data distribution across partitions
- **Z-Ordering**: Optimize data layout for query performance
- **Adaptive Query Execution**: Runtime query optimization
- **Resource Management**: Optimize cluster resources for workload

### 14. How do you implement data governance in Azure Databricks?
**Answer:** Data governance implementation:
- **Unity Catalog**: Centralized metadata and governance (preview)
- **Table ACLs**: Fine-grained access control
- **Data Lineage**: Track data flow and transformations
- **Audit Logging**: Comprehensive activity monitoring
- **Data Classification**: Classify and tag sensitive data
- **Compliance**: Meet regulatory requirements
- **Documentation**: Maintain data catalogs and documentation

### 15. How do you troubleshoot performance issues in Databricks?
**Answer:** Performance troubleshooting approach:
- **Spark UI**: Analyze job execution and resource utilization
- **Ganglia Metrics**: Monitor cluster resource usage
- **Query Plans**: Examine Spark SQL execution plans
- **Event Logs**: Analyze Spark event logs for bottlenecks
- **Profiling**: Use profiling tools for code optimization
- **Monitoring**: Set up proactive monitoring and alerting
- **Optimization**: Apply performance tuning techniques

## Real-World Scenarios

### 16. How would you design a real-time fraud detection system using Azure Databricks?
**Answer:** Fraud detection system design:
- **Data Ingestion**: Stream transaction data from Event Hubs
- **Feature Engineering**: Real-time feature computation
- **ML Model**: Deploy trained fraud detection models
- **Scoring**: Real-time transaction scoring
- **Alerting**: Generate alerts for suspicious transactions
- **Feedback Loop**: Incorporate feedback to improve models
- **Monitoring**: Monitor system performance and accuracy
- **Compliance**: Ensure regulatory compliance and audit trails

### 17. How would you migrate an on-premises Hadoop cluster to Azure Databricks?
**Answer:** Migration strategy:
- **Assessment**: Analyze existing Hadoop workloads and dependencies
- **Data Migration**: Move data to Azure Data Lake Storage
- **Code Conversion**: Convert MapReduce jobs to Spark
- **Testing**: Validate migrated workloads in Databricks
- **Performance Tuning**: Optimize for cloud environment
- **Training**: Train team on Databricks platform
- **Gradual Migration**: Migrate workloads incrementally
- **Monitoring**: Implement monitoring and alerting

### 18. How would you implement a data lake architecture using Azure Databricks?
**Answer:** Data lake architecture:
- **Raw Layer**: Ingest raw data into ADLS Gen2
- **Bronze Layer**: Basic data cleansing and validation
- **Silver Layer**: Structured and cleaned data
- **Gold Layer**: Business-ready aggregated data
- **Delta Lake**: Use Delta format for ACID transactions
- **Governance**: Implement data governance and security
- **Processing**: Use Databricks for ETL and analytics
- **Serving**: Connect to BI tools and applications

### 19. How would you build an ML pipeline using Azure Databricks and MLflow?
**Answer:** ML pipeline implementation:
- **Data Preparation**: Clean and prepare training data
- **Feature Engineering**: Create and validate features
- **Model Training**: Train models using distributed computing
- **Experiment Tracking**: Track experiments with MLflow
- **Model Registry**: Register and version models
- **Model Deployment**: Deploy models for batch/real-time inference
- **Monitoring**: Monitor model performance and drift
- **Retraining**: Automate model retraining workflows

### 20. How would you implement data quality monitoring in Azure Databricks?
**Answer:** Data quality monitoring:
- **Quality Checks**: Implement automated data quality validations
- **Profiling**: Profile data to understand quality patterns
- **Anomaly Detection**: Detect data anomalies and outliers
- **Alerting**: Alert on quality threshold breaches
- **Dashboards**: Create data quality monitoring dashboards
- **Lineage**: Track data lineage for impact analysis
- **Remediation**: Implement automated data remediation
- **Reporting**: Generate data quality reports for stakeholders