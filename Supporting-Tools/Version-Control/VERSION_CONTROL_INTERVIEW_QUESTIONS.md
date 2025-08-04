# Version Control Interview Questions

## Basic Level (0-2 years)

### 1. What is Git and why is it important for data engineering?
**Answer:**
Git is a distributed version control system that tracks changes in files and coordinates work among multiple developers.

**Importance for Data Engineering:**
- Track changes in data pipeline code
- Collaborate on data processing scripts
- Manage configuration files across environments
- Enable rollbacks when pipeline issues occur
- Maintain history of schema changes

### 2. Explain the difference between git merge and git rebase.
**Answer:**
- **Git Merge**: Creates a merge commit that combines two branches
  - Preserves branch history
  - Non-destructive operation
  - Creates a merge commit with two parents

- **Git Rebase**: Replays commits from one branch onto another
  - Creates linear history
  - Rewrites commit history
  - No merge commits

```bash
# Merge example
git checkout main
git merge feature-branch

# Rebase example  
git checkout feature-branch
git rebase main
```

### 3. How do you handle merge conflicts in data pipeline code?
**Answer:**
```bash
# When conflict occurs
git status  # Shows conflicted files

# Edit conflicted files, look for conflict markers:
<<<<<<< HEAD
current_code = "production version"
=======
current_code = "feature version"  
>>>>>>> feature-branch

# Resolve conflicts, then:
git add resolved_file.py
git commit -m "Resolve merge conflict in data pipeline"
```

## Intermediate Level (2-5 years)

### 4. How would you structure a Git repository for a data engineering project?
**Answer:**
```
data-platform/
├── src/
│   ├── pipelines/
│   ├── utils/
│   └── config/
├── tests/
├── infrastructure/
├── docs/
├── scripts/
├── .gitignore
├── requirements.txt
└── README.md
```

### 5. Explain GitFlow workflow for data engineering teams.
**Answer:**
GitFlow uses multiple branch types:
- **main**: Production-ready code
- **develop**: Integration branch
- **feature/***: New features
- **release/***: Prepare releases
- **hotfix/***: Critical fixes

```bash
# Feature development
git checkout develop
git checkout -b feature/new-etl-pipeline
# Develop feature
git checkout develop
git merge feature/new-etl-pipeline

# Release process
git checkout -b release/v1.2.0
# Test and fix
git checkout main
git merge release/v1.2.0
git tag v1.2.0
```

## Advanced Level (5+ years)

### 6. How do you manage database schema changes with version control?
**Answer:**
Use migration scripts with version control:

```sql
-- migrations/001_create_customers.sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- migrations/002_add_email_column.sql
ALTER TABLE customers ADD COLUMN email VARCHAR(255);
```

```python
# Migration management script
class MigrationManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.create_migration_table()
    
    def run_migrations(self):
        applied_migrations = self.get_applied_migrations()
        migration_files = self.get_migration_files()
        
        for migration_file in migration_files:
            if migration_file not in applied_migrations:
                self.apply_migration(migration_file)
```