# DevOps Automation Key Concepts for Data Engineering

## 1. Infrastructure as Code (IaC)
**What it is**: Managing and provisioning infrastructure through code rather than manual processes.

**Why important**: IaC enables version control, repeatability, and automation of infrastructure deployment, crucial for data engineering environments that require consistent and scalable infrastructure.

**When to use**: 
- Setting up data pipelines across environments
- Scaling data processing infrastructure
- Ensuring consistent development, staging, and production environments
- Disaster recovery scenarios

**Terraform Example**:
```hcl
# terraform/data-infrastructure.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Data Lake S3 Bucket
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-${var.environment}"
  
  tags = {
    Environment = var.environment
    Purpose     = "DataLake"
    Team        = "DataEngineering"
  }
}

# EMR Cluster for Spark Processing
resource "aws_emr_cluster" "spark_cluster" {
  name          = "spark-data-processing-${var.environment}"
  release_label = "emr-6.15.0"
  applications  = ["Spark", "Hadoop", "Hive"]

  ec2_attributes {
    key_name                          = var.key_name
    instance_profile                  = aws_iam_instance_profile.emr_profile.arn
    subnet_id                         = var.subnet_id
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_slave.id
  }

  master_instance_group {
    instance_type = "m5.xlarge"
  }

  core_instance_group {
    instance_type  = "m5.large"
    instance_count = 2

    ebs_config {
      size                 = 40
      type                 = "gp2"
      volumes_per_instance = 1
    }
  }

  configurations_json = jsonencode([
    {
      "Classification": "spark-defaults",
      "Properties": {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true"
      }
    }
  ])

  service_role = aws_iam_role.emr_service_role.arn
}

# RDS Database for Metadata
resource "aws_db_instance" "metadata_db" {
  identifier = "data-metadata-${var.environment}"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true
  
  db_name  = "metadata"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = var.environment != "prod"
  
  tags = {
    Environment = var.environment
    Purpose     = "MetadataStore"
  }
}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "db_username" {
  description = "Database username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

## 2. Containerization with Docker
**What it is**: Packaging applications and their dependencies into lightweight, portable containers.

**Why important**: Containers ensure consistent environments across development, testing, and production, solving the "it works on my machine" problem common in data engineering.

**When to use**:
- Packaging data processing applications
- Creating reproducible data science environments
- Microservices architecture for data platforms
- CI/CD pipelines for data applications

**Docker Examples**:
```dockerfile
# Dockerfile for PySpark Data Processing
FROM apache/spark:3.5.0-python3

# Set working directory
WORKDIR /app

# Install additional Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Set environment variables
ENV SPARK_APPLICATION_PYTHON_LOCATION=/app/src/main.py
ENV SPARK_SUBMIT_ARGS="--master local[*] --py-files /app/src/utils.py"

# Create non-root user
RUN groupadd -r spark && useradd -r -g spark spark
RUN chown -R spark:spark /app
USER spark

# Command to run the application
CMD ["spark-submit", "--master", "local[*]", "src/main.py"]
```

```yaml
# docker-compose.yml for Data Engineering Stack
version: '3.8'

services:
  # Apache Airflow
  airflow-webserver:
    image: apache/airflow:2.7.0
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      - AIRFLOW__CORE__FERNET_KEY=your-fernet-key-here
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    ports:
      - "8080:8080"
    depends_on:
      - postgres
    command: webserver

  airflow-scheduler:
    image: apache/airflow:2.7.0
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    depends_on:
      - postgres
    command: scheduler

  # PostgreSQL Database
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # Redis for Caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Jupyter Notebook for Development
  jupyter:
    image: jupyter/pyspark-notebook:latest
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
    environment:
      - JUPYTER_ENABLE_LAB=yes

  # MinIO for S3-compatible Storage
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    command: server /data --console-address ":9001"

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

## 3. Container Orchestration with Kubernetes
**What it is**: Platform for automating deployment, scaling, and management of containerized applications.

**Why important**: Kubernetes provides robust orchestration for data processing workloads, enabling auto-scaling, self-healing, and efficient resource utilization.

**When to use**:
- Large-scale data processing workloads
- Microservices-based data platforms
- Auto-scaling data pipelines
- Multi-tenant data processing environments

**Kubernetes Examples**:
```yaml
# k8s/spark-operator.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-operator
  namespace: data-processing
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spark-operator
  template:
    metadata:
      labels:
        app: spark-operator
    spec:
      serviceAccountName: spark-operator
      containers:
      - name: spark-operator
        image: gcr.io/spark-operator/spark-operator:v1beta2-1.3.8-3.1.1
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        args:
        - -v=2
        - -logtostderr
        - -namespace=data-processing
        - -enable-ui-service=true
        - -enable-webhook=true
        - -webhook-svc-namespace=data-processing
        - -webhook-port=8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "100m"
          limits:
            memory: "1Gi"
            cpu: "500m"

---
# Spark Application CRD
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: data-processing-job
  namespace: data-processing
spec:
  type: Python
  pythonVersion: "3"
  mode: cluster
  image: "my-registry/spark-data-processing:latest"
  imagePullPolicy: Always
  mainApplicationFile: local:///app/main.py
  sparkVersion: "3.1.1"
  restartPolicy:
    type: OnFailure
    onFailureRetries: 3
    onFailureRetryInterval: 10
    onSubmissionFailureRetries: 5
    onSubmissionFailureRetryInterval: 20
  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "2g"
    labels:
      version: 3.1.1
    serviceAccount: spark-operator
  executor:
    cores: 2
    instances: 3
    memory: "4g"
    labels:
      version: 3.1.1
  monitoring:
    exposeDriverMetrics: true
    exposeExecutorMetrics: true
    prometheus:
      jmxExporterJar: "/prometheus/jmx_prometheus_javaagent-0.11.0.jar"
      port: 8090
```

```yaml
# k8s/airflow-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airflow-webserver
  namespace: data-platform
spec:
  replicas: 2
  selector:
    matchLabels:
      app: airflow-webserver
  template:
    metadata:
      labels:
        app: airflow-webserver
    spec:
      containers:
      - name: airflow-webserver
        image: apache/airflow:2.7.0
        ports:
        - containerPort: 8080
        env:
        - name: AIRFLOW__CORE__EXECUTOR
          value: "KubernetesExecutor"
        - name: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
          valueFrom:
            secretKeyRef:
              name: airflow-secrets
              key: database-url
        - name: AIRFLOW__KUBERNETES__NAMESPACE
          value: "data-platform"
        - name: AIRFLOW__KUBERNETES__WORKER_CONTAINER_REPOSITORY
          value: "apache/airflow"
        - name: AIRFLOW__KUBERNETES__WORKER_CONTAINER_TAG
          value: "2.7.0"
        volumeMounts:
        - name: dags-volume
          mountPath: /opt/airflow/dags
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
      volumes:
      - name: dags-volume
        configMap:
          name: airflow-dags

---
apiVersion: v1
kind: Service
metadata:
  name: airflow-webserver-service
  namespace: data-platform
spec:
  selector:
    app: airflow-webserver
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

## 4. CI/CD Pipelines for Data Engineering
**What it is**: Automated processes for building, testing, and deploying data applications and infrastructure.

**Why important**: CI/CD ensures data pipelines are tested, reliable, and can be deployed consistently across environments, reducing manual errors and deployment time.

**When to use**:
- Deploying data pipeline changes
- Testing data transformations
- Infrastructure updates
- Data quality validation automation

**GitHub Actions Example**:
```yaml
# .github/workflows/data-pipeline-ci-cd.yml
name: Data Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: data-processing
  EKS_CLUSTER_NAME: data-platform-cluster

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=src --cov-report=xml

    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db

    - name: Run data quality tests
      run: |
        python -m great_expectations checkpoint run data_quality_checkpoint

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: Build, tag, and push image to Amazon ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --region $AWS_REGION --name $EKS_CLUSTER_NAME
        
        # Update image in deployment
        kubectl set image deployment/data-processing-app \
          data-processing-app=${{ steps.login-ecr.outputs.registry }}/$ECR_REPOSITORY:${{ github.sha }} \
          -n data-platform
        
        # Wait for rollout to complete
        kubectl rollout status deployment/data-processing-app -n data-platform

    - name: Run smoke tests
      run: |
        python scripts/smoke_tests.py --environment production

  infrastructure:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: 1.5.0

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Terraform Init
      run: terraform init
      working-directory: ./terraform

    - name: Terraform Plan
      run: terraform plan -var-file="prod.tfvars"
      working-directory: ./terraform

    - name: Terraform Apply
      run: terraform apply -auto-approve -var-file="prod.tfvars"
      working-directory: ./terraform
```

## 5. Configuration Management with Ansible
**What it is**: Automation tool for configuration management, application deployment, and task automation.

**Why important**: Ansible ensures consistent configuration across data infrastructure, automates repetitive tasks, and maintains infrastructure state.

**When to use**:
- Configuring data processing clusters
- Installing and updating software on multiple servers
- Managing configuration files across environments
- Automating data pipeline deployments

**Ansible Examples**:
```yaml
# ansible/playbooks/spark-cluster-setup.yml
---
- name: Setup Spark Cluster
  hosts: spark_cluster
  become: yes
  vars:
    spark_version: "3.5.0"
    hadoop_version: "3"
    java_version: "11"

  tasks:
    - name: Install Java
      package:
        name: "openjdk-{{ java_version }}-jdk"
        state: present

    - name: Create spark user
      user:
        name: spark
        system: yes
        shell: /bin/bash
        home: /opt/spark

    - name: Download Spark
      get_url:
        url: "https://archive.apache.org/dist/spark/spark-{{ spark_version }}/spark-{{ spark_version }}-bin-hadoop{{ hadoop_version }}.tgz"
        dest: "/tmp/spark-{{ spark_version }}-bin-hadoop{{ hadoop_version }}.tgz"
        mode: '0644'

    - name: Extract Spark
      unarchive:
        src: "/tmp/spark-{{ spark_version }}-bin-hadoop{{ hadoop_version }}.tgz"
        dest: /opt
        remote_src: yes
        owner: spark
        group: spark

    - name: Create Spark symlink
      file:
        src: "/opt/spark-{{ spark_version }}-bin-hadoop{{ hadoop_version }}"
        dest: /opt/spark
        state: link
        owner: spark
        group: spark

    - name: Configure Spark environment
      template:
        src: spark-env.sh.j2
        dest: /opt/spark/conf/spark-env.sh
        owner: spark
        group: spark
        mode: '0755'

    - name: Configure Spark defaults
      template:
        src: spark-defaults.conf.j2
        dest: /opt/spark/conf/spark-defaults.conf
        owner: spark
        group: spark
        mode: '0644'

    - name: Start Spark services
      systemd:
        name: "{{ item }}"
        state: started
        enabled: yes
      loop:
        - spark-master
        - spark-worker
      when: inventory_hostname in groups['spark_master'] or inventory_hostname in groups['spark_workers']

# ansible/templates/spark-defaults.conf.j2
# Spark Configuration
spark.master                     {{ spark_master_url }}
spark.eventLog.enabled           true
spark.eventLog.dir               {{ spark_event_log_dir }}
spark.history.fs.logDirectory    {{ spark_history_log_dir }}

# Performance tuning
spark.sql.adaptive.enabled                    true
spark.sql.adaptive.coalescePartitions.enabled true
spark.sql.adaptive.skewJoin.enabled           true

# Memory settings
spark.executor.memory            {{ spark_executor_memory }}
spark.executor.cores             {{ spark_executor_cores }}
spark.driver.memory              {{ spark_driver_memory }}

# Serialization
spark.serializer                 org.apache.spark.serializer.KryoSerializer

# Dynamic allocation
spark.dynamicAllocation.enabled          true
spark.dynamicAllocation.minExecutors     {{ spark_min_executors }}
spark.dynamicAllocation.maxExecutors     {{ spark_max_executors }}
spark.dynamicAllocation.initialExecutors {{ spark_initial_executors }}
```

## 6. Monitoring and Observability
**What it is**: Collecting, analyzing, and acting on data about system performance, health, and behavior.

**Why important**: Monitoring ensures data pipelines run reliably, helps identify bottlenecks, and enables proactive issue resolution.

**When to use**:
- Production data pipeline monitoring
- Performance optimization
- Alerting on data quality issues
- Capacity planning

**Monitoring Stack Example**:
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  # Prometheus for metrics collection
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'

  # Grafana for visualization
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false

  # AlertManager for alerting
  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager

  # Node Exporter for system metrics
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:
```

```python
# monitoring/custom_metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import logging

# Define custom metrics
PIPELINE_RUNS_TOTAL = Counter(
    'data_pipeline_runs_total',
    'Total number of pipeline runs',
    ['pipeline_name', 'status']
)

PIPELINE_DURATION_SECONDS = Histogram(
    'data_pipeline_duration_seconds',
    'Time spent processing pipeline',
    ['pipeline_name']
)

RECORDS_PROCESSED_TOTAL = Counter(
    'data_records_processed_total',
    'Total number of records processed',
    ['pipeline_name', 'stage']
)

DATA_QUALITY_SCORE = Gauge(
    'data_quality_score',
    'Data quality score (0-100)',
    ['dataset_name']
)

class DataPipelineMonitor:
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.logger = logging.getLogger(__name__)
    
    def record_pipeline_start(self):
        """Record pipeline start."""
        self.start_time = time.time()
        self.logger.info(f"Pipeline {self.pipeline_name} started")
    
    def record_pipeline_completion(self, status='success'):
        """Record pipeline completion."""
        duration = time.time() - self.start_time
        
        PIPELINE_RUNS_TOTAL.labels(
            pipeline_name=self.pipeline_name,
            status=status
        ).inc()
        
        PIPELINE_DURATION_SECONDS.labels(
            pipeline_name=self.pipeline_name
        ).observe(duration)
        
        self.logger.info(f"Pipeline {self.pipeline_name} completed with status: {status}")
    
    def record_records_processed(self, stage, count):
        """Record number of records processed."""
        RECORDS_PROCESSED_TOTAL.labels(
            pipeline_name=self.pipeline_name,
            stage=stage
        ).inc(count)
    
    def update_data_quality_score(self, dataset_name, score):
        """Update data quality score."""
        DATA_QUALITY_SCORE.labels(dataset_name=dataset_name).set(score)

# Usage example
if __name__ == "__main__":
    # Start metrics server
    start_http_server(8000)
    
    # Use monitor in pipeline
    monitor = DataPipelineMonitor("customer_etl")
    monitor.record_pipeline_start()
    
    # Simulate pipeline work
    time.sleep(2)
    monitor.record_records_processed("extraction", 1000)
    monitor.record_records_processed("transformation", 950)
    monitor.record_records_processed("loading", 950)
    monitor.update_data_quality_score("customer_data", 95.5)
    
    monitor.record_pipeline_completion("success")
```

These DevOps automation concepts provide the foundation for building reliable, scalable, and maintainable data engineering platforms that can adapt to changing requirements while maintaining high availability and performance.