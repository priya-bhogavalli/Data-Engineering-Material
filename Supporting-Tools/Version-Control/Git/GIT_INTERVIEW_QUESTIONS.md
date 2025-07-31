# Git Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Git and why is it essential for data engineering?
**Answer**: Git is a distributed version control system that tracks changes in files and coordinates work among multiple developers.

**Key Benefits for Data Engineering**:
- **Code Versioning**: Track changes in ETL scripts, SQL queries, and configurations
- **Collaboration**: Multiple team members working on data pipelines
- **Branching**: Parallel development of features and experiments
- **Rollback**: Revert to previous versions when issues occur
- **Documentation**: Commit messages provide change history

```bash
# Initialize repository
git init data-pipeline-project
cd data-pipeline-project

# Configure user
git config user.name "Data Engineer"
git config user.email "engineer@company.com"

# Add files
echo "# Data Pipeline Project" > README.md
git add README.md
git commit -m "Initial commit: Add README"

# Check status
git status
git log --oneline
```

### 2. Explain the Git workflow and basic commands
**Answer**: Git follows a typical workflow of modify, stage, commit, and push changes.

```bash
# Basic workflow
# 1. Modify files
echo "SELECT * FROM users;" > queries/user_analysis.sql

# 2. Stage changes
git add queries/user_analysis.sql
# Or stage all changes
git add .

# 3. Commit changes
git commit -m "Add user analysis query"

# 4. Push to remote
git push origin main

# Check differences
git diff                    # Working directory vs staging
git diff --staged          # Staging vs last commit
git diff HEAD~1            # Current vs previous commit

# View commit history
git log                    # Full log
git log --oneline         # Compact log
git log --graph           # Visual branch graph
git log --author="John"   # Filter by author

# Undo changes
git checkout -- file.sql  # Discard working directory changes
git reset HEAD file.sql   # Unstage file
git reset --soft HEAD~1   # Undo last commit, keep changes staged
git reset --hard HEAD~1   # Undo last commit, discard changes
```

### 3. How do you work with branches in Git?
**Answer**: Branches allow parallel development and feature isolation.

```bash
# Create and switch to new branch
git checkout -b feature/new-etl-pipeline
# Or using newer syntax
git switch -c feature/new-etl-pipeline

# List branches
git branch                 # Local branches
git branch -r             # Remote branches
git branch -a             # All branches

# Switch branches
git checkout main
git switch main

# Merge branch
git checkout main
git merge feature/new-etl-pipeline

# Delete branch
git branch -d feature/new-etl-pipeline    # Safe delete
git branch -D feature/new-etl-pipeline    # Force delete

# Push branch to remote
git push origin feature/new-etl-pipeline

# Track remote branch
git checkout -b feature/remote-feature origin/feature/remote-feature
```

**Data Engineering Branching Strategy**:
```bash
# Feature branch workflow
git checkout main
git pull origin main
git checkout -b feature/kafka-integration

# Work on feature
echo "kafka_config = {...}" > config/kafka.py
git add config/kafka.py
git commit -m "Add Kafka integration configuration"

# Push feature branch
git push origin feature/kafka-integration

# Create pull request (via GitHub/GitLab UI)
# After review and approval, merge to main
```

### 4. How do you handle merge conflicts?
**Answer**: Merge conflicts occur when Git cannot automatically merge changes. Manual resolution is required.

```bash
# Scenario: Conflict during merge
git checkout main
git merge feature/data-validation

# Git shows conflict
# Auto-merging scripts/validate_data.py
# CONFLICT (content): Merge conflict in scripts/validate_data.py
# Automatic merge failed; fix conflicts and then commit the result.

# Check conflict status
git status

# Edit conflicted file
# <<<<<<< HEAD
# def validate_data(data):
#     return check_schema(data)
# =======
# def validate_data(data):
#     return validate_schema(data) and check_nulls(data)
# >>>>>>> feature/data-validation

# Resolve conflict by editing file
def validate_data(data):
    return validate_schema(data) and check_nulls(data)

# Stage resolved file
git add scripts/validate_data.py

# Complete merge
git commit -m "Merge feature/data-validation with conflict resolution"

# Abort merge if needed
git merge --abort
```

### 5. How do you work with remote repositories?
**Answer**: Remote repositories enable collaboration and backup of code.

```bash
# Add remote repository
git remote add origin https://github.com/company/data-pipeline.git

# View remotes
git remote -v

# Push to remote
git push origin main
git push -u origin main    # Set upstream tracking

# Pull from remote
git pull origin main       # Fetch and merge
git fetch origin          # Fetch without merging
git merge origin/main      # Merge fetched changes

# Clone repository
git clone https://github.com/company/data-pipeline.git
cd data-pipeline

# Work with multiple remotes
git remote add upstream https://github.com/original/data-pipeline.git
git fetch upstream
git merge upstream/main

# Push tags
git tag v1.0.0
git push origin v1.0.0
git push origin --tags    # Push all tags
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you manage data engineering projects with Git?
**Answer**: Use proper repository structure, branching strategies, and workflow automation.

```bash
# Repository structure for data projects
data-engineering-project/
├── .gitignore
├── README.md
├── requirements.txt
├── config/
│   ├── dev.yaml
│   ├── staging.yaml
│   └── prod.yaml
├── src/
│   ├── etl/
│   ├── transformations/
│   └── utils/
├── sql/
│   ├── ddl/
│   ├── dml/
│   └── queries/
├── tests/
├── docs/
├── scripts/
└── docker/

# .gitignore for data projects
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.pytest_cache/

# Data files
*.csv
*.parquet
*.json
data/
logs/
*.log

# Environment
.env
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Credentials
credentials.json
*.key
*.pem
```

**Git Flow for Data Projects**:
```bash
# Feature development
git checkout -b feature/spark-optimization
# Develop feature
git add .
git commit -m "Optimize Spark job memory usage"
git push origin feature/spark-optimization

# Hotfix workflow
git checkout -b hotfix/fix-data-corruption main
# Fix critical issue
git add .
git commit -m "Fix data corruption in ETL pipeline"
git push origin hotfix/fix-data-corruption

# Release workflow
git checkout -b release/v2.1.0 develop
# Prepare release
git add .
git commit -m "Prepare release v2.1.0"
git checkout main
git merge release/v2.1.0
git tag v2.1.0
git push origin main --tags
```

### 7. How do you handle large files and data in Git?
**Answer**: Use Git LFS (Large File Storage) and proper data management strategies.

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.parquet"
git lfs track "*.csv"
git lfs track "data/**"
git lfs track "models/*.pkl"

# Add .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS for large files"

# Add large file
git add data/large_dataset.parquet
git commit -m "Add large dataset"
git push origin main

# Clone with LFS
git lfs clone https://github.com/company/data-project.git

# Check LFS status
git lfs ls-files
git lfs status

# Pull LFS files
git lfs pull

# Alternative: Use data versioning tools
# DVC (Data Version Control)
pip install dvc
dvc init
dvc add data/large_dataset.csv
git add data/large_dataset.csv.dvc .gitignore
git commit -m "Add dataset with DVC"

# Push data to remote storage
dvc remote add -d storage s3://my-bucket/data
dvc push
```

### 8. How do you implement CI/CD with Git for data pipelines?
**Answer**: Use Git hooks, GitHub Actions, or similar tools for automated testing and deployment.

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
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src/ --cov-report=xml
    
    - name: Lint code
      run: |
        flake8 src/
        black --check src/
    
    - name: Validate SQL
      run: |
        sqlfluff lint sql/
    
    - name: Test data quality
      run: |
        python scripts/data_quality_tests.py

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to staging
      run: |
        # Deploy pipeline to staging environment
        ./scripts/deploy.sh staging
    
    - name: Run integration tests
      run: |
        python tests/integration_tests.py
    
    - name: Deploy to production
      if: success()
      run: |
        ./scripts/deploy.sh production
```

**Pre-commit Hooks**:
```bash
# Install pre-commit
pip install pre-commit

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8

  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 1.0.0
    hooks:
      - id: sqlfluff-lint

  - repo: local
    hooks:
      - id: data-validation
        name: Data Validation
        entry: python scripts/validate_data.py
        language: system
        files: ^data/

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### 9. How do you manage configuration and secrets in Git?
**Answer**: Use environment-specific configurations and secure secret management.

```bash
# Environment-specific configuration
# config/base.yaml
database:
  host: localhost
  port: 5432
  name: datawarehouse

spark:
  master: local[*]
  executor_memory: 2g

# config/dev.yaml
database:
  host: dev-db.company.com
  name: datawarehouse_dev

# config/prod.yaml
database:
  host: prod-db.company.com
  name: datawarehouse_prod

spark:
  master: spark://prod-cluster:7077
  executor_memory: 8g
```

**Secret Management**:
```bash
# Use environment variables
export DATABASE_PASSWORD="secret_password"
export API_KEY="api_key_value"

# .env file (not committed)
DATABASE_PASSWORD=secret_password
API_KEY=api_key_value
SPARK_MASTER=spark://cluster:7077

# Load in application
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
API_KEY = os.getenv('API_KEY')

# Git-crypt for encrypted files
git-crypt init
git-crypt add-gpg-user user@company.com
echo "secrets/* filter=git-crypt diff=git-crypt" >> .gitattributes
git add .gitattributes
git commit -m "Configure git-crypt"

# Add encrypted file
echo "api_key: secret123" > secrets/api_keys.yaml
git add secrets/api_keys.yaml
git commit -m "Add encrypted API keys"
```

### 10. How do you troubleshoot Git issues in data projects?
**Answer**: Use Git diagnostic tools and recovery techniques.

```bash
# Check repository health
git fsck
git gc --aggressive

# Find lost commits
git reflog
git show HEAD@{2}

# Recover deleted branch
git reflog
git checkout -b recovered-branch HEAD@{5}

# Find when bug was introduced
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
# Git will checkout commits for testing
# Mark each as good or bad
git bisect good  # or git bisect bad
# Continue until bug is found
git bisect reset

# Blame for line-by-line history
git blame src/etl/transform.py
git log -p src/etl/transform.py  # Show changes to file

# Search commit history
git log --grep="fix"
git log -S "function_name"  # Search for code changes
git log --author="John" --since="2024-01-01"

# Stash work in progress
git stash
git stash list
git stash apply stash@{0}
git stash drop stash@{0}
git stash pop  # Apply and drop

# Cherry-pick commits
git cherry-pick abc123def
git cherry-pick --no-commit abc123def  # Don't auto-commit

# Rewrite history (use carefully)
git rebase -i HEAD~3  # Interactive rebase last 3 commits
git commit --amend    # Modify last commit
git filter-branch --tree-filter 'rm -f passwords.txt' HEAD  # Remove file from history

# Resolve submodule issues
git submodule update --init --recursive
git submodule foreach git pull origin main
```

**Data Pipeline Recovery Scenarios**:
```bash
# Scenario 1: Accidentally committed large data file
git rm --cached large_file.csv
echo "large_file.csv" >> .gitignore
git add .gitignore
git commit -m "Remove large file and add to gitignore"

# Scenario 2: Need to revert pipeline deployment
git log --oneline
git revert abc123def  # Revert specific commit
git revert HEAD~3..HEAD  # Revert range of commits

# Scenario 3: Merge conflicts in configuration
git status
git diff
# Edit conflicted files
git add .
git commit -m "Resolve configuration conflicts"

# Scenario 4: Lost work due to hard reset
git reflog
git reset --hard HEAD@{2}  # Restore to previous state
```

This comprehensive set covers Git fundamentals through advanced repository management and troubleshooting with practical data engineering examples.