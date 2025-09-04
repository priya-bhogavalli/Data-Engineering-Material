# GitLab CI/CD Interview Questions & Answers

## 📋 Table of Contents
1. [Core Concepts](#core-concepts)
2. [Pipeline Configuration](#pipeline-configuration)
3. [Advanced Features](#advanced-features)
4. [Security & Compliance](#security--compliance)
5. [Operations & Monitoring](#operations--monitoring)

---

## Core Concepts

### 1. What is GitLab CI/CD and how does it differ from other CI/CD platforms?

**Answer:**
GitLab CI/CD is an integrated continuous integration and deployment platform built into GitLab, providing end-to-end DevOps capabilities.

**Key Features:**
- **Integrated Platform**: Built into GitLab repository management
- **Pipeline as Code**: `.gitlab-ci.yml` configuration
- **Auto DevOps**: Automatic CI/CD pipeline generation
- **Built-in Registry**: Container and package registries
- **Security Scanning**: Integrated security testing

**GitLab vs Other Platforms:**
| Feature | GitLab CI/CD | Jenkins | GitHub Actions |
|---------|--------------|---------|----------------|
| **Integration** | Native GitLab | Plugin-based | Native GitHub |
| **Configuration** | YAML file | Groovy/UI | YAML workflows |
| **Runners** | Shared/dedicated | Agents/nodes | Hosted/self-hosted |
| **Security** | Built-in scanning | Plugins | Marketplace actions |

### 2. How do you create and configure GitLab CI/CD pipelines for data engineering workflows?

**Answer:**
GitLab pipelines are defined using `.gitlab-ci.yml` files with stages, jobs, and various configuration options.

**Basic Data Pipeline Configuration:**
```yaml
stages:
  - validate
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  SPARK_VERSION: "3.4.0"

data_validation:
  stage: validate
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - python scripts/validate_schema.py
  artifacts:
    reports:
      junit: test-results/validation-report.xml
  only:
    - main

unit_tests:
  stage: test
  image: python:3.9
  services:
    - postgres:13
  script:
    - pytest tests/unit/ --junitxml=test-results/unit-tests.xml
  coverage: '/TOTAL.*\s+(\d+%)$/'

build_image:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy_staging:
  stage: deploy
  image: alpine/helm:3.10.0
  script:
    - helm upgrade --install data-pipeline ./helm-chart
        --set image.tag=$CI_COMMIT_SHA
  environment:
    name: staging
  only:
    - main
```

### 3. How do you implement complex pipeline workflows with dependencies?

**Answer:**
GitLab supports complex workflows through job dependencies, parallel execution, and conditional logic.

**Advanced Pipeline Configuration:**
```yaml
stages:
  - prepare
  - parallel_processing
  - integration
  - deploy

prepare_environment:
  stage: prepare
  script:
    - python scripts/setup_test_data.py
  artifacts:
    paths:
      - test-data/

process_customer_data:
  stage: parallel_processing
  script:
    - spark-submit jobs/customer_processing.py
  needs: ["prepare_environment"]
  parallel:
    matrix:
      - REGION: [us-east, us-west, eu-central]

process_transaction_data:
  stage: parallel_processing
  script:
    - spark-submit jobs/transaction_processing.py
  needs: ["prepare_environment"]
  parallel: 3

data_integration:
  stage: integration
  script:
    - python scripts/integrate_all_data.py
  needs:
    - job: process_customer_data
      artifacts: true
    - job: process_transaction_data
      artifacts: true
```

---

## Pipeline Configuration

### 4. How do you use GitLab Container Registry in data pipelines?

**Answer:**
GitLab Container Registry provides centralized storage for Docker images used in data engineering workflows.

**Container Registry Usage:**
```yaml
build_spark_image:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - docker build -f docker/Spark.dockerfile 
        -t $CI_REGISTRY_IMAGE/spark:$CI_COMMIT_SHA .
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $CI_REGISTRY_IMAGE/spark:$CI_COMMIT_SHA

run_spark_job:
  stage: process
  image: $CI_REGISTRY_IMAGE/spark:latest
  script:
    - spark-submit --master local[*] jobs/data_processing.py
```

### 5. How do you implement security scanning in GitLab CI/CD?

**Answer:**
GitLab provides comprehensive security scanning capabilities integrated into CI/CD pipelines.

**Security Scanning Configuration:**
```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

variables:
  SAST_EXCLUDED_PATHS: "tests/, docs/"
  CS_SEVERITY_THRESHOLD: "MEDIUM"

security_audit:
  stage: test
  image: python:3.9
  script:
    - pip install safety bandit
    - safety check -r requirements.txt
    - bandit -r src/ -f json -o bandit-report.json
  artifacts:
    reports:
      sast: bandit-report.json
```

---

## Advanced Features

### 6. How do you manage secrets in GitLab CI/CD?

**Answer:**
GitLab provides multiple mechanisms for secure secret management in CI/CD pipelines.

**Secret Management:**
```yaml
deploy_with_secrets:
  stage: deploy
  script:
    - kubectl create secret generic app-secrets 
        --from-literal=db-password="$DB_PASSWORD"
        --from-literal=api-key="$API_KEY"
  environment:
    name: production
  only:
    - main

vault_integration:
  stage: deploy
  script:
    - export VAULT_TOKEN=$(vault write -field=token auth/jwt/login 
        role=gitlab-ci jwt=$CI_JOB_JWT)
    - export DB_PASSWORD=$(vault kv get -field=password secret/database)
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.company.com
```

### 7. How do you implement multi-environment deployments?

**Answer:**
Multi-environment deployments require careful orchestration with approval gates and environment-specific configurations.

**Multi-Environment Pipeline:**
```yaml
deploy_dev:
  stage: deploy_dev
  script:
    - helm upgrade --install data-pipeline ./helm-chart
        --set environment=development
        --set replicas=1
  environment:
    name: development
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy_staging:
  stage: deploy_staging
  script:
    - helm upgrade --install data-pipeline ./helm-chart
        --set environment=staging
        --set replicas=2
  environment:
    name: staging
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual

deploy_production:
  stage: deploy_production
  script:
    - helm upgrade --install data-pipeline ./helm-chart
        --set environment=production
        --set replicas=3
  environment:
    name: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main" && $CI_COMMIT_TAG
      when: manual
```

---

## Security & Compliance

### 8. How do you implement compliance checks in GitLab pipelines?

**Answer:**
Compliance checks ensure adherence to regulatory and organizational requirements.

**Compliance Configuration:**
```yaml
license_scanning:
  stage: test
  image: python:3.9
  script:
    - pip install pip-licenses
    - pip-licenses --format=json --output-file=licenses.json
    - python scripts/check_license_compliance.py licenses.json
  artifacts:
    reports:
      license_scanning: licenses.json

compliance_check:
  stage: test
  script:
    - python scripts/gdpr_compliance_check.py
    - python scripts/data_retention_check.py
  artifacts:
    reports:
      junit: compliance-results.xml
```

### 9. How do you prevent secrets from being committed?

**Answer:**
GitLab provides secret detection to prevent sensitive data from being committed to repositories.

**Secret Detection:**
```yaml
secret_detection:
  extends: .secret-analyzer
  variables:
    SECRET_DETECTION_EXCLUDED_PATHS: "tests/, docs/"

validate_no_secrets:
  stage: validate
  script:
    - |
      if grep -r "password\|secret\|key" --include="*.py" src/; then
        echo "Potential hardcoded secrets found!"
        exit 1
      fi
```

---

## Operations & Monitoring

### 10. How do you monitor GitLab CI/CD pipeline performance?

**Answer:**
Pipeline monitoring involves tracking execution times, resource usage, and identifying bottlenecks.

**Performance Monitoring:**
```yaml
performance_test:
  stage: test
  script:
    - echo "PIPELINE_START_TIME=$(date +%s)" >> performance.env
    - python scripts/run_performance_tests.py
  artifacts:
    reports:
      dotenv: performance.env
      performance: performance-results.json

analyze_pipeline:
  stage: .post
  script:
    - python scripts/analyze_pipeline_performance.py
  artifacts:
    paths:
      - pipeline-analysis.html
  when: always
```

**Pipeline Analysis Script:**
```python
import requests
import json
from datetime import datetime, timedelta

class GitLabPipelineAnalyzer:
    def __init__(self, project_id, access_token):
        self.project_id = project_id
        self.headers = {'PRIVATE-TOKEN': access_token}
        self.base_url = f"https://gitlab.com/api/v4/projects/{project_id}"
    
    def get_pipeline_data(self, days=30):
        since = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"{self.base_url}/pipelines"
        params = {'updated_after': since, 'per_page': 100}
        
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
    
    def analyze_performance(self, pipeline_data):
        success_rate = len([p for p in pipeline_data if p['status'] == 'success']) / len(pipeline_data) * 100
        avg_duration = sum(p.get('duration', 0) for p in pipeline_data) / len(pipeline_data)
        
        return {
            'success_rate': success_rate,
            'avg_duration': avg_duration
        }
```

---

## Summary

GitLab CI/CD provides comprehensive DevOps capabilities with:

1. **Integrated Platform**: Built-in CI/CD with repository management
2. **Pipeline as Code**: YAML-based configuration with advanced features
3. **Security Integration**: Built-in security scanning and compliance tools
4. **Multi-Environment Support**: Sophisticated deployment workflows
5. **Monitoring & Analytics**: Performance tracking and optimization