# Version Control Key Concepts for Data Engineering

## 1. Git Fundamentals
**What it is**: Distributed version control system for tracking changes in source code and managing collaborative development.

**Why important**: Essential for data engineering teams to track changes in data pipelines, collaborate on code, manage releases, and maintain code history for debugging and rollbacks.

**When to use**:
- All data pipeline code development
- Configuration management
- Documentation versioning
- Collaborative development workflows
- Release management and deployment

**Basic Git Operations**:
```bash
# Repository initialization
git init
git clone https://github.com/company/data-pipeline.git

# Basic workflow
git add .                    # Stage changes
git commit -m "Add ETL pipeline for customer data"
git push origin main         # Push to remote

# Branching
git branch feature/new-pipeline
git checkout feature/new-pipeline
git checkout -b feature/data-quality-checks  # Create and switch

# Merging
git checkout main
git merge feature/new-pipeline

# Status and history
git status
git log --oneline
git diff HEAD~1              # Compare with previous commit
```

**Data Engineering Git Structure**:
```
data-platform/
├── .gitignore
├── README.md
├── requirements.txt
├── src/
│   ├── pipelines/
│   │   ├── etl/
│   │   │   ├── customer_pipeline.py
│   │   │   └── product_pipeline.py
│   │   └── streaming/
│   │       └── real_time_processor.py
│   ├── utils/
│   │   ├── data_quality.py
│   │   └── database_utils.py
│   └── config/
│       ├── dev.yaml
│       ├── staging.yaml
│       └── prod.yaml
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   ├── architecture.md
│   └── deployment.md
├── infrastructure/
│   ├── terraform/
│   └── kubernetes/
└── scripts/
    ├── deploy.sh
    └── setup.sh
```

## 2. Branching Strategies for Data Engineering
**What it is**: Systematic approaches to organizing branches for different development workflows and environments.

**Why important**: Data pipelines often require careful coordination between development, testing, and production environments. Proper branching strategies ensure safe deployments and enable parallel development.

**When to use**:
- Multi-environment deployments (dev/staging/prod)
- Feature development with multiple developers
- Hotfix deployments to production
- Release management for data platform updates

**GitFlow for Data Pipelines**:
```bash
# Main branches
main          # Production-ready code
develop       # Integration branch for features

# Supporting branches
feature/*     # New pipeline features
release/*     # Prepare for production release
hotfix/*      # Critical production fixes

# Example workflow
git checkout develop
git checkout -b feature/customer-segmentation-pipeline

# Develop feature
git add .
git commit -m "Implement customer segmentation logic"
git push origin feature/customer-segmentation-pipeline

# Create pull request to develop
# After review and merge to develop

# Create release branch
git checkout develop
git checkout -b release/v1.2.0
git push origin release/v1.2.0

# After testing, merge to main and develop
git checkout main
git merge release/v1.2.0
git tag v1.2.0
git push origin main --tags

git checkout develop
git merge release/v1.2.0
git push origin develop
```

**Environment-based Branching**:
```bash
# Branch structure for data engineering
main          # Production environment
staging       # Staging environment  
develop       # Development environment

# Deployment workflow
git checkout develop
# Develop and test features

git checkout staging
git merge develop
# Deploy to staging for integration testing

git checkout main
git merge staging
# Deploy to production after validation
```

## 3. Data-Specific Version Control Practices
**What it is**: Specialized version control practices for managing data schemas, configurations, and pipeline definitions.

**Why important**: Data engineering involves more than just code - schemas, configurations, and data definitions need versioning to ensure consistency across environments and enable rollbacks.

**When to use**:
- Database schema changes
- Configuration management across environments
- Data pipeline definitions
- Infrastructure as Code (IaC)

**Schema Version Control**:
```sql
-- migrations/001_create_customer_table.sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- migrations/002_add_customer_segment.sql
ALTER TABLE customers 
ADD COLUMN segment VARCHAR(50) DEFAULT 'standard';

-- migrations/003_create_orders_table.sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Configuration Management**:
```yaml
# config/base.yaml
database:
  host: ${DB_HOST}
  port: ${DB_PORT}
  name: ${DB_NAME}

spark:
  app_name: "DataPipeline"
  executor_memory: "2g"
  executor_cores: 2

# config/dev.yaml
database:
  host: "dev-db.company.com"
  port: 5432
  name: "dev_datawarehouse"

spark:
  executor_memory: "1g"
  executor_cores: 1

# config/prod.yaml  
database:
  host: "prod-db.company.com"
  port: 5432
  name: "prod_datawarehouse"

spark:
  executor_memory: "4g"
  executor_cores: 4
```

**Pipeline Definition Versioning**:
```python
# pipelines/customer_etl_v1.py
class CustomerETLPipelineV1:
    """Version 1 of customer ETL pipeline."""
    
    def __init__(self, config):
        self.config = config
        self.version = "1.0.0"
    
    def extract(self):
        """Extract customer data from source systems."""
        return self.read_from_database("SELECT * FROM raw_customers")
    
    def transform(self, data):
        """Basic transformation logic."""
        return data.dropna().drop_duplicates()
    
    def load(self, data):
        """Load to data warehouse."""
        data.to_sql('customers', self.warehouse_connection)

# pipelines/customer_etl_v2.py
class CustomerETLPipelineV2:
    """Version 2 with enhanced data quality checks."""
    
    def __init__(self, config):
        self.config = config
        self.version = "2.0.0"
    
    def extract(self):
        """Enhanced extraction with error handling."""
        try:
            return self.read_from_database("SELECT * FROM raw_customers")
        except Exception as e:
            self.log_error(f"Extraction failed: {e}")
            return self.read_from_backup_source()
    
    def transform(self, data):
        """Enhanced transformation with quality checks."""
        # Data quality validation
        if self.validate_data_quality(data):
            cleaned_data = data.dropna().drop_duplicates()
            return self.apply_business_rules(cleaned_data)
        else:
            raise ValueError("Data quality validation failed")
    
    def load(self, data):
        """Load with upsert logic."""
        self.upsert_to_warehouse(data, 'customers', ['id'])
```

## 4. Collaborative Development Workflows
**What it is**: Structured approaches for multiple developers to work together on data engineering projects.

**Why important**: Data engineering teams need to coordinate changes to shared pipelines, avoid conflicts, and ensure code quality through reviews and testing.

**When to use**:
- Team-based development
- Code review processes
- Continuous integration/deployment
- Knowledge sharing and documentation

**Pull Request Workflow**:
```bash
# Developer workflow
git checkout main
git pull origin main
git checkout -b feature/improve-data-validation

# Make changes
git add src/utils/data_quality.py
git commit -m "Add comprehensive data validation rules

- Implement null value checks
- Add data type validation  
- Include range validation for numeric fields
- Add email format validation"

git push origin feature/improve-data-validation

# Create pull request with description:
# Title: Improve data validation in ETL pipelines
# Description: 
# - Added comprehensive validation rules
# - Includes unit tests for all validation functions
# - Updated documentation with validation examples
# - Fixes issue #123
```

**Code Review Best Practices**:
```python
# Example of well-documented code for review
class DataQualityValidator:
    """
    Validates data quality for incoming datasets.
    
    This class provides comprehensive data validation including:
    - Schema validation
    - Null value checks
    - Data type validation
    - Business rule validation
    
    Example:
        validator = DataQualityValidator(schema_config)
        is_valid, errors = validator.validate(dataframe)
        if not is_valid:
            handle_validation_errors(errors)
    """
    
    def __init__(self, schema_config: Dict[str, Any]):
        """
        Initialize validator with schema configuration.
        
        Args:
            schema_config: Dictionary containing validation rules
                          Format: {
                              'column_name': {
                                  'type': 'string|integer|float|date',
                                  'nullable': True|False,
                                  'min_value': numeric_value,
                                  'max_value': numeric_value,
                                  'pattern': 'regex_pattern'
                              }
                          }
        """
        self.schema_config = schema_config
        self.validation_errors = []
    
    def validate(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate dataframe against schema configuration.
        
        Args:
            df: Pandas DataFrame to validate
            
        Returns:
            Tuple of (is_valid: bool, errors: List[str])
            
        Raises:
            ValueError: If schema_config is invalid
        """
        self.validation_errors = []
        
        # Schema validation
        self._validate_schema(df)
        
        # Data type validation
        self._validate_data_types(df)
        
        # Business rule validation
        self._validate_business_rules(df)
        
        return len(self.validation_errors) == 0, self.validation_errors
```

## 5. Release Management and Deployment
**What it is**: Systematic approach to managing releases of data pipeline code and coordinating deployments across environments.

**Why important**: Data pipelines often have dependencies and require coordinated deployments. Proper release management ensures smooth deployments and enables quick rollbacks if issues occur.

**When to use**:
- Production deployments
- Coordinated releases across multiple pipelines
- Rollback scenarios
- Environment synchronization

**Semantic Versioning for Data Pipelines**:
```bash
# Version format: MAJOR.MINOR.PATCH
# MAJOR: Breaking changes (schema changes, API changes)
# MINOR: New features (new pipelines, enhanced functionality)  
# PATCH: Bug fixes (data quality fixes, performance improvements)

v1.0.0  # Initial release
v1.0.1  # Bug fix: Fixed null handling in customer pipeline
v1.1.0  # New feature: Added product recommendation pipeline
v2.0.0  # Breaking change: Updated database schema

# Tagging releases
git tag -a v1.2.0 -m "Release v1.2.0: Add real-time streaming pipeline"
git push origin v1.2.0
```

**Release Pipeline with CI/CD**:
```yaml
# .github/workflows/release.yml
name: Release Pipeline

on:
  push:
    tags:
      - 'v*'

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
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src
        
    - name: Run data quality tests
      run: |
        python -m great_expectations checkpoint run data_quality_checkpoint

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - name: Deploy to staging
      run: |
        # Deploy pipeline code
        kubectl apply -f k8s/staging/
        
        # Run database migrations
        python scripts/migrate.py --env staging
        
        # Smoke tests
        python scripts/smoke_tests.py --env staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
    - name: Deploy to production
      run: |
        # Blue-green deployment
        kubectl apply -f k8s/production/
        
        # Database migrations with rollback capability
        python scripts/migrate.py --env production --backup
        
        # Comprehensive testing
        python scripts/integration_tests.py --env production
        
        # Switch traffic to new version
        kubectl patch service data-pipeline -p '{"spec":{"selector":{"version":"green"}}}'
```

**Rollback Strategy**:
```bash
# Automated rollback script
#!/bin/bash
# rollback.sh

PREVIOUS_VERSION=$1
ENVIRONMENT=$2

if [ -z "$PREVIOUS_VERSION" ] || [ -z "$ENVIRONMENT" ]; then
    echo "Usage: ./rollback.sh <version> <environment>"
    exit 1
fi

echo "Rolling back to version $PREVIOUS_VERSION in $ENVIRONMENT"

# Rollback application code
kubectl set image deployment/data-pipeline app=data-pipeline:$PREVIOUS_VERSION

# Rollback database if needed
python scripts/migrate.py --env $ENVIRONMENT --rollback-to $PREVIOUS_VERSION

# Verify rollback
python scripts/health_check.py --env $ENVIRONMENT

echo "Rollback completed"
```

**Environment Synchronization**:
```python
# scripts/sync_environments.py
import subprocess
import yaml
from typing import Dict, List

class EnvironmentSync:
    def __init__(self, source_env: str, target_env: str):
        self.source_env = source_env
        self.target_env = target_env
    
    def sync_database_schema(self):
        """Sync database schema between environments."""
        # Export schema from source
        subprocess.run([
            'pg_dump', '--schema-only', 
            f'--host={self.get_db_host(self.source_env)}',
            f'--dbname={self.get_db_name(self.source_env)}',
            '--file=schema_export.sql'
        ])
        
        # Apply to target
        subprocess.run([
            'psql',
            f'--host={self.get_db_host(self.target_env)}',
            f'--dbname={self.get_db_name(self.target_env)}',
            '--file=schema_export.sql'
        ])
    
    def sync_configuration(self):
        """Sync configuration files between environments."""
        source_config = self.load_config(self.source_env)
        target_config = self.load_config(self.target_env)
        
        # Merge configurations (keeping environment-specific values)
        merged_config = self.merge_configs(source_config, target_config)
        
        # Save updated target configuration
        self.save_config(self.target_env, merged_config)
    
    def sync_pipeline_definitions(self):
        """Sync pipeline definitions and ensure compatibility."""
        # Copy pipeline files
        subprocess.run([
            'rsync', '-av', 
            f'src/pipelines/',
            f'{self.target_env}-deployment:/app/src/pipelines/'
        ])
        
        # Validate pipeline compatibility
        self.validate_pipeline_compatibility()
    
    def get_db_host(self, env: str) -> str:
        config = self.load_config(env)
        return config['database']['host']
    
    def get_db_name(self, env: str) -> str:
        config = self.load_config(env)
        return config['database']['name']
    
    def load_config(self, env: str) -> Dict:
        with open(f'config/{env}.yaml', 'r') as f:
            return yaml.safe_load(f)
    
    def save_config(self, env: str, config: Dict):
        with open(f'config/{env}.yaml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

# Usage
sync = EnvironmentSync('staging', 'production')
sync.sync_database_schema()
sync.sync_configuration()
sync.sync_pipeline_definitions()
```

These version control concepts provide the foundation for managing data engineering projects effectively, ensuring code quality, enabling collaboration, and supporting reliable deployments across different environments.