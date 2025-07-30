# CI/CD Key Concepts

## 1. Continuous Integration/Continuous Deployment
**What it is**: Software development practices that enable frequent, reliable, and automated code integration, testing, and deployment.

**Core Components**:
- **Continuous Integration**: Automated code integration and testing
- **Continuous Delivery**: Automated deployment to staging environments
- **Continuous Deployment**: Automated deployment to production
- **Pipeline**: Automated workflow from code to production

## 2. CI/CD Pipeline Stages
**Typical Pipeline Flow**:
```yaml
# Basic CI/CD Pipeline
Source → Build → Test → Deploy → Monitor

# Detailed Pipeline
1. Source Control (Git)
2. Build (Compile, Package)
3. Unit Tests
4. Integration Tests
5. Security Scanning
6. Deploy to Staging
7. End-to-End Tests
8. Deploy to Production
9. Monitoring & Alerts
```

**GitHub Actions Pipeline**:
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '16'
  PYTHON_VERSION: '3.9'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
    
    - name: Lint code
      run: flake8 src/ tests/
    
    - name: Run unit tests
      run: |
        pytest tests/ --cov=src/ --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .
        docker tag myapp:${{ github.sha }} myapp:latest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push myapp:${{ github.sha }}
        docker push myapp:latest

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps:
    - name: Deploy to staging
      run: |
        kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n staging
        kubectl rollout status deployment/myapp -n staging

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
    - name: Deploy to production
      run: |
        kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n production
        kubectl rollout status deployment/myapp -n production
```

## 3. Build Automation
**Docker Multi-Stage Build**:
```dockerfile
# Multi-stage Dockerfile
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim as runtime

# Copy dependencies from builder stage
COPY --from=builder /root/.local /root/.local

WORKDIR /app
COPY src/ ./src/
COPY config/ ./config/

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["python", "-m", "src.main"]
```

**Build Scripts**:
```bash
#!/bin/bash
# build.sh

set -e  # Exit on any error

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run linting
echo "Running code quality checks..."
flake8 src/ tests/
black --check src/ tests/
isort --check-only src/ tests/

# Run tests
echo "Running tests..."
pytest tests/ --cov=src/ --cov-report=html --cov-fail-under=80

# Build application
echo "Building application..."
python setup.py sdist bdist_wheel

# Build Docker image
echo "Building Docker image..."
docker build -t myapp:$(git rev-parse --short HEAD) .

echo "Build completed successfully!"
```

## 4. Testing Strategies
**Test Pyramid**:
```yaml
# Test Types (from bottom to top)
Unit Tests: 70%
  - Fast execution
  - Test individual functions/methods
  - Mock external dependencies

Integration Tests: 20%
  - Test component interactions
  - Database connections
  - API integrations

End-to-End Tests: 10%
  - Full user workflows
  - UI testing
  - Slowest but most comprehensive
```

**Automated Testing**:
```python
# pytest configuration
# conftest.py
import pytest
import docker
import time

@pytest.fixture(scope="session")
def database():
    """Start test database container"""
    client = docker.from_env()
    
    # Start PostgreSQL container
    container = client.containers.run(
        "postgres:13",
        environment={
            "POSTGRES_DB": "testdb",
            "POSTGRES_USER": "testuser", 
            "POSTGRES_PASSWORD": "testpass"
        },
        ports={'5432/tcp': 5433},
        detach=True
    )
    
    # Wait for database to be ready
    time.sleep(10)
    
    yield "postgresql://testuser:testpass@localhost:5433/testdb"
    
    # Cleanup
    container.stop()
    container.remove()

# test_integration.py
def test_database_connection(database):
    import psycopg2
    
    conn = psycopg2.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    
    assert result[0] == 1
    conn.close()
```

## 5. Deployment Strategies
**Blue-Green Deployment**:
```yaml
# Blue-Green deployment with Kubernetes
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: blue  # Switch between blue/green
  ports:
  - port: 80
    targetPort: 8000

---
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0
        ports:
        - containerPort: 8000

---
# Green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myapp:v2.0
        ports:
        - containerPort: 8000
```

**Canary Deployment**:
```python
# Canary deployment script
import requests
import time
import random

class CanaryDeployment:
    def __init__(self, old_version_url, new_version_url):
        self.old_version_url = old_version_url
        self.new_version_url = new_version_url
        self.traffic_percentage = 0
        self.error_threshold = 0.05
        
    def deploy_canary(self, target_percentage=100, step_size=10, step_duration=300):
        """Gradually increase traffic to new version"""
        
        while self.traffic_percentage < target_percentage:
            # Increase traffic
            self.traffic_percentage = min(
                self.traffic_percentage + step_size, 
                target_percentage
            )
            
            print(f"Routing {self.traffic_percentage}% traffic to new version")
            
            # Monitor for specified duration
            if not self._monitor_health(step_duration):
                print("Health check failed, rolling back...")
                self._rollback()
                return False
            
            time.sleep(step_duration)
        
        print("Canary deployment completed successfully")
        return True
    
    def _monitor_health(self, duration):
        """Monitor application health during canary"""
        start_time = time.time()
        error_count = 0
        total_requests = 0
        
        while time.time() - start_time < duration:
            # Route traffic based on percentage
            if random.randint(1, 100) <= self.traffic_percentage:
                url = self.new_version_url
            else:
                url = self.old_version_url
            
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code != 200:
                    error_count += 1
            except:
                error_count += 1
            
            total_requests += 1
            time.sleep(1)
        
        error_rate = error_count / total_requests if total_requests > 0 else 0
        return error_rate < self.error_threshold
    
    def _rollback(self):
        """Rollback to previous version"""
        self.traffic_percentage = 0
        print("Rolled back to previous version")
```

## 6. Infrastructure as Code
**Terraform for CI/CD Infrastructure**:
```hcl
# main.tf
provider "aws" {
  region = "us-west-2"
}

# S3 bucket for build artifacts
resource "aws_s3_bucket" "build_artifacts" {
  bucket = "cicd-build-artifacts-${random_id.bucket_suffix.hex}"
}

# CodeBuild project
resource "aws_codebuild_project" "app_build" {
  name          = "app-build"
  service_role  = aws_iam_role.codebuild_role.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_MEDIUM"
    image        = "aws/codebuild/standard:5.0"
    type         = "LINUX_CONTAINER"
    
    environment_variable {
      name  = "AWS_DEFAULT_REGION"
      value = "us-west-2"
    }
  }

  source {
    type = "CODEPIPELINE"
    buildspec = "buildspec.yml"
  }
}

# CodePipeline
resource "aws_codepipeline" "app_pipeline" {
  name     = "app-pipeline"
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = aws_s3_bucket.build_artifacts.bucket
    type     = "S3"
  }

  stage {
    name = "Source"
    
    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["source_output"]
      
      configuration = {
        Owner  = "myorg"
        Repo   = "myapp"
        Branch = "main"
      }
    }
  }

  stage {
    name = "Build"
    
    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      version          = "1"
      
      configuration = {
        ProjectName = aws_codebuild_project.app_build.name
      }
    }
  }

  stage {
    name = "Deploy"
    
    action {
      name            = "Deploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "ECS"
      input_artifacts = ["build_output"]
      version         = "1"
      
      configuration = {
        ClusterName = "production"
        ServiceName = "myapp"
      }
    }
  }
}
```

## 7. Security in CI/CD
**Security Scanning**:
```yaml
# Security scanning in pipeline
security-scan:
  runs-on: ubuntu-latest
  steps:
  - name: Checkout code
    uses: actions/checkout@v3
  
  - name: Run SAST scan
    uses: github/super-linter@v4
    env:
      DEFAULT_BRANCH: main
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  
  - name: Run dependency check
    run: |
      pip install safety
      safety check -r requirements.txt
  
  - name: Container security scan
    run: |
      docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        -v $(pwd):/tmp aquasec/trivy:latest \
        image myapp:latest
  
  - name: Infrastructure security scan
    run: |
      docker run --rm -v $(pwd):/tf bridgecrew/checkov \
        -d /tf --framework terraform
```

**Secrets Management**:
```python
# Secrets management in CI/CD
import os
import boto3
from botocore.exceptions import ClientError

class SecretsManager:
    def __init__(self):
        self.secrets_client = boto3.client('secretsmanager')
        self.ssm_client = boto3.client('ssm')
    
    def get_secret(self, secret_name):
        """Get secret from AWS Secrets Manager"""
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name)
            return response['SecretString']
        except ClientError as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None
    
    def get_parameter(self, parameter_name, decrypt=True):
        """Get parameter from AWS Systems Manager"""
        try:
            response = self.ssm_client.get_parameter(
                Name=parameter_name,
                WithDecryption=decrypt
            )
            return response['Parameter']['Value']
        except ClientError as e:
            print(f"Error retrieving parameter {parameter_name}: {e}")
            return None
    
    def inject_secrets_to_env(self, secret_mappings):
        """Inject secrets into environment variables"""
        for env_var, secret_name in secret_mappings.items():
            secret_value = self.get_secret(secret_name)
            if secret_value:
                os.environ[env_var] = secret_value

# Usage in deployment script
secrets_manager = SecretsManager()
secrets_manager.inject_secrets_to_env({
    'DATABASE_PASSWORD': 'prod/database/password',
    'API_KEY': 'prod/external-api/key'
})
```

## 8. Monitoring and Observability
**Pipeline Monitoring**:
```python
import time
import requests
from datetime import datetime

class PipelineMonitor:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url
        self.metrics = {}
    
    def track_stage(self, stage_name):
        """Context manager to track pipeline stage"""
        return StageTracker(stage_name, self)
    
    def record_metric(self, stage_name, duration, status):
        """Record stage metrics"""
        if stage_name not in self.metrics:
            self.metrics[stage_name] = []
        
        self.metrics[stage_name].append({
            'duration': duration,
            'status': status,
            'timestamp': datetime.now()
        })
    
    def send_notification(self, message, level='info'):
        """Send notification to webhook"""
        if self.webhook_url:
            payload = {
                'text': f"[{level.upper()}] {message}",
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                requests.post(self.webhook_url, json=payload, timeout=10)
            except Exception as e:
                print(f"Failed to send notification: {e}")

class StageTracker:
    def __init__(self, stage_name, monitor):
        self.stage_name = stage_name
        self.monitor = monitor
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        print(f"Starting stage: {self.stage_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        status = 'failed' if exc_type else 'success'
        
        self.monitor.record_metric(self.stage_name, duration, status)
        
        if status == 'failed':
            self.monitor.send_notification(
                f"Stage {self.stage_name} failed after {duration:.2f}s",
                level='error'
            )
        else:
            print(f"Completed stage: {self.stage_name} ({duration:.2f}s)")

# Usage in pipeline
monitor = PipelineMonitor(webhook_url="https://hooks.slack.com/...")

with monitor.track_stage("build"):
    # Build logic here
    pass

with monitor.track_stage("test"):
    # Test logic here
    pass
```

## 9. Performance Optimization
**Pipeline Optimization**:
```yaml
# Parallel job execution
jobs:
  test-unit:
    runs-on: ubuntu-latest
    steps:
    - name: Run unit tests
      run: pytest tests/unit/

  test-integration:
    runs-on: ubuntu-latest
    steps:
    - name: Run integration tests
      run: pytest tests/integration/

  lint:
    runs-on: ubuntu-latest
    steps:
    - name: Run linting
      run: flake8 src/

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - name: Security scan
      run: bandit -r src/

  deploy:
    needs: [test-unit, test-integration, lint, security-scan]
    runs-on: ubuntu-latest
    steps:
    - name: Deploy application
      run: ./deploy.sh
```

**Caching Strategies**:
```yaml
# Dependency caching
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

# Docker layer caching
- name: Build Docker image
  uses: docker/build-push-action@v3
  with:
    context: .
    push: true
    tags: myapp:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## 10. Best Practices
**Pipeline Design**:
```yaml
# Best practices checklist
✓ Fast feedback loops (< 10 minutes for basic pipeline)
✓ Fail fast (run quick tests first)
✓ Parallel execution where possible
✓ Immutable artifacts (same artifact through all stages)
✓ Environment parity (staging mirrors production)
✓ Automated rollback capabilities
✓ Comprehensive logging and monitoring
✓ Security scanning at multiple stages
✓ Infrastructure as code
✓ Secrets management
```

**Error Handling**:
```bash
#!/bin/bash
# Robust pipeline script

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Cleanup function
cleanup() {
    echo "Cleaning up..."
    docker-compose down || true
    rm -f temp_files/* || true
}

# Set trap for cleanup
trap cleanup EXIT

# Function with error handling
run_tests() {
    echo "Running tests..."
    
    if ! pytest tests/ --junitxml=test-results.xml; then
        echo "Tests failed!"
        return 1
    fi
    
    echo "Tests passed!"
    return 0
}

# Main pipeline logic
main() {
    echo "Starting CI/CD pipeline..."
    
    # Each stage with error handling
    run_tests || exit 1
    
    echo "Pipeline completed successfully!"
}

main "$@"
```