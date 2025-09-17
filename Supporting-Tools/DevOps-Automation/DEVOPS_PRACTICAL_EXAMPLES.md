# 🚀 DevOps Practical Examples for Data Engineering

## 🐳 **Docker for Data Pipelines**

### **Data Processing Container**
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Set environment variables
ENV PYTHONPATH=/app
ENV DATA_PATH=/data

# Create data directory
RUN mkdir -p /data

# Run the application
CMD ["python", "src/main.py"]
```

### **Multi-Service Data Stack**
```yaml
# docker-compose.yml
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: datawarehouse
      POSTGRES_USER: dataeng
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - data_network

  # Redis for caching
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    networks:
      - data_network

  # Data processing service
  data_processor:
    build: .
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://dataeng:secure_password@postgres:5432/datawarehouse
      REDIS_URL: redis://redis:6379
    volumes:
      - ./data:/data
      - ./logs:/app/logs
    networks:
      - data_network

  # Jupyter for analysis
  jupyter:
    image: jupyter/datascience-notebook
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./data:/home/jovyan/data
    environment:
      JUPYTER_ENABLE_LAB: "yes"
    networks:
      - data_network

  # Monitoring
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - data_network

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - data_network

volumes:
  postgres_data:
  grafana_data:

networks:
  data_network:
    driver: bridge
```

## ☸️ **Kubernetes for Data Workloads**

### **Data Pipeline Deployment**
```yaml
# k8s/namespace.yml
apiVersion: v1
kind: Namespace
metadata:
  name: data-engineering
---
# k8s/configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: data-config
  namespace: data-engineering
data:
  database_host: "postgres-service"
  redis_host: "redis-service"
  log_level: "INFO"
---
# k8s/secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: data-secrets
  namespace: data-engineering
type: Opaque
data:
  database_password: c2VjdXJlX3Bhc3N3b3Jk  # base64 encoded
  api_key: eW91cl9hcGlfa2V5X2hlcmU=  # base64 encoded
---
# k8s/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processor
  namespace: data-engineering
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-processor
  template:
    metadata:
      labels:
        app: data-processor
    spec:
      containers:
      - name: data-processor
        image: my-registry/data-processor:v1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_HOST
          valueFrom:
            configMapKeyRef:
              name: data-config
              key: database_host
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: data-secrets
              key: database_password
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
# k8s/service.yml
apiVersion: v1
kind: Service
metadata:
  name: data-processor-service
  namespace: data-engineering
spec:
  selector:
    app: data-processor
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

### **Spark on Kubernetes**
```yaml
# k8s/spark-job.yml
apiVersion: batch/v1
kind: Job
metadata:
  name: spark-data-job
  namespace: data-engineering
spec:
  template:
    spec:
      containers:
      - name: spark-driver
        image: apache/spark:3.4.0
        command: ["/opt/spark/bin/spark-submit"]
        args:
          - "--master"
          - "k8s://https://kubernetes.default.svc:443"
          - "--deploy-mode"
          - "cluster"
          - "--name"
          - "data-processing-job"
          - "--conf"
          - "spark.executor.instances=3"
          - "--conf"
          - "spark.kubernetes.container.image=apache/spark:3.4.0"
          - "--conf"
          - "spark.kubernetes.namespace=data-engineering"
          - "/opt/spark/examples/jars/spark-examples_2.12-3.4.0.jar"
        env:
        - name: SPARK_CONF_DIR
          value: "/opt/spark/conf"
      restartPolicy: Never
  backoffLimit: 3
```

## 🏗️ **Terraform Infrastructure**

### **AWS Data Infrastructure**
```hcl
# terraform/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

# Data Lake S3 Bucket
resource "aws_s3_bucket" "data_lake" {
  bucket = "data-lake-${var.environment}-${random_string.suffix.result}"
}

resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake_encryption" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# VPC for data services
resource "aws_vpc" "data_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "data-vpc-${var.environment}"
    Environment = var.environment
  }
}

# Subnets
resource "aws_subnet" "private_subnet" {
  count             = 2
  vpc_id            = aws_vpc.data_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-subnet-${count.index + 1}-${var.environment}"
  }
}

resource "aws_subnet" "public_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.data_vpc.id
  cidr_block              = "10.0.${count.index + 10}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index + 1}-${var.environment}"
  }
}

# RDS Database
resource "aws_db_instance" "data_warehouse" {
  identifier     = "data-warehouse-${var.environment}"
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"
  storage_encrypted     = true

  db_name  = "datawarehouse"
  username = "dataeng"
  password = random_password.db_password.result

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.data_subnet_group.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  skip_final_snapshot = true

  tags = {
    Name        = "data-warehouse-${var.environment}"
    Environment = var.environment
  }
}

# EKS Cluster for data processing
resource "aws_eks_cluster" "data_cluster" {
  name     = "data-cluster-${var.environment}"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.27"

  vpc_config {
    subnet_ids = concat(aws_subnet.private_subnet[*].id, aws_subnet.public_subnet[*].id)
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
  ]

  tags = {
    Name        = "data-cluster-${var.environment}"
    Environment = var.environment
  }
}

# Random resources
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "random_password" "db_password" {
  length  = 16
  special = true
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

# Outputs
output "s3_bucket_name" {
  value = aws_s3_bucket.data_lake.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.data_warehouse.endpoint
}

output "eks_cluster_name" {
  value = aws_eks_cluster.data_cluster.name
}
```

## 🔄 **CI/CD Pipeline**

### **GitHub Actions for Data Pipeline**
```yaml
# .github/workflows/data-pipeline.yml
name: Data Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
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
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 src/ tests/
        black --check src/ tests/
        isort --check-only src/ tests/
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --name data-cluster-prod
        kubectl set image deployment/data-processor data-processor=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main-${{ github.sha }}
        kubectl rollout status deployment/data-processor
```

### **Jenkins Pipeline**
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        IMAGE_NAME = 'data-processor'
        KUBECONFIG = credentials('kubeconfig')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh '''
                            python -m venv venv
                            source venv/bin/activate
                            pip install -r requirements.txt
                            pytest tests/unit/
                        '''
                    }
                }
                
                stage('Integration Tests') {
                    steps {
                        sh '''
                            docker-compose -f docker-compose.test.yml up -d
                            sleep 30
                            source venv/bin/activate
                            pytest tests/integration/
                            docker-compose -f docker-compose.test.yml down
                        '''
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    def image = docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                sh '''
                    kubectl config use-context staging
                    kubectl set image deployment/data-processor data-processor=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                    kubectl rollout status deployment/data-processor
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                sh '''
                    kubectl config use-context production
                    kubectl set image deployment/data-processor data-processor=${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                    kubectl rollout status deployment/data-processor
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            emailext (
                subject: "Pipeline Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Build failed. Check console output at ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

## 📊 **Monitoring Setup**

### **Prometheus Configuration**
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'data-processor'
    kubernetes_sd_configs:
      - role: endpoints
        namespaces:
          names:
            - data-engineering
    relabel_configs:
      - source_labels: [__meta_kubernetes_service_name]
        action: keep
        regex: data-processor-service

  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'node-exporter'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
```

### **Grafana Dashboard**
```json
{
  "dashboard": {
    "title": "Data Pipeline Monitoring",
    "panels": [
      {
        "title": "Pipeline Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(data_pipeline_success_total[5m]) / rate(data_pipeline_total[5m]) * 100"
          }
        ]
      },
      {
        "title": "Data Processing Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(data_processing_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "Database Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "pg_stat_database_numbackends"
          }
        ]
      }
    ]
  }
}
```

## 🔧 **Quick Commands**

### **Docker Commands**
```bash
# Build and run
docker build -t data-processor .
docker run -d --name data-app -p 8080:8080 data-processor

# Compose operations
docker-compose up -d
docker-compose logs -f data_processor
docker-compose exec postgres psql -U dataeng -d datawarehouse

# Cleanup
docker system prune -a
docker volume prune
```

### **Kubernetes Commands**
```bash
# Deploy application
kubectl apply -f k8s/
kubectl get pods -n data-engineering
kubectl logs -f deployment/data-processor -n data-engineering

# Scale deployment
kubectl scale deployment data-processor --replicas=5 -n data-engineering

# Port forwarding
kubectl port-forward service/data-processor-service 8080:80 -n data-engineering

# Debug
kubectl exec -it pod/data-processor-xxx -n data-engineering -- /bin/bash
```

### **Terraform Commands**
```bash
# Initialize and plan
terraform init
terraform plan -var="environment=dev"
terraform apply -var="environment=dev"

# Destroy resources
terraform destroy -var="environment=dev"

# State management
terraform state list
terraform state show aws_s3_bucket.data_lake
```

---

*Updated: December 2024 | Examples: Production-ready | Complexity: Beginner to Advanced*