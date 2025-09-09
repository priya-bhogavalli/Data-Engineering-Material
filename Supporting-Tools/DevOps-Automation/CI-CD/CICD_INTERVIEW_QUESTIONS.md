# CI/CD Interview Questions for Data Engineering

## 🚀 CI/CD Fundamentals

### Q1: What is CI/CD and why is it important for data engineering?
**Answer:**
**Continuous Integration (CI):**
- Automated code integration and testing
- Early detection of integration issues
- Consistent build processes

**Continuous Deployment (CD):**
- Automated deployment to environments
- Faster time to production
- Reduced manual errors

**Data Engineering Benefits:**
- Automated data pipeline testing
- Schema validation and migration
- Data quality checks in pipelines
- Environment consistency (dev/staging/prod)

### Q2: Explain the CI/CD pipeline stages for data projects.
**Answer:**

**Typical Data Engineering CI/CD Pipeline:**
```yaml
# .github/workflows/data-pipeline.yml
name: Data Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      

### Q3: How do you implement automated testing for data pipelines?
**Answer:**

**Unit Testing:**
```python
# tests/test_data_transformations.py
import pytest
import pandas as pd
from src.transformations import clean_user_data, calculate_metrics

def test_clean_user_data():
    # Arrange
    input_data = pd.DataFrame({
        'user_id': [1, 2, None, 4],
        'email': ['user1@test.com', 'INVALID', 'user3@test.com', 'user4@test.com'],
        'age': [25, -5, 30, 150]
    })
    
    # Act
    result = clean_user_data(input_data)
    
    # Assert
    assert len(result) == 2  # Only valid records
    assert result['age'].min() >= 0
    assert result['age'].max() <= 120
    assert '@' in result['email'].iloc[0]

def test_calculate_metrics():
    # Test data aggregation logic
    orders = pd.DataFrame({
        'user_id': [1, 1, 2, 2],
        'amount': [100, 200, 50, 75],
        'date': ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-03']
    })
    
    metrics = calculate_metrics(orders)
    
    assert metrics.loc[1, 'total_amount'] == 300
    assert metrics.loc[2, 'total_amount'] == 125
```

**Integration Testing:**
```python
# tests/test_pipeline_integration.py
import pytest
from testcontainers import DockerCompose
from src.pipeline import DataPipeline

@pytest.fixture(scope="module")
def test_environment():
    with DockerCompose(".", compose_file_name="docker-compose.test.yml") as compose:
        # Wait for services to be ready
        postgres_port = compose.get_service_port("postgres", 5432)
        kafka_port = compose.get_service_port("kafka", 9092)
        
        yield {
            'postgres_url': f'postgresql://test:test@localhost:{postgres_port}/testdb',
            'kafka_url': f'localhost:{kafka_port}'
        }

def test_end_to_end_pipeline(test_environment):
    # Setup test data
    pipeline = DataPipeline(
        postgres_url=test_environment['postgres_url'],
        kafka_url=test_environment['kafka_url']
    )
    
    # Insert test data
    test_events = [
        {'user_id': 1, 'event': 'login', 'timestamp': '2023-01-01T10:00:00'},
        {'user_id': 2, 'event': 'purchase', 'amount': 100, 'timestamp': '2023-01-01T11:00:00'}
    ]
    
    # Run pipeline
    pipeline.process_events(test_events)
    
    # Verify results
    results = pipeline.get_processed_data()
    assert len(results) == 2
    assert results[0]['processed'] == True
```

**Data Quality Testing:**
```python
# tests/test_data_quality.py
import great_expectations as ge

def test_data_quality_expectations():
    # Load data
    df = ge.read_csv('data/processed/user_metrics.csv')
    
    # Define expectations
    df.expect_column_to_exist('user_id')
    df.expect_column_values_to_not_be_null('user_id')
    df.expect_column_values_to_be_unique('user_id')
    df.expect_column_values_to_be_between('age', min_value=0, max_value=120)
    df.expect_column_values_to_match_regex('email', r'^[^@]+@[^@]+\.[^@]+$')
    
    # Validate expectations
    validation_result = df.validate()
    assert validation_result.success, f"Data quality checks failed: {validation_result}"

def test_schema_validation():
    from pandera import DataFrameSchema, Column, Check
    
    schema = DataFrameSchema({
        'user_id': Column(int, Check.greater_than(0)),
        'email': Column(str, Check.str_matches(r'^[^@]+@[^@]+\.[^@]+$')),
        'signup_date': Column('datetime64[ns]'),
        'total_orders': Column(int, Check.greater_than_or_equal_to(0))
    })
    
    df = pd.read_csv('data/processed/users.csv')
    validated_df = schema.validate(df)  # Raises exception if invalid
    assert len(validated_df) > 0
```

## 🔧 CI/CD Tools & Platforms

### Q4: Compare different CI/CD platforms for data engineering.
**Answer:**

| Platform | Strengths | Data Engineering Use Cases |
|----------|-----------|---------------------------|
| **GitHub Actions** | Git integration, free tier | Code-driven pipelines, open source |
| **GitLab CI** | Built-in registry, security scanning | Enterprise, compliance requirements |
| **Jenkins** | Highly customizable, plugins | Complex workflows, on-premise |
| **Azure DevOps** | Microsoft ecosystem | .NET/SQL Server environments |
| **AWS CodePipeline** | AWS native, serverless | AWS-heavy architectures |

**Jenkins Pipeline Example:**
```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        KUBECONFIG = credentials('k8s-config')
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
                        sh 'python -m pytest tests/unit/'
                    }
                }
                stage('Lint') {
                    steps {
                        sh 'flake8 src/'
                        sh 'black --check src/'
                    }
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    def image = docker.build("${DOCKER_REGISTRY}/data-pipeline:${BUILD_NUMBER}")
                    image.push()
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                sh '''
                    helm upgrade --install data-pipeline-staging ./helm-chart \
                        --set image.tag=${BUILD_NUMBER} \
                        --set environment=staging
                '''
            }
        }
        
        stage('Integration Tests') {
            steps {
                sh 'python scripts/integration_tests.py --env staging'
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                sh '''
                    helm upgrade --install data-pipeline-prod ./helm-chart \
                        --set image.tag=${BUILD_NUMBER} \
                        --set environment=production
                '''
            }
        }
    }
    
    post {
        always {
            publishTestResults testResultsPattern: 'test-results.xml'
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'coverage',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
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

### Q5: How do you handle database migrations in CI/CD?
**Answer:**

**Database Migration Strategy:**
```python
# migrations/001_create_users_table.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_table('users')

# CI/CD Pipeline Integration
# .github/workflows/deploy.yml
- name: Run database migrations
  run: |
    # Install dependencies
    pip install alembic psycopg2-binary
    
    # Run migrations
    alembic upgrade head
    
    # Verify migration success
    python scripts/verify_schema.py
```

**Zero-Downtime Deployment:**
```python
# Blue-Green Deployment for Data Pipelines
class BlueGreenDeployment:
    def __init__(self):
        self.current_env = self.get_current_environment()
        self.target_env = 'green' if self.current_env == 'blue' else 'blue'
    
    def deploy(self):
        # 1. Deploy to target environment
        self.deploy_to_environment(self.target_env)
        
        # 2. Run smoke tests
        if not self.run_smoke_tests(self.target_env):
            raise Exception("Smoke tests failed")
        
        # 3. Switch traffic
        self.switch_traffic(self.target_env)
        
        # 4. Verify switch
        if not self.verify_traffic_switch():
            self.rollback()
            raise Exception("Traffic switch verification failed")
    
    def rollback(self):
        self.switch_traffic(self.current_env)
```

## 🛡️ Security & Compliance

### Q6: How do you implement security in CI/CD pipelines?
**Answer:**

**Secret Management:**
```yaml
# GitHub Actions with secrets
- name: Deploy to AWS
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
  run: |
    # Use secrets in deployment
    aws s3 sync ./data s3://my-bucket/
```

**Security Scanning:**
```yaml
# Security checks in pipeline
- name: Security scan
  run: |
    # Dependency vulnerability scanning
    pip install safety
    safety check
    
    # Secret scanning
    pip install detect-secrets
    detect-secrets scan --all-files
    
    # Container security scanning
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
      aquasec/trivy image data-pipeline:latest
```

**Compliance Automation:**
```python
# Automated compliance checks
class ComplianceChecker:
    def check_data_retention(self, table_name):
        # Verify data retention policies
        query = f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE created_at < NOW() - INTERVAL '7 years'
        """
        old_records = self.db.execute(query).scalar()
        
        if old_records > 0:
            raise ComplianceError(f"Found {old_records} records older than retention policy")
    
    def check_pii_encryption(self, table_name):
        # Verify PII fields are encrypted
        pii_fields = ['email', 'phone', 'ssn']
        for field in pii_fields:
            if self.is_field_unencrypted(table_name, field):
                raise ComplianceError(f"PII field {field} is not encrypted")
```

## 📊 Monitoring & Observability

### Q7: How do you monitor CI/CD pipelines and deployments?
**Answer:**

**Pipeline Monitoring:**
```python
# Pipeline metrics collection
import time
import requests
from prometheus_client import Counter, Histogram, Gauge

# Metrics
pipeline_runs_total = Counter('pipeline_runs_total', 'Total pipeline runs', ['status', 'branch'])
pipeline_duration = Histogram('pipeline_duration_seconds', 'Pipeline execution time')
deployment_status = Gauge('deployment_status', 'Current deployment status', ['environment'])

class PipelineMonitor:
    def __init__(self):
        self.start_time = None
    
    def start_pipeline(self, branch):
        self.start_time = time.time()
        self.branch = branch
    
    def end_pipeline(self, status):
        duration = time.time() - self.start_time
        pipeline_duration.observe(duration)
        pipeline_runs_total.labels(status=status, branch=self.branch).inc()
        
        # Send to monitoring system
        self.send_metrics({
            'pipeline_duration': duration,
            'status': status,
            'branch': self.branch,
            'timestamp': time.time()
        })
    
    def send_metrics(self, metrics):
        # Send to DataDog, New Relic, etc.
        requests.post('https://api.datadoghq.com/api/v1/series', 
                     json={'series': [metrics]},
                     headers={'DD-API-KEY': os.getenv('DATADOG_API_KEY')})
```

**Deployment Health Checks:**
```python
# Health check implementation
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
                    'response_time': response.elapsed.total_seconds(),
                    'details': response.json()
                }
            except Exception as e:
                results[name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        return results
    
    def verify_data_pipeline(self):
        # Check if data is flowing correctly
        latest_batch = self.get_latest_batch_timestamp()
        current_time = datetime.utcnow()
        
        if (current_time - latest_batch).total_seconds() > 3600:  # 1 hour
            raise Exception("Data pipeline appears to be stalled")
        
        # Check data quality metrics
        quality_metrics = self.get_data_quality_metrics()
        if quality_metrics['error_rate'] > 0.05:  # 5%
            raise Exception(f"High error rate: {quality_metrics['error_rate']}")
```

## 🎯 Key Takeaways

**CI/CD Pipeline Stages:**
- **Code Quality**: Linting, formatting, security scanning
- **Testing**: Unit, integration, data quality tests
- **Build**: Container images, artifacts
- **Deploy**: Staging, production with approvals
- **Monitor**: Health checks, metrics collection

**Data Engineering Specific Considerations:**
- **Schema validation** and migration testing
- **Data quality** checks in pipelines
- **Environment consistency** for data sources
- **Zero-downtime** deployments for data services

**Best Practices:**
- Automate everything possible
- Fail fast with comprehensive testing
- Use infrastructure as code
- Implement proper secret management
- Monitor pipeline and deployment health
- Maintain rollback capabilities