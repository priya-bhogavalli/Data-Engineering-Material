# DevOps Automation Best Practices for Data Engineering

## 1. Infrastructure as Code (IaC) Best Practices

### Version Control and Structure
```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── modules/
│   ├── data-lake/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── emr-cluster/
│   └── rds-instance/
├── shared/
│   ├── backend.tf
│   └── providers.tf
└── scripts/
    ├── deploy.sh
    └── destroy.sh
```

### Terraform Best Practices
```hcl
# terraform/modules/data-lake/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Use data sources for existing resources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Use locals for computed values
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
    Owner       = var.team_name
  }
  
  bucket_name = "${var.project_name}-data-lake-${var.environment}-${data.aws_caller_identity.current.account_id}"
}

# S3 bucket with proper configuration
resource "aws_s3_bucket" "data_lake" {
  bucket = local.bucket_name
  tags   = local.common_tags
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
      kms_master_key_id = aws_kms_key.data_lake_key.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake_lifecycle" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "data_lifecycle"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# KMS key for encryption
resource "aws_kms_key" "data_lake_key" {
  description             = "KMS key for ${var.project_name} data lake encryption"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  
  tags = local.common_tags
}

resource "aws_kms_alias" "data_lake_key_alias" {
  name          = "alias/${var.project_name}-data-lake-${var.environment}"
  target_key_id = aws_kms_key.data_lake_key.key_id
}

# Variables with validation
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}

# Outputs
output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.data_lake.bucket
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.data_lake.arn
}

output "kms_key_id" {
  description = "ID of the KMS key"
  value       = aws_kms_key.data_lake_key.key_id
}
```

### Remote State Management
```hcl
# terraform/shared/backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "data-platform/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    
    # Workspace-specific state files
    workspace_key_prefix = "workspaces"
  }
}

# Create backend resources
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-bucket"
  
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name           = "terraform-locks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

## 2. Container Best Practices

### Multi-stage Docker Builds
```dockerfile
# Dockerfile for PySpark application
# Stage 1: Build dependencies
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime image
FROM apache/spark:3.5.0-python3

# Create non-root user
RUN groupadd -r spark && useradd -r -g spark spark

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/spark/.local

# Copy application code
COPY --chown=spark:spark src/ /app/src/
COPY --chown=spark:spark config/ /app/config/

# Set environment variables
ENV PATH=/home/spark/.local/bin:$PATH
ENV PYTHONPATH=/app/src:$PYTHONPATH
ENV SPARK_HOME=/opt/spark

# Switch to non-root user
USER spark

WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["spark-submit", "--master", "local[*]", "src/main.py"]
```

### Docker Compose for Development
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  # Data processing application
  data-processor:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - ./src:/app/src:ro
      - ./config:/app/config:ro
      - ./data:/app/data
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    depends_on:
      - postgres
      - redis
    networks:
      - data-platform

  # PostgreSQL database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-dataplatform}
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init:/docker-entrypoint-initdb.d:ro
    ports:
      - "5432:5432"
    networks:
      - data-platform
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis for caching
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - data-platform
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Jupyter for development
  jupyter:
    image: jupyter/pyspark-notebook:latest
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./src:/home/jovyan/src:ro
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - GRANT_SUDO=yes
    networks:
      - data-platform

  # MinIO for S3-compatible storage
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
    volumes:
      - minio_data:/data
    networks:
      - data-platform
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

volumes:
  postgres_data:
  redis_data:
  minio_data:

networks:
  data-platform:
    driver: bridge
```

### Container Security Best Practices
```dockerfile
# Secure Dockerfile example
FROM python:3.9-slim

# Create non-root user early
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages as root, then switch user
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Remove unnecessary packages and files
RUN find /usr/local/lib/python3.9/site-packages -name "*.pyc" -delete && \
    find /usr/local/lib/python3.9/site-packages -name "__pycache__" -delete

# Set security-focused environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/appuser/.local/bin:$PATH"

# Expose port (non-privileged)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run application
CMD ["python", "app.py"]
```

## 3. Kubernetes Best Practices

### Resource Management
```yaml
# k8s/data-processing-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processing
  namespace: data-platform
  labels:
    app: data-processing
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: data-processing
  template:
    metadata:
      labels:
        app: data-processing
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: data-processing-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: data-processor
        image: data-processing:v1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 8081
          name: metrics
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "INFO"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
            ephemeral-storage: "1Gi"
          limits:
            memory: "2Gi"
            cpu: "1000m"
            ephemeral-storage: "2Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
          readOnly: true
        - name: temp-storage
          mountPath: /tmp
      volumes:
      - name: config-volume
        configMap:
          name: data-processing-config
      - name: temp-storage
        emptyDir:
          sizeLimit: 1Gi
      nodeSelector:
        workload-type: data-processing
      tolerations:
      - key: "data-processing"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - data-processing
              topologyKey: kubernetes.io/hostname
```

### Auto-scaling Configuration
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: data-processing-hpa
  namespace: data-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-processing
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: pending_jobs
      target:
        type: AverageValue
        averageValue: "5"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max

---
# Vertical Pod Autoscaler
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: data-processing-vpa
  namespace: data-platform
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-processing
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: data-processor
      maxAllowed:
        cpu: 4
        memory: 8Gi
      minAllowed:
        cpu: 100m
        memory: 128Mi
      controlledResources: ["cpu", "memory"]
```

### Network Policies
```yaml
# k8s/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: data-processing-network-policy
  namespace: data-platform
spec:
  podSelector:
    matchLabels:
      app: data-processing
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: api-gateway
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8080
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 8081
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS
    - protocol: TCP
      port: 53   # DNS
    - protocol: UDP
      port: 53   # DNS
```

## 4. CI/CD Pipeline Best Practices

### Pipeline Security
```yaml
# .github/workflows/secure-pipeline.yml
name: Secure Data Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run Semgrep security scan
      uses: returntocorp/semgrep-action@v1
      with:
        config: >-
          p/security-audit
          p/secrets
          p/python
    
    - name: Check for secrets
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: main
        head: HEAD

  build-and-scan:
    needs: security-scan
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Run Trivy container scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-container-results.sarif'
    
    - name: Upload container scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-container-results.sarif'

  deploy:
    needs: build-and-scan
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
        aws-region: us-east-1
    
    - name: Deploy with Helm
      run: |
        aws eks update-kubeconfig --region us-east-1 --name prod-cluster
        
        helm upgrade --install data-platform ./helm/data-platform \
          --namespace data-platform \
          --create-namespace \
          --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }} \
          --set image.tag=${{ github.sha }} \
          --set environment=production \
          --wait \
          --timeout=10m
    
    - name: Run smoke tests
      run: |
        kubectl wait --for=condition=available --timeout=300s deployment/data-platform
        python scripts/smoke_tests.py --environment production
```

### GitOps with ArgoCD
```yaml
# argocd/application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: data-platform
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/company/data-platform-config
    targetRevision: HEAD
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: data-platform
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
```

## 5. Monitoring and Observability

### Comprehensive Monitoring Stack
```yaml
# monitoring/prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - "/etc/prometheus/rules/*.yml"
    
    alerting:
      alertmanagers:
        - static_configs:
            - targets:
              - alertmanager:9093
    
    scrape_configs:
      # Kubernetes API server
      - job_name: 'kubernetes-apiservers'
        kubernetes_sd_configs:
        - role: endpoints
        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
        - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
          action: keep
          regex: default;kubernetes;https
      
      # Data platform applications
      - job_name: 'data-platform'
        kubernetes_sd_configs:
        - role: pod
        relabel_configs:
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
          action: keep
          regex: true
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
          action: replace
          target_label: __metrics_path__
          regex: (.+)
        - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
          action: replace
          regex: ([^:]+)(?::\d+)?;(\d+)
          replacement: $1:$2
          target_label: __address__
        - action: labelmap
          regex: __meta_kubernetes_pod_label_(.+)
        - source_labels: [__meta_kubernetes_namespace]
          action: replace
          target_label: kubernetes_namespace
        - source_labels: [__meta_kubernetes_pod_name]
          action: replace
          target_label: kubernetes_pod_name

  # Alert rules
  alerts.yml: |
    groups:
    - name: data-platform.rules
      rules:
      - alert: DataPipelineDown
        expr: up{job="data-platform"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Data pipeline is down"
          description: "Data pipeline {{ $labels.instance }} has been down for more than 1 minute."
      
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second."
      
      - alert: HighMemoryUsage
        expr: (container_memory_usage_bytes / container_spec_memory_limit_bytes) > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Container {{ $labels.container }} is using {{ $value | humanizePercentage }} of its memory limit."
```

### Custom Metrics and Dashboards
```python
# monitoring/metrics_collector.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import logging
from typing import Dict, Any

# Define custom metrics
PIPELINE_EXECUTIONS = Counter(
    'data_pipeline_executions_total',
    'Total number of pipeline executions',
    ['pipeline_name', 'status', 'environment']
)

PIPELINE_DURATION = Histogram(
    'data_pipeline_duration_seconds',
    'Time spent executing pipeline',
    ['pipeline_name', 'environment'],
    buckets=[1, 5, 10, 30, 60, 300, 600, 1800, 3600]
)

RECORDS_PROCESSED = Counter(
    'data_records_processed_total',
    'Total number of records processed',
    ['pipeline_name', 'stage', 'environment']
)

DATA_QUALITY_SCORE = Gauge(
    'data_quality_score',
    'Data quality score (0-100)',
    ['dataset_name', 'environment']
)

ACTIVE_CONNECTIONS = Gauge(
    'database_connections_active',
    'Number of active database connections',
    ['database_name', 'environment']
)

class MetricsCollector:
    def __init__(self, environment: str):
        self.environment = environment
        self.logger = logging.getLogger(__name__)
    
    def record_pipeline_execution(self, pipeline_name: str, status: str, duration: float):
        """Record pipeline execution metrics."""
        PIPELINE_EXECUTIONS.labels(
            pipeline_name=pipeline_name,
            status=status,
            environment=self.environment
        ).inc()
        
        PIPELINE_DURATION.labels(
            pipeline_name=pipeline_name,
            environment=self.environment
        ).observe(duration)
    
    def record_data_processing(self, pipeline_name: str, stage: str, record_count: int):
        """Record data processing metrics."""
        RECORDS_PROCESSED.labels(
            pipeline_name=pipeline_name,
            stage=stage,
            environment=self.environment
        ).inc(record_count)
    
    def update_data_quality_score(self, dataset_name: str, score: float):
        """Update data quality score."""
        DATA_QUALITY_SCORE.labels(
            dataset_name=dataset_name,
            environment=self.environment
        ).set(score)
    
    def update_database_connections(self, database_name: str, connection_count: int):
        """Update active database connections."""
        ACTIVE_CONNECTIONS.labels(
            database_name=database_name,
            environment=self.environment
        ).set(connection_count)

# Usage example
if __name__ == "__main__":
    # Start metrics server
    start_http_server(8000)
    
    collector = MetricsCollector("production")
    
    # Simulate metrics collection
    while True:
        # Simulate pipeline execution
        start_time = time.time()
        time.sleep(2)  # Simulate work
        duration = time.time() - start_time
        
        collector.record_pipeline_execution("customer_etl", "success", duration)
        collector.record_data_processing("customer_etl", "extraction", 1000)
        collector.record_data_processing("customer_etl", "transformation", 950)
        collector.update_data_quality_score("customer_data", 95.5)
        collector.update_database_connections("postgres", 15)
        
        time.sleep(30)
```

These best practices ensure robust, secure, and maintainable DevOps automation for data engineering platforms, covering infrastructure management, containerization, orchestration, and comprehensive monitoring.