# GitLab Interview Questions & Answers

## Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [GitLab CI/CD](#gitlab-cicd)
3. [Repository Management](#repository-management)
4. [Merge Requests](#merge-requests)
5. [GitLab Runner](#gitlab-runner)
6. [Security & Compliance](#security--compliance)
7. [Project Management](#project-management)
8. [GitLab Administration](#gitlab-administration)
9. [Integration & APIs](#integration--apis)
10. [Best Practices](#best-practices)

---

## Basic Concepts

### 1. What is GitLab and how does it differ from GitHub?

**Answer:**
GitLab is a complete DevOps platform that provides Git repository management with built-in CI/CD, issue tracking, and more.

**Key Differences:**
- **GitLab**: Complete DevOps platform with built-in CI/CD
- **GitHub**: Primarily Git hosting with marketplace integrations
- **GitLab**: Self-hosted and SaaS options
- **GitHub**: Primarily SaaS with GitHub Enterprise
- **GitLab**: Integrated security scanning
- **GitHub**: Third-party security tools

**GitLab Features:**
- Source code management
- Continuous Integration/Deployment
- Issue tracking and project management
- Built-in container registry
- Security and compliance tools
- Monitoring and analytics

### 2. Explain GitLab's architecture components.

**Answer:**
GitLab architecture consists of several components:

**Core Components:**
- **GitLab Rails**: Main application server
- **GitLab Shell**: SSH access and Git operations
- **GitLab Workhorse**: HTTP request handling
- **Gitaly**: Git RPC service
- **PostgreSQL**: Primary database
- **Redis**: Caching and job queues

**Optional Components:**
- **GitLab Runner**: CI/CD job execution
- **Container Registry**: Docker image storage
- **Mattermost**: Team communication
- **Prometheus**: Monitoring and metrics

---

## GitLab CI/CD

### 3. What is GitLab CI/CD and how does it work?

**Answer:**
GitLab CI/CD is an integrated continuous integration and deployment system.

**Key Concepts:**
- **Pipeline**: Collection of jobs organized in stages
- **Job**: Individual tasks (build, test, deploy)
- **Stage**: Logical grouping of jobs
- **Runner**: Agent that executes jobs

**Pipeline Configuration (.gitlab-ci.yml):**
```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building application"
    - npm install
    - npm run build

test_job:
  stage: test
  script:
    - echo "Running tests"
    - npm test

deploy_job:
  stage: deploy
  script:
    - echo "Deploying application"
    - kubectl apply -f deployment.yaml
  only:
    - main
```

### 4. Explain GitLab CI/CD pipeline stages and jobs.

**Answer:**
Pipelines organize work into stages and jobs:

**Stage Execution:**
- Stages run sequentially
- Jobs within a stage run in parallel
- Pipeline fails if any job fails

**Job Configuration:**
```yaml
job_name:
  stage: stage_name
  script:
    - command1
    - command2
  before_script:
    - setup_command
  after_script:
    - cleanup_command
  artifacts:
    paths:
      - build/
    expire_in: 1 week
  only:
    - branches
  except:
    - tags
```

### 5. How do you configure GitLab Runners?

**Answer:**
GitLab Runners execute CI/CD jobs:

**Runner Types:**
- **Shared Runners**: Available to all projects
- **Group Runners**: Available to group projects
- **Specific Runners**: Dedicated to specific projects

**Runner Installation:**
```bash
# Install GitLab Runner
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
sudo apt-get install gitlab-runner

# Register Runner
sudo gitlab-runner register \
  --url "https://gitlab.com/" \
  --registration-token "PROJECT_TOKEN" \
  --executor "docker" \
  --docker-image "alpine:latest"
```

**Runner Configuration:**
```toml
[[runners]]
  name = "docker-runner"
  url = "https://gitlab.com/"
  token = "TOKEN"
  executor = "docker"
  [runners.docker]
    image = "alpine:latest"
    privileged = false
    volumes = ["/cache"]
```

---

## Repository Management

### 6. How do you manage branches and merge strategies in GitLab?

**Answer:**
GitLab provides comprehensive branch management:

**Branch Protection:**
```yaml
# Push rules
- Prevent committing secrets to Git
- GitLab will reject any files that are likely to contain secrets
- Restrict commits by author email
- Restrict by branch name
- Restrict by commit message
```

**Merge Strategies:**
- **Merge Commit**: Creates merge commit
- **Squash and Merge**: Combines commits into one
- **Rebase and Merge**: Linear history without merge commit

**Branch Policies:**
- Required approvals
- Dismiss stale reviews
- Require status checks
- Restrict push access

### 7. What are GitLab's code review features?

**Answer:**
GitLab provides comprehensive code review capabilities:

**Merge Request Features:**
- **Diff Viewing**: Side-by-side and unified views
- **Inline Comments**: Line-specific discussions
- **Approval Rules**: Required reviewers
- **Merge Checks**: Automated quality gates

**Review Process:**
```yaml
# Merge request template
## Description
Brief description of changes

## Changes
- [ ] Feature A implemented
- [ ] Tests added
- [ ] Documentation updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
```

---

## Merge Requests

### 8. How do you create and manage merge requests in GitLab?

**Answer:**
Merge requests facilitate code collaboration:

**Creation Process:**
1. Create feature branch
2. Make changes and commit
3. Push branch to GitLab
4. Create merge request
5. Add description and reviewers
6. Address review feedback
7. Merge when approved

**Merge Request Configuration:**
```yaml
# .gitlab/merge_request_templates/feature.md
## Summary
Brief description of the change

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Documentation
- [ ] README updated
- [ ] API documentation updated
```

### 9. What are GitLab's merge request approval rules?

**Answer:**
Approval rules enforce code review policies:

**Rule Types:**
- **Required Approvals**: Minimum number of approvers
- **Code Owner Approval**: Specific file/directory owners
- **Security Approval**: Security team review
- **Compliance Approval**: Regulatory requirements

**Configuration Example:**
```yaml
# CODEOWNERS file
# Global owners
* @admin-team

# Frontend code
/frontend/ @frontend-team

# Backend code
/backend/ @backend-team

# Database migrations
/db/migrate/ @dba-team @backend-team

# Security-sensitive files
/config/secrets/ @security-team
```

---

## GitLab Runner

### 10. What are the different GitLab Runner executors?

**Answer:**
GitLab Runner supports multiple execution environments:

**Executor Types:**
- **Shell**: Direct command execution
- **Docker**: Container-based execution
- **Docker Machine**: Auto-scaling Docker hosts
- **Kubernetes**: Kubernetes pod execution
- **SSH**: Remote server execution
- **VirtualBox**: VM-based execution

**Docker Executor Configuration:**
```toml
[[runners]]
  name = "docker-runner"
  executor = "docker"
  [runners.docker]
    image = "node:14"
    privileged = false
    volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
    pull_policy = "if-not-present"
```

### 11. How do you implement auto-scaling with GitLab Runner?

**Answer:**
Auto-scaling automatically manages runner capacity:

**Docker Machine Configuration:**
```toml
[[runners]]
  name = "docker-machine-runner"
  executor = "docker+machine"
  limit = 10
  [runners.machine]
    IdleCount = 2
    IdleTime = 1800
    MaxBuilds = 100
    MachineDriver = "amazonec2"
    MachineName = "gitlab-runner-%s"
    MachineOptions = [
      "amazonec2-access-key=ACCESS_KEY",
      "amazonec2-secret-key=SECRET_KEY",
      "amazonec2-region=us-east-1",
      "amazonec2-instance-type=t3.medium"
    ]
```

**Kubernetes Executor:**
```toml
[[runners]]
  name = "kubernetes-runner"
  executor = "kubernetes"
  [runners.kubernetes]
    namespace = "gitlab-runner"
    image = "alpine:latest"
    cpu_limit = "1"
    memory_limit = "1Gi"
    service_cpu_limit = "200m"
    service_memory_limit = "256Mi"
```

---

## Security & Compliance

### 12. What security features does GitLab provide?

**Answer:**
GitLab offers comprehensive security capabilities:

**Security Scanning:**
- **SAST**: Static Application Security Testing
- **DAST**: Dynamic Application Security Testing
- **Container Scanning**: Vulnerability scanning for containers
- **Dependency Scanning**: Third-party dependency vulnerabilities
- **License Compliance**: License policy enforcement

**Pipeline Security Configuration:**
```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/DAST.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml

variables:
  DAST_WEBSITE: https://example.com
  DAST_FULL_SCAN_ENABLED: "true"
```

### 13. How do you implement compliance pipelines in GitLab?

**Answer:**
Compliance pipelines ensure regulatory adherence:

**Compliance Features:**
- **Audit Events**: Track all activities
- **Compliance Dashboard**: Centralized compliance view
- **Merge Request Approvals**: Required approvals
- **Push Rules**: Prevent non-compliant commits
- **Compliance Frameworks**: Industry-specific templates

**Compliance Pipeline Example:**
```yaml
stages:
  - compliance-check
  - build
  - test
  - security-scan
  - deploy

compliance-check:
  stage: compliance-check
  script:
    - echo "Running compliance checks"
    - compliance-tool --check-policies
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

security-scan:
  stage: security-scan
  script:
    - security-scanner --output compliance-report.json
  artifacts:
    reports:
      sast: compliance-report.json
```

---

## Project Management

### 14. How does GitLab's issue tracking system work?

**Answer:**
GitLab provides integrated issue management:

**Issue Features:**
- **Labels**: Categorization and filtering
- **Milestones**: Release planning
- **Assignees**: Responsibility tracking
- **Due Dates**: Timeline management
- **Time Tracking**: Effort estimation
- **Issue Boards**: Kanban-style workflow

**Issue Templates:**
```markdown
## Summary
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: 
- Browser: 
- Version: 

/label ~bug ~priority::high
/assign @developer
/milestone %v1.0
```

### 15. What are GitLab Epics and how do you use them?

**Answer:**
Epics organize related issues across projects:

**Epic Structure:**
- **Epic**: High-level feature or initiative
- **Issues**: Specific tasks within the epic
- **Child Epics**: Sub-epics for complex features

**Epic Planning:**
```markdown
# Epic: User Authentication System

## Description
Implement comprehensive user authentication system

## Child Issues
- [ ] #123 User registration
- [ ] #124 Login functionality  
- [ ] #125 Password reset
- [ ] #126 Two-factor authentication
- [ ] #127 Social login integration

## Acceptance Criteria
- Users can register and login
- Password security requirements met
- 2FA optional for users
- Social login with Google/GitHub
```

---

## GitLab Administration

### 16. How do you configure GitLab for high availability?

**Answer:**
GitLab HA requires multiple components:

**HA Architecture:**
- **Load Balancer**: Distribute traffic
- **Multiple GitLab Nodes**: Application servers
- **Shared Storage**: NFS or object storage
- **Database Cluster**: PostgreSQL HA
- **Redis Cluster**: Cache and sessions

**Configuration Example:**
```ruby
# /etc/gitlab/gitlab.rb
external_url 'https://gitlab.example.com'

# Database
postgresql['enable'] = false
gitlab_rails['db_host'] = 'postgres-cluster.example.com'
gitlab_rails['db_port'] = 5432
gitlab_rails['db_database'] = 'gitlabhq_production'

# Redis
redis['enable'] = false
gitlab_rails['redis_host'] = 'redis-cluster.example.com'
gitlab_rails['redis_port'] = 6379

# Object storage
gitlab_rails['object_store']['enabled'] = true
gitlab_rails['object_store']['connection'] = {
  'provider' => 'AWS',
  'region' => 'us-east-1',
  'aws_access_key_id' => 'ACCESS_KEY',
  'aws_secret_access_key' => 'SECRET_KEY'
}
```

### 17. How do you backup and restore GitLab?

**Answer:**
GitLab provides comprehensive backup solutions:

**Backup Components:**
- Database (PostgreSQL)
- Git repositories
- Uploaded files
- CI/CD job artifacts
- Container registry
- Configuration files

**Backup Commands:**
```bash
# Create backup
sudo gitlab-backup create

# Create backup with specific name
sudo gitlab-backup create BACKUP=1609459200_2021_01_01_13.6.0

# Restore backup
sudo gitlab-ctl stop unicorn
sudo gitlab-ctl stop puma
sudo gitlab-ctl stop sidekiq
sudo gitlab-backup restore BACKUP=1609459200_2021_01_01_13.6.0
sudo gitlab-ctl restart
sudo gitlab-rake gitlab:check SANITIZE=true
```

**Automated Backup Script:**
```bash
#!/bin/bash
# Automated GitLab backup
BACKUP_DIR="/var/opt/gitlab/backups"
RETENTION_DAYS=30

# Create backup
gitlab-backup create

# Clean old backups
find $BACKUP_DIR -name "*.tar" -mtime +$RETENTION_DAYS -delete

# Upload to S3
aws s3 sync $BACKUP_DIR s3://gitlab-backups/
```

---

## Integration & APIs

### 18. How do you use GitLab's REST API?

**Answer:**
GitLab provides comprehensive REST API access:

**Authentication:**
```bash
# Personal Access Token
curl --header "PRIVATE-TOKEN: your_token" \
  "https://gitlab.example.com/api/v4/projects"

# OAuth2 Token
curl --header "Authorization: Bearer oauth_token" \
  "https://gitlab.example.com/api/v4/projects"
```

**Common API Operations:**
```bash
# List projects
curl --header "PRIVATE-TOKEN: token" \
  "https://gitlab.example.com/api/v4/projects"

# Create project
curl --header "PRIVATE-TOKEN: token" \
  --header "Content-Type: application/json" \
  --data '{"name":"new-project","visibility":"private"}' \
  --request POST \
  "https://gitlab.example.com/api/v4/projects"

# Create merge request
curl --header "PRIVATE-TOKEN: token" \
  --header "Content-Type: application/json" \
  --data '{"source_branch":"feature","target_branch":"main","title":"Feature implementation"}' \
  --request POST \
  "https://gitlab.example.com/api/v4/projects/1/merge_requests"
```

### 19. How do you integrate GitLab with external tools?

**Answer:**
GitLab supports various integration methods:

**Webhook Integration:**
```json
{
  "url": "https://external-tool.com/webhook",
  "push_events": true,
  "merge_requests_events": true,
  "issues_events": true,
  "pipeline_events": true,
  "job_events": true,
  "token": "webhook_secret_token"
}
```

**CI/CD Integration Example:**
```yaml
# Deploy to Kubernetes
deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --insecure-skip-tls-verify=true
    - kubectl config set-credentials admin --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=admin
    - kubectl config use-context default
    - kubectl apply -f k8s/
  only:
    - main
```

---

## Best Practices

### 20. What are GitLab CI/CD best practices?

**Answer:**
Key best practices for GitLab CI/CD:

**Pipeline Design:**
- Keep pipelines fast and efficient
- Use parallel jobs where possible
- Implement proper error handling
- Cache dependencies appropriately

**Security Practices:**
- Use protected variables for secrets
- Implement least privilege access
- Scan for vulnerabilities regularly
- Validate all inputs

**Example Optimized Pipeline:**
```yaml
variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

cache:
  paths:
    - node_modules/
    - .npm/

stages:
  - build
  - test
  - security
  - deploy

build:
  stage: build
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

test:
  stage: test
  script:
    - npm run test:unit
    - npm run test:integration
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

security:
  stage: security
  include:
    - template: Security/SAST.gitlab-ci.yml
    - template: Security/Container-Scanning.gitlab-ci.yml
```

### 21. How do you implement GitLab CI/CD for data engineering pipelines?
**Answer**: Data engineering pipelines require specialized CI/CD configurations for ETL processes, data validation, and deployment.

```yaml
# .gitlab-ci.yml for data engineering pipeline
stages:
  - validate
  - test
  - build
  - deploy-dev
  - deploy-staging
  - deploy-prod

variables:
  DOCKER_DRIVER: overlay2
  SPARK_VERSION: "3.3.0"
  PYTHON_VERSION: "3.9"

# Data validation stage
validate-data-schema:
  stage: validate
  image: python:${PYTHON_VERSION}
  script:
    - pip install great-expectations pandas
    - python scripts/validate_schema.py
    - great_expectations checkpoint run data_quality_checkpoint
  artifacts:
    reports:
      junit: validation-results.xml
    paths:
      - validation-reports/
    expire_in: 1 week
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "main"'

# SQL linting and testing
sql-lint:
  stage: test
  image: python:${PYTHON_VERSION}
  script:
    - pip install sqlfluff dbt-core dbt-postgres
    - sqlfluff lint sql/ --dialect postgres
    - dbt parse --profiles-dir profiles/
    - dbt test --profiles-dir profiles/ --target ci
  artifacts:
    reports:
      junit: dbt-test-results.xml

# Python code quality
code-quality:
  stage: test
  image: python:${PYTHON_VERSION}
  script:
    - pip install pylint black isort mypy pytest pytest-cov
    - black --check .
    - isort --check-only .
    - pylint src/
    - mypy src/
    - pytest --cov=src/ --cov-report=xml --junitxml=pytest-results.xml
  artifacts:
    reports:
      junit: pytest-results.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

### 22. How do you implement GitLab Container Registry for data engineering?
**Answer**: GitLab Container Registry stores Docker images for data processing applications.

```yaml
# Build and push data processing images
build-base-image:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -f Dockerfile.base -t $CI_REGISTRY_IMAGE/base:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE/base:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE/base:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE/base:latest
    - docker push $CI_REGISTRY_IMAGE/base:latest
```

This comprehensive set of interview questions covers all major aspects of GitLab, from basic concepts to advanced administration and best practices. The questions progress from fundamental understanding to practical implementation scenarios that data engineers would encounter in real-world environments.