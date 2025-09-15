# CI/CD Interview Questions for Data Engineering - Comprehensive Guide

## 📋 Table of Contents

### Question Categories
1. [Basic Level Questions (Q1-Q30)](#basic-level-questions)
2. [Intermediate Level Questions (Q31-Q70)](#intermediate-level-questions)
3. [Advanced Level Questions (Q71-Q110)](#advanced-level-questions)
4. [Architecture & Performance (Q111-Q140)](#architecture--performance)
5. [Streaming & Real-time Processing (Q141-Q160)](#streaming--real-time-processing)
6. [Production & Operations (Q161-Q190)](#production--operations)
7. [Scenario-Based Questions (Q191-Q220)](#scenario-based-questions)

---

## Basic Level Questions

### Q1: What is CI/CD and why is it important for data engineering?
**Answer:**
**Continuous Integration (CI):**
- Automated code integration and testing
- Early detection of integration issues
- Consistent build processes
- Code quality enforcement

**Continuous Deployment (CD):**
- Automated deployment to environments
- Faster time to production
- Reduced manual errors
- Standardized release processes

**Data Engineering Benefits:**
```python
# Example: Automated data pipeline testing
def test_data_transformation():
    input_data = create_test_dataset()
    result = transform_user_data(input_data)
    
    # Automated validation
    assert result.schema == expected_schema
    assert result.count() > 0
    assert result.filter(col("age") < 0).count() == 0
```

### Q2: Explain the difference between Continuous Integration and Continuous Deployment.
**Answer:**

**Continuous Integration (CI):**
- Focuses on code integration and testing
- Triggered by code commits
- Validates code quality and functionality
- Produces deployable artifacts

**Continuous Deployment (CD):**
- Focuses on automated deployment
- Uses artifacts from CI process
- Manages environment-specific configurations
- Handles rollback and monitoring

**Pipeline Flow:**
```yaml
# CI Stage
ci_pipeline:
  - checkout_code
  - run_tests
  - build_artifacts
  - security_scan

# CD Stage  
cd_pipeline:
  - deploy_to_staging
  - run_integration_tests
  - deploy_to_production
  - monitor_deployment
```

### Q3: What are the key stages in a data engineering CI/CD pipeline?
**Answer:**

**Typical Data Pipeline Stages:**
```yaml
stages:
  1. Source Control:
     - Code checkout
     - Dependency resolution
  
  2. Quality Checks:
     - Linting (flake8, black)
     - Security scanning
     - Unit tests
  
  3. Data Testing:
     - Schema validation
     - Data quality checks
     - Transformation tests
  
  4. Build:
     - Docker image creation
     - Artifact packaging
  
  5. Deploy:
     - Staging deployment
     - Integration tests
     - Production deployment
  
  6. Monitor:
     - Health checks
     - Performance monitoring
```

### Q4: How do you implement automated testing for data pipelines?
**Answer:**

**Unit Testing:**
```python
import pytest
import pandas as pd
from src.transformations import clean_user_data

def test_data_cleaning():
    # Arrange
    input_data = pd.DataFrame({
        'user_id': [1, 2, None, 4],
        'email': ['user1@test.com', 'INVALID', 'user3@test.com', ''],
        'age': [25, -5, 30, 150]
    })
    
    # Act
    result = clean_user_data(input_data)
    
    # Assert
    assert len(result) == 2  # Only valid records
    assert result['age'].min() >= 0
    assert result['age'].max() <= 120
    assert all('@' in email for email in result['email'])
```

**Integration Testing:**
```python
def test_pipeline_integration():
    # Setup test environment
    test_db = create_test_database()
    
    # Run pipeline
    pipeline = DataPipeline(test_db)
    result = pipeline.process_batch(test_data)
    
    # Verify results
    assert result.success
    assert result.records_processed == len(test_data)
    assert result.error_count == 0
```

### Q5: What is Infrastructure as Code (IaC) and how does it relate to CI/CD?
**Answer:**

**Infrastructure as Code (IaC):**
- Managing infrastructure through code
- Version-controlled infrastructure definitions
- Reproducible environments
- Automated provisioning and updates

**Terraform Example:**
```hcl
# Infrastructure definition
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-${var.environment}"
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    enabled = true
    
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
  }
}

resource "aws_glue_job" "etl_job" {
  name     = "user-data-etl-${var.environment}"
  role_arn = aws_iam_role.glue_role.arn
  
  command {
    script_location = "s3://${aws_s3_bucket.scripts.bucket}/etl_script.py"
  }
}
```

**CI/CD Integration:**
```yaml
# Deploy infrastructure changes
- name: Deploy Infrastructure
  run: |
    terraform init
    terraform plan -var="environment=staging"
    terraform apply -auto-approve
```

### Q6: How do you handle secrets and sensitive data in CI/CD pipelines?
**Answer:**

**Secret Management Strategies:**

**1. Environment Variables:**
```yaml
# GitHub Actions
env:
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
  API_KEY: ${{ secrets.API_KEY }}
```

**2. External Secret Stores:**
```python
# AWS Secrets Manager integration
import boto3

def get_database_credentials():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='prod/database/credentials')
    return json.loads(response['SecretString'])

# Usage in pipeline
credentials = get_database_credentials()
db_connection = create_connection(
    host=credentials['host'],
    password=credentials['password']
)
```

**3. Kubernetes Secrets:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: database-secret
type: Opaque
data:
  username: <base64-encoded-username>
  password: <base64-encoded-password>
```

### Q7: What are the benefits of containerization in CI/CD?
**Answer:**

**Containerization Benefits:**
- **Environment Consistency**: Same runtime across all environments
- **Dependency Isolation**: No conflicts between applications
- **Scalability**: Easy horizontal scaling
- **Portability**: Run anywhere containers are supported

**Docker Example:**
```dockerfile
# Multi-stage build for data pipeline
FROM python:3.9-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
COPY src/ /app/src/
WORKDIR /app

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python src/health_check.py || exit 1

CMD ["python", "src/main.py"]
```

**CI/CD Integration:**
```yaml
- name: Build and Push Docker Image
  run: |
    docker build -t data-pipeline:${{ github.sha }} .
    docker tag data-pipeline:${{ github.sha }} registry.com/data-pipeline:latest
    docker push registry.com/data-pipeline:${{ github.sha }}
    docker push registry.com/data-pipeline:latest
```

### Q8: How do you implement rollback strategies in CI/CD?
**Answer:**

**Rollback Strategies:**

**1. Blue-Green Deployment:**
```python
class BlueGreenDeployment:
    def __init__(self):
        self.current_env = self.get_current_environment()
        self.target_env = 'green' if self.current_env == 'blue' else 'blue'
    
    def deploy(self):
        # Deploy to target environment
        self.deploy_to_environment(self.target_env)
        
        # Run health checks
        if self.health_check(self.target_env):
            self.switch_traffic(self.target_env)
        else:
            self.cleanup_failed_deployment(self.target_env)
            raise DeploymentError("Health checks failed")
    
    def rollback(self):
        self.switch_traffic(self.current_env)
        self.cleanup_environment(self.target_env)
```

**2. Database Migration Rollback:**
```python
# Alembic migration with rollback
def upgrade():
    op.add_column('users', sa.Column('new_field', sa.String(50)))

def downgrade():
    op.drop_column('users', 'new_field')

# Automated rollback in pipeline
def rollback_deployment():
    # Rollback database
    alembic.downgrade('-1')
    
    # Rollback application
    kubectl.rollout_undo('deployment/data-pipeline')
```

### Q9: What is GitOps and how does it differ from traditional CI/CD?
**Answer:**

**GitOps Principles:**
- Git as single source of truth
- Declarative infrastructure and applications
- Automated deployment through Git operations
- Continuous monitoring and drift detection

**Traditional CI/CD vs GitOps:**

| Aspect | Traditional CI/CD | GitOps |
|--------|------------------|---------|
| **Deployment Trigger** | Push-based (CI system pushes) | Pull-based (agents pull from Git) |
| **Configuration** | Imperative scripts | Declarative manifests |
| **State Management** | External systems | Git repository |
| **Rollback** | Manual or scripted | Git revert |

**GitOps Example:**
```yaml
# Application manifest in Git
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-pipeline
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-pipeline
  template:
    spec:
      containers:
      - name: pipeline
        image: data-pipeline:v1.2.3
        env:
        - name: ENVIRONMENT
          value: "production"
```

**ArgoCD Configuration:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: data-pipeline
spec:
  source:
    repoURL: https://github.com/company/data-pipeline-config
    path: manifests/production
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: data-pipeline
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Q10: How do you monitor CI/CD pipelines and deployments?
**Answer:**

**Pipeline Monitoring:**
```python
import time
from prometheus_client import Counter, Histogram, Gauge

# Metrics collection
pipeline_runs_total = Counter('pipeline_runs_total', 'Total pipeline runs', ['status', 'branch'])
pipeline_duration = Histogram('pipeline_duration_seconds', 'Pipeline execution time')
deployment_status = Gauge('deployment_status', 'Current deployment status', ['environment'])

class PipelineMonitor:
    def __init__(self):
        self.start_time = None
    
    def start_pipeline(self, branch):
        self.start_time = time.time()
        self.branch = branch
        print(f"Pipeline started for branch: {branch}")
    
    def end_pipeline(self, status):
        duration = time.time() - self.start_time
        pipeline_duration.observe(duration)
        pipeline_runs_total.labels(status=status, branch=self.branch).inc()
        
        # Send to monitoring system
        self.send_metrics({
            'pipeline_duration': duration,
            'status': status,
            'branch': self.branch
        })
```

**Deployment Health Checks:**
```python
class HealthChecker:
    def __init__(self, endpoints):
        self.endpoints = endpoints
    
    def check_deployment_health(self):
        results = {}
        
        for name, endpoint in self.endpoints.items():
            try:
                response = requests.get(f"{endpoint}/health", timeout=10)
                results[name] = {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'response_time': response.elapsed.total_seconds()
                }
            except Exception as e:
                results[name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        return results
```

### Q11: What are quality gates and how do you implement them?
**Answer:**

**Quality Gates Definition:**
- Automated checkpoints in CI/CD pipeline
- Prevent low-quality code from progressing
- Enforce coding standards and best practices
- Maintain system reliability and security

**Implementation Example:**
```yaml
# Quality gate configuration
quality_gates:
  code_coverage:
    threshold: 80%
    tool: pytest-cov
  
  security_scan:
    tool: bandit
    severity: medium
  
  performance_test:
    response_time: 2s
    error_rate: 1%
  
  data_quality:
    completeness: 95%
    accuracy: 98%
```

**Pipeline Integration:**
```python
class QualityGate:
    def __init__(self, thresholds):
        self.thresholds = thresholds
    
    def check_code_coverage(self, coverage_report):
        coverage_percentage = coverage_report.get_percentage()
        if coverage_percentage < self.thresholds['code_coverage']:
            raise QualityGateError(f"Code coverage {coverage_percentage}% below threshold")
    
    def check_security_scan(self, scan_results):
        high_severity_issues = scan_results.filter_by_severity('high')
        if len(high_severity_issues) > 0:
            raise QualityGateError(f"Found {len(high_severity_issues)} high severity security issues")
```

### Q12: How do you handle database migrations in CI/CD pipelines?
**Answer:**

**Database Migration Strategy:**
```python
# Alembic migration example
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Forward migration
    op.create_table(
        'user_metrics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('metric_name', sa.String(100), nullable=False),
        sa.Column('metric_value', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now())
    )
    
    # Create indexes
    op.create_index('idx_user_metrics_user_id', 'user_metrics', ['user_id'])
    op.create_index('idx_user_metrics_created_at', 'user_metrics', ['created_at'])

def downgrade():
    # Rollback migration
    op.drop_table('user_metrics')
```

**CI/CD Integration:**
```yaml
# Database migration in pipeline
- name: Run Database Migrations
  run: |
    # Install migration tool
    pip install alembic psycopg2-binary
    
    # Run migrations
    alembic upgrade head
    
    # Verify migration success
    python scripts/verify_schema.py
    
    # Run data validation
    python scripts/validate_data_integrity.py
```

**Zero-Downtime Migration:**
```python
class ZeroDowntimeMigration:
    def migrate_with_rollback(self):
        try:
            # Create new table structure
            self.create_new_table()
            
            # Migrate data in batches
            self.migrate_data_batches()
            
            # Switch application to new table
            self.switch_table_reference()
            
            # Cleanup old table
            self.cleanup_old_table()
            
        except Exception as e:
            # Automatic rollback
            self.rollback_migration()
            raise MigrationError(f"Migration failed: {e}")
```

### Q13: What are the different deployment strategies and when to use them?
**Answer:**

**Deployment Strategies:**

**1. Blue-Green Deployment:**
```python
# Complete environment switch
def blue_green_deploy():
    # Deploy to inactive environment
    deploy_to_environment('green')
    
    # Run comprehensive tests
    if run_smoke_tests('green') and run_integration_tests('green'):
        # Switch traffic instantly
        switch_load_balancer('green')
        
        # Keep blue for rollback
        schedule_cleanup('blue', delay='1h')
    else:
        cleanup_environment('green')
        raise DeploymentError("Tests failed")
```

**Use Cases:**
- Critical production systems
- When instant rollback is required
- Database-heavy applications

**2. Canary Deployment:**
```python
# Gradual traffic shift
def canary_deploy():
    # Deploy to subset of instances
    deploy_canary(percentage=5)
    
    # Monitor metrics
    if monitor_metrics(duration='10m'):
        increase_canary(percentage=25)
        
        if monitor_metrics(duration='10m'):
            complete_deployment(percentage=100)
    else:
        rollback_canary()
```

**Use Cases:**
- High-traffic applications
- Risk mitigation for new features
- A/B testing scenarios

**3. Rolling Deployment:**
```python
# Instance-by-instance update
def rolling_deploy():
    instances = get_all_instances()
    
    for instance in instances:
        # Remove from load balancer
        remove_from_lb(instance)
        
        # Update instance
        update_instance(instance)
        
        # Health check
        if health_check(instance):
            add_to_lb(instance)
        else:
            rollback_instance(instance)
            raise DeploymentError(f"Instance {instance} failed health check")
```

### Q14: How do you implement security scanning in CI/CD pipelines?
**Answer:**

**Security Scanning Types:**

**1. Dependency Vulnerability Scanning:**
```yaml
# GitHub Actions security scan
- name: Security Scan
  run: |
    # Python dependency scanning
    pip install safety
    safety check --json --output safety-report.json
    
    # Node.js dependency scanning
    npm audit --audit-level moderate
    
    # Container scanning
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
      aquasec/trivy image data-pipeline:latest
```

**2. Secret Detection:**
```python
# Automated secret detection
import re

class SecretScanner:
    def __init__(self):
        self.patterns = {
            'aws_access_key': r'AKIA[0-9A-Z]{16}',
            'api_key': r'api[_-]?key[\s]*[:=][\s]*["\']?([a-zA-Z0-9_\-]{20,})',
            'password': r'password[\s]*[:=][\s]*["\']?([^\s"\';]{8,})'
        }
    
    def scan_file(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            
        findings = []
        for secret_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                findings.append({
                    'type': secret_type,
                    'line': content[:match.start()].count('\n') + 1,
                    'file': file_path
                })
        
        return findings
```

**3. Static Code Analysis:**
```yaml
# Security-focused linting
- name: Static Security Analysis
  run: |
    # Python security linting
    bandit -r src/ -f json -o bandit-report.json
    
    # General security patterns
    semgrep --config=auto src/
    
    # Infrastructure security
    checkov -f terraform/ --framework terraform
```

### Q15: What is the role of artifact management in CI/CD?
**Answer:**

**Artifact Management:**
- **Storage**: Centralized repository for build artifacts
- **Versioning**: Track artifact versions and dependencies
- **Distribution**: Efficient artifact distribution to environments
- **Security**: Signed and scanned artifacts

**Docker Registry Example:**
```yaml
# Multi-registry strategy
registries:
  development:
    url: "dev-registry.company.com"
    retention: "7 days"
  
  staging:
    url: "staging-registry.company.com"
    retention: "30 days"
  
  production:
    url: "prod-registry.company.com"
    retention: "1 year"
    signing: required
```

**Artifact Pipeline:**
```python
class ArtifactManager:
    def __init__(self, registry_config):
        self.registry = registry_config
    
    def build_and_push(self, dockerfile_path, tag):
        # Build image
        image = docker.build(dockerfile_path, tag=tag)
        
        # Security scan
        scan_results = self.security_scan(image)
        if scan_results.has_critical_vulnerabilities():
            raise SecurityError("Critical vulnerabilities found")
        
        # Sign image
        signed_image = self.sign_image(image)
        
        # Push to registry
        self.push_to_registry(signed_image)
        
        # Update metadata
        self.update_artifact_metadata(tag, scan_results)
    
    def promote_artifact(self, source_env, target_env, tag):
        # Pull from source registry
        artifact = self.pull_artifact(source_env, tag)
        
        # Verify signature
        if not self.verify_signature(artifact):
            raise SecurityError("Artifact signature verification failed")
        
        # Push to target registry
        self.push_artifact(target_env, artifact)
```

### Q16: How do you handle environment-specific configurations?
**Answer:**

**Configuration Management Strategies:**

**1. Environment Variables:**
```python
# Configuration class
import os
from dataclasses import dataclass

@dataclass
class Config:
    database_url: str = os.getenv('DATABASE_URL')
    kafka_brokers: str = os.getenv('KAFKA_BROKERS')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    batch_size: int = int(os.getenv('BATCH_SIZE', '1000'))
    
    def __post_init__(self):
        if not self.database_url:
            raise ValueError("DATABASE_URL is required")
```

**2. Configuration Files:**
```yaml
# config/development.yml
database:
  host: "dev-db.company.com"
  port: 5432
  name: "dev_database"
  pool_size: 5

kafka:
  brokers: ["dev-kafka-1:9092", "dev-kafka-2:9092"]
  consumer_group: "dev-data-pipeline"

logging:
  level: "DEBUG"
  format: "detailed"

# config/production.yml
database:
  host: "prod-db-cluster.company.com"
  port: 5432
  name: "production_database"
  pool_size: 20
  ssl_mode: "require"

kafka:
  brokers: ["prod-kafka-1:9092", "prod-kafka-2:9092", "prod-kafka-3:9092"]
  consumer_group: "prod-data-pipeline"
  security_protocol: "SASL_SSL"

logging:
  level: "WARNING"
  format: "json"
```

**3. Kubernetes ConfigMaps:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: data-pipeline-config
  namespace: production
data:
  database_host: "prod-db-cluster.company.com"
  kafka_brokers: "prod-kafka-1:9092,prod-kafka-2:9092"
  batch_size: "5000"
  log_level: "WARNING"
```

**Configuration Injection:**
```python
class ConfigManager:
    def __init__(self, environment):
        self.environment = environment
        self.config = self.load_config()
    
    def load_config(self):
        # Load base configuration
        base_config = self.load_yaml('config/base.yml')
        
        # Load environment-specific overrides
        env_config = self.load_yaml(f'config/{self.environment}.yml')
        
        # Merge configurations
        return self.merge_configs(base_config, env_config)
    
    def get_database_config(self):
        return DatabaseConfig(**self.config['database'])
```

### Q17: What are the best practices for CI/CD pipeline design?
**Answer:**

**Pipeline Design Principles:**

**1. Fail Fast:**
```yaml
# Optimized stage order
stages:
  - lint_and_format      # Fast feedback (30s)
  - security_scan        # Early security check (2m)
  - unit_tests          # Quick validation (3m)
  - build_artifacts     # Create deployables (5m)
  - integration_tests   # Slower but thorough (10m)
  - deploy_staging      # Environment deployment (5m)
  - e2e_tests          # Full system validation (15m)
  - deploy_production   # Final deployment (5m)
```

**2. Parallel Execution:**
```yaml
# Parallel test execution
test_stage:
  parallel:
    unit_tests:
      script: pytest tests/unit/
    
    integration_tests:
      script: pytest tests/integration/
    
    security_scan:
      script: bandit -r src/
    
    performance_tests:
      script: locust -f tests/performance/
```

**3. Idempotent Operations:**
```python
class IdempotentDeployment:
    def deploy(self, config):
        # Check current state
        current_state = self.get_current_state()
        desired_state = self.calculate_desired_state(config)
        
        # Only apply changes if needed
        if current_state != desired_state:
            changes = self.calculate_changes(current_state, desired_state)
            self.apply_changes(changes)
        else:
            print("No changes needed, deployment is up to date")
```

**4. Comprehensive Logging:**
```python
import logging
from datetime import datetime

class PipelineLogger:
    def __init__(self, pipeline_id):
        self.pipeline_id = pipeline_id
        self.logger = logging.getLogger(f"pipeline.{pipeline_id}")
    
    def log_stage_start(self, stage_name):
        self.logger.info(f"Stage '{stage_name}' started", extra={
            'pipeline_id': self.pipeline_id,
            'stage': stage_name,
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'stage_start'
        })
    
    def log_stage_end(self, stage_name, duration, status):
        self.logger.info(f"Stage '{stage_name}' completed", extra={
            'pipeline_id': self.pipeline_id,
            'stage': stage_name,
            'duration': duration,
            'status': status,
            'event_type': 'stage_end'
        })
```

### Q18: How do you implement automated rollback mechanisms?
**Answer:**

**Automated Rollback Strategies:**

**1. Health Check-Based Rollback:**
```python
class AutoRollback:
    def __init__(self, health_check_config):
        self.config = health_check_config
        self.rollback_threshold = 3  # Failed checks before rollback
    
    def deploy_with_auto_rollback(self, deployment_config):
        # Store previous version for rollback
        previous_version = self.get_current_version()
        
        try:
            # Deploy new version
            self.deploy(deployment_config)
            
            # Monitor health for specified duration
            if not self.monitor_health(duration=300):  # 5 minutes
                raise HealthCheckError("Health checks failed")
                
        except Exception as e:
            self.logger.error(f"Deployment failed: {e}")
            self.rollback_to_version(previous_version)
            raise
    
    def monitor_health(self, duration):
        start_time = time.time()
        failed_checks = 0
        
        while time.time() - start_time < duration:
            if not self.run_health_check():
                failed_checks += 1
                if failed_checks >= self.rollback_threshold:
                    return False
            else:
                failed_checks = 0  # Reset counter on success
            
            time.sleep(30)  # Check every 30 seconds
        
        return True
```

**2. Metric-Based Rollback:**
```python
class MetricBasedRollback:
    def __init__(self, metrics_config):
        self.thresholds = metrics_config['thresholds']
        self.monitoring_duration = metrics_config['duration']
    
    def monitor_deployment_metrics(self):
        metrics = self.collect_metrics()
        
        # Check error rate
        if metrics['error_rate'] > self.thresholds['max_error_rate']:
            self.trigger_rollback("High error rate detected")
        
        # Check response time
        if metrics['avg_response_time'] > self.thresholds['max_response_time']:
            self.trigger_rollback("High response time detected")
        
        # Check throughput
        if metrics['throughput'] < self.thresholds['min_throughput']:
            self.trigger_rollback("Low throughput detected")
    
    def trigger_rollback(self, reason):
        self.logger.warning(f"Triggering rollback: {reason}")
        self.send_alert(f"Auto-rollback triggered: {reason}")
        self.execute_rollback()
```

### Q19: What is the difference between CI/CD and DevOps?
**Answer:**

**CI/CD vs DevOps:**

| Aspect | CI/CD | DevOps |
|--------|-------|--------|
| **Scope** | Specific practices and tools | Cultural and organizational approach |
| **Focus** | Automation of build/deploy | Collaboration and communication |
| **Implementation** | Technical pipelines | People, processes, and tools |
| **Goal** | Faster, reliable deployments | Improved software delivery lifecycle |

**CI/CD as Part of DevOps:**
```python
# DevOps encompasses CI/CD plus:
class DevOpsPractices:
    def __init__(self):
        # CI/CD components
        self.ci_cd_pipeline = CICDPipeline()
        
        # Additional DevOps practices
        self.monitoring = MonitoringSystem()
        self.incident_management = IncidentManagement()
        self.collaboration_tools = CollaborationTools()
        self.infrastructure_as_code = IaC()
    
    def implement_devops_culture(self):
        # Technical practices
        self.setup_automated_pipelines()
        self.implement_monitoring()
        self.setup_infrastructure_automation()
        
        # Cultural practices
        self.establish_shared_responsibility()
        self.implement_feedback_loops()
        self.promote_continuous_learning()
```

**DevOps Principles:**
- **Collaboration**: Breaking down silos between teams
- **Automation**: Reducing manual, error-prone processes
- **Measurement**: Data-driven decision making
- **Sharing**: Knowledge and responsibility sharing

### Q20: How do you handle data quality checks in CI/CD pipelines?
**Answer:**

**Data Quality Integration:**

**1. Great Expectations Integration:**
```python
# Data quality test suite
import great_expectations as ge
from great_expectations.checkpoint import SimpleCheckpoint

class DataQualityValidator:
    def __init__(self, data_context_path):
        self.context = ge.get_context(data_context_path)
    
    def validate_dataset(self, dataset_name, data_source):
        # Load data
        batch = self.context.get_batch({
            'datasource': data_source,
            'data_asset': dataset_name
        })
        
        # Run expectations
        results = batch.validate(expectation_suite_name=f"{dataset_name}_suite")
        
        if not results.success:
            failed_expectations = [
                exp for exp in results.results 
                if not exp.success
            ]
            raise DataQualityError(f"Data quality checks failed: {failed_expectations}")
        
        return results
```

**2. Custom Data Quality Checks:**
```python
class CustomDataQualityChecks:
    def __init__(self, df):
        self.df = df
        self.errors = []
    
    def check_completeness(self, required_columns):
        for column in required_columns:
            null_percentage = self.df[column].isnull().sum() / len(self.df)
            if null_percentage > 0.05:  # 5% threshold
                self.errors.append(f"Column {column} has {null_percentage:.2%} null values")
    
    def check_uniqueness(self, unique_columns):
        for column in unique_columns:
            duplicate_count = self.df[column].duplicated().sum()
            if duplicate_count > 0:
                self.errors.append(f"Column {column} has {duplicate_count} duplicate values")
    
    def check_data_freshness(self, timestamp_column, max_age_hours=24):
        latest_timestamp = self.df[timestamp_column].max()
        age_hours = (datetime.now() - latest_timestamp).total_seconds() / 3600
        
        if age_hours > max_age_hours:
            self.errors.append(f"Data is {age_hours:.1f} hours old, exceeds {max_age_hours}h threshold")
    
    def validate(self):
        if self.errors:
            raise DataQualityError("\n".join(self.errors))
        return True
```

**3. Pipeline Integration:**
```yaml
# Data quality stage in CI/CD
- name: Data Quality Validation
  run: |
    # Run data quality checks
    python scripts/validate_data_quality.py \
      --dataset user_events \
      --config config/data_quality.yml
    
    # Generate quality report
    python scripts/generate_quality_report.py \
      --output reports/data_quality_report.html
  
  # Fail pipeline if quality checks fail
  continue-on-error: false
```

---

*[Questions 21-30 will be added in the next batch]*