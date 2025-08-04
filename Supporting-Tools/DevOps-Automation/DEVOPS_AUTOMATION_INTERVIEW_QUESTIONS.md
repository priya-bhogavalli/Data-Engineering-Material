# DevOps Automation Interview Questions for Data Engineering

## Basic Level (0-2 years experience)

### 1. What is Infrastructure as Code (IaC) and why is it important for data engineering?

**Answer:**
Infrastructure as Code (IaC) is the practice of managing and provisioning infrastructure through code rather than manual processes.

**Importance for Data Engineering:**
- **Reproducibility**: Ensures consistent environments across dev, staging, and production
- **Version Control**: Infrastructure changes can be tracked and rolled back
- **Scalability**: Easy to scale data processing resources up or down
- **Documentation**: Infrastructure is self-documenting through code
- **Automation**: Reduces manual errors and deployment time

**Example:**
```hcl
# Terraform example for data lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-${var.environment}"
  
  tags = {
    Environment = var.environment
    Purpose     = "DataLake"
  }
}

resource "aws_glue_catalog_database" "data_catalog" {
  name = "data_catalog_${var.environment}"
}
```

### 2. Explain the difference between containers and virtual machines.

**Answer:**
- **Virtual Machines (VMs)**:
  - Include full operating system
  - Higher resource overhead
  - Slower startup times
  - Better isolation
  - Suitable for running multiple different OS

- **Containers**:
  - Share host OS kernel
  - Lightweight and efficient
  - Fast startup times
  - Process-level isolation
  - Ideal for microservices and data processing jobs

**Data Engineering Use Case:**
```dockerfile
# Container for Spark job
FROM apache/spark:3.5.0-python3

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
CMD ["spark-submit", "src/etl_job.py"]
```

### 3. What is CI/CD and how does it apply to data pipelines?

**Answer:**
**CI/CD** stands for Continuous Integration/Continuous Deployment.

**Continuous Integration (CI):**
- Automatically test code changes
- Validate data transformations
- Run data quality checks
- Build and package applications

**Continuous Deployment (CD):**
- Automatically deploy to different environments
- Update data pipeline configurations
- Deploy infrastructure changes

**Data Pipeline CI/CD Example:**
```yaml
# GitHub Actions workflow
name: Data Pipeline CI/CD
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run data quality tests
      run: |
        pytest tests/
        great_expectations checkpoint run data_quality
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        kubectl apply -f k8s/
```

## Intermediate Level (2-5 years experience)

### 4. How would you implement blue-green deployment for a data pipeline?

**Answer:**
Blue-green deployment maintains two identical production environments, switching traffic between them for zero-downtime deployments.

**Implementation Strategy:**
```yaml
# Blue environment (current production)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-pipeline-blue
  labels:
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-pipeline
      version: blue
  template:
    metadata:
      labels:
        app: data-pipeline
        version: blue
    spec:
      containers:
      - name: pipeline
        image: data-pipeline:v1.0
        
---
# Green environment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-pipeline-green
  labels:
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-pipeline
      version: green
  template:
    metadata:
      labels:
        app: data-pipeline
        version: green
    spec:
      containers:
      - name: pipeline
        image: data-pipeline:v2.0

---
# Service that switches between blue and green
apiVersion: v1
kind: Service
metadata:
  name: data-pipeline-service
spec:
  selector:
    app: data-pipeline
    version: blue  # Switch to 'green' for deployment
  ports:
  - port: 80
    targetPort: 8080
```

**Deployment Process:**
1. Deploy green environment with new version
2. Run smoke tests on green environment
3. Switch service selector from blue to green
4. Monitor for issues
5. Keep blue environment for quick rollback if needed

### 5. Explain how you would use Kubernetes for auto-scaling data processing workloads.

**Answer:**
Kubernetes provides multiple auto-scaling mechanisms for data workloads:

**Horizontal Pod Autoscaler (HPA):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: spark-driver-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: spark-driver
  minReplicas: 2
  maxReplicas: 10
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
```

**Vertical Pod Autoscaler (VPA):**
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: data-processing-vpa
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
```

**Custom Metrics Scaling:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: queue-based-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-processor
  minReplicas: 1
  maxReplicas: 20
  metrics:
  - type: External
    external:
      metric:
        name: sqs_messages_visible
        selector:
          matchLabels:
            queue_name: data-processing-queue
      target:
        type: AverageValue
        averageValue: "5"
```

### 6. How do you handle secrets management in a data engineering environment?

**Answer:**
Secrets management is crucial for protecting database credentials, API keys, and other sensitive information.

**Kubernetes Secrets:**
```yaml
# Create secret
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: cGFzc3dvcmQ=  # base64 encoded

---
# Use secret in deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-pipeline
spec:
  template:
    spec:
      containers:
      - name: pipeline
        image: data-pipeline:latest
        env:
        - name: DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: password
```

**External Secret Management (AWS Secrets Manager):**
```python
import boto3
import json

class SecretsManager:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)
    
    def get_secret(self, secret_name):
        """Retrieve secret from AWS Secrets Manager."""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            return None
    
    def get_database_credentials(self, secret_name):
        """Get database credentials."""
        secret = self.get_secret(secret_name)
        if secret:
            return {
                'host': secret['host'],
                'username': secret['username'],
                'password': secret['password'],
                'database': secret['database']
            }
        return None

# Usage
secrets_manager = SecretsManager()
db_creds = secrets_manager.get_database_credentials('prod/database/credentials')
```

**HashiCorp Vault Integration:**
```python
import hvac

class VaultClient:
    def __init__(self, vault_url, vault_token):
        self.client = hvac.Client(url=vault_url, token=vault_token)
    
    def get_database_credentials(self, path):
        """Get database credentials from Vault."""
        response = self.client.secrets.kv.v2.read_secret_version(path=path)
        return response['data']['data']
    
    def get_dynamic_database_credentials(self, role_name):
        """Get dynamic database credentials."""
        response = self.client.secrets.database.generate_credentials(name=role_name)
        return {
            'username': response['data']['username'],
            'password': response['data']['password']
        }

# Usage
vault = VaultClient('https://vault.company.com', 'vault-token')
creds = vault.get_dynamic_database_credentials('data-engineer-role')
```

## Advanced Level (5+ years experience)

### 7. Design a complete CI/CD pipeline for a multi-environment data platform.

**Answer:**
A comprehensive CI/CD pipeline for data platforms should handle code, infrastructure, and data validation across multiple environments.

**Pipeline Architecture:**
```yaml
# .github/workflows/data-platform-cicd.yml
name: Data Platform CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  AWS_REGION: us-east-1
  TERRAFORM_VERSION: 1.5.0

jobs:
  # Stage 1: Code Quality and Testing
  code-quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Code linting
      run: |
        flake8 src/ tests/
        black --check src/ tests/
        isort --check-only src/ tests/
    
    - name: Security scan
      run: |
        bandit -r src/
        safety check
    
    - name: Unit tests
      run: |
        pytest tests/unit/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  # Stage 2: Infrastructure Validation
  infrastructure-validation:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TERRAFORM_VERSION }}
    
    - name: Terraform Format Check
      run: terraform fmt -check -recursive
      working-directory: ./terraform
    
    - name: Terraform Validate
      run: |
        terraform init -backend=false
        terraform validate
      working-directory: ./terraform
    
    - name: Terraform Security Scan
      uses: aquasecurity/tfsec-action@v1.0.0
      with:
        working_directory: ./terraform

  # Stage 3: Integration Testing
  integration-tests:
    needs: [code-quality, infrastructure-validation]
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run integration tests
      run: pytest tests/integration/ -v
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/postgres
        REDIS_URL: redis://localhost:6379
    
    - name: Data quality tests
      run: |
        great_expectations checkpoint run integration_data_quality

  # Stage 4: Build and Push Images
  build-and-push:
    needs: [code-quality, infrastructure-validation, integration-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    
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
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ steps.login-ecr.outputs.registry }}/data-platform
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}
    
    - name: Build and push Docker image
      id: build
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}

  # Stage 5: Deploy to Development
  deploy-dev:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: development
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy Infrastructure
      run: |
        terraform init
        terraform plan -var-file="dev.tfvars"
        terraform apply -auto-approve -var-file="dev.tfvars"
      working-directory: ./terraform
      env:
        TF_VAR_image_tag: ${{ needs.build-and-push.outputs.image-tag }}
    
    - name: Deploy Applications
      run: |
        aws eks update-kubeconfig --region ${{ env.AWS_REGION }} --name dev-cluster
        helm upgrade --install data-platform ./helm/data-platform \
          --namespace data-platform \
          --set image.tag=${{ needs.build-and-push.outputs.image-tag }} \
          --values helm/values-dev.yaml
    
    - name: Run smoke tests
      run: python scripts/smoke_tests.py --environment dev

  # Stage 6: Deploy to Staging
  deploy-staging:
    needs: [build-and-push, deploy-dev]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy Infrastructure
      run: |
        terraform init
        terraform plan -var-file="staging.tfvars"
        terraform apply -auto-approve -var-file="staging.tfvars"
      working-directory: ./terraform
      env:
        TF_VAR_image_tag: ${{ needs.build-and-push.outputs.image-tag }}
    
    - name: Deploy Applications
      run: |
        aws eks update-kubeconfig --region ${{ env.AWS_REGION }} --name staging-cluster
        helm upgrade --install data-platform ./helm/data-platform \
          --namespace data-platform \
          --set image.tag=${{ needs.build-and-push.outputs.image-tag }} \
          --values helm/values-staging.yaml
    
    - name: Run end-to-end tests
      run: python scripts/e2e_tests.py --environment staging
    
    - name: Performance tests
      run: python scripts/performance_tests.py --environment staging

  # Stage 7: Deploy to Production
  deploy-production:
    needs: [build-and-push, deploy-staging]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy Infrastructure
      run: |
        terraform init
        terraform plan -var-file="prod.tfvars"
        terraform apply -auto-approve -var-file="prod.tfvars"
      working-directory: ./terraform
      env:
        TF_VAR_image_tag: ${{ needs.build-and-push.outputs.image-tag }}
    
    - name: Blue-Green Deployment
      run: |
        aws eks update-kubeconfig --region ${{ env.AWS_REGION }} --name prod-cluster
        
        # Deploy to green environment
        helm upgrade --install data-platform-green ./helm/data-platform \
          --namespace data-platform \
          --set image.tag=${{ needs.build-and-push.outputs.image-tag }} \
          --set environment=green \
          --values helm/values-prod.yaml
        
        # Wait for green to be ready
        kubectl wait --for=condition=available --timeout=300s deployment/data-platform-green
        
        # Run production smoke tests on green
        python scripts/smoke_tests.py --environment prod --target green
        
        # Switch traffic to green
        kubectl patch service data-platform-service -p '{"spec":{"selector":{"version":"green"}}}'
        
        # Monitor for 5 minutes
        sleep 300
        
        # If successful, remove blue deployment
        helm uninstall data-platform-blue --namespace data-platform || true
        
        # Rename green to blue for next deployment
        helm upgrade data-platform-blue ./helm/data-platform \
          --namespace data-platform \
          --set image.tag=${{ needs.build-and-push.outputs.image-tag }} \
          --set environment=blue \
          --values helm/values-prod.yaml
    
    - name: Post-deployment monitoring
      run: |
        python scripts/monitor_deployment.py --environment prod --duration 600
    
    - name: Notify stakeholders
      run: |
        python scripts/notify_deployment.py --environment prod --status success
```

### 8. How would you implement disaster recovery for a containerized data platform?

**Answer:**
Disaster recovery for containerized data platforms requires multi-layered approach covering data, applications, and infrastructure.

**Multi-Region Architecture:**
```yaml
# terraform/disaster-recovery.tf
# Primary region resources
resource "aws_eks_cluster" "primary" {
  provider = aws.primary
  name     = "data-platform-primary"
  
  vpc_config {
    subnet_ids = var.primary_subnet_ids
  }
}

# Secondary region resources
resource "aws_eks_cluster" "secondary" {
  provider = aws.secondary
  name     = "data-platform-secondary"
  
  vpc_config {
    subnet_ids = var.secondary_subnet_ids
  }
}

# Cross-region S3 replication
resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.primary
  
  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket.primary_data_lake.id

  rule {
    id     = "replicate_to_secondary"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.secondary_data_lake.arn
      storage_class = "STANDARD_IA"
    }
  }
}

# RDS Cross-region automated backups
resource "aws_db_instance" "primary" {
  provider = aws.primary
  
  identifier = "data-platform-primary"
  
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  copy_tags_to_snapshot  = true
  
  # Enable automated backups to secondary region
  enabled_cloudwatch_logs_exports = ["postgresql"]
}
```

**Application-Level DR Strategy:**
```python
# disaster_recovery/dr_manager.py
import boto3
import kubernetes
import time
from typing import Dict, List

class DisasterRecoveryManager:
    def __init__(self, primary_region: str, secondary_region: str):
        self.primary_region = primary_region
        self.secondary_region = secondary_region
        self.primary_k8s = self._get_k8s_client(primary_region)
        self.secondary_k8s = self._get_k8s_client(secondary_region)
    
    def _get_k8s_client(self, region: str):
        """Get Kubernetes client for specific region."""
        session = boto3.Session(region_name=region)
        eks = session.client('eks')
        
        cluster_name = f"data-platform-{region}"
        cluster_info = eks.describe_cluster(name=cluster_name)
        
        # Configure kubectl context
        # Implementation depends on your authentication method
        return kubernetes.client.ApiClient()
    
    def check_primary_health(self) -> bool:
        """Check if primary region is healthy."""
        try:
            # Check EKS cluster health
            v1 = kubernetes.client.CoreV1Api(self.primary_k8s)
            nodes = v1.list_node()
            
            healthy_nodes = sum(1 for node in nodes.items 
                              if self._is_node_ready(node))
            
            # Require at least 50% of nodes to be healthy
            return healthy_nodes >= len(nodes.items) * 0.5
            
        except Exception as e:
            print(f"Primary region health check failed: {e}")
            return False
    
    def _is_node_ready(self, node) -> bool:
        """Check if a node is ready."""
        for condition in node.status.conditions:
            if condition.type == "Ready":
                return condition.status == "True"
        return False
    
    def initiate_failover(self) -> bool:
        """Initiate failover to secondary region."""
        try:
            print("Initiating failover to secondary region...")
            
            # 1. Update DNS to point to secondary region
            self._update_dns_records()
            
            # 2. Scale up secondary region applications
            self._scale_secondary_applications()
            
            # 3. Restore database from latest backup
            self._restore_database_in_secondary()
            
            # 4. Update application configurations
            self._update_app_configs_for_secondary()
            
            # 5. Verify secondary region health
            if self._verify_secondary_health():
                print("Failover completed successfully")
                return True
            else:
                print("Failover verification failed")
                return False
                
        except Exception as e:
            print(f"Failover failed: {e}")
            return False
    
    def _update_dns_records(self):
        """Update Route53 records to point to secondary region."""
        route53 = boto3.client('route53')
        
        # Update A record to point to secondary region load balancer
        route53.change_resource_record_sets(
            HostedZoneId='Z123456789',
            ChangeBatch={
                'Changes': [{
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'data-platform.company.com',
                        'Type': 'CNAME',
                        'TTL': 60,
                        'ResourceRecords': [
                            {'Value': f'data-platform-{self.secondary_region}.elb.amazonaws.com'}
                        ]
                    }
                }]
            }
        )
    
    def _scale_secondary_applications(self):
        """Scale up applications in secondary region."""
        apps_v1 = kubernetes.client.AppsV1Api(self.secondary_k8s)
        
        # Scale up critical applications
        critical_apps = [
            'data-ingestion',
            'data-processing',
            'api-gateway',
            'monitoring'
        ]
        
        for app in critical_apps:
            try:
                # Scale deployment to production levels
                apps_v1.patch_namespaced_deployment_scale(
                    name=app,
                    namespace='data-platform',
                    body={'spec': {'replicas': 3}}
                )
                print(f"Scaled {app} to 3 replicas")
            except Exception as e:
                print(f"Failed to scale {app}: {e}")
    
    def _restore_database_in_secondary(self):
        """Restore database from latest backup in secondary region."""
        rds = boto3.client('rds', region_name=self.secondary_region)
        
        # Get latest automated backup
        snapshots = rds.describe_db_snapshots(
            DBInstanceIdentifier=f'data-platform-{self.primary_region}',
            SnapshotType='automated'
        )
        
        latest_snapshot = max(snapshots['DBSnapshots'], 
                            key=lambda x: x['SnapshotCreateTime'])
        
        # Restore from snapshot
        rds.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=f'data-platform-{self.secondary_region}',
            DBSnapshotIdentifier=latest_snapshot['DBSnapshotIdentifier'],
            DBInstanceClass='db.r5.large',
            MultiAZ=True
        )
        
        # Wait for database to be available
        waiter = rds.get_waiter('db_instance_available')
        waiter.wait(DBInstanceIdentifier=f'data-platform-{self.secondary_region}')
    
    def _verify_secondary_health(self) -> bool:
        """Verify secondary region is healthy after failover."""
        # Check application health endpoints
        health_checks = [
            self._check_api_health(),
            self._check_database_health(),
            self._check_processing_health()
        ]
        
        return all(health_checks)
    
    def initiate_failback(self) -> bool:
        """Failback to primary region when it's healthy again."""
        if not self.check_primary_health():
            print("Primary region not healthy, cannot failback")
            return False
        
        try:
            print("Initiating failback to primary region...")
            
            # 1. Sync data from secondary to primary
            self._sync_data_to_primary()
            
            # 2. Scale up primary applications
            self._scale_primary_applications()
            
            # 3. Update DNS back to primary
            self._update_dns_to_primary()
            
            # 4. Scale down secondary applications
            self._scale_down_secondary()
            
            print("Failback completed successfully")
            return True
            
        except Exception as e:
            print(f"Failback failed: {e}")
            return False

# Automated DR monitoring
class DRMonitor:
    def __init__(self, dr_manager: DisasterRecoveryManager):
        self.dr_manager = dr_manager
        self.failover_initiated = False
    
    def monitor_and_respond(self):
        """Continuously monitor and respond to failures."""
        while True:
            try:
                if not self.dr_manager.check_primary_health():
                    if not self.failover_initiated:
                        print("Primary region failure detected, initiating failover...")
                        success = self.dr_manager.initiate_failover()
                        self.failover_initiated = success
                else:
                    if self.failover_initiated:
                        print("Primary region recovered, initiating failback...")
                        success = self.dr_manager.initiate_failback()
                        if success:
                            self.failover_initiated = False
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"DR monitoring error: {e}")
                time.sleep(60)

# Usage
if __name__ == "__main__":
    dr_manager = DisasterRecoveryManager('us-east-1', 'us-west-2')
    dr_monitor = DRMonitor(dr_manager)
    dr_monitor.monitor_and_respond()
```

**Data Backup and Recovery Strategy:**
```python
# backup/backup_manager.py
import boto3
import subprocess
import schedule
import time
from datetime import datetime, timedelta

class DataBackupManager:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.rds = boto3.client('rds')
        self.backup_bucket = 'data-platform-backups'
    
    def backup_databases(self):
        """Backup all databases."""
        databases = [
            'metadata-db',
            'analytics-db',
            'user-db'
        ]
        
        for db in databases:
            try:
                snapshot_id = f"{db}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                
                self.rds.create_db_snapshot(
                    DBSnapshotIdentifier=snapshot_id,
                    DBInstanceIdentifier=db
                )
                
                print(f"Created snapshot {snapshot_id} for {db}")
                
            except Exception as e:
                print(f"Failed to backup {db}: {e}")
    
    def backup_data_lake(self):
        """Backup critical data lake contents."""
        critical_prefixes = [
            'raw/critical/',
            'processed/master-data/',
            'analytics/reports/'
        ]
        
        for prefix in critical_prefixes:
            try:
                # Use AWS CLI for efficient large file transfers
                subprocess.run([
                    'aws', 's3', 'sync',
                    f's3://data-lake/{prefix}',
                    f's3://{self.backup_bucket}/data-lake/{prefix}',
                    '--storage-class', 'GLACIER'
                ], check=True)
                
                print(f"Backed up {prefix} to Glacier")
                
            except subprocess.CalledProcessError as e:
                print(f"Failed to backup {prefix}: {e}")
    
    def cleanup_old_backups(self, retention_days=30):
        """Clean up backups older than retention period."""
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Clean up RDS snapshots
        snapshots = self.rds.describe_db_snapshots(SnapshotType='manual')
        
        for snapshot in snapshots['DBSnapshots']:
            if snapshot['SnapshotCreateTime'].replace(tzinfo=None) < cutoff_date:
                try:
                    self.rds.delete_db_snapshot(
                        DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier']
                    )
                    print(f"Deleted old snapshot: {snapshot['DBSnapshotIdentifier']}")
                except Exception as e:
                    print(f"Failed to delete snapshot: {e}")
    
    def schedule_backups(self):
        """Schedule regular backups."""
        # Daily database backups at 2 AM
        schedule.every().day.at("02:00").do(self.backup_databases)
        
        # Weekly data lake backups on Sunday at 1 AM
        schedule.every().sunday.at("01:00").do(self.backup_data_lake)
        
        # Monthly cleanup on first day of month
        schedule.every().month.do(self.cleanup_old_backups)
        
        print("Backup schedule configured")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Usage
if __name__ == "__main__":
    backup_manager = DataBackupManager()
    backup_manager.schedule_backups()
```

This comprehensive disaster recovery strategy ensures business continuity for containerized data platforms through automated monitoring, failover procedures, and data protection mechanisms.