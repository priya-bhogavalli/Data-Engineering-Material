# GitLab Key Concepts

## 1. DevOps Platform
**What it is**: Complete DevOps platform with Git repository management, CI/CD, and project management in one application.

**Core Components**:
- **Git Repository**: Version control and code management
- **GitLab CI/CD**: Continuous integration and deployment
- **Issue Tracking**: Project management and bug tracking
- **Container Registry**: Docker image storage
- **Security Scanning**: Built-in security analysis

## 2. Project Structure
**Project Organization**:
```bash
# Create new project
git clone https://gitlab.com/username/project-name.git
cd project-name

# Project structure
project-name/
├── .gitlab-ci.yml          # CI/CD pipeline configuration
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
├── src/                   # Source code
├── tests/                 # Test files
├── docs/                  # Documentation
└── deploy/                # Deployment scripts
```

**Groups and Subgroups**:
```yaml
# Group hierarchy
data-engineering/           # Main group
├── etl-pipelines/         # Subgroup
│   ├── sales-pipeline/    # Project
│   └── customer-pipeline/ # Project
└── analytics/             # Subgroup
    ├── reporting/         # Project
    └── dashboards/        # Project
```

## 3. GitLab CI/CD
**Pipeline Configuration**:
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  PYTHON_VERSION: "3.9"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip/
    - venv/

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt

test:
  stage: test
  script:
    - python -m pytest tests/ --cov=src/ --cov-report=xml
    - python -m flake8 src/
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  script:
    - python setup.py sdist bdist_wheel
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
  only:
    - main
    - develop

deploy_staging:
  stage: deploy
  script:
    - echo "Deploying to staging"
    - ./deploy.sh staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy_production:
  stage: deploy
  script:
    - echo "Deploying to production"
    - ./deploy.sh production
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

**Advanced Pipeline Features**:
```yaml
# Parallel jobs
test:
  stage: test
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.8", "3.9", "3.10"]
  script:
    - python$PYTHON_VERSION -m pytest

# Include external configurations
include:
  - project: 'data-engineering/ci-templates'
    file: '/templates/python.yml'
  - remote: 'https://example.com/ci-template.yml'

# Rules for complex conditions
deploy:
  script: echo "Deploy"
  rules:
    - if: $CI_COMMIT_BRANCH == "main" && $CI_PIPELINE_SOURCE == "push"
    - if: $CI_COMMIT_BRANCH == "develop" && $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
```

## 4. Merge Requests
**Creating Merge Requests**:
```bash
# Create feature branch
git checkout -b feature/new-data-source
git add .
git commit -m "Add support for new data source"
git push origin feature/new-data-source

# Create merge request via GitLab UI or CLI
glab mr create --title "Add new data source support" \
               --description "Implements connector for PostgreSQL data source" \
               --assignee @data-team-lead \
               --reviewer @senior-engineer
```

**Merge Request Templates**:
```markdown
<!-- .gitlab/merge_request_templates/default.md -->
## Description
Brief description of the changes

## Related Issues
Closes #123

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## 5. Container Registry
**Docker Integration**:
```yaml
# Build and push Docker image
build_image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
```

**Dockerfile Example**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 8000

CMD ["python", "-m", "src.main"]
```

## 6. Security Features
**Security Scanning**:
```yaml
# SAST (Static Application Security Testing)
sast:
  stage: test
  variables:
    SAST_EXCLUDED_PATHS: "tests/, docs/"

# Dependency Scanning
dependency_scanning:
  stage: test
  variables:
    DS_PYTHON_VERSION: "3.9"

# Container Scanning
container_scanning:
  stage: test
  variables:
    CS_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

# Include security templates
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
```

**Secret Management**:
```yaml
# Using CI/CD variables
deploy:
  script:
    - echo "Database URL: $DATABASE_URL"
    - echo "API Key: $API_KEY"
  variables:
    DATABASE_URL: "postgresql://localhost:5432/app"
  # API_KEY stored as protected variable in GitLab UI
```

## 7. Issue Tracking
**Issue Templates**:
```markdown
<!-- .gitlab/issue_templates/bug.md -->
## Bug Report

### Description
A clear and concise description of what the bug is.

### Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

### Expected Behavior
A clear and concise description of what you expected to happen.

### Actual Behavior
A clear and concise description of what actually happened.

### Environment
- OS: [e.g. Ubuntu 20.04]
- Python Version: [e.g. 3.9.7]
- Package Version: [e.g. 1.2.3]

### Additional Context
Add any other context about the problem here.
```

**Labels and Milestones**:
```yaml
# Issue labels
labels:
  - bug
  - enhancement
  - documentation
  - priority::high
  - status::in-progress
  - team::data-engineering

# Milestone planning
milestones:
  - name: "Q1 2024 Release"
    due_date: "2024-03-31"
    description: "Major features for Q1"
```

## 8. GitLab Pages
**Static Site Deployment**:
```yaml
# Deploy documentation
pages:
  stage: deploy
  script:
    - pip install mkdocs mkdocs-material
    - mkdocs build --site-dir public
  artifacts:
    paths:
      - public
  only:
    - main
```

**Documentation Structure**:
```yaml
# mkdocs.yml
site_name: Data Engineering Documentation
nav:
  - Home: index.md
  - API Reference: api.md
  - Deployment Guide: deployment.md
theme:
  name: material
```

## 9. API and Automation
**GitLab API**:
```python
import requests

class GitLabAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def create_project(self, name, description):
        url = f"{self.base_url}/projects"
        data = {
            'name': name,
            'description': description,
            'visibility': 'private'
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def create_merge_request(self, project_id, source_branch, target_branch, title):
        url = f"{self.base_url}/projects/{project_id}/merge_requests"
        data = {
            'source_branch': source_branch,
            'target_branch': target_branch,
            'title': title
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_pipeline_status(self, project_id, pipeline_id):
        url = f"{self.base_url}/projects/{project_id}/pipelines/{pipeline_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

# Usage
gitlab = GitLabAPI('https://gitlab.com/api/v4', 'your-token')
project = gitlab.create_project('new-data-pipeline', 'ETL pipeline for sales data')
```

## 10. Monitoring and Analytics
**Pipeline Analytics**:
```yaml
# Custom metrics
metrics_job:
  stage: deploy
  script:
    - echo "deployment_duration_seconds $(date +%s)" > metrics.txt
    - echo "tests_passed_total $TESTS_PASSED" >> metrics.txt
  artifacts:
    reports:
      metrics: metrics.txt
```

**Notification Integration**:
```yaml
# Slack notifications
notify_slack:
  stage: .post
  script:
    - 'curl -X POST -H "Content-type: application/json" 
       --data "{\"text\":\"Pipeline $CI_PIPELINE_STATUS for $CI_PROJECT_NAME\"}" 
       $SLACK_WEBHOOK_URL'
  when: always
```

**Performance Monitoring**:
```yaml
# Performance testing
performance:
  stage: test
  script:
    - pip install locust
    - locust --headless --users 10 --spawn-rate 2 -H http://localhost:8000 --run-time 1m
  artifacts:
    reports:
      performance: performance.json
```