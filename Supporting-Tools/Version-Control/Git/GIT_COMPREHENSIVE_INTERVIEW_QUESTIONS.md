# Git - Comprehensive Interview Questions & Answers for Data Engineers

## 📋 Table of Contents
1. [Basic Git Concepts](#basic-git-concepts)
2. [Repository Management](#repository-management)
3. [Branching & Merging](#branching--merging)
4. [Advanced Git Operations](#advanced-git-operations)
5. [Collaboration & Remote Repositories](#collaboration--remote-repositories)
6. [Git Workflows](#git-workflows)
7. [Data Engineering Specific](#data-engineering-specific)
8. [Troubleshooting & Recovery](#troubleshooting--recovery)
9. [Git Hooks & Automation](#git-hooks--automation)
10. [Best Practices & Security](#best-practices--security)

---

## Basic Git Concepts

### 1. What is Git and how does it differ from other version control systems?

**Answer:**
Git is a distributed version control system that tracks changes in files and coordinates work among multiple developers.

**Key Differences:**
- **Distributed**: Every clone is a full backup of the repository
- **Branching**: Lightweight and fast branching operations
- **Performance**: Optimized for speed and efficiency
- **Data Integrity**: Uses SHA-1 hashing for data verification
- **Staging Area**: Three-tree architecture (working directory, staging area, repository)

**Git vs Other VCS:**
```bash
# Git (Distributed)
git clone https://github.com/user/repo.git  # Full repository copy
git log --oneline                           # Local history access
git branch feature-branch                   # Instant branch creation

# SVN (Centralized) - for comparison
svn checkout http://server/repo/trunk       # Working copy only
svn log                                     # Requires server connection
svn copy trunk branches/feature             # Server operation
```

### 2. Explain Git's three-tree architecture.

**Answer:**
Git uses a three-tree architecture to manage file states:

**1. Working Directory:**
- Your actual files and folders
- Where you make changes

**2. Staging Area (Index):**
- Intermediate area between working directory and repository
- Prepares changes for commit

**3. Repository (.git directory):**
- Contains all project history and metadata
- Where commits are stored

```bash
# Workflow demonstration
echo "Hello World" > file.txt        # Working Directory
git add file.txt                     # Move to Staging Area
git commit -m "Add hello world"      # Move to Repository

# Check status at each stage
git status                           # Shows working directory and staging area
git log --oneline                    # Shows repository history
```

### 3. What are the different states of files in Git?

**Answer:**
Files in Git can be in four different states:

**File States:**
1. **Untracked**: New files not yet added to Git
2. **Tracked**: Files that Git knows about
   - **Unmodified**: No changes since last commit
   - **Modified**: Changed but not staged
   - **Staged**: Changes ready for commit

```bash
# File state transitions
touch new_file.txt                   # Untracked
git add new_file.txt                 # Staged
git commit -m "Add new file"         # Unmodified

echo "changes" >> new_file.txt       # Modified
git add new_file.txt                 # Staged
git commit -m "Update file"          # Unmodified

# Check file states
git status                           # Shows current state
git status --porcelain              # Machine-readable format
```

### 4. Explain the difference between `git add`, `git commit`, and `git push`.

**Answer:**

**git add:**
- Stages changes for commit
- Moves files from working directory to staging area
- Prepares snapshot of changes

**git commit:**
- Creates a snapshot of staged changes
- Saves changes to local repository
- Generates unique commit hash

**git push:**
- Uploads local commits to remote repository
- Synchronizes local and remote repositories
- Makes changes available to other developers

```bash
# Complete workflow
echo "Data pipeline code" > pipeline.py    # Working Directory
git add pipeline.py                         # Staging Area
git commit -m "Add data pipeline"           # Local Repository
git push origin main                        # Remote Repository

# Batch operations
git add .                                   # Stage all changes
git commit -am "Quick commit"               # Stage and commit tracked files
git push                                    # Push to default remote/branch
```

---

## Repository Management

### 5. How do you initialize and configure a new Git repository?

**Answer:**

**Initialize Repository:**
```bash
# Create new repository
mkdir data-engineering-project
cd data-engineering-project
git init

# Or clone existing repository
git clone https://github.com/user/data-project.git
cd data-project
```

**Configure Repository:**
```bash
# Global configuration (applies to all repositories)
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
git config --global init.defaultBranch main

# Repository-specific configuration
git config user.name "Data Engineer"
git config user.email "dataeng@company.com"

# Useful configurations for data engineering
git config --global core.autocrlf input        # Handle line endings
git config --global core.editor "code --wait"  # Set VS Code as editor
git config --global pull.rebase false          # Merge strategy for pulls
git config --global push.default simple        # Push current branch only

# View configuration
git config --list
git config --global --list
```

### 6. How do you handle large files in Git repositories?

**Answer:**

**Problem with Large Files:**
- Git stores complete file history
- Large files slow down operations
- Repository size grows quickly

**Solutions:**

**1. Git LFS (Large File Storage):**
```bash
# Install and initialize Git LFS
git lfs install

# Track large file types
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "*.pkl"
git lfs track "data/**"

# Add .gitattributes file
git add .gitattributes
git commit -m "Configure Git LFS"

# Add large files normally
git add large_dataset.csv
git commit -m "Add large dataset"
git push origin main
```

**2. .gitignore for Data Files:**
```bash
# .gitignore for data engineering projects
# Data files
*.csv
*.json
*.parquet
*.avro
*.orc
data/
datasets/
*.db
*.sqlite

# Model files
*.pkl
*.joblib
*.h5
models/

# Logs and outputs
logs/
outputs/
*.log

# Environment files
.env
.env.local
venv/
.venv/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db
```

**3. Alternative Approaches:**
```bash
# Use symbolic links for large files
ln -s /shared/data/large_dataset.csv data/
git add data/large_dataset.csv  # Only adds the link

# Store data externally and reference in code
# config.py
DATA_PATH = os.environ.get('DATA_PATH', '/default/data/path')
```

### 7. How do you manage sensitive information in Git repositories?

**Answer:**

**Never Commit Sensitive Data:**
```bash
# .gitignore sensitive files
# Credentials
*.key
*.pem
*.p12
.env
.env.*
secrets/
credentials/

# Configuration files with secrets
config/production.yml
database.conf
```

**Use Environment Variables:**
```python
# config.py - Good practice
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
API_KEY = os.environ.get('API_KEY')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')

# .env file (not committed)
DATABASE_URL=postgresql://user:pass@localhost:5432/db
API_KEY=your-secret-api-key
AWS_ACCESS_KEY_ID=your-access-key
```

**Git-crypt for Encrypted Files:**
```bash
# Install git-crypt
git-crypt init

# Add users
git-crypt add-gpg-user user@company.com

# Configure .gitattributes
echo "secrets/** filter=git-crypt diff=git-crypt" >> .gitattributes
echo ".env filter=git-crypt diff=git-crypt" >> .gitattributes

# Files are automatically encrypted on commit
git add secrets/production.env
git commit -m "Add encrypted production config"
```

**Remove Sensitive Data from History:**
```bash
# Remove file from all history (dangerous!)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch secrets.txt' \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner (faster)
java -jar bfg.jar --delete-files secrets.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

## Branching & Merging

### 8. Explain Git branching and common branching strategies.

**Answer:**

**Git Branching Basics:**
```bash
# Create and switch to new branch
git branch feature/data-pipeline
git checkout feature/data-pipeline

# Or create and switch in one command
git checkout -b feature/data-pipeline

# Modern syntax (Git 2.23+)
git switch -c feature/data-pipeline

# List branches
git branch                    # Local branches
git branch -r                 # Remote branches
git branch -a                 # All branches
```

**Common Branching Strategies:**

**1. Git Flow:**
```bash
# Main branches
main        # Production-ready code
develop     # Integration branch

# Supporting branches
feature/    # New features
release/    # Release preparation
hotfix/     # Production fixes

# Example workflow
git checkout develop
git checkout -b feature/etl-pipeline
# ... work on feature ...
git checkout develop
git merge feature/etl-pipeline
git branch -d feature/etl-pipeline
```

**2. GitHub Flow (Simplified):**
```bash
# Simple workflow
main        # Always deployable
feature/    # Feature branches

# Example
git checkout main
git pull origin main
git checkout -b feature/data-validation
# ... work on feature ...
git push origin feature/data-validation
# Create pull request
# Merge to main after review
```

**3. GitLab Flow:**
```bash
# Environment branches
main            # Development
pre-production  # Staging
production      # Production

# Feature workflow
git checkout main
git checkout -b feature/monitoring
# ... work ...
git push origin feature/monitoring
# Merge to main → pre-production → production
```

### 9. How do you resolve merge conflicts?

**Answer:**

**Understanding Merge Conflicts:**
```bash
# Scenario: Two developers modify the same file
# Developer A
git checkout main
git checkout -b feature/config-update
echo "database_host = prod-db" >> config.py
git add config.py
git commit -m "Update database host"

# Developer B (simultaneously)
git checkout main
git checkout -b feature/config-change
echo "database_host = new-db" >> config.py
git add config.py
git commit -m "Change database host"
```

**Resolving Conflicts:**
```bash
# Merge attempt causes conflict
git checkout main
git merge feature/config-update    # Success
git merge feature/config-change    # Conflict!

# Git shows conflict markers
cat config.py
# <<<<<<< HEAD
# database_host = prod-db
# =======
# database_host = new-db
# >>>>>>> feature/config-change

# Manual resolution
# Edit file to resolve conflict
echo "database_host = final-db" > config.py

# Mark as resolved
git add config.py
git commit -m "Resolve database host conflict"
```

**Merge Tools:**
```bash
# Configure merge tool
git config --global merge.tool vimdiff
git config --global merge.tool vscode

# Use merge tool
git mergetool

# Abort merge if needed
git merge --abort
```

**Advanced Conflict Resolution:**
```bash
# Show conflict details
git status
git diff

# Choose specific version
git checkout --ours config.py      # Keep current branch version
git checkout --theirs config.py    # Keep merging branch version

# Interactive rebase for complex conflicts
git rebase -i HEAD~3
```

### 10. What's the difference between merge, rebase, and squash?

**Answer:**

**Merge:**
- Creates a merge commit
- Preserves branch history
- Non-destructive operation

```bash
git checkout main
git merge feature/data-pipeline
# Creates merge commit with two parents
```

**Rebase:**
- Replays commits on top of another branch
- Creates linear history
- Rewrites commit history

```bash
git checkout feature/data-pipeline
git rebase main
# Moves feature commits to tip of main
```

**Squash:**
- Combines multiple commits into one
- Cleans up commit history
- Useful for feature branches

```bash
# Interactive squash
git rebase -i HEAD~3
# Change 'pick' to 'squash' for commits to combine

# Squash merge
git merge --squash feature/data-pipeline
git commit -m "Add complete data pipeline feature"
```

**When to Use Each:**

| Operation | Use Case | Pros | Cons |
|-----------|----------|------|------|
| **Merge** | Preserving context | Complete history | Cluttered history |
| **Rebase** | Clean linear history | Simple timeline | Rewrites history |
| **Squash** | Feature completion | Clean commits | Loses detailed history |

**Data Engineering Example:**
```bash
# Feature branch with multiple commits
git log --oneline feature/etl-pipeline
# a1b2c3d Fix data validation
# e4f5g6h Add error handling  
# i7j8k9l Initial ETL implementation

# Option 1: Merge (preserve all commits)
git checkout main
git merge feature/etl-pipeline

# Option 2: Squash (single clean commit)
git merge --squash feature/etl-pipeline
git commit -m "Implement ETL pipeline with validation and error handling"

# Option 3: Rebase (clean up then merge)
git checkout feature/etl-pipeline
git rebase -i main  # Clean up commits
git checkout main
git merge feature/etl-pipeline  # Fast-forward merge
```

---

## Advanced Git Operations

### 11. How do you use `git stash` effectively?

**Answer:**

**Basic Stashing:**
```bash
# Stash current changes
git stash
git stash push -m "Work in progress on data validation"

# List stashes
git stash list
# stash@{0}: On main: Work in progress on data validation
# stash@{1}: WIP on feature: Quick fix

# Apply stash
git stash apply              # Apply most recent stash
git stash apply stash@{1}    # Apply specific stash
git stash pop               # Apply and remove stash
```

**Advanced Stashing:**
```bash
# Stash specific files
git stash push -m "Config changes" config.py database.yml

# Stash untracked files
git stash -u                # Include untracked files
git stash -a                # Include all files (even ignored)

# Partial stashing
git stash -p                # Interactive stashing

# Create branch from stash
git stash branch feature/temp-work stash@{0}
```

**Data Engineering Use Cases:**
```bash
# Scenario: Working on data pipeline, need to fix urgent bug
echo "# TODO: Add data validation" >> pipeline.py
git stash push -m "Pipeline validation work"

# Fix urgent issue
git checkout hotfix/data-bug
# ... fix bug ...
git commit -m "Fix data processing bug"

# Return to original work
git checkout main
git stash pop
# Continue working on validation
```

### 12. How do you rewrite Git history safely?

**Answer:**

**Interactive Rebase:**
```bash
# Rewrite last 3 commits
git rebase -i HEAD~3

# Options in interactive mode:
# pick    = use commit
# reword  = use commit, but edit message
# edit    = use commit, but stop for amending
# squash  = use commit, but meld into previous commit
# fixup   = like squash, but discard commit message
# drop    = remove commit
```

**Common History Rewriting Tasks:**

**1. Fix Commit Messages:**
```bash
# Change last commit message
git commit --amend -m "Correct commit message"

# Change older commit messages
git rebase -i HEAD~3
# Change 'pick' to 'reword' for commits to modify
```

**2. Combine Commits:**
```bash
# Example: Multiple small commits for one feature
git log --oneline
# a1b2c3d Fix typo in pipeline
# e4f5g6h Add error handling
# i7j8k9l Add data validation
# m0n1o2p Initial pipeline implementation

git rebase -i HEAD~4
# Change to:
# pick m0n1o2p Initial pipeline implementation
# squash i7j8k9l Add data validation
# squash e4f5g6h Add error handling
# squash a1b2c3d Fix typo in pipeline
```

**3. Split Commits:**
```bash
git rebase -i HEAD~2
# Change 'pick' to 'edit' for commit to split
# When rebase stops:
git reset HEAD^
git add file1.py
git commit -m "Add data validation"
git add file2.py
git commit -m "Add error handling"
git rebase --continue
```

**Safety Guidelines:**
```bash
# NEVER rewrite public history (pushed commits)
# Create backup branch before rewriting
git branch backup-branch

# Only rewrite local commits
git log --oneline origin/main..HEAD  # Show unpushed commits

# Force push carefully (only to feature branches)
git push --force-with-lease origin feature/data-pipeline
```

### 13. How do you use `git bisect` for debugging?

**Answer:**

**Git Bisect for Bug Hunting:**
```bash
# Start bisect session
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good v1.2.0

# Git checks out middle commit
# Test the commit
python test_data_pipeline.py

# Mark result
git bisect good    # If test passes
git bisect bad     # If test fails

# Continue until bug is found
# Git will show the first bad commit

# End bisect session
git bisect reset
```

**Automated Bisect:**
```bash
# Create test script
cat > test_script.sh << 'EOF'
#!/bin/bash
python -m pytest tests/test_data_validation.py
exit $?
EOF

chmod +x test_script.sh

# Run automated bisect
git bisect start HEAD v1.0.0
git bisect run ./test_script.sh
```

**Data Engineering Example:**
```bash
# Scenario: Data pipeline worked in v1.0 but broken in current version
git bisect start
git bisect bad                    # Current version is broken
git bisect good v1.0.0           # v1.0.0 worked

# Git checks out middle commit
# Test data pipeline
python run_pipeline.py --test-mode

# If pipeline works:
git bisect good
# If pipeline fails:
git bisect bad

# Continue until exact commit is found
# Result: "commit abc123 introduced the bug"
```

---

## Collaboration & Remote Repositories

### 14. How do you manage multiple remotes in Git?

**Answer:**

**Working with Multiple Remotes:**
```bash
# Add multiple remotes
git remote add origin https://github.com/company/data-pipeline.git
git remote add upstream https://github.com/original/data-pipeline.git
git remote add fork https://github.com/myusername/data-pipeline.git

# List remotes
git remote -v
# origin    https://github.com/company/data-pipeline.git (fetch)
# origin    https://github.com/company/data-pipeline.git (push)
# upstream  https://github.com/original/data-pipeline.git (fetch)
# upstream  https://github.com/original/data-pipeline.git (push)

# Fetch from specific remote
git fetch upstream
git fetch origin

# Push to specific remote
git push origin feature/new-pipeline
git push fork feature/new-pipeline
```

**Fork Workflow:**
```bash
# 1. Fork repository on GitHub
# 2. Clone your fork
git clone https://github.com/yourusername/data-pipeline.git
cd data-pipeline

# 3. Add upstream remote
git remote add upstream https://github.com/original/data-pipeline.git

# 4. Keep fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 5. Create feature branch
git checkout -b feature/data-validation
# ... work on feature ...
git push origin feature/data-validation

# 6. Create pull request from your fork to upstream
```

**Enterprise Workflow:**
```bash
# Multiple environments
git remote add dev https://git.company.com/data-team/pipeline-dev.git
git remote add staging https://git.company.com/data-team/pipeline-staging.git
git remote add prod https://git.company.com/data-team/pipeline-prod.git

# Deploy to different environments
git push dev feature/new-feature      # Development
git push staging release/v1.2.0       # Staging
git push prod main                     # Production
```

### 15. How do you handle large team collaboration?

**Answer:**

**Branch Protection Rules:**
```bash
# Configure branch protection (via GitHub/GitLab UI or API)
# - Require pull request reviews
# - Require status checks to pass
# - Require branches to be up to date
# - Restrict pushes to main branch
```

**Code Review Process:**
```bash
# 1. Create feature branch
git checkout -b feature/data-quality-checks

# 2. Work on feature with atomic commits
git commit -m "Add data schema validation"
git commit -m "Add data completeness checks"
git commit -m "Add data freshness validation"

# 3. Push and create pull request
git push origin feature/data-quality-checks

# 4. Address review feedback
git commit -m "Address review comments"
git push origin feature/data-quality-checks

# 5. Squash merge after approval
```

**Conventional Commits:**
```bash
# Use conventional commit format
git commit -m "feat: add real-time data validation"
git commit -m "fix: resolve memory leak in data processor"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for data pipeline"
git commit -m "refactor: optimize data transformation logic"

# Types: feat, fix, docs, style, refactor, test, chore
```

**Team Workflow Example:**
```bash
# .gitmessage template
cat > .gitmessage << 'EOF'
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>

# Type: feat, fix, docs, style, refactor, test, chore
# Scope: component affected (pipeline, api, database)
# Subject: imperative, present tense, no period
# Body: explain what and why vs. how
# Footer: breaking changes, issue references
EOF

git config commit.template .gitmessage
```

---

## Git Workflows

### 16. Compare different Git workflows for data engineering teams.

**Answer:**

**1. Centralized Workflow:**
```bash
# Simple workflow for small teams
git clone https://github.com/company/data-pipeline.git
# Work directly on main branch
git add .
git commit -m "Update data transformation"
git pull origin main  # Get latest changes
git push origin main
```

**2. Feature Branch Workflow:**
```bash
# Each feature gets its own branch
git checkout main
git pull origin main
git checkout -b feature/add-data-validation

# Work on feature
git add data_validation.py
git commit -m "Add data validation module"
git push origin feature/add-data-validation

# Create pull request
# Merge after review
git checkout main
git pull origin main
git branch -d feature/add-data-validation
```

**3. Gitflow Workflow:**
```bash
# Initialize gitflow
git flow init

# Start new feature
git flow feature start data-pipeline-v2
# Work on feature...
git flow feature finish data-pipeline-v2

# Start release
git flow release start 1.2.0
# Prepare release...
git flow release finish 1.2.0

# Hotfix
git flow hotfix start critical-bug
# Fix bug...
git flow hotfix finish critical-bug
```

**4. Forking Workflow:**
```bash
# Fork repository
# Clone your fork
git clone https://github.com/yourusername/data-pipeline.git

# Add upstream
git remote add upstream https://github.com/company/data-pipeline.git

# Create feature branch
git checkout -b feature/new-algorithm

# Work and push to your fork
git push origin feature/new-algorithm

# Create pull request to upstream
```

**Data Engineering Team Recommendations:**

| Team Size | Workflow | Rationale |
|-----------|----------|-----------|
| 1-3 developers | Feature Branch | Simple, flexible |
| 4-10 developers | GitHub Flow | Continuous deployment |
| 10+ developers | Gitflow | Structured releases |
| Open source | Forking | External contributions |

### 17. How do you implement CI/CD with Git hooks?

**Answer:**

**Pre-commit Hooks:**
```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running pre-commit checks..."

# Check Python syntax
python -m py_compile *.py
if [ $? -ne 0 ]; then
    echo "Python syntax errors found!"
    exit 1
fi

# Run linting
flake8 --max-line-length=88 *.py
if [ $? -ne 0 ]; then
    echo "Linting errors found!"
    exit 1
fi

# Run tests
python -m pytest tests/
if [ $? -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi

echo "All pre-commit checks passed!"
```

**Pre-push Hook:**
```bash
# .git/hooks/pre-push
#!/bin/bash

protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ $protected_branch = $current_branch ]; then
    echo "Direct push to main branch is not allowed!"
    echo "Please create a feature branch and submit a pull request."
    exit 1
fi

# Run integration tests before push
echo "Running integration tests..."
python -m pytest tests/integration/
if [ $? -ne 0 ]; then
    echo "Integration tests failed!"
    exit 1
fi
```

**Post-receive Hook (Server-side):**
```bash
# hooks/post-receive (on Git server)
#!/bin/bash

while read oldrev newrev refname; do
    branch=$(git rev-parse --symbolic --abbrev-ref $refname)
    
    if [ "main" = "$branch" ]; then
        echo "Deploying to production..."
        
        # Deploy to production server
        ssh production-server "cd /app && git pull origin main"
        
        # Run database migrations
        ssh production-server "cd /app && python manage.py migrate"
        
        # Restart services
        ssh production-server "sudo systemctl restart data-pipeline"
        
        echo "Deployment completed!"
    fi
done
```

**Using pre-commit Framework:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
```

```bash
# Install and setup pre-commit
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

---

## Data Engineering Specific

### 18. How do you version control data science notebooks and data pipelines?

**Answer:**

**Jupyter Notebook Versioning:**
```bash
# Problem: Notebooks contain output and metadata
# Solution 1: Clean notebooks before committing

# Install nbstripout
pip install nbstripout

# Configure git filter
nbstripout --install

# Or manually clean
jupyter nbconvert --clear-output --inplace notebook.ipynb
git add notebook.ipynb
git commit -m "Add data analysis notebook"
```

**Better Approach - Convert to Scripts:**
```bash
# Convert notebook to Python script
jupyter nbconvert --to script analysis.ipynb

# Version control the script instead
git add analysis.py
git commit -m "Add data analysis script"

# Use jupytext for bidirectional sync
pip install jupytext
jupytext --set-formats ipynb,py:percent analysis.ipynb
```

**Data Pipeline Versioning:**
```python
# pipeline_config.py
PIPELINE_VERSION = "1.2.0"
DATA_SCHEMA_VERSION = "2.1.0"

# Version configuration files
# config/v1.2.0/
#   ├── pipeline.yaml
#   ├── schema.json
#   └── transformations.sql

# Version SQL transformations
# sql/
#   ├── v1.0/
#   │   ├── extract.sql
#   │   └── transform.sql
#   └── v1.1/
#       ├── extract.sql
#       └── transform.sql
```

**Data Schema Evolution:**
```bash
# Track schema changes
mkdir schemas
echo '{"version": "1.0", "fields": [...]}' > schemas/v1.0.json
git add schemas/v1.0.json
git commit -m "Add initial data schema v1.0"

# Schema migration
echo '{"version": "1.1", "fields": [...]}' > schemas/v1.1.json
git add schemas/v1.1.json
git commit -m "Update schema v1.1 - add customer_segment field"
```

### 19. How do you manage configuration files and environment-specific settings?

**Answer:**

**Environment-Specific Configuration:**
```bash
# Directory structure
config/
├── base.yaml           # Common configuration
├── development.yaml    # Development overrides
├── staging.yaml        # Staging overrides
├── production.yaml     # Production overrides
└── local.yaml.example  # Template for local config
```

**Configuration Files:**
```yaml
# config/base.yaml
database:
  host: localhost
  port: 5432
  name: data_warehouse

spark:
  app_name: "Data Pipeline"
  master: "local[*]"
  
logging:
  level: INFO
```

```yaml
# config/production.yaml
database:
  host: prod-db.company.com
  port: 5432
  
spark:
  master: "yarn"
  executor_memory: "4g"
  
logging:
  level: WARNING
```

**Git Configuration:**
```bash
# .gitignore
config/local.yaml
config/secrets.yaml
.env
.env.local

# Track template files
git add config/local.yaml.example
git commit -m "Add local configuration template"
```

**Environment Loading:**
```python
# config_loader.py
import os
import yaml
from pathlib import Path

def load_config(env='development'):
    config_dir = Path('config')
    
    # Load base configuration
    with open(config_dir / 'base.yaml') as f:
        config = yaml.safe_load(f)
    
    # Load environment-specific overrides
    env_file = config_dir / f'{env}.yaml'
    if env_file.exists():
        with open(env_file) as f:
            env_config = yaml.safe_load(f)
            config.update(env_config)
    
    # Override with environment variables
    if 'DATABASE_HOST' in os.environ:
        config['database']['host'] = os.environ['DATABASE_HOST']
    
    return config

# Usage
env = os.environ.get('ENVIRONMENT', 'development')
config = load_config(env)
```

### 20. How do you handle data lineage and pipeline versioning?

**Answer:**

**Data Lineage Tracking:**
```python
# data_lineage.py
import json
from datetime import datetime
from pathlib import Path

class DataLineageTracker:
    def __init__(self, pipeline_version, git_commit):
        self.pipeline_version = pipeline_version
        self.git_commit = git_commit
        self.lineage = {
            'pipeline_version': pipeline_version,
            'git_commit': git_commit,
            'timestamp': datetime.utcnow().isoformat(),
            'inputs': [],
            'outputs': [],
            'transformations': []
        }
    
    def add_input(self, source, schema_version=None):
        self.lineage['inputs'].append({
            'source': source,
            'schema_version': schema_version,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def add_transformation(self, name, version, parameters=None):
        self.lineage['transformations'].append({
            'name': name,
            'version': version,
            'parameters': parameters or {}
        })
    
    def add_output(self, destination, schema_version=None):
        self.lineage['outputs'].append({
            'destination': destination,
            'schema_version': schema_version,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def save_lineage(self, output_path):
        with open(output_path, 'w') as f:
            json.dump(self.lineage, f, indent=2)

# Usage in pipeline
def run_pipeline():
    # Get Git information
    git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    
    # Initialize lineage tracker
    tracker = DataLineageTracker('1.2.0', git_commit)
    
    # Track inputs
    tracker.add_input('s3://raw-data/customers.csv', 'v1.1')
    tracker.add_input('s3://raw-data/orders.csv', 'v1.0')
    
    # Track transformations
    tracker.add_transformation('data_cleaning', '1.0', {'null_threshold': 0.1})
    tracker.add_transformation('feature_engineering', '2.1', {'encoding': 'one_hot'})
    
    # Track outputs
    tracker.add_output('s3://processed-data/customer_features.parquet', 'v2.0')
    
    # Save lineage
    tracker.save_lineage(f'lineage/run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
```

**Pipeline Versioning Strategy:**
```bash
# Tag releases
git tag -a v1.2.0 -m "Release v1.2.0 - Add customer segmentation"
git push origin v1.2.0

# Branch for major versions
git checkout -b pipeline-v2
# ... major changes ...
git tag -a v2.0.0 -m "Release v2.0.0 - New architecture"

# Semantic versioning for data pipelines
# MAJOR.MINOR.PATCH
# MAJOR: Breaking changes to output schema
# MINOR: New features, backward compatible
# PATCH: Bug fixes, no schema changes
```

---

## Troubleshooting & Recovery

### 21. How do you recover from common Git mistakes?

**Answer:**

**Undo Last Commit (Not Pushed):**
```bash
# Undo commit, keep changes staged
git reset --soft HEAD~1

# Undo commit, keep changes in working directory
git reset HEAD~1

# Undo commit, discard all changes (dangerous!)
git reset --hard HEAD~1
```

**Recover Deleted Branch:**
```bash
# Find deleted branch commit
git reflog
# a1b2c3d HEAD@{0}: checkout: moving from feature/data-pipeline to main
# e4f5g6h HEAD@{1}: commit: Add data validation

# Recreate branch
git checkout -b feature/data-pipeline e4f5g6h
```

**Undo Pushed Commits:**
```bash
# Create revert commit (safe for shared repositories)
git revert HEAD
git revert HEAD~2..HEAD  # Revert range of commits

# Force push (dangerous, only for feature branches)
git reset --hard HEAD~1
git push --force-with-lease origin feature/branch
```

**Recover Lost Work:**
```bash
# Find lost commits
git reflog --all
git fsck --lost-found

# Recover specific commit
git show <commit-hash>
git cherry-pick <commit-hash>

# Recover deleted file
git checkout HEAD~1 -- deleted_file.py
```

**Fix Merge Conflicts:**
```bash
# Abort merge
git merge --abort

# Reset to before merge
git reset --hard HEAD~1

# Use specific strategy
git merge -X ours feature/branch    # Prefer current branch
git merge -X theirs feature/branch  # Prefer merging branch
```

### 22. How do you clean up repository history and optimize performance?

**Answer:**

**Clean Up Local Repository:**
```bash
# Remove untracked files
git clean -f        # Remove files
git clean -fd       # Remove files and directories
git clean -fX       # Remove only ignored files

# Prune remote tracking branches
git remote prune origin
git fetch --prune

# Delete merged branches
git branch --merged main | grep -v main | xargs -n 1 git branch -d
```

**Optimize Repository:**
```bash
# Garbage collection
git gc --aggressive --prune=now

# Repack repository
git repack -ad

# Check repository size
git count-objects -vH

# Find large files
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort --numeric-sort --key=2 | \
  tail -10
```

**Remove Large Files from History:**
```bash
# Using git filter-branch (slow)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch large_file.csv' \
  --prune-empty --tag-name-filter cat -- --all

# Using BFG Repo-Cleaner (fast)
java -jar bfg.jar --strip-blobs-bigger-than 100M
java -jar bfg.jar --delete-files "*.{csv,json,parquet}"

# Clean up after BFG
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**Repository Maintenance Script:**
```bash
#!/bin/bash
# git-maintenance.sh

echo "Starting Git repository maintenance..."

# Clean untracked files
git clean -fd

# Prune remote branches
git remote prune origin

# Delete merged branches
git branch --merged main | grep -v main | xargs -n 1 git branch -d

# Garbage collection
git gc --aggressive

# Show repository statistics
echo "Repository size after cleanup:"
git count-objects -vH

echo "Maintenance completed!"
```

---

## Best Practices & Security

### 23. What are Git security best practices for data engineering teams?

**Answer:**

**Commit Signing:**
```bash
# Generate GPG key
gpg --gen-key

# Configure Git to use GPG key
git config --global user.signingkey <key-id>
git config --global commit.gpgsign true

# Sign commits
git commit -S -m "Add secure data processing module"

# Verify signatures
git log --show-signature
```

**Access Control:**
```bash
# SSH key authentication
ssh-keygen -t ed25519 -C "your.email@company.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Configure SSH for different hosts
# ~/.ssh/config
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work

Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
```

**Secure Configuration:**
```bash
# Disable HTTP, enforce HTTPS
git config --global http.sslVerify true
git config --global url."https://github.com/".insteadOf "git://github.com/"

# Configure credential helper
git config --global credential.helper store
git config --global credential.helper 'cache --timeout=3600'

# Audit configuration
git config --list --show-origin
```

**Repository Security:**
```bash
# .gitignore security patterns
# Credentials
*.key
*.pem
*.p12
.env*
secrets/
credentials/

# Database files
*.db
*.sqlite
*.sqlite3

# Configuration files
config/production.yml
database.conf

# IDE and OS files
.vscode/settings.json
.idea/
.DS_Store
```

**Pre-commit Security Checks:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/gitguardian/ggshield
    rev: v1.18.0
    hooks:
      - id: ggshield
        language: python
        stages: [commit]
```

### 24. How do you implement Git best practices for data engineering projects?

**Answer:**

**Repository Structure:**
```
data-engineering-project/
├── .github/
│   ├── workflows/          # CI/CD workflows
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE.md
├── config/
│   ├── base.yaml
│   ├── development.yaml
│   └── production.yaml
├── data/
│   ├── raw/               # Raw data (not committed)
│   ├── processed/         # Processed data (not committed)
│   └── schemas/           # Data schemas (committed)
├── notebooks/
│   ├── exploratory/       # EDA notebooks
│   └── analysis/          # Analysis notebooks
├── src/
│   ├── pipelines/         # Data pipelines
│   ├── transformations/   # Data transformations
│   └── utils/             # Utility functions
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test data
├── docs/
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── architecture.md
├── .gitignore
├── .pre-commit-config.yaml
├── requirements.txt
└── setup.py
```

**Commit Message Standards:**
```bash
# Use conventional commits
git commit -m "feat(pipeline): add real-time data validation"
git commit -m "fix(transform): resolve null value handling"
git commit -m "docs(api): update transformation documentation"
git commit -m "test(pipeline): add integration tests"

# Include issue references
git commit -m "fix(etl): resolve memory leak in data processor

Fixes memory leak that occurred during large dataset processing.
Added proper resource cleanup and memory monitoring.

Closes #123"
```

**Branch Naming Conventions:**
```bash
# Feature branches
feature/add-data-validation
feature/implement-streaming-pipeline
feature/optimize-transformations

# Bug fix branches
fix/memory-leak-in-processor
fix/incorrect-date-parsing
hotfix/critical-data-corruption

# Release branches
release/v1.2.0
release/v2.0.0-beta

# Maintenance branches
maintenance/update-dependencies
maintenance/security-patches
```

**Code Review Checklist:**
```markdown
## Data Engineering Code Review Checklist

### Code Quality
- [ ] Code follows team style guidelines
- [ ] Functions are well-documented
- [ ] Error handling is implemented
- [ ] Logging is appropriate

### Data Engineering Specific
- [ ] Data validation is implemented
- [ ] Schema evolution is handled
- [ ] Resource cleanup is proper
- [ ] Performance considerations addressed

### Testing
- [ ] Unit tests are included
- [ ] Integration tests cover main flows
- [ ] Test data is appropriate
- [ ] Edge cases are tested

### Security
- [ ] No credentials in code
- [ ] Sensitive data is handled properly
- [ ] Access controls are appropriate
- [ ] Data privacy requirements met

### Documentation
- [ ] README is updated
- [ ] API documentation is current
- [ ] Configuration changes documented
- [ ] Migration guide provided (if needed)
```

**Automated Quality Gates:**
```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate

on:
  pull_request:
    branches: [main]

jobs:
  quality-checks:
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
          pip install pytest flake8 black isort
      
      - name: Code formatting
        run: |
          black --check .
          isort --check-only .
      
      - name: Linting
        run: flake8 .
      
      - name: Unit tests
        run: pytest tests/unit/
      
      - name: Integration tests
        run: pytest tests/integration/
      
      - name: Security scan
        uses: gitguardian/ggshield-action@v1
        env:
          GITGUARDIAN_API_KEY: ${{ secrets.GITGUARDIAN_API_KEY }}
```

This comprehensive guide covers all essential Git concepts and practices specifically tailored for data engineering teams, providing practical examples and real-world scenarios that data engineers encounter in their daily work.