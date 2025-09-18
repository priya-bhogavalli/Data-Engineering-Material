# Bitbucket Interview Questions & Answers

## Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Repository Management](#repository-management)
3. [Bitbucket Pipelines](#bitbucket-pipelines)
4. [Pull Requests](#pull-requests)
5. [Branching Strategies](#branching-strategies)
6. [Integration & APIs](#integration--apis)
7. [Security & Permissions](#security--permissions)
8. [Administration](#administration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Basic Concepts

### 1. What is Bitbucket and how does it compare to other Git platforms?

**Answer:**
Bitbucket is Atlassian's Git repository management solution with integrated CI/CD capabilities.

**Key Features:**
- Git and Mercurial repository hosting
- Built-in CI/CD with Bitbucket Pipelines
- Integration with Atlassian ecosystem (Jira, Confluence)
- Pull request workflows
- Branch permissions and security

**Comparison with Competitors:**
- **vs GitHub**: Better Jira integration, unlimited private repos
- **vs GitLab**: Stronger Atlassian ecosystem integration
- **vs Azure DevOps**: More focused on Git, less comprehensive DevOps

### 2. Explain Bitbucket's architecture and deployment options.

**Answer:**
Bitbucket offers multiple deployment options:

**Bitbucket Cloud:**
- SaaS solution hosted by Atlassian
- Automatic updates and maintenance
- Built-in scalability
- Pay-per-user pricing

**Bitbucket Server (Data Center):**
- Self-hosted on-premises solution
- Full control over infrastructure
- Enterprise features and compliance
- High availability clustering

**Architecture Components:**
- **Application Server**: Core Bitbucket application
- **Database**: PostgreSQL or SQL Server
- **File System**: Git repository storage
- **Search Index**: Elasticsearch for code search
- **Load Balancer**: For high availability setups

---

## Repository Management

### 3. How do you create and configure repositories in Bitbucket?

**Answer:**
Repository creation and configuration process:

**Creating Repository:**
1. Navigate to workspace/project
2. Click "Create repository"
3. Configure repository settings
4. Set access permissions
5. Initialize with README/gitignore

**Repository Configuration:**
```bash
# Clone repository
git clone https://bitbucket.org/workspace/repo-name.git

# Configure repository settings
git config user.name "Your Name"
git config user.email "your.email@company.com"

# Add remote origin
git remote add origin https://bitbucket.org/workspace/repo-name.git
```

**Repository Settings:**
- **Access Level**: Private, public, or team access
- **Language**: Primary programming language
- **Issue Tracking**: Enable/disable issue tracker
- **Wiki**: Enable/disable wiki
- **Forking**: Allow/restrict repository forking

### 4. What are Bitbucket workspaces and projects?

**Answer:**
Bitbucket organizes repositories using workspaces and projects:

**Workspaces:**
- Top-level organizational unit
- Contains all repositories and projects
- Manages billing and user access
- Equivalent to GitHub organizations

**Projects:**
- Logical grouping within workspaces
- Organize related repositories
- Shared permissions and settings
- Integration with Jira projects

**Hierarchy:**
```
Workspace (company-name)
├── Project A (frontend-apps)
│   ├── Repository 1 (web-app)
│   └── Repository 2 (mobile-app)
└── Project B (backend-services)
    ├── Repository 3 (api-service)
    └── Repository 4 (auth-service)
```

---

## Bitbucket Pipelines

### 5. What are Bitbucket Pipelines and how do they work?

**Answer:**
Bitbucket Pipelines is the integrated CI/CD solution:

**Key Concepts:**
- **Pipeline**: Automated build/deployment process
- **Step**: Individual task within pipeline
- **Image**: Docker container for execution
- **Artifact**: Files passed between steps
- **Deployment**: Environment-specific releases

**Pipeline Configuration (bitbucket-pipelines.yml):**
```yaml
image: node:14

pipelines:
  default:
    - step:
        name: Build and Test
        caches:
          - node
        script:
          - npm install
          - npm test
          - npm run build
        artifacts:
          - dist/**

  branches:
    main:
      - step:
          name: Build
          caches:
            - node
          script:
            - npm install
            - npm run build
          artifacts:
            - dist/**
      - step:
          name: Deploy to Production
          deployment: production
          script:
            - echo "Deploying to production"
            - ./deploy.sh production
```

### 6. How do you configure parallel and conditional pipelines?

**Answer:**
Bitbucket Pipelines supports parallel execution and conditions:

**Parallel Steps:**
```yaml
pipelines:
  default:
    - parallel:
        - step:
            name: Unit Tests
            script:
              - npm run test:unit
        - step:
            name: Integration Tests
            script:
              - npm run test:integration
        - step:
            name: Lint Code
            script:
              - npm run lint
```

**Conditional Pipelines:**
```yaml
pipelines:
  branches:
    main:
      - step:
          name: Deploy Production
          condition:
            changesets:
              includePaths:
                - "src/**"
          script:
            - ./deploy.sh production

  pull-requests:
    '**':
      - step:
          name: Test Changes
          script:
            - npm test

  tags:
    'v*':
      - step:
          name: Release
          script:
            - ./release.sh
```

### 7. How do you manage secrets and environment variables in Pipelines?

**Answer:**
Bitbucket provides secure variable management:

**Repository Variables:**
- Stored in repository settings
- Available to all pipelines
- Can be secured (encrypted)

**Deployment Variables:**
- Environment-specific variables
- Associated with deployment environments
- Override repository variables

**Configuration Example:**
```yaml
pipelines:
  default:
    - step:
        name: Deploy
        script:
          - echo "Database URL: $DATABASE_URL"
          - echo "API Key: $API_KEY"
          - ./deploy.sh
        deployment: staging

  branches:
    main:
      - step:
          name: Production Deploy
          script:
            - echo "Production Database: $PROD_DATABASE_URL"
            - ./deploy.sh production
          deployment: production
```

**Variable Types:**
- **Regular**: Visible in pipeline logs
- **Secured**: Encrypted, hidden in logs
- **Deployment**: Environment-specific

---

## Pull Requests

### 8. How do pull requests work in Bitbucket?

**Answer:**
Pull requests facilitate code review and collaboration:

**Pull Request Workflow:**
1. Create feature branch
2. Make changes and commit
3. Create pull request
4. Add reviewers and description
5. Address review feedback
6. Merge when approved

**Pull Request Features:**
- **Diff Viewing**: Side-by-side and unified views
- **Inline Comments**: Line-specific discussions
- **Approval System**: Required approvers
- **Merge Strategies**: Merge commit, squash, fast-forward
- **Build Status**: CI/CD integration

**Example Pull Request Template:**
```markdown
## Description
Brief description of changes made

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### 9. What are Bitbucket's merge strategies?

**Answer:**
Bitbucket supports multiple merge strategies:

**Merge Strategies:**
- **Merge Commit**: Creates explicit merge commit
- **Squash**: Combines all commits into single commit
- **Fast-Forward**: Linear history without merge commit

**Strategy Configuration:**
```json
{
  "merge_strategies": {
    "allowed": ["merge_commit", "squash", "fast_forward"],
    "default": "merge_commit"
  },
  "delete_source_branch": true,
  "close_source_branch": true
}
```

**When to Use Each:**
- **Merge Commit**: Preserve complete history
- **Squash**: Clean history for features
- **Fast-Forward**: Simple linear progression

---

## Branching Strategies

### 10. How do you implement Git Flow in Bitbucket?

**Answer:**
Git Flow implementation with Bitbucket features:

**Branch Structure:**
- **main**: Production-ready code
- **develop**: Integration branch
- **feature/***: Feature development
- **release/***: Release preparation
- **hotfix/***: Production fixes

**Bitbucket Configuration:**
```yaml
# Branch permissions
branches:
  main:
    - require_pull_request: true
    - require_approvals: 2
    - dismiss_stale_reviews: true
    - restrict_pushes: true
  
  develop:
    - require_pull_request: true
    - require_approvals: 1
    - allow_force_pushes: false

  feature/*:
    - allow_force_pushes: true
    - delete_after_merge: true
```

**Pipeline Configuration for Git Flow:**
```yaml
pipelines:
  branches:
    main:
      - step:
          name: Deploy Production
          deployment: production
          script:
            - ./deploy.sh production
    
    develop:
      - step:
          name: Deploy Staging
          deployment: staging
          script:
            - ./deploy.sh staging
    
    feature/*:
      - step:
          name: Feature Tests
          script:
            - npm test
```

### 11. How do you configure branch permissions in Bitbucket?

**Answer:**
Branch permissions control access and enforce workflows:

**Permission Types:**
- **Write Access**: Who can push to branch
- **Merge Access**: Who can merge pull requests
- **Delete Access**: Who can delete branch
- **Force Push**: Allow/prevent force pushes

**Configuration Example:**
```json
{
  "branch_restrictions": [
    {
      "kind": "push",
      "branch_match_kind": "glob",
      "pattern": "main",
      "users": [],
      "groups": ["administrators"],
      "value": null
    },
    {
      "kind": "require_pull_request_approvals_to_merge",
      "branch_match_kind": "glob", 
      "pattern": "main",
      "value": 2
    },
    {
      "kind": "require_passing_builds_to_merge",
      "branch_match_kind": "glob",
      "pattern": "main",
      "value": null
    }
  ]
}
```

---

## Integration & APIs

### 12. How do you use Bitbucket's REST API?

**Answer:**
Bitbucket provides comprehensive REST API access:

**Authentication:**
```bash
# App Password
curl -u username:app_password \
  https://api.bitbucket.org/2.0/repositories/workspace/repo

# OAuth2
curl -H "Authorization: Bearer access_token" \
  https://api.bitbucket.org/2.0/repositories/workspace/repo
```

**Common API Operations:**
```bash
# List repositories
curl -u username:password \
  https://api.bitbucket.org/2.0/repositories/workspace

# Create repository
curl -X POST -u username:password \
  -H "Content-Type: application/json" \
  -d '{"name":"new-repo","is_private":true}' \
  https://api.bitbucket.org/2.0/repositories/workspace/new-repo

# Create pull request
curl -X POST -u username:password \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Feature implementation",
    "source":{"branch":{"name":"feature-branch"}},
    "destination":{"branch":{"name":"main"}}
  }' \
  https://api.bitbucket.org/2.0/repositories/workspace/repo/pullrequests
```

### 13. How do you integrate Bitbucket with Jira?

**Answer:**
Bitbucket-Jira integration provides seamless workflow:

**Integration Features:**
- **Smart Commits**: Link commits to Jira issues
- **Development Panel**: View code changes in Jira
- **Deployment Tracking**: Track releases in Jira
- **Automated Transitions**: Update issue status

**Smart Commit Examples:**
```bash
# Link commit to issue
git commit -m "PROJ-123 Fix login bug"

# Transition issue and add time
git commit -m "PROJ-123 #time 2h #comment Fixed authentication issue"

# Close issue
git commit -m "PROJ-123 #close Fixed user registration"
```

**Pipeline Integration:**
```yaml
pipelines:
  default:
    - step:
        name: Build and Deploy
        script:
          - npm run build
          - ./deploy.sh
        after-script:
          - pipe: atlassian/jira-integration:1.0.0
            variables:
              JIRA_BASE_URL: $JIRA_BASE_URL
              JIRA_USER_EMAIL: $JIRA_USER_EMAIL
              JIRA_API_TOKEN: $JIRA_API_TOKEN
              STATE: 'successful'
              ISSUE_KEYS: $BITBUCKET_COMMIT_MESSAGE
```

---

## Security & Permissions

### 14. How do you implement security best practices in Bitbucket?

**Answer:**
Bitbucket security involves multiple layers:

**Access Control:**
- **Two-Factor Authentication**: Mandatory 2FA
- **App Passwords**: Secure API access
- **SSH Keys**: Secure Git operations
- **IP Whitelisting**: Restrict access by location

**Repository Security:**
```yaml
# Security scanning in pipelines
pipelines:
  default:
    - step:
        name: Security Scan
        script:
          - npm audit
          - snyk test
          - docker run --rm -v $(pwd):/app clair-scanner
        after-script:
          - pipe: atlassian/security-scan:1.0.0
```

**Branch Protection:**
- Require pull requests for protected branches
- Mandatory code reviews
- Status checks must pass
- Restrict force pushes

### 15. What are Bitbucket's user and group management features?

**Answer:**
Bitbucket provides comprehensive user management:

**User Management:**
- **Workspace Members**: Add/remove users
- **Permission Levels**: Admin, write, read access
- **Group Management**: Organize users into groups
- **External Users**: Guest access for external collaborators

**Permission Levels:**
- **Admin**: Full workspace control
- **Member**: Repository access based on permissions
- **Read**: View repositories and clone
- **Write**: Push changes and create branches
- **Admin**: Repository administration

**Group Configuration:**
```json
{
  "groups": [
    {
      "name": "developers",
      "permission": "write",
      "members": ["user1", "user2", "user3"]
    },
    {
      "name": "reviewers", 
      "permission": "admin",
      "members": ["senior1", "senior2"]
    }
  ]
}
```

---

## Administration

### 16. How do you configure Bitbucket Server for high availability?

**Answer:**
Bitbucket Server HA requires clustering setup:

**HA Components:**
- **Load Balancer**: Distribute traffic across nodes
- **Shared Database**: PostgreSQL or SQL Server cluster
- **Shared File System**: NFS or SAN for repositories
- **Search Index**: Elasticsearch cluster

**Configuration Example:**
```properties
# bitbucket.properties
jdbc.driver=org.postgresql.Driver
jdbc.url=jdbc:postgresql://db-cluster:5432/bitbucket
jdbc.user=bitbucket
jdbc.password=password

# Shared home directory
bitbucket.shared.home=/shared/bitbucket-shared

# Clustering
hazelcast.network.tcpip=true
hazelcast.network.tcpip.members=node1:5701,node2:5701,node3:5701
```

**Load Balancer Configuration:**
```nginx
upstream bitbucket {
    server bitbucket-node1:7990;
    server bitbucket-node2:7990;
    server bitbucket-node3:7990;
}

server {
    listen 80;
    server_name bitbucket.company.com;
    
    location / {
        proxy_pass http://bitbucket;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 17. How do you backup and restore Bitbucket?

**Answer:**
Bitbucket backup involves multiple components:

**Backup Components:**
- **Database**: Application data and metadata
- **Repositories**: Git repository data
- **Shared Home**: Configuration and plugins
- **Search Index**: Elasticsearch data

**Backup Script:**
```bash
#!/bin/bash
BACKUP_DIR="/backup/bitbucket/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Stop Bitbucket
systemctl stop bitbucket

# Backup database
pg_dump -h db-server -U bitbucket bitbucket > $BACKUP_DIR/database.sql

# Backup repositories
rsync -av /var/atlassian/application-data/bitbucket/shared/data/repositories/ \
  $BACKUP_DIR/repositories/

# Backup shared home
rsync -av /var/atlassian/application-data/bitbucket/shared/ \
  $BACKUP_DIR/shared/

# Start Bitbucket
systemctl start bitbucket

# Compress backup
tar -czf $BACKUP_DIR.tar.gz -C /backup/bitbucket $(basename $BACKUP_DIR)
rm -rf $BACKUP_DIR
```

---

## Best Practices

### 18. What are Bitbucket Pipelines best practices?

**Answer:**
Key best practices for efficient pipelines:

**Performance Optimization:**
- Use appropriate Docker images
- Implement caching strategies
- Parallelize independent tasks
- Optimize build scripts

**Example Optimized Pipeline:**
```yaml
image: node:14-alpine

definitions:
  caches:
    npm: ~/.npm
    cypress: ~/.cache/Cypress

pipelines:
  default:
    - step:
        name: Install Dependencies
        caches:
          - npm
        script:
          - npm ci
        artifacts:
          - node_modules/**

    - parallel:
        - step:
            name: Unit Tests
            script:
              - npm run test:unit
            artifacts:
              - coverage/**
        - step:
            name: Lint
            script:
              - npm run lint
        - step:
            name: Build
            script:
              - npm run build
            artifacts:
              - dist/**

    - step:
        name: Integration Tests
        caches:
          - cypress
        script:
          - npm run test:integration
        services:
          - postgres
```

### 19. How do you implement effective code review workflows?

**Answer:**
Effective code review practices in Bitbucket:

**Review Guidelines:**
- **Small Pull Requests**: Easier to review
- **Clear Descriptions**: Context and reasoning
- **Automated Checks**: CI/CD integration
- **Timely Reviews**: Set SLA expectations

**Pull Request Template:**
```markdown
## Summary
Brief description of the change

## Motivation and Context
Why is this change required? What problem does it solve?

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Types of Changes
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature causing existing functionality to change)

## Checklist
- [ ] My code follows the code style of this project
- [ ] My change requires a change to the documentation
- [ ] I have updated the documentation accordingly
- [ ] I have added tests to cover my changes
```

---

## Troubleshooting

### 20. How do you troubleshoot common Bitbucket issues?

**Answer:**
Common troubleshooting approaches:

**Pipeline Issues:**
```bash
# Check pipeline logs
# View step details in Bitbucket UI
# Validate YAML syntax
yamllint bitbucket-pipelines.yml

# Test locally with Docker
docker run -it --rm node:14 /bin/bash
npm install
npm test
```

**Git Issues:**
```bash
# Authentication problems
git config --global credential.helper store
git remote set-url origin https://username@bitbucket.org/workspace/repo.git

# Large file issues
git lfs track "*.zip"
git add .gitattributes
git add large-file.zip
git commit -m "Add large file with LFS"
```

**Performance Issues:**
- Monitor repository size
- Clean up old branches
- Optimize pipeline caching
- Review database performance

**Common Error Solutions:**
- **Permission Denied**: Check user access and SSH keys
- **Pipeline Timeout**: Increase timeout or optimize scripts
- **Out of Memory**: Adjust Docker memory limits
- **Build Failures**: Check dependencies and environment

### 21. How do you implement Bitbucket Pipelines for data engineering workflows?
**Answer**: Data engineering pipelines require specialized configurations for ETL processes, data validation, and deployment.

```yaml
# bitbucket-pipelines.yml for data engineering
image: python:3.9

definitions:
  services:
    postgres:
      image: postgres:13
      environment:
        POSTGRES_DB: testdb
        POSTGRES_USER: testuser
        POSTGRES_PASSWORD: testpass
    redis:
      image: redis:6-alpine
  
  caches:
    pip: ~/.cache/pip
    spark: ~/.cache/spark

pipelines:
  default:
    - step:
        name: Data Quality Validation
        caches:
          - pip
        script:
          - pip install great-expectations pandas sqlalchemy
          - python scripts/validate_data_schema.py
          - great_expectations checkpoint run data_quality_checkpoint
        artifacts:
          - validation_results/**
        services:
          - postgres
```

This comprehensive set of interview questions covers all major aspects of Bitbucket, from basic repository management to advanced administration and troubleshooting scenarios that data engineers would encounter.