# Bitbucket Key Concepts

## 1. Git-Based Repository Hosting
**What it is**: Atlassian's Git repository management solution with integrated CI/CD and project management.

**Core Features**:
- **Git Repositories**: Version control for code
- **Pull Requests**: Code review and collaboration
- **Pipelines**: Built-in CI/CD automation
- **Jira Integration**: Issue tracking and project management
- **Branch Permissions**: Access control and workflow enforcement

## 2. Repository Management
**Creating Repositories**:
```bash
# Clone repository
git clone https://bitbucket.org/workspace/repository-name.git

# Add Bitbucket as remote
git remote add origin https://bitbucket.org/workspace/repository-name.git

# Push to Bitbucket
git push -u origin main
```

**Repository Settings**:
```yaml
# .gitignore for data projects
*.pyc
__pycache__/
.env
.venv/
*.log
data/raw/
*.parquet
*.csv
.DS_Store
.idea/
```

## 3. Branching Strategy
**Git Flow with Bitbucket**:
```bash
# Feature branch workflow
git checkout -b feature/data-pipeline-enhancement
git add .
git commit -m "Add new data transformation logic"
git push origin feature/data-pipeline-enhancement

# Create pull request (via Bitbucket UI)
# After approval and merge:
git checkout main
git pull origin main
git branch -d feature/data-pipeline-enhancement
```

**Branch Permissions**:
```json
{
  "branch": "main",
  "restrictions": [
    {
      "type": "push",
      "users": [],
      "groups": ["administrators"],
      "access_keys": []
    },
    {
      "type": "require_pull_request_approval",
      "value": 2
    }
  ]
}
```

## 4. Pull Requests
**Creating Pull Requests**:
```bash
# Push feature branch
git push origin feature/new-etl-job

# Pull request template (.bitbucket/pull_request_template.md)
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

**Code Review Process**:
```yaml
# Required reviewers configuration
reviewers:
  - type: "user"
    username: "senior-engineer"
  - type: "group"
    name: "data-team"
    
approval_rules:
  - name: "Require 2 approvals"
    pattern: "**"
    required_approvals: 2
  - name: "Admin approval for main"
    pattern: "main"
    required_approvals: 1
    users: ["admin"]
```

## 5. Bitbucket Pipelines
**Pipeline Configuration**:
```yaml
# bitbucket-pipelines.yml
image: python:3.9

pipelines:
  default:
    - step:
        name: Test and Build
        caches:
          - pip
        script:
          - pip install -r requirements.txt
          - python -m pytest tests/
          - python -m flake8 src/
        artifacts:
          - dist/**
  
  branches:
    main:
      - step:
          name: Deploy to Production
          deployment: production
          script:
            - pip install -r requirements.txt
            - python setup.py sdist bdist_wheel
            - aws s3 cp dist/ s3://deployment-bucket/ --recursive
          services:
            - docker
  
  pull-requests:
    '**':
      - step:
          name: Code Quality Check
          script:
            - pip install -r requirements.txt
            - python -m pytest tests/ --cov=src/
            - python -m black --check src/
            - python -m isort --check-only src/
```

**Advanced Pipeline Features**:
```yaml
# Parallel steps
pipelines:
  default:
    - parallel:
        - step:
            name: Unit Tests
            script:
              - python -m pytest tests/unit/
        - step:
            name: Integration Tests
            script:
              - python -m pytest tests/integration/
        - step:
            name: Linting
            script:
              - python -m flake8 src/
    - step:
        name: Deploy
        script:
          - echo "Deploying application"

# Custom Docker image
image: 
  name: python:3.9-slim
  username: $DOCKER_HUB_USERNAME
  password: $DOCKER_HUB_PASSWORD

# Environment variables
pipelines:
  default:
    - step:
        script:
          - export DATABASE_URL=$DATABASE_URL
          - python manage.py migrate
```

## 6. Jira Integration
**Linking Issues**:
```bash
# Commit message with Jira issue
git commit -m "DATA-123: Implement new data validation logic

- Add validation for customer data
- Update error handling
- Add unit tests for validation functions"

# Branch naming with Jira issue
git checkout -b feature/DATA-123-data-validation
```

**Smart Commits**:
```bash
# Transition Jira issue
git commit -m "DATA-123 #time 2h #comment Fixed data validation bug"

# Close issue
git commit -m "DATA-123 #close Fixed validation and deployed to production"
```

## 7. Access Management
**User Permissions**:
```yaml
# Repository access levels
permissions:
  - user: "data-engineer"
    permission: "write"
  - user: "data-analyst" 
    permission: "read"
  - group: "administrators"
    permission: "admin"

# Workspace permissions
workspace_permissions:
  - user: "team-lead"
    permission: "workspace-admin"
  - group: "developers"
    permission: "repository-create"
```

**SSH Keys**:
```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096 -C "your.email@company.com"

# Add to Bitbucket (Personal settings > SSH keys)
cat ~/.ssh/id_rsa.pub

# Clone with SSH
git clone git@bitbucket.org:workspace/repository.git
```

## 8. Code Insights and Quality
**Code Quality Tools**:
```yaml
# SonarQube integration
pipelines:
  default:
    - step:
        name: SonarQube Analysis
        script:
          - sonar-scanner
        after-script:
          - curl -u $SONAR_TOKEN: $SONAR_HOST_URL/api/qualitygates/project_status?projectKey=$SONAR_PROJECT_KEY
```

**Security Scanning**:
```yaml
# Security scan step
- step:
    name: Security Scan
    script:
      - pip install safety bandit
      - safety check -r requirements.txt
      - bandit -r src/ -f json -o bandit-report.json
    artifacts:
      - bandit-report.json
```

## 9. Deployment Strategies
**Environment Management**:
```yaml
# Multiple environments
pipelines:
  branches:
    develop:
      - step:
          name: Deploy to Staging
          deployment: staging
          script:
            - ./deploy.sh staging
    
    main:
      - step:
          name: Deploy to Production
          deployment: production
          trigger: manual
          script:
            - ./deploy.sh production

# Deployment variables
deployments:
  staging:
    - variable:
        name: DATABASE_URL
        value: "postgresql://staging-db:5432/app"
  production:
    - variable:
        name: DATABASE_URL
        value: "postgresql://prod-db:5432/app"
        secured: true
```

## 10. API and Automation
**Bitbucket REST API**:
```python
import requests
from requests.auth import HTTPBasicAuth

# API configuration
base_url = "https://api.bitbucket.org/2.0"
auth = HTTPBasicAuth('username', 'app_password')

# Create repository
def create_repository(workspace, repo_name):
    url = f"{base_url}/repositories/{workspace}/{repo_name}"
    data = {
        "scm": "git",
        "is_private": True,
        "description": "Data engineering repository"
    }
    response = requests.post(url, json=data, auth=auth)
    return response.json()

# Create pull request
def create_pull_request(workspace, repo_name, source_branch, destination_branch):
    url = f"{base_url}/repositories/{workspace}/{repo_name}/pullrequests"
    data = {
        "title": "Feature implementation",
        "source": {"branch": {"name": source_branch}},
        "destination": {"branch": {"name": destination_branch}},
        "reviewers": [{"username": "reviewer1"}]
    }
    response = requests.post(url, json=data, auth=auth)
    return response.json()

# Get pipeline status
def get_pipeline_status(workspace, repo_name, commit_hash):
    url = f"{base_url}/repositories/{workspace}/{repo_name}/commit/{commit_hash}/statuses"
    response = requests.get(url, auth=auth)
    return response.json()
```

**Webhooks**:
```python
# Webhook payload example
webhook_payload = {
    "repository": {
        "name": "data-pipeline",
        "full_name": "workspace/data-pipeline"
    },
    "push": {
        "changes": [
            {
                "new": {
                    "name": "main",
                    "target": {
                        "hash": "abc123",
                        "message": "Add new ETL job"
                    }
                }
            }
        ]
    }
}

# Webhook handler
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.json
    if payload['push']['changes'][0]['new']['name'] == 'main':
        trigger_deployment()
    return 'OK'
```