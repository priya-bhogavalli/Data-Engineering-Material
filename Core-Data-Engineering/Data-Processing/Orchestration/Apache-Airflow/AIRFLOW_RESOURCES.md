# Apache Airflow Comprehensive Resources Guide

## Quick Start
- [Installation Guide](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)
- [Quick Start with Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [Quick Start with Local Executor](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html)
- [Airflow UI Tour](https://airflow.apache.org/docs/apache-airflow/stable/ui.html)
- [First DAG Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html)

## Official Documentation
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow GitHub Repository](https://github.com/apache/airflow)
- [Airflow Python API Reference](https://airflow.apache.org/docs/apache-airflow/stable/_api/)
- [Airflow Tutorials](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Common Pitfalls](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Airflow CLI Reference](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html)
- [REST API Reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)
- [Configuration Reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)

## Version Information
- [Release Notes](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html)
- [Upgrading from 1.10 to 2.0](https://airflow.apache.org/docs/apache-airflow/stable/upgrading-from-1-10/index.html)
- [Upgrading to 2.0+](https://airflow.apache.org/docs/apache-airflow/stable/upgrading-from-1-10/index.html)
- [Provider Packages Compatibility](https://airflow.apache.org/docs/apache-airflow-providers/index.html)
- [Airflow Roadmap](https://airflow.apache.org/roadmap/)

## Core Concepts
- [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html)
- [Tasks](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html)
- [Operators](https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html)
- [Connections](https://airflow.apache.org/docs/apache-airflow/stable/concepts/connections.html)
- [XComs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html)
- [Variables](https://airflow.apache.org/docs/apache-airflow/stable/concepts/variables.html)
- [Datasets](https://airflow.apache.org/docs/apache-airflow/stable/concepts/datasets.html)
- [Dynamic Task Mapping](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dynamic-task-mapping.html)
- [Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html)
- [Plugins](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html)
- [Trigger Rules](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html#trigger-rules)
- [Pools](https://airflow.apache.org/docs/apache-airflow/stable/concepts/pools.html)
- [SLAs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html#slas)

## Troubleshooting & Debugging
- [Common Issues](https://airflow.apache.org/docs/apache-airflow/stable/faq.html)
- [Task Debugging](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/index.html)
- [Handling Task Failures](https://airflow.apache.org/docs/apache-airflow/stable/concepts/tasks.html#handling-task-failures)
- [Zombie Task Killing](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html#zombie-task-killing)
- [Database Deadlocks](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#database-performance)
- [Debugging DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html)

## Executors
- [Executor Overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html)
- [Local Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/local.html)
- [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery.html)
- [Kubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/kubernetes.html)
- [CeleryKubernetes Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery_kubernetes.html)
- [Debug Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html)

## Operators and Hooks
- [Python Operator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html)
- [Bash Operator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/bash.html)
- [SQL Operators](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/index.html)
- [Sensors](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html)
  - [File Sensor](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html#filesensor)
  - [External Task Sensor](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html#externaltasksensor)
  - [SQL Sensor](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html#sqlsensor)
  - [Time Sensor](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html#timesensor)
  - [Python Sensor](https://airflow.apache.org/docs/apache-airflow/stable/concepts/sensors.html#pythonsensor)
- [Email Operator](https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html)
- [Empty Operator](https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html)
- [Branch Operator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html#branchpythonoperator)
- [Trigger DAG Run Operator](https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/index.html)
- [Hooks Overview](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html)

## Advanced Features
- [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
- [Task Groups](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html#task-groups)
- [Dynamic Task Mapping](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dynamic-task-mapping.html)
- [Datasets & Data-Driven Scheduling](https://airflow.apache.org/docs/apache-airflow/stable/concepts/datasets.html)
- [Branching](https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html#branching)
- [Jinja Templating](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)
- [Custom Operators](https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html)
- [Callbacks](https://airflow.apache.org/docs/apache-airflow/stable/logging-monitoring/callbacks.html)
- [Timetables](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/timetable.html)

## Testing & CI/CD
- [Unit Testing DAGs](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing)
- [DAG Validation](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#validate)
- [CI/CD for Airflow](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#cicd)
- [GitHub Actions for Airflow](https://github.com/apache/airflow/tree/main/.github/workflows)
- [Testing with pytest](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#unit-tests)
- [Mocking Connections](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#mocking-connections)

## Cloud Provider Integrations

### Amazon Web Services (AWS)
- [AWS Provider Overview](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html)
- [S3 Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/s3.html)
- [Redshift Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/redshift/index.html)
- [EMR Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/emr.html)
- [Lambda Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/lambda.html)
- [SageMaker Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/sagemaker.html)
- [Athena Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/athena.html)
- [DynamoDB Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/dynamodb.html)
- [ECS Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/ecs.html)
- [Glue Operators](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/glue.html)
- [S3 to Redshift Transfer](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/s3_to_redshift.html)

### Google Cloud Platform (GCP)
- [GCP Provider Overview](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html)
- [BigQuery Operators](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html)
- [GCS Operators](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/gcs.html)
- [Dataflow Operators](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/dataflow.html)
- [Dataproc Operators](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/dataproc.html)
- [Cloud SQL Operators](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/cloud_sql.html)
- [Cloud Functions Operators](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/functions.html)
- [Vertex AI Operators](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html)
- [GCS to BigQuery Transfer](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html)

### Microsoft Azure
- [Azure Provider Overview](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html)
- [Blob Storage Operators](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html)
- [Data Factory Operators](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html)
- [Cosmos DB Operators](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html)
- [Azure Container Instances](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html)
- [Azure Data Lake](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html)

## Database Integrations

### SQL Databases
- [PostgreSQL](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/index.html)
- [MySQL](https://airflow.apache.org/docs/apache-airflow-providers-mysql/stable/index.html)
- [SQLite](https://airflow.apache.org/docs/apache-airflow-providers-sqlite/stable/index.html)
- [Microsoft SQL Server](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/index.html)
- [Oracle](https://airflow.apache.org/docs/apache-airflow-providers-oracle/stable/index.html)

### Data Warehouses
- [Snowflake Integration](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/index.html)
  - [Snowflake Operators](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/operators/snowflake.html)
  - [Snowflake to Slack](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/index.html)
  - [S3 to Snowflake](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/index.html)
  - [Snowflake Hooks](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/index.html)
- [Redshift](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/redshift/index.html)
- [BigQuery](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html)
- [Databricks](https://airflow.apache.org/docs/apache-airflow-providers-databricks/stable/index.html)

### NoSQL Databases
- [MongoDB](https://airflow.apache.org/docs/apache-airflow-providers-mongo/stable/index.html)
- [Cassandra](https://airflow.apache.org/docs/apache-airflow-providers-apache-cassandra/stable/index.html)
- [DynamoDB](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/dynamodb.html)
- [Elasticsearch](https://airflow.apache.org/docs/apache-airflow-providers-elasticsearch/stable/index.html)

## Data Processing Integrations

### Apache Ecosystem
- [Spark](https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/index.html)
- [Hive](https://airflow.apache.org/docs/apache-airflow-providers-apache-hive/stable/index.html)
- [Hadoop](https://airflow.apache.org/docs/apache-airflow-providers-apache-hdfs/stable/index.html)
- [Kafka](https://airflow.apache.org/docs/apache-airflow-providers-apache-kafka/stable/index.html)
- [Beam](https://airflow.apache.org/docs/apache-airflow-providers-apache-beam/stable/index.html)
- [Druid](https://airflow.apache.org/docs/apache-airflow-providers-apache-druid/stable/index.html)

### dbt Integration
- [dbt Operator Examples](https://registry.astronomer.io/providers/airflow-provider-dbt/versions/latest)
- [dbt Core Operator](https://registry.astronomer.io/providers/airflow-provider-dbt/modules/dbtcoreoperator)
- [dbt Cloud Run Job Operator](https://registry.astronomer.io/providers/airflow-provider-dbt/modules/dbtcloudrunjoboperator)
- [dbt Cloud Job Run Sensor](https://registry.astronomer.io/providers/airflow-provider-dbt/modules/dbtcloudjobrunstatussensor)

### Other Data Tools
- [Great Expectations](https://greatexpectations.io/blog)
- [Pandas](https://airflow.apache.org/docs/apache-airflow-providers/index.html)
- [Papermill](https://airflow.apache.org/docs/apache-airflow-providers-papermill/stable/index.html)
- [Tableau](https://airflow.apache.org/docs/apache-airflow-providers-tableau/stable/index.html)
- [Airbyte](https://docs.airbyte.com/operator-guides/using-the-airflow-airbyte-operator/)

## Protocol & Service Integrations
- [HTTP/REST API](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/index.html)
- [FTP](https://airflow.apache.org/docs/apache-airflow-providers-ftp/stable/index.html)
- [SFTP](https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/index.html)
- [SSH](https://airflow.apache.org/docs/apache-airflow-providers-ssh/stable/index.html)
- [IMAP](https://airflow.apache.org/docs/apache-airflow-providers-imap/stable/index.html)
- [Slack](https://airflow.apache.org/docs/apache-airflow-providers-slack/stable/index.html)
- [Discord](https://airflow.apache.org/docs/apache-airflow-providers-discord/stable/index.html)
- [Telegram](https://airflow.apache.org/docs/apache-airflow-providers-telegram/stable/index.html)
- [Jira](https://airflow.apache.org/docs/apache-airflow-providers-jira/stable/index.html)
- [GitHub](https://airflow.apache.org/docs/apache-airflow-providers-github/stable/index.html)
- [Docker](https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/index.html)
- [Kubernetes](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/index.html)

## Deployment & Administration
- [Security](https://airflow.apache.org/docs/apache-airflow/stable/security/index.html)
- [Authentication](https://airflow.apache.org/docs/apache-airflow/stable/security/index.html#authentication)
- [Authorization](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html)

## Security Best Practices
- [Securing Connections](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/index.html)
- [Securing Variables](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html)
- [Webserver Security](https://airflow.apache.org/docs/apache-airflow/stable/security/index.html)
- [API Security](https://airflow.apache.org/docs/apache-airflow/stable/security/api.html)
- [DAG Code Security](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#dag-dependencies)
- [Encryption](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/secrets/fernet.html)
- [RBAC Setup](https://airflow.apache.org/docs/apache-airflow/stable/security/access-control.html)
- [Scaling Airflow](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/index.html)
- [Logging & Monitoring](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/index.html)
- [Metrics & Monitoring](https://airflow.apache.org/docs/apache-airflow/stable/logging-monitoring/metrics.html)
- [Alerting](https://airflow.apache.org/docs/apache-airflow/stable/logging-monitoring/callbacks.html)
- [Performance Tuning](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#performance)
- [Production Deployment](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/production-deployment.html)
- [Kubernetes Deployment](https://airflow.apache.org/docs/helm-chart/stable/index.html)
- [Database Backend Setup](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html)
- [Upgrading Airflow](https://airflow.apache.org/docs/apache-airflow/stable/upgrading-from-1-10/index.html)

## Performance Optimization
- [Scaling Airflow](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/production-deployment.html)
- [Optimizing Performance](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#performance)
- [Database Optimization](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html#database-optimization)
- [Scheduler Tuning](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html)
- [Executor Selection Guide](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html#executor-selection-guide)
- [Pools for Resource Management](https://airflow.apache.org/docs/apache-airflow/stable/concepts/pools.html)
- [Concurrency Settings](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html#concurrency)

## Community Resources
- [Airflow Slack Channel](https://apache-airflow.slack.com/)
- [Airflow Stack Overflow](https://stackoverflow.com/search?q=apache+airflow)
- [Airflow Discourse Forum](https://github.com/apache/airflow/discussions)
- [Astronomer Guides](https://docs.astronomer.io/learn/)
- [Airflow Summit](https://airflowsummit.org/)
- [Airflow Podcast](https://soundcloud.com/the-airflow-podcast)
- [Airflow Blog](https://airflow.apache.org/blog/)
- [Airflow Roadmap](https://airflow.apache.org/roadmap/)

## Books & Courses
- [Data Pipelines with Apache Airflow](https://www.oreilly.com/library/view/data-pipelines-with/9781617296901/)
- [Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)
- [Udemy: The Complete Hands-On Course to Master Apache Airflow](https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/)
- [Manning: Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow)

## Example DAGs & Code
- [Astronomer Registry](https://registry.astronomer.io/)

## Design Patterns & Best Practices
- [Task Idempotency](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#idempotency)
- [Task Atomicity](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#tasks-should-be-atomic)
- [Fan-in/Fan-out Pattern](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#dynamic-dags)
- [ETL Patterns](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#etl-best-practices)
- [DAG Dependencies](https://airflow.apache.org/docs/apache-airflow/stable/concepts/datasets.html)
- [Subdags vs Task Groups](https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html#task-groups)
- [Incremental Loading](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#incremental-loading)

## Data Quality & Observability
- [Great Expectations](https://greatexpectations.io/blog)
- [Dagster](https://docs.dagster.io/integrations/airflow)
- [Prefect](https://docs.prefect.io/latest/guides/airflow/)

## ML & AI Integrations
- [SageMaker](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/sagemaker.html)
- [Vertex AI](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html)
- [Azure ML](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/index.html)

## Tools & Extensions
- [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html)
- [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)
- [Airflow UI](https://airflow.apache.org/docs/apache-airflow/stable/ui.html)
- [Airflow Plugins](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html)
- [Airflow Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/index.html)
- [Airflow Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Airflow API Auth](https://airflow.apache.org/docs/apache-airflow/stable/security/api.html)

## Commercial Solutions
- [Astronomer](https://www.astronomer.io/)
- [Amazon MWAA](https://aws.amazon.com/managed-workflows-for-apache-airflow/)
- [Google Cloud Composer](https://cloud.google.com/composer)
- [Microsoft Azure Data Factory](https://azure.microsoft.com/en-us/services/data-factory/)
- [Databricks Workflows](https://databricks.com/product/workflows)

## Container & Orchestration
- [Docker Compose Setup](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Kubernetes Operator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)
- [Helm Chart Configuration](https://airflow.apache.org/docs/helm-chart/stable/parameters-ref.html)
- [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)
- [Docker Operator](https://airflow.apache.org/docs/apache-airflow-providers-docker/stable/index.html)
- [ECS Operator](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/ecs.html)](https://docs.dagster.io/integrations/airflow)
- [Prefect](https://docs.prefect.io/latest/guides/airflow/)

## Example DAGs
- [Astronomer Registry](https://registry.astronomer.io/)

## Tools & Extensions
- [Airflow CLI](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html)
- [Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)
- [Airflow UI](https://airflow.apache.org/docs/apache-airflow/stable/ui.html)
- [Airflow Plugins](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html)
- [Airflow Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/index.html)