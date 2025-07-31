# Git Best Practices for Data Engineering

## Repository Structure

### Project Organization
```
data-pipeline/
├── .gitignore
├── README.md
├── requirements.txt
├── src/
│   ├── etl/
│   ├── models/
│   └── utils/
├── tests/
├── config/
├── scripts/
├── docs/
└── .github/
    └── workflows/
```

### .gitignore for Data Projects
```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Data files
*.csv
*.parquet
*.json
data/
datasets/
*.db
*.sqlite

# Jupyter Notebooks
.ipynb_checkpoints/
*.ipynb

# Environment files
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
```

## Branching Strategy

### GitFlow for Data Projects
```bash
# Main branches
git checkout -b develop
git checkout -b feature/customer-etl
git checkout -b hotfix/data-quality-fix

# Feature development
git checkout develop
git pull origin develop
git checkout -b feature/new-data-source
# Work on feature
git add .
git commit -m "feat: add new data source integration"
git push origin feature/new-data-source

# Create pull request, then merge
git checkout develop
git pull origin develop
git branch -d feature/new-data-source
```

### Commit Message Convention
```bash
# Format: type(scope): description
git commit -m "feat(etl): add customer data transformation"
git commit -m "fix(pipeline): resolve memory leak in spark job"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(etl): add unit tests for data validation"
git commit -m "refactor(models): optimize SQL queries"

# Types: feat, fix, docs, style, refactor, test, chore
```

## Data Pipeline Versioning

### Configuration Management
```yaml
# config/pipeline_config.yaml
version: "1.2.0"
pipeline:
  name: "customer_etl"
  source:
    type: "postgresql"
    connection: "prod_db"
  destination:
    type: "s3"
    bucket: "data-lake-prod"
  transformations:
    - name: "clean_customer_data"
      version: "1.1.0"
    - name: "enrich_customer_data"
      version: "1.0.0"
```

### Schema Evolution
```python
# src/models/customer_schema.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CustomerSchemaV1:
    customer_id: int
    name: str
    email: str

@dataclass
class CustomerSchemaV2:
    customer_id: int
    name: str
    email: str
    phone: Optional[str] = None  # New field
    
# Migration script
def migrate_v1_to_v2(data_v1):
    return CustomerSchemaV2(
        customer_id=data_v1.customer_id,
        name=data_v1.name,
        email=data_v1.email,
        phone=None
    )
```

## Code Review Process

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Data Impact
- [ ] Schema changes
- [ ] New data sources
- [ ] Performance impact
- [ ] Data quality impact

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Data validation tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data in commit
```

### Review Guidelines
```bash
# Check for sensitive data
git log --all --full-history -- "*.env"
git log --all --full-history -S "password"

# Review data changes
git diff --name-only HEAD~1 HEAD | grep -E "\.(sql|py|yaml)$"

# Check file sizes
git ls-files | xargs ls -la | awk '{if($5 > 1000000) print $9, $5}'
```

## CI/CD Integration

### GitHub Actions Workflow
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
        
    - name: Data quality checks
      run: |
        python scripts/validate_schemas.py
        python scripts/check_data_quality.py
        
  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        # Deploy pipeline
        echo "Deploying to production"
```

## Security Best Practices

### Secrets Management
```bash
# Never commit secrets
echo "API_KEY=secret123" >> .env
echo ".env" >> .gitignore

# Use environment variables
export DATABASE_URL="postgresql://user:pass@host:5432/db"

# Remove secrets from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch config/secrets.yaml' \
  --prune-empty --tag-name-filter cat -- --all
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key
      
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
      
  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8
```

## Collaboration Workflows

### Feature Development
```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/add-kafka-integration

# Regular commits during development
git add src/kafka_consumer.py
git commit -m "feat(kafka): add basic consumer implementation"

git add tests/test_kafka_consumer.py
git commit -m "test(kafka): add consumer unit tests"

# Push and create PR
git push origin feature/add-kafka-integration
```

### Hotfix Process
```bash
# Critical production fix
git checkout main
git pull origin main
git checkout -b hotfix/fix-data-corruption

# Make fix
git add src/etl/data_cleaner.py
git commit -m "fix(etl): prevent data corruption in date parsing"

# Deploy hotfix
git checkout main
git merge hotfix/fix-data-corruption
git tag v1.2.1
git push origin main --tags

# Merge back to develop
git checkout develop
git merge main
git push origin develop
```

## Monitoring and Maintenance

### Repository Health
```bash
# Check repository size
git count-objects -vH

# Find large files
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort --numeric-sort --key=2 | \
  tail -10

# Clean up
git gc --aggressive --prune=now
```

### Branch Management
```bash
# List merged branches
git branch --merged main

# Delete merged branches
git branch --merged main | grep -v "main\|develop" | xargs -n 1 git branch -d

# Prune remote branches
git remote prune origin
```