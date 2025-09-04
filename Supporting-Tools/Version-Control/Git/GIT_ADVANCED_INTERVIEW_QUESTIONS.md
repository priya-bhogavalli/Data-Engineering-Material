# Git Advanced Interview Questions & Answers

## 📋 Table of Contents
1. [Advanced Git Concepts](#advanced-git-concepts)
2. [Branching Strategies](#branching-strategies)
3. [Merge vs Rebase](#merge-vs-rebase)
4. [Git Workflows](#git-workflows)
5. [Troubleshooting](#troubleshooting)

---

## Advanced Git Concepts

### 1. Explain Git's internal object model and how commits are stored.

**Answer:**
Git uses a content-addressable filesystem with four main object types:

**Object Types:**
```bash
# Blob: File content
git cat-file -t <hash>  # blob
git cat-file -p <hash>  # show content

# Tree: Directory structure
git ls-tree HEAD        # show tree objects

# Commit: Snapshot with metadata
git cat-file -p HEAD    # show commit object

# Tag: Named reference to commit
git show-ref --tags     # list tag references
```

**Internal Structure:**
```
Commit Object:
├── Tree SHA (root directory)
├── Parent commit(s)
├── Author & Committer info
├── Timestamp
└── Commit message

Tree Object:
├── File permissions & type
├── Filename
└── Blob SHA
```

### 2. How do you handle large files and repositories in Git?

**Answer:**
Large files require special handling to maintain repository performance:

**Git LFS (Large File Storage):**
```bash
# Install and configure Git LFS
git lfs install
git lfs track "*.csv"
git lfs track "*.parquet"
git add .gitattributes

# Check LFS files
git lfs ls-files
git lfs status

# Clone with LFS
git lfs clone <repository-url>
```

**Repository Optimization:**
```bash
# Clean up repository
git gc --aggressive --prune=now
git repack -ad

# Remove large files from history
git filter-branch --tree-filter 'rm -f large-file.csv' HEAD
# Or use BFG Repo-Cleaner (faster)
java -jar bfg.jar --delete-files large-file.csv
```

---

## Branching Strategies

### 3. Compare different Git branching strategies for data engineering teams.

**Answer:**
Different strategies suit different team sizes and deployment patterns:

**Git Flow:**
```bash
# Feature development
git checkout -b feature/customer-pipeline develop
git push -u origin feature/customer-pipeline

# Release preparation
git checkout -b release/v1.2.0 develop
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"

# Hotfix
git checkout -b hotfix/critical-bug main
git checkout main
git merge --no-ff hotfix/critical-bug
```

**GitHub Flow (Simplified):**
```bash
# Feature branch from main
git checkout -b feature/data-validation main
# Work and push
git push -u origin feature/data-validation
# Create PR, review, merge to main
```

**Comparison:**
| Strategy | Complexity | Release Cycle | Team Size | Use Case |
|----------|------------|---------------|-----------|----------|
| Git Flow | High | Scheduled | Large | Complex releases |
| GitHub Flow | Low | Continuous | Small-Medium | Continuous deployment |
| GitLab Flow | Medium | Flexible | Medium-Large | Environment promotion |

### 4. How do you implement feature flags with Git branching?

**Answer:**
Feature flags allow deploying code without activating features:

**Implementation:**
```python
# Feature flag configuration
FEATURE_FLAGS = {
    'new_data_pipeline': os.getenv('ENABLE_NEW_PIPELINE', 'false').lower() == 'true',
    'advanced_analytics': os.getenv('ENABLE_ANALYTICS', 'false').lower() == 'true'
}

def process_data():
    if FEATURE_FLAGS['new_data_pipeline']:
        return new_pipeline_process()
    else:
        return legacy_pipeline_process()
```

**Git Workflow:**
```bash
# Develop feature behind flag
git checkout -b feature/new-pipeline main
# Implement with feature flag disabled by default
git commit -m "Add new pipeline behind feature flag"
git push origin feature/new-pipeline

# Merge to main (feature disabled)
git checkout main
git merge feature/new-pipeline

# Enable in production when ready
# Set environment variable: ENABLE_NEW_PIPELINE=true
```

---

## Merge vs Rebase

### 5. When should you use merge vs rebase in data engineering workflows?

**Answer:**
Choice depends on history preservation needs and collaboration patterns:

**Merge (Preserves History):**
```bash
# Feature branch merge
git checkout main
git merge feature/data-pipeline
# Creates merge commit, preserves branch history

# Use for:
# - Shared feature branches
# - Release branches
# - When history context matters
```

**Rebase (Linear History):**
```bash
# Interactive rebase to clean up commits
git rebase -i HEAD~3
# pick, squash, edit, drop commits

# Rebase feature branch
git checkout feature/data-pipeline
git rebase main
git checkout main
git merge feature/data-pipeline  # Fast-forward merge

# Use for:
# - Personal feature branches
# - Cleaning commit history
# - Linear project history
```

**Data Engineering Example:**
```bash
# Pipeline development workflow
git checkout -b feature/customer-etl main

# Multiple commits during development
git commit -m "Add customer data extraction"
git commit -m "Fix data validation bug"
git commit -m "Add error handling"
git commit -m "Update documentation"

# Clean up before merge
git rebase -i HEAD~4
# Squash related commits, improve messages

# Final merge
git checkout main
git merge feature/customer-etl
```

### 6. How do you resolve complex merge conflicts in data engineering projects?

**Answer:**
Systematic approach to conflict resolution:

**Conflict Resolution Process:**
```bash
# Start merge
git merge feature/data-pipeline
# CONFLICT in pipeline_config.py

# Check conflict status
git status
git diff

# Resolve conflicts manually or with tools
git mergetool  # Use configured merge tool
# Or edit files directly

# Common conflict patterns in data engineering:
```

**Configuration Conflicts:**
```python
# pipeline_config.py
<<<<<<< HEAD
DATABASE_URL = "postgresql://prod-server/analytics"
BATCH_SIZE = 1000
=======
DATABASE_URL = "postgresql://staging-server/analytics"  
BATCH_SIZE = 5000
ENABLE_MONITORING = True
>>>>>>> feature/data-pipeline

# Resolution strategy:
DATABASE_URL = "postgresql://prod-server/analytics"  # Keep production
BATCH_SIZE = 5000  # Take improved batch size
ENABLE_MONITORING = True  # Add new feature
```

**Schema Conflicts:**
```sql
-- schema.sql conflict resolution
<<<<<<< HEAD
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255)
);
=======
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
>>>>>>> feature/audit-columns

-- Resolution: Combine both changes
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Git Workflows

### 7. Design a Git workflow for a data engineering team with multiple environments.

**Answer:**
Environment-based workflow with promotion strategy:

**Branch Structure:**
```
main (production)
├── staging
├── develop
└── feature branches
```

**Workflow Implementation:**
```bash
# Development workflow
git checkout -b feature/new-etl develop
# Develop and test locally
git push origin feature/new-etl

# Code review and merge to develop
git checkout develop
git merge feature/new-etl
git push origin develop

# Deploy to development environment
# Automated CI/CD triggers on develop push

# Promote to staging
git checkout staging
git merge develop
git push origin staging
# Automated deployment to staging

# Production release
git checkout main
git merge staging
git tag -a v1.3.0 -m "Release v1.3.0"
git push origin main --tags
# Automated deployment to production
```

**Environment Configuration:**
```yaml
# .github/workflows/deploy.yml
name: Deploy Pipeline
on:
  push:
    branches: [develop, staging, main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Development
        if: github.ref == 'refs/heads/develop'
        run: |
          echo "Deploying to development environment"
          ./deploy.sh dev
          
      - name: Deploy to Staging  
        if: github.ref == 'refs/heads/staging'
        run: |
          echo "Deploying to staging environment"
          ./deploy.sh staging
          
      - name: Deploy to Production
        if: github.ref == 'refs/heads/main'
        run: |
          echo "Deploying to production environment"
          ./deploy.sh prod
```

### 8. How do you implement code review workflows for data engineering teams?

**Answer:**
Structured review process ensures code quality and knowledge sharing:

**Pull Request Template:**
```markdown
## Data Pipeline Change Request

### Summary
Brief description of changes made to the data pipeline.

### Type of Change
- [ ] New data source integration
- [ ] Pipeline optimization
- [ ] Bug fix
- [ ] Configuration change
- [ ] Documentation update

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Data quality validation
- [ ] Performance benchmarks met

### Data Impact
- [ ] No breaking changes to downstream consumers
- [ ] Schema changes documented
- [ ] Data migration plan (if applicable)
- [ ] Rollback plan documented

### Checklist
- [ ] Code follows team standards
- [ ] Documentation updated
- [ ] Monitoring/alerting configured
- [ ] Security review completed (if applicable)

### Reviewers
@data-engineering-team @senior-data-engineer
```

**Review Process:**
```bash
# Create feature branch
git checkout -b feature/customer-segmentation develop

# Make changes and commit
git add .
git commit -m "Implement customer segmentation pipeline

- Add customer data extraction from CRM
- Implement RFM analysis algorithm  
- Add segmentation results to data warehouse
- Configure monitoring and alerting"

# Push and create PR
git push origin feature/customer-segmentation
# Create pull request with template

# Review process:
# 1. Automated checks (CI/CD, tests, linting)
# 2. Peer review (code quality, logic)
# 3. Senior review (architecture, performance)
# 4. Approval and merge
```

---

## Troubleshooting

### 9. How do you recover from common Git disasters in data engineering projects?

**Answer:**
Recovery strategies for different scenarios:

**Accidental Commit to Wrong Branch:**
```bash
# Move commits to correct branch
git log --oneline -5  # Find commit hashes
git checkout correct-branch
git cherry-pick <commit-hash>

# Remove from wrong branch
git checkout wrong-branch
git reset --hard HEAD~1  # Remove last commit
```

**Lost Work Recovery:**
```bash
# Find lost commits
git reflog
git log --all --full-history -- path/to/file

# Recover deleted branch
git reflog
git checkout -b recovered-branch <commit-hash>

# Recover deleted files
git checkout HEAD~1 -- path/to/deleted/file
```

**Repository Corruption:**
```bash
# Check repository integrity
git fsck --full

# Recover from backup
git clone --mirror <backup-url> .git
git config --bool core.bare false
git reset --hard

# Rebuild from remotes
git fetch --all
git reset --hard origin/main
```

### 10. How do you optimize Git performance for large data engineering repositories?

**Answer:**
Performance optimization strategies:

**Repository Optimization:**
```bash
# Garbage collection
git gc --aggressive --prune=now

# Repack objects
git repack -ad

# Clean up unreachable objects
git prune --expire=now

# Check repository size
git count-objects -vH
```

**Clone Optimization:**
```bash
# Shallow clone (recent history only)
git clone --depth 1 <repository-url>

# Partial clone (exclude large files)
git clone --filter=blob:limit=1m <repository-url>

# Sparse checkout (specific directories)
git config core.sparseCheckout true
echo "data-pipelines/*" > .git/info/sparse-checkout
git read-tree -m -u HEAD
```

**Configuration Tuning:**
```bash
# Increase buffer sizes
git config core.preloadindex true
git config core.fscache true
git config gc.auto 256

# Optimize for large repositories
git config feature.manyFiles true
git config index.threads 4
```

---

## Summary

Advanced Git skills for data engineering teams include:

1. **Internal Understanding**: Object model and storage mechanisms
2. **Branching Strategies**: Choosing appropriate workflows for team size and deployment patterns
3. **Merge Strategies**: When to use merge vs rebase for different scenarios
4. **Workflow Design**: Environment promotion and code review processes
5. **Troubleshooting**: Recovery from common Git disasters and performance optimization